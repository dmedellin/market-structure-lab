"""Course 3, lessons 01-06 — induction."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "the-well-ordering-principle",
        "title": "The Well-Ordering Principle",
        "module": "Foundations",
        "one_line": "Every nonempty set of naturals has a least element — and why that is enough.",
        "summary": (
            "Induction has to rest on something. The well-ordering principle is that "
            "something: every nonempty subset of `ℕ` has a smallest member. From it, "
            "induction follows in half a page."
        ),
        "key": [
            "Every nonempty S ⊆ ℕ has a least element.",
            "FALSE for ℤ:  {…, −2, −1, 0} has no least element",
            "FALSE for ℚ⁺: {x ∈ ℚ : x > 0} has no least element",
            "well-ordering  ⟺  induction  ⟺  strong induction",
        ],
        "key_label": "The axiom the course rests on",
        "concepts_intro": (
            "Before proving anything by induction it is worth knowing what induction "
            "itself rests on, and that it is not obvious for every number system."
        ),
        "concepts": [
            ("Well-ordering is a property of `ℕ`, not of numbers",
             "`ℤ` and `ℚ⁺` both fail it. The property that makes induction work is "
             "specific to the naturals, and it is why induction is about `ℕ`."),
            ("It is equivalent to induction",
             "Each can be derived from the other. Which is taken as the axiom is a "
             "matter of presentation, not of mathematics."),
            ("It powers the minimal-counterexample argument",
             "\"Take the smallest `n` for which the claim fails\" is well-ordering used "
             "directly, and it is often the shortest route to a result."),
        ],
        "read_title": "The principle and what follows from it",
        "read_intro": "Statement, the systems where it fails, and the derivation of induction.",
        "body": [
            ("def", ("Well-ordering principle",
                     "Every nonempty subset of `ℕ` has a least element. That is: if "
                     "`S ⊆ ℕ` and `S ≠ ∅`, there is `m ∈ S` with `m ≤ s` for every "
                     "`s ∈ S`.")),
            ("p", "The principle is not a theorem about numbers in general; it is a "
                  "specific property of `ℕ` that fails elsewhere and has to be assumed or "
                  "derived from an equivalent assumption."),
            ("ul", [
                "In `ℤ`, the set of negative integers is nonempty and has no least "
                "element &mdash; every candidate has a smaller one below it.",
                "In `ℚ⁺`, the set of positive rationals is nonempty and has no least "
                "element: whatever `q` you name, `q/2` is smaller and still positive.",
                "In `ℝ`, the open interval `(0, 1)` has no least element for the same "
                "reason.",
            ]),
            ("thm", ("Well-ordering implies induction",
                     "Suppose `P(0)` holds and `P(k) → P(k+1)` for every `k ∈ ℕ`. Then "
                     "`P(n)` holds for every `n ∈ ℕ`.")),
            ("proof", [
                "Let `S = {n ∈ ℕ : P(n) is false}` and suppose `S ≠ ∅`. By well-ordering "
                "`S` has a least element `m`.",
                "`m ≠ 0`, because `P(0)` holds. So `m ≥ 1` and `m − 1` is a natural number. "
                "Since `m` is the least member of `S`, `m − 1 ∉ S`, so `P(m − 1)` is true.",
                "But the hypothesis gives `P(m − 1) → P(m)`, so `P(m)` is true &mdash; "
                "contradicting `m ∈ S`.",
                "Therefore `S = ∅`, which is to say `P(n)` holds for every `n`.",
            ]),
            ("p", "That proof is the entire justification for the technique the rest of "
                  "the course uses, and it is worth reading twice. The base case rules out "
                  "`m = 0`; the inductive step rules out every other `m`; well-ordering is "
                  "what guarantees that if any counterexample existed, a smallest one "
                  "would."),
            ("h3", "Minimal counterexample as a technique"),
            ("p", "The proof above is itself a template. To show a claim holds for all "
                  "`n`, assume it fails somewhere, take the least such `n`, and derive a "
                  "contradiction &mdash; usually by producing a smaller counterexample. "
                  "This is sometimes called <em>infinite descent</em>."),
            ("thm", ("Every integer greater than 1 has a prime factor",
                     "For every integer `n &gt; 1` there is a prime `p` with `p | n`.")),
            ("proof", [
                "Suppose not, and let `S` be the set of integers greater than 1 with no "
                "prime factor. If `S ≠ ∅`, well-ordering gives a least element `m`.",
                "`m` is not prime, since a prime divides itself. So `m = ab` with "
                "`1 &lt; a &lt; m`. Now `a &gt; 1` and `a &lt; m`, so `a ∉ S` by "
                "minimality, so `a` has a prime factor `p`.",
                "But `p | a` and `a | m`, so `p | m`, contradicting `m ∈ S`.",
                "Hence `S = ∅`.",
            ]),
            ("p", "Notice the shape: minimality of `m` is what licenses the claim about "
                  "`a`. Without well-ordering there would be no smallest counterexample to "
                  "reason about, and the argument would have nothing to grip."),
        ],
        "lab": ("induction", {
            "statement": "sum",
            "panel_title": "Checking is not proving",
            "panel_intro": "Two of the statements in this list are FALSE and pass every "
                           "check a careful reader would run. Find them before going on; "
                           "the rest of this course is the technique that would have "
                           "caught them.",
        }),
        "steps_title": "Using minimal counterexample",
        "steps_intro": "Assume failure, take the smallest, break it.",
        "steps": [
            ("Assume the claim fails somewhere",
             "Let `S` be the set of `n` for which it fails, and suppose `S ≠ ∅`."),
            ("Take the least element of `S`",
             "Well-ordering guarantees one exists. This is the step that is unavailable "
             "over `ℤ` or `ℚ`."),
            ("Derive a contradiction from minimality",
             "Usually by exhibiting a smaller counterexample, or by showing the claim "
             "holds at `m` after all because it holds below `m`."),
            ("Conclude `S` is empty",
             "Which is the claim, stated the other way round."),
        ],
        "worked": {
            "title": "The division algorithm, by well-ordering",
            "intro": ["For `a ∈ ℤ` and `d &gt; 0` there are `q, r` with `a = dq + r` and `0 ≤ r &lt; d`."],
            "lines": [
                "Let S = { a − dq : q ∈ ℤ,  a − dq ≥ 0 }.",
                "",
                "S is nonempty:  take q very negative and a − dq is large and positive.",
                "S ⊆ ℕ by construction, so well-ordering gives a least element r = a − dq.",
                "",
                "Claim r < d.  Suppose r ≥ d.  Then",
                "    r − d = a − d(q + 1) ≥ 0,",
                "so r − d ∈ S and r − d < r, contradicting minimality of r.",
                "",
                "So 0 ≤ r < d and a = dq + r.        ∎",
            ],
            "after": [
                "Course 6 opens with this theorem and uses it in every lesson. Here it is "
                "an example of the technique; there it is the foundation of modular "
                "arithmetic. The uniqueness of `q` and `r` needs a separate short argument."
            ],
        },
        "quiz_title": "Well-ordering",
        "quiz": [
            {"q": "Which set has no least element?",
             "a": ["`{n ∈ ℕ : n &gt; 5}`", "the positive rationals",
                   "`{2, 4, 6, 8}`", "`{n ∈ ℕ : n is prime}`"],
             "c": 1,
             "why": "For any positive rational `q`, `q/2` is smaller and still positive. "
                    "Every nonempty subset of `ℕ` does have one."},
            {"q": "Well-ordering and mathematical induction are:",
             "a": ["unrelated", "equivalent — each can be derived from the other",
                   "induction is stronger", "well-ordering is stronger"],
             "c": 1,
             "why": "The lesson derives induction from well-ordering; the reverse "
                    "derivation is equally short. Which is called the axiom is a choice."},
            {"q": "In a minimal-counterexample proof, the contradiction usually comes from:",
             "a": ["the base case being false",
                   "producing a smaller counterexample, or showing the claim holds at `m`",
                   "the set being infinite",
                   "assuming the claim is true"],
             "c": 1,
             "why": "Minimality is the lever: anything smaller than `m` satisfies the "
                    "claim, and using that to establish it at `m` is the contradiction."},
        ],
        "mistakes": [
            ("Assuming well-ordering holds for `ℤ` or `ℚ`",
             "It does not. A minimal-counterexample argument over the integers or the "
             "rationals needs a lower bound before it is legitimate."),
            ("Forgetting to show the set is nonempty",
             "Well-ordering applies only to nonempty sets. In the division algorithm "
             "proof, exhibiting one member of `S` was a necessary step."),
            ("Taking the least element of a set that is not a subset of `ℕ`",
             "The set in the division algorithm proof was constructed to consist of "
             "non-negative integers precisely so the principle would apply."),
        ],
        "standard": ("Finish when you can prove induction from well-ordering unaided.",
                     "Write the argument out: assume the set of counterexamples is "
                     "nonempty, take its least element, and use the base case and the step "
                     "to contradict minimality. Understanding why induction is valid makes "
                     "the next four lessons mechanical."),
        "note": "Every set can be well-ordered &mdash; this is the well-ordering theorem, "
                "and it is equivalent to the axiom of choice. That is a far deeper "
                "statement than the principle here, which is only about `ℕ` and needs no "
                "such machinery.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "mathematical-induction",
        "title": "Mathematical Induction",
        "module": "Induction",
        "one_line": "Base case, inductive step, conclusion — and the step must use the hypothesis.",
        "summary": (
            "The technique in full: what each part does, how to write it, and the three "
            "ways an induction proof is wrong &mdash; no base case, an unused "
            "hypothesis, and a step proved only for a particular `k`."
        ),
        "key": [
            "1. BASE CASE:      prove P(n₀)",
            "2. INDUCTIVE STEP: assume P(k) for arbitrary k ≥ n₀, prove P(k+1)",
            "3. CONCLUDE:       P(n) holds for all n ≥ n₀",
            "The step must USE P(k). A step that does not is not induction.",
        ],
        "key_label": "Three parts, all required",
        "concepts_intro": (
            "Induction proves infinitely many statements by proving two: one specific "
            "case, and one implication that holds generally."
        ),
        "concepts": [
            ("The step is a conditional, proved for arbitrary `k`",
             "You are not assuming `P(k)` is true for all `k`. You are proving the "
             "implication `P(k) → P(k+1)`, which is a direct proof of a conditional."),
            ("The base case anchors the chain",
             "Without it the implications form a chain with nothing at the start. "
             "`n = k+1` provable from `n = k` proves nothing on its own."),
            ("The hypothesis must actually be used",
             "If the step never invokes `P(k)`, you have proved `P(k+1)` outright and "
             "written induction around a direct proof. That is usually a sign the "
             "statement was easier than it looked &mdash; or that the proof is wrong."),
        ],
        "read_title": "The technique",
        "read_intro": "The three parts, the standard example, and the three failure modes.",
        "body": [
            ("thm", ("Principle of mathematical induction",
                     "Let `P(n)` be a statement about integers `n ≥ n₀`. If `P(n₀)` holds, "
                     "and `P(k) → P(k+1)` for every `k ≥ n₀`, then `P(n)` holds for every "
                     "`n ≥ n₀`.")),
            ("p", "The domino picture is standard and slightly misleading. It is right "
                  "that the base case tips the first domino and the step is the guarantee "
                  "that each knocks over the next. It is misleading in suggesting a process "
                  "that takes time: the conclusion is not that every `P(n)` will eventually "
                  "be proved, but that every `P(n)` is true."),
            ("thm", ("Sum of the first `n` positive integers",
                     "For every `n ≥ 1`, `1 + 2 + ⋯ + n = n(n+1)/2`.")),
            ("proof", [
                "<strong>Base case.</strong> For `n = 1` the left side is 1 and the right "
                "is `1 · 2 / 2 = 1`. They agree.",
                "<strong>Inductive step.</strong> Let `k ≥ 1` be arbitrary and assume "
                "`1 + 2 + ⋯ + k = k(k+1)/2` &mdash; the inductive hypothesis. Then",
                "`1 + 2 + ⋯ + k + (k+1) = k(k+1)/2 + (k+1)` &mdash; here the hypothesis "
                "was used to replace the first `k` terms &mdash; `= (k+1)(k+2)/2`, "
                "which is the claim at `k+1`.",
                "<strong>Conclusion.</strong> By induction the formula holds for every "
                "`n ≥ 1`.",
            ]),
            ("p", "The sentence \"here the hypothesis was used\" is not padding. It is the "
                  "sentence a reader checks for, and a proof that cannot point to it is "
                  "not an induction proof."),
            ("h3", "Three ways to get it wrong"),
            ("ul", [
                "<strong>No base case.</strong> Consider `P(n)`: \"`n = n + 1`\". The step "
                "is fine &mdash; if `k = k+1` then adding 1 gives `k+1 = k+2` &mdash; and "
                "the statement is false for every `n`. The base case is what fails.",
                "<strong>The hypothesis is never used.</strong> If the step proves "
                "`P(k+1)` from scratch, the proof is a direct proof with an induction "
                "wrapper. Not wrong, but not induction &mdash; and often it means the step "
                "was misread.",
                "<strong>The step is proved for one `k`.</strong> Verifying `P(3) → P(4)` "
                "is not the inductive step. `k` must be arbitrary, exactly as in any "
                "universally quantified proof.",
            ]),
            ("example", ("The classic bogus proof",
                         "\"All horses are the same colour.\" Base: one horse, trivially. "
                         "Step: given `k+1` horses, the first `k` are the same colour by "
                         "hypothesis, and the last `k` are too, so all `k+1` agree. The "
                         "flaw is at `k = 1`: the two groups of one horse do not overlap, "
                         "so nothing links them. The step fails for exactly one value of "
                         "`k`, and one failure breaks the chain.")),
            ("p", "That example is worth more than its joke. It shows that an inductive "
                  "step can be correct for every `k` but one, and that the whole proof "
                  "collapses at that point. Checking the step at the smallest values is a "
                  "cheap and effective habit."),
        ],
        "lab": ("induction", {
            "statement": "odd",
            "panel_title": "The step, and the checks",
            "panel_intro": "The inductive step for each statement is shown in the note "
                           "below the controls. The table only checks cases &mdash; the "
                           "step is what makes the claim general.",
        }),
        "steps_title": "Writing an induction proof",
        "steps_intro": "Four sentences, in this order, every time.",
        "steps": [
            ("State `P(n)` precisely",
             "Write the statement being proved as a formula in `n`. Vague statements "
             "produce proofs that cannot be checked."),
            ("Prove the base case",
             "Evaluate both sides at `n₀` and show they agree. Say which `n₀` you are "
             "using, especially when it is not 1."),
            ("Assume `P(k)` for arbitrary `k ≥ n₀`, and say so",
             "Write the hypothesis out in full. A hypothesis you did not write is one you "
             "will not notice failing to use."),
            ("Derive `P(k+1)`, pointing at where the hypothesis entered",
             "The algebra usually splits off the `(k+1)` term and replaces the rest using "
             "the hypothesis. Name that substitution."),
        ],
        "worked": {
            "title": "Prove `1 + 3 + 5 + ⋯ + (2n − 1) = n²`",
            "intro": ["The sum of the first `n` odd numbers."],
            "lines": [
                "BASE   n = 1:   left = 1,   right = 1² = 1.     ✓",
                "",
                "STEP   Let k ≥ 1 and assume  1 + 3 + … + (2k−1) = k².",
                "",
                "       The sum to k+1 adds the next odd number, 2(k+1)−1 = 2k+1:",
                "",
                "         1 + 3 + … + (2k−1) + (2k+1)",
                "       =        k²          + (2k+1)      ← hypothesis used HERE",
                "       = k² + 2k + 1",
                "       = (k+1)²                            ← the claim at k+1",
                "",
                "CONCLUDE  By induction the identity holds for every n ≥ 1.      ∎",
            ],
            "after": [
                "The step has exactly one interesting move: recognising `k² + 2k + 1` as "
                "`(k+1)²`. Every induction proof of a sum formula has this shape &mdash; "
                "peel off the last term, substitute, and recognise the target."
            ],
        },
        "quiz_title": "Induction",
        "quiz": [
            {"q": "In the inductive step you assume:",
             "a": ["`P(n)` for all `n`", "`P(k)` for one arbitrary `k`",
                   "`P(k+1)`", "nothing"],
             "c": 1,
             "why": "You assume `P(k)` for an arbitrary `k` and derive `P(k+1)`. That is a "
                    "direct proof of the conditional `P(k) → P(k+1)`."},
            {"q": "A proof has a correct step and no base case. What is established?",
             "a": ["The statement for all `n`",
                   "The statement for all `n ≥ 1`",
                   "Nothing — the chain has no starting point",
                   "The statement for even `n`"],
             "c": 2,
             "why": "\"`n = n+1`\" has a perfectly correct inductive step and is false "
                    "everywhere. The base case is what anchors the chain."},
            {"q": "The all-horses proof fails because:",
             "a": ["the base case is wrong",
                   "the step fails at `k = 1`, where the two subgroups do not overlap",
                   "induction does not apply to horses",
                   "the statement is unprovable"],
             "c": 1,
             "why": "The step needs the two overlapping subgroups to share a horse, which "
                    "they do for `k ≥ 2` and not for `k = 1`. One broken link breaks the "
                    "chain."},
        ],
        "mistakes": [
            ("Omitting the base case",
             "Without it the implications prove nothing. It is one line and it is the line "
             "that makes the rest mean something."),
            ("Never using the inductive hypothesis",
             "If the step does not invoke `P(k)`, ask what you have actually proved. "
             "Sometimes it is a stronger direct result; more often the step is wrong."),
            ("Assuming what is to be proved",
             "\"Assume `P(k+1)`\" is circular. The hypothesis is `P(k)`, and the "
             "distinction is the whole technique."),
        ],
        "standard": ("Finish when you can point at the line where the hypothesis was used.",
                     "Prove `2 + 4 + ⋯ + 2n = n(n+1)` and then mark the exact substitution "
                     "that used the hypothesis. If you cannot mark it, the proof is either "
                     "not induction or not finished."),
        "note": "Induction proves statements about `ℕ`. Extending it to other structures "
                "&mdash; lists, trees, formulas &mdash; requires structural induction, "
                "which is lesson 7 and is the same idea over a different well-founded "
                "order.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "induction-with-sums-and-products",
        "title": "Induction with Sums and Products",
        "module": "Induction",
        "one_line": "The standard family of identities, and the pattern they share.",
        "summary": (
            "Sums of integers, squares, cubes, geometric series and telescoping sums. "
            "Every proof has the same shape, and recognising it makes these routine."
        ),
        "key": [
            "Σ i        = n(n+1)/2",
            "Σ i²       = n(n+1)(2n+1)/6",
            "Σ i³       = (n(n+1)/2)²        = (Σ i)²",
            "Σ arⁱ      = a(rⁿ⁺¹ − 1)/(r − 1)      geometric, r ≠ 1",
        ],
        "key_label": "Four identities worth knowing",
        "concepts_intro": (
            "These proofs are mechanical once the pattern is visible: peel, substitute, "
            "factor."
        ),
        "concepts": [
            ("Peel off the last term",
             "`Σ_{i≤k+1} f(i) = (Σ_{i≤k} f(i)) + f(k+1)`. This split is what lets the "
             "hypothesis apply to the first part."),
            ("Substitute the hypothesis",
             "Replace the sum to `k` by its closed form. From here it is algebra with no "
             "sums in it."),
            ("Factor toward the target",
             "Write the claim at `k+1` first, so you know what you are aiming at. Working "
             "without a target is how these proofs stall."),
        ],
        "read_title": "The standard sums",
        "read_intro": "Notation, then the proofs, then a route that avoids induction entirely.",
        "body": [
            ("def", ("Summation notation",
                     "`Σ_{i=1}^{n} f(i)` means `f(1) + f(2) + ⋯ + f(n)`. The index `i` is "
                     "bound; the sum is empty and equal to 0 when the upper limit is below "
                     "the lower. Products use `Π` and an empty product is 1.")),
            ("thm", ("Sum of squares",
                     "For `n ≥ 1`, `1² + 2² + ⋯ + n² = n(n+1)(2n+1)/6`.")),
            ("proof", [
                "<strong>Base.</strong> At `n = 1`: left is 1, right is "
                "`1 · 2 · 3 / 6 = 1`.",
                "<strong>Step.</strong> Assume the identity at `k`. Then",
                "`Σ_{i≤k+1} i² = k(k+1)(2k+1)/6 + (k+1)²` by the hypothesis "
                "`= (k+1)[k(2k+1) + 6(k+1)]/6 = (k+1)(2k² + 7k + 6)/6 "
                "= (k+1)(k+2)(2k+3)/6`,",
                "which is the claim at `k+1`, since `2(k+1)+1 = 2k+3`.",
            ]),
            ("p", "The factoring step `2k² + 7k + 6 = (k+2)(2k+3)` is the only place "
                  "cleverness is required, and it is found by knowing the target: the "
                  "claim at `k+1` must contain `(k+2)`, so `(k+2)` is what to look for."),
            ("thm", ("Geometric series",
                     "For `r ≠ 1` and `n ≥ 0`, "
                     "`a + ar + ar² + ⋯ + arⁿ = a(rⁿ⁺¹ − 1)/(r − 1)`.")),
            ("proof", [
                "<strong>Base.</strong> At `n = 0` the left is `a` and the right is "
                "`a(r − 1)/(r − 1) = a`.",
                "<strong>Step.</strong> Assume the formula at `k`. Adding the next term,",
                "`a(r^{k+1} − 1)/(r − 1) + ar^{k+1} = [a(r^{k+1} − 1) + ar^{k+1}(r − 1)]/(r − 1) "
                "= a(r^{k+2} − 1)/(r − 1)`,",
                "which is the claim at `k+1`.",
            ]),
            ("p", "The condition `r ≠ 1` is not decoration: at `r = 1` the denominator "
                  "vanishes and the sum is simply `a(n+1)`. Every hypothesis in a theorem "
                  "statement is doing work somewhere, and finding where is a good habit."),
            ("h3", "Telescoping, and proofs without induction"),
            ("p", "Some sums collapse without any induction at all. If `f(i) = g(i) − "
                  "g(i−1)`, then `Σ_{i=1}^{n} f(i) = g(n) − g(0)`, because every "
                  "intermediate term appears once positively and once negatively."),
            ("example", ("A telescoping sum",
                         "`Σ_{i=1}^{n} 1/(i(i+1))`. Since `1/(i(i+1)) = 1/i − 1/(i+1)`, "
                         "the sum is `(1 − 1/2) + (1/2 − 1/3) + ⋯ + (1/n − 1/(n+1)) "
                         "= 1 − 1/(n+1) = n/(n+1)`. No induction needed, though induction "
                         "would work.")),
            ("p", "Gauss's pairing argument for `Σ i` is another such route: add the sum to "
                  "its own reversal, obtaining `n` copies of `n+1`, hence `n(n+1)/2`. "
                  "Induction verifies a formula you already have; arguments like these "
                  "produce one."),
        ],
        "lab": ("induction", {
            "statement": "cubes",
            "panel_title": "The sum identities, checked",
            "panel_intro": "The rational sum at the end of the list is computed in exact "
                           "fractions, so its equality with `n/(n+1)` is not a rounding "
                           "artefact.",
        }),
        "steps_title": "Proving a sum identity",
        "steps_intro": "Write the target first; the algebra then has somewhere to go.",
        "steps": [
            ("Write the claim at `k+1` before starting",
             "Substituting `k+1` into the formula tells you what the algebra must produce. "
             "Working forward blindly is how these stall."),
            ("Peel the last term off the sum",
             "`Σ_{i≤k+1} = (Σ_{i≤k}) + f(k+1)`. This is the only structural move."),
            ("Substitute the hypothesis and factor",
             "Take out the common factor &mdash; usually `(k+1)` &mdash; and simplify what "
             "remains toward the target."),
            ("Check the base case at the right place",
             "`n = 0` and `n = 1` are different starting points and give different base "
             "cases. Use whichever the statement claims."),
        ],
        "worked": {
            "title": "Prove `Σ_{i=1}^{n} i·i! = (n+1)! − 1`",
            "intro": ["A less familiar identity, same shape of proof."],
            "lines": [
                "BASE   n = 1:  left = 1·1! = 1,   right = 2! − 1 = 1.     ✓",
                "",
                "STEP   Assume  Σ_{i≤k} i·i! = (k+1)! − 1.",
                "",
                "       Σ_{i≤k+1} i·i!  =  [(k+1)! − 1] + (k+1)(k+1)!",
                "                       =  (k+1)!·[1 + (k+1)] − 1",
                "                       =  (k+1)!·(k+2) − 1",
                "                       =  (k+2)! − 1                ← claim at k+1",
                "",
                "CONCLUDE  Holds for all n ≥ 1.        ∎",
            ],
            "after": [
                "The move that makes it work is factoring `(k+1)!` out of both terms, "
                "which is available because `(k+1)(k+1)!` shares it. Recognising "
                "`(k+1)!(k+2) = (k+2)!` is the same kind of target-driven step as before."
            ],
        },
        "quiz_title": "Sums",
        "quiz": [
            {"q": "`Σ_{i=1}^{n} i³` equals:",
             "a": ["`n(n+1)(2n+1)/6`", "`(n(n+1)/2)²`", "`n²(n+1)/2`", "`n⁴/4`"],
             "c": 1,
             "why": "The sum of the first `n` cubes is the square of the sum of the first "
                    "`n` integers &mdash; a striking identity, and one induction verifies "
                    "in three lines."},
            {"q": "In the inductive step for a sum identity, the first move is:",
             "a": ["substitute `n = k+1` into the closed form",
                   "split off the `(k+1)`th term so the hypothesis applies to the rest",
                   "differentiate",
                   "check the base case again"],
             "c": 1,
             "why": "The hypothesis speaks about the sum to `k`, so the sum to `k+1` must "
                    "be written as that sum plus one term before it can be used."},
            {"q": "The geometric series formula requires `r ≠ 1` because:",
             "a": ["the series diverges", "the denominator `r − 1` is zero",
                   "the base case fails", "the sum is infinite"],
             "c": 1,
             "why": "At `r = 1` every term is `a` and the sum is `a(n+1)`; the closed form "
                    "divides by zero. Each hypothesis of a theorem is doing work somewhere."},
        ],
        "mistakes": [
            ("Not writing the target before doing the algebra",
             "The claim at `k+1` tells you which factorisation to aim for. Without it the "
             "step becomes trial and error."),
            ("Peeling the wrong term",
             "The sum to `k+1` splits as the sum to `k` plus `f(k+1)`. Splitting off the "
             "first term instead leaves a sum the hypothesis does not describe."),
            ("Using the wrong base case",
             "A formula claimed for `n ≥ 0` needs `n = 0` checked. Starting at 1 leaves "
             "the claim unproved exactly where it is most likely to be false."),
        ],
        "standard": ("Finish when these proofs are mechanical.",
                     "Prove `Σ_{i=1}^{n} (2i − 1)² = n(2n−1)(2n+1)/3` &mdash; the sum of "
                     "the squares of the odd numbers. Same three moves, slightly heavier "
                     "algebra, and no new idea required."),
        "note": "Sums of `k`th powers have closed forms for every `k`, given by Faulhaber's "
                "formula, and each is a polynomial of degree `k+1` in `n`. Induction "
                "verifies any one of them; producing them requires a different technique.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "induction-with-inequalities-and-divisibility",
        "title": "Induction with Inequalities and Divisibility",
        "module": "Induction",
        "one_line": "Two families where the base case is often not `n = 1`.",
        "summary": (
            "Inequalities like `2ⁿ > n²` fail for small `n` and hold from some point on, "
            "so the base case moves. Divisibility claims need the hypothesis to supply a "
            "multiple, which changes what the algebra is aiming at."
        ),
        "key": [
            "2ⁿ > n²        FALSE for n = 2, 3, 4;  TRUE from n = 5",
            "n! > 2ⁿ        TRUE from n = 4",
            "divisibility:  write the k+1 case as (k case) + (obvious multiple)",
            "Bernoulli:     (1 + x)ⁿ ≥ 1 + nx   for x ≥ −1",
        ],
        "key_label": "Where the base case moves",
        "concepts_intro": (
            "Both families need the same three parts, and both introduce a wrinkle: "
            "finding where the claim actually starts, and knowing what the step must produce."
        ),
        "concepts": [
            ("The base case is where the claim starts holding",
             "`2ⁿ > n²` is false at `n = 2, 3, 4`. Its base case is `n = 5`, and claiming "
             "it from `n = 1` makes the statement false."),
            ("Divisibility steps aim for an explicit multiple",
             "To show `d | f(k+1)`, rewrite `f(k+1)` as `f(k)` plus something visibly "
             "divisible by `d`, then apply the hypothesis."),
            ("Inequality steps often need a second fact",
             "Going from `2^{k+1} > 2k²` to `(k+1)²` needs `2k² ≥ (k+1)²`, which is true "
             "only for `k ≥ 3`. That side condition is part of the proof."),
        ],
        "read_title": "Inequalities and divisibility",
        "read_intro": "One worked proof of each, with the side conditions made explicit.",
        "body": [
            ("h3", "Inequalities"),
            ("thm", ("`2ⁿ > n²` for `n ≥ 5`",
                     "The inequality fails at `n = 2, 3, 4` and holds for every `n ≥ 5`.")),
            ("proof", [
                "<strong>Base.</strong> At `n = 5`: `2⁵ = 32 &gt; 25 = 5²`.",
                "<strong>Step.</strong> Let `k ≥ 5` and assume `2^k &gt; k²`. Then "
                "`2^{k+1} = 2 · 2^k &gt; 2k²` by the hypothesis.",
                "It remains to show `2k² ≥ (k+1)²` for `k ≥ 5`. Expanding, this is "
                "`2k² ≥ k² + 2k + 1`, that is `k² − 2k − 1 ≥ 0`, that is "
                "`(k−1)² ≥ 2`, which holds for every `k ≥ 3` and in particular for `k ≥ 5`.",
                "Chaining: `2^{k+1} &gt; 2k² ≥ (k+1)²`.",
            ]),
            ("p", "The second half of that step is a separate inequality that has nothing "
                  "to do with induction, and it is where the proof actually lives. "
                  "Induction supplied `2^k &gt; k²`; ordinary algebra supplied the bridge "
                  "from `2k²` to `(k+1)²`."),
            ("p", "Finding the right base case is part of the problem. Evaluate the claim "
                  "at `n = 1, 2, 3, …` until it starts holding, and check that it does not "
                  "fail again later &mdash; which the inductive step is what guarantees."),
            ("thm", ("Bernoulli's inequality",
                     "For `x ≥ −1` and `n ≥ 0`, `(1 + x)ⁿ ≥ 1 + nx`.")),
            ("proof", [
                "<strong>Base.</strong> At `n = 0` both sides are 1.",
                "<strong>Step.</strong> Assume `(1+x)^k ≥ 1 + kx`. Since `x ≥ −1`, the "
                "factor `1 + x` is non-negative, so multiplying the inequality by it "
                "preserves the direction:",
                "`(1+x)^{k+1} ≥ (1 + kx)(1 + x) = 1 + (k+1)x + kx² ≥ 1 + (k+1)x`,",
                "the last step because `kx² ≥ 0`.",
            ]),
            ("p", "The hypothesis `x ≥ −1` was used exactly once, to justify multiplying "
                  "an inequality by `1 + x` without flipping it. That is the kind of step "
                  "that is easy to perform silently and wrong to perform without the "
                  "condition."),
            ("h3", "Divisibility"),
            ("thm", ("`3 | (n³ + 2n)` for every `n ≥ 0`",
                     "The integer `n³ + 2n` is divisible by 3 for every natural `n`.")),
            ("proof", [
                "<strong>Base.</strong> At `n = 0`: `0` is divisible by 3.",
                "<strong>Step.</strong> Assume `3 | (k³ + 2k)`, so `k³ + 2k = 3m` for some "
                "integer `m`. Then",
                "`(k+1)³ + 2(k+1) = k³ + 3k² + 3k + 1 + 2k + 2 = (k³ + 2k) + 3(k² + k + 1) "
                "= 3m + 3(k² + k + 1) = 3(m + k² + k + 1)`,",
                "which is divisible by 3.",
            ]),
            ("p", "The whole technique is in the regrouping: separate the expression into "
                  "the `k` case plus a remainder, and show the remainder is visibly a "
                  "multiple. If the remainder is not visibly a multiple, the regrouping was "
                  "wrong, not the claim."),
        ],
        "lab": ("induction", {
            "statement": "pow",
            "panel_title": "Find where the claim starts",
            "panel_intro": "`2ⁿ > n²` is selected. Look at the small `n`: the lab counts "
                           "only from the value where the statement claims to hold, and "
                           "the rows below it show why the base case is 5 and not 1.",
        }),
        "steps_title": "Inequalities and divisibility",
        "steps_intro": "Locate the base case first; it is not always 1.",
        "steps": [
            ("Evaluate the claim at small `n`",
             "Find the first `n` where it holds. That is your base case, and starting "
             "earlier makes the theorem false."),
            ("For an inequality, chain through the hypothesis",
             "Apply the hypothesis to get a bound, then bridge from that bound to the "
             "target with ordinary algebra &mdash; and state the range where the bridge "
             "holds."),
            ("For divisibility, regroup as (`k` case) + (multiple)",
             "Expand `f(k+1)`, extract `f(k)`, and show what remains is a visible multiple "
             "of `d`."),
            ("Check every inequality manipulation",
             "Multiplying by a possibly-negative quantity flips the direction. Bernoulli's "
             "hypothesis `x ≥ −1` exists for exactly this reason."),
        ],
        "worked": {
            "title": "Prove `n! > 2ⁿ` for `n ≥ 4`",
            "intro": ["It fails at `n = 1, 2, 3`: `1 &lt; 2`, `2 &lt; 4`, `6 &lt; 8`."],
            "lines": [
                "BASE   n = 4:   4! = 24  >  16 = 2⁴.     ✓",
                "",
                "STEP   Let k ≥ 4 and assume k! > 2ᵏ.",
                "",
                "       (k+1)! = (k+1)·k!",
                "              > (k+1)·2ᵏ            ← hypothesis, and k+1 > 0",
                "              ≥ 5·2ᵏ                ← since k ≥ 4",
                "              > 2·2ᵏ  =  2ᵏ⁺¹",
                "",
                "CONCLUDE  n! > 2ⁿ for every n ≥ 4.        ∎",
            ],
            "after": [
                "The `k + 1 > 0` note matters: multiplying an inequality by a factor is "
                "only safe when the factor is positive. It is true here for trivial "
                "reasons, and writing it is the difference between a proof and a "
                "manipulation that happens to work."
            ],
        },
        "quiz_title": "Inequalities and divisibility",
        "quiz": [
            {"q": "What is the correct base case for `2ⁿ > n²`?",
             "a": ["`n = 0`", "`n = 1`", "`n = 5`", "`n = 2`"],
             "c": 2,
             "why": "It holds at `n = 0` and `n = 1` but fails at 2, 3 and 4, so the claim "
                    "is stated for `n ≥ 5` and the base case is 5."},
            {"q": "To prove `d | f(k+1)` from `d | f(k)`, you should:",
             "a": ["divide `f(k+1)` by `d`",
                   "write `f(k+1)` as `f(k)` plus a visible multiple of `d`",
                   "show `f(k+1) &gt; f(k)`",
                   "check a few values"],
             "c": 1,
             "why": "The hypothesis gives you a multiple of `d`; the step needs the extra "
                    "part to be one too. The regrouping is the whole technique."},
            {"q": "Bernoulli's inequality assumes `x ≥ −1` because:",
             "a": ["negative `x` makes it false",
                   "`1 + x` must be non-negative for the inequality to survive multiplication",
                   "the base case fails otherwise",
                   "`x` must be an integer"],
             "c": 1,
             "why": "The step multiplies both sides by `1 + x`. If that factor were "
                    "negative the inequality would reverse, and the argument would break."},
        ],
        "mistakes": [
            ("Starting the induction at `n = 1` out of habit",
             "Several standard inequalities fail for small `n`. The base case belongs "
             "where the claim starts holding, and stating it elsewhere makes the theorem "
             "false as written."),
            ("Multiplying an inequality by a possibly-negative quantity",
             "The direction flips. Every such step needs the sign of the factor stated."),
            ("Leaving the divisibility remainder unfactored",
             "\"`3k² + 3k + 3` is divisible by 3\" is only convincing once written as "
             "`3(k² + k + 1)`. Show the factor."),
        ],
        "standard": ("Finish when you can locate a base case by testing rather than by "
                     "assuming.",
                     "Determine the smallest `n` for which `n² &lt; 2ⁿ` holds and stays "
                     "true, prove it from there, and state explicitly the side inequality "
                     "your step needed. Both halves are the lesson."),
        "note": "An inequality proof usually splits into an induction and a piece of "
                "ordinary algebra. Isolating the second piece as its own claim &mdash; "
                "\"it suffices to show `2k² ≥ (k+1)²` for `k ≥ 3`\" &mdash; makes the "
                "proof much easier to check.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "strong-induction",
        "title": "Strong Induction",
        "module": "Induction",
        "one_line": "Assume every earlier case, not only the previous one.",
        "summary": (
            "When `P(k+1)` depends on cases further back than `P(k)`, ordinary induction "
            "gives you the wrong hypothesis. Strong induction assumes all of "
            "`P(n₀), …, P(k)` and is exactly as valid."
        ),
        "key": [
            "ordinary:  P(k)          ⟹  P(k+1)",
            "strong:    P(n₀)…P(k)    ⟹  P(k+1)",
            "Same power. Strong induction proves nothing ordinary cannot.",
            "Use it when the step reaches back an unknown distance.",
        ],
        "key_label": "A stronger hypothesis, the same theorem",
        "concepts_intro": (
            "Strong induction is not a stronger technique. It is a more convenient "
            "hypothesis for claims whose step does not reach back exactly one step."
        ),
        "concepts": [
            ("The hypothesis covers everything below `k+1`",
             "You may use any of `P(n₀)` through `P(k)`, and you need not know in advance "
             "which."),
            ("It is equivalent to ordinary induction",
             "Apply ordinary induction to `Q(n)` = \"`P(m)` holds for all `n₀ ≤ m ≤ n`\" "
             "and strong induction falls out. Neither proves more than the other."),
            ("Multiple base cases are often needed",
             "If the step reaches back two places, two base cases are required &mdash; "
             "otherwise the step at `k+1 = n₀+1` has nothing to stand on."),
        ],
        "read_title": "Strong induction",
        "read_intro": "Statement, the two standard applications, and the base-case trap.",
        "body": [
            ("thm", ("Strong induction",
                     "Let `P(n)` be a statement about `n ≥ n₀`. If `P(n₀)` holds and, for "
                     "every `k ≥ n₀`, the truth of `P(n₀), …, P(k)` implies `P(k+1)`, then "
                     "`P(n)` holds for all `n ≥ n₀`.")),
            ("p", "Nothing is gained in strength. Define `Q(n)` to be \"`P(m)` holds for "
                  "all `n₀ ≤ m ≤ n`\". Ordinary induction applied to `Q` gives exactly "
                  "strong induction for `P`. What is gained is a hypothesis that matches "
                  "the shape of certain arguments."),
            ("thm", ("Every integer `n ≥ 2` is a product of primes",
                     "Every integer greater than 1 can be written as a product of one or "
                     "more primes.")),
            ("proof", [
                "<strong>Base.</strong> `2` is prime, so it is a product of one prime.",
                "<strong>Step.</strong> Let `k ≥ 2` and assume every integer from 2 to `k` "
                "is a product of primes. Consider `k+1`.",
                "If `k+1` is prime, it is a product of one prime and we are done. "
                "Otherwise `k+1 = ab` with `2 ≤ a, b ≤ k`. By the strong hypothesis both "
                "`a` and `b` are products of primes, so their product `k+1` is too.",
            ]),
            ("p", "Ordinary induction is useless here. Knowing that `k` factors says "
                  "nothing about `k+1`, and the factors `a` and `b` could be anywhere below "
                  "`k+1`. The hypothesis has to cover them all, and only strong induction "
                  "provides that."),
            ("h3", "Multiple base cases"),
            ("thm", ("Every amount of postage `n ≥ 8` can be made from 3¢ and 5¢ stamps",
                     "For every `n ≥ 8` there are non-negative integers `a, b` with "
                     "`n = 3a + 5b`.")),
            ("proof", [
                "<strong>Bases.</strong> `8 = 3 + 5`, `9 = 3 + 3 + 3`, `10 = 5 + 5`. Three "
                "base cases are needed because the step reaches back three places.",
                "<strong>Step.</strong> Let `k ≥ 10` and assume the claim for every value "
                "from 8 to `k`. Then `k + 1 − 3 = k − 2 ≥ 8`, so by the hypothesis `k − 2` "
                "is expressible; adding one 3¢ stamp expresses `k+1`.",
            ]),
            ("p", "Three base cases, because the step goes back three. Providing only "
                  "`n = 8` would leave the step at `k+1 = 9` and `k+1 = 10` appealing to "
                  "`6` and `7`, which are outside the claim &mdash; and indeed 7 cannot be "
                  "made at all. Counting the base cases correctly is the whole difficulty "
                  "of this style of proof."),
            ("h3", "Strong induction and recursion"),
            ("p", "Strong induction is the natural partner of a recursive definition whose "
                  "recursive calls are not on `n − 1`. Merge sort splits at `n/2`; binary "
                  "search halves; the Fibonacci recurrence reaches back two. In every case "
                  "the correctness proof needs a hypothesis covering all smaller values, "
                  "which is what lesson 8 does."),
            ("example", ("Fibonacci and strong induction",
                         "Proving a property of `Fₙ = Fₙ₋₁ + Fₙ₋₂` requires both `Fₙ₋₁` and "
                         "`Fₙ₋₂`, so it needs two base cases and a hypothesis covering two "
                         "steps back. Attempting it with ordinary induction leaves `Fₙ₋₂` "
                         "unavailable.")),
        ],
        "lab": ("induction", {
            "statement": "chords",
            "panel_title": "A statement that survives five checks",
            "panel_intro": "The chord-region claim gives 1, 2, 4, 8, 16 &mdash; five "
                           "consecutive powers of two &mdash; and then 31. No amount of "
                           "checking would have caught it; a proof would have.",
        }),
        "steps_title": "Writing a strong induction proof",
        "steps_intro": "Count how far the step reaches, then supply that many base cases.",
        "steps": [
            ("Decide whether ordinary induction suffices",
             "If `P(k+1)` follows from `P(k)` alone, use ordinary induction. Reaching for "
             "the stronger hypothesis unnecessarily obscures what the proof used."),
            ("State the strong hypothesis explicitly",
             "\"Assume `P(m)` for every `m` with `n₀ ≤ m ≤ k`.\" Writing it out is what "
             "keeps you from using a case outside the range."),
            ("Count how far back the step reaches",
             "The postage step used `k − 2`, three places back, so three base cases were "
             "needed. Miscounting here is the standard error."),
            ("Verify every base case",
             "Each one individually. A base case you assumed rather than checked is a hole "
             "at exactly the place the step cannot cover."),
        ],
        "worked": {
            "title": "Every `n ≥ 12` is `4a + 5b` for non-negative integers",
            "intro": ["The step will reach back four, so four base cases are needed."],
            "lines": [
                "BASES  12 = 4+4+4      13 = 4+4+5      14 = 4+5+5      15 = 5+5+5",
                "",
                "STEP   Let k ≥ 15 and assume the claim for every m with 12 ≤ m ≤ k.",
                "",
                "       k + 1 − 4  =  k − 3  ≥  12,",
                "       so k − 3 = 4a + 5b by the hypothesis,",
                "       and k + 1 = 4(a+1) + 5b.",
                "",
                "CONCLUDE  Every n ≥ 12 is expressible.        ∎",
                "",
                "Why four bases:  the step covers k+1 ≥ 16 only.",
                "12 through 15 are not reached by it and must be checked.",
            ],
            "after": [
                "The largest amount that cannot be made from 4 and 5 is 11, which is the "
                "Frobenius number of the pair. For coprime `a` and `b` it is always "
                "`ab − a − b`, here `20 − 4 − 5 = 11` &mdash; which is why the claim starts "
                "at 12 and not somewhere else."
            ],
        },
        "quiz_title": "Strong induction",
        "quiz": [
            {"q": "In strong induction the inductive hypothesis is:",
             "a": ["`P(k)`", "`P(k+1)`", "`P(m)` for every `m` from the base to `k`",
                   "`P(k)` and `P(k−1)`"],
             "c": 2,
             "why": "All earlier cases are available, which is what lets a step reach back "
                    "an unknown distance."},
            {"q": "The postage proof needs three base cases because:",
             "a": ["8, 9 and 10 are special",
                   "the step reaches back three places, so the first three values are not covered by it",
                   "3 + 5 = 8",
                   "strong induction always needs three"],
             "c": 1,
             "why": "The step derives `k+1` from `k−2`. For `k+1 = 9, 10, 11` that would "
                    "point at 6, 7, 8 &mdash; two of which are outside the claim."},
            {"q": "Strong induction can prove:",
             "a": ["strictly more than ordinary induction",
                   "exactly what ordinary induction can, more conveniently",
                   "less than ordinary induction",
                   "statements about real numbers"],
             "c": 1,
             "why": "Each derives the other. The choice is about which hypothesis matches "
                    "the argument, not about power."},
        ],
        "mistakes": [
            ("Supplying one base case when the step reaches back several",
             "The number of base cases must cover every value the step cannot reach. This "
             "is the single most common error in strong induction proofs."),
            ("Using a case outside the hypothesis range",
             "The hypothesis covers `n₀` to `k`. Appealing to `P(k+2)` or to `P(n₀ − 1)` "
             "is using something you have not got."),
            ("Reaching for strong induction by default",
             "If the step uses only `P(k)`, say so. Stating a stronger hypothesis than the "
             "proof needs hides what the argument actually depends on."),
        ],
        "standard": ("Finish when you can count the base cases from the step.",
                     "Prove that every `n ≥ 18` can be made from 4¢ and 7¢ stamps. Work out "
                     "how far back your step reaches before writing any base case, and "
                     "check that the number of bases matches."),
        "note": "The equivalence of ordinary induction, strong induction and well-ordering "
                "means a proof by one can always be rewritten as a proof by another. Which "
                "reads best depends entirely on the claim, and choosing well is a matter "
                "of exposition rather than correctness.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "recursive-definitions",
        "title": "Recursive Definitions",
        "module": "Recursion",
        "one_line": "Defining an object in terms of smaller instances of itself.",
        "summary": (
            "A recursive definition has a base clause and a recursive clause, and "
            "together they must reach every object exactly once. Sequences, sets and "
            "structures are all defined this way."
        ),
        "key": [
            "BASE       0! = 1",
            "RECURSIVE  n! = n · (n−1)!   for n ≥ 1",
            "Every object must be reachable from the base in finitely many steps.",
            "Recursive definition ⟷ induction proof: the same structure.",
        ],
        "key_label": "Two clauses, and a reachability condition",
        "concepts_intro": (
            "A recursive definition is well formed when every object it defines is built "
            "from the base in finitely many steps, and nothing is defined twice."
        ),
        "concepts": [
            ("Base clause and recursive clause",
             "The base gives the starting values outright; the recursive clause builds "
             "larger objects from smaller ones. Both are required."),
            ("The recursion must decrease",
             "Each application must move toward the base. A clause that refers to a larger "
             "or equal object defines nothing."),
            ("Definition and proof mirror each other",
             "A recursive definition with `k` base clauses is proved about by an induction "
             "with `k` base cases. The shapes match exactly, and that is the point."),
        ],
        "read_title": "Recursive definitions",
        "read_intro": "Sequences, sets and structures, and the condition that makes a definition legitimate.",
        "body": [
            ("h3", "Recursively defined sequences"),
            ("math", [
                "factorial     0! = 1                  n! = n·(n−1)!        n ≥ 1",
                "Fibonacci     F₀ = 0,  F₁ = 1         Fₙ = Fₙ₋₁ + Fₙ₋₂     n ≥ 2",
                "powers        a⁰ = 1                  aⁿ = a·aⁿ⁻¹          n ≥ 1",
                "Hanoi         H₁ = 1                  Hₙ = 2Hₙ₋₁ + 1       n ≥ 2",
            ]),
            ("p", "Fibonacci needs two base values because its recursive clause reaches "
                  "back two. The number of base clauses is determined by the recursion, not "
                  "chosen: one fewer and some values would be undefined, one more and the "
                  "definition might contradict itself."),
            ("def", ("Well-formed recursive definition",
                     "A recursive definition is <strong>well formed</strong> when every "
                     "object in its domain is produced by finitely many applications of "
                     "the clauses starting from a base object, and the clauses do not "
                     "assign two different values to one object.")),
            ("example", ("A definition that fails",
                         "\"`f(0) = 1` and `f(n) = f(n+1) − 1`\" defines nothing: computing "
                         "`f(1)` requires `f(2)`, which requires `f(3)`, and the recursion "
                         "never reaches the base. The clause must decrease.")),
            ("h3", "Recursively defined sets"),
            ("p", "Sets are defined the same way: name some elements outright, then give "
                  "rules for building more."),
            ("example", ("The set of even naturals",
                         "BASE: `0 ∈ E`. RECURSIVE: if `n ∈ E` then `n + 2 ∈ E`. Nothing "
                         "else is in `E`. That last sentence is not optional &mdash; "
                         "without it the definition permits any superset.")),
            ("example", ("Well-formed parenthesis strings",
                         "BASE: the empty string is well formed. RECURSIVE: if `s` is well "
                         "formed then so is `(s)`, and if `s` and `t` are well formed then "
                         "so is `st`. This generates `()`, `(())`, `()()`, `(()())` and "
                         "nothing else &mdash; and course 4 lesson 14 counts them.")),
            ("h3", "Recursively defined structures"),
            ("example", ("Binary trees",
                         "BASE: the empty tree is a binary tree. RECURSIVE: if `L` and `R` "
                         "are binary trees and `v` is a value, then the tree with root `v`, "
                         "left subtree `L` and right subtree `R` is a binary tree. Course 7 "
                         "lesson 12 traverses exactly this object.")),
            ("p", "This is where recursion earns its place. A binary tree has no obvious "
                  "\"size parameter\" to induct on, but it does have a structure, and "
                  "lesson 7's structural induction proves things about it directly."),
            ("thm", ("Recursion theorem, informally",
                     "Given a base value and a rule producing `f(n)` from `f(n−1)`, there "
                     "is exactly one function satisfying both. Existence and uniqueness "
                     "both follow from induction &mdash; which is why recursive definitions "
                     "are legitimate rather than merely suggestive.")),
        ],
        "lab": ("recurrence", {
            "preset": "hanoi",
            "panel_title": "A definition, unrolled",
            "panel_intro": "The left column applies the recursive clause repeatedly from "
                           "the base. The right evaluates the closed form. Nothing "
                           "guarantees they agree until they are computed separately and "
                           "compared.",
        }),
        "steps_title": "Writing a recursive definition",
        "steps_intro": "Base first, then the rule, then the closing sentence.",
        "steps": [
            ("Give enough base cases",
             "As many as the recursive clause reaches back. Fibonacci needs two; a "
             "three-term recurrence needs three."),
            ("Write the recursive clause so it decreases",
             "Every application must move toward a base. A clause referring to a larger "
             "argument defines nothing."),
            ("Say that nothing else qualifies",
             "For a recursively defined set, the sentence \"and nothing else is in `S`\" "
             "is what makes the definition determinate."),
            ("Unroll a few values",
             "Computing the first four or five entries catches an off-by-one in the base "
             "or the clause immediately."),
        ],
        "worked": {
            "title": "The Tower of Hanoi",
            "intro": ["Moving `n` discs between three pegs, never placing a larger on a smaller."],
            "lines": [
                "To move n discs from A to C:",
                "   1. move the top n−1 discs from A to B     (Hₙ₋₁ moves)",
                "   2. move the largest disc from A to C      (1 move)",
                "   3. move the n−1 discs from B to C         (Hₙ₋₁ moves)",
                "",
                "BASE       H₁ = 1",
                "RECURSIVE  Hₙ = 2Hₙ₋₁ + 1",
                "",
                "Unrolling:  1, 3, 7, 15, 31, 63, …           = 2ⁿ − 1",
                "",
                "With 64 discs and one move per second: 2⁶⁴ − 1 seconds,",
                "about 585 billion years.",
            ],
            "after": [
                "The recursive definition came directly from the structure of the problem "
                "&mdash; the largest disc can only move once everything above it is out of "
                "the way &mdash; and the closed form came afterwards. Lesson 10 shows how "
                "to derive `2ⁿ − 1` rather than guess it."
            ],
        },
        "quiz_title": "Recursive definitions",
        "quiz": [
            {"q": "How many base cases does `aₙ = aₙ₋₁ + aₙ₋₂` need?",
             "a": ["None", "One", "Two", "It depends on the values"],
             "c": 2,
             "why": "The clause reaches back two places, so `a₀` and `a₁` must be given "
                    "outright or `a₂` is undefined."},
            {"q": "Why does \"`f(0) = 1`, `f(n) = f(n+1) − 1`\" define nothing?",
             "a": ["The base case is wrong",
                   "The recursion increases, so it never reaches the base",
                   "It is circular",
                   "`f` is not injective"],
             "c": 1,
             "why": "Every application moves further from the base, so no value is ever "
                    "determined. A recursive clause must decrease."},
            {"q": "In a recursively defined set, the sentence \"and nothing else is in `S`\" is:",
             "a": ["optional", "required, or the definition permits any superset",
                   "the base clause", "a proof obligation"],
             "c": 1,
             "why": "Without it, `ℕ` would satisfy the definition of the even numbers. The "
                    "closing sentence is what makes the set the smallest one satisfying "
                    "the clauses."},
        ],
        "mistakes": [
            ("Too few base cases",
             "A two-term recurrence with one base value leaves everything undefined from "
             "the second term on. Count the reach of the clause."),
            ("A recursion that does not decrease",
             "Defining `f(n)` in terms of `f(n+1)` or `f(n)` produces no values at all. "
             "Every path must terminate at a base."),
            ("Omitting the closure sentence for a set",
             "The clauses say what belongs; only the closure says what does not. Without "
             "it the definition does not determine a set."),
        ],
        "standard": ("Finish when you can write a recursive definition and unroll it "
                     "correctly.",
                     "Define the set of binary strings with no two consecutive 1s "
                     "recursively, and unroll the count for lengths 1 to 6. You should get "
                     "2, 3, 5, 8, 13, 21 &mdash; Fibonacci, which lesson 9 explains."),
        "note": "The correspondence between recursive definitions and induction proofs is "
                "exact and worth relying on: a definition with two base clauses is proved "
                "about by an induction with two base cases, and a clause reaching back "
                "`k` places calls for strong induction.",
    },
]
