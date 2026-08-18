"""The Algebra path, as data.

Nine courses in one order. The content lives here and only here; scripts/
turns it into pages. Nothing in this package emits markup beyond the inline
`x` shorthand, and nothing in scripts/ decides what a lesson says.
"""

from . import (
    c1_foundations,
    c2_equations,
    c3_functions,
    c4_polynomials,
    c5_rational,
    c6_quadratics,
    c7_exponentials,
    c8_systems,
    c9_sequences,
)

# A course module still being authored exports COURSE = None. It is filtered
# here rather than left out of the import list, so an unfinished course is
# visible in the source and cannot be forgotten.
COURSES = [c for c in [
    c1_foundations.COURSE,
    c2_equations.COURSE,
    c3_functions.COURSE,
    c4_polynomials.COURSE,
    c5_rational.COURSE,
    c6_quadratics.COURSE,
    c7_exponentials.COURSE,
    c8_systems.COURSE,
    c9_sequences.COURSE,
] if c is not None]

for _index, _course in enumerate(COURSES, start=1):
    _course["number"] = _index

PATH = {
    "slug": "algebra",
    "title": "Algebra",
    "level": "Beginner → Advanced",
    "level_note": "arithmetic is the only prerequisite",
    "tagline": (
        "The language the rest of mathematics is written in: expressions and the "
        "rules for rearranging them, equations and what it means to solve one, "
        "functions and their graphs, polynomials and factoring, quadratics and the "
        "complex numbers they force into existence, exponentials and logarithms, and "
        "systems solved several unknowns at a time, and the sums of ordered lists. Nine courses, taken front to back."
    ),
    "description": (
        "The Algebra path: nine courses in one deliberate order, from the real numbers "
        "and the properties that license every rearrangement, through linear equations "
        "and inequalities, lines and functions, polynomials and factoring, rational and "
        "radical expressions, quadratics and complex numbers, exponentials and "
        "logarithms, to systems and matrices, and sequences and series. All nine courses and 112 "
        "lessons are available. Every lesson is one self-contained page whose figures "
        "are computed in your browser."
    ),
    "key": [
        "a(b + c) = ab + ac              the law behind almost every rearrangement",
        "x = (−b ± √(b² − 4ac)) / 2a",
        "f(c) = 0   ⟺   (x − c) is a factor of f",
        "log_b(x) = y   ⟺   b^y = x",
        "aₙ = a₁r^(n−1)                  Sₙ = a₁(1 − rⁿ)/(1 − r)",
    ],
    "sequence_intro": (
        "Each course assumes the ones before it and nothing else. Course 4 factors the "
        "expressions course 1 taught you to build; course 5 cannot start until you can "
        "factor; course 6 needs both, and course 8 needs all of them."
    ),
    "why_order": [
        "Foundations comes first because algebra is arithmetic with the numbers "
        "withheld, and every later move is one of a small set of properties applied to "
        "an expression. A reader who cannot say why `-(x - 3)` is `-x + 3` will make "
        "that error in every course that follows, and will not know they made it.",
        "Equations come second, and functions third, in that order rather than the "
        "reverse. Solving is a mechanical skill built on the properties; a function is "
        "an idea, and it is far easier to meet once you can already manipulate the "
        "formula that defines one.",
        "Factoring sits in the middle of the path because it is the bottleneck. "
        "Rational expressions, quadratics, and every polynomial graph after course 4 "
        "are stated in terms of factors, and none of those techniques applies to a sum. "
        "It is placed where there is still time to practise it.",
        "Exponentials and logarithms come seventh because a logarithm is an inverse "
        "function, and inverse functions are course 3. Systems and matrices come last "
        "because row reduction is elimination performed on exact fractions, and it is "
        "unreadable to anyone not already fluent in both.",
    ],
    "prerequisites": [
        "Arithmetic, and specifically arithmetic with fractions and negative numbers. "
        "If `-3 - (-5)` and `2/3 ÷ 4/9` are not automatic, do those first &mdash; every "
        "course here runs on them, and course 8 runs on them for pages at a time.",
        "No prior algebra. Course 1 starts from what a variable is. If you have met "
        "some of this before, the labs are still worth opening: they show the step "
        "list, and a wrong step list survives a lot of correct answers.",
        "No calculus, and none is used. Course 6 finds a maximum with the vertex of a "
        "parabola rather than a derivative, which is the honest algebraic method and "
        "not a workaround.",
        "No programming. Nothing here asks you to write code. The labs run so that you "
        "can change a coefficient and watch what moves, which is the one thing a "
        "printed page cannot do.",
    ],
    # The hazard of learning THIS subject from interactive examples is not the
    # same one. Algebra's characteristic error is the invented law -- cancelling
    # a term rather than a factor, log(M + N), (a + b)^2 = a^2 + b^2 -- and each
    # of those gives the right answer on SOME example. Watching a step work is
    # therefore not evidence that the step is a rule.
    "material": (
        "every figure is computed in your browser from the stated definition, "
        "and a step that gives the right answer here is not thereby a valid rule."
    ),
    "footer_lead": (
        "<strong>Educational course material.</strong> Every figure on this path is "
        "computed in your browser from the definition the lesson states, and the "
        "arithmetic is exact &mdash; coefficients, solutions and steps are carried as "
        "fractions, so `1/3` is `1/3` after twenty operations rather than `0.333`. "
        "Curves are drawn by evaluating the function, never from a stored shape. Where "
        "a quantity is genuinely irrational the lab says where it rounded."
    ),
    "courses": COURSES,
}
