"""Course 5, lessons 01-06 — the model and conditioning."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "sample-spaces-and-events",
        "title": "Sample Spaces and Events",
        "module": "The model",
        "one_line": "The set of outcomes, and the subsets we ask about.",
        "summary": (
            "A probability model is a set of outcomes and an assignment of "
            "probabilities to them. Almost every mistake in this course is a mistake "
            "about what the outcomes are."
        ),
        "key": [
            "S     the SAMPLE SPACE: all possible outcomes",
            "E ⊆ S the EVENT: the outcomes we are asking about",
            "Outcomes must be MUTUALLY EXCLUSIVE and EXHAUSTIVE.",
            "\"Equally likely\" is an assumption about S, not a fact.",
        ],
        "key_label": "Two objects, one assumption",
        "concepts_intro": (
            "Getting the sample space right is most of the work. The arithmetic that "
            "follows is course 4."
        ),
        "concepts": [
            ("An outcome is a complete result",
             "For two dice the outcomes are ordered pairs, not sums. Choosing the wrong "
             "granularity is the first and most damaging error."),
            ("An event is a subset",
             "\"The sum is 7\" is the set of six pairs that sum to 7. Set operations from "
             "course 2 apply unchanged: `∪` is \"or\", `∩` is \"and\", complement is \"not\"."),
            ("Equally likely is a modelling choice",
             "It is justified by symmetry of the physical situation, and it must be "
             "checked. Sums of two dice are not equally likely; pairs are."),
        ],
        "read_title": "Setting up a model",
        "read_intro": "Outcomes, events, and the choice of granularity.",
        "body": [
            ("def", ("Sample space, outcome, event",
                     "The <strong>sample space</strong> `S` is the set of all possible "
                     "outcomes of an experiment. An <strong>outcome</strong> is one "
                     "element of `S`; an <strong>event</strong> is a subset of `S`.")),
            ("p", "The outcomes must be <strong>mutually exclusive</strong> (exactly one "
                  "happens) and <strong>exhaustive</strong> (at least one happens). Those "
                  "are the same conditions a proof by cases needs, and they fail in the "
                  "same ways."),
            ("example", ("Two dice, two models",
                         "Model A: `S` is the 36 ordered pairs `(1,1)` through `(6,6)`, all "
                         "equally likely. Model B: `S` is the 11 sums `2, …, 12`. Both are "
                         "legitimate sample spaces; only in model A are the outcomes "
                         "equally likely. A sum of 7 arises six ways and a sum of 2 arises "
                         "one way.")),
            ("p", "That is the granularity trap, and it produced a famous error: Cardano "
                  "and later gamblers computed dice probabilities from the sums and got "
                  "them wrong. The fix is to keep outcomes fine enough that symmetry "
                  "justifies equal likelihood."),
            ("h3", "Events as sets"),
            ("math", [
                "in words                 as a set",
                "A or B                   A ∪ B",
                "A and B                  A ∩ B",
                "not A                    Ā  =  S \\ A",
                "A but not B              A \\ B",
                "exactly one of A, B      A △ B",
                "A and B cannot both      A ∩ B = ∅     (mutually exclusive)",
            ]),
            ("p", "Every identity from course 2 lesson 4 therefore applies, and De Morgan "
                  "is used constantly: \"not (A or B)\" is \"neither A nor B\", which is "
                  "usually the easier event to count."),
            ("def", ("Probability of an event (equally likely case)",
                     "When the outcomes of a finite `S` are equally likely, "
                     "`P(E) = |E| / |S|`. Every probability in this course's early lessons "
                     "is this ratio, computed with course 4's tools.")),
            ("example", ("Choosing a granularity",
                         "Flip three coins and ask for the probability of exactly two "
                         "heads. Outcomes as ordered triples: 8 equally likely, of which "
                         "`HHT`, `HTH`, `THH` qualify, so `3/8`. Outcomes as \"number of "
                         "heads\": four possibilities, but not equally likely &mdash; and "
                         "answering `1/4` is the error the fine model prevents.")),
        ],
        "lab": ("probability", {
            "experiment": "coins4",
            "panel_title": "Every outcome, listed",
            "panel_intro": "The sample space is drawn in full and each event highlights "
                           "its members. Every probability below is a count of highlighted "
                           "chips divided by the total.",
        }),
        "steps_title": "Building a probability model",
        "steps_intro": "Outcomes first, and choose them fine enough.",
        "steps": [
            ("List the outcomes",
             "As tuples if several things happen. Fine enough that symmetry makes them "
             "equally likely."),
            ("Check exclusivity and exhaustiveness",
             "Exactly one outcome occurs. If two could occur together, the outcomes are "
             "not outcomes."),
            ("Write the event as a subset",
             "\"At least one 6\" is a specific set of pairs. Writing it out is what makes "
             "the count possible."),
            ("Count and divide",
             "Course 4 supplies the counting. The division is the only new step in this "
             "lesson."),
        ],
        "worked": {
            "title": "Two dice, three events",
            "intro": ["`S` is the 36 ordered pairs, all equally likely."],
            "lines": [
                "A = \"sum is 7\"      {(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)}   |A| = 6",
                "B = \"a double\"      {(1,1),(2,2),(3,3),(4,4),(5,5),(6,6)}   |B| = 6",
                "C = \"first die 4\"   {(4,1),(4,2),(4,3),(4,4),(4,5),(4,6)}   |C| = 6",
                "",
                "P(A) = P(B) = P(C) = 6/36 = 1/6",
                "",
                "A ∩ B = ∅          a double sums to an even number, never 7",
                "A ∩ C = {(4,3)}    P = 1/36",
                "B ∩ C = {(4,4)}    P = 1/36",
                "",
                "P(A ∪ C) = 6/36 + 6/36 − 1/36 = 11/36",
            ],
            "after": [
                "`A` and `B` are mutually exclusive and `A` and `C` are not, even though "
                "all three have the same probability. Exclusivity is a fact about the sets, "
                "not about their sizes &mdash; and lesson 5 shows that independence is a "
                "third, different property again."
            ],
        },
        "quiz_title": "Sample spaces",
        "quiz": [
            {"q": "For two dice, the correct equally-likely sample space is:",
             "a": ["the 11 possible sums",
                   "the 36 ordered pairs",
                   "the 21 unordered pairs",
                   "the 12 faces"],
             "c": 1,
             "why": "Only the ordered pairs are equally likely. Sums are not: 7 arises six "
                    "ways and 2 arises one."},
            {"q": "An event is:",
             "a": ["a single outcome", "a subset of the sample space",
                   "a probability", "a random variable"],
             "c": 1,
             "why": "Any subset, including `∅` (probability 0) and `S` (probability 1). A "
                    "single outcome is a one-element event."},
            {"q": "Outcomes must be mutually exclusive, meaning:",
             "a": ["they are equally likely",
                   "exactly one of them occurs",
                   "there are finitely many",
                   "they are independent"],
             "c": 1,
             "why": "Exclusive and exhaustive together mean exactly one occurs, which is "
                    "what makes the probabilities sum to 1."},
        ],
        "mistakes": [
            ("Choosing outcomes too coarse",
             "Sums of dice, numbers of heads and unordered pairs are all legitimate "
             "descriptions and none of them is equally likely. Keep the outcomes fine."),
            ("Assuming equal likelihood without a symmetry",
             "A loaded die has the same sample space and different probabilities. The "
             "assumption belongs to the model and should be stated."),
            ("Treating mutually exclusive as independent",
             "They are nearly opposite. Two exclusive events with positive probability are "
             "strongly dependent: knowing one occurred tells you the other did not."),
        ],
        "standard": ("Finish when you write the sample space before computing.",
                     "For \"draw two cards from a standard deck\", write down what an "
                     "outcome is, how many there are, and whether they are equally likely "
                     "&mdash; before touching any event."),
        "note": "For countably infinite sample spaces &mdash; \"flip until the first "
                "head\" &mdash; the equally-likely model is unavailable and probabilities "
                "are assigned directly. Lesson 12 does exactly that for the geometric "
                "distribution.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "computing-probabilities",
        "title": "Computing Probabilities",
        "module": "The model",
        "one_line": "Counting the event, counting the space, dividing.",
        "summary": (
            "With equally likely outcomes, every probability is a ratio of two counts, "
            "so course 4 is the whole technique. Complementary counting is as useful "
            "here as it was there."
        ),
        "key": [
            "P(E) = |E| / |S|",
            "P(Ē) = 1 − P(E)                 complement",
            "\"at least one\"  ⟹  1 − P(none)",
            "The hard part is the counting, not the division.",
        ],
        "key_label": "Two counts and a division",
        "concepts_intro": (
            "Nothing new is needed beyond course 4. What is new is that the answer must "
            "lie between 0 and 1, which is a free check."
        ),
        "concepts": [
            ("Count with the same tools",
             "Permutations, combinations, complements and inclusion&ndash;exclusion. The "
             "denominator is a count too and is often the easier one."),
            ("The complement rule saves work",
             "`P(at least one) = 1 − P(none)`, exactly as in course 4 lesson 2 and for "
             "the same reason."),
            ("The answer is bounded",
             "Any probability outside `[0, 1]` is a counting error, and that check costs "
             "nothing."),
        ],
        "read_title": "Probability as a ratio",
        "read_intro": "The rule, the complement, and three classic calculations.",
        "body": [
            ("thm", ("Equally likely outcomes",
                     "If `S` is finite and its outcomes are equally likely, then for any "
                     "event `E`, `P(E) = |E|/|S|`.")),
            ("thm", ("Complement rule",
                     "`P(Ē) = 1 − P(E)`, because `|Ē| = |S| − |E|`.")),
            ("example", ("Poker: a flush",
                         "Five cards from 52: `C(52,5) = 2 598 960` hands. A flush is five "
                         "cards of one suit: choose the suit (4 ways) and five of its "
                         "thirteen cards (`C(13,5) = 1287`), giving `5148`. So "
                         "`P = 5148/2598960 ≈ 0.00198`. (This includes straight flushes; "
                         "excluding them subtracts 40.)")),
            ("example", ("At least one six",
                         "Roll four dice. `P(at least one 6) = 1 − P(no 6) = 1 − (5/6)⁴ "
                         "= 1 − 625/1296 = 671/1296 ≈ 0.518`. Counting the ways to get at "
                         "least one six directly requires inclusion and exclusion over the "
                         "four dice; the complement is one line.")),
            ("h3", "The birthday problem"),
            ("thm", ("Shared birthdays",
                     "With `n` people and 365 equally likely birthdays, "
                     "`P(some pair shares) = 1 − (365 · 364 ⋯ (365−n+1)) / 365ⁿ`.")),
            ("math", [
                "n     P(a shared birthday)",
                "10           0.117",
                "20           0.411",
                "23           0.507        ← passes one half",
                "30           0.706",
                "50           0.970",
                "70           0.999",
            ]),
            ("p", "Twenty-three people suffice for a better-than-even chance, which "
                  "surprises nearly everyone. The reason is that the question is about "
                  "<em>pairs</em>: 23 people form `C(23,2) = 253` pairs, and each has about "
                  "a `1/365` chance of matching. The intuition that fails is comparing 23 "
                  "with 365 rather than 253 with 365."),
            ("p", "This is a different question from the pigeonhole statement in course 2. "
                  "That one said 367 people <em>guarantee</em> a match; this one says 23 "
                  "make it likely. Certainty and probability are different claims and "
                  "neither implies the other."),
            ("h3", "When outcomes are not equally likely"),
            ("p", "Then probabilities are assigned to outcomes directly, subject to being "
                  "non-negative and summing to 1, and `P(E) = Σ_{s ∈ E} P(s)`. A loaded "
                  "die, a biased coin and a weighted lottery all work this way, and lesson "
                  "3 states the axioms that govern them."),
        ],
        "lab": ("probability", {
            "experiment": "cards",
            "panel_title": "Count, count, divide",
            "panel_intro": "The table shows each probability as a count over a count "
                           "before showing it as a fraction and a percentage. The counts "
                           "are what you would compute by hand.",
        }),
        "steps_title": "Computing a probability",
        "steps_intro": "Denominator first; it is often easier and it anchors the model.",
        "steps": [
            ("Count the sample space",
             "This confirms what an outcome is. If `|S|` is hard to write down, the model "
             "is probably wrong."),
            ("Count the event",
             "Using course 4. Classify by order and repetition exactly as there."),
            ("Consider the complement",
             "\"At least one\" and \"not all\" almost always count more easily the other "
             "way round."),
            ("Check the answer lies in `[0,1]`",
             "And that it is plausible. A probability of 0.99 for a rare event is a "
             "counting error announcing itself."),
        ],
        "worked": {
            "title": "Two aces",
            "intro": ["Five cards from a standard deck. Probability of exactly two aces."],
            "lines": [
                "Sample space:  C(52,5) = 2 598 960 hands",
                "",
                "Event: exactly two aces",
                "   choose 2 of the 4 aces:        C(4,2)  =    6",
                "   choose 3 of the 48 non-aces:   C(48,3) = 17 296",
                "   product:                        103 776",
                "",
                "P = 103 776 / 2 598 960 ≈ 0.0399",
                "",
                "CHECK by summing over the number of aces:",
                "   C(4,0)C(48,5) + C(4,1)C(48,4) + C(4,2)C(48,3)",
                " + C(4,3)C(48,2) + C(4,4)C(48,1)",
                " = 1712304 + 778320 + 103776 + 4512 + 48  =  2 598 960     ✓",
            ],
            "after": [
                "The check is Vandermonde's identity from course 4 lesson 5, appearing as "
                "a probability check: the five disjoint cases must exhaust the hands. It "
                "would catch a wrong `C(48,3)` immediately."
            ],
        },
        "quiz_title": "Computing probabilities",
        "quiz": [
            {"q": "Roll two dice. `P(sum is 7)` equals:",
             "a": ["1/11", "1/6", "1/12", "7/36"],
             "c": 1,
             "why": "Six of the 36 ordered pairs sum to 7, so `6/36 = 1/6`. Answering "
                    "`1/11` uses the sums as the sample space, which are not equally likely."},
            {"q": "`P(at least one head)` in four coin flips:",
             "a": ["1/2", "15/16", "1/16", "4/16"],
             "c": 1,
             "why": "`1 − P(no heads) = 1 − 1/16 = 15/16`. The complement is one "
                    "calculation; the direct count needs four cases."},
            {"q": "The birthday problem's answer surprises people because:",
             "a": ["365 is large",
                   "the question is about pairs, and 23 people form 253 pairs",
                   "birthdays are not equally likely",
                   "the calculation is wrong"],
             "c": 1,
             "why": "The relevant comparison is 253 pairs against 365 days, not 23 people "
                    "against 365 days."},
        ],
        "mistakes": [
            ("Counting the event with a different model from the space",
             "If the denominator counts ordered outcomes, the numerator must too. Mixing "
             "ordered and unordered counts is the commonest arithmetic-looking error."),
            ("Counting \"at least one\" directly",
             "It produces overlapping cases. `1 − P(none)` cannot double-count."),
            ("Confusing certainty with high probability",
             "367 people guarantee a shared birthday; 23 make it likely. Course 2's "
             "pigeonhole and this lesson answer different questions."),
        ],
        "standard": ("Finish when you check your answer against a complementary count.",
                     "Compute the probability that a five-card hand contains at least one "
                     "ace, both directly (four cases) and by complement. The complement is "
                     "one line and the agreement is the check."),
        "note": "The birthday calculation assumes birthdays are uniform and independent, "
                "and neither is exactly true. Real birth data makes coincidences slightly "
                "MORE likely, so 23 remains a safe answer &mdash; but the assumptions "
                "should be stated rather than assumed away.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "probability-axioms",
        "title": "The Probability Axioms",
        "module": "The model",
        "one_line": "Three rules that every probability assignment obeys.",
        "summary": (
            "Non-negativity, total mass 1, and additivity over disjoint events. "
            "Everything else &mdash; the complement rule, monotonicity, the union bound "
            "&mdash; is derived from these three."
        ),
        "key": [
            "A1   P(E) ≥ 0",
            "A2   P(S) = 1",
            "A3   P(A ∪ B) = P(A) + P(B)   when A ∩ B = ∅",
            "everything else is a THEOREM",
        ],
        "key_label": "Three axioms",
        "concepts_intro": (
            "The axioms are what make probability a mathematical subject rather than a "
            "collection of intuitions."
        ),
        "concepts": [
            ("The axioms are few",
             "Non-negative, total 1, additive over disjoint events. The equally-likely "
             "model satisfies them, and so do many others."),
            ("The familiar rules are consequences",
             "`P(Ē) = 1 − P(E)` and `P(A ∪ B) = P(A) + P(B) − P(A ∩ B)` are proved, not "
             "assumed."),
            ("Additivity needs disjointness",
             "For overlapping events the general rule is inclusion and exclusion, which is "
             "course 4 lesson 9 with probabilities in place of counts."),
        ],
        "read_title": "The axioms and what follows",
        "read_intro": "The three rules, then six theorems derived from them.",
        "body": [
            ("def", ("Probability space",
                     "A finite <strong>probability space</strong> is a sample space `S` "
                     "with a function `P` on its subsets satisfying: "
                     "(A1) `P(E) ≥ 0` for every event `E`; "
                     "(A2) `P(S) = 1`; "
                     "(A3) `P(A ∪ B) = P(A) + P(B)` whenever `A ∩ B = ∅`.")),
            ("p", "Nothing here says what probability means. The axioms constrain how "
                  "probabilities combine, and the equally-likely model of lesson 2 is one "
                  "assignment satisfying them &mdash; not the only one."),
            ("thm", ("Consequences of the axioms",
                     "`P(∅) = 0`; `P(Ē) = 1 − P(E)`; `P(E) ≤ 1`; if `A ⊆ B` then "
                     "`P(A) ≤ P(B)`; `P(A ∪ B) = P(A) + P(B) − P(A ∩ B)`; and "
                     "`P(A ∪ B) ≤ P(A) + P(B)`.")),
            ("proof", [
                "`P(∅) = 0`: `S` and `∅` are disjoint with union `S`, so "
                "`P(S) = P(S) + P(∅)` by A3, giving `P(∅) = 0`.",
                "`P(Ē) = 1 − P(E)`: `E` and `Ē` are disjoint with union `S`, so A3 and A2 "
                "give `P(E) + P(Ē) = 1`.",
                "`P(E) ≤ 1`: from the previous line and A1 applied to `Ē`.",
                "<strong>Monotonicity.</strong> If `A ⊆ B` then `B = A ∪ (B \\ A)` with the "
                "two disjoint, so `P(B) = P(A) + P(B \\ A) ≥ P(A)` by A1.",
                "<strong>Inclusion&ndash;exclusion.</strong> `A ∪ B` splits into the three "
                "disjoint pieces `A \\ B`, `A ∩ B`, `B \\ A`. Adding `P(A)` and `P(B)` "
                "counts `A ∩ B` twice, so subtracting it once gives the union.",
                "<strong>Union bound.</strong> Immediate from the previous line and A1.",
            ]),
            ("p", "The union bound `P(A ∪ B) ≤ P(A) + P(B)` looks weak and is used "
                  "constantly: it bounds the probability that anything goes wrong by the "
                  "sum of the individual failure probabilities, with no independence "
                  "assumption at all."),
            ("h3", "Assigning probabilities directly"),
            ("p", "For a finite `S`, any assignment of non-negative numbers to the "
                  "outcomes summing to 1 defines a probability space, with "
                  "`P(E) = Σ_{s ∈ E} P(s)`. The equally-likely case gives each outcome "
                  "`1/|S|`; a biased coin gives `P(H) = p` and `P(T) = 1 − p`."),
            ("example", ("A loaded die",
                         "Suppose `P(6) = 1/3` and the other five faces share the rest "
                         "equally, so each has `2/15`. Check: `1/3 + 5 · 2/15 = 1/3 + 2/3 = "
                         "1`. Then `P(even) = 2/15 + 2/15 + 1/3 = 3/5`, which the "
                         "equally-likely model would have put at `1/2`.")),
            ("p", "Notice that the axioms did all the work and the equally-likely "
                  "assumption did none. Everything in lessons 4 to 12 is proved from the "
                  "axioms and therefore holds for loaded dice too."),
        ],
        "lab": ("probability", {
            "experiment": "urn",
            "panel_title": "The axioms, in a finite space",
            "panel_intro": "Every quantity in the table obeys the axioms because it is a "
                           "ratio of counts. Check monotonicity yourself: an event "
                           "contained in another never has a larger probability.",
        }),
        "steps_title": "Working from the axioms",
        "steps_intro": "Use disjointness where you have it, inclusion and exclusion where you do not.",
        "steps": [
            ("Check the events are disjoint before adding",
             "A3 requires it. Adding overlapping probabilities over-counts exactly the "
             "intersection."),
            ("Use the complement when the event is large",
             "`P(E) = 1 − P(Ē)` is often the shorter calculation, and it is a theorem "
             "rather than a trick."),
            ("Decompose into disjoint pieces",
             "Any union splits into disjoint parts, and A3 then applies cleanly to the "
             "parts."),
            ("Bound when you cannot compute",
             "The union bound needs no independence and is often enough &mdash; \"the "
             "chance anything fails is at most the sum of the individual chances\"."),
        ],
        "worked": {
            "title": "Deriving inclusion and exclusion",
            "intro": ["From the axioms, with no counting."],
            "lines": [
                "Split A ∪ B into three DISJOINT pieces:",
                "",
                "   A ∪ B  =  (A \\ B)  ∪  (A ∩ B)  ∪  (B \\ A)",
                "",
                "By A3 applied twice:",
                "   P(A ∪ B) = P(A\\B) + P(A∩B) + P(B\\A)",
                "",
                "Also  A = (A\\B) ∪ (A∩B), disjoint, so  P(A\\B) = P(A) − P(A∩B),",
                "and likewise                            P(B\\A) = P(B) − P(A∩B).",
                "",
                "Substituting:",
                "   P(A ∪ B) = [P(A) − P(A∩B)] + P(A∩B) + [P(B) − P(A∩B)]",
                "            = P(A) + P(B) − P(A∩B)                       ∎",
            ],
            "after": [
                "No counting appeared. The rule holds for any probability assignment "
                "satisfying the axioms, including loaded dice and continuous "
                "distributions, which is exactly why the axiomatic route is worth taking."
            ],
        },
        "quiz_title": "Axioms",
        "quiz": [
            {"q": "`P(A ∪ B) = P(A) + P(B)` requires:",
             "a": ["`A` and `B` independent",
                   "`A` and `B` disjoint",
                   "nothing",
                   "`P(A) + P(B) ≤ 1`"],
             "c": 1,
             "why": "Axiom A3 is additivity over DISJOINT events. Independence is a "
                    "different and unrelated condition, introduced in lesson 5."},
            {"q": "`A ⊆ B`. What follows about their probabilities?",
             "a": ["`P(A) = P(B)`", "`P(A) ≤ P(B)`", "`P(A) ≥ P(B)`", "nothing"],
             "c": 1,
             "why": "Monotonicity, proved by splitting `B` into `A` and `B \\ A` and "
                    "applying non-negativity."},
            {"q": "The union bound says:",
             "a": ["`P(A ∪ B) = P(A) + P(B)`",
                   "`P(A ∪ B) ≤ P(A) + P(B)`",
                   "`P(A ∩ B) ≤ P(A)P(B)`",
                   "`P(A) ≤ 1`"],
             "c": 1,
             "why": "It follows from inclusion&ndash;exclusion and non-negativity, and it "
                    "needs no independence &mdash; which is what makes it so widely usable."},
        ],
        "mistakes": [
            ("Adding probabilities of overlapping events",
             "A3 needs disjointness. Without it the sum exceeds the true probability by "
             "`P(A ∩ B)`, and may exceed 1."),
            ("Confusing disjoint with independent",
             "Disjoint events with positive probability are maximally dependent: one "
             "occurring rules the other out."),
            ("Assuming the equally-likely model when computing",
             "The axioms are general. A loaded die satisfies them and `|E|/|S|` is simply "
             "the wrong formula for it."),
        ],
        "standard": ("Finish when you can derive a rule rather than recall it.",
                     "Derive `P(A ∪ B ∪ C)` from the axioms by splitting into disjoint "
                     "pieces. It is the three-set inclusion&ndash;exclusion formula, and "
                     "deriving it is more useful than memorising the signs."),
        "note": "Kolmogorov's axioms add countable additivity, which matters for infinite "
                "sample spaces and is what makes the geometric distribution of lesson 12 "
                "legitimate. For finite spaces the three rules here are the whole story.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "conditional-probability",
        "title": "Conditional Probability",
        "module": "Conditioning",
        "one_line": "Restricting the sample space to what you now know.",
        "summary": (
            "`P(A | B) = P(A ∩ B)/P(B)` is not a new axiom: it is the original counting "
            "restricted to the outcomes where `B` holds. The traps are all about which "
            "of `P(A|B)` and `P(B|A)` you have computed."
        ),
        "key": [
            "P(A | B) = P(A ∩ B) / P(B)        requires P(B) > 0",
            "P(A ∩ B) = P(A | B) · P(B)        the multiplication rule",
            "P(A | B) ≠ P(B | A)               in general",
            "conditioning SHRINKS the sample space to B",
        ],
        "key_label": "A smaller sample space",
        "concepts_intro": (
            "Conditioning is re-counting inside a subset. Everything difficult about it "
            "is about interpretation, not arithmetic."
        ),
        "concepts": [
            ("Conditioning restricts the space",
             "`P(A|B)` counts the outcomes in `A` among those in `B`. The denominator is "
             "`|B|`, not `|S|`."),
            ("The two conditionals are different numbers",
             "`P(test positive | disease)` and `P(disease | test positive)` differ by the "
             "base rate, often by orders of magnitude."),
            ("The multiplication rule chains",
             "`P(A ∩ B ∩ C) = P(A)P(B|A)P(C|A∩B)` &mdash; useful for sequential draws, "
             "where each step conditions on the previous ones."),
        ],
        "read_title": "Conditioning",
        "read_intro": "The definition, why it is a definition rather than a theorem, and the standard traps.",
        "body": [
            ("def", ("Conditional probability",
                     "For events `A`, `B` with `P(B) &gt; 0`, "
                     "`P(A | B) = P(A ∩ B) / P(B)`.")),
            ("p", "In the equally-likely model this is transparent: "
                  "`P(A|B) = (|A ∩ B|/|S|)/(|B|/|S|) = |A ∩ B|/|B|`. The outcomes outside "
                  "`B` have been discarded, and `B` is now the sample space."),
            ("thm", ("Conditional probability is a probability",
                     "For fixed `B` with `P(B) &gt; 0`, the function `A ↦ P(A|B)` satisfies "
                     "all three axioms. So every theorem about probability holds for "
                     "conditional probability too.")),
            ("thm", ("Multiplication rule",
                     "`P(A ∩ B) = P(A|B)P(B) = P(B|A)P(A)`, and more generally "
                     "`P(A₁ ∩ ⋯ ∩ A_n) = P(A₁)P(A₂|A₁)P(A₃|A₁∩A₂)⋯`.")),
            ("example", ("Sequential draws",
                         "Two cards from a deck without replacement. "
                         "`P(both aces) = P(first ace) · P(second ace | first ace) = "
                         "(4/52)(3/51) = 1/221`. Conditioning is exactly what handles "
                         "\"without replacement\": the second probability changes because "
                         "the first draw changed the deck.")),
            ("h3", "The two conditionals are different"),
            ("example", ("Dice",
                         "Roll two dice. `P(sum is 7 | first die is 4) = 1/6`, since among "
                         "the six outcomes with a 4 first, exactly one has sum 7. But "
                         "`P(first die is 4 | sum is 7) = 1/6` too &mdash; a coincidence "
                         "arising from symmetry, not a rule.")),
            ("example", ("Where they differ wildly",
                         "`P(is a mammal | is a dog) = 1`, while "
                         "`P(is a dog | is a mammal)` is small. The two conditionals share "
                         "a numerator `P(A ∩ B)` and have different denominators, and the "
                         "ratio of the denominators is exactly how much they differ.")),
            ("h3", "The Monty Hall problem"),
            ("p", "Three doors, a prize behind one. You pick door 1. The host, who knows "
                  "where the prize is, opens a different door with no prize behind it "
                  "&mdash; say door 3 &mdash; and offers you a switch. Should you?"),
            ("math", [
                "prize behind  your choice  host must open   switching wins?",
                "   door 1        door 1     door 2 or 3          NO",
                "   door 2        door 1     door 3              YES",
                "   door 3        door 1     door 2              YES",
                "",
                "Each row has probability 1/3, so switching wins with probability 2/3.",
            ]),
            ("p", "The step people miss is that the host's action is not random: he "
                  "<em>knows</em> and is constrained to open a losing door. That constraint "
                  "is information, and conditioning on it is what makes switching better. "
                  "If the host opened a door at random and it happened to be empty, the "
                  "answer would be `1/2` &mdash; a different problem with the same picture."),
        ],
        "lab": ("probability", {
            "experiment": "dice2",
            "panel_title": "Conditioning, visibly",
            "panel_intro": "Event B is the condition. The table shows `P(A|B)` as the count "
                           "of outcomes in both divided by the count in B &mdash; the "
                           "restricted sample space, not the original one.",
        }),
        "steps_title": "Conditioning correctly",
        "steps_intro": "Say which event is the condition, out loud.",
        "steps": [
            ("Identify the conditioning event",
             "`P(A|B)` conditions on `B`. Writing the sentence \"given that `B` happened\" "
             "prevents the swap."),
            ("Restrict the sample space",
             "In the equally-likely model, count within `B`. The denominator changes and "
             "the numerator becomes `|A ∩ B|`."),
            ("Use the multiplication rule for sequences",
             "Each draw conditions on the previous ones. Without replacement, the "
             "denominators shrink."),
            ("Ask whether you wanted the other conditional",
             "The two are related by Bayes, which is lesson 6. Computing the wrong one is "
             "the most consequential error in this course."),
        ],
        "worked": {
            "title": "The two-child problem",
            "intro": ["A family has two children. The sample space is `{BB, BG, GB, GG}`, "
                      "equally likely."],
            "lines": [
                "\"At least one is a boy.\"  What is P(both boys)?",
                "",
                "   B = {BB, BG, GB}          |B| = 3",
                "   A ∩ B = {BB}              |A ∩ B| = 1",
                "   P(A | B) = 1/3",
                "",
                "\"The ELDER is a boy.\"  What is P(both boys)?",
                "",
                "   B' = {BB, BG}             |B'| = 2",
                "   A ∩ B' = {BB}             |A ∩ B'| = 1",
                "   P(A | B') = 1/2",
                "",
                "Same family, two different pieces of information, two answers.",
            ],
            "after": [
                "The difference is real and not a trick: \"at least one is a boy\" and "
                "\"the elder is a boy\" restrict the sample space to sets of different "
                "sizes. Almost every disputed probability puzzle turns out to be an "
                "ambiguity about which restriction was intended."
            ],
        },
        "quiz_title": "Conditioning",
        "quiz": [
            {"q": "`P(A|B)` is defined as:",
             "a": ["`P(A)P(B)`", "`P(A ∩ B)/P(B)`", "`P(A ∩ B)/P(A)`", "`P(A ∪ B)/P(B)`"],
             "c": 1,
             "why": "The outcomes in both, out of the outcomes in `B`. It requires "
                    "`P(B) &gt; 0`."},
            {"q": "Two cards drawn without replacement. `P(second is an ace | first is an ace)`:",
             "a": ["4/52", "3/51", "4/51", "1/13"],
             "c": 1,
             "why": "After removing one ace, 3 aces remain among 51 cards. Conditioning is "
                    "what \"without replacement\" means."},
            {"q": "In Monty Hall, switching wins with probability 2/3 because:",
             "a": ["there are three doors",
                   "the host's choice is constrained by knowledge, which is information",
                   "the doors are equally likely",
                   "the prize moves"],
             "c": 1,
             "why": "The host must open a losing door, so his action carries information. "
                    "A random host who happened to reveal an empty door gives 1/2."},
        ],
        "mistakes": [
            ("Swapping the two conditionals",
             "`P(A|B)` and `P(B|A)` are different numbers with the same numerator. Lesson "
             "6 gives the exact relationship."),
            ("Forgetting the denominator changed",
             "Conditioning restricts the sample space. Dividing by `|S|` instead of `|B|` "
             "gives `P(A ∩ B)`, not `P(A|B)`."),
            ("Ignoring how the information arrived",
             "Monty Hall and the two-child problem both hinge on it. \"At least one boy\" "
             "and \"the elder is a boy\" are different conditions."),
        ],
        "standard": ("Finish when you can state the restricted sample space.",
                     "For each conditional probability you compute, write down explicitly "
                     "which outcomes remain. That sentence catches the swap, the wrong "
                     "denominator and the ambiguity all at once."),
        "note": "Conditional probability is where probability stops being counting and "
                "starts being modelling. The arithmetic never gets harder than division; "
                "deciding what to condition on is where the difficulty lives.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "independence",
        "title": "Independence",
        "module": "Conditioning",
        "one_line": "`P(A ∩ B) = P(A)P(B)`, and nothing more.",
        "summary": (
            "Independence is an equation, not a story about causation. Two events are "
            "independent when conditioning on one does not change the other &mdash; and "
            "checking that means checking the equation."
        ),
        "key": [
            "A, B independent   ⟺   P(A ∩ B) = P(A)·P(B)",
            "equivalently  P(A | B) = P(A)      when P(B) > 0",
            "DISJOINT is nearly the opposite of independent",
            "pairwise independent ⇏ mutually independent",
        ],
        "key_label": "One equation",
        "concepts_intro": (
            "Independence is defined by an equation so that it can be checked. Intuition "
            "about it is unreliable."
        ),
        "concepts": [
            ("It is a property of the probabilities",
             "Not of causation, not of physical separation. Two events in the same "
             "experiment can be independent and two in different rooms need not be."),
            ("Disjoint is almost the opposite",
             "If `A` and `B` are disjoint with positive probability, then "
             "`P(A|B) = 0 ≠ P(A)`: knowing `B` occurred tells you `A` did not."),
            ("Pairwise is weaker than mutual",
             "Three events can be independent in every pair and still fail the "
             "three-way condition, which is why mutual independence requires every "
             "subset."),
        ],
        "read_title": "Independence",
        "read_intro": "The definition, the equivalent form, and the two standard confusions.",
        "body": [
            ("def", ("Independent events",
                     "`A` and `B` are <strong>independent</strong> when "
                     "`P(A ∩ B) = P(A)P(B)`. Equivalently, when `P(B) &gt; 0`, "
                     "`P(A|B) = P(A)`: conditioning on `B` changes nothing.")),
            ("p", "The second form is the meaning and the first is the test. The first is "
                  "preferred as the definition because it is symmetric and does not require "
                  "`P(B) &gt; 0`."),
            ("example", ("Independent within one experiment",
                         "Roll two dice. `A` = \"first die is even\", `B` = \"second die is "
                         "5\". `P(A) = 1/2`, `P(B) = 1/6`, `P(A ∩ B) = 3/36 = 1/12 = "
                         "(1/2)(1/6)`. Independent, and unsurprisingly so.")),
            ("example", ("Independent, surprisingly",
                         "Same two dice. `A` = \"first die is even\", `B` = \"the sum is "
                         "7\". `P(A) = 1/2`, `P(B) = 1/6`, and `A ∩ B` is "
                         "`{(2,5),(4,3),(6,1)}` with probability `3/36 = 1/12`. Independent "
                         "&mdash; even though the sum obviously depends on the first die.")),
            ("p", "That second example is why the definition is an equation. Nothing in "
                  "the physical description suggests independence; the numbers satisfy the "
                  "equation, and that is what independence means."),
            ("thm", ("Complements preserve independence",
                     "If `A` and `B` are independent, so are `A` and `B̄`, `Ā` and `B`, and "
                     "`Ā` and `B̄`.")),
            ("proof", [
                "`P(A ∩ B̄) = P(A) − P(A ∩ B) = P(A) − P(A)P(B) = P(A)(1 − P(B)) = "
                "P(A)P(B̄)`. The other cases follow by symmetry and by applying this twice.",
            ]),
            ("h3", "Disjoint is not independent"),
            ("p", "If `A ∩ B = ∅` and both have positive probability, then "
                  "`P(A ∩ B) = 0` while `P(A)P(B) &gt; 0`, so they are dependent. "
                  "Intuitively: knowing `B` occurred tells you `A` did not, which is a "
                  "large change in your information. The only way to be both disjoint and "
                  "independent is for one of them to have probability 0."),
            ("h3", "Mutual independence"),
            ("def", ("Mutually independent",
                     "Events `A₁, …, A_n` are <strong>mutually independent</strong> when "
                     "for every subset of them the probability of the intersection is the "
                     "product of the probabilities. Pairwise independence is only the "
                     "two-element case.")),
            ("example", ("Pairwise but not mutually",
                         "Flip two fair coins. `A` = \"first is heads\", `B` = \"second is "
                         "heads\", `C` = \"the two agree\". Each has probability `1/2`, and "
                         "each pair is independent: `P(A ∩ C) = P(HH) = 1/4 = (1/2)(1/2)`. "
                         "But `P(A ∩ B ∩ C) = P(HH) = 1/4`, while "
                         "`P(A)P(B)P(C) = 1/8`. Any two of these events determine the "
                         "third, so they cannot be mutually independent.")),
            ("p", "The example is worth keeping. Checking pairs and declaring mutual "
                  "independence is a real and common error, and the failure here is total: "
                  "any two of the three events determine the third completely."),
        ],
        "lab": ("probability", {
            "experiment": "dice2",
            "panel_title": "Test the equation",
            "panel_intro": "The table prints `P(A∩B)` and `P(A)·P(B)` on adjacent rows. "
                           "Independence is those two being equal, which the status line "
                           "reports &mdash; and some independent pairs are genuinely "
                           "surprising.",
        }),
        "steps_title": "Checking independence",
        "steps_intro": "Compute three numbers and compare two of them.",
        "steps": [
            ("Compute `P(A)`, `P(B)` and `P(A ∩ B)`",
             "All three, exactly. Estimating any of them defeats the check."),
            ("Compare `P(A ∩ B)` with `P(A)P(B)`",
             "Equal means independent. This is the definition and there is no other test."),
            ("Do not reason from the story",
             "Physical separation does not imply independence and shared causes do not "
             "preclude it. The example with the sum of two dice settles that."),
            ("For several events, check every subset",
             "Pairwise independence does not give mutual independence. All `2ⁿ − n − 1` "
             "conditions are required."),
        ],
        "worked": {
            "title": "Three events, checked properly",
            "intro": ["Two fair coins. `A` = first heads, `B` = second heads, `C` = the two agree."],
            "lines": [
                "S = {HH, HT, TH, TT}, each 1/4.",
                "",
                "A = {HH, HT}   P(A) = 1/2",
                "B = {HH, TH}   P(B) = 1/2",
                "C = {HH, TT}   P(C) = 1/2",
                "",
                "PAIRWISE:",
                "   P(A∩B) = P(HH) = 1/4 = (1/2)(1/2)      independent",
                "   P(A∩C) = P(HH) = 1/4 = (1/2)(1/2)      independent",
                "   P(B∩C) = P(HH) = 1/4 = (1/2)(1/2)      independent",
                "",
                "TRIPLE:",
                "   P(A∩B∩C) = P(HH) = 1/4",
                "   P(A)P(B)P(C) = 1/8                     NOT equal",
                "",
                "Pairwise independent, NOT mutually independent.",
            ],
            "after": [
                "Any two of these events determine the third: if the first is heads and "
                "they agree, the second is heads. Mutual independence would mean no "
                "combination of the events carries information about another, and here two "
                "of them carry all of it."
            ],
        },
        "quiz_title": "Independence",
        "quiz": [
            {"q": "`A` and `B` are disjoint with `P(A), P(B) &gt; 0`. They are:",
             "a": ["independent", "dependent", "mutually exclusive and independent",
                   "impossible to classify"],
             "c": 1,
             "why": "`P(A∩B) = 0` but `P(A)P(B) &gt; 0`. Knowing `B` occurred rules out "
                    "`A` entirely, which is maximal dependence."},
            {"q": "The test for independence is:",
             "a": ["the events have no common cause",
                   "`P(A ∩ B) = P(A)P(B)`",
                   "the events are disjoint",
                   "`P(A) = P(B)`"],
             "c": 1,
             "why": "The equation is the definition. Stories about causes are not evidence "
                    "either way &mdash; the sum-of-dice example is independent despite an "
                    "obvious dependence in the description."},
            {"q": "Three events are pairwise independent. Are they mutually independent?",
             "a": ["Yes, always", "Not necessarily", "Only if disjoint", "Only if equally likely"],
             "c": 1,
             "why": "The two-coin example is pairwise independent and fails the triple "
                    "condition. Mutual independence requires every subset."},
        ],
        "mistakes": [
            ("Confusing independent with disjoint",
             "They are close to opposite. Disjoint events with positive probability are "
             "strongly dependent."),
            ("Inferring independence from the description",
             "Physical intuition is unreliable. Compute the three probabilities and "
             "compare."),
            ("Checking pairs and stopping",
             "Mutual independence needs every subset. Pairwise is a strictly weaker "
             "condition, and the gap is not a technicality."),
        ],
        "standard": ("Finish when you check the equation rather than the story.",
                     "Take three events in the two-dice experiment and determine which "
                     "pairs are independent, computing all three probabilities each time. "
                     "At least one answer will not be the one you expected."),
        "note": "Independence of random variables (lesson 7) is the same idea applied to "
                "every pair of values at once: `X` and `Y` are independent when "
                "`P(X = a, Y = b) = P(X = a)P(Y = b)` for all `a` and `b`. Lesson 9 shows "
                "that expectation adds without needing it.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "bayes-theorem",
        "title": "Bayes' Theorem",
        "module": "Conditioning",
        "one_line": "Reversing a conditional, and why the base rate dominates.",
        "summary": (
            "`P(A|B) = P(B|A)P(A)/P(B)` converts one conditional into the other. Applied "
            "to a medical test with a rare disease, it produces an answer most people "
            "&mdash; including most doctors &mdash; get badly wrong."
        ),
        "key": [
            "P(A|B) = P(B|A)·P(A) / P(B)",
            "P(B) = P(B|A)P(A) + P(B|Ā)P(Ā)        law of total probability",
            "P(A)  is the PRIOR;  P(A|B) is the POSTERIOR",
            "A rare condition means most positives are FALSE positives.",
        ],
        "key_label": "Reversing the conditional",
        "concepts_intro": (
            "The theorem is one line of algebra. Its consequences are the reason this "
            "lesson exists."
        ),
        "concepts": [
            ("It follows immediately from the definition",
             "Both `P(A|B)P(B)` and `P(B|A)P(A)` equal `P(A ∩ B)`, so they are equal to "
             "each other. Dividing gives the theorem."),
            ("The denominator needs the law of total probability",
             "`P(B)` is usually computed by splitting on `A` and `Ā`, which is where the "
             "base rate enters the calculation."),
            ("The base rate dominates for rare events",
             "A 99%-accurate test for a disease affecting 1 in 10 000 produces about 100 "
               "false positives for every true one."),
        ],
        "read_title": "Bayes' theorem",
        "read_intro": "The statement, the total-probability denominator, and the medical-test calculation.",
        "body": [
            ("thm", ("Law of total probability",
                     "If `A₁, …, A_n` partition `S` with each `P(Aᵢ) &gt; 0`, then "
                     "`P(B) = Σᵢ P(B|Aᵢ)P(Aᵢ)`. The two-case form is "
                     "`P(B) = P(B|A)P(A) + P(B|Ā)P(Ā)`.")),
            ("proof", [
                "The sets `B ∩ Aᵢ` are disjoint with union `B`, so by additivity "
                "`P(B) = Σ P(B ∩ Aᵢ)`, and each term is `P(B|Aᵢ)P(Aᵢ)` by the "
                "multiplication rule.",
            ]),
            ("thm", ("Bayes' theorem",
                     "For events with `P(A), P(B) &gt; 0`, "
                     "`P(A|B) = P(B|A)P(A) / P(B)`, where `P(B)` is normally expanded by "
                     "the law of total probability.")),
            ("proof", [
                "`P(A ∩ B) = P(A|B)P(B)` and `P(A ∩ B) = P(B|A)P(A)`. Setting the two equal "
                "and dividing by `P(B)` gives the result.",
            ]),
            ("h3", "The medical test"),
            ("p", "A disease affects 1 in 1000 people. A test detects it in 99% of those "
                  "who have it, and gives a false positive in 5% of those who do not. You "
                  "test positive. What is the probability you have the disease?"),
            ("math", [
                "P(D)       = 0.001            prior — the base rate",
                "P(+ | D)   = 0.99             sensitivity",
                "P(+ | D̄)   = 0.05             false positive rate",
                "",
                "P(+) = P(+|D)P(D) + P(+|D̄)P(D̄)",
                "     = 0.99 × 0.001  +  0.05 × 0.999",
                "     = 0.00099       +  0.04995        =  0.05094",
                "",
                "P(D | +) = 0.00099 / 0.05094  ≈  0.0194",
            ]),
            ("p", "About <strong>2%</strong>. A positive result on a 99%-sensitive test "
                  "leaves you 98% likely not to have the disease, because the test is "
                  "applied to a population in which almost nobody does."),
            ("h3", "The same calculation in frequencies"),
            ("math", [
                "Imagine 100 000 people:",
                "        100 have the disease   →   99 test positive",
                "     99 900 do not             → 4 995 test positive",
                "",
                "     total positives = 5 094,   of whom 99 actually have it",
                "     99 / 5094 ≈ 2%",
            ]),
            ("p", "The frequency version is the same arithmetic and is far easier to "
                  "believe. It is worth doing both ways every time: the formula gives the "
                  "number and the frequencies explain it."),
            ("p", "The error the calculation prevents is <strong>base-rate neglect</strong>: "
                  "reading `P(+ | D) = 0.99` as though it were `P(D | +)`. The two differ "
                  "by the factor `P(D)/P(+)`, and when the disease is rare that factor is "
                  "enormous."),
        ],
        "lab": ("probability", {
            "experiment": "urn",
            "panel_title": "Both conditionals at once",
            "panel_intro": "The table shows `P(A|B)` and `P(B|A)` on adjacent rows so the "
                           "difference between them is visible. The status line confirms "
                           "that both routes to `P(A ∩ B)` agree, which is Bayes.",
        }),
        "steps_title": "Applying Bayes",
        "steps_intro": "Write the prior down first; it is the number people forget.",
        "steps": [
            ("Name the events and write the given conditionals",
             "\"Sensitivity\" is `P(+|D)`; \"false positive rate\" is `P(+|D̄)`. Neither is "
             "the number you were asked for."),
            ("Write the prior",
             "The base rate `P(A)`. Omitting it is the error the whole lesson is about."),
            ("Expand the denominator",
             "`P(B) = P(B|A)P(A) + P(B|Ā)P(Ā)`. Both branches contribute, and for rare "
             "conditions the second dominates."),
            ("Sanity-check with frequencies",
             "Take a population of 100 000 and count. If the two methods disagree, the "
             "arithmetic is wrong; if they agree, the surprising answer is right."),
        ],
        "worked": {
            "title": "The same test, a common condition",
            "intro": ["Identical test, but the condition affects 30% of those tested."],
            "lines": [
                "P(D) = 0.30      P(+|D) = 0.99      P(+|D̄) = 0.05",
                "",
                "P(+) = 0.99 × 0.30 + 0.05 × 0.70",
                "     = 0.297      + 0.035        = 0.332",
                "",
                "P(D|+) = 0.297 / 0.332  ≈  0.895",
                "",
                "Compare with the rare case:   P(D) = 0.001  ⟹  P(D|+) ≈ 0.019",
                "",
                "SAME TEST.  The prior moved from 0.001 to 0.30 and the answer",
                "moved from 2% to 89%.",
            ],
            "after": [
                "This is why screening a whole population and testing a symptomatic "
                "patient are different acts with the same instrument. The test did not "
                "change; the population it was applied to did, and the posterior depends "
                "on both."
            ],
        },
        "quiz_title": "Bayes",
        "quiz": [
            {"q": "A test is 99% sensitive for a disease affecting 1 in 1000, with a 5% false positive rate. `P(disease | positive)` is about:",
             "a": ["99%", "95%", "2%", "50%"],
             "c": 2,
             "why": "The false positives from the 99.9% who are healthy vastly outnumber "
                    "the true positives. About 2%."},
            {"q": "The law of total probability is used in Bayes to:",
             "a": ["compute the numerator", "expand the denominator `P(B)`",
                   "check independence", "normalise the prior"],
             "c": 1,
             "why": "`P(B)` is split over the partition, which is where the base rate "
                    "enters and why the answer depends on it."},
            {"q": "Base-rate neglect is:",
             "a": ["ignoring the false positive rate",
                   "reading `P(B|A)` as though it were `P(A|B)`",
                   "using the wrong test",
                   "a rounding error"],
             "c": 1,
             "why": "The two conditionals differ by the factor `P(A)/P(B)`, and neglecting "
                    "the prior is treating that factor as 1."},
        ],
        "mistakes": [
            ("Reporting the sensitivity as the answer",
             "`P(+|D) = 0.99` is a property of the test. `P(D|+)` is what the patient "
             "wants and depends on the population as well."),
            ("Omitting the false-positive branch of the denominator",
             "For a rare condition that branch is almost all of `P(B)`. Dropping it "
             "produces an answer near 1 instead of near 0."),
            ("Trusting the formula without the frequency check",
             "The frequency version takes thirty seconds and makes the surprising answer "
             "believable rather than merely computed."),
        ],
        "standard": ("Finish when you can do the calculation both ways.",
                     "Take a test with 95% sensitivity and 10% false positives for a "
                     "condition affecting 2% of the population. Compute `P(D|+)` by the "
                     "formula, then by counting a population of 10 000. The agreement is "
                     "the point."),
        "note": "Bayes' theorem is also the foundation of a whole approach to statistics, "
                "in which the prior encodes belief before the data and the posterior "
                "encodes it afterwards. The mathematics here is the same; what is "
                "contested is where priors come from.",
    },
]
