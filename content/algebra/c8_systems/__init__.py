"""Systems, Matrices and Sequences."""

from . import part_a, part_b

COURSE = {
    "slug": "systems-matrices-and-sequences",
    "title": "Systems, Matrices and Sequences",
    "level": "Advanced",
    "summary": (
        "Several equations at once, the array that organises them, and the ordered lists that algebra ends on: substitution and elimination, three-variable systems, row reduction, matrix arithmetic, determinants and inverses, linear programming, arithmetic and geometric sequences and series, and the binomial theorem."
    ),
    "blurb": (
        "Solve for several unknowns together, then find the notation that makes it mechanical. Matrices are elimination with the letters removed. The course closes with sequences, series and the binomial theorem &mdash; algebra's last look back at counting."
    ),
    "key": [
        "one solution, none, or infinitely many  —  and nothing else",
        "aₙ = a₁ + (n − 1)d          aₙ = a₁r^(n−1)",
        "Sₙ = n(a₁ + aₙ)/2           S∞ = a₁/(1 − r),  |r| < 1",
        "(a + b)ⁿ = Σ C(n,k) aⁿ⁻ᵏ bᵏ",
    ],
    "assumes_short": "Courses 1–7",
    "assumes_long": "lines, functions, and exact fraction arithmetic",
    "outcomes_intro": (
        "By the end you can solve a system of any size by hand, and recognise the two sequence families and sum them."
    ),
    "outcomes": [
        ("Solve a system three ways",
         "By substitution, by elimination and by graphing, and say which is quickest for a given system before starting."),
        ("Classify before solving",
         "Recognise an inconsistent system and a dependent one from the algebra, and connect each to what the lines or planes are doing."),
        ("Row reduce",
         "Write a system as an augmented matrix, carry it to reduced row echelon form, and read the solution &mdash; including when there is not exactly one."),
        ("Sum a sequence",
         "Identify an arithmetic or geometric sequence, find its n-th term and its sum, and know when an infinite geometric series has one."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 4 solve systems by hand; 5 to 10 build the matrix machinery and apply it; 11 to 14 are sequences, series and the binomial theorem."
    ),
    "how_to": [
        "Do the elimination by hand before using the matrix lessons. Row reduction is the same arithmetic with the `x`s deleted, and it is opaque if you have not done it with them.",
        "Keep everything in fractions. Row reduction produces thirds and sevenths immediately, and a decimal here compounds into a visibly wrong answer three rows later.",
        "In the series lessons, add the first several terms by hand and compare with the formula. It is the only way the infinite sum stops looking like a trick.",
    ],
    "not_covered": [
        "Vector spaces, linear independence, rank and eigenvalues. This is the matrix algebra a school course needs, not a linear algebra course.",
        "Convergence tests for general series. Only the geometric case is settled here, and it is settled completely.",
        "Mathematical induction as a proof technique, which the Discrete Mathematics path covers in a course of its own.",
    ],
    "footer_lead": (
        "Row reduction and every system solution on this course are computed in exact fractions &mdash; the arithmetic that produces a visibly wrong answer in floating point is exactly the arithmetic these lessons are about. Sums are computed term by term as well as by formula, so the formula is checked rather than asserted."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
