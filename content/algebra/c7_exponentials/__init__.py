"""Exponential and Logarithmic Functions."""

from . import part_a, part_b

COURSE = {
    "slug": "exponential-and-logarithmic-functions",
    "title": "Exponential and Logarithmic Functions",
    "level": "Intermediate → Advanced",
    "summary": (
        "Growth that compounds, and the function that undoes it: exponential functions and their graphs, decay, the number e, the logarithm as an inverse, the three laws, change of base, solving equations of both kinds, and the scales built on logarithms."
    ),
    "blurb": (
        "The variable moves into the exponent, and ordinary algebra stops working. A logarithm is the tool that brings it back down &mdash; defined as an inverse, with three laws that are the exponent laws read backwards."
    ),
    "key": [
        "log_b(x) = y   ⟺   b^y = x",
        "log(MN) = log M + log N        log(M/N) = log M − log N",
        "log(M^p) = p·log M              the law that solves equations",
        "A = P·e^(rt)        e = 2.71828…",
    ],
    "assumes_short": "Courses 1–6",
    "assumes_long": "exponents, inverse functions, and graphing",
    "outcomes_intro": (
        "By the end you can solve for a variable in an exponent, and read a logarithmic scale for what it is."
    ),
    "outcomes": [
        ("Read an exponential graph",
         "Identify growth from decay by the base alone, find the horizontal asymptote, and say why the curve never reaches it."),
        ("Define a logarithm correctly",
         "State `log_b(x)` as the exponent that produces `x`, convert between the two forms instantly, and evaluate one without a calculator when you can."),
        ("Apply the three laws",
         "Expand and condense logarithmic expressions, and avoid the two invented laws that catch everyone &mdash; `log(M + N)` and `log M / log N`."),
        ("Solve both kinds of equation",
         "Take a logarithm of both sides to bring a variable down, exponentiate to undo a logarithm, and check every answer against the domain."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 3 are exponential functions and `e`; 4 to 8 define the logarithm and its laws; 9 to 12 solve and apply."
    ),
    "how_to": [
        "Say the definition out loud until it is automatic: a logarithm is an exponent. Almost every error in this course is a step taken without that sentence in mind.",
        "Check the domain of every solution to a logarithmic equation. `log(x - 5)` has nothing to say about `x = 2`, and the algebra will happily produce it.",
        "Use the log-scale lesson on numbers you know. The distance from 1 to 10 being the same as 10 to 100 is either obvious or wrong-feeling, and it is worth being the first.",
    ],
    "not_covered": [
        "The derivative of `e^x` and the reason `e` is the natural base for calculus. This course gives `e` by compounding, which is honest and complete for algebra.",
        "Logarithms of negative and complex numbers.",
        "Curve fitting and regression on transformed data, which is a statistics topic.",
    ],
    "footer_lead": (
        "Exponential and logarithmic values are irrational, so this is the one course on the path where the labs show rounded decimals &mdash; and they say where they rounded. The exact statements, the laws and the domains, are computed exactly and the rounding never enters them."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
