#!/usr/bin/env python3
"""Machine-checkable form of the learn.geterdone.io site invariants.

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
  * The site is a subject-agnostic LIBRARY OF PATHS now. A path is an ordered
    sequence of courses on one subject; the trading path is the first one, and
    mathematics, computer science and philosophy are planned. So the shared
    chrome -- the site index at / and the path page at /paths/<subject>/ -- is
    tested for the things that must hold for ANY subject, and the trading
    vocabulary is allowed only on the course and lesson pages themselves.
  * Every invariant that used to be "the course" is stated per course and
    asserted for every one of them. The
    theme localStorage key is checked site-wide for exactly that reason: courses
    that each persist the reader's theme under their own key is a bug that looks
    like nothing until a reader crosses from one course to the next.
  * Seven courses share one origin, one visual system and one navigation model,
    so the conventions that cross course boundaries -- the lesson pager markup,
    the light palette token VALUES, and the theme-toggle button -- are pinned in
    TestPinnedConventions. Each course inventing its own variant is invisible in
    review (every variant works inside its own course) and visible to a reader
    the moment they cross from one course into the next.
  * The path page is NEITHER a course home NOR a lesson. It is declared on its
    own line (PATH_PAGE) and every per-course collection is built by excluding
    it, because it is two segments deep exactly like a lesson is and a guard
    that classifies by URL SHAPE would demand a lesson pager on it.
"""

import html
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

# The published URL space:
#
#     /                                  the site index (paths, plus course search)
#     /paths/trading/                    the trading PATH PAGE: its ordered courses
#     /market-structure/                 course 1 home, "Market Structure"
#     /market-structure/<lesson>/        course 1's seven lessons, in course order
#     /trade-setup-execution/            course 2 home, "Trade Setup and Execution"
#     /trade-setup-execution/<lesson>/   course 2's fifteen lessons, in course order
#     /options-trading/                  course 3 home, "Options Trading"
#     /options-trading/<lesson>/         course 3's sixteen lessons, in course order
#     /technical-indicators/             course 4 home, "Technical Indicators"
#     /technical-indicators/<lesson>/    course 4's sixteen lessons, in course order
#     /volume-and-order-flow/            course 5 home, "Volume and Order Flow"
#     /volume-and-order-flow/<lesson>/   course 5's sixteen lessons, in course order
#     /trading-risk-management/          course 6 home, "Trading Risk Management"
#     /trading-risk-management/<lesson>/ course 6's sixteen lessons, in course order
#     /backtesting-and-trading-systems/  course 7 home, "Backtesting and Trading Systems"
#     /backtesting-and-trading-systems/<lesson>/
#                                        course 7's sixteen lessons, in course order
#
# That is 111 HTML pages. The document root publishes exactly six further
# things, all non-HTML assets -- one exchange schema per course that ships one --
# declared separately in NON_HTML_ASSETS below.
#
# Containerfile.release, .github/workflows/{ci,pages}.yml, release/contract.json
# (acceptance.checks) and scripts/smoke.py all assert the same mapping; changing
# one without the others is how a lesson silently stops being published.
#
# Course 1 was published at /market-structure-lab/ until the library became a
# library of PATHS: the old slug named the whole site, not the course, so the
# course took its own name. The old URLs are gone, there are no redirect stubs,
# and the same is true of the seven FLAT lesson URLs course 1 published before
# that. Neither may be re-added here: a path listed below is a path that must
# exist.
#
# LESSON ORDER IS THE COURSE SEQUENCE, not alphabetical order. It is declared
# once, here, and TestLessonChain walks the prev/next pager against it, so a
# course whose pager disagrees with its own syllabus fails rather than shipping.
SITE_INDEX = "/"

# The path page. It is NEITHER a course home NOR a lesson, and no test may
# classify it as either. It is two segments deep exactly like a lesson is
# (/paths/trading/ has the same shape as /options-trading/moneyness/), so any
# guard that infers "two segments means a lesson" would sweep it into the
# per-course suites and demand a lesson pager, an owning course home, and the
# course disclaimer -- none of which a path page has or should have. It is
# therefore declared on its own line here, and every per-course collection below
# is built by EXCLUDING it rather than by matching a URL shape.
PATH_PAGE = "/paths/trading/"

# The paths layer owns this first segment. A course may never claim it, or
# /paths/ would answer for a course home and vice versa.
PATHS_PREFIX = "/paths/"

COURSE_1_HOME = "/market-structure/"
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

COURSE_4_HOME = "/technical-indicators/"
COURSE_4_LESSONS = (
    "technical-indicator-fundamentals",
    "moving-averages",
    "moving-average-crossovers",
    "relative-strength-index",
    "stochastic-oscillator",
    "macd",
    "average-directional-index",
    "average-true-range",
    "bollinger-bands",
    "keltner-channels",
    "donchian-channels",
    "rate-of-change-and-momentum",
    "indicator-divergence",
    "combining-indicators",
    "indicator-selection-by-market-regime",
    "indicator-based-trading-rules",
)

COURSE_5_HOME = "/volume-and-order-flow/"
COURSE_5_LESSONS = (
    "volume-fundamentals",
    "price-volume-relationships",
    "relative-volume-and-volume-spikes",
    "volume-confirmation",
    "on-balance-volume",
    "accumulation-distribution-and-chaikin-money-flow",
    "volume-weighted-average-price",
    "anchored-volume-weighted-average-price",
    "volume-profile",
    "value-area-poc-hvn-lvn",
    "bid-ask-spread-and-order-types",
    "time-and-sales",
    "footprint-charts-and-bid-ask-delta",
    "cumulative-volume-delta",
    "order-book-and-market-depth",
    "volume-and-order-flow-trading-rules",
)

