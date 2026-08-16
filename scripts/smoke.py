#!/usr/bin/env python3
"""Production smoke client for the learn.geterdone.io course library.

Standard library only, by design: this runs on the production host and inside the
release workflow, where installing third-party packages is not a permitted mutation.

It implements the blocking acceptance checks declared in release/contract.schema.json
(``acceptance.checks``) and uses the identical check ids, so a smoke report line maps
one-to-one onto a contract check:

    internal-health     /healthz is 200 and never cached
    learn-index         / is 200 HTML, is the site index, and links to the path
    trading-path        /paths/trading/ is 200 and is that document: it lists the
                        published courses AND the announced ones
    course-home         /market-structure/ is 200 and is that document
    lesson-page         /market-structure/market-structure/ is 200 and is that
                        document
    lesson-<slug>       one check per remaining lab of course 1, Market
                        Structure: 200 HTML, its own canonical tag, and the
                        educational-use disclaimer
    course2-home        /trade-setup-execution/ is 200 and is that document
    course2-lesson-<slug>
                        one check per lesson of course 2, Trade Setup and
                        Execution, on the same terms
    course3-home        /options-trading/ is 200 and is that document
    course3-lesson-<slug>
                        one check per lesson of course 3, Options Trading, on
                        the same terms
    course4-home        /technical-indicators/ is 200 and is that document
    course4-lesson-<slug>
                        one check per lesson of course 4, Technical Indicators,
                        on the same terms
    journal-schema      /trade-setup-execution/trade-journal-schema.json is 200,
                        is served as JSON, and parses
    trade-plan-schema   /options-trading/options-trade-plan-schema.json is 200,
                        is served as JSON, and parses
    indicator-rule-schema
                        /technical-indicators/indicator-rule-schema.json is 200,
                        is served as JSON, and parses
    self-containment    served HTML references no origin but its own, on EVERY
                        published page
    security-headers    the application security header policy is present
    unknown-path-404    an unknown path is a real 404, not a soft 200 or a redirect

The published URL space: the site index at /, the path page at /paths/trading/,
a home per course (/market-structure/, /trade-setup-execution/, /options-trading/,
/technical-indicators/, /volume-and-order-flow/, /trading-risk-management/ and
/backtesting-and-trading-systems/), and each course's lessons beneath its own
home -- 111 HTML pages, plus six published JSON assets. Checking one page and
calling the site smoke-tested is how a hundred and ten broken pages ship, so
every published URL gets its own check id and its own line in the report.

Usage:
    python3 scripts/smoke.py https://learn.geterdone.io
    python3 scripts/smoke.py http://127.0.0.1:<LOOPBACK_PORT> --timeout 5
    python3 scripts/smoke.py https://learn.geterdone.io --json

Exit status:
    0  every check passed
    1  at least one check failed (per-check detail is printed)
    2  usage or configuration error

Per platform-ops docs/RELEASE_SAFETY_GATES.md, there is no warning-only result: a
missing, malformed, timed-out, or unexpectedly redirected response is a failure.
"""

from __future__ import annotations

import argparse
import http.client
import json
from html.parser import HTMLParser
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

MAX_BODY_BYTES = 8 * 1024 * 1024
USER_AGENT = "market-structure-lab-smoke/1"

# The published URL space -- the site index, the paths layer, then a course, then
# that course's lessons:
#
#     /                                          the site index (paths + search)
#     /paths/trading/                            the trading PATH PAGE
#     /market-structure/                         course 1 home
#     /market-structure/<lesson>/                course 1's seven labs, in order
#     /trade-setup-execution/                    course 2 home
#     /trade-setup-execution/<lesson>/           course 2's fifteen lessons, in order
#     /trade-setup-execution/trade-journal-schema.json   published JSON asset
#     /options-trading/                          course 3 home
#     /options-trading/<lesson>/                 course 3's sixteen lessons, in order
#     /options-trading/options-trade-plan-schema.json    published JSON asset
#     /technical-indicators/                     course 4 home
#     /technical-indicators/<lesson>/            course 4's sixteen lessons, in order
#     /technical-indicators/indicator-rule-schema.json   published JSON asset
#     /volume-and-order-flow/                    course 5 home
#     /volume-and-order-flow/<lesson>/           course 5's sixteen lessons, in order
#     /volume-and-order-flow/volume-order-flow-rule-schema.json  published JSON asset
#     /trading-risk-management/                  course 6 home
#     /trading-risk-management/<lesson>/         course 6's sixteen lessons, in order
#     /trading-risk-management/trading-risk-plan-schema.json     published JSON asset
#     /backtesting-and-trading-systems/          course 7 home
#     /backtesting-and-trading-systems/<lesson>/ course 7's sixteen lessons, in order
#     /backtesting-and-trading-systems/trading-system-specification-schema.json
#                                                published JSON asset
#
# The path page is NOT a course home and NOT a lesson. It is probed by its own
# check id (trading-path) with its own markers, because it is the only page that
# proves the ANNOUNCED course renders: course 8 exists nowhere else in this
# URL space and nothing else would notice if it silently vanished.
#
# The seven FLAT lesson URLs this site used to serve are retired with no redirect
# stub behind them, and so is course 1's old /market-structure-lab/ prefix (that
# slug named the whole site, not the course). They are not probed here and must
# not be re-added: a path in this file is a path that must answer 200.
#
# Below: (check id, URL path, markers that must appear VERBATIM in the served
# body of that document). The ids are the acceptance-check ids in
# release/contract.json, so one report line maps onto one contract check.
# tests/test_site_invariants.py REQUIRED_PAGES and NON_HTML_ASSETS declare the
# same URL space against the files on disk.
#
# Course 1's lab 01 is NOT listed in COURSE_1_LESSONS: it is addressed through
# --lesson-path/--lesson-marker under the contract id "lesson-page", and course
# 1's home through --course-path/--course-marker, so those flags keep working.
# Courses 2 and 3 arrived after those flags existed and are addressed only by the
# map.
DISCLAIMER_MARKER = "Educational use only"
CANONICAL_ORIGIN = "https://learn.geterdone.io"

