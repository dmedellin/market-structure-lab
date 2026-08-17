"""Course 2, lessons 08-14 — equivalence, order, functions, cardinality."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "equivalence-relations-and-partitions",
        "title": "Equivalence Relations and Partitions",
        "module": "Relations",
        "one_line": "Reflexive, symmetric, transitive — and the partition that comes free.",
        "summary": (
            "An equivalence relation is one that behaves like equality in the respects "
            "that matter. Every one of them cuts its set into disjoint classes, and "
            "every such cutting comes from exactly one equivalence relation."
        ),
        "key": [
            "equivalence  =  reflexive + symmetric + transitive",
            "[a] = {x : x R a}                the class of a",
            "a R b  ⟺  [a] = [b]              classes are equal or disjoint",
            "equivalence relations on A  ⟷  partitions of A     (a bijection)",
        ],
        "key_label": "One structure, two descriptions",
        "concepts_intro": (
            "This is the first theorem on the path that says two apparently different "
            "things are the same thing."
        ),
        "concepts": [
            ("Equivalence generalises equality",
             "It is the relation of \"the same in some respect\": same remainder, same "
             "shape, same parity. It keeps equality's three structural properties and "
             "drops the demand that the objects be identical."),
            ("Classes partition the set",
             "Every element lies in exactly one class. Two classes are either identical "
             "or share nothing &mdash; there is no partial overlap."),
            ("The correspondence goes both ways",
             "Every equivalence relation gives a partition; every partition gives an "
             "equivalence relation; and the two constructions undo each other."),
        ],
        "read_title": "Classes and partitions",
        "read_intro": "The definition, the theorem, and the proof that the classes fit together.",
        "body": [
            ("def", ("Equivalence relation",
                     "A relation `R` on `A` is an <strong>equivalence relation</strong> "
                     "when it is reflexive, symmetric and transitive. It is often written "
                     "`∼`.")),
            ("def", ("Equivalence class",
                     "For `a ∈ A`, the <strong>class</strong> of `a` is "
                     "`[a] = {x ∈ A : x ∼ a}`. Any member of a class is called a "
                     "<strong>representative</strong> of it.")),
            ("def", ("Partition",
                     "A <strong>partition</strong> of `A` is a collection of nonempty, "
                     "pairwise disjoint subsets whose union is `A`. Every element of `A` "
                     "lies in exactly one block.")),
            ("thm", ("Classes are equal or disjoint",
                     "For an equivalence relation on `A` and any `a, b ∈ A`: "
                     "`a ∼ b` if and only if `[a] = [b]`; and if `a ≁ b` then "
                     "`[a] ∩ [b] = ∅`.")),
            ("proof", [
                "Suppose `a ∼ b` and let `x ∈ [a]`, so `x ∼ a`. By transitivity `x ∼ b`, "
                "so `x ∈ [b]`; hence `[a] ⊆ [b]`. Symmetry of `∼` gives `b ∼ a`, and the "
                "same argument gives `[b] ⊆ [a]`. So `[a] = [b]`.",
                "Conversely if `[a] = [b]` then, since `a ∈ [a]` by reflexivity, "
                "`a ∈ [b]`, which means `a ∼ b`.",
                "Finally suppose `x ∈ [a] ∩ [b]`, so `x ∼ a` and `x ∼ b`. By symmetry and "
                "transitivity `a ∼ b`, so by the first part `[a] = [b]`. Contrapositively, "
                "`[a] ≠ [b]` forces the intersection to be empty.",
            ]),
            ("p", "All three properties were needed, and each did a distinct job: "
                  "reflexivity puts `a` into its own class, symmetry lets the argument run "
                  "in both directions, and transitivity is what links two members of the "
                  "same class to each other."),
            ("thm", ("The fundamental correspondence",
                     "The equivalence relations on `A` and the partitions of `A` are in "
                     "bijection. An equivalence relation gives the partition into its "
                     "classes; a partition gives the relation \"lies in the same block\"; "
                     "and each construction undoes the other.")),
            ("example", ("Congruence modulo 3",
                         "On `ℤ`, define `a ∼ b` when `3 | (a − b)`. It is reflexive "
                         "(`3 | 0`), symmetric (`3 | (a−b)` gives `3 | (b−a)`) and "
                         "transitive (`3 | (a−b)` and `3 | (b−c)` give `3 | (a−c)`). The "
                         "three classes are the integers leaving remainder 0, 1 and 2. "
                         "Course 6 builds on nothing else.")),
            ("p", "The utility is that a class can be treated as one object. Arithmetic "
                  "modulo 3 works because `+` and `×` respect the classes: adding any "
                  "member of `[1]` to any member of `[2]` always lands in `[0]`. That "
                  "compatibility is not automatic and is exactly what makes modular "
                  "arithmetic well defined."),
            ("example", ("A relation that just misses",
                         "\"`|a − b| ≤ 1`\" on `ℤ` is reflexive and symmetric but not "
                         "transitive: `1 ∼ 2` and `2 ∼ 3` but `1 ≁ 3`. So it produces no "
                         "partition &mdash; and indeed the \"classes\" `[1] = {0,1,2}` and "
                         "`[2] = {1,2,3}` overlap without being equal, which is exactly "
                         "what the theorem forbids.")),
        ],
        "lab": ("relation", {
            "size": 5, "preset": "mod2",
            "panel_title": "Build an equivalence relation",
            "panel_intro": "When the three properties all hold, the lab lists the classes. "
                           "Break any one of them by clicking a cell and watch the classes "
                           "stop being reported &mdash; because they stop existing.",
        }),
        "steps_title": "Working with an equivalence relation",
        "steps_intro": "Verify all three properties, then find the classes.",
        "steps": [
            ("Check reflexivity, symmetry and transitivity",
             "All three, with witnesses. Missing one means there are no classes to find, "
             "and any \"classes\" you write down will overlap."),
            ("Find the class of one element",
             "Collect everything related to it. That set is a block of the partition."),
            ("Move to an element not yet placed",
             "Its class is a new block, disjoint from the ones found. Repeat until every "
             "element is placed."),
            ("Check the blocks partition the set",
             "Nonempty, pairwise disjoint, covering everything. If two overlap, one of "
             "the three properties failed."),
        ],
        "worked": {
            "title": "The classes of congruence mod 4",
            "intro": ["On `ℤ`, `a ∼ b` when `4 | (a − b)`."],
            "lines": [
                "[0] = {…, −8, −4, 0, 4, 8, …}      remainder 0",
                "[1] = {…, −7, −3, 1, 5, 9, …}      remainder 1",
                "[2] = {…, −6, −2, 2, 6, 10, …}     remainder 2",
                "[3] = {…, −5, −1, 3, 7, 11, …}     remainder 3",
                "",
                "[4] = [0]   — same class, different representative",
                "[−1] = [3]",
                "",
                "Four classes, pairwise disjoint, union ℤ.  This partition is",
                "written ℤ/4ℤ, and course 6 does arithmetic in it.",
            ],
            "after": [
                "`[4] = [0]` is the point at which representatives stop mattering. A class "
                "has many names and one identity, which is why a definition made through a "
                "representative has to be checked for independence of the choice &mdash; "
                "the well-definedness question course 6 raises for modular arithmetic."
            ],
        },
        "quiz_title": "Equivalence",
        "quiz": [
            {"q": "Which is NOT required for an equivalence relation?",
             "a": ["reflexive", "symmetric", "antisymmetric", "transitive"],
             "c": 2,
             "why": "Antisymmetry belongs to partial orders. An equivalence relation that "
                    "is also antisymmetric is just equality."},
            {"q": "`[a] ∩ [b] ≠ ∅`. What follows?",
             "a": ["`a` and `b` are equal", "`[a] = [b]`",
                   "nothing", "`a ∼ b` is false"],
             "c": 1,
             "why": "Classes are equal or disjoint. A shared element forces equality of "
                    "the classes, though not of `a` and `b` themselves."},
            {"q": "How many equivalence relations are there on a 3-element set?",
             "a": ["3", "5", "8", "512"],
             "c": 1,
             "why": "One per partition: all separate, three ways to pair two together, "
                    "and all in one block &mdash; five in total. This count is the Bell "
                    "number `B₃`."},
        ],
        "mistakes": [
            ("Calling a relation an equivalence after checking two properties",
             "\"`|a − b| ≤ 1`\" is reflexive and symmetric and produces overlapping "
             "classes. Transitivity is the property that makes the classes fit together."),
            ("Treating a class as its representative",
             "`[4]` and `[0]` are the same object modulo 4. A definition that gives "
             "different answers for different representatives is not well defined."),
            ("Forgetting that blocks must be nonempty",
             "A partition has no empty block. It is a small condition and it is what makes "
             "the correspondence with equivalence relations exact."),
        ],
        "standard": ("Finish when you can go from a partition to its relation and back.",
                     "Take the partition `{{1,4}, {2}, {3,5}}` of `{1,…,5}`, write the "
                     "relation it induces as a set of pairs, and verify all three "
                     "properties. Then read the classes back off the relation."),
        "note": "The number of partitions of an `n`-element set is the Bell number `Bₙ`: "
                "1, 1, 2, 5, 15, 52, 203. It grows faster than exponentially and has no "
                "simple closed form, which is a first sign that counting problems can be "
                "hard in ways course 4 makes precise.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "partial-orders",
        "title": "Partial Orders",
        "module": "Relations",
        "one_line": "Reflexive, antisymmetric, transitive — ranking rather than grouping.",
        "summary": (
            "Swap symmetry for antisymmetry and the structure changes completely: "
            "instead of grouping elements into classes, the relation ranks them. Some "
            "pairs stay incomparable, which is what makes it partial."
        ),
        "key": [
            "partial order  =  reflexive + antisymmetric + transitive",
            "a and b incomparable  ⟺  neither a ≼ b nor b ≼ a",
            "total order  =  partial order with no incomparable pairs",
            "Hasse diagram: drop loops, drop implied edges, point upward",
        ],
        "key_label": "The other structure a relation can carry",
        "concepts_intro": (
            "Equivalence and order are the two structures a relation commonly has, and "
            "they differ in exactly one of the four properties."
        ),
        "concepts": [
            ("Antisymmetry is what makes it an order",
             "Distinct elements never relate both ways, so the relation cannot fold "
             "elements together. It separates rather than groups."),
            ("Partial means some pairs are incomparable",
             "Under `⊆`, the sets `{1}` and `{2}` are incomparable. That is not a defect: "
             "most natural orders have incomparable pairs."),
            ("A Hasse diagram removes the redundancy",
             "Loops are implied by reflexivity and long edges by transitivity, so both "
             "are omitted. What remains is the covering relation."),
        ],
        "read_title": "Orders, comparability and diagrams",
        "read_intro": "The definition, the special elements, and how to draw one.",
        "body": [
            ("def", ("Partial order",
                     "A relation `≼` on `A` is a <strong>partial order</strong> when it is "
                     "reflexive, antisymmetric and transitive. The pair `(A, ≼)` is a "
                     "<strong>poset</strong>.")),
            ("def", ("Comparable, total order",
                     "`a` and `b` are <strong>comparable</strong> when `a ≼ b` or `b ≼ a`. "
                     "A partial order in which every two elements are comparable is a "
                     "<strong>total</strong> (or linear) order.")),
            ("example", ("Four posets",
                         "`(ℤ, ≤)` is total. `(P(S), ⊆)` is partial: `{1}` and `{2}` are "
                         "incomparable. Divisibility on the positive integers is partial: "
                         "2 and 3 are incomparable. Alphabetical order on words is total.")),
            ("h3", "Hasse diagrams"),
            ("p", "Drawing every pair of a partial order is unreadable, and most of the "
                  "pairs are forced. A <strong>Hasse diagram</strong> draws only what is "
                  "not: place `b` above `a` when `a ≺ b`, and draw an edge only when `b` "
                  "<strong>covers</strong> `a` &mdash; that is, `a ≺ b` with nothing "
                  "strictly between."),
            ("ul", [
                "<strong>No loops.</strong> Reflexivity is assumed, so `(a,a)` is never drawn.",
                "<strong>No arrowheads.</strong> Height encodes direction: higher is later.",
                "<strong>No implied edges.</strong> If `a ≺ b ≺ c`, the edge `a` to `c` "
                "is forced by transitivity and is omitted.",
            ]),
            ("p", "The full order is recovered from the diagram by taking the reflexive "
                  "transitive closure of what is drawn: `a ≼ b` exactly when an upward "
                  "path leads from `a` to `b`. The diagram is a compressed encoding, not "
                  "a different relation."),
            ("def", ("Extremal elements",
                     "`a` is <strong>minimal</strong> if nothing is strictly below it, and "
                     "<strong>maximal</strong> if nothing is strictly above. `a` is the "
                     "<strong>least</strong> element if `a ≼ x` for every `x`, and the "
                     "<strong>greatest</strong> if `x ≼ a` for every `x`.")),
            ("p", "Minimal and least are different, and the difference is the whole "
                  "content of partiality. In `({2,3,4,6}, |)` both 2 and 3 are minimal "
                  "&mdash; nothing divides them within the set &mdash; and there is no "
                  "least element, because neither divides the other. A least element is "
                  "unique when it exists; minimal elements need not be."),
            ("thm", ("Uniqueness of least and greatest",
                     "A poset has at most one least element and at most one greatest.")),
            ("proof", [
                "Suppose `a` and `b` are both least. Then `a ≼ b` (since `a` is least) and "
                "`b ≼ a` (since `b` is least). Antisymmetry gives `a = b`. The greatest "
                "case is identical with the inequalities reversed.",
            ]),
            ("p", "That proof is where antisymmetry earns its place. Without it, two "
                  "distinct elements could each precede the other and both count as least, "
                  "and the notion would be useless."),
            ("def", ("Topological sort",
                     "A <strong>topological sort</strong> of a finite poset is a total "
                     "order extending it: a listing of the elements in which every element "
                     "appears after everything below it. Every finite poset has at least "
                     "one, and course 7 lesson 12 produces them from a directed graph.")),
        ],
        "lab": ("relation", {
            "size": 5, "preset": "div",
            "panel_title": "Divisibility is a partial order",
            "panel_intro": "The divisibility preset is reflexive, antisymmetric and "
                           "transitive, so the lab reports a partial order. Note that 2 "
                           "and 3 are incomparable &mdash; neither cell is on.",
        }),
        "steps_title": "Analysing a poset",
        "steps_intro": "Verify, then find the structure.",
        "steps": [
            ("Verify the three properties",
             "Reflexive, antisymmetric, transitive. Symmetry would collapse the order "
             "into an equivalence, so its absence is the point."),
            ("Find the incomparable pairs",
             "These are what make it partial. If there are none, it is a total order and "
             "much of the subtlety disappears."),
            ("Identify minimal and maximal elements",
             "Then ask separately whether a least or greatest exists. The two questions "
             "have different answers more often than not."),
            ("Draw the Hasse diagram",
             "Only covering relations, only upward. If you have drawn an edge implied by "
             "transitivity, remove it."),
        ],
        "worked": {
            "title": "Divisibility on `{1, 2, 3, 4, 6, 12}`",
            "intro": ["`a ≼ b` when `a` divides `b`."],
            "lines": [
                "Covering relations (nothing strictly between):",
                "   1 ≺ 2      1 ≺ 3      2 ≺ 4      2 ≺ 6      3 ≺ 6      4 ≺ 12   6 ≺ 12",
                "",
                "Hasse diagram, bottom to top:",
                "                 12",
                "                /  \\",
                "               4    6",
                "                \\  / \\",
                "                 2    3",
                "                  \\  /",
                "                   1",
                "",
                "least element:     1   (divides everything)",
                "greatest element: 12   (everything divides it)",
                "incomparable:     4 and 6,   3 and 4,   2 and 3",
            ],
            "after": [
                "The edge from 1 to 4 is absent although `1 | 4`: it is implied by "
                "`1 ≺ 2 ≺ 4`, so it is not a covering relation. Drawing it would be "
                "redundant, and a diagram that includes implied edges is not a Hasse "
                "diagram."
            ],
        },
        "quiz_title": "Orders",
        "quiz": [
            {"q": "Which property distinguishes a partial order from an equivalence relation?",
             "a": ["reflexivity", "transitivity",
                   "antisymmetry instead of symmetry", "totality"],
             "c": 2,
             "why": "Both are reflexive and transitive. The third property is symmetry for "
                    "an equivalence and antisymmetry for an order, and it changes the "
                    "structure completely."},
            {"q": "In `(P({1,2}), ⊆)`, are `{1}` and `{2}` comparable?",
             "a": ["Yes, `{1} ⊆ {2}`", "Yes, `{2} ⊆ {1}`",
                   "No, neither contains the other", "Only if they are equal"],
             "c": 2,
             "why": "Neither is a subset of the other, so they are incomparable &mdash; "
                    "which is exactly what makes `⊆` a partial rather than a total order."},
            {"q": "A poset has three minimal elements. How many least elements can it have?",
             "a": ["Three", "One", "Zero", "At most one, and here zero"],
             "c": 3,
             "why": "A least element is comparable to everything, so it would be the only "
                    "minimal element. With three minimal elements there can be no least "
                    "one, and in general there is at most one."},
        ],
        "mistakes": [
            ("Confusing minimal with least",
             "Minimal means nothing is below it; least means it is below everything. In a "
             "partial order these come apart, and that is the whole point of the word "
             "\"partial\"."),
            ("Drawing implied edges in a Hasse diagram",
             "If `a ≺ b ≺ c`, the edge from `a` to `c` is forced and must not be drawn. "
             "A diagram with it is just the relation, unreduced."),
            ("Assuming every poset is a total order",
             "Subset, divisibility and task dependency are all partial. Incomparable pairs "
             "are the normal case, not an anomaly."),
        ],
        "standard": ("Finish when you can draw the Hasse diagram of the subsets of a "
                     "three-element set.",
                     "Eight vertices in four levels, with edges only between sets differing "
                     "by one element. Then identify the least, the greatest, and a pair of "
                     "incomparable elements in the middle two levels."),
        "note": "Topological sorting is the practical face of this lesson: build "
                "dependencies, course prerequisites and spreadsheet recalculation all "
                "extend a partial order to a total one. Course 7 lesson 12 gives the "
                "algorithm, and it fails exactly when the dependencies contain a cycle "
                "&mdash; which is to say, when they were not a partial order at all.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "functions",
        "title": "Functions",
        "module": "Functions",
        "one_line": "A relation where every input has exactly one output.",
        "summary": (
            "A function is a relation from `A` to `B` in which every element of `A` "
            "appears exactly once as a first coordinate. Domain, codomain and image are "
            "three different sets, and confusing the last two causes most of the trouble."
        ),
        "key": [
            "f : A → B      every a ∈ A has EXACTLY ONE f(a) ∈ B",
            "domain    A        where inputs come from",
            "codomain  B        where outputs are DECLARED to live",
            "image     f(A) ⊆ B  where outputs ACTUALLY live",
        ],
        "key_label": "Three sets, not two",
        "concepts_intro": (
            "Two conditions define a function: every input is used, and none is used "
            "twice. Everything else is vocabulary."
        ),
        "concepts": [
            ("Totality and single-valuedness",
             "Every element of the domain must have an image (total), and only one "
             "(well defined). A rule failing either is not a function."),
            ("Codomain is declared, image is derived",
             "`f : ℝ → ℝ` with `f(x) = x²` has codomain `ℝ` and image `[0, ∞)`. "
             "Surjectivity in lesson 11 is exactly the question of whether they coincide."),
            ("The codomain is part of the function",
             "`x ↦ x²` from `ℝ` to `ℝ` and from `ℝ` to `[0, ∞)` are different functions, "
             "and one is surjective while the other is not."),
        ],
        "read_title": "What a function is",
        "read_intro": "The definition as a relation, then the vocabulary and the standard traps.",
        "body": [
            ("def", ("Function",
                     "A <strong>function</strong> `f : A → B` is a relation "
                     "`f ⊆ A × B` such that for every `a ∈ A` there is exactly one `b ∈ B` "
                     "with `(a, b) ∈ f`. That `b` is written `f(a)`.")),
            ("p", "The definition packs two conditions. <strong>At least one</strong> "
                  "output for each input makes the function total &mdash; a rule undefined "
                  "somewhere on its stated domain is not a function on that domain. "
                  "<strong>At most one</strong> makes it well defined &mdash; a rule giving "
                  "two answers for one input is not a function at all."),
            ("def", ("Domain, codomain, image",
                     "In `f : A → B`, `A` is the <strong>domain</strong>, `B` the "
                     "<strong>codomain</strong>, and "
                     "`f(A) = {f(a) : a ∈ A} ⊆ B` the <strong>image</strong> (or range).")),
            ("example", ("The same rule, three functions",
                         "`f : ℝ → ℝ`, `f(x) = x²` has image `[0, ∞) ≠ ℝ`. "
                         "`g : ℝ → [0, ∞)`, `g(x) = x²` has image equal to its codomain. "
                         "`h : [0, ∞) → [0, ∞)`, `h(x) = x²` is in addition one-to-one. "
                         "Same formula, three different functions, three different "
                         "answers in lesson 11.")),
            ("h3", "Two ways a rule fails to be a function"),
            ("ul", [
                "<strong>Not total.</strong> `f : ℝ → ℝ` with `f(x) = 1/x` is not a "
                "function on `ℝ`: nothing is assigned to 0. It is a function on "
                "`ℝ \\ {0}`, and stating the domain correctly is the fix.",
                "<strong>Not single-valued.</strong> \"`f(x)` is a square root of `x`\" "
                "assigns two values to 4. Choosing the non-negative one makes it a "
                "function; leaving both does not.",
            ]),
            ("p", "A third failure is subtler and appears whenever a function is defined "
                  "through a representative. \"Define `f([a]) = a mod 2` on classes mod 4\" "
                  "must be checked: `[1] = [5]`, so `f` must give the same answer for 1 and "
                  "5, and it does. Had the rule been `f([a]) = a mod 3`, then `1 mod 3 = 1` "
                  "and `5 mod 3 = 2`, and `f` would not be <strong>well defined</strong>."),
            ("def", ("Image and preimage of a set",
                     "For `S ⊆ A`, `f(S) = {f(a) : a ∈ S}`. For `T ⊆ B`, the "
                     "<strong>preimage</strong> `f⁻¹(T) = {a ∈ A : f(a) ∈ T}`. The "
                     "preimage notation does not presuppose an inverse function.")),
            ("p", "That last remark matters. `f⁻¹(T)` is defined for every function and "
                  "every `T`; it may be empty. The inverse <em>function</em> `f⁻¹` exists "
                  "only when `f` is a bijection, which is lesson 12."),
            ("def", ("Some standard functions",
                     "`⌊x⌋` is the largest integer `≤ x`; `⌈x⌉` the smallest integer "
                     "`≥ x`. The <strong>identity</strong> `id_A(a) = a`. A "
                     "<strong>sequence</strong> is a function `ℕ → A`, which is why "
                     "course 3's recurrences are functions on the naturals.")),
        ],
        "lab": ("function", {
            "panel_title": "Assign each input an output",
            "panel_intro": "Every element of `A` has exactly one arrow, which is what "
                           "makes this a function. Notice you cannot build a non-function "
                           "here &mdash; the control only permits one target per source.",
        }),
        "steps_title": "Checking a rule is a function",
        "steps_intro": "Two conditions, plus a third when classes are involved.",
        "steps": [
            ("Is every element of the domain assigned a value?",
             "Division, square roots and logarithms are the usual places a rule quietly "
             "fails. Either restrict the domain or the rule is not a function on it."),
            ("Is the value unique?",
             "One input, one output. If the rule offers a choice, the function is not "
             "specified until the choice is made."),
            ("If inputs are classes, check well-definedness",
             "Compute the rule on two representatives of the same class. Different answers "
             "mean the rule is not a function on classes at all."),
            ("State the codomain deliberately",
             "It is part of the function. Declaring `f : ℝ → ℝ` rather than "
             "`f : ℝ → [0,∞)` changes the answer to lesson 11's question."),
        ],
        "worked": {
            "title": "Is it a function?",
            "intro": ["Four candidate rules, with the domain stated in each case."],
            "lines": [
                "1.  f : ℝ → ℝ,      f(x) = 2x + 1          YES",
                "",
                "2.  f : ℝ → ℝ,      f(x) = 1/x             NO — undefined at 0",
                "    f : ℝ\\{0} → ℝ, f(x) = 1/x             YES",
                "",
                "3.  f : ℝ → ℝ,      f(x)² = x              NO — two values for x = 4,",
                "                                            and none for x = −1",
                "",
                "4.  f : ℤ/4ℤ → ℤ/2ℤ, f([a]₄) = [a]₂        YES — well defined:",
                "    if a ≡ b (mod 4) then 4 | (a−b), so 2 | (a−b), so a ≡ b (mod 2)",
            ],
            "after": [
                "Case 4 is the one that needs an argument rather than an inspection. The "
                "rule is stated through a representative, so it is a function only because "
                "any two representatives of the same class mod 4 agree mod 2 &mdash; and "
                "that had to be proved, not assumed."
            ],
        },
        "quiz_title": "Functions",
        "quiz": [
            {"q": "`f : ℝ → ℝ`, `f(x) = x²`. What is the image?",
             "a": ["`ℝ`", "`[0, ∞)`", "`(0, ∞)`", "the same as the codomain"],
             "c": 1,
             "why": "Squares are non-negative and every non-negative real is a square, so "
                    "the image is `[0, ∞)`. The codomain was declared to be `ℝ`, so image "
                    "and codomain differ."},
            {"q": "Why is \"`f(x)` = a square root of `x`\" not a function on `[0, ∞)`?",
             "a": ["Its domain is wrong",
                   "It assigns two values to every positive `x`",
                   "It is undefined at 0",
                   "It is not surjective"],
             "c": 1,
             "why": "Single-valuedness fails: 4 has square roots 2 and −2. Choosing the "
                    "non-negative root turns the rule into a function."},
            {"q": "`f⁻¹(T)` is defined:",
             "a": ["only when `f` is a bijection",
                   "for any function `f` and any `T ⊆ B`",
                   "only when `f` is injective",
                   "only when `T` is a single element"],
             "c": 1,
             "why": "The preimage of a set is always defined and may be empty. The inverse "
                    "FUNCTION requires a bijection; the notation is unfortunately shared."},
        ],
        "mistakes": [
            ("Treating image and codomain as the same set",
             "They coincide exactly when the function is surjective, which is lesson 11's "
             "question. Assuming they coincide answers it without asking."),
            ("Ignoring the domain when a rule is undefined somewhere",
             "`1/x` is a perfectly good function &mdash; on `ℝ \\ {0}`. The rule and the "
             "domain together make the function."),
            ("Defining a function on classes without checking well-definedness",
             "Any rule stated through a representative owes this check. It is the most "
             "commonly skipped step in course 6."),
        ],
        "standard": ("Finish when you can state domain, codomain and image separately for "
                     "any function you meet.",
                     "For `f : ℤ → ℤ` with `f(n) = n²`, name all three, and then say what "
                     "changes if the codomain is narrowed to the set of perfect squares. "
                     "That narrowing is the whole difference lesson 11 measures."),
        "note": "A function is formally a set of pairs, so two functions are equal when "
                "they have the same domain, the same codomain and the same value at every "
                "point. Two formulas that agree everywhere define one function; the same "
                "formula with different codomains defines two.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "injective-surjective-bijective",
        "title": "Injective, Surjective, Bijective",
        "module": "Functions",
        "one_line": "No collisions, no gaps, or neither.",
        "summary": (
            "Injective means distinct inputs get distinct outputs; surjective means the "
            "image fills the codomain; bijective is both. On finite sets of equal size "
            "the two properties imply each other, and on infinite sets they do not."
        ),
        "key": [
            "injective   f(x) = f(y) → x = y            no two inputs collide",
            "surjective  ∀b ∈ B ∃a ∈ A. f(a) = b        the image IS the codomain",
            "bijective   both                           a perfect pairing",
            "|A| = |B| finite  ⟹  injective ⟺ surjective",
        ],
        "key_label": "Two properties, four combinations",
        "concepts_intro": (
            "Each property is a quantified sentence, and each is refuted by naming a "
            "specific collision or a specific gap."
        ),
        "concepts": [
            ("Injective is about collisions",
             "Two different inputs may never share an output. To refute it, name the two "
             "inputs; the contrapositive `x ≠ y → f(x) ≠ f(y)` says the same thing."),
            ("Surjective is about coverage",
             "Every element of the codomain must be hit. To refute it, name the element "
             "nothing maps to. It depends on the codomain, so it is not a property of the "
             "formula alone."),
            ("On finite equal-sized sets the two coincide",
             "Injective and surjective imply each other when `|A| = |B|` is finite. On "
             "infinite sets they come apart, and that failure defines infinity."),
        ],
        "read_title": "The three properties",
        "read_intro": "Definitions, how to prove and refute each, and the finite/infinite split.",
        "body": [
            ("def", ("Injective",
                     "`f : A → B` is <strong>injective</strong> (one-to-one) when "
                     "`f(x) = f(y) ⟹ x = y` for all `x, y ∈ A`. Equivalently, "
                     "`x ≠ y ⟹ f(x) ≠ f(y)`.")),
            ("def", ("Surjective",
                     "`f : A → B` is <strong>surjective</strong> (onto) when for every "
                     "`b ∈ B` there is some `a ∈ A` with `f(a) = b` &mdash; equivalently, "
                     "when the image equals the codomain.")),
            ("def", ("Bijective",
                     "`f` is <strong>bijective</strong> when it is both injective and "
                     "surjective. A bijection pairs the elements of `A` with those of `B` "
                     "so that nothing is left over on either side.")),
            ("p", "The two definitions are stated in the two directions that make them "
                  "usable. Injectivity is proved by assuming `f(x) = f(y)` and deriving "
                  "`x = y` &mdash; a direct proof. Surjectivity is proved by taking an "
                  "arbitrary `b` and constructing an `a` that maps to it &mdash; an "
                  "existence proof, and usually the harder of the two."),
            ("example", ("The same rule, different verdicts",
                         "`f : ℝ → ℝ`, `f(x) = x²`: neither &mdash; `f(2) = f(−2)` breaks "
                         "injectivity, and nothing maps to `−1`. "
                         "`f : [0,∞) → ℝ`: injective, not surjective. "
                         "`f : ℝ → [0,∞)`: surjective, not injective. "
                         "`f : [0,∞) → [0,∞)`: bijective. The formula never changed.")),
            ("thm", ("On finite sets of equal size, one implies the other",
                     "Let `A` and `B` be finite with `|A| = |B|`, and `f : A → B`. Then "
                     "`f` is injective if and only if it is surjective.")),
            ("proof", [
                "If `f` is injective, its image has `|A|` distinct elements, all inside "
                "`B`. Since `|B| = |A|` and `B` is finite, the image is all of `B`, so `f` "
                "is surjective.",
                "If `f` is surjective, every one of the `|B|` elements of `B` needs at "
                "least one preimage; with only `|A| = |B|` inputs available, each gets "
                "exactly one, so no two inputs collide and `f` is injective.",
            ]),
            ("thm", ("The cardinality constraints",
                     "If `f : A → B` is injective then `|A| ≤ |B|`; if surjective then "
                     "`|A| ≥ |B|`; if bijective then `|A| = |B|`. For finite sets these "
                     "are the pigeonhole principle of lesson 14.")),
            ("p", "So the answer is sometimes settled before any function is examined. "
                  "With `|A| = 5` and `|B| = 3` no injection exists, whatever the rule; "
                  "with `|A| = 3` and `|B| = 5` no surjection does. The lab reports this "
                  "before letting you hunt."),
            ("p", "On infinite sets the equivalence fails, and the failure is the "
                  "definition of infinity. `f : ℕ → ℕ` with `f(n) = n + 1` is injective and "
                  "not surjective &mdash; nothing maps to 0 &mdash; even though the domain "
                  "and codomain are the same set. A set is infinite exactly when it admits "
                  "an injection to a proper subset of itself."),
        ],
        "lab": ("function", {
            "panel_title": "Try to build each kind",
            "panel_intro": "Set the two sizes first. With `|A| &gt; |B|` no injection "
                           "exists at all and the lab says so, which is the pigeonhole "
                           "principle arriving three lessons early.",
        }),
        "steps_title": "Deciding the three properties",
        "steps_intro": "Check the sizes first; they often settle it.",
        "steps": [
            ("Compare the cardinalities",
             "`|A| &gt; |B|` rules out injective; `|A| &lt; |B|` rules out surjective. "
             "Both are free and both are conclusive."),
            ("For injectivity, assume `f(x) = f(y)`",
             "Derive `x = y` by algebra. If the derivation needs a case split or fails, "
             "look for the collision instead."),
            ("For surjectivity, solve `f(a) = b` for `a`",
             "Take an arbitrary `b` in the codomain and construct a preimage. If the "
             "construction leaves the domain, `f` is not surjective."),
            ("Name the witness when a property fails",
             "The colliding pair, or the unhit element. \"Not injective\" without the pair "
             "is an assertion, not an answer."),
        ],
        "worked": {
            "title": "Classify `f : ℤ → ℤ`, `f(n) = 2n + 3`",
            "intro": ["Both directions, written out."],
            "lines": [
                "INJECTIVE?",
                "   Suppose f(m) = f(n).",
                "   2m + 3 = 2n + 3  ⟹  2m = 2n  ⟹  m = n.        YES",
                "",
                "SURJECTIVE?",
                "   Take b ∈ ℤ.  Solve 2a + 3 = b:  a = (b − 3)/2.",
                "   For b = 0 this gives a = −3/2 ∉ ℤ.             NO",
                "   Nothing maps to 0 — indeed the image is the ODD integers.",
                "",
                "So f is injective, not surjective, and NOT bijective.",
                "Change the codomain to the odd integers and it becomes a bijection.",
            ],
            "after": [
                "Note that `|ℤ| = |ℤ|` here and injectivity still did not give "
                "surjectivity. The finite theorem above genuinely needs finiteness, and "
                "this is the counterexample."
            ],
        },
        "quiz_title": "Classification",
        "quiz": [
            {"q": "`f : ℝ → ℝ`, `f(x) = x³`. This is:",
             "a": ["injective only", "surjective only", "bijective", "neither"],
             "c": 2,
             "why": "Cubing is strictly increasing so no two inputs collide, and every "
                    "real has a real cube root so nothing is missed."},
            {"q": "`|A| = 5`, `|B| = 7`. Which is impossible?",
             "a": ["an injection `A → B`", "a surjection `A → B`",
                   "a function `A → B`", "an injection `B → A`"],
             "c": 1,
             "why": "Five inputs cannot cover seven targets. (An injection `B → A` is also "
                    "impossible, for the mirror reason &mdash; but the question asks for "
                    "`A → B`.)"},
            {"q": "`f : ℕ → ℕ`, `f(n) = n + 1`. This shows that:",
             "a": ["injectivity implies surjectivity",
                   "on infinite sets, injective does not imply surjective",
                   "`f` is bijective",
                   "`ℕ` is finite"],
             "c": 1,
             "why": "It is injective and misses 0, with domain and codomain the same "
                    "infinite set. The finite theorem does not extend."},
        ],
        "mistakes": [
            ("Deciding surjectivity without the codomain",
             "It is not a property of the formula. `x ↦ x²` is surjective onto `[0, ∞)` "
             "and not onto `ℝ`, with no change to the rule."),
            ("Assuming injective implies surjective",
             "True for finite sets of equal size, false in general. `n ↦ n + 1` on `ℕ` is "
             "the standard counterexample and is worth remembering."),
            ("Refuting a property without a witness",
             "\"Not injective\" needs the colliding pair; \"not surjective\" needs the "
             "unhit element. The witness is the proof."),
        ],
        "standard": ("Finish when you can produce a witness for every negative verdict.",
                     "Classify `f : ℤ → ℤ` with `f(n) = n² − n`, giving either a proof or "
                     "a specific witness for each property. (`f(0) = f(1) = 0`, which "
                     "settles one of them immediately.)"),
        "note": "The four combinations all occur, and it is worth having an example of "
                "each in mind: `n ↦ 2n` on `ℤ` (injective only), `n ↦ ⌊n/2⌋` on `ℤ` "
                "(surjective only), `n ↦ n + 1` on `ℤ` (bijective), and `n ↦ n²` on `ℤ` "
                "(neither).",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "composition-and-inverses",
        "title": "Composition and Inverse Functions",
        "module": "Functions",
        "one_line": "Chaining functions, and undoing them.",
        "summary": (
            "`(g ∘ f)(x) = g(f(x))` &mdash; right to left. Composition preserves "
            "injectivity and surjectivity, and an inverse function exists exactly when "
            "`f` is a bijection."
        ),
        "key": [
            "(g ∘ f)(x) = g(f(x))              apply f FIRST",
            "f ∘ g ≠ g ∘ f                     in general",
            "f⁻¹ exists  ⟺  f is a bijection",
            "f⁻¹ ∘ f = id_A      f ∘ f⁻¹ = id_B",
        ],
        "key_label": "Compose right to left",
        "concepts_intro": (
            "Composition is how functions are built out of simpler ones, and the inverse "
            "is the question of whether the building can be undone."
        ),
        "concepts": [
            ("Composition reads right to left",
             "`g ∘ f` applies `f` first. The notation matches `g(f(x))`, which is why it "
             "looks backwards until you read it as substitution."),
            ("Composition is associative, not commutative",
             "`(h ∘ g) ∘ f = h ∘ (g ∘ f)` always. `f ∘ g = g ∘ f` almost never."),
            ("An inverse needs a bijection",
             "Not injective means two inputs share an output, so the inverse could not "
             "choose. Not surjective means some output has no input, so the inverse would "
             "be undefined there."),
        ],
        "read_title": "Composition and inversion",
        "read_intro": "The definitions, what composition preserves, and the inverse theorem.",
        "body": [
            ("def", ("Composition",
                     "For `f : A → B` and `g : B → C`, the composition `g ∘ f : A → C` is "
                     "defined by `(g ∘ f)(a) = g(f(a))`. It requires the codomain of `f` "
                     "to be contained in the domain of `g`.")),
            ("p", "Order matters twice over. `g ∘ f` and `f ∘ g` are different functions "
                  "when both are defined, and often only one of them is defined at all "
                  "&mdash; the types have to line up."),
            ("thm", ("Associativity",
                     "`(h ∘ g) ∘ f = h ∘ (g ∘ f)` whenever the compositions are defined.")),
            ("proof", [
                "Both sides send `a` to `h(g(f(a)))`. Two functions with the same domain, "
                "the same codomain and the same value everywhere are equal.",
            ]),
            ("thm", ("Composition preserves the properties",
                     "If `f` and `g` are both injective, so is `g ∘ f`. If both are "
                     "surjective, so is `g ∘ f`. If both are bijective, so is `g ∘ f`.")),
            ("proof", [
                "Injective: suppose `g(f(x)) = g(f(y))`. Injectivity of `g` gives "
                "`f(x) = f(y)`, and injectivity of `f` gives `x = y`.",
                "Surjective: take `c ∈ C`. Surjectivity of `g` gives `b ∈ B` with "
                "`g(b) = c`; surjectivity of `f` gives `a ∈ A` with `f(a) = b`. Then "
                "`(g ∘ f)(a) = c`.",
            ]),
            ("p", "The converses are weaker and worth knowing. If `g ∘ f` is injective "
                  "then `f` must be injective &mdash; but `g` need not be. If `g ∘ f` is "
                  "surjective then `g` must be surjective &mdash; but `f` need not be. Each "
                  "is a short argument and each catches a plausible false claim."),
            ("def", ("Inverse function",
                     "`g : B → A` is an <strong>inverse</strong> of `f : A → B` when "
                     "`g ∘ f = id_A` and `f ∘ g = id_B`. When it exists it is unique and is "
                     "written `f⁻¹`.")),
            ("thm", ("Inverses exist exactly for bijections",
                     "`f : A → B` has an inverse if and only if `f` is a bijection.")),
            ("proof", [
                "Suppose `f` is a bijection. For each `b ∈ B`, surjectivity gives at least "
                "one `a` with `f(a) = b` and injectivity gives at most one, so exactly one. "
                "Defining `f⁻¹(b)` to be that `a` is a legitimate function, and it "
                "satisfies both identities by construction.",
                "Conversely, suppose `g` is an inverse. If `f(x) = f(y)` then applying `g` "
                "gives `x = y`, so `f` is injective. And for any `b`, `f(g(b)) = b`, so "
                "`g(b)` is a preimage of `b` and `f` is surjective.",
            ]),
            ("p", "Uniqueness follows quickly: if `g` and `h` are both inverses then "
                  "`g = g ∘ id = g ∘ (f ∘ h) = (g ∘ f) ∘ h = id ∘ h = h`. The chain uses "
                  "associativity, which is why associativity was worth stating."),
            ("example", ("Finding an inverse",
                         "`f : ℝ → ℝ`, `f(x) = 3x − 5`. Set `y = 3x − 5` and solve: "
                         "`x = (y + 5)/3`, so `f⁻¹(y) = (y + 5)/3`. Check: "
                         "`f(f⁻¹(y)) = 3((y+5)/3) − 5 = y`. Both directions should be "
                         "checked, because solving for `x` proves only one of them.")),
            ("thm", ("Inverse of a composition",
                     "`(g ∘ f)⁻¹ = f⁻¹ ∘ g⁻¹` when both inverses exist &mdash; the order "
                     "reverses. Undoing \"socks then shoes\" is \"shoes off, then socks\".")),
        ],
        "lab": ("function", {
            "panel_title": "When does an inverse exist?",
            "panel_intro": "Build a bijection and the arrows can be read backwards without "
                           "ambiguity. Break injectivity and two arrows point at one "
                           "target, so the reverse has a choice to make &mdash; which is "
                           "exactly why no inverse exists.",
        }),
        "steps_title": "Composing and inverting",
        "steps_intro": "Check the types, then work inside out.",
        "steps": [
            ("Check the codomain and domain line up",
             "`g ∘ f` needs `f`'s outputs to be legal inputs for `g`. A type mismatch is "
             "not a subtlety; the composition does not exist."),
            ("Evaluate inside out",
             "`(g ∘ f)(3)` is `g(f(3))`. Compute `f(3)` first. Half of all composition "
             "errors are order errors."),
            ("To invert, verify bijectivity first",
             "No bijection, no inverse. Solving `y = f(x)` for `x` and finding two "
             "solutions or none is the same discovery arrived at slowly."),
            ("Check both identities",
             "`f⁻¹ ∘ f = id` and `f ∘ f⁻¹ = id`. Solving for `x` naturally establishes "
             "one; the other is a separate substitution."),
        ],
        "worked": {
            "title": "Composition is not commutative",
            "intro": ["`f(x) = 2x` and `g(x) = x + 3`, both `ℝ → ℝ`."],
            "lines": [
                "(g ∘ f)(x) = g(f(x)) = g(2x)   = 2x + 3",
                "(f ∘ g)(x) = f(g(x)) = f(x + 3) = 2x + 6",
                "",
                "At x = 1:   g∘f gives 5,   f∘g gives 8.   Different functions.",
                "",
                "Inverses:",
                "   f⁻¹(y) = y/2          g⁻¹(y) = y − 3",
                "   (g ∘ f)⁻¹(y) = (y − 3)/2",
                "   f⁻¹(g⁻¹(y))  = f⁻¹(y − 3) = (y − 3)/2        agree",
                "   g⁻¹(f⁻¹(y))  = g⁻¹(y/2)   = y/2 − 3          does NOT",
            ],
            "after": [
                "The last two lines are the order-reversal law being tested rather than "
                "asserted. `(g ∘ f)⁻¹ = f⁻¹ ∘ g⁻¹`, and composing the inverses in the "
                "original order gives a different function entirely."
            ],
        },
        "quiz_title": "Composition and inverses",
        "quiz": [
            {"q": "`f(x) = x + 1`, `g(x) = x²`. What is `(g ∘ f)(2)`?",
             "a": ["5", "9", "6", "4"],
             "c": 1,
             "why": "Apply `f` first: `f(2) = 3`. Then `g`: `3² = 9`. The other order "
                    "would give `g(2) = 4` then `f(4) = 5`."},
            {"q": "`f : A → B` is injective but not surjective. Does `f⁻¹` exist?",
             "a": ["Yes", "No, because some `b ∈ B` has no preimage",
                   "No, because two inputs collide", "Only if `A` is finite"],
             "c": 1,
             "why": "An inverse must be defined on all of `B`. Surjectivity is exactly the "
                    "condition that gives every `b` a preimage to map back to."},
            {"q": "`(g ∘ f)⁻¹` equals:",
             "a": ["`g⁻¹ ∘ f⁻¹`", "`f⁻¹ ∘ g⁻¹`", "`f ∘ g`", "`(f ∘ g)⁻¹`"],
             "c": 1,
             "why": "The order reverses: undo the last thing done first. Socks then shoes "
                    "is undone by shoes then socks."},
        ],
        "mistakes": [
            ("Composing left to right",
             "`g ∘ f` applies `f` first. The notation follows `g(f(x))`, and reading it "
             "the other way produces a different function silently."),
            ("Writing `f⁻¹` for a function that is not a bijection",
             "The preimage `f⁻¹(T)` of a set always exists; the inverse function does not. "
             "The shared notation is a genuine trap."),
            ("Checking only one of the two inverse identities",
             "`g ∘ f = id_A` alone makes `g` a left inverse, which is weaker. Both "
             "identities are needed for `g = f⁻¹`."),
        ],
        "standard": ("Finish when you can invert a composition in the right order.",
                     "With `f(x) = 3x + 1` and `g(x) = x − 4` on `ℝ`, compute `g ∘ f` and "
                     "`(g ∘ f)⁻¹` directly, then check the answer equals `f⁻¹ ∘ g⁻¹`. If "
                     "the two agree you have the order right."),
        "note": "Bijections from a set to itself are called permutations, and under "
                "composition they form a group: associative, with identity, and every "
                "element invertible. Course 4 counts them &mdash; there are `n!` &mdash; "
                "and that count is the reason permutations appear everywhere in "
                "combinatorics.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "cardinality-and-countability",
        "title": "Cardinality and Countability",
        "module": "Counting",
        "one_line": "Same size means a bijection, even for infinite sets.",
        "summary": (
            "Two sets have the same size when a bijection pairs them. That definition "
            "makes `ℤ` and `ℚ` the same size as `ℕ`, and Cantor's diagonal argument "
            "shows `ℝ` is strictly larger."
        ),
        "key": [
            "|A| = |B|   ⟺   a bijection A → B exists",
            "countable   =   finite, or in bijection with ℕ",
            "|ℕ| = |ℤ| = |ℚ|          all countably infinite",
            "|ℝ| > |ℕ|                Cantor's diagonal argument",
        ],
        "key_label": "Size, defined by pairing",
        "concepts_intro": (
            "Counting stops working at infinity, so size is redefined by pairing. The "
            "consequences are strange and they are forced."
        ),
        "concepts": [
            ("Bijection is the definition of same size",
             "For finite sets it agrees with counting. For infinite ones it is the only "
             "definition available, and it must be accepted before anything here parses."),
            ("An infinite set can match a proper subset",
             "`ℕ` and the even naturals are the same size, via `n ↦ 2n`. For finite sets "
             "that is impossible; for infinite ones it is the definition of infinite."),
            ("Not all infinities are equal",
             "`ℝ` cannot be listed. Cantor's diagonal argument constructs, from any "
             "proposed list, a real number missing from it."),
        ],
        "read_title": "Countable and uncountable",
        "read_intro": "The definition, the three positive results, and the one negative one.",
        "body": [
            ("def", ("Same cardinality",
                     "`|A| = |B|` means there is a bijection `A → B`. `|A| ≤ |B|` means "
                     "there is an injection `A → B`.")),
            ("def", ("Countable",
                     "A set is <strong>countably infinite</strong> if it is in bijection "
                     "with `ℕ`, and <strong>countable</strong> if it is finite or countably "
                     "infinite. Otherwise it is <strong>uncountable</strong>.")),
            ("p", "Countably infinite means listable: a bijection with `ℕ` is exactly an "
                  "enumeration `a₀, a₁, a₂, …` in which every element appears exactly once. "
                  "Proving countability means producing such a list."),
            ("thm", ("`ℤ` is countable",
                     "The integers can be listed: `0, 1, −1, 2, −2, 3, −3, …`")),
            ("proof", [
                "Define `f : ℕ → ℤ` by `f(n) = n/2` for even `n` and `f(n) = −(n+1)/2` for "
                "odd `n`. The even inputs produce `0, 1, 2, 3, …` and the odd ones produce "
                "`−1, −2, −3, …`, so every integer appears exactly once. That is a "
                "bijection, so `|ℤ| = |ℕ|`.",
            ]),
            ("p", "Listing them in their natural order `…, −2, −1, 0, 1, 2, …` does not "
                  "work: it has no first element, so it is not an enumeration by `ℕ`. "
                  "Reordering is allowed and is exactly what the alternating list does."),
            ("thm", ("`ℚ` is countable",
                     "The rational numbers can be listed.")),
            ("proof", [
                "Arrange the positive rationals `a/b` in a grid with `a` as the row and `b` "
                "as the column, and walk it along diagonals: `1/1`, then `1/2, 2/1`, then "
                "`1/3, 2/2, 3/1`, and so on. Every positive rational appears; skip any "
                "fraction not in lowest terms so each appears once.",
                "Each diagonal is finite, so the walk reaches every cell in finitely many "
                "steps. Interleave the negatives and 0 as in the previous theorem to get "
                "all of `ℚ`.",
            ]),
            ("p", "This is genuinely surprising: the rationals are dense &mdash; between "
                  "any two there is another &mdash; and there are still no more of them "
                  "than there are counting numbers. Density and cardinality are unrelated "
                  "properties."),
            ("thm", ("Cantor: `ℝ` is uncountable",
                     "There is no surjection `ℕ → ℝ`; in particular no bijection.")),
            ("proof", [
                "It is enough to show the interval `(0,1)` cannot be listed. Suppose "
                "`r₀, r₁, r₂, …` is any list of reals in `(0,1)`, each written as a decimal "
                "expansion `rₙ = 0.dₙ₁dₙ₂dₙ₃…`",
                "Build a new number `x = 0.x₁x₂x₃…` by choosing `xₖ = 5` if `dₖₖ ≠ 5`, and "
                "`xₖ = 4` otherwise. (Restricting to 4 and 5 avoids the ambiguity of "
                "expansions ending in all 9s.)",
                "Then `x` differs from `r₁` in the first decimal place, from `r₂` in the "
                "second, and from `rₙ` in the `n`th &mdash; so `x` is on no line of the "
                "list, yet lies in `(0,1)`.",
                "Every proposed list therefore misses something, so no list of all the "
                "reals exists.",
            ]),
            ("p", "The argument is constructive in a useful sense: hand it a list and it "
                  "hands back a specific missing number. It does not rely on the list "
                  "being defined by any rule, which is why it defeats all lists at once."),
            ("thm", ("Cantor's theorem",
                     "For every set `A`, there is no surjection `A → P(A)`; so "
                     "`|A| &lt; |P(A)|`. There is no largest cardinality.")),
        ],
        "lab": ("function", {
            "panel_title": "Bijection as the definition of size",
            "panel_intro": "On finite sets a bijection needs `|A| = |B|`, and the lab "
                           "enforces it. The whole content of this lesson is that on "
                           "infinite sets that constraint disappears.",
        }),
        "steps_title": "Proving a set countable or uncountable",
        "steps_intro": "Produce a list, or defeat every list.",
        "steps": [
            ("To prove countable, produce an explicit enumeration",
             "A rule that reaches every element in finitely many steps, with no repeats. "
             "The diagonal walk is the standard device for a two-dimensional family."),
            ("Check the list covers everything",
             "A list that never reaches some element is not an enumeration. The finiteness "
             "of each diagonal is what makes the rational walk work."),
            ("To prove uncountable, take an arbitrary list",
             "Not a specific one. The argument must defeat every list, which is why it "
             "starts with an unspecified enumeration."),
            ("Construct the missing element by diagonalising",
             "Differ from the `n`th entry in the `n`th position. The element you build is "
             "in the set and on no line of the list."),
        ],
        "worked": {
            "title": "The evens are the same size as `ℕ`",
            "intro": ["Which is impossible for finite sets and routine for infinite ones."],
            "lines": [
                "f : ℕ → E,  f(n) = 2n,  where E = {0, 2, 4, 6, …}",
                "",
                "injective?    2m = 2n ⟹ m = n                        yes",
                "surjective?   any even e = 2k, and f(k) = e           yes",
                "",
                "So |ℕ| = |E|, even though E ⊊ ℕ and E omits every odd number.",
                "",
                "  0 1 2 3 4 5 …",
                "  ↓ ↓ ↓ ↓ ↓ ↓",
                "  0 2 4 6 8 10 …",
            ],
            "after": [
                "This is Hilbert's hotel in arithmetic form, and it is the property that "
                "<em>defines</em> an infinite set: a set is infinite exactly when it is in "
                "bijection with a proper subset of itself. For a finite set that is "
                "impossible, by lesson 11's theorem."
            ],
        },
        "quiz_title": "Countability",
        "quiz": [
            {"q": "Which set is uncountable?",
             "a": ["`ℤ`", "`ℚ`", "`ℝ`", "the set of finite bit strings"],
             "c": 2,
             "why": "Cantor's diagonal argument defeats every proposed list of the reals. "
                    "The other three are all countable, the last by listing strings by "
                    "length then alphabetically."},
            {"q": "What does \"`|A| = |B|`\" mean for infinite sets?",
             "a": ["They have the same number of elements, counted",
                   "There is a bijection `A → B`",
                   "One is a subset of the other",
                   "They are both infinite"],
             "c": 1,
             "why": "Counting is unavailable, so pairing is the definition. It agrees with "
                    "counting whenever counting works."},
            {"q": "The diagonal argument works by:",
             "a": ["listing all reals and finding a duplicate",
                   "assuming `ℝ` is finite",
                   "constructing, from any list, a real differing from the `n`th entry in the `n`th place",
                   "showing `ℝ` has no smallest element"],
             "c": 2,
             "why": "It defeats every list at once by building a number that disagrees with "
                    "each line somewhere. The list is arbitrary, which is what makes the "
                    "argument general."},
        ],
        "mistakes": [
            ("Thinking a proper subset must be smaller",
             "True for finite sets and false for infinite ones. `n ↦ 2n` pairs `ℕ` with "
             "the evens, and no element is left over."),
            ("Confusing dense with uncountable",
             "`ℚ` is dense in `ℝ` and still countable. Having something between any two "
             "elements says nothing about cardinality."),
            ("Diagonalising against one specific list",
             "The argument must begin with an arbitrary list. Defeating one enumeration "
             "shows only that that enumeration was incomplete."),
        ],
        "standard": ("Finish when you can run the diagonal argument from memory.",
                     "Write out Cantor's proof for `(0,1)`, including why the digits 4 and "
                     "5 are chosen rather than any two. If you can state the reason &mdash; "
                     "avoiding the `0.4999… = 0.5000…` ambiguity &mdash; you have the "
                     "argument rather than its outline."),
        "note": "Whether any cardinality lies strictly between `|ℕ|` and `|ℝ|` is the "
                "continuum hypothesis. It was shown independent of the standard axioms of "
                "set theory: it can be neither proved nor disproved from them. That is a "
                "fact about the axioms, not about our ignorance.",
    },
    # ---------------------------------------------------------------- 14
    {
        "slug": "the-pigeonhole-principle",
        "title": "The Pigeonhole Principle",
        "module": "Counting",
        "one_line": "More objects than boxes means some box has two.",
        "summary": (
            "If `n` objects go into `k` boxes with `n > k`, some box holds at least two. "
            "It is obvious, it is a one-line consequence of lesson 11, and it proves "
            "things that are not obvious at all."
        ),
        "key": [
            "n objects, k boxes, n > k   ⟹   some box has ≥ 2",
            "generalised:  some box has ≥ ⌈n/k⌉",
            "equivalently: no injection A → B when |A| > |B|",
            "The art is choosing the boxes.",
        ],
        "key_label": "The principle, and its sharpening",
        "concepts_intro": (
            "The statement is trivial. Every application is an act of choosing what the "
            "boxes are, and that is where the work is."
        ),
        "concepts": [
            ("It is lesson 11 restated",
             "No injection exists from a larger finite set to a smaller one. Objects are "
             "the domain, boxes the codomain, and a collision is two objects sharing a box."),
            ("The generalised form is sharper",
             "With `n` objects in `k` boxes some box holds at least `⌈n/k⌉`. The basic "
             "form is this with `n = k + 1`."),
            ("Choosing the boxes is the whole difficulty",
             "The principle never tells you what the boxes are. Every interesting "
             "application is a clever choice of classification."),
        ],
        "read_title": "The principle and its applications",
        "read_intro": "Statement, proof, and four uses of increasing subtlety.",
        "body": [
            ("thm", ("Pigeonhole principle",
                     "If `n` objects are placed into `k` boxes and `n &gt; k`, then some "
                     "box contains at least two objects.")),
            ("proof", [
                "Suppose every box contained at most one object. Then the total number of "
                "objects would be at most `k`, contradicting `n &gt; k`.",
            ]),
            ("thm", ("Generalised pigeonhole principle",
                     "If `n` objects are placed into `k` boxes, some box contains at least "
                     "`⌈n/k⌉` objects.")),
            ("proof", [
                "Suppose every box held at most `⌈n/k⌉ − 1` objects. The total would then "
                "be at most `k(⌈n/k⌉ − 1)`. Since `⌈n/k⌉ &lt; n/k + 1`, this is less than "
                "`k(n/k + 1 − 1) = n`, contradicting that all `n` objects were placed.",
            ]),
            ("h3", "Four applications"),
            ("example", ("Shared birthdays",
                         "Among 367 people, two share a birthday. Boxes are the 366 "
                         "possible dates; objects are the people. No assumption about "
                         "distribution is needed &mdash; this is certainty, not probability, "
                         "and is a different claim from the birthday problem of course 5.")),
            ("example", ("A repeated remainder",
                         "Among any `n + 1` integers, two leave the same remainder on "
                         "division by `n`. The boxes are the `n` possible remainders "
                         "`0, …, n−1`. Consequently their difference is divisible by `n`, "
                         "which is a fact about divisibility obtained by counting.")),
            ("example", ("Two people with the same number of friends",
                         "In any group of `n ≥ 2` people, two have the same number of "
                         "acquaintances within the group. Degrees range over `0, …, n−1` "
                         "&mdash; `n` boxes for `n` people, which is not enough on its own. "
                         "But 0 and `n−1` cannot both occur: if someone knows nobody, "
                         "nobody can know everybody. So only `n−1` boxes are actually "
                         "available, and the principle applies.")),
            ("p", "That third example is the one worth studying. A naive count gives "
                  "exactly as many boxes as objects, and the principle does not apply; the "
                  "argument that two boxes are mutually exclusive is what creates the "
                  "surplus. Applications usually turn on an observation of that kind."),
            ("example", ("A subset summing to a multiple of `n`",
                         "Given any `n` integers `a₁, …, aₙ`, some consecutive block "
                         "`aᵢ₊₁ + ⋯ + aⱼ` is divisible by `n`. Consider the `n` partial "
                         "sums `s₁, …, sₙ` and their remainders mod `n`. If some `sⱼ ≡ 0` "
                         "we are done; otherwise the `n` remainders lie in the `n−1` boxes "
                         "`1, …, n−1`, so two partial sums share a remainder, and their "
                         "difference &mdash; a consecutive block &mdash; is divisible by "
                         "`n`.")),
            ("p", "None of these is a statement about counting on its face, and every one "
                  "is proved by counting. That is the pattern: the principle converts a "
                  "size comparison into an existence claim, and the existence claim is what "
                  "you actually wanted."),
        ],
        "lab": ("function", {
            "panel_title": "The principle, as a constraint on arrows",
            "panel_intro": "Set `|A|` above `|B|`. The lab reports that no injection "
                           "exists at all &mdash; not that this assignment fails, but that "
                           "no arrangement of arrows could succeed. That is the pigeonhole "
                           "principle stated as a fact about functions.",
        }),
        "steps_title": "Applying the principle",
        "steps_intro": "The objects are usually given. The boxes are yours to invent.",
        "steps": [
            ("Identify the objects",
             "Usually stated in the problem: the people, the integers, the points. This "
             "step is rarely the difficulty."),
            ("Invent the boxes",
             "A classification with fewer categories than objects. Remainders, parities, "
             "ranges, and degree counts are the standard choices."),
            ("Count both sides",
             "You need strictly more objects than boxes. If the counts are equal, look "
             "for a reason some box is unusable &mdash; that was the friends argument."),
            ("Say what a shared box means",
             "Two objects in one box gives you the conclusion: same remainder means the "
             "difference divides, same degree means the claim is proved. Name it."),
        ],
        "worked": {
            "title": "Five points in a unit square",
            "intro": ["Show two of any five points are within `√2 / 2` of each other."],
            "lines": [
                "Boxes: cut the unit square into four quarters, each ½ × ½.",
                "Objects: the five points.",
                "",
                "5 points into 4 quarters ⟹ some quarter holds two points.",
                "",
                "Two points in a ½ × ½ square are at most its diagonal apart:",
                "   √(½² + ½²)  =  √(1/2)  =  √2 / 2  ≈ 0.707",
                "",
                "So two of the five points are within √2 / 2 of each other.      ∎",
            ],
            "after": [
                "The choice of four quarters is the entire proof. Cutting into nine "
                "ninths would give nine boxes for five points and prove nothing; cutting "
                "into two halves would give a weaker bound. The classification is chosen "
                "to make the counts work and the conclusion strong."
            ],
        },
        "quiz_title": "Pigeonhole",
        "quiz": [
            {"q": "13 people are in a room. What is guaranteed?",
             "a": ["Two share a birthday",
                   "Two were born in the same month",
                   "Two are the same age",
                   "Nothing"],
             "c": 1,
             "why": "Twelve months, thirteen people. Birthdays need 367 people, and ages "
                    "have no bounded range that forces a collision."},
            {"q": "20 objects into 6 boxes. Some box holds at least:",
             "a": ["3", "4", "5", "6"],
             "c": 1,
             "why": "`⌈20/6⌉ = ⌈3.33⌉ = 4`. The generalised principle rounds up, and 3 "
                    "would be the answer if it rounded down."},
            {"q": "Why can 0 and `n−1` not both appear as acquaintance counts?",
             "a": ["Because degrees must be distinct",
                   "Because someone who knows nobody prevents anyone from knowing everybody",
                   "Because the graph must be connected",
                   "They can both appear"],
             "c": 1,
             "why": "If A knows nobody then B cannot know all `n−1` others, since B does "
                    "not know A. That mutual exclusion is what reduces the box count to "
                    "`n−1` and makes the principle apply."},
        ],
        "mistakes": [
            ("Choosing boxes that outnumber the objects",
             "The principle needs strictly more objects than boxes. A finer classification "
             "is not a better one."),
            ("Rounding the generalised bound down",
             "It is `⌈n/k⌉`. With 20 objects and 6 boxes the guarantee is 4, not 3."),
            ("Reading the conclusion as probabilistic",
             "Pigeonhole gives certainty. \"Two of 367 people share a birthday\" is not "
             "likely; it is unavoidable, and course 5's birthday problem is a genuinely "
             "different question."),
        ],
        "standard": ("Finish when you can invent the boxes yourself.",
                     "Prove that among any 10 distinct integers between 1 and 100, two "
                     "different subsets have the same sum. The objects are subsets and the "
                     "boxes are possible sums &mdash; count both and the argument writes "
                     "itself, which is the skill this lesson is for."),
        "note": "Course 4 lesson 12 returns to the generalised principle with harder "
                "applications, and course 7 uses it to prove that a graph on `n` vertices "
                "with more than `n − 1` edges must contain a cycle. It is the most "
                "reusable single fact on this path.",
    },
]