COURSE_6_HOME = "/trading-risk-management/"
COURSE_6_LESSONS = (
    "risk-management-fundamentals",
    "account-risk-and-risk-budget",
    "risk-per-trade",
    "stop-loss-and-structural-invalidation",
    "position-sizing",
    "reward-to-risk-and-r-multiples",
    "win-rate-average-win-loss-and-expectancy",
    "losing-streaks-and-drawdown",
    "risk-of-ruin",
    "volatility-and-atr-based-risk",
    "gap-slippage-liquidity-and-execution-risk",
    "leverage-and-margin-risk",
    "correlation-concentration-and-portfolio-exposure",
    "options-risk-management",
    "daily-and-weekly-risk-limits",
    "trading-risk-plan",
)

COURSE_7_HOME = "/backtesting-and-trading-systems/"
COURSE_7_LESSONS = (
    "backtesting-fundamentals",
    "testable-trading-rules-and-hypotheses",
    "historical-data-and-data-quality",
    "survivorship-selection-and-corporate-actions",
    "timeframes-sessions-and-bar-construction",
    "signal-timing-look-ahead-bias-and-data-leakage",
    "trade-execution-simulation",
    "position-sizing-and-portfolio-accounting",
    "transaction-costs-spread-slippage-and-liquidity",
    "trade-log-equity-curve-and-drawdown",
    "performance-metrics-and-expectancy",
    "benchmarking-and-risk-adjusted-performance",
    "in-sample-validation-and-out-of-sample-data",
    "walk-forward-testing",
    "overfitting-sensitivity-monte-carlo-and-stress-testing",
    "trading-system-specification-and-backtest-report",
)

# NOTE: course 6 ships a lesson slug "position-sizing" and so does course 2, and
# course 7 ships "position-sizing-and-portfolio-accounting". Slugs are only ever
# unique WITHIN a course -- they are resolved beneath their own course home, and
# the uniqueness assertion below is per course for exactly that reason.

# (course title, course home URL, lesson slugs in course order). The order of
# this tuple IS the order of the path: index 0 is course 1. TestPathPosition
# reads it that way, so a course inserted in the wrong place fails there.
COURSES = (
    ("Market Structure", COURSE_1_HOME, COURSE_1_LESSONS),
    ("Trade Setup and Execution", COURSE_2_HOME, COURSE_2_LESSONS),
    ("Options Trading", COURSE_3_HOME, COURSE_3_LESSONS),
    ("Technical Indicators", COURSE_4_HOME, COURSE_4_LESSONS),
    ("Volume and Order Flow", COURSE_5_HOME, COURSE_5_LESSONS),
    ("Trading Risk Management", COURSE_6_HOME, COURSE_6_LESSONS),
    ("Backtesting and Trading Systems", COURSE_7_HOME, COURSE_7_LESSONS),
)

# The trading path is EIGHT courses long. Seven are published; course 8 is
# announced, holds its place in the order, and is NOT a link. The only facts
# that exist about it are its number and its name -- no lesson count, no
# description, no date -- so those are the only facts recorded here, and
# TestPathPage asserts that the page invents nothing more.
#
# Courses 5, 6 and 7 each moved OUT of this tuple and into COURSES the day their
# pages landed. That direction is one-way: an entry here is a promise with no
# page behind it, so the move happens when the pages exist, never in
# anticipation of them.
PATH_COURSE_COUNT = 8
UPCOMING_COURSES = (
    (8, "Algorithmic and Automated Trading"),
)

UNKNOWN_PATH_CHECK = "/release-smoke-unknown-path"


def lesson_url(home, slug):
    """The published URL of one lesson of the course whose home is `home`."""
    return "%s%s/" % (home, slug)


def source_of(url):
    """The file under site/ that must be published at this directory URL."""
    return url.lstrip("/") + "index.html"


# The site index and the path page are SHARED CHROME: the same frame will hold
# a mathematics path or a computer-science path without being rewritten. They
# are published pages like any other, so every whole-tree invariant applies to
# them -- but the per-course invariants do not, because neither is a course.
SHARED_CHROME_PAGES = (SITE_INDEX, PATH_PAGE)

REQUIRED_PAGES = {SITE_INDEX: "index.html", PATH_PAGE: source_of(PATH_PAGE)}
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
    "/technical-indicators/indicator-rule-schema.json":
        "technical-indicators/indicator-rule-schema.json",
    "/volume-and-order-flow/volume-order-flow-rule-schema.json":
        "volume-and-order-flow/volume-order-flow-rule-schema.json",
    "/trading-risk-management/trading-risk-plan-schema.json":
        "trading-risk-management/trading-risk-plan-schema.json",
    "/backtesting-and-trading-systems/trading-system-specification-schema.json":
        "backtesting-and-trading-systems/trading-system-specification-schema.json",
}

# Rides along inside the document root without being published content. CNAME
# is GitHub Pages' custom-domain control file (it holds learn.geterdone.io); it
# configures delivery and is not a page or an asset any lesson links to.
DELIVERY_CONTROL_FILES = frozenset({"CNAME"})

