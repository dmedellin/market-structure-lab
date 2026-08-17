"""Quadratics and Complex Numbers."""

from . import part_a, part_b

COURSE = {
    "slug": "quadratics-and-complex-numbers",
    "title": "Quadratics and Complex Numbers",
    "level": "Intermediate",
    "summary": (
        "The quadratic, four ways: factoring, the square root property, completing the square and the formula that completing the square proves. Then the discriminant, the complex numbers that appear when it is negative, parabolas, optimisation and quadratic inequalities."
    ),
    "blurb": (
        "One equation shape, four solution methods, and a number system that has to be extended so that every one of them always finishes. Completing the square is the centre of the course: it derives the formula and it puts a parabola in vertex form."
    ),
    "key": [
        "ab = 0  ⟹  a = 0 or b = 0",
        "x = (−b ± sqrt(b² − 4ac)) / 2a",
        "b² − 4ac  >  0, = 0, <  0     two, one, none (real)",
        "i² = −1        y = a(x − h)² + k",
    ],
    "assumes_short": "Courses 1–5",
    "assumes_long": "factoring and radical simplification",
    "outcomes_intro": (
        "By the end you can solve any quadratic, know before you start how many real solutions it has, and read its graph off its form."
    ),
    "outcomes": [
        ("Pick a method deliberately",
         "Use factoring when it is quick, the square root property when there is no linear term, and the formula when nothing else applies &mdash; not always the formula."),
        ("Complete the square",
         "Carry out the process on any quadratic, and recognise it as both the derivation of the formula and the route to vertex form."),
        ("Use the discriminant",
         "Predict the number and kind of solutions before solving, and connect that to the number of times the parabola meets the x-axis."),
        ("Work with complex numbers",
         "Add, multiply and divide complex numbers, use the conjugate, and interpret a conjugate pair of roots as a parabola that misses the axis."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 6 solve quadratics and count their solutions; 7 to 9 build the complex numbers; 10 to 14 graph, optimise and extend."
    ),
    "how_to": [
        "Complete the square by hand at least five times. It is the one procedure in this course that pays for itself twice &mdash; once as the formula, once as vertex form.",
        "Use the discriminant before you solve, every time. Knowing the answer is a conjugate pair before you start prevents the most common error, which is discarding a negative under the root.",
        "In the graphing lessons, change one coefficient at a time and watch. `a`, `h` and `k` each do exactly one thing, and seeing them separated is worth more than the formula.",
    ],
    "not_covered": [
        "Polar form of complex numbers, De Moivre's theorem and complex roots of unity, which need trigonometry.",
        "Cubic and quartic formulas. Course 4's rational root theorem is the tool this path gives for higher degrees.",
        "Conic sections in general. The parabola appears here as the graph of a quadratic function, not as a locus.",
    ],
    "footer_lead": (
        "Every quadratic on this course is solved by all four methods at once, in exact arithmetic, and the four answers are compared on screen &mdash; they agree because they are computed independently. Roots, vertex and axis are marked on the parabola using the same numbers printed beside it."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
