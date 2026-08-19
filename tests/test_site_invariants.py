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
  * The site is a subject-agnostic LIBRARY OF PATHS. A path is an ordered
    sequence of courses on one subject; trading was the first and discrete
    mathematics is the second. So the shared chrome -- the site index at / and
    one path page per subject at /paths/<subject>/ -- is tested for the things
    that must hold for ANY subject, and the trading vocabulary is allowed only
    on the course and lesson pages themselves.
  * EVERY per-path invariant is now stated per path and asserted for each of
    them. PATHS below is the list, and each entry carries its own course tuple,
    its own length and its own required material notice. A guard that iterates
    one path's courses and calls the job done is the failure this structure
    exists to prevent: the trading path was complete and correct on the day the
    mathematics path shipped with no pager at all, and only a per-path sweep
    would have caught it.
  * Every invariant that used to be "the course" is stated per course and
    asserted for every one of them. The
    theme localStorage key is checked site-wide for exactly that reason: courses
    that each persist the reader's theme under their own key is a bug that looks
    like nothing until a reader crosses from one course to the next.
  * Eight courses share one origin, one visual system and one navigation model,
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
#     /algorithmic-and-automated-trading/
#                                        course 8 home, "Algorithmic and Automated Trading"
#     /algorithmic-and-automated-trading/<lesson>/
#                                        course 8's sixteen lessons, in course order
#
# That is 128 HTML pages, and it is the COURSE TREE. Two further HTML pages are
# published under the path page -- the dated, real-data CAPSTONE and its slide
# deck (REAL_DATA_PAGES below) -- for 130 in all. The capstone is a worked
# example, not a ninth course: nothing about it may grow COURSES, and the path
# is still eight courses long everywhere a count appears.
#
# The document root publishes exactly eight further things, all non-HTML assets:
# one exchange schema per course that ships one, plus the capstone's dataset --
# declared separately in NON_HTML_ASSETS below.
#
# The trading path is COMPLETE at course 8. Every course it was ever going to
# hold is published, so there is no announced-but-unpublished entry anywhere in
# this file any more, and none may be re-added without a page behind it.
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

COURSE_8_HOME = "/algorithmic-and-automated-trading/"
COURSE_8_LESSONS = (
    "algorithmic-and-automated-trading-fundamentals",
    "trading-system-architecture-and-components",
    "market-data-ingestion-and-normalization",
    "time-sessions-events-and-scheduling",
    "signal-engine-and-strategy-state",
    "portfolio-position-and-risk-engine",
    "broker-apis-and-order-lifecycle",
    "order-management-and-execution",
    "paper-trading-and-forward-testing",
    "scanners-alerts-and-human-approval",
    "reliability-idempotency-retries-and-recovery",
    "observability-logging-and-auditability",
    "security-secrets-permissions-and-kill-switches",
    "deployment-environments-and-configuration",
    "ai-assisted-and-agentic-trading-workflows",
    "automated-trading-system-specification-and-production-readiness",
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
    ("Algorithmic and Automated Trading", COURSE_8_HOME, COURSE_8_LESSONS),
)

# ---------------------------------------------------------------------------
# The second path: DISCRETE MATHEMATICS
# ---------------------------------------------------------------------------
# Eight courses, 106 lessons, published at /paths/discrete-math/ and at eight
# further top-level course homes. It is GENERATED: content/discrete_math/ holds
# the lessons as data and scripts/build_paths.py renders the pages, so
# the slugs below are a copy of a declaration that lives in the content package.
# TestGeneratedPathIsCurrent asserts the two agree, which is what stops this
# list drifting from the pages it claims to describe.
#
# No math course home may collide with a trading one, share a prefix with one,
# or take the /paths/ segment. That is asserted rather than assumed, in
# test_declared_url_space_is_the_index_the_path_pages_and_the_course_trees.
MATH_PATH_PAGE = "/paths/discrete-math/"

MATH_COURSE_1_HOME = "/logic-and-proof/"
MATH_COURSE_1_LESSONS = (
    "propositions-and-truth-values", "logical-connectives", "truth-tables",
    "conditional-statements", "logical-equivalence",
    "tautologies-and-satisfiability", "normal-forms-and-boolean-algebra",
    "predicates-and-quantifiers", "nested-quantifiers",
    "negating-quantified-statements", "rules-of-inference", "direct-proof",
    "contraposition-and-contradiction", "proof-by-cases-and-counterexample",
)

MATH_COURSE_2_HOME = "/sets-relations-functions/"
MATH_COURSE_2_LESSONS = (
    "sets-and-membership", "subsets-and-power-sets", "set-operations",
    "set-identities", "cartesian-products-and-tuples", "binary-relations",
    "properties-of-relations", "equivalence-relations-and-partitions",
    "partial-orders", "functions", "injective-surjective-bijective",
    "composition-and-inverses", "cardinality-and-countability",
    "the-pigeonhole-principle",
)

MATH_COURSE_3_HOME = "/induction-and-recursion/"
MATH_COURSE_3_LESSONS = (
    "the-well-ordering-principle", "mathematical-induction",
    "induction-with-sums-and-products",
    "induction-with-inequalities-and-divisibility", "strong-induction",
    "recursive-definitions", "structural-induction", "recursive-algorithms",
    "recurrence-relations", "solving-linear-recurrences",
    "divide-and-conquer-recurrences", "loop-invariants-and-correctness",
)

MATH_COURSE_4_HOME = "/combinatorics-and-counting/"
MATH_COURSE_4_LESSONS = (
    "sum-and-product-rules", "counting-with-restrictions", "permutations",
    "combinations", "binomial-coefficients", "the-binomial-theorem",
    "permutations-with-repetition", "combinations-with-repetition",
    "inclusion-exclusion", "derangements", "generalized-pigeonhole",
    "generating-functions", "combinatorial-proof", "choosing-a-counting-method",
)

MATH_COURSE_5_HOME = "/discrete-probability/"
MATH_COURSE_5_LESSONS = (
    "sample-spaces-and-events", "computing-probabilities", "probability-axioms",
    "conditional-probability", "independence", "bayes-theorem",
    "random-variables", "expected-value", "linearity-of-expectation",
    "variance", "binomial-distribution", "geometric-distribution",
)

MATH_COURSE_6_HOME = "/number-theory-and-cryptography/"
MATH_COURSE_6_LESSONS = (
    "divisibility-and-the-division-algorithm", "primes-and-factorisation",
    "the-sieve-of-eratosthenes", "greatest-common-divisor",
    "the-euclidean-algorithm", "bezout-and-modular-inverses",
    "modular-arithmetic", "modular-exponentiation", "linear-congruences",
    "chinese-remainder-theorem", "fermat-and-euler",
    "hashing-and-pseudorandom-numbers", "classical-ciphers", "rsa-encryption",
)

MATH_COURSE_7_HOME = "/graphs-and-trees/"
MATH_COURSE_7_LESSONS = (
    "graphs-and-graph-models", "degree-and-the-handshake-theorem",
    "graph-representations", "paths-and-connectivity", "graph-isomorphism",
    "bipartite-graphs", "euler-and-hamilton", "graph-traversal",
    "shortest-paths", "trees", "tree-traversals", "spanning-trees",
    "graph-colouring", "planar-graphs",
)

MATH_COURSE_8_HOME = "/algorithms-and-complexity/"
MATH_COURSE_8_LESSONS = (
    "algorithms-and-pseudocode", "correctness-and-termination",
    "growth-of-functions", "big-o-notation", "analysing-iterative-algorithms",
    "searching-and-sorting", "divide-and-conquer",
    "recursion-trees-and-amortised-analysis", "greedy-algorithms",
    "dynamic-programming", "complexity-classes",
    "decidability-and-the-halting-problem",
)

MATH_COURSES = (
    ("Logic and Proof", MATH_COURSE_1_HOME, MATH_COURSE_1_LESSONS),
    ("Sets, Relations, and Functions", MATH_COURSE_2_HOME, MATH_COURSE_2_LESSONS),
    ("Induction and Recursion", MATH_COURSE_3_HOME, MATH_COURSE_3_LESSONS),
    ("Combinatorics and Counting", MATH_COURSE_4_HOME, MATH_COURSE_4_LESSONS),
    ("Discrete Probability", MATH_COURSE_5_HOME, MATH_COURSE_5_LESSONS),
    ("Number Theory and Cryptography", MATH_COURSE_6_HOME, MATH_COURSE_6_LESSONS),
    ("Graphs and Trees", MATH_COURSE_7_HOME, MATH_COURSE_7_LESSONS),
    ("Algorithms and Complexity", MATH_COURSE_8_HOME, MATH_COURSE_8_LESSONS),
)

# Every course on the site, in path order, path by path. Any invariant that is
# about A COURSE rather than about a particular subject iterates this.

# ---------------------------------------------------------------------------
# The third path: ALGEBRA
# ---------------------------------------------------------------------------
# Eight courses, 105 lessons, published at /paths/algebra/ and at eight further
# top-level course homes. GENERATED, like the mathematics path:
# content/algebra/ holds the lessons as data and scripts/build_paths.py renders
# the pages, so the slugs below are a copy of a declaration that lives in the
# content package. TestGeneratedPathIsCurrent asserts the two agree.
#
# No algebra course home may collide with a trading or discrete mathematics
# one, share a prefix with one, or take the /paths/ segment. That is asserted
# rather than assumed, in
# test_declared_url_space_is_the_index_the_path_pages_and_the_course_trees.
ALGEBRA_PATH_PAGE = "/paths/algebra/"

ALGEBRA_COURSE_1_HOME = "/algebra-foundations/"
ALGEBRA_COURSE_1_LESSONS = (
    "real-numbers-and-the-number-line", "properties-of-the-real-numbers",
    "order-of-operations", "absolute-value", "integer-exponents",
    "scientific-notation", "roots-and-radicals", "rational-exponents",
    "algebraic-expressions-and-terms", "the-distributive-law",
    "combining-like-terms", "evaluating-expressions",
    "translating-words-into-algebra",
)

ALGEBRA_COURSE_2_HOME = "/linear-equations-and-inequalities/"
ALGEBRA_COURSE_2_LESSONS = (
    "what-it-means-to-solve-an-equation", "one-and-two-step-equations",
    "variables-on-both-sides", "equations-with-fractions",
    "literal-equations-and-formulas", "identities-and-contradictions",
    "ratio-proportion-and-percent", "modelling-with-linear-equations",
    "linear-inequalities", "compound-inequalities",
    "absolute-value-equations", "absolute-value-inequalities",
    "interval-and-set-builder-notation",
)

ALGEBRA_COURSE_3_HOME = "/lines-functions-and-graphs/"
ALGEBRA_COURSE_3_LESSONS = (
    "the-coordinate-plane", "graphing-a-linear-equation", "slope",
    "slope-intercept-form", "point-slope-and-standard-form",
    "parallel-and-perpendicular-lines", "what-a-function-is",
    "function-notation", "domain-and-range", "piecewise-functions",
    "transformations-of-graphs", "composition-of-functions",
    "inverse-functions", "linear-inequalities-in-two-variables",
)

ALGEBRA_COURSE_4_HOME = "/polynomials-and-factoring/"
ALGEBRA_COURSE_4_LESSONS = (
    "polynomials-degree-and-standard-form",
    "adding-and-subtracting-polynomials", "multiplying-polynomials",
    "special-products", "factoring-out-the-greatest-common-factor",
    "factoring-by-grouping", "factoring-simple-trinomials", "the-ac-method",
    "factoring-special-forms", "polynomial-long-division",
    "synthetic-division-and-the-remainder-theorem",
    "the-factor-theorem-and-rational-roots",
    "graphs-of-polynomial-functions",
)

ALGEBRA_COURSE_5_HOME = "/rational-and-radical-expressions/"
ALGEBRA_COURSE_5_LESSONS = (
    "rational-expressions-and-their-domains",
    "simplifying-rational-expressions",
    "multiplying-and-dividing-rational-expressions",
    "adding-and-subtracting-rational-expressions", "complex-fractions",
    "solving-rational-equations", "graphs-and-asymptotes",
    "simplifying-radical-expressions", "operations-with-radicals",
    "rationalizing-denominators", "solving-radical-equations",
    "radical-functions-and-their-graphs",
)

ALGEBRA_COURSE_6_HOME = "/quadratics-and-complex-numbers/"
ALGEBRA_COURSE_6_LESSONS = (
    "quadratic-equations-and-the-zero-product-property",
    "solving-by-factoring", "the-square-root-property",
    "completing-the-square", "the-quadratic-formula", "the-discriminant",
    "complex-numbers", "operations-with-complex-numbers",
    "complex-roots-of-quadratics", "graphs-of-quadratic-functions",
    "vertex-form-and-the-axis-of-symmetry", "maximum-and-minimum-problems",
    "quadratic-inequalities", "equations-reducible-to-quadratic-form",
)

