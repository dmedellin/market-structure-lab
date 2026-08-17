"""Course 4, lessons 08-13 — the AC method, special forms, division, roots and graphs."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "the-ac-method",
        "title": "The AC Method",
        "module": "Factoring",
        "one_line": "Factoring ax² + bx + c when a is not 1.",
        "summary": (
            "When the leading coefficient is not `1`, guessing the two binomials is a "
            "search with too many branches. The AC method replaces the guess with "
            "arithmetic: one product to compute, one pair of integers to find, and "
            "then the grouping of lesson 6 finishes the job."
        ),
        "key": [
            "ax² + bx + c            a ≠ 1",
            "find m, n :   mn = ac   and   m + n = b",
            "ax² + mx + nx + c       split, then group",
            "6x² + 11x + 3  =  (3x + 1)(2x + 3)",
        ],
        "key_label": "One product, one pair, then grouping",
        "concepts_intro": (
            "The method is three lines of arithmetic. What matters is why the middle "
            "step is allowed, and what it means when the search comes back empty."
        ),
        "concepts": [
            ("Splitting the middle term changes nothing",
             "`mx + nx` is `(m + n)x`, and `m + n` is `b` by construction. The "
             "expression after the split is equal to the one before it for every "
             "value of `x` &mdash; you have written `bx` as a sum, not altered the "
             "polynomial. That equality is the whole licence for the step."),
            ("The search is finite, so it can be completed",
             "`ac` is one integer and it has finitely many factor pairs. Listing them "
             "and checking each sum is a complete search, so it either produces the "
             "pair or establishes that none exists."),
            ("No pair means no factorisation over the integers",
             "An empty search is an answer. If no integer factor pair of `ac` sums to "
             "`b`, then `ax² + bx + c` is not a product of two binomials with integer "
             "coefficients, and no amount of further staring will make it one."),
        ],
        "read_title": "The AC method",
        "read_intro": "Why splitting the middle term is legal, and what an empty search proves.",
        "body": [
            ("p", "Lesson 7 factored `x² + bx + c` by finding two numbers that multiply "
                  "to `c` and add to `b`. That shortcut depends on the leading "
                  "coefficient being `1`. Once `a ≠ 1`, the constant term of the product "
                  "is no longer the product of the two numbers you are looking for, "
                  "because the `a` distributes into both binomials."),
            ("def", ("The AC method",
                     "To factor `ax² + bx + c` with integer coefficients: compute `ac`; "
                     "find integers `m` and `n` with `mn = ac` and `m + n = b`; rewrite "
                     "`bx` as `mx + nx`; then factor the resulting four terms by "
                     "grouping.")),
            ("thm", ("The split is an identity",
                     "If `m + n = b` then `ax² + mx + nx + c = ax² + (m + n)x + c = "
                     "ax² + bx + c`. The two expressions agree for every `x`, so one "
                     "may be replaced by the other anywhere. Nothing is being done to "
                     "an equation; a single expression is being rewritten.")),
            ("p", "This is the point worth holding on to. The method looks like a trick "
                  "because the number `ac` appears from nowhere, but the only step that "
                  "could possibly be illegal &mdash; replacing `bx` by `mx + nx` &mdash; "
                  "is justified by one line of arithmetic that you control."),
            ("example", ("6x² + 11x + 3",
                         "`ac = 6 · 3 = 18`. The factor pairs of `18` are `1·18`, `2·9` "
                         "and `3·6`, with sums `19`, `11` and `9`. The pair is `9` and "
                         "`2`. Splitting: `6x² + 9x + 2x + 3 = 3x(2x + 3) + 1(2x + 3) = "
                         "(3x + 1)(2x + 3)`.")),
            ("p", "The order of `m` and `n` does not matter. Splitting as "
                  "`6x² + 2x + 9x + 3` gives `2x(3x + 1) + 3(3x + 1) = (2x + 3)(3x + 1)` "
                  "&mdash; the same two factors in the other order. If your grouping "
                  "produces two brackets that are not identical, you have made an "
                  "arithmetic slip, not discovered a second answer."),
            ("h3", "When there is no pair"),
            ("thm", ("The integer factorisation criterion",
                     "For integers `a`, `b`, `c` with `a ≠ 0`, the trinomial "
                     "`ax² + bx + c` factors as a product of two binomials with integer "
                     "coefficients exactly when the discriminant `b² - 4ac` is a perfect "
                     "square.")),
            ("example", ("2x² + 3x + 4 does not factor",
                         "`ac = 8`. The positive pairs `1·8` and `2·4` give sums `9` and "
                         "`6`; the negative pairs `(-1)(-8)` and `(-2)(-4)` give `-9` and "
                         "`-6`. None is `3`, and the search is now complete. The "
                         "discriminant agrees: `b² - 4ac = 9 - 32 = -23`, which is not a "
                         "perfect square.")),
            ("p", "Take the common factor out first, always. `12x² + 22x + 6` has `ac = "
                  "72` and a messier pair list, but `12x² + 22x + 6 = 2(6x² + 11x + 3) = "
                  "2(3x + 1)(2x + 3)` reduces it to the example above. Lesson 5 put the "
                  "common factor at the top of the decision list for exactly this "
                  "reason."),
        ],
        "lab": ("factoring", {
            "mode": "ac",
            "panel_title": "Watch the pair search run",
            "panel_intro": "Enter `a`, `b` and `c`. The lab computes `ac`, lists every "
                           "integer factor pair of it with its sum, and marks the one "
                           "that equals `b`. Try `2x² + 3x + 4` and watch the list run "
                           "out with nothing marked.",
        }),
        "steps_title": "Factoring ax² + bx + c",
        "steps_intro": "Four steps, and the first one is not optional.",
        "steps": [
            ("Take out the greatest common factor",
             "Divide out any factor common to all three terms, including a leading "
             "`-1` if `a` is negative. Skipping this is what turns a small pair "
             "search into a large one."),
            ("Compute ac",
             "Multiply the leading coefficient by the constant term, signs included. "
             "For `12x² - 17x + 6` this is `72`; for `6x² - 7x - 20` it is `-120`."),
            ("Search the factor pairs of ac",
             "List every pair, with its sum. If `ac` is positive the pair shares the "
             "sign of `b`; if `ac` is negative the pair has opposite signs. Stop at "
             "the pair whose sum is `b`, or stop when the list is exhausted."),
            ("Split, group, then expand to check",
             "Rewrite `bx` as `mx + nx`, group the four terms in pairs, and take out "
             "the common binomial. Multiply your answer back out &mdash; on this "
             "topic checking is faster than the work."),
        ],
        "worked": {
            "title": "Factoring 12x² - 17x + 6",
            "intro": [
                "`ac = 72` is positive and `b = -17` is negative, so both members of "
                "the pair are negative. That observation halves the list before it is "
                "written."
            ],
            "lines": [
                "12x² - 17x + 6              a = 12,  b = -17,  c = 6",
                "ac = 12 · 6 = 72            need  mn = 72,  m + n = -17",
                "",
                "pairs of 72    1·72   2·36   3·24   4·18   6·12   8·9",
                "sums           73     38     27     22     18     17",
                "both negative: -8 and -9    (-8)(-9) = 72,   -8 + (-9) = -17",
                "",
                "12x² - 8x - 9x + 6          split the middle term",
                "4x(3x - 2) - 3(3x - 2)      group; the common binomial is 3x - 2",
                "(4x - 3)(3x - 2)            the factorisation",
                "",
                "check  (4x - 3)(3x - 2) = 12x² - 8x - 9x + 6 = 12x² - 17x + 6",
            ],
            "after": [
                "The second group is `-9x + 6`, and the factor taken out is `-3`, not "
                "`3`. Pulling out `3` would give `3(-3x + 2)`, whose bracket does not "
                "match `3x - 2`, and the grouping would appear to fail. When the two "
                "brackets differ only by an overall sign, the sign you extracted is "
                "the thing to fix."
            ],
        },
        "quiz_title": "Check yourself",
        "quiz": [
            {"q": "For `10x² + 11x - 6`, which product must the pair of integers have?",
             "a": ["`11`", "`-6`", "`-60`", "`10`"],
             "c": 2,
             "why": "The pair multiplies to `ac = 10 · (-6) = -60` and adds to `b = 11`. "
                    "The pair is `15` and `-4`."},
            {"q": "Why may `bx` be replaced by `mx + nx`?",
             "a": ["Because both sides of the equation are changed equally",
                   "Because `m + n = b`, so the two expressions are equal for every `x`",
                   "Because factoring allows any regrouping of terms",
                   "Because `mn = ac` guarantees it"],
             "c": 1,
             "why": "The licence is the identity `mx + nx = (m + n)x = bx`. The "
                    "condition `mn = ac` is what makes the grouping succeed afterwards, "
                    "but it is not what makes the split legal."},
            {"q": "No integer factor pair of `ac` sums to `b`. What follows?",
             "a": ["A different method will factor it",
                   "The trinomial factors, but only with fractions",
                   "The trinomial does not factor into binomials with integer coefficients",
                   "The arithmetic must be wrong"],
             "c": 2,
             "why": "The pair search is complete, so an empty result is a proof. "
                    "Equivalently `b² - 4ac` is not a perfect square."},
        ],
        "mistakes": [
            ("Forgetting the common factor and searching a huge ac",
             "`24x² + 44x + 12` has `ac = 288`. Divided by `4` it is `6x² + 11x + 3` "
             "with `ac = 18`. Same answer, about a third of the work &mdash; `288` has "
             "nine factor pairs to check, `18` has three &mdash; and far fewer chances "
             "to misread a pair."),
            ("Losing the sign when grouping the second pair",
             "In `12x² - 8x - 9x + 6` the second group needs `-3` extracted, not `3`. "
             "If your two brackets come out as `3x - 2` and `-3x + 2`, factor `-1` out "
             "of the second and continue."),
            ("Treating a failed search as a failed attempt",
             "Running out of pairs is the method succeeding. It has told you the "
             "trinomial is irreducible over the integers, which is exactly what "
             "lesson 12 will need you to be able to conclude."),
        ],
        "standard": ("Finish when an empty pair list reads as a result rather than a dead end.",
                     "You should be able to factor `6x² - 7x - 20` and `12x² - 17x + 6` "
                     "without hesitation, and to say of `2x² + 3x + 4` that it does not "
                     "factor over the integers &mdash; naming the completed search or "
                     "the discriminant as your reason."),
        "note": "The lab prints the whole pair list rather than only the winning pair, "
                "because the list is the argument. A pair that is simply asserted is a "
                "guess that happened to work; a list that has been exhausted is a "
                "proof, and lesson 12 runs the same kind of complete search over a "
                "candidate list of roots.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "factoring-special-forms",
        "title": "Factoring Special Forms",
        "module": "Factoring",
        "one_line": "Differences of squares, perfect square trinomials, sums and differences of cubes.",
        "summary": (
            "Four patterns, recognised rather than derived. Each is one of the special "
            "products of lesson 4 read backwards, and each is worth knowing on sight "
            "because the general methods are slower and, for the cubes, will not find "
            "the factorisation at all."
        ),
        "key": [
            "a² - b²   =  (a - b)(a + b)",
            "a² ± 2ab + b²  =  (a ± b)²",
            "a³ - b³   =  (a - b)(a² + ab + b²)",
            "a³ + b³   =  (a + b)(a² - ab + b²)",
            "a² + b²   does NOT factor over the reals",
        ],
        "key_label": "Four patterns, and one non-pattern",
        "concepts_intro": (
            "These are identities, so they hold in both directions. Reading them "
            "right to left is multiplying; reading them left to right is factoring."
        ),
        "concepts": [
            ("A pattern matches only if both parts are perfect powers",
             "`9x² - 25` is a difference of squares because `9x²` is `(3x)²` and `25` "
             "is `5²`. `9x² - 24` is not, because `24` is not the square of anything "
             "rational. Checking both parts is the whole of the recognition step."),
            ("The sum of two squares does not factor",
             "`a² + b²` has no factorisation over the real numbers. This is not a gap "
             "in your technique; there is nothing to find. Course 6 introduces `i` and "
             "factors it as `(a + bi)(a - bi)`, which is a different number system."),
            ("Factor completely means keep going",
             "`x⁴ - 16` is `(x² - 4)(x² + 4)`, and `x² - 4` is itself a difference of "
             "squares. A pattern that applies once may apply again to one of the "
             "pieces, and an answer that stops early is incomplete."),
        ],
        "read_title": "The four special forms",
        "read_intro": "How to recognise each, and the two that are most often faked.",
        "body": [
            ("p", "Lesson 4 multiplied these out. Every identity here is one of those "
                  "products with the two sides exchanged, which is why they need no "
                  "proof beyond expanding the right-hand side."),
            ("h3", "Difference of squares"),
            ("thm", ("a² - b² = (a - b)(a + b)",
                     "Expanding the right side gives `a² + ab - ab - b² = a² - b²`; the "
                     "middle terms cancel. Conversely, any expression that is one "
                     "perfect square minus another factors this way.")),
            ("example", ("9x² - 25 and x⁴ - 16",
                         "`9x² - 25 = (3x)² - 5² = (3x - 5)(3x + 5)`. And `x⁴ - 16 = "
                         "(x²)² - 4² = (x² - 4)(x² + 4) = (x - 2)(x + 2)(x² + 4)`, where "
                         "the last factor is a sum of squares and stops there.")),
            ("p", "There is no difference-of-squares pattern for a sum. `a² + b²` is "
                  "irreducible over the reals &mdash; for `x² + 4` the discriminant is "
                  "`0 - 16 = -16`, so no real linear factors exist. Writing "
                  "`x² + 4 = (x + 2)(x + 2)` is the single most common invented law in "
                  "this lesson; expanding it gives `x² + 4x + 4`."),
            ("h3", "Perfect square trinomials"),
            ("thm", ("a² ± 2ab + b² = (a ± b)²",
                     "A trinomial is a perfect square exactly when its first and last "
                     "terms are perfect squares and its middle term is twice the product "
                     "of their roots, up to sign.")),
            ("example", ("x² + 12x + 36 and 25x² - 20x + 4",
                         "For the first, `x² = (x)²`, `36 = 6²`, and `2 · x · 6 = 12x` "
                         "matches: it is `(x + 6)²`. For the second, `25x² = (5x)²`, "
                         "`4 = 2²`, and `2 · 5x · 2 = 20x` matches the middle term with "
                         "the sign negative: it is `(5x - 2)²`.")),
            ("p", "The middle-term test is what makes this a theorem rather than a "
                  "guess. `x² + 13x + 36` has square outer terms too, but `2 · 1 · 6 = "
                  "12`, not `13`, so it is not a perfect square. It happens to factor "
                  "as `(x + 4)(x + 9)`, by the method of lesson 7."),
            ("h3", "Sums and differences of cubes"),
            ("thm", ("a³ - b³ = (a - b)(a² + ab + b²)   and   a³ + b³ = (a + b)(a² - ab + b²)",
                     "Unlike squares, a SUM of cubes does factor. In both identities the "
                     "linear factor carries the sign of the original and the quadratic "
                     "factor carries the opposite sign on its middle term; the quadratic "
                     "never factors further over the reals.")),
            ("example", ("8x³ - 27 and 27x³ + 64",
                         "`8x³ - 27 = (2x)³ - 3³ = (2x - 3)(4x² + 6x + 9)`. And "
                         "`27x³ + 64 = (3x)³ + 4³ = (3x + 4)(9x² - 12x + 16)`. Expanding "
                         "either one back is four lines and worth doing once.")),
            ("p", "The sign rule is the part that is misremembered. In `a³ - b³` the "
                  "binomial is `(a - b)` and the trinomial's middle term is `+ab`; in "
                  "`a³ + b³` the binomial is `(a + b)` and the middle term is `-ab`. The "
                  "trinomial's last term is `+b²` in both cases, never negative."),
        ],
        "lab": ("factoring", {
            "mode": "special",
            "panel_title": "Match the pattern, then check it",
            "panel_intro": "Type an expression and the lab reports which special form "
                           "it matches, or that it matches none. Feed it `x² + 4` to "
                           "see a sum of squares refused, and `x⁴ - 16` to see a "
                           "pattern applied twice.",
        }),
        "steps_title": "Recognising a special form",
        "steps_intro": "Count the terms first; the count tells you which patterns are even possible.",
        "steps": [
            ("Take out the common factor",
             "`2x² - 50` is not a difference of squares as written, because `2x²` is "
             "not a perfect square. As `2(x² - 25)` it is, giving `2(x - 5)(x + 5)`."),
            ("Two terms: try squares, then cubes",
             "A difference of squares factors; a sum of squares does not. Both a sum "
             "and a difference of cubes factor. Check that each term really is a "
             "perfect square or cube before claiming the pattern."),
            ("Three terms: test the middle term",
             "If the outer terms are perfect squares, compute twice the product of "
             "their roots. If that equals the middle term, it is a perfect square "
             "trinomial; if not, use lesson 7 or lesson 8."),
            ("Factor each piece again",
             "Apply the list to every factor you produced. Stop only when no factor "
             "matches any pattern and none factors by the AC method."),
        ],
        "worked": {
            "title": "Factoring x⁴ - 16 completely",
            "intro": [
                "Two terms, both perfect squares, so the difference of squares applies "
                "&mdash; and then applies again."
            ],
            "lines": [
                "x⁴ - 16",
                "  = (x²)² - 4²                  both terms are perfect squares",
                "  = (x² - 4)(x² + 4)            a² - b² with a = x², b = 4",
                "  = (x - 2)(x + 2)(x² + 4)      x² - 4 is a difference of squares too",
                "",
                "x² + 4 is a SUM of squares: it stops here.",
                "",
                "check   (x - 2)(x + 2) = x² - 4",
                "        (x² - 4)(x² + 4) = x⁴ + 4x² - 4x² - 16 = x⁴ - 16",
            ],
            "after": [
                "Two things are being claimed at the end, and only one of them is a "
                "calculation. That `(x - 2)(x + 2)(x² + 4)` multiplies back to `x⁴ - 16` "
                "is checked by expanding. That `x² + 4` cannot be factored further is a "
                "separate claim, and its justification is that a sum of squares has no "
                "real factorisation &mdash; not that no factorisation came to mind."
            ],
        },
        "quiz_title": "Check yourself",
        "quiz": [
            {"q": "Which of these does NOT factor over the real numbers?",
             "a": ["`x³ + 8`", "`x² - 8`", "`x² + 9`", "`4x² - 9`"],
             "c": 2,
             "why": "`x² + 9` is a sum of squares. A sum of CUBES does factor, which is "
                    "why `x³ + 8 = (x + 2)(x² - 2x + 4)`."},
            {"q": "Is `x² + 10x + 25` a perfect square trinomial?",
             "a": ["No, because the middle term is positive",
                   "Yes, it is `(x + 5)²`",
                   "No, because `25` is not twice `5`",
                   "Yes, it is `(x + 25)²`"],
             "c": 1,
             "why": "`x² = (x)²`, `25 = 5²`, and `2 · x · 5 = 10x` matches the middle "
                    "term exactly."},
            {"q": "Factor `27x³ + 64`.",
             "a": ["`(3x + 4)(9x² - 12x + 16)`", "`(3x + 4)(9x² + 12x + 16)`",
                   "`(3x - 4)(9x² + 12x + 16)`", "`(3x + 4)³`"],
             "c": 0,
             "why": "For `a³ + b³` with `a = 3x` and `b = 4`, the binomial takes the "
                    "plus sign and the trinomial's middle term takes the minus: "
                    "`a² - ab + b² = 9x² - 12x + 16`."},
        ],
        "mistakes": [
            ("Factoring a sum of squares",
             "`x² + 4` is irreducible over the reals, and `(x + 2)²` is `x² + 4x + 4`. "
             "The habit is picked up from the difference of squares, where the pattern "
             "is real, and it survives because nobody expands the answer."),
            ("Skipping the middle-term test",
             "`4x² + 10x + 25` has perfect square outer terms, but `2 · 2x · 5 = 20x`, "
             "not `10x`. It is not `(2x + 5)²`, and in fact `b² - 4ac = 100 - 400` is "
             "negative, so it does not factor at all."),
            ("Putting the wrong signs in the cubes trinomial",
             "The trinomial's last term is `+b²` in both identities. If you have "
             "written `(a - b)(a² + ab - b²)`, expand it: the `a³` and `b³` will not "
             "come out alone."),
        ],
        "standard": ("Finish when you can refuse a sum of squares as confidently as you accept a difference.",
                     "Given `9x² - 25`, `x² + 12x + 36`, `8x³ - 27` and `x² + 16` you "
                     "should factor the first three on sight and say of the fourth that "
                     "it does not factor over the reals, without treating that as a "
                     "failure to spot something."),
        "note": "These patterns matter beyond factoring. Course 5 cancels a difference "
                "of squares out of a rational expression on almost every page, and "
                "course 6 returns to `a² + b²` once `i` exists and factors it properly. "
                "What is true here is that it does not factor over the REALS, and that "
                "qualifier is the whole content of the claim.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "polynomial-long-division",
        "title": "Polynomial Long Division",
        "module": "Division and roots",
        "one_line": "Dividing by any polynomial, and what the remainder means.",
        "summary": (
            "The long division you learned for integers, performed on polynomials. It "
            "works for a divisor of any degree, it always terminates, and it produces "
            "a quotient and a remainder that are unique &mdash; which is what makes it "
            "an algorithm rather than a technique."
        ),
        "key": [
            "f(x) = d(x)·q(x) + r(x)",
            "with   deg r < deg d    or   r = 0",
            "",
            "2x⁴ - 3x³ + 5x - 1  ÷  (x² - x + 2)",
            "  q = 2x² - x - 5     r = 2x + 9",
        ],
        "key_label": "The division algorithm for polynomials",
        "concepts_intro": (
            "One statement carries this lesson. Everything in the procedure exists to "
            "produce the `q` and `r` it promises."
        ),
        "concepts": [
            ("Division always succeeds, but not always exactly",
             "For any `f` and any non-zero `d` there are a quotient `q` and a remainder "
             "`r` with `f = dq + r`. A remainder of zero means `d` is a factor of `f`; "
             "any other remainder means it is not."),
            ("The remainder must have smaller degree than the divisor",
             "That is the stopping rule, and it is not a convention. While the leading "
             "term of what is left is still divisible by the leading term of `d`, "
             "there is another step to take."),
            ("Missing powers must be written in",
             "`2x⁴ - 3x³ + 5x - 1` has no `x²` term, and the division needs a column "
             "for it. Writing `+ 0x²` costs one symbol; omitting it misaligns every "
             "subtraction that follows."),
        ],
        "read_title": "Long division for polynomials",
        "read_intro": "The algorithm, the stopping rule, and the subtraction that goes wrong.",
        "body": [
            ("p", "Dividing `17` by `5` gives `3` remainder `2`, and the content of "
                  "that sentence is `17 = 5 · 3 + 2` with `2 &lt; 5`. Polynomial division "
                  "makes the same statement, with degree playing the part of size."),
            ("thm", ("The division algorithm for polynomials",
                     "Let `f` and `d` be polynomials with `d ≠ 0`. There exist unique "
                     "polynomials `q` and `r` such that `f(x) = d(x)q(x) + r(x)`, where "
                     "either `r = 0` or `deg r &lt; deg d`.")),
            ("p", "Uniqueness is the half that is usually skipped, and it is what lets "
                  "you check an answer. If you and I divide the same `f` by the same "
                  "`d` and get different quotients, one of us is wrong; there is no "
                  "second correct answer to compare against."),
            ("def", ("The procedure",
                     "Write both polynomials in descending order with every power "
                     "present. Divide the leading term of the current remainder by the "
                     "leading term of the divisor to get the next quotient term; "
                     "multiply the whole divisor by that term; subtract; bring down. "
                     "Stop when the remainder's degree is less than the divisor's.")),
            ("p", "Only the LEADING terms decide each quotient term. To start "
                  "`2x⁴ - 3x³ + 0x² + 5x - 1` divided by `x² - x + 2` you ask what "
                  "times `x²` gives `2x⁴`, and the answer `2x²` depends on nothing "
                  "else in either polynomial."),
            ("example", ("The first step in full",
                         "`2x² · (x² - x + 2) = 2x⁴ - 2x³ + 4x²`. Subtracting this from "
                         "`2x⁴ - 3x³ + 0x²` gives `-x³ - 4x²`, because `-3x³ - (-2x³) = "
                         "-x³` and `0x² - 4x² = -4x²`. Both signs come from the "
                         "subtraction, and both are places where a term is commonly "
                         "lost.")),
            ("p", "Subtracting a polynomial means subtracting every one of its terms. "
                  "Lesson 2 made this point about `-(x - 3)`; here the same slip costs "
                  "you the rest of the division, because each line feeds the next. If "
                  "you find it easier, negate the product and add."),
            ("h3", "Reading the result"),
            ("p", "The division above ends with `q = 2x² - x - 5` and `r = 2x + 9`. "
                  "The remainder has degree `1`, the divisor degree `2`, so the "
                  "stopping rule is satisfied and the work is finished. Written out in "
                  "full: `2x⁴ - 3x³ + 5x - 1 = (x² - x + 2)(2x² - x - 5) + (2x + 9)`."),
            ("p", "Because `r ≠ 0`, the divisor is not a factor. Had the remainder "
                  "been `0`, we would have a factorisation of a quartic into a "
                  "quadratic times a quadratic &mdash; which is how division earns its "
                  "place in a course about factoring, and what lesson 12 exploits."),
            ("thm", ("Degrees add",
                     "If `r = 0` then `deg f = deg d + deg q`. So dividing a degree-4 "
                     "polynomial by a degree-2 one gives a degree-2 quotient, and a "
                     "quotient of any other degree is an arithmetic error you can catch "
                     "before checking a single coefficient.")),
        ],
        "lab": ("polynomial", {
            "mode": "divide",
            "panel_title": "Every line of the division",
            "panel_intro": "Enter a dividend and a divisor. The lab shows each "
                           "quotient term, the product it forms with the divisor, and "
                           "the subtraction &mdash; then states `f = dq + r` and "
                           "verifies it by expanding.",
        }),
        "steps_title": "Dividing one polynomial by another",
        "steps_intro": "The setup carries most of the risk; the loop itself is short.",
        "steps": [
            ("Write both in descending order, with gaps filled",
             "Insert `0x^k` for every missing power in the dividend. The divisor needs "
             "the same treatment if it has gaps."),
            ("Divide leading term by leading term",
             "That single division gives the next term of the quotient. Ignore every "
             "other term in both polynomials while you do it."),
            ("Multiply and subtract, carefully",
             "Multiply the entire divisor by the new quotient term, then subtract the "
             "entire product. Change every sign, not just the first."),
            ("Stop by degree, then state the result",
             "When the remainder's degree drops below the divisor's, stop and write "
             "`f = dq + r`. Expand it to check &mdash; the check catches every sign "
             "error at once."),
        ],
        "worked": {
            "title": "Dividing 2x⁴ - 3x³ + 5x - 1 by x² - x + 2",
            "intro": [
                "The dividend has no `x²` term, so it is written with `0x²` in place. "
                "The divisor has degree `2`, so the division stops as soon as what "
                "remains has degree `1` or `0`."
            ],
            "lines": [
                "                2x²  -   x  -  5",
                "            ┌──────────────────────────────────────",
                "x² - x + 2  │ 2x⁴ - 3x³ + 0x² + 5x - 1",
                "              2x⁴ - 2x³ + 4x²                 2x² · (x² - x + 2)",
                "              ─────────────────────",
                "                   - x³ - 4x² + 5x",
                "                   - x³ +  x² - 2x            -x · (x² - x + 2)",
                "                   ──────────────────",
                "                        - 5x² + 7x - 1",
                "                        - 5x² + 5x - 10       -5 · (x² - x + 2)",
                "                        ────────────────",
                "                               2x + 9         degree 1 < 2 : stop",
                "",
                "2x⁴ - 3x³ + 5x - 1 = (x² - x + 2)(2x² - x - 5) + (2x + 9)",
            ],
            "after": [
                "Each subtraction is where the work is lost. At the second step the "
                "line being subtracted is `-x³ + x² - 2x`, and `-4x² - (+x²)` is "
                "`-5x²` while `5x - (-2x)` is `7x`. Two sign changes in one line, both "
                "from the same rule.",
                "The check is mechanical: expand `(x² - x + 2)(2x² - x - 5)` to get "
                "`2x⁴ - 3x³ + 3x - 10`, then add `2x + 9` to get `2x⁴ - 3x³ + 5x - 1`. "
                "That is the original dividend, so the quotient and remainder are right."
            ],
        },
        "quiz_title": "Check yourself",
        "quiz": [
            {"q": "Dividing a degree-5 polynomial by a degree-2 polynomial, what is the largest possible degree of the remainder?",
             "a": ["`5`", "`3`", "`2`", "`1`"],
             "c": 3,
             "why": "The remainder's degree must be strictly less than the divisor's, "
                    "so at most `1`. The quotient has degree `3`."},
            {"q": "`f(x) = d(x)q(x) + r(x)` with `r(x) = 0`. What does that tell you?",
             "a": ["`d` is a factor of `f`", "`f` has no real roots",
                   "`d` and `f` have the same degree", "The division was done incorrectly"],
             "c": 0,
             "why": "A zero remainder means `f = dq` exactly, so `d` divides `f`. This "
                    "is the observation lesson 12 turns into the factor theorem."},
            {"q": "Why write `+ 0x²` in the dividend?",
             "a": ["It changes the value of the polynomial",
                   "It keeps the columns aligned so each subtraction uses like terms",
                   "The algorithm requires all coefficients to be non-zero",
                   "It increases the degree of the dividend"],
             "c": 1,
             "why": "`0x²` adds nothing to the polynomial. It reserves the column, so "
                    "the terms being subtracted line up with the terms they belong to."},
        ],
        "mistakes": [
            ("Subtracting only the first term of the product",
             "The whole product is subtracted, so every sign in it flips. This single "
             "error accounts for most wrong quotients, and because each line feeds the "
             "next, it is invisible until the final check fails."),
            ("Omitting a missing power",
             "Leaving out `0x²` slides every later coefficient one column left, and "
             "the result is a quotient of the right degree with entirely wrong "
             "coefficients &mdash; the kind of wrong answer that looks plausible."),
            ("Dividing whole polynomials instead of leading terms",
             "Each quotient term comes from the leading terms alone. Trying to account "
             "for the divisor's other terms at that moment is doing the multiply step "
             "early, and it double-counts them."),
        ],
        "standard": ("Finish when you can divide, state f = dq + r, and check it by expanding.",
                     "The result is not the quotient on its own. You should write the "
                     "full identity with the remainder in place, and verify it by "
                     "multiplying out &mdash; which is the only step here that "
                     "confirms every sign at once."),
        "note": "Long division works for a divisor of any degree, and that generality "
                "is why it comes first. Lesson 11's synthetic division is faster but "
                "applies only when the divisor is `x - c`; when a divisor is quadratic "
                "or worse, this is the method, and there is no shortcut waiting.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "synthetic-division-and-the-remainder-theorem",
        "title": "Synthetic Division and the Remainder Theorem",
        "module": "Division and roots",
        "one_line": "A shorthand for dividing by x - c, and what the remainder equals.",
        "summary": (
            "When the divisor is `x - c`, the long division of lesson 10 repeats the "
            "same three symbols on every line and can be compressed to one row of "
            "numbers. The remainder it leaves is not merely a leftover: it is `f(c)`, "
            "which is the fact the next lesson is built on."
        ),
        "key": [
            "divisor must be  x - c     (degree 1, leading coefficient 1)",
            "",
            "c │  a₃   a₂   a₁   a₀      multiply down, add across",
            "",
            "f(x) = (x - c)·q(x) + f(c)",
            "remainder  =  f(c)",
        ],
        "key_label": "The remainder theorem",
        "concepts_intro": (
            "One shortcut and one theorem. The shortcut saves time; the theorem "
            "changes what division is for."
        ),
        "concepts": [
            ("Synthetic division is long division with the symbols removed",
             "Every line of the long division by `x - c` contains the same powers of "
             "`x` in the same columns, so the powers carry no information. Strip them "
             "and only the coefficients are left."),
            ("It applies only to a divisor x - c",
             "Degree one, leading coefficient one. For `x² - x + 2`, or for `2x - 1` "
             "as written, the compression does not work and lesson 10's method is the "
             "method."),
            ("The remainder is the function value",
             "Dividing `f` by `x - c` leaves a constant remainder, and that constant "
             "is `f(c)`. So synthetic division evaluates a polynomial as a side "
             "effect, usually with less arithmetic than substituting."),
        ],
        "read_title": "Synthetic division, and what the remainder is",
        "read_intro": "The shorthand, the sign that goes wrong, and the theorem that makes it matter.",
        "body": [
            ("p", "Divide any cubic by `x - c` by long division and the pattern repeats: "
                  "multiply the divisor by a term, subtract, bring down. Because the "
                  "divisor is `x - c` and monic, each quotient coefficient is just the "
                  "previous line's leading coefficient, and each subtraction becomes an "
                  "addition once the sign of `c` is flipped."),
            ("def", ("Synthetic division",
                     "To divide `f(x)` by `x - c`: write `c`, then the coefficients of "
                     "`f` in descending order with zeros for missing powers. Bring down "
                     "the first coefficient. Multiply it by `c`, add to the next "
                     "coefficient, and repeat. The final number is the remainder; the "
                     "others are the quotient's coefficients, one degree lower.")),
            ("example", ("2x³ - 5x² + 3x - 7 divided by x - 3",
                         "The row is `2, -5, 3, -7` and `c = 3`. Bring down `2`; "
                         "`2·3 = 6` and `-5 + 6 = 1`; `1·3 = 3` and `3 + 3 = 6`; "
                         "`6·3 = 18` and `-7 + 18 = 11`. So the quotient is "
                         "`2x² + x + 6` and the remainder is `11`.")),
            ("p", "The quotient drops exactly one degree, because dividing a cubic by "
                  "a linear polynomial gives a quadratic. If your quotient has the "
                  "same degree as `f`, you have kept one coefficient too many."),
            ("h3", "The sign of c"),
            ("p", "The divisor must be written as `x - c`, and `c` is what is "
                  "SUBTRACTED. For `x - 3` we have `c = 3`. For `x + 4` write it as "
                  "`x - (-4)`, so `c = -4`. Using `4` there divides by `x - 4`, which "
                  "is a different polynomial and gives a wrong answer that looks "
                  "perfectly well-formed."),
            ("example", ("x³ + 2x² - 5x + 1 divided by x + 4",
                         "Here `c = -4` and the row is `1, 2, -5, 1`. Bring down `1`; "
                         "`1·(-4) = -4` and `2 + (-4) = -2`; `(-2)(-4) = 8` and "
                         "`-5 + 8 = 3`; `3·(-4) = -12` and `1 + (-12) = -11`. Quotient "
                         "`x² - 2x + 3`, remainder `-11`.")),
            ("h3", "The remainder theorem"),
            ("thm", ("The remainder theorem",
                     "For any polynomial `f` and any number `c`, the remainder on "
                     "dividing `f(x)` by `x - c` is `f(c)`.")),
            ("proof", [
                "By the division algorithm, `f(x) = (x - c)q(x) + r(x)` where `r = 0` "
                "or `deg r &lt; 1`. In either case `r` is a constant; call it `r`.",
                "The identity holds for every value of `x`, so it holds at `x = c`. "
                "Substituting gives `f(c) = (c - c)q(c) + r = 0 · q(c) + r = r`.",
                "So the constant remainder is `f(c)`.",
            ]),
            ("p", "Check it on the first example: `f(3) = 2(27) - 5(9) + 3(3) - 7 = "
                  "54 - 45 + 9 - 7 = 11`, which is the remainder the synthetic "
                  "division produced. On the second, `g(-4) = -64 + 32 + 20 + 1 = -11`, "
                  "again the remainder."),
            ("p", "This is worth pausing on, because it points in two directions. It "
                  "gives a fast way to evaluate a polynomial &mdash; three "
                  "multiplications and three additions for a cubic, against the powers "
                  "you would otherwise compute. And it says that a remainder of zero "
                  "means `f(c) = 0`, which is where lesson 12 begins."),
        ],
        "lab": ("polynomial", {
            "mode": "synthetic",
            "panel_title": "The row, and the value it computes",
            "panel_intro": "Enter the coefficients and a value of `c`. The lab builds "
                           "the row one multiply-and-add at a time, then evaluates "
                           "`f(c)` independently and shows the two agreeing.",
        }),
        "steps_title": "Dividing by x - c synthetically",
        "steps_intro": "Read c off the divisor first. That is where the errors are.",
        "steps": [
            ("Check the divisor is x - c",
             "Degree one and monic. `x - 3` gives `c = 3`; `x + 4` gives `c = -4`. "
             "For `2x - 1`, either factor the `2` out first or use long division."),
            ("Write every coefficient, zeros included",
             "Descending order, with `0` for each missing power. `x³ - 8` is "
             "`1, 0, 0, -8`, and dropping the zeros is the error that ruins the row."),
            ("Bring down, multiply, add",
             "Bring the first coefficient down unchanged. Then repeat: multiply the "
             "number you just wrote by `c`, and add it to the next coefficient."),
            ("Read off the quotient and the remainder",
             "The last number is the remainder, and equals `f(c)`. The rest are the "
             "quotient's coefficients, starting one degree below `f`."),
        ],
        "worked": {
            "title": "2x³ - 5x² + 3x - 7 divided by x - 3",
            "intro": [
                "The divisor is `x - 3`, so `c = 3` &mdash; the number that makes the "
                "divisor zero, not the number printed in it."
            ],
            "lines": [
                "  3 │   2    -5     3    -7",
                "    │         6     3    18        multiply down by 3",
                "    └──────────────────────────",
                "        2     1     6    11",
                "        └──── quotient ────┘   remainder",
                "",
                "quotient   2x² + x + 6          (degree 2, one below f)",
                "remainder  11",
                "",
                "2x³ - 5x² + 3x - 7 = (x - 3)(2x² + x + 6) + 11",
                "",
                "check by the remainder theorem:",
                "f(3) = 2(27) - 5(9) + 3(3) - 7 = 54 - 45 + 9 - 7 = 11",
            ],
            "after": [
                "The two checks available here are different in kind. Expanding "
                "`(x - 3)(2x² + x + 6) + 11` confirms the whole division. Evaluating "
                "`f(3)` confirms only the remainder &mdash; but it is one line, and a "
                "wrong remainder almost always means a wrong row above it."
            ],
        },
        "quiz_title": "Check yourself",
        "quiz": [
            {"q": "To divide by `x + 5` synthetically, what value of `c` do you use?",
             "a": ["`5`", "`-5`", "`1/5`", "`-1/5`"],
             "c": 1,
             "why": "The divisor must be read as `x - c`, and `x + 5 = x - (-5)`. So "
                    "`c = -5`, the value that makes the divisor zero."},
            {"q": "Synthetic division of `f` by `x - 2` ends with the number `0`. What follows?",
             "a": ["`f` has degree `0`", "`f(2) = 0`, so `x - 2` is a factor of `f`",
                   "The division was set up wrongly", "`f(0) = 2`"],
             "c": 1,
             "why": "By the remainder theorem the last number is `f(2)`. A zero "
                    "remainder means `f = (x - 2)q` exactly."},
            {"q": "Which divisor can NOT be handled by synthetic division as written?",
             "a": ["`x - 1`", "`x + 7`", "`x² - 4`", "`x - 1/2`"],
             "c": 2,
             "why": "The method needs a monic divisor of degree one. `x² - 4` has "
                    "degree two, so it needs long division."},
        ],
        "mistakes": [
            ("Using the sign printed in the divisor",
             "For `x + 4` the value is `c = -4`. Using `+4` performs a valid division "
             "by a different polynomial, so nothing looks wrong until the answer is "
             "checked &mdash; which is the argument for always checking."),
            ("Leaving out the zero coefficients",
             "`x³ - 8` must enter the row as `1, 0, 0, -8`. Writing `1, -8` divides "
             "some other, lower-degree polynomial and produces a confidently wrong "
             "quotient."),
            ("Reading the remainder as part of the quotient",
             "The last number is separate. For a cubic divided by a linear, the "
             "quotient has three coefficients and the fourth number is the remainder; "
             "including it makes the quotient a degree too high."),
        ],
        "standard": ("Finish when you can state the remainder without dividing.",
                     "Asked for the remainder when `x⁴ - 3x + 1` is divided by `x - 2`, "
                     "you should evaluate `f(2) = 16 - 6 + 1 = 11` and stop. Reaching "
                     "for the division at that point means the theorem has not yet "
                     "replaced the procedure."),
        "note": "Synthetic division is a compression of lesson 10, not a separate "
                "theory, and it earns its keep by being cheap enough to run many times. "
                "Lesson 12 tests a list of candidate roots one after another; doing "
                "that by long division would be accurate and unusable.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "the-factor-theorem-and-rational-roots",
        "title": "The Factor Theorem and Rational Roots",
        "module": "Division and roots",
        "one_line": "Turning a root into a factor, and generating every candidate root.",
        "summary": (
            "The factor theorem converts a question about values into a question about "
            "factors. The rational root theorem then supplies a finite list of "
            "candidates, so factoring a cubic stops being inspiration and becomes a "
            "search that can be completed &mdash; including when it finds nothing."
        ),
        "key": [
            "f(c) = 0   ⟺   (x - c) is a factor of f",
            "",
            "root p/q in lowest terms  ⟹  p | a₀  and  q | aₙ",
            "",
            "2x³ - 3x² - 8x - 3  =  (x + 1)(2x + 1)(x - 3)",
        ],
        "key_label": "Two theorems, one search",
        "concepts_intro": (
            "The first theorem says what a root is worth. The second says where to "
            "look. Together they make the search finite."
        ),
        "concepts": [
            ("A root and a factor are the same information",
             "`f(c) = 0` and `(x - c)` divides `f` are equivalent statements, not two "
             "related facts. Each direction follows from the remainder theorem in one "
             "line."),
            ("The candidate list is generated, not guessed",
             "Every rational root has numerator dividing the constant term and "
             "denominator dividing the leading coefficient. That gives a finite list "
             "you can write down before testing anything."),
            ("An empty list is a conclusion",
             "If no candidate is a root, the polynomial has no rational roots at all. "
             "It may still have irrational or complex ones &mdash; `x³ - 2` does "
             "&mdash; but none that this course can produce exactly, and saying so is "
             "the correct answer."),
        ],
        "read_title": "From roots to factors, and back",
        "read_intro": "Two theorems, a proof each, and the search they license.",
        "body": [
            ("thm", ("The factor theorem",
                     "For a polynomial `f` and a number `c`: `(x - c)` is a factor of "
                     "`f` if and only if `f(c) = 0`.")),
            ("proof", [
                "By the remainder theorem, `f(x) = (x - c)q(x) + f(c)`.",
                "If `f(c) = 0` this reads `f(x) = (x - c)q(x)`, so `(x - c)` is a "
                "factor.",
                "Conversely, if `(x - c)` is a factor then `f(x) = (x - c)h(x)` for "
                "some polynomial `h`, and substituting `x = c` gives `f(c) = 0`.",
            ]),
            ("p", "Both directions are used. Left to right, a root you have found "
                  "hands you a factor and lets you divide the degree down by one. "
                  "Right to left, a factor you have found tells you a root without "
                  "any further work."),
            ("h3", "Where to look for roots"),
            ("thm", ("The rational root theorem",
                     "Let `f(x) = aₙxⁿ + … + a₁x + a₀` have integer coefficients with "
                     "`aₙ ≠ 0` and `a₀ ≠ 0`. If the rational number `p/q`, in lowest "
                     "terms, is a root of `f`, then `p` divides `a₀` and `q` divides "
                     "`aₙ`.")),
            ("p", "Read the direction carefully. The theorem does not say that every "
                  "such `p/q` is a root &mdash; almost all of them are not. It says "
                  "that any rational root must be on that list, which is what makes "
                  "checking the list a complete search."),
            ("p", "For `2x³ - 3x² - 8x - 3` the constant term is `-3`, whose divisors "
                  "are `±1` and `±3`; the leading coefficient is `2`, whose divisors "
                  "are `±1` and `±2`. Every candidate `p/q` is therefore one of `±1`, "
                  "`±3`, `±1/2`, `±3/2` &mdash; eight numbers, and any rational root "
                  "is among them."),
            ("example", ("Factoring 2x³ - 3x² - 8x - 3 completely",
                         "Test `c = -1`: `f(-1) = -2 - 3 + 8 - 3 = 0`, so `(x + 1)` is a "
                         "factor. Synthetic division by `x + 1` gives the quotient "
                         "`2x² - 5x - 3`, which the AC method factors as "
                         "`(2x + 1)(x - 3)`. Hence "
                         "`2x³ - 3x² - 8x - 3 = (x + 1)(2x + 1)(x - 3)`, with roots "
                         "`-1`, `-1/2` and `3`.")),
            ("p", "Notice what happened after the first success. The problem became a "
                  "quadratic, and quadratics are already solved &mdash; so the "
                  "candidate list is only needed until the degree drops to two. "
                  "Testing more candidates against the original cubic would be work "
                  "with nothing to show for it."),
            ("h3", "When the search comes back empty"),
            ("example", ("x³ - 2 has no rational root",
                         "The constant term is `-2` and the leading coefficient is `1`, "
                         "so the candidates are `1, -1, 2, -2`. Evaluating: `f(1) = -1`, "
                         "`f(-1) = -3`, `f(2) = 6`, `f(-2) = -10`. None is zero, and the "
                         "list is exhausted. `x³ - 2` has no rational root, and no "
                         "rational linear factor.")),
            ("p", "It does have a real root, `∛2`, which is irrational; the theorem is "
                  "exactly the tool that proves `∛2` cannot be written as a fraction. "
                  "This course states that the root is irrational and stops there. "
                  "Approximating it is a numerical question, not an algebraic one."),
            ("thm", ("How many roots there can be",
                     "A polynomial of degree `n` has at most `n` roots. Each root `c` "
                     "contributes a factor `(x - c)`, and the degrees of the factors "
                     "cannot exceed `n`.")),
        ],
        "lab": ("factoring", {
            "mode": "roots",
            "panel_title": "The whole candidate list, tested",
            "panel_intro": "Enter the coefficients. The lab lists every divisor of "
                           "`a₀` and of `aₙ`, forms every candidate `p/q`, and "
                           "evaluates each in exact fractions. Try `x³ - 2` and watch "
                           "the list finish with no root found.",
        }),
        "steps_title": "Factoring a polynomial of degree 3 or more",
        "steps_intro": "The list first, then one root at a time, then stop early.",
        "steps": [
            ("Take out the common factor",
             "A common factor lowers the constant and leading coefficients, and so "
             "shortens the candidate list before it is written. `2x³ - 6x² + 4x` "
             "becomes `2x(x² - 3x + 2)`, and the hard part is now a quadratic."),
            ("Build the candidate list",
             "List the divisors of the constant term as `p`, the divisors of the "
             "leading coefficient as `q`, and form every `± p/q`. Remove duplicates; "
             "`2/2` and `1/1` are the same candidate."),
            ("Test candidates until one is a root",
             "Evaluate `f` at each, by synthetic division so that a hit hands you the "
             "quotient immediately. `f(c) = 0` means `(x - c)` is a factor."),
            ("Repeat on the quotient, and stop at degree 2",
             "The quotient is one degree lower; search it the same way. Once it is a "
             "quadratic, factor it or use the discriminant &mdash; no list needed."),
        ],
        "worked": {
            "title": "Factoring 2x³ - 3x² - 8x - 3",
            "intro": [
                "The constant term is `-3` and the leading coefficient is `2`, so the "
                "candidate list has eight entries and any rational root is among them."
            ],
            "lines": [
                "f(x) = 2x³ - 3x² - 8x - 3        a₀ = -3,  aₙ = 2",
                "",
                "p divides -3 :   ±1, ±3",
                "q divides  2 :   ±1, ±2",
                "candidates p/q:  ±1, ±3, ±1/2, ±3/2      (8 in total)",
                "",
                "f(1)  = 2 - 3 - 8 - 3  = -12       not a root",
                "f(-1) = -2 - 3 + 8 - 3 =   0       ROOT  ->  (x + 1) is a factor",
                "",
                "synthetic division by x + 1,  c = -1 :",
                "  -1 │   2    -3    -8    -3",
                "     │        -2     5     3",
                "     └────────────────────────",
                "         2    -5    -3     0        remainder 0, as required",
                "",
                "quotient  2x² - 5x - 3",
                "AC method: ac = -6,  pair -6 and 1,  sum -5",
                "2x² - 6x + x - 3 = 2x(x - 3) + 1(x - 3) = (2x + 1)(x - 3)",
                "",
                "2x³ - 3x² - 8x - 3 = (x + 1)(2x + 1)(x - 3)",
                "roots:  x = -1,  x = -1/2,  x = 3",
            ],
            "after": [
                "The search stopped after two candidates, and that is normal &mdash; "
                "but it stopped for a reason, not from fatigue. Once `(x + 1)` came "
                "out, the remaining problem was a quadratic, and the candidate list "
                "had done its job.",
                "Every root that appeared is on the original list: `-1`, `-1/2` and `3` "
                "are all of the form `p/q` with `p` dividing `-3` and `q` dividing `2`. "
                "That is the theorem doing what it promised, and it is worth checking "
                "once to believe it."
            ],
        },
        "quiz_title": "Check yourself",
        "quiz": [
            {"q": "For `3x³ + 2x² - 7x + 4`, which is NOT a candidate rational root?",
             "a": ["`4/3`", "`-2`", "`2/5`", "`1/3`"],
             "c": 2,
             "why": "The denominator must divide the leading coefficient `3`, and `5` "
                    "does not. The numerator must divide `4`, so `±1, ±2, ±4` over "
                    "`±1, ±3` are the candidates."},
            {"q": "`f(2) = 0` for a polynomial `f`. What is guaranteed?",
             "a": ["`x + 2` is a factor of `f`", "`x - 2` is a factor of `f`",
                   "`f` has degree `2`", "`2` is the only root of `f`"],
             "c": 1,
             "why": "The factor theorem: `f(c) = 0` is equivalent to `(x - c)` being a "
                    "factor, and here `c = 2`."},
            {"q": "Every candidate has been tested and none is a root. What can you conclude?",
             "a": ["The polynomial has no roots at all",
                   "The polynomial has no rational roots",
                   "The candidate list was built incorrectly",
                   "The polynomial cannot be factored in any way"],
             "c": 1,
             "why": "The theorem constrains only RATIONAL roots. `x³ - 2` has no "
                    "rational root but does have the real root `∛2`."},
        ],
        "mistakes": [
            ("Reading the theorem as a promise that candidates are roots",
             "The list is where roots must be, not a list of roots. For a typical "
             "cubic most of the eight candidates fail, and that is the theorem working "
             "correctly."),
            ("Getting p and q the wrong way round",
             "The numerator divides the CONSTANT term and the denominator divides the "
             "LEADING coefficient. Swapping them for `2x³ - 3x² - 8x - 3` would offer "
             "`±1, ±2, ±1/3, ±2/3` &mdash; eight candidates, of which only `-1` "
             "happens to be a root &mdash; and miss the actual root `-1/2` entirely."),
            ("Continuing to test candidates after the degree drops to two",
             "Once the quotient is a quadratic, factor it or apply the discriminant. "
             "Further candidate testing can only rediscover what those methods give "
             "directly, and it can miss irrational roots that the quadratic has."),
        ],
        "standard": ("Finish when a complete search that finds nothing reads as a proof.",
                     "You should factor `2x³ - 3x² - 8x - 3` down to three linear "
                     "factors, and state of `x³ - 2` that it has no rational root "
                     "&mdash; citing the four tested candidates as the reason rather "
                     "than reporting that you could not find one."),
        "note": "This is the lesson the course was arranged around. Course 5 needs "
                "factored denominators, course 6 needs the roots of quadratics, and "
                "lesson 13 needs the factored form to draw a graph. All three are "
                "downstream of a search that either produces exact factors or proves "
                "there are none.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "graphs-of-polynomial-functions",
        "title": "Graphs of Polynomial Functions",
        "module": "Polynomial graphs",
        "one_line": "Reading end behaviour, roots and multiplicity off the factored form.",
        "summary": (
            "The factored form answers the questions a graph asks. Degree and leading "
            "coefficient fix what happens at the far ends; each factor fixes where the "
            "curve meets the axis; and the multiplicity of a factor decides whether it "
            "crosses there or turns around."
        ),
        "key": [
            "f(x) = (x + 2)(x - 1)²(x - 3)     degree 4,  leading coefficient 1",
            "",
            "even degree, a > 0   both ends rise",
            "odd multiplicity     the curve CROSSES the axis",
            "even multiplicity    the curve TOUCHES and turns back",
            "degree n:  at most n roots,  at most n - 1 turning points",
        ],
        "key_label": "What the factored form tells you",
        "concepts_intro": (
            "A sketch here is not a plot. It is four deductions from the formula, and "
            "each one has a reason you can state."
        ),
        "concepts": [
            ("The leading term decides both ends",
             "For large `|x|` the highest power dwarfs everything else. Even degree "
             "sends both ends the same way, odd degree sends them opposite ways, and "
             "the sign of the leading coefficient says which way."),
            ("Multiplicity decides cross or touch",
             "A factor `(x - c)` appearing an odd number of times gives a sign change "
             "at `c`, so the curve crosses. An even number of times gives no sign "
             "change, so the curve touches the axis and turns back."),
            ("Degree bounds the shape",
             "A degree-`n` polynomial has at most `n` roots and at most `n - 1` "
             "turning points. A sketch with more of either is wrong before any "
             "arithmetic is checked."),
        ],
        "read_title": "Sketching from the factored form",
        "read_intro": "Four deductions, in the order that makes each one easy.",
        "body": [
            ("p", "Polynomial graphs are continuous and smooth &mdash; no jumps, no "
                  "corners, no asymptotes. Everything that distinguishes one from "
                  "another is the degree, the leading coefficient, and the roots with "
                  "their multiplicities, all of which are visible in the factored "
                  "form."),
            ("h3", "End behaviour"),
            ("thm", ("The leading term governs the ends",
                     "For `f(x) = aₙxⁿ + …` the behaviour as `x → ±∞` matches that of "
                     "`aₙxⁿ`. If `n` is even the two ends go the same way &mdash; both "
                     "up when `aₙ &gt; 0`, both down when `aₙ &lt; 0`. If `n` is odd "
                     "they go opposite ways: down-then-up when `aₙ &gt; 0`.")),
            ("p", "The reason is division rather than intuition. Writing "
                  "`f(x) = xⁿ(aₙ + aₙ₋₁/x + … + a₀/xⁿ)`, every term after `aₙ` tends "
                  "to `0` as `|x|` grows, so the bracket tends to `aₙ` and the sign of "
                  "`f` follows `aₙxⁿ`."),
            ("h3", "Roots and multiplicity"),
            ("def", ("Multiplicity",
                     "If `(x - c)^k` divides `f` but `(x - c)^(k+1)` does not, then `c` "
                     "is a root of multiplicity `k`.")),
            ("thm", ("Cross or touch",
                     "At a root of odd multiplicity the graph crosses the x-axis; at a "
                     "root of even multiplicity it touches the axis and returns to the "
                     "side it came from.")),
            ("p", "The reason is the sign of the factor. Passing `c` from left to "
                  "right, `(x - c)` changes sign, so `(x - c)^k` changes sign exactly "
                  "when `k` is odd. The other factors are non-zero near `c` and keep "
                  "their signs, so the sign of `f` changes precisely when `k` is odd."),
            ("example", ("f(x) = (x + 2)(x - 1)²(x - 3)",
                         "Degree `4` with leading coefficient `1`, so both ends rise. "
                         "The roots are `-2` with multiplicity `1` (crosses), `1` with "
                         "multiplicity `2` (touches), and `3` with multiplicity `1` "
                         "(crosses). The y-intercept is "
                         "`f(0) = (2)(1)(-3) = -6`.")),
            ("p", "That is enough for a sketch. Coming down from the upper left, the "
                  "curve crosses at `-2` into negative values, rises to touch the axis "
                  "at `1` without crossing, falls back below, and crosses at `3` on "
                  "its way up. Sample values confirm it: `f(-3) = 96`, `f(0) = -6`, "
                  "`f(2) = -4`, `f(4) = 54`."),
            ("h3", "Turning points and intercepts"),
            ("p", "A degree-`n` polynomial has at most `n - 1` turning points, so the "
                  "quartic above has at most three &mdash; and it needs all three: one "
                  "between `-2` and `1`, one at `1` itself, and one between `1` and "
                  "`3`. The y-intercept is always `f(0)`, which is the constant term "
                  "in standard form and the product of the constants in factored form."),
            ("p", "This course finds turning points only where a factor forces one, as "
                  "at the touch above. Locating the others exactly needs calculus, and "
                  "course 6 handles the one case algebra can do on its own: the vertex "
                  "of a parabola."),
        ],
        "lab": ("grapher", {
            "mode": "polynomial",
            "panel_title": "Change a multiplicity, watch the axis",
            "panel_intro": "Enter the roots and their multiplicities. The lab plots "
                           "the polynomial by evaluating it, and marks each root as a "
                           "crossing or a touch. Raise a multiplicity from `1` to `2` "
                           "and watch the crossing become a turn.",
        }),
        "steps_title": "Sketching a polynomial",
        "steps_intro": "Ends first, then the axis, then the one point you should always plot.",
        "steps": [
            ("Factor it, if it is not factored already",
             "Everything below is read off the factored form. Lessons 5 to 9 and the "
             "search of lesson 12 exist to get you here."),
            ("Fix the two ends",
             "Look at the degree and the leading coefficient only. Even degree: both "
             "ends together. Odd degree: opposite ends. Positive leading coefficient: "
             "the right-hand end rises."),
            ("Mark each root, cross or touch",
             "Odd multiplicity crosses; even multiplicity touches and turns. Write "
             "the multiplicity next to each root before drawing anything."),
            ("Plot the y-intercept and join up",
             "Compute `f(0)`. Then draw the only smooth curve consistent with the "
             "ends, the crossings and that point &mdash; using at most `n - 1` "
             "turning points."),
        ],
        "worked": {
            "title": "Sketching f(x) = (x + 2)(x - 1)²(x - 3)",
            "intro": [
                "Every line below is read from the factored form. The expanded form is "
                "computed once, only to confirm the degree and the leading coefficient."
            ],
            "lines": [
                "f(x) = (x + 2)(x - 1)²(x - 3)",
                "expanded:  x⁴ - 3x³ - 3x² + 11x - 6",
                "",
                "degree 4 (even),  leading coefficient +1",
                "  ->  both ends rise:   f -> +∞ as x -> -∞  and  as x -> +∞",
                "",
                "roots and multiplicities",
                "  x = -2   multiplicity 1   odd    CROSSES",
                "  x =  1   multiplicity 2   even   TOUCHES, turns back",
                "  x =  3   multiplicity 1   odd    CROSSES",
                "",
                "y-intercept   f(0) = (2)(1)(-3) = -6",
                "",
                "sign of f            x < -2   +        f(-3) =  96",
                "                -2 < x <  1   -        f( 0) =  -6",
                "                 1 < x <  3   -        f( 2) =  -4",
                "                     x >  3   +        f( 4) =  54",
                "",
                "at most 4 roots (3 distinct), at most 3 turning points",
            ],
            "after": [
                "The sign row is the check that the multiplicities were read "
                "correctly. `f` is negative on both sides of `x = 1`, which is exactly "
                "what an even multiplicity predicts, and it changes sign at `-2` and "
                "at `3`, as odd multiplicities require.",
                "Note that the multiplicities sum to `4`, the degree. Counted with "
                "multiplicity there are four roots here; counted as distinct points on "
                "the axis there are three. Both statements are true and they are not "
                "the same statement."
            ],
        },
        "quiz_title": "Check yourself",
        "quiz": [
            {"q": "For `f(x) = -2x⁵ + 3x² - 1`, what happens at the two ends?",
             "a": ["Both ends rise", "Both ends fall",
                   "Rises on the left, falls on the right",
                   "Falls on the left, rises on the right"],
             "c": 2,
             "why": "Degree `5` is odd, so the ends go opposite ways, and the leading "
                    "coefficient `-2` is negative, so the right-hand end falls."},
            {"q": "`f(x) = (x - 4)³(x + 1)²`. What happens at `x = -1`?",
             "a": ["The graph crosses the axis", "The graph touches the axis and turns back",
                   "The graph has a vertical asymptote", "`f` is undefined there"],
             "c": 1,
             "why": "The multiplicity of `-1` is `2`, which is even, so `(x + 1)²` does "
                    "not change sign there and the curve turns back."},
            {"q": "What is the greatest number of turning points a degree-6 polynomial can have?",
             "a": ["`4`", "`5`", "`6`", "`7`"],
             "c": 1,
             "why": "At most `n - 1` turning points for degree `n`, so at most `5`."},
        ],
        "mistakes": [
            ("Deciding the ends from the constant term or the number of roots",
             "Only the leading term matters at the ends. `x³ - 100` and `x³ + 100` "
             "behave identically as `x → ±∞`, however different they look near the "
             "origin."),
            ("Drawing every root as a crossing",
             "A squared factor touches and turns. Treating `(x - 1)²` as a crossing "
             "gives a curve on the wrong side of the axis for the whole interval that "
             "follows, and the sign check will catch it."),
            ("Sketching more turning points than the degree allows",
             "A cubic cannot wiggle three times. If your curve needs four turning "
             "points to reach all the marked roots, one of the multiplicities has been "
             "misread."),
        ],
        "standard": ("Finish when you can sketch from the factored form without plotting points.",
                     "Given `f(x) = (x + 2)(x - 1)²(x - 3)` you should produce the "
                     "shape from the ends, the three roots with their multiplicities "
                     "and `f(0)` alone &mdash; using sample values only to confirm the "
                     "signs, never to discover them."),
        "note": "This is where the course arrives. The graph is drawn from the "
                "factored form, the factored form came from the search in lesson 12, "
                "and that search was made possible by the techniques of lessons 5 to "
                "9. Anything the lab plots is computed by evaluating the polynomial "
                "you entered, so a curve that looks wrong is telling you something "
                "about the polynomial rather than about the drawing.",
    },
]
