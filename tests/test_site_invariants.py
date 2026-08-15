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
  * The site is a LIBRARY of courses now, so every invariant that used to be
    "the course" is stated per course and asserted for both. The theme
    localStorage key is checked site-wide for exactly that reason: two courses
    that each persist the reader's theme under their own key is a bug that looks
    like nothing until a reader crosses from one course to the other.
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

# The published URL space is two levels deep: the site index is the LEARNING
# PATH (an ordered catalog of courses), each course has a home page, and each
# course's lessons live under that home.
#
#     /                                  the learning path (catalog of courses)
#     /market-structure-lab/             course 1 home, "Market Structure Lab"
#     /market-structure-lab/<lesson>/    course 1's seven lessons, in course order
#     /trade-setup-execution/            course 2 home, "Trade Setup and Execution"
#     /trade-setup-execution/<lesson>/   course 2's fifteen lessons, in course order
#
# That is 25 HTML pages. The document root publishes exactly one further thing,
# a non-HTML asset, declared separately in NON_HTML_ASSETS below.
#
# Containerfile.release, .github/workflows/{ci,pages}.yml, release/contract.json
# (acceptance.checks) and scripts/smoke.py all assert the same mapping; changing
# one without the others is how a lesson silently stops being published.
#
# The seven FLAT URLs course 1 used to publish (/market-structure/ and its six
# siblings) are deliberately gone. Breaking them was an accepted decision, there
# are no redirect stubs, and they must not be re-added here: a path listed below
# is a path that must exist.
#
# LESSON ORDER IS THE COURSE SEQUENCE, not alphabetical order. It is declared
# once, here, and TestLessonChain walks the prev/next pager against it, so a
# course whose pager disagrees with its own syllabus fails rather than shipping.
SITE_INDEX = "/"

COURSE_1_HOME = "/market-structure-lab/"
COURSE_1_LESSONS = (
    "market-structure",
    "ranges-breakouts-liquidity",
    "multi-timeframe-market-structure",
    "pullbacks-entry-models",
    "invalidation-stops-risk-reward",
    "volume-relative-strength",
    "options-contract-selection",
)

COURSE_2_HOME = "/trade-setup-execution/"
COURSE_2_LESSONS = (
    "trade-thesis",
    "support-resistance",
    "confluence",
    "breakout-setups",
    "pullback-setups",
    "reversal-setups",
    "entry-confirmation",
    "stop-loss-placement",
    "profit-targets",
    "risk-to-reward",
    "position-sizing",
    "trade-management",
    "backtesting",
    "trading-journal",
    "performance-review",
)

# (course title, course home URL, lesson slugs in course order)
COURSES = (
    ("Market Structure Lab", COURSE_1_HOME, COURSE_1_LESSONS),
    ("Trade Setup and Execution", COURSE_2_HOME, COURSE_2_LESSONS),
)

UNKNOWN_PATH_CHECK = "/release-smoke-unknown-path"


def lesson_url(home, slug):
    """The published URL of one lesson of the course whose home is `home`."""
    return "%s%s/" % (home, slug)


def source_of(url):
    """The file under site/ that must be published at this directory URL."""
    return url.lstrip("/") + "index.html"


REQUIRED_PAGES = {SITE_INDEX: "index.html"}
for _title, _home, _slugs in COURSES:
    REQUIRED_PAGES[_home] = source_of(_home)
    for _slug in _slugs:
        REQUIRED_PAGES[lesson_url(_home, _slug)] = source_of(lesson_url(_home, _slug))

# Published, but NOT a document. The HTML invariants -- <title>,
# <meta name="description">, rel=canonical, the educational-use disclaimer --
# are properties of a page a reader reads; a JSON schema file has none of them
# and never should. Rather than loosen those checks so one file can slip
# through, the asset is declared here as what it is: it is still published, so
# it is still guarded by every publish-time page list, still probed by
# scripts/smoke.py, and still checked here -- as JSON (TestPublishedAssets).
NON_HTML_ASSETS = {
    "/trade-setup-execution/trade-journal-schema.json":
        "trade-setup-execution/trade-journal-schema.json",
}

# Rides along inside the document root without being published content. CNAME
# is GitHub Pages' custom-domain control file (it holds learn.geterdone.io); it
# configures delivery and is not a page or an asset any lesson links to.
DELIVERY_CONTROL_FILES = frozenset({"CNAME"})

COURSE_HOMES = tuple(home for _title, home, _slugs in COURSES)

