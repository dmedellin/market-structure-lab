#!/usr/bin/env python3
"""Machine-checkable form of the market-structure-lab site invariants.

Standard library only. Run from the repository root:

    python3 -m unittest discover -s tests -v

These tests assert against the files on disk, before any image is built. They are
the pre-build half of the acceptance evidence; scripts/smoke.py asserts the same
invariants against the SERVED response after the container is running. The
self-containment scanner is imported from scripts/smoke.py on purpose, so the
on-disk verdict and the served verdict can never drift apart.

What is deliberately strict here:
  * Self-containment is about LOADS. An external <a href> navigates and fetches
    nothing, so it is not a violation; an external script/style/icon/font/image/
    iframe/@import/url()/fetch/XHR is.
  * The published layout is checked against the canonical URLs, because
    Containerfile.release publishes site/ as the document root of
    https://learn.geterdone.io/ . An extra directory level silently changes every
    public URL.
"""

import json
import os
import re
import sys
import unittest
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_ROOT = Path(os.environ.get("SITE_ROOT") or (REPO_ROOT / "site")).resolve()
CANONICAL_ORIGIN = "https://learn.geterdone.io"
CANONICAL_HOST = "learn.geterdone.io"

# The published URL space is two levels deep: the site index is a catalog of
# COURSES, each course has a home page, and each course's lessons live under it.
#
#     /                                   catalog of courses
#     /market-structure-lab/              course home (lists its seven labs)
#     /market-structure-lab/<lesson>/     the seven labs, in course order
#
# The document root must publish exactly these nine URLs and nothing else.
# Containerfile.release, .github/workflows/{ci,pages}.yml, release/contract.json
# (acceptance.checks) and scripts/smoke.py all assert the same mapping; changing
# one without the others is how a lesson silently stops being published.
#
# The seven FLAT URLs this course used to publish (/market-structure/ and its six
# siblings) are deliberately gone. Breaking them was an accepted decision, there
# are no redirect stubs, and they must not be re-added here: a path listed below
# is a path that must exist.
COURSE_HOME = "/market-structure-lab/"

UNKNOWN_PATH_CHECK = "/release-smoke-unknown-path"

REQUIRED_PAGES = {
    "/": "index.html",
    COURSE_HOME: "market-structure-lab/index.html",
    "/market-structure-lab/market-structure/": "market-structure-lab/market-structure/index.html",
    "/market-structure-lab/ranges-breakouts-liquidity/": "market-structure-lab/ranges-breakouts-liquidity/index.html",
    "/market-structure-lab/multi-timeframe-market-structure/": "market-structure-lab/multi-timeframe-market-structure/index.html",
    "/market-structure-lab/pullbacks-entry-models/": "market-structure-lab/pullbacks-entry-models/index.html",
    "/market-structure-lab/invalidation-stops-risk-reward/": "market-structure-lab/invalidation-stops-risk-reward/index.html",
    "/market-structure-lab/volume-relative-strength/": "market-structure-lab/volume-relative-strength/index.html",
    "/market-structure-lab/options-contract-selection/": "market-structure-lab/options-contract-selection/index.html",
}

# "/" is the catalog of courses; every other published URL is course material --
# the course home and its seven labs. All of it teaches trading, so all of it
# carries the same disclaimer. There is no exempt page below the catalog root.
COURSE_PAGES = {url: rel for url, rel in REQUIRED_PAGES.items() if url != "/"}

# The seven labs alone, without the course home.
LESSON_PAGES = {url: rel for url, rel in COURSE_PAGES.items() if url != COURSE_HOME}

# Every course page (any page below the catalog root) must keep this disclaimer.
DISCLAIMER_RE = re.compile(r"(?i)educational use only")

SECRET_PATTERNS = [
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JSON Web Token", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("Authorization header value", re.compile(r"(?i)authorization\s*[:=]\s*['\"]?(?:bearer|basic)\s+\S{8,}")),
    (
        "assigned credential literal",
        re.compile(
            r"(?i)\b(?:api[_-]?key|secret|secret[_-]?key|password|passwd|access[_-]?token"
            r"|auth[_-]?token|client[_-]?secret|private[_-]?key)\b\s*[:=]\s*['\"][^'\"]{12,}['\"]"
        ),
    ),
    ("connection string with credentials", re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s/@'\"]+:[^\s/@'\"]+@")),
]

try:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from smoke import scan_self_containment
except ImportError as exc:  # pragma: no cover - a missing smoke client is itself a failure
    raise SystemExit(
        "cannot import the self-containment scanner from scripts/smoke.py: %s" % exc
    )


class Document(HTMLParser):
    """Everything the invariants need to know about one HTML file."""

    URL_ATTRS = {
        "href", "src", "srcset", "imagesrcset", "action", "formaction",
        "poster", "data", "background", "ping", "xlink:href",
    }

    def __init__(self, path, text):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.text = text
        self.title = None
        self.description = None
        self.canonical = None
        self.lang = None
        self.ids = set()
        self.urls = []  # (tag, attr, value, line)
        self.has_base = False
        self._in_title = False
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        attrd = {}
        for name, value in attrs:
            attrd.setdefault(name.lower(), value)

        if tag == "html":
            self.lang = attrd.get("lang")
        if tag == "base":
            self.has_base = True
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            name = (attrd.get("name") or "").lower()
            if name == "description" and attrd.get("content"):
                self.description = attrd["content"].strip()
        if tag == "link":
            rel = (attrd.get("rel") or "").lower().split()
            if "canonical" in rel:
                self.canonical = (attrd.get("href") or "").strip()

        if attrd.get("id"):
            self.ids.add(attrd["id"])
        if attrd.get("name") and tag == "a":
            self.ids.add(attrd["name"])

        for attr, value in attrd.items():
            if attr in self.URL_ATTRS and value:
                if attr in ("srcset", "imagesrcset"):
                    for candidate in value.split(","):
                        url = candidate.strip().split(" ", 1)[0]
                        if url:
                            self.urls.append((tag, attr, url, line))
                else:
                    self.urls.append((tag, attr, value.strip(), line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data


def html_files():
    return sorted(p for p in SITE_ROOT.rglob("*.html") if p.is_file())


def served_path(path):
    """Public URL path a file is published at, given SITE_ROOT is the document root."""
    rel = path.relative_to(SITE_ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


class SiteFixture(unittest.TestCase):
    documents = None

    @classmethod
    def setUpClass(cls):
        if not SITE_ROOT.is_dir():
            raise unittest.SkipTest("no site directory at %s" % SITE_ROOT)
        cls.documents = [
            Document(path, path.read_text(encoding="utf-8")) for path in html_files()
        ]


class TestPublishedLayout(SiteFixture):
    def test_site_root_contains_pages(self):
        self.assertTrue(self.documents, "no HTML files found under %s" % SITE_ROOT)

    def test_required_pages_exist_at_their_published_paths(self):
        for url, relative in sorted(REQUIRED_PAGES.items()):
            with self.subTest(url=url):
                target = SITE_ROOT / relative
                self.assertTrue(
                    target.is_file(),
                    "%s must be served from %s, but that file does not exist. "
                    "Containerfile.release publishes site/ as the document root of %s, "
                    "so an extra directory level changes the public URL."
                    % (url, target, CANONICAL_ORIGIN),
                )

    def test_no_page_is_published_outside_the_declared_url_space(self):
        published = {served_path(doc.path) for doc in self.documents}
        unexpected = published - set(REQUIRED_PAGES)
        self.assertEqual(
            set(),
            unexpected,
            "pages published at undeclared URLs: %s. The public URL space is a "
            "contract (registry domains, canonical tags, and the acceptance checks "
            "in release/contract.example.json all name it). When a lesson is added "
            "on purpose, add its URL to REQUIRED_PAGES here and to the acceptance "
            "checks; do not delete this test." % sorted(unexpected),
        )


class TestDeclaredUrlSpaceAgrees(unittest.TestCase):
    """The published URL map is declared in several places. Drift is the failure.

    REQUIRED_PAGES above is the on-disk declaration. scripts/smoke.py declares the
    same map for the SERVED responses and release/contract.json declares it as the
    acceptance matrix. A page added to one and not the others is a live page that
    nothing probes, which is exactly the hole these tests exist to close. The
    course home counts: it is published, so it is probed.
    """

    def test_declared_url_space_is_the_two_level_course_tree(self):
        """Catalog, then one course home, then that course's lessons under it.

        Nine URLs exactly: /, /market-structure-lab/, and seven labs beneath it.
        The flat /<lesson>/ URLs were retired without redirects, so a two-segment
        lesson path is the only shape a lesson may have; re-adding a one-segment
        lesson here would declare a page that no longer exists on disk.
        """
        self.assertEqual(
            9, len(REQUIRED_PAGES), "expected 9 published URLs, got %d" % len(REQUIRED_PAGES)
        )
        self.assertIn(COURSE_HOME, REQUIRED_PAGES, "the course home must be published")
        self.assertEqual(
            7, len(LESSON_PAGES), "the course is seven labs, got %d" % len(LESSON_PAGES)
        )
        for url, relative in sorted(REQUIRED_PAGES.items()):
            with self.subTest(url=url):
                self.assertTrue(url.startswith("/") and url.endswith("/"),
                                "a published URL is a directory URL")
                self.assertEqual(url.lstrip("/"), relative[: -len("index.html")],
                                 "URL and source file disagree")
        for url in sorted(LESSON_PAGES):
            with self.subTest(url=url):
                self.assertTrue(
                    url.startswith(COURSE_HOME),
                    "a lesson lives under its course home %s, got %s" % (COURSE_HOME, url),
                )
                self.assertEqual(
                    2,
                    url.strip("/").count("/") + 1,
                    "a lesson URL is exactly <course>/<lesson>/, got %s" % url,
                )

    def test_smoke_client_probes_every_published_page(self):
        from smoke import parse_args, published_paths

        args = parse_args([CANONICAL_ORIGIN])
        probed = set(published_paths(args))
        self.assertEqual(
            set(REQUIRED_PAGES),
            probed,
            "scripts/smoke.py probes a different URL set than this suite declares "
            "(only in smoke: %s; only here: %s). A production smoke run would leave "
            "a published page unchecked."
            % (sorted(probed - set(REQUIRED_PAGES)), sorted(set(REQUIRED_PAGES) - probed)),
        )

    def test_release_contract_accepts_every_published_page(self):
        for name in ("contract.json", "contract.example.json"):
            path = REPO_ROOT / "release" / name
            with self.subTest(contract=name):
                if not path.is_file():
                    self.skipTest("no release/%s in this checkout" % name)
                document = json.loads(path.read_text(encoding="utf-8"))
                checked = {
                    check["path"]
                    for check in document["acceptance"]["checks"]
                    if check.get("scope") == "public"
                }
                missing = sorted(set(REQUIRED_PAGES) - checked)
                self.assertEqual(
                    [],
                    missing,
                    "release/%s declares no public acceptance check for %s; a release "
                    "would be accepted without ever fetching those pages" % (name, missing),
                )
                # Bidirectional on purpose: a one-way check would let a retired
                # URL linger in the contract forever, quietly asserting a page
                # that is no longer published.
                stale = sorted(checked - set(REQUIRED_PAGES) - {UNKNOWN_PATH_CHECK})
                self.assertEqual(
                    [],
                    stale,
                    "release/%s declares public acceptance checks for %s, which the "
                    "site does not publish; the contract has drifted from the tree"
                    % (name, stale),
                )


class TestSelfContainment(SiteFixture):
    def test_pages_reference_no_external_origin(self):
        for doc in self.documents:
            with self.subTest(page=str(doc.path.relative_to(REPO_ROOT))):
                violations = scan_self_containment(doc.text, {CANONICAL_HOST})
                self.assertEqual(
                    [], violations, "self-containment violations:\n  " + "\n  ".join(violations)
                )

    def test_pages_have_no_base_tag(self):
        for doc in self.documents:
            with self.subTest(page=str(doc.path.relative_to(REPO_ROOT))):
                self.assertFalse(
                    doc.has_base,
                    "<base> rewrites every relative URL and breaks subpath serving",
                )

    def test_scanner_detects_planted_violations(self):
        """The invariant checker must not be silently inert."""
        planted = {
            "remote script": '<script src="https://cdn.example.com/a.js"></script>',
            "remote stylesheet": '<link rel="stylesheet" href="https://cdn.example.com/a.css">',
            "remote @import": '<style>@import url("https://cdn.example.com/a.css");</style>',
            "remote css url()": "<style>body{background:url(https://cdn.example.com/i.png)}</style>",
            "protocol relative": '<img src="//cdn.example.com/i.png">',
            "preconnect": '<link rel="preconnect" href="https://fonts.gstatic.com">',
            "fetch call": "<script>fetch('/x')</script>",
            "XHR": "<script>new XMLHttpRequest()</script>",
            "websocket": "<script>new WebSocket('wss://x.example')</script>",
            "base tag": '<base href="/">',
            "remote svg use": '<svg><use href="https://icons.example.com/s.svg#i"/></svg>',
            "remote og:image": '<meta property="og:image" content="https://cdn.example.org/c.png">',
        }
        for label, fragment in sorted(planted.items()):
            with self.subTest(planted=label):
                found = scan_self_containment(
                    "<!doctype html><html><head>%s</head><body></body></html>" % fragment,
                    {CANONICAL_HOST},
                )
                self.assertTrue(found, "scanner failed to detect a planted %s" % label)

    def test_scanner_accepts_a_clean_document(self):
        clean = (
            "<!doctype html><html><head>"
            '<link rel="canonical" href="%s/">'
            "<style>body{background:url(data:image/png;base64,AAAA)}</style>"
            "</head><body><a href=\"./market-structure-lab/\">go</a>"
            "<script>var x=1;</script></body></html>" % CANONICAL_ORIGIN
        )
        self.assertEqual([], scan_self_containment(clean, {CANONICAL_HOST}))


class TestSubpathSafety(SiteFixture):
    def test_no_absolute_asset_paths(self):
        for doc in self.documents:
            for tag, attr, value, line in doc.urls:
                if not value.startswith("/") or value.startswith("//"):
                    continue
                with self.subTest(page=str(doc.path.relative_to(REPO_ROOT)), line=line):
                    self.fail(
                        "root-relative URL <%s %s=%r> at line %d: use a document-relative "
                        "path so the page keeps working under any prefix"
                        % (tag, attr, value, line)
                    )

    def test_relative_links_resolve_to_real_files(self):
        for doc in self.documents:
            page = str(doc.path.relative_to(REPO_ROOT))
            for tag, attr, value, line in doc.urls:
                if not is_internal_relative(value):
                    continue
                target = value.split("#", 1)[0].split("?", 1)[0]
                if not target:
                    continue
                with self.subTest(page=page, url=value, line=line):
                    resolved = (doc.path.parent / target).resolve()
                    self.assertTrue(
                        str(resolved).startswith(str(SITE_ROOT)),
                        "link escapes the document root: %r -> %s" % (value, resolved),
                    )
                    if target.endswith("/") or resolved.is_dir():
                        resolved = resolved / "index.html"
                    self.assertTrue(
                        resolved.is_file(),
                        "<%s %s=%r> at line %d resolves to %s, which does not exist"
                        % (tag, attr, value, line, resolved),
                    )

    def test_in_page_anchors_resolve(self):
        for doc in self.documents:
            page = str(doc.path.relative_to(REPO_ROOT))
            for tag, attr, value, line in doc.urls:
                if not value.startswith("#") or value == "#":
                    continue
                fragment = urllib.parse.unquote(value[1:])
                with self.subTest(page=page, anchor=value, line=line):
                    self.assertIn(
                        fragment,
                        doc.ids,
                        "<%s %s=%r> at line %d points at an id that does not exist on the page"
                        % (tag, attr, value, line),
                    )


class TestPageMetadata(SiteFixture):
    def test_pages_declare_title_description_and_canonical(self):
        for doc in self.documents:
            page = str(doc.path.relative_to(REPO_ROOT))
            with self.subTest(page=page):
                self.assertTrue((doc.title or "").strip(), "missing a non-empty <title>")
                self.assertTrue(
                    (doc.description or "").strip(), 'missing <meta name="description">'
                )
                self.assertTrue(doc.canonical, 'missing <link rel="canonical">')
                self.assertTrue(
                    (doc.lang or "").strip(), "missing a lang attribute on <html>"
                )

    def test_canonical_matches_the_published_url(self):
        for doc in self.documents:
            page = str(doc.path.relative_to(REPO_ROOT))
            with self.subTest(page=page):
                expected = CANONICAL_ORIGIN + served_path(doc.path)
                self.assertEqual(
                    expected,
                    doc.canonical,
                    "canonical URL disagrees with where the file is published; "
                    "one of the two is wrong",
                )

    def test_canonical_never_claims_the_apex(self):
        """geterdone.io is a separate live site this platform does not control."""
        for doc in self.documents:
            page = str(doc.path.relative_to(REPO_ROOT))
            with self.subTest(page=page):
                host = urllib.parse.urlsplit(doc.canonical or "").hostname or ""
                self.assertEqual(
                    CANONICAL_HOST,
                    host,
                    "canonical host must be %s, got %r" % (CANONICAL_HOST, host),
                )


class TestContent(SiteFixture):
    def test_course_pages_retain_the_disclaimer(self):
        """Everything below the catalog root teaches trading and must say so.

        That is the course home as well as all seven labs: the course home is not
        an exempt landing page, it sells the same material.

        Checked two ways on purpose: every DECLARED course page must be present (a
        lab that vanished cannot pass by not being iterated), and every PUBLISHED
        non-catalog page must carry the disclaimer (a page added without touching
        REQUIRED_PAGES is still covered).
        """
        by_url = {served_path(doc.path): doc for doc in self.documents}
        missing = sorted(set(COURSE_PAGES) - set(by_url))
        self.assertEqual(
            [],
            missing,
            "declared course pages are not published: %s" % missing,
        )
        course_pages = [doc for url, doc in sorted(by_url.items()) if url != "/"]
        self.assertTrue(course_pages, "no course page found under %s" % SITE_ROOT)
        for doc in course_pages:
            with self.subTest(page=str(doc.path.relative_to(REPO_ROOT))):
                self.assertRegex(
                    doc.text,
                    DISCLAIMER_RE,
                    "course page lost its educational-use disclaimer",
                )

    def test_no_secret_like_strings(self):
        for path in sorted(p for p in SITE_ROOT.rglob("*") if p.is_file()):
            text = read_text_or_none(path)
            if text is None:
                continue
            for label, pattern in SECRET_PATTERNS:
                match = pattern.search(text)
                with self.subTest(file=str(path.relative_to(REPO_ROOT)), kind=label):
                    if match:
                        self.fail(
                            "possible %s at offset %d: %r"
                            % (label, match.start(), match.group(0)[:40])
                        )

    def test_secret_scanner_detects_planted_secrets(self):
        planted = [
            "AKIA" + "A" * 16,
            "ghp_" + "b" * 36,
            'api_key = "abcdefghijklmnop"',
            "-----BEGIN RSA PRIVATE KEY-----",
            "postgres://user:hunter2@db.example/app",
        ]
        for sample in planted:
            with self.subTest(sample=sample[:24]):
                self.assertTrue(
                    any(pattern.search(sample) for _, pattern in SECRET_PATTERNS),
                    "secret scanner missed a planted credential",
                )

    def test_secret_scanner_tolerates_ordinary_prose(self):
        benign = "DESIGN TOKENS - copied verbatim from the lesson page. Token colors: #36d6e7."
        for label, pattern in SECRET_PATTERNS:
            with self.subTest(kind=label):
                self.assertIsNone(pattern.search(benign))


def is_internal_relative(value):
    if not value or value.startswith(("#", "//")):
        return False
    scheme = urllib.parse.urlsplit(value).scheme.lower()
    return scheme == ""


def read_text_or_none(path):
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


if __name__ == "__main__":
    unittest.main(verbosity=2)
