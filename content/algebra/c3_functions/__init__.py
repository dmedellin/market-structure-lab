"""Lines, Functions and Graphs."""

from . import part_a, part_b

COURSE = {
    "slug": "lines-functions-and-graphs",
    "title": "Lines, Functions and Graphs",
    "level": "Beginner → Intermediate",
    "summary": (
        "The plane, the line, and the idea of a function: slope and the forms of a linear equation, parallel and perpendicular, what makes a rule a function, domain and range, piecewise definitions, transformations, composition and inverses."
    ),
    "blurb": (
        "Put algebra on a picture. Slope and every form of a line, then the definition that organises the rest of the path &mdash; a function &mdash; with its notation, its domain, the transformations that move its graph, and its inverse."
    ),
    "key": [
        "m = (y₂ − y₁)/(x₂ − x₁)",
        "y = mx + b        y − y₁ = m(x − x₁)",
        "m₁m₂ = −1         perpendicular",
        "(f ∘ g)(x) = f(g(x))         f⁻¹(f(x)) = x",
    ],
    "assumes_short": "Courses 1–2",
    "assumes_long": "solving and rearranging linear equations",
    "outcomes_intro": (
        "By the end you can move between an equation, its graph and its description in words without re-deriving the connection each time."
    ),
    "outcomes": [
        ("Read and write a line four ways",
         "Move between slope-intercept, point-slope, standard form and two given points, and pick the form that makes the question easy."),
        ("Apply the definition of a function",
         "Decide whether a rule, a table or a graph defines a function, and say which input breaks it when one does."),
        ("State a domain and a range",
         "Find what a formula excludes &mdash; a zero denominator, a negative under a square root &mdash; and write the result in interval notation."),
        ("Transform, compose and invert",
         "Predict the graph of `a·f(b(x − h)) + k` from the parent, compose two functions in the right order, and find an inverse and the restriction it needs."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 6 are lines. Lesson 7 defines a function, and 8 to 14 develop everything a function has: notation, domain, shape, composition, inverse."
    ),
    "how_to": [
        "Sketch before you compute. Every graphing lab lets you type your own function; predicting the picture and then drawing it is worth more than reading the picture.",
        "Watch the order in the transformation lesson. `f(x − 3)` moves right, not left, and no amount of memorising fixes it &mdash; watch the lab move the curve while you change the number.",
        "Composition is not multiplication. `(f ∘ g)` and `(g ∘ f)` are different functions, and the lab computes both side by side for exactly that reason.",
    ],
    "not_covered": [
        "Continuity and limits. The word \"smooth\" is used informally here; making it precise is calculus.",
        "Polynomial and rational graphs beyond lines, which need factoring and arrive in courses 4 and 5.",
        "Conic sections. Circles and ellipses are not functions of `x`, and this course is about functions.",
    ],
    "footer_lead": (
        "Every curve on this course is drawn by evaluating the function at hundreds of points and joining them; nothing is a stored shape. When a lab marks a vertex or an intercept, the label and the picture come from the same computation, so the drawing cannot flatter the answer."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
