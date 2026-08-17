"""Course 3, lessons 07-12 — structural induction, algorithms, recurrences."""

LESSONS = [
    # ---------------------------------------------------------------- 07
    {
        "slug": "structural-induction",
        "title": "Structural Induction",
        "module": "Recursion",
        "one_line": "Induction over how an object was built, not over a number.",
        "summary": (
            "When a set is defined recursively, proving something about all its members "
            "means proving it for the base objects and showing each construction rule "
            "preserves it. No numeric parameter is needed."
        ),
        "key": [
            "BASE   prove P for every object given outright",
            "STEP   assume P for the parts, prove P for the object built from them",
            "Valid because every object is built in finitely many steps.",
            "Applies to strings, trees, formulas — anything with a recursive definition.",
        ],
        "key_label": "Induction over structure",
        "concepts_intro": (
            "Structural induction is ordinary induction over the number of construction "
            "steps, with the counting left implicit."
        ),
        "concepts": [
            ("The cases mirror the definition",
             "One base case per base clause, one step per recursive clause. If the "
             "definition has three rules the proof has three parts."),
            ("The hypothesis is about the parts",
             "For a tree built from `L` and `R`, you assume the claim for `L` and for `R` "
             "and prove it for the whole. That is strong induction on structure."),
            ("No size parameter is needed",
             "Trees and formulas have no obvious `n`. Structural induction sidesteps the "
             "question by inducting on how the object was assembled."),
        ],
        "read_title": "Induction over a recursive structure",
        "read_intro": "The principle, why it is valid, and three applications.",
        "body": [
            ("thm", ("Structural induction",
                     "Let `S` be defined recursively. To prove `P(x)` for every `x ∈ S`, "
                     "prove `P` for each object given by a base clause, and prove that "
                     "each recursive clause preserves `P` &mdash; that is, if `P` holds "
                     "for the parts, it holds for the object built from them.")),
            ("p", "Validity comes straight from the definition. Every member of `S` is "
                  "produced in finitely many steps, so induct on that number: at zero "
                  "steps the object is a base object, and each further step is a recursive "
                  "clause applied to objects built in fewer steps."),
            ("example", ("Parenthesis strings are balanced",
                         "Recall the definition: the empty string is well formed; if `s` "
                         "is, so is `(s)`; if `s` and `t` are, so is `st`. Claim: every "
                         "well-formed string has equally many left and right parentheses.")),
            ("proof", [
                "<strong>Base.</strong> The empty string has 0 of each.",
                "<strong>Clause `(s)`.</strong> Assume `s` has `m` of each. Then `(s)` has "
                "`m + 1` of each.",
                "<strong>Clause `st`.</strong> Assume `s` has `m` of each and `t` has `p` "
                "of each. Then `st` has `m + p` of each.",
                "Every well-formed string is built by these clauses, so the property holds "
                "throughout.",
            ]),
            ("p", "Three parts, matching the three clauses. Missing one &mdash; forgetting "
                  "the concatenation clause, say &mdash; would leave a whole family of "
                  "strings unproved, and the omission is invisible unless the definition "
                  "is beside the proof."),
            ("h3", "Trees"),
            ("def", ("Height and node count",
                     "For a binary tree: `h(empty) = −1` and "
                     "`h(node(v, L, R)) = 1 + max(h(L), h(R))`. "
                     "`n(empty) = 0` and `n(node(v, L, R)) = 1 + n(L) + n(R)`.")),
            ("thm", ("A binary tree of height `h` has at most `2^{h+1} − 1` nodes",
                     "For every binary tree `T`, `n(T) ≤ 2^{h(T)+1} − 1`.")),
            ("proof", [
                "<strong>Base.</strong> The empty tree has `h = −1` and `n = 0`, and "
                "`2⁰ − 1 = 0`.",
                "<strong>Step.</strong> Let `T = node(v, L, R)` and assume the bound for "
                "`L` and `R`. Write `h = h(T)`, so `h(L) ≤ h − 1` and `h(R) ≤ h − 1`.",
                "Then `n(T) = 1 + n(L) + n(R) ≤ 1 + (2^h − 1) + (2^h − 1) = 2·2^h − 1 "
                "= 2^{h+1} − 1`.",
            ]),
            ("p", "Both subtrees needed the hypothesis, which makes this structural "
                  "induction with two recursive parts &mdash; the structural analogue of "
                  "the two-term recurrence that forced strong induction in lesson 5."),
            ("h3", "Formulas"),
            ("p", "The well-formed formulas of course 1 are a recursively defined set: a "
                  "variable is a formula; if `A` is a formula so is `¬A`; if `A` and `B` "
                  "are, so is `(A ∧ B)`, and similarly for the other binary connectives. "
                  "Structural induction over that definition proves the syntactic facts "
                  "course 1 used without proof."),
            ("example", ("Parentheses balance in every formula",
                         "Base: a variable has none of either. Negation adds none. Each "
                         "binary clause adds one of each. So every well-formed formula has "
                         "matching parentheses &mdash; which is what makes the parser in "
                         "the truth-table lab able to reject the strings that are not "
                         "formulas.")),
        ],
        "lab": ("recurrence", {
            "preset": "fib",
            "panel_title": "Two parts, two base cases",
            "panel_intro": "Fibonacci is the numeric shadow of a two-part structure: each "
                           "value depends on two smaller ones, exactly as a binary tree "
                           "node depends on two subtrees.",
        }),
        "steps_title": "Writing a structural induction proof",
        "steps_intro": "Put the definition beside the proof and match them clause for clause.",
        "steps": [
            ("List the clauses of the definition",
             "Base clauses and recursive clauses. The proof will have exactly this many "
             "parts, and matching them is how you know none was skipped."),
            ("Prove the claim for each base object",
             "Usually immediate. Do it anyway, in writing."),
            ("For each recursive clause, assume the claim for the parts",
             "Then establish it for the object constructed. This is the inductive "
             "hypothesis, and there may be more than one part."),
            ("Check nothing else is in the set",
             "The closure sentence of the definition is what makes these cases exhaustive. "
             "Without it the proof covers a subset."),
        ],
        "worked": {
            "title": "Every full binary tree has an odd number of nodes",
            "intro": ["A tree is full when every node has either 0 or 2 children."],
            "lines": [
                "Definition:  BASE       a single node is a full binary tree",
                "             RECURSIVE  if L and R are full binary trees, then the tree",
                "                        with a new root and subtrees L, R is one",
                "",
                "BASE   a single node has 1 node.  Odd.        ✓",
                "",
                "STEP   Assume L has n(L) nodes and R has n(R), both odd.",
                "       The new tree has  1 + n(L) + n(R)  nodes.",
                "       odd + odd = even,  and  1 + even = odd.               ✓",
                "",
                "Every full binary tree is built by these two clauses, so every one",
                "has an odd number of nodes.        ∎",
            ],
            "after": [
                "The parity argument is course 1 lesson 12's result reused: the sum of two "
                "odd integers is even. Structural induction supplied the two odd numbers; "
                "elementary arithmetic finished the job."
            ],
        },
        "quiz_title": "Structural induction",
        "quiz": [
            {"q": "How many parts does a structural induction proof have?",
             "a": ["Always two",
                   "One per clause of the recursive definition",
                   "One per element of the set",
                   "Three"],
             "c": 1,
             "why": "Base clauses give base cases and recursive clauses give inductive "
                    "steps. Skipping one leaves a family of objects unproved."},
            {"q": "For a tree `node(v, L, R)`, the inductive hypothesis is:",
             "a": ["the claim for `L` only",
                   "the claim for the whole tree",
                   "the claim for both `L` and `R`",
                   "the claim for trees of smaller height"],
             "c": 2,
             "why": "The object is built from both subtrees, so both are available as "
                    "hypotheses &mdash; and the proof will generally need both."},
            {"q": "Structural induction is valid because:",
             "a": ["it is an axiom",
                   "every object is built from a base in finitely many steps",
                   "the set is finite",
                   "trees are countable"],
             "c": 1,
             "why": "That finiteness is what lets it be reduced to ordinary induction on "
                    "the number of construction steps."},
        ],
        "mistakes": [
            ("Omitting a clause",
             "The concatenation clause for strings and the second subtree for trees are "
             "the ones usually forgotten. Write the definition out first."),
            ("Using the hypothesis for only one part",
             "A binary construction gives you two hypotheses. Using one and asserting the "
             "other is a gap."),
            ("Assuming the set has no other members",
             "That is the closure sentence of the definition, and if the definition omits "
             "it the proof cannot supply it."),
        ],
        "standard": ("Finish when you can match a proof to a definition clause by clause.",
                     "Prove that every well-formed parenthesis string has no proper prefix "
                     "with more right than left parentheses. Three clauses, three parts, "
                     "and the concatenation case is the one that needs thought."),
        "note": "Structural induction is how properties of programs and of syntax are "
                "proved: type soundness, evaluation termination and compiler correctness "
                "are all structural inductions over a recursively defined language.",
    },
    # ---------------------------------------------------------------- 08
    {
        "slug": "recursive-algorithms",
        "title": "Recursive Algorithms and Correctness",
        "module": "Recursion",
        "one_line": "An algorithm that calls itself, and the induction that proves it right.",
        "summary": (
            "A recursive algorithm mirrors a recursive definition, and its correctness "
            "proof mirrors an induction. Two obligations: it terminates, and it returns "
            "the right answer when it does."
        ),
        "key": [
            "TERMINATION  every call reduces a quantity bounded below",
            "CORRECTNESS  base case right, and recursive case right GIVEN the calls are",
            "Both are needed. Either alone is worthless.",
            "The proof is strong induction on the size of the input.",
        ],
        "key_label": "Two separate obligations",
        "concepts_intro": (
            "Correctness of a recursive algorithm splits cleanly in two, and the split "
            "is what makes the proofs short."
        ),
        "concepts": [
            ("Termination is a separate proof",
             "Find a quantity that strictly decreases at every call and cannot decrease "
             "forever. Usually the input size; sometimes something less obvious."),
            ("Correctness assumes the recursive calls work",
             "That is the inductive hypothesis. You do not trace the recursion; you assume "
             "smaller inputs are handled and check the combination."),
            ("A correct algorithm that never stops is not correct",
             "And a terminating one that returns nonsense is not either. The two "
             "obligations are independent."),
        ],
        "read_title": "Recursive algorithms",
        "read_intro": "Three algorithms, each with both obligations discharged.",
        "body": [
            ("h3", "Factorial"),
            ("math", [
                "FACTORIAL(n):",
                "    if n = 0:  return 1",
                "    else:      return n × FACTORIAL(n − 1)",
            ]),
            ("p", "<strong>Termination.</strong> Each call has argument one smaller, and "
                  "the argument is a natural number, so it cannot decrease past 0. The "
                  "sequence of calls is finite."),
            ("p", "<strong>Correctness.</strong> By induction on `n`. At `n = 0` the "
                  "algorithm returns 1, which is `0!`. For `n ≥ 1`, assume the call "
                  "`FACTORIAL(n−1)` returns `(n−1)!`; the algorithm returns "
                  "`n · (n−1)! = n!` by the recursive definition of factorial."),
            ("h3", "Binary search"),
            ("math", [
                "SEARCH(A, lo, hi, x):        # A sorted ascending",
                "    if lo > hi:      return NOT FOUND",
                "    mid = ⌊(lo + hi)/2⌋",
                "    if A[mid] = x:   return mid",
                "    if A[mid] < x:   return SEARCH(A, mid + 1, hi, x)",
                "    else:            return SEARCH(A, lo, mid − 1, x)",
            ]),
            ("p", "<strong>Termination.</strong> The quantity `hi − lo + 1` &mdash; the "
                  "size of the range &mdash; strictly decreases at every recursive call, "
                  "because `mid` is inside the range and is excluded from both "
                  "subproblems. It is bounded below by 0, at which point the first line "
                  "returns."),
            ("p", "<strong>Correctness.</strong> By strong induction on the range size. "
                  "If the range is empty, `x` is not in it and NOT FOUND is right. "
                  "Otherwise, if `A[mid] = x` the index is right. If `A[mid] &lt; x` then, "
                  "because `A` is sorted, every index at or below `mid` holds a value "
                  "less than `x`, so `x` can only be in the upper half; the hypothesis "
                  "says the recursive call handles that smaller range correctly. The "
                  "other branch is symmetric."),
            ("p", "The sortedness assumption is doing the real work: it is what licenses "
                  "discarding half the array. Applied to unsorted data the algorithm still "
                  "terminates and returns confident wrong answers, which is the most "
                  "dangerous kind of failure."),
            ("h3", "Merge sort"),
            ("math", [
                "MERGESORT(A):",
                "    if |A| ≤ 1:  return A",
                "    split A into halves L and R",
                "    return MERGE( MERGESORT(L), MERGESORT(R) )",
            ]),
            ("p", "<strong>Termination.</strong> Each call receives an array of size at "
                  "most `⌈n/2⌉ &lt; n` for `n ≥ 2`, and size is a natural number."),
            ("p", "<strong>Correctness.</strong> Strong induction on `|A|`. Arrays of size "
                  "0 or 1 are already sorted. Otherwise the hypothesis says both recursive "
                  "calls return sorted arrays, and MERGE of two sorted arrays is sorted "
                  "&mdash; which is itself a small proof, by induction on the number of "
                  "elements merged."),
            ("p", "Notice the shape. Nothing traced the recursion; the argument assumed "
                  "the subcalls worked and checked the combining step. That is why "
                  "recursive correctness proofs are short while tracing recursive "
                  "execution by hand is not."),
            ("thm", ("The two obligations are independent",
                     "An algorithm can terminate and be wrong (binary search on unsorted "
                     "data), and can be \"correct if it terminates\" and never terminate "
                     "(a recursion that fails to decrease). Both proofs are required.")),
        ],
        "lab": ("algorithm", {
            "mode": "search", "n": 32,
            "panel_title": "Binary search, counted",
            "panel_intro": "The comparison counts are produced by running both searches. "
                           "The binary column matches `⌊log₂n⌋ + 1` exactly, which is the "
                           "termination argument turned into a bound.",
        }),
        "steps_title": "Proving a recursive algorithm correct",
        "steps_intro": "Termination first, then correctness assuming the calls.",
        "steps": [
            ("Find the decreasing quantity",
             "Input size, range width, remaining depth. It must strictly decrease at every "
             "recursive call and be bounded below."),
            ("Check the base case handles the smallest inputs",
             "And check that the recursion actually reaches it. A base case for `n = 0` "
             "with a recursion that skips from 2 to 0 needs care about odd inputs."),
            ("Assume the recursive calls are correct",
             "This is the strong inductive hypothesis. Do not trace &mdash; assume."),
            ("Verify the combining step",
             "Given correct answers on the subproblems, does the algorithm produce the "
             "right answer for the whole? That is where the real content is."),
        ],
        "worked": {
            "title": "Fast exponentiation",
            "intro": ["Computing `aⁿ` in about `log₂ n` multiplications rather than `n`."],
            "lines": [
                "POWER(a, n):",
                "    if n = 0:       return 1",
                "    if n is even:   h = POWER(a, n/2);      return h × h",
                "    else:           return a × POWER(a, n − 1)",
                "",
                "TERMINATION  n decreases at every call (halved, or reduced by 1)",
                "             and is bounded below by 0.",
                "",
                "CORRECTNESS  strong induction on n.",
                "   n = 0:   returns 1 = a⁰.                              ✓",
                "   n even:  hypothesis gives h = a^(n/2);",
                "            h × h = a^(n/2) · a^(n/2) = aⁿ.               ✓",
                "   n odd:   hypothesis gives a^(n−1);",
                "            a × a^(n−1) = aⁿ.                             ✓",
                "",
                "Cost: at most 2·log₂ n calls — two odd steps never occur in a row.",
            ],
            "after": [
                "Strong induction is essential here: the even branch reaches back to `n/2`, "
                "not to `n − 1`. Ordinary induction would give a hypothesis about the wrong "
                "value. Course 6 lesson 8 uses this algorithm as modular exponentiation, "
                "where the saving is the difference between feasible and impossible."
            ],
        },
        "quiz_title": "Recursive correctness",
        "quiz": [
            {"q": "What must a termination argument exhibit?",
             "a": ["a base case",
                   "a quantity that strictly decreases at each call and is bounded below",
                   "a loop invariant",
                   "the running time"],
             "c": 1,
             "why": "Strictly decreasing and bounded below means the sequence of calls "
                    "cannot be infinite. Either half alone is insufficient."},
            {"q": "In proving a recursive algorithm correct you:",
             "a": ["trace the recursion to the base",
                   "assume the recursive calls are correct and check the combination",
                   "test on many inputs",
                   "prove it terminates and stop"],
             "c": 1,
             "why": "That assumption is the inductive hypothesis, and it is what makes the "
                    "proof short. Tracing is what the proof exists to avoid."},
            {"q": "Binary search on an unsorted array:",
             "a": ["does not terminate",
                   "terminates but may return a wrong answer",
                   "is still correct",
                   "raises an error"],
             "c": 1,
             "why": "Termination depends only on the shrinking range. Correctness depends "
                    "on sortedness, which is what licenses discarding half the array."},
        ],
        "mistakes": [
            ("Proving correctness and forgetting termination",
             "\"Correct if it terminates\" is worth nothing for an algorithm that does "
             "not. The two obligations are separate and both are required."),
            ("Tracing instead of assuming",
             "Following the recursion by hand does not generalise past the input you "
             "traced. The hypothesis covers all smaller inputs at once."),
            ("Overlooking a precondition",
             "Binary search needs sorted input; merge needs sorted halves. A precondition "
             "used but not stated is a proof of a different theorem."),
        ],
        "standard": ("Finish when you can discharge both obligations in a paragraph.",
                     "Write a recursive algorithm computing the `n`th Fibonacci number, "
                     "prove it terminates and prove it correct. Then count the calls it "
                     "makes: the naive version makes exponentially many, which lesson 11 "
                     "and course 8 both return to."),
        "note": "The naive recursive Fibonacci makes about `1.6ⁿ` calls because it "
                "recomputes the same subproblems repeatedly. Storing results &mdash; "
                "memoisation &mdash; drops it to `n` calls, and that observation is the "
                "whole idea of dynamic programming in course 8 lesson 10.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "recurrence-relations",
        "title": "Recurrence Relations",
        "module": "Recurrences",
        "one_line": "Sequences defined by their own earlier terms.",
        "summary": (
            "A recurrence gives each term from previous ones. Setting one up is modelling; "
            "solving it means finding a closed form. This lesson does the first and "
            "prepares the second."
        ),
        "key": [
            "linear homogeneous, order k:   aₙ = c₁aₙ₋₁ + … + c_k aₙ₋ₖ",
            "nonhomogeneous:                 … + f(n)",
            "k initial conditions determine the sequence completely",
            "solving = finding a formula for aₙ that does not mention earlier terms",
        ],
        "key_label": "Vocabulary before technique",
        "concepts_intro": (
            "Most of the difficulty in recurrences is setting them up. The solving "
            "techniques of lessons 10 and 11 are mechanical once the recurrence is right."
        ),
        "concepts": [
            ("A recurrence plus initial conditions determines the sequence",
             "Order `k` needs `k` initial values. With them every term is determined; "
             "without them the recurrence describes a family."),
            ("Linear means the terms appear to the first power",
             "`aₙ = 2aₙ₋₁ + 3aₙ₋₂` is linear. `aₙ = aₙ₋₁²` and `aₙ = aₙ₋₁ · aₙ₋₂` are not, "
             "and the techniques of lesson 10 do not apply to them."),
            ("Homogeneous means no standalone term",
             "The `+ f(n)` in a nonhomogeneous recurrence is what makes the Tower of Hanoi "
             "`2aₙ₋₁ + 1` rather than `2aₙ₋₁`."),
        ],
        "read_title": "Setting up a recurrence",
        "read_intro": "The classification, then four models built from scratch.",
        "body": [
            ("def", ("Recurrence relation",
                     "A <strong>recurrence relation</strong> expresses `aₙ` in terms of "
                     "earlier terms of the sequence. Its <strong>order</strong> is how far "
                     "back it reaches. <strong>Initial conditions</strong> supply the "
                     "first terms outright.")),
            ("def", ("Linear homogeneous with constant coefficients",
                     "`aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ + ⋯ + c_k aₙ₋ₖ`, with the `cᵢ` constants and "
                     "`c_k ≠ 0`. <strong>Linear</strong>: terms appear to the first power "
                     "and are not multiplied together. <strong>Homogeneous</strong>: no "
                     "term without an `a` in it.")),
            ("h3", "Building recurrences"),
            ("example", ("Compound interest",
                         "A balance growing at `r` per period: `aₙ = (1 + r)aₙ₋₁`, with "
                         "`a₀` the initial deposit. First order, linear, homogeneous, and "
                         "its solution `a₀(1+r)ⁿ` is immediate.")),
            ("example", ("Tower of Hanoi",
                         "`Hₙ = 2Hₙ₋₁ + 1`, `H₁ = 1`. First order, linear, "
                         "<em>non</em>homogeneous &mdash; the `+1` is the single move of "
                         "the largest disc, and it is what makes the answer `2ⁿ − 1` "
                         "rather than a power of 2.")),
            ("example", ("Rabbits, or bit strings",
                         "Fibonacci `Fₙ = Fₙ₋₁ + Fₙ₋₂` is second order, linear, "
                         "homogeneous. It counts more than rabbits: the number of binary "
                         "strings of length `n` with no two consecutive 1s satisfies it "
                         "too, because such a string either ends in 0 (any valid string of "
                         "length `n−1`) or in 01 (any valid string of length `n−2`).")),
            ("p", "That derivation is the model for setting up a counting recurrence: "
                  "split the objects by their last piece, and each part is counted by a "
                  "smaller instance of the same problem. Getting the split right &mdash; "
                  "exhaustive and non-overlapping &mdash; is the whole task."),
            ("example", ("Codewords",
                         "How many strings of length `n` over `{0,1,2}` contain an even "
                         "number of 0s? Let `aₙ` be that count. A valid string of length "
                         "`n` is a valid string of length `n−1` followed by 1 or 2, or an "
                         "<em>invalid</em> one followed by 0. Since there are `3ⁿ⁻¹` "
                         "strings in total, `aₙ = 2aₙ₋₁ + (3ⁿ⁻¹ − aₙ₋₁) = aₙ₋₁ + 3ⁿ⁻¹`, "
                         "with `a₁ = 2`. Nonhomogeneous, with `f(n) = 3ⁿ⁻¹`.")),
            ("h3", "Iteration: solving by unrolling"),
            ("p", "Before any technique, a recurrence can often be solved by unrolling it "
                  "and spotting the pattern &mdash; then proving the guess by induction. "
                  "That last step is not optional: unrolling produces a conjecture."),
            ("math", [
                "Hₙ = 2Hₙ₋₁ + 1",
                "   = 2(2Hₙ₋₂ + 1) + 1      = 4Hₙ₋₂ + 2 + 1",
                "   = 4(2Hₙ₋₃ + 1) + 3      = 8Hₙ₋₃ + 4 + 2 + 1",
                "   …",
                "   = 2ⁿ⁻¹H₁ + (2ⁿ⁻² + … + 2 + 1)",
                "   = 2ⁿ⁻¹ + 2ⁿ⁻¹ − 1       = 2ⁿ − 1",
            ]),
            ("p", "The geometric sum from lesson 3 finished it. Unrolling works well for "
                  "first-order recurrences and becomes unmanageable for higher orders, "
                  "which is why lesson 10 exists."),
        ],
        "lab": ("recurrence", {
            "preset": "hanoi",
            "panel_title": "Set up, unroll, compare",
            "panel_intro": "Each preset shows the recurrence unrolled beside its closed "
                           "form. The note under the status line explains where the closed "
                           "form came from &mdash; which is lessons 10 and 11.",
        }),
        "steps_title": "Setting up a recurrence",
        "steps_intro": "Find the last decision; everything before it is a smaller instance.",
        "steps": [
            ("Define `aₙ` precisely",
             "\"The number of …of length `n`\". A vague definition produces a recurrence "
             "that counts something else."),
            ("Split by the last piece",
             "Classify the objects by their final element or final move. Each class should "
             "correspond to a smaller instance."),
            ("Check the split is exhaustive and non-overlapping",
             "Every object in exactly one class. Overlap double-counts; a gap undercounts, "
             "and neither shows up until the numbers are wrong."),
            ("Supply as many initial conditions as the order",
             "A second-order recurrence needs two, and computing them by hand from the "
             "definition is where off-by-one errors surface."),
        ],
        "worked": {
            "title": "Strings with no two consecutive 1s",
            "intro": ["Let `aₙ` be the number of binary strings of length `n` with no `11`."],
            "lines": [
                "Split by the last character:",
                "   ends in 0:   the first n−1 characters are any valid string  →  aₙ₋₁",
                "   ends in 1:   the character before must be 0, and the first",
                "                n−2 are any valid string                       →  aₙ₋₂",
                "",
                "Exhaustive (a string ends in 0 or 1) and disjoint.",
                "",
                "   aₙ = aₙ₋₁ + aₙ₋₂",
                "",
                "Initial conditions, by listing:",
                "   n = 1:  0, 1                     a₁ = 2",
                "   n = 2:  00, 01, 10               a₂ = 3   (11 excluded)",
                "",
                "Sequence: 2, 3, 5, 8, 13, 21, 34 …   = Fₙ₊₂",
            ],
            "after": [
                "Same recurrence as Fibonacci, different initial conditions, so the "
                "sequence is shifted. That is the general situation: the recurrence "
                "determines the shape of the solution and the initial conditions select "
                "which one, which is exactly what lesson 10 formalises."
            ],
        },
        "quiz_title": "Recurrences",
        "quiz": [
            {"q": "Which is linear homogeneous with constant coefficients?",
             "a": ["`aₙ = aₙ₋₁²`", "`aₙ = 3aₙ₋₁ − 2aₙ₋₂`",
                   "`aₙ = aₙ₋₁ + n`", "`aₙ = n·aₙ₋₁`"],
             "c": 1,
             "why": "First powers, no standalone term, constant coefficients. The third is "
                    "nonhomogeneous; the fourth has a non-constant coefficient; the first "
                    "is not linear."},
            {"q": "How many initial conditions does a third-order recurrence need?",
             "a": ["One", "Two", "Three", "It depends on the coefficients"],
             "c": 2,
             "why": "The recurrence reaches back three places, so the first three terms "
                    "must be supplied before it can compute anything."},
            {"q": "In deriving a counting recurrence, splitting by the last character requires:",
             "a": ["the classes to be equal in size",
                   "the classes to be exhaustive and non-overlapping",
                   "at least three classes",
                   "the string to be sorted"],
             "c": 1,
             "why": "Every object must fall in exactly one class, or the recurrence "
                    "counts wrongly &mdash; and the error is invisible until the numbers "
                    "are checked."},
        ],
        "mistakes": [
            ("Overlapping cases in the split",
             "Strings counted in two classes are counted twice. Check by listing the small "
             "cases and comparing with the recurrence's prediction."),
            ("Wrong number of initial conditions",
             "Order `k` needs `k` of them. Fewer leaves the sequence undetermined; more "
             "may be inconsistent with the recurrence."),
            ("Treating an unrolled pattern as proved",
             "Unrolling produces a conjecture. The induction proof is what turns it into a "
             "solution, and course 1 lesson 14 explains why that step is not a formality."),
        ],
        "standard": ("Finish when you can derive a recurrence and verify its first terms "
                     "by hand.",
                     "Find a recurrence for the number of ways to tile a `2 × n` strip "
                     "with `1 × 2` dominoes, and check `a₁` through `a₄` by drawing them. "
                     "You should get Fibonacci again, which is worth understanding rather "
                     "than noticing."),
        "note": "Recurrences are the discrete counterpart of differential equations, and "
                "the solution methods parallel each other closely: characteristic "
                "equations, homogeneous plus particular solutions, and the same trouble "
                "when a root of the characteristic equation collides with the forcing term.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "solving-linear-recurrences",
        "title": "Solving Linear Recurrences",
        "module": "Recurrences",
        "one_line": "Characteristic roots, repeated roots, and particular solutions.",
        "summary": (
            "For a linear homogeneous recurrence, substitute `aₙ = rⁿ` and solve the "
            "resulting polynomial. Distinct roots give a combination of geometric "
            "sequences; repeated roots need an extra factor of `n`."
        ),
        "key": [
            "aₙ = c₁aₙ₋₁ + c₂aₙ₋₂    ⟹   r² = c₁r + c₂",
            "distinct roots r₁ ≠ r₂:  aₙ = A r₁ⁿ + B r₂ⁿ",
            "repeated root r:         aₙ = (A + Bn) rⁿ",
            "nonhomogeneous:          general homogeneous + one particular solution",
        ],
        "key_label": "The recipe",
        "concepts_intro": (
            "The whole method rests on one guess &mdash; that the solution is geometric "
            "&mdash; and on the fact that solutions can be added."
        ),
        "concepts": [
            ("Guess `rⁿ` and see what `r` must be",
             "Substituting turns the recurrence into a polynomial equation. Its roots are "
             "the geometric sequences that satisfy the recurrence."),
            ("Solutions combine linearly",
             "If two sequences satisfy a linear homogeneous recurrence, so does any "
             "combination of them. The initial conditions pick the combination."),
            ("A repeated root needs `n rⁿ` too",
             "One root gives one solution, and two initial conditions need two free "
             "constants. `n rⁿ` supplies the second and does satisfy the recurrence."),
        ],
        "read_title": "The characteristic equation",
        "read_intro": "Derivation, the two cases, and the nonhomogeneous extension.",
        "body": [
            ("p", "Take `aₙ = c₁aₙ₋₁ + c₂aₙ₋₂` and try `aₙ = rⁿ` with `r ≠ 0`. Substituting "
                  "gives `rⁿ = c₁rⁿ⁻¹ + c₂rⁿ⁻²`, and dividing by `rⁿ⁻²` leaves"),
            ("math", [
                "r² = c₁r + c₂          the CHARACTERISTIC EQUATION",
            ]),
            ("thm", ("Distinct roots",
                     "If `r² − c₁r − c₂ = 0` has distinct roots `r₁ ≠ r₂`, then every "
                     "solution of the recurrence has the form `aₙ = A r₁ⁿ + B r₂ⁿ`, and "
                     "`A`, `B` are determined by the initial conditions.")),
            ("thm", ("Repeated root",
                     "If the characteristic equation has a single root `r` of multiplicity "
                     "2, then every solution has the form `aₙ = (A + Bn) rⁿ`.")),
            ("p", "Why the extra `n`? With one root there is only one geometric solution "
                  "and only one free constant, which cannot generally satisfy two initial "
                  "conditions. Substituting `n rⁿ` into the recurrence and using "
                  "`c₁ = 2r`, `c₂ = −r²` (which is what a repeated root means) confirms it "
                  "is also a solution."),
            ("example", ("Fibonacci, solved",
                         "`Fₙ = Fₙ₋₁ + Fₙ₋₂` gives `r² = r + 1`, so `r = (1 ± √5)/2`. "
                         "Writing `φ` and `ψ` for the two roots, `Fₙ = Aφⁿ + Bψⁿ`. From "
                         "`F₀ = 0` we get `A + B = 0`, and from `F₁ = 1` we get "
                         "`Aφ + Bψ = 1`, giving `A = 1/√5`, `B = −1/√5`. So "
                         "`Fₙ = (φⁿ − ψⁿ)/√5` &mdash; Binet's formula, which produces "
                         "integers from irrational numbers at every `n`.")),
            ("h3", "Nonhomogeneous recurrences"),
            ("thm", ("General solution",
                     "For `aₙ = c₁aₙ₋₁ + ⋯ + c_k aₙ₋ₖ + f(n)`, the general solution is "
                     "`aₙ = (general solution of the homogeneous part) + (any one "
                     "particular solution)`.")),
            ("p", "So the work is finding one particular solution. The standard approach "
                  "is to guess a form matching `f(n)` and solve for its coefficients."),
            ("math", [
                "f(n)              try                    unless it collides with a root",
                "constant          A                      then try An",
                "linear   an + b   An + B                 then multiply by n",
                "polynomial deg d  general poly of deg d  then multiply by n",
                "sⁿ                A sⁿ                   if s is a root, try A n sⁿ",
            ]),
            ("example", ("Tower of Hanoi, properly",
                         "`Hₙ = 2Hₙ₋₁ + 1`. Homogeneous part: `r = 2`, so `C·2ⁿ`. "
                         "Particular: try a constant `A`, giving `A = 2A + 1`, so `A = −1`. "
                         "General solution `Hₙ = C·2ⁿ − 1`, and `H₁ = 1` gives `C = 1`. "
                         "So `Hₙ = 2ⁿ − 1` &mdash; derived rather than guessed.")),
            ("p", "The collision case is worth a sentence. If `f(n) = 2ⁿ` and 2 is a root "
                  "of the characteristic equation, then `A·2ⁿ` already solves the "
                  "homogeneous equation and cannot produce the forcing term. Multiplying by "
                  "`n` and trying `A n 2ⁿ` is the fix, exactly as with a repeated root."),
        ],
        "lab": ("recurrence", {
            "preset": "two",
            "panel_title": "Roots, and the solution they build",
            "panel_intro": "Each preset shows its characteristic equation and the "
                           "constants fitted to the initial conditions. The iterated "
                           "column and the closed-form column are computed independently.",
        }),
        "steps_title": "Solving a linear recurrence",
        "steps_intro": "Homogeneous part first, then a particular solution, then fit.",
        "steps": [
            ("Write the characteristic equation",
             "Replace `aₙ₋ⱼ` by `r^{k−j}` and set the polynomial to zero. Its degree is "
             "the order of the recurrence."),
            ("Find the roots and their multiplicities",
             "Distinct roots give `A r₁ⁿ + B r₂ⁿ`; a root of multiplicity `m` contributes "
             "`(A₀ + A₁n + ⋯ + A_{m−1}n^{m−1}) rⁿ`."),
            ("For a nonhomogeneous recurrence, find one particular solution",
             "Guess a form matching `f(n)`, substitute, and solve for the coefficients. "
             "Multiply by `n` if the guess collides with a root."),
            ("Fit the constants to the initial conditions",
             "One linear equation per initial condition. Then check the closed form "
             "reproduces a term you did not use in the fitting."),
        ],
        "worked": {
            "title": "Solve `aₙ = 5aₙ₋₁ − 6aₙ₋₂`, `a₀ = 1`, `a₁ = 5`",
            "intro": ["Second order, homogeneous, distinct roots."],
            "lines": [
                "Characteristic:   r² = 5r − 6",
                "                  r² − 5r + 6 = 0",
                "                  (r − 2)(r − 3) = 0      ⟹  r = 2, 3",
                "",
                "General:          aₙ = A·2ⁿ + B·3ⁿ",
                "",
                "Fit:              a₀ = A + B     = 1",
                "                  a₁ = 2A + 3B   = 5",
                "                  subtract twice the first:  B = 3,  so A = −2",
                "",
                "Solution:         aₙ = −2·2ⁿ + 3·3ⁿ",
                "",
                "Check a₂:  formula −8 + 27 = 19;  recurrence 5(5) − 6(1) = 19.   ✓",
            ],
            "after": [
                "The check at `a₂` used a term not involved in fitting the constants, "
                "which is what makes it a real check. Verifying `a₀` and `a₁` would only "
                "confirm the arithmetic of the fitting."
            ],
        },
        "quiz_title": "Solving recurrences",
        "quiz": [
            {"q": "`aₙ = 4aₙ₋₁ − 4aₙ₋₂` has characteristic equation:",
             "a": ["`r² − 4r + 4 = 0`, root 2 twice",
                   "`r² + 4r − 4 = 0`",
                   "`r = 4`",
                   "`r² = 4r + 4`"],
             "c": 0,
             "why": "`(r − 2)² = 0`, a repeated root, so the general solution is "
                    "`(A + Bn)2ⁿ` rather than `A·2ⁿ + B·2ⁿ`."},
            {"q": "Why does a repeated root need the extra factor of `n`?",
             "a": ["To make the sequence grow faster",
                   "One root gives only one free constant, and two initial conditions need two",
                   "Because `rⁿ` is not a solution",
                   "To avoid negative terms"],
             "c": 1,
             "why": "`A·rⁿ` and `B·rⁿ` are the same family. `n rⁿ` is a genuinely different "
                    "solution and supplies the second constant."},
            {"q": "For `aₙ = 3aₙ₋₁ + 2ⁿ`, the particular solution should be tried as:",
             "a": ["`A`", "`A·2ⁿ`", "`A n 2ⁿ`", "`An + B`"],
             "c": 1,
             "why": "`f(n) = 2ⁿ` and 2 is not a root (the only root is 3), so `A·2ⁿ` works "
                    "without modification. The `n` factor is needed only on collision."},
        ],
        "mistakes": [
            ("Forgetting the `n` on a repeated root",
             "`A·2ⁿ + B·2ⁿ` collapses to a single constant and cannot satisfy two initial "
             "conditions. The general solution is `(A + Bn)2ⁿ`."),
            ("Fitting the constants before finding a particular solution",
             "For a nonhomogeneous recurrence the constants must be fitted to the FULL "
             "general solution, homogeneous plus particular. Fitting early gives wrong "
             "constants."),
            ("Not checking the collision case",
             "If the forcing term matches a characteristic root, the obvious guess solves "
             "the homogeneous equation and produces `0 = f(n)`. Multiply by `n`."),
        ],
        "standard": ("Finish when you can solve a second-order recurrence and verify it "
                     "independently.",
                     "Solve `aₙ = 6aₙ₋₁ − 9aₙ₋₂` with `a₀ = 1`, `a₁ = 6`, and check your "
                     "closed form at `a₃` against the recurrence. The repeated root makes "
                     "this the case people get wrong."),
        "note": "The same method solves linear differential equations with constant "
                "coefficients: substitute `e^{rt}`, get a characteristic polynomial, and "
                "handle repeated roots with an extra factor of `t`. The parallel is exact "
                "and not a coincidence.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "divide-and-conquer-recurrences",
        "title": "Divide-and-Conquer Recurrences",
        "module": "Recurrences",
        "one_line": "`T(n) = aT(n/b) + f(n)`, and the one comparison that solves it.",
        "summary": (
            "Algorithms that split a problem into `a` pieces of size `n/b` produce "
            "recurrences of one shape. The master theorem settles them by comparing "
            "`log_b a` with the exponent in `f(n)`."
        ),
        "key": [
            "T(n) = a T(n/b) + nᵈ",
            "log_b a < d   ⟹  T(n) = Θ(nᵈ)              root dominates",
            "log_b a = d   ⟹  T(n) = Θ(nᵈ log n)        every level equal",
            "log_b a > d   ⟹  T(n) = Θ(n^{log_b a})     leaves dominate",
        ],
        "key_label": "One comparison, three cases",
        "concepts_intro": (
            "The three cases are not arbitrary: they are which level of the recursion "
            "tree carries most of the work."
        ),
        "concepts": [
            ("The recursion tree explains the three cases",
             "Level `i` has `aⁱ` subproblems of size `n/bⁱ`. Whether the work grows, "
             "shrinks or stays level down the tree is exactly the comparison."),
            ("Merge sort is the balanced case",
             "`a = 2`, `b = 2`, `d = 1`, so `log₂2 = 1 = d`. Every level does `Θ(n)` work "
             "and there are `log n` levels."),
            ("Fewer, bigger pieces can beat more, smaller ones",
             "Karatsuba multiplication does 3 multiplications of half-size instead of 4, "
             "and `log₂3 ≈ 1.585 &lt; 2` is the entire improvement."),
        ],
        "read_title": "The master theorem",
        "read_intro": "Where the recurrence comes from, what the tree looks like, and the statement.",
        "body": [
            ("p", "A divide-and-conquer algorithm splits an input of size `n` into `a` "
                  "subproblems of size `n/b`, solves each recursively, and spends `f(n)` "
                  "combining. The running time therefore satisfies `T(n) = aT(n/b) + f(n)`."),
            ("h3", "The recursion tree"),
            ("math", [
                "level   subproblems   size      work per level",
                "  0          1          n            f(n)",
                "  1          a         n/b         a·f(n/b)",
                "  2          a²        n/b²        a²·f(n/b²)",
                "  …",
                "  L         a^L        1           a^L · f(1)",
                "",
                "with L = log_b n levels, so a^L = a^{log_b n} = n^{log_b a}.",
            ]),
            ("p", "With `f(n) = nᵈ`, the work at level `i` is `aⁱ(n/bⁱ)ᵈ = nᵈ(a/bᵈ)ⁱ` "
                  "&mdash; a geometric series in `i` with ratio `a/bᵈ`. Which end dominates "
                  "depends entirely on whether that ratio is less than, equal to, or "
                  "greater than 1, and `a/bᵈ` compared with 1 is `log_b a` compared with "
                  "`d`. That is the whole theorem."),
            ("thm", ("Master theorem (polynomial form)",
                     "Let `T(n) = aT(n/b) + Θ(nᵈ)` with `a ≥ 1`, `b &gt; 1`, `d ≥ 0`. Then "
                     "`T(n) = Θ(nᵈ)` if `log_b a &lt; d`; `T(n) = Θ(nᵈ log n)` if "
                     "`log_b a = d`; and `T(n) = Θ(n^{log_b a})` if `log_b a &gt; d`.")),
            ("example", ("Merge sort",
                         "`T(n) = 2T(n/2) + n`: `a = 2`, `b = 2`, `d = 1`, `log₂2 = 1 = d`. "
                         "Balanced case, so `Θ(n log n)`. Every level does `n` units of "
                         "merging and there are `log₂ n` levels.")),
            ("example", ("Binary search",
                         "`T(n) = T(n/2) + 1`: `a = 1`, `b = 2`, `d = 0`, `log₂1 = 0 = d`. "
                         "Balanced again, so `Θ(log n)`. One subproblem and constant work "
                         "per level.")),
            ("example", ("Karatsuba multiplication",
                         "Multiplying two `n`-digit numbers by splitting into halves needs "
                         "four half-size products naively: `T(n) = 4T(n/2) + n`, and "
                         "`log₂4 = 2 &gt; 1`, giving `Θ(n²)` &mdash; no better than the "
                         "schoolbook method. Karatsuba's identity does it with three: "
                         "`T(n) = 3T(n/2) + n`, and `log₂3 ≈ 1.585`, giving "
                         "`Θ(n^{1.585})`. One fewer multiplication changes the exponent.")),
            ("p", "Two cautions. The theorem as stated covers `f(n) = Θ(nᵈ)`; forcing terms "
                  "like `n log n` fall between the cases and need the fuller version. And "
                  "it says nothing about constants &mdash; an algorithm with a better "
                  "exponent may lose on realistic inputs, which is why Karatsuba is used "
                  "for large numbers and schoolbook multiplication for small ones."),
            ("thm", ("Substituting to make it linear",
                     "Setting `n = bᵏ` and `Sₖ = T(bᵏ)` turns `T(n) = aT(n/b) + nᵈ` into "
                     "`Sₖ = aSₖ₋₁ + (bᵈ)ᵏ`, an ordinary linear recurrence that lesson 10 "
                     "solves. The master theorem is that solution, read back.")),
        ],
        "lab": ("algorithm", {
            "mode": "master",
            "panel_title": "The three cases, tabulated",
            "panel_intro": "Each row computes `log_b a` and compares it with `d`. The case "
                           "is decided by that one comparison and nothing else.",
        }),
        "steps_title": "Applying the master theorem",
        "steps_intro": "Read off `a`, `b`, `d`, then compare.",
        "steps": [
            ("Identify `a`, `b` and `d`",
             "`a` is the number of subproblems, `b` the shrink factor, `d` the exponent of "
             "the combining work. Reading `a` off as the shrink factor is the standard slip."),
            ("Compute `log_b a`",
             "`log₂ 2 = 1`, `log₂ 3 ≈ 1.585`, `log₂ 4 = 2`, `log₂ 8 = 3`. These four cover "
             "most examples."),
            ("Compare with `d` and read the case",
             "Less, equal, greater &mdash; root dominates, level, leaves dominate."),
            ("Sanity check with the tree",
             "Does the work per level grow, stay constant or shrink? The answer should "
             "match the case you selected."),
        ],
        "worked": {
            "title": "Three recurrences",
            "intro": ["Same theorem, three different answers."],
            "lines": [
                "1.  T(n) = 2T(n/2) + n            a=2  b=2  d=1",
                "    log₂2 = 1 = d      →  CASE 2  →  Θ(n log n)      merge sort",
                "",
                "2.  T(n) = 8T(n/2) + n²           a=8  b=2  d=2",
                "    log₂8 = 3 > 2      →  CASE 3  →  Θ(n³)           naive matrix mult.",
                "",
                "3.  T(n) = 2T(n/2) + n²           a=2  b=2  d=2",
                "    log₂2 = 1 < 2      →  CASE 1  →  Θ(n²)           root dominates",
                "",
                "Strassen improves case 2 above by using 7 multiplications, not 8:",
                "    T(n) = 7T(n/2) + n²,   log₂7 ≈ 2.807  →  Θ(n^2.807)",
            ],
            "after": [
                "Case 3 is the one where the recursion is doing the damage: `n³` work "
                "arises from `n^{log₂8}` leaves, not from the combining. Strassen attacks "
                "exactly that by reducing `a` from 8 to 7, and gains an exponent "
                "improvement that no faster combining step could have produced."
            ],
        },
        "quiz_title": "Master theorem",
        "quiz": [
            {"q": "`T(n) = 4T(n/2) + n`. Which case and what result?",
             "a": ["Case 1, `Θ(n)`", "Case 2, `Θ(n log n)`",
                   "Case 3, `Θ(n²)`", "The theorem does not apply"],
             "c": 2,
             "why": "`log₂4 = 2 &gt; 1 = d`, so the leaves dominate and `T(n) = Θ(n²)`."},
            {"q": "In the balanced case, why does `log n` appear?",
             "a": ["Because the input is halved",
                   "Because every level does the same work and there are `log_b n` levels",
                   "Because `a = b`",
                   "Because of the combining step"],
             "c": 1,
             "why": "Equal work per level times the number of levels. The number of levels "
                    "is `log_b n` because the size divides by `b` each time."},
            {"q": "Karatsuba beats schoolbook multiplication because:",
             "a": ["it combines faster",
                   "it uses 3 half-size multiplications instead of 4, and `log₂3 &lt; 2`",
                   "it has a smaller constant",
                   "it uses less memory"],
             "c": 1,
             "why": "Reducing `a` from 4 to 3 changes the exponent from `log₂4 = 2` to "
                    "`log₂3 ≈ 1.585`. The combining work is `Θ(n)` in both."},
        ],
        "mistakes": [
            ("Mixing up `a` and `b`",
             "`a` counts subproblems, `b` is the shrink factor. `T(n) = 2T(n/3) + n` has "
             "`a = 2`, `b = 3`, and swapping them gives the wrong case."),
            ("Applying the polynomial form to a non-polynomial `f`",
             "`f(n) = n log n` falls between cases 2 and 3 and needs the general statement. "
             "Forcing it into the version here gives a wrong answer."),
            ("Reading `Θ` as a statement about real running time",
             "It describes asymptotic growth. An algorithm with a better exponent and a "
             "worse constant can be slower on every input you will ever run."),
        ],
        "standard": ("Finish when you can decide the case from the tree, not from the "
                     "formula.",
                     "For `T(n) = 3T(n/4) + n`, compute the work at levels 0, 1 and 2 and "
                     "say whether it is growing or shrinking. Then check that the master "
                     "theorem gives the case your tree predicted."),
        "note": "The master theorem does not cover every divide-and-conquer recurrence: "
                "unequal splits like `T(n) = T(n/3) + T(2n/3) + n` need the tree argument "
                "directly, and that one turns out to be `Θ(n log n)` &mdash; the same as an "
                "even split, which is why quicksort survives an imperfect pivot.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "loop-invariants-and-correctness",
        "title": "Loop Invariants and Program Correctness",
        "module": "Correctness",
        "one_line": "Induction, applied to a loop instead of to a number.",
        "summary": (
            "A loop invariant is a statement true before the loop and preserved by every "
            "iteration. Together with termination it proves the loop computes what it "
            "should &mdash; and the argument is exactly induction."
        ),
        "key": [
            "INITIALISATION  the invariant holds before the first iteration",
            "MAINTENANCE     if it holds before an iteration, it holds after",
            "TERMINATION     the loop stops, and the invariant then gives the result",
            "This is induction: base case, step, conclusion.",
        ],
        "key_label": "Three obligations",
        "concepts_intro": (
            "The three parts of a loop-invariant proof are the three parts of an "
            "induction proof, renamed."
        ),
        "concepts": [
            ("Initialisation is the base case",
             "The invariant must hold before any iteration has run, which is usually "
             "immediate and is usually where an off-by-one hides."),
            ("Maintenance is the inductive step",
             "Assume the invariant before an iteration and prove it after. The loop body "
             "is what you reason about."),
            ("Termination converts the invariant into the result",
             "The invariant plus the negated loop condition should give exactly the "
             "postcondition. If it does not, the invariant is too weak."),
        ],
        "read_title": "Loop invariants",
        "read_intro": "The method, three worked loops, and how to find an invariant.",
        "body": [
            ("def", ("Loop invariant",
                     "A <strong>loop invariant</strong> is a statement that is true "
                     "immediately before the loop begins and remains true immediately "
                     "before each subsequent iteration.")),
            ("h3", "Summing an array"),
            ("math", [
                "SUM(A):                          invariant:  s = A[0] + … + A[i−1]",
                "    s = 0",
                "    i = 0",
                "    while i < n:",
                "        s = s + A[i]",
                "        i = i + 1",
                "    return s",
            ]),
            ("p", "<strong>Initialisation.</strong> Before the loop, `i = 0` and `s = 0`; "
                  "the sum of the first zero elements is 0, so the invariant holds "
                  "vacuously."),
            ("p", "<strong>Maintenance.</strong> Suppose `s = A[0] + ⋯ + A[i−1]` at the "
                  "top of an iteration. The body adds `A[i]` to `s` and increments `i`, so "
                  "afterwards `s = A[0] + ⋯ + A[i−1]` with the new `i` &mdash; the "
                  "invariant again."),
            ("p", "<strong>Termination.</strong> The loop exits with `i = n`, and the "
                  "invariant then reads `s = A[0] + ⋯ + A[n−1]`, which is the whole sum. "
                  "That the loop exits follows because `i` increases by 1 each iteration "
                  "and is bounded above by `n`."),
            ("h3", "Insertion sort"),
            ("math", [
                "for j = 1 to n−1:",
                "    key = A[j]",
                "    i = j − 1",
                "    while i ≥ 0 and A[i] > key:",
                "        A[i+1] = A[i]",
                "        i = i − 1",
                "    A[i+1] = key",
                "",
                "invariant (outer loop):  A[0..j−1] contains the original first j",
                "                         elements, in sorted order",
            ]),
            ("p", "Initialisation: at `j = 1` the subarray `A[0..0]` is one element, "
                  "trivially sorted. Maintenance: the inner loop shifts elements greater "
                  "than `key` one place right and inserts `key` in the gap, so `A[0..j]` "
                  "ends sorted and holds the same elements. Termination: the outer loop "
                  "ends with `j = n`, so `A[0..n−1]` is sorted &mdash; which is the "
                  "postcondition."),
            ("p", "The invariant says two things: sorted, and the same elements. Dropping "
                  "the second half would leave the proof compatible with an algorithm that "
                  "sorts by replacing the array with zeros. Invariants that are too weak "
                  "are the usual failure, and they fail at the termination step."),
            ("h3", "Finding an invariant"),
            ("ul", [
                "<strong>Start from the postcondition.</strong> What should be true at the "
                "end? The invariant is usually that statement with the loop variable in "
                "place of its final value.",
                "<strong>Include everything the proof needs.</strong> \"Sorted\" alone is "
                "not enough; \"sorted and a permutation of the original\" is.",
                "<strong>Check the boundaries.</strong> The invariant must hold when the "
                "loop has run zero times, which is where the vacuous cases live.",
            ]),
            ("thm", ("Partial and total correctness",
                     "<strong>Partial correctness</strong> is: if the loop terminates, the "
                     "postcondition holds. <strong>Total correctness</strong> adds that it "
                     "does terminate. An invariant gives the first; a decreasing bounded "
                     "quantity gives the second.")),
            ("p", "The distinction matters. A loop with a correct invariant that never "
                  "exits is partially correct and useless. Termination is proved the same "
                  "way as for a recursion: exhibit a quantity that strictly decreases and "
                  "cannot decrease forever."),
        ],
        "lab": ("algorithm", {
            "mode": "sort", "n": 20,
            "panel_title": "Insertion sort, counted",
            "panel_intro": "The insertion sort column is the one that varies with the "
                           "data: its inner loop stops early on nearly sorted input. Bubble "
                           "sort's count does not depend on the data at all.",
        }),
        "steps_title": "Proving a loop correct",
        "steps_intro": "State the invariant before writing anything else.",
        "steps": [
            ("Write the postcondition",
             "What must be true when the loop finishes. Without it there is nothing to aim "
             "the invariant at."),
            ("Guess an invariant and test the boundaries",
             "Usually the postcondition with the loop variable substituted. Check it holds "
             "before any iteration has run."),
            ("Prove maintenance",
             "Assume the invariant at the top of an iteration, follow the body, and show "
             "it holds at the top of the next."),
            ("Prove termination and combine",
             "A decreasing bounded quantity ends the loop; the invariant plus the negated "
             "loop condition must give the postcondition. If it does not, strengthen the "
             "invariant."),
        ],
        "worked": {
            "title": "Euclid's algorithm",
            "intro": ["Course 6 lesson 5 uses this; here it is the correctness argument."],
            "lines": [
                "GCD(a, b):",
                "    while b ≠ 0:",
                "        (a, b) = (b, a mod b)",
                "    return a",
                "",
                "INVARIANT   gcd(a, b) = gcd(a₀, b₀)      for the original inputs",
                "",
                "INITIALISATION  trivially true before the first iteration.",
                "",
                "MAINTENANCE     gcd(a, b) = gcd(b, a mod b) — any common divisor of",
                "                a and b divides a − qb, and conversely. So the pair",
                "                changes but its gcd does not.",
                "",
                "TERMINATION     b strictly decreases and is a non-negative integer,",
                "                so the loop ends, with b = 0. Then",
                "                gcd(a, 0) = a, and by the invariant that equals",
                "                gcd(a₀, b₀).                                    ∎",
            ],
            "after": [
                "The invariant is the entire proof: the algorithm works because the "
                "quantity it is computing never changes while the numbers get smaller. "
                "Every good invariant has that character &mdash; it names what the loop "
                "preserves, which is more informative than what the loop does."
            ],
        },
        "quiz_title": "Invariants",
        "quiz": [
            {"q": "The three parts of a loop-invariant proof correspond to:",
             "a": ["three loops",
                   "base case, inductive step, and conclusion",
                   "input, process, output",
                   "the three master theorem cases"],
             "c": 1,
             "why": "Initialisation is the base case, maintenance is the step, and "
                    "termination converts the invariant into the postcondition."},
            {"q": "An invariant that is true but too weak fails at:",
             "a": ["initialisation", "maintenance",
                   "termination — it does not imply the postcondition", "all three"],
             "c": 2,
             "why": "A weak invariant is preserved happily and simply does not give you "
                    "what you needed at the end. \"Sorted\" without \"same elements\" is "
                    "the standard example."},
            {"q": "Partial correctness means:",
             "a": ["the algorithm is correct on some inputs",
                   "if the loop terminates, the postcondition holds",
                   "the loop terminates",
                   "the invariant holds initially"],
             "c": 1,
             "why": "Termination is a separate obligation. A partially correct loop that "
                    "never exits is of no use."},
        ],
        "mistakes": [
            ("An invariant too weak to give the postcondition",
             "Test it at termination before doing any other work: substitute the exit "
             "condition and see whether the postcondition follows."),
            ("Checking maintenance and skipping initialisation",
             "The base case is where off-by-one errors live, and it is one line to check."),
            ("Proving partial correctness and calling it done",
             "Termination is the other half. A quantity that strictly decreases and is "
             "bounded below is all it takes to write."),
        ],
        "standard": ("Finish when you can state an invariant strong enough to close the "
                     "argument.",
                     "Write a loop computing `xⁿ` by repeated multiplication and state its "
                     "invariant. Then check that at exit the invariant plus the loop "
                     "condition gives exactly `result = xⁿ` &mdash; if it needs an extra "
                     "sentence, the invariant was too weak."),
        "note": "This is the whole of Hoare logic in miniature: preconditions, "
                "postconditions and invariants, with a proof rule for each construct. "
                "Course 8 lesson 2 returns to correctness as a property to be established "
                "before efficiency is worth measuring.",
    },
]
