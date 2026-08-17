"""Course 2 — Sets, Relations, and Functions."""

from . import part_a, part_b

COURSE = {
    "slug": "sets-relations-functions",
    "title": "Sets, Relations, and Functions",
    "level": "Beginner",
    "summary": (
        "The vocabulary the rest of the path is written in: sets and their algebra, "
        "power sets and Cartesian products, relations and the two kinds that matter "
        "(equivalence and order), functions and the three properties they may have, "
        "cardinality, and the pigeonhole principle."
    ),
    "blurb": (
        "Sets, the operations on them and the identities those obey; relations and "
        "the two structures they produce &mdash; partitions and orderings; functions, "
        "injections, surjections and bijections; countable and uncountable; and the "
        "counting principle that follows from all of it."
    ),
    "key": [
        "A ⊆ B        ⟺  ∀x (x ∈ A → x ∈ B)",
        "|P(A)| = 2^|A|                    the power set doubles",
        "equivalence relation  ⟺  partition",
        "|A| = |B|    ⟺  a bijection A → B exists",
    ],
    "assumes_short": "Course 1",
    "assumes_long": "quantifiers and proof technique",
    "outcomes_intro": (
        "By the end you have the objects every later course manipulates, and the "
        "proof habits from course 1 applied to them."
    ),
    "outcomes": [
        ("Prove a set identity",
         "By double inclusion or by a chain of laws &mdash; and know that a Venn "
         "diagram illustrates an identity without proving it."),
        ("Classify a relation",
         "Decide reflexivity, symmetry, antisymmetry and transitivity by checking the "
         "definition, and recognise the equivalence relations and partial orders."),
        ("Work with functions precisely",
         "Distinguish injective from surjective, compose functions in the right order, "
         "and say exactly when an inverse exists."),
        ("Compare infinite sets",
         "Show `ℤ` and `ℚ` are countable and `ℝ` is not, using the two arguments "
         "that settle both &mdash; explicit listing and diagonalisation."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 5 are sets, 6 to 9 relations, 10 to 12 functions, and 13 and 14 "
        "the counting consequences that course 4 builds on."
    ),
    "how_to": [
        "Do the set proofs by double inclusion at least once each, even when a chain "
        "of laws is shorter. The habit of proving `A ⊆ B` and `B ⊆ A` separately is "
        "what makes the later structural proofs writable.",
        "Use the relation lab as a counterexample machine. Almost every claim about "
        "relations is refuted by a three-element example, and building one yourself "
        "is faster than recalling which property implies which.",
        "Pay attention to lesson 13. Countability is where intuition about size stops "
        "working, and every argument after it depends on accepting bijection as the "
        "definition of \"same size\".",
    ],
    "not_covered": [
        "Axiomatic set theory. Sets here are naive: collections of objects. The "
        "Zermelo&ndash;Fraenkel axioms, the axiom of choice and the cardinal "
        "arithmetic beyond countable versus uncountable are a separate subject.",
        "Russell's paradox is mentioned where it explains a restriction, but the "
        "resolution &mdash; separating sets from classes &mdash; is not developed.",
        "Ordinals, transfinite induction, and the continuum hypothesis. Lesson 13 "
        "stops at the two cardinalities the rest of the path uses.",
    ],
    "footer_lead": (
        "The set, relation and function labs on this course decide every property by "
        "evaluating its definition over the finite object you built, and name the "
        "element or pair that decides it. A property that holds on the twelve "
        "elements you can see is a property of those twelve elements; the proofs are "
        "what extend it."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
