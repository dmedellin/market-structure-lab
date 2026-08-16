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
    "the course" is stated per course and asserted for every one of them. The
    theme localStorage key is checked site-wide for exactly that reason: courses
    that each persist the reader's theme under their own key is a bug that looks
    like nothing until a reader crosses from one course to the next.
  * Three courses share one origin, one visual system and one navigation model,
    so the conventions that cross course boundaries -- the lesson pager markup,
    the light palette token VALUES, and the theme-toggle button -- are pinned in
    TestPinnedConventions. Each course inventing its own variant is invisible in
    review (every variant works inside its own course) and visible to a reader
    the moment they cross from one course into the next.
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
#     /options-trading/                  course 3 home, "Options Trading"
#     /options-trading/<lesson>/         course 3's sixteen lessons, in course order
#
# That is 42 HTML pages. The document root publishes exactly two further things,
# both non-HTML assets -- one exchange schema per course that ships one --
# declared separately in NON_HTML_ASSETS below.
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

COURSE_3_HOME = "/options-trading/"
COURSE_3_LESSONS = (
    "options-contract-fundamentals",
    "calls-and-puts",
    "moneyness",
    "option-premium",
    "option-chain-and-liquidity",
    "expiration-and-time-decay",
    "implied-volatility",
    "delta-and-gamma",
    "theta-and-vega",
    "long-calls-and-long-puts",
    "covered-calls",
    "cash-secured-puts",
    "vertical-debit-spreads",
    "vertical-credit-spreads",
    "exercise-assignment-and-expiration",
    "options-trade-planning",
)

