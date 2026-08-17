"""Course 8, lessons 07-12 — recursion, design techniques, and limits."""

LESSONS = [
    # ---------------------------------------------------------------- 07
    {
        "slug": "divide-and-conquer",
        "title": "Divide and Conquer",
        "module": "Design",
        "one_line": "Split, solve the pieces, combine — and the theorem that costs it.",
        "summary": (
            "Divide-and-conquer produces recurrences of one shape, `T(n) = aT(n/b) + f(n)`, "
            "solved by the master theorem. The technique's power comes from reducing `a`, "
            "not from combining faster."
        ),
        "key": [
            "T(n) = a·T(n/b) + nᵈ",
            "log_b a < d   ⟹  Θ(nᵈ)              the combining dominates",
            "log_b a = d   ⟹  Θ(nᵈ log n)        every level equal",
            "log_b a > d   ⟹  Θ(n^{log_b a})     the leaves dominate",
        ],
        "key_label": "One comparison decides",
        "concepts_intro": (
            "Course 3 lesson 11 solved these recurrences; this lesson uses them to "
            "compare algorithm designs."
        ),
        "concepts": [
            ("The three cases are which level dominates",
             "Work per level either grows, shrinks or stays constant down the recursion "
             "tree, and `log_b a` against `d` is exactly that comparison."),
            ("Reducing `a` changes the exponent",
             "Karatsuba's improvement is three multiplications instead of four, and "
             "`log₂3 &lt; log₂4`. Faster combining cannot do that."),
            ("Not every split is even",
             "Quicksort's split depends on the pivot, so it has no fixed `b` &mdash; and "
             "its worst case is quadratic while its average is `n log n`."),
        ],
        "read_title": "Divide and conquer",
        "read_intro": "The pattern, the master theorem, and four algorithms compared.",
        "body": [
            ("p", "A divide-and-conquer algorithm splits an input of size `n` into `a` "
                  "subproblems of size `n/b`, solves each recursively, and spends `f(n)` "
                  "dividing and combining. The running time therefore satisfies "
                  "`T(n) = aT(n/b) + f(n)`."),
            ("thm", ("Master theorem",
                     "For `T(n) = aT(n/b) + Θ(nᵈ)` with `a ≥ 1`, `b &gt; 1`, `d ≥ 0`: "
                     "`T(n) = Θ(nᵈ)` if `log_b a &lt; d`; `Θ(nᵈ log n)` if `log_b a = d`; "
                     "and `Θ(n^{log_b a})` if `log_b a &gt; d`.")),
            ("p", "The three cases are the recursion tree's shape. Level `i` holds `aⁱ` "
                  "subproblems of size `n/bⁱ`, doing `nᵈ(a/bᵈ)ⁱ` work in total &mdash; a "
                  "geometric series whose ratio `a/bᵈ` is below, equal to, or above 1 "
                  "exactly as `log_b a` is below, equal to, or above `d`."),
            ("math", [
                "algorithm                     a   b   d    log_b a    result",
                "binary search                 1   2   0     0.000     Θ(log n)",
                "merge sort                    2   2   1     1.000     Θ(n log n)",
                "Karatsuba multiplication      3   2   1     1.585     Θ(n^1.585)",
                "naive matrix multiplication   8   2   2     3.000     Θ(n³)",
                "Strassen                      7   2   2     2.807     Θ(n^2.807)",
                "closest pair of points        2   2   1     1.000     Θ(n log n)",
            ]),
            ("h3", "Where the improvements come from"),
            ("p", "Karatsuba multiplies two `n`-digit numbers by splitting each in half. "
                  "The obvious method needs four half-size products, giving "
                  "`T(n) = 4T(n/2) + n = Θ(n²)` &mdash; no better than schoolbook "
                  "multiplication. Karatsuba's identity computes the same result with three "
                  "products, and `log₂ 3 ≈ 1.585 &lt; 2`."),
            ("math", [
                "(a·10^m + b)(c·10^m + d)",
                "   = ac·10^{2m} + (ad + bc)·10^m + bd",
                "",
                "ad + bc  =  (a + b)(c + d) − ac − bd        ← one product, not two",
                "",
                "so three products suffice:  ac,  bd,  (a+b)(c+d)",
            ]),
            ("p", "Strassen does the same for matrices: seven products of half-size blocks "
                  "instead of eight, giving `Θ(n^{2.807})`. In both cases the gain came "
                  "from reducing `a`, and no amount of faster combining could have produced "
                  "it &mdash; `d` only matters when it exceeds `log_b a`."),
            ("h3", "When the split is uneven"),
            ("p", "Quicksort partitions around a pivot, and the split depends on the data. "
                  "A perfect pivot gives `T(n) = 2T(n/2) + n = Θ(n log n)`; the worst pivot "
                  "gives `T(n) = T(n−1) + n = Θ(n²)`. The master theorem does not apply to "
                  "the second, which has no fixed `b` at all."),
            ("p", "Remarkably, even a badly unbalanced but constant split is fine: "
                  "`T(n) = T(n/10) + T(9n/10) + n` is still `Θ(n log n)`, because the "
                  "recursion tree still has logarithmic depth. Quicksort survives imperfect "
                  "pivots for exactly this reason, and fails only on consistently extreme "
                  "ones."),
        ],
        "lab": ("algorithm", {
            "mode": "master",
            "panel_title": "The cases, tabulated",
            "panel_intro": "Each row computes `log_b a` and compares it with `d`. Note that "
                           "Karatsuba and Strassen both improve by lowering `a`, and both "
                           "keep the same `d`.",
        }),
        "steps_title": "Analysing a divide-and-conquer algorithm",
        "steps_intro": "Read off `a`, `b`, `d`; compare.",
        "steps": [
            ("Count the recursive calls: that is `a`",
             "How many subproblems, not how much smaller they are."),
            ("Find the shrink factor: that is `b`",
             "Halving gives `b = 2`. If the factor varies with the data, the theorem does "
             "not apply."),
            ("Find the combining cost: that is `nᵈ`",
             "Merging costs `Θ(n)` so `d = 1`; a constant combine gives `d = 0`."),
            ("Compare `log_b a` with `d`",
             "Less, equal or greater. That single comparison gives the answer, and the "
             "recursion tree explains why."),
        ],
        "worked": {
            "title": "Improving an algorithm two ways",
            "intro": ["Start from `T(n) = 4T(n/2) + n`, which is `Θ(n²)`."],
            "lines": [
                "BASELINE   a=4  b=2  d=1   log₂4 = 2 > 1   ⟹  Θ(n²)",
                "",
                "Attempt 1: make the combining faster, d = 1 → d = 0",
                "   a=4  b=2  d=0   log₂4 = 2 > 0   ⟹  still Θ(n²)",
                "   NO IMPROVEMENT — the leaves already dominated.",
                "",
                "Attempt 2: use one fewer subproblem, a = 4 → a = 3",
                "   a=3  b=2  d=1   log₂3 ≈ 1.585 > 1   ⟹  Θ(n^1.585)",
                "   A GENUINE IMPROVEMENT.",
                "",
                "In case 3 the cost is all at the leaves, and only a affects them.",
            ],
            "after": [
                "This is the structural reason Karatsuba and Strassen both take the form "
                "they do. In the leaf-dominated case the combining work is irrelevant, so "
                "the only route to a better exponent is fewer subproblems &mdash; and "
                "finding an identity that removes one is the hard creative step."
            ],
        },
        "quiz_title": "Divide and conquer",
        "quiz": [
            {"q": "`T(n) = 2T(n/2) + n` solves to:",
             "a": ["`Θ(n)`", "`Θ(n log n)`", "`Θ(n²)`", "`Θ(log n)`"],
             "c": 1,
             "why": "`log₂2 = 1 = d`, the balanced case: every level does `Θ(n)` work and "
                    "there are `log n` levels."},
            {"q": "Karatsuba beats the naive method because it:",
             "a": ["combines faster", "uses 3 subproblems instead of 4",
                   "splits into thirds", "uses less memory"],
             "c": 1,
             "why": "`log₂3 ≈ 1.585` against `log₂4 = 2`. The combining cost is `Θ(n)` in "
                    "both."},
            {"q": "The master theorem does not apply to quicksort's worst case because:",
             "a": ["quicksort is not recursive",
                   "the split depends on the data, so there is no fixed `b`",
                   "the combining is too slow",
                   "it is randomised"],
             "c": 1,
             "why": "`T(n) = T(n−1) + n` is not of the form `aT(n/b) + f(n)`. Its solution "
                    "is `Θ(n²)`, found by unrolling."},
        ],
        "mistakes": [
            ("Swapping `a` and `b`",
             "`a` counts subproblems and `b` is the shrink factor. `T(n) = 3T(n/2)` has "
             "`a = 3`, `b = 2`, and reversing them gives the wrong case."),
            ("Optimising the combining step in case 3",
             "When the leaves dominate, `d` is irrelevant. Effort must go into reducing "
             "`a`."),
            ("Applying the theorem to an uneven split",
             "It needs a fixed `b`. Data-dependent splits are analysed by unrolling or by "
             "the recursion tree."),
        ],
        "standard": ("Finish when you can say which parameter to attack.",
                     "For `T(n) = 9T(n/3) + n²`, identify the case and say whether faster "
                     "combining or fewer subproblems would help. `log₃9 = 2 = d`, the "
                     "balanced case, where both would."),
        "note": "The master theorem as stated covers `f(n) = Θ(nᵈ)`. The full version "
                "handles forcing terms between the cases &mdash; `n log n`, for instance "
                "&mdash; and needs a regularity condition. The polynomial version covers "
                "almost every algorithm you will meet.",
    },
    # ---------------------------------------------------------------- 08
    {
        "slug": "recursion-trees-and-amortised-analysis",
        "title": "Recursion Trees and Amortised Analysis",
        "module": "Design",
        "one_line": "When the master theorem does not apply, and when the worst case is misleading.",
        "summary": (
            "A recursion tree solves recurrences the master theorem cannot. Amortised "
            "analysis answers a different question: what a sequence of operations costs "
            "on average, when one of them is occasionally expensive."
        ),
        "key": [
            "recursion tree: sum the work level by level",
            "amortised cost = total cost of a sequence / number of operations",
            "a doubling array: worst case Θ(n) per insert, amortised Θ(1)",
            "amortised is a GUARANTEE, not an average over random inputs",
        ],
        "key_label": "Two techniques",
        "concepts_intro": (
            "One technique for recurrences the theorem misses, and one for the case where "
            "the worst case is a bad summary."
        ),
        "concepts": [
            ("A recursion tree is the master theorem's proof, drawn",
             "Sum the work at each level and add up the levels. It applies to uneven "
             "splits, where the theorem does not."),
            ("Amortised analysis bounds a sequence",
             "Not a single operation. Occasional expensive operations are paid for by many "
             "cheap ones."),
            ("Amortised is not average-case",
             "It is a worst-case guarantee over any sequence, with no probability. Averaging "
             "over random inputs is a different claim."),
        ],
        "read_title": "Two techniques",
        "read_intro": "Recursion trees for awkward recurrences, amortisation for uneven costs.",
        "body": [
            ("h3", "Recursion trees"),
            ("p", "Draw the recursion as a tree: the root does the top-level combining "
                  "work, its children are the subproblems, and so on to the base cases. "
                  "The total cost is the sum of the work at every node, which is best "
                  "computed level by level."),
            ("example", ("An uneven split",
                         "`T(n) = T(n/3) + T(2n/3) + n`. Each level does `n` units of "
                         "combining work, because the subproblem sizes at each level still "
                         "sum to `n`. The deepest branch shrinks by `2/3` each time, so the "
                         "depth is `log_{3/2} n`. Total: `Θ(n log n)` &mdash; the same as an "
                         "even split.")),
            ("p", "That is why quicksort survives an imperfect pivot. Any constant-fraction "
                  "split gives logarithmic depth, and only a consistently extreme pivot "
                  "&mdash; splitting off one element at a time &mdash; produces the "
                  "quadratic worst case."),
            ("example", ("A tree with unequal levels",
                         "`T(n) = 2T(n/2) + n²`. Level `i` has `2ⁱ` subproblems of size "
                         "`n/2ⁱ`, doing `2ⁱ(n/2ⁱ)² = n²/2ⁱ` work. The total is "
                         "`n² Σ 1/2ⁱ &lt; 2n²`, so `T(n) = Θ(n²)`: the root dominates, and "
                         "the master theorem agrees since `log₂2 = 1 &lt; 2 = d`.")),
            ("h3", "Amortised analysis"),
            ("def", ("Amortised cost",
                     "The <strong>amortised cost</strong> of an operation is the total cost "
                     "of a worst-case sequence of `m` operations, divided by `m`. It is a "
                     "guarantee about sequences, not about any single operation.")),
            ("thm", ("The doubling array",
                     "A dynamic array that doubles its capacity when full, copying all "
                     "elements, supports insertion in `Θ(1)` amortised time, even though a "
                     "single insertion can cost `Θ(n)`.")),
            ("proof", [
                "Consider `n` insertions starting from capacity 1. The copies happen when "
                "the size reaches `1, 2, 4, 8, …`, costing `1 + 2 + 4 + ⋯ + 2^{⌊log₂ n⌋} "
                "&lt; 2n` element moves in total.",
                "Adding the `n` insertions themselves, the total is under `3n`, so the "
                "amortised cost per insertion is under 3 &mdash; a constant.",
            ]),
            ("p", "The geometric series is doing the work: the expensive operations are "
                  "rare and their cost grows exactly as fast as the gaps between them, so "
                  "the total telescopes. Course 3 lesson 3's geometric sum is the "
                  "calculation."),
            ("p", "Doubling is essential. Growing by a fixed amount `c` instead means "
                  "copies at sizes `c, 2c, 3c, …`, totalling `Θ(n²)` moves &mdash; an "
                  "amortised cost of `Θ(n)` per insertion. The two policies differ by a "
                  "whole class."),
            ("h3", "The three methods"),
            ("math", [
                "AGGREGATE     total cost of m operations, divided by m",
                "ACCOUNTING    charge each cheap operation extra; save the credit",
                "              to pay for the rare expensive one",
                "POTENTIAL     define a potential function Φ on the data structure;",
                "              amortised cost = actual cost + ΔΦ",
            ]),
            ("p", "The accounting method applied to the doubling array: charge 3 units per "
                  "insertion &mdash; one to insert, one saved to copy this element later, "
                  "one saved to copy an older element. When the array doubles, every "
                  "element has exactly the credit needed for its move."),
            ("p", "<strong>Amortised is not average-case.</strong> Average-case analysis "
                  "assumes a distribution over inputs and computes an expectation. "
                  "Amortised analysis assumes nothing and bounds the total for any "
                  "sequence, which is a strictly stronger guarantee."),
        ],
        "lab": ("algorithm", {
            "mode": "growth", "n": 32,
            "panel_title": "Where the cost accumulates",
            "panel_intro": "Compare `n` with `n log n` on the log scale. The doubling "
                           "array's copies sum to less than `2n`, which is why they "
                           "disappear into the linear term.",
        }),
        "steps_title": "Using each technique",
        "steps_intro": "Tree for a recurrence, amortisation for a sequence.",
        "steps": [
            ("Draw the tree when the master theorem does not apply",
             "Uneven splits, varying subproblem sizes, or a forcing term between the cases."),
            ("Sum the work level by level",
             "Then sum over levels. The depth is set by the branch that shrinks slowest."),
            ("For amortisation, bound the total over a sequence",
             "Not the worst single operation. A geometric series usually appears."),
            ("Say which guarantee you have",
             "Amortised bounds hold for any sequence; average-case bounds need a "
             "distribution. They are different claims."),
        ],
        "worked": {
            "title": "The doubling array, counted",
            "intro": ["Inserting 16 elements, starting from capacity 1."],
            "lines": [
                "insert  1   capacity 1→1     copies 0",
                "insert  2   capacity 1→2     copies 1",
                "insert  3   capacity 2→4     copies 2",
                "insert  5   capacity 4→8     copies 4",
                "insert  9   capacity 8→16    copies 8",
                "inserts 10–16                copies 0",
                "",
                "total copies = 1 + 2 + 4 + 8 = 15  <  16 = n",
                "total cost   = 16 inserts + 15 copies = 31  <  2n",
                "",
                "amortised cost per insertion  <  2",
                "worst single insertion        = 9 (the resize at element 9)",
                "",
                "GROWING BY 1 INSTEAD:  copies = 1+2+…+15 = 120 = Θ(n²)",
                "                       amortised cost per insertion = Θ(n)",
            ],
            "after": [
                "The last two lines are the point. Doubling and incrementing look like "
                "minor implementation choices and differ by a whole complexity class. Every "
                "dynamic array in every standard library doubles for this reason."
            ],
        },
        "quiz_title": "Trees and amortisation",
        "quiz": [
            {"q": "`T(n) = T(n/3) + T(2n/3) + n` solves to:",
             "a": ["`Θ(n)`", "`Θ(n log n)`", "`Θ(n²)`", "the master theorem gives it directly"],
             "c": 1,
             "why": "Each level does `Θ(n)` work and the depth is logarithmic. The master "
                    "theorem does not apply because the split is uneven."},
            {"q": "Amortised `Θ(1)` insertion means:",
             "a": ["every insertion costs `Θ(1)`",
                   "any sequence of `m` insertions costs `Θ(m)` in total",
                   "insertions are `Θ(1)` on average over random inputs",
                   "the worst case is `Θ(1)`"],
             "c": 1,
             "why": "A guarantee about sequences. A single insertion can cost `Θ(n)` when a "
                    "resize happens."},
            {"q": "Growing an array by a fixed amount rather than doubling gives amortised:",
             "a": ["`Θ(1)`", "`Θ(log n)`", "`Θ(n)`", "the same as doubling"],
             "c": 2,
             "why": "Copies at sizes `c, 2c, 3c, …` total `Θ(n²)`, so `Θ(n)` per "
                    "insertion. The geometric series is what makes doubling work."},
        ],
        "mistakes": [
            ("Confusing amortised with average-case",
             "Amortised holds for every sequence with no probabilistic assumption. It is "
             "the stronger guarantee."),
            ("Summing a recursion tree by branch instead of by level",
             "Level by level is what makes the sums tractable, because the sizes at each "
             "level usually add to something simple."),
            ("Assuming any growth policy gives amortised constant time",
             "Only geometric growth does. Fixed increments give `Θ(n)` amortised."),
        ],
        "standard": ("Finish when you can produce the geometric series yourself.",
                     "Show that a dynamic array growing by a factor of 1.5 still has "
                     "amortised `Θ(1)` insertion, and identify the ratio of the series. Any "
                     "constant factor above 1 works, and that is the theorem."),
        "note": "Amortised analysis was named by Tarjan and is what makes union&ndash;find, "
                "Fibonacci heaps and dynamic arrays practical. In each case a single "
                "operation can be slow and no sequence can be, which is the guarantee that "
                "actually matters.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "greedy-algorithms",
        "title": "Greedy Algorithms",
        "module": "Design",
        "one_line": "Take the best local choice — and prove it was safe.",
        "summary": (
            "A greedy algorithm never reconsiders. Sometimes that is provably optimal "
            "&mdash; minimum spanning trees, interval scheduling, Huffman codes &mdash; "
            "and usually it is not, so the proof is the whole content."
        ),
        "key": [
            "greedy: make the locally best choice, never revisit",
            "correct when a GREEDY CHOICE PROPERTY holds",
            "exchange argument: any optimum can be modified toward the greedy choice",
            "coins {1,3,4}: greedy fails at 6  (4+1+1 vs 3+3)",
        ],
        "key_label": "Fast, and usually wrong",
        "concepts_intro": (
            "Greedy algorithms are easy to write and hard to justify, and the "
            "justification is what separates a method from a heuristic."
        ),
        "concepts": [
            ("Greed is a design pattern, not a guarantee",
             "It produces an answer quickly. Whether that answer is optimal is a separate "
             "theorem about the specific problem."),
            ("The exchange argument is the standard proof",
             "Take any optimal solution and show it can be modified to agree with the "
             "greedy choice without getting worse."),
            ("Failure is common and often silent",
             "Coin change with `{1,3,4}` fails at 6. Nothing in the algorithm signals it, "
             "which is why the proof matters."),
        ],
        "read_title": "Greedy algorithms",
        "read_intro": "Three where it works, one where it fails, and the proof technique.",
        "body": [
            ("h3", "Interval scheduling"),
            ("p", "Given intervals with start and finish times, select as many "
                  "non-overlapping ones as possible. The greedy rule is: repeatedly take "
                  "the interval that finishes earliest among those compatible with what is "
                  "already chosen."),
            ("thm", ("Earliest finish time is optimal",
                     "The greedy algorithm selects a maximum-size set of pairwise "
                     "compatible intervals.")),
            ("proof", [
                "Let `g₁, g₂, …` be the greedy selection in order and `o₁, o₂, …` an "
                "optimal one, both sorted by finish time. We show by induction that `gᵢ` "
                "finishes no later than `oᵢ`.",
                "For `i = 1`, greedy chose the earliest-finishing interval overall. For the "
                "step, if `gᵢ` finishes no later than `oᵢ`, then `o_{i+1}` is available to "
                "greedy at step `i+1`, so `g_{i+1}` finishes no later.",
                "If the optimum had more intervals than greedy, its next interval would be "
                "compatible with everything greedy chose, so greedy would not have stopped. "
                "Hence the sizes are equal.",
            ]),
            ("p", "Other plausible rules fail. Shortest interval first fails on a short "
                  "interval overlapping two long disjoint ones. Earliest start first fails "
                  "on one very long interval that begins first. Only earliest finish is "
                  "optimal, and the difference is not visible without the proof."),
            ("h3", "Where greedy fails"),
            ("example", ("Coin change",
                         "With `{1, 5, 10, 25}` the greedy rule &mdash; largest coin first "
                         "&mdash; is optimal for every amount. With `{1, 3, 4}` it fails at "
                         "6: greedy gives `4 + 1 + 1` (three coins) while `3 + 3` uses two. "
                         "\"Greedy works for coin change\" is a property of the coin system, "
                         "not of the strategy.")),
            ("example", ("The travelling salesman",
                         "Nearest-neighbour tour construction can be arbitrarily bad: "
                         "instances exist where it exceeds the optimum by any factor you "
                         "like. Greedy gives a tour quickly and offers no guarantee at all.")),
            ("h3", "The exchange argument"),
            ("p", "The standard proof technique has three steps. Assume an optimal solution "
                  "differing from the greedy one. Find the first place they differ. Show the "
                  "optimum can be modified to agree with greedy there without becoming "
                  "worse. Repeating turns the optimum into the greedy solution, so greedy is "
                  "optimal too."),
            ("p", "This is exactly the argument used for the cut property in course 7 "
                  "lesson 12: swapping the heavier edge for the lighter one in a minimum "
                  "spanning tree does not increase the total. The technique is the same "
                  "wherever greedy is correct."),
            ("h3", "Huffman coding"),
            ("thm", ("Huffman codes are optimal",
                     "Repeatedly merging the two least frequent symbols into a combined "
                     "node produces a prefix-free binary code of minimum expected length.")),
            ("p", "The greedy choice is merging the two rarest symbols, and the exchange "
                  "argument shows an optimal tree can always be modified to place them as "
                  "siblings at the deepest level. It is the compression method behind "
                  "several standard formats, and its optimality is a genuine theorem rather "
                  "than an observation."),
        ],
        "lab": ("algorithm", {
            "mode": "greedy", "n": 20,
            "panel_title": "Greedy against optimal",
            "panel_intro": "Both are computed for every amount: greedy takes the largest "
                           "coin, dynamic programming solves it exactly. With `{1,3,4}` "
                           "they part company at 6.",
        }),
        "steps_title": "Designing a greedy algorithm",
        "steps_intro": "Write it, then prove it, then test it.",
        "steps": [
            ("Identify the greedy choice",
             "The locally best option: earliest finish, lightest edge, largest coin, "
             "rarest symbol."),
            ("Attempt an exchange argument",
             "Can any optimal solution be modified to include the greedy choice without "
             "getting worse? If yes, greedy is optimal."),
            ("If the proof fails, look for a counterexample",
             "Small instances usually reveal it. Coin change fails at 6 with a three-coin "
             "system."),
            ("Say what you have",
             "\"Optimal, by exchange argument\" or \"a heuristic with no guarantee\". "
             "Both are legitimate; conflating them is not."),
        ],
        "worked": {
            "title": "Two greedy rules for interval scheduling",
            "intro": ["Intervals `A(0,10)`, `B(1,3)`, `C(4,6)`, `D(7,9)`."],
            "lines": [
                "EARLIEST START FIRST",
                "   A (0,10) chosen first — it blocks everything else",
                "   result: {A},  1 interval",
                "",
                "SHORTEST FIRST",
                "   B (1,3) length 2, C (4,6) length 2, D (7,9) length 2, A length 10",
                "   result: {B, C, D},  3 intervals    — optimal here, by luck",
                "",
                "EARLIEST FINISH FIRST",
                "   B finishes at 3, then C at 6, then D at 9",
                "   result: {B, C, D},  3 intervals    — optimal, PROVABLY",
                "",
                "Shortest-first fails elsewhere: intervals (0,5), (4,6), (5,10)",
                "   shortest first takes (4,6) and blocks both others → 1",
                "   earliest finish takes (0,5) then (5,10)           → 2",
            ],
            "after": [
                "Three rules, all plausible, and only one is optimal in general. The second "
                "happened to work on the first instance and fails on the second, which is "
                "exactly why a counterexample search is not a substitute for a proof."
            ],
        },
        "quiz_title": "Greedy",
        "quiz": [
            {"q": "Greedy coin change with `{1, 3, 4}` first fails at:",
             "a": ["3", "4", "6", "it never fails"],
             "c": 2,
             "why": "Greedy gives `4 + 1 + 1` (three coins); the optimum is `3 + 3` (two). "
                    "The same rule is optimal for `{1,5,10,25}`."},
            {"q": "The standard technique for proving a greedy algorithm optimal is:",
             "a": ["induction on the input size",
                   "an exchange argument",
                   "contradiction",
                   "testing many inputs"],
             "c": 1,
             "why": "Show any optimal solution can be modified toward the greedy choice "
                    "without getting worse. It is what proves the cut property too."},
            {"q": "For interval scheduling, the optimal greedy rule is:",
             "a": ["earliest start", "shortest interval",
                   "earliest finish", "fewest conflicts"],
             "c": 2,
             "why": "Earliest finish leaves the most room for what follows, and the "
                    "exchange argument proves it. The others all have counterexamples."},
        ],
        "mistakes": [
            ("Assuming greedy is optimal because it seems reasonable",
             "Three plausible rules for interval scheduling, one correct. The proof is the "
             "only way to tell."),
            ("Testing instead of proving",
             "Shortest-first passes the first example and fails the second. Course 1 lesson "
             "14's point applies unchanged."),
            ("Not saying which you have",
             "\"Optimal by exchange argument\" and \"a heuristic\" are both respectable. "
             "Presenting the second as the first is not."),
        ],
        "standard": ("Finish when you attempt the exchange argument before trusting a "
                     "greedy rule.",
                     "For the fractional knapsack problem &mdash; items may be split "
                     "&mdash; show that taking items in decreasing value-per-weight order "
                     "is optimal. Then observe that the 0/1 version, where items cannot be "
                     "split, defeats the same rule, and lesson 10 handles it."),
        "note": "The structure making greed provably correct is a matroid, and the "
                "forests of a graph form one &mdash; which is why Kruskal's algorithm "
                "works. Most problems have no such structure, and dynamic programming is "
                "the usual alternative.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "dynamic-programming",
        "title": "Dynamic Programming",
        "module": "Design",
        "one_line": "Solve every subproblem once, and reuse the answers.",
        "summary": (
            "When subproblems overlap, recomputing them is exponentially wasteful. "
            "Storing each answer turns an exponential recursion into a polynomial one, "
            "and the technique applies exactly when the problem has optimal substructure."
        ),
        "key": [
            "OPTIMAL SUBSTRUCTURE  an optimal solution contains optimal sub-solutions",
            "OVERLAPPING SUBPROBLEMS  the same subproblem recurs",
            "memoise (top down) or fill a table (bottom up)",
            "naive Fibonacci: ~1.6ⁿ calls.  With memoisation: n.",
        ],
        "key_label": "Two conditions, one technique",
        "concepts_intro": (
            "Both conditions are needed. Optimal substructure without overlap is "
            "divide-and-conquer; overlap without optimal substructure is not helped."
        ),
        "concepts": [
            ("Overlap is what makes memoisation pay",
             "Merge sort's subproblems are disjoint, so caching them saves nothing. "
             "Fibonacci's recur constantly."),
            ("Optimal substructure is what makes the recurrence valid",
             "The best solution must be assemblable from best sub-solutions. Longest "
             "<em>simple</em> path fails this, and no dynamic program for it exists."),
            ("Top-down and bottom-up are the same computation",
             "Memoised recursion computes only the subproblems it needs; a table computes "
             "all of them in dependency order. The complexity is the same."),
        ],
        "read_title": "Dynamic programming",
        "read_intro": "The two conditions, three worked examples, and the problem it cannot help.",
        "body": [
            ("h3", "The motivating case"),
            ("p", "The naive recursive Fibonacci makes about `1.6ⁿ` calls because it "
                  "recomputes the same values exponentially often: `F(5)` calls `F(3)` "
                  "twice, `F(2)` three times, and so on. Storing each value when first "
                  "computed reduces the count to `n`."),
            ("math", [
                "n        naive calls        memoised calls",
                "10               177                    10",
                "30           2 692 537                  30",
                "50    ~ 40 000 000 000                  50",
            ]),
            ("def", ("The two conditions",
                     "<strong>Optimal substructure</strong>: an optimal solution is built "
                     "from optimal solutions to subproblems. <strong>Overlapping "
                     "subproblems</strong>: the recursion revisits the same subproblems "
                     "many times.")),
            ("p", "Both are required. Merge sort has optimal substructure and no overlap, "
                  "so it is divide-and-conquer and memoisation would help nothing. A "
                  "problem with overlap and no optimal substructure cannot be solved by "
                  "combining sub-solutions at all."),
            ("h3", "Coin change"),
            ("math", [
                "best[0] = 0",
                "best[v] = 1 + min{ best[v − c] : c a coin, c ≤ v }",
                "",
                "coins {1,3,4}, target 6:",
                "   best[1]=1  best[2]=2  best[3]=1  best[4]=1  best[5]=2  best[6]=2",
                "   best[6] = 1 + min(best[5], best[3], best[2]) = 1 + 1 = 2",
                "   the two coins are 3 + 3 — which greedy missed",
            ]),
            ("p", "The recurrence is the optimal substructure written down: the best way to "
                  "make `v` uses some coin `c`, and the rest must be the best way to make "
                  "`v − c`. Filling the table costs `Θ(v · |coins|)`, and the greedy failure "
                  "of lesson 9 disappears."),
            ("h3", "Longest common subsequence"),
            ("math", [
                "L[i][j] = length of the longest common subsequence of the first i",
                "          characters of X and the first j of Y",
                "",
                "L[i][j] = 0                              if i = 0 or j = 0",
                "        = L[i−1][j−1] + 1                if X[i] = Y[j]",
                "        = max(L[i−1][j], L[i][j−1])      otherwise",
            ]),
            ("p", "Cost `Θ(mn)`, against exponential for the naive recursion. This is the "
                  "algorithm behind `diff`, behind version-control merges, and behind "
                  "sequence alignment in bioinformatics."),
            ("h3", "Where it does not apply"),
            ("example", ("Longest simple path",
                         "Finding the longest path with no repeated vertex has no optimal "
                         "substructure: the longest path from `a` to `c` need not consist of "
                         "the longest path from `a` to `b` plus the longest from `b` to `c`, "
                         "because those may share vertices and the concatenation would not "
                         "be simple. The problem is NP-hard, and no dynamic program for it "
                         "exists.")),
            ("p", "Contrast with the SHORTEST path, which does have optimal substructure "
                  "&mdash; any subpath of a shortest path is shortest &mdash; and is "
                  "solved in polynomial time by course 7's Dijkstra. Two problems whose "
                  "statements differ by one word, on opposite sides of tractability."),
            ("h3", "Top-down or bottom-up"),
            ("math", [
                "MEMOISED (top down)      recursion + a cache",
                "                         computes only the subproblems needed",
                "                         natural to write from the recurrence",
                "",
                "TABULATED (bottom up)    fill a table in dependency order",
                "                         no recursion overhead",
                "                         often allows the space to be reduced",
            ]),
            ("p", "The two have the same asymptotic cost. Bottom-up often permits dropping "
                  "old rows of the table &mdash; the Fibonacci table needs only the last "
                  "two entries &mdash; which is why it is preferred when memory matters."),
        ],
        "lab": ("algorithm", {
            "mode": "greedy", "n": 24,
            "panel_title": "Dynamic programming against greed",
            "panel_intro": "The optimal columns are computed by the coin-change recurrence "
                           "above, filling the table from 1 upward. Where greedy differs, "
                           "the table is right.",
        }),
        "steps_title": "Designing a dynamic program",
        "steps_intro": "Recurrence first; the implementation follows.",
        "steps": [
            ("Define the subproblem precisely",
             "\"The fewest coins making value `v`\", \"the LCS of the first `i` and first "
             "`j` characters\". A vague subproblem gives no recurrence."),
            ("Write the recurrence",
             "How an optimal solution decomposes. This is where optimal substructure is "
             "either present or absent."),
            ("Identify the base cases",
             "The smallest subproblems, answered outright."),
            ("Choose memoisation or a table",
             "Same cost. Bottom-up if the space can be reduced; top-down if only some "
             "subproblems are needed."),
        ],
        "worked": {
            "title": "Coin change with `{1, 3, 4}`",
            "intro": ["Filling the table from 0 upward."],
            "lines": [
                "v:      0   1   2   3   4   5   6   7   8",
                "best:   0   1   2   1   1   2   2   2   2",
                "",
                "best[6] = 1 + min( best[5], best[3], best[2] )",
                "        = 1 + min(   2,       1,       2   ) = 2      via coin 3",
                "",
                "best[7] = 1 + min( best[6], best[4], best[3] )",
                "        = 1 + min(   2,       1,       1   ) = 2      via coin 3 or 4",
                "",
                "GREEDY at 6:   4 + 1 + 1     three coins",
                "TABLE at 6:    3 + 3         two coins",
                "",
                "Cost: Θ(v · number of coins) — here 6 × 3 = 18 comparisons.",
            ],
            "after": [
                "Every entry was computed once and read several times, which is the whole "
                "saving. The naive recursion would recompute `best[3]` at values 4, 6 and "
                "7, and each of those recomputations would recurse again."
            ],
        },
        "quiz_title": "Dynamic programming",
        "quiz": [
            {"q": "Dynamic programming requires:",
             "a": ["recursion only",
                   "optimal substructure and overlapping subproblems",
                   "a greedy choice property",
                   "sorted input"],
             "c": 1,
             "why": "Both. Optimal substructure without overlap is divide-and-conquer; "
                    "overlap without it is not helped."},
            {"q": "Memoising the naive Fibonacci reduces the call count from about `1.6ⁿ` to:",
             "a": ["`log n`", "`n`", "`n²`", "`2ⁿ`"],
             "c": 1,
             "why": "Each value is computed once and reused thereafter."},
            {"q": "Longest simple path has no dynamic program because:",
             "a": ["it is too large",
                   "it lacks optimal substructure — subpaths may share vertices",
                   "graphs are not ordered",
                   "it is undecidable"],
             "c": 1,
             "why": "Concatenating two longest subpaths may repeat a vertex, so the "
                    "combination is not a simple path. The problem is NP-hard."},
        ],
        "mistakes": [
            ("Applying it without checking optimal substructure",
             "The recurrence will be written and will be wrong. Longest simple path is the "
             "standard example."),
            ("Memoising a divide-and-conquer algorithm",
             "Merge sort's subproblems never repeat, so the cache never hits and the "
             "overhead is pure loss."),
            ("Defining the subproblem loosely",
             "\"The best solution so far\" is not a subproblem. It must be a function of "
             "explicit parameters."),
        ],
        "standard": ("Finish when you can write the recurrence before any code.",
                     "Write the recurrence for the 0/1 knapsack problem &mdash; items with "
                     "weights and values, a capacity, items cannot be split. Define the "
                     "subproblem in terms of the first `i` items and remaining capacity `w`, "
                     "and the recurrence writes itself."),
        "note": "The name is historical and misleading: Bellman chose it in the 1950s "
                "partly because \"programming\" then meant planning and partly, by his own "
                "account, because it sounded impressive enough to survive a hostile funding "
                "review. It has nothing to do with programming in the modern sense.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "complexity-classes",
        "title": "P, NP and NP-Completeness",
        "module": "Limits",
        "one_line": "Solvable quickly, checkable quickly, and the hardest problems in between.",
        "summary": (
            "P is what can be solved in polynomial time; NP is what can be verified in "
            "polynomial time. Whether they are equal is the central open question, and "
            "the NP-complete problems are the ones on which it turns."
        ),
        "key": [
            "P     solvable in polynomial time",
            "NP    a proposed solution is VERIFIABLE in polynomial time",
            "P ⊆ NP;  whether P = NP is OPEN",
            "NP-complete: in NP, and everything in NP reduces to it",
        ],
        "key_label": "Two classes and an open question",
        "concepts_intro": (
            "The classification is about the problem, not about any particular algorithm, "
            "and knowing it changes what you should attempt."
        ),
        "concepts": [
            ("NP is about verification, not non-determinism",
             "A problem is in NP when a claimed solution can be checked quickly. The name "
             "comes from an older definition and misleads."),
            ("NP-complete problems are the hardest in NP",
             "Everything in NP reduces to them, so a polynomial algorithm for one gives "
             "one for all."),
            ("The classification is practical information",
             "\"NP-complete\" means stop looking for an exact efficient algorithm and "
             "consider approximation, heuristics or special cases."),
        ],
        "read_title": "The classes",
        "read_intro": "Definitions, examples, reductions, and what the classification means in practice.",
        "body": [
            ("def", ("P",
                     "The class of decision problems solvable by an algorithm running in "
                     "time `O(nᵏ)` for some constant `k`, where `n` is the input size. "
                     "Informally: efficiently solvable.")),
            ("def", ("NP",
                     "The class of decision problems for which a proposed solution can be "
                     "<strong>verified</strong> in polynomial time. Informally: if someone "
                     "hands you an answer, you can check it quickly.")),
            ("p", "The name stands for <em>nondeterministic polynomial</em>, from an older "
                  "definition using a machine that guesses. The verification definition is "
                  "equivalent and far more intuitive: <strong>NP is not \"not "
                  "polynomial\"</strong>, and P is a subset of NP."),
            ("math", [
                "problem                          in P?      in NP?",
                "is n prime?                       yes         yes",
                "sort a list                       yes         yes",
                "shortest path                     yes         yes",
                "is this formula satisfiable?      unknown     yes",
                "does a Hamilton circuit exist?    unknown     yes",
                "graph colouring with 3 colours    unknown     yes",
                "does this program halt?           NO           NO — undecidable",
            ]),
            ("p", "Every problem in P is in NP: if you can solve it quickly you can verify "
                  "a claimed answer quickly by solving it and comparing. The reverse "
                  "inclusion is the open question."),
            ("h3", "Reductions"),
            ("def", ("Polynomial-time reduction",
                     "Problem `A` <strong>reduces</strong> to `B` if any instance of `A` "
                     "can be transformed in polynomial time into an instance of `B` with "
                     "the same answer. Then an efficient algorithm for `B` gives one for "
                     "`A`, so `B` is at least as hard as `A`.")),
            ("def", ("NP-complete",
                     "A problem is <strong>NP-complete</strong> if it is in NP and every "
                     "problem in NP reduces to it. It is <strong>NP-hard</strong> if the "
                     "second condition holds whether or not it is in NP.")),
            ("thm", ("Cook-Levin theorem (1971)",
                     "SAT &mdash; deciding whether a propositional formula is satisfiable "
                     "&mdash; is NP-complete. It was the first problem shown to be so, and "
                     "every subsequent NP-completeness proof reduces from a problem already "
                     "known to be complete.")),
            ("p", "Course 1 lesson 6 raised the question and named the result; here is what "
                  "it means. Thousands of problems are now known to be NP-complete: "
                  "Hamilton circuit, 3-colouring, subset sum, the travelling salesman "
                  "decision problem, 0/1 knapsack, and clique among them."),
            ("p", "They are all equivalent in the sense that matters: a polynomial-time "
                  "algorithm for any one would give one for all of them, and hence "
                  "`P = NP`. Fifty years of effort has produced neither such an algorithm "
                  "nor a proof that none exists."),
            ("h3", "What the classification means in practice"),
            ("ul", [
                "<strong>In P.</strong> Look for a good polynomial algorithm and expect to "
                "find one.",
                "<strong>NP-complete.</strong> Stop looking for an efficient exact "
                "algorithm. Consider approximation algorithms with proved ratios, "
                "heuristics with no guarantee, exact methods on restricted inputs, or "
                "solvers that are fast in practice.",
                "<strong>Undecidable.</strong> Stop entirely. No algorithm exists, and "
                "lesson 12 is about what that means.",
            ]),
            ("p", "Being NP-complete is a worst-case statement and does not mean instances "
                  "are hard in practice. Industrial SAT solvers routinely handle formulas "
                  "with millions of variables, because real instances have structure. The "
                  "classification tells you what to expect in general and not what will "
                  "happen on your data."),
            ("p", "If `P = NP` were proved constructively, essentially every "
                  "optimisation problem would become tractable and public-key cryptography "
                  "would collapse. Most researchers expect `P ≠ NP`; nobody has proved it, "
                  "and it is one of the Clay Millennium Problems."),
        ],
        "lab": ("algorithm", {
            "mode": "growth", "n": 24,
            "panel_title": "The line the classification draws",
            "panel_intro": "Polynomial curves and `2ⁿ` on one log-scale plot. The gap at "
                           "`n = 64` is the practical content of \"tractable\", and it is "
                           "why the boundary is drawn at polynomial.",
        }),
        "steps_title": "Placing a problem",
        "steps_intro": "Verification first; it is the cheapest test.",
        "steps": [
            ("Can a claimed solution be checked quickly?",
             "If yes, the problem is in NP. This is usually obvious and is the first step."),
            ("Is there a known polynomial algorithm?",
             "Then it is in P. Shortest path, sorting, primality, matching, minimum "
             "spanning tree."),
            ("Does it resemble a known NP-complete problem?",
             "Hamilton circuit, SAT, 3-colouring, subset sum, clique. A reduction from one "
             "of these proves NP-hardness."),
            ("Act on the answer",
             "In P: find the algorithm. NP-complete: approximate, restrict or use a solver. "
             "Undecidable: change the question."),
        ],
        "worked": {
            "title": "Two similar problems, opposite sides",
            "intro": ["The clearest pair on this path."],
            "lines": [
                "EULER CIRCUIT — does a circuit using every edge once exist?",
                "   criterion: connected, all degrees even",
                "   check: one pass over the vertices                  Θ(n + |E|)",
                "   IN P",
                "",
                "HAMILTON CIRCUIT — does a circuit visiting every vertex once exist?",
                "   criterion: none known",
                "   verification of a claimed circuit: check n edges   Θ(n)   ⟹ IN NP",
                "   best known exact algorithm: exponential",
                "   NP-COMPLETE",
                "",
                "Nothing in the two statements reveals which is which.",
                "The difficulty is a fact about the problems, not about the wording.",
            ],
            "after": [
                "Course 7 lesson 7 presented both and noted the contrast; this is what the "
                "contrast means. Verifying a Hamilton circuit is easy, which puts it in NP; "
                "finding one is believed hard, which is the `P` versus `NP` question in "
                "miniature."
            ],
        },
        "quiz_title": "Complexity classes",
        "quiz": [
            {"q": "NP stands for:",
             "a": ["not polynomial", "nondeterministic polynomial — problems verifiable in polynomial time",
                   "nearly polynomial", "no problem"],
             "c": 1,
             "why": "It is about verification. P is a subset of NP, so \"not polynomial\" "
                    "would be a contradiction."},
            {"q": "A polynomial algorithm for one NP-complete problem would:",
             "a": ["solve only that problem",
                   "give polynomial algorithms for every problem in NP",
                   "prove P ≠ NP",
                   "have no consequences"],
             "c": 1,
             "why": "Every problem in NP reduces to it, so `P = NP` would follow. That is "
                    "what completeness means."},
            {"q": "\"NP-complete\" tells a practitioner to:",
             "a": ["give up entirely",
                   "stop seeking an efficient exact algorithm and consider approximation, heuristics or restricted cases",
                   "use a faster computer",
                   "rewrite in a faster language"],
             "c": 1,
             "why": "It is actionable information about which approaches are worth "
                    "attempting."},
        ],
        "mistakes": [
            ("Reading NP as \"not polynomial\"",
             "Every problem in P is in NP. The name is historical and actively misleading."),
            ("Treating NP-complete as \"unsolvable\"",
             "It is a worst-case statement. SAT solvers handle industrial instances with "
             "millions of variables."),
            ("Confusing NP-complete with undecidable",
             "NP-complete problems have algorithms that are slow. Undecidable problems have "
             "no algorithm at all, which is lesson 12."),
        ],
        "standard": ("Finish when you can say what the classification changes.",
                     "For a problem you are handed, decide whether a solution is quickly "
                     "verifiable, whether it resembles a known complete problem, and what "
                     "you would attempt in each case. The last part is the point."),
        "note": "`P` versus `NP` is one of the seven Clay Millennium Problems, with a "
                "million-dollar prize. It was posed by Cook in 1971 and, unusually for a "
                "problem of that stature, is stated in terms an undergraduate course can "
                "reach.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "decidability-and-the-halting-problem",
        "title": "Decidability and the Halting Problem",
        "module": "Limits",
        "one_line": "Some problems have no algorithm at all — and that is provable.",
        "summary": (
            "The halting problem is undecidable: no program can determine, for every "
            "program and input, whether it terminates. The proof is a diagonal argument "
            "and it fits on a page."
        ),
        "key": [
            "DECIDABLE     some algorithm always terminates with the right answer",
            "UNDECIDABLE   no such algorithm exists — proved, not merely unknown",
            "the HALTING PROBLEM is undecidable                (Turing, 1936)",
            "Rice: every nontrivial semantic property is undecidable",
        ],
        "key_label": "The hard limit",
        "concepts_intro": (
            "Undecidability is a theorem, not a state of ignorance, and its proof uses "
            "the same self-reference course 1 excluded from propositions."
        ),
        "concepts": [
            ("Undecidable is proved, not unknown",
             "It is not that nobody has found an algorithm. It is that none can exist, and "
             "the proof is a page long."),
            ("The proof is Cantor's diagonal argument",
             "Assume the decider exists, build a program that does the opposite of what it "
             "predicts, and ask about that program."),
            ("Rice's theorem generalises it",
             "Every nontrivial question about what a program computes is undecidable, which "
             "is why static analysis is necessarily approximate."),
        ],
        "read_title": "The limits of computation",
        "read_intro": "Decidability, the halting problem, the proof, and what follows.",
        "body": [
            ("def", ("Decidable",
                     "A decision problem is <strong>decidable</strong> if some algorithm "
                     "terminates on every input with the correct yes/no answer. Otherwise "
                     "it is <strong>undecidable</strong>.")),
            ("p", "Note what undecidable does not mean. Not \"hard\", not \"exponential\", "
                  "not \"nobody has managed it\". It means no algorithm exists and none "
                  "ever will, and the statement is a theorem."),
            ("thm", ("The halting problem is undecidable (Turing, 1936)",
                     "There is no algorithm `H(P, x)` that, for every program `P` and input "
                     "`x`, terminates and correctly reports whether `P` halts on `x`.")),
            ("proof", [
                "Suppose such an `H` exists. Build a program `D` that takes one input `P` "
                "&mdash; the source of a program &mdash; and does the following: run "
                "`H(P, P)`; if `H` says `P` halts on input `P`, then loop forever; if `H` "
                "says `P` does not halt, then halt immediately.",
                "`D` is a perfectly ordinary program: it calls `H`, which by assumption "
                "always terminates, and then branches.",
                "Now ask what `D` does on input `D`.",
                "If `D` halts on `D`, then `H(D, D)` reported \"halts\", so by construction "
                "`D` loops forever. Contradiction.",
                "If `D` does not halt on `D`, then `H(D, D)` reported \"does not halt\", so "
                "by construction `D` halts immediately. Contradiction.",
                "Both cases are impossible, so `H` cannot exist.",
            ]),
            ("p", "The structure is exactly course 2 lesson 13's diagonal argument: assume "
                  "a complete listing or a complete decider, construct the object that "
                  "differs from every entry, and derive a contradiction. Cantor used it "
                  "against enumerations of the reals; Turing used it against deciders."),
            ("p", "It is also the self-reference course 1 lesson 1 excluded from "
                  "propositions, reappearing where it cannot be excluded: programs can take "
                  "programs as input, and `D` is applied to itself. That is not a trick, "
                  "it is what makes computation universal."),
            ("h3", "Rice's theorem"),
            ("thm", ("Rice's theorem",
                     "Every nontrivial property of the function a program computes is "
                     "undecidable. \"Nontrivial\" means some programs have it and some do "
                     "not.")),
            ("p", "So all of the following are undecidable: does this program ever output "
                  "0? do these two programs compute the same function? does this program "
                  "ever access an unallocated address? is this code reachable? does this "
                  "loop terminate?"),
            ("p", "This is why static analysis tools are necessarily conservative. A "
                  "compiler warning about unreachable code, a type system, a linter and a "
                  "verifier all approximate: they may report a problem that does not exist "
                  "or miss one that does, and Rice's theorem says no tool can do "
                  "otherwise for every program."),
            ("h3", "Other undecidable problems"),
            ("ul", [
                "<strong>The Post correspondence problem.</strong> Given two lists of "
                "strings, can a sequence of indices be found making the concatenations "
                "equal? A purely combinatorial question with no algorithm.",
                "<strong>Hilbert's tenth problem.</strong> Does a given polynomial equation "
                "have integer solutions? Shown undecidable by Matiyasevich in 1970 &mdash; "
                "arithmetic itself is not fully mechanisable.",
                "<strong>Program equivalence.</strong> Do two programs compute the same "
                "function? Undecidable by Rice, which is why compiler optimisations are "
                "verified by construction rather than by comparison.",
            ]),
            ("h3", "The hierarchy"),
            ("math", [
                "P                       solvable efficiently",
                "NP                      verifiable efficiently",
                "NP-complete             the hardest in NP",
                "EXPTIME                 solvable, but exponentially",
                "DECIDABLE               solvable eventually",
                "UNDECIDABLE             no algorithm exists",
            ]),
            ("p", "The path ends here, and the position is worth stating plainly. Course 1 "
                  "made statements precise; course 3 gave the technique for proving them; "
                  "courses 4 to 7 built the structures; and this course measured the cost "
                  "of computing with them. The last two lessons say what cost cannot be "
                  "paid at all &mdash; some problems are intractable, and some are outside "
                  "the reach of any algorithm whatever."),
        ],
        "lab": ("algorithm", {
            "mode": "growth", "n": 20,
            "panel_title": "Beyond the last curve",
            "panel_intro": "Every curve here is a running time, and every one is finite. "
                           "Undecidable problems have no curve at all, which is a different "
                           "kind of statement from anything the plot can show.",
        }),
        "steps_title": "Recognising an undecidable problem",
        "steps_intro": "Ask what is being asked about.",
        "steps": [
            ("Is the question about program behaviour?",
             "\"Does it halt\", \"does it output\", \"are these equivalent\". Rice's "
             "theorem makes all such nontrivial questions undecidable."),
            ("Try reducing the halting problem to it",
             "If a decider for your problem would give one for halting, yours is "
             "undecidable too. That is the standard proof technique."),
            ("Distinguish undecidable from intractable",
             "NP-complete means slow; undecidable means impossible. Different responses "
             "are appropriate."),
            ("Restrict the question until it is decidable",
             "Bounded loops, finite state spaces, restricted languages. Practical "
             "verification works by narrowing the question, not by defeating the theorem."),
        ],
        "worked": {
            "title": "The proof, in seven lines",
            "intro": ["Short enough to reconstruct from memory, and worth being able to."],
            "lines": [
                "Assume H(P, x) exists and always answers correctly.",
                "",
                "Define    D(P):",
                "              if H(P, P) says \"halts\":  loop forever",
                "              else:                       halt",
                "",
                "Ask:  does D halt on input D?",
                "",
                "   D halts on D   ⟹  H said \"halts\"        ⟹  D loops.   ✗",
                "   D loops on D   ⟹  H said \"does not halt\" ⟹  D halts.   ✗",
                "",
                "Both branches contradict.  H cannot exist.               ∎",
            ],
            "after": [
                "The whole proof rests on `D` being a legitimate program, which it is: it "
                "calls `H`, which was assumed to be an algorithm, and then branches. Nothing "
                "exotic is required, and that is what makes the conclusion so strong."
            ],
        },
        "quiz_title": "Decidability",
        "quiz": [
            {"q": "\"The halting problem is undecidable\" means:",
             "a": ["it is very hard",
                   "no algorithm can solve it for all inputs — proved, not unknown",
                   "it takes exponential time",
                   "it has not been solved yet"],
             "c": 1,
             "why": "A theorem, not a state of ignorance. No future technique will produce "
                    "the algorithm."},
            {"q": "Rice's theorem says:",
             "a": ["all programs halt",
                   "every nontrivial property of what a program computes is undecidable",
                   "P = NP",
                   "sorting needs `n log n`"],
             "c": 1,
             "why": "Which is why static analysis is necessarily approximate: no tool can "
                    "be both sound and complete for every program."},
            {"q": "The halting proof works by:",
             "a": ["exhaustive search",
                   "constructing a program that does the opposite of what the decider predicts about it",
                   "counting programs",
                   "assuming P = NP"],
             "c": 1,
             "why": "A diagonal argument: build the object that differs from every entry, "
                    "here by applying `D` to itself."},
        ],
        "mistakes": [
            ("Reading undecidable as \"very hard\"",
             "NP-complete is very hard. Undecidable means no algorithm exists, and the two "
             "call for entirely different responses."),
            ("Thinking a specific program's halting cannot be determined",
             "Many individual programs are easy to analyse. The theorem is about a general "
             "procedure covering all of them."),
            ("Believing better tools will eventually decide these questions",
             "Rice's theorem is a proof. Practical verification works by restricting the "
             "question, not by defeating the theorem."),
        ],
        "standard": ("Finish when you can reproduce the halting proof from memory.",
                     "Seven lines: assume the decider, build the contrary program, apply it "
                     "to itself, and read off both contradictions. It is the sharpest "
                     "argument on this path and the shortest of the major ones."),
        "note": "Turing's 1936 paper introduced the machine model, proved this result, and "
                "established that a single universal machine can simulate any other &mdash; "
                "the theoretical basis of the stored-program computer. The limits and the "
                "possibility arrived in the same paper.",
    },
]