# "/" is the learning path; every other published page is course material --
# both course homes as well as all 22 lessons. All of it teaches trading, so all
# of it carries the same disclaimer. There is no exempt page below the root.
COURSE_PAGES = {url: rel for url, rel in REQUIRED_PAGES.items() if url != SITE_INDEX}

# The 22 lessons alone, without either course home.
LESSON_PAGES = {url: rel for url, rel in COURSE_PAGES.items() if url not in COURSE_HOMES}

# Every page of the library persists the reader's theme under ONE localStorage
# key. Course 1 shipped "marketStructureTheme" and course 2 shipped
# "market-lab-theme"; with two courses on one origin that meant a reader's
# choice silently reset at the course boundary. The site standardized on
# "learn-theme" everywhere. Note the check below reads storage CALL SITES, not
# prose: site/index.html names both retired keys in a comment that explains the
# migration, and documenting the fix must not fail the build.
THEME_STORAGE_KEY = "learn-theme"
RETIRED_THEME_KEYS = ("marketStructureTheme", "market-lab-theme")

# localStorage.getItem("k") / setItem("k", v) / removeItem("k") -- a literal key.
STORAGE_LITERAL_KEY_RE = re.compile(
    r"""localStorage\s*\.\s*(?:get|set|remove)Item\s*\(\s*(['"])([^'"\n]*)\1"""
)
# The same call with an identifier, e.g. localStorage.setItem(THEME_KEY, next).
STORAGE_IDENT_KEY_RE = re.compile(
    r"""localStorage\s*\.\s*(?:get|set|remove)Item\s*\(\s*([A-Za-z_$][\w$]*)\s*[,)]"""
)
# A storage key is a THEME key when the key itself says so. This is what keeps
# unrelated storage (the journal export key, for instance) out of the check.
THEMEISH_KEY_RE = re.compile(r"(?i)theme")

# The pre-paint read every page must perform, with either quote style.
PREPAINT_THEME_READ_RE = re.compile(
    r"""localStorage\s*\.\s*getItem\s*\(\s*(['"])%s\1\s*\)""" % THEME_STORAGE_KEY
)

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
        self.pager = []  # (rel, href, line) for <a rel="prev"|"next">
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
        if tag == "a":
            rel = (attrd.get("rel") or "").lower().split()
            for direction in ("prev", "next"):
                if direction in rel and attrd.get("href"):
                    self.pager.append((direction, attrd["href"].strip(), line))

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

    def test_no_file_is_published_outside_the_declared_url_space(self):
        """Same contract, applied to everything in the tree, not only to pages.

        A .json, .css or .png dropped into site/ is published at a live URL the
        moment it is committed, and the HTML-only sweep above would never see
        it. Declaring it (NON_HTML_ASSETS) is one line; publishing something
        nothing has declared is how an unreviewed file goes live.
        """
        declared = set(REQUIRED_PAGES.values()) | set(NON_HTML_ASSETS.values())
        published = {
            path.relative_to(SITE_ROOT).as_posix()
            for path in SITE_ROOT.rglob("*")
            if path.is_file()
        }
        undeclared = sorted(
            rel for rel in published - declared
            if Path(rel).name not in DELIVERY_CONTROL_FILES
        )
        self.assertEqual(
            [],
            undeclared,
            "files published under undeclared URLs: %s. Add each to "
            "REQUIRED_PAGES (a page) or NON_HTML_ASSETS (an asset), and to the "
            "publish guards in ci.yml, pages.yml and Containerfile.release."
            % undeclared,
        )


