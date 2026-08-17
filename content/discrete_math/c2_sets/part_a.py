"""Course 2, lessons 01-07 — sets and relations."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "sets-and-membership",
        "title": "Sets and Membership",
        "module": "Sets",
        "one_line": "Collections, membership, and the two ways to describe a set.",
        "summary": (
            "A set is determined entirely by what belongs to it. Roster and "
            "set-builder notation, the empty set, and why order and repetition carry "
            "no information."
        ),
        "key": [
            "A = {1, 2, 3}                    roster notation",
            "A = {x ∈ ℤ : 0 < x < 4}          set-builder notation",
            "A = B   ⟺   ∀x (x ∈ A ↔ x ∈ B)   extensionality",
            "{1, 2} = {2, 1} = {1, 1, 2}      order and repetition mean nothing",
        ],
        "key_label": "One set, several descriptions",
        "concepts_intro": (
            "Two sets are equal when they have the same members. Everything in this "
            "lesson follows from that single sentence."
        ),
        "concepts": [
            ("A set is its members",
             "`{1, 2}` and `{2, 1, 1}` are the same set. Notation differs; the object "
             "does not. This is called <em>extensionality</em>."),
            ("Membership is the primitive relation",
             "`x ∈ A` is either true or false for every `x`. A collection where "
             "membership is uncertain is not a set in this sense."),
            ("The empty set is a set",
             "`∅` has no members, and there is only one such set. `∅` and `{∅}` are "
             "different: the second has one member, which happens to be empty."),
        ],
        "read_title": "What a set is",
        "read_intro": "Notation, equality, and the standard number sets.",
        "body": [
            ("def", ("Set and membership",
                     "A <strong>set</strong> is a collection of distinct objects, called "
                     "its <strong>elements</strong> or <strong>members</strong>. We write "
                     "`x ∈ A` when `x` is a member of `A`, and `x ∉ A` when it is not.")),
            ("p", "Two notations describe sets. <strong>Roster</strong> notation lists the "
                  "members: `A = {2, 3, 5, 7}`. <strong>Set-builder</strong> notation "
                  "states the property that characterises them: "
                  "`A = {x ∈ ℤ : x is prime and x &lt; 10}`. The colon is read \"such "
                  "that\", and a vertical bar is used equally often."),
            ("def", ("Extensionality",
                     "`A = B` exactly when every member of `A` is a member of `B` and "
                     "conversely &mdash; that is, `∀x (x ∈ A ↔ x ∈ B)`. A set carries no "
                     "information beyond its membership.")),
            ("p", "Two consequences follow immediately, and both surprise people once. "
                  "Order carries no information: `{1, 2} = {2, 1}`. Repetition carries "
                  "none either: `{1, 1, 2} = {1, 2}`. If you need order, you need a "
                  "sequence or a tuple, which lesson 5 supplies."),
            ("def", ("The empty set",
                     "`∅` (also written `{}`) is the set with no members. There is exactly "
                     "one: any two sets with no members satisfy extensionality vacuously.")),
            ("p", "The distinction between `∅` and `{∅}` is worth ten seconds. The first "
                  "has zero members. The second has one member &mdash; the empty set. "
                  "`|∅| = 0` and `|{∅}| = 1`, and a box containing an empty box is not "
                  "an empty box."),
            ("h3", "The standard sets"),
            ("math", [
                "ℕ    natural numbers      {0, 1, 2, 3, …}   (0 included here)",
                "ℤ    integers             {…, −2, −1, 0, 1, 2, …}",
                "ℚ    rationals            {a/b : a, b ∈ ℤ,  b ≠ 0}",
                "ℝ    real numbers",
                "ℂ    complex numbers",
            ]),
            ("p", "Whether `0 ∈ ℕ` is a convention, not a fact, and sources differ. This "
                  "path includes it, and says so wherever it matters &mdash; a base case "
                  "at `n = 0` versus `n = 1` is exactly the kind of detail course 3 "
                  "cannot leave ambiguous."),
            ("def", ("Cardinality",
                     "For a finite set `A`, `|A|` is the number of members. `|{1, 2, 3}| = 3` "
                     "and `|∅| = 0`. Lesson 13 extends this to infinite sets, where it "
                     "stops behaving the way the notation suggests.")),
            ("example", ("Set-builder can hide emptiness",
                         "`{x ∈ ℝ : x² &lt; 0}` is `∅`, written in a form that does not "
                         "look empty. A set-builder description says which objects belong; "
                         "it does not promise that any do.")),
        ],
        "lab": ("sets", {
            "default": ["A", "B"],
            "panel_title": "Twelve elements, three sets",
            "panel_intro": "Click an element to cycle it through the eight possible "
                           "memberships. The chips below the diagram show which elements "
                           "are in each region.",
        }),
        "steps_title": "Working with a set description",
        "steps_intro": "Decide membership one element at a time.",
        "steps": [
            ("Read the set-builder condition as a predicate",
             "`{x ∈ ℤ : P(x)}` is exactly the elements of `ℤ` satisfying `P`. The domain "
             "before the colon matters as much as the condition after it."),
            ("Test a few candidate elements",
             "Substituting three or four values tells you whether you have read the "
             "condition correctly. It does not tell you the set."),
            ("Check whether the set is empty",
             "A condition no element satisfies describes `∅`. This is not an error, and "
             "it is easy to miss."),
            ("Convert between notations",
             "Roster for small sets, set-builder for large or infinite ones. Being able "
             "to move between them is what makes a proof of equality writable."),
        ],
        "worked": {
            "title": "Deciding membership",
            "intro": ["Let `A = {x ∈ ℤ : x = 3k + 1 for some k ∈ ℤ}`."],
            "lines": [
                "Is 7 ∈ A?    7 = 3(2) + 1     yes, with k = 2",
                "Is 9 ∈ A?    9 = 3(3) + 0     no  — 9 = 3k + 1 has no integer solution",
                "Is −2 ∈ A?  −2 = 3(−1) + 1    yes, with k = −1",
                "",
                "So A = {…, −5, −2, 1, 4, 7, 10, …}   — the integers ≡ 1 (mod 3).",
                "Course 6 gives that description its own notation.",
            ],
            "after": [
                "Note that `−2` required a negative `k`. Set-builder conditions quantify "
                "over the domain stated, and forgetting that `k` may be negative is how "
                "half a set goes missing."
            ],
        },
        "quiz_title": "Sets and membership",
        "quiz": [
            {"q": "Which is true?",
             "a": ["`{1, 2, 2, 3}` has four elements",
                   "`{1, 2, 3} ≠ {3, 2, 1}`",
                   "`{1, 2, 2, 3} = {1, 2, 3}`",
                   "`∅ = {∅}`"],
             "c": 2,
             "why": "Repetition carries no information, so both sets have exactly the "
                    "members 1, 2 and 3. Order carries none either."},
            {"q": "What is `|{∅, {∅}}|`?",
             "a": ["0", "1", "2", "undefined"],
             "c": 2,
             "why": "Two members: the empty set, and the set containing the empty set. "
                    "They are different objects, so both count."},
            {"q": "`{x ∈ ℕ : x &lt; 0}` is:",
             "a": ["`∅`", "`{0}`", "undefined", "all negative integers"],
             "c": 0,
             "why": "No natural number is negative, so nothing satisfies the condition. "
                    "A set-builder description that nothing satisfies denotes the empty set."},
        ],
        "mistakes": [
            ("Confusing `∈` with `⊆`",
             "`1 ∈ {1, 2}` is true; `1 ⊆ {1, 2}` is not even well formed, because 1 is "
             "not a set. Lesson 2 makes the distinction sharp."),
            ("Reading `{∅}` as empty",
             "It has one element. This matters immediately in lesson 2, where the power "
             "set of `∅` is `{∅}` &mdash; a set with one member."),
            ("Forgetting the domain in set-builder notation",
             "`{x : x² = 2}` is empty over `ℚ` and has two elements over `ℝ`. The part "
             "before the colon is half the definition."),
        ],
        "standard": ("Finish when you can convert between the two notations in both "
                     "directions.",
                     "Given `{2, 4, 6, 8, 10}`, write a set-builder description; given "
                     "`{x ∈ ℤ : x² &lt; 10}`, write the roster. If the second gives you "
                     "seven elements you have remembered the negatives."),
        "note": "Naive set theory &mdash; \"a set is any collection\" &mdash; is "
                "inconsistent if pushed: the set of all sets that do not contain "
                "themselves cannot exist. Every set on this path is built from a stated "
                "domain, which is enough to stay clear of the problem.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "subsets-and-power-sets",
        "title": "Subsets and Power Sets",
        "module": "Sets",
        "one_line": "Containment, proper containment, and the set of all subsets.",
        "summary": (
            "`A ⊆ B` is a universally quantified conditional, which is why the empty "
            "set is a subset of everything. The power set collects all subsets, and "
            "there are exactly `2ⁿ` of them."
        ),
        "key": [
            "A ⊆ B    ⟺   ∀x (x ∈ A → x ∈ B)",
            "∅ ⊆ A    for every A                (vacuously)",
            "A = B    ⟺   A ⊆ B and B ⊆ A        the double-inclusion proof",
            "|P(A)| = 2^|A|",
        ],
        "key_label": "Containment and its consequences",
        "concepts_intro": (
            "Subset is defined by a conditional, and every surprising fact in this "
            "lesson comes from that conditional being vacuously true."
        ),
        "concepts": [
            ("Subset is a conditional, quantified",
             "`A ⊆ B` says every member of `A` is a member of `B`. Course 1's rules for "
             "`∀` and `→` apply unchanged."),
            ("The empty set is a subset of everything",
             "`∀x (x ∈ ∅ → x ∈ B)` is vacuously true, since nothing is in `∅`. This is "
             "not a special case; it is the definition applied honestly."),
            ("Double inclusion is how set equality is proved",
             "To show `A = B`, show `A ⊆ B` and `B ⊆ A`. Two conditional proofs, one in "
             "each direction &mdash; exactly like a biconditional."),
        ],
        "read_title": "Containment and the power set",
        "read_intro": "The definition, the proof technique it gives you, and the counting result.",
        "body": [
            ("def", ("Subset",
                     "`A ⊆ B` (\"`A` is a subset of `B`\") means `∀x (x ∈ A → x ∈ B)`. "
                     "`A ⊂ B` or `A ⊊ B` means `A ⊆ B` and `A ≠ B` &mdash; a "
                     "<strong>proper</strong> subset.")),
            ("p", "`∈` and `⊆` are different relations and mixing them is the standard "
                  "error. `1 ∈ {1, 2}` and `{1} ⊆ {1, 2}` are both true; `1 ⊆ {1, 2}` and "
                  "`{1} ∈ {1, 2}` are both false. The first because 1 is not a set, the "
                  "second because the members of `{1, 2}` are 1 and 2, not `{1}`."),
            ("thm", ("Every set contains the empty set",
                     "`∅ ⊆ A` for every set `A`.")),
            ("proof", [
                "The claim is `∀x (x ∈ ∅ → x ∈ A)`. The hypothesis `x ∈ ∅` is false for "
                "every `x`, so each conditional is vacuously true, and the universal "
                "statement holds. There is nothing to check, which is exactly why it holds.",
            ]),
            ("thm", ("Set equality by double inclusion",
                     "`A = B` if and only if `A ⊆ B` and `B ⊆ A`.")),
            ("p", "This is the workhorse. To prove two sets equal, take an arbitrary "
                  "element of one and show it belongs to the other, then do the same in "
                  "reverse. Each half is a direct proof of a conditional, which is "
                  "exactly what course 1 lesson 12 taught."),
            ("def", ("Power set",
                     "The <strong>power set</strong> `P(A)` is the set of all subsets of "
                     "`A`: `P(A) = {S : S ⊆ A}`. Its members are sets.")),
            ("example", ("Power sets of small sets",
                         "`P(∅) = {∅}` &mdash; one member. `P({a}) = {∅, {a}}` &mdash; two. "
                         "`P({a, b}) = {∅, {a}, {b}, {a, b}}` &mdash; four. "
                         "`P({a, b, c})` has eight.")),
            ("thm", ("The power set doubles",
                     "If `|A| = n` then `|P(A)| = 2ⁿ`.")),
            ("proof", [
                "A subset of `A` is determined by an independent yes/no decision for each "
                "of the `n` elements: is it in, or out? Two choices, made `n` times "
                "independently, give `2ⁿ` distinct subsets, and distinct choice patterns "
                "give distinct subsets because a set is determined by its members.",
                "Course 4 formalises this as the product rule; course 3 proves it again "
                "by induction on `n`.",
            ]),
            ("p", "The doubling is why power sets are not something to enumerate casually. "
                  "A ten-element set has 1024 subsets; a thirty-element set has over a "
                  "billion. This is the same `2ⁿ` as the truth table row count, and for "
                  "the same reason: a subset is a truth assignment to the membership "
                  "question."),
        ],
        "lab": ("counting", {
            "n": 4, "r": 2, "rule": "c",
            "panel_title": "Subsets by size",
            "panel_intro": "The C column counts subsets of a given size. Summing it over "
                           "all sizes from 0 to `n` gives `2ⁿ` &mdash; the identity course "
                           "4 lesson 5 highlights in Pascal's triangle.",
        }),
        "steps_title": "Proving a containment or an equality",
        "steps_intro": "One arbitrary element, followed all the way through.",
        "steps": [
            ("To prove `A ⊆ B`, take an arbitrary `x ∈ A`",
             "Then show `x ∈ B`, using nothing about `x` beyond its membership in `A`."),
            ("Unfold the definitions of both sets",
             "If `A = {x : P(x)}`, then `x ∈ A` means `P(x)`. The proof is then a "
             "propositional argument from `P(x)` to `Q(x)`."),
            ("To prove `A = B`, do it twice",
             "Both inclusions, each written out. Proving one and asserting the other is "
             "the incomplete answer this technique exists to prevent."),
            ("To disprove `A ⊆ B`, exhibit one element",
             "One `x` with `x ∈ A` and `x ∉ B` settles it, exactly as one counterexample "
             "refutes any universal claim."),
        ],
        "worked": {
            "title": "Prove `A ∩ B ⊆ A ∪ B`",
            "intro": ["One inclusion, one arbitrary element."],
            "lines": [
                "Let x be arbitrary with x ∈ A ∩ B.",
                "",
                "By definition of intersection:  x ∈ A  and  x ∈ B.",
                "In particular x ∈ A.",
                "By definition of union, x ∈ A is enough for x ∈ A ∪ B.",
                "",
                "Since x was arbitrary, A ∩ B ⊆ A ∪ B.        ∎",
                "",
                "The reverse inclusion is FALSE: take A = {1}, B = {2}.",
                "Then A ∪ B = {1, 2} but A ∩ B = ∅, and 1 ∉ A ∩ B.",
            ],
            "after": [
                "The counterexample at the end is doing real work. Having proved one "
                "inclusion it is tempting to assume the other; one two-element example "
                "shows it fails, and produces the standard fact that intersection is "
                "contained in union and not conversely."
            ],
        },
        "quiz_title": "Subsets",
        "quiz": [
            {"q": "Which is true for `A = {1, {2}}`?",
             "a": ["`2 ∈ A`", "`{2} ∈ A`", "`{2} ⊆ A`", "`{1} ∈ A`"],
             "c": 1,
             "why": "The members of `A` are 1 and `{2}`. So `{2} ∈ A` holds; `2 ∈ A` does "
                    "not, because 2 itself is not a member."},
            {"q": "How many subsets does a set with 5 elements have?",
             "a": ["5", "10", "25", "32"],
             "c": 3,
             "why": "`2⁵ = 32`. Each element is independently in or out, which is five "
                    "binary choices."},
            {"q": "Why is `∅ ⊆ A` for every `A`?",
             "a": ["By convention",
                   "Because `∅` has no elements, so the defining conditional is vacuously true",
                   "Because `∅ ∈ A`",
                   "It is false when `A = ∅`"],
             "c": 1,
             "why": "`∀x (x ∈ ∅ → x ∈ A)` has a false hypothesis in every instance, so "
                    "every instance is true. It holds for `A = ∅` too."},
        ],
        "mistakes": [
            ("Writing `∈` where `⊆` is meant",
             "`{1} ∈ {1, 2}` is false and `{1} ⊆ {1, 2}` is true. The two symbols relate "
             "different kinds of thing, and no context makes them interchangeable."),
            ("Proving one inclusion and claiming equality",
             "`A ⊆ B` is half of `A = B`. The other half needs its own argument, and is "
             "often the half that fails."),
            ("Forgetting `A ⊆ A`",
             "Every set is a subset of itself, so `⊆` is reflexive while `⊂` is not. "
             "That difference is what makes `⊆` a partial order in lesson 9."),
        ],
        "standard": ("Finish when double inclusion is your reflex for any set equality.",
                     "Prove `A ∩ (A ∪ B) = A` by double inclusion. Both directions are "
                     "three lines, and writing them is what makes lesson 4's algebraic "
                     "shortcuts safe to use."),
        "note": "`|P(A)| = 2^|A|` holds for infinite sets too, in the sense that `P(A)` "
                "is always strictly larger than `A` &mdash; Cantor's theorem, which "
                "lesson 13 proves for the case that matters.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "set-operations",
        "title": "Set Operations",
        "module": "Sets",
        "one_line": "Union, intersection, difference, complement, symmetric difference.",
        "summary": (
            "Five operations, each defined by a connective from course 1. Union is `∨`, "
            "intersection is `∧`, complement is `¬` &mdash; which is why the set "
            "identities are the logical equivalences wearing different symbols."
        ),
        "key": [
            "A ∪ B = {x : x ∈ A  ∨  x ∈ B}",
            "A ∩ B = {x : x ∈ A  ∧  x ∈ B}",
            "A \\ B = {x : x ∈ A  ∧  x ∉ B}",
            "Ā     = {x ∈ U : x ∉ A}          complement, relative to a universe U",
        ],
        "key_label": "Each operation is a connective",
        "concepts_intro": (
            "Every set operation is a logical connective applied to membership. That "
            "correspondence is the reason to have done course 1 first."
        ),
        "concepts": [
            ("Union is inclusive",
             "`x ∈ A ∪ B` when `x` is in at least one. Elements in both are in the union "
             "once &mdash; a set has no multiplicities."),
            ("Complement needs a universe",
             "`Ā` is meaningless without a stated universal set `U`. The complement of "
             "the even numbers is different inside `ℤ` and inside `ℝ`."),
            ("Difference is not symmetric",
             "`A \\ B` and `B \\ A` are generally different sets. Symmetric difference "
             "`A △ B` is the union of the two, and is the set analogue of `⊕`."),
        ],
        "read_title": "The five operations",
        "read_intro": "Definitions, then the correspondence with the connectives.",
        "body": [
            ("def", ("Union, intersection, difference",
                     "`A ∪ B = {x : x ∈ A ∨ x ∈ B}`, "
                     "`A ∩ B = {x : x ∈ A ∧ x ∈ B}`, "
                     "`A \\ B = {x : x ∈ A ∧ x ∉ B}`.")),
            ("def", ("Complement",
                     "Relative to a <strong>universal set</strong> `U` containing every "
                     "set under discussion, `Ā = U \\ A = {x ∈ U : x ∉ A}`.")),
            ("def", ("Symmetric difference",
                     "`A △ B = (A \\ B) ∪ (B \\ A)` &mdash; the elements in exactly one of "
                     "the two. Equivalently `(A ∪ B) \\ (A ∩ B)`.")),
            ("def", ("Disjoint",
                     "`A` and `B` are <strong>disjoint</strong> when `A ∩ B = ∅`. A "
                     "collection is <strong>pairwise disjoint</strong> when every two "
                     "distinct members of it are disjoint &mdash; the condition lesson 8 "
                     "needs for partitions.")),
            ("h3", "The correspondence with logic"),
            ("math", [
                "set operation        membership condition       connective",
                "A ∪ B                x ∈ A  ∨  x ∈ B            ∨",
                "A ∩ B                x ∈ A  ∧  x ∈ B            ∧",
                "Ā                    ¬(x ∈ A)                   ¬",
                "A \\ B                x ∈ A  ∧  ¬(x ∈ B)         ∧, ¬",
                "A △ B                x ∈ A  ⊕  x ∈ B            ⊕",
                "A ⊆ B                x ∈ A  →  x ∈ B            →",
            ]),
            ("p", "This is not an analogy. Every set identity in lesson 4 is a logical "
                  "equivalence from course 1 lesson 5, applied pointwise to membership. "
                  "De Morgan for sets and De Morgan for propositions are the same theorem "
                  "in two notations, and knowing that halves what has to be memorised."),
            ("thm", ("Inclusion-exclusion for two sets",
                     "For finite sets, `|A ∪ B| = |A| + |B| − |A ∩ B|`.")),
            ("proof", [
                "Adding `|A|` and `|B|` counts every element of `A ∩ B` twice &mdash; once "
                "in each term &mdash; and every other element of `A ∪ B` once. Subtracting "
                "`|A ∩ B|` removes exactly the surplus.",
            ]),
            ("p", "Course 4 lesson 10 generalises this to any number of sets, where the "
                  "alternating signs are less obvious and the correction is larger. The "
                  "two-set case is worth having by heart now."),
            ("example", ("Difference is not symmetric",
                         "With `A = {1, 2, 3}` and `B = {3, 4}`: `A \\ B = {1, 2}` and "
                         "`B \\ A = {4}`. Their union `{1, 2, 4}` is `A △ B`, and "
                         "`A ∩ B = {3}` is exactly what `△` excludes.")),
        ],
        "lab": ("sets", {
            "default": ["A ∪ (B ∩ C)", "(A ∪ B) ∩ (A ∪ C)"],
            "panel_title": "Evaluate any expression",
            "panel_intro": "Both expressions are evaluated against the same membership, "
                           "so the row labelled \"difference\" lists exactly the elements "
                           "separating them &mdash; empty when they are equal.",
        }),
        "steps_title": "Evaluating a set expression",
        "steps_intro": "Translate to membership conditions, then evaluate elementwise.",
        "steps": [
            ("Rewrite the expression as a membership condition",
             "`x ∈ A ∩ (B ∪ C)` becomes `x ∈ A ∧ (x ∈ B ∨ x ∈ C)`. From here it is "
             "propositional logic."),
            ("Decide the condition for each element in turn",
             "With a small universe this is quick and cannot go wrong. It is also how "
             "the lab computes."),
            ("Watch the universe when complementing",
             "`Ā` depends entirely on `U`. An expression mixing complements and an "
             "unstated universe is not well defined."),
            ("Check a boundary case",
             "What does the expression give when `A = ∅`, or when `A = B`? Degenerate "
             "cases catch misreadings faster than general ones."),
        ],
        "worked": {
            "title": "Evaluating `(A \\ B) ∪ (B ∩ C)`",
            "intro": ["`U = {1,…,8}`, `A = {1,2,3,4}`, `B = {3,4,5,6}`, `C = {4,6,8}`."],
            "lines": [
                "A \\ B   = {1, 2, 3, 4} minus anything in B   = {1, 2}",
                "B ∩ C   = {3,4,5,6} ∩ {4,6,8}                 = {4, 6}",
                "union    = {1, 2} ∪ {4, 6}                     = {1, 2, 4, 6}",
                "",
                "Check element by element:",
                "  1 ∈ A, 1 ∉ B  ⟹ in A\\B          ✓",
                "  3 ∈ A but 3 ∈ B ⟹ not in A\\B;  3 ∉ C ⟹ not in B∩C   ✗",
                "  4 ∈ A and 4 ∈ B ⟹ not in A\\B;  4 ∈ B and 4 ∈ C ⟹ in B∩C  ✓",
            ],
            "after": [
                "Element 4 is the interesting one: it fails the first term and passes the "
                "second. Checking a few elements individually is how you catch a "
                "misplaced parenthesis, which the set-level calculation hides."
            ],
        },
        "quiz_title": "Operations",
        "quiz": [
            {"q": "`A = {1,2,3}`, `B = {3,4}`. What is `A △ B`?",
             "a": ["`{3}`", "`{1,2,4}`", "`{1,2,3,4}`", "`{1,2}`"],
             "c": 1,
             "why": "Symmetric difference keeps the elements in exactly one set. 3 is in "
                    "both, so it is excluded."},
            {"q": "`Ā` is well defined only when:",
             "a": ["`A` is finite", "a universal set `U` has been stated",
                   "`A` is nonempty", "always"],
             "c": 1,
             "why": "The complement is relative: the complement of the evens is different "
                    "inside `ℤ` and inside `ℝ`."},
            {"q": "`|A| = 7`, `|B| = 5`, `|A ∩ B| = 2`. What is `|A ∪ B|`?",
             "a": ["12", "10", "14", "9"],
             "c": 1,
             "why": "`7 + 5 − 2 = 10`. Adding the sizes double-counts the intersection, "
                    "so it is subtracted once."},
        ],
        "mistakes": [
            ("Assuming `A \\ B = B \\ A`",
             "Difference is not symmetric. `A \\ B` keeps what is in `A` only; `B \\ A` "
             "keeps what is in `B` only, and those are different sets."),
            ("Adding cardinalities without subtracting the overlap",
             "`|A ∪ B| = |A| + |B|` holds only when `A` and `B` are disjoint. Otherwise "
             "the shared elements are counted twice."),
            ("Complementing without a universe",
             "An expression containing `Ā` and no stated `U` is incomplete. The lab pins "
             "`U = {1, …, 12}` for exactly this reason."),
        ],
        "standard": ("Finish when you can translate any set expression into a membership "
                     "condition without hesitating.",
                     "Take `(A △ B) \\ C` and write the condition for `x` to belong. If "
                     "you produce `(x ∈ A ⊕ x ∈ B) ∧ x ∉ C`, the rest of the course's set "
                     "algebra is course 1 in different symbols."),
        "note": "`A △ B` is associative and every element is its own inverse under it, "
                "which makes the subsets of `U` a group under symmetric difference. That "
                "structure is why `△` behaves like addition modulo 2, the same connection "
                "`⊕` had in course 1.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "set-identities",
        "title": "Set Identities and Proofs",
        "module": "Sets",
        "one_line": "The laws, and the two ways to prove one.",
        "summary": (
            "The set identities are course 1's logical equivalences in set notation. "
            "Prove them by double inclusion or by a chain of laws &mdash; and note that "
            "a Venn diagram illustrates without proving."
        ),
        "key": [
            "(A ∪ B)‾ = Ā ∩ B̄               De Morgan",
            "(A ∩ B)‾ = Ā ∪ B̄               De Morgan",
            "A ∩ (B ∪ C) = (A∩B) ∪ (A∩C)    distribution",
            "A ∪ (A ∩ B) = A                absorption",
        ],
        "key_label": "Four identities worth knowing",
        "concepts_intro": (
            "Every identity here is a logical equivalence in disguise, which means "
            "course 1 already did most of the work."
        ),
        "concepts": [
            ("Every set law mirrors a logical law",
             "De Morgan for sets follows from De Morgan for propositions applied to the "
             "membership condition. There is nothing new to memorise, only a translation."),
            ("Double inclusion always works",
             "Take an arbitrary element of each side and show it belongs to the other. "
             "Longer than a chain of laws, and impossible to get wrong."),
            ("A Venn diagram is not a proof",
             "It shows the identity on a picture of the general position. It is excellent "
             "for finding identities and for spotting false ones, and it establishes "
             "nothing on its own."),
        ],
        "read_title": "The identities and how to establish them",
        "read_intro": "The laws, then both proof routes on the same example.",
        "body": [
            ("math", [
                "identity        A ∪ ∅ = A            A ∩ U = A",
                "domination      A ∪ U = U            A ∩ ∅ = ∅",
                "idempotent      A ∪ A = A            A ∩ A = A",
                "complementation (Ā)‾ = A",
                "commutative     A ∪ B = B ∪ A        A ∩ B = B ∩ A",
                "associative     (A ∪ B) ∪ C = A ∪ (B ∪ C)",
                "distributive    A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)",
                "                A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)",
                "De Morgan       (A ∪ B)‾ = Ā ∩ B̄     (A ∩ B)‾ = Ā ∪ B̄",
                "absorption      A ∪ (A ∩ B) = A      A ∩ (A ∪ B) = A",
                "complement      A ∪ Ā = U            A ∩ Ā = ∅",
                "difference      A \\ B = A ∩ B̄",
            ]),
            ("p", "Set every one of these beside the corresponding line in course 1 "
                  "lesson 5 and the correspondence is exact: `∪` for `∨`, `∩` for `∧`, "
                  "overbar for `¬`, `U` for `T`, `∅` for `F`. The last line is the most "
                  "useful in practice, because it removes `\\` from an expression and "
                  "leaves only operations the laws speak about."),
            ("thm", ("De Morgan for sets",
                     "`(A ∪ B)‾ = Ā ∩ B̄` for all sets `A`, `B` inside a universe `U`.")),
            ("proof", [
                "<strong>(⊆)</strong> Let `x ∈ (A ∪ B)‾`. Then `x ∈ U` and `x ∉ A ∪ B`, "
                "so it is not the case that `x ∈ A` or `x ∈ B`. By De Morgan for "
                "propositions, `x ∉ A` and `x ∉ B`, so `x ∈ Ā` and `x ∈ B̄`, hence "
                "`x ∈ Ā ∩ B̄`.",
                "<strong>(⊇)</strong> Let `x ∈ Ā ∩ B̄`. Then `x ∉ A` and `x ∉ B`, so `x` "
                "is in neither, so `x ∉ A ∪ B`, so `x ∈ (A ∪ B)‾`.",
                "Both inclusions hold, so the sets are equal.",
            ]),
            ("p", "The second half is the first half read backwards, because every step "
                  "used a biconditional. When that happens the two inclusions can be "
                  "written as a single chain of `⟺`, which is shorter and just as "
                  "rigorous &mdash; provided every step really is reversible."),
            ("h3", "The chain-of-laws route"),
            ("math", [
                "A \\ (A ∩ B)",
                "  = A ∩ (A ∩ B)‾          difference law",
                "  = A ∩ (Ā ∪ B̄)           De Morgan",
                "  = (A ∩ Ā) ∪ (A ∩ B̄)     distribution",
                "  = ∅ ∪ (A ∩ B̄)           complement",
                "  = A ∩ B̄                 identity",
                "  = A \\ B                 difference law",
            ]),
            ("p", "Six named steps, no arbitrary elements, and each line justified. This "
                  "is the faster route once the laws are familiar, and it fails safely: a "
                  "step you cannot name is a step you have not made."),
            ("h3", "Why a Venn diagram is not enough"),
            ("p", "A three-set Venn diagram shows eight regions, which is every possible "
                  "membership pattern, so shading it does establish a three-set identity. "
                  "What it does not do is generalise: there is no readable Venn diagram "
                  "for five sets, and the usual four-circle picture is missing regions. "
                  "The diagram is a device for seeing what is true, and the proof is "
                  "still owed."),
        ],
        "lab": ("sets", {
            "default": ["(A ∪ B)‾", "Ā ∩ B̄"],
            "panel_title": "Try to break an identity",
            "panel_intro": "Both sides are evaluated on your membership. If an identity "
                           "is real, no arrangement of the twelve elements separates them "
                           "&mdash; and failing to break it is worth more than being told.",
        }),
        "steps_title": "Proving a set identity",
        "steps_intro": "Pick the route by how many operations are involved.",
        "steps": [
            ("Two or three operations? Chain the laws",
             "Rewrite `\\` as `∩` with a complement first, then apply De Morgan, "
             "distribution and absorption, naming each."),
            ("Anything unfamiliar? Double inclusion",
             "Take an arbitrary `x` in the left side and derive membership in the right, "
             "then reverse. It always works and needs no recall."),
            ("Watch for reversibility",
             "If every step is a biconditional you may write one chain of `⟺` instead of "
             "two inclusions. If any step is one-way, you owe both directions."),
            ("To refute, find one element",
             "A single element in one side and not the other disproves the identity. The "
             "lab's difference row is exactly this."),
        ],
        "worked": {
            "title": "Prove `A \\ (B ∪ C) = (A \\ B) ∩ (A \\ C)`",
            "intro": ["By the chain of laws, which is shorter than double inclusion here."],
            "lines": [
                "A \\ (B ∪ C)",
                "  = A ∩ (B ∪ C)‾           difference law",
                "  = A ∩ (B̄ ∩ C̄)            De Morgan",
                "  = (A ∩ A) ∩ (B̄ ∩ C̄)      idempotent, backwards",
                "  = (A ∩ B̄) ∩ (A ∩ C̄)      commutative and associative",
                "  = (A \\ B) ∩ (A \\ C)      difference law, twice",
            ],
            "after": [
                "Step three is the one that looks like a trick. Replacing `A` by `A ∩ A` "
                "is legitimate because idempotence is an equality and may be used in "
                "either direction &mdash; and it is what lets the single `A` be shared "
                "between the two factors."
            ],
        },
        "quiz_title": "Identities",
        "quiz": [
            {"q": "`(A ∩ B)‾` equals:",
             "a": ["`Ā ∩ B̄`", "`Ā ∪ B̄`", "`A ∪ B`", "`A \\ B`"],
             "c": 1,
             "why": "De Morgan: the complement passes inward and the operation flips. "
                    "Not being in both means missing at least one."},
            {"q": "To prove `A = B` by double inclusion you must show:",
             "a": ["`A ⊆ B`", "`B ⊆ A`", "both", "`A ∩ B = A ∪ B`"],
             "c": 2,
             "why": "Each inclusion is half the claim. The last option is actually "
                    "equivalent to `A = B` as well, but it is not what double inclusion "
                    "means."},
            {"q": "A three-circle Venn diagram shows an identity holding. This:",
             "a": ["proves it for all sets",
                   "proves it for three sets, since all eight membership regions appear",
                   "proves nothing at all",
                   "proves it only for finite sets"],
             "c": 1,
             "why": "The eight regions are every possible membership pattern for three "
                    "sets, so a correctly shaded diagram is a case check. It does not "
                    "extend to more sets, where no such picture exists."},
        ],
        "mistakes": [
            ("Distributing a complement across an operation without flipping it",
             "`(A ∪ B)‾` is `Ā ∩ B̄`, not `Ā ∪ B̄`. This is the same slip as the "
             "propositional one, and the lab separates the two in one click."),
            ("Treating a Venn diagram as a proof for arbitrarily many sets",
             "Three circles cover eight regions. Four circles do not cover all sixteen, "
             "so the usual four-set picture is not a case check at all."),
            ("Using a step you cannot name",
             "Every line of a chain proof should cite a law. \"Rearranging\" is where "
             "errors hide, and the fix is to write which law licenses the rearrangement."),
        ],
        "standard": ("Finish when you can prove an identity both ways.",
                     "Prove `(A \\ B) ∪ (B \\ A) = (A ∪ B) \\ (A ∩ B)` &mdash; both sides "
                     "are `A △ B` &mdash; once by double inclusion and once by chaining "
                     "laws. The second will be shorter; the first will be the one you can "
                     "always produce."),
        "note": "Sets under `∪`, `∩` and complement form a Boolean algebra, exactly as "
                "propositions under `∨`, `∧` and `¬` do. That is why the two lists of "
                "laws match line for line, and why course 1 lesson 7's remarks about "
                "circuits apply here too.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "cartesian-products-and-tuples",
        "title": "Cartesian Products and Tuples",
        "module": "Sets",
        "one_line": "Ordered pairs, and the set of all of them.",
        "summary": (
            "A tuple has order and allows repetition, which a set does not. The "
            "Cartesian product collects every ordered pair, has size `|A| · |B|`, and "
            "is where relations and functions will live."
        ),
        "key": [
            "(a, b) = (c, d)   ⟺   a = c  and  b = d      order matters",
            "A × B = {(a, b) : a ∈ A, b ∈ B}",
            "|A × B| = |A| · |B|",
            "A × B ≠ B × A     in general",
        ],
        "key_label": "Ordered, unlike a set",
        "concepts_intro": (
            "Sets forget order. Tuples remember it, and everything from relations to "
            "graphs needs that memory."
        ),
        "concepts": [
            ("Tuples are ordered and sets are not",
             "`(1, 2) ≠ (2, 1)` while `{1, 2} = {2, 1}`. Tuples also allow repetition: "
             "`(1, 1)` is a perfectly good pair."),
            ("The product multiplies sizes",
             "`|A × B| = |A| · |B|`, because each of `|A|` first coordinates can be paired "
             "with each of `|B|` second ones. This is course 4's product rule."),
            ("The product is not commutative",
             "`A × B` and `B × A` contain different pairs unless `A = B` or one is empty. "
             "There is a natural bijection between them, which is a weaker statement."),
        ],
        "read_title": "Products and tuples",
        "read_intro": "The definitions, the size formula, and where products get used.",
        "body": [
            ("def", ("Ordered pair",
                     "An <strong>ordered pair</strong> `(a, b)` satisfies "
                     "`(a, b) = (c, d)` exactly when `a = c` and `b = d`. More generally "
                     "an <strong>n-tuple</strong> `(a₁, …, aₙ)` is equal to another "
                     "exactly when they agree coordinate by coordinate.")),
            ("def", ("Cartesian product",
                     "`A × B = {(a, b) : a ∈ A and b ∈ B}`. The `n`-fold product "
                     "`A₁ × ⋯ × Aₙ` is the set of `n`-tuples with `aᵢ ∈ Aᵢ`, and `Aⁿ` "
                     "abbreviates `A × ⋯ × A` with `n` factors.")),
            ("thm", ("The size of a product",
                     "For finite sets, `|A × B| = |A| · |B|`, and `|A₁ × ⋯ × Aₙ|` is the "
                     "product of the sizes.")),
            ("proof", [
                "Each pair is formed by choosing a first coordinate (`|A|` ways) and then "
                "a second (`|B|` ways, independently of the first). Distinct choices give "
                "distinct pairs, by the definition of pair equality, and every pair arises "
                "this way. So the count is `|A| · |B|`.",
            ]),
            ("p", "If either factor is empty the product is empty: there is no pair to "
                  "form. `A × ∅ = ∅` for every `A`, which the size formula also predicts."),
            ("example", ("A small product",
                         "`{1, 2} × {a, b, c}` has `2 · 3 = 6` elements: `(1,a)`, `(1,b)`, "
                         "`(1,c)`, `(2,a)`, `(2,b)`, `(2,c)`. Note `{a,b,c} × {1,2}` "
                         "contains `(a,1)`, a different object from `(1,a)`.")),
            ("h3", "Where products are used"),
            ("ul", [
                "<strong>Relations</strong> (lesson 6) are subsets of `A × B`. \"`x` is "
                "less than `y`\" is the set of pairs where that holds.",
                "<strong>Functions</strong> (lesson 10) are relations with an extra "
                "condition, so they too are sets of pairs.",
                "<strong>The plane</strong> is `ℝ × ℝ`, written `ℝ²`. Coordinate geometry "
                "is the observation that points are ordered pairs.",
                "<strong>Bit strings</strong> of length `n` are elements of `{0, 1}ⁿ`, "
                "and there are `2ⁿ` of them &mdash; the same count as the subsets of an "
                "`n`-element set, for the same reason.",
            ]),
            ("p", "That last coincidence is worth pausing on. A subset of an `n`-element "
                  "set is exactly a choice of in-or-out for each element, which is exactly "
                  "a bit string of length `n`. The bijection between `P(A)` and `{0,1}ⁿ` "
                  "is why both are counted by `2ⁿ`, and it is a preview of lesson 12's "
                  "argument style."),
            ("def", ("Cardinality of a product of a set with itself",
                     "`|Aⁿ| = |A|ⁿ`. With `|A| = 2` this gives `2ⁿ`; with `|A| = 26` and "
                     "`n = 4` it gives the number of four-letter strings, 456 976.")),
        ],
        "lab": ("counting", {
            "n": 3, "r": 2, "rule": "pr",
            "panel_title": "Ordered with repetition is a product",
            "panel_intro": "The first row, `nʳ`, counts exactly the elements of `Aʳ` "
                           "when `|A| = n`. The enumeration below lists them, which is "
                           "the product written out.",
        }),
        "steps_title": "Working with products",
        "steps_intro": "Coordinates first, then count.",
        "steps": [
            ("Fix which set supplies which coordinate",
             "`A × B` takes its first coordinate from `A`. Reversing this silently "
             "produces a different set."),
            ("Count by multiplying",
             "`|A × B × C| = |A| · |B| · |C|`. Independent choices multiply; this is the "
             "product rule course 4 states in general."),
            ("Enumerate systematically when listing",
             "Vary the last coordinate fastest, exactly as truth table rows do. The "
             "pattern makes a missing tuple visible."),
            ("Remember that a subset of a product is a relation",
             "This is the whole content of lesson 6: any set of pairs is a relation, and "
             "any relation is a set of pairs."),
        ],
        "worked": {
            "title": "Counting with a product",
            "intro": ["How many strings of length 4 use letters from `{a, b, c}`?"],
            "lines": [
                "A string of length 4 is an element of {a,b,c}⁴.",
                "",
                "|{a,b,c}⁴| = 3⁴ = 81",
                "",
                "How many use no repeated letter?",
                "   first  3 choices",
                "   second 2 choices (one used)",
                "   third  1 choice",
                "   fourth 0 choices          ⟹  0 such strings",
                "",
                "Length 4 from a 3-letter alphabet must repeat: pigeonhole (lesson 14).",
            ],
            "after": [
                "The second count is the pigeonhole principle arriving early, and by "
                "arithmetic rather than by argument: four positions, three letters, so "
                "some letter is used twice. Lesson 14 states it in general."
            ],
        },
        "quiz_title": "Products",
        "quiz": [
            {"q": "`|A| = 4` and `|B| = 3`. What is `|A × B|`?",
             "a": ["7", "12", "64", "81"],
             "c": 1,
             "why": "`4 · 3 = 12`. Each first coordinate pairs with each second, "
                    "independently."},
            {"q": "Which is true?",
             "a": ["`(1, 2) = (2, 1)`", "`{1, 2} ≠ {2, 1}`",
                   "`A × B = B × A` always", "`(1, 1)` is a legitimate ordered pair"],
             "c": 3,
             "why": "Tuples allow repeated coordinates; only sets discard duplicates. "
                    "The first three are all false."},
            {"q": "How many bit strings of length 8 are there?",
             "a": ["16", "64", "256", "512"],
             "c": 2,
             "why": "`|{0,1}⁸| = 2⁸ = 256`. Same count as the subsets of an eight-element "
                    "set, and for the same reason."},
        ],
        "mistakes": [
            ("Treating `A × B` and `B × A` as the same set",
             "They contain different objects. There is a natural bijection between them, "
             "which is a statement about size, not about equality."),
            ("Adding sizes instead of multiplying",
             "`|A × B|` is a product because the choices are made together, not "
             "alternatively. Course 4 lesson 1 draws the line between the two rules."),
            ("Writing `{a, b}` when order matters",
             "If swapping the entries changes the meaning, you need a tuple. Using a set "
             "throws away exactly the information you were relying on."),
        ],
        "standard": ("Finish when you can say why `2ⁿ` counts both subsets and bit strings.",
                     "Describe the bijection explicitly: given a subset, produce its bit "
                     "string; given a bit string, produce its subset. That construction "
                     "is the pattern lesson 12 formalises and course 4 uses constantly."),
        "note": "Formally an ordered pair can be defined purely in terms of sets, as "
                "`(a, b) = {{a}, {a, b}}` &mdash; Kuratowski's definition &mdash; which "
                "does satisfy the equality property. Nothing on this path needs it; it is "
                "worth knowing that order is not an extra primitive.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "binary-relations",
        "title": "Binary Relations",
        "module": "Relations",
        "one_line": "A relation is a set of ordered pairs, and nothing more.",
        "summary": (
            "Any subset of `A × B` is a relation. Three ways to present one &mdash; as "
            "pairs, as a matrix, as a directed graph &mdash; and the operations of "
            "inverse and composition."
        ),
        "key": [
            "R ⊆ A × B         a relation FROM A TO B",
            "a R b             means (a, b) ∈ R",
            "R⁻¹ = {(b, a) : (a, b) ∈ R}          the inverse",
            "S ∘ R = {(a, c) : ∃b. aRb and bSc}   composition",
        ],
        "key_label": "Pairs, and what you can do with them",
        "concepts_intro": (
            "The definition is deliberately weak: any set of pairs qualifies. The "
            "interesting relations are the ones with extra properties, from lesson 7 on."
        ),
        "concepts": [
            ("A relation is just a set of pairs",
             "No condition at all. `{(1,1), (2,5)}` is a relation on `{1,2,5}`, and so is "
             "the empty set."),
            ("Three presentations, one object",
             "The pair list, the boolean matrix and the directed graph carry identical "
             "information. Each makes different properties obvious."),
            ("Composition is not commutative",
             "`S ∘ R` follows `R` then `S`. Reversing the order generally gives a "
             "different relation, and often an empty one."),
        ],
        "read_title": "Relations and their presentations",
        "read_intro": "The definition, three ways to draw it, and two operations.",
        "body": [
            ("def", ("Binary relation",
                     "A <strong>relation from `A` to `B`</strong> is a subset "
                     "`R ⊆ A × B`. A <strong>relation on `A`</strong> is a subset of "
                     "`A × A`. We write `a R b` for `(a, b) ∈ R`.")),
            ("p", "The definition permits everything. `∅` is a relation (nothing is "
                  "related), and `A × A` is a relation (everything is related to "
                  "everything). Between those extremes there are `2^(n²)` relations on an "
                  "`n`-element set &mdash; 512 on a three-element set, and over half a "
                  "billion on a five-element one."),
            ("h3", "Three presentations"),
            ("ul", [
                "<strong>As pairs.</strong> `R = {(1,2), (2,3), (3,1)}`. Complete and "
                "unreadable beyond a handful.",
                "<strong>As a matrix.</strong> An `n × n` grid with a 1 in row `a`, "
                "column `b` when `a R b`. Reflexivity is the diagonal, symmetry is "
                "the matrix equalling its transpose.",
                "<strong>As a directed graph.</strong> A dot per element, an arrow from "
                "`a` to `b` when `a R b`. Transitivity becomes \"every two-step path has "
                "a one-step shortcut\", which is the reading course 7 uses.",
            ]),
            ("p", "The matrix is what the lab shows, because the four properties of "
                  "lesson 7 are all visible in it: the diagonal, the transpose, and the "
                  "presence of both `(a,b)` and `(b,a)` for distinct `a`, `b`."),
            ("def", ("Inverse relation",
                     "`R⁻¹ = {(b, a) : (a, b) ∈ R}` &mdash; every pair reversed. As a "
                     "matrix this is the transpose.")),
            ("def", ("Composition",
                     "For `R ⊆ A × B` and `S ⊆ B × C`, "
                     "`S ∘ R = {(a, c) : ∃b ∈ B with (a,b) ∈ R and (b,c) ∈ S}`. Read right "
                     "to left: apply `R` first, then `S`.")),
            ("p", "The right-to-left order is chosen to match function composition, where "
                  "`(g ∘ f)(x) = g(f(x))`. It is a convention and some texts reverse it; "
                  "what matters is being consistent and saying which you mean."),
            ("example", ("Composing two relations",
                         "On `{1,2,3}`, let `R = {(1,2), (2,3)}` and `S = {(2,1), (3,3)}`. "
                         "Then `S ∘ R = {(1,1), (2,3)}`: from 1, `R` reaches 2 and `S` "
                         "takes 2 to 1; from 2, `R` reaches 3 and `S` takes 3 to 3. "
                         "Meanwhile `R ∘ S = {(2,2)}` &mdash; a different relation.")),
            ("thm", ("Composition and matrices",
                     "If `M_R` and `M_S` are the boolean matrices of `R` and `S`, then "
                     "the matrix of `S ∘ R` is the boolean product `M_R M_S`, where "
                     "multiplication is `∧` and addition is `∨`.")),
            ("p", "That is the same computation as counting walks of length 2 in course 7 "
                  "lesson 3, with `∨` in place of `+`. Composition of relations and paths "
                  "in a directed graph are the same idea."),
        ],
        "lab": ("relation", {
            "size": 5, "preset": "succ",
            "panel_title": "A relation as a matrix",
            "panel_intro": "Every cell is one pair. The presets give relations you know "
                           "by name; clicking cells gives you ones nobody named, which is "
                           "where the properties of lesson 7 get interesting.",
        }),
        "steps_title": "Reading a relation",
        "steps_intro": "Choose the presentation that makes your question easy.",
        "steps": [
            ("Write it as pairs when it is small",
             "Nothing is clearer than the list for four or five pairs, and the list is "
             "what the definition actually is."),
            ("Use the matrix to check properties",
             "Reflexive is a full diagonal; symmetric is equal to its transpose. Both are "
             "one glance in matrix form and tedious in list form."),
            ("Use the digraph to trace paths",
             "Transitivity and the transitive closure are statements about paths, and "
             "arrows make paths visible."),
            ("Compose right to left",
             "`S ∘ R` means `R` first. Pick each `a`, follow `R` to every `b`, then `S` "
             "to every `c`, and collect the pairs `(a, c)`."),
        ],
        "worked": {
            "title": "Composing with itself",
            "intro": ["On `{1,2,3,4}`, let `R = {(1,2), (2,3), (3,4)}` &mdash; the successor relation."],
            "lines": [
                "R ∘ R  (two steps):",
                "   1 → 2 → 3      gives (1, 3)",
                "   2 → 3 → 4      gives (2, 4)",
                "   3 → 4 → ?      4 has no outgoing pair — nothing",
                "R ∘ R = {(1,3), (2,4)}",
                "",
                "R ∘ R ∘ R  (three steps):  {(1,4)}",
                "R⁴ = ∅       no path of length 4 exists in a 4-element chain",
                "",
                "R ∪ R² ∪ R³ = {(1,2),(2,3),(3,4),(1,3),(2,4),(1,4)}  =  the",
                "relation \"a < b\", which is the transitive closure of R.",
            ],
            "after": [
                "The last line is lesson 7's transitive closure computed by hand: the "
                "union of all powers of `R` is exactly the pairs joined by a path of any "
                "length. Warshall's algorithm in the lab does this without enumerating "
                "the powers."
            ],
        },
        "quiz_title": "Relations",
        "quiz": [
            {"q": "How many relations are there on a set with 3 elements?",
             "a": ["9", "27", "512", "6"],
             "c": 2,
             "why": "A relation is any subset of the 9 pairs in `A × A`, so there are "
                    "`2⁹ = 512` of them."},
            {"q": "`R = {(1,2)}` and `S = {(2,3)}`. What is `S ∘ R`?",
             "a": ["`{(1,3)}`", "`{(3,1)}`", "`∅`", "`{(1,2),(2,3)}`"],
             "c": 0,
             "why": "Apply `R` first: 1 goes to 2. Then `S`: 2 goes to 3. So `(1,3)` is "
                    "the only pair. `R ∘ S` would be empty."},
            {"q": "In the matrix of a relation, symmetry appears as:",
             "a": ["a full diagonal", "the matrix equalling its transpose",
                   "an empty diagonal", "every row summing to 1"],
             "c": 1,
             "why": "Symmetry says `(a,b) ∈ R` implies `(b,a) ∈ R`, which is exactly "
                    "`M = Mᵀ`. A full diagonal is reflexivity."},
        ],
        "mistakes": [
            ("Composing in the wrong order",
             "`S ∘ R` applies `R` first. Getting this backwards produces a different "
             "relation, usually a different size, and the error is silent."),
            ("Assuming a relation must be meaningful",
             "Any set of pairs qualifies. Most relations have no description shorter than "
             "their pair list, which is why properties rather than names are what matter."),
            ("Confusing `R⁻¹` with a complement",
             "The inverse reverses each pair; the complement takes the pairs not in `R`. "
             "They are unrelated operations."),
        ],
        "standard": ("Finish when you can move between all three presentations.",
                     "Take `R = {(1,1),(1,2),(2,3),(3,1)}` on `{1,2,3}`, write its matrix, "
                     "sketch its digraph, and compute `R ∘ R` in whichever presentation is "
                     "easiest. Then check the answer in a second presentation."),
        "note": "Relations need not be on one set: `R ⊆ A × B` with `A ≠ B` is a "
                "<em>bipartite</em> relation, and lesson 10's functions are exactly the "
                "relations from `A` to `B` in which every element of `A` appears exactly "
                "once as a first coordinate.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "properties-of-relations",
        "title": "Properties of Relations",
        "module": "Relations",
        "one_line": "Reflexive, symmetric, antisymmetric, transitive — and closures.",
        "summary": (
            "Four properties, each a quantified sentence you can check. Then the three "
            "closures: the smallest relation containing yours that has the property you "
            "want."
        ),
        "key": [
            "reflexive       ∀a.  aRa",
            "symmetric       ∀a,b.  aRb → bRa",
            "antisymmetric   ∀a,b.  aRb ∧ bRa → a = b",
            "transitive      ∀a,b,c.  aRb ∧ bRc → aRc",
        ],
        "key_label": "Four definitions to check, not recall",
        "concepts_intro": (
            "Each property is a sentence from course 1. Deciding whether it holds is "
            "evaluating that sentence, and refuting it is naming one bad pair."
        ),
        "concepts": [
            ("Antisymmetric is not \"not symmetric\"",
             "It says distinct elements never relate both ways. Equality is both "
             "symmetric and antisymmetric; many relations are neither."),
            ("Transitivity is about two-step paths",
             "Every path of length two must have a one-step shortcut. In the matrix that "
             "is a condition on the boolean square."),
            ("A closure adds the least it can",
             "The transitive closure of `R` is the smallest transitive relation "
             "containing `R` &mdash; not any transitive relation containing it."),
        ],
        "read_title": "The four properties and the three closures",
        "read_intro": "Definitions, the pairs that decide them, and how to repair a relation.",
        "body": [
            ("def", ("The four properties",
                     "`R` on `A` is <strong>reflexive</strong> if `∀a ∈ A. (a,a) ∈ R`; "
                     "<strong>symmetric</strong> if `∀a,b. (a,b) ∈ R → (b,a) ∈ R`; "
                     "<strong>antisymmetric</strong> if `∀a,b. (a,b) ∈ R ∧ (b,a) ∈ R → a = b`; "
                     "<strong>transitive</strong> if `∀a,b,c. (a,b) ∈ R ∧ (b,c) ∈ R → (a,c) ∈ R`.")),
            ("p", "Two remarks that prevent most of the confusion in this lesson. "
                  "<strong>Antisymmetric is not the negation of symmetric.</strong> The "
                  "equality relation is both. The relation `{(1,2), (2,1), (1,3)}` is "
                  "neither. And <strong>irreflexive is not the negation of reflexive</strong> "
                  "either: a relation with some but not all loops is neither reflexive "
                  "nor irreflexive."),
            ("p", "Each property is refuted by naming a specific witness, and a check that "
                  "does not produce one has not really been done. The lab reports the "
                  "witness on every failure for exactly this reason."),
            ("example", ("Familiar relations, classified",
                         "`=` on `ℤ`: reflexive, symmetric, antisymmetric, transitive. "
                         "`≤`: reflexive, antisymmetric, transitive, not symmetric. "
                         "`&lt;`: transitive and antisymmetric, not reflexive. "
                         "\"divides\" on positive integers: reflexive, antisymmetric, "
                         "transitive. \"`a − b` is even\": reflexive, symmetric, "
                         "transitive &mdash; and not antisymmetric.")),
            ("h3", "Closures"),
            ("def", ("Closure",
                     "The <strong>closure</strong> of `R` with respect to a property is "
                     "the smallest relation containing `R` that has the property, when one "
                     "exists.")),
            ("math", [
                "reflexive closure    R ∪ {(a,a) : a ∈ A}          add the diagonal",
                "symmetric closure    R ∪ R⁻¹                       add every reverse",
                "transitive closure   R ∪ R² ∪ R³ ∪ …               add every path",
            ]),
            ("p", "The transitive closure is the interesting one. Its pairs are exactly "
                  "the `(a, b)` joined by a path of one or more steps, so on an "
                  "`n`-element set the union stops at `Rⁿ` &mdash; a longer path repeats "
                  "a vertex and can be shortened. Computing it by taking powers is "
                  "wasteful; Warshall's algorithm does it in `n³` steps, and is what the "
                  "lab runs."),
            ("thm", ("Warshall's algorithm",
                     "For `k = 1` to `n`, and for every `a, b`: if `a` reaches `k` and `k` "
                     "reaches `b` in the relation built so far, add `(a, b)`. After the "
                     "outer loop finishes, the relation is the transitive closure.")),
            ("proof", [
                "The invariant is that after stage `k`, the relation contains `(a, b)` "
                "exactly when a path from `a` to `b` exists using only `1 … k` as "
                "intermediate points. Stage `k+1` adds the paths that route through "
                "`k+1`, which is the only new possibility.",
                "After stage `n` every intermediate point is permitted, so every path is "
                "represented &mdash; which is the transitive closure.",
            ]),
            ("p", "There is no such thing as an \"antisymmetric closure\": adding pairs "
                  "can never remove a violation, since the offending pair `(a,b)` and "
                  "`(b,a)` are already both present. A closure exists only for properties "
                  "that adding pairs can establish."),
        ],
        "lab": ("relation", {
            "size": 5, "preset": "lt",
            "panel_title": "Check properties, then close",
            "panel_intro": "Every verdict names the pair that decides it. The closure "
                           "selector marks in amber the pairs a closure would add "
                           "&mdash; the least it can add, not any repair that works.",
        }),
        "steps_title": "Deciding a property",
        "steps_intro": "Evaluate the sentence; produce the witness either way.",
        "steps": [
            ("Reflexive: check the diagonal",
             "Every `(a, a)` must be present, for every element of the set, not just the "
             "ones that appear in some pair."),
            ("Symmetric: check each pair's reverse",
             "For each `(a,b)` in `R`, is `(b,a)` there? One missing reverse settles it."),
            ("Antisymmetric: look for two-way pairs between distinct elements",
             "Both `(a,b)` and `(b,a)` with `a ≠ b` refutes it. Loops `(a,a)` never do."),
            ("Transitive: check every two-step path",
             "For each `(a,b)` and `(b,c)`, is `(a,c)` present? This is the expensive "
             "check, and the one people skip."),
        ],
        "worked": {
            "title": "Classifying \"divides\" on `{1, 2, 3, 4, 6}`",
            "intro": ["`a R b` when `a` divides `b`."],
            "lines": [
                "reflexive?      a | a always            YES",
                "symmetric?      2 | 4 but 4 ∤ 2         NO",
                "antisymmetric?  a | b and b | a with a, b positive ⟹ a = b   YES",
                "transitive?     a | b and b | c ⟹ a | c                       YES",
                "",
                "reflexive + antisymmetric + transitive  ⟹  a PARTIAL ORDER",
                "",
                "It is only PARTIAL: 2 and 3 are incomparable — neither divides",
                "the other — so not every pair of elements is ranked.",
            ],
            "after": [
                "The antisymmetry argument uses positivity. Over all integers it fails: "
                "`2 | −2` and `−2 | 2` with `2 ≠ −2`. A property of a relation depends on "
                "the set it is defined over, and dropping that qualification changes the "
                "answer."
            ],
        },
        "quiz_title": "Properties",
        "quiz": [
            {"q": "Which relation on `ℤ` is symmetric but not transitive?",
             "a": ["`=`", "`≤`", "`|a − b| ≤ 1`", "`a` divides `b`"],
             "c": 2,
             "why": "`|1−2| ≤ 1` and `|2−3| ≤ 1` but `|1−3| = 2`, so transitivity fails. "
                    "Symmetry is clear since `|a−b| = |b−a|`."},
            {"q": "A relation is antisymmetric. Can it also be symmetric?",
             "a": ["No, they are opposites",
                   "Yes, if it contains no pair `(a,b)` with `a ≠ b`",
                   "Only if it is empty",
                   "Only if it is reflexive"],
             "c": 1,
             "why": "Equality is both. Any relation contained in the diagonal satisfies "
                    "both conditions vacuously for distinct elements."},
            {"q": "The transitive closure of `R` on an `n`-element set equals:",
             "a": ["`R²`", "`R ∪ R²`", "`R ∪ R² ∪ … ∪ Rⁿ`", "`R × R`"],
             "c": 2,
             "why": "Pairs joined by a path of any length, and no path needs more than "
                    "`n` steps: a longer one repeats a vertex and can be shortened."},
        ],
        "mistakes": [
            ("Reading antisymmetric as \"not symmetric\"",
             "They are independent. Equality is both; `{(1,2),(2,1),(1,3)}` is neither. "
             "The definition is about distinct elements relating both ways."),
            ("Checking reflexivity only on elements that appear in pairs",
             "Every element of the underlying set needs its loop. An element in no pair "
             "at all is exactly what breaks reflexivity."),
            ("Stopping the transitivity check early",
             "Every two-step path must be checked, including the ones through loops. "
             "A single missed triple is a wrong verdict."),
        ],
        "standard": ("Finish when you can name the witness for every verdict.",
                     "For each of `=`, `≤`, `&lt;`, `⊆` and \"has the same remainder mod "
                     "3\", state which of the four properties hold, and for each failure "
                     "give the specific pair or triple. Naming the witness is the check; "
                     "everything else is recall."),
        "note": "Transitivity is expensive to verify: `n³` triples in the worst case, "
                "against `n` for reflexivity and `n²` for symmetry. That asymmetry is why "
                "transitive closure has an algorithm with a name and the other two do not.",
    },
]
