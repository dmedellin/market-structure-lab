"""Polynomials and Factoring."""

from . import part_a, part_b

COURSE = {
    "slug": "polynomials-and-factoring",
    "title": "Polynomials and Factoring",
    "level": "Intermediate",
    "summary": (
        "Polynomial arithmetic and the reverse of it: degree and standard form, the four operations, special products, every standard factoring technique, long and synthetic division, the remainder and factor theorems, rational roots and polynomial graphs."
    ),
    "blurb": (
        "Multiply out, then learn to go back. The factored form is the one that answers questions &mdash; where a graph crosses, when a product is zero &mdash; and this course is about producing it reliably rather than by inspection."
    ),
    "key": [
        "(a + b)(a − b) = a² − b²",
        "(a ± b)² = a² ± 2ab + b²",
        "f(c) = 0   ⟺   (x − c) is a factor",
        "root p/q  ⟹  p | a₀  and  q | aₙ",
    ],
    "assumes_short": "Courses 1–3",
    "assumes_long": "exponents, distribution, function notation",
    "outcomes_intro": (
        "By the end you can factor any polynomial a school course will hand you, and say when one cannot be factored."
    ),
    "outcomes": [
        ("Operate on polynomials",
         "Add, subtract and multiply polynomials of any degree, and recognise the special products on sight rather than expanding them."),
        ("Choose the right factoring technique",
         "Work down a decision list &mdash; common factor, then count the terms, then match a pattern &mdash; instead of trying methods at random."),
        ("Divide polynomials",
         "Carry out long division, use synthetic division where it applies, and read the remainder as a function value."),
        ("Find every rational root",
         "Generate the candidate list from the constant and leading coefficients, test it, and know that an empty result is an answer."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 4 multiply. Lessons 5 to 9 factor, in the order you should try the techniques. Lessons 10 to 13 divide and then graph."
    ),
    "how_to": [
        "Always look for a common factor first. The lab's decision list starts there because skipping it is what turns a one-line problem into an unfactorable-looking mess.",
        "Expand your factored answer to check it. Factoring is the only topic on this path where checking is faster than the work itself.",
        "Use the rational-root lab on something that has no rational root. Watching a complete search come back empty is the fastest way to believe the theorem.",
    ],
    "not_covered": [
        "Factoring over the complex numbers, and the fundamental theorem of algebra. Course 6 introduces `i` and factors quadratics with it; the general theorem is stated there and not proved.",
        "Numerical root-finding. Where a polynomial has an irrational root, this course says so and stops; approximating it is a computational topic.",
        "Polynomial interpolation and finite differences.",
    ],
    "footer_lead": (
        "Every factorisation on this course is SEARCHED for, in exact integer arithmetic, by the theorem the lesson states &mdash; the candidate list is generated and each candidate tested where you can see it. When a lab reports that a polynomial does not factor over the rationals, that is the result of a complete search, not a lookup."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
