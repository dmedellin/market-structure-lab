"""Course 5 — Discrete Probability."""

from . import part_a, part_b

COURSE = {
    "slug": "discrete-probability",
    "title": "Discrete Probability",
    "level": "Intermediate",
    "summary": (
        "Probability over finite sample spaces: events, the axioms, conditional "
        "probability and independence, Bayes' theorem, random variables, expectation "
        "and its linearity, variance, and the binomial and geometric distributions."
    ),
    "blurb": (
        "Counting with a denominator. Every probability here is a ratio of counts, so "
        "course 4 does most of the work &mdash; and the parts that go wrong, "
        "conditioning and independence, go wrong for reasons that have nothing to do "
        "with arithmetic."
    ),
    "key": [
        "P(E) = |E| / |S|                 equally likely outcomes",
        "P(A | B) = P(A ∩ B) / P(B)",
        "independent  ⟺  P(A ∩ B) = P(A)·P(B)",
        "E[X + Y] = E[X] + E[Y]           always, independent or not",
    ],
    "assumes_short": "Courses 1–4",
    "assumes_long": "counting, sets and functions",
    "outcomes_intro": (
        "By the end you can compute a probability exactly, condition correctly, and "
        "say what an expectation does and does not tell you."
    ),
    "outcomes": [
        ("Compute a probability from a sample space",
         "Identify the outcomes, check they are equally likely, count the event, and "
         "divide &mdash; with the counting techniques of course 4."),
        ("Condition without falling into the standard traps",
         "`P(A|B)` and `P(B|A)` are different numbers, and the base rate is what "
         "separates them."),
        ("Use Bayes' theorem on a real question",
         "The medical-test calculation, done properly, and the reason its answer "
         "surprises almost everyone."),
        ("Compute expectation and variance",
         "From the definition, and by linearity &mdash; which holds whether or not the "
         "variables are independent, and is the most useful fact in the course."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 3 set up the model, 4 to 6 are conditioning, and 7 to 12 are "
        "random variables and the two distributions worth knowing by name."
    ),
    "how_to": [
        "Write the sample space down for the first few lessons, even when it is "
        "obvious. Most probability errors are errors about what the outcomes are.",
        "Use the probability lab's outcome list. Every probability on this course is a "
        "count divided by a count, and seeing the outcomes highlighted makes "
        "conditioning concrete rather than formal.",
        "Do the Bayes calculation by frequencies as well as by the formula. The two "
        "agree, and the frequency version is the one that makes the answer believable.",
    ],
    "not_covered": [
        "Continuous probability: densities, the normal distribution, and anything "
        "requiring an integral. Everything here is finite or countable.",
        "Limit theorems. The law of large numbers and the central limit theorem are "
        "mentioned where they explain something and are not proved.",
        "Markov chains, martingales and stochastic processes, which are the natural "
        "sequel and a course of their own.",
    ],
    "footer_lead": (
        "Probabilities on this course are computed as exact fractions from the "
        "enumerated sample space, so `1/6` appears as `1/6` rather than as a decimal "
        "that is nearly it. The distributions in the last lessons are summed term by "
        "term from their definitions and compared with the closed forms."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
