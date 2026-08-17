"""Course 4, lessons 08-14 — repetition, corrections, and technique."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "combinations-with-repetition",
        "title": "Combinations with Repetition",
        "module": "Repetition",
        "one_line": "Stars and bars: `C(n + r − 1, r)`.",
        "summary": (
            "Choosing `r` items from `n` types with repetition allowed and order "
            "irrelevant. The count is `C(n+r−1, r)`, and the reason is a bijection with "
            "arrangements of stars and bars."
        ),
        "key": [
            "unordered, repetition allowed:   C(n + r − 1, r)",
            "equivalently  x₁ + x₂ + … + xₙ = r  with xᵢ ≥ 0",
            "stars = the r items,  bars = the n−1 dividers between types",
            "with xᵢ ≥ 1 instead:  C(r − 1, n − 1)",
        ],
        "key_label": "The fourth rule",
        "concepts_intro": (
            "The last of the four counting rules, and the only one whose formula is not "
            "obvious from the statement."
        ),
        "concepts": [
            ("The selection is a count per type",
             "Choosing 5 doughnuts from 3 kinds is choosing how many of each: a solution "
             "of `x₁ + x₂ + x₃ = 5` in non-negative integers."),
            ("Stars and bars encodes that solution",
             "Write `r` stars and `n − 1` bars; the bars split the stars into `n` groups. "
             "Every arrangement is a selection and conversely."),
            ("Positivity shifts the problem",
             "Requiring each `xᵢ ≥ 1` is the same problem with `r − n` items to distribute "
             "freely, so the count is `C(r−1, n−1)`."),
        ],
        "read_title": "Stars and bars",
        "read_intro": "The bijection, the formula, and the variants.",
        "body": [
            ("thm", ("Combinations with repetition",
                     "The number of ways to choose `r` items from `n` types, with "
                     "repetition allowed and order irrelevant, is `C(n + r − 1, r)`.")),
            ("proof", [
                "Encode a selection as a row of `r` stars and `n − 1` bars: the stars "
                "before the first bar are the items of type 1, those between the first and "
                "second bar are type 2, and so on. Empty groups are allowed and represent "
                "types not chosen.",
                "This is a bijection. Every selection gives exactly one such row, and every "
                "row of `r` stars and `n − 1` bars gives exactly one selection.",
                "A row is an arrangement of `r + n − 1` symbols of which `r` are stars, so "
                "there are `C(n + r − 1, r)` of them.",
            ]),
            ("example", ("Doughnuts",
                         "Five doughnuts from three kinds: `C(3 + 5 − 1, 5) = C(7,5) = 21`. "
                         "The selection \"two glazed, none jam, three chocolate\" is the row "
                         "`** | | ***`.")),
            ("p", "The picture is worth keeping. `n` types need `n − 1` bars, not `n`, "
                  "because the bars go <em>between</em> the groups. Using `n` bars is the "
                  "standard error and gives `C(n+r, r)`."),
            ("thm", ("Non-negative integer solutions",
                     "The number of solutions of `x₁ + ⋯ + x_n = r` in non-negative "
                     "integers is `C(n + r − 1, r)` &mdash; the same count, since a "
                     "solution is exactly a selection.")),
            ("thm", ("Positive integer solutions",
                     "The number of solutions with every `xᵢ ≥ 1` is `C(r − 1, n − 1)`.")),
            ("proof", [
                "Give each variable 1 up front, leaving `r − n` units to distribute freely "
                "among `n` variables. That is the non-negative problem with `r − n` in "
                "place of `r`, so the count is `C(n + (r−n) − 1, r−n) = C(r−1, r−n)`, which "
                "equals `C(r−1, n−1)` by symmetry.",
            ]),
            ("p", "The substitution trick generalises. A constraint `xᵢ ≥ c` is handled by "
                  "pre-assigning `c` units to that variable and solving the reduced "
                  "problem; an upper bound `xᵢ ≤ c` is harder and needs the inclusion and "
                  "exclusion of lesson 9."),
            ("h3", "The four rules, together"),
            ("math", [
                "                        order matters     order does not",
                "repetition forbidden      P(n, r)             C(n, r)",
                "repetition allowed         nʳ            C(n + r − 1, r)",
            ]),
            ("p", "Every basic counting problem in this course is one of these four. The "
                  "arithmetic differs by orders of magnitude &mdash; at `n = 5`, `r = 3` "
                  "the four give 60, 10, 125 and 35 &mdash; so classifying correctly "
                  "matters far more than computing carefully."),
        ],
        "lab": ("counting", {
            "n": 3, "r": 5, "rule": "cr",
            "panel_title": "All four rules at once",
            "panel_intro": "The CR row is this lesson. The enumeration lists the actual "
                           "multisets, which is what makes `C(n+r−1, r)` believable rather "
                           "than memorised.",
        }),
        "steps_title": "Recognising a stars-and-bars problem",
        "steps_intro": "Look for identical items distributed among distinct types.",
        "steps": [
            ("Check the items are interchangeable",
             "Five identical doughnuts, `r` indistinguishable units. If the items are "
             "distinct, this is not the right formula."),
            ("Check the types are distinct",
             "Three named kinds, `n` labelled boxes. Identical boxes give a much harder "
             "problem that this course does not cover."),
            ("Translate to an equation",
             "`x₁ + ⋯ + x_n = r` with the constraints stated. This form makes the "
             "substitutions visible."),
            ("Handle lower bounds by substitution",
             "`xᵢ ≥ c` becomes `yᵢ = xᵢ − c ≥ 0` with the total reduced by `c`. Upper "
             "bounds need lesson 9."),
        ],
        "worked": {
            "title": "A bounded distribution",
            "intro": ["Solutions of `x₁ + x₂ + x₃ = 12` with `xᵢ ≥ 2` for each `i`."],
            "lines": [
                "Substitute yᵢ = xᵢ − 2, so each yᵢ ≥ 0 and",
                "",
                "   y₁ + y₂ + y₃ = 12 − 6 = 6",
                "",
                "Non-negative solutions:  C(3 + 6 − 1, 6) = C(8, 6) = 28",
                "",
                "Check the extremes:",
                "   y = (6,0,0)  ⟹  x = (8,2,2)      ✓ all ≥ 2",
                "   y = (2,2,2)  ⟹  x = (4,4,4)      ✓",
                "",
                "Without the constraint:  C(3 + 12 − 1, 12) = C(14,12) = 91",
            ],
            "after": [
                "Lower bounds are free: pre-assign and shrink the total. Upper bounds are "
                "not &mdash; counting the solutions with `xᵢ ≤ 5` requires subtracting the "
                "violating cases and adding back the double violations, which is exactly "
                "lesson 9."
            ],
        },
        "quiz_title": "Stars and bars",
        "quiz": [
            {"q": "How many ways to choose 4 items from 3 types with repetition?",
             "a": ["12", "15", "81", "24"],
             "c": 1,
             "why": "`C(3 + 4 − 1, 4) = C(6,4) = 15`. Four stars and two bars, arranged in "
                    "`C(6,4)` ways."},
            {"q": "How many bars does a stars-and-bars diagram with `n` types use?",
             "a": ["`n`", "`n − 1`", "`n + 1`", "`r`"],
             "c": 1,
             "why": "The bars sit between the groups, so `n` groups need `n − 1` "
                    "separators. Using `n` is the standard error."},
            {"q": "Solutions of `x₁ + x₂ + x₃ = 10` with each `xᵢ ≥ 1`:",
             "a": ["`C(12,10)`", "`C(9,2) = 36`", "`C(10,3)`", "`3¹⁰`"],
             "c": 1,
             "why": "`C(r−1, n−1) = C(9,2) = 36`. Equivalently, give each variable 1 and "
                    "distribute the remaining 7 freely."},
        ],
        "mistakes": [
            ("Using `n` bars instead of `n − 1`",
             "The bars separate the groups, so there is one fewer of them than there are "
             "types. The picture makes it obvious; the formula does not."),
            ("Applying it to distinguishable items",
             "Stars and bars needs the items interchangeable. Distributing distinct objects "
             "into boxes is the multinomial count of lesson 7."),
            ("Trying to handle an upper bound by substitution",
             "Lower bounds shift cleanly; upper bounds require subtracting the violations, "
             "which is inclusion and exclusion."),
        ],
        "standard": ("Finish when you can translate between the three phrasings.",
                     "Take \"how many ways to put 8 identical balls into 4 labelled boxes\", "
                     "restate it as an equation and as a stars-and-bars diagram, and "
                     "compute. All three descriptions are the same problem, and recognising "
                     "that is the point."),
        "note": "The complementary problem &mdash; identical balls into identical boxes "
                "&mdash; is counted by partition numbers, which have no closed form and "
                "grow subexponentially. Labelling the boxes is what makes this lesson's "
                "problem tractable.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "inclusion-exclusion",
        "title": "The Inclusion-Exclusion Principle",
        "module": "Corrections",
        "one_line": "Add the sizes, subtract the pairs, add back the triples.",
        "summary": (
            "When sets overlap the sum rule over-counts. Inclusion and exclusion corrects "
            "it exactly, with alternating signs, and it is the tool behind derangements, "
            "surjection counts and Euler's totient function."
        ),
        "key": [
            "|A ∪ B| = |A| + |B| − |A ∩ B|",
            "|A∪B∪C| = Σ|Aᵢ| − Σ|Aᵢ∩Aⱼ| + |A∩B∩C|",
            "general: alternating sum over all nonempty subsets of the index set",
            "usually applied to the COMPLEMENT: none of the properties",
        ],
        "key_label": "Correcting the over-count",
        "concepts_intro": (
            "Each element must be counted exactly once. The alternating signs are what "
            "makes that happen for every element regardless of how many sets it lies in."
        ),
        "concepts": [
            ("Adding sizes over-counts overlaps",
             "An element in two sets is counted twice, one in three is counted three "
             "times. Subtracting pairwise intersections over-corrects the triples, so "
             "they are added back."),
            ("The signs are forced",
             "An element in exactly `m` of the sets is counted `C(m,1) − C(m,2) + C(m,3) "
             "− ⋯`, which is 1 for every `m ≥ 1` by the alternating-sum identity of "
             "lesson 5."),
            ("The complement form is usually what you want",
             "\"None of the properties\" equals the total minus the union, and that is "
             "how derangements and surjection counts are computed."),
        ],
        "read_title": "The principle",
        "read_intro": "The two-set and three-set cases, the general statement, and why it is exact.",
        "body": [
            ("thm", ("Two and three sets",
                     "`|A ∪ B| = |A| + |B| − |A ∩ B|` and "
                     "`|A ∪ B ∪ C| = |A| + |B| + |C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|`.")),
            ("thm", ("Inclusion-exclusion",
                     "For finite sets `A₁, …, A_n`, "
                     "`|A₁ ∪ ⋯ ∪ A_n| = Σ|Aᵢ| − Σ_{i&lt;j}|Aᵢ∩Aⱼ| + Σ_{i&lt;j&lt;k}|Aᵢ∩Aⱼ∩A_k| − ⋯ "
                     "+ (−1)^{n+1}|A₁∩⋯∩A_n|` &mdash; an alternating sum over all nonempty "
                     "subsets of the indices.")),
            ("proof", [
                "Take an element lying in exactly `m` of the sets, `m ≥ 1`. It is counted "
                "`C(m,1)` times in the first sum, `C(m,2)` times in the second, and so on, "
                "so its net contribution is "
                "`C(m,1) − C(m,2) + C(m,3) − ⋯ = 1 − [C(m,0) − C(m,1) + C(m,2) − ⋯]`.",
                "The bracket is the alternating row sum, which is 0 for `m ≥ 1` (lesson 5). "
                "So the contribution is exactly 1.",
                "An element in none of the sets contributes 0 to every term. Hence each "
                "element of the union is counted once and nothing else is counted.",
            ]),
            ("p", "That proof explains the signs rather than asserting them: they are "
                  "exactly what is needed to make every element's contribution collapse to "
                  "1, and the collapse is the alternating-sum identity from Pascal's "
                  "triangle."),
            ("h3", "The complement form"),
            ("thm", ("Counting elements with none of the properties",
                     "If `Aᵢ` is the set of objects with property `i`, then the number "
                     "with none of them is "
                     "`|U| − Σ|Aᵢ| + Σ|Aᵢ∩Aⱼ| − ⋯`, the same alternating sum with the "
                     "signs shifted.")),
            ("example", ("Divisibility",
                         "How many of `1, …, 1000` are divisible by none of 2, 3, 5? "
                         "`1000 − (500 + 333 + 200) + (166 + 100 + 66) − 33 = 266`. Each "
                         "term is a floor division: `⌊1000/6⌋ = 166` counts the multiples "
                         "of both 2 and 3.")),
            ("thm", ("Euler's totient",
                     "The count of integers in `1, …, n` coprime to `n` is "
                     "`φ(n) = n·Π(1 − 1/p)` over the distinct primes `p` dividing `n`. "
                     "That product is inclusion and exclusion over the prime divisors, "
                     "multiplied out. Course 6 uses `φ` throughout.")),
            ("thm", ("Counting surjections",
                     "The number of surjections from an `m`-set onto an `n`-set is "
                     "`Σ_{k=0}^{n} (−1)^k C(n,k)(n−k)^m` &mdash; total functions minus "
                     "those missing at least one target, corrected.")),
            ("p", "The pattern in all three: the direct count is hard and the count of "
                  "\"violates condition `i`\" is easy, so count the violations and "
                  "alternate. Recognising that shape is what this lesson is for."),
        ],
        "lab": ("inclusion_exclusion", {
            "panel_title": "Both routes to the same number",
            "panel_intro": "The table builds the alternating sum term by term while the "
                           "right-hand count walks 1 to N one integer at a time. They must "
                           "agree, and watching the running total shows where the naive sum "
                           "goes wrong.",
        }),
        "steps_title": "Applying inclusion and exclusion",
        "steps_intro": "Define the sets so the intersections are easy.",
        "steps": [
            ("Define `Aᵢ` as \"has property `i`\"",
             "Usually the bad property. Counting `Aᵢ` and its intersections must be easier "
             "than counting the objects you want."),
            ("Compute every intersection size",
             "Pairs, triples, and so on. Symmetry often makes many of them equal, which is "
             "what keeps the sum manageable."),
            ("Alternate the signs",
             "Add the singles, subtract the pairs, add the triples. Off by one in the sign "
             "pattern gives an answer that is wrong by twice the correction."),
            ("Sanity check the magnitude",
             "The answer must lie between 0 and the total. A negative result means a sign "
             "error; a result above the total means a missed subtraction."),
        ],
        "worked": {
            "title": "Surjections from a 5-set onto a 3-set",
            "intro": ["How many functions from `{1,…,5}` onto `{a,b,c}` hit every target?"],
            "lines": [
                "Total functions:  3⁵ = 243",
                "",
                "Let Aₓ = functions that MISS target x.",
                "   |Aₓ| = 2⁵ = 32,  and there are C(3,1) = 3 of them",
                "   |Aₓ ∩ A_y| = 1⁵ = 1,  and there are C(3,2) = 3 of them",
                "   |Aₐ ∩ A_b ∩ A_c| = 0⁵ = 0",
                "",
                "Functions missing at least one:  3·32 − 3·1 + 0 = 93",
                "",
                "Surjections:  243 − 93 = 150",
                "",
                "Formula check:  Σ (−1)ᵏ C(3,k)(3−k)⁵",
                "              = 243 − 3·32 + 3·1 − 0  =  150       ✓",
            ],
            "after": [
                "`0⁵ = 0` is the right value here: no function can miss all three targets "
                "when the domain is nonempty. The convention `0⁰ = 1` would matter if the "
                "domain were empty, which is exactly the edge case such formulas are "
                "tested on."
            ],
        },
        "quiz_title": "Inclusion and exclusion",
        "quiz": [
            {"q": "`|A| = 20`, `|B| = 15`, `|A ∩ B| = 6`. What is `|A ∪ B|`?",
             "a": ["35", "29", "41", "26"],
             "c": 1,
             "why": "`20 + 15 − 6 = 29`. The six shared elements were counted twice by the "
                    "naive sum."},
            {"q": "In the three-set formula, the triple intersection is:",
             "a": ["subtracted", "added", "ignored", "counted twice"],
             "c": 1,
             "why": "Added back. Elements in all three were counted three times, then "
                    "subtracted three times by the pairs, leaving zero &mdash; so one "
                    "addition restores them."},
            {"q": "Inclusion and exclusion is usually applied to:",
             "a": ["the union directly",
                   "the complement — the objects with none of the properties",
                   "the intersection",
                   "the power set"],
             "c": 1,
             "why": "Derangements, surjections and totients are all \"none of the bad "
                    "properties\" counts, computed as total minus the union of the bad sets."},
        ],
        "mistakes": [
            ("Getting the sign pattern wrong",
             "Odd-sized intersections are added, even-sized subtracted &mdash; in the union "
             "form. The complement form starts from the total and reverses. Write which "
             "form you are using."),
            ("Missing an intersection term",
             "With `n` sets there are `2ⁿ − 1` terms. For four sets that is 15, and "
             "forgetting one silently changes the answer."),
            ("Assuming the intersections are all equal",
             "They often are, by symmetry, and when they are not the count must be done "
             "term by term."),
        ],
        "standard": ("Finish when you can set up the sets so the intersections are easy.",
                     "Count the permutations of `1, …, 6` in which no element stays in its "
                     "own position. Define `Aᵢ` as \"element `i` is fixed\", compute the "
                     "intersections, and alternate. Lesson 10 is that answer in general."),
        "note": "The principle generalises far beyond counting: the same alternating "
                "structure appears in Möbius inversion, in the sieve methods of analytic "
                "number theory, and in the probabilistic version course 5 uses for "
                "`P(A ∪ B)`.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "derangements",
        "title": "Derangements",
        "module": "Corrections",
        "one_line": "Permutations with no fixed point, and the surprising limit.",
        "summary": (
            "A derangement moves every element. Inclusion and exclusion counts them, and "
            "the proportion of permutations that are derangements converges to `1/e` "
            "almost immediately &mdash; it is already accurate at `n = 7`."
        ),
        "key": [
            "Dₙ = n! · Σ_{k=0}^{n} (−1)^k / k!",
            "Dₙ / n!  →  1/e ≈ 0.3679          and fast",
            "D₁=0  D₂=1  D₃=2  D₄=9  D₅=44  D₆=265",
            "Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂)           a recurrence too",
        ],
        "key_label": "The canonical application",
        "concepts_intro": (
            "Derangements are the standard worked example of inclusion and exclusion, "
            "and their limit is genuinely surprising."
        ),
        "concepts": [
            ("A derangement has no fixed point",
             "`σ(i) ≠ i` for every `i`. The hat-check problem: nobody gets their own hat."),
            ("Inclusion and exclusion counts them",
             "Let `Aᵢ` be the permutations fixing `i`. Then `|Aᵢ| = (n−1)!` and the "
             "intersections are similarly clean, so the alternating sum closes."),
            ("The proportion converges immediately",
             "`Dₙ/n!` is within `10⁻⁴` of `1/e` by `n = 7`. The chance that nobody gets "
             "their own hat is essentially the same for 10 people and for 10 million."),
        ],
        "read_title": "Counting derangements",
        "read_intro": "The derivation, the recurrence, and the limit.",
        "body": [
            ("def", ("Derangement",
                     "A <strong>derangement</strong> of `{1, …, n}` is a permutation `σ` "
                     "with `σ(i) ≠ i` for every `i`. `Dₙ` denotes the number of them.")),
            ("thm", ("The derangement formula",
                     "`Dₙ = n! Σ_{k=0}^{n} (−1)^k / k! "
                     "= n! (1 − 1/1! + 1/2! − 1/3! + ⋯ + (−1)ⁿ/n!)`.")),
            ("proof", [
                "Let `Aᵢ` be the set of permutations fixing `i`. A permutation is a "
                "derangement exactly when it lies in none of the `Aᵢ`, so "
                "`Dₙ = n! − |A₁ ∪ ⋯ ∪ A_n|`.",
                "Fixing a specified set of `k` elements leaves the other `n − k` free, so "
                "each `k`-fold intersection has `(n−k)!` members, and there are `C(n,k)` "
                "such intersections.",
                "By inclusion and exclusion, "
                "`Dₙ = Σ_{k=0}^{n} (−1)^k C(n,k)(n−k)! = Σ_{k=0}^{n} (−1)^k n!/k!`, which "
                "is the stated formula.",
            ]),
            ("math", [
                "n     1    2    3    4     5      6       7        8",
                "n!    1    2    6   24   120    720    5040    40320",
                "Dₙ    0    1    2    9    44    265    1854    14833",
                "Dₙ/n!  0  .500 .333 .375 .3667 .36806 .367857 .3678792",
                "1/e ≈ 0.3678794412",
            ]),
            ("p", "The convergence is startlingly quick because the series for `1/e` "
                  "alternates with rapidly shrinking terms: the error after `n` terms is "
                  "below `1/(n+1)!`. By `n = 7` that is under `1/40320`."),
            ("thm", ("Rounding formula",
                     "`Dₙ` is the nearest integer to `n!/e` for every `n ≥ 1`, which "
                     "follows from the same error bound.")),
            ("thm", ("A recurrence",
                     "`Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂)` for `n ≥ 3`, with `D₁ = 0` and `D₂ = 1`.")),
            ("proof", [
                "In a derangement, element 1 goes to some position `j ≠ 1`, and there are "
                "`n − 1` choices of `j`. Split on what happens to `j`:",
                "If `j` goes to position 1, the remaining `n − 2` elements form a "
                "derangement among themselves: `Dₙ₋₂` ways.",
                "If `j` does not go to position 1, then treating \"position 1\" as the "
                "forbidden position for `j` makes the remaining `n − 1` elements a "
                "derangement of `n − 1` items: `Dₙ₋₁` ways.",
                "So `Dₙ = (n−1)(Dₙ₋₂ + Dₙ₋₁)`.",
            ]),
            ("p", "Two derivations of the same numbers, by different techniques. The "
                  "recurrence is a case split of the kind course 3 lesson 9 taught; the "
                  "formula came from inclusion and exclusion. Agreement between them is a "
                  "genuine check, and both are worth having."),
            ("example", ("The hat-check problem",
                         "`n` people check hats and receive them back at random. The "
                         "probability nobody gets their own is `Dₙ/n!`, which for `n ≥ 5` "
                         "is 0.3679 to four places whatever `n` is. Course 5 makes the "
                         "division into a probability statement.")),
        ],
        "lab": ("inclusion_exclusion", {
            "panel_title": "The correction, term by term",
            "panel_intro": "Derangements are this alternating structure applied to fixed "
                           "points. Watch the running total swing above and below the "
                           "answer before settling &mdash; that is what alternating means.",
        }),
        "steps_title": "Using derangements",
        "steps_intro": "Recognise the \"nothing in its own place\" shape.",
        "steps": [
            ("Check every element has exactly one forbidden position",
             "That is what makes it a derangement. More complicated forbidden patterns "
             "need the permanent of a matrix and are outside this course."),
            ("Use the formula or the recurrence",
             "The recurrence is faster by hand for small `n`; the formula is what "
             "generalises."),
            ("For a partial condition, combine with combinations",
             "\"Exactly `k` fixed points\" is `C(n,k)·D_{n−k}`: choose which stay, derange "
             "the rest."),
            ("Check against `n!/e`",
             "`Dₙ` is the nearest integer to `n!/e`. It is a one-line verification of an "
             "answer computed another way."),
        ],
        "worked": {
            "title": "Exactly two people get their own hat",
            "intro": ["Out of six people, how many outcomes fix exactly two?"],
            "lines": [
                "Choose WHICH two get their own hat:   C(6,2) = 15",
                "Derange the other four so none is fixed:  D₄ = 9",
                "",
                "   15 × 9 = 135 outcomes",
                "",
                "Total outcomes:  6! = 720,  so the proportion is 135/720 = 0.1875",
                "",
                "Check by summing over all k:",
                "   Σ_k C(6,k)·D_{6−k}",
                " = 265 + 6·44 + 15·9 + 20·2 + 15·1 + 6·0 + 1·1",
                " = 265 + 264 + 135 + 40 + 15 + 0 + 1  =  720  =  6!     ✓",
            ],
            "after": [
                "The final check is the useful one: every permutation has exactly one "
                "number of fixed points, so summing over `k` must recover `n!`. `D₀ = 1` "
                "&mdash; the empty permutation deranges vacuously &mdash; is what makes the "
                "last term come out right."
            ],
        },
        "quiz_title": "Derangements",
        "quiz": [
            {"q": "`D₄` equals:",
             "a": ["6", "9", "12", "24"],
             "c": 1,
             "why": "`4!(1 − 1 + 1/2 − 1/6 + 1/24) = 24 · 9/24 = 9`. The recurrence gives "
                    "the same: `3(D₃ + D₂) = 3(2 + 1) = 9`."},
            {"q": "As `n` grows, `Dₙ/n!` approaches:",
             "a": ["0", "1/2", "`1/e ≈ 0.3679`", "1"],
             "c": 2,
             "why": "The sum is the alternating series for `e⁻¹`, and it converges so fast "
                    "that four decimal places are correct by `n = 7`."},
            {"q": "Permutations of 5 elements with exactly one fixed point:",
             "a": ["`D₅`", "`C(5,1)·D₄ = 45`", "`5!`", "`D₄`"],
             "c": 1,
             "why": "Choose which element is fixed (5 ways) and derange the other four "
                    "(`D₄ = 9`)."},
        ],
        "mistakes": [
            ("Forgetting `D₀ = 1`",
             "The empty permutation has no fixed points, so it is a derangement. This "
             "convention is what makes `Σ_k C(n,k)D_{n−k} = n!` come out exactly."),
            ("Applying derangements to unequal forbidden sets",
             "Derangements assume each element has exactly one forbidden position. "
             "General forbidden-position problems are much harder."),
            ("Expecting the proportion to vary with `n`",
             "It stabilises immediately. The chance nobody gets their own hat is the same "
             "for 8 people as for 8000, to four decimal places."),
        ],
        "standard": ("Finish when you can count \"exactly `k` fixed points\" unaided.",
                     "Compute the number of permutations of 7 elements with exactly three "
                     "fixed points, then verify that summing your formula over all `k` from "
                     "0 to 7 gives `7! = 5040`. The check is what confirms the setup."),
        "note": "`e` appearing in a purely combinatorial count is not a coincidence: the "
                "alternating sum in the derangement formula is a truncation of the Taylor "
                "series for `e⁻¹`, and the truncation error is smaller than the gap "
                "between consecutive integers.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "generalized-pigeonhole",
        "title": "The Generalised Pigeonhole Principle",
        "module": "Corrections",
        "one_line": "`⌈n/k⌉` in a box, and what that proves.",
        "summary": (
            "With `n` objects in `k` boxes, some box holds at least `⌈n/k⌉`. Course 2 "
            "stated it; here it is applied to monotone subsequences and to the Ramsey "
            "number `R(3,3) = 6`."
        ),
        "key": [
            "n objects, k boxes  ⟹  some box has ≥ ⌈n/k⌉",
            "Erdős–Szekeres: any sequence of n²+1 distinct reals has a monotone",
            "                subsequence of length n+1",
            "R(3,3) = 6:  any 2-colouring of K₆ has a monochromatic triangle",
        ],
        "key_label": "One bound, two theorems",
        "concepts_intro": (
            "The principle is elementary. The theorems it proves are not, and the gap "
            "between the two is the point of this lesson."
        ),
        "concepts": [
            ("The bound rounds up",
             "20 objects into 6 boxes guarantees a box with 4, not 3. Rounding down gives "
             "a claim that is true but weaker than what holds."),
            ("Choosing the boxes is the whole difficulty",
             "In Erdős&ndash;Szekeres the boxes are pairs of subsequence lengths, which is "
             "not a classification anyone would guess."),
            ("It gives certainty, not likelihood",
             "Six people always contain three mutual acquaintances or three mutual "
             "strangers. No probability is involved."),
        ],
        "read_title": "The principle, applied",
        "read_intro": "Statement, then two theorems whose proofs are pigeonhole with a clever classification.",
        "body": [
            ("thm", ("Generalised pigeonhole principle",
                     "If `n` objects are placed into `k` boxes, some box contains at least "
                     "`⌈n/k⌉` objects.")),
            ("proof", [
                "If every box held at most `⌈n/k⌉ − 1`, the total would be at most "
                "`k(⌈n/k⌉ − 1) &lt; k(n/k + 1 − 1) = n`, using `⌈n/k⌉ &lt; n/k + 1`. That "
                "contradicts having placed all `n`.",
            ]),
            ("example", ("Basic applications",
                         "Among 100 people, at least `⌈100/12⌉ = 9` share a birth month. In "
                         "any set of 10 integers, at least `⌈10/2⌉ = 5` share a parity. "
                         "Each is one division.")),
            ("h3", "Monotone subsequences"),
            ("thm", ("Erdős-Szekeres",
                     "Every sequence of `n² + 1` distinct real numbers contains a "
                     "monotone subsequence of length `n + 1` &mdash; increasing or "
                     "decreasing.")),
            ("proof", [
                "For each position `i`, let `aᵢ` be the length of the longest increasing "
                "subsequence ending at `i`, and `bᵢ` the length of the longest decreasing "
                "one ending at `i`.",
                "Suppose no monotone subsequence of length `n+1` exists. Then every `aᵢ` "
                "and every `bᵢ` lies in `{1, …, n}`, so the pair `(aᵢ, bᵢ)` takes one of "
                "`n²` values. With `n² + 1` positions, two positions `i &lt; j` share a "
                "pair.",
                "But that is impossible. If `xᵢ &lt; xⱼ` then the increasing subsequence "
                "ending at `i` extends to `j`, so `aⱼ &gt; aᵢ`. If `xᵢ &gt; xⱼ` then "
                "`bⱼ &gt; bᵢ`. Either way the pairs differ.",
            ]),
            ("p", "The boxes are the `n²` possible pairs `(aᵢ, bᵢ)`, and inventing them is "
                  "the entire proof. Once the classification is chosen, the pigeonhole "
                  "principle does the rest in one line. This is the lesson's real content: "
                  "the principle is trivial and the classification is not."),
            ("h3", "A Ramsey number"),
            ("thm", ("`R(3,3) = 6`",
                     "Among any six people, three are mutual acquaintances or three are "
                     "mutual strangers. Five people do not suffice.")),
            ("proof", [
                "Take a person `P`. Each of the other five is an acquaintance or a "
                "stranger, so by pigeonhole at least `⌈5/2⌉ = 3` fall in one class; say "
                "three acquaintances `A`, `B`, `C`.",
                "If any two of `A`, `B`, `C` know each other, they and `P` are three mutual "
                "acquaintances. If no two of them do, `A`, `B`, `C` are three mutual "
                "strangers.",
                "For five people it can fail: arrange them in a circle where each knows "
                "exactly the two neighbours. That has no triangle of either kind.",
            ]),
            ("p", "Both halves are needed. The construction on five people is what makes "
                  "the theorem say `R(3,3) = 6` rather than `R(3,3) ≤ 6`, and producing "
                  "such constructions is generally much harder than the pigeonhole bound."),
            ("p", "Ramsey numbers grow ferociously and are almost entirely unknown. "
                  "`R(4,4) = 18`; `R(5,5)` is only known to lie between 43 and 46, despite "
                  "decades of effort. Erdős's remark is the standard one: if aliens "
                  "demanded `R(5,5)` we should marshal all our computers, and if they "
                  "demanded `R(6,6)` we should attack them instead."),
        ],
        "lab": ("counting", {
            "n": 12, "r": 3, "rule": "c",
            "panel_title": "Objects and boxes",
            "panel_intro": "Pigeonhole arguments are about ratios rather than "
                           "enumerations, but the counts here are the size of the object "
                           "sets those arguments range over.",
        }),
        "steps_title": "Constructing a pigeonhole argument",
        "steps_intro": "Objects are usually given; boxes are invented.",
        "steps": [
            ("Identify the objects",
             "The people, the numbers, the positions in the sequence. Usually explicit in "
             "the problem."),
            ("Invent the classification",
             "The hard step. Remainders, parities, degree counts, pairs of subsequence "
             "lengths &mdash; whatever gives fewer boxes than objects."),
            ("Compute `⌈n/k⌉`",
             "Round up. This is the guaranteed occupancy, and rounding down weakens the "
             "conclusion for no reason."),
            ("State what a full box gives you",
             "Two objects in one box must yield the conclusion. If it does not, the "
             "classification was the wrong one."),
        ],
        "worked": {
            "title": "A subset summing to a multiple of `n`",
            "intro": ["Given any `n` integers, some consecutive block sums to a multiple of `n`."],
            "lines": [
                "Let a₁, …, aₙ be the integers and define the partial sums",
                "   s₁ = a₁,  s₂ = a₁+a₂,  …,  sₙ = a₁+…+aₙ",
                "",
                "Consider their remainders mod n.",
                "",
                "CASE 1  some sⱼ ≡ 0 (mod n).",
                "        Then the block a₁ + … + aⱼ works.",
                "",
                "CASE 2  no sⱼ ≡ 0.  Then the n remainders lie in {1, …, n−1},",
                "        which is n objects in n−1 boxes.",
                "        So sᵢ ≡ sⱼ for some i < j, and",
                "           sⱼ − sᵢ = a_{i+1} + … + aⱼ ≡ 0 (mod n).           ∎",
            ],
            "after": [
                "The classification is \"remainder mod `n`\", and case 1 is what reduces "
                "the box count from `n` to `n − 1` &mdash; the same move as the "
                "acquaintance-count argument in course 2. Creating a surplus by ruling out "
                "one box is the recurring trick."
            ],
        },
        "quiz_title": "Generalised pigeonhole",
        "quiz": [
            {"q": "50 objects into 7 boxes. Some box holds at least:",
             "a": ["7", "8", "6", "9"],
             "c": 1,
             "why": "`⌈50/7⌉ = ⌈7.14⌉ = 8`. Rounding down would give the weaker and "
                    "still-true claim of 7."},
            {"q": "In the Erdős&ndash;Szekeres proof, the boxes are:",
             "a": ["the numbers themselves",
                   "pairs (longest increasing, longest decreasing) ending at each position",
                   "the positions",
                   "the parities"],
             "c": 1,
             "why": "`n²` such pairs and `n² + 1` positions, so two positions share a pair "
                    "&mdash; which the proof then shows is impossible."},
            {"q": "`R(3,3) = 6` means:",
             "a": ["six people always contain three mutual acquaintances",
                   "six is the smallest number forcing three mutual acquaintances or three mutual strangers",
                   "there are six Ramsey numbers",
                   "`R(4,4) = 8`"],
             "c": 1,
             "why": "Six always forces one or the other, and five does not &mdash; the "
                    "five-cycle construction is a counterexample. Both halves are needed "
                    "for equality."},
        ],
        "mistakes": [
            ("Rounding the bound down",
             "It is `⌈n/k⌉`. With 20 objects in 6 boxes the guarantee is 4, and claiming 3 "
             "throws away part of the theorem."),
            ("Choosing more boxes than objects",
             "A finer classification proves less. The boxes must be fewer than the objects "
             "for anything to follow."),
            ("Proving only the upper bound of a Ramsey-type result",
             "`R(3,3) ≤ 6` is the pigeonhole half. Equality needs a construction on five "
             "people, and that half is usually the harder one."),
        ],
        "standard": ("Finish when you can invent a classification for a new problem.",
                     "Show that among any 5 points in a unit square, two are within "
                     "`√2 / 2` of each other &mdash; then improve the bound by choosing a "
                     "finer partition and see what it costs you in the object count."),
        "note": "Ramsey theory is the study of how much order is unavoidable in large "
                "structures. The pigeonhole principle is its simplest instance, and its "
                "characteristic feature is already visible here: the bounds are enormous "
                "and the exact values are almost always unknown.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "generating-functions",
        "title": "Generating Functions",
        "module": "Technique",
        "one_line": "Encode a sequence as coefficients and let algebra do the counting.",
        "summary": (
            "A generating function packs a counting sequence into one formal power "
            "series. Multiplying series corresponds to combining choices, so a counting "
            "problem becomes an algebra problem."
        ),
        "key": [
            "G(x) = a₀ + a₁x + a₂x² + …          the sequence, packed",
            "1/(1−x)   = 1 + x + x² + …          any number of one type",
            "(1+x)ⁿ    = Σ C(n,k) xᵏ             at most one of each of n types",
            "MULTIPLY series  ⟷  COMBINE independent choices",
        ],
        "key_label": "A sequence as one object",
        "concepts_intro": (
            "The idea is a change of representation: turn a sequence into a function so "
            "that operations on sequences become arithmetic."
        ),
        "concepts": [
            ("Coefficients are the answers",
             "`[xᵏ]G(x)` &mdash; the coefficient of `xᵏ` &mdash; is the count for size `k`. "
             "The whole sequence travels together."),
            ("Multiplication is combination",
             "Multiplying two generating functions convolves their coefficients, which is "
             "exactly \"choose some from the first source and the rest from the second\"."),
            ("The series is formal",
             "Convergence is irrelevant. `x` is a bookkeeping symbol and the series is a "
             "way of writing an infinite sequence, not a function to be evaluated."),
        ],
        "read_title": "Generating functions",
        "read_intro": "The definition, the basic series, and two problems solved by algebra.",
        "body": [
            ("def", ("Ordinary generating function",
                     "For a sequence `a₀, a₁, a₂, …`, its <strong>generating function</strong> "
                     "is the formal power series `G(x) = Σ_{k≥0} a_k x^k`. Two series are "
                     "equal exactly when all their coefficients agree.")),
            ("math", [
                "1/(1 − x)      = 1 + x + x² + x³ + …          all a_k = 1",
                "1/(1 − x)²     = 1 + 2x + 3x² + 4x³ + …       a_k = k+1",
                "1/(1 − ax)     = 1 + ax + a²x² + …            a_k = aᵏ",
                "(1 + x)ⁿ       = Σ_k C(n,k) xᵏ                binomial",
                "1/(1 − x)ⁿ     = Σ_k C(n+k−1, k) xᵏ           stars and bars!",
                "(1 − xᵐ⁺¹)/(1 − x) = 1 + x + … + xᵐ           at most m copies",
            ]),
            ("p", "The fifth line is lesson 8 in a different notation, and that is the "
                  "point of the method: `1/(1−x)ⁿ` encodes \"choose any number from each of "
                  "`n` types\", and its coefficients are exactly the stars-and-bars counts."),
            ("h3", "Why multiplication combines choices"),
            ("p", "If `A(x)` counts the ways to pick items from source 1 and `B(x)` from "
                  "source 2, then the coefficient of `xᵏ` in `A(x)B(x)` is "
                  "`Σ_j a_j b_{k−j}` &mdash; take `j` items from the first source and "
                  "`k − j` from the second, over all splits. That is precisely the product "
                  "rule combined with the sum rule."),
            ("example", ("Coins",
                         "In how many ways can `n` cents be made from pennies, nickels and "
                         "dimes? Each denomination contributes a factor: "
                         "`1/(1−x)` for pennies, `1/(1−x⁵)` for nickels, `1/(1−x¹⁰)` for "
                         "dimes. The answer is the coefficient of `xⁿ` in the product. "
                         "For `n = 25` it is 12.")),
            ("example", ("A restricted selection",
                         "How many ways to choose 10 items from 4 types with at most 3 of "
                         "each? Each type contributes `1 + x + x² + x³`, so the answer is "
                         "`[x¹⁰](1 + x + x² + x³)⁴`. Expanding gives 4. Inclusion and "
                         "exclusion would also work; the generating function encodes the "
                         "constraint directly.")),
            ("h3", "Solving a recurrence"),
            ("p", "Generating functions solve recurrences by turning them into equations. "
                  "For `aₙ = 3aₙ₋₁` with `a₀ = 1`, write `G(x) = Σ aₙxⁿ`. Multiplying the "
                  "recurrence by `xⁿ` and summing gives `G(x) − 1 = 3xG(x)`, so "
                  "`G(x) = 1/(1 − 3x)`, whose coefficients are `3ⁿ`."),
            ("p", "The same method handles Fibonacci: `G(x) = x/(1 − x − x²)`, and a "
                  "partial-fraction decomposition recovers Binet's formula from course 3 "
                  "lesson 10. The method is more general than characteristic roots, and it "
                  "extends to recurrences those cannot touch."),
            ("thm", ("Formal manipulation is legitimate",
                     "Addition, multiplication and (when `a₀ ≠ 0`) inversion of formal power "
                     "series are well defined coefficient by coefficient, with no "
                     "convergence question, because each coefficient of a product depends "
                     "on finitely many coefficients of the factors.")),
        ],
        "lab": ("counting", {
            "n": 4, "r": 10, "rule": "cr",
            "panel_title": "The count a generating function encodes",
            "panel_intro": "The CR row is `[xʳ] 1/(1−x)ⁿ`. The generating function packs "
                           "every `r` at once into one expression, which is what makes "
                           "constraints easy to attach.",
        }),
        "steps_title": "Using a generating function",
        "steps_intro": "One factor per source of choice.",
        "steps": [
            ("Write a factor for each source",
             "Unlimited supply gives `1/(1−x)`; at most one gives `1 + x`; at most `m` "
             "gives `1 + x + ⋯ + x^m`; multiples of `d` only gives `1/(1−x^d)`."),
            ("Multiply the factors",
             "The product's coefficients count the combined selections, by the convolution "
             "argument above."),
            ("Extract the coefficient you need",
             "By expansion, by a known series, or by partial fractions. This is where the "
             "algebra lives."),
            ("Check against a direct count",
             "For small `n` the answer should match an enumeration. A generating function "
             "set up wrongly produces a confident wrong series."),
        ],
        "worked": {
            "title": "Making 25 cents",
            "intro": ["Pennies, nickels and dimes, unlimited supply."],
            "lines": [
                "G(x) = 1/(1−x) · 1/(1−x⁵) · 1/(1−x¹⁰)",
                "",
                "We need [x²⁵]G(x).  Split by the number of dimes:",
                "",
                "   0 dimes:  25 cents from pennies and nickels",
                "             nickels 0..5   →  6 ways",
                "   1 dime:   15 cents from pennies and nickels",
                "             nickels 0..3   →  4 ways",
                "   2 dimes:   5 cents from pennies and nickels",
                "             nickels 0..1   →  2 ways",
                "",
                "   total 6 + 4 + 2 = 12",
                "",
                "The generating function ENCODES this split; the case analysis is",
                "what extracting the coefficient amounts to.",
            ],
            "after": [
                "For 25 cents the case split is quicker than the algebra. The generating "
                "function earns its place when the target is symbolic &mdash; it gives the "
                "answer for every `n` at once, and the cases would have to be redone for "
                "each."
            ],
        },
        "quiz_title": "Generating functions",
        "quiz": [
            {"q": "`1/(1 − x)` is the generating function of:",
             "a": ["`1, 1, 1, 1, …`", "`1, 2, 3, 4, …`", "`1, 0, 0, 0, …`", "`2ⁿ`"],
             "c": 0,
             "why": "`1/(1−x) = 1 + x + x² + ⋯`, all coefficients 1. `1/(1−x)²` gives "
                    "`1, 2, 3, 4, …`."},
            {"q": "Multiplying two generating functions corresponds to:",
             "a": ["adding the sequences",
                   "combining independent selections from the two sources",
                   "differentiating",
                   "nothing combinatorial"],
             "c": 1,
             "why": "The coefficient of `xᵏ` in the product sums over all splits of `k` "
                    "between the two sources &mdash; the product rule and the sum rule "
                    "together."},
            {"q": "Which factor encodes \"at most 2 of this type\"?",
             "a": ["`1/(1−x)`", "`1 + x + x²`", "`x²`", "`1/(1−x²)`"],
             "c": 1,
             "why": "One term per allowed quantity: zero, one or two. `1/(1−x²)` would "
                    "encode \"any even number\"."},
        ],
        "mistakes": [
            ("Worrying about convergence",
             "These are formal series. `x` never takes a value, and each coefficient "
             "depends on finitely many others."),
            ("Using the wrong factor for a constraint",
             "\"At most `m`\" is a polynomial with `m+1` terms; \"multiples of `d`\" is "
             "`1/(1−x^d)`. Getting the factor wrong makes the whole product count "
             "something else."),
            ("Reaching for generating functions on a small problem",
             "For one specific `n`, a case split is usually faster. The method pays when "
             "the answer must hold for all `n`."),
        ],
        "standard": ("Finish when you can write the generating function for a constrained "
                     "selection.",
                     "Write the generating function for making `n` cents from pennies, "
                     "nickels and quarters with at most three of each, and extract the "
                     "coefficient for `n = 30`. The factors are where the constraints live."),
        "note": "Exponential generating functions `Σ aₙxⁿ/n!` are the right tool when the "
                "objects are labelled and order matters, and they turn the derangement "
                "recurrence into a two-line calculation. This lesson stays with the "
                "ordinary kind, which suits unlabelled selection problems.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "combinatorial-proof",
        "title": "Combinatorial Proof",
        "module": "Technique",
        "one_line": "Count one set two ways, or biject two sets.",
        "summary": (
            "Two techniques that prove identities without algebra: count a single set in "
            "two ways, or construct a bijection between two sets. Both explain the "
            "identity as well as establishing it."
        ),
        "key": [
            "DOUBLE COUNTING  one set, two counts  ⟹  the counts are equal",
            "BIJECTION        a pairing between two sets  ⟹  equal sizes",
            "Both give WHY, which algebra does not.",
            "State the objects first. Everything else follows.",
        ],
        "key_label": "Two techniques",
        "concepts_intro": (
            "An algebraic proof confirms an identity. A combinatorial proof explains it, "
            "and is usually shorter."
        ),
        "concepts": [
            ("Double counting needs one set and two classifications",
             "Both expressions must count the same objects. Naming those objects precisely "
             "is where the proof is won."),
            ("A bijection needs an explicit map",
             "Describe the map, show it is injective, show it is surjective. \"Clearly "
             "there is a correspondence\" is not a proof."),
            ("The explanation is the value",
             "`Σ k·C(n,k) = n·2ⁿ⁻¹` proved by counting tells you the `n` is a chair and "
             "the `2ⁿ⁻¹` is everyone else. The algebra tells you nothing."),
        ],
        "read_title": "Two techniques",
        "read_intro": "Double counting and bijection, with several identities each.",
        "body": [
            ("h3", "Double counting"),
            ("thm", ("The method",
                     "To prove `A = B`, find a set `S` and show that counting `S` one way "
                     "gives `A` and another way gives `B`. Since `S` has one size, "
                     "`A = B`.")),
            ("example", ("Handshakes",
                         "In any graph, `Σ_v deg(v) = 2|E|`. Count the incidences "
                         "&mdash; pairs (vertex, edge at that vertex). By vertex: each "
                         "contributes its degree. By edge: each has two endpoints. Course "
                         "7 lesson 2 opens with this.")),
            ("example", ("Pascal's rule, again",
                         "`C(n,k) = C(n−1,k−1) + C(n−1,k)`: count `k`-subsets by whether "
                         "they contain a fixed element. One set, two classifications.")),
            ("example", ("Vandermonde",
                         "`C(m+n,r) = Σ_k C(m,k)C(n,r−k)`: count `r`-subsets of a set split "
                         "into groups of `m` and `n`, classified by how many come from the "
                         "first group.")),
            ("h3", "Bijective proof"),
            ("thm", ("The method",
                     "To prove `|A| = |B|`, construct an explicit bijection `f : A → B`. "
                     "Course 2 lesson 11's criteria apply: injective and surjective, both "
                     "argued.")),
            ("example", ("Symmetry of binomial coefficients",
                         "`C(n,k) = C(n,n−k)` via complementation: send each `k`-subset to "
                         "its complement. It is its own inverse, hence a bijection.")),
            ("example", ("Subsets and bit strings",
                         "`|P(S)| = 2ⁿ` via the indicator map: send a subset to the string "
                         "with a 1 in position `i` exactly when the `i`th element is in. "
                         "Injective because a subset is determined by its members; "
                         "surjective because every string names a subset.")),
            ("example", ("Compositions",
                         "The number of ways to write `n` as an ordered sum of positive "
                         "integers is `2ⁿ⁻¹`. Bijection: write `n` as `n` ones separated by "
                         "`n−1` gaps, and choose which gaps to cut. Each subset of gaps "
                         "gives one composition, and conversely.")),
            ("h3", "When to use which"),
            ("ul", [
                "The identity has a <strong>sum</strong> on one side: double count, "
                "classifying by whatever the summation index measures.",
                "The identity says two <strong>counts are equal</strong> with no sum: look "
                "for a bijection.",
                "The identity has <strong>alternating signs</strong>: neither directly. "
                "Look for a sign-reversing involution &mdash; a pairing that cancels most "
                "terms &mdash; or use inclusion and exclusion.",
            ]),
            ("p", "A word on rigour. A combinatorial proof is a proof, not an intuition. "
                  "The obligations are precise: for double counting, say what the objects "
                  "are and check both classifications are exhaustive and disjoint; for a "
                  "bijection, define the map and argue both directions."),
        ],
        "lab": ("pascal", {
            "identity": "hockey", "n": 6, "k": 2,
            "panel_title": "An identity with a counting proof",
            "panel_intro": "The hockey stick is proved by classifying `(k+1)`-subsets by "
                           "their largest element. The lab checks the arithmetic; the "
                           "classification is the proof.",
        }),
        "steps_title": "Constructing a combinatorial proof",
        "steps_intro": "Name the objects before anything else.",
        "steps": [
            ("Decide what each side counts",
             "Read the expressions as counts. `n·2ⁿ⁻¹` counts a choice followed by "
             "independent decisions; `Σ k·C(n,k)` counts a set and a distinguished element."),
            ("Find one set both sides could count",
             "Usually the more complicated side names it. Write the objects down "
             "explicitly."),
            ("Justify each count",
             "Say which rule you are applying and check the classification is disjoint and "
             "exhaustive."),
            ("For a bijection, define the map both ways",
             "Give `f` and give its inverse. Producing the inverse is the cleanest way to "
             "establish bijectivity."),
        ],
        "worked": {
            "title": "Prove `C(n,k)·C(k,j) = C(n,j)·C(n−j, k−j)`",
            "intro": ["Count pairs (a `k`-subset, a `j`-subset of it) two ways."],
            "lines": [
                "OBJECTS  pairs (A, B) with B ⊆ A ⊆ S, |S| = n, |A| = k, |B| = j.",
                "",
                "COUNT 1 — choose A first:",
                "   A: C(n,k) ways.   Then B ⊆ A with |B| = j:  C(k,j) ways.",
                "   Total  C(n,k)·C(k,j).",
                "",
                "COUNT 2 — choose B first:",
                "   B: C(n,j) ways.   Then the other k−j elements of A come from",
                "   the n−j elements outside B:  C(n−j, k−j) ways.",
                "   Total  C(n,j)·C(n−j, k−j).",
                "",
                "One set, two counts  ⟹  the expressions are equal.        ∎",
            ],
            "after": [
                "The algebraic proof expands four factorial expressions and cancels. It is "
                "correct and it leaves you knowing nothing. The counting proof says the "
                "identity is true because the inner set can be chosen before or after the "
                "outer one, which is a fact you can carry to the next problem."
            ],
        },
        "quiz_title": "Combinatorial proof",
        "quiz": [
            {"q": "A double-counting proof requires:",
             "a": ["two different sets",
                   "one set counted in two ways",
                   "an algebraic identity",
                   "induction"],
             "c": 1,
             "why": "One set has one size, so two correct counts of it must agree. Two "
                    "different sets would need a bijection instead."},
            {"q": "To prove `|A| = |B|` bijectively you must:",
             "a": ["show both are finite",
                   "give an explicit map and argue it is injective and surjective",
                   "count both",
                   "show `A ⊆ B`"],
             "c": 1,
             "why": "A described correspondence is not a proof until both directions are "
                    "argued. Producing the inverse map is the usual way."},
            {"q": "`Σ_v deg(v) = 2|E|` is proved by counting:",
             "a": ["vertices", "edges",
                   "incidences — pairs of a vertex and an edge meeting it",
                   "paths"],
             "c": 2,
             "why": "By vertex each contributes its degree; by edge each contributes 2. "
                    "The incidences are the set counted twice."},
        ],
        "mistakes": [
            ("Not saying what the objects are",
             "\"Both sides count the same thing\" is not a proof until the thing is named. "
             "The naming is most of the work."),
            ("A classification with a gap or an overlap",
             "The same discipline as a proof by cases. Every object in exactly one class, "
             "and say why."),
            ("Asserting a bijection without defining it",
             "\"There is an obvious correspondence\" is where errors hide. Write the map "
             "and its inverse."),
        ],
        "standard": ("Finish when you prefer the counting proof.",
                     "Prove `Σ_k C(n,k)² = C(2n,n)` by counting the `n`-subsets of a "
                     "`2n`-set split into two halves. The classification is by how many "
                     "come from the first half, and the square arises from the symmetry "
                     "`C(n,k) = C(n,n−k)`."),
        "note": "Some identities have no known combinatorial proof, which is a genuine "
                "open kind of question: finding a bijection where only algebra is known is "
                "an active research activity, because the bijection carries information the "
                "algebra does not.",
    },
    # ---------------------------------------------------------------- 14
    {
        "slug": "choosing-a-counting-method",
        "title": "Choosing a Counting Method",
        "module": "Technique",
        "one_line": "The decision procedure, and how to check the answer.",
        "summary": (
            "A summary of the course as a procedure: classify the problem, apply the "
            "rule, and verify. Most errors are classification errors, and most of them "
            "are caught by a small-case check."
        ),
        "key": [
            "1. Does ORDER matter?      2. Is REPETITION allowed?",
            "3. Are there RESTRICTIONS?    cases, complement, or inclusion–exclusion",
            "4. CHECK on a small case where enumeration is possible.",
            "A right calculation of the wrong quantity is the standard failure.",
        ],
        "key_label": "The procedure",
        "concepts_intro": (
            "The arithmetic in this course is easy. Deciding what to compute is not, and "
            "checking is what catches the difference."
        ),
        "concepts": [
            ("Classify before computing",
             "Order and repetition determine which of four formulas applies. Answering "
             "those two questions out loud prevents most errors."),
            ("Restrictions are handled by three techniques",
             "Constrain first, split into cases, or count the complement. Inclusion and "
             "exclusion is the general version of the third."),
            ("Always check a small case",
             "Shrink the parameters until enumeration is possible. A formula disagreeing "
             "with a list is wrong, whatever the reasoning looked like."),
        ],
        "read_title": "The decision procedure",
        "read_intro": "The four questions, the whole toolkit in one table, and how to verify.",
        "body": [
            ("h3", "Step 1: order and repetition"),
            ("math", [
                "                        order matters      order does not",
                "repetition forbidden      P(n, r)              C(n, r)",
                "repetition allowed         nʳ             C(n + r − 1, r)",
            ]),
            ("p", "Ask what makes two outcomes different. If rearranging the same objects "
                  "gives a new outcome, order matters. If an object can be used twice, "
                  "repetition is allowed. At `n = 5`, `r = 3` these give 60, 10, 125 and 35 "
                  "&mdash; four different answers to four different questions."),
            ("h3", "Step 2: restrictions"),
            ("ul", [
                "<strong>A constrained position:</strong> choose it first, then the rest "
                "freely.",
                "<strong>Varying counts:</strong> split into cases where the count is "
                "constant, then add.",
                "<strong>\"At least one\":</strong> count the complement.",
                "<strong>Overlapping conditions:</strong> inclusion and exclusion.",
                "<strong>Adjacency required:</strong> glue into a block, count, multiply by "
                "internal arrangements.",
                "<strong>Adjacency forbidden:</strong> arrange the others, then choose gaps.",
            ]),
            ("h3", "Step 3: the whole toolkit"),
            ("math", [
                "identical objects, distinct boxes      C(n + r − 1, r)     stars and bars",
                "distinct objects, distinct boxes       multinomial coefficient",
                "arrangements of a multiset             n!/(n₁!⋯n_k!)",
                "circular arrangements                  (n−1)!",
                "no fixed points                        Dₙ",
                "at least one of several properties     inclusion–exclusion",
                "answer needed for every n              generating function",
                "an identity to prove                   double count or biject",
                "existence rather than a count          pigeonhole",
            ]),
            ("h3", "Step 4: verification"),
            ("ul", [
                "<strong>Shrink and enumerate.</strong> Set `n = 3`, `r = 2` and list. The "
                "lab does this up to 400 objects.",
                "<strong>Count a second way.</strong> Cases and complement should agree. "
                "Two routes to one number is the strongest cheap check available.",
                "<strong>Check the magnitude.</strong> The answer cannot exceed the "
                "unrestricted count or fall below zero.",
                "<strong>Check the extremes.</strong> Does the formula give the right "
                "answer at `r = 0` and `r = n`? Those are where off-by-one errors surface.",
            ]),
            ("p", "The habit worth taking from this course is the last one. A formula "
                  "checked at its boundaries and against one small enumeration is very "
                  "unlikely to be the right calculation of the wrong quantity, which is "
                  "the failure this whole procedure exists to prevent."),
        ],
        "lab": ("counting", {
            "n": 5, "r": 3, "rule": "c",
            "panel_title": "All four, side by side",
            "panel_intro": "At `n = 5`, `r = 3` the four rules give 125, 60, 10 and 35. "
                           "The classification decides which is your answer, and the "
                           "enumeration shows why they differ.",
        }),
        "steps_title": "The procedure",
        "steps_intro": "Four questions, in order, before any arithmetic.",
        "steps": [
            ("Does order matter?",
             "Ask what makes two outcomes different. Committees and hands: no. Podiums and "
             "passwords: yes."),
            ("Is repetition allowed?",
             "Can an object be used twice? Drawing with replacement, yes; without, no."),
            ("What are the restrictions, and which technique fits?",
             "Constrain first, split into cases, complement, or inclusion and exclusion."),
            ("Verify",
             "A small enumeration, a second method, and the boundary values. Three cheap "
             "checks that between them catch nearly everything."),
        ],
        "worked": {
            "title": "One problem, fully classified",
            "intro": ["How many 5-letter strings over `{a,…,z}` have no repeated letter "
                      "and at least one vowel?"],
            "lines": [
                "1. ORDER?       yes — strings",
                "2. REPETITION?  no — \"no repeated letter\"",
                "   ⟹ base rule is P(26, 5)",
                "3. RESTRICTION? \"at least one vowel\"  ⟹ complement",
                "",
                "   all:        P(26,5) = 26·25·24·23·22 = 7 893 600",
                "   no vowel:   P(21,5) = 21·20·19·18·17 =  2 441 880",
                "   answer:     7 893 600 − 2 441 880    =  5 451 720",
                "",
                "4. CHECK",
                "   magnitude:  5 451 720 < 7 893 600                    ✓",
                "   proportion: 1 − 2441880/7893600 ≈ 0.691 — plausible,",
                "               since 5 of 26 letters are vowels and there are",
                "               5 chances to hit one                      ✓",
                "   small case: length 2 from {a,b,c,d} with vowel a:",
                "               P(4,2) − P(3,2) = 12 − 6 = 6,",
                "               and listing gives ab,ba,ac,ca,ad,da       ✓",
            ],
            "after": [
                "The small-case check is the one that would catch a misclassification. "
                "Enumerating six strings takes ten seconds and confirms that the formula "
                "counts what was intended, which no amount of re-reading the arithmetic can."
            ],
        },
        "quiz_title": "Choosing a method",
        "quiz": [
            {"q": "Distributing 10 identical balls into 4 distinct boxes uses:",
             "a": ["`P(10,4)`", "`C(10,4)`", "`C(13,10)` — stars and bars", "`4¹⁰`"],
             "c": 2,
             "why": "Identical items into distinct types, repetition allowed and order "
                    "irrelevant: `C(n + r − 1, r) = C(13, 10) = 286`."},
            {"q": "The most common error in this course is:",
             "a": ["arithmetic slips",
                   "a correct calculation of the wrong quantity",
                   "using a calculator",
                   "factorials being too large"],
             "c": 1,
             "why": "Misclassifying order or repetition produces a fluent, confident and "
                    "wrong answer. That is why the classification is stated first and the "
                    "answer is checked on a small case."},
            {"q": "The single most useful check is:",
             "a": ["re-reading the arithmetic",
                   "enumerating a small instance and comparing",
                   "checking the answer is even",
                   "using a bigger example"],
             "c": 1,
             "why": "A list is ground truth. It catches classification errors, which "
                    "rechecking the arithmetic never will."},
        ],
        "mistakes": [
            ("Computing before classifying",
             "The formula is the last step, not the first. Two sentences of classification "
             "prevent most wrong answers."),
            ("Skipping the check because the reasoning felt sound",
             "Wrong classifications feel exactly as sound as right ones. That is what "
             "makes them dangerous and what makes the check worth doing."),
            ("Ignoring the boundaries",
             "`r = 0` and `r = n` are where off-by-one errors show. Both take a second to "
             "evaluate."),
        ],
        "standard": ("Finish when classification precedes computation automatically.",
                     "Take any five counting problems, write the classification for each "
                     "before computing anything, and then verify one of them two ways. That "
                     "sequence &mdash; classify, compute, check &mdash; is the whole course."),
        "note": "Course 5 turns these counts into probabilities by dividing by the size of "
                "the sample space, so every classification error here becomes a wrong "
                "probability there. The counting is the hard part; the division is not.",
    },
]
