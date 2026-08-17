"""Course 1, lessons 01-07 — the real number system, its properties, and integer exponents through radicals."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "real-numbers-and-the-number-line",
        "title": "Real Numbers and the Number Line",
        "module": "The number system",
        "one_line": "Which numbers there are, and where each one sits.",
        "summary": (
            "The counting numbers, the integers, the rationals and the reals, each built "
            "from the one before. A number is a place on the line, not the notation you "
            "happened to write it in, and comparing two of them means comparing places."
        ),
        "key": [
            "naturals     1, 2, 3, …",
            "integers     …, −2, −1, 0, 1, 2, …",
            "rationals    p/q  with p, q integers and q ≠ 0",
            "reals        every point on the line, rational or not",
        ],
        "key_label": "Four systems, each inside the next",
        "concepts_intro": (
            "Algebra puts a letter where a number goes. Before that is useful you have to "
            "know what the letter is allowed to stand for."
        ),
        "concepts": [
            ("Each system contains the one before it",
             "Every natural number is an integer, every integer is a rational (`5` is "
             "`5/1`), every rational is a real. The containments are strict in one "
             "direction only: `−3` is an integer and not a natural, `2/3` is rational and "
             "not an integer, `√2` is real and not rational."),
            ("A number is a place, not a spelling",
             "`1/2`, `2/4`, `0.5` and `3/6` are four ways of writing one number, and it "
             "occupies one point on the line. Almost every question in this course is a "
             "question about the point; the spelling is chosen for convenience."),
            ("Comparison is position, and it is exact",
             "`a &lt; b` means `a` lies to the left of `b`. Deciding it from a rounded "
             "decimal is guesswork &mdash; `1.414` and `√2` agree to three places and are "
             "different numbers. Compare by a common denominator, or by squaring."),
        ],
        "read_title": "The number system, and the line it sits on",
        "read_intro": "Four systems, how you tell a rational from an irrational, and the two facts about the line the rest of the course leans on.",
        "body": [
            ("p", "The systems are built outward, and each one is built because the "
                  "previous one could not answer a question. The naturals cannot answer "
                  "`3 − 5`. The integers cannot answer `3 / 5`. The rationals "
                  "cannot answer \"what is the side of a square of area 2\". Each answer "
                  "forces a larger system."),
            ("def", ("The four systems",
                     "The <strong>natural numbers</strong> are `1, 2, 3, …`. The "
                     "<strong>integers</strong> are the naturals, their negatives, and "
                     "`0`. A <strong>rational number</strong> is one that can be written "
                     "`p/q` where `p` and `q` are integers and `q ≠ 0`. The "
                     "<strong>real numbers</strong> are all the numbers on the number "
                     "line; a real number that is not rational is called "
                     "<strong>irrational</strong>.",
                     "Whether `0` counts as a natural number is a convention and it "
                     "differs between books. This course starts the naturals at `1` and "
                     "nothing later depends on the choice.")),
            ("p", "\"Can be written\" is the operative phrase, exactly as it will be for "
                  "polynomials in course 4. `4` is rational because `4 = 4/1`. `0.25` is "
                  "rational because `0.25 = 1/4`. You do not have to be shown the "
                  "fraction; it has to exist."),
            ("h3", "Decimals tell you which kind you have"),
            ("p", "Every rational number has a decimal expansion that either stops or "
                  "falls into a repeating block, and every such decimal is a rational. An "
                  "irrational number is exactly one whose expansion does neither."),
            ("math", [
                "1/4  =  0.25                 stops",
                "1/3  =  0.333…               repeats, block length 1",
                "3/7  =  0.428571428571…      repeats, block length 6",
                "√2   =  1.41421356…          neither: irrational",
            ]),
            ("p", "The dots are not an approximation. `1/3` <em>is</em> `0.333…` exactly; "
                  "`0.333` is a different number, and a smaller one, because it is "
                  "`333/1000`. Throughout this course the fraction is the number and the "
                  "decimal is a report on it."),
            ("thm", ("There is no rational number whose square is 2",
                     "No integers `p` and `q` with `q ≠ 0` satisfy `(p/q)² = 2`.")),
            ("proof", [
                "Suppose `(p/q)² = 2`, with the fraction already reduced so that `p` and "
                "`q` share no common factor. Multiplying by `q²` gives `p² = 2q²`, so "
                "`p²` is even.",
                "If `p` were odd, say `p = 2k + 1`, then `p² = 4k² + 4k + 1`, which is "
                "odd. So `p` is even: write `p = 2m`.",
                "Then `4m² = 2q²`, so `q² = 2m²`, and by the same argument `q` is even "
                "too. But `p` and `q` share no common factor, and we have just shown they "
                "share the factor 2. The supposition cannot hold.",
            ]),
            ("p", "So the rationals have gaps, and the line does not. That gap is the "
                  "whole reason the real numbers are needed."),
            ("h3", "The line"),
            ("p", "Fix a point for `0` and a length for `1`. Every real number then "
                  "corresponds to exactly one point, and every point to exactly one real "
                  "number. The second half of that sentence is an assumption about the "
                  "reals, not something proved here; constructing the reals so that it "
                  "holds belongs to analysis."),
            ("def", ("Order",
                     "`a &lt; b` means `a` lies to the left of `b` on the line.",
                     "For any two reals exactly one of `a &lt; b`, `a = b`, `a &gt; b` "
                     "holds. And between any two distinct reals there is another one "
                     "&mdash; their average will do &mdash; so no real number has a "
                     "next one. The integers do: after `4` comes `5`.")),
            ("p", "To compare two numbers exactly, put them over a common denominator, or "
                  "square them when both are positive. `1.41` against `√2`: "
                  "`1.41² = 1.9881`, which is less than `2`, so `1.41 &lt; √2`. Squaring "
                  "is safe here only because both numbers are positive &mdash; on "
                  "negatives it reverses the order, since `−3 &lt; −2` but `9 &gt; 4`."),
            ("example", ("Ordering a mixed list",
                         "`−5/4`, `−1.2`, `0.6`, `2/3`, `1.41`, `√2`. Over a common "
                         "denominator `−5/4 = −25/20` and `−1.2 = −24/20`, so `−5/4` is "
                         "the leftmost. Likewise `0.6 = 9/15` and `2/3 = 10/15`. And "
                         "`1.41 &lt; √2` by the squaring test. The order is "
                         "`−5/4 &lt; −1.2 &lt; 0.6 &lt; 2/3 &lt; 1.41 &lt; √2`.")),
        ],
        "lab": ("realline", {
            "mode": "place",
            "panel_title": "Place values on the line",
            "panel_intro": "Type any mixture of whole numbers, fractions, decimals and "
                           "square roots. Every comparison is made exactly rather than by "
                           "rounding, and the count of distinct places is the interesting "
                           "column: the preset `sqrt(2), 2/sqrt(2), sqrt(8)/2` is three "
                           "spellings of one point.",
        }),
        "steps_title": "Deciding where a number goes",
        "steps_intro": "Identify it, then place it. The two jobs use different information.",
        "steps": [
            ("Try to write it as a fraction of integers",
             "If you can, it is rational and its decimal will stop or repeat. The square "
             "root of a whole number is irrational unless that number is a perfect square, "
             "which is what settles `√2` and `√10`. A radical sign on its own proves "
             "nothing: `√9` is `3`, and `√(4/9)` is `2/3`."),
            ("Use the decimal as evidence, not as the number",
             "A decimal you can see is always a rounding of an irrational and often a "
             "rounding of a rational. It tells you roughly where to look and never "
             "settles a close comparison."),
            ("Compare exactly",
             "For fractions, a common denominator. For positive square roots, square both "
             "sides &mdash; but only when both are positive, because squaring reverses the "
             "order of two negatives."),
            ("Place it, then check the sign",
             "Left of `0` for negatives, right for positives. Among negatives the number "
             "with the larger digits is further left: `−5/4` sits left of `−1.2`."),
        ],
        "worked": {
            "title": "Six numbers, sorted exactly",
            "intro": ["No decimal is trusted beyond the digits it actually has."],
            "lines": [
                "values    −5/4,  −1.2,  0.6,  2/3,  1.41,  √2",
                "",
                "the two negatives",
                "    −5/4 = −25/20      −1.2 = −6/5 = −24/20",
                "    −25/20 < −24/20    so  −5/4 < −1.2",
                "",
                "the two near 0.6",
                "    0.6 = 3/5 = 9/15   2/3 = 10/15",
                "    9/15 < 10/15       so  0.6 < 2/3",
                "",
                "1.41 against √2        both positive, so square both",
                "    1.41² = 1.9881     (√2)² = 2",
                "    1.9881 < 2         so  1.41 < √2",
                "",
                "order     −5/4 < −1.2 < 0.6 < 2/3 < 1.41 < √2",
            ],
            "after": [
                "Only one of these six is irrational. The other five are fractions, and "
                "every comparison between them was settled by a common denominator rather "
                "than by a decimal.",
                "The squaring step is the one with a condition attached. It compared `1.41` "
                "and `√2` correctly because both are positive. Applied to `−5/4` and "
                "`−1.2` it would give `25/16 &gt; 36/25` and suggest the wrong order, so "
                "the negatives were handled by the denominator instead.",
            ],
        },
        "quiz_title": "Which number, and where",
        "quiz": [
            {"q": "Which of these is irrational?",
             "a": ["`0.375`", "`√9`", "`√10`", "`22/7`"],
             "c": 2,
             "why": "`10` is not a perfect square, so `√10` has no fractional form. `√9` "
                    "is `3` &mdash; a radical sign does not make a number irrational. "
                    "`0.375` is `3/8`, and `22/7` is a fraction of integers, so both are "
                    "rational; `22/7` is an approximation to `π`, not `π`."},
            {"q": "Which statement about `1.414` and `√2` is true?",
             "a": ["They are equal", "`1.414 &gt; √2`", "`1.414 &lt; √2`",
                   "A decimal cannot be compared with a square root"],
             "c": 2,
             "why": "Both are positive, so square them: `1.414² = 1.999396`, which is less "
                    "than `2`. They agree to three decimal places and are different "
                    "numbers, which is exactly why the comparison is made exactly rather "
                    "than by eye."},
            {"q": "How many real numbers lie strictly between `1/3` and `1/2`?",
             "a": ["None", "One", "Finitely many", "Infinitely many"],
             "c": 3,
             "why": "The average `5/12` lies between them, and the same argument applies "
                    "again to `1/3` and `5/12`, without end. Between any two distinct "
                    "reals there is another, which is why no real number has a next one."},
        ],
        "mistakes": [
            ("Treating a rounded decimal as the number itself",
             "`1/3` is not `0.333`. `0.333` is `333/1000`, which is smaller. Rounding is "
             "a report on a number, and a comparison decided by a report is a guess."),
            ("Assuming a radical sign means irrational",
             "`√9 = 3` and `√(4/9) = 2/3`, both rational. The root is irrational only "
             "when the radicand is not a perfect square of a rational, which is lesson 7's "
             "subject."),
            ("Ordering negatives by their digits",
             "`5/4` is larger than `1.2`, and `−5/4` is <em>smaller</em> than `−1.2`. "
             "Adding a minus sign reflects the line, so the order of the two numbers "
             "reverses with it."),
        ],
        "standard": ("Finish when you can order a mixed list of fractions, decimals and roots without a calculator.",
                     "Given `−5/4`, `0.6`, `2/3` and `√2` you should reach for a common "
                     "denominator or for squaring, not for a decimal expansion, and you "
                     "should be able to say which entries are rational and why. That habit "
                     "is what makes lesson 7 &mdash; where `√72` becomes `6√2` &mdash; an "
                     "exact calculation rather than an approximate one."),
        "note": "The line reappears twice on this course. Lesson 4 measures distance along "
                "it, which is what absolute value is, and course 3 crosses two copies of "
                "it to get the coordinate plane. Nothing about it is decorative: `a &lt; b` "
                "means one point is left of another, and every inequality you solve in "
                "course 2 is a statement about a stretch of this line.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "properties-of-the-real-numbers",
        "title": "Properties of the Real Numbers",
        "module": "The number system",
        "one_line": "Commutativity, associativity, distribution, identities, inverses.",
        "summary": (
            "Five properties are all the licence you have to rearrange an expression, and "
            "everything later in this path is one of them applied to a longer expression. "
            "Subtraction and division have none of them, and that omission is where most "
            "sign errors come from."
        ),
        "key": [
            "a + b  =  b + a                 commutative",
            "(a + b) + c  =  a + (b + c)     associative",
            "a(b + c)  =  ab + ac            distributive",
            "a + 0 = a,   a · 1 = a          identities",
        ],
        "key_label": "The properties you are allowed to use",
        "concepts_intro": (
            "A property is not a fact about one sum. It is a permission, granted for every "
            "pair of real numbers at once, and that is what makes it usable on a letter."
        ),
        "concepts": [
            ("A property is a licence, not an observation",
             "`3 + 5 = 5 + 3` is arithmetic; you can check it. `a + b = b + a` for every "
             "pair of reals is the property, and it is what lets you reorder `x + 7` into "
             "`7 + x` when you have no idea what `x` is."),
            ("Distribution is the only one that mixes the two operations",
             "Commutativity and associativity each talk about one operation on its own. "
             "Distribution is the bridge between addition and multiplication, and every "
             "expansion, every collection of like terms and every sign that reaches "
             "through a bracket is that one property."),
            ("Subtraction and division have none of these",
             "`7 − 3` is not `3 − 7`, and `(24 / 4) / 2` is `3` while `24 / (4 / 2)` is "
             "`12`. The repair is to stop treating them as operations: subtracting is "
             "adding the negative, dividing is multiplying by the reciprocal. Once "
             "rewritten, every property applies again."),
        ],
        "read_title": "The rules you are permitted to use",
        "read_intro": "Five properties, stated and not proved, and then the ones people invent because they look similar.",
        "body": [
            ("p", "These properties are assumed. This course states them and uses them; "
                  "building the real numbers so that they hold is a different subject. "
                  "What matters here is knowing precisely what each one says, because "
                  "anything beyond that is not licensed."),
            ("def", ("Commutative properties",
                     "For all reals `a` and `b`: `a + b = b + a` and `ab = ba`.",
                     "Order does not matter &mdash; for addition and for multiplication, "
                     "and for nothing else.")),
            ("def", ("Associative properties",
                     "For all reals `a`, `b`, `c`: `(a + b) + c = a + (b + c)` and "
                     "`(ab)c = a(bc)`.",
                     "Grouping does not matter, which is why `a + b + c` can be written "
                     "with no brackets at all and still name one number.")),
            ("p", "Taken together those two say that a sum of any number of terms may be "
                  "added in any order and any grouping. That is the entire justification "
                  "for \"collect the `x` terms\" in lesson 11 &mdash; you are moving terms "
                  "past each other, and commutativity and associativity are the permission "
                  "to do it."),
            ("def", ("Distributive property",
                     "For all reals `a`, `b`, `c`: `a(b + c) = ab + ac`, and equally "
                     "`(b + c)a = ba + ca`.",
                     "Read left to right it expands a bracket. Read right to left it "
                     "factors one out. Both directions are used constantly, and they are "
                     "the same statement.",
                     "This is also the property that makes `−(x − 3)` equal `−x + 3`. "
                     "Writing the minus as `(−1) ·` turns it into a distribution: "
                     "`(−1)(x) + (−1)(−3) = −x + 3`. Nothing is remembered; both signs are "
                     "computed.")),
            ("h3", "Identities and inverses"),
            ("def", ("Identities",
                     "`a + 0 = a` for every real `a`, and `a · 1 = a` for every real `a`.",
                     "`0` is the additive identity and `1` the multiplicative identity. "
                     "Multiplying by `1` in a chosen disguise &mdash; by `3/3`, say "
                     "&mdash; is how every common denominator in course 2 is built.")),
            ("def", ("Inverses",
                     "Every real `a` has an additive inverse `−a` with `a + (−a) = 0`. "
                     "Every real `a` <em>except</em> `0` has a multiplicative inverse "
                     "`1/a` with `a · (1/a) = 1`.",
                     "That single exclusion is the reason division by zero is undefined. "
                     "It is not a rule imposed on top; there is simply no number that "
                     "works.")),
            ("thm", ("Multiplying by zero",
                     "`a · 0 = 0` for every real `a`.",
                     "This is not one of the assumed properties. It follows from them, "
                     "which is worth seeing once.")),
            ("proof", [
                "`0 = 0 + 0`, by the additive identity. So `a · 0 = a · (0 + 0)`, and by "
                "distribution `a · 0 = a · 0 + a · 0`.",
                "Add the additive inverse of `a · 0` to both sides. The left becomes `0` "
                "and the right becomes `a · 0`. So `a · 0 = 0`.",
            ]),
            ("p", "That theorem is why `0` has no reciprocal: `0 · x` is `0` for every `x` "
                  "and so is never `1`. It is also the engine of every quadratic you "
                  "solve in course 6, where a product being zero forces one of its factors "
                  "to be zero."),
            ("h3", "Properties that do not exist"),
            ("p", "The errors in this course are almost all invented properties &mdash; "
                  "rules that have the shape of a real one. Each is killed by a single "
                  "pair of numbers:"),
            ("ul", [
                "`a(bc) = (ab)(ac)` is false. At `a = 2, b = 3, c = 4` the left side is "
                "`24` and the right side is `48`. Multiplication does not distribute over "
                "multiplication.",
                "`√(a + b) = √a + √b` is false. At `a = 4, b = 9` the left side is `√13` "
                "and the right side is `5`, and `5² = 25`, not `13`.",
                "`1/(a + b) = 1/a + 1/b` is false. At `a = b = 1` the left side is `1/2` "
                "and the right side is `2`.",
            ]),
            ("p", "One counterexample is a complete disproof, and it costs about ten "
                  "seconds. Whenever you are unsure whether a rearrangement is legal, put "
                  "small numbers in both sides. It will not tell you that a rule is true, "
                  "but it will tell you when one is false, and that is the direction the "
                  "errors run."),
            ("example", ("Every step named",
                         "`2(x + 5) + 3x` becomes `(2x + 10) + 3x` by distribution, then "
                         "`10 + (2x + 3x)` by commutativity and associativity of addition, "
                         "then `10 + (2 + 3)x` by distribution read backwards, and finally "
                         "`10 + 5x`. Four lines, four named properties, no invention.")),
        ],
        "lab": ("expression", {
            "mode": "property",
            "panel_title": "Test a claim on your own numbers",
            "panel_intro": "Enter values for `a`, `b` and `c`. Every claim in the list is "
                           "evaluated on your three numbers and then searched over 512 "
                           "further triples for a counterexample. Some of the claims are "
                           "not laws, and the lab has not been told which.",
        }),
        "steps_title": "Justifying a rearrangement",
        "steps_intro": "The goal is not the answer. It is being able to say why each line follows from the one above.",
        "steps": [
            ("Rewrite subtraction and division out of the way",
             "`a − b` becomes `a + (−b)`; `a / b` becomes `a · (1/b)` for `b ≠ 0`. Until "
             "you do this, no commutative or associative property applies, and the "
             "temptation to use one anyway is where the sign errors start."),
            ("Change one thing per line",
             "Reorder, or regroup, or distribute &mdash; not two at once. A line that does "
             "three things is a line you cannot check and cannot name."),
            ("Name the property",
             "Say which of the five you used. If you cannot name it, you have either "
             "invented a rule or done arithmetic, and it matters which."),
            ("Test on numbers when unsure",
             "Substitute small values into the expression you started with and the one you "
             "finished with. They must agree. Disagreement locates the illegal step; "
             "agreement is evidence, not proof."),
        ],
        "worked": {
            "title": "Simplifying, with every property named",
            "intro": ["`5 − 2(x − 3)`. The answer is short; the point is the column on the "
                      "right."],
            "lines": [
                "5 − 2(x − 3)",
                "",
                "  = 5 + (−2)(x − 3)              subtraction is adding the negative",
                "",
                "  = 5 + [(−2)(x) + (−2)(−3)]     distributive",
                "",
                "  = 5 + (−2x + 6)                arithmetic:  (−2)(−3) = 6",
                "",
                "  = 5 + (6 + (−2x))              commutative (addition)",
                "",
                "  = (5 + 6) + (−2x)              associative (addition)",
                "",
                "  = 11 − 2x                      arithmetic",
            ],
            "after": [
                "The sign on the `6` was computed by distribution, not recalled. That is "
                "the difference between this and the common wrong answer `−1 − 2x`, which "
                "comes from taking `(−2)(−3)` to be `−6` and finishing `5 − 6 − 2x`. At "
                "`x = 4` that gives `−9` rather than `3`.",
                "Check by substitution. At `x = 4` the original is `5 − 2(4 − 3) = 3`, and "
                "the answer is `11 − 8 = 3`. Agreement at one value does not prove the two "
                "expressions are equal everywhere &mdash; the named steps do that &mdash; "
                "but disagreement would have proved they are not.",
            ],
        },
        "quiz_title": "Name the property",
        "quiz": [
            {"q": "Which property justifies `3 + (x + 7) = (3 + x) + 7`?",
             "a": ["Commutative property of addition", "Associative property of addition",
                   "Distributive property", "Additive identity"],
             "c": 1,
             "why": "The three quantities appear in the same order on both sides; only the "
                    "bracketing moved, which is associativity. Commutativity would have "
                    "changed the order, and nothing here was expanded or added to zero."},
            {"q": "`(8 − 3) − 2 = 3` and `8 − (3 − 2) = 7`. What does that pair show?",
             "a": ["Subtraction is commutative", "Subtraction is associative",
                   "Subtraction is not associative", "The order of operations was applied wrongly"],
             "c": 2,
             "why": "Same numbers, same order, different grouping, different answers "
                    "&mdash; so grouping matters and subtraction is not associative. "
                    "Rewriting as `8 + (−3) + (−2)` restores associativity, because "
                    "addition has it."},
            {"q": "Why does `0` have no multiplicative inverse?",
             "a": ["Because `0/0 = 1`",
                   "Because `0 · x = 0` for every real `x`, so no `x` gives `1`",
                   "Because `0` is not a real number",
                   "Because `0` is neither positive nor negative"],
             "c": 1,
             "why": "An inverse of `0` would have to satisfy `0 · x = 1`, and the theorem "
                    "above says the left side is `0` whatever `x` is. `0` is a real number, "
                    "and `0/0` is undefined rather than `1`. Being neither positive nor "
                    "negative is beside the point &mdash; `−1` is negative and has the "
                    "inverse `−1`."},
        ],
        "mistakes": [
            ("Reordering across a subtraction sign",
             "`5 − x` is not `x − 5`. Commutativity is a property of addition, and "
             "subtraction does not have it. Write `5 + (−x)` and then the reordering to "
             "`(−x) + 5` is legal, which is `−x + 5`."),
            ("Distributing over a product",
             "`a(bc)` is `abc`, not `(ab)(ac)`. At `a = 2, b = 3, c = 4` those are `24` "
             "and `48`. Distribution crosses from multiplication to addition and nowhere "
             "else."),
            ("Letting a minus sign reach only the first term",
             "`−(x − 3)` is `−x + 3`, not `−x − 3`. The `−1` multiplies every term inside "
             "the bracket, and `(−1)(−3) = 3`. This one error will outnumber all the "
             "others in the next two courses."),
        ],
        "standard": ("Finish when you can name the property behind every line of a rearrangement.",
                     "Take a short simplification and annotate it, one property per line, "
                     "with \"arithmetic\" allowed as a label for the steps that are just "
                     "numbers. When you meet an unfamiliar manipulation later, this is the "
                     "test you apply to it: which of the five is that, and if it is none "
                     "of them, why is it allowed?"),
        "note": "Lesson 10 does nothing but the distributive property, at length, and "
                "lesson 11 does it backwards. It is worth being fluent here first, because "
                "an error made in a property is invisible &mdash; the result still looks "
                "like algebra, and only substituting a number reveals it.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "order-of-operations",
        "title": "Order of Operations",
        "module": "The number system",
        "one_line": "One expression, one value, and the convention that guarantees it.",
        "summary": (
            "Written arithmetic is ambiguous until a reading order is fixed. The order "
            "everybody uses is a convention, not a theorem, and the two places it is "
            "misremembered are same-level operations and the base of an exponent."
        ),
        "key": [
            "1   brackets, innermost first",
            "2   exponents",
            "3   multiplication and division    left to right, one level",
            "4   addition and subtraction       left to right, one level",
        ],
        "key_label": "The convention, in four levels",
        "concepts_intro": (
            "Nothing in this lesson is a fact about numbers. All of it is a fact about "
            "notation, and it is agreed rather than discovered."
        ),
        "concepts": [
            ("The order is a convention, and it is arbitrary",
             "`2 + 3 · 4` could mean `20` or `14`, and both readings are coherent. The "
             "world settled on `14`. Nothing forced that choice; what matters is that "
             "every book, calculator and piece of software makes the same one, so an "
             "expression names a single number."),
            ("Same level means left to right",
             "Multiplication and division are one level, not two. So are addition and "
             "subtraction. `8 − 3 + 2` is `7`, and `24 / 4 / 2` is `3`. The familiar "
             "acronyms list the four operations separately and quietly suggest an order "
             "between them that does not exist."),
            ("Brackets are the override, and some are invisible",
             "Anything you want evaluated first goes in brackets. A fraction bar brackets "
             "its whole numerator and its whole denominator, and a radical sign brackets "
             "everything under it &mdash; which is why typing a printed fraction onto one "
             "line changes its value unless you add the brackets back."),
        ],
        "read_title": "One reading order, and where it is misread",
        "read_intro": "The four levels, the two operations that share a level, and the two things that look like grouping symbols because they are.",
        "body": [
            ("p", "`2 + 3 · 4` has to mean something definite or algebra cannot start. "
                  "Read strictly left to right it is `20`; read with multiplication first "
                  "it is `14`. The convention picks the second, and the reason is "
                  "convenience rather than truth: it lets a polynomial like `3x² + 5x + 7` "
                  "be written without a single bracket."),
            ("def", ("Order of operations",
                     "Evaluate in this order: brackets first, innermost outward; then "
                     "exponents; then multiplication and division together, left to right; "
                     "then addition and subtraction together, left to right.",
                     "Levels 3 and 4 each contain two operations, and within a level the "
                     "rule is position, not the kind of operation.")),
            ("h3", "Within a level, left to right"),
            ("math", [
                "8 − 3 + 2   =  (8 − 3) + 2   =  7        not  8 − (3 + 2) = 3",
                "",
                "24 / 4 / 2  =  (24 / 4) / 2  =  3        not  24 / (4 / 2) = 12",
            ]),
            ("p", "Both wrong readings come from treating the last-named operation as the "
                  "one to do first. Addition does not outrank subtraction and "
                  "multiplication does not outrank division; they are read in the order "
                  "they are written."),
            ("h3", "The base of an exponent"),
            ("p", "An exponent applies to the smallest thing written immediately before "
                  "it. A minus sign written in front is not part of that thing unless "
                  "brackets say so."),
            ("math", [
                "−3²    =  −(3²)      =  −9",
                "(−3)²  =  (−3)(−3)   =   9",
            ]),
            ("p", "This is not a trick question and it is not a disagreement between "
                  "sources; it follows from the exponent level coming before any "
                  "multiplication, and `−3²` is `(−1) · 3²`. The practical consequence "
                  "arrives in lesson 12: when you substitute a negative value for a "
                  "letter, write brackets round it. `x²` at `x = −3` is `(−3)² = 9`."),
            ("h3", "The brackets you cannot see"),
            ("p", "A fraction bar groups everything above it and everything below it. When "
                  "the same expression is typed on one line, those groupings have to be "
                  "written as brackets or the value changes:"),
            ("math", [
                "  2 + 4",
                "  -----   =  (2 + 4) / (3 − 1)  =  6 / 2  =  3",
                "  3 − 1",
                "",
                "typed as  2 + 4 / 3 − 1  it means",
                "    2 + 4/3 − 1  =  (2 − 1) + 4/3  =  1 + 4/3  =  7/3",
            ]),
            ("p", "A radical sign groups in the same way. `√(9 + 16)` is `√25 = 5`, while "
                  "`√9 + √16` is `3 + 4 = 7`. The bar over the radicand is a bracket "
                  "drawn differently."),
            ("example", ("All four levels in one expression",
                         "`2 · (3 + 4)² − 10 / 5`. The bracket gives `7`; the exponent "
                         "gives `49`; at level 3, `2 · 49 = 98` and `10 / 5 = 2`; at level "
                         "4, `98 − 2 = 96`.")),
        ],
        "lab": ("expression", {
            "mode": "order",
            "panel_title": "Watch the queue build",
            "panel_intro": "Type an expression in numbers only. The lab builds the queue of "
                           "pending operations before evaluating anything and names the "
                           "rule behind each step, then shows what a straight left-to-right "
                           "reading would have given, so you can see which expressions the "
                           "convention actually decides.",
        }),
        "steps_title": "Evaluating an expression",
        "steps_intro": "Rewrite the whole expression after each step. Working in your head across two levels is where the value gets lost.",
        "steps": [
            ("Finish the innermost bracket",
             "Find the bracket with no brackets inside it and evaluate it completely, then "
             "rewrite the expression without it. Repeat outward. Treat a fraction bar and "
             "a radical sign as brackets while you do this."),
            ("Take the exponents, reading the base carefully",
             "The base is the smallest thing the exponent is written on. `−3²` has base "
             "`3`; `(−3)²` has base `−3`. These are `−9` and `9`."),
            ("Multiplication and division, left to right",
             "One level. Sweep from the left and do whichever of the two you meet first. "
             "Do not do all the multiplications and then all the divisions."),
            ("Addition and subtraction, left to right",
             "One level again, and the same sweep. `20 − 3 + 1` is `18`; grouping it as "
             "`20 − (3 + 1)` gives `16` and is a misreading."),
        ],
        "worked": {
            "title": "One expression, every level used",
            "intro": ["`20 − 2 · (5 − 8)² / 6 + 1`, rewritten in full at each stage."],
            "lines": [
                "20 − 2 · (5 − 8)² / 6 + 1",
                "",
                "brackets      5 − 8  =  −3",
                "              20 − 2 · (−3)² / 6 + 1",
                "",
                "exponents     (−3)²  =  9        the brackets are written, so the base is −3",
                "              20 − 2 · 9 / 6 + 1",
                "",
                "× and /       left to right:   2 · 9  =  18",
                "                               18 / 6  =  3",
                "              20 − 3 + 1",
                "",
                "+ and −       left to right:   20 − 3  =  17",
                "                               17 + 1  =  18",
                "",
                "answer        18",
            ],
            "after": [
                "The last level is where the direction mattered. Reading it as "
                "`20 − (3 + 1)` gives `16`, and that is the single most common way to lose "
                "this expression.",
                "At the third level the direction happened not to matter for these numbers "
                "&mdash; `2 · (9 / 6)` is also `3` &mdash; so this example does not "
                "demonstrate the rule there. `24 / 4 / 2` does: it is `3`, and `24 / (4 / 2)` "
                "is `12`.",
                "Had the expression read `20 − 2 · 5 − 8² / 6 + 1`, the base of the "
                "exponent would be `8` and nothing else, and the answer would be different. "
                "Read the brackets before you read anything else.",
            ],
        },
        "quiz_title": "One value each",
        "quiz": [
            {"q": "Evaluate `8 − 3 + 2`.",
             "a": ["`3`", "`7`", "`13`", "`−3`"],
             "c": 1,
             "why": "Addition and subtraction share a level, so this is `(8 − 3) + 2 = 7`. "
                    "`3` comes from doing the addition first, `8 − (3 + 2)`. `13` comes "
                    "from reading the minus as a plus, and `−3` from reordering across the "
                    "minus sign as `3 + 2 − 8`."},
            {"q": "Evaluate `−4²`.",
             "a": ["`16`", "`−16`", "`−8`", "`8`"],
             "c": 1,
             "why": "The exponent applies to `4` alone, so this is `−(4²) = −16`. `16` is "
                    "the value of `(−4)²`, which is a different expression. `−8` and `8` "
                    "come from reading the exponent as \"times two\" rather than as a "
                    "square."},
            {"q": "Evaluate `2 + 12 / 2 · 3`.",
             "a": ["`20`", "`4`", "`21`", "`7/3`"],
             "c": 0,
             "why": "Level 3 first, left to right: `12 / 2 = 6`, then `6 · 3 = 18`, then "
                    "`2 + 18 = 20`. `4` comes from doing the multiplication before the "
                    "division, `12 / (2 · 3)`. `21` comes from adding first. `7/3` comes "
                    "from reading the whole thing as one fraction, `(2 + 12) / (2 · 3)`."},
        ],
        "mistakes": [
            ("Trusting an acronym over the two-level rule",
             "PEMDAS and BODMAS list four operations in a row, which reads as if "
             "multiplication precedes division and addition precedes subtraction. Neither "
             "is true: `8 − 3 + 2 = 7` and `24 / 4 / 2 = 3`."),
            ("Writing the base of an exponent without its sign",
             "`−3²` is `−9` and `(−3)²` is `9`. When a negative number is substituted for "
             "a letter, the brackets are what carry the sign into the power, and leaving "
             "them out changes the answer rather than the appearance."),
            ("Losing the invisible brackets when a fraction is typed on one line",
             "`(2 + 4) / (3 − 1)` is `3`. Typed as `2 + 4 / 3 − 1` it is `7/3`, because "
             "the bar was grouping both the numerator and the denominator and nothing on "
             "the typed line does."),
        ],
        "standard": ("Finish when your value and a calculator's value agree on the awkward expressions, not just the easy ones.",
                     "Test yourself on `−4²`, `24 / 4 / 2`, `8 − 3 + 2` and any expression "
                     "with a fraction bar in it. Those four shapes account for nearly every "
                     "arithmetic disagreement in the rest of the path, and each one is "
                     "settled by the convention rather than by opinion."),
        "note": "This convention is why a polynomial can be written `3x² + 5x + 7` with no "
                "brackets at all: the exponent level binds before the multiplication level, "
                "which binds before the addition level, so the expression reads as "
                "`(3 · x²) + (5 · x) + 7` without being told to. Every notation you meet "
                "later is built on top of it.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "absolute-value",
        "title": "Absolute Value",
        "module": "The number system",
        "one_line": "Distance from zero, and why the definition has two cases.",
        "summary": (
            "The absolute value of a number is its distance from zero, which is never "
            "negative. Getting that from a formula takes two cases, and the second case "
            "&mdash; where the answer is `−x` &mdash; is the one that has to be read "
            "carefully."
        ),
        "key": [
            "|x|  =    x   when x ≥ 0",
            "         −x   when x < 0",
            "|x − y|  =  the distance from x to y",
            "|−7| = 7,    |0| = 0,    −|−7| = −7",
        ],
        "key_label": "The definition, and what it measures",
        "concepts_intro": (
            "One symbol, one definition, and a single reading error that accounts for most "
            "of the trouble it causes."
        ),
        "concepts": [
            ("The second case is a negation, not a negative",
             "`−x` means the additive inverse of `x`. If `x = −7`, then `−x = 7`. Reading "
             "`−x` as \"a negative number\" makes the definition look as though it "
             "sometimes returns a negative absolute value, which it never does."),
            ("Distance is the meaning; the cases are the machinery",
             "`|x|` is how far `x` is from `0`, and `|x − y|` is how far `x` is from `y`. "
             "Every later use &mdash; the equations and inequalities in course 2, the "
             "error bounds in any applied subject &mdash; reads as a distance."),
            ("An absolute value equation has two solutions, one, or none",
             "`|x| = 3` has two, `|x| = 0` has one, `|x| = −1` has none. Which case you "
             "are in is decided by the number on the right before any algebra happens, and "
             "\"no solution\" is a complete answer."),
        ],
        "read_title": "Distance, written as a formula",
        "read_intro": "The two-case definition, what it guarantees, and how an equation in one absolute value is split.",
        "body": [
            ("p", "How far is `−7` from `0`? Seven. Distance does not carry a sign. So "
                  "there has to be an operation that removes the sign of a number without "
                  "pretending the number was positive all along, and it needs a definition "
                  "that works for a letter whose sign you do not know."),
            ("def", ("Absolute value",
                     "For a real number `x`, `|x| = x` when `x ≥ 0`, and `|x| = −x` when "
                     "`x &lt; 0`.",
                     "The boundary case `x = 0` is assigned to the first line by choice; "
                     "both lines give `0` there, so the choice is harmless.")),
            ("p", "Run it three times. `|5|`: `5 ≥ 0`, so the first line applies and `|5| "
                  "= 5`. `|−5|`: `−5 &lt; 0`, so the second applies and `|−5| = −(−5) = "
                  "5`. `|0|`: the first line, giving `0`."),
            ("p", "The middle one is the whole lesson. The second line does not say the "
                  "answer is negative; it says the answer is the inverse of a negative, "
                  "which is positive. When `x` is a letter you cannot see the sign of, "
                  "that is exactly why both cases have to be carried."),
            ("thm", ("What absolute value guarantees",
                     "`|x| ≥ 0` for every real `x`, and `|x| = 0` only when `x = 0`.")),
            ("proof", [
                "If `x ≥ 0` then `|x| = x ≥ 0`. If `x &lt; 0` then `−x &gt; 0`, so "
                "`|x| = −x &gt; 0`. Every real falls into one of those two cases, so "
                "`|x| ≥ 0` always.",
                "For the second part: the first case gives `0` only at `x = 0`, and the "
                "second case gives a value strictly greater than `0`, so no other `x` "
                "produces `0`.",
            ]),
            ("h3", "Distance between two numbers"),
            ("def", ("Distance",
                     "The distance between reals `a` and `b` is `|a − b|`.",
                     "`|a − b| = |b − a|`, because `b − a = −(a − b)` and a number and its "
                     "inverse have the same absolute value. So it does not matter which "
                     "end you subtract from.")),
            ("math", [
                "|3 − 10|   =  |−7|  =  7",
                "|10 − 3|   =  |7|   =  7",
                "|−2 − 5|   =  |−7|  =  7          −2 and 5 are 7 apart",
            ]),
            ("h3", "Solving an equation with one absolute value"),
            ("p", "Read `|x − a| = c` as \"`x` is at distance `c` from `a`\". On a line "
                  "there are two such points when `c` is positive, one when `c` is zero, "
                  "and none when `c` is negative."),
            ("math", [
                "|x| = 3     →   x = 3  or  x = −3        two solutions",
                "|x| = 0     →   x = 0                    one solution",
                "|x| = −1    →   no solution              |x| is never negative",
            ]),
            ("p", "The two solutions are not optional and neither is the check. The formal "
                  "route splits the equation into the two cases of the definition, and "
                  "that split is exhaustive &mdash; every real `x` satisfies either "
                  "`x − a ≥ 0` or `x − a &lt; 0` &mdash; which is what tells you there are "
                  "no further solutions hiding."),
            ("p", "Absolute value passes through products and quotients but not through "
                  "sums: `|ab| = |a| · |b|` is true for all reals, and `|a + b| = |a| + "
                  "|b|` is not. At `a = 3` and `b = −5`, the left side is `|−2| = 2` and "
                  "the right side is `8`. What is always true is `|a + b| ≤ |a| + |b|`."),
            ("example", ("Reading the centre off the bars",
                         "`|x − 4| = 3` asks for the points 3 away from `4`, namely `1` "
                         "and `7`. `|x + 4| = 3` is `|x − (−4)| = 3`, so the centre is "
                         "`−4` and the points are `−7` and `−1`. The sign inside flips the "
                         "centre, not the distance.")),
        ],
        "lab": ("realline", {
            "mode": "absolute",
            "panel_title": "Both cases, and the equation",
            "panel_intro": "Set `a`, `b` and `c`. The lab applies the two-case definition "
                           "to your `a` and highlights the case that fires, measures the "
                           "distance from `a` to `b`, and solves `|x − a| = c`. Make `c` "
                           "negative and watch the solution count fall to zero.",
        }),
        "steps_title": "Working with an absolute value",
        "steps_intro": "Decide the sign of what is inside the bars. Everything else follows from that.",
        "steps": [
            ("Look at the sign of the contents, not of the whole expression",
             "The definition branches on whether the quantity inside the bars is negative. "
             "`|3 − 10|` is decided by `3 − 10` being `−7`, so the second line applies and "
             "the result is `7`."),
            ("Apply the case that fires",
             "If the contents are `≥ 0`, drop the bars. If they are `&lt; 0`, drop the "
             "bars and negate the whole contents &mdash; every term of them, which is the "
             "distributive law from lesson 2."),
            ("For an equation, check the right-hand side first, then split",
             "If it is negative, there are no solutions and you are finished. If it is "
             "zero, there is one. If it is positive, write the two equations: contents "
             "equal to it, and contents equal to its negative."),
            ("Substitute every candidate back",
             "Put each answer into the original equation, bars and all. The split itself "
             "guarantees you have found all of them; the substitution guarantees each one "
             "is real rather than an arithmetic slip."),
        ],
        "worked": {
            "title": "Solving |x − 4| = 3, two ways",
            "intro": ["The same equation read as a distance and read through the "
                      "definition. The second way is the one that generalises."],
            "lines": [
                "by distance",
                "    |x − 4|  is the distance from x to 4",
                "    3 to the left:   4 − 3  =  1",
                "    3 to the right:  4 + 3  =  7",
                "",
                "by the definition",
                "    case  x − 4 ≥ 0:     x − 4  =  3      →   x = 7",
                "    case  x − 4 < 0:   −(x − 4) =  3",
                "                          x − 4  = −3      →   x = 1",
                "",
                "check",
                "    x = 7:   |7 − 4|  =  |3|   =  3",
                "    x = 1:   |1 − 4|  =  |−3|  =  3",
                "",
                "solutions   x = 1  and  x = 7",
            ],
            "after": [
                "The two checks confirm that `1` and `7` satisfy the equation. They do not, "
                "on their own, say there is nothing else. That comes from the case split: "
                "every real number makes `x − 4` either non-negative or negative, so the "
                "two cases cover all of them and each yielded one value.",
                "Compare with `|x − 4| = −3`. The distance reading kills it immediately "
                "&mdash; no point is at distance `−3` from anything &mdash; and the "
                "definition agrees, since `|x − 4| ≥ 0` for every `x`. Writing \"no "
                "solution\" is the finished answer.",
            ],
        },
        "quiz_title": "Bars and distance",
        "quiz": [
            {"q": "If `x = −7`, what is `−x`?",
             "a": ["`−7`", "`7`", "`0`", "It is undefined"],
             "c": 1,
             "why": "`−x` is the additive inverse of `x`, and the inverse of `−7` is `7`. "
                    "Reading `−x` as \"a negative number\" is what makes the second line of "
                    "the definition look wrong; it is the line that turns a negative input "
                    "into a positive output."},
            {"q": "Solve `|x + 2| = 5`.",
             "a": ["`x = 3` only", "`x = 3` or `x = −7`", "`x = 3` or `x = 7`",
                   "`x = −3` or `x = 7`"],
             "c": 1,
             "why": "`|x + 2|` is `|x − (−2)|`, the distance from `−2`. Five to the right "
                    "is `3`, five to the left is `−7`. `x = 3` alone drops the second "
                    "case. `x = 3` or `x = 7` is `5 ± 2` rather than `−2 ± 5`. And "
                    "`x = −3` or `x = 7` is the solution set of `|x − 2| = 5`, with the "
                    "sign inside the bars misread."},
            {"q": "How many solutions does `|2x − 1| = −4` have?",
             "a": ["None", "One", "Two", "Infinitely many"],
             "c": 0,
             "why": "An absolute value is never negative, so no `x` can make the left side "
                    "`−4`. Splitting into cases before checking the right-hand side "
                    "produces `2x − 1 = 4` and `2x − 1 = −4`, two candidates that both "
                    "fail the original equation."},
        ],
        "mistakes": [
            ("Reading the second line of the definition as producing a negative",
             "`|x| = −x` when `x &lt; 0` gives a positive answer, because `−x` is the "
             "inverse of a negative number. At `x = −7` it reads `|−7| = −(−7) = 7`."),
            ("Keeping only the positive solution",
             "`|x| = 3` has solutions `3` and `−3`. Dropping the second is the same "
             "omission as writing `√` where `±` is needed in course 6, and it loses half "
             "the answer every time."),
            ("Splitting the bars over a sum",
             "`|a + b|` is not `|a| + |b|`. At `a = 3` and `b = −5` those are `2` and `8`. "
             "Products are different: `|ab| = |a| · |b|` really does hold, which is why the "
             "false version looks plausible."),
        ],
        "standard": ("Finish when both cases of the definition are automatic and \"no solution\" is an answer you will write.",
                     "You should be able to evaluate `|3 − 10|` without pausing, say what "
                     "`|x − 4| = 3` means before solving it, and reject `|2x − 1| = −4` on "
                     "sight. Course 2 spends two lessons on absolute value equations and "
                     "inequalities, and both of them assume this one is finished."),
        "note": "The two-case shape returns in course 3 as a piecewise function &mdash; "
                "`|x|` is the standard first example of one &mdash; and again in lesson 7 "
                "here, where `√(x²)` turns out to be `|x|` rather than `x`. The reason is "
                "the same both times: a formula that has to work for inputs of either sign "
                "needs a branch.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "integer-exponents",
        "title": "Integer Exponents",
        "module": "Exponents and radicals",
        "one_line": "The laws, including what a zero and a negative exponent mean.",
        "summary": (
            "Three laws, each of which is counting factors rather than remembering a rule. "
            "A zero exponent and a negative exponent are then defined &mdash; not derived "
            "&mdash; and the definitions are chosen as the only ones that keep the three "
            "laws true for every integer."
        ),
        "key": [
            "xᵐ · xⁿ  =  xᵐ⁺ⁿ           exponents add",
            "xᵐ / xⁿ  =  xᵐ⁻ⁿ           exponents subtract",
            "(xᵐ)ⁿ  =  xᵐⁿ              exponents multiply",
            "x⁰ = 1   and   x⁻ⁿ = 1/xⁿ  both require x ≠ 0",
        ],
        "key_label": "Three laws and two definitions",
        "concepts_intro": (
            "The laws are short enough to memorise and short enough to rederive. Rederiving "
            "them is better, because it also tells you when they do not apply."
        ),
        "concepts": [
            ("The laws are counting, not memory",
             "`x² · x³` is two `x`s multiplied by three `x`s, which is five `x`s. If you "
             "cannot recall whether the exponents add or multiply, write the factors out "
             "for a small case and read the answer off."),
            ("x⁰ and x⁻ⁿ are choices, made to keep the laws",
             "\"Multiply `x` by itself zero times\" is not a meaningful instruction. The "
             "quotient law is what forces the value: extended to equal exponents it makes "
             "`x³ / x³` into `x⁰`, and arithmetic makes it `1`, so `x⁰` must be `1`. The "
             "definition is designed backwards from the law it has to preserve."),
            ("Every law is about a single base",
             "`x² · y³` does not combine, and `2³ · 3²` is `72` &mdash; a number, not a "
             "power of anything you can read off. The laws move exponents around when the "
             "base is the same and say nothing otherwise."),
        ],
        "read_title": "Three laws, then two definitions",
        "read_intro": "Where each law comes from, why zero and negative exponents have the values they do, and where the distribution stops.",
        "body": [
            ("def", ("Power with a positive integer exponent",
                     "For an integer `n ≥ 1`, `xⁿ` means the product of `n` factors of "
                     "`x`. `x` is the <strong>base</strong> and `n` is the "
                     "<strong>exponent</strong>.",
                     "`x¹ = x`. Note that this definition says nothing at all about `n = "
                     "0` or `n` negative; those cases are handled below, and they have to "
                     "be handled separately.")),
            ("h3", "The three laws, from counting factors"),
            ("thm", ("Product, quotient and power laws",
                     "For a base `x` and positive integers `m` and `n`: "
                     "`xᵐ · xⁿ = xᵐ⁺ⁿ`; `xᵐ / xⁿ = xᵐ⁻ⁿ` when `x ≠ 0` and `m &gt; n`; "
                     "and `(xᵐ)ⁿ = xᵐⁿ`.")),
            ("proof", [
                "The first: `xᵐ` is `m` factors and `xⁿ` is `n` factors, so their product "
                "is `m + n` factors, which is `xᵐ⁺ⁿ`.",
                "The second: in `xᵐ / xⁿ` each of the `n` factors below cancels one of the "
                "`m` above, leaving `m − n` factors.",
                "The third: `(xᵐ)ⁿ` is `n` copies of a block of `m` factors, so `mn` "
                "factors in all.",
            ]),
            ("math", [
                "x² · x³  =  (x·x)(x·x·x)      =  x⁵",
                "x⁵ / x²  =  (x·x·x·x·x)/(x·x) =  x³",
                "(x²)³    =  (x·x)(x·x)(x·x)   =  x⁶",
            ]),
            ("p", "Two more, and they are the ones that get overextended: "
                  "`(xy)ⁿ = xⁿyⁿ` and `(x/y)ⁿ = xⁿ/yⁿ` for `y ≠ 0`. An exponent "
                  "distributes over a product and over a quotient. It does <em>not</em> "
                  "distribute over a sum: `(x + y)²` is not `x² + y²`, and at `x = 1`, "
                  "`y = 3` those are `16` and `10`."),
            ("h3", "Zero and negative exponents"),
            ("p", "Neither case is covered by the laws as stated, because those were "
                  "proved for positive exponents by counting factors. So ask instead what "
                  "the laws <em>would</em> say if they were extended, and let arithmetic "
                  "say what the value would then have to be:"),
            ("math", [
                "if the quotient law is to hold when the exponents are equal",
                "    x³ / x³  =  x³⁻³  =  x⁰",
                "and arithmetic gives",
                "    x³ / x³  =  1                     for x ≠ 0",
                "so           x⁰  =  1",
                "",
                "if the product law is to hold for a negative exponent",
                "    x³ · x⁻³  =  x³⁺⁽⁻³⁾  =  x⁰  =  1",
                "so            x⁻³  =  1 / x³",
            ]),
            ("def", ("Zero and negative exponents",
                     "For `x ≠ 0` and a positive integer `n`: `x⁰ = 1` and "
                     "`x⁻ⁿ = 1/xⁿ`.",
                     "These are definitions, not consequences. They are the only values "
                     "that keep the three laws true for every integer exponent, which is "
                     "the reason they were chosen. `0⁰` is left undefined on this course, "
                     "because both arguments above need `x ≠ 0`.")),
            ("p", "A negative exponent does not make the value negative. `2⁻³` is `1/8`, a "
                  "positive number. The exponent's sign says which side of the fraction "
                  "bar the power belongs on; the value's sign comes from the base."),
            ("p", "That gives a useful move: a factor may cross the fraction bar if its "
                  "exponent changes sign. `x⁻²/y⁻³` is `y³/x²`. It is not a new rule "
                  "&mdash; it is the definition applied twice."),
            ("example", ("An expression with every law in it",
                         "`(2x⁻³y²)⁻²`. The outer exponent distributes over the product: "
                         "`2⁻² = 1/4`, `(x⁻³)⁻² = x⁶` and `(y²)⁻² = y⁻⁴`. Collecting, that "
                         "is `x⁶ / (4y⁴)`, valid for `x ≠ 0` and `y ≠ 0`.")),
        ],
        "lab": ("exponents", {
            "mode": "laws",
            "panel_title": "Each law, computed twice",
            "panel_intro": "Choose `a`, `b`, `m` and `n`. Every law is evaluated once by "
                           "the law itself and once by writing all the powers out as "
                           "products and multiplying the factors one at a time, so the two "
                           "columns agree only when the law is real. The last row of the "
                           "summary is not a law, and it is on the list to be caught.",
        }),
        "steps_title": "Simplifying a power expression",
        "steps_intro": "Outermost first, then one base at a time, then the negatives. Changing that order is what produces stray factors.",
        "steps": [
            ("Deal with the outermost exponent first",
             "An exponent on a bracket distributes over every factor inside it, including "
             "the numerical one: in `(2x³)⁴` the `2` is raised too, giving `16x¹²`. It "
             "distributes over a quotient as well, and over a sum never."),
            ("Collect one base at a time",
             "Gather all the powers of `x`, then all the powers of `y`, then the plain "
             "numbers. Each base is tracked separately and they never mix, so this turns "
             "one hard problem into three easy ones."),
            ("Convert negative exponents last",
             "Do the arithmetic on the exponents while they are still exponents &mdash; "
             "adding `−6` and `−1` is easier than manipulating two nested fractions. Move "
             "factors across the bar only once the exponents are final."),
            ("State the restrictions",
             "Every quotient law and every negative exponent needs its base to be nonzero. "
             "Writing `x ≠ 0` beside the answer is not pedantry; in course 5 the excluded "
             "values become the first thing you are asked for."),
        ],
        "worked": {
            "title": "One expression, every law used once",
            "intro": ["`(2x³y⁻²)⁻² · (4x⁻¹y³)`, with `x ≠ 0` and `y ≠ 0`."],
            "lines": [
                "(2x³y⁻²)⁻² · (4x⁻¹y³)",
                "",
                "outer exponent, over each factor of the bracket",
                "    2⁻² = 1/4      (x³)⁻² = x⁻⁶      (y⁻²)⁻² = y⁴",
                "    →  (1/4)x⁻⁶y⁴ · 4x⁻¹y³",
                "",
                "the numbers",
                "    (1/4) · 4  =  1",
                "",
                "the x factors",
                "    x⁻⁶ · x⁻¹  =  x⁻⁶⁺⁽⁻¹⁾  =  x⁻⁷",
                "",
                "the y factors",
                "    y⁴ · y³    =  y⁴⁺³      =  y⁷",
                "",
                "    →  x⁻⁷y⁷",
                "",
                "negative exponent last",
                "    x⁻⁷  =  1/x⁷",
                "",
                "answer      y⁷ / x⁷",
            ],
            "after": [
                "Four exponent arithmetics decided the whole thing: `3 · (−2) = −6` and "
                "`(−2)(−2) = 4` inside the first bracket, then `−6 + (−1) = −7` and "
                "`4 + 3 = 7`. Every one of them is signed integer addition or "
                "multiplication, which is why the bracket-and-sign care of lesson 3 "
                "matters here.",
                "Check at `x = 2` and `y = 3`. The first bracket is "
                "`2 · 8 · (1/9) = 16/9`, and `(16/9)⁻² = 81/256`. The second factor is "
                "`4 · (1/2) · 27 = 54`. Their product is `4374/256`, which reduces to "
                "`2187/128`. And `y⁷/x⁷` is `2187/128`. Agreement at one pair of values is "
                "not a proof, but a disagreement would have been decisive.",
            ],
        },
        "quiz_title": "Powers",
        "quiz": [
            {"q": "Simplify `x⁵ · x³`.",
             "a": ["`x¹⁵`", "`x⁸`", "`2x⁸`", "`x²`"],
             "c": 1,
             "why": "Five factors times three factors is eight factors, so the exponents "
                    "add. `x¹⁵` multiplies them, which is the rule for `(x⁵)³`. `2x⁸` adds "
                    "a coefficient that was never there. `x²` subtracts, which is the "
                    "quotient law applied to a product."},
            {"q": "What is `5⁻²`?",
             "a": ["`−25`", "`1/25`", "`−1/25`", "`1/10`"],
             "c": 1,
             "why": "`5⁻² = 1/5² = 1/25`. The minus sign in the exponent moves the power "
                    "below the bar; it does not move to the value. `−25` and `−1/25` both "
                    "read it as a sign, and `1/10` reads the exponent as a multiplier."},
            {"q": "Which expression equals `(2x)³`?",
             "a": ["`2x³`", "`8x³`", "`6x³`", "`2x⁶`"],
             "c": 1,
             "why": "The exponent distributes over the whole product: `(2x)³ = 2³x³ = "
                    "8x³`. `2x³` raises only the `x`, which is what `2 · x³` means. `6x³` "
                    "multiplies the `2` by the exponent, and `2x⁶` multiplies the "
                    "exponents."},
        ],
        "mistakes": [
            ("Multiplying the exponents when the bases are multiplied",
             "`x² · x³ = x⁵`, not `x⁶`. Exponents multiply for a power of a power, "
             "`(x²)³ = x⁶`, and the two rules get swapped under pressure. Writing out "
             "`(x·x)(x·x·x)` settles it in five seconds."),
            ("Applying a law across two different bases",
             "`2³ · 3²` is `8 · 9 = 72`. There is no law that combines it into a single "
             "power, because every law here begins \"for a base `x`\". Different bases stay "
             "apart."),
            ("Reading a negative exponent as a negative value",
             "`2⁻³` is `1/8`, and `(−2)³` is `−8`. The exponent's sign controls which side "
             "of the fraction bar the power sits on; the base's sign controls whether the "
             "value is negative."),
        ],
        "standard": ("Finish when you can produce x⁰ = 1 from the quotient law instead of recalling it.",
                     "The test is not whether you know the value but whether you can say "
                     "why it has to be that value and where the condition `x ≠ 0` comes "
                     "from. Lesson 8 asks the same question about `x^(1/n)` and answers it "
                     "the same way, so the argument is worth having in hand rather than the "
                     "conclusion."),
        "note": "Lesson 6 uses these laws on powers of ten and nothing else, which makes "
                "them concrete. Lesson 8 pushes the exponent out of the integers "
                "altogether: if `x^(1/2) · x^(1/2)` is to equal `x¹`, then `x^(1/2)` has no "
                "choice but to be a square root. Every extension of the exponent on this "
                "path is made by that same argument.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "scientific-notation",
        "title": "Scientific Notation",
        "module": "Exponents and radicals",
        "one_line": "Writing very large and very small numbers, and computing with them.",
        "summary": (
            "One digit before the point, a power of ten behind it. The form makes two "
            "numbers comparable at a glance and turns multiplication into an addition of "
            "exponents; addition is the operation it does not simplify, and that is worth "
            "knowing before you attempt one."
        ),
        "key": [
            "a × 10ⁿ          1 ≤ |a| < 10,  n an integer",
            "93000    =  9.3 × 10⁴",
            "0.00072  =  7.2 × 10⁻⁴",
            "(a × 10ᵐ)(b × 10ⁿ)  =  ab × 10ᵐ⁺ⁿ",
        ],
        "key_label": "One form, and the arithmetic it makes easy",
        "concepts_intro": (
            "This is the exponent laws of lesson 5, applied to one base, plus a rule about "
            "where the decimal point goes."
        ),
        "concepts": [
            ("The form is a normalisation, so two numbers can be compared at a glance",
             "Exactly one nonzero digit in front of the point. Two numbers in this form "
             "are compared by their exponents first, and only by their mantissas if the "
             "exponents tie &mdash; which is why `8.9 × 10⁻⁵` is smaller than "
             "`1.2 × 10⁻⁴` despite the larger-looking front."),
            ("The exponent counts places, and its sign says which way",
             "A positive exponent moves the point right and makes the number bigger; a "
             "negative one moves it left. \"`n` zeros\" is a description that works only "
             "when the mantissa is a single digit, and it fails on `9.3 × 10⁵`, which is "
             "`930000`."),
            ("Multiplying is easy, adding is not",
             "Multiply the mantissas and add the exponents. Adding requires both numbers "
             "to carry the same power of ten first, which is the same manoeuvre as finding "
             "a common denominator, and it is the step people skip."),
        ],
        "read_title": "The form, and computing in it",
        "read_intro": "What normalised means, how to convert either way, and why one of the four operations behaves differently from the others.",
        "body": [
            ("p", "`602000000000000000000000` and `0.00000000000000000016` are unreadable, "
                  "and the failure is not aesthetic: nobody can count 21 zeros reliably, so "
                  "the notation itself introduces errors. Scientific notation replaces the "
                  "zeros with a number."),
            ("def", ("Scientific notation",
                     "A number is in <strong>scientific notation</strong> when it is "
                     "written `a × 10ⁿ` with `1 ≤ |a| &lt; 10` and `n` an integer. `a` is "
                     "the <strong>mantissa</strong> and `n` the exponent.",
                     "`0` has no such form, since no mantissa with `|a| ≥ 1` can produce "
                     "it. Every other real number has exactly one.")),
            ("p", "`12.5 × 10³` is a perfectly correct way to write `12500`, and it is not "
                  "in scientific notation, because `12.5` is not below `10`. Those are two "
                  "different criticisms and only the second one applies. Renormalised it "
                  "is `1.25 × 10⁴`, and the value never changed."),
            ("h3", "Converting"),
            ("p", "Move the decimal point until exactly one nonzero digit stands in front "
                  "of it, count the places you moved, and that count is the exponent. "
                  "Moving left raises the exponent; moving right lowers it."),
            ("math", [
                "93000    →  9.3      point moved 4 places left       9.3 × 10⁴",
                "0.00072  →  7.2      point moved 4 places right      7.2 × 10⁻⁴",
            ]),
            ("p", "Then check the sign against the size of the number rather than against "
                  "your count: anything bigger than `1` has `n ≥ 0`, and anything strictly "
                  "between `0` and `1` has `n &lt; 0`. That single check catches a reversed "
                  "sign every time, and a reversed sign is the error of the lesson."),
            ("h3", "Multiplying and dividing"),
            ("p", "Mantissas multiply, exponents add &mdash; the product law of lesson 5 "
                  "with base `10`. For division, mantissas divide and exponents subtract."),
            ("math", [
                "(3 × 10⁸)(2 × 10⁻³)      =  (3·2) × 10⁸⁺⁽⁻³⁾   =  6 × 10⁵",
                "",
                "(9.9 × 10³) / (2 × 10²)  =  (9.9/2) × 10³⁻²    =  4.95 × 10¹",
            ]),
            ("p", "The result may not be normalised, and that is expected rather than "
                  "wrong. If the mantissa reaches `10`, move the point one place left and "
                  "add one to the exponent; if it falls below `1`, move it right and "
                  "subtract one. `(5 × 10⁻⁷)(2 × 10⁻³)` is `10 × 10⁻¹⁰`, which "
                  "renormalises to `1 × 10⁻⁹`."),
            ("h3", "Adding"),
            ("p", "Addition needs a shared power of ten before the mantissas can be "
                  "touched at all:"),
            ("math", [
                "1.2 × 10⁵ + 3.4 × 10⁴",
                "    =  1.2 × 10⁵ + 0.34 × 10⁵",
                "    =  (1.2 + 0.34) × 10⁵",
                "    =  1.54 × 10⁵",
            ]),
            ("p", "The rewritten term `0.34 × 10⁵` is not in scientific notation and does "
                  "not need to be; it is an intermediate line. Only the final answer is "
                  "held to the form."),
            ("example", ("A quantity you cannot write out",
                         "One electron carries about `1.6 × 10⁻¹⁹` coulombs, so one coulomb "
                         "is `1 / (1.6 × 10⁻¹⁹)` electrons. The mantissas give "
                         "`1/1.6 = 0.625` and the exponents give `0 − (−19) = 19`, so the "
                         "answer is `0.625 × 10¹⁹`, renormalised to `6.25 × 10¹⁸`.")),
        ],
        "lab": ("exponents", {
            "mode": "scientific",
            "panel_title": "Two numbers, one operation",
            "panel_intro": "Enter two mantissas and two powers of ten, and pick an "
                           "operation. Both inputs are normalised first &mdash; `45.6` and "
                           "`0.004` are accepted and corrected &mdash; and the result is "
                           "checked against the same calculation performed on the plain "
                           "numbers.",
        }),
        "steps_title": "Putting a number into the form",
        "steps_intro": "Four moves, and the fourth is the one that catches a reversed sign.",
        "steps": [
            ("Find the first nonzero digit",
             "Leading zeros are placeholders and are not part of the mantissa. In "
             "`0.00072` the first nonzero digit is the `7`, and in `93000` it is the `9`."),
            ("Put the point immediately after it",
             "That produces the mantissa: `7.2` and `9.3`. Trailing zeros after the last "
             "nonzero digit are dropped unless you are deliberately recording precision."),
            ("Count the places the point moved",
             "The count is the size of the exponent. Four places in both examples above, "
             "in opposite directions."),
            ("Fix the sign by the size of the number",
             "Bigger than `1` means a positive exponent, between `0` and `1` means a "
             "negative one. Then confirm the mantissa satisfies `1 ≤ |a| &lt; 10`, which "
             "is the only condition the form imposes."),
        ],
        "worked": {
            "title": "A product and a quotient, both renormalised",
            "intro": ["The two directions of renormalising, one in each calculation."],
            "lines": [
                "1.  (6.4 × 10⁵) · (5 × 10⁻⁸)",
                "",
                "    mantissas    6.4 · 5    =  32",
                "    exponents    5 + (−8)   =  −3",
                "                 32 × 10⁻³        correct value, mantissa too big",
                "",
                "    renormalise  32  =  3.2 × 10¹",
                "                 3.2 × 10¹ × 10⁻³  =  3.2 × 10⁻²",
                "",
                "    check        640000 · 0.00000005  =  0.032  =  3.2 × 10⁻²",
                "",
                "2.  (1.5 × 10³) / (6 × 10⁷)",
                "",
                "    mantissas    1.5 / 6    =  0.25",
                "    exponents    3 − 7      =  −4",
                "                 0.25 × 10⁻⁴      correct value, mantissa too small",
                "",
                "    renormalise  0.25  =  2.5 × 10⁻¹",
                "                 2.5 × 10⁻¹ × 10⁻⁴  =  2.5 × 10⁻⁵",
            ],
            "after": [
                "In the first the mantissa was too large and the exponent went up by one; "
                "in the second it was too small and the exponent went down by one. In both "
                "cases the move to the mantissa is paid for by the exponent, which is the "
                "whole content of renormalising.",
                "Neither `32 × 10⁻³` nor `0.25 × 10⁻⁴` is a wrong answer to the arithmetic. "
                "They are the right numbers in the wrong form, and the distinction is worth "
                "keeping: the form is a convention about presentation, and the value is not.",
            ],
        },
        "quiz_title": "Form and arithmetic",
        "quiz": [
            {"q": "Write `0.00046` in scientific notation.",
             "a": ["`4.6 × 10⁻⁴`", "`4.6 × 10⁴`", "`4.6 × 10⁻⁵`", "`4.6 × 10⁻³`"],
             "c": 0,
             "why": "The point moves four places right to reach `4.6`, so the exponent is "
                    "`−4`. `4.6 × 10⁴` is `46000` and has the sign reversed; `4.6 × 10⁻⁵` "
                    "counts one place too many and `4.6 × 10⁻³` one too few. The number is "
                    "below `1`, which fixes the sign before any counting."},
            {"q": "Compute `(4 × 10⁶)(3 × 10⁻²)`, in scientific notation.",
             "a": ["`1.2 × 10⁵`", "`1.2 × 10⁴`", "`7 × 10⁴`", "`12 × 10⁻¹²`"],
             "c": 0,
             "why": "Mantissas multiply to `12`, exponents add to `4`, giving `12 × 10⁴`, "
                    "which renormalises to `1.2 × 10⁵`. `1.2 × 10⁴` moves the point in the "
                    "mantissa without paying for it in the exponent. `7 × 10⁴` adds the "
                    "mantissas and `12 × 10⁻¹²` multiplies the exponents."},
            {"q": "Which of these is the largest number?",
             "a": ["`8.9 × 10⁻⁵`", "`1.2 × 10⁻⁴`", "`9.9 × 10⁻⁶`", "`1.05 × 10⁻⁵`"],
             "c": 1,
             "why": "Compare the exponents first: `−4` beats `−5` and `−6` whatever the "
                    "mantissas are, because every mantissa is below `10`. `9.9 × 10⁻⁶` has "
                    "the biggest mantissa on the list and is the smallest number on it; "
                    "`8.9 × 10⁻⁵` has the second biggest and is only the second largest "
                    "number &mdash; it is `0.89 × 10⁻⁴`."},
        ],
        "mistakes": [
            ("Counting zeros instead of moving the point",
             "`9 × 10⁵` is `9` followed by five zeros, so the shortcut looks reliable. "
             "`9.3 × 10⁵` is `930000`, which is `93` followed by four. Count places moved, "
             "not zeros written."),
            ("Renormalising the mantissa and leaving the exponent alone",
             "`12 × 10⁴` is `1.2 × 10⁵`, not `1.2 × 10⁴`. Dividing the mantissa by ten has "
             "to be repaid by multiplying the power of ten by ten, or the value changes by "
             "a factor of ten."),
            ("Adding the mantissas while the exponents differ",
             "`1.2 × 10⁵ + 3.4 × 10⁴` is `1.54 × 10⁵`, not `4.6 × 10⁵` and not "
             "`4.6 × 10⁹`. Rewrite the smaller number with the larger exponent first; "
             "until the powers of ten match there is nothing the mantissas can be added "
             "across."),
        ],
        "standard": ("Finish when the sign of the exponent is decided by the size of the number, not by your count.",
                     "Convert in both directions without hesitating, multiply and divide by "
                     "handling mantissas and exponents separately, and renormalise a result "
                     "in either direction. The reflex worth building is the last one: look "
                     "at the answer, ask whether the mantissa lies in `[1, 10)`, and fix it "
                     "by moving the exponent."),
        "note": "The split into a mantissa and an exponent is exactly what a calculator "
                "shows as `6.02E23`, and it is the reason logarithms in course 7 turn "
                "multiplication into addition: the exponent of a number in this form is "
                "very nearly its base-10 logarithm, and adding exponents is what you did "
                "here every time you multiplied.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "roots-and-radicals",
        "title": "Roots and Radicals",
        "module": "Exponents and radicals",
        "one_line": "Square roots, n-th roots, and which of them are real.",
        "summary": (
            "A radical sign names one number, not two, and the choice of which one is a "
            "convention worth stating plainly. Whether that number exists at all depends "
            "on the sign of the radicand and on whether the index is even or odd."
        ),
        "key": [
            "√x         the one number r ≥ 0 with r² = x",
            "√9 = 3     not ±3;  x² = 9 has two solutions, √9 names one",
            "√(−4)      no real value;  the 3rd root of −8 is −2",
            "√(x²)  =  |x|          not x",
        ],
        "key_label": "One symbol, one value",
        "concepts_intro": (
            "Most of the difficulty here is notation rather than arithmetic: what the "
            "symbol denotes, and when it denotes nothing."
        ),
        "concepts": [
            ("A radical sign names exactly one number",
             "The equation `x² = 9` has two solutions, `3` and `−3`. The expression `√9` "
             "is a single number, and by convention it is the non-negative one. Confusing "
             "the equation with the symbol is the most common error in the topic, and it "
             "is not an algebra error."),
            ("Odd roots always exist; even roots need a non-negative radicand",
             "An even power of a real number is never negative, so nothing real squares to "
             "`−4` and `√(−4)` has no value on this course. Odd powers keep the sign of "
             "the base, so every real has exactly one real cube root, negatives included."),
            ("Simplifying means removing complete groups",
             "Factor the radicand into primes. For a square root, each pair of equal "
             "primes leaves one factor outside; for an n-th root, each group of `n` does. "
             "What is left under the sign is whatever could not form a full group."),
        ],
        "read_title": "What the symbol denotes, and when it denotes nothing",
        "read_intro": "The principal square root, the general n-th root, why the even case needs absolute value, and how a radical is reduced.",
        "body": [
            ("def", ("Principal square root",
                     "For `x ≥ 0`, `√x` is the unique number `r` with `r ≥ 0` and `r² = x`.",
                     "`√0 = 0`. For `x &lt; 0` there is no real `r` with `r² = x`, because "
                     "the square of any real number is `≥ 0`. On this course such a "
                     "radical has no value and is said to have none; course 6 introduces "
                     "`i` and gives it one.")),
            ("p", "So `√9 = 3`, and `√9 = ±3` is wrong as written. The `±` belongs to "
                  "solving an equation: `x² = 9` gives `x = ±3`, and the `±` is put there "
                  "explicitly because `√` alone would only have supplied the positive "
                  "root. That is also why the quadratic formula in course 6 carries a `±` "
                  "in front of its radical."),
            ("def", ("n-th root",
                     "For an integer `n ≥ 2`, an n-th root of `x` is a number `r` with "
                     "`rⁿ = x`. The `n` is called the <strong>index</strong>.",
                     "When `n` is odd, every real `x` has exactly one real n-th root and "
                     "it has the same sign as `x`. When `n` is even and `x &gt; 0` there "
                     "are two, one positive and one negative, and the radical denotes the "
                     "positive one; when `n` is even and `x &lt; 0` there are none.")),
            ("math", [
                "the 3rd root of   8  =   2          2³  =  8",
                "the 3rd root of  −8  =  −2        (−2)³ = −8",
                "the 4th root of  16  =   2          2⁴  = 16",
                "                                  (−2)⁴ = 16 as well; the radical names 2",
                "the 4th root of −16  =  no real value",
            ]),
            ("h3", "Why the even case needs absolute value"),
            ("p", "`√(x²)` is required to be non-negative, by the definition. At `x = −5`, "
                  "`x²` is `25` and `√25` is `5`, which is `−x` rather than `x`. So the "
                  "cancellation people write as `√(x²) = x` is false for every negative "
                  "`x`:"),
            ("math", [
                "x =  5:   √(5²)    =  √25  =  5  =  |5|",
                "x = −5:   √((−5)²) =  √25  =  5  =  |−5|",
            ]),
            ("p", "The correct statement is `√(x²) = |x|`, which is lesson 4's two-case "
                  "definition arriving from a different direction. For an odd index no "
                  "absolute value is needed: the cube root of `x³` is `x` for every real "
                  "`x`, because a cube keeps the sign."),
            ("h3", "Simplifying a radical"),
            ("thm", ("Product and quotient rules",
                     "For `a ≥ 0` and `b ≥ 0`: `√(ab) = √a · √b`. For `a ≥ 0` and "
                     "`b &gt; 0`: `√(a/b) = √a / √b`.",
                     "Both rules hold for an n-th root as well. For odd `n` no sign "
                     "restriction is needed, since every real has exactly one real odd "
                     "root; for even `n` the radicands must be non-negative, for the same "
                     "reason they must be here.",
                     "There is no corresponding rule for a sum. `√(9 + 16) = √25 = 5`, "
                     "while `√9 + √16 = 7`. The radical sign brackets everything under it, "
                     "exactly as lesson 3 said.")),
            ("p", "To simplify, factor the radicand into primes and take out each prime in "
                  "complete groups of the index &mdash; pairs for a square root, triples "
                  "for a cube root:"),
            ("math", [
                "√72  =  √(2³ · 3²)  =  √(2² · 3² · 2)  =  2 · 3 · √2  =  6√2",
                "",
                "√30  =  √(2 · 3 · 5)      already simplest: no prime repeats",
                "",
                "the 3rd root of 54  =  the 3rd root of (3³ · 2)  =  3 · (3rd root of 2)",
            ]),
            ("p", "Fractions come apart the same way: `√(18/25) = √18 / √25 = 3√2 / 5`. "
                  "When the denominator is not a perfect square the root stays below the "
                  "bar &mdash; `√(1/2) = 1/√2` &mdash; and clearing it is rationalising, "
                  "which course 5 covers."),
            ("example", ("Which of these are real",
                         "`√16 = 4`. `√(−16)` has no real value. The 3rd root of `−27` is "
                         "`−3`, because `(−3)³ = −27`. The 4th root of `81` is `3`, because "
                         "`3⁴ = 81`; `−3` is also a fourth root of `81`, and the radical "
                         "denotes `3`.")),
        ],
        "lab": ("radicals", {
            "mode": "simplify",
            "panel_title": "Factor first, then pull out",
            "panel_intro": "Set a radicand and an index. The radicand is factorised into "
                           "primes and each prime leaves the root in complete groups of the "
                           "index, so what comes out and what has to stay are both visible. "
                           "Try `sqrt(-9)` and read what it reports.",
        }),
        "steps_title": "Simplifying a radical",
        "steps_intro": "Check that the thing exists before working on it. That order saves a page of algebra now and again.",
        "steps": [
            ("Check the sign of the radicand against the index",
             "Even index and a negative radicand means there is no real value, and that is "
             "the finished answer rather than a dead end. Odd index means there is always "
             "exactly one, and it carries the sign of the radicand."),
            ("Factor the radicand into primes",
             "`72` is `2³ · 3²`; `54` is `3³ · 2`. Guessing at a large square factor works "
             "sometimes and fails silently when it is not the largest, which leaves a "
             "half-simplified answer. The prime factorisation cannot leave one."),
            ("Take out complete groups of the index",
             "A pair of equal primes under a square root sends one copy outside; a triple "
             "under a cube root sends one copy outside. Anything that cannot fill a group "
             "stays in."),
            ("Check what is left, and check the value",
             "No prime under the sign should appear to the index or higher, and no fraction "
             "should be left under it. Then raise your answer to the index and confirm you "
             "get the radicand back."),
        ],
        "worked": {
            "title": "Three radicals, one method",
            "intro": ["Each one is factorised first, and each answer is raised back to the "
                      "index at the end."],
            "lines": [
                "1.  √72",
                "        72  =  2³ · 3²  =  2² · 3² · 2",
                "        complete pairs out:  2 and 3        left in:  2",
                "        √72  =  6√2",
                "        check:  (6√2)²  =  36 · 2  =  72",
                "",
                "2.  the 3rd root of −54",
                "        −54  =  −(3³ · 2)",
                "        complete triple out:  −3            left in:  2",
                "        3rd root of −54  =  −3 · (3rd root of 2)",
                "        check:  (−3)³ · 2  =  −27 · 2  =  −54",
                "",
                "3.  √(18/25)",
                "        √(18/25)  =  √18 / √25",
                "        18 = 3² · 2, so √18 = 3√2;   √25 = 5",
                "        √(18/25)  =  3√2 / 5",
                "        check:  (3√2 / 5)²  =  (9 · 2)/25  =  18/25",
            ],
            "after": [
                "Each check raises the answer to the index and recovers the radicand. That "
                "establishes the value is a root of the radicand. For the two square roots "
                "it takes one more observation to know it is <em>the</em> principal root: "
                "`6√2` and `3√2 / 5` are both positive, and positivity is the second half "
                "of the definition.",
                "Line 2 keeps the minus sign outside the radical throughout, which is the "
                "tidy way to handle an odd index over a negative radicand. Line 3 leaves no "
                "root below the bar because `25` is a perfect square; had the denominator "
                "been `24`, the answer would need the rationalising step of course 5.",
            ],
        },
        "quiz_title": "Roots",
        "quiz": [
            {"q": "What is `√16`?",
             "a": ["`4`", "`±4`", "`−4`", "`8`"],
             "c": 0,
             "why": "The radical denotes one number, the non-negative one. `±4` answers a "
                    "different question &mdash; the solutions of `x² = 16` &mdash; and "
                    "`−4` is a square root of `16` that the symbol does not name. `8` is "
                    "`16` halved, not a root of it."},
            {"q": "Simplify `√75`.",
             "a": ["`5√3`", "`3√5`", "`25√3`", "It is already in simplest form"],
             "c": 0,
             "why": "`75 = 5² · 3`, so the pair of fives sends one `5` outside and the `3` "
                    "stays in. `3√5` swaps the two, and is `√45`. `25√3` takes out the "
                    "whole square instead of its root. And `75` has a repeated prime "
                    "factor, so it is not in simplest form."},
            {"q": "Which of these has no real value?",
             "a": ["the 3rd root of `−27`", "`−√25`", "the 4th root of `−16`", "`√(4/9)`"],
             "c": 2,
             "why": "No real number has a negative fourth power, so nothing real is a "
                    "fourth root of `−16`. The 3rd root of `−27` is `−3`, since "
                    "`(−3)³ = −27`; `−√25` is `−5`, with the minus outside the radical and "
                    "applied afterwards; and `√(4/9)` is `2/3`."},
        ],
        "mistakes": [
            ("Writing that the square root of 9 is plus or minus 3",
             "The symbol names one number. The `±` is written by hand when you solve "
             "`x² = 9`, precisely because the radical would otherwise supply only the "
             "positive root. Losing that distinction loses a solution in course 6."),
            ("Splitting a root over a sum",
             "`√(9 + 16)` is `√25 = 5`, not `3 + 4`. The product rule `√(ab) = √a · √b` is "
             "real and the sum version is not, which is what makes the false one look "
             "reasonable. Two numbers settle it in seconds."),
            ("Cancelling the square root of x squared to x",
             "It is `|x|`. At `x = −5` the left side is `5` and the right is `−5`. For an "
             "odd index the cancellation really is clean &mdash; the cube root of `x³` is "
             "`x` &mdash; and that is exactly why the even case is forgotten."),
        ],
        "standard": ("Finish when you can say whether a radical has a real value before you try to simplify it.",
                     "Given a radical, the first two things you should produce are the "
                     "parity of the index and the sign of the radicand, and only then a "
                     "factorisation. You should also be able to state, without hesitating, "
                     "that `√9` is `3` and that `x² = 9` has two solutions, and say why "
                     "those are not in conflict."),
        "note": "Lesson 8 gives the radical a second notation: `x^(1/n)`. That is not a new "
                "idea but a forced one &mdash; if the exponent laws of lesson 5 are to hold "
                "for fractional exponents, then `(x^(1/2))²` must be `x¹`, and `x^(1/2)` "
                "has no choice but to be the square root. Every restriction stated here, "
                "including the even-index one, travels with it.",
    },
]
