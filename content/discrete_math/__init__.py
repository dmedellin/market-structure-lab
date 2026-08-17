"""The Discrete Mathematics path, as data.

Eight courses in one order. The content lives here and only here; scripts/
turns it into pages. Nothing in this package emits markup beyond the inline
`x` shorthand, and nothing in scripts/ decides what a lesson says.
"""

from . import (
    c1_logic,
    c2_sets,
    c3_induction,
    c4_counting,
    c5_probability,
    c6_number_theory,
    c7_graphs,
    c8_algorithms,
)

# A course module still being authored exports COURSE = None. It is filtered
# here rather than left out of the import list, so an unfinished course is
# visible in the source and cannot be forgotten.
COURSES = [c for c in [
    c1_logic.COURSE,
    c2_sets.COURSE,
    c3_induction.COURSE,
    c4_counting.COURSE,
    c5_probability.COURSE,
    c6_number_theory.COURSE,
    c7_graphs.COURSE,
    c8_algorithms.COURSE,
] if c is not None]

for _index, _course in enumerate(COURSES, start=1):
    _course["number"] = _index

PATH = {
    "slug": "discrete-math",
    "title": "Discrete Mathematics",
    "level": "Beginner → Advanced",
    "level_note": "no calculus required",
    "tagline": (
        "The mathematics of things you can count, list and check: statements that "
        "are true or false, sets and the relations between them, proof by "
        "induction, counting without enumerating, probability over finite "
        "outcomes, the arithmetic of remainders, graphs, and the analysis of the "
        "algorithms that run on all of it. Eight courses, taken front to back."
    ),
    "description": (
        "The Discrete Mathematics path: eight courses in one deliberate order, from "
        "propositional logic and proof through sets, relations and functions, "
        "induction and recursion, combinatorics, discrete probability, number theory "
        "and cryptography, graphs and trees, and the analysis of algorithms. All "
        "eight courses and 106 lessons are available. Every lesson is one "
        "self-contained page whose figures are computed in your browser."
    ),
    "key": [
        "∀n ∈ ℕ.  P(n)          proved by induction, not by checking",
        "|A ∪ B| = |A| + |B| − |A ∩ B|",
        "C(n, k) = n! / (k!(n−k)!)",
        "gcd(a, b) = ax + by          for some integers x, y",
        "Σ deg(v) = 2|E|",
        "T(n) = 2T(n/2) + n  ⟹  T(n) = Θ(n log n)",
    ],
    "sequence_intro": (
        "Each course assumes the ones before it and nothing else. Course 3 proves "
        "things about the sets built in course 2; course 5 counts the outcomes "
        "course 4 taught you to count; course 8 analyses the structures course 7 "
        "built."
    ),
    "why_order": [
        "Logic comes first because everything after it is a claim that has to be "
        "stated precisely enough to be true or false. A reader who has not settled "
        "what `∀x ∃y P(x, y)` means cannot read a single theorem in the later "
        "courses, and will silently misread several.",
        "Sets, relations and functions come second because they are the vocabulary. "
        "An equivalence relation, a bijection and a partial order each appear in "
        "four of the six courses that follow; they are introduced once.",
        "Induction is third rather than last because it is the proof technique the "
        "rest of the path depends on. Counting arguments, recurrence solutions, "
        "graph theorems and algorithm correctness are all induction wearing "
        "different clothes.",
        "Counting, probability and number theory then apply that machinery to three "
        "specific worlds, and graphs give it an object to act on. Algorithms and "
        "complexity comes last because it needs all of them: recurrences from "
        "course 3, counting from course 4, and graphs from course 7.",
    ],
    "prerequisites": [
        "School algebra, and nothing beyond it. You need to be comfortable "
        "rearranging an equation, working with exponents, and reading summation "
        "notation &mdash; the first course that uses `Σ` explains it where it "
        "first appears.",
        "No calculus. Nothing on this path takes a limit, a derivative or an "
        "integral. Where a growth rate is compared to another, it is compared by "
        "an explicit constant and threshold rather than by a limit.",
        "No programming. Course 8 reads pseudocode and course 6 walks through "
        "algorithms step by step, but nothing asks you to write or run code. The "
        "labs execute in your browser so that you can watch an algorithm rather "
        "than implement it.",
        "Patience with definitions. The single largest difficulty in this subject "
        "is that its words are used precisely: <em>or</em> is inclusive, "
        "<em>some</em> means at least one, and a <em>graph</em> is not a plot. "
        "Every one of those is stated where it first matters.",
    ],
    # The hazard of learning THIS subject from interactive examples: a widget
    # that checks a claim for n = 1..40 has demonstrated nothing about n = 41,
    # and course 3 is about exactly that.
    "material": (
        "every figure is computed in your browser from the stated definition, "
        "and a worked example is not a proof."
    ),
    "footer_lead": (
        "<strong>Educational course material.</strong> Every figure on this path is "
        "computed in your browser from the definition the lesson states &mdash; the "
        "counting is done in exact integer arithmetic and the probabilities as exact "
        "fractions, so the numbers are not approximations. What the labs cannot do is "
        "prove anything: checking a statement for the cases on screen is evidence "
        "about those cases and nothing more, which is the subject of course 3."
    ),
    "courses": COURSES,
}