SITE_INDEX_PATH = "/"
PATH_PAGE_PATH = "/paths/trading/"
COURSE_PATH = "/market-structure/"
LESSON_01_PATH = COURSE_PATH + "market-structure/"
COURSE_2_PATH = "/trade-setup-execution/"
JOURNAL_SCHEMA_PATH = COURSE_2_PATH + "trade-journal-schema.json"
COURSE_3_PATH = "/options-trading/"
TRADE_PLAN_SCHEMA_PATH = COURSE_3_PATH + "options-trade-plan-schema.json"
COURSE_4_PATH = "/technical-indicators/"
INDICATOR_SCHEMA_PATH = COURSE_4_PATH + "indicator-rule-schema.json"
COURSE_5_PATH = "/volume-and-order-flow/"
VOLUME_RULE_SCHEMA_PATH = COURSE_5_PATH + "volume-order-flow-rule-schema.json"
COURSE_6_PATH = "/trading-risk-management/"
RISK_PLAN_SCHEMA_PATH = COURSE_6_PATH + "trading-risk-plan-schema.json"
COURSE_7_PATH = "/backtesting-and-trading-systems/"
SYSTEM_SPEC_SCHEMA_PATH = COURSE_7_PATH + "trading-system-specification-schema.json"


def canonical_marker(path):
    """The marker that proves WHICH document was served.

    Course and lesson paths overlap by construction: /trade-setup-execution/ is a
    prefix of /trade-setup-execution/confluence/, and every course home links to
    every one of its lessons, so a bare path substring is satisfied by several
    different documents -- the home passes the lesson's check and the lesson
    passes the home's. A page has exactly ONE rel=canonical, and the closing
    quote ends the prefix, so the full opening tag is satisfied by exactly one
    document in the whole site. That is what makes these checks independent
    evidence rather than a shared 200.
    """
    return '<link rel="canonical" href="%s%s"' % (CANONICAL_ORIGIN, path)


def page_markers(path, *extra):
    """Identity (the canonical tag), then whatever else the page must carry.

    Every course and lesson page is trading material, so the educational-use
    disclaimer is part of every page check, never an extra. The site index and
    the path page are shared chrome and are checked with their own markers: a
    subject-specific disclaimer is not theirs to carry.
    """
    return (canonical_marker(path),) + tuple(extra) + (DISCLAIMER_MARKER,)


COURSE_1_TITLE_MARKER = "Market Structure"
COURSE_2_TITLE_MARKER = "Trade Setup and Execution"
COURSE_3_TITLE_MARKER = "Options Trading"
COURSE_4_TITLE_MARKER = "Technical Indicators"
COURSE_5_TITLE_MARKER = "Volume and Order Flow"
COURSE_6_TITLE_MARKER = "Trading Risk Management"
COURSE_7_TITLE_MARKER = "Backtesting and Trading Systems"

# The path page's markers. They are NOT page_markers(): the path page is shared
# chrome, not course material, so the educational-use disclaimer is not part of
# its identity -- the same frame is meant to hold a mathematics path next. The
# canonical tag proves WHICH document was served; the other three prove the two
# halves of the path actually rendered: a published course, an announced one,
# and the words that mark an announced one as unavailable.
#
# These two titles MOVE as the path advances. They name the LAST published
# course and the FIRST announced one, so they are the pair that changes at every
# course launch: "Trading Risk Management" was the announced marker until course
# 6 shipped and "Backtesting and Trading Systems" until course 7 shipped, at
# which point leaving either here would have proved only that the page still
# names a course -- not that the published/announced boundary rendered on the
# correct side of it. Course 8 is now the only announced one.
PATH_PAGE_MARKERS = (
    canonical_marker(PATH_PAGE_PATH),
    COURSE_7_TITLE_MARKER,
    "Algorithmic and Automated Trading",
    "Not yet available",
)

# Course 1, labs 02-07. Lab titles avoid "&" on purpose: a title may be served
# escaped or raw, and the marker must match the bytes either way.
COURSE_LESSONS = (
    (
        "lesson-ranges-breakouts-liquidity",
        COURSE_PATH + "ranges-breakouts-liquidity/",
        page_markers(COURSE_PATH + "ranges-breakouts-liquidity/", "Liquidity Sweeps Lab"),
    ),
    (
        "lesson-multi-timeframe-market-structure",
        COURSE_PATH + "multi-timeframe-market-structure/",
        page_markers(COURSE_PATH + "multi-timeframe-market-structure/",
                     "Multi-Timeframe Market Structure Lab"),
    ),
    (
        "lesson-pullbacks-entry-models",
        COURSE_PATH + "pullbacks-entry-models/",
        page_markers(COURSE_PATH + "pullbacks-entry-models/", "Entry Models Lab"),
    ),
    (
        "lesson-invalidation-stops-risk-reward",
        COURSE_PATH + "invalidation-stops-risk-reward/",
        page_markers(COURSE_PATH + "invalidation-stops-risk-reward/", "Reward-to-Risk Lab"),
    ),
    (
        "lesson-volume-relative-strength",
        COURSE_PATH + "volume-relative-strength/",
        page_markers(COURSE_PATH + "volume-relative-strength/", "Relative Strength Lab"),
    ),
    (
        "lesson-options-contract-selection",
        COURSE_PATH + "options-contract-selection/",
        page_markers(COURSE_PATH + "options-contract-selection/",
                     "Options Contract Selection Lab"),
    ),
)

