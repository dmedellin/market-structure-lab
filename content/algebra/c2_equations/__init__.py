"""Linear Equations and Inequalities."""

from . import part_a, part_b

COURSE = {
    "slug": "linear-equations-and-inequalities",
    "title": "Linear Equations and Inequalities",
    "level": "Beginner",
    "summary": (
        "Solving for an unknown: what a solution is, the operations that preserve one, equations with fractions and with the variable on both sides, formulas rearranged for any letter, inequalities and their one surprising rule, and absolute value."
    ),
    "blurb": (
        "Find the value that makes a statement true &mdash; and know why each move you made kept it true. Linear equations, literal formulas, inequalities, compound and absolute value statements, and the notation for writing a solution set down."
    ),
    "key": [
        "a = b  ⟹  a + c = b + c            and the same for ×, ÷ by a nonzero c",
        "multiply an inequality by a negative  ⟹  reverse it",
        "|x| = k  ⟹  x = k  or  x = −k       two equations, not one",
        "0 = 5   no solution        0 = 0   every number",
    ],
    "assumes_short": "Course 1",
    "assumes_long": "expressions, exponents, the distributive law",
    "outcomes_intro": (
        "By the end you can solve any linear statement and say what its solution set is, in either standard notation."
    ),
    "outcomes": [
        ("Solve and justify",
         "Carry a linear equation to `x = ` a number, naming the operation applied to both sides at each step, and check the answer in the ORIGINAL equation."),
        ("Recognise the three outcomes",
         "Tell a conditional equation from an identity and from a contradiction, and read `0 = 0` and `0 = 5` correctly rather than as \"x = 0\"."),
        ("Rearrange any formula",
         "Solve a literal equation for whichever letter is asked for, including when that letter appears twice."),
        ("Handle inequalities and absolute value",
         "Solve linear, compound and absolute-value statements, reverse the sign when and only when you must, and write the answer in interval notation."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 6 are equations, 7 and 8 apply them, and 9 to 13 are inequalities, absolute value and the notation for a solution set."
    ),
    "how_to": [
        "Check every answer by substituting it back. It costs ten seconds and it catches the arithmetic slip that a step-by-step trace will not.",
        "Do the fraction lessons without decimals. `x = 7/3` is the answer; `x = 2.333` is a rounding of it, and the rest of this path expects the fraction.",
        "In the inequality lessons, test a number from your own answer against the original statement. A reversed sign is invisible in the algebra and obvious in the test.",
    ],
    "not_covered": [
        "Quadratic and higher equations. `x^2 = 9` waits for course 6, where the two roots and the reason there are exactly two are both handled properly.",
        "Systems of several equations at once, which need their own machinery and get it in course 8.",
        "Inequalities involving products or quotients of factors, which need sign analysis and arrive in courses 5 and 6.",
    ],
    "footer_lead": (
        "Every solution on this course is found by the same steps shown on screen, in exact fractions, and then substituted back into the original statement by the lab itself. A check that passes is evidence the step list is right; the step list is what the lesson is teaching."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