ALGEBRA_COURSE_7_HOME = "/exponential-and-logarithmic-functions/"
ALGEBRA_COURSE_7_LESSONS = (
    "exponential-functions", "growth-and-decay", "the-number-e",
    "what-a-logarithm-is", "logarithmic-functions-and-their-graphs",
    "the-laws-of-logarithms", "common-and-natural-logarithms",
    "change-of-base", "solving-exponential-equations",
    "solving-logarithmic-equations",
    "compound-interest-and-continuous-growth", "logarithmic-scales",
)

ALGEBRA_COURSE_8_HOME = "/systems-and-matrices/"
ALGEBRA_COURSE_8_LESSONS = (
    "systems-of-two-linear-equations", "solving-by-substitution",
    "solving-by-elimination", "systems-in-three-variables",
    "matrices-and-row-operations", "gaussian-elimination",
    "matrix-arithmetic", "determinants-and-cramers-rule",
    "inverse-matrices", "systems-of-inequalities-and-linear-programming",
)

ALGEBRA_COURSE_9_HOME = "/sequences-and-series/"
ALGEBRA_COURSE_9_LESSONS = (
    "sequences-and-recursion", "sigma-notation",
    "arithmetic-sequences-and-series", "geometric-sequences-and-series",
    "partial-sums-and-telescoping", "infinite-geometric-series",
    "repeating-decimals-as-series", "annuities-and-accumulated-payments",
    "pascals-triangle", "the-binomial-theorem",
    "the-general-term-of-an-expansion",
)

ALGEBRA_COURSES = (
    ("Foundations of Algebra", ALGEBRA_COURSE_1_HOME, ALGEBRA_COURSE_1_LESSONS),
    ("Linear Equations and Inequalities", ALGEBRA_COURSE_2_HOME, ALGEBRA_COURSE_2_LESSONS),
    ("Lines, Functions and Graphs", ALGEBRA_COURSE_3_HOME, ALGEBRA_COURSE_3_LESSONS),
    ("Polynomials and Factoring", ALGEBRA_COURSE_4_HOME, ALGEBRA_COURSE_4_LESSONS),
    ("Rational and Radical Expressions", ALGEBRA_COURSE_5_HOME, ALGEBRA_COURSE_5_LESSONS),
    ("Quadratics and Complex Numbers", ALGEBRA_COURSE_6_HOME, ALGEBRA_COURSE_6_LESSONS),
    ("Exponential and Logarithmic Functions", ALGEBRA_COURSE_7_HOME, ALGEBRA_COURSE_7_LESSONS),
    ("Systems and Matrices", ALGEBRA_COURSE_8_HOME, ALGEBRA_COURSE_8_LESSONS),
    ("Sequences and Series", ALGEBRA_COURSE_9_HOME, ALGEBRA_COURSE_9_LESSONS),
)

# The algebra path is complete too: eight courses, all published, nothing
# announced. Declared separately from the other two so that a future path
# arriving part-written cannot be smuggled in under a finished path's
# completeness.
ALGEBRA_PATH_COURSE_COUNT = 9
ALGEBRA_UPCOMING_COURSES = ()

ALL_COURSES = COURSES + MATH_COURSES + ALGEBRA_COURSES

# The trading path is EIGHT courses long and all eight are published. This tuple
# is EMPTY, and that is the finished state rather than an oversight: an entry
# here is a promise with no page behind it, and there are none left to make.
#
# Courses 5, 6, 7 and finally 8 each moved OUT of this tuple and into COURSES on
# the day their pages landed. That direction is one-way, and course 8 was the
# last move it will ever carry for this path: nothing may be added back without a
# published page, and a ninth course was never announced, so no page may reserve
# a slot for one. TestPathIsComplete asserts the consequences -- every course on
# the path links, and no page anywhere still calls a course unavailable.
PATH_COURSE_COUNT = 8
UPCOMING_COURSES = ()

# The discrete mathematics path is also complete: eight courses, all published,
# nothing announced. Same finished state, declared separately so that a future
# path arriving part-written cannot be smuggled in under the trading path's
# completeness.
MATH_PATH_COURSE_COUNT = 8
MATH_UPCOMING_COURSES = ()

# ---------------------------------------------------------------------------
# The capstone: a dated, REAL-DATA worked example
# ---------------------------------------------------------------------------
# Two pages published UNDER the path page, at /paths/trading/<dated slug>/ .
# They are not a ninth course, not lessons, and not shared chrome:
#
#   * they are not a course -- there are eight, the path is complete, and
#     COURSES may not grow for them (TestPathIsComplete still asserts that);
#   * they are not lessons -- they have no owning course home and no pager, so
#     every per-course collection below is built by EXCLUDING them by name, the
#     same way PATH_PAGE is;
#   * they are not chrome -- they are the most subject-specific pages on the
#     site, so the subject-agnostic sweeps do not apply to them either.
#
# What makes them different from every other published page is the DATA. Every
# course page on this site teaches with synthetic series and says so, in the
# pinned sentence SYNTHETIC_DISCLAIMER_RE matches. These two pages analyse a
# real listed security over a real, closed window of real market data, so that
# sentence would be FALSE on them -- and a disclaimer that is false is worse
# than none, because it is the sentence a reader trusts.
#
# So the exception is declared here BY NAME, and it is a trade, not a waiver:
# a page in REAL_DATA_PAGES is exempt from the synthetic assertion and is
# required instead to carry
#
#   * the real-data notice, phrase by phrase (REAL_DATA_DISCLAIMER_PHRASES:
#     real market data, not investment advice, not a trade signal, and the
#     point-in-time framing), and
#   * the AS-OF DATE in the page BODY, not merely in <title> -- the analysis
#     ages, and a reader arriving months later must not be able to mistake it
#     for a present-tense view;
#
# and it is forbidden to carry the synthetic sentence at all. That is strictly
# MORE than a course page must satisfy. TestRealDataPages proves the exemption
# cannot be used as a loophole: a page in this set that carries neither
# disclaimer fails, and the set may never name course material.
CAPSTONE_HOME = PATH_PAGE + "iren-analysis-2026-08-16/"
CAPSTONE_SLIDES = CAPSTONE_HOME + "slides/"
CAPSTONE_DATASET = CAPSTONE_HOME + "iren-analysis-data.json"

# The as-of date, written the way the pages write it. The analysis is a
# snapshot of Sunday 2026-08-16 looking ahead to the Monday 2026-08-17 session;
# an undated real-data page is the failure this string exists to catch.
CAPSTONE_AS_OF = "August 16, 2026"

# The declared exception. Two pages, listed one per line: a third real-data page
# is a third LINE here plus the notice it has to carry, never a reason to soften
# the assertion that binds the other 126.
REAL_DATA_PAGES = (CAPSTONE_HOME, CAPSTONE_SLIDES)

# ---------------------------------------------------------------------------
# The two pages that may talk to Microsoft
# ---------------------------------------------------------------------------
# Every other page on this site makes ZERO network requests. That invariant is
# why the material reads offline and carries no third party, and it is not
# negotiable for course content. Signing in cannot honour it: OAuth is a
# conversation with an identity provider. So the conversation is confined to
# exactly two pages, named here, and the other 367 are untouched.
#
#   /oauth2/spa/callback/  receives the authorization code and exchanges it
#   /progress/             signs in, shows your marks, syncs them
#
# The exemption is NARROW and it is a trade, not a waiver. These pages are
# excused from self-containment and from the external-origin sweep, and from
# nothing else: they carry the pinned palette, both light paths, the shared
# theme key, the pinned theme toggle, a correct canonical tag and relative
# links, exactly as a lesson page does. A sign-in page that looked foreign
# would be a page a reader is right to distrust.
#
# They are also NOT course pages: they teach nothing, so the material
# disclaimer sweep skips them.
#
# What they may reach is fixed here rather than left to the page:
AUTH_PAGES = ("/oauth2/spa/callback/", "/progress/")
AUTH_ORIGINS = frozenset({
    "login.microsoftonline.com",   # authorize + token endpoints (PKCE, no secret)
    "graph.microsoft.com",         # the reader's OWN OneDrive app folder
})

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
SHARED_CHROME_PAGES = (SITE_INDEX, PATH_PAGE, MATH_PATH_PAGE, ALGEBRA_PATH_PAGE)

# Every path, as one row: the subject name, its page, its courses and the
# length it claims. Each per-path invariant below iterates THIS, so a third
# path is a third row plus its pages -- never a relaxed assertion.
PATHS = (
    ("Trading", PATH_PAGE, COURSES, PATH_COURSE_COUNT, UPCOMING_COURSES),
    ("Discrete Mathematics", MATH_PATH_PAGE, MATH_COURSES, MATH_PATH_COURSE_COUNT,
     MATH_UPCOMING_COURSES),
    ("Algebra", ALGEBRA_PATH_PAGE, ALGEBRA_COURSES, ALGEBRA_PATH_COURSE_COUNT,
     ALGEBRA_UPCOMING_COURSES),
)

PATH_PAGES = tuple(page for _t, page, _c, _n, _u in PATHS)

# Which path a course home belongs to. Built from PATHS so it cannot disagree
# with it, and used by the disclaimer sweep: what a course page must promise
# its reader depends on the subject, and nothing else in this file does.
PATH_OF_COURSE = {}
for _subject, _page, _courses, _n, _upcoming in PATHS:
    for _t, _home, _slugs in _courses:
        PATH_OF_COURSE[_home] = _page

REQUIRED_PAGES = {SITE_INDEX: "index.html"}
for _page in PATH_PAGES:
    REQUIRED_PAGES[_page] = source_of(_page)
for _title, _home, _slugs in ALL_COURSES:
    REQUIRED_PAGES[_home] = source_of(_home)
    for _slug in _slugs:
        REQUIRED_PAGES[lesson_url(_home, _slug)] = source_of(lesson_url(_home, _slug))
# The capstone pages are published like any other page -- every whole-tree
# invariant (self-containment, subpath safety, metadata, theme key, the pinned
# palette and toggle) applies to them unchanged. Only the DISCLAIMER differs,
# and only because the synthetic one would be false; see REAL_DATA_PAGES.
for _url in REAL_DATA_PAGES:
    REQUIRED_PAGES[_url] = source_of(_url)
# The sign-in pages are published like any other page; only the network
# sweeps treat them differently.
for _url in AUTH_PAGES:
    REQUIRED_PAGES[_url] = source_of(_url)

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
    "/algorithmic-and-automated-trading/automated-trading-system-schema.json":
        "algorithmic-and-automated-trading/automated-trading-system-schema.json",
    # Not a schema: the capstone's DATASET. It is published so the analysis is
    # inspectable -- every price, bar, indicator and backtest figure on those two
    # pages derives from this file, and a reader who wants to check the
    # arithmetic can fetch it. Declared as an asset for the same reason the seven
    # schemas are: it is not a document and has none of a document's properties.
    CAPSTONE_DATASET: CAPSTONE_DATASET.lstrip("/"),
}

# Rides along inside the document root without being published content. CNAME
# is GitHub Pages' custom-domain control file (it holds learn.geterdone.io); it
# configures delivery and is not a page or an asset any lesson links to.
DELIVERY_CONTROL_FILES = frozenset({"CNAME"})

COURSE_HOMES = tuple(home for _title, home, _slugs in ALL_COURSES)

# Everything that is not shared chrome is course material -- all eight course
# homes as well as all 118 lessons. All of it teaches trading, so all of it
# carries the same disclaimer. The two chrome pages are excluded BY NAME, not by
# URL shape: /paths/trading/ looks exactly like a lesson URL.
# Everything that is not shared chrome AND not a declared real-data page. The
# real-data pages are excluded BY NAME, exactly like the chrome pages: they are
# published under /paths/trading/ and are two segments deeper than a lesson, so a
# guard that classified by URL SHAPE would demand an owning course home, a lesson
# pager and the synthetic-examples disclaimer of a page that has none of the
# three. Excluding them here is not a hole -- TestRealDataPages asserts a
# strictly larger set of requirements against exactly these URLs.
COURSE_PAGES = {
    url: rel
    for url, rel in REQUIRED_PAGES.items()
    if url not in SHARED_CHROME_PAGES and url not in REAL_DATA_PAGES
}

# The 118 lessons alone, without any course home.
LESSON_PAGES = {url: rel for url, rel in COURSE_PAGES.items()
                if url not in COURSE_HOMES and url not in AUTH_PAGES}

# Every page of the library persists the reader's theme under ONE localStorage
# key. Course 1 shipped "marketStructureTheme", course 2 shipped
# "market-lab-theme", course 3 arrived with a third key, "options-course-theme",
# course 4's source package arrived with a FOURTH, "technical-indicators-theme",
# course 5's arrived with a FIFTH, "vof-theme", courses 6 and 7 arrived with a
# SIXTH and SEVENTH, "trm-theme" and "bts-theme", and course 8 -- the last
# package this path will ever receive -- arrived with an EIGHTH, "aat-theme":
# one per package, every package, without exception; with several courses on one
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
    "aat-theme",
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

# Every course page (every page that is not shared chrome and not a declared
# real-data page) must keep this disclaimer.
DISCLAIMER_RE = re.compile(r"(?i)educational use only")