COURSE_HOMES = tuple(home for _title, home, _slugs in COURSES)

# Everything that is not shared chrome is course material -- all seven course
# homes as well as all 102 lessons. All of it teaches trading, so all of it
# carries the same disclaimer. The two chrome pages are excluded BY NAME, not by
# URL shape: /paths/trading/ looks exactly like a lesson URL.
COURSE_PAGES = {
    url: rel for url, rel in REQUIRED_PAGES.items() if url not in SHARED_CHROME_PAGES
}

# The 102 lessons alone, without any course home.
LESSON_PAGES = {url: rel for url, rel in COURSE_PAGES.items() if url not in COURSE_HOMES}

# Every page of the library persists the reader's theme under ONE localStorage
# key. Course 1 shipped "marketStructureTheme", course 2 shipped
# "market-lab-theme", course 3 arrived with a third key, "options-course-theme",
# course 4's source package arrived with a FOURTH, "technical-indicators-theme",
# course 5's arrived with a FIFTH, "vof-theme", and courses 6 and 7 arrived with
# a SIXTH and SEVENTH, "trm-theme" and "bts-theme"; with several courses on one
# origin that meant a reader's choice silently reset at every course boundary.
# Every source package so far has invented its own key, which is why this is
# checked site-wide rather than trusted. The site standardized on "learn-theme"
# everywhere. Note the check below reads storage CALL SITES, not prose:
# site/index.html names retired keys in a comment that explains the migration,
# and documenting the fix must not fail the build.
THEME_STORAGE_KEY = "learn-theme"
RETIRED_THEME_KEYS = (
    "marketStructureTheme", "market-lab-theme", "options-course-theme",
    "technical-indicators-theme", "vof-theme", "trm-theme", "bts-theme",
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
HEAD_RE = re.compile(r"<head\b[^>]*>(.*?)</head>", re.S | re.I)

PREPAINT_THEME_READ_RE = re.compile(
    r"""localStorage\s*\.\s*getItem\s*\(\s*(['"])%s\1\s*\)""" % THEME_STORAGE_KEY
)

# Every course page (every page that is not shared chrome) must keep this
# disclaimer.
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
    path page, and so are all six non-HTML assets, each checked as JSON rather
    than as a page.
    """

    def test_declared_url_space_is_the_index_the_path_page_and_the_course_tree(self):
        """Site index, path page, then a home per course and that course's lessons.

        111 URLs exactly: /, /paths/trading/, seven course homes, and
        7 + 15 + 16 + 16 + 16 + 16 + 16 lessons beneath them. The flat /<lesson>/ URLs and
        the old /market-structure-lab/ course prefix were retired without
        redirects, so a two-segment lesson path under a declared course home is
        the only shape a lesson may have; re-adding either would declare a page
        that no longer exists on disk.
        """
        expected = (
            1  # the site index
            + 1  # the path page
            + len(COURSES)
            + sum(len(slugs) for _t, _h, slugs in COURSES)
        )
        self.assertEqual(
            111,
            expected,
            "the library is 1 + 1 + 7 + 7 + 15 + 16 + 16 + 16 + 16 + 16 = 111 pages, "
            "got %d" % expected,
        )
        self.assertEqual(
            expected,
            len(REQUIRED_PAGES),
            "expected %d published URLs, got %d" % (expected, len(REQUIRED_PAGES)),
        )
        self.assertEqual(7, len(COURSES), "the library publishes seven courses")
        self.assertEqual(7, len(COURSE_1_LESSONS), "course 1 is seven lessons")
        self.assertEqual(15, len(COURSE_2_LESSONS), "course 2 is fifteen lessons")
        self.assertEqual(16, len(COURSE_3_LESSONS), "course 3 is sixteen lessons")
        self.assertEqual(16, len(COURSE_4_LESSONS), "course 4 is sixteen lessons")
        self.assertEqual(16, len(COURSE_5_LESSONS), "course 5 is sixteen lessons")
        self.assertEqual(16, len(COURSE_6_LESSONS), "course 6 is sixteen lessons")
        self.assertEqual(16, len(COURSE_7_LESSONS), "course 7 is sixteen lessons")
        for index, (title, _home, slugs) in enumerate(COURSES, start=1):
            with self.subTest(course=title):
                self.assertEqual(
                    len(set(slugs)), len(slugs), "duplicate slug in course %d" % index
                )
        for _title, home, _slugs in COURSES:
            with self.subTest(course=home):
                self.assertIn(home, REQUIRED_PAGES, "the course home must be published")
        # The path page is published, and it is neither a course home nor a
        # lesson. Stating that here means a future guard cannot quietly start
        # classifying it by URL shape: it is two segments deep exactly like a
        # lesson, and it lives under a first segment no course may take.
        self.assertIn(PATH_PAGE, REQUIRED_PAGES, "the path page must be published")
        self.assertNotIn(PATH_PAGE, COURSE_HOMES, "the path page is not a course home")
        self.assertNotIn(PATH_PAGE, LESSON_PAGES, "the path page is not a lesson")
        self.assertNotIn(PATH_PAGE, COURSE_PAGES, "the path page is not course material")
        self.assertTrue(
            PATH_PAGE.startswith(PATHS_PREFIX),
            "the path page lives under %s" % PATHS_PREFIX,
        )
        for _title, home, _slugs in COURSES:
            with self.subTest(course=home):
                self.assertFalse(
                    home.startswith(PATHS_PREFIX) or PATHS_PREFIX.startswith(home),
                    "%s collides with the paths layer at %s" % (home, PATHS_PREFIX),
                )
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

        All six published schemas are declared here, one line each. Every new
        one is the moment the temptation appears to relax an HTML assertion so a
        JSON file can slip through the page sweep; the fix for "this check cannot
        apply to that file" is another declaration, never a weaker check.
        """
        self.assertEqual(
            6,
            len(NON_HTML_ASSETS),
            "all six published JSON schemas must stay declared: course 2's "
            "trade journal exchange schema, course 3's options trade plan "
            "schema, course 4's indicator rule schema, course 5's volume "
            "and order flow rule schema, course 6's trading risk plan schema, "
            "and course 7's trading system specification schema",
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
            "</head><body><a href=\"./market-structure/\">go</a>"
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
        """Every course page teaches trading and must say so.

        That is all seven course homes as well as all 102 lessons: a course home
        is not an exempt landing page, it sells the same material.

        The two shared-chrome pages are excluded, and excluded BY NAME. They are
        not trading material -- the same frame is meant to hold a mathematics
        path next -- so a trading disclaimer is not theirs to carry, and a
        subject-specific notice on a subject-agnostic page is precisely what
        TestSharedChromeIsSubjectAgnostic forbids.

        Checked two ways on purpose: every DECLARED course page must be present (a
        lesson that vanished cannot pass by not being iterated), and every
        PUBLISHED page that is not chrome must carry the disclaimer (a page added
        without touching REQUIRED_PAGES is still covered).
        """
        by_url = {served_path(doc.path): doc for doc in self.documents}
        missing = sorted(set(COURSE_PAGES) - set(by_url))
        self.assertEqual(
            [],
            missing,
            "declared course pages are not published: %s" % missing,
        )
        course_pages = [
            doc
            for url, doc in sorted(by_url.items())
            if url not in SHARED_CHROME_PAGES
        ]
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

    Course 1 shipped "marketStructureTheme", course 2 shipped "market-lab-theme",
    course 3 arrived carrying "options-course-theme", course 4 arrived with
    "technical-indicators-theme" and course 5 with "vof-theme". Each worked
    perfectly inside its own course and broke the moment they shared an origin:
    the reader's explicit light/dark choice silently reset at the course
    boundary, on a site whose whole point is that a reader walks from course 1
    through course 5. The site now uses "learn-theme" everywhere, and
    "everywhere" is the invariant -- the NEXT course package to quietly invent
    its own key must fail here rather than at a reader's expense.
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
        """The read must be in <head>, not merely somewhere in the document.

        "Before paint" is a claim about POSITION. A page that reads the key from
        a script at the end of <body> satisfies "reads the key" and still paints
        the wrong theme first and snaps -- the exact defect course 1 shipped
        with. Asserting against the whole document could never catch it, so
        assert against the head.
        """
        for doc in self.documents:
            with self.subTest(page=str(doc.path.relative_to(REPO_ROOT))):
                head = HEAD_RE.search(doc.text)
                self.assertIsNotNone(
                    head, "page has no <head> to place the pre-paint script in"
                )
                self.assertRegex(
                    head.group(1),
                    PREPAINT_THEME_READ_RE,
                    "page does not read localStorage[%r] inside <head>; every "
                    "page applies the stored theme before first paint, or the "
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
# The library is subject-agnostic
# ---------------------------------------------------------------------------
# The site is a LIBRARY OF PATHS that currently holds one path. Mathematics,
# computer science and philosophy are planned, and they will reuse this frame
# unchanged. So two pages -- the site index and the path page -- are shared
# chrome, and the checks below state the properties that must survive a subject
# the site does not have yet.

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
SCRIPT_OR_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
ANCHOR_RE = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.S | re.I)
ELEMENT_RE_CACHE = {}

# A risk / disclaimer notice, marked as such by its class. It is excluded from
# the chrome sweep on purpose: a notice is attached to the COURSES a page shows,
# not to the frame around them. A path of trading courses owes its reader a
# trading risk notice; a mathematics path will carry a different one or none,
# and neither fact says anything about whether the frame assumes a subject.
NOTICE_ELEMENT_RE = re.compile(
    r"""<(p|div|section|aside)\b[^>]*class="[^"]*\brisk\b[^"]*"[^>]*>.*?</\1>""",
    re.S | re.I,
)


def elements(markup, tag):
    """The outer markup of every non-nested <tag>...</tag> in the document."""
    pattern = ELEMENT_RE_CACHE.get(tag)
    if pattern is None:
        pattern = ELEMENT_RE_CACHE[tag] = re.compile(
            r"<%s\b[^>]*>.*?</%s>" % (tag, tag), re.S | re.I
        )
    return pattern.findall(markup)


def visible_text(markup):
    """Readable copy: no comments, no script or style, no tags, entities resolved.

    Comments are dropped deliberately. A comment that DOCUMENTS one of the rules
    below ("never write 'the path' here") is documentation, not copy, and the
    build must not punish a page for explaining its own convention -- the same
    reasoning TestThemeKey applies to storage call sites versus prose.
    """
    markup = COMMENT_RE.sub(" ", markup)
    markup = SCRIPT_OR_STYLE_RE.sub(" ", markup)
    return re.sub(r"\s+", " ", html.unescape(TAG_RE.sub(" ", markup))).strip()


def anchor_texts(markup):
    """The readable text of every <a> in the document."""
    return [visible_text(body) for _attrs, body in ANCHOR_RE.findall(markup)]


def footer_markup(text):
    return "\n".join(elements(text, "footer"))


def chrome_frame(text):
    """The masthead and the footer, minus any subject-scoped notice.

    That is the part of a shared page which will be byte-identical on the next
    path added to this library: brand, primary navigation, the licence and
    identity lines. If a subject leaks anywhere, it leaks here first.
    """
    frame = "\n".join(elements(text, "header") + elements(text, "footer"))
    return visible_text(NOTICE_ELEMENT_RE.sub(" ", frame))


def metadata_text(doc):
    """<title> plus every <meta content> the page declares, as one string."""
    values = [doc.title or "", doc.description or ""]
    for match in re.finditer(r"<meta\b[^>]*>", doc.text, re.I):
        content = re.search(r'content="([^"]*)"', match.group(0))
        if content:
            values.append(html.unescape(content.group(1)))
    return " ".join(values)


# Vocabulary that only makes sense if the subject is TRADING. The list is short
# and made of JARGON on purpose, and the two exclusions matter as much as the
# entries:
#
#   * The subject's NAME is not here. "trading", "trade", "market" and "course"
#     are absent, because the trading path is called Trading, its courses are
#     called "Options Trading" and "Trade Setup and Execution", and chrome that
#     names the subject of the path it is currently showing is displaying its
#     DATA, not assuming a subject. Banning the word would make the correct page
#     unwritable.
#   * Ordinary English that trading happens to reuse is not here either
#     ("position", "value", "risk", "signal", "chart"), because a mathematics or
#     computer-science path will legitimately use every one of them in the same
#     frame.
#
# What remains is vocabulary with no meaning outside speculation on markets:
# instruments, order handling, chart-reading technique, and the promise a
# trading site makes and a learning library must not. If one of these appears in
# the frame, that frame cannot be reused for the next subject as it stands.
#
# The SCOPE is the frame, not the page, and that is a deliberate line too. Both
# chrome pages DISPLAY trading data -- a path card, a course list, course titles
# ("Backtesting and Trading Systems" is a course NAME, and "backtest" is on the
# list below) -- and displaying a subject's catalog is the job. What must not
# assume a subject is the masthead, the navigation and the footer, which the
# next path inherits unchanged. So chrome_frame() sweeps exactly those, minus
# any notice marked class="risk".
TRADING_VOCABULARY = (
    "candlestick",
    "ticker",
    "broker",
    "portfolio",
    "stop-loss",
    "position sizing",
    "backtest",
    "trade signal",
)

# The site index shows MANY paths (one today, more being written), so its copy
# must never speak of "the path" as though there were one. This is a phrase, not
# a word: "a path", "each path", "paths" and "the path page" are all correct and
# must keep passing, which is why the check is anchored on the definite article
# followed by the bare noun.
SINGULAR_PATH_PHRASE_RE = re.compile(r"(?i)\bthe\s+path\b(?!\s+page\b)")


class TestSharedChromeIsSubjectAgnostic(SiteFixture):
    """The frame must not assume the subject is trading.

    The site index and the path page are the two pages a second subject will
    reuse: the index lists every path, and the path page is the template the
    mathematics path will be written from. Course and lesson pages are exempt --
    they ARE the trading material, and a lesson that avoided trading vocabulary
    would be a broken lesson.
    """

    def chrome_documents(self):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        pages = []
        for url in SHARED_CHROME_PAGES:
            doc = by_url.get(url)
            self.assertIsNotNone(doc, "%s is not published" % url)
            pages.append((url, doc))
        return pages

    def test_shared_chrome_frame_uses_no_trading_vocabulary(self):
        for url, doc in self.chrome_documents():
            frame = chrome_frame(doc.text).lower()
            for word in TRADING_VOCABULARY:
                with self.subTest(page=url, word=word):
                    self.assertNotIn(
                        word,
                        frame,
                        "the masthead/footer frame of %s uses trading vocabulary "
                        "(%r). This frame is reused verbatim by the next path in "
                        "the library -- mathematics, computer science -- so it "
                        "must describe a LIBRARY, not a subject. Subject-specific "
                        "wording belongs on the course and lesson pages, or "
                        "inside a notice marked class=\"risk\", which is scoped to "
                        "the courses the page lists and is not swept here."
                        % (url, word),
                    )

    def test_site_index_metadata_names_no_subject_vocabulary(self):
        """The index is the front door of the whole library, not of one path.

        Its <title> and <meta> copy are what a search engine and a link preview
        show for the SITE. A path page's own title and description name the
        subject it presents, which is correct and is why only the index's
        metadata is swept here.
        """
        by_url = {served_path(doc.path): doc for doc in self.documents}
        doc = by_url.get(SITE_INDEX)
        self.assertIsNotNone(doc, "the site index is not published")
        metadata = metadata_text(doc).lower()
        for word in TRADING_VOCABULARY:
            with self.subTest(word=word):
                self.assertNotIn(
                    word, metadata, "the site index's metadata assumes a subject"
                )

    def test_site_index_copy_never_says_the_path(self):
        """One index, many paths: "the path" presumes there is only one.

        The index held a single ordered path before the paths layer existed, and
        its copy said so. Now a path is one row of a catalog, so the copy has to
        read "a path" / "each path" / "paths". Comments are not copy (see
        visible_text), so a note explaining this rule does not fail the build.
        """
        by_url = {served_path(doc.path): doc for doc in self.documents}
        doc = by_url.get(SITE_INDEX)
        self.assertIsNotNone(doc, "the site index is not published")
        copy = visible_text(doc.text) + " " + metadata_text(doc)
        found = sorted({m.group(0) for m in SINGULAR_PATH_PHRASE_RE.finditer(copy)})
        self.assertEqual(
            [],
            found,
            "the site index copy says %s. The index lists paths in the plural; "
            "write \"a path\", \"each path\" or \"paths\" instead." % found,
        )

    def test_chrome_scanners_are_not_inert(self):
        """The two scanners above must detect what they forbid, and only that."""
        planted = (
            '<header><nav><a href="./">Candlestick basics</a></nav></header>'
            "<footer><p>Ask your broker.</p></footer>"
        )
        frame = chrome_frame(planted).lower()
        self.assertIn("candlestick", frame)
        self.assertIn("broker", frame)

        scoped = (
            "<footer>"
            '<p class="risk">Trading carries the risk of losing money; check with '
            "your broker.</p>"
            "<p>&copy; 2026 dmedellin</p>"
            "</footer>"
        )
        self.assertNotIn(
            "broker",
            chrome_frame(scoped).lower(),
            "a notice marked class=risk is scoped to the courses it describes",
        )

        documented = (
            "<footer><!-- never write 'the path' here: the index lists paths -->"
            "<p>Pick a path and take its courses in order.</p></footer>"
        )
        self.assertEqual(
            [],
            SINGULAR_PATH_PHRASE_RE.findall(visible_text(documented)),
            "documenting the rule in a comment is not breaking it",
        )
        self.assertTrue(
            SINGULAR_PATH_PHRASE_RE.search("Open the path and start at course 1."),
            "the singular-path scanner must actually match",
        )
        self.assertFalse(
            SINGULAR_PATH_PHRASE_RE.search("Every path is an ordered sequence."),
            "the plural and the indefinite article are correct copy",
        )
        self.assertFalse(
            SINGULAR_PATH_PHRASE_RE.search("Listed on the path page."),
            '"the path page" names this site\'s page type, not a single path',
        )


class TestFooterSiteIdentity(SiteFixture):
    """Every footer names this site, and names it at the right host.

    geterdone.io is a SEPARATE live site that this project does not control;
    learn.geterdone.io is the library. A footer link to the apex sends the reader
    off this property from every page in the library at once, and it is the kind
    of defect that survives forever because a link that 200s never looks broken.
    The canonical tag is already pinned to the same host (see
    TestPageMetadata.test_canonical_never_claims_the_apex); this closes the other
    half, the visible link a reader can click. The rule is about WHERE a footer
    link points: a footer that names no host at all is not this test's business,
    and test_footer_scanner_is_not_inert keeps the check honest instead.
    """

    def footer_links(self, doc):
        links = []
        for attrs, _body in ANCHOR_RE.findall(footer_markup(doc.text)):
            match = re.search(r'href="([^"]*)"', attrs)
            if match:
                links.append(html.unescape(match.group(1)).strip())
        return links

    def test_no_footer_links_to_another_geterdone_host(self):
        for doc in self.documents:
            page = str(doc.path.relative_to(REPO_ROOT))
            for href in self.footer_links(doc):
                host = (urllib.parse.urlsplit(href).hostname or "").lower()
                if not host or not (
                    host == "geterdone.io" or host.endswith(".geterdone.io")
                ):
                    continue
                with self.subTest(page=page, href=href):
                    self.assertEqual(
                        CANONICAL_HOST,
                        host,
                        "the footer links to %s. This library lives at %s; %s is a "
                        "different site this project does not control, so a footer "
                        "on every page pointing there walks the reader off the "
                        "library." % (href, CANONICAL_ORIGIN, host),
                    )

    def test_footer_scanner_is_not_inert(self):
        """A guard that cannot fail is worse than no guard: it reads as coverage.

        The rule above is about WHERE a footer link points, not about whether one
        exists -- some lessons carry no site link at all, and that is a different
        question. So the scanner is handed the defect it exists to catch, the
        correct link it must accept, and a footer-shaped near miss.
        """
        planted = (
            "<html><body><main>"
            '<p><a href="https://geterdone.io">apex, outside the footer</a></p>'
            "</main><footer>"
            '<p><a href="https://geterdone.io">geterdone.io</a></p>'
            "</footer></body></html>"
        )

        class _Doc:
            text = planted

        hosts = [
            (urllib.parse.urlsplit(href).hostname or "").lower()
            for href in self.footer_links(_Doc)
        ]
        self.assertEqual(
            ["geterdone.io"],
            hosts,
            "the scanner must read the FOOTER's links, and only the footer's",
        )
        good = "<footer><p><a href=\"%s\">%s</a></p></footer>" % (
            CANONICAL_ORIGIN,
            CANONICAL_HOST,
        )

        class _Good:
            text = good

        self.assertEqual(
            [CANONICAL_HOST],
            [
                (urllib.parse.urlsplit(href).hostname or "").lower()
                for href in self.footer_links(_Good)
            ],
        )


class TestPathPosition(SiteFixture):
    """A course knows where it sits in the path, and how to leave in either direction.

    The library is a path, not a shelf: course 3 assumes course 2. A reader who
    lands on a course home from a search result has to be told which number they
    are holding and what comes before and after it, or the ordering that the
    whole path page exists to express is invisible one click deeper.
    """

    def course_pager(self, doc, direction):
        return [href for rel, href, _line in doc.pager if rel == direction]

    def test_every_course_home_declares_its_position_in_the_path(self):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        for index, (title, home, _slugs) in enumerate(COURSES, start=1):
            doc = by_url.get(home)
            with self.subTest(course=title):
                self.assertIsNotNone(doc, "%s is not published" % home)
                position = re.compile(
                    r"(?i)\bcourse\s+0?%d\s+of\s+%d\b" % (index, PATH_COURSE_COUNT)
                )
                self.assertRegex(
                    visible_text(doc.text),
                    position,
                    "%s does not say it is course %d of %d. The path is eight "
                    "courses long including the three that are not published "
                    "yet, and a course home that states a position out of seven "
                    "would describe a path that does not exist."
                    % (home, index, PATH_COURSE_COUNT),
                )

    def test_course_pager_points_at_the_adjacent_course_homes(self):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        homes = [home for _title, home, _slugs in COURSES]
        for index, (title, home, _slugs) in enumerate(COURSES):
            doc = by_url.get(home)
            with self.subTest(course=title):
                self.assertIsNotNone(doc, "%s is not published" % home)
                previous = self.course_pager(doc, "prev")
                following = self.course_pager(doc, "next")

                if index == 0:
                    self.assertEqual(
                        [],
                        previous,
                        "course 1 starts the path; nothing precedes it, so it "
                        "ships the forward half of the pager alone rather than a "
                        "disabled backward one",
                    )
                else:
                    self.assertEqual(
                        1,
                        len(previous),
                        'expected exactly one <a rel="prev"> on %s, got %d'
                        % (home, len(previous)),
                    )
                    self.assertEqual(
                        homes[index - 1],
                        urllib.parse.urljoin(home, previous[0]),
                        "prev must point at course %d's home" % index,
                    )

                if index == len(homes) - 1:
                    self.assertEqual(
                        [],
                        following,
                        "course %d is the last PUBLISHED course: course %d is "
                        "announced but has no page, so there is nothing to link "
                        "forward to. An upcoming course is listed on the path "
                        "page and is never a link."
                        % (len(homes), len(homes) + 1),
                    )
                else:
                    self.assertEqual(
                        1,
                        len(following),
                        'expected exactly one <a rel="next"> on %s, got %d'
                        % (home, len(following)),
                    )
                    self.assertEqual(
                        homes[index + 1],
                        urllib.parse.urljoin(home, following[0]),
                        "next must point at course %d's home" % (index + 2),
                    )

    def test_course_pager_targets_are_published_pages(self):
        """The href has to resolve to a real page, not merely to the right string."""
        by_url = {served_path(doc.path): doc for doc in self.documents}
        for title, home, _slugs in COURSES:
            doc = by_url.get(home)
            if doc is None:
                continue  # reported above
            for direction in ("prev", "next"):
                for href in self.course_pager(doc, direction):
                    target = urllib.parse.urljoin(home, href)
                    with self.subTest(course=title, rel=direction, href=href):
                        self.assertIn(
                            target,
                            REQUIRED_PAGES,
                            "the course pager points at %s, which the site does "
                            "not publish" % target,
                        )
                        self.assertTrue(
                            (SITE_ROOT / REQUIRED_PAGES[target]).is_file(),
                            "%s is declared but missing on disk" % target,
                        )


class TestPathPage(SiteFixture):
    """The path page is the ordered spine of one subject.

    It is the only page that shows the WHOLE path: seven published courses that
    link to their homes, and one announced course that holds its place in the
    order without pretending to be openable. Both halves are asserted, because
    each fails in its own way -- a missing link strands a published course, and
    an upcoming course rendered as a link is a 404 with a promise attached.
    """

    def path_document(self):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        doc = by_url.get(PATH_PAGE)
        self.assertIsNotNone(doc, "%s is not published" % PATH_PAGE)
        return doc

    def test_the_path_page_links_to_every_published_course_home(self):
        doc = self.path_document()
        linked = {
            urllib.parse.urljoin(PATH_PAGE, value.split("#", 1)[0])
            for tag, attr, value, _line in doc.urls
            if tag == "a" and attr == "href" and is_internal_relative(value)
        }
        missing = [home for _title, home, _slugs in COURSES if home not in linked]
        self.assertEqual(
            [], missing, "%s does not link to %s" % (PATH_PAGE, missing)
        )

    def test_the_site_index_links_to_the_path_page(self):
        """The index is how a reader reaches a path at all."""
        by_url = {served_path(doc.path): doc for doc in self.documents}
        doc = by_url.get(SITE_INDEX)
        self.assertIsNotNone(doc, "the site index is not published")
        linked = {
            urllib.parse.urljoin(SITE_INDEX, value.split("#", 1)[0])
            for tag, attr, value, _line in doc.urls
            if tag == "a" and attr == "href" and is_internal_relative(value)
        }
        self.assertIn(
            PATH_PAGE,
            linked,
            "the site index does not link to %s; a path nothing links to is a "
            "path nobody can open" % PATH_PAGE,
        )

    def test_all_eight_courses_appear_in_path_order(self):
        doc = self.path_document()
        copy = visible_text(doc.text)
        expected = [title for _n, title in UPCOMING_COURSES]
        names = [title for title, _home, _slugs in COURSES] + expected
        self.assertEqual(
            PATH_COURSE_COUNT,
            len(names),
            "the path is %d courses long" % PATH_COURSE_COUNT,
        )
        positions = []
        for name in names:
            index = copy.find(name)
            with self.subTest(course=name):
                self.assertNotEqual(
                    -1,
                    index,
                    "%s names no course %r. Courses 6 to 8 are announced, so "
                    "they are listed in order and marked unavailable rather than "
                    "hidden until they exist." % (PATH_PAGE, name),
                )
            positions.append(index)
        self.assertEqual(
            sorted(positions),
            positions,
            "the courses are listed out of order: %s"
            % list(zip(names, positions)),
        )

    def test_upcoming_courses_are_marked_and_are_not_links(self):
        doc = self.path_document()
        copy = visible_text(doc.text)
        links = [text for text in anchor_texts(doc.text) if text]
        for number, name in UPCOMING_COURSES:
            with self.subTest(course=name):
                self.assertNotIn(
                    name,
                    " | ".join(links),
                    "course %d, %r, is rendered as a link. It is not published; "
                    "there is nothing to open, and a link that 404s is worse than "
                    "an entry that says so." % (number, name),
                )
                start = copy.find(name)
                self.assertNotEqual(-1, start, "%r is not listed" % name)
                window = copy[max(0, start - 260):start + 260].lower()
                self.assertIn(
                    "not yet available",
                    window,
                    "course %d, %r, is listed without saying it is unavailable. "
                    "It must be unmistakable, next to the entry itself."
                    % (number, name),
                )

    def test_upcoming_courses_declare_no_invented_lesson_count(self):
        """Nothing is known about courses 6 to 8 but the number and the name.

        A lesson count or a syllabus for an unwritten course is an invention,
        and it is the kind that reads as fact forever. The window runs from the
        course's name to the next entry, which is exactly where such a claim
        would be written.
        """
        doc = self.path_document()
        copy = visible_text(doc.text)
        upcoming = [name for _number, name in UPCOMING_COURSES]
        for index, name in enumerate(upcoming):
            start = copy.find(name)
            if start == -1:
                continue  # reported above
            end = copy.find(upcoming[index + 1]) if index + 1 < len(upcoming) else -1
            window = copy[start:end] if end > start else copy[start:start + 420]
            with self.subTest(course=name):
                self.assertIsNone(
                    re.search(r"(?i)\b\d+\s+lessons?\b", window),
                    "%r is announced only: it has no published lesson count, so "
                    "the path page must not state one." % name,
                )


# ---------------------------------------------------------------------------
# The pinned cross-course conventions
# ---------------------------------------------------------------------------
# Seven courses, authored at seven different times, now share one origin. The
# review before course 3 landed found all of them drifting in the same three
# places, course 4's source package arrived drifting in all three again -- a
# light block with no accent tokens and no prefers-color-scheme path, and a
# fourth theme key -- and course 5's arrived with a shape of its own again: a
# <button id="themeBtn"> whose label was swapped between two glyphs from
# script, no setupTheme(), the theme applied AFTER paint so the page flashed,
# and a fifth theme key. Every variant looked correct inside its own course:
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
# character, and the NEXT course package to invent its own variant fails here
# -- as every package so far has, which is why nothing here is relaxed to
# accommodate one.

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
# the courses shipped separately and must never come back.
LESSON_NAV_MARKUP = '<nav class="lesson-nav" aria-label="Lesson navigation">'
LESSON_NAV_RE = re.compile(r"<nav class=\"lesson-nav\"[^>]*>(.*?)</nav>", re.S)
PAGER_ANCHOR_RE = re.compile(r"<a\s+([^>]*?)>(.*?)</a>", re.S)
ATTRIBUTE_RE = re.compile(r"([A-Za-z_:][-\w:.]*)\s*=\s*\"([^\"]*)\"")
# The <strong> body is pinned to "NN &middot; Title", not merely "something".
# Spec B mandates that exact shape, and a bare `.+?` let the separator drift to
# "-" or "|" across courses without a single test noticing -- the precise class
# of cross-course drift TestPinnedConventions exists to stop.
PAGER_BODY_RE = re.compile(
    r"\A\s*<span>([^<]+)</span>\s*<strong>(.+?)</strong>\s*\Z", re.S
)
# The <strong> label has exactly two legitimate shapes, and both are pinned so
# the separator cannot drift to "-" or "|" across courses -- a bare `.+?` here
# let precisely that happen once already.
#   lesson -> lesson            "NN &middot; Title"
#   last lesson -> course home  a plain label with no ordinal, because the
#                               course home is not lesson number anything.
PAGER_LABEL_RE = re.compile(r"\A\s*\d{2}\s*&middot;\s*\S.*\Z", re.S)
PAGER_TERMINAL_LABEL_RE = re.compile(r"\A\s*[^<&]*\S[^<]*\Z", re.S)
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
                        label = PAGER_BODY_RE.match(body).group(2)
                        terminal = attrs.get("href") == "../"
                        self.assertRegex(
                            label,
                            PAGER_TERMINAL_LABEL_RE if terminal else PAGER_LABEL_RE,
                            "a lesson-to-lesson pager label is pinned to "
                            "'NN &middot; Title'; only the link out to the course "
                            "home may use a plain label (href=%r)" % attrs.get("href"),
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