# Course 2, lessons 01-15, in course order. The check ids are course-scoped:
# course 1's ids are unprefixed for historical reasons and cannot change without
# invalidating recorded evidence, but a slug is only unique WITHIN a course, so
# every later course names its course in the id. Two courses that both teach
# "confluence" must not collide into one check.
COURSE_2_LESSON_SLUGS = (
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

COURSE_2_LESSONS = tuple(
    (
        "course2-lesson-%s" % slug,
        COURSE_2_PATH + slug + "/",
        page_markers(COURSE_2_PATH + slug + "/", COURSE_2_TITLE_MARKER),
    )
    for slug in COURSE_2_LESSON_SLUGS
)

# Course 3, lessons 01-16, in course order, on the same terms as course 2: the
# ids name the course because a slug is unique only within one.
COURSE_3_LESSON_SLUGS = (
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

COURSE_3_LESSONS = tuple(
    (
        "course3-lesson-%s" % slug,
        COURSE_3_PATH + slug + "/",
        page_markers(COURSE_3_PATH + slug + "/", COURSE_3_TITLE_MARKER),
    )
    for slug in COURSE_3_LESSON_SLUGS
)

# Course 4, lessons 01-16, in course order, on the same terms.
COURSE_4_LESSON_SLUGS = (
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

COURSE_4_LESSONS = tuple(
    (
        "course4-lesson-%s" % slug,
        COURSE_4_PATH + slug + "/",
        page_markers(COURSE_4_PATH + slug + "/", COURSE_4_TITLE_MARKER),
    )
    for slug in COURSE_4_LESSON_SLUGS
)

# Course 5, lessons 01-16, in course order, on the same terms.
COURSE_5_LESSON_SLUGS = (
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

COURSE_5_LESSONS = tuple(
    (
        "course5-lesson-%s" % slug,
        COURSE_5_PATH + slug + "/",
        page_markers(COURSE_5_PATH + slug + "/", COURSE_5_TITLE_MARKER),
    )
    for slug in COURSE_5_LESSON_SLUGS
)

# Course 6, lessons 01-16, in course order, on the same terms.
COURSE_6_LESSON_SLUGS = (
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

# The check id carries the course number, not the slug alone: course 2 and
# course 6 both ship a "position-sizing" lesson, and two checks with one id
# would collapse into a single report line for two different URLs.
COURSE_6_LESSONS = tuple(
    (
        "course6-lesson-%s" % slug,
        COURSE_6_PATH + slug + "/",
        page_markers(COURSE_6_PATH + slug + "/", COURSE_6_TITLE_MARKER),
    )
    for slug in COURSE_6_LESSON_SLUGS
)

# Course 7, lessons 01-16, in course order, on the same terms.
COURSE_7_LESSON_SLUGS = (
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

COURSE_7_LESSONS = tuple(
    (
        "course7-lesson-%s" % slug,
        COURSE_7_PATH + slug + "/",
        page_markers(COURSE_7_PATH + slug + "/", COURSE_7_TITLE_MARKER),
    )
    for slug in COURSE_7_LESSON_SLUGS
)

# (check id, URL path, markers) for every course home addressed by the map.
# Course 1's home is not here: it comes from --course-path/--course-marker.
COURSE_HOMES = (
    (
        "course2-home",
        COURSE_2_PATH,
        page_markers(COURSE_2_PATH, COURSE_2_TITLE_MARKER),
    ),
    (
        "course3-home",
        COURSE_3_PATH,
        page_markers(COURSE_3_PATH, COURSE_3_TITLE_MARKER),
    ),
    (
        "course4-home",
        COURSE_4_PATH,
        page_markers(COURSE_4_PATH, COURSE_4_TITLE_MARKER),
    ),
    (
        "course5-home",
        COURSE_5_PATH,
        page_markers(COURSE_5_PATH, COURSE_5_TITLE_MARKER),
    ),
    (
        "course6-home",
        COURSE_6_PATH,
        page_markers(COURSE_6_PATH, COURSE_6_TITLE_MARKER),
    ),
    (
        "course7-home",
        COURSE_7_PATH,
        page_markers(COURSE_7_PATH, COURSE_7_TITLE_MARKER),
    ),
)

# Published, and not documents. The lessons that export and import these shapes
# point the reader at the files, so each is a live URL like any other -- but an
# HTML-shaped assertion against a JSON body proves nothing, so each gets a check
# that fits what it is: served as JSON, parses, and declares the schema id its
# lessons exchange. Each id also discriminates: no HTML page served by mistake at
# one of these paths would contain that string inside valid JSON. A second asset
# is a second ENTRY here, never a reason to loosen a page check so both fit one.
PUBLISHED_ASSETS = (
    (
        "journal-schema",
        JOURNAL_SCHEMA_PATH,
        ('"const": "trade-journal-v1"',),
    ),
    (
        "trade-plan-schema",
        TRADE_PLAN_SCHEMA_PATH,
        ('"const": "options-trade-plan-v1"',),
    ),
    (
        "indicator-rule-schema",
        INDICATOR_SCHEMA_PATH,
        ('"const": "technical-indicator-rule-v1"',),
    ),
    (
        "volume-order-flow-rule-schema",
        VOLUME_RULE_SCHEMA_PATH,
        ('"const": "volume-order-flow-rule-v1"',),
    ),
    (
        "trading-risk-plan-schema",
        RISK_PLAN_SCHEMA_PATH,
        ('"const": "trading-risk-plan-v1"',),
    ),
    (
        "trading-system-specification-schema",
        SYSTEM_SPEC_SCHEMA_PATH,
        ('"const": "trading-system-specification-v1"',),
    ),
)


def path_page_targets(args):
    """(check id, path, markers) for every PATH page the library publishes.

    A path page is neither a course home nor a lesson, so it is not folded into
    either list: those lists carry course-shaped markers (a course title, the
    educational-use disclaimer) that a path page has no reason to satisfy.
    """
    return [("trading-path", PATH_PAGE_PATH, tuple(args.path_marker))]


def course_home_targets(args):
    """(check id, path, markers) for every course home, course 1 first."""
    targets = [("course-home", args.course_path, tuple(args.course_marker))]
    seen = {args.course_path}
    for check_id, path, markers in COURSE_HOMES:
        if path in seen:
            continue
        seen.add(path)
        targets.append((check_id, path, markers))
    return targets


def asset_targets(args):
    """(check id, path, markers) for every published non-HTML asset."""
    return [(check_id, path, markers) for check_id, path, markers in PUBLISHED_ASSETS]


def lesson_targets(args):
    """(check id, path, markers) for every lesson of every course, in course order.

    Course 1's lab 01 comes from --lesson-path/--lesson-marker so the flags still
    steer it; every other lesson of all seven courses comes from the published
    URL map.
    """
    targets = [("lesson-page", args.lesson_path, tuple(args.lesson_marker))]
    seen = {args.lesson_path}
    for check_id, path, markers in (
        COURSE_LESSONS
        + COURSE_2_LESSONS
        + COURSE_3_LESSONS
        + COURSE_4_LESSONS
        + COURSE_5_LESSONS
        + COURSE_6_LESSONS
        + COURSE_7_LESSONS
    ):
        if path in seen:
            # --lesson-path was pointed at a lesson that is already in the map;
            # check it once rather than reporting two lines for one URL.
            continue
        seen.add(path)
        targets.append((check_id, path, markers))
    return targets


def published_paths(args):
    """Every published PAGE, site index first: what a whole-site probe covers.

    tests/test_site_invariants.py compares this against REQUIRED_PAGES, so a page
    that exists on disk but is missing here fails the suite rather than shipping
    unprobed. Assets are deliberately not in this list: it feeds the HTML
    self-containment sweep, and parsing JSON as HTML would be a check that cannot
    fail rather than a check that passes.
    """
    paths = [SITE_INDEX_PATH]
    for _, path, _ in path_page_targets(args):
        if path not in paths:
            paths.append(path)
    for _, path, _ in course_home_targets(args):
        if path not in paths:
            paths.append(path)
    for _, path, _ in lesson_targets(args):
        if path not in paths:
            paths.append(path)
    return paths

# Origins that may appear in a served document without being an external
# dependency. These are identifiers, not fetches:
#   - w3.org: XML/SVG/xlink namespace URIs, required by inline and data: SVG.
#   - schema.org: JSON-LD @context identifier; browsers never dereference it.
NAMESPACE_HOSTS = frozenset({"www.w3.org", "w3.org", "schema.org", "www.schema.org"})

# Attribute positions the browser actually loads a subresource from. An external
# origin in any of these breaks self-containment.
LOADING_ATTRS = frozenset(
    {
        ("script", "src"), ("img", "src"), ("img", "srcset"), ("img", "lowsrc"),
        ("source", "src"), ("source", "srcset"), ("iframe", "src"), ("frame", "src"),
        ("embed", "src"), ("track", "src"), ("audio", "src"), ("video", "src"),
        ("video", "poster"), ("object", "data"), ("input", "src"), ("a", "ping"),
        ("use", "href"), ("use", "xlink:href"), ("image", "href"),
        ("image", "xlink:href"), ("body", "background"), ("table", "background"),
        ("td", "background"), ("feimage", "href"), ("feimage", "xlink:href"),
    }
)

# Attribute positions that only ever navigate or identify. An external origin here
# loads nothing: it is an ordinary outbound hyperlink, not a third-party dependency.
NAVIGATION_ATTRS = frozenset({("a", "href"), ("area", "href"), ("form", "action")})

# <link rel=...> values that identify rather than load. Everything else that a
# <link> can carry (stylesheet, icon, preload, prefetch, preconnect, dns-prefetch,
# manifest, modulepreload, mask-icon, apple-touch-icon) fetches.
NON_LOADING_LINK_RELS = frozenset(
    {"canonical", "alternate", "author", "license", "me", "help", "bookmark",
     "next", "prev", "prefetch-disabled", "search", "tag", "index", "up"}
)

# Runtime network APIs. On a self-contained static page there is nothing legitimate
# for these to talk to, so any occurrence is a violation.
NETWORK_API_RE = re.compile(
    r"""(?i)\b(?:fetch\s*\(|XMLHttpRequest|navigator\s*\.\s*sendBeacon|importScripts\s*\("""
    r"""|new\s+WebSocket|new\s+EventSource|new\s+SharedWorker|navigator\s*\.\s*serviceWorker)"""
)
CSS_URL_RE = re.compile(r"""(?i)url\(\s*(['\"]?)([^)'\"]+)\1\s*\)""")
CSS_IMPORT_RE = re.compile(r"""(?i)@import\s+(?:url\(\s*)?['\"]([^'\"]+)['\"]""")
SCHEME_URL_RE = re.compile(r"""(?i)\bhttps?://[A-Za-z0-9._~%-]+(?::[0-9]+)?""")
# Schemes that are inert for self-containment purposes.
INERT_SCHEMES = ("data:", "mailto:", "tel:", "sms:", "blob:", "about:", "javascript:")


class Violation:
    """One self-containment defect, with enough detail to fix it without guessing."""

    def __init__(self, line, kind, detail):
        self.line = line
        self.kind = kind
        self.detail = detail

    def __str__(self):
        return "line %d: %s: %s" % (self.line, self.kind, self.detail)

    def __eq__(self, other):
        return isinstance(other, Violation) and str(self) == str(other)

    def __hash__(self):
        return hash(str(self))


def _host_of(value):
    """Return the lowercase host of an absolute or protocol-relative URL, else None."""
    value = value.strip()
    if value.startswith("//"):
        value = "https:" + value
    parts = urllib.parse.urlsplit(value)
    if parts.scheme in ("http", "https") and parts.hostname:
        return parts.hostname.lower()
    return None


class SelfContainmentParser(HTMLParser):
    """Find every place a document would reach outside its own origin."""

    def __init__(self, allowed_hosts, strict_links=False):
        super().__init__(convert_charrefs=True)
        self.allowed_hosts = {h.lower() for h in allowed_hosts}
        self.strict_links = strict_links
        self.violations = []
        self._stack = []

    # -- helpers

    def _add(self, kind, detail, line=None):
        self.violations.append(Violation(line or self.getpos()[0], kind, detail))

    def _external(self, value):
        host = _host_of(value)
        if host is None or host in self.allowed_hosts or host in NAMESPACE_HOSTS:
            return None
        return host

    def _check_url(self, value, kind, context):
        """Check one URL-valued attribute for an external origin."""
        value = (value or "").strip()
        if not value or value.startswith("#"):
            return
        low = value.lower()
        if low.startswith("data:"):
            self._scan_embedded(value, context)
            return
        if low.startswith(INERT_SCHEMES):
            return
        scheme = urllib.parse.urlsplit(value).scheme.lower()
        if scheme and scheme not in ("http", "https"):
            self._add(kind, "%s uses non-http scheme %r" % (context, value))
            return
        host = self._external(value)
        if host is not None:
            self._add(kind, "%s -> %s" % (context, value))

    def _check_srcset(self, value, context):
        for candidate in (value or "").split(","):
            url = candidate.strip().split(" ", 1)[0]
            if url:
                self._check_url(url, "external subresource", context)

    def _scan_embedded(self, value, context):
        """Scan inside a data: URI (inline SVG can still reference remote images)."""
        for match in SCHEME_URL_RE.finditer(urllib.parse.unquote(value)):
            if self._external(match.group(0)) is not None:
                self._add("external subresource", "%s embeds %s" % (context, match.group(0)))

    def _scan_css(self, text, context):
        for match in CSS_IMPORT_RE.finditer(text):
            self._check_url(match.group(1), "remote @import", "%s @import" % context)
        for match in CSS_URL_RE.finditer(text):
            self._check_url(match.group(2), "external subresource", "%s url()" % context)

    # -- HTMLParser hooks

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        attrd = {}
        for name, value in attrs:
            attrd.setdefault(name.lower(), value)
        self._stack.append(tag)

        if tag == "base":
            self._add("base tag", "<base> rewrites every relative URL and breaks subpath serving", line)

        if tag == "meta":
            equiv = (attrd.get("http-equiv") or "").lower()
            if equiv == "refresh":
                content = attrd.get("content") or ""
                if "url=" in content.lower():
                    url = content.lower().split("url=", 1)[1].strip().strip("'\"")
                    self._check_url(url, "external redirect", "<meta http-equiv=refresh>")
            elif attrd.get("content") and (attrd.get("property") or attrd.get("name")):
                key = (attrd.get("property") or attrd.get("name") or "").lower()
                if key.endswith(("image", "url", "audio", "video", "src")):
                    self._check_url(attrd["content"], "external metadata origin", "<meta %s>" % key)

        if tag == "link":
            rel = (attrd.get("rel") or "").lower().split()
            href = attrd.get("href")
            if any(r in ("preconnect", "dns-prefetch") for r in rel):
                if self._external(href or "") is not None:
                    self._add("external origin hint", "<link rel=%s href=%s>" % (" ".join(rel), href), line)
            elif href and not any(r in NON_LOADING_LINK_RELS for r in rel):
                self._check_url(href, "external subresource", "<link rel=%s>" % (" ".join(rel) or "?"))

        for name, value in attrd.items():
            if value is None:
                continue
            if name in ("srcset", "imagesrcset"):
                self._check_srcset(value, "<%s %s>" % (tag, name))
            elif (tag, name) in LOADING_ATTRS:
                self._check_url(value, "external subresource", "<%s %s>" % (tag, name))
            elif (tag, name) in NAVIGATION_ATTRS:
                if self.strict_links and self._external(value) is not None:
                    self._add("external link", "<%s %s> -> %s" % (tag, name, value), line)
            elif name == "style":
                self._scan_css(value, "<%s style>" % tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_endtag(self, tag):
        if tag in self._stack:
            while self._stack and self._stack.pop() != tag:
                pass

    def handle_data(self, data):
        current = self._stack[-1] if self._stack else None
        if current == "style":
            self._scan_css(data, "<style>")
        elif current == "script":
            for match in NETWORK_API_RE.finditer(data):
                self._add("runtime network call", match.group(0).strip())
            for match in SCHEME_URL_RE.finditer(data):
                if self._external(match.group(0)) is not None:
                    self._add("external origin in script", match.group(0))


def scan_self_containment(body, allowed_hosts, strict_links=False):
    """Return the ordered, de-duplicated self-containment violations in a document.

    An external origin is a violation when the browser would LOAD from it
    (script, stylesheet, icon, font, image, iframe, preconnect, @import, url(),
    fetch/XHR/WebSocket). A plain outbound <a href> navigates and loads nothing,
    so it is reported only under strict_links.
    """
    parser = SelfContainmentParser(allowed_hosts, strict_links=strict_links)
    parser.feed(body)
    parser.close()
    seen = set()
    unique = []
    for violation in parser.violations:
        if violation not in seen:
            seen.add(violation)
            unique.append(violation)
    return [str(v) for v in unique]


class Response:
    """A normalized HTTP response, redirect chain included."""

    def __init__(self, status, headers, body, final_url, chain, elapsed_ms, blocked_redirect=None):
        self.status = status
        self.headers = headers
        self.body = body
        self.final_url = final_url
        self.chain = chain
        self.elapsed_ms = elapsed_ms
        # Set when a redirect pointed off the tested origin and was refused.
        self.blocked_redirect = blocked_redirect

    def header(self, name):
        return self.headers.get(name)

    def text(self):
        return self.body.decode("utf-8", errors="replace")


class FetchError(Exception):
    pass


class _NoAutoRedirect(urllib.request.HTTPRedirectHandler):
    """Surface 3xx as a response instead of following it.

    urllib.request.build_opener ADDS to the default handler set rather than
    replacing it, so the stock HTTPRedirectHandler must be explicitly overridden
    or every redirect is followed invisibly and the hop chain becomes unobservable.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def build_opener(ca_file=None):
    context = ssl.create_default_context(cafile=ca_file)
    # Redirects are followed explicitly in fetch() so that the chain, the hop
    # count, and the origin of every hop are observable evidence. Proxy
    # environment variables are ignored: acceptance evidence must describe the
    # upstream under test, not whatever a proxy returned.
    return urllib.request.build_opener(
        _NoAutoRedirect(),
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=context),
    )


def fetch(opener, url, method="GET", timeout=10.0, max_redirects=0, same_origin_only=True):
    """Fetch url, following at most max_redirects same-origin hops.

    A redirect that leaves the tested origin is REFUSED, not followed: an
    acceptance probe must never issue a request to a host it was not pointed at,
    and "redirected to an unexpected origin" is itself the finding.

    Never raises for an HTTP status; raises FetchError for transport failures.
    """
    origin = origin_of(url)
    chain = [url]
    started = time.monotonic()
    current = url
    for _ in range(max_redirects + 1):
        request = urllib.request.Request(current, method=method)
        request.add_header("User-Agent", USER_AGENT)
        request.add_header("Accept", "*/*")
        # Caches must not mask a broken release.
        request.add_header("Cache-Control", "no-cache")
        try:
            with opener.open(request, timeout=timeout) as raw:
                status, headers, body = raw.status, raw.headers, raw.read(MAX_BODY_BYTES)
        except urllib.error.HTTPError as exc:
            status, headers = exc.code, exc.headers
            try:
                body = exc.read(MAX_BODY_BYTES)
            except Exception:  # noqa: BLE001 - a body-less error response is still evidence
                body = b""
            finally:
                exc.close()
        except urllib.error.URLError as exc:
            raise FetchError("%s %s: %s" % (method, current, exc.reason)) from exc
        except (http.client.HTTPException, socket.timeout, ssl.SSLError, OSError) as exc:
            raise FetchError("%s %s: %s" % (method, current, exc)) from exc

        elapsed = (time.monotonic() - started) * 1000.0
        location = headers.get("Location")
        if status in (301, 302, 303, 307, 308) and location:
            nxt = urllib.parse.urljoin(current, location)
            if same_origin_only and origin_of(nxt) != origin:
                chain.append(nxt)
                return Response(status, headers, body, current, chain, elapsed, blocked_redirect=nxt)
            chain.append(nxt)
            current = nxt
            if method == "HEAD" and status == 303:
                method = "GET"
            continue
        return Response(status, headers, body, current, chain, elapsed)

    raise FetchError("exceeded %d redirect(s): %s" % (max_redirects, " -> ".join(chain)))


def origin_of(url):
    """(scheme, host, port) with the default port normalized, so https://h and
    https://h:443 are one origin while a different port is a different origin."""
    parts = urllib.parse.urlsplit(url)
    scheme = parts.scheme.lower()
    port = parts.port or {"http": 80, "https": 443}.get(scheme)
    return (scheme, (parts.hostname or "").lower(), port)


class Check:
    def __init__(self, check_id, description, target):
        self.id = check_id
        self.description = description
        self.target = target
        self.failures = []
        self.status = None
        self.elapsed_ms = None

    def fail(self, message):
        self.failures.append(message)

    @property
    def passed(self):
        return not self.failures


class Smoke:
    def __init__(self, args):
        self.args = args
        self.base = args.base_url.rstrip("/")
        self.opener = build_opener(args.ca_file)
        self.checks = []
        self._cache = {}

    def url(self, path):
        return self.base + path

    def get(self, path, max_redirects, method="GET"):
        key = (method, path, max_redirects)
        if key not in self._cache:
            self._cache[key] = fetch(
                self.opener,
                self.url(path),
                method=method,
                timeout=self.args.timeout,
                max_redirects=max_redirects,
            )
        return self._cache[key]

    def new_check(self, check_id, description, target):
        check = Check(check_id, description, target)
        self.checks.append(check)
        return check

    # -- shared assertions -------------------------------------------------

    def assert_status(self, check, response, expected):
        check.status = response.status
        check.elapsed_ms = round(response.elapsed_ms, 1)
        if response.status != expected:
            check.fail("expected HTTP %d, got HTTP %d" % (expected, response.status))
            return False
        return True

    def assert_same_origin_chain(self, check, response):
        base_origin = origin_of(self.base)
        if response.blocked_redirect:
            check.status = response.status
            check.fail(
                "refused to follow a redirect to an unexpected origin: %s (chain: %s)"
                % (response.blocked_redirect, " -> ".join(response.chain))
            )
            return False
        for hop in response.chain[1:]:
            if origin_of(hop) != base_origin:
                check.fail(
                    "redirected to an unexpected origin: %s (chain: %s)"
                    % (hop, " -> ".join(response.chain))
                )
                return False
        return True

    def assert_header(self, check, response, name, expected=None, mode="present"):
        value = response.header(name)
        if mode == "absent":
            if value is not None:
                check.fail("header %s must not be sent, got %r" % (name, value))
            return
        if value is None:
            check.fail("missing header: %s" % name)
            return
        if mode == "equals" and value.strip().lower() != expected.lower():
            check.fail("header %s expected %r, got %r" % (name, expected, value))
        elif mode == "contains" and expected.lower() not in value.lower():
            check.fail("header %s expected to contain %r, got %r" % (name, expected, value))

    def assert_contains(self, check, response, marker, label):
        if marker not in response.text():
            check.fail("%s not found in served body: %r" % (label, marker))

    # -- checks ------------------------------------------------------------

    def check_internal_health(self):
        check = self.new_check(
            "internal-health", "health endpoint is 200 and never cached", self.args.health_path
        )
        try:
            response = self.get(self.args.health_path, max_redirects=0)
        except FetchError as exc:
            check.fail(str(exc))
            return
        if not self.assert_status(check, response, 200):
            return
        self.assert_header(check, response, "Cache-Control", "no-store", "contains")

    def check_learn_index(self):
        check = self.new_check(
            "learn-index", "site index is served at /", SITE_INDEX_PATH
        )
        try:
            response = self.get(SITE_INDEX_PATH, max_redirects=self.args.max_redirects)
        except FetchError as exc:
            check.fail(str(exc))
            return
        if not self.assert_same_origin_chain(check, response):
            return
        if not self.assert_status(check, response, 200):
            return
        self.assert_header(check, response, "Content-Type", "text/html", "contains")
        for marker in self.args.index_marker:
            self.assert_contains(check, response, marker, "site index marker")

    def check_path_pages(self):
        """The path page: the ordered spine of one subject.

        It is the only page in the URL space that mentions the ANNOUNCED
        courses. If it 404s, or if it renders without them, the library still
        looks complete from every other page -- which is exactly why it gets its
        own check id rather than riding along on the index's.
        """
        for check_id, path, markers in path_page_targets(self.args):
            check = self.new_check(check_id, "path page is served at its subpath", path)
            try:
                response = self.get(path, max_redirects=self.args.max_redirects)
            except FetchError as exc:
                check.fail(str(exc))
                continue
            if not self.assert_same_origin_chain(check, response):
                continue
            if not self.assert_status(check, response, 200):
                continue
            self.assert_header(check, response, "Content-Type", "text/html", "contains")
            for marker in markers:
                self.assert_contains(check, response, marker, "path page marker")

    def check_course_homes(self):
        """Each course's own page. They are published URLs, so they are probed
        like any other: the path page links to them and every lesson links
        back up to its own, so a 404 here breaks navigation across a whole
        course."""
        for check_id, path, markers in course_home_targets(self.args):
            check = self.new_check(check_id, "course home is served at its subpath", path)
            try:
                response = self.get(path, max_redirects=self.args.max_redirects)
            except FetchError as exc:
                check.fail(str(exc))
                continue
            if not self.assert_same_origin_chain(check, response):
                continue
            if not self.assert_status(check, response, 200):
                continue
            self.assert_header(check, response, "Content-Type", "text/html", "contains")
            for marker in markers:
                self.assert_contains(check, response, marker, "course home marker")

    def check_lesson_pages(self):
        for check_id, path, markers in lesson_targets(self.args):
            check = self.new_check(check_id, "lesson is served at its subpath", path)
            try:
                response = self.get(path, max_redirects=self.args.max_redirects)
            except FetchError as exc:
                check.fail(str(exc))
                continue
            if not self.assert_same_origin_chain(check, response):
                continue
            if not self.assert_status(check, response, 200):
                continue
            self.assert_header(check, response, "Content-Type", "text/html", "contains")
            for marker in markers:
                self.assert_contains(check, response, marker, "lesson marker")

    def check_published_assets(self):
        """The published non-HTML assets, checked as what they are.

        A JSON file that answers 200 with an HTML error page, or with truncated
        bytes, is still "up" by every page-shaped assertion; parsing it is the
        only check that can tell. Course 2's lesson 14 exports the journal shape
        and its lesson 15 imports it; course 3's lesson 16 exports the trade plan
        shape. A broken asset breaks a documented handoff between lessons.
        """
        for check_id, path, markers in asset_targets(self.args):
            check = self.new_check(check_id, "published asset is served and parses", path)
            try:
                response = self.get(path, max_redirects=self.args.max_redirects)
            except FetchError as exc:
                check.fail(str(exc))
                continue
            if not self.assert_same_origin_chain(check, response):
                continue
            if not self.assert_status(check, response, 200):
                continue
            self.assert_header(check, response, "Content-Type", "json", "contains")
            for marker in markers:
                self.assert_contains(check, response, marker, "asset marker")
            try:
                json.loads(response.text())
            except ValueError as exc:
                check.fail("body does not parse as JSON: %s" % exc)

    def check_self_containment(self):
        paths = published_paths(self.args)
        check = self.new_check(
            "self-containment",
            "served HTML references no origin but its own",
            "all %d published pages" % len(paths),
        )
        allowed_hosts = set(NAMESPACE_HOSTS)
        served_host = urllib.parse.urlsplit(self.base).hostname
        if served_host:
            allowed_hosts.add(served_host.lower())
        for host in self.args.allow_origin:
            allowed_hosts.add(host.lower())

        for path in paths:
            try:
                response = self.get(path, max_redirects=self.args.max_redirects)
            except FetchError as exc:
                check.fail(str(exc))
                continue
            check.status = response.status
            if response.blocked_redirect:
                check.fail(
                    "%s: refused to follow a redirect to an unexpected origin: %s"
                    % (path, response.blocked_redirect)
                )
                continue
            if response.status != 200:
                check.fail(
                    "%s: expected HTTP 200 before scanning, got HTTP %d" % (path, response.status)
                )
                continue
            violations = scan_self_containment(
                response.text(), allowed_hosts, strict_links=self.args.strict_links
            )
            for violation in violations:
                check.fail("%s: %s" % (path, violation))

    def check_security_headers(self):
        check = self.new_check("security-headers", "application security header policy", "/")
        try:
            response = self.get("/", max_redirects=self.args.max_redirects)
        except FetchError as exc:
            check.fail(str(exc))
            return
        if not self.assert_same_origin_chain(check, response):
            return
        if not self.assert_status(check, response, 200):
            return
        self.assert_header(check, response, "X-Content-Type-Options", "nosniff", "equals")
        self.assert_header(check, response, "Referrer-Policy")
        self.assert_header(check, response, "Permissions-Policy")
        self.assert_header(check, response, "Content-Security-Policy", "frame-ancestors", "contains")
        self.assert_header(check, response, "Cache-Control", "no-cache", "contains")
        csp = response.header("Content-Security-Policy") or ""
        if "default-src" not in csp.lower():
            check.fail("Content-Security-Policy has no default-src directive: %r" % csp)
        xfo = response.header("X-Frame-Options")
        if xfo is not None and xfo.strip().lower() not in ("deny", "sameorigin"):
            check.fail("X-Frame-Options must be DENY or SAMEORIGIN, got %r" % xfo)

    def check_unknown_path_404(self):
        path = self.args.unknown_path or "/release-smoke-unknown-%s" % uuid.uuid4().hex[:12]
        check = self.new_check("unknown-path-404", "unknown path is a real 404", path)
        try:
            response = self.get(path, max_redirects=0)
        except FetchError as exc:
            check.fail(str(exc))
            return
        if response.status in (301, 302, 303, 307, 308):
            check.status = response.status
            check.fail(
                "unknown path redirected to %r instead of returning 404"
                % (response.header("Location") or "")
            )
            return
        self.assert_status(check, response, 404)

    def run(self):
        self.check_internal_health()
        self.check_learn_index()
        self.check_path_pages()
        self.check_course_homes()
        self.check_lesson_pages()
        self.check_published_assets()
        self.check_self_containment()
        self.check_security_headers()
        self.check_unknown_path_404()
        return self.checks


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="smoke.py",
        description="Blocking acceptance smoke checks for the learn.geterdone.io release.",
    )
    parser.add_argument("base_url", help="scheme://host[:port] of the deployment under test")
    parser.add_argument("--timeout", type=float, default=10.0, help="per-request timeout seconds (default: 10)")
    parser.add_argument("--max-redirects", type=int, default=2, help="redirect hops allowed for document requests (default: 2)")
    parser.add_argument("--health-path", default="/healthz")
    parser.add_argument(
        "--course-path",
        default=COURSE_PATH,
        help="course 1's home URL, checked as contract id course-home (default: %s); "
        "the other course homes are fixed by the published URL map" % COURSE_PATH,
    )
    parser.add_argument(
        "--lesson-path",
        default=LESSON_01_PATH,
        help="course 1 lab 01's URL, checked as contract id lesson-page (default: %s); "
        "every other lesson of all seven courses is fixed by the published URL map"
        % LESSON_01_PATH,
    )
    parser.add_argument("--unknown-path", default=None, help="override the 404 probe path (default: random)")
    parser.add_argument(
        "--index-marker",
        action="append",
        default=None,
        help="string that must appear in the Learn index (repeatable)",
    )
    parser.add_argument(
        "--course-marker",
        action="append",
        default=None,
        help="string that must appear in the --course-path page (repeatable)",
    )
    parser.add_argument(
        "--lesson-marker",
        action="append",
        default=None,
        help="string that must appear in the --lesson-path page (repeatable); "
        "the other labs carry their own markers",
    )
    parser.add_argument(
        "--path-marker",
        action="append",
        default=None,
        help="string that must appear in the path page at %s (repeatable)"
        % PATH_PAGE_PATH,
    )
    parser.add_argument(
        "--allow-origin",
        action="append",
        default=None,
        metavar="HOST",
        help="additional host allowed to appear in served HTML (repeatable); "
        "defaults to the canonical public host so rel=canonical is not a violation",
    )
    parser.add_argument(
        "--strict-links",
        action="store_true",
        help="also fail on outbound <a href> navigation to another origin "
        "(off by default: a hyperlink loads nothing from the other origin)",
    )
    parser.add_argument("--ca-file", default=None, help="PEM bundle for TLS verification")
    parser.add_argument("--json", action="store_true", help="emit a machine-readable report")
    args = parser.parse_args(argv)

    # The site index is the library's front door: it lists the PATHS and names
    # the courses each one holds, and it is the only way a reader reaches a path
    # at all -- so the link to the path page is a marker, not an assumption. The
    # index names every AVAILABLE course, so each course title is a marker; a
    # course that vanished from the index would still leave its own page serving
    # 200 and nothing else would notice. The index does not link a course home
    # directly (a course is opened from its path, or from a search result),
    # which is why the course titles are checked as text rather than as links.
    if args.index_marker is None:
        args.index_marker = [
            canonical_marker(SITE_INDEX_PATH),
            "paths/trading/",
            COURSE_1_TITLE_MARKER,
            COURSE_2_TITLE_MARKER,
            COURSE_3_TITLE_MARKER,
            COURSE_4_TITLE_MARKER,
            COURSE_5_TITLE_MARKER,
        ]
    if args.path_marker is None:
        args.path_marker = list(PATH_PAGE_MARKERS)
    # Course 1's home and its lab 01 share the title "Market Structure", and the
    # course path is a prefix of the lab path, so neither a title nor a bare path
    # marker discriminates between them: each document satisfies the other's
    # markers. /paths/trading/ shares no prefix with any course home, and it is
    # built the same way regardless -- a marker set that discriminates only when
    # the URLs happen to overlap is a marker set nobody can reason about. The full canonical TAG does discriminate, because the closing
    # quote stops the prefix overlap. Every page check in this file is built that
    # way (see canonical_marker), so any of them can detect a document served at
    # the wrong URL.
    if args.course_marker is None:
        args.course_marker = list(page_markers(COURSE_PATH, COURSE_1_TITLE_MARKER))
    if args.lesson_marker is None:
        args.lesson_marker = list(page_markers(LESSON_01_PATH, COURSE_1_TITLE_MARKER))
    if args.allow_origin is None:
        args.allow_origin = ["learn.geterdone.io"]

    parts = urllib.parse.urlsplit(args.base_url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        parser.error("base_url must be http://host[:port] or https://host[:port]")
    if parts.path.rstrip("/"):
        parser.error("base_url must not carry a path: %r" % parts.path)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.max_redirects < 0:
        parser.error("--max-redirects must not be negative")
    if not args.course_path.startswith("/"):
        parser.error("--course-path must start with /")
    if not args.lesson_path.startswith("/"):
        parser.error("--lesson-path must start with /")
    if not args.health_path.startswith("/"):
        parser.error("--health-path must start with /")
    return args


def report_text(args, checks, stream):
    print(
        "learn.geterdone.io smoke  base=%s  timeout=%.1fs"
        % (args.base_url.rstrip("/"), args.timeout),
        file=stream,
    )
    for check in checks:
        verdict = "PASS" if check.passed else "FAIL"
        status = "HTTP %s" % check.status if check.status is not None else "no response"
        timing = " %.0f ms" % check.elapsed_ms if check.elapsed_ms is not None else ""
        print("%s  %-39s %-34s %s%s" % (verdict, check.id, check.target, status, timing), file=stream)
        for failure in check.failures:
            print("        - %s" % failure, file=stream)
    failed = [c for c in checks if not c.passed]
    print(
        "%d passed, %d failed" % (len(checks) - len(failed), len(failed)),
        file=stream,
    )


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    checks = Smoke(args).run()
    failed = [c for c in checks if not c.passed]
    if args.json:
        json.dump(
            {
                "base_url": args.base_url.rstrip("/"),
                "passed": len(checks) - len(failed),
                "failed": len(failed),
                "checks": [
                    {
                        "id": c.id,
                        "description": c.description,
                        "target": c.target,
                        "status": c.status,
                        "elapsed_ms": c.elapsed_ms,
                        "result": "PASS" if c.passed else "FAIL",
                        "failures": c.failures,
                    }
                    for c in checks
                ],
            },
            sys.stdout,
            indent=2,
        )
        sys.stdout.write("\n")
    else:
        report_text(args, checks, sys.stdout)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
