"""Systems and Matrices."""


from . import part_a, part_b


COURSE = {
    "slug": "systems-and-matrices",
    "title": "Systems and Matrices",
    "level": "Advanced",
    "summary": (
        "Several equations at once, and the array that makes solving them mechanical: substitution, elimination, three-variable systems, row operations, Gaussian elimination, matrix arithmetic, determinants, inverses, and linear programming."
    ),
    "blurb": (
        "Solve for several unknowns together, then find the notation that removes the bookkeeping. A matrix is elimination with the letters deleted, which is why this course does elimination by hand first and only then writes it down as rows."
    ),
    "key": [
        "one solution, none, or infinitely many  —  and nothing else",
        "R2 → R2 − 3R1        an elimination step, written as a row operation",
        "det A = 0   ⟺   A has no inverse",
        "the optimum of a linear objective sits at a corner",
    ],
    "assumes_short": "Courses 1\u20137",
    "assumes_long": "lines, functions, and exact fraction arithmetic",
    "outcomes_intro": (
        "By the end you can solve a system of any size by hand and say, before finishing, how many solutions it has."
    ),
    "outcomes": [
        ("Solve a system three ways",
         "By substitution, by elimination and by graphing, and say which is quickest for a given system before starting."),
        ("Classify before solving",
         "Recognise an inconsistent system and a dependent one from the algebra, and connect each to what the lines or planes are doing."),
        ("Row reduce",
         "Write a system as an augmented matrix, carry it to reduced row echelon form, and read the solution &mdash; including when there is not exactly one."),
        ("Use the determinant as a test",
         "Compute it two ways, use it to decide invertibility before attempting an inverse, and apply Cramer's rule where it is the quickest route."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 4 solve systems by hand. Lessons 5 to 9 build the matrix machinery that automates exactly that work, and lesson 10 applies it."
    ),
    "how_to": [
        "Do the elimination by hand before starting lesson 5. Row reduction is the same arithmetic with the `x`s deleted, and it is opaque to anyone who has not done it with them.",
        "Keep everything in fractions. Row reduction produces thirds and sevenths immediately, and a decimal here compounds into a visibly wrong answer three rows later &mdash; which is why every lab on this course is exact.",
        "Check an inverse by multiplying. `A⁻¹` is only the inverse if `AA⁻¹` is the identity, and the lab performs that multiplication rather than asserting it.",
    ],
    "not_covered": [
        "Vector spaces, linear independence, rank as a general concept, and eigenvalues. This is the matrix algebra a school course needs, not a linear algebra course.",
        "Systems with more equations than unknowns, least squares, and numerical conditioning.",
        "The simplex algorithm. Linear programming here is done by evaluating the objective at every corner of a feasible region you can draw.",
    ],
    "footer_lead": (
        "Row reduction and every system solution on this course are computed in exact fractions &mdash; the arithmetic that goes visibly wrong in floating point is exactly the arithmetic these lessons are about. Where a lab reports an inverse it multiplies the two matrices together in front of you rather than claiming the result."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
