"""Course 1, lessons 08-14 — predicate logic and proof."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "predicates-and-quantifiers",
        "title": "Predicates and Quantifiers",
        "module": "Predicate logic",
        "one_line": "Turning open sentences into propositions.",
        "summary": (
            "A predicate is a sentence with a free variable. `∀` and `∃` bind that "
            "variable and produce something with a truth value &mdash; and both depend "
            "entirely on the domain, which is why an unstated domain is an unstated claim."
        ),
        "key": [
            "P(x) : \"x > 3\"        a predicate — no truth value yet",
            "∀x P(x)               true when P(x) holds for EVERY x in the domain",
            "∃x P(x)               true when P(x) holds for AT LEAST ONE x",
            "The domain is part of the statement, not context.",
        ],
        "key_label": "Predicate, then quantifier",
        "concepts_intro": (
            "Propositional logic cannot express \"every integer has a successor\". "
            "Predicates and quantifiers are what it takes."
        ),
        "concepts": [
            ("A predicate becomes a proposition when its variables are bound",
             "`P(x)` has no truth value; `P(5)` and `∀x P(x)` both do. Binding happens by "
             "substitution or by a quantifier."),
            ("The domain changes the answer",
             "`∃x (x² = 2)` is false over the rationals and true over the reals. Stating "
             "the domain is not pedantry &mdash; without it there is no claim."),
            ("`∀` over an empty domain is true",
             "Vacuous truth again: with nothing to check, nothing fails. Symmetrically, "
             "`∃` over an empty domain is false."),
        ],
        "read_title": "Predicates, domains and the two quantifiers",
        "read_intro": "What each quantifier asserts, and what it takes to establish or refute it.",
        "body": [
            ("def", ("Predicate",
                     "A <strong>predicate</strong> `P(x)` is a sentence containing a free "
                     "variable, which becomes a proposition once a value from the domain "
                     "is substituted. Predicates may have several variables: `Q(x, y)`.")),
            ("def", ("Domain of discourse",
                     "The <strong>domain</strong> is the set of values the variables range "
                     "over. It is part of the statement: `∀x (x² ≥ 0)` is true over the "
                     "reals and false over the complex numbers.")),
            ("def", ("Universal quantifier",
                     "`∀x P(x)` (\"for all `x`, `P(x)`\") is true when `P(c)` is true for "
                     "every `c` in the domain, and false as soon as one `c` makes it false.")),
            ("def", ("Existential quantifier",
                     "`∃x P(x)` (\"there exists `x` such that `P(x)`\") is true when "
                     "`P(c)` is true for at least one `c` in the domain.")),
            ("p", "The asymmetry in what it costs to settle these is the heart of the "
                  "lesson. To <strong>prove</strong> `∀x P(x)` over an infinite domain you "
                  "need an argument covering every case; to <strong>refute</strong> it you "
                  "need one counterexample. For `∃x P(x)` it is the reverse: one witness "
                  "proves it, and refuting it takes a general argument."),
            ("math", [
                "                 to PROVE                 to REFUTE",
                "∀x P(x)          argument over all x      one counterexample",
                "∃x P(x)          one witness              argument over all x",
            ]),
            ("p", "Over a finite domain both quantifiers collapse into connectives. With "
                  "domain `{1, 2, 3}`, `∀x P(x)` is `P(1) ∧ P(2) ∧ P(3)` and `∃x P(x)` is "
                  "`P(1) ∨ P(2) ∨ P(3)`. That is exactly why the empty-domain conventions "
                  "come out as they do: an empty conjunction is `T` and an empty "
                  "disjunction is `F`."),
            ("def", ("Bound and free variables",
                     "In `∀x P(x, y)` the variable `x` is <strong>bound</strong> and `y` "
                     "is <strong>free</strong>. A formula with a free variable is still a "
                     "predicate; only when all variables are bound is it a proposition.")),
            ("example", ("Restricting the domain",
                         "\"Every even integer greater than 2 is composite\" is written "
                         "`∀x ((x &gt; 2 ∧ Even(x)) → Composite(x))` &mdash; the "
                         "restriction becomes the hypothesis of a conditional. With `∃` "
                         "the restriction becomes a conjunction instead: `∃x (Even(x) ∧ "
                         "Prime(x))`. Mixing these two patterns up is the standard error.")),
            ("thm", ("Uniqueness",
                     "`∃!x P(x)` means \"there is exactly one `x` with `P(x)`\", and "
                     "abbreviates `∃x (P(x) ∧ ∀y (P(y) → y = x))`. It is two claims: "
                     "something exists, and nothing else does.")),
        ],
        "lab": ("quantifier", {
            "size": 4,
            "preset": "le",
            "panel_title": "A predicate you can edit",
            "panel_intro": "The grid IS the predicate: cell `(x, y)` says whether "
                           "`P(x, y)` holds. Every verdict is recomputed by walking it.",
        }),
        "steps_title": "Translating into quantifiers",
        "steps_intro": "Domain first, predicate second, quantifier last.",
        "steps": [
            ("State the domain explicitly",
             "\"All integers\", \"all real numbers\", \"all students in this class\". "
             "Without it the formula is not a claim."),
            ("Name the predicates",
             "Give each property a symbol with its variables shown: `P(x)` for \"`x` is "
             "prime\", `L(x, y)` for \"`x` likes `y`\"."),
            ("Choose the quantifier",
             "\"Every\", \"all\", \"each\", \"any\" signal `∀`. \"Some\", \"there is\", "
             "\"at least one\" signal `∃`. Beware \"any\", which is `∀` in a positive "
             "sentence and often `∃` under a negation."),
            ("Attach restrictions correctly",
             "With `∀`, a restriction becomes the hypothesis of `→`. With `∃`, it becomes "
             "a conjunct of `∧`. Using `∧` under `∀` claims far too much."),
        ],
        "worked": {
            "title": "Why the restriction pattern differs",
            "intro": ["Domain: all integers. `P(x)` = \"`x` is prime\", `E(x)` = \"`x` is even\"."],
            "lines": [
                "\"Every prime greater than 2 is odd\"",
                "   ∀x ((P(x) ∧ x > 2) → ¬E(x))          correct",
                "   ∀x (P(x) ∧ x > 2 ∧ ¬E(x))            WRONG — claims every integer",
                "                                        is an odd prime > 2",
                "",
                "\"Some prime is even\"",
                "   ∃x (P(x) ∧ E(x))                     correct  (x = 2)",
                "   ∃x (P(x) → E(x))                     WRONG — satisfied by any",
                "                                        non-prime, e.g. x = 9",
            ],
            "after": [
                "The second wrong form is the subtler one. `P(9) → E(9)` is `F → F`, which "
                "is true, so the existential is satisfied by a number that is neither "
                "prime nor even. A conditional under `∃` is almost always a mistake."
            ],
        },
        "quiz_title": "Quantifiers",
        "quiz": [
            {"q": "Domain: the empty set. What is the value of `∀x P(x)`?",
             "a": ["False", "True", "Undefined", "It depends on `P`"],
             "c": 1,
             "why": "Vacuously true: there is no `x` to serve as a counterexample. "
                    "Symmetrically `∃x P(x)` is false over the empty domain."},
            {"q": "How do you refute `∀x P(x)`?",
             "a": ["Show `P(x)` fails for every `x`",
                   "Exhibit one `c` in the domain with `P(c)` false",
                   "Show `∃x ¬P(x)` is false",
                   "Build a truth table"],
             "c": 1,
             "why": "One counterexample is a complete refutation of a universal claim. "
                    "Showing it fails for every `x` proves something stronger than needed."},
            {"q": "\"Some student passed\" is correctly written as:",
             "a": ["`∃x (Student(x) → Passed(x))`",
                   "`∀x (Student(x) → Passed(x))`",
                   "`∃x (Student(x) ∧ Passed(x))`",
                   "`∃x (Student(x) ∨ Passed(x))`"],
             "c": 2,
             "why": "Under `∃` a restriction is a conjunction. The first option is "
                    "satisfied by any non-student, since a false hypothesis makes the "
                    "conditional true."},
        ],
        "mistakes": [
            ("Leaving the domain implicit",
             "`∃x (x² = 2)` is false over `ℚ` and true over `ℝ`. A quantified statement "
             "without a stated domain has no truth value to argue about."),
            ("Using `∧` under `∀` for a restriction",
             "`∀x (P(x) ∧ Q(x))` says every element of the domain has both properties, "
             "which is far stronger than \"every `P` is a `Q`\"."),
            ("Using `→` under `∃`",
             "`∃x (P(x) → Q(x))` is satisfied by any `x` failing `P`, so it is nearly "
             "always vacuously true and almost never what was meant."),
        ],
        "standard": ("Finish when the two restriction patterns are automatic.",
                     "Translate \"every positive even integer greater than 2 is composite\" "
                     "and \"some composite number is odd\" into symbols, and say for each "
                     "why the connective inside had to be what it is."),
        "note": "The lab uses a four-element domain so that both quantifiers can be "
                "checked exhaustively. That is a luxury of finiteness: over `ℕ` no "
                "amount of checking settles a `∀`, which is the whole motivation for "
                "course 3.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "nested-quantifiers",
        "title": "Nested Quantifiers",
        "module": "Predicate logic",
        "one_line": "Why `∀x ∃y` and `∃y ∀x` are different claims.",
        "summary": (
            "When quantifiers stack, order decides meaning. `∀x ∃y` lets `y` depend on "
            "`x`; `∃y ∀x` demands one `y` that works for all of them. One implies the "
            "other, in one direction only."
        ),
        "key": [
            "∀x ∃y P(x, y)     each x gets its own y     (y may depend on x)",
            "∃y ∀x P(x, y)     ONE y works for every x   (strictly stronger)",
            "∃y ∀x P  ⟹  ∀x ∃y P        and NOT conversely",
            "Same-kind quantifiers commute: ∀x∀y ≡ ∀y∀x,  ∃x∃y ≡ ∃y∃x",
        ],
        "key_label": "Order matters, in one direction",
        "concepts_intro": (
            "Nested quantifiers are where careful readers and careless ones separate. The "
            "difference is a single swap and a change of meaning."
        ),
        "concepts": [
            ("Inner variables may depend on outer ones",
             "In `∀x ∃y P(x, y)` the `y` is chosen after `x` is known, so it may be a "
             "different `y` for each `x`. That dependence is the whole content."),
            ("`∃∀` is strictly stronger than `∀∃`",
             "One `y` serving every `x` implies each `x` has some `y`. The converse fails "
             "&mdash; and the lab lets you build the case where it fails."),
            ("Like quantifiers commute; unlike ones do not",
             "`∀x ∀y` may be swapped freely, and so may `∃x ∃y`. Swapping `∀` past `∃` "
             "changes the claim."),
        ],
        "read_title": "Stacked quantifiers",
        "read_intro": "The four two-variable forms, and the implication that holds between two of them.",
        "body": [
            ("p", "With one two-place predicate and two quantifiers there are four "
                  "statements. Written out over a domain, they say quite different things."),
            ("math", [
                "∀x ∀y P(x, y)     P holds for every pair",
                "∀x ∃y P(x, y)     for each x there is SOME y (which may depend on x)",
                "∃x ∀y P(x, y)     there is ONE x that works with every y",
                "∃x ∃y P(x, y)     some pair works",
            ]),
            ("thm", ("The one implication",
                     "`∃y ∀x P(x, y) ⟹ ∀x ∃y P(x, y)`, and the converse does not hold in "
                     "general.")),
            ("proof", [
                "Suppose `∃y ∀x P(x, y)`, and let `b` be such a `y`. Then `P(x, b)` holds "
                "for every `x`. So given any `x`, the value `b` witnesses `∃y P(x, y)`. "
                "Hence `∀x ∃y P(x, y)`.",
                "For the converse, take the domain `ℤ` and `P(x, y)` = \"`y` is greater "
                "than `x`\". Every integer has something larger, so `∀x ∃y P(x, y)` holds. "
                "But no single integer is larger than every integer, so `∃y ∀x P(x, y)` is "
                "false.",
            ]),
            ("p", "The English versions are worth having by heart. `∀x ∃y` is "
                  "\"everybody has somebody\"; `∃y ∀x` is \"somebody is everybody's\". "
                  "The first is a mild claim; the second is a strong one."),
            ("example", ("The same swap, in analysis",
                         "Continuity of `f` at every point is `∀ε ∀x ∃δ`, where `δ` may "
                         "depend on both `ε` and `x`. Uniform continuity is `∀ε ∃δ ∀x`: "
                         "one `δ` that works at every point. The entire difference between "
                         "the two definitions is where the `∃δ` sits.")),
            ("p", "Three or more quantifiers behave the same way. `∀x ∃y ∀z` is read left "
                  "to right, and each variable may depend on those bound to its left and "
                  "on no others. Reading the string in the order written is the whole "
                  "technique."),
            ("def", ("Order of evaluation",
                     "A nested quantified statement is evaluated outside in. To decide "
                     "`∀x ∃y P(x, y)`, take each `x` in turn and ask whether some `y` "
                     "works for that particular `x`.")),
        ],
        "lab": ("quantifier", {
            "size": 4,
            "preset": "succ",
            "panel_title": "Separate the two orders",
            "panel_intro": "The successor preset is the classic separator: every `x` has "
                           "a `y` with `y = x + 1`, but no single `y` is the successor of "
                           "everything. Watch the two middle rows disagree.",
        }),
        "steps_title": "Reading a nested statement",
        "steps_intro": "Left to right, and never rearrange.",
        "steps": [
            ("Read the quantifiers in written order",
             "`∀x ∃y` is \"for each `x`… there is a `y`\". Reading it as \"there is a `y` "
             "for each `x`\" in the sense of one shared `y` is the error itself."),
            ("Ask what each variable may depend on",
             "A variable may depend on everything bound to its left. If your witness for "
             "`y` mentions `x`, you are proving `∀x ∃y`, not `∃y ∀x`."),
            ("To prove `∃∀`, produce the single witness",
             "Name one value and show it works for every `x`. If you cannot name it "
             "without knowing `x`, the statement is probably false."),
            ("To refute `∃∀`, argue against every candidate",
             "For each candidate `y`, exhibit an `x` that defeats it. The `x` may depend "
             "on `y`, which is exactly what the negation permits."),
        ],
        "worked": {
            "title": "Two statements over the integers",
            "intro": ["Domain `ℤ`, `P(x, y)` = \"`x + y = 0`\"."],
            "lines": [
                "∀x ∃y (x + y = 0)      TRUE",
                "   given x, take y = −x.  The witness DEPENDS on x, which is allowed.",
                "",
                "∃y ∀x (x + y = 0)      FALSE",
                "   a single y would need x + y = 0 for every x at once;",
                "   x = 0 forces y = 0, and then x = 1 gives 1 + 0 = 1 ≠ 0.",
                "",
                "∀x ∀y (x + y = y + x)  TRUE   — order of two ∀ is irrelevant",
                "∃x ∃y (x + y = 5)      TRUE   — x = 2, y = 3",
            ],
            "after": [
                "In the first, the witness `y = −x` mentions `x`, which is the signature "
                "of a `∀∃` proof. If a proof of an `∃∀` statement produces a witness "
                "mentioning the universally quantified variable, the proof is wrong."
            ],
        },
        "quiz_title": "Order of quantifiers",
        "quiz": [
            {"q": "Domain `ℤ`, `P(x, y)` = \"`y` is greater than `x`\". Which is true?",
             "a": ["Both `∀x ∃y P` and `∃y ∀x P`",
                   "`∀x ∃y P` only",
                   "`∃y ∀x P` only",
                   "Neither"],
             "c": 1,
             "why": "Every integer has something bigger, so `∀x ∃y` holds. No integer "
                    "exceeds all integers, so `∃y ∀x` fails."},
            {"q": "Which implication is valid in general?",
             "a": ["`∀x ∃y P(x,y) ⟹ ∃y ∀x P(x,y)`",
                   "`∃y ∀x P(x,y) ⟹ ∀x ∃y P(x,y)`",
                   "Both", "Neither"],
             "c": 1,
             "why": "A single `y` that works for every `x` certainly gives each `x` some "
                    "`y`. The other direction fails whenever the witness must depend on `x`."},
            {"q": "In `∀x ∃y ∀z Q(x, y, z)`, the choice of `y` may depend on:",
             "a": ["nothing", "`x` only", "`z` only", "both `x` and `z`"],
             "c": 1,
             "why": "A variable may depend on the variables bound to its LEFT. `x` is to "
                    "the left of `y`; `z` is to its right and is chosen afterwards."},
        ],
        "mistakes": [
            ("Swapping `∀` and `∃` while \"simplifying\"",
             "This changes the statement into a strictly stronger or weaker one. It is "
             "not a simplification and it is not valid."),
            ("Producing an `x`-dependent witness for an `∃∀` claim",
             "If the witness mentions the universally quantified variable, you have "
             "proved the `∀∃` version instead. This is the most common invalid proof in "
             "the whole course."),
            ("Assuming English word order settles it",
             "\"There is a key for every door\" is genuinely ambiguous in English. The "
             "symbols are not, which is why the translation must be done deliberately."),
        ],
        "standard": ("Finish when you can build a predicate separating `∀∃` from `∃∀`.",
                     "Using the lab's grid, construct a relation where `∀x ∃y` holds and "
                     "`∃x ∀y` fails, and one where both hold. Being able to build the "
                     "separating case is stronger evidence of understanding than "
                     "recognising it."),
        "note": "The `∀ε ∃δ` versus `∃δ ∀ε` distinction is the single place this lesson "
                "pays off outside discrete mathematics: pointwise and uniform continuity "
                "differ by precisely this swap, and so do pointwise and uniform convergence.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "negating-quantified-statements",
        "title": "Negating Quantified Statements",
        "module": "Predicate logic",
        "one_line": "Push the negation inward; every quantifier flips.",
        "summary": (
            "`¬∀x P(x) ≡ ∃x ¬P(x)` and `¬∃x P(x) ≡ ∀x ¬P(x)`. Applied repeatedly, this "
            "converts any negated statement into one with the negation on the predicate "
            "&mdash; which is how you find out what a counterexample must look like."
        ),
        "key": [
            "¬∀x P(x)   ≡   ∃x ¬P(x)         \"not all\" = \"some fails\"",
            "¬∃x P(x)   ≡   ∀x ¬P(x)         \"none\"    = \"all fail\"",
            "¬∀x ∃y P   ≡   ∃x ∀y ¬P         flip every quantifier in turn",
            "¬(P → Q)   ≡   P ∧ ¬Q           inside the predicate",
        ],
        "key_label": "Generalised De Morgan",
        "concepts_intro": (
            "Negation is mechanical here, and the mechanism is worth trusting: it tells "
            "you exactly what would have to be shown to refute a claim."
        ),
        "concepts": [
            ("Each quantifier flips as the negation passes",
             "`∀` becomes `∃` and `∃` becomes `∀`, in order, until the negation reaches "
             "the predicate. This is De Morgan generalised to arbitrary domains."),
            ("The result tells you what to look for",
             "Negating a theorem statement produces the exact shape of a counterexample. "
             "That is the practical payoff of doing it mechanically."),
            ("Restrictions survive the flip",
             "`¬∀x (P(x) → Q(x)) ≡ ∃x (P(x) ∧ ¬Q(x))`: the conditional becomes a "
             "conjunction, which is why restricted universals negate into restricted "
             "existentials."),
        ],
        "read_title": "Pushing negation through quantifiers",
        "read_intro": "The two rules, why they generalise De Morgan, and how to apply them in sequence.",
        "body": [
            ("thm", ("Quantifier negation",
                     "`¬∀x P(x) ≡ ∃x ¬P(x)` and `¬∃x P(x) ≡ ∀x ¬P(x)`, over any domain.")),
            ("proof", [
                "`¬∀x P(x)` says it is not the case that `P` holds throughout the domain "
                "&mdash; so some element fails it, which is `∃x ¬P(x)`. Conversely, if "
                "some `c` has `¬P(c)` then `∀x P(x)` cannot hold.",
                "For a finite domain `{a₁, …, aₙ}` this is literally De Morgan: "
                "`¬(P(a₁) ∧ … ∧ P(aₙ)) ≡ ¬P(a₁) ∨ … ∨ ¬P(aₙ)`. The quantifier rules are "
                "the same statement freed from finiteness.",
            ]),
            ("p", "Applied to a nested statement, the rules are used one at a time from "
                  "the outside in. Each application moves the negation one quantifier "
                  "further right and flips that quantifier."),
            ("math", [
                "¬ ∀x ∃y ∀z  P(x, y, z)",
                "  ≡ ∃x ¬ ∃y ∀z  P(x, y, z)",
                "  ≡ ∃x ∀y ¬ ∀z  P(x, y, z)",
                "  ≡ ∃x ∀y ∃z ¬P(x, y, z)",
            ]),
            ("p", "Every quantifier has flipped and the negation now sits on the "
                  "predicate, where the propositional rules of lesson 5 take over. If "
                  "`P` is a conditional, `¬(A → B) ≡ A ∧ ¬B` finishes the job."),
            ("example", ("Negating a restricted universal",
                         "\"Every prime greater than 2 is odd\" is "
                         "`∀x ((P(x) ∧ x &gt; 2) → Odd(x))`. Its negation is "
                         "`∃x (P(x) ∧ x &gt; 2 ∧ ¬Odd(x))` &mdash; \"there is an even "
                         "prime greater than 2\". That is exactly the counterexample you "
                         "would have to produce, and its shape came out of the mechanism "
                         "rather than out of thinking about primes.")),
            ("p", "This is the lesson's real use. Faced with a claim you suspect is false, "
                  "negate it mechanically and read what the negation demands. Very often "
                  "the negation is easy to satisfy and the counterexample writes itself."),
            ("thm", ("Negating uniqueness",
                     "`¬∃!x P(x)` says either nothing satisfies `P` or at least two "
                     "things do. Unfolding `∃!` and negating gives exactly that "
                     "disjunction &mdash; a good check on whether the mechanism has been "
                     "applied correctly.")),
        ],
        "lab": ("quantifier", {
            "size": 4,
            "preset": "diag",
            "panel_title": "Negation as a flip",
            "panel_intro": "Use the complement button: it replaces `P` by `¬P` everywhere. "
                           "Watch `∀x ∀y` and `∃x ∃y` swap verdicts, and the two mixed "
                           "rows swap with each other.",
        }),
        "steps_title": "Negating a statement",
        "steps_intro": "One quantifier at a time, outside in. Never guess the result.",
        "steps": [
            ("Write the statement fully symbolically",
             "Including the domain restriction as a conditional or conjunction. "
             "Negating English directly is where errors enter."),
            ("Flip the outermost quantifier",
             "`∀` to `∃` or `∃` to `∀`, moving the negation inside it."),
            ("Repeat until the negation reaches the predicate",
             "Each step flips exactly one quantifier. Do not skip ahead."),
            ("Simplify the predicate propositionally",
             "`¬(A → B) ≡ A ∧ ¬B`, De Morgan for `∧`/`∨`, double negation. Then read the "
             "result back into English as the description of a counterexample."),
        ],
        "worked": {
            "title": "Negating the definition of continuity",
            "intro": ["`f` is continuous at `a` when "
                      "`∀ε &gt; 0 ∃δ &gt; 0 ∀x (|x − a| &lt; δ → |f(x) − f(a)| &lt; ε)`."],
            "lines": [
                "¬ ∀ε ∃δ ∀x ( |x−a| < δ  →  |f(x)−f(a)| < ε )",
                "  ≡ ∃ε ¬ ∃δ ∀x ( … )",
                "  ≡ ∃ε ∀δ ¬ ∀x ( … )",
                "  ≡ ∃ε ∀δ ∃x ¬( |x−a| < δ  →  |f(x)−f(a)| < ε )",
                "  ≡ ∃ε ∀δ ∃x ( |x−a| < δ  ∧  |f(x)−f(a)| ≥ ε )",
            ],
            "after": [
                "Read it: there is a tolerance `ε` such that no matter how small `δ` is "
                "made, some point within `δ` of `a` is thrown further than `ε` away. That "
                "is precisely what discontinuity looks like, and the mechanism produced it "
                "without any geometric intuition being consulted."
            ],
        },
        "quiz_title": "Negation",
        "quiz": [
            {"q": "The negation of \"all swans are white\" is:",
             "a": ["No swan is white", "All swans are non-white",
                   "Some swan is not white", "Some swan is white"],
             "c": 2,
             "why": "`¬∀x (S(x) → W(x)) ≡ ∃x (S(x) ∧ ¬W(x))`. \"No swan is white\" is the "
                    "much stronger `∀x (S(x) → ¬W(x))`."},
            {"q": "`¬∃x ∀y P(x, y)` is equivalent to:",
             "a": ["`∀x ∃y ¬P(x, y)`", "`∃x ∀y ¬P(x, y)`",
                   "`∀x ∀y ¬P(x, y)`", "`∃y ∀x ¬P(x, y)`"],
             "c": 0,
             "why": "Each quantifier flips in order as the negation moves right: `∃` "
                    "becomes `∀`, then `∀` becomes `∃`, and the negation lands on `P`."},
            {"q": "To refute \"every continuous function is differentiable\", you must exhibit:",
             "a": ["a differentiable function that is not continuous",
                   "a continuous function that is not differentiable",
                   "a function that is neither",
                   "all functions that are continuous"],
             "c": 1,
             "why": "`¬∀x (C(x) → D(x)) ≡ ∃x (C(x) ∧ ¬D(x))`. The negation names its own "
                    "counterexample &mdash; here, `|x|` at 0."},
        ],
        "mistakes": [
            ("Negating \"all are\" as \"none are\"",
             "\"Not all\" is `∃x ¬P(x)`; \"none\" is `∀x ¬P(x)`. The second is far "
             "stronger and is a different claim entirely."),
            ("Forgetting the conditional turns into a conjunction",
             "`¬(P(x) → Q(x))` is `P(x) ∧ ¬Q(x)`, not `P(x) → ¬Q(x)`. Getting this wrong "
             "produces a negation that is satisfied by irrelevant elements."),
            ("Flipping only the outermost quantifier",
             "Every quantifier the negation passes must flip. Stopping after the first "
             "leaves a statement that is neither the original nor its negation."),
        ],
        "standard": ("Finish when you can negate a three-quantifier definition without "
                     "thinking about its meaning.",
                     "Negate `∀ε ∃N ∀n (n ≥ N → |aₙ − L| &lt; ε)`, the definition of a "
                     "convergent sequence, and read the answer back into English. If the "
                     "mechanism carried you through, it will carry you through any "
                     "definition you meet later."),
        "note": "Doing this mechanically is a genuine technique, not a crutch. "
                "Mathematicians negate definitions symbolically precisely because "
                "intuition about what \"not continuous\" means is unreliable and the "
                "rules are not.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "rules-of-inference",
        "title": "Rules of Inference",
        "module": "Proof",
        "one_line": "Valid argument forms, and the two fallacies that mimic them.",
        "summary": (
            "An argument is valid when its premises cannot all be true with its "
            "conclusion false. Modus ponens, modus tollens, syllogism, resolution "
            "&mdash; and the two invalid forms that look identical until you check."
        ),
        "key": [
            "modus ponens      p → q,  p        ⊢ q        VALID",
            "modus tollens     p → q, ¬q        ⊢ ¬p       VALID",
            "affirming the consequent  p → q, q  ⊢ p       INVALID",
            "denying the antecedent    p → q, ¬p ⊢ ¬q      INVALID",
        ],
        "key_label": "Two valid, two not",
        "concepts_intro": (
            "Validity is about form, not content. An argument can have false premises and "
            "still be valid, and true premises with a true conclusion and still be invalid."
        ),
        "concepts": [
            ("Validity is a property of form",
             "The argument is valid when `(premises) → conclusion` is a tautology. What "
             "the propositions mean never enters."),
            ("Sound is valid plus true premises",
             "A valid argument from false premises proves nothing about the world; it "
             "guarantees only that the conclusion follows."),
            ("The two fallacies are conditional confusions",
             "Affirming the consequent uses the converse; denying the antecedent uses the "
             "inverse. Lesson 4 already showed neither is equivalent to the original."),
        ],
        "read_title": "Valid inference",
        "read_intro": "The definition, the standard rules, and how to check any candidate rule yourself.",
        "body": [
            ("def", ("Valid argument",
                     "An argument with premises `P₁, …, Pₙ` and conclusion `C` is "
                     "<strong>valid</strong> when `(P₁ ∧ … ∧ Pₙ) → C` is a tautology "
                     "&mdash; equivalently, when no assignment makes every premise true "
                     "and the conclusion false.")),
            ("def", ("Sound argument",
                     "An argument is <strong>sound</strong> when it is valid and its "
                     "premises are actually true. Validity is a matter of logic; soundness "
                     "adds a claim about the world.")),
            ("h3", "The standard rules"),
            ("math", [
                "modus ponens           p → q,  p          ⊢  q",
                "modus tollens          p → q,  ¬q         ⊢  ¬p",
                "hypothetical syllogism p → q,  q → r      ⊢  p → r",
                "disjunctive syllogism  p ∨ q,  ¬p         ⊢  q",
                "addition               p                  ⊢  p ∨ q",
                "simplification         p ∧ q              ⊢  p",
                "conjunction            p,  q              ⊢  p ∧ q",
                "resolution             p ∨ q,  ¬p ∨ r     ⊢  q ∨ r",
            ]),
            ("p", "Each of these is a tautology when written as a conditional, and each "
                  "can be checked with a truth table in under a minute. They are worth "
                  "knowing by name because a proof that cites them is a proof someone "
                  "else can follow."),
            ("p", "<strong>Resolution</strong> deserves a note: it is the single rule "
                  "automated theorem provers and SAT solvers are built on. Given a formula "
                  "in CNF, repeatedly resolving clauses either derives the empty clause "
                  "&mdash; proving unsatisfiability &mdash; or exhausts the possibilities."),
            ("h3", "The two fallacies"),
            ("thm", ("Affirming the consequent is invalid",
                     "From `p → q` and `q`, nothing follows about `p`. Take `p = F`, "
                     "`q = T`: both premises hold and the conclusion `p` is false.")),
            ("thm", ("Denying the antecedent is invalid",
                     "From `p → q` and `¬p`, nothing follows about `q`. Take `p = F`, "
                     "`q = T`: both premises hold and the conclusion `¬q` is false.")),
            ("example", ("Both fallacies in one sentence",
                         "\"If it rains, the ground is wet.\" The ground is wet &mdash; "
                         "so it rained? No: a sprinkler wets the ground. It did not rain "
                         "&mdash; so the ground is dry? No: same sprinkler. Both errors "
                         "come from treating the conditional as a biconditional.")),
            ("h3", "Rules for quantifiers"),
            ("math", [
                "universal instantiation    ∀x P(x)  ⊢  P(c)      any c in the domain",
                "existential instantiation  ∃x P(x)  ⊢  P(c)      for a NEW name c",
                "universal generalisation   P(c) for arbitrary c  ⊢  ∀x P(x)",
                "existential generalisation P(c)     ⊢  ∃x P(x)",
            ]),
            ("p", "The two with conditions attached are where care is needed. Existential "
                  "instantiation may only introduce a <em>fresh</em> name &mdash; you know "
                  "something exists, not which thing it is, so it must not be confused "
                  "with anything already named. Universal generalisation requires that `c` "
                  "was genuinely arbitrary: nothing was assumed about it."),
        ],
        "lab": ("truth_table", {
            "formulas": ["((p -> q) & p) -> q", "((p -> q) & ~q) -> ~p",
                         "((p -> q) & q) -> p", "((p -> q) & ~p) -> ~q",
                         "((p -> q) & (q -> r)) -> (p -> r)",
                         "((p | q) & ~p) -> q", "(p & q) -> p", "p -> (p | q)"],
            "panel_title": "Check a rule yourself",
            "panel_intro": "Each formula is one argument form written as a conditional. A "
                           "tautology means the rule is valid; a false row is a "
                           "counterexample with the premises true and the conclusion false.",
        }),
        "steps_title": "Checking an argument",
        "steps_intro": "Form first. The content is a distraction until the form is settled.",
        "steps": [
            ("Strip it to symbols",
             "Assign letters to the atomic propositions and write the premises and "
             "conclusion. Content that feels persuasive is the enemy here."),
            ("Try to make premises true and conclusion false",
             "That single assignment, if it exists, proves invalidity. If it cannot exist, "
             "the argument is valid."),
            ("Name the rule, or the fallacy",
             "If it matches a standard form, say which. If it matches a fallacy, say "
             "which &mdash; and produce the counterexample assignment."),
            ("Separate validity from truth",
             "A valid argument with a false premise establishes nothing. Say which of the "
             "two you are claiming."),
        ],
        "worked": {
            "title": "Is this argument valid?",
            "intro": ["\"If the program has a bug, the test fails. The test failed. "
                      "Therefore the program has a bug.\""],
            "lines": [
                "p = the program has a bug      q = the test fails",
                "premises:   p → q,   q",
                "conclusion: p",
                "",
                "Try p = F, q = T:",
                "   p → q  =  F → T  =  T      premise 1 holds",
                "   q      =  T                premise 2 holds",
                "   p      =  F                conclusion FAILS",
                "",
                "INVALID — affirming the consequent.",
            ],
            "after": [
                "The counterexample is not artificial: a test can fail because the test "
                "itself is wrong. The valid inference available here is modus tollens "
                "&mdash; the test passed, therefore no bug of the kind that test detects."
            ],
        },
        "quiz_title": "Valid or fallacious",
        "quiz": [
            {"q": "From `p → q` and `¬q`, what validly follows?",
             "a": ["`q`", "`p`", "`¬p`", "Nothing"],
             "c": 2,
             "why": "Modus tollens. If `p` held then `q` would hold; `q` does not, so `p` "
                    "does not. This is contraposition used as an inference."},
            {"q": "An argument is valid but has a false premise. What can you conclude about the conclusion?",
             "a": ["It is false", "It is true", "Nothing", "It is a tautology"],
             "c": 2,
             "why": "Validity guarantees only that true premises would force a true "
                    "conclusion. With a false premise the conclusion may be either &mdash; "
                    "the argument is valid but not sound."},
            {"q": "\"If she studied, she passed. She did not study. Therefore she did not pass.\" This is:",
             "a": ["Modus tollens", "Valid by hypothetical syllogism",
                   "Denying the antecedent, invalid", "Affirming the consequent, invalid"],
             "c": 2,
             "why": "It uses the INVERSE, `¬p → ¬q`, which is not equivalent to `p → q`. "
                    "She might have passed without studying."},
        ],
        "mistakes": [
            ("Confusing validity with truth",
             "\"That conclusion is false, so the argument is invalid\" does not follow. "
             "A valid argument can carry a false premise to a false conclusion."),
            ("Reusing a name in existential instantiation",
             "From `∃x P(x)` and `∃x Q(x)` you may not conclude `∃x (P(x) ∧ Q(x))`. The "
             "two witnesses need not be the same object, so each needs a fresh name."),
            ("Generalising from a non-arbitrary element",
             "Universal generalisation needs `c` about which nothing was assumed. If the "
             "argument used a property of `c`, the conclusion does not extend to all `x`."),
        ],
        "standard": ("Finish when you can name the fallacy AND produce its counterexample "
                     "assignment.",
                     "Given any two-premise argument about a conditional, you should be "
                     "able to say in one line whether it is modus ponens, modus tollens, "
                     "or one of the two fallacies &mdash; and for the fallacies, state the "
                     "row that breaks it."),
        "note": "The four quantifier rules are stated here without full justification "
                "because the conditions on them (fresh names, arbitrary elements) are "
                "what a proof must respect. Lessons 12 to 14 use them in prose, which is "
                "how they appear in practice.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "direct-proof",
        "title": "Direct Proof",
        "module": "Proof",
        "one_line": "Assume the hypothesis, derive the conclusion, write it for a reader.",
        "summary": (
            "The default technique: to prove `p → q`, assume `p` and reason forward to "
            "`q`. Most of the difficulty is not logical but expository &mdash; a proof is "
            "a piece of writing whose job is to convince a careful reader."
        ),
        "key": [
            "To prove  ∀x (P(x) → Q(x)):",
            "  1. Let x be arbitrary with P(x).",
            "  2. ... reasoning, each step justified ...",
            "  3. Therefore Q(x).  Since x was arbitrary, the claim holds for all x.",
        ],
        "key_label": "The shape of a direct proof",
        "concepts_intro": (
            "Three things make a direct proof work: the right starting assumption, "
            "justified steps, and a reader who can follow them."
        ),
        "concepts": [
            ("Start by assuming the hypothesis",
             "You are not proving `q`. You are proving that `q` follows from `p`, so `p` "
             "is yours to use from the first line."),
            ("Unfold the definitions",
             "\"`n` is even\" is not a fact to be contemplated but a statement to be "
             "replaced: `n = 2k` for some integer `k`. Most direct proofs are definition "
             "unfolding plus algebra."),
            ("Arbitrary means arbitrary",
             "\"Let `n` be an even integer\" licenses a conclusion about every even "
             "integer. \"Let `n = 4`\" does not."),
        ],
        "read_title": "How a direct proof is built and written",
        "read_intro": "The method, then the standards a written proof is held to.",
        "body": [
            ("p", "Almost every theorem is a universally quantified conditional: "
                  "`∀x (P(x) → Q(x))`. A direct proof takes an arbitrary `x` satisfying "
                  "`P`, and derives `Q(x)` by a chain of justified steps."),
            ("def", ("Direct proof",
                     "To prove `p → q`, assume `p` and derive `q` through a sequence of "
                     "steps, each justified by a definition, a previously proved result, "
                     "or a rule of inference.")),
            ("thm", ("The sum of two odd integers is even",
                     "For all integers `m` and `n`, if `m` and `n` are odd then `m + n` is "
                     "even.")),
            ("proof", [
                "Let `m` and `n` be arbitrary odd integers. By definition of odd, there "
                "are integers `j` and `k` with `m = 2j + 1` and `n = 2k + 1`.",
                "Then `m + n = (2j + 1) + (2k + 1) = 2j + 2k + 2 = 2(j + k + 1)`.",
                "Since `j + k + 1` is an integer, `m + n` is twice an integer, which is "
                "the definition of even. As `m` and `n` were arbitrary odd integers, the "
                "claim holds for all of them.",
            ]),
            ("p", "Notice how much of that is definition management. \"Odd\" was replaced "
                  "by `2j + 1` immediately, the algebra was routine, and the final step "
                  "recognised `2(j + k + 1)` as matching the definition of even. Two "
                  "different letters `j` and `k` were used because `m` and `n` are "
                  "different numbers &mdash; reusing one letter for both would have proved "
                  "only the case `m = n`."),
            ("h3", "What a written proof owes the reader"),
            ("ul", [
                "<strong>State what is being proved</strong>, in full, before starting.",
                "<strong>Introduce every variable</strong> as it appears: \"let `n` be an "
                "arbitrary integer\", \"there exists `k` such that\".",
                "<strong>Justify each step</strong> by name: by definition, by hypothesis, "
                "by the theorem just proved. A step whose justification you cannot state "
                "is a step you have not made.",
                "<strong>Say when you are done</strong> and what has been established. "
                "The reader should never have to guess whether the argument has finished.",
            ]),
            ("p", "Two conventions worth adopting. Write in complete sentences &mdash; a "
                  "proof is prose containing symbols, not a column of formulas. And "
                  "distinguish the assumption you made from the conclusion you reached; "
                  "confusing the two is how a proof silently becomes circular."),
            ("example", ("A proof that assumes what it proves",
                         "\"Claim: if `n²` is even then `n` is even. Proof: `n` is even, "
                         "so `n = 2k`, so `n² = 4k²` is even.\" This proves the converse, "
                         "having assumed the conclusion. It is the most common flawed "
                         "proof in this course, and lesson 13 gives the technique that "
                         "handles the real claim.")),
            ("p", "When a direct proof stalls, that is information. Being unable to get "
                  "from `p` to `q` forwards often means the natural route is backwards "
                  "&mdash; through the contrapositive &mdash; which is the next lesson."),
        ],
        "lab": ("induction", {
            "statement": "div6",
            "panel_title": "Check the claim you are about to prove",
            "panel_intro": "Before proving `n³ − n` is divisible by 6, look at it. The lab "
                           "confirms it for the `n` you can see; the proof is what covers "
                           "the rest, and this lesson is about writing that proof.",
        }),
        "steps_title": "Writing a direct proof",
        "steps_intro": "The first two steps are where proofs are won or lost.",
        "steps": [
            ("Write the statement in full",
             "Including quantifiers and domain. If you cannot state it precisely you "
             "cannot prove it, and half of all failed attempts end here."),
            ("Assume the hypothesis and unfold every definition",
             "Replace \"even\", \"divides\", \"rational\" by what they mean. Symbols can "
             "be manipulated; adjectives cannot."),
            ("Work forward to the conclusion",
             "Keep the target in view. If a step is not moving toward it, it is probably "
             "not the step to take."),
            ("Recognise the conclusion in the form you need it",
             "The last line must match the definition of the conclusion. `2(j + k + 1)` "
             "is even because it is twice an integer &mdash; say so."),
        ],
        "worked": {
            "title": "If `a | b` and `b | c` then `a | c`",
            "intro": ["`a | b` means \"`a` divides `b`\": there is an integer `k` with `b = ak`."],
            "lines": [
                "Let a, b, c be integers with a | b and b | c.",
                "",
                "By definition of divisibility:",
                "   a | b  ⟹  b = a·j   for some integer j",
                "   b | c  ⟹  c = b·k   for some integer k",
                "",
                "Substituting the first into the second:",
                "   c = b·k = (a·j)·k = a·(j·k)",
                "",
                "j·k is an integer, so c = a·(integer), i.e. a | c.        ∎",
            ],
            "after": [
                "Two separate letters `j` and `k` are essential: the two factors have no "
                "reason to be equal. Using `k` twice would prove only the special case "
                "`b = aj` and `c = bj`, which is a different and much weaker theorem."
            ],
        },
        "quiz_title": "Direct proof",
        "quiz": [
            {"q": "To prove `∀x (P(x) → Q(x))` directly, you begin by:",
             "a": ["assuming `Q(x)` for an arbitrary `x`",
                   "assuming `P(x)` for an arbitrary `x`",
                   "assuming `¬Q(x)`",
                   "checking `x = 1, 2, 3`"],
             "c": 1,
             "why": "The hypothesis is given to you; the conclusion is what must be "
                    "derived. Assuming `Q(x)` would be assuming what is to be proved."},
            {"q": "A proof writes `m = 2k + 1` and `n = 2k + 1` for two arbitrary odd integers. What is wrong?",
             "a": ["Nothing", "Odd numbers are not of that form",
                   "It forces `m = n`, so only a special case is proved",
                   "`k` should be even"],
             "c": 2,
             "why": "Reusing one letter asserts the two numbers have the same `k` and so "
                    "are equal. Distinct arbitrary objects need distinct witnesses."},
            {"q": "\"Let `n = 6`. Then `n³ − n = 210 = 6 · 35`. Therefore `n³ − n` is divisible by 6 for all `n`.\" This is:",
             "a": ["A valid direct proof", "Valid only for even `n`",
                   "Not a proof: one case establishes nothing about all `n`",
                   "A proof by cases"],
             "c": 2,
             "why": "A direct proof of a universal statement must take an ARBITRARY "
                    "element. Verifying `n = 6` establishes the claim for `n = 6` and "
                    "nothing more."},
        ],
        "mistakes": [
            ("Assuming the conclusion",
             "Starting from `q` and deriving something true proves nothing: true "
             "statements follow from false ones. Start from `p`."),
            ("Proving one case and claiming all",
             "\"Let `n = 4`\" proves a fact about 4. The word that makes a proof general "
             "is \"arbitrary\", and it has to be earned."),
            ("Leaving a step unjustified because it is obvious",
             "If it is obvious, the justification is one clause long. If you cannot write "
             "that clause, it was not obvious &mdash; it was unexamined."),
        ],
        "standard": ("Finish when you can write a proof another person could check "
                     "line by line.",
                     "Prove: if `n` is an odd integer then `n²` is odd. Then hand it to "
                     "someone and watch for the place they hesitate. That place is where "
                     "a justification is missing, whether or not the mathematics is right."),
        "note": "Every proof in this course is written in prose, because that is how "
                "mathematics is actually communicated. A formal derivation is a different "
                "object with a different purpose, and neither replaces the other.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "contraposition-and-contradiction",
        "title": "Contraposition and Contradiction",
        "module": "Proof",
        "one_line": "Two indirect techniques, and when each is the right one.",
        "summary": (
            "To prove `p → q` by contraposition, prove `¬q → ¬p` instead &mdash; a "
            "different theorem with the same meaning. To prove `s` by contradiction, "
            "assume `¬s` and derive an impossibility. They are not the same technique."
        ),
        "key": [
            "contraposition   prove ¬q → ¬p          an EQUIVALENT statement",
            "contradiction    assume ¬s, derive F     any absurdity will do",
            "Use contraposition when ¬q is easier to work with than p.",
            "Use contradiction when ¬s gives you something concrete to hold.",
        ],
        "key_label": "Two indirect routes",
        "concepts_intro": (
            "Both techniques replace a hard target with an easier one. They differ in "
            "what they assume and what they must produce."
        ),
        "concepts": [
            ("Contraposition proves an equivalent statement",
             "`p → q ≡ ¬q → ¬p` (lesson 4), so proving one proves the other. Nothing is "
             "assumed beyond the new hypothesis `¬q`."),
            ("Contradiction assumes the negation of the goal",
             "You assume `¬s` and derive something false. The falsehood may be anything: "
             "`0 = 1`, a number both even and odd, a contradiction of a hypothesis."),
            ("They are often confused, and the difference matters",
             "A \"proof by contradiction\" that assumes `p ∧ ¬q` and derives `¬p` is "
             "really contraposition with extra steps. Naming it correctly makes it shorter."),
        ],
        "read_title": "Indirect proof",
        "read_intro": "Each technique, a worked instance, and the rule for choosing between them.",
        "body": [
            ("h3", "Proof by contraposition"),
            ("def", ("Proof by contraposition",
                     "To prove `p → q`, prove `¬q → ¬p`. Since the two are logically "
                     "equivalent, a proof of either is a proof of both.")),
            ("thm", ("If `n²` is even then `n` is even",
                     "For every integer `n`, if `n²` is even then `n` is even.")),
            ("proof", [
                "We prove the contrapositive: if `n` is odd then `n²` is odd.",
                "Let `n` be an odd integer, so `n = 2k + 1` for some integer `k`. Then "
                "`n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1`, which is odd since `2k² + 2k` is "
                "an integer.",
                "The contrapositive holds, so the original statement holds.",
            ]),
            ("p", "Compare with the direct attempt. Assuming `n²` is even gives "
                  "`n² = 2m`, and there is nowhere useful to go: extracting information "
                  "about `n` from a statement about `n²` requires the unique "
                  "factorisation of course 6. The contrapositive hands you `n` itself, "
                  "in a form you can compute with. That asymmetry is the whole reason to "
                  "choose it."),
            ("h3", "Proof by contradiction"),
            ("def", ("Proof by contradiction",
                     "To prove `s`, assume `¬s` and derive a statement known to be false. "
                     "Since a false conclusion cannot follow from a true assumption, `¬s` "
                     "must be false, so `s` holds.")),
            ("thm", ("√2 is irrational",
                     "There is no rational number whose square is 2.")),
            ("proof", [
                "Suppose, for contradiction, that `√2` is rational. Then `√2 = a/b` for "
                "integers `a, b` with `b ≠ 0`, and we may take the fraction in lowest "
                "terms, so `a` and `b` share no common factor greater than 1.",
                "Squaring: `2 = a²/b²`, hence `a² = 2b²`. So `a²` is even, and by the "
                "theorem above `a` is even. Write `a = 2c`.",
                "Substituting: `4c² = 2b²`, so `b² = 2c²`. Then `b²` is even, so `b` is "
                "even. But then `a` and `b` are both divisible by 2, contradicting that "
                "the fraction was in lowest terms.",
                "The assumption is therefore false, and `√2` is irrational.",
            ]),
            ("p", "That proof is worth studying for its structure as much as its result. "
                  "The contradiction is not with a law of arithmetic but with a condition "
                  "we imposed ourselves &mdash; lowest terms &mdash; and imposing it was "
                  "the move that made the proof possible."),
            ("h3", "Choosing between them"),
            ("ul", [
                "The statement is a conditional and `¬q` is concrete: use "
                "<strong>contraposition</strong>. \"`n` is odd\" is workable; \"`n²` is "
                "even\" is not.",
                "The statement asserts non-existence or impossibility: use "
                "<strong>contradiction</strong>. Assuming the thing exists gives you an "
                "object to work with, which is the only handle available.",
                "The statement is a conditional and you find yourself assuming `p ∧ ¬q` "
                "and deriving `¬p`: you are doing contraposition. Say so &mdash; the "
                "proof gets shorter and clearer.",
            ]),
            ("thm", ("There are infinitely many primes (Euclid)",
                     "For any finite list of primes, there is a prime not on it.")),
            ("proof", [
                "Suppose `p₁, …, pₙ` are primes and consider `N = p₁p₂⋯pₙ + 1`. `N` is "
                "greater than 1, so it has a prime factor `q`.",
                "If `q` were one of the `pᵢ`, it would divide both the product "
                "`p₁⋯pₙ` and `N`, hence their difference, which is 1. No prime divides 1, "
                "so `q` is not on the list.",
                "Every finite list of primes therefore omits one, so no finite list "
                "contains them all.",
            ]),
            ("p", "This is often presented as a proof by contradiction &mdash; \"assume "
                  "finitely many primes\" &mdash; but as written it is direct and "
                  "constructive: given any list, it produces a prime not on it. That is a "
                  "stronger result, and it is worth noticing that the contradiction was "
                  "never needed."),
        ],
        "lab": ("truth_table", {
            "formulas": ["p -> q", "~q -> ~p", "~p | q", "(p & ~q) -> (r & ~r)",
                         "(p & ~q) -> ~p", "q -> p", "~p -> ~q"],
            "compare_with": "~q -> ~p",
            "mode": "two",
            "panel_title": "Why contraposition is legitimate",
            "panel_intro": "`p -> q` and `~q -> ~p` agree in every row, which is what "
                           "licenses proving one instead of the other. Compare with the "
                           "converse and inverse, which do not.",
        }),
        "steps_title": "Choosing and executing an indirect proof",
        "steps_intro": "Try direct first. Indirect methods are answers to a specific difficulty.",
        "steps": [
            ("Attempt the direct proof and notice where it stalls",
             "The stall is diagnostic. Unable to use `p`? Try contraposition. Nothing to "
             "grab hold of at all? Try contradiction."),
            ("For contraposition, write both negations first",
             "State `¬q → ¬p` explicitly before proving anything. Negating the wrong part "
             "produces the inverse, which is not equivalent."),
            ("For contradiction, say what you are assuming",
             "\"Suppose, for contradiction, that…\" &mdash; and keep that assumption "
             "visibly separate from what you have proved."),
            ("Name the contradiction when you reach it",
             "\"This contradicts the assumption that the fraction was in lowest terms.\" "
             "A reader must not have to search for what went wrong."),
        ],
        "worked": {
            "title": "If `3n + 2` is odd then `n` is odd",
            "intro": ["Direct is awkward; the contrapositive is two lines."],
            "lines": [
                "Contrapositive:  if n is EVEN then 3n + 2 is EVEN.",
                "",
                "Let n be even, so n = 2k for some integer k.",
                "   3n + 2 = 3(2k) + 2 = 6k + 2 = 2(3k + 1)",
                "3k + 1 is an integer, so 3n + 2 is even.",
                "",
                "The contrapositive holds, hence so does the original.      ∎",
            ],
            "after": [
                "The direct route would start from \"`3n + 2` is odd\", giving "
                "`3n + 2 = 2m + 1` and so `3n = 2m − 1` &mdash; and then needs an argument "
                "about why `3n` odd forces `n` odd. Not impossible, but longer, and the "
                "contrapositive avoided it by handing us `n` directly."
            ],
        },
        "quiz_title": "Indirect proof",
        "quiz": [
            {"q": "To prove \"if `n³` is odd then `n` is odd\" by contraposition, you prove:",
             "a": ["if `n` is odd then `n³` is odd",
                   "if `n` is even then `n³` is even",
                   "if `n³` is even then `n` is even",
                   "`n³` is odd and `n` is even, contradiction"],
             "c": 1,
             "why": "The contrapositive negates and swaps: `¬q → ¬p` is \"if `n` is not "
                    "odd then `n³` is not odd\". Option (a) is the converse."},
            {"q": "In a proof by contradiction of statement `s`, what do you assume?",
             "a": ["`s`", "`¬s`", "the hypothesis of `s`", "nothing"],
             "c": 1,
             "why": "You assume the negation of the goal and derive a falsehood, which "
                    "shows the negation cannot hold."},
            {"q": "A proof assumes `p ∧ ¬q` and derives `¬p`. This is best described as:",
             "a": ["an invalid proof",
                   "a proof by contradiction that is really contraposition",
                   "a direct proof",
                   "a proof by cases"],
             "c": 1,
             "why": "Deriving `¬p` from `¬q` is the contrapositive; the assumption `p` "
                    "was carried along unused until it supplied the contradiction. Valid, "
                    "but shorter written as contraposition."},
        ],
        "mistakes": [
            ("Proving the inverse instead of the contrapositive",
             "`¬p → ¬q` is the inverse and is not equivalent to `p → q`. The "
             "contrapositive negates AND swaps."),
            ("Calling every indirect proof a contradiction",
             "If the falsehood you derive is `¬p` and `p` was the hypothesis, you have "
             "proved the contrapositive. Naming it correctly removes an unnecessary "
             "assumption from the proof."),
            ("Not saying which assumption the contradiction contradicts",
             "A proof that ends \"contradiction\" without saying with what leaves the "
             "reader to reconstruct the argument. Name it."),
        ],
        "standard": ("Finish when you can pick the technique from the shape of the claim.",
                     "Prove \"if `n` is an integer and `n² + 5` is odd then `n` is even\" "
                     "&mdash; and be able to say, before starting, which technique you "
                     "will use and why the other would be harder."),
        "note": "Constructive mathematics rejects proof by contradiction for existence "
                "claims: knowing that no counterexample exists is not the same as being "
                "able to produce an example. That distinction has no consequences on this "
                "path, but Euclid's proof above is worth revisiting with it in mind.",
    },
    # ---------------------------------------------------------------- 14
    {
        "slug": "proof-by-cases-and-counterexample",
        "title": "Cases, Counterexamples, and Writing a Proof",
        "module": "Proof",
        "one_line": "Exhaustive cases, single counterexamples, and the standard a proof must meet.",
        "summary": (
            "Split into cases that are exhaustive, or refute a universal claim with one "
            "counterexample. Then the summary of the whole course: what a proof owes its "
            "reader, and why checking cases is never enough."
        ),
        "key": [
            "cases           cover EVERY possibility, prove the claim in each",
            "counterexample  ONE instance refutes ∀x P(x), completely",
            "WLOG            only when a genuine symmetry justifies it",
            "checking n = 1..40 proves nothing about n = 41",
        ],
        "key_label": "The last three techniques",
        "concepts_intro": (
            "Two more techniques, and then the standard everything on this path is held to."
        ),
        "concepts": [
            ("Cases must be exhaustive",
             "A proof by cases is valid only if the cases cover every possibility. They "
             "may overlap; they may not leave a gap."),
            ("One counterexample is a complete refutation",
             "To disprove `∀x P(x)` you exhibit a single `x` with `¬P(x)`. No further "
             "argument is needed or useful."),
            ("Verification is not proof",
             "`n² + n + 41` is prime for `n = 0` through 39 and composite at 40. The lab "
             "lets you meet that personally."),
        ],
        "read_title": "Cases, counterexamples, and the standard",
        "read_intro": "Two techniques, then what separates a proof from a persuasive argument.",
        "body": [
            ("h3", "Proof by cases"),
            ("def", ("Proof by cases",
                     "To prove `s`, find statements `c₁, …, cₙ` with `c₁ ∨ … ∨ cₙ` "
                     "guaranteed true, and prove `s` under each `cᵢ` separately. The "
                     "cases must be <strong>exhaustive</strong>; they need not be "
                     "mutually exclusive.")),
            ("thm", ("`n² + n` is even for every integer `n`",
                     "For all integers `n`, the number `n² + n` is even.")),
            ("proof", [
                "Every integer is even or odd, so these two cases are exhaustive.",
                "<strong>Case 1: `n` is even.</strong> Then `n = 2k`, so "
                "`n² + n = 4k² + 2k = 2(2k² + k)`, which is even.",
                "<strong>Case 2: `n` is odd.</strong> Then `n = 2k + 1`, so "
                "`n² + n = (4k² + 4k + 1) + (2k + 1) = 4k² + 6k + 2 = 2(2k² + 3k + 1)`, "
                "which is even.",
                "In both cases `n² + n` is even, and the cases cover every integer.",
            ]),
            ("p", "A cleaner argument exists &mdash; `n² + n = n(n + 1)`, a product of "
                  "consecutive integers, one of which is even &mdash; and finding it is "
                  "better mathematics. But the case proof is correct, and correctness "
                  "comes first."),
            ("p", "<strong>Without loss of generality</strong> is a legitimate abbreviation "
                  "for a case argument, and only when a genuine symmetry makes the "
                  "remaining cases identical. If proving one case and the other requires "
                  "different arguments, WLOG is being used to hide a gap."),
            ("h3", "Disproof by counterexample"),
            ("def", ("Counterexample",
                     "A <strong>counterexample</strong> to `∀x P(x)` is an element `c` of "
                     "the domain with `¬P(c)`. Exhibiting one disproves the statement "
                     "completely.")),
            ("p", "This follows directly from lesson 10: `¬∀x P(x) ≡ ∃x ¬P(x)`, and an "
                  "existential is proved by producing a witness. It is why negating a "
                  "claim before attacking it is worth the two minutes &mdash; the "
                  "negation describes exactly what you are hunting for."),
            ("example", ("Refuting a plausible claim",
                         "\"Every positive integer is the sum of at most three squares\" "
                         "is false: 7 requires four (`4 + 1 + 1 + 1`). One number settles "
                         "it. The corrected statement &mdash; every positive integer is "
                         "the sum of at most four squares &mdash; is Lagrange's theorem, "
                         "and needs a real proof.")),
            ("h3", "Why checking is not proving"),
            ("p", "This is the point the whole course has been building toward, and "
                  "course 3 exists because of it."),
            ("thm", ("Two statements that survive dozens of checks and are false",
                     "`n² + n + 41` is prime for every `n` from 0 to 39, and composite at "
                     "`n = 40`, where it equals `1681 = 41²`. And `n` points on a circle "
                     "with all chords drawn divide it into `1, 2, 4, 8, 16` regions for "
                     "`n = 1` to 5 &mdash; and 31, not 32, at `n = 6`.")),
            ("p", "Both are in the lab on this page. Meeting them is more useful than "
                  "being told about them: the second in particular gives five consecutive "
                  "powers of two, which is exactly the kind of evidence that feels "
                  "conclusive and is not."),
            ("h3", "What a proof owes its reader"),
            ("ul", [
                "<strong>A precise statement.</strong> Quantifiers, domain, hypotheses. "
                "An imprecise claim cannot be proved or refuted.",
                "<strong>A declared method.</strong> \"We prove the contrapositive\", "
                "\"suppose for contradiction\", \"there are two cases\". The reader should "
                "know the shape before the details.",
                "<strong>Justified steps.</strong> Every line follows from a definition, a "
                "hypothesis, or a result already established.",
                "<strong>No gaps disguised as brevity.</strong> \"Clearly\" and \"it is "
                "obvious that\" are where errors hide. If it is clear, the reason is short "
                "&mdash; write it.",
                "<strong>An explicit ending.</strong> State what has been proved.",
            ]),
            ("p", "A proof is a social object as much as a logical one: its purpose is to "
                  "convince a careful, skeptical reader who does not already believe the "
                  "claim. Everything in the last three lessons serves that purpose."),
        ],
        "lab": ("induction", {
            "statement": "prime41",
            "panel_title": "Two false statements to find",
            "panel_intro": "Two entries in the list are false and pass every check a "
                           "careful person would run. Push the slider until each breaks, "
                           "and note how far it went first.",
        }),
        "steps_title": "Cases and counterexamples",
        "steps_intro": "Coverage for cases; a single instance for a counterexample.",
        "steps": [
            ("Check the cases are exhaustive",
             "State why they cover everything: every integer is even or odd, every real "
             "is negative, zero or positive. A gap invalidates the whole proof."),
            ("Prove the claim in each case separately",
             "Each case is its own small proof and gets the full treatment. Sharing an "
             "argument across cases without saying so is where errors enter."),
            ("Use WLOG only for genuine symmetry",
             "State the symmetry: \"by symmetry in `x` and `y`, assume `x ≤ y`\". If you "
             "cannot state it, do the other case."),
            ("To disprove, produce the witness",
             "Negate the claim to learn what the counterexample must satisfy, then find "
             "one and verify it explicitly. Verification is not optional."),
        ],
        "worked": {
            "title": "Prove `|x + y| ≤ |x| + |y|` for all reals",
            "intro": ["The triangle inequality, by cases on the sign of `x + y`."],
            "lines": [
                "Case 1: x + y ≥ 0.",
                "   |x + y| = x + y ≤ |x| + |y|,",
                "   since x ≤ |x| and y ≤ |y| always hold.",
                "",
                "Case 2: x + y < 0.",
                "   |x + y| = −(x + y) = (−x) + (−y) ≤ |x| + |y|,",
                "   since −x ≤ |x| and −y ≤ |y| always hold.",
                "",
                "Every real number is ≥ 0 or < 0, so the cases are exhaustive.   ∎",
            ],
            "after": [
                "The two cases are near-mirrors, which invites a WLOG. It would not be "
                "legitimate here: the symmetry is between `x + y ≥ 0` and `x + y &lt; 0`, "
                "not between `x` and `y`, and the second case genuinely uses "
                "`−x ≤ |x|` rather than `x ≤ |x|`. Writing both is two extra lines and "
                "removes all doubt."
            ],
        },
        "quiz_title": "Cases and counterexamples",
        "quiz": [
            {"q": "How many counterexamples are needed to disprove `∀x P(x)`?",
             "a": ["One", "At least two", "Half the domain", "All of them"],
             "c": 0,
             "why": "`¬∀x P(x) ≡ ∃x ¬P(x)`, and an existential is proved by one witness. "
                    "Further counterexamples add nothing logically."},
            {"q": "A proof by cases splits into `x` positive and `x` negative. What is wrong?",
             "a": ["The cases overlap",
                   "The cases are not exhaustive: `x = 0` is uncovered",
                   "Nothing", "Cases must be mutually exclusive"],
             "c": 1,
             "why": "Zero falls in neither case, so the proof establishes nothing about "
                    "it. Overlapping cases are fine; a gap is fatal."},
            {"q": "A statement has been verified for `n = 1` through `n = 1000`. What follows?",
             "a": ["It is true for all `n`",
                   "It is very likely true for all `n`",
                   "It is true for those 1000 values and nothing more follows",
                   "It is a theorem"],
             "c": 2,
             "why": "`n² + n + 41` survives 40 checks and fails at 40; the chord-region "
                    "formula survives 5 and fails at 6. Verification establishes exactly "
                    "the cases verified."},
        ],
        "mistakes": [
            ("Cases with a gap",
             "\"Positive or negative\" omits zero; \"greater than or less than\" omits "
             "equality. State why the cases cover everything, every time."),
            ("Using WLOG where there is no symmetry",
             "It is the most common way a real gap gets past a reader, because it reads "
             "like rigour. If the other case needs a different argument, write it."),
            ("Offering many examples in place of a proof",
             "Twenty confirming instances and zero counterexamples is not weak evidence "
             "for a universal claim &mdash; it is not evidence of the right kind at all. "
             "Course 3 supplies what is."),
        ],
        "standard": ("Finish when you can state, for any claim, what would refute it.",
                     "That single habit &mdash; asking what a counterexample would look "
                     "like before trying to prove anything &mdash; is what this course "
                     "was for. It tells you whether to hunt for a proof or for a "
                     "counterexample, and it is the mechanical negation of lesson 10 put "
                     "to work."),
        "note": "Course 3 supplies the technique this lesson leaves missing: induction "
                "proves a statement for every natural number by proving one implication "
                "rather than infinitely many cases. It is the answer to \"checking is not "
                "proving\", and it is two courses away.",
    },
]