class TestDeclaredUrlSpaceAgrees(unittest.TestCase):
    """The published URL map is declared in several places. Drift is the failure.

    REQUIRED_PAGES above is the on-disk declaration. scripts/smoke.py declares the
    same map for the SERVED responses and release/contract.json declares it as the
    acceptance matrix. A page added to one and not the others is a live page that
    nothing probes, which is exactly the hole these tests exist to close. The
    course homes count: they are published, so they are probed -- and so is the
    one non-HTML asset, which is checked as JSON rather than as a page.
    """

    def test_declared_url_space_is_the_two_level_course_tree(self):
        """Learning path, then a home per course, then that course's lessons.

        25 URLs exactly: /, two course homes, and 7 + 15 lessons beneath them.
        The flat /<lesson>/ URLs were retired without redirects, so a two-segment
        lesson path is the only shape a lesson may have; re-adding a one-segment
        lesson here would declare a page that no longer exists on disk.
        """
        expected = 1 + len(COURSES) + sum(len(slugs) for _t, _h, slugs in COURSES)
        self.assertEqual(
            25, expected, "the library is 1 + 2 + 7 + 15 = 25 pages, got %d" % expected
        )
        self.assertEqual(
            expected,
            len(REQUIRED_PAGES),
            "expected %d published URLs, got %d" % (expected, len(REQUIRED_PAGES)),
        )
        self.assertEqual(7, len(COURSE_1_LESSONS), "course 1 is seven lessons")
        self.assertEqual(15, len(COURSE_2_LESSONS), "course 2 is fifteen lessons")
        self.assertEqual(
            len(set(COURSE_1_LESSONS)), len(COURSE_1_LESSONS), "duplicate slug in course 1"
        )
        self.assertEqual(
            len(set(COURSE_2_LESSONS)), len(COURSE_2_LESSONS), "duplicate slug in course 2"
        )
        for _title, home, _slugs in COURSES:
            with self.subTest(course=home):
                self.assertIn(home, REQUIRED_PAGES, "the course home must be published")
        # Two course homes, neither a prefix of the other: the first path
        # segment must identify the course on its own, or /a/ and /a-b/x/ start
        # answering for each other in guards that match on prefixes.
        for _title, home, _slugs in COURSES:
            for _other_title, other, _other_slugs in COURSES:
                if home is other:
                    continue
                with self.subTest(home=home, other=other):
                    self.assertFalse(
                        home.startswith(other) or other.startswith(home),
                        "course homes %s and %s are prefix-ambiguous" % (home, other),
                    )
        for url, relative in sorted(REQUIRED_PAGES.items()):
            with self.subTest(url=url):
                self.assertTrue(url.startswith("/") and url.endswith("/"),
                                "a published URL is a directory URL")
                self.assertEqual(url.lstrip("/"), relative[: -len("index.html")],
                                 "URL and source file disagree")
        for url in sorted(LESSON_PAGES):
            with self.subTest(url=url):
                owners = [home for home in COURSE_HOMES if url.startswith(home)]
                self.assertEqual(
                    1,
                    len(owners),
                    "a lesson lives under exactly one course home, %s matched %s"
                    % (url, owners),
                )
                self.assertEqual(
                    2,
                    url.strip("/").count("/") + 1,
                    "a lesson URL is exactly <course>/<lesson>/, got %s" % url,
                )

    def test_declared_assets_are_not_pages(self):
        """The asset map exists so no page check has to be softened for it."""
        self.assertTrue(NON_HTML_ASSETS, "the JSON schema asset must stay declared")
        for url, relative in sorted(NON_HTML_ASSETS.items()):
            with self.subTest(url=url):
                self.assertNotIn(
                    url, REQUIRED_PAGES, "an asset is not a page; declare it once"
                )
                self.assertFalse(
                    url.endswith("/"), "an asset URL names a file, not a directory"
                )
                self.assertEqual(
                    url.lstrip("/"), relative, "asset URL and source file disagree"
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

    def test_smoke_client_probes_every_published_asset(self):
        """The asset is published, so a whole-site probe must fetch it too.

        It is probed by its own check, not folded into the page sweep: an
        HTML-shaped assertion against a JSON body proves nothing.
        """
        from smoke import parse_args, asset_targets

        args = parse_args([CANONICAL_ORIGIN])
        probed = {path for _check_id, path, _markers in asset_targets(args)}
        self.assertEqual(
            set(NON_HTML_ASSETS),
            probed,
            "scripts/smoke.py probes a different asset set than this suite "
            "declares (only in smoke: %s; only here: %s)"
            % (sorted(probed - set(NON_HTML_ASSETS)), sorted(set(NON_HTML_ASSETS) - probed)),
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
                published = set(REQUIRED_PAGES) | set(NON_HTML_ASSETS)
                missing = sorted(published - checked)
                self.assertEqual(
                    [],
                    missing,
                    "release/%s declares no public acceptance check for %s; a release "
                    "would be accepted without ever fetching those pages" % (name, missing),
                )
                # Bidirectional on purpose: a one-way check would let a retired
                # URL linger in the contract forever, quietly asserting a page
                # that is no longer published.
                stale = sorted(checked - published - {UNKNOWN_PATH_CHECK})
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
        """Everything below the learning path teaches trading and must say so.

        That is both course homes as well as all 22 lessons: a course home is not
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


class TestPublishedAssets(SiteFixture):
    """The one non-HTML thing the document root publishes.

    It is checked as what it is. A JSON schema has no <title>, no
    <meta name="description">, no rel=canonical and no disclaimer, and inventing
    them would be worse than declaring the file's real type: the fix for "this
    check cannot apply to that file" is a check that fits the file, never a
    weakened check that fits both.
    """

    def test_declared_assets_exist_at_their_published_paths(self):
        for url, relative in sorted(NON_HTML_ASSETS.items()):
            with self.subTest(url=url):
                target = SITE_ROOT / relative
                self.assertTrue(
                    target.is_file(),
                    "%s must be served from %s, but that file does not exist" % (url, target),
                )
                self.assertEqual(
                    url,
                    served_path(target),
                    "the asset is published at a different URL than it declares",
                )

    def test_declared_json_assets_parse(self):
        """A corrupt export schema is a broken lesson 14 -> 15 handoff.

        Lesson 14 exports trade-journal-v1 and lesson 15 imports it; this file
        is the exchange shape both refer a reader to. Shipping it unparseable
        would 200 happily and still be broken, so parse it here.
        """
        for url, relative in sorted(NON_HTML_ASSETS.items()):
            if not url.endswith(".json"):
                continue
            with self.subTest(url=url):
                target = SITE_ROOT / relative
                try:
                    document = json.loads(target.read_text(encoding="utf-8"))
                except (ValueError, OSError) as exc:
                    self.fail("%s does not parse as JSON: %s" % (url, exc))
                self.assertIsInstance(
                    document, dict, "%s must be a JSON object" % url
                )
                self.assertTrue(document, "%s is an empty JSON document" % url)


class TestThemeKey(SiteFixture):
    """One library, one theme key.

    Course 1 shipped "marketStructureTheme" and course 2 shipped
    "market-lab-theme". Both worked perfectly inside their own course and broke
    the moment the two shared an origin: the reader's explicit light/dark choice
    silently reset at the course boundary, on a site whose whole point is that a
    reader walks from course 1 into course 2. The site now uses "learn-theme"
    everywhere, and "everywhere" is the invariant -- a third course that quietly
    invents its own key must fail here rather than at a reader's expense.
    """

    @staticmethod
    def storage_keys(text):
        """Every localStorage key the document actually uses, literal or named.

        Prose is deliberately not evidence: only a real getItem/setItem/
        removeItem call site counts, so a comment explaining the migration (as
        site/index.html carries) is not a use. An identifier key is resolved
        through its own `var NAME = "..."` declaration; one that cannot be
        resolved statically (a function parameter in a generic storage helper)
        is skipped rather than guessed at.
        """
        keys = {m.group(2) for m in STORAGE_LITERAL_KEY_RE.finditer(text)}
        for match in STORAGE_IDENT_KEY_RE.finditer(text):
            declaration = re.search(
                r"""(?:var|let|const)\s+%s\s*=\s*(['"])([^'"\n]*)\1"""
                % re.escape(match.group(1)),
                text,
            )
            if declaration:
                keys.add(declaration.group(2))
        return keys

    @classmethod
    def theme_keys(cls, text):
        return {key for key in cls.storage_keys(text) if THEMEISH_KEY_RE.search(key)}

    def test_every_page_reads_the_shared_theme_key_before_paint(self):
        for doc in self.documents:
            with self.subTest(page=str(doc.path.relative_to(REPO_ROOT))):
                self.assertRegex(
                    doc.text,
                    PREPAINT_THEME_READ_RE,
                    "page does not read localStorage[%r]; every page in the "
                    "library applies the stored theme before first paint, or the "
                    "reader's choice flashes away on this page alone"
                    % THEME_STORAGE_KEY,
                )

    def test_no_page_stores_the_theme_under_any_other_key(self):
        for doc in self.documents:
            with self.subTest(page=str(doc.path.relative_to(REPO_ROOT))):
                self.assertEqual(
                    {THEME_STORAGE_KEY},
                    self.theme_keys(doc.text),
                    "this page's theme storage key(s) are not exactly %r. Two "
                    "courses with two keys is the bug this test exists to make "
                    "impossible; the retired keys are %s."
                    % (THEME_STORAGE_KEY, ", ".join(repr(k) for k in RETIRED_THEME_KEYS)),
                )

    def test_the_whole_library_shares_one_theme_key(self):
        used = set()
        for doc in self.documents:
            used |= self.theme_keys(doc.text)
        self.assertEqual(
            {THEME_STORAGE_KEY},
            used,
            "the library uses %d theme storage keys (%s); it must use exactly one"
            % (len(used), ", ".join(sorted(repr(k) for k in used))),
        )

    def test_theme_key_scanner_is_not_inert(self):
        """A planted second key is caught; a comment about one is not."""
        for retired in RETIRED_THEME_KEYS:
            with self.subTest(planted=retired):
                self.assertEqual(
                    {retired},
                    self.theme_keys(
                        "<script>var t = localStorage.getItem('%s');</script>" % retired
                    ),
                )
                self.assertEqual(
                    {retired},
                    self.theme_keys(
                        '<script>var KEY = "%s"; localStorage.setItem(KEY, next);</script>'
                        % retired
                    ),
                )
                self.assertEqual(
                    {THEME_STORAGE_KEY},
                    self.theme_keys(
                        "<script>/* the retired key %s could not survive two "
                        "courses */ var t = localStorage.getItem('%s');"
                        "</script>" % (retired, THEME_STORAGE_KEY)
                    ),
                    "naming a retired key in a comment is documentation, not a "
                    "use: site/index.html explains the migration in prose and "
                    "must keep passing",
                )


class TestLessonChain(SiteFixture):
    """Each course's prev/next pager walks that course, in course order.

    The pager is the only way a reader moves through a lesson sequence without
    going back to the course home, so a missing or misdirected link strands
    them. The expected order is COURSES above -- the syllabus -- so a course
    reordered in one place and not the other fails here instead of teaching the
    lessons in the wrong sequence.
    """

    def pager(self, doc, direction):
        return [href for rel, href, _line in doc.pager if rel == direction]

    def resolve(self, url, href):
        return urllib.parse.urljoin(url, href)

    def test_prev_next_links_form_a_complete_chain_per_course(self):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        for title, home, slugs in COURSES:
            urls = [lesson_url(home, slug) for slug in slugs]
            for index, url in enumerate(urls):
                doc = by_url.get(url)
                with self.subTest(course=title, lesson=url):
                    self.assertIsNotNone(doc, "%s is not published" % url)
                    previous = self.pager(doc, "prev")
                    following = self.pager(doc, "next")

                    if index == 0:
                        # Nothing precedes lesson 01. A pager link back to the
                        # course home is allowed; a link to another lesson is
                        # not, because it would enter the chain out of order.
                        for href in previous:
                            self.assertEqual(
                                home,
                                self.resolve(url, href),
                                "lesson 01 of %s links back to %r; the only thing "
                                "before the first lesson is the course home"
                                % (title, href),
                            )
                    else:
                        self.assertEqual(
                            1,
                            len(previous),
                            'expected exactly one <a rel="prev">, got %d' % len(previous),
                        )
                        self.assertEqual(
                            urls[index - 1],
                            self.resolve(url, previous[0]),
                            "prev must point at lesson %02d of %s"
                            % (index, title),
                        )

                    if index == len(urls) - 1:
                        # Nothing follows the last lesson but the course home.
                        for href in following:
                            self.assertEqual(
                                home,
                                self.resolve(url, href),
                                "the last lesson of %s links forward to %r; the "
                                "only thing after it is the course home"
                                % (title, href),
                            )
                    else:
                        self.assertEqual(
                            1,
                            len(following),
                            'expected exactly one <a rel="next">, got %d' % len(following),
                        )
                        self.assertEqual(
                            urls[index + 1],
                            self.resolve(url, following[0]),
                            "next must point at lesson %02d of %s"
                            % (index + 2, title),
                        )

    def test_every_course_home_links_to_every_one_of_its_lessons(self):
        """The home is the other way in; a lesson it omits is unreachable."""
        by_url = {served_path(doc.path): doc for doc in self.documents}
        for title, home, slugs in COURSES:
            doc = by_url.get(home)
            with self.subTest(course=title):
                self.assertIsNotNone(doc, "%s is not published" % home)
                linked = {
                    urllib.parse.urljoin(home, value.split("#", 1)[0])
                    for tag, attr, value, _line in doc.urls
                    if tag == "a" and attr == "href" and is_internal_relative(value)
                }
                missing = [
                    lesson_url(home, slug)
                    for slug in slugs
                    if lesson_url(home, slug) not in linked
                ]
                self.assertEqual(
                    [], missing, "%s does not link to %s" % (home, missing)
                )


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
