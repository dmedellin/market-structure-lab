"""Foundations of Algebra."""

from . import part_a, part_b

COURSE = {
    "slug": "algebra-foundations",
    "title": "Foundations of Algebra",
    "level": "Beginner",
    "summary": (
        "The real numbers and the rules for operating on them: order of operations, the properties that license every rearrangement you will make, integer and rational exponents, radicals, absolute value, and the step from arithmetic to an expression with a letter in it."
    ),
    "blurb": (
        "Arithmetic, made general. Why a letter can stand for a number, which rearrangements are always allowed and which only look allowed, and the exponent and radical rules that everything after this course leans on."
    ),
    "key": [
        "a(b + c) = ab + ac                 the distributive law",
        "x^m · x^n = x^(m+n)                exponents add",
        "x^(1/n) = the n-th root of x",
        "|x| = x if x ≥ 0, −x if x < 0",
    ],
    "assumes_short": "Arithmetic",
    "assumes_long": "fractions, negatives, and long division",
    "outcomes_intro": (
        "By the end you can evaluate and rearrange any expression in this path without guessing at which move is legal."
    ),
    "outcomes": [
        ("Evaluate without ambiguity",
         "Apply the order of operations to an expression with nested brackets, exponents and a fraction bar, and get the value a marker gets."),
        ("Name the property you used",
         "Say which of commutativity, associativity, distribution or the identity you just applied &mdash; and notice when you have used one that does not exist."),
        ("Work fluently with exponents and radicals",
         "Combine powers, handle a zero or negative exponent, convert between `x^(1/n)` and roots, and simplify a radical to its lowest form."),
        ("Turn a sentence into an expression",
         "Translate an English quantity into algebra, keeping track of what the letter stands for &mdash; which is where most word-problem errors are made."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 4 are the number system and the rules; 5 to 9 are exponents and radicals; 10 to 13 build expressions and read them back as English."
    ),
    "how_to": [
        "Do the arithmetic yourself before you read the answer. Every lab shows its steps, and the steps are worth more than the result &mdash; the result you could have got from a calculator.",
        "Take the property lessons seriously even if the arithmetic is easy. Lesson 2 is the reason `-(x - 3)` is `-x + 3`, and that single sign is the most common error in the next two courses.",
        "When a lab disagrees with you, find which step differs rather than which answer. The step is the thing you will repeat a thousand times.",
    ],
    "not_covered": [
        "Proof of the field axioms. This course states the properties of the real numbers and uses them; constructing the reals from the rationals belongs to analysis.",
        "Complex numbers. `sqrt(-4)` has no value on this course and is said to have none; course 6 introduces `i` and gives it one.",
        "Trigonometry and logarithms. Logarithms arrive in course 7, where exponentials make them necessary; trigonometry is not on this path at all.",
    ],
    "footer_lead": (
        "Every value on this course is computed in your browser by applying the rule the lesson states, and the arithmetic is exact &mdash; a third is `1/3` through every step, not `0.3333`. Where a lesson is about approximation it says so and shows the rounding it did."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