# (course title, course home URL, lesson slugs in course order)
COURSES = (
    ("Market Structure Lab", COURSE_1_HOME, COURSE_1_LESSONS),
    ("Trade Setup and Execution", COURSE_2_HOME, COURSE_2_LESSONS),
    ("Options Trading", COURSE_3_HOME, COURSE_3_LESSONS),
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
# Each entry is declared explicitly. A second asset is a second LINE here, never
# a reason to relax an HTML check so both files can pass one sweep.
NON_HTML_ASSETS = {
    "/trade-setup-execution/trade-journal-schema.json":
        "trade-setup-execution/trade-journal-schema.json",
    "/options-trading/options-trade-plan-schema.json":
        "options-trading/options-trade-plan-schema.json",
}

# Rides along inside the document root without being published content. CNAME
# is GitHub Pages' custom-domain control file (it holds learn.geterdone.io); it
# configures delivery and is not a page or an asset any lesson links to.
DELIVERY_CONTROL_FILES = frozenset({"CNAME"})

COURSE_HOMES = tuple(home for _title, home, _slugs in COURSES)

# "/" is the learning path; every other published page is course material --
# all three course homes as well as all 38 lessons. All of it teaches trading, so
# all of it carries the same disclaimer. There is no exempt page below the root.
COURSE_PAGES = {url: rel for url, rel in REQUIRED_PAGES.items() if url != SITE_INDEX}

# The 38 lessons alone, without any course home.
LESSON_PAGES = {url: rel for url, rel in COURSE_PAGES.items() if url not in COURSE_HOMES}

# Every page of the library persists the reader's theme under ONE localStorage
# key. Course 1 shipped "marketStructureTheme", course 2 shipped
# "market-lab-theme" and course 3 arrived with a third key,
# "options-course-theme"; with several courses on one origin that meant a
# reader's choice silently reset at every course boundary. The site standardized
# on "learn-theme" everywhere. Note the check below reads storage CALL SITES, not
# prose: site/index.html names both retired keys in a comment that explains the
# migration, and documenting the fix must not fail the build.
THEME_STORAGE_KEY = "learn-theme"
RETIRED_THEME_KEYS = (
    "marketStructureTheme", "market-lab-theme", "options-course-theme",
)

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
    course homes count: they are published, so they are probed -- and so are both
    non-HTML assets, each checked as JSON rather than as a page.
    """

    def test_declared_url_space_is_the_two_level_course_tree(self):
        """Learning path, then a home per course, then that course's lessons.

        42 URLs exactly: /, three course homes, and 7 + 15 + 16 lessons beneath
        them. The flat /<lesson>/ URLs were retired without redirects, so a
        two-segment lesson path is the only shape a lesson may have; re-adding a
        one-segment lesson here would declare a page that no longer exists on
        disk.
        """
        expected = 1 + len(COURSES) + sum(len(slugs) for _t, _h, slugs in COURSES)
        self.assertEqual(
            42,
            expected,
            "the library is 1 + 3 + 7 + 15 + 16 = 42 pages, got %d" % expected,
        )
        self.assertEqual(
            expected,
            len(REQUIRED_PAGES),
            "expected %d published URLs, got %d" % (expected, len(REQUIRED_PAGES)),
        )
        self.assertEqual(3, len(COURSES), "the library is three courses")
        self.assertEqual(7, len(COURSE_1_LESSONS), "course 1 is seven lessons")
        self.assertEqual(15, len(COURSE_2_LESSONS), "course 2 is fifteen lessons")
        self.assertEqual(16, len(COURSE_3_LESSONS), "course 3 is sixteen lessons")
        for index, (title, _home, slugs) in enumerate(COURSES, start=1):
            with self.subTest(course=title):
                self.assertEqual(
                    len(set(slugs)), len(slugs), "duplicate slug in course %d" % index
                )
        for _title, home, _slugs in COURSES:
            with self.subTest(course=home):
                self.assertIn(home, REQUIRED_PAGES, "the course home must be published")
        # No course home may be a prefix of another: the first path segment
        # must identify the course on its own, or /a/ and /a-b/x/ start
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
        """The asset map exists so no page check has to be softened for it.

        Both published schemas are declared here, one line each. The second one
        arriving with course 3 is the moment the temptation appears to relax an
        HTML assertion so a JSON file can slip through the page sweep; the fix
        for "this check cannot apply to that file" is another declaration, never
        a weaker check.
        """
        self.assertEqual(
            2,
            len(NON_HTML_ASSETS),
            "both published JSON schemas must stay declared: course 2's trade "
            "journal exchange schema and course 3's options trade plan schema",
        )
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

        That is all three course homes as well as all 38 lessons: a course home
        is not an exempt landing page, it sells the same material.

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
    """The non-HTML things the document root publishes.

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
        """A corrupt export schema is a broken handoff between two lessons.

        Course 2's lesson 14 exports trade-journal-v1 and lesson 15 imports it;
        course 3's lesson 16 exports options-trade-plan-v1. Each file is the
        exchange shape those lessons refer a reader to. Shipping one
        unparseable would 200 happily and still be broken, so parse it here.
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

    Course 1 shipped "marketStructureTheme", course 2 shipped "market-lab-theme"
    and course 3 arrived carrying "options-course-theme". Each worked perfectly
    inside its own course and broke the moment they shared an origin: the
    reader's explicit light/dark choice silently reset at the course boundary, on
    a site whose whole point is that a reader walks from course 1 through course
    3. The site now uses "learn-theme" everywhere, and "everywhere" is the
    invariant -- a fourth course that quietly invents its own key must fail here
    rather than at a reader's expense.
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


# ---------------------------------------------------------------------------
# The pinned cross-course conventions
# ---------------------------------------------------------------------------
# Three courses, authored at three different times, now share one origin. The
# review before course 3 landed found all three drifting in the same three
# places, and every variant looked correct inside its own course:
#
#   * three incompatible pager families, so "the next lesson link" was a
#     different component on each course;
#   * light palette token values that differ by a digit or two per page, so the
#     page ground shifts as a reader walks the library;
#   * a theme-toggle button whose accessible name was rewritten from JavaScript
#     to describe the NEXT state on some pages and the CURRENT state on others,
#     which is two different meanings for one control.
#
# None of that fails a single-course review and all of it is visible to a
# reader crossing a course boundary. So it is pinned below, character for
# character, and a fourth course that invents its own variant fails here.

# The light palette, one value per token. Contrast against --bg #edf4f8:
# cyan 4.98, cyan-2 5.43, green 4.94, red 5.14, amber 5.33, purple 5.44,
# blue 5.64, muted 4.91 -- all >= 4.5:1. A page declares only the tokens it
# actually uses, but a token it DOES declare carries exactly this value.
LIGHT_PALETTE = {
    "--bg": "#edf4f8",
    "--bg-2": "#f9fbfd",
    "--panel": "rgba(255, 255, 255, 0.94)",
    "--panel-solid": "#ffffff",
    "--panel-2": "#f3f8fb",
    "--panel-3": "#eaf2f7",
    "--text": "#102433",
    "--muted": "#586c7c",
    "--line": "rgba(24, 62, 88, 0.13)",
    "--line-strong": "rgba(24, 62, 88, 0.24)",
    "--cyan": "#0e7382",
    "--cyan-2": "#0b6d79",
    "--green": "#10784f",
    "--red": "#c22a34",
    "--amber": "#8a5a06",
    "--purple": "#6b46d6",
    "--blue": "#1d5fd0",
    "--on-accent": "#ffffff",
    "--shadow": "0 22px 55px rgba(39, 77, 101, 0.14)",
}

# Light has TWO paths, and both must carry the same values: the explicit toggle
# ([data-theme="light"]) and the system preference, for the reader who never
# touches the toggle. A component-level `[data-theme="light"] .foo {…}` rule
# reaches only the first of them, which is precisely how the two paths drift
# apart -- so components read tokens and nothing else.
LIGHT_TOGGLE_SELECTOR = '[data-theme="light"]'
LIGHT_MEDIA_PRELUDE = "@media (prefers-color-scheme: light)"
LIGHT_MEDIA_SELECTOR = ':root:not([data-theme="dark"])'

STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
CSS_VARIABLE_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+);")

# The lesson pager, verbatim. Class names are exactly lesson-nav /
# lesson-link prev / lesson-link next; the retired families below are the ones
# the three courses shipped separately and must never come back.
LESSON_NAV_MARKUP = '<nav class="lesson-nav" aria-label="Lesson navigation">'
LESSON_NAV_RE = re.compile(r"<nav class=\"lesson-nav\"[^>]*>(.*?)</nav>", re.S)
PAGER_ANCHOR_RE = re.compile(r"<a\s+([^>]*?)>(.*?)</a>", re.S)
ATTRIBUTE_RE = re.compile(r"([A-Za-z_:][-\w:.]*)\s*=\s*\"([^\"]*)\"")
PAGER_BODY_RE = re.compile(r"\A\s*<span>([^<]+)</span>\s*<strong>(.+?)</strong>\s*\Z", re.S)
RETIRED_PAGER_MARKUP = (
    "lesson-pager", "pager-link",
    'class="prev"', 'class="next"', 'class="dir"', 'class="name"',
)

# The theme toggle, verbatim. The label is STATIC and direction-neutral, so it
# is accurate in both states; a label rewritten per state has to pick between
# describing the current theme and the next one, and the courses picked
# differently. type="button" keeps it out of any form submission.
THEME_TOGGLE_MARKUP = (
    '<button class="icon-btn" id="themeToggle" type="button" '
    'aria-label="Toggle light and dark theme" title="Toggle theme">'
)
# An accessible name written from script, with the value expression captured.
# Only a THEME label is a violation: a lesson widget that labels itself from
# script is ordinary, but the theme toggle's name must not depend on state.
SCRIPTED_LABEL_RE = re.compile(
    r"""(?:setAttribute\s*\(\s*(['"])aria-label\1\s*,|\.\s*ariaLabel\s*=)([^;\n]*)"""
)


def stylesheet(text):
    """Every <style> block of one document, CSS comments removed.

    Comments are stripped so the prose that DOCUMENTS these conventions (the
    header comment on each page explains the two light paths and quotes the
    component-override anti-pattern) is never mistaken for a rule.
    """
    return "\n".join(
        CSS_COMMENT_RE.sub(" ", block) for block in STYLE_BLOCK_RE.findall(text)
    )


def css_rules(css):
    """(enclosing at-rule preludes, selector, declarations) for every rule."""
    rules = []
    stack = []
    buffer = []
    for char in css:
        if char == "{":
            stack.append(re.sub(r"\s+", " ", "".join(buffer)).strip())
            buffer = []
        elif char == "}":
            if stack:
                rules.append((tuple(stack[:-1]), stack.pop(), "".join(buffer)))
            buffer = []
        else:
            buffer.append(char)
    return rules


def css_variables(declarations):
    return {
        name: re.sub(r"\s+", " ", value).strip()
        for name, value in CSS_VARIABLE_RE.findall(declarations)
    }


def light_paths(text):
    """{"toggle": [...], "media": [...]} -- the custom properties each path sets."""
    paths = {"toggle": [], "media": []}
    for context, selector, declarations in css_rules(stylesheet(text)):
        if not context and selector == LIGHT_TOGGLE_SELECTOR:
            paths["toggle"].append(css_variables(declarations))
        elif (context == (LIGHT_MEDIA_PRELUDE,)
              and selector == LIGHT_MEDIA_SELECTOR):
            paths["media"].append(css_variables(declarations))
    return paths


def light_component_overrides(text):
    """Selectors that scope a component to the toggle path only."""
    return [
        selector
        for _context, selector, _declarations in css_rules(stylesheet(text))
        if LIGHT_TOGGLE_SELECTOR in selector and selector != LIGHT_TOGGLE_SELECTOR
    ]


def pager_anchors(text):
    """[(attributes, inner markup)] of one page's lesson pager, in document order."""
    anchors = []
    for inner in LESSON_NAV_RE.findall(text):
        for attributes, body in PAGER_ANCHOR_RE.findall(inner):
            anchors.append((dict(ATTRIBUTE_RE.findall(attributes)), body))
    return anchors


class TestPinnedConventions(SiteFixture):
    """One library, one pager, one light palette, one theme toggle.

    Every assertion here is about a convention that CROSSES course boundaries.
    A course is free to have its own lessons, its own charts and its own
    layout; it is not free to have its own version of the navigation control, of
    the light theme, or of the theme toggle, because a reader walks from one
    course into the next and those three are what they carry with them.

    These fail loudly on purpose. A future course that reintroduces its own
    variant should fail here, in a suite that names the pinned form, rather than
    pass review because the variant looks fine inside its own course.
    """

    def pages(self):
        return [(str(doc.path.relative_to(REPO_ROOT)), doc) for doc in self.documents]

    # -- the light palette --------------------------------------------------

    def test_every_page_declares_both_light_paths(self):
        """A page with one light path is a page that is light for half its readers.

        The toggle path serves the reader who chose light; the media path serves
        the reader who never touched the toggle and whose OS is light. Course 3
        arrived with the toggle path only -- no
        @media (prefers-color-scheme: light) block at all -- which reads as
        "light mode is broken" to everyone in the second group.
        """
        for page, doc in self.pages():
            with self.subTest(page=page):
                paths = light_paths(doc.text)
                self.assertEqual(
                    1,
                    len(paths["toggle"]),
                    "expected exactly one `%s { … }` block, found %d"
                    % (LIGHT_TOGGLE_SELECTOR, len(paths["toggle"])),
                )
                self.assertEqual(
                    1,
                    len(paths["media"]),
                    "expected exactly one `%s { %s { … } }` block, found %d"
                    % (LIGHT_MEDIA_PRELUDE, LIGHT_MEDIA_SELECTOR, len(paths["media"])),
                )

    def test_both_light_paths_declare_identical_values(self):
        """The two paths are one palette written twice; they may not disagree."""
        for page, doc in self.pages():
            paths = light_paths(doc.text)
            if not (paths["toggle"] and paths["media"]):
                continue  # reported by test_every_page_declares_both_light_paths
            toggle, media = paths["toggle"][0], paths["media"][0]
            for token in sorted(set(toggle) | set(media)):
                with self.subTest(page=page, token=token):
                    self.assertEqual(
                        toggle.get(token),
                        media.get(token),
                        "%s differs between the toggle path and the system-preference "
                        "path; the two are the same palette and must be "
                        "value-identical" % token,
                    )

    def test_light_palette_values_are_the_pinned_ones(self):
        """The palette is pinned, and the pinned values are contrast-checked.

        A page declares only the tokens it uses, so a missing token is fine. A
        token declared with its own slightly different value is not: those are
        the "improvements" that put four different --muted values in one library
        and drop a heading below 4.5:1 on one page of it.
        """
        for page, doc in self.pages():
            for label, blocks in sorted(light_paths(doc.text).items()):
                for declarations in blocks:
                    for token, value in sorted(declarations.items()):
                        if token not in LIGHT_PALETTE:
                            continue
                        with self.subTest(page=page, path=label, token=token):
                            self.assertEqual(
                                LIGHT_PALETTE[token],
                                value,
                                "%s is pinned; do not re-tune it per page" % token,
                            )

    def test_light_palette_is_identical_across_every_page_that_declares_it(self):
        """Same token, same value, library-wide -- including page-local tokens.

        LIGHT_PALETTE pins the shared tokens. A course that adds one of its own
        (a chart grid line, a code surface) is still bound by this: the second
        page to declare that token must declare the same value, or the library
        has two light themes wearing one name.
        """
        values = {}
        for page, doc in self.pages():
            for blocks in light_paths(doc.text).values():
                for declarations in blocks:
                    for token, value in declarations.items():
                        values.setdefault(token, {}).setdefault(value, []).append(page)
        for token, seen in sorted(values.items()):
            with self.subTest(token=token):
                self.assertEqual(
                    1,
                    len(seen),
                    "%s has %d different light values across the library: %s"
                    % (
                        token,
                        len(seen),
                        "; ".join(
                            "%s on %d page(s) (e.g. %s)" % (value, len(pages), pages[0])
                            for value, pages in sorted(seen.items())
                        ),
                    ),
                )

    def test_no_component_is_scoped_to_the_toggle_path_alone(self):
        """`[data-theme="light"] .foo` is how the two light paths drift apart.

        Such a rule applies when the reader clicked the toggle and NOT when
        their OS is light, so that reader gets the light ground with dark-theme
        ink on that component alone. Components read tokens; only the palette
        blocks name a theme.
        """
        for page, doc in self.pages():
            with self.subTest(page=page):
                self.assertEqual(
                    [],
                    light_component_overrides(doc.text),
                    "component-level light override(s); move the value into the "
                    "palette tokens both light paths declare",
                )

    # -- the lesson pager ---------------------------------------------------

    def test_every_lesson_carries_the_pinned_pager_markup(self):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        for url in sorted(LESSON_PAGES):
            doc = by_url.get(url)
            with self.subTest(lesson=url):
                self.assertIsNotNone(doc, "%s is not published" % url)
                self.assertEqual(
                    1,
                    doc.text.count(LESSON_NAV_MARKUP),
                    "expected exactly one pager opening tag, verbatim:\n  %s"
                    % LESSON_NAV_MARKUP,
                )

    def test_pager_anchors_use_the_pinned_class_names(self):
        """Exactly lesson-link prev / lesson-link next, and nothing else."""
        by_url = {served_path(doc.path): doc for doc in self.documents}
        for title, home, slugs in COURSES:
            urls = [lesson_url(home, slug) for slug in slugs]
            for index, url in enumerate(urls):
                doc = by_url.get(url)
                if doc is None:
                    continue  # reported by TestPublishedLayout
                anchors = pager_anchors(doc.text)
                first, last = index == 0, index == len(urls) - 1
                expected = ([] if first else ["lesson-link prev"]) + ["lesson-link next"]
                with self.subTest(course=title, lesson=url):
                    self.assertEqual(
                        expected,
                        [attrs.get("class") for attrs, _body in anchors],
                        "the pager's anchors must be exactly %s, in that order. "
                        "The first lesson omits the prev anchor entirely rather "
                        "than shipping a disabled one." % expected,
                    )
                for attrs, body in anchors:
                    with self.subTest(course=title, lesson=url, anchor=attrs.get("class")):
                        self.assertEqual(
                            set(),
                            set(attrs) - {"class", "href", "rel"},
                            "a pager anchor carries only class, href and rel",
                        )
                        self.assertRegex(
                            body,
                            PAGER_BODY_RE,
                            "a pager anchor is <span>direction</span> then "
                            "<strong>label</strong>; no other elements",
                        )

    def test_pager_rel_asserts_only_true_document_relationships(self):
        """rel=prev/next inside a course; no rel on the link out of one.

        The last lesson's forward link points at the COURSE HOME, which is not
        the next document in the sequence, so rel="next" there asserts a
        relationship that is not true.
        """
        by_url = {served_path(doc.path): doc for doc in self.documents}
        for title, home, slugs in COURSES:
            urls = [lesson_url(home, slug) for slug in slugs]
            for index, url in enumerate(urls):
                doc = by_url.get(url)
                if doc is None:
                    continue
                for attrs, _body in pager_anchors(doc.text):
                    direction = (attrs.get("class") or "").split()[-1]
                    terminal = direction == "next" and index == len(urls) - 1
                    with self.subTest(course=title, lesson=url, anchor=direction):
                        if terminal:
                            self.assertNotIn(
                                "rel",
                                attrs,
                                "the last lesson's forward link goes to the course "
                                "home (%s); it must carry no rel attribute" % home,
                            )
                            self.assertEqual(
                                "../", attrs.get("href"), "it points at the course home"
                            )
                        else:
                            self.assertEqual(
                                direction,
                                attrs.get("rel"),
                                'a pager anchor inside the sequence declares rel="%s"'
                                % direction,
                            )

    def test_no_page_ships_a_retired_pager_variant(self):
        """The three families that shipped separately must not come back."""
        for page, doc in self.pages():
            for markup in RETIRED_PAGER_MARKUP:
                with self.subTest(page=page, retired=markup):
                    self.assertNotIn(
                        markup,
                        doc.text,
                        "retired pager markup %r; the pinned pager is %s with "
                        "lesson-link prev / lesson-link next anchors"
                        % (markup, LESSON_NAV_MARKUP),
                    )

    # -- the theme toggle ---------------------------------------------------

    def test_every_page_ships_the_pinned_theme_toggle(self):
        for page, doc in self.pages():
            with self.subTest(page=page):
                self.assertEqual(
                    1,
                    doc.text.count(THEME_TOGGLE_MARKUP),
                    "expected exactly one theme toggle, verbatim:\n  %s"
                    % THEME_TOGGLE_MARKUP,
                )

    def test_pinned_convention_scanners_are_not_inert(self):
        """Each scanner above must actually detect the variant it forbids.

        A guard that cannot fail is worse than no guard: it reads as coverage.
        Every helper is handed the defect it exists to catch, and one benign
        near-miss, so a regex that quietly stops matching is caught here.
        """
        drifted = (
            "<style>[data-theme=\"light\"] { --bg: #eef4f8; }"
            "@media (prefers-color-scheme: light) {"
            " :root:not([data-theme=\"dark\"]) { --bg: #edf4f8; } }</style>"
        )
        paths = light_paths(drifted)
        self.assertEqual([{"--bg": "#eef4f8"}], paths["toggle"])
        self.assertEqual([{"--bg": "#edf4f8"}], paths["media"])

        self.assertEqual(
            ['[data-theme="light"] .rule-output'],
            light_component_overrides(
                '<style>[data-theme="light"] .rule-output { color: #111; }</style>'
            ),
            "a component scoped to the toggle path alone must be reported",
        )
        self.assertEqual(
            [],
            light_component_overrides(
                "<style>/* never write [data-theme=\"light\"] .foo {…} */"
                '[data-theme="light"] { --bg: #edf4f8; }</style>'
            ),
            "documenting the anti-pattern in a comment is not committing it",
        )

        anchors = pager_anchors(
            '<nav class="lesson-nav" aria-label="Lesson navigation">'
            '<a class="lesson-link prev" href="../a/" rel="prev">'
            "<span>Previous lesson</span><strong>01 &middot; A</strong></a>"
            '<a class="lesson-link next" href="../">'
            "<span>Next</span><strong>Course home</strong></a></nav>"
        )
        self.assertEqual(
            ["lesson-link prev", "lesson-link next"],
            [attrs["class"] for attrs, _body in anchors],
        )
        self.assertNotIn("rel", anchors[1][0], "the terminal link carries no rel")
        for _attrs, body in anchors:
            self.assertRegex(body, PAGER_BODY_RE)

        themed = 'x.setAttribute("aria-label", light ? "Switch to the dark theme" : "y");'
        match = SCRIPTED_LABEL_RE.search(themed)
        self.assertIsNotNone(match, "a scripted aria-label must be found")
        self.assertRegex(match.group(2), THEMEISH_KEY_RE)
        other = 'chart.setAttribute("aria-label", "Payoff at expiration");'
        match = SCRIPTED_LABEL_RE.search(other)
        self.assertIsNotNone(match)
        self.assertNotRegex(
            match.group(2),
            THEMEISH_KEY_RE,
            "labelling a lesson widget from script is ordinary and must not fail",
        )

    def test_no_page_rewrites_the_toggle_label_from_script(self):
        """A static label is accurate in both states; a scripted one is a fork.

        "Switch to the dark theme" and "Toggle light and dark theme" are two
        different contracts with a screen reader, and pages that rewrote the
        label chose differently -- some named the next state, some the current
        one. The pinned label is direction-neutral, so nothing has to be
        rewritten and nothing can disagree.
        """
        for page, doc in self.pages():
            scripted = [
                match.group(0).strip()
                for match in SCRIPTED_LABEL_RE.finditer(doc.text)
                if THEMEISH_KEY_RE.search(match.group(2) or "")
            ]
            with self.subTest(page=page):
                self.assertEqual(
                    [],
                    scripted,
                    "the theme control's accessible name is written from script. "
                    "The pinned toggle carries a static, direction-neutral "
                    "aria-label plus title and needs no runtime rewrite.",
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
