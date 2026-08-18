"""Sequences and Series."""


from . import part_a, part_b


COURSE = {
    "slug": "sequences-and-series",
    "title": "Sequences and Series",
    "level": "Intermediate → Advanced",
    "summary": (
        "Ordered lists and the sums of their terms: recursive and closed forms, sigma notation, arithmetic and geometric families, partial sums, infinite geometric series and when they converge, repeating decimals, annuities, Pascal's triangle and the binomial theorem."
    ),
    "blurb": (
        "A sequence is a function whose input is a position. Once that is settled, two families cover almost everything a school course needs, both have a closed form for the n-th term and for the sum, and one of them can be added forever."
    ),
    "key": [
        "aₙ = a₁ + (n − 1)d          aₙ = a₁rⁿ⁻¹",
        "Sₙ = n(a₁ + aₙ)/2           Sₙ = a₁(1 − rⁿ)/(1 − r)",
        "S∞ = a₁/(1 − r)             only when |r| < 1",
        "(a + b)ⁿ = Σ C(n,k) aⁿ⁻ᵏ bᵏ",
    ],
    "assumes_short": "Courses 1\u20137",
    "assumes_long": "exponents, functions, and exact fractions",
    "outcomes_intro": (
        "By the end you can recognise which family a sequence belongs to, sum it, and say whether summing it forever gives a number."
    ),
    "outcomes": [
        ("Move between the two definitions",
         "Turn a recursive rule into a closed form and back, and say which one answers which question &mdash; the hundredth term is a closed-form question."),
        ("Read and write sigma notation",
         "Expand a sum, write one down, and shift an index without changing the value."),
        ("Sum both families",
         "Derive the arithmetic sum by pairing and the geometric sum by the `Sₙ − rSₙ` cancellation, rather than reciting either formula."),
        ("Decide whether an infinite sum exists",
         "Apply `|r| < 1` and say what the sum means when it holds &mdash; a limit of partial sums, not an act of adding infinitely many things."),
    ],
    "syllabus_intro": (
        "Lessons 1 and 2 set up sequences and the notation for their sums. Lessons 3 to 5 handle the two families and partial sums, 6 to 8 go infinite, and 9 to 11 are the binomial theorem."
    ),
    "how_to": [
        "Add the first several terms by hand before using any sum formula. It is the only way the closed form stops looking like a trick, and every lab on this course computes the sum both ways and prints both.",
        "Take the `|r| < 1` condition seriously in lesson 6. The formula returns a number for `r = 2` as happily as for `r = 1/2`, and that number is meaningless.",
        "Build Pascal's triangle by hand once, at least to row 6. Lesson 10 is much easier for anyone who has seen the coefficients appear before being given a formula for them.",
    ],
    "not_covered": [
        "Convergence tests for series in general. Only the geometric case is settled here, and it is settled completely; the rest belongs to calculus.",
        "Sequences of functions, power series and Taylor series.",
        "Mathematical induction as a proof technique. Several formulas on this course are proved by other means and stated as proved by induction elsewhere; the Discrete Mathematics path devotes a course to it.",
    ],
    "footer_lead": (
        "Every sum on this course is computed twice &mdash; once by adding the terms up and once by the closed form &mdash; and both are printed, so the formula arrives as something checked rather than something asserted. Terms and sums are exact fractions; where an infinite sum exists the lab shows the partial sums approaching it rather than jumping to the answer."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
