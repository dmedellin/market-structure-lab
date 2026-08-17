"""Course 8, lessons 01-06 — algorithms and analysis."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "algorithms-and-pseudocode",
        "title": "Algorithms and Pseudocode",
        "module": "Foundations",
        "one_line": "A finite, definite procedure — and how to write one down.",
        "summary": (
            "An algorithm is a finite sequence of precise steps producing an output from "
            "an input. Pseudocode is how it is communicated: precise enough to analyse, "
            "free of the details of any language."
        ),
        "key": [
            "INPUT      DEFINITENESS      FINITENESS      OUTPUT      EFFECTIVENESS",
            "pseudocode: precise about the method, silent about the language",
            "the same problem admits many algorithms",
            "correctness first, efficiency second",
        ],
        "key_label": "Five requirements",
        "concepts_intro": (
            "The definition rules out things that look like algorithms and are not, and "
            "each requirement rules out a specific failure."
        ),
        "concepts": [
            ("Every step must be unambiguous",
             "\"Choose a good pivot\" is not a step. If two people executing the "
             "description could do different things, it is not an algorithm."),
            ("It must terminate",
             "On every valid input. A procedure that may run forever is not an algorithm, "
             "however useful it is."),
            ("Pseudocode is for humans",
             "Detailed enough to analyse and implement, free of syntax. Analysis is about "
             "the method, not the language."),
        ],
        "read_title": "What an algorithm is",
        "read_intro": "The five requirements, pseudocode conventions, and one problem solved three ways.",
        "body": [
            ("def", ("Algorithm",
                     "A finite sequence of precise instructions transforming an input into "
                     "an output. It must have: <strong>input</strong> from a specified set; "
                     "<strong>definiteness</strong>, every step unambiguous; "
                     "<strong>finiteness</strong>, terminating after finitely many steps; "
                     "<strong>output</strong> in a specified relation to the input; and "
                     "<strong>effectiveness</strong>, every step performable exactly.")),
            ("p", "Each requirement excludes something real. Definiteness excludes "
                  "\"pick a suitable value\"; finiteness excludes a loop that may never "
                  "exit; effectiveness excludes \"decide whether this program halts\", "
                  "which lesson 12 shows is not performable at all."),
            ("h3", "Pseudocode"),
            ("math", [
                "MAXIMUM(a₁, …, aₙ):",
                "    max = a₁",
                "    for i = 2 to n:",
                "        if aᵢ > max:  max = aᵢ",
                "    return max",
            ]),
            ("p", "The conventions used on this course: indentation for blocks, `=` for "
                  "assignment, `←` avoided, one-based indexing, and enough English to keep "
                  "it readable. Nothing depends on a language, and the analysis of lesson 5 "
                  "counts the comparisons regardless of how it is implemented."),
            ("h3", "One problem, three algorithms"),
            ("p", "Computing `xⁿ` for a positive integer `n`:"),
            ("math", [
                "A.  repeated multiplication          n − 1 multiplications",
                "        result = x",
                "        repeat n−1 times: result = result · x",
                "",
                "B.  repeated squaring                about 2·log₂ n multiplications",
                "        as in course 6 lesson 8",
                "",
                "C.  addition-chain exponentiation    slightly fewer than B, sometimes",
                "        precompute an optimal chain of products",
            ]),
            ("p", "All three are correct and they differ enormously in cost. At `n = 1000`, "
                  "A performs 999 multiplications and B performs about 15. That gap is the "
                  "subject of this course, and it is a property of the algorithm rather "
                  "than of the machine."),
            ("h3", "Correctness before efficiency"),
            ("p", "An algorithm that is fast and wrong is worthless, and the order of work "
                  "is therefore fixed: establish correctness (lesson 2), then measure cost "
                  "(lessons 3 to 8), then look for a better method (lessons 9 to 10)."),
            ("p", "The order is worth stating because the temptation runs the other way. "
                  "Optimising an algorithm before knowing it is right produces a faster "
                  "wrong answer, and the speed makes the error harder to find."),
        ],
        "lab": ("algorithm", {
            "mode": "growth", "n": 16,
            "panel_title": "Why the choice matters",
            "panel_intro": "The functions plotted are the cost curves of different "
                           "algorithms for the same tasks. At `n = 64` they differ by "
                           "nineteen orders of magnitude.",
        }),
        "steps_title": "Writing an algorithm down",
        "steps_intro": "State the contract before the steps.",
        "steps": [
            ("State the input and the output",
             "What is given, what is produced, and the relation between them. This is the "
             "specification, and lesson 2 proves the algorithm meets it."),
            ("Write the steps unambiguously",
             "No step may require judgement. If it does, it is a subproblem needing its own "
             "algorithm."),
            ("Check it terminates on every valid input",
             "Exhibit a quantity that strictly decreases and is bounded below, as in "
             "course 3 lesson 8."),
            ("Only then consider the cost",
             "Count the dominant operation as a function of the input size. That is "
             "lesson 5."),
        ],
        "worked": {
            "title": "Specifying and writing linear search",
            "intro": ["The specification is the part usually skipped."],
            "lines": [
                "INPUT   a list a₁ … aₙ and a value x",
                "OUTPUT  an index i with aᵢ = x, or 0 if x does not occur",
                "",
                "LINEAR-SEARCH(a, x):",
                "    for i = 1 to n:",
                "        if aᵢ = x:  return i",
                "    return 0",
                "",
                "definiteness   every step is a comparison or a return       ✓",
                "finiteness     the loop runs at most n times                ✓",
                "output         returns an index or 0, as specified          ✓",
                "cost           n comparisons in the worst case",
            ],
            "after": [
                "The specification says \"an index\", not \"the first index\". If the "
                "caller needs the first occurrence that must be stated, because it "
                "constrains which algorithms are acceptable &mdash; binary search on a "
                "sorted list with duplicates does not guarantee it without modification."
            ],
        },
        "quiz_title": "Algorithms",
        "quiz": [
            {"q": "Which requirement excludes \"choose a suitable value for `k`\"?",
             "a": ["finiteness", "definiteness", "output", "input"],
             "c": 1,
             "why": "Every step must be unambiguous. A step requiring judgement is a "
                    "subproblem, not an instruction."},
            {"q": "A procedure that may loop forever on some inputs is:",
             "a": ["an algorithm", "not an algorithm — finiteness fails",
                   "an efficient algorithm", "a heuristic that is also an algorithm"],
             "c": 1,
             "why": "Termination on every valid input is part of the definition."},
            {"q": "Computing `x¹⁰⁰⁰` by repeated multiplication versus repeated squaring:",
             "a": ["both take 1000 steps",
                   "999 multiplications versus about 15",
                   "squaring is slower",
                   "the difference depends on the machine"],
             "c": 1,
             "why": "The gap is a property of the algorithms, not of the hardware, which "
                    "is why analysis is about the method."},
        ],
        "mistakes": [
            ("Leaving a step to judgement",
             "\"Pick a good pivot\" hides an entire algorithm. Every step must be "
             "mechanically performable."),
            ("Optimising before proving correct",
             "A faster wrong answer is worse than a slow right one, and the speed makes "
             "the error harder to notice."),
            ("Specifying the output loosely",
             "\"Find the element\" leaves open whether the first, any, or all occurrences "
             "are wanted, and different algorithms answer different questions."),
        ],
        "standard": ("Finish when you write the specification before the pseudocode.",
                     "Specify and write an algorithm that returns the two largest values "
                     "in a list. State what happens when the list has fewer than two "
                     "elements &mdash; the edge case the specification exists to settle."),
        "note": "\"Algorithm\" comes from al-Khwārizmī, the ninth-century mathematician "
                "whose book on Hindu&ndash;Arabic numerals gave Europe both the word and "
                "the method of calculation. \"Algebra\" comes from the title of another of "
                "his works.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "correctness-and-termination",
        "title": "Correctness and Termination",
        "module": "Foundations",
        "one_line": "Two separate obligations, and neither is optional.",
        "summary": (
            "Partial correctness says the output is right if the algorithm stops. "
            "Termination says it stops. Loop invariants establish the first and a "
            "decreasing bounded quantity establishes the second."
        ),
        "key": [
            "PARTIAL CORRECTNESS   if it terminates, the postcondition holds",
            "TERMINATION           it does terminate",
            "TOTAL CORRECTNESS     both",
            "invariant for the first, a decreasing measure for the second",
        ],
        "key_label": "Two obligations",
        "concepts_intro": (
            "This is course 3 lesson 12 applied to algorithms, and the split is what "
            "makes the proofs short."
        ),
        "concepts": [
            ("The two are independent",
             "An algorithm can be partially correct and never stop, or terminate promptly "
             "with a wrong answer. Neither proof implies the other."),
            ("An invariant is what the loop preserves",
             "Naming the preserved property is more informative than describing what the "
             "loop does, and it is what closes the argument."),
            ("Termination needs a decreasing measure",
             "A quantity that strictly decreases on every iteration and cannot decrease "
             "forever. Usually an index or a remaining size."),
        ],
        "read_title": "Proving an algorithm right",
        "read_intro": "The two obligations, both discharged on three algorithms.",
        "body": [
            ("def", ("Partial and total correctness",
                     "An algorithm is <strong>partially correct</strong> when, if it "
                     "terminates, its output satisfies the specification. It is "
                     "<strong>totally correct</strong> when it is partially correct and "
                     "terminates on every valid input.")),
            ("h3", "Linear search"),
            ("math", [
                "LINEAR-SEARCH(a, x):",
                "    for i = 1 to n:",
                "        if aᵢ = x:  return i",
                "    return 0",
                "",
                "INVARIANT   before iteration i,  x ∉ {a₁, …, a_{i−1}}",
            ]),
            ("p", "<strong>Initialisation.</strong> Before the first iteration the set is "
                  "empty and the claim is vacuous. <strong>Maintenance.</strong> The "
                  "iteration returns if `aᵢ = x`, so reaching the next iteration means "
                  "`x ≠ aᵢ`, extending the invariant. <strong>Termination.</strong> If the "
                  "loop finishes, the invariant says `x` is in none of `a₁ … aₙ`, so "
                  "returning 0 is correct; if it returns `i`, then `aᵢ = x`."),
            ("p", "<strong>Termination</strong> holds because `n − i` strictly decreases and "
                  "is a non-negative integer."),
            ("h3", "Insertion sort"),
            ("p", "The outer-loop invariant is that `a[1..j−1]` holds the original first "
                  "`j−1` elements in sorted order. Both halves are needed: \"sorted\" alone "
                  "would be satisfied by an algorithm that replaced the array with zeros, "
                  "and the specification says the output must be a permutation of the input."),
            ("p", "Termination: the outer loop runs `n − 1` times, and the inner loop "
                  "decreases `i` each iteration with `i ≥ 0` enforced by its own condition."),
            ("h3", "Euclid's algorithm"),
            ("p", "The invariant is `gcd(a, b) = gcd(a₀, b₀)`, preserved because "
                  "`gcd(a,b) = gcd(b, a mod b)`. Termination holds because `b` strictly "
                  "decreases and is a non-negative integer. At exit `b = 0` and "
                  "`gcd(a, 0) = a`, which the invariant identifies as the answer."),
            ("p", "That invariant is the whole proof and it is one line, which is "
                  "characteristic: a good invariant names the quantity the loop preserves, "
                  "and the correctness then follows from the exit condition."),
            ("h3", "When termination is the hard part"),
            ("example", ("The Collatz procedure",
                         "From `n`, repeat: if `n` is even, halve it; otherwise replace it "
                         "by `3n + 1`; stop at 1. It terminates for every starting value "
                         "ever tested &mdash; beyond `10²⁰` &mdash; and no proof is known "
                         "that it always does. Partial correctness is trivial; termination "
                         "is an open problem.")),
            ("p", "That example separates the two obligations cleanly. It also previews "
                  "lesson 12: there is no general procedure that decides termination for "
                  "arbitrary programs, which is why each one needs its own argument."),
        ],
        "lab": ("algorithm", {
            "mode": "sort", "n": 16,
            "panel_title": "Counts, from running",
            "panel_intro": "The counts come from executing each algorithm on the same "
                           "input. Insertion sort's count depends on the data and bubble "
                           "sort's does not &mdash; which is a fact about their loop "
                           "structures.",
        }),
        "steps_title": "Proving an algorithm correct",
        "steps_intro": "Invariant, then measure.",
        "steps": [
            ("Write the specification",
             "Precondition and postcondition. Without them there is nothing to prove."),
            ("Find an invariant strong enough",
             "Test it at exit first: the invariant plus the negated loop condition must "
             "give the postcondition. If it does not, strengthen it."),
            ("Prove initialisation and maintenance",
             "True before the first iteration, preserved by the body. This is base case "
             "and inductive step."),
            ("Exhibit a decreasing bounded measure",
             "For termination. An index, a range size, a remaining count &mdash; strictly "
             "decreasing and bounded below."),
        ],
        "worked": {
            "title": "Exponentiation by squaring, both obligations",
            "intro": ["Course 6's algorithm, proved."],
            "lines": [
                "POWER(x, n):",
                "    result = 1;  base = x;  m = n",
                "    while m > 0:",
                "        if m is odd:  result = result · base",
                "        base = base · base",
                "        m = m div 2",
                "    return result",
                "",
                "INVARIANT      result · base^m = xⁿ",
                "",
                "INITIALISATION  1 · x^n = xⁿ                                   ✓",
                "MAINTENANCE     m even:  result·(base²)^{m/2} = result·base^m  ✓",
                "                m odd:   (result·base)·(base²)^{(m−1)/2}",
                "                       = result·base^m                          ✓",
                "TERMINATION     m halves each iteration, bounded below by 0    ✓",
                "                at exit m = 0, so invariant reads result = xⁿ  ✓",
            ],
            "after": [
                "The invariant was chosen to be exactly what the exit condition needs. "
                "That is the technique: work backwards from the postcondition, substitute "
                "the loop variable for its final value, and the invariant usually appears."
            ],
        },
        "quiz_title": "Correctness",
        "quiz": [
            {"q": "Partial correctness means:",
             "a": ["correct on some inputs",
                   "if the algorithm terminates, the output is right",
                   "the algorithm terminates",
                   "the algorithm is efficient"],
             "c": 1,
             "why": "Termination is the separate obligation. Partial correctness says "
                    "nothing about whether it stops."},
            {"q": "An invariant that is preserved but does not give the postcondition at exit is:",
             "a": ["sufficient", "too weak", "false", "a termination proof"],
             "c": 1,
             "why": "Weak invariants are easy to preserve and prove nothing. Test at exit "
                    "before doing any other work."},
            {"q": "The Collatz procedure illustrates that:",
             "a": ["invariants are unnecessary",
                   "termination can be the hard obligation",
                   "partial correctness is hard",
                   "algorithms always terminate"],
             "c": 1,
             "why": "Partial correctness is trivial and termination is an open problem "
                    "after decades of work."},
        ],
        "mistakes": [
            ("Proving one obligation and stopping",
             "Both are required, and neither implies the other. Say explicitly which you "
             "have established."),
            ("Choosing an invariant that is too weak",
             "\"The array is sorted\" without \"and is a permutation of the input\" is "
             "satisfied by an algorithm that destroys the data."),
            ("Assuming loops obviously terminate",
             "Name the decreasing quantity and its lower bound. It is one sentence and it "
             "is where an off-by-one shows."),
        ],
        "standard": ("Finish when you test the invariant at exit first.",
                     "Write a loop computing the sum of an array, state its invariant, and "
                     "check that the invariant plus the exit condition gives exactly \"the "
                     "sum of all `n` elements\". If it needs an extra sentence, strengthen "
                     "the invariant."),
        "note": "Hoare logic formalises this with a rule for each language construct, and "
                "modern verification tools mechanise it. What does not mechanise is "
                "finding the invariant, which remains the creative step.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "growth-of-functions",
        "title": "The Growth of Functions",
        "module": "Analysis",
        "one_line": "What matters at scale, and what does not.",
        "summary": (
            "Comparing algorithms means comparing how their costs grow, not their costs "
            "at any one size. Constants and lower-order terms vanish; the gap between "
            "polynomial and exponential does not."
        ),
        "key": [
            "1 < log n < √n < n < n log n < n² < n³ < 2ⁿ < n!",
            "constants and lower-order terms do not affect the class",
            "polynomial vs exponential is a difference of KIND",
            "a faster machine moves the wall; it does not remove it",
        ],
        "key_label": "The hierarchy",
        "concepts_intro": (
            "Growth rate is the property that survives changes of machine, language and "
            "constant factor."
        ),
        "concepts": [
            ("Growth is what survives",
             "A machine ten times faster multiplies every cost by `1/10` and changes no "
             "growth rate. The classification is about the algorithm."),
            ("Lower-order terms vanish",
             "`3n² + 5n + 100` grows like `n²`: at `n = 1000` the quadratic term is 99.8% "
             "of the total."),
            ("Exponential is a different kind",
             "Polynomial costs scale with hardware; exponential ones do not. `2ⁿ` at "
             "`n = 100` exceeds the number of atoms in the observable universe."),
        ],
        "read_title": "Comparing growth",
        "read_intro": "The hierarchy, the numbers behind it, and what a faster machine buys.",
        "body": [
            ("math", [
                "n           log₂n     n log₂n        n²            2ⁿ",
                "10            3.3          33          100         1 024",
                "100           6.6         664       10 000        1.3 × 10³⁰",
                "1 000        10.0      9 966    1 000 000        1.1 × 10³⁰¹",
                "1 000 000    20.0   2.0 × 10⁷    10¹²             —",
            ]),
            ("p", "At a million elements, an `n log n` algorithm does about 20 million "
                  "operations and an `n²` algorithm does `10¹²` &mdash; the difference "
                  "between a fraction of a second and about a fortnight. Both are "
                  "polynomial; the gap is already decisive."),
            ("p", "`2ⁿ` at `n = 100` is `1.27 × 10³⁰`. At a billion operations per second "
                  "that is about `4 × 10¹³` years, roughly three thousand times the age of "
                  "the universe. No hardware improvement addresses this."),
            ("h3", "What a faster machine buys"),
            ("thm", ("Speed-up moves the wall",
                     "If a machine becomes `k` times faster, the largest instance solvable "
                     "in fixed time grows by a factor of `k` for a linear algorithm, by "
                     "`√k` for a quadratic one, and by only `log₂ k` ADDED for an "
                     "exponential one.")),
            ("proof", [
                "Linear: solving `n` in time `T` becomes solving `kn`. Quadratic: `n²` in "
                "time `T` becomes `kn²`, so the new size is `n√k`.",
                "Exponential: `2^n` in time `T` becomes `k · 2^n = 2^{n + log₂ k}`, so the "
                "size increases by `log₂ k` &mdash; an additive constant.",
            ]),
            ("p", "A thousandfold speed-up lets a linear algorithm handle a thousand times "
                  "more data, a quadratic one about 32 times more, and an exponential one "
                  "ten more items. That is the practical meaning of the polynomial/"
                  "exponential distinction, and it is why lesson 11 draws the line where it "
                  "does."),
            ("h3", "Lower-order terms"),
            ("math", [
                "f(n) = 3n² + 5n + 100",
                "",
                "n = 10       300 + 50 + 100 = 450        quadratic term is 67%",
                "n = 100    30 000 + 500 + 100 = 30 600   quadratic term is 98%",
                "n = 1000  3 000 000 + 5 000 + 100        quadratic term is 99.8%",
            ]),
            ("p", "So `3n² + 5n + 100` is `Θ(n²)`, and the constant 3 and the additions are "
                  "discarded &mdash; not because they do not exist, but because they do not "
                  "affect the comparison with an algorithm of a different growth rate."),
            ("p", "Constants do matter in practice, and the analysis knows it. An `n log n` "
                  "algorithm with a huge constant can lose to an `n²` one on every input "
                  "anyone will run, which is why real sort implementations switch to "
                  "insertion sort for small subarrays. Asymptotic analysis is a tool with "
                  "known limits, not a complete answer."),
        ],
        "lab": ("algorithm", {
            "mode": "growth", "n": 32,
            "panel_title": "The hierarchy, drawn",
            "panel_intro": "The vertical axis is logarithmic, so exponential growth is a "
                           "straight line. The table gives the values, which are more "
                           "persuasive than the picture.",
        }),
        "steps_title": "Comparing two algorithms",
        "steps_intro": "Growth first; constants only when the growth matches.",
        "steps": [
            ("Identify the dominant term",
             "The fastest-growing one. Everything else is discarded for the classification."),
            ("Compare the classes",
             "Consult the hierarchy. A different class settles the comparison for all "
             "large `n`."),
            ("If the classes match, look at constants",
             "Two `Θ(n log n)` algorithms are separated by their constants, and that "
             "requires measurement rather than analysis."),
            ("Check the sizes you actually face",
             "Asymptotics describe large `n`. If your inputs are always small, the "
             "crossover point matters more than the class."),
        ],
        "worked": {
            "title": "When the worse class wins",
            "intro": ["Algorithm A costs `100n log₂ n`; algorithm B costs `n²`."],
            "lines": [
                "A beats B when   100 n log₂ n  <  n²      i.e.  100 log₂ n < n",
                "",
                "n = 100      100·6.6 = 664   >   100        B wins",
                "n = 500      100·9.0 = 897   >   500        B wins",
                "n = 1000     100·10  = 1000  =  1000        equal",
                "n = 2000     100·11  = 1100  <  2000        A wins",
                "n = 10⁶      100·20  = 2000  <  10⁶         A wins by 500×",
                "",
                "The asymptotically better algorithm loses on every input below 1000.",
            ],
            "after": [
                "Both facts are true and neither is the whole story. `A` is asymptotically "
                "better and `B` is better on small inputs, and which matters depends on the "
                "data. Real sort implementations resolve exactly this by using insertion "
                "sort below a threshold of a few dozen elements."
            ],
        },
        "quiz_title": "Growth",
        "quiz": [
            {"q": "Which grows fastest?",
             "a": ["`n²`", "`n log n`", "`2ⁿ`", "`n³`"],
             "c": 2,
             "why": "Exponential eventually exceeds every polynomial. At `n = 100`, `2ⁿ` is "
                    "about `10³⁰` and `n³` is `10⁶`."},
            {"q": "A machine becomes 1000 times faster. An exponential algorithm can now handle:",
             "a": ["1000 times more data", "about 32 times more",
                   "about 10 more items", "the same amount"],
             "c": 2,
             "why": "`1000 ≈ 2¹⁰`, so the solvable size increases by about 10 &mdash; "
                    "additively. That is the practical meaning of exponential."},
            {"q": "`3n² + 5n + 100` grows like:",
             "a": ["`n`", "`n²`", "`n³`", "`3n²`"],
             "c": 1,
             "why": "The dominant term is quadratic. The constant 3 and the lower-order "
                    "terms do not affect the class."},
        ],
        "mistakes": [
            ("Comparing at one input size",
             "Growth is about the trend. An algorithm faster at `n = 100` may be hopeless "
             "at `n = 10⁶`."),
            ("Ignoring constants entirely",
             "They decide between algorithms of the same class, and they decide the "
             "crossover point between different classes."),
            ("Believing hardware fixes exponential cost",
             "A thousandfold speed-up buys about ten more items. The wall moves and does "
             "not disappear."),
        ],
        "standard": ("Finish when you can find a crossover point.",
                     "Determine where `50n log₂ n` overtakes `n²` and say which algorithm "
                     "you would use for `n = 200` and for `n = 10⁶`. Both answers are "
                     "defensible and they are different."),
        "note": "The distinction between polynomial and exponential is the one that "
                "organises complexity theory. Lesson 11 makes it the definition of "
                "tractability, and every argument there depends on the arithmetic in this "
                "lesson's tables.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "big-o-notation",
        "title": "Big-O, Big-Omega and Big-Theta",
        "module": "Analysis",
        "one_line": "Upper bound, lower bound, and both — each with explicit witnesses.",
        "summary": (
            "`f(n) = O(g(n))` asserts the existence of a constant `C` and a threshold `k` "
            "with `f(n) ≤ Cg(n)` beyond `k`. Proving it means producing them; that is the "
            "entire content of the definition."
        ),
        "key": [
            "O(g)   f ≤ C·g   for n ≥ k          upper bound",
            "Ω(g)   f ≥ C·g   for n ≥ k          lower bound",
            "Θ(g)   both                          tight",
            "the proof IS the pair (C, k)",
        ],
        "key_label": "Three relations, one shape",
        "concepts_intro": (
            "Each of the three is an existence claim, and each is proved by exhibiting "
            "the witnesses."
        ),
        "concepts": [
            ("Big-O is an upper bound and may be loose",
             "`n = O(n²)` is true and uninformative. \"Is `O(n²)`\" does not mean \"grows "
             "like `n²`\"."),
            ("`Θ` is the tight statement",
             "Both bounds. It is what should be claimed when the growth is actually known, "
             "and the one people usually mean when they say `O`."),
            ("The witnesses are the proof",
             "A `C` and a `k` that work. Anything else is a restatement of the claim."),
        ],
        "read_title": "The three notations",
        "read_intro": "Definitions, worked proofs, and the properties that shorten later work.",
        "body": [
            ("def", ("Big-O",
                     "`f(n) = O(g(n))` means there are constants `C &gt; 0` and `k` such "
                     "that `|f(n)| ≤ C|g(n)|` for every `n ≥ k`. The pair `(C, k)` is a "
                     "<strong>witness</strong>.")),
            ("def", ("Big-Omega and Big-Theta",
                     "`f(n) = Ω(g(n))` means `|f(n)| ≥ C|g(n)|` for some `C &gt; 0` and all "
                     "`n ≥ k`. `f(n) = Θ(g(n))` means both, so `f` and `g` grow at the same "
                     "rate.")),
            ("p", "The `=` is traditional and misleading: these are set memberships, and "
                  "`O(g)` is the class of functions bounded above by a multiple of `g`. "
                  "`f(n) = O(g(n))` should be read \"`f` is in `O(g)`\", and it is not "
                  "symmetric."),
            ("h3", "Proving a bound"),
            ("example", ("`3n² + 5n + 100 = O(n²)`",
                         "For `n ≥ 1` we have `n ≤ n²` and `1 ≤ n²`, so "
                         "`3n² + 5n + 100 ≤ 3n² + 5n² + 100n² = 108n²`. The witnesses are "
                         "`C = 108` and `k = 1`. Sharper choices exist &mdash; at `n ≥ 10`, "
                         "`C = 5` works &mdash; and any valid pair proves the claim.")),
            ("example", ("`n² ≠ O(n)`",
                         "Suppose `n² ≤ Cn` for all `n ≥ k`. Dividing by `n` gives `n ≤ C` "
                         "for all `n ≥ k`, which is false for `n &gt; max(C, k)`. No pair "
                         "of witnesses exists.")),
            ("p", "That is the shape of a disproof: assume witnesses and derive a "
                  "contradiction. It is a direct proof of a negation, and course 1 lesson "
                  "13 is the technique."),
            ("h3", "Useful properties"),
            ("math", [
                "transitive       f = O(g),  g = O(h)   ⟹   f = O(h)",
                "sum              f₁ = O(g₁), f₂ = O(g₂) ⟹ f₁+f₂ = O(max(g₁,g₂))",
                "product          f₁ = O(g₁), f₂ = O(g₂) ⟹ f₁·f₂ = O(g₁·g₂)",
                "constants        c·f = O(f)   for any constant c > 0",
                "polynomials      aₖnᵏ + … + a₀ = Θ(nᵏ)",
                "logs             log_a n = Θ(log_b n)   — the base is a constant factor",
            ]),
            ("p", "The last line is why the base of a logarithm is never written in a "
                  "complexity class: `log₂ n` and `log₁₀ n` differ by the constant factor "
                  "`log₂ 10`, which `Θ` discards."),
            ("p", "The sum rule is what makes analysis of straight-line code easy: a "
                  "sequence of blocks costs the maximum of their costs, not the sum, in "
                  "asymptotic terms."),
            ("h3", "The common misuse"),
            ("p", "\"Quicksort is `O(n log n)`\" is a widespread and false statement: "
                  "quicksort's worst case is `Θ(n²)`. What is true is that its "
                  "<em>average</em> case is `Θ(n log n)`. Big-O is an upper bound and "
                  "quoting it without saying which case is being bounded loses the "
                  "distinction the notation exists to express."),
            ("p", "Similarly \"at least `O(n)`\" is meaningless &mdash; `O` is already an "
                  "upper bound &mdash; and \"`Ω`\" is the word wanted there."),
        ],
        "lab": ("algorithm", {
            "mode": "witness", "n": 16,
            "panel_title": "Find the witnesses",
            "panel_intro": "The lab searches for a `C` and a `k` that work, and reports "
                           "them. When no pair in its range works it says so rather than "
                           "inventing one &mdash; and that is evidence the relation is "
                           "false.",
        }),
        "steps_title": "Proving a big-O claim",
        "steps_intro": "Bound each term, then collect.",
        "steps": [
            ("Bound every term by a multiple of `g(n)`",
             "For `n ≥ 1`, lower powers are bounded by higher ones. That is usually the "
             "whole argument."),
            ("Add the coefficients to get `C`",
             "Any valid `C` proves the claim. Optimising it is not required and rarely "
             "worth the effort."),
            ("State the threshold `k`",
             "The bound need only hold beyond it, which is what lets small-`n` behaviour "
             "be ignored."),
            ("To disprove, assume witnesses and derive a contradiction",
             "Divide through by `g(n)` and show the resulting bound on `n` is impossible."),
        ],
        "worked": {
            "title": "Two proofs",
            "intro": ["One positive, one negative."],
            "lines": [
                "CLAIM   n² + 2n + 1 = O(n²)",
                "",
                "   for n ≥ 1:   2n ≤ 2n²   and   1 ≤ n²",
                "   so  n² + 2n + 1 ≤ n² + 2n² + n² = 4n²",
                "",
                "   WITNESSES  C = 4,  k = 1.                                  ∎",
                "",
                "CLAIM   2ⁿ ≠ O(n¹⁰⁰)",
                "",
                "   Suppose 2ⁿ ≤ C·n¹⁰⁰ for all n ≥ k.",
                "   Then 2ⁿ / n¹⁰⁰ ≤ C, a bounded quantity.",
                "   But 2ⁿ / n¹⁰⁰ → ∞, since exponential growth eventually",
                "   dominates any fixed power.  Contradiction.               ∎",
            ],
            "after": [
                "The first proof produced a specific pair, which is what the definition "
                "asks for. The second assumed a pair existed and refuted it. Every big-O "
                "argument on this course has one of these two shapes."
            ],
        },
        "quiz_title": "Asymptotic notation",
        "quiz": [
            {"q": "`f(n) = O(g(n))` means:",
             "a": ["`f` grows exactly like `g`",
                   "there exist `C, k` with `f(n) ≤ Cg(n)` for all `n ≥ k`",
                   "`f` is smaller than `g`",
                   "`f` and `g` are equal"],
             "c": 1,
             "why": "An upper bound with witnesses. \"Exactly like\" is `Θ`."},
            {"q": "Is `n = O(n²)` true?",
             "a": ["No", "Yes, but it is a loose bound",
                   "Only for `n &gt; 1`", "Only if `n` is large"],
             "c": 1,
             "why": "`n ≤ n²` for `n ≥ 1`, so `C = 1`, `k = 1` works. Big-O is an upper "
                    "bound and may be far from tight."},
            {"q": "\"Quicksort is `O(n log n)`\" is:",
             "a": ["correct",
                   "false — its worst case is `Θ(n²)`; the AVERAGE case is `Θ(n log n)`",
                   "correct only for sorted input",
                   "meaningless"],
             "c": 1,
             "why": "The unqualified claim asserts an upper bound on every case, and "
                    "quicksort's worst case is quadratic."},
        ],
        "mistakes": [
            ("Claiming `O` where `Θ` is meant",
             "`n = O(n²)` is true and says almost nothing. If the growth is known, say `Θ`."),
            ("Omitting which case is being bounded",
             "Worst, average and best case are different functions. \"Quicksort is "
             "`O(n log n)`\" is false; \"its average case is\" is true."),
            ("Writing \"at least `O(n)`\"",
             "`O` is already an upper bound. The intended word is `Ω`."),
        ],
        "standard": ("Finish when you produce witnesses without being asked.",
                     "Prove `5n³ + 2n² + n = O(n³)` by exhibiting a `C` and a `k`, and then "
                     "prove `n³ ≠ O(n²)` by contradiction. The two shapes cover almost "
                     "every claim you will meet."),
        "note": "The notation is due to Bachmann and Landau, from analytic number theory, "
                "and Knuth introduced it to algorithm analysis. The abuse of `=` is his "
                "too, and it is now unfixable.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "analysing-iterative-algorithms",
        "title": "Analysing Iterative Algorithms",
        "module": "Analysis",
        "one_line": "Count the dominant operation as a function of the input size.",
        "summary": (
            "Nested loops multiply, sequential blocks take the maximum, and a loop whose "
            "bound depends on the outer index gives a sum &mdash; which is course 3's "
            "summation formulas doing the work."
        ),
        "key": [
            "sequential blocks     add, so the class is the MAXIMUM",
            "nested loops          multiply the iteration counts",
            "dependent inner bound  gives a SUM — evaluate it",
            "worst / average / best case are different functions",
        ],
        "key_label": "Three loop patterns",
        "concepts_intro": (
            "Analysis of a loop is counting how many times the body runs, which is "
            "usually a sum course 3 already evaluated."
        ),
        "concepts": [
            ("Choose one dominant operation",
             "Comparisons for a search or sort, multiplications for arithmetic. Counting "
             "everything changes only the constant."),
            ("Nested loops multiply, sequences take the maximum",
             "Two independent nested loops give the product; two blocks in sequence give "
             "the sum, which asymptotically is the larger."),
            ("A dependent inner bound gives a sum",
             "`for i = 1 to n: for j = 1 to i` runs `Σ i = n(n+1)/2` times, which is "
             "`Θ(n²)` &mdash; course 3 lesson 3's formula."),
        ],
        "read_title": "Counting operations",
        "read_intro": "The three patterns, the case distinction, and four worked analyses.",
        "body": [
            ("h3", "Sequential blocks"),
            ("math", [
                "for i = 1 to n:      … n operations",
                "for j = 1 to n²:     … n² operations",
                "",
                "total  n + n²  =  Θ(n²)",
            ]),
            ("p", "Adding the costs and taking the dominant term. This is the sum rule of "
                  "lesson 4, and it means a fast block before a slow one contributes "
                  "nothing asymptotically."),
            ("h3", "Independent nested loops"),
            ("math", [
                "for i = 1 to n:",
                "    for j = 1 to m:",
                "        constant work",
                "",
                "total  n · m       and if m = n,  Θ(n²)",
            ]),
            ("h3", "Dependent nested loops"),
            ("math", [
                "for i = 1 to n:",
                "    for j = 1 to i:",
                "        constant work",
                "",
                "total  Σ_{i=1}^{n} i  =  n(n+1)/2  =  Θ(n²)",
            ]),
            ("p", "The constant differs from the independent case &mdash; half as many "
                  "iterations &mdash; and the class does not. This is where course 3 "
                  "lesson 3's summation formulas earn their place, and where a triple "
                  "dependent nest gives `Σ i² = Θ(n³)`."),
            ("h3", "Loops that multiply or divide"),
            ("math", [
                "i = 1",
                "while i < n:  i = i · 2",
                "",
                "i takes the values 1, 2, 4, 8, …, so the loop runs ⌈log₂ n⌉ times.",
                "",
                "for i = 1 to n:",
                "    j = 1",
                "    while j < n:  j = j · 2",
                "",
                "total  n · log₂ n  =  Θ(n log n)",
            ]),
            ("p", "Any loop whose counter is multiplied or divided by a constant runs "
                  "logarithmically many times. Recognising that pattern is what identifies "
                  "the `log` factors in an analysis."),
            ("h3", "Worst, average and best case"),
            ("def", ("The three cases",
                     "<strong>Worst case</strong> is the maximum cost over inputs of size "
                     "`n`; <strong>best case</strong> the minimum; <strong>average "
                     "case</strong> the expectation over some distribution of inputs.")),
            ("math", [
                "linear search      best 1        worst n         average about n/2",
                "insertion sort     best n        worst n²/2      average n²/4",
                "quicksort          best n log n  worst n²        average n log n",
                "merge sort         n log n       n log n         n log n",
                "bubble sort        n²/2          n²/2            n²/2   — data-independent",
            ]),
            ("p", "Two things stand out. Merge sort and bubble sort have identical bounds "
                  "in all three cases, for opposite reasons &mdash; one is always efficient "
                  "and the other always wasteful, and neither looks at the data to decide "
                  "how much work to do. And quicksort's average and worst cases differ by a "
                  "whole class, which is why the unqualified `O(n log n)` claim of lesson 4 "
                  "is wrong."),
            ("p", "The average case needs a distribution over inputs, and stating it is "
                  "part of the claim. \"Average case `Θ(n log n)`\" for quicksort assumes "
                  "all input orderings equally likely, which real data frequently violates "
                  "&mdash; nearly sorted input is the classic bad case for a naive pivot."),
        ],
        "lab": ("algorithm", {
            "mode": "sort", "n": 24,
            "panel_title": "Predicted and measured",
            "panel_intro": "Bubble sort's count matches `n(n−1)/2` exactly, because its "
                           "loops never look at the data. Insertion sort's does not, which "
                           "is the whole difference between them.",
        }),
        "steps_title": "Analysing a loop nest",
        "steps_intro": "Innermost outward.",
        "steps": [
            ("Choose the operation to count",
             "The one performed most often: comparisons, multiplications, array accesses. "
             "Others differ by a constant factor."),
            ("Count the innermost loop's iterations",
             "As a function of the outer indices. This is where the dependence shows."),
            ("Work outward, summing or multiplying",
             "Independent bounds multiply; a dependent bound gives a sum to evaluate with "
             "course 3's formulas."),
            ("State which case you have analysed",
             "Worst, best or average, and for the average say what distribution. An "
             "unqualified bound is ambiguous."),
        ],
        "worked": {
            "title": "Three nests",
            "intro": ["Same shape, three different answers."],
            "lines": [
                "A.  for i = 1 to n:",
                "        for j = 1 to n:",
                "            for k = 1 to n:  op",
                "    independent nests:  n · n · n  =  Θ(n³)",
                "",
                "B.  for i = 1 to n:",
                "        for j = i to n:  op",
                "    inner runs n − i + 1 times",
                "    Σ_{i=1}^{n} (n − i + 1) = Σ_{m=1}^{n} m = n(n+1)/2 = Θ(n²)",
                "",
                "C.  for i = 1 to n:",
                "        j = n",
                "        while j > 1:  j = j / 2;  op",
                "    inner runs ⌊log₂ n⌋ times, independent of i",
                "    total  Θ(n log n)",
            ],
            "after": [
                "B is the one worth checking: reindexing the sum by `m = n − i + 1` turns "
                "it into `Σ m`, which course 3 evaluated. Recognising that substitution is "
                "most of the technique for dependent nests."
            ],
        },
        "quiz_title": "Iterative analysis",
        "quiz": [
            {"q": "`for i = 1 to n: for j = 1 to i: op` performs how many operations?",
             "a": ["`n`", "`n²`", "`n(n+1)/2`, which is `Θ(n²)`", "`n log n`"],
             "c": 2,
             "why": "The inner loop runs `i` times, so the total is `Σ i = n(n+1)/2` "
                    "&mdash; half of `n²`, and the same class."},
            {"q": "A loop `while i &lt; n: i = i · 3` runs:",
             "a": ["`n` times", "`n/3` times", "about `log₃ n` times", "3 times"],
             "c": 2,
             "why": "The counter is multiplied by a constant each time, so it reaches `n` "
                    "after logarithmically many steps."},
            {"q": "Bubble sort's comparison count is the same in all three cases because:",
             "a": ["it is optimal",
                   "its loop bounds do not depend on the data",
                   "it is randomised",
                   "the count is wrong"],
             "c": 1,
             "why": "The two loops run to fixed limits regardless of what the comparisons "
                    "find. Insertion sort's inner loop stops early, so its count varies."},
        ],
        "mistakes": [
            ("Multiplying loop bounds when the inner one depends on the outer",
             "That over-counts by a factor of 2 for a triangular nest. Write the sum and "
             "evaluate it."),
            ("Adding nested loop costs",
             "Nesting multiplies. Sequential blocks add, and the two are easy to confuse "
             "when reading quickly."),
            ("Not saying which case",
             "Insertion sort is `Θ(n)` on sorted input and `Θ(n²)` on reversed input. An "
             "unqualified bound is ambiguous between them."),
        ],
        "standard": ("Finish when a triangular nest gives you a sum, not a product.",
                     "Analyse `for i = 1 to n: for j = 1 to i: for k = 1 to j: op` and get "
                     "`Σ_i Σ_j j`, which is `Θ(n³)` with a constant of `1/6`. The "
                     "reindexing is the skill."),
        "note": "Modern hardware complicates all of this: cache behaviour can make an "
                "algorithm with more operations run faster, because memory locality "
                "dominates. Operation counting remains the right first analysis and is not "
                "the last word.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "searching-and-sorting",
        "title": "Searching and Sorting",
        "module": "Analysis",
        "one_line": "The standard algorithms, and the lower bound nobody can beat.",
        "summary": (
            "Linear and binary search, three quadratic sorts and merge sort &mdash; and "
            "the proof that no comparison sort can do better than `n log n`, which is a "
            "statement about the problem rather than about any algorithm."
        ),
        "key": [
            "linear search   Θ(n)          binary search  Θ(log n),  needs SORTED input",
            "bubble, selection, insertion  Θ(n²)",
            "merge sort      Θ(n log n)    always",
            "LOWER BOUND: every comparison sort needs Ω(n log n) comparisons",
        ],
        "key_label": "Algorithms, and a limit",
        "concepts_intro": (
            "Six algorithms, and then a theorem about every possible algorithm of a "
            "certain kind."
        ),
        "concepts": [
            ("Binary search needs sorted input",
             "That is what licenses discarding half the array. On unsorted data it "
             "terminates and returns wrong answers."),
            ("The quadratic sorts differ in their constants and their adaptivity",
             "Insertion sort is `Θ(n)` on nearly sorted data; bubble and selection sort do "
             "the same work regardless."),
            ("`n log n` is a lower bound, not a target",
             "A decision-tree argument shows no comparison sort can beat it. It is a "
             "statement about the problem."),
        ],
        "read_title": "The standard algorithms",
        "read_intro": "Searching, sorting, and the information-theoretic limit.",
        "body": [
            ("h3", "Searching"),
            ("math", [
                "linear search   check each in turn         Θ(n) worst      any array",
                "binary search   halve the range each step  Θ(log n)        SORTED array",
            ]),
            ("thm", ("Binary search cost",
                     "On a sorted array of `n` elements, binary search performs at most "
                     "`⌊log₂ n⌋ + 1` comparisons.")),
            ("proof", [
                "Each comparison at least halves the range: from `m` candidates it leaves "
                "at most `⌊m/2⌋`. Starting at `n`, after `t` comparisons at most "
                "`⌊n/2^t⌋` remain, and the search ends when that reaches 0.",
                "So `t ≤ log₂ n + 1`.",
            ]),
            ("p", "Sorting first costs `Θ(n log n)`, so binary search pays for itself only "
                  "across many searches on the same data &mdash; roughly, once the number "
                  "of searches exceeds `log n`."),
            ("h3", "Sorting"),
            ("math", [
                "bubble      compare adjacent, swap, repeat        Θ(n²)  always",
                "selection   find the minimum, place it, repeat    Θ(n²)  always",
                "insertion   insert each into the sorted prefix    Θ(n²) worst, Θ(n) best",
                "merge       split, sort each half, merge          Θ(n log n) always",
            ]),
            ("p", "Insertion sort is the interesting quadratic one: its inner loop stops as "
                  "soon as it finds a smaller element, so on nearly sorted data it does "
                  "almost no work. That adaptivity is why real implementations use it below "
                  "a size threshold."),
            ("p", "Merge sort satisfies `T(n) = 2T(n/2) + n`, which lesson 7's master "
                  "theorem solves as `Θ(n log n)`. Its cost does not depend on the data at "
                  "all, and it needs `Θ(n)` extra space, which is its one drawback."),
            ("h3", "The lower bound"),
            ("thm", ("Comparison sorting requires `Ω(n log n)`",
                     "Any sorting algorithm that gets information about the input only by "
                     "comparing pairs of elements must perform `Ω(n log n)` comparisons in "
                     "the worst case.")),
            ("proof", [
                "Model the algorithm as a decision tree: each internal node is a "
                "comparison with two outcomes, and each leaf is one possible output "
                "ordering. To sort correctly the tree must have at least `n!` leaves, one "
                "per permutation of the input.",
                "A binary tree with `L` leaves has height at least `log₂ L` (course 7 "
                "lesson 10). So the height is at least `log₂(n!)`.",
                "By Stirling's approximation `log₂(n!) = Θ(n log n)`, and the height is the "
                "worst-case number of comparisons.",
            ]),
            ("p", "This is a genuine impossibility result and it is worth distinguishing "
                  "from a failure of ingenuity: no comparison sort will ever beat "
                  "`n log n`, and merge sort therefore achieves the optimum. Course 4's "
                  "count of permutations and course 7's tree height bound are both doing "
                  "work in the proof."),
            ("p", "Sorts that beat the bound exist and they do not compare. Counting sort "
                  "and radix sort use the values themselves as indices and run in `Θ(n)` "
                  "under assumptions about the key range. They do not contradict the "
                  "theorem; they fall outside its hypothesis."),
        ],
        "lab": ("algorithm", {
            "mode": "sort", "n": 24,
            "panel_title": "Three sorts, counted",
            "panel_intro": "The counts come from running each algorithm on the same array. "
                           "Compare merge sort's column with `n log₂ n` &mdash; it stays "
                           "below, as the analysis predicts.",
        }),
        "steps_title": "Choosing a search or a sort",
        "steps_intro": "The data decides.",
        "steps": [
            ("Is the data sorted, and will it be searched often?",
             "If both, sort once and binary search. If neither, linear search is fine and "
             "simpler."),
            ("How large is the input?",
             "Below a few dozen, insertion sort beats merge sort on constants. Above that "
             "the class dominates."),
            ("Is the data nearly sorted?",
             "Insertion sort is `Θ(n)` there and merge sort is still `Θ(n log n)`. "
             "Adaptivity is worth real money on partially ordered data."),
            ("Is extra space available?",
             "Merge sort needs `Θ(n)` of it. Where that is unacceptable, heapsort achieves "
             "`Θ(n log n)` in place."),
        ],
        "worked": {
            "title": "Comparison counts at `n = 16`",
            "intro": ["Measured by running each algorithm on the same shuffled array."],
            "lines": [
                "bubble      120        = n(n−1)/2, exactly — data-independent",
                "insertion    62        data-dependent; 15 on sorted input",
                "merge        48        below n log₂ n = 64, as the analysis allows",
                "",
                "binary search worst case:  ⌊log₂ 16⌋ + 1 = 5",
                "linear search worst case:  16",
                "",
                "At n = 1000:",
                "   bubble ≈ 500 000     merge ≈ 8 700     binary search ≈ 10",
            ],
            "after": [
                "Merge sort's 48 comparisons is below `n log₂ n` because the true bound is "
                "`n log₂ n − n + 1`, and the analysis quotes the leading term. Measured "
                "counts sitting under a predicted curve is normal and not an error."
            ],
        },
        "quiz_title": "Searching and sorting",
        "quiz": [
            {"q": "Binary search requires:",
             "a": ["a linked list", "sorted input", "distinct elements", "extra space"],
             "c": 1,
             "why": "Sortedness is what licenses discarding half the range. On unsorted "
                    "data it terminates and is wrong."},
            {"q": "No comparison sort can do better than:",
             "a": ["`Θ(n)`", "`Ω(n log n)`", "`Θ(n²)`", "there is no limit"],
             "c": 1,
             "why": "The decision tree needs `n!` leaves and a binary tree with `n!` leaves "
                    "has height `Θ(n log n)`."},
            {"q": "Counting sort runs in `Θ(n)`. Does it contradict the lower bound?",
             "a": ["Yes", "No — it does not use comparisons",
                   "Only for small `n`", "The bound is wrong"],
             "c": 1,
             "why": "The theorem constrains comparison sorts. Counting sort uses values as "
                    "indices and falls outside its hypothesis."},
        ],
        "mistakes": [
            ("Binary searching unsorted data",
             "It terminates and returns confident wrong answers, which is the most "
             "dangerous failure mode."),
            ("Believing the lower bound applies to all sorting",
             "It applies to comparison sorts. Counting and radix sort beat it under "
             "assumptions about the keys."),
            ("Ignoring adaptivity",
             "Insertion sort is linear on nearly sorted data. On partially ordered inputs "
             "that is worth more than a better asymptotic class."),
        ],
        "standard": ("Finish when you can state the lower bound and why it holds.",
                     "Explain in three sentences why `n!` leaves force `Θ(n log n)` height. "
                     "The argument uses course 4's permutation count and course 7's tree "
                     "bound, and it is the cleanest impossibility proof on this path."),
        "note": "Timsort, the default sort in Python and Java, is merge sort with insertion "
                "sort for small runs and special handling for existing sorted runs. Every "
                "element of that design is a response to something in this lesson.",
    },
]