# ...and the sentence that says WHAT KIND of material it is. Every one of the
# 126 course pages carries it today; it is asserted here rather than assumed,
# because it is the claim a reader relies on when they see a chart. It was
# previously covered only by the four words above, which a page could satisfy
# while quietly dropping the part that matters.
#
# Written to match the served bytes either way: the em dash before it may be a
# literal or an entity, and only the sentence itself is pinned.
SYNTHETIC_DISCLAIMER_RE = re.compile(
    r"(?i)charts are synthetic examples,\s*not trade signals"
)

# ...and the sentence the DISCRETE MATHEMATICS path carries instead.
#
# The synthetic-examples sentence would be meaningless on that path: there are
# no charts of anything and nothing to signal, and a disclaimer that does not
# apply is worse than none because it is the sentence a reader trusts. What a
# reader of that material needs told is different, and it is two claims that are
# both true and both checkable: every figure is computed in the browser from the
# stated definition (the labs enumerate, count and verify; none ships a
# precomputed answer), and a worked example is not a proof -- which is the
# actual intellectual hazard of learning this subject from interactive examples,
# and the subject of that path's course 3.
#
# Only the second half is pinned here, because it is the half that makes a
# claim about what the material does NOT establish.
MATH_DISCLAIMER_RE = re.compile(r"(?i)a worked example is not a proof")
ALGEBRA_DISCLAIMER_RE = re.compile(
    r"(?i)a step that gives the right answer here is not thereby a valid rule")

# Which sentence each path's course pages must carry. A path is a KEY here, so
# adding one without deciding what it promises its reader fails immediately
# rather than inheriting another subject's promise.
PATH_MATERIAL_DISCLAIMER = {
    PATH_PAGE: ("the synthetic-examples disclaimer", SYNTHETIC_DISCLAIMER_RE),
    MATH_PATH_PAGE: ("the worked-example-is-not-a-proof disclaimer", MATH_DISCLAIMER_RE),
    ALGEBRA_PATH_PAGE: ("the a-step-is-not-a-rule disclaimer", ALGEBRA_DISCLAIMER_RE),
}

# The notice a REAL-DATA page carries instead. Each phrase is asserted
# separately so a page cannot satisfy the check with a vague gesture at
# "educational": what a reader needs to be told is that the data is real, that
# this is not advice, that it is not a signal, and that it is a snapshot of a
# past moment rather than a live view.
#
# The alternations are deliberately narrow. "not personalized investment advice"
# and "not investment advice" are the same promise and both pass; "point-in-time"
# and "not a live or current view" are the same framing and both pass. Nothing
# weaker than those does.
REAL_DATA_DISCLAIMER_PHRASES = (
    ("real market data", re.compile(r"(?i)\breal market data\b")),
    (
        "not investment advice",
        re.compile(r"(?i)\bnot\s+(?:personalized\s+)?investment advice\b"),
    ),
    ("not a trade signal", re.compile(r"(?i)\bnot a trade signal\b")),
    (
        "point-in-time framing (not a live or current view)",
        re.compile(
            r"(?i)point[\s\u2010-\u2015-]?in[\s\u2010-\u2015-]?time"
            r"|\bnot (?:a )?(?:live|current)\b"
        ),
    ),
)

# The as-of date, as it must appear in the BODY of a real-data page. A date in
# <title> alone is invisible to a reader who has scrolled, and this analysis
# ages: the whole point of the string is that a reader arriving months later
# reads it as history.
AS_OF_DATE_RE = re.compile(r"(?i)" + re.escape(CAPSTONE_AS_OF))

BODY_RE = re.compile(r"<body\b[^>]*>(.*?)</body>", re.S | re.I)


def body_text(markup):
    """Readable copy of the <body> only -- <title> deliberately excluded.

    visible_text() over a whole document keeps the <title> text, which is
    exactly the loophole this helper closes: a real-data page must state its
    as-of date where a reader reads, not only in the tab.
    """
    match = BODY_RE.search(markup)
    return visible_text(match.group(1) if match else markup)


