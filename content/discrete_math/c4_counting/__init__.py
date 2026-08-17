"""Course 4 — Combinatorics and Counting."""

from . import part_a, part_b

COURSE = {
    "slug": "combinatorics-and-counting",
    "title": "Combinatorics and Counting",
    "level": "Intermediate",
    "summary": (
        "Counting without enumerating: the sum and product rules, permutations and "
        "combinations, the binomial theorem, repetition, inclusion and exclusion, "
        "derangements, the generalised pigeonhole principle, generating functions and "
        "combinatorial proof."
    ),
    "blurb": (
        "How many? The two basic rules, the four ways to choose `r` from `n`, what "
        "changes when repetition is allowed, how to correct an over-count, and the "
        "double-counting arguments that prove identities without algebra."
    ),
    "key": [
        "P(n, r) = n!/(n−r)!            ordered, no repetition",
        "C(n, r) = n!/(r!(n−r)!)        unordered, no repetition",
        "C(n+r−1, r)                    unordered, with repetition",
        "|A ∪ B ∪ C| = ΣA − Σ(pairs) + |A∩B∩C|",
    ],
    "assumes_short": "Courses 1–3",
    "assumes_long": "sets, functions and induction",
    "outcomes_intro": (
        "By the end you can choose the right rule, justify the choice, and check the "
        "answer against a small enumeration."
    ),
    "outcomes": [
        ("Pick the right one of four rules",
         "Ordered or not, repetition or not. The arithmetic is easy; the classification "
         "is where the answer is won or lost."),
        ("Count with restrictions",
         "Complementary counting, cases, and knowing when to count the bad outcomes "
         "instead of the good ones."),
        ("Correct an over-count",
         "Inclusion and exclusion for any number of sets, and derangements as the "
         "canonical application."),
        ("Prove an identity by counting",
         "Count one set two ways and conclude the two expressions are equal &mdash; "
         "shorter and more informative than the algebra."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 4 are the basic rules, 5 to 8 the binomial coefficients and "
        "repetition, 9 to 11 corrections and bounds, and 12 to 14 the techniques that "
        "generalise them."
    ),
    "how_to": [
        "Check every formula against an enumeration while the numbers are small. The "
        "counting lab lists the actual selections up to 400 of them, and a formula that "
        "disagrees with the list is wrong however good the reasoning looked.",
        "Say out loud whether order matters and whether repetition is allowed, before "
        "writing anything. Almost every wrong answer in this course is a right "
        "calculation of the wrong quantity.",
        "Do the combinatorial proofs in lesson 13 twice: once by algebra and once by "
        "counting. The second is shorter and tells you why the identity is true.",
    ],
    "not_covered": [
        "Advanced enumerative combinatorics: species, the transfer-matrix method, and "
        "the deeper theory of generating functions. Lesson 12 is an introduction, not "
        "a survey.",
        "Design theory, Latin squares and error-correcting codes, which are the natural "
        "applications of this material but a separate subject.",
        "Ramsey theory beyond the statement that `R(3,3) = 6`, which appears in lesson "
        "11 as a pigeonhole application.",
    ],
    "footer_lead": (
        "Every count on this course is computed in exact big-integer arithmetic, so a "
        "figure like `52!` is the number and not a floating-point approximation of it. "
        "Where the total is small enough to list, the lab lists it and checks the "
        "formula against the enumeration."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
