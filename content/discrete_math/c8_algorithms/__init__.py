"""Course 8 — Algorithms and Complexity."""

from . import part_a, part_b

COURSE = {
    "slug": "algorithms-and-complexity",
    "title": "Algorithms and Complexity",
    "level": "Advanced",
    "summary": (
        "How to say how long an algorithm takes and why it matters: correctness and "
        "termination, growth of functions, big-O with explicit witnesses, analysis of "
        "iterative and recursive algorithms, greedy and dynamic programming, complexity "
        "classes, and the limits of computation."
    ),
    "blurb": (
        "The course the rest of the path was building toward. Recurrences from course 3, "
        "counting from course 4 and graphs from course 7 all reappear as the running "
        "time of something &mdash; and the last two lessons say what no algorithm can do."
    ),
    "key": [
        "f(n) = O(g(n))   ⟺   ∃C, k.  f(n) ≤ C·g(n)  for all n ≥ k",
        "T(n) = aT(n/b) + nᵈ   ⟹   compare log_b a with d",
        "P ⊆ NP;  whether the inclusion is strict is open",
        "some problems have NO algorithm at all",
    ],
    "assumes_short": "Courses 1–7",
    "assumes_long": "especially induction, recurrences and graphs",
    "outcomes_intro": (
        "By the end you can analyse an algorithm you are shown and recognise when a "
        "problem is likely to be intractable."
    ),
    "outcomes": [
        ("Prove a bound with witnesses",
         "Big-O is an existence claim about a constant and a threshold. Producing them "
         "is the proof; quoting the class is not."),
        ("Analyse loops and recursions",
         "Counting the operations of an iterative algorithm, and solving a "
         "divide-and-conquer recurrence with the master theorem."),
        ("Recognise the two design techniques",
         "Greedy where it is provably correct, dynamic programming where it is not "
         "&mdash; and be able to say which and why."),
        ("Place a problem",
         "P, NP, NP-complete, undecidable. Knowing which of those a problem is in "
         "changes what you should attempt."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 2 are what an algorithm is and what correctness means, 3 to 8 are "
        "analysis, 9 to 10 are design, and 11 to 12 are the limits."
    ),
    "how_to": [
        "Produce the witnesses. Every big-O claim in lesson 4 comes with a `C` and a `k`, "
        "and the lab searches for them; a claim without them is a slogan.",
        "Use the measured columns. The lab counts operations by running the algorithms, "
        "so the predicted growth can be compared with something rather than believed.",
        "Take lesson 12 seriously. Undecidability is not a statement about current "
        "technology, and the halting proof is short enough to follow completely.",
    ],
    "not_covered": [
        "Data structures as a subject: heaps, balanced trees, hash tables and their "
        "analyses. They appear where an algorithm needs one and are not developed.",
        "Randomised and approximation algorithms beyond passing mentions, and the "
        "average-case analysis that quicksort needs.",
        "Formal models of computation. Turing machines are described in lesson 12 only "
        "as far as the halting problem requires.",
    ],
    "footer_lead": (
        "Every operation count on this course is produced by executing the algorithm "
        "with a counter, on a deterministic input, so the measured column is a "
        "measurement. Where it diverges from the predicted growth the reason is stated "
        "rather than smoothed over."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