def missing_real_data_phrases(markup):
    """Labels of the real-data notice this document does NOT carry.

    Module level and text-only on purpose: TestRealDataPages hands it planted
    documents to prove the check is not inert, which a method reading files off
    disk could never do.
    """
    missing = [
        label for label, pattern in REAL_DATA_DISCLAIMER_PHRASES
        if not pattern.search(markup)
    ]
    if not AS_OF_DATE_RE.search(body_text(markup)):
        missing.append("the as-of date %r in the page body" % CAPSTONE_AS_OF)
    return missing

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
    path page, and so are all seven non-HTML assets, each checked as JSON rather
    than as a page.
    """

    def test_declared_url_space_is_the_index_the_path_pages_and_the_course_trees(self):
        """Site index, path page, a home per course and that course's lessons,
        then the capstone.

        The COURSE TREE is 365 URLs exactly: the site index, three path pages,
        25 course homes, and the lessons beneath them -- 118 trading, 106
        discrete mathematics, 112 algebra. The flat /<lesson>/ URLs and the old
        /market-structure-lab/ course prefix were retired without redirects, so
        a two-segment lesson path under a declared course home is the only shape
        a lesson may have; re-adding either would declare a page that no longer
        exists on disk.

        The capstone adds two more pages BESIDE that tree, under the path page.
        They are counted separately here on purpose: the number that must never
        drift is the course tree, and folding the capstone into it would let a
        course quietly disappear behind a worked example being added.
        """
        trading_tree = (
            1  # the trading path page
            + len(COURSES)
            + sum(len(slugs) for _t, _h, slugs in COURSES)
        )
        math_tree = (
            1  # the discrete mathematics path page
            + len(MATH_COURSES)
            + sum(len(slugs) for _t, _h, slugs in MATH_COURSES)
        )
        algebra_tree = (
            1  # the algebra path page
            + len(ALGEBRA_COURSES)
            + sum(len(slugs) for _t, _h, slugs in ALGEBRA_COURSES)
        )
        course_tree = 1 + trading_tree + math_tree + algebra_tree  # 1 for the index
        self.assertEqual(
            127,
            trading_tree,
            "the trading path is 1 + 8 + 7 + 15 + 16 + 16 + 16 + 16 + 16 + 16 = 127 "
            "pages, got %d" % trading_tree,
        )
        self.assertEqual(
            115,
            math_tree,
            "the discrete mathematics path is 1 + 8 + 14 + 14 + 12 + 14 + 12 + 14 "
            "+ 14 + 12 = 115 pages, got %d" % math_tree,
        )
        self.assertEqual(
            122,
            algebra_tree,
            "the algebra path is 1 + 9 + 13 + 13 + 14 + 13 + 12 + 14 + 12 + 10 + 11 = 122 "
            "pages, got %d" % algebra_tree,
        )
        self.assertEqual(
            365,
            course_tree,
            "the site index plus all three path trees is 365 pages, got %d" % course_tree,
        )
        self.assertEqual(
            2,
            len(REAL_DATA_PAGES),
            "the capstone is two pages: the interactive lab and the slide deck",
        )
        # The two sign-in pages are published like any other page; only the
        # network sweeps treat them differently.
        expected = course_tree + len(REAL_DATA_PAGES) + len(AUTH_PAGES)
        self.assertEqual(
            369,
            expected,
            "365 course-tree pages, the 2 capstone pages and the 2 sign-in pages is 369, "
            "got %d" % expected,
        )
        self.assertEqual(
            expected,
            len(REQUIRED_PAGES),
            "expected %d published URLs, got %d" % (expected, len(REQUIRED_PAGES)),
        )
        self.assertEqual(8, len(COURSES), "the trading path publishes eight courses")
        self.assertEqual(
            8, len(MATH_COURSES),
            "the discrete mathematics path publishes eight courses",
        )
        self.assertEqual(
            [14, 14, 12, 14, 12, 14, 14, 12],
            [len(slugs) for _t, _h, slugs in MATH_COURSES],
            "the discrete mathematics course lengths, in path order",
        )
        self.assertEqual(
            106,
            sum(len(slugs) for _t, _h, slugs in MATH_COURSES),
            "the discrete mathematics path is 106 lessons",
        )
        self.assertEqual(
            9, len(ALGEBRA_COURSES), "the algebra path publishes nine courses",
        )
        self.assertEqual(
            [13, 13, 14, 13, 12, 14, 12, 10, 11],
            [len(slugs) for _t, _h, slugs in ALGEBRA_COURSES],
            "the algebra course lengths, in path order. Courses 8 and 9 were one "
            "course until sequences and series were separated from systems and "
            "matrices: they shared a course because there was a slot, not because "
            "they share a subject.",
        )
        self.assertEqual(
            112,
            sum(len(slugs) for _t, _h, slugs in ALGEBRA_COURSES),
            "the algebra path is 112 lessons",
        )
        self.assertEqual(7, len(COURSE_1_LESSONS), "course 1 is seven lessons")
        self.assertEqual(15, len(COURSE_2_LESSONS), "course 2 is fifteen lessons")
        self.assertEqual(16, len(COURSE_3_LESSONS), "course 3 is sixteen lessons")
        self.assertEqual(16, len(COURSE_4_LESSONS), "course 4 is sixteen lessons")
        self.assertEqual(16, len(COURSE_5_LESSONS), "course 5 is sixteen lessons")
        self.assertEqual(16, len(COURSE_6_LESSONS), "course 6 is sixteen lessons")
        self.assertEqual(16, len(COURSE_7_LESSONS), "course 7 is sixteen lessons")
        self.assertEqual(16, len(COURSE_8_LESSONS), "course 8 is sixteen lessons")
        for title, _home, slugs in ALL_COURSES:
            with self.subTest(course=title):
                self.assertEqual(
                    len(set(slugs)), len(slugs), "duplicate slug in course %r" % title
                )
        for _title, home, _slugs in ALL_COURSES:
            with self.subTest(course=home):
                self.assertIn(home, REQUIRED_PAGES, "the course home must be published")
        # The path page is published, and it is neither a course home nor a
        # lesson. Stating that here means a future guard cannot quietly start
        # classifying it by URL shape: it is two segments deep exactly like a
        # lesson, and it lives under a first segment no course may take.
        for page in PATH_PAGES:
            with self.subTest(path=page):
                self.assertIn(page, REQUIRED_PAGES, "the path page must be published")
                self.assertNotIn(page, COURSE_HOMES, "a path page is not a course home")
                self.assertNotIn(page, LESSON_PAGES, "a path page is not a lesson")
                self.assertNotIn(page, COURSE_PAGES, "a path page is not course material")
                self.assertTrue(
                    page.startswith(PATHS_PREFIX),
                    "a path page lives under %s" % PATHS_PREFIX,
                )
        self.assertEqual(
            len(set(PATH_PAGES)), len(PATH_PAGES), "two paths declare the same page"
        )
        for _title, home, _slugs in ALL_COURSES:
            with self.subTest(course=home):
                self.assertFalse(
                    home.startswith(PATHS_PREFIX) or PATHS_PREFIX.startswith(home),
                    "%s collides with the paths layer at %s" % (home, PATHS_PREFIX),
                )
        # No course home may be a prefix of another: the first path segment
        # must identify the course on its own, or /a/ and /a-b/x/ start
        # answering for each other in guards that match on prefixes. This runs
        # ACROSS paths as well as within one: both paths publish their courses
        # at the top level, so a mathematics slug colliding with a trading slug
        # would be one URL claimed by two builders.
        for _title, home, _slugs in ALL_COURSES:
            for _other_title, other, _other_slugs in ALL_COURSES:
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

        All seven published schemas are declared here, one line each, and so is
        the capstone's dataset -- which is not a schema at all, but is published
        for the same reason and is not a document either. Every new one is the
        moment the temptation appears to relax an HTML assertion so a JSON file
        can slip through the page sweep; the fix for "this check cannot apply to
        that file" is another declaration, never a weaker check.
        """
        self.assertEqual(
            8,
            len(NON_HTML_ASSETS),
            "all seven published JSON schemas must stay declared: course 2's "
            "trade journal exchange schema, course 3's options trade plan "
            "schema, course 4's indicator rule schema, course 5's volume "
            "and order flow rule schema, course 6's trading risk plan schema, "
            "course 7's trading system specification schema, and course 8's "
            "automated trading system schema -- plus the capstone's published "
            "dataset, which is not a schema but is the file every figure on the "
            "two real-data pages derives from",
        )
        self.assertIn(
            CAPSTONE_DATASET,
            NON_HTML_ASSETS,
            "the capstone dataset is published so the analysis is inspectable; "
            "declare it or stop publishing it",
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

    def test_smoke_check_ids_are_release_contract_check_ids(self):
        """One smoke report line maps onto one acceptance check, by id.

        The two files already agree on the URL SET (the tests above). They also
        have to agree on the NAME of each check, because that is what makes a
        failing smoke line traceable to the contract clause it violates -- and
        because release/contract.schema.json caps a check id at 72 characters
        while nothing caps a lesson slug. Course 8's lesson 16 slug is long
        enough to exceed the cap, so smoke.py shortens that one id deliberately;
        if the shortening ever drifts from the contract, the two files name the
        same page differently and this fails rather than shipping.
        """
        from smoke import (
            parse_args, lesson_targets, course_home_targets, asset_targets,
            path_page_targets, capstone_page_targets,
        )

        args = parse_args([CANONICAL_ORIGIN])
        probed = {
            check_id
            for check_id, _path, _markers in (
                lesson_targets(args) + course_home_targets(args)
                + asset_targets(args) + path_page_targets(args)
                + capstone_page_targets(args)
            )
        }
        for name in ("contract.json", "contract.example.json"):
            path = REPO_ROOT / "release" / name
            with self.subTest(contract=name):
                if not path.is_file():
                    self.skipTest("no release/%s in this checkout" % name)
                document = json.loads(path.read_text(encoding="utf-8"))
                declared = {
                    check["id"]
                    for check in document["acceptance"]["checks"]
                    if check.get("scope") == "public"
                }
                missing = sorted(probed - declared)
                self.assertEqual(
                    [],
                    missing,
                    "scripts/smoke.py reports check id(s) %s that release/%s does "
                    "not declare; a failing smoke line would name a contract "
                    "clause that does not exist" % (missing, name),
                )
                overlong = sorted(i for i in declared if len(i) > 72)
                self.assertEqual(
                    [],
                    overlong,
                    "release/%s declares check id(s) longer than the 72 characters "
                    "release/contract.schema.json allows: %s" % (name, overlong),
                )

    def test_smoke_probes_the_capstone_with_real_data_markers(self):
        """The served capstone must prove the notice that is TRUE about it.

        A page check whose markers include the synthetic-examples disclaimer
        would demand a false sentence from these two pages; one that dropped the
        disclaimer and asked for nothing in its place would accept a real-data
        analysis served with no notice and no date at all. So the markers are
        asserted here: the real-data phrases AND the as-of date, and NOT the
        course disclaimer.
        """
        from smoke import parse_args, capstone_page_targets, DISCLAIMER_MARKER

        args = parse_args([CANONICAL_ORIGIN])
        targets = capstone_page_targets(args)
        self.assertEqual(
            set(REAL_DATA_PAGES),
            {path for _check_id, path, _markers in targets},
            "scripts/smoke.py probes a different set of real-data pages than "
            "this suite declares",
        )
        for check_id, path, markers in targets:
            with self.subTest(page=path):
                joined = " ".join(markers)
                self.assertIn(
                    CAPSTONE_AS_OF,
                    joined,
                    "%s is probed without its as-of date; a served page that "
                    "lost its date would pass" % check_id,
                )
                for phrase in ("real market data", "not a trade signal"):
                    self.assertIn(
                        phrase,
                        joined,
                        "%s is probed without the phrase %r" % (check_id, phrase),
                    )
                self.assertNotIn(
                    DISCLAIMER_MARKER,
                    markers,
                    "%s demands the course disclaimer of a page built from real "
                    "market data" % check_id,
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

    def test_the_release_schema_requires_every_declared_check_by_name(self):
        """The schema is the guard on the contract; it has to name every check.

        release/contract.schema.json does not merely count checks: it carries one
        `contains` clause per required id, so a check cannot be dropped, renamed
        or swapped for another and still validate. That only holds while the
        clause list keeps up with the tree. Course 8 landed with its eighteen
        checks written into both contract documents and NONE of them required by
        the schema, which validated cleanly and would have kept validating with
        the whole course missing from the acceptance matrix -- a guard that
        cannot fail. This asserts the list is exhaustive in both directions, and
        that minItems agrees with it, so the next course cannot repeat it.
        """
        schema_path = REPO_ROOT / "release" / "contract.schema.json"
        if not schema_path.is_file():
            self.skipTest("no release/contract.schema.json in this checkout")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        checks = schema["properties"]["acceptance"]["properties"]["checks"]
        required = [
            clause["contains"]["properties"]["id"]["const"]
            for clause in checks["allOf"]
        ]
        self.assertEqual(
            len(set(required)),
            len(required),
            "release/contract.schema.json requires the same check id twice",
        )
        self.assertEqual(
            len(required),
            checks["minItems"],
            "minItems (%d) and the required-id list (%d) disagree; the count and "
            "the names must describe the same matrix"
            % (checks["minItems"], len(required)),
        )
        for name in ("contract.json", "contract.example.json"):
            path = REPO_ROOT / "release" / name
            with self.subTest(contract=name):
                if not path.is_file():
                    self.skipTest("no release/%s in this checkout" % name)
                document = json.loads(path.read_text(encoding="utf-8"))
                declared = [check["id"] for check in document["acceptance"]["checks"]]
                unguarded = sorted(set(declared) - set(required))
                self.assertEqual(
                    [],
                    unguarded,
                    "release/%s declares check(s) %s that release/contract.schema.json "
                    "does not require by name; they could be deleted from the "
                    "contract and it would still validate" % (name, unguarded),
                )
                phantom = sorted(set(required) - set(declared))
                self.assertEqual(
                    [],
                    phantom,
                    "release/contract.schema.json requires check id(s) %s that "
                    "release/%s does not declare; the schema would reject a "
                    "contract that matches the published tree" % (phantom, name),
                )


class TestSelfContainment(SiteFixture):
    def test_pages_reference_no_external_origin(self):
        """Every page but the two sign-in pages reaches nothing.

        Those two are allowed exactly the identity provider and Graph, listed in
        AUTH_ORIGINS, because OAuth is a conversation and there is no way to have
        one silently. The allowance is per ORIGIN and per PAGE: a lesson that
        started calling login.microsoftonline.com still fails here, and so would
        a sign-in page that reached anywhere else.
        """
        for doc in self.documents:
            url = served_path(doc.path)
            is_auth = url in AUTH_PAGES
            allowed = {CANONICAL_HOST} | (AUTH_ORIGINS if is_auth else frozenset())
            with self.subTest(page=str(doc.path.relative_to(REPO_ROOT))):
                violations = scan_self_containment(doc.text, allowed)
                if is_auth:
                    # The scanner reports a runtime call by PRIMITIVE as well as
                    # by origin, and a sign-in page necessarily makes one. The
                    # origin allowance above is what bounds where it may go; this
                    # drops only the primitive report, and only on these two
                    # pages, so any OTHER violation on them still fails.
                    violations = [v for v in violations
                                  if "runtime network call" not in v]
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
        """Every course page teaches trading with synthetic data and must say so.

        That is all eight course homes as well as all 118 lessons: a course home
        is not an exempt landing page, it sells the same material.

        BOTH halves of the notice are asserted. "Educational use only" alone was
        the whole check once, which a page could satisfy while dropping the part
        a reader actually relies on -- that the charts are synthetic and are not
        signals. All 126 course pages carry the full sentence today, so it is
        pinned here rather than left to review.

        Two kinds of page are excluded, and both BY NAME, never by URL shape:

          * the two shared-chrome pages. They are not trading material -- the
            same frame is meant to hold a mathematics path next -- so a trading
            disclaimer is not theirs to carry, and a subject-specific notice on a
            subject-agnostic page is what TestSharedChromeIsSubjectAgnostic
            forbids;
          * the declared REAL_DATA_PAGES. The synthetic sentence would be FALSE
            on them, and they are held to the strictly larger requirement in
            TestRealDataPages instead: the real-data notice, phrase by phrase,
            the as-of date in the body, and a ban on claiming to be synthetic.

        Checked two ways on purpose: every DECLARED course page must be present (a
        lesson that vanished cannot pass by not being iterated), and every
        PUBLISHED page that is neither chrome nor a declared real-data page must
        carry the disclaimer (a page added without touching REQUIRED_PAGES is
        still covered).
        """
        by_url = {served_path(doc.path): doc for doc in self.documents}
        missing = sorted(set(COURSE_PAGES) - set(by_url))
        self.assertEqual(
            [],
            missing,
            "declared course pages are not published: %s" % missing,
        )
        course_pages = [
            (url, doc)
            for url, doc in sorted(by_url.items())
            if url not in SHARED_CHROME_PAGES and url not in REAL_DATA_PAGES
            and url not in AUTH_PAGES
        ]
        self.assertTrue(course_pages, "no course page found under %s" % SITE_ROOT)
        self.assertEqual(
            361,
            len(course_pages),
            "twenty-five course homes and 336 lessons carry a material "
            "disclaimer; found %d pages, so a page has been added or removed "
            "without being declared" % len(course_pages),
        )
        for url, doc in course_pages:
            page = str(doc.path.relative_to(REPO_ROOT))
            # Which path a page belongs to is decided by its OWNING COURSE HOME,
            # never by its URL shape. Both paths publish their courses at the top
            # level, so the first segment carries no subject information at all.
            owners = [home for home in COURSE_HOMES if url.startswith(home)]
            with self.subTest(page=page):
                self.assertEqual(
                    1, len(owners),
                    "a course page belongs to exactly one course home, %s matched %s"
                    % (url, owners),
                )
                path_page = PATH_OF_COURSE[owners[0]]
                label, pattern = PATH_MATERIAL_DISCLAIMER[path_page]
                self.assertRegex(
                    doc.text,
                    DISCLAIMER_RE,
                    "course page lost its educational-use disclaimer",
                )
                self.assertRegex(
                    doc.text,
                    pattern,
                    "course page on the %s path lost %s. What a course page "
                    "promises its reader depends on the subject: a trading "
                    "lesson must say its charts are synthetic, and a mathematics "
                    "lesson must say a worked example is not a proof. Carrying "
                    "the other path's sentence is worse than carrying none, "
                    "because it is a sentence the reader trusts."
                    % (path_page, label),
                )
                # ...and it must NOT carry the other path's promise, which would
                # be a false statement about this material.
                for other_page, (other_label, other_pattern) in sorted(
                    PATH_MATERIAL_DISCLAIMER.items()
                ):
                    if other_page == path_page:
                        continue
                    self.assertNotRegex(
                        doc.text,
                        other_pattern,
                        "a page on the %s path carries %s, which belongs to %s "
                        "and is not true here"
                        % (path_page, other_label, other_page),
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


class TestRealDataPages(SiteFixture):
    """The dated capstone: real data, and a notice that is TRUE about real data.

    Every other page in this library teaches with synthetic series and says so.
    These two analyse a real listed security over a real, closed window, so the
    synthetic sentence would be a false statement on them -- and the sentence a
    reader trusts is exactly the one that must never be false.

    The exemption from that sentence is therefore paired with a LARGER
    obligation, asserted here:

      * the real-data notice, phrase by phrase -- real market data, not
        investment advice, not a trade signal, and the point-in-time framing;
      * the as-of date, in the page BODY, because the analysis ages and a reader
        arriving months later must read it as history rather than as a view of
        today;
      * a ban on carrying the synthetic sentence at all, so a page cannot hold
        both notices and let a reader pick.

    And the set itself is guarded: it may name only published pages, it may
    never name course material, and a page in it that carries NEITHER notice
    fails. An exemption that could be pointed at a lesson would be a hole in the
    disclaimer, not an exception to it.
    """

    def real_data_documents(self):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        pages = []
        for url in REAL_DATA_PAGES:
            doc = by_url.get(url)
            self.assertIsNotNone(
                doc,
                "%s is declared in REAL_DATA_PAGES but is not published. The "
                "exemption may only name pages that exist: an exemption for a "
                "page nobody can open is a rule with nothing behind it." % url,
            )
            pages.append((url, doc))
        return pages

    # -- the set is declared, published, and never course material -----------

    def test_the_exemption_names_only_published_non_course_pages(self):
        self.assertTrue(REAL_DATA_PAGES, "the declared set must not be empty")
        self.assertEqual(
            len(set(REAL_DATA_PAGES)),
            len(REAL_DATA_PAGES),
            "the same page is declared twice",
        )
        for url in REAL_DATA_PAGES:
            with self.subTest(url=url):
                self.assertIn(
                    url,
                    REQUIRED_PAGES,
                    "a real-data page is a published page like any other",
                )
                self.assertNotIn(
                    url,
                    COURSE_PAGES,
                    "%s is course material AND exempt from the course "
                    "disclaimer, which is the loophole this set exists not to "
                    "be" % url,
                )
                self.assertNotIn(
                    url, LESSON_PAGES, "a real-data page is not a lesson"
                )
                self.assertNotIn(
                    url, COURSE_HOMES, "a real-data page is not a course home"
                )
                self.assertNotIn(
                    url,
                    SHARED_CHROME_PAGES,
                    "chrome is subject-agnostic; a dated analysis of one "
                    "security is the opposite of that",
                )
                self.assertTrue(
                    url.startswith(PATH_PAGE),
                    "the capstone belongs to the path as a whole and is "
                    "published beneath %s, got %s" % (PATH_PAGE, url),
                )
        for _title, home, slugs in ALL_COURSES:
            with self.subTest(course=home):
                self.assertNotIn(
                    home,
                    REAL_DATA_PAGES,
                    "a course home may never be exempted from the "
                    "synthetic-examples disclaimer",
                )
                for slug in slugs:
                    self.assertNotIn(
                        lesson_url(home, slug),
                        REAL_DATA_PAGES,
                        "a lesson may never be exempted from the "
                        "synthetic-examples disclaimer",
                    )

    # -- what those pages must say ------------------------------------------

    def test_real_data_pages_carry_the_real_data_disclaimer(self):
        for url, doc in self.real_data_documents():
            with self.subTest(page=url):
                missing = missing_real_data_phrases(doc.text)
                self.assertEqual(
                    [],
                    missing,
                    "%s is exempt from the synthetic-examples disclaimer because "
                    "its data is real, and it does not carry what it owes "
                    "instead. Missing: %s. The notice has to state that the data "
                    "is real market data, that this is not investment advice, "
                    "that it is not a trade signal, that it is a point-in-time "
                    "view rather than a live one, and it has to name the as-of "
                    "date in the body." % (url, ", ".join(missing)),
                )

    def test_real_data_pages_state_the_as_of_date_above_the_analysis(self):
        """The date is in the BODY, not only in <title>.

        The analysis is a snapshot of one weekend. A date that lives only in the
        tab is invisible to the reader who scrolled, and this is the page where
        a reader mistaking a snapshot for a current view is the whole risk.
        """
        for url, doc in self.real_data_documents():
            with self.subTest(page=url):
                copy = body_text(doc.text)
                self.assertRegex(
                    copy,
                    AS_OF_DATE_RE,
                    "%s does not state its as-of date (%s) in the page body. A "
                    "dated analysis that is undated where a reader reads is a "
                    "page that ages into a false present-tense claim."
                    % (url, CAPSTONE_AS_OF),
                )
                title = doc.title or ""
                self.assertNotEqual(
                    "",
                    body_text(doc.text).replace(title, "").strip(),
                    "%s has no body copy at all" % url,
                )

    def test_real_data_pages_never_claim_their_charts_are_synthetic(self):
        """The exemption is a ban, not a choice between two notices."""
        for url, doc in self.real_data_documents():
            with self.subTest(page=url):
                self.assertNotRegex(
                    doc.text,
                    SYNTHETIC_DISCLAIMER_RE,
                    "%s carries the synthetic-examples disclaimer. It analyses "
                    "real market data, so that sentence is false there, and a "
                    "page carrying both notices lets a reader believe whichever "
                    "one they saw first." % url,
                )

    # -- the exemption cannot be used as a loophole -------------------------

    def test_a_real_data_page_carrying_neither_disclaimer_fails(self):
        """The scanner must reject the page the exemption would otherwise shelter.

        This is the whole risk of a declared exception: the page stops being
        checked for the sentence it is exempt from, and nothing checks it for the
        sentence it owes instead. Planted documents, so the guard is proven
        against the defect itself rather than against whatever happens to be on
        disk today.
        """
        neither = (
            "<!doctype html><html><head><title>IREN, %s</title></head>"
            "<body><h1>IREN</h1><p>Fifty sessions, read end to end.</p>"
            "</body></html>" % CAPSTONE_AS_OF
        )
        self.assertNotEqual(
            [],
            missing_real_data_phrases(neither),
            "a real-data page with NEITHER disclaimer must fail. The exemption "
            "removes one obligation and adds a larger one; a page that satisfies "
            "no obligation at all is the loophole.",
        )
        self.assertIn(
            "the as-of date %r in the page body" % CAPSTONE_AS_OF,
            missing_real_data_phrases(neither),
            "a date that appears only in <title> is not a dated page",
        )

        synthetic_only = (
            "<!doctype html><html><head><title>IREN</title></head><body>"
            "<p>Educational use only &mdash; charts are synthetic examples, not "
            "trade signals.</p></body></html>"
        )
        self.assertNotEqual(
            [],
            missing_real_data_phrases(synthetic_only),
            "carrying the course disclaimer does not satisfy the real-data one; "
            "on real data that sentence is the false claim, not the fix",
        )
        self.assertTrue(
            SYNTHETIC_DISCLAIMER_RE.search(synthetic_only),
            "the synthetic scanner must match the sentence it pins",
        )

        complete = (
            "<!doctype html><html><head><title>IREN</title></head><body>"
            "<p class=\"risk\">This page analyses real market data. It is "
            "educational analysis, not personalized investment advice, not a "
            "trade signal, and not a guarantee of any outcome. Point-in-time "
            "analysis as of Sunday, %s.</p></body></html>" % CAPSTONE_AS_OF
        )
        self.assertEqual(
            [],
            missing_real_data_phrases(complete),
            "the notice the pages are required to carry must PASS, or the "
            "requirement is unwritable",
        )
        self.assertIsNone(
            SYNTHETIC_DISCLAIMER_RE.search(complete),
            "a correct real-data notice is not the synthetic one",
        )

    def test_the_real_data_scanners_are_not_inert(self):
        """Each phrase is load-bearing: drop any one and the page must fail."""
        template = (
            "<!doctype html><html><head><title>x</title></head><body><p>"
            "%s</p></body></html>"
        )
        full = (
            "This page analyses real market data. It is educational analysis, "
            "not personalized investment advice, not a trade signal, and not a "
            "guarantee of any outcome. Point-in-time analysis as of %s."
            % CAPSTONE_AS_OF
        )
        self.assertEqual([], missing_real_data_phrases(template % full))
        for label, phrase in (
            ("real market data", "real market data"),
            ("not investment advice", "not personalized investment advice"),
            ("not a trade signal", "not a trade signal"),
            ("point-in-time framing", "Point-in-time"),
            ("as-of date", CAPSTONE_AS_OF),
        ):
            with self.subTest(dropped=label):
                self.assertNotEqual(
                    [],
                    missing_real_data_phrases(template % full.replace(phrase, "")),
                    "dropping %r still passed; that phrase is not actually "
                    "required" % phrase,
                )
        # The shorter form of the advice phrase is the same promise and passes.
        self.assertEqual(
            [],
            missing_real_data_phrases(
                template % full.replace("not personalized investment advice",
                                        "not investment advice")
            ),
        )
        # ...and so is the plainer form of the point-in-time framing.
        self.assertEqual(
            [],
            missing_real_data_phrases(
                template % full.replace("Point-in-time analysis as of",
                                        "Not a current view. Analysis as of")
            ),
        )
        # A page with no <body> is read whole rather than silently passing.
        self.assertIn(
            "the as-of date %r in the page body" % CAPSTONE_AS_OF,
            missing_real_data_phrases("<p>real market data</p>"),
        )


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
        for title, home, slugs in ALL_COURSES:
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
        for title, home, slugs in ALL_COURSES:
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

# Copy that announces something a reader cannot open yet. The trading path is
# COMPLETE -- all eight courses are published -- so none of this may appear in
# the visible copy or the metadata of any page. It is deliberately a list of
# announcement phrases rather than the bare word "available": "available now" is
# correct copy and appears on every course entry of the path page.
#
# Comments are not copy (visible_text drops them), so the several pages that
# explain in a comment why they no longer style an unavailable course keep
# passing -- the same line this file draws for the theme key and the singular
# path phrase.
UNAVAILABLE_COPY_RE = re.compile(
    r"(?i)\b(not yet available|coming soon|still to come|upcoming"
    r"|announced,? (?:but )?not yet published)\b"
)

# An availability CLAIM: how many courses of a path a reader can open. This site
# writes it two ways, and both are read below by availability_claims():
#
#   * in a sentence or a chip -- "7 of 8 courses available", "Available 7 of 8";
#   * as the path page's progress meter, role="progressbar" with aria-valuenow
#     and aria-valuemax, where the numbers are attributes rather than copy and no
#     text sweep would ever see them.
#
# A bare "N of M" is deliberately NOT a claim: "Course 7 of 8" is the POSITION
# every course home is required to state, and banning that shape would make the
# correct page unwritable.
AVAILABILITY_SENTENCE_RE = re.compile(
    r"(?i)(?:available\D{0,12}?)?\b(\d+)\s+of\s+(\d+)\s+courses?(?:\s+available)?\b"
)
AVAILABLE_WORD_RE = re.compile(r"(?i)\bavailable\b")
PROGRESSBAR_RE = re.compile(r"(?i)<[^>]*\brole=\"progressbar\"[^>]*>")
ARIA_NUMBER_RE = re.compile(r"(?i)\baria-value(now|max)=\"(\d+)\"")


def availability_claims(doc):
    """[(quoted claim, courses available, courses on the path)] on one page.

    Both shapes, normalized to one tuple, so the test that reads them does not
    have to know which shape it came from.
    """
    claims = []
    copy = visible_text(doc.text) + " " + metadata_text(doc)
    for match in AVAILABILITY_SENTENCE_RE.finditer(copy):
        window = copy[max(0, match.start() - 40):match.end() + 40]
        if AVAILABLE_WORD_RE.search(window):
            claims.append((match.group(0).strip(), int(match.group(1)), int(match.group(2))))
    for tag in PROGRESSBAR_RE.finditer(doc.text):
        numbers = dict(
            (name.lower(), int(value)) for name, value in ARIA_NUMBER_RE.findall(tag.group(0))
        )
        if "now" in numbers and "max" in numbers:
            claims.append((tag.group(0).strip(), numbers["now"], numbers["max"]))
    return claims

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
        for subject, page, courses, total, _upcoming in PATHS:
            for index, (title, home, _slugs) in enumerate(courses, start=1):
                doc = by_url.get(home)
                with self.subTest(path=subject, course=title):
                    self.assertIsNotNone(doc, "%s is not published" % home)
                    position = re.compile(
                        r"(?i)\bcourse\s+0?%d\s+of\s+%d\b" % (index, total)
                    )
                    self.assertRegex(
                        visible_text(doc.text),
                        position,
                        "%s does not say it is course %d of %d. The %s path is %d "
                        "courses long and all of them are published, so a course "
                        "home stating a position out of any other number would "
                        "describe a path that does not exist."
                        % (home, index, total, page, total),
                    )

    def test_course_pager_points_at_the_adjacent_course_homes(self):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        for subject, _page, courses, _total, _upcoming in PATHS:
            self._check_course_pager(by_url, subject, courses)

    def _check_course_pager(self, by_url, subject, courses):
        homes = [home for _title, home, _slugs in courses]
        for index, (title, home, _slugs) in enumerate(courses):
            doc = by_url.get(home)
            with self.subTest(path=subject, course=title):
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
                        "course %d is the LAST course on the path -- the path "
                        "ends there, and no course %d was ever announced -- so "
                        "there is nothing to link forward to and no placeholder "
                        "to draw for one. The page may still link onward to the "
                        "path page; that link carries no rel=\"next\", because "
                        "the path page is not the next course."
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
        for title, home, _slugs in ALL_COURSES:
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

    It is the only page that shows the WHOLE path. It used to show two kinds of
    entry -- published courses that link to their homes, and announced ones that
    held their place in the order without pretending to be openable -- and the
    second kind is gone: all eight courses are published. So what is asserted
    here is that every one of the eight is listed, in order, and that every one
    of them links; TestPathIsComplete asserts the other half, that nothing on
    this page or anywhere else still describes a course as unavailable.
    """

    def path_document(self, page):
        by_url = {served_path(doc.path): doc for doc in self.documents}
        doc = by_url.get(page)
        self.assertIsNotNone(doc, "%s is not published" % page)
        return doc

    def test_every_path_page_links_to_every_one_of_its_course_homes(self):
        for subject, page, courses, _total, _upcoming in PATHS:
            doc = self.path_document(page)
            linked = {
                urllib.parse.urljoin(page, value.split("#", 1)[0])
                for tag, attr, value, _line in doc.urls
                if tag == "a" and attr == "href" and is_internal_relative(value)
            }
            missing = [home for _title, home, _slugs in courses if home not in linked]
            with self.subTest(path=subject):
                self.assertEqual(
                    [], missing, "%s does not link to %s" % (page, missing)
                )

    def test_the_site_index_links_to_every_path_page(self):
        """The index is how a reader reaches a path at all."""
        by_url = {served_path(doc.path): doc for doc in self.documents}
        doc = by_url.get(SITE_INDEX)
        self.assertIsNotNone(doc, "the site index is not published")
        linked = {
            urllib.parse.urljoin(SITE_INDEX, value.split("#", 1)[0])
            for tag, attr, value, _line in doc.urls
            if tag == "a" and attr == "href" and is_internal_relative(value)
        }
        for page in PATH_PAGES:
            with self.subTest(path=page):
                self.assertIn(
                    page,
                    linked,
                    "the site index does not link to %s; a path nothing links to "
                    "is a path nobody can open" % page,
                )

    def test_every_path_lists_its_courses_in_path_order(self):
        for subject, page, courses, total, upcoming in PATHS:
            doc = self.path_document(page)
            copy = visible_text(doc.text)
            names = [title for title, _home, _slugs in courses] + [
                title for _n, title in upcoming
            ]
            with self.subTest(path=subject):
                self.assertEqual(
                    total, len(names), "the %s path is %d courses long" % (page, total)
                )
            positions = []
            for name in names:
                index = copy.find(name)
                with self.subTest(path=subject, course=name):
                    self.assertNotEqual(
                        -1,
                        index,
                        "%s names no course %r. A path page lists every course on "
                        "its path, in order, and all of them are published."
                        % (page, name),
                    )
                positions.append(index)
            with self.subTest(path=subject):
                self.assertEqual(
                    sorted(positions),
                    positions,
                    "the courses are listed out of order: %s"
                    % list(zip(names, positions)),
                )

    def test_every_course_on_the_path_page_is_a_link(self):
        """No entry on the path page is inert any more.

        The page used to carry two kinds of entry, and the unlinked kind was
        correct while a course had no page behind it. All eight are published, so
        an entry a reader cannot open is now simply a broken listing. This is the
        positive form of the retired upcoming checks: instead of asserting that
        an announced course is NOT a link, it asserts that every course IS one.
        """
        for subject, page, courses, _total, _upcoming in PATHS:
            doc = self.path_document(page)
            links = [text for text in anchor_texts(doc.text) if text]
            joined = " | ".join(links)
            for title, home, _slugs in courses:
                with self.subTest(path=subject, course=title):
                    self.assertIn(
                        title,
                        joined,
                        "%s lists %r without linking it. Every course on the path "
                        "is published; the entry must open %s." % (page, title, home),
                    )


class TestPathIsComplete(SiteFixture):
    """The trading path is finished, and the whole library has to read that way.

    This suite replaces the pair that guarded the opposite state. While courses
    were still being written, the invariant was that an announced course must be
    listed, marked unavailable, and never rendered as a link -- and with
    UPCOMING_COURSES now empty those checks would iterate over nothing and pass
    forever, which is exactly the "guard that cannot fail" this file refuses to
    keep. The invariant has an inverse, and it is the one that matters now: no
    page may still say a course is coming, and no availability count may read as
    a fraction of the path.

    Both halves are swept across EVERY published page, not only the path page.
    The claim "7 of 8 courses available" lived on the site index, the progress
    meter on the path page, and the forward half of course 7's pager, and a
    reader who finishes course 8 can arrive at any of them.
    """

    def test_no_page_describes_a_course_as_unavailable(self):
        for doc in self.documents:
            page = str(doc.path.relative_to(REPO_ROOT))
            copy = visible_text(doc.text) + " " + metadata_text(doc)
            found = sorted({m.group(0).lower() for m in UNAVAILABLE_COPY_RE.finditer(copy)})
            with self.subTest(page=page):
                self.assertEqual(
                    [],
                    found,
                    "this page still announces something as unavailable (%s). All "
                    "eight courses on the trading path are published; nothing is "
                    "upcoming, and copy that says otherwise is now simply wrong. "
                    "Comments are not copy (see visible_text), so a note "
                    "explaining that the state was retired keeps passing."
                    % ", ".join(found),
                )

    def test_every_availability_count_reads_as_complete(self):
        """An availability claim has to name the WHOLE path, everywhere it appears.

        "Course 7 of 8" is a POSITION and must keep passing -- it is what every
        course home is required to state. What is checked here is the narrower
        claim about how many courses a reader can OPEN, in both shapes the site
        writes it: an availability sentence or chip, and the path page's progress
        meter, whose numbers live in aria attributes where no copy sweep sees
        them.
        """
        for doc in self.documents:
            page = str(doc.path.relative_to(REPO_ROOT))
            for claim, available, total in availability_claims(doc):
                with self.subTest(page=page, claim=claim):
                    self.assertEqual(
                        total,
                        available,
                        "%r claims only %d of %d courses can be opened. Every "
                        "course on the path is published, so an availability "
                        "count that is not the whole path is out of date."
                        % (claim, available, total),
                    )

    def test_completion_scanners_are_not_inert(self):
        """Both scanners must catch the copy they forbid, and only that."""
        self.assertTrue(
            UNAVAILABLE_COPY_RE.search("Course 8 &mdash; not yet available"),
            "the unavailable-copy scanner must match the phrase it retired",
        )
        self.assertTrue(UNAVAILABLE_COPY_RE.search("7 available &middot; 1 upcoming"))
        self.assertIsNone(
            UNAVAILABLE_COPY_RE.search(
                "Every course on the path is published and available now."
            ),
            "correct copy must keep passing",
        )
        self.assertIsNone(
            UNAVAILABLE_COPY_RE.search(
                visible_text("<p><!-- the retired 'not yet available' state --></p>")
            ),
            "documenting the retired state in a comment is not committing it",
        )
        class _Doc:
            def __init__(self, text):
                self.text = text
                self.title = ""
                self.description = ""

        claims = availability_claims(_Doc("<p>7 of 8 courses available</p>"))
        self.assertEqual([("7 of 8 courses available", 7, 8)], claims)
        self.assertEqual(
            [],
            availability_claims(_Doc("<p>Course 7 of 8</p>")),
            "a course POSITION is not an availability claim and must not be swept",
        )
        meter = availability_claims(
            _Doc('<div role="progressbar" aria-valuemin="0" aria-valuemax="8" '
                 'aria-valuenow="7"></div>')
        )
        self.assertEqual([(7, 8)], [(have, total) for _c, have, total in meter],
                         "the progress meter's aria numbers must be swept too")
        self.assertEqual(
            [("8 of 8 courses available", 8, 8)],
            availability_claims(_Doc("<p>8 of 8 courses available</p>")),
            "the finished claim is found and simply passes the equality check",
        )


class TestGeneratedPathIsCurrent(unittest.TestCase):
    """The GENERATED pages are DERIVED. Nothing may edit them by hand.

    Two of the three paths are generated: content/discrete_math/ and
    content/algebra/ hold them as data and scripts/build_paths.py renders them.
    Two things can therefore drift and both are silent:

      * a page edited directly on disk, which the next build reverts without
        telling anyone;
      * this file's MATH_COURSES and ALGEBRA_COURSES, each a copy of a
        declaration living in a content package, which nothing else compares
        against it.

    Both are checked here, for every generated path rather than for a named one,
    so a fourth path is covered the moment it is added to GENERATED. The build
    script's --check mode re-renders every page in memory and reports any that
    differ, so a hand edit fails the suite rather than surviving until someone
    rebuilds.
    """

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT / "content"))
        try:
            from algebra import PATH as ALGEBRA
            from discrete_math import PATH as DISCRETE
        except ImportError as exc:  # pragma: no cover - a missing package is a failure
            raise unittest.SkipTest("cannot import a content package: %s" % exc)
        # (declared courses, declared path page, the content package's PATH)
        cls.generated = (
            ("discrete mathematics", MATH_COURSES, MATH_PATH_PAGE, DISCRETE),
            ("algebra", ALGEBRA_COURSES, ALGEBRA_PATH_PAGE, ALGEBRA),
        )

    def test_declared_slugs_match_the_content_package(self):
        """The tuples above and the content packages must name the same courses."""
        for subject, declared, _page, path in self.generated:
            with self.subTest(path=subject):
                from_content = tuple(
                    (course["title"], "/%s/" % course["slug"],
                     tuple(lesson["slug"] for lesson in course["lessons"]))
                    for course in path["courses"]
                )
                self.assertEqual(
                    declared,
                    from_content,
                    "the %s course tuple in this file disagrees with its content "
                    "package. This file declares the URL space and the content "
                    "package builds it; when they differ, one of them describes "
                    "pages that do not exist." % subject,
                )

    def test_the_path_page_slug_matches(self):
        for subject, _declared, page, path in self.generated:
            with self.subTest(path=subject):
                self.assertEqual(
                    page,
                    "/paths/%s/" % path["slug"],
                    "the declared %s path page and its content package's slug "
                    "disagree" % subject,
                )

    def test_every_generated_path_states_its_own_material_clause(self):
        """A path may not ship another subject's disclaimer.

        The licence line in the shared footer ends with a clause naming the
        intellectual hazard of the subject. That clause was a module constant
        while one path was generated, which made it FALSE the moment a second
        subject rendered through the same chrome. It is now required per path,
        and required to be distinct: two paths sharing a clause means one of
        them is telling its reader about the other one's hazard.
        """
        clauses = {}
        for subject, _declared, page, path in self.generated:
            with self.subTest(path=subject):
                clause = path.get("material")
                self.assertTrue(
                    clause,
                    "the %s path states no material clause, so its footer would "
                    "carry no hazard notice at all" % subject,
                )
                self.assertNotIn(
                    clause, clauses,
                    "the %s path repeats the material clause already used by the "
                    "%s path" % (subject, clauses.get(clause)),
                )
                clauses[clause] = subject
                label, pattern = PATH_MATERIAL_DISCLAIMER[page]
                self.assertRegex(
                    clause, pattern,
                    "the %s path's material clause is not the one this file "
                    "sweeps its pages for (%s)" % (subject, label),
                )

    def test_no_generated_page_has_been_edited_by_hand(self):
        """Re-render every page and compare with what is published.

        A hand edit to a generated page is not a small liberty: it is reverted by
        the next build, so the change appears to work and then vanishes. Failing
        here is the only way that gets noticed.
        """
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        try:
            from build_paths import pages
        except ImportError as exc:  # pragma: no cover
            raise unittest.SkipTest("cannot import the build script: %s" % exc)

        stale = []
        for relative, markup in pages():
            target = SITE_ROOT / relative
            if not target.is_file():
                stale.append("%s (missing)" % relative)
            elif target.read_text(encoding="utf-8") != markup:
                stale.append(relative)
        self.assertEqual(
            [],
            stale,
            "%d published page(s) differ from what the content package renders. "
            "Either the content changed and the site was not rebuilt, or a "
            "generated page was edited by hand and the next build will revert it. "
            "Run: python3 scripts/build_paths.py" % len(stale),
        )


class TestLessonDataMatchesTheRenderer(unittest.TestCase):
    """The lesson dicts must have the shape the renderer draws.

    render.py lays concepts into a `grid-3` and the method steps into a
    `grid-4`. Those counts are in the CSS, not in the data, so a lesson that
    supplies two concepts or five steps still renders -- lopsidedly, with a hole
    in the row, on one page out of hundreds. Nothing else in this file would
    notice, because the markup is valid either way.

    Missing keys fail loudly at build time and need no test. These are the
    failures that are quiet.
    """

    # These were all EXACT once, on the reasoning that "the CSS draws a fixed
    # number of cards". That reasoning was wrong: .grid-3 and .grid-4 are
    # repeat(auto-fit, minmax(...)), so they take whatever they are given -- five
    # step cards sit in one row at 1280px and 3+2 at 820px, and FOUR cards
    # already leave a 3+1 orphan at 820px, so five is not a new failure mode.
    #
    # What is pinned is therefore the SHAPE a reader learns -- three ideas, four
    # method steps, three mistakes -- with a little room where a lesson earned
    # it. The quiz shows one question at a time behind a Next button, so a fourth
    # question costs nothing at all and is simply more practice.
    #
    # `key` is a range because it is a <div> with white-space: pre: it grows, and
    # a few lessons legitimately want six lines (the five special products, with
    # a blank line separating the squares from the cubes). The upper bounds guard
    # against a hero block long enough to push the opening paragraph off screen.
    EXACT = {"concepts": 3, "mistakes": 3}
    RANGES = {"steps": (4, 5), "quiz": (3, 4), "key": (3, 8), "body": (7, 18)}

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT / "content"))
        try:
            from algebra import PATH as ALGEBRA
            from discrete_math import PATH as DISCRETE
        except ImportError as exc:  # pragma: no cover
            raise unittest.SkipTest("cannot import a content package: %s" % exc)
        cls.lessons = []
        for path in (DISCRETE, ALGEBRA):
            for course in path["courses"]:
                for lesson in course["lessons"]:
                    cls.lessons.append(("%s/%s" % (course["slug"], lesson["slug"]), lesson))

    def test_counts_the_layout_depends_on(self):
        for where, lesson in self.lessons:
            for field, want in self.EXACT.items():
                with self.subTest(lesson=where, field=field):
                    self.assertEqual(
                        want, len(lesson[field]),
                        "%s has %d %s; the layout draws exactly %d"
                        % (where, len(lesson[field]), field, want),
                    )
            for field, (lo, hi) in self.RANGES.items():
                with self.subTest(lesson=where, field=field):
                    self.assertTrue(
                        lo <= len(lesson[field]) <= hi,
                        "%s has %d %s, outside %d-%d"
                        % (where, len(lesson[field]), field, lo, hi),
                    )

    def test_every_quiz_question_is_answerable(self):
        """Four choices, and a correct index that points at one of them."""
        for where, lesson in self.lessons:
            for i, q in enumerate(lesson["quiz"]):
                with self.subTest(lesson=where, question=i):
                    self.assertEqual(4, len(q["a"]), "%s quiz %d: not four choices" % (where, i))
                    self.assertTrue(
                        0 <= q["c"] < len(q["a"]),
                        "%s quiz %d: correct index %r is out of range" % (where, i, q["c"]),
                    )
                    self.assertTrue(
                        q["why"].strip(),
                        "%s quiz %d: no explanation. An unexplained answer teaches "
                        "the reader to guess again." % (where, i),
                    )
                    self.assertEqual(
                        len(set(q["a"])), len(q["a"]),
                        "%s quiz %d: two choices are identical" % (where, i),
                    )

    def test_fields_that_reach_metadata_stay_plain(self):
        """A lesson title becomes <title> and og:title.

        Those are not markup: a `x` math run there is six visible characters in
        a browser tab and in every link preview. Headings inside the page may
        use the shorthand -- render.esc_inline escapes first and then applies it
        -- but a title that also leaves the page may not.
        """
        for where, lesson in self.lessons:
            for field in ("title", "module"):
                with self.subTest(lesson=where, field=field):
                    self.assertNotIn(
                        "`", lesson[field],
                        "%s %s contains the math shorthand, but this field "
                        "reaches <title> and og:title as plain text"
                        % (where, field),
                    )

    def test_escaped_fields_carry_no_html(self):
        """Fields the renderer escapes must not contain entities or markup.

        `esc()` turns `&mdash;` into the six visible characters `&mdash;`. This
        is the single most likely authoring mistake on this path, because every
        neighbouring field wants the entity.
        """
        import re
        suspicious = re.compile(r"&[a-z]+;|&#\d+;|<[a-z/][^>]*>")
        for where, lesson in self.lessons:
            fields = [("title", lesson["title"]), ("module", lesson["module"]),
                      ("one_line", lesson["one_line"]), ("key_label", lesson["key_label"]),
                      ("read_title", lesson["read_title"]),
                      ("steps_title", lesson["steps_title"]),
                      ("quiz_title", lesson["quiz_title"]),
                      ("worked.title", lesson["worked"]["title"]),
                      ("standard[0]", lesson["standard"][0])]
            fields += [("key[%d]" % i, k) for i, k in enumerate(lesson["key"])]
            fields += [("worked.lines[%d]" % i, k) for i, k in enumerate(lesson["worked"]["lines"])]
            fields += [("concepts[%d].title" % i, t) for i, (t, _b) in enumerate(lesson["concepts"])]
            fields += [("steps[%d].title" % i, t) for i, (t, _b) in enumerate(lesson["steps"])]
            fields += [("mistakes[%d].title" % i, t) for i, (t, _b) in enumerate(lesson["mistakes"])]
            for kind, payload in lesson["body"]:
                if kind == "h3":
                    fields.append(("body h3", payload))
                elif kind == "math":
                    fields += [("body math", line) for line in payload]
            for name, value in fields:
                with self.subTest(lesson=where, field=name):
                    hit = suspicious.search(value)
                    self.assertIsNone(
                        hit,
                        "%s %s contains %r, which this field shows literally "
                        "because the renderer escapes it" % (where, name, hit.group(0) if hit else ""),
                    )


class TestEveryLabBuilds(unittest.TestCase):
    """Every (lab, mode) a lesson asks for must actually produce a lab.

    A lesson names its widget by key and mode. Two things can go wrong quietly:
    a key that no longer exists, and a mode a lab does not handle and silently
    treats as its default. The first fails the build loudly; the second does
    not -- it ships a lesson on completing the square whose lab is showing the
    quadratic formula, and no markup assertion anywhere would notice.

    So each pair is built here, and each is required to differ from the lab's
    fallback. That is a weaker claim than "the mode is correct", which no test
    can make, but it is exactly the claim that catches a mode being ignored.
    """

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT / "content"))
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        try:
            from mathpath import labs
            from algebra import PATH as ALGEBRA
            from discrete_math import PATH as DISCRETE
        except ImportError as exc:  # pragma: no cover
            raise unittest.SkipTest("cannot import the lab kit: %s" % exc)
        cls.labs = labs
        cls.used = []
        for path in (DISCRETE, ALGEBRA):
            for course in path["courses"]:
                for lesson in course["lessons"]:
                    key, cfg = lesson["lab"]
                    cls.used.append((path["slug"], course["slug"], lesson["slug"], key, cfg))

    def test_every_lesson_names_a_lab_that_exists(self):
        unknown = sorted({key for _p, _c, _l, key, _cfg in self.used
                          if key not in self.labs.REGISTRY})
        self.assertEqual(
            [], unknown,
            "lesson(s) name a lab that is not in the registry: %s. Known labs: %s"
            % (", ".join(unknown), ", ".join(sorted(self.labs.REGISTRY))),
        )

    def test_every_lab_builds_and_assigns_redraw(self):
        for slug, course, lesson, key, cfg in self.used:
            with self.subTest(lesson="%s/%s" % (course, lesson)):
                lab = self.labs.build(key, cfg)
                self.assertTrue(lab.markup.strip(), "%s produced no markup" % key)
                self.assertTrue(lab.script.strip(), "%s produced no script" % key)
                self.assertIn(
                    "window.redrawLab", lab.script,
                    "%s never assigns window.redrawLab, so scripts/labcheck.js "
                    "cannot redraw it and a broken control would go unnoticed" % key,
                )

    def test_no_lab_reaches_through_parent_element(self):
        """A lab must find an element by its own id, not by walking the tree.

        This is the specific defect that shipped once: a lab hid a control with
        `input.parentElement.hidden = true`, the markup later gained a wrapper,
        and the lesson rendered a dead panel that every markup assertion passed.
        Giving the wrapper an id costs one attribute and cannot break that way.

        There WAS a broader test here -- every id a lab reads must appear in its
        own markup -- and it was removed because it could not tell a bug from the
        normal shape of these labs. One lab function serves up to ten modes and
        looks its elements up conditionally:

            var inA1 = (MODE === 'binomial') ? null : document.getElementById('sqA1');

        A static scan sees a read of `sqA1` and markup that, in binomial mode,
        does not declare it, and reports 28 lessons broken. Every one was a false
        positive. The real question -- does this lab ever dereference null? -- is
        a question about EXECUTION, and scripts/labcheck.js answers it properly by
        running all 229 generated pages in a DOM and failing on the throw. A
        static approximation of a dynamic property was worse than no test,
        because it would have been silenced rather than believed.
        """
        import re
        walk = re.compile(r"\.parentElement\b|\.parentNode\b")
        for slug, course, lesson, key, cfg in self.used:
            with self.subTest(lesson="%s/%s" % (course, lesson)):
                lab = self.labs.build(key, cfg)
                hit = walk.search(lab.script)
                self.assertIsNone(
                    hit,
                    "lab %r walks the DOM with %s instead of reading an id it "
                    "declares; give the element an id" % (key, hit.group(0) if hit else ""),
                )

    def test_labs_use_only_classes_the_stylesheet_defines(self):
        """A lab styled by a class that does not exist renders unstyled.

        Nothing else here would notice: the markup is valid, the page builds,
        the lab runs and paints. The reader gets a control panel with no panel.
        There is exactly one stylesheet on this path and it is generated, so
        "does this class exist" is a question with a definite answer.
        """
        import re
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        try:
            from mathpath import theme
        except ImportError as exc:  # pragma: no cover
            raise unittest.SkipTest("cannot import the stylesheet: %s" % exc)
        defined = set(re.findall(r"\.([a-zA-Z][\w-]*)", theme.stylesheet()))
        # Classes the RENDERER wraps a lab in, rather than the lab itself.
        frame = {"card", "lab-main", "side-panel", "practice", "choice-grid",
                 "feedback", "score", "practice-head", "small-copy", "math", "mathblock"}
        seen = set()
        for _slug, _course, _lesson, key, cfg in self.used:
            if (key, cfg.get("mode")) in seen:
                continue
            seen.add((key, cfg.get("mode")))
            lab = self.labs.build(key, cfg)
            used = set()
            for chunk in (lab.markup, lab.controls):
                for value in re.findall(r'class="([^"]+)"', chunk):
                    used |= set(value.split())
            unknown = sorted(c for c in used if c not in defined and c not in frame)
            with self.subTest(lab=key, mode=cfg.get("mode")):
                self.assertEqual(
                    [], unknown,
                    "lab %r uses CSS class(es) %s that scripts/mathpath/theme.py "
                    "does not define, so that element ships unstyled"
                    % (key, ", ".join(unknown)),
                )

    def test_a_mode_is_not_silently_ignored(self):
        """Distinct modes of one lab must produce distinct labs."""
        by_key = {}
        for _s, _c, _l, key, cfg in self.used:
            by_key.setdefault(key, {})[cfg.get("mode")] = cfg
        for key, modes in sorted(by_key.items()):
            if len(modes) < 2:
                continue
            built = {}
            for mode, cfg in modes.items():
                lab = self.labs.build(key, cfg)
                built.setdefault(lab.markup + lab.controls + lab.script, []).append(mode)
            collisions = [ms for ms in built.values() if len(ms) > 1]
            self.assertEqual(
                [], collisions,
                "lab %r renders identically for modes %s, so at least one of "
                "those lessons is showing a widget for a different lesson"
                % (key, collisions),
            )


# ---------------------------------------------------------------------------
# The pinned cross-course conventions
# ---------------------------------------------------------------------------
# Eight courses, authored at eight different times, now share one origin. The
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
        for title, home, slugs in ALL_COURSES:
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
        for title, home, slugs in ALL_COURSES:
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


class TestDataAssetsCannotBecomeLoads(unittest.TestCase):
    """The CI scanner lets a published .json DATA asset carry absolute URLs.

    That is only safe while no page can turn such a string into a request. A
    citation in a dataset loads nothing; a citation handed to fetch() is a
    third-party request. This test is the compensating control for that
    carve-out: if any page ever gains a network primitive, the exemption stops
    being safe and this fails first.
    """

    def test_no_page_can_perform_a_network_request(self):
        primitives = re.compile(
            r"(?:\bnew\s+(?:WebSocket|XMLHttpRequest|EventSource)\s*\()"
            r"|(?:(?<![\w.])fetch\s*\()"
            r"|(?:\.(?:sendBeacon|importScripts)\s*\()"
            r"|(?:\bimportScripts\s*\()"
        )
        offenders = []
        for path in sorted(SITE_ROOT.rglob("*.html")):
            # The sign-in pages fetch the token endpoint and Graph. They are the
            # only two, they are named in AUTH_PAGES, and everything else in this
            # sweep still applies to them.
            if served_path(path) in AUTH_PAGES:
                continue
            text = path.read_text(encoding="utf-8")
            for match in primitives.finditer(text):
                start = text.rfind("\n", 0, match.start()) + 1
                line = text[start:text.find("\n", match.start())]
                if line.lstrip().startswith(("*", "//", "<!--")):
                    continue
                offenders.append("%s: %s" % (served_path(path), match.group(0)))
        self.assertEqual(
            [],
            offenders,
            "a page gained a network primitive: %s. Published .json assets are "
            "allowed to contain absolute URLs as data precisely because nothing "
            "can request them; that stops being true here." % offenders,
        )


# The sign-in feature shipped once with no way in.
#
# /progress/ and its Microsoft sign-in were built, published, tested and served
# 200 -- and were unreachable in practice. The only link into them was one
# sentence of body copy under a lesson's completion button reading "Carry it to
# another device", which names a benefit rather than an action; the site index
# did not mention them at all. Every invariant in this file passed, because
# every invariant asked whether the pages EXISTED and none asked whether a
# reader could FIND them. A published page nobody can reach is not a feature.
#
# So the rule is tied to the capability, not to a hand-kept list of URLs: if a
# page can RECORD a completion mark, it must offer a way to the page that SYNCS
# them. Add a path, and its lessons inherit this the day they are generated.
#
# The site index is named separately for the reason the bug was reported: it is
# where a reader looks first, and it is not a lesson.
SIGNIN_HREF = "/progress/"
SIGNIN_LINK_ID = "signinLink"
PROGRESS_TOGGLE_ID = "progressToggle"


class TestTheWayIntoSignIn(SiteFixture):
    """Whatever can record a mark must be able to reach what syncs it."""

    def pages_that_must_offer_it(self):
        """The site index, plus every page carrying a completion toggle."""
        for document in self.documents:
            url = served_path(document.path)
            if url == SITE_INDEX or PROGRESS_TOGGLE_ID in document.ids:
                yield url, document

    def test_the_pages_that_must_offer_sign_in_exist(self):
        """Guard the guard: an empty sweep must not read as a pass."""
        found = [url for url, _doc in self.pages_that_must_offer_it()]
        self.assertIn(SITE_INDEX, found, "the site index was not swept")
        self.assertGreater(
            len(found), 100,
            "only %d page(s) claim a completion toggle; this sweep is meant to "
            "cover the whole generated library, so either the toggle's id "
            "changed or the pages stopped carrying it" % len(found),
        )

    def test_every_such_page_links_to_progress(self):
        missing = []
        for url, document in self.pages_that_must_offer_it():
            targets = {
                urllib.parse.urljoin(url, value)
                for tag, attr, value, _line in document.urls
                if tag == "a" and attr == "href"
            }
            if SIGNIN_HREF not in targets:
                missing.append(url)
        self.assertEqual(
            [], sorted(missing),
            "these pages can record a completion mark but offer no link to %s, "
            "so the marks they take can never leave the browser that took "
            "them: %s" % (SIGNIN_HREF, sorted(missing)),
        )

    def test_the_link_is_in_the_masthead_and_not_only_in_body_copy(self):
        """A sentence inside an article is not a way in; the masthead is.

        This is the exact defect that shipped: a real link to /progress/
        existed on every lesson, so the test above would have passed while the
        feature stayed invisible. What makes it findable is that it sits in
        the persistent chrome, in the same place on every page.
        """
        missing = []
        for url, document in self.pages_that_must_offer_it():
            if SIGNIN_LINK_ID not in document.ids:
                missing.append(url)
        self.assertEqual(
            [], sorted(missing),
            'these pages have no masthead sign-in control (id="%s"). A link '
            "buried in body copy is why this feature shipped unreachable: %s"
            % (SIGNIN_LINK_ID, sorted(missing)),
        )

    def test_the_masthead_control_resolves_to_progress_from_every_depth(self):
        """The href is relative, so its depth is wrong page-type by page-type.

        A lesson sits two levels down and a course home one; the same string
        cannot serve both. Nothing else here would notice -- a wrong relative
        href is valid markup that 404s only when clicked.
        """
        wrong = []
        for url, document in self.pages_that_must_offer_it():
            match = re.search(
                r'<a[^>]*id="%s"[^>]*href="([^"]*)"' % SIGNIN_LINK_ID, document.text
            ) or re.search(
                r'<a[^>]*href="([^"]*)"[^>]*id="%s"' % SIGNIN_LINK_ID, document.text
            )
            if match is None:
                continue  # absence is the previous test's failure, not this one's
            resolved = urllib.parse.urljoin(url, match.group(1))
            if resolved != SIGNIN_HREF:
                wrong.append("%s -> %s (resolves to %s)" % (url, match.group(1), resolved))
        self.assertEqual(
            [], sorted(wrong),
            "the masthead sign-in href does not resolve to %s from these "
            "pages, so clicking it 404s: %s" % (SIGNIN_HREF, sorted(wrong)),
        )

    def test_the_control_shares_its_group_with_the_theme_toggle(self):
        """The masthead is `justify-content: space-between`.

        That layout spreads its CHILDREN, so adding the sign-in as a fourth
        bare child does not put it beside the toggle -- it strands it in the
        middle of the bar, and on a lesson page (which has no nav) it lands
        dead centre. The two right-hand controls must therefore be one child.

        No other invariant here can see this: the markup is valid, the link
        resolves, and the page looks broken only to a person.
        """
        stranded = []
        for url, document in self.pages_that_must_offer_it():
            group = re.search(
                r'<div class="topbar-actions">(.*?)</div>', document.text, re.S
            )
            if group is None:
                stranded.append("%s (no .topbar-actions group)" % url)
                continue
            inner = group.group(1)
            if 'id="%s"' % SIGNIN_LINK_ID not in inner or 'id="themeToggle"' not in inner:
                stranded.append("%s (group does not hold both controls)" % url)
        self.assertEqual(
            [], sorted(stranded),
            "the sign-in control and the theme toggle must sit in one "
            ".topbar-actions child, or space-between spreads them apart: %s"
            % sorted(stranded),
        )


# Two defects that shipped to production together, both visible on /progress/
# and neither catchable by anything already here.
ESCAPED_ENTITY_RE = re.compile(r"&amp;#\d+;")
HIDDEN_RULE_RE = re.compile(r"\[hidden\]\s*\{[^}]*display:\s*none\s*!important")
# A selector that only theme.py writes, so "this page inlines the shared
# stylesheet" is a fact about the page rather than a list to maintain.
HIDDEN_ELEMENT_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)[^>]*?\shidden(?=[\s/>=])[^>]*>")
CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')
DISPLAY_DECL_RE = re.compile(r"(?<![-a-z])display\s*:")


class TestChromeRendersWhatItMeans(SiteFixture):
    """Markup that reaches the reader as its own source text is a defect."""

    def test_no_page_ships_a_double_escaped_character_entity(self):
        """"&#10003;" escaped once more is the literal text &#10003;.

        topbar() escapes any brand mark that is not already markup, which is
        right for a course number and wrong for an entity. Both sign-in pages
        therefore drew the string "&#10003;" where the logo belongs, in the
        masthead, on the two pages a reader is asked to trust with a sign-in.
        """
        offenders = []
        for doc in self.documents:
            for match in ESCAPED_ENTITY_RE.finditer(doc.text):
                offenders.append("%s: %s" % (served_path(doc.path), match.group(0)))
        self.assertEqual(
            [], sorted(offenders),
            "a character entity was escaped on its way into the page, so the "
            "reader sees its source text instead of the character: %s" % sorted(offenders),
        )

    def test_nothing_hidden_wears_a_class_that_un_hides_it(self):
        """`hidden` is a DEFAULT, and any author rule that sets display beats it.

        The browser's own rule is `[hidden] { display: none }` at UA
        precedence. The shared .btn sets `display: inline-flex`, which outranks
        it -- so `<button class="btn" hidden>` is not hidden at all. That is
        exactly how "Sign out" came to sit beside "Sign in" on a page reading
        "Not signed in": the script set the attribute correctly, and the
        attribute did nothing.

        Checked per element rather than by demanding a stylesheet rule
        everywhere, because a page whose hidden elements wear no
        display-setting class is already correct and should not be made to
        carry a rule it has no use for.
        """
        offenders = []
        for doc in self.documents:
            page = served_path(doc.path)
            # stylesheet() strips CSS comments. That matters here more than
            # anywhere: theme.py's comment EXPLAINING this bug names both
            # "[hidden]" and ".btn", and parsed as a rule it marks .btn settled
            # and switches this test off. It did exactly that until caught.
            css = stylesheet(doc.text)
            if HIDDEN_RULE_RE.search(css):
                continue  # the page settles it once, for every element
            rules = [(selector, body) for _at, selector, body in css_rules(css)]
            # A class the page neutralises itself -- `.results[hidden] { display:
            # none }` -- is handled, and must not be reported as if it were not.
            settled = {
                name
                for selector, body in rules
                if "[hidden]" in selector and DISPLAY_DECL_RE.search(body)
                for name in re.findall(r"\.([A-Za-z0-9_-]+)", selector)
            }
            clean = COMMENT_RE.sub(" ", doc.text)
            for tag in HIDDEN_ELEMENT_RE.finditer(clean):
                classes = CLASS_ATTR_RE.search(tag.group(0))
                for name in (classes.group(1).split() if classes else []):
                    if name in settled:
                        continue
                    for selector, body in rules:
                        # A class name ends at the token boundary: .btn must not
                        # match .btn-row, or the report names the wrong rule.
                        if "[hidden]" in selector:
                            continue
                        if not re.search(r"\.%s(?![\w-])" % re.escape(name), selector):
                            continue
                        if DISPLAY_DECL_RE.search(body):
                            offenders.append(
                                "%s: <%s ... hidden> wears .%s, and `%s` sets display"
                                % (page, tag.group(1), name, selector.strip()[:60])
                            )
        self.assertEqual(
            [], sorted(set(offenders)),
            "these elements are marked hidden but carry a class that sets "
            "display, which outranks the browser's [hidden] rule, so they stay "
            "on screen: %s" % sorted(set(offenders)),
        )


# The trading path's 129 pages are hand-written and have no generator, so the
# completion marks were added to them in place by scripts/add_progress_marks.py.
# What a generated path gets by construction, this path only has for as long as
# nobody edits a page and drops a hook -- so the hooks are checked here against
# the SAME course declaration the rest of this file uses.
DATA_LESSON_RE = re.compile(r'data-lesson="([^"]*)"')
DATA_COURSE_RE = re.compile(r'data-course="([^"]*)"\s+data-lessons="(\d+)"')
LESSON_ID_RE = re.compile(r"var id = \"([^\"]+)\";")


class TestTradingPathCanBeTicked(SiteFixture):
    """Every trading lesson is markable, and the marks add up to the course."""

    def by_url(self):
        return {served_path(doc.path): doc for doc in self.documents}

    def test_every_trading_lesson_carries_a_toggle_for_its_own_id(self):
        """A toggle keyed to the wrong lesson silently ticks a different page.

        The id is written into the page by a patcher that derives it from the
        course home's own links, so a mis-stamped page is exactly the failure
        that leaves no visible trace: the button works, the tick lands on
        another lesson, and /progress/ shows a lesson the reader never opened.
        """
        pages = self.by_url()
        wrong = []
        for _title, home, slugs in COURSES:
            for slug in slugs:
                url = lesson_url(home, slug)
                doc = pages.get(url)
                if doc is None:
                    wrong.append("%s is not published" % url)
                    continue
                if PROGRESS_TOGGLE_ID not in doc.ids:
                    wrong.append("%s has no completion toggle" % url)
                    continue
                found = LESSON_ID_RE.search(doc.text)
                expected = "%s/%s" % (home.strip("/"), slug)
                if found is None:
                    wrong.append("%s has a toggle but no id" % url)
                elif found.group(1) != expected:
                    wrong.append("%s ticks %r, not %r" % (url, found.group(1), expected))
        self.assertEqual([], sorted(wrong), "trading lesson toggles: %s" % sorted(wrong))

    def test_every_trading_course_home_hooks_exactly_its_own_lessons(self):
        pages = self.by_url()
        wrong = []
        for _title, home, slugs in COURSES:
            doc = pages[home]
            found = DATA_LESSON_RE.findall(doc.text)
            expected = ["%s/%s" % (home.strip("/"), slug) for slug in slugs]
            if found != expected:
                wrong.append(
                    "%s hooks %d card(s), expected %d; first difference %r vs %r"
                    % (home, len(found), len(expected),
                       (found or [None])[0], (expected or [None])[0])
                )
            if "courseProgress" not in doc.ids:
                wrong.append("%s has no completion count" % home)
        self.assertEqual([], sorted(wrong), "trading course homes: %s" % sorted(wrong))

    def test_the_trading_path_page_counts_each_course_correctly(self):
        """data-lessons is the denominator a reader sees; a stale one misleads."""
        doc = self.by_url()[PATH_PAGE]
        found = dict(
            (slug, int(total)) for slug, total in DATA_COURSE_RE.findall(doc.text)
        )
        expected = dict((home.strip("/"), len(slugs)) for _t, home, slugs in COURSES)
        self.assertEqual(
            expected, found,
            "the trading path page's per-course lesson counts disagree with the "
            "courses themselves, so a reader would see a total they can never reach",
        )


# Recommendations: what a reader thinks should CHANGE about a lesson, as
# opposed to the completion mark, which says they have finished it.
FEEDBACK_PANEL_ID = "lessonFeedback"
FEEDBACK_LESSON_RE = re.compile(r'<section class="lesson-feedback"[^>]*data-lesson-id="([^"]*)"', re.S)
NOSCRIPT_RE = re.compile(r"<noscript\b.*?</noscript>", re.S | re.I)


class TestEveryLessonTakesFeedback(SiteFixture):
    """The panel exists on every lesson, and is keyed to that lesson."""

    def lesson_pages(self):
        for doc in self.documents:
            if PROGRESS_TOGGLE_ID in doc.ids:
                yield served_path(doc.path), doc

    def test_every_lesson_has_a_panel_keyed_to_itself(self):
        """A panel keyed to the wrong lesson files notes against another page.

        Both families are checked in one sweep -- the 218 generated lessons and
        the 118 hand-patched trading ones -- because a reader cannot tell which
        family they are on and neither should behave differently.
        """
        wrong = []
        for url, doc in self.lesson_pages():
            if FEEDBACK_PANEL_ID not in doc.ids:
                wrong.append("%s has no feedback panel" % url)
                continue
            found = FEEDBACK_LESSON_RE.search(doc.text)
            expected = url.strip("/")
            if found is None:
                wrong.append("%s has a panel with no lesson id" % url)
            elif found.group(1) != expected:
                wrong.append("%s files notes against %r" % (url, found.group(1)))
        self.assertEqual([], sorted(wrong), "lesson feedback panels: %s" % sorted(wrong))

    def test_the_sweep_covers_both_lesson_families(self):
        """Guard the guard: this must not quietly become a check of one path."""
        urls = [url for url, _doc in self.lesson_pages()]
        trading = [u for u in urls if u.startswith("/technical-indicators/")]
        generated = [u for u in urls if u.startswith("/logic-and-proof/")]
        self.assertTrue(trading, "no trading lessons were swept")
        self.assertTrue(generated, "no generated lessons were swept")
        self.assertGreater(len(urls), 300, "only %d lesson(s) swept" % len(urls))

    def test_the_controls_are_styled_with_scripting_ON(self):
        """Rules that live only inside <noscript> style nothing for a reader.

        This is not hypothetical. The patcher that added these controls to the
        trading pages inserted its stylesheet before the LAST </style>, and
        every one of those pages ends with a <noscript><style> that hides the
        theme toggle -- so the completion button and the whole feedback panel
        rendered unstyled for everybody who had JavaScript on, which is
        everybody who can use them. Every other check passed: the markup was
        valid, the ids were right, and the behaviour worked.
        """
        unstyled = []
        for url, doc in self.lesson_pages():
            css = stylesheet(NOSCRIPT_RE.sub(" ", doc.text))
            for selector in (".progress-toggle", ".lesson-feedback", ".fb-item"):
                if selector not in css:
                    unstyled.append("%s: %s is styled only inside <noscript>" % (url, selector))
        self.assertEqual(
            [], sorted(unstyled)[:6],
            "these controls have no styling once <noscript> is discounted, so "
            "they render unstyled for every reader who can actually use them: %s"
            % sorted(unstyled)[:6],
        )
