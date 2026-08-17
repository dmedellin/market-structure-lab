"""Course 1 — Logic and Proof.

Split across two lesson modules because fourteen lessons in one file is a file
nobody reviews. part_a is propositional logic, part_b is quantifiers and proof.
"""

from . import part_a, part_b

COURSE = {
    "slug": "logic-and-proof",
    "title": "Logic and Proof",
    "level": "Beginner",
    "summary": (
        "Propositional and predicate logic from truth values to written proofs: "
        "connectives, truth tables, equivalence, normal forms, quantifiers and their "
        "negations, rules of inference, and the four proof techniques the rest of the "
        "path uses."
    ),
    "blurb": (
        "Make a statement precise enough to be true or false, then establish it. "
        "Connectives and truth tables, logical equivalence, quantifiers and the order "
        "they come in, valid inference, and direct, contrapositive, contradiction and "
        "case proofs written out in full."
    ),
    "key": [
        "p → q   ≡   ¬p ∨ q            the conditional, in disjunctive form",
        "¬(p ∧ q)  ≡  ¬p ∨ ¬q          De Morgan",
        "¬∀x P(x)  ≡  ∃x ¬P(x)         negation flips the quantifier",
        "p → q   ≡   ¬q → ¬p           contraposition: the basis of a proof method",
    ],
    "assumes_short": "Nothing",
    "assumes_long": "school algebra is enough",
    "outcomes_intro": (
        "By the end you can read a theorem statement exactly as written, and write a "
        "proof someone else can check."
    ),
    "outcomes": [
        ("Read a formula unambiguously",
         "Parse a compound statement, apply precedence correctly, and build its truth "
         "table without guessing at what `→` means when its hypothesis is false."),
        ("Prove two statements equivalent",
         "Either by a full truth table, or by a chain of named equivalences &mdash; and "
         "know that one separating assignment refutes the claim outright."),
        ("Handle quantifiers with care",
         "Distinguish `∀x ∃y` from `∃x ∀y`, negate a quantified statement mechanically, "
         "and recognise the vacuous truth that catches everyone once."),
        ("Write the four standard proofs",
         "Direct, contrapositive, contradiction and cases &mdash; knowing which shape of "
         "claim invites which technique, and what each one owes the reader."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 7 are propositional logic, 8 to 10 add quantifiers, and 11 to 14 "
        "turn all of it into proofs."
    ),
    "how_to": [
        "Work forward. Lesson 5 assumes you can build a truth table; lesson 13 assumes "
        "you know what the contrapositive is and why it is equivalent.",
        "Use the labs adversarially. Most of them let you type your own formula or edit "
        "the predicate. The fastest way to understand a claim is to spend two minutes "
        "trying to make it false and finding out you cannot.",
        "Write the proofs out. The last four lessons each end with a claim to prove "
        "yourself. Reading a proof and producing one are different skills, and only the "
        "second transfers to the rest of the path.",
    ],
    "not_covered": [
        "Formal proof systems. This course teaches proof as mathematicians write it "
        "&mdash; rigorous prose &mdash; not natural deduction trees, sequent calculus, or "
        "a machine-checkable proof assistant.",
        "Completeness and soundness of first-order logic, model theory, and G&ouml;del's "
        "incompleteness theorems. Those are the subject of a logic course; this is the "
        "logic a discrete mathematics course needs.",
        "Fuzzy, modal and intuitionistic logics. Everything here is classical and "
        "two-valued: every proposition is either true or false, and `p ∨ ¬p` always holds.",
    ],
    "footer_lead": (
        "Truth tables, equivalences and quantifier evaluations on this course are "
        "computed in your browser by evaluating the formula under every assignment, so "
        "a column is right because the evaluation is right. Verifying a statement on "
        "the cases shown is not a proof of it &mdash; lesson 14 and course 3 are about "
        "exactly that gap."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
