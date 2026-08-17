"""Course 6, lessons 08-14 — complex arithmetic, parabolas, optimisation and substitution."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "operations-with-complex-numbers",
        "title": "Operations with Complex Numbers",
        "module": "Complex numbers",
        "one_line": "Arithmetic, and the conjugate that makes division work.",
        "summary": (
            "Addition and subtraction collect like terms, multiplication is the "
            "distributive law followed by a single substitution, and division is "
            "multiplication by the conjugate. An answer is finished only when it is "
            "written as `a + bi` with `a` and `b` real."
        ),
        "key": [
            "(a + bi) + (c + di)  =  (a + c) + (b + d)i",
            "(a + bi)(c + di)     =  (ac - bd) + (ad + bc)i      because i² = -1",
            "conjugate of a + bi  =  a - bi",
            "(a + bi)(a - bi)     =  a² + b²      real, and 0 only when a = b = 0",
        ],
        "key_label": "Three operations and the conjugate",
        "concepts_intro": (
            "Complex arithmetic is ordinary algebra in one letter, with one rule "
            "applied at the end and one form the answer has to reach."
        ),
        "concepts": [
            ("Treat i as a variable until the last step",
             "Expand `(3 + 2i)(4 - 5i)` exactly as you would expand `(3 + 2t)(4 - 5t)`. "
             "Only then replace `i²` by `-1`. Nothing about the manipulation is new; "
             "the substitution is the only thing that is."),
            ("Standard form is the finishing line",
             "An answer is `a + bi` with `a` and `b` real. `2/(1 + i)` is a complex "
             "number but is not yet in that form. Two complex numbers are compared "
             "part by part &mdash; and only for equality: there is no ordering of the "
             "complex numbers that respects the arithmetic, so `3 + 2i &lt; 5` is not "
             "a false statement, it is not a statement at all."),
            ("The conjugate turns a denominator real",
             "`(a + bi)(a - bi) = a² + b²`, with no `i` left. That one fact is the "
             "whole of complex division, and it is the same cancellation that cleared "
             "`2 + √3` from a denominator in course 5."),
        ],
        "read_title": "Arithmetic in a + bi",
        "read_intro": "Four operations, and the one substitution they all come down to.",
        "body": [
            ("p", "Lesson 7 defined `i` by `i² = -1` and called `a + bi` a complex "
                  "number, with real part `a` and imaginary part `b`, both of them real "
                  "numbers. The arithmetic below is arranged so that every law from "
                  "course 1 &mdash; commutativity, associativity, distribution "
                  "&mdash; keeps working unchanged. That was the design goal when the "
                  "system was built, and it is why there is so little to learn here."),
            ("def", ("Addition and subtraction",
                     "`(a + bi) + (c + di) = (a + c) + (b + d)i`, and "
                     "`(a + bi) - (c + di) = (a - c) + (b - d)i`. Real parts combine "
                     "with real parts, imaginary parts with imaginary parts.")),
            ("p", "Nothing is being asserted beyond collecting like terms: `bi` and "
                  "`di` are both multiples of `i`, so they add the way `3t` and `5t` "
                  "do. `(2 - 7i) - (5 + 3i) = -3 - 10i`, and the minus sign has to "
                  "reach both parts of the second bracket &mdash; the same place a "
                  "sign goes missing when polynomials are subtracted in course 4."),
            ("def", ("Multiplication",
                     "`(a + bi)(c + di) = (ac - bd) + (ad + bc)i`. Do not memorise "
                     "that. Expand the two brackets, replace `i²` by `-1`, and "
                     "collect; the formula is what that always produces.")),
            ("math", [
                "(a + bi)(c + di) =  ac + adi + bci + bd·i²",
                "                 =  ac + adi + bci - bd            since i² = -1",
                "                 = (ac - bd) + (ad + bc)i",
            ]),
            ("example", ("A product in full",
                         "`(3 + 2i)(4 - 5i) = 12 - 15i + 8i - 10i²`. Now `-10i²` is "
                         "`-10 · (-1) = +10`, so the answer is `22 - 7i`.",
                         "The `+10` is where complex multiplication goes wrong. "
                         "Subtracting `10i²` <em>adds</em> 10, and an answer that is "
                         "20 out from the right one usually has that step in it.")),
            ("h3", "Powers of i"),
            ("math", [
                "i⁰ = 1      i¹ = i      i² = -1      i³ = -i",
                "i⁴ = 1      i⁵ = i      i⁶ = -1      i⁷ = -i",
                "",
                "i⁴ = (i²)² = (-1)² = 1,  so the four values repeat for ever",
            ]),
            ("p", "So `iⁿ` depends only on the remainder of `n` on division by 4. "
                  "`i²³` has `23 = 4·5 + 3`, remainder 3, so `i²³ = -i`. Written out: "
                  "`i²³ = (i⁴)⁵ · i³ = 1 · i³ = -i`."),
            ("p", "One law from course 1 does <strong>not</strong> extend. "
                  "`√a · √b = √(ab)` is stated for non-negative `a` and `b`, and it "
                  "fails here: `√-4 · √-9` is `2i · 3i = 6i² = -6`, not `√36 = 6`. "
                  "Convert every root of a negative number to `i` first, then "
                  "multiply."),
            ("def", ("Complex conjugate",
                     "The conjugate of `a + bi` is `a - bi`: same real part, opposite "
                     "imaginary part. Conjugating twice returns the original number, "
                     "and a number equals its own conjugate exactly when `b = 0`, "
                     "that is, exactly when it is real.")),
            ("thm", ("The conjugate product is real",
                     "For real `a` and `b`, `(a + bi)(a - bi) = a² + b²`. This is a "
                     "real number, it is never negative, and it is `0` only when "
                     "`a = 0` and `b = 0`.")),
            ("proof", [
                "Expand: `(a + bi)(a - bi) = a² - abi + abi - b²i²`. The two cross "
                "terms are negatives of one another and cancel.",
                "The last term is `-b²i² = -b²(-1) = b²`, so what remains is "
                "`a² + b²`, with no `i` in it.",
                "`a` and `b` are real, so `a²` and `b²` are each at least `0` and the "
                "sum is at least `0`. A sum of two non-negative numbers is `0` only "
                "when both are `0`, which forces `a = 0` and `b = 0`.",
            ]),
            ("p", "That is what makes division work. To divide by `c + di`, multiply "
                  "above and below by `c - di`. Multiplying a fraction by "
                  "`(c - di)/(c - di)` is multiplying it by `1`, so the value is "
                  "untouched &mdash; only the form changes, and the new denominator "
                  "`c² + d²` is an ordinary real number you can divide by."),
            ("example", ("A quotient",
                         "`(4 + i)/(2 + 3i)`. The conjugate of the denominator is "
                         "`2 - 3i`. On top: `(4 + i)(2 - 3i) = 8 - 12i + 2i - 3i² = "
                         "11 - 10i`. Underneath: `(2 + 3i)(2 - 3i) = 4 + 9 = 13`. So "
                         "the quotient is `11/13 - (10/13)i`.")),
            ("thm", ("Every non-zero complex number has a reciprocal",
                     "If `a + bi ≠ 0` then `a² + b² &gt; 0`, and "
                     "`1/(a + bi) = (a - bi)/(a² + b²)`, which is again of the form "
                     "`p + qi` with `p` and `q` real. So the complex numbers are "
                     "closed under all four operations: adding, subtracting, "
                     "multiplying and dividing them never leads outside the system.")),
        ],
        "lab": ("complex", {
            "mode": "arith",
            "panel_title": "Two complex numbers, four operations",
            "panel_intro": "Set `z` and `w`, then read the sum, difference, product "
                           "and quotient computed side by side. In the quotient, watch "
                           "the conjugate of `w` appear on the top and the bottom at "
                           "once: that is multiplication by `1`, which is the reason "
                           "the value survives the rewriting.",
        }),
        "steps_title": "Dividing one complex number by another",
        "steps_intro": "Four steps. The second is the whole method; the rest is arithmetic.",
        "steps": [
            ("Write the quotient as a fraction",
             "`(3 + 2i) ÷ (1 - 4i)` becomes `(3 + 2i)/(1 - 4i)`. Nothing can be "
             "cancelled yet, and cancelling a term rather than a factor is as illegal "
             "here as it was in course 5."),
            ("Multiply top and bottom by the conjugate of the denominator",
             "The conjugate of `1 - 4i` is `1 + 4i`. You are multiplying by "
             "`(1 + 4i)/(1 + 4i)`, which is `1`, so the value cannot change."),
            ("Expand both products and replace i² by -1",
             "The denominator becomes `1 + 16 = 17`: real, with the cross terms gone. "
             "That cancellation is the only reason the conjugate is the right thing "
             "to multiply by rather than any other complex number."),
            ("Split into two real fractions",
             "`(p + qi)/r = p/r + (q/r)i`. Keep exact fractions &mdash; `-5/17` is the "
             "answer, and a decimal is a rounding of it."),
        ],
        "worked": {
            "title": "(3 + 2i) divided by (1 - 4i)",
            "intro": [
                "The denominator is `1 - 4i`, so the conjugate in play is `1 + 4i`. "
                "Everything else is expansion."
            ],
            "lines": [
                "     3 + 2i     3 + 2i     1 + 4i",
                "     ------  =  ------  ·  ------          multiplying by 1",
                "     1 - 4i     1 - 4i     1 + 4i",
                "",
                "top:     (3 + 2i)(1 + 4i) = 3 + 12i + 2i + 8i²",
                "                          = 3 + 14i - 8",
                "                          = -5 + 14i",
                "",
                "bottom:  (1 - 4i)(1 + 4i) = 1 + 4i - 4i - 16i²",
                "                          = 1 + 16",
                "                          = 17",
                "",
                "     -5 + 14i        5     14",
                "     --------  =  - --  +  -- i          standard form",
                "        17          17     17",
                "",
                "check:   (-5/17 + (14/17)i)(1 - 4i)",
                "           real part:  -5/17 + 56/17 = 51/17 = 3    ✓",
                "           imaginary:  20/17 + 14/17 = 34/17 = 2    ✓",
            ],
            "after": [
                "The bottom lost its `i` because `+4i` and `-4i` cancel. That is the "
                "one thing the conjugate is chosen for; multiplying above and below by "
                "`1 - 4i` instead would give `(1 - 4i)² = -15 - 8i`, which is no "
                "improvement.",
                "The last line is standard form. `(-5 + 14i)/17` is the same number, "
                "but a real part and an imaginary part cannot be read off it, so it is "
                "not yet an answer.",
            ],
        },
        "quiz_title": "Complex arithmetic",
        "quiz": [
            {"q": "What is `(2 + 3i)(2 - 3i)`?",
             "a": ["`-5`", "`13`", "`4 + 9i`", "`13i`"],
             "c": 1,
             "why": "`(a + bi)(a - bi) = a² + b² = 4 + 9 = 13`. `-5` comes from "
                    "replacing `i²` by `+1`; `4 + 9i` comes from squaring `3i` as "
                    "`9i` rather than `-9`; and a product of conjugates has no "
                    "imaginary part at all, so `13i` cannot be right."},
            {"q": "Written in standard form, `1/i` is:",
             "a": ["`i`", "`-i`", "`-1`", "`1`"],
             "c": 1,
             "why": "The conjugate of `i` is `-i`, and `(1)(-i) / (i)(-i) = -i / 1 = "
                    "-i`. Multiplying above and below by `i` instead gives "
                    "`i/i² = i/(-1)`, which is the same `-i` once that sign flip is "
                    "carried out; the answer `i` comes from stopping at `i/(-1)` and "
                    "never performing the flip."},
            {"q": "To put `(4 + i)/(2 + 3i)` in standard form, multiply the top and "
                  "the bottom by:",
             "a": ["`2 - 3i`", "`2 + 3i`", "`-2 + 3i`", "`3 + 2i`"],
             "c": 0,
             "why": "The conjugate of the denominator: `(2 + 3i)(2 - 3i) = 13`, a real "
                    "number. `(2 + 3i)(2 + 3i) = -5 + 12i` is still complex, and "
                    "`3 + 2i` is the two parts swapped, which is not the conjugate of "
                    "anything here."},
        ],
        "mistakes": [
            ("Leaving i² in the answer",
             "`i²` is not a term to be carried, it is the number `-1`. An expression "
             "still containing `i²` is unfinished, and the error it hides is usually "
             "double the size of that term: `-10i²` is `+10`, so getting it wrong "
             "moves the answer by 20."),
            ("Multiplying only the denominator by the conjugate",
             "That changes the value of the fraction. The legal move is multiplying by "
             "`(c - di)/(c - di)`, which is `1`; multiplying the bottom alone is "
             "multiplying the fraction by `1/(c - di)`, which is a different number."),
            ("Using √a · √b = √(ab) on negatives",
             "`√-4 · √-9` is `2i · 3i = -6`, not `6`. The radical law assumes "
             "non-negative radicands, and this is the one place in the course where "
             "quoting a law outside its hypotheses gives a wrong sign rather than a "
             "wrong form."),
        ],
        "standard": ("Finish when every answer you write is in the form a + bi.",
                     "Multiply two complex numbers, divide two complex numbers and "
                     "reduce a power of `i`, without looking anything up. The check on "
                     "a quotient is multiplying it back by the divisor: three lines, "
                     "and it catches the sign slips this arithmetic invites."),
        "note": "The conjugate is doing here exactly what it did in course 5 when a "
                "denominator like `2 + √3` had to be cleared: multiply by the thing "
                "that makes the cross terms cancel. The next lesson turns it into a "
                "statement about solutions &mdash; a quadratic with real coefficients "
                "that has one non-real root has that root's conjugate as its other "
                "one.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "complex-roots-of-quadratics",
        "title": "Complex Roots of Quadratics",
        "module": "Complex numbers",
        "one_line": "A negative discriminant, and the pair it produces.",
        "summary": (
            "When `b² - 4ac` is negative the quadratic formula still works: the root "
            "of the negative discriminant becomes a multiple of `i`, and the two "
            "solutions are conjugates of one another. Every quadratic with real "
            "coefficients has exactly two solutions once complex numbers are allowed."
        ),
        "key": [
            "b² - 4ac < 0   →   two solutions, neither of them real",
            "x = -b/(2a)  ±  ( √(4ac - b²) / (2a) ) i",
            "the pair is p + qi and p - qi:  conjugates, since only ± differs",
            "sum = -b/a      product = c/a      both still real",
        ],
        "key_label": "What a negative discriminant produces",
        "concepts_intro": (
            "Lesson 6 counted the real solutions. This lesson finds the ones it "
            "counted as absent."
        ),
        "concepts": [
            ("Negative discriminant means no REAL solution",
             "It does not mean no solution. `x² + 4 = 0` has no real solution and two "
             "complex ones, `2i` and `-2i`. Dropping the word \"real\" is the error "
             "the whole lesson is aimed at."),
            ("The two roots are conjugates",
             "The formula produces `-b/(2a) ± (something)i`, and the `±` is the only "
             "difference between the two answers. So one is `p + qi` and the other is "
             "`p - qi`, provided `a`, `b`, `c` are real."),
            ("A conjugate pair is a parabola that misses the axis",
             "x-intercepts are real solutions. If there are none of those, the curve "
             "never reaches the x-axis &mdash; the two solutions are still there, but "
             "not at any point of the picture."),
        ],
        "read_title": "Solving with a negative discriminant",
        "read_intro": "The formula does not change. What changes is what is under the root.",
        "body": [
            ("p", "Lesson 6 read the sign of `D = b² - 4ac` and reported two, one or "
                  "no real solutions. The last case was left open on purpose: `√D` "
                  "with `D &lt; 0` had no meaning yet. Lesson 7 gave it one, and "
                  "nothing else about the method needs adjusting."),
            ("thm", ("Solutions when the discriminant is negative",
                     "Let `a`, `b`, `c` be real with `a ≠ 0`, and let "
                     "`D = b² - 4ac &lt; 0`. Then `ax² + bx + c = 0` has exactly two "
                     "solutions, `x = -b/(2a) ± (√(-D)/(2a)) i`, and each is the "
                     "conjugate of the other.")),
            ("proof", [
                "`D &lt; 0`, so `-D &gt; 0` and `√(-D)` is an ordinary positive real "
                "number. Since `(i√(-D))² = i² · (-D) = -(-D) = D`, the quantity "
                "`i√(-D)` is a square root of `D`.",
                "Putting that into the formula gives "
                "`x = (-b ± i√(-D)) / (2a)`, and dividing both parts of the numerator "
                "by `2a` gives `x = -b/(2a) ± (√(-D)/(2a)) i`.",
                "`a`, `b` and `D` are real and `a ≠ 0`, so `-b/(2a)` and "
                "`√(-D)/(2a)` are both real numbers. The two solutions therefore have "
                "the same real part and opposite imaginary parts, which is what it "
                "means to be conjugates.",
            ]),
            ("p", "Both parts of the numerator are divided by `2a`. Writing "
                  "`x = (-6 ± 4i)/2` as `-3 ± 4i` divides the real part and forgets "
                  "the other; the correct reduction is `-3 ± 2i`."),
            ("example", ("x² - 6x + 13 = 0",
                         "`D = 36 - 52 = -16`, so `√(-D) = √16 = 4` and "
                         "`x = (6 ± 4i)/2 = 3 ± 2i`. The two solutions are `3 + 2i` "
                         "and `3 - 2i`.")),
            ("h3", "The same pair by completing the square"),
            ("math", [
                "x² - 6x + 13 = 0",
                "(x - 3)² - 9 + 13 = 0            half of -6 is -3, squared is 9",
                "(x - 3)² = -4",
                "x - 3 = ±2i                      since (2i)² = -4",
                "x = 3 ± 2i",
            ]),
            ("p", "Two methods, computed independently, agreeing. That is the pattern "
                  "the whole course is built on, and it is worth noticing that "
                  "completing the square never had to mention the discriminant: the "
                  "negative appears on its own, as the number a square is being asked "
                  "to equal."),
            ("thm", ("Conjugate pairs need real coefficients",
                     "The pairing is a consequence of `a`, `b` and `c` being real "
                     "numbers. Without that hypothesis it fails: `x² - ix = 0` factors "
                     "as `x(x - i) = 0`, so its solutions are `0` and `i`, which are "
                     "not conjugates of one another.")),
            ("p", "With the pair in hand the quadratic factors, just not over the "
                  "reals: `x² - 6x + 13 = (x - 3 - 2i)(x - 3 + 2i)`. Expanding "
                  "confirms it, since `(x - 3)² - (2i)² = x² - 6x + 9 + 4`. Course 4 "
                  "called such a quadratic irreducible; that word always means "
                  "irreducible <em>over some system</em>, and over the complex numbers "
                  "no quadratic is."),
            ("p", "The sum and product survive as a check. For `3 ± 2i` the sum is "
                  "`6 = -b/a` and the product is `(3 + 2i)(3 - 2i) = 9 + 4 = 13 = "
                  "c/a`. Both come out real, as they must: the imaginary parts cancel "
                  "in the sum and the conjugate product is real by lesson 8."),
            ("example", ("2x² + 3x + 5 = 0",
                         "`D = 9 - 40 = -31`, which is negative and not a perfect "
                         "square. `x = (-3 ± i√31)/4 = -3/4 ± (√31/4) i`. The root "
                         "`√31` stays exactly as it is; there is nothing to simplify "
                         "and a decimal would only lose information.")),
            ("p", "On the graph nothing dramatic happens. The parabola "
                  "`y = x² - 6x + 13` sits entirely above the x-axis &mdash; its "
                  "lowest point is `(3, 4)` &mdash; so it has no x-intercepts, which "
                  "is the picture of \"no real solutions\". The conjugate pair is not "
                  "hiding anywhere in that picture, and lesson 10 explains why the "
                  "picture only ever shows real numbers."),
        ],
        "lab": ("complex", {
            "mode": "roots",
            "panel_title": "The pair a negative discriminant produces",
            "panel_intro": "Choose a quadratic whose discriminant is negative and "
                           "watch the formula run. The two answers differ only in the "
                           "sign of the imaginary part; the parabola drawn beside them "
                           "never reaches the x-axis, which is the same fact told "
                           "twice.",
        }),
        "steps_title": "Solving when the discriminant is negative",
        "steps_intro": "The discriminant is computed first, so that nothing later is a surprise.",
        "steps": [
            ("Compute D = b² - 4ac before anything else",
             "If it is negative you already know the shape of the answer: two "
             "conjugate solutions, and no x-intercept on the graph."),
            ("Write the root of the negative as a multiple of i",
             "`√-36 = 6i`, because `(6i)² = 36i² = -36`. Take the positive multiple "
             "here; the `±` already in the formula supplies the other sign, and "
             "writing `-6i` as well would count each solution twice."),
            ("Divide BOTH parts of the numerator by 2a",
             "`(-2 ± 6i)/4` is `-1/2 ± (3/2)i`. This is the step that is quietly "
             "skipped more often than any other in the lesson."),
            ("Check one solution by substituting it",
             "The other needs no separate check. Conjugating an equation with real "
             "coefficients conjugates both sides, and `0` is its own conjugate, so "
             "if one of the pair works the other does too."),
        ],
        "worked": {
            "title": "2x² + 2x + 5 = 0",
            "intro": [
                "`a = 2`, `b = 2`, `c = 5`. Nothing here factors and there is no "
                "missing linear term, so the formula is the method."
            ],
            "lines": [
                "D = b² - 4ac = 2² - 4(2)(5) = 4 - 40 = -36        negative",
                "",
                "x = ( -2 ± √-36 ) / (2·2)",
                "",
                "√-36 = 6i                       since (6i)² = 36i² = -36",
                "",
                "x = ( -2 ± 6i ) / 4",
                "",
                "       2      6             1      3",
                "x = -  --  ±  -- i   =   -  --  ±  -- i",
                "       4      4             2      2",
                "",
                "check   x = -1/2 + (3/2)i :",
                "",
                "   x²           = 1/4 - (3/2)i + (9/4)i²  =  -2 - (3/2)i",
                "   2x²          = -4 - 3i",
                "   2x           = -1 + 3i",
                "   2x² + 2x + 5 = (-4 - 3i) + (-1 + 3i) + 5 = 0        ✓",
            ],
            "after": [
                "Both parts of the numerator were divided by 4. Stopping at "
                "`(-2 ± 6i)/4`, or dividing only the `-2`, are the two ways this last "
                "step fails, and the substitution above catches either of them "
                "immediately.",
                "The other solution is `-1/2 - (3/2)i`. Its check is the conjugate of "
                "the one written out, line for line, so doing it again would confirm "
                "nothing new.",
            ],
        },
        "quiz_title": "Negative discriminants",
        "quiz": [
            {"q": "Solve `x² - 2x + 5 = 0`.",
             "a": ["`x = 1 ± 2i`", "`x = -1 ± 2i`", "`x = 1 ± 4i`",
                   "There are no solutions"],
             "c": 0,
             "why": "`D = 4 - 20 = -16`, so `x = (2 ± 4i)/2 = 1 ± 2i`. `-1 ± 2i` uses "
                    "`b` where the formula wants `-b`; `1 ± 4i` divides only the real "
                    "part by `2a`; and a negative discriminant rules out real "
                    "solutions, not solutions."},
            {"q": "`5 - 3i` is a solution of a quadratic equation with real "
                  "coefficients. The other solution is:",
             "a": ["`5 + 3i`", "`-5 + 3i`", "`3 - 5i`", "It cannot be determined"],
             "c": 0,
             "why": "Conjugating changes the sign of the imaginary part only. "
                    "`-5 + 3i` negates both parts, `3 - 5i` swaps them, and the "
                    "answer is determined precisely because the coefficients were "
                    "stated to be real."},
            {"q": "A quadratic with real coefficients has `D = -24`. What follows?",
             "a": ["Two real solutions, and the parabola crosses the x-axis twice",
                   "One repeated solution, and the parabola touches the x-axis",
                   "Two conjugate non-real solutions, and the parabola never meets "
                   "the x-axis",
                   "The equation has no solutions of any kind"],
             "c": 2,
             "why": "`D &lt; 0` gives the conjugate pair "
                    "`-b/(2a) ± (√24/(2a)) i`. x-intercepts are real solutions, so "
                    "there are none of those; the solutions exist, they are simply "
                    "not on the real line the picture is drawn on."},
        ],
        "mistakes": [
            ("Answering \"no solution\" with no qualifier",
             "After this lesson the honest answers are \"no real solution\" or \"two "
             "complex solutions\". `x² + 4 = 0` has both descriptions and they do not "
             "contradict each other."),
            ("Dividing only part of the numerator by 2a",
             "`(-2 ± 6i)/4` is `-1/2 ± (3/2)i`, not `-1/2 ± 6i`. The fraction bar "
             "runs under the whole numerator, exactly as it does when the "
             "discriminant is positive."),
            ("Writing √-36 as -6",
             "`(-6)² = 36`, not `-36`, so `-6` is not a square root of `-36`. The "
             "minus does not come out of a square root as a factor of `-1`; it comes "
             "out as a factor of `i`, and `i` is not a real number that can be "
             "absorbed into the sign."),
        ],
        "standard": ("Finish when a negative discriminant makes you reach for i rather than stop.",
                     "Take any quadratic with `D &lt; 0`, produce the conjugate pair "
                     "in the form `p ± qi` with `p` and `q` exact, and verify one of "
                     "them by substitution. If the check is a nuisance, the arithmetic "
                     "of lesson 8 needs another pass before this one does."),
        "note": "Every quadratic with real coefficients now has exactly two solutions "
                "&mdash; two distinct real ones, one repeated real one, or a conjugate "
                "pair. That completeness is what the complex numbers were introduced "
                "for. The remaining lessons return to real coefficients and real "
                "graphs, where the discriminant decides how the parabola meets the "
                "axis.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "graphs-of-quadratic-functions",
        "title": "Graphs of Quadratic Functions",
        "module": "Parabolas",
        "one_line": "The parabola, its direction, and its intercepts.",
        "summary": (
            "The graph of `y = ax² + bx + c` is a parabola. The sign of `a` decides "
            "which way it opens, `c` is the y-intercept, the real solutions of "
            "`ax² + bx + c = 0` are the x-intercepts, and the curve is symmetric about "
            "the line `x = -b/(2a)`."
        ),
        "key": [
            "y = ax² + bx + c,  a ≠ 0            the graph is a parabola",
            "a > 0  opens upward        a < 0  opens downward",
            "y-intercept (0, c)         x-intercepts: the real solutions",
            "axis of symmetry  x = -b/(2a),  midway between the roots",
        ],
        "key_label": "Everything readable from a, b and c",
        "concepts_intro": (
            "Four features, each one read from the equation rather than discovered by "
            "plotting."
        ),
        "concepts": [
            ("Only a decides the direction",
             "`b` and `c` slide the curve about; they never turn it over. "
             "`y = x² - 100` opens upward and `y = -x² + 100` opens downward, and the "
             "constants had nothing to do with it."),
            ("Intercepts are the two solved problems you already have",
             "Setting `x = 0` gives the y-intercept, `c`, in one step. Setting "
             "`y = 0` gives the x-intercepts, which is the equation lessons 1 to 6 "
             "solved &mdash; so the discriminant counts them: two, one or none."),
            ("The curve is symmetric, exactly",
             "Every parabola has a vertical mirror line, `x = -b/(2a)`. Two points "
             "the same distance either side of it have the same height, which halves "
             "the work of plotting and checks the arithmetic for free."),
        ],
        "read_title": "Reading a parabola off its equation",
        "read_intro": "Direction, then intercepts, then the line the whole picture folds along.",
        "body": [
            ("def", ("Quadratic function",
                     "A function `f(x) = ax² + bx + c` with `a`, `b`, `c` real and "
                     "`a ≠ 0`. The condition `a ≠ 0` is not decoration: with `a = 0` "
                     "the graph is a straight line and none of this lesson applies.")),
            ("p", "The graph of a quadratic function is a curve called a "
                  "<strong>parabola</strong>. Every quadratic gives one, and they are "
                  "all the same shape up to stretching and moving &mdash; a fact "
                  "lesson 11 makes precise. This course meets the parabola only as the "
                  "graph of a function; its geometric definition is a topic for conic "
                  "sections and is not needed here."),
            ("p", "The coefficient `a` does two jobs. Its sign sets the direction: "
                  "`a &gt; 0` opens upward, `a &lt; 0` opens downward. Its size sets "
                  "the steepness: at `x = 2`, `y = x²` is at height 4, `y = 2x²` at 8 "
                  "and `y = (1/2)x²` at 2, so a larger `|a|` gives a narrower curve. "
                  "The three parabolas are otherwise identical in shape."),
            ("p", "The y-intercept is `f(0) = c`, and there is exactly one of them, "
                  "because `f` is a function and course 3 fixed that a function "
                  "assigns one output to the input `0`. No vertical line can meet the "
                  "graph twice, including the y-axis."),
            ("p", "The x-intercepts are the values of `x` with `f(x) = 0` &mdash; the "
                  "real solutions of the quadratic equation. So the discriminant of "
                  "lesson 6 counts them before any drawing: `D &gt; 0` gives two "
                  "crossings, `D = 0` gives one point where the curve touches the axis "
                  "and turns back, and `D &lt; 0` gives none at all. A parabola with "
                  "no x-intercept lies entirely on one side of the axis."),
            ("thm", ("Symmetry about x = -b/(2a)",
                     "Let `f(x) = ax² + bx + c` with `a ≠ 0` and write `h = -b/(2a)`. "
                     "Then `f(h + t) = f(h) + at²` for every real `t`. In particular "
                     "`f(h + t) = f(h - t)`: the graph is symmetric about the vertical "
                     "line `x = h`.")),
            ("proof", [
                "Expand: `f(h + t) = a(h + t)² + b(h + t) + c = ah² + 2aht + at² + bh + bt + c`.",
                "Group the terms by their power of `t`: "
                "`f(h + t) = (ah² + bh + c) + (2ah + b)t + at² = f(h) + (2ah + b)t + at²`.",
                "Now `2ah + b = 2a·(-b/(2a)) + b = -b + b = 0`, so the middle term "
                "vanishes and `f(h + t) = f(h) + at²`.",
                "Replacing `t` by `-t` leaves `at²` unchanged, so "
                "`f(h - t) = f(h) + at² = f(h + t)`. Two points at equal distances "
                "either side of `x = h` have equal heights, which is what symmetry "
                "about that line means.",
            ]),
            ("p", "When there are two x-intercepts, the axis runs midway between them "
                  "&mdash; the same conclusion reached from the formula rather than "
                  "from the symmetry."),
            ("math", [
                "roots      (-b + √D)/(2a)     and     (-b - √D)/(2a)",
                "",
                "                (-b + √D)/(2a)  +  (-b - √D)/(2a)",
                "midpoint  =  ---------------------------------------",
                "                                2",
                "",
                "             (-2b)/(2a)      -b/a       -b",
                "          =  ----------  =  ------  =  ----",
                "                  2            2         2a",
            ]),
            ("h3", "Sketching from the intercepts"),
            ("math", [
                "y = x² - 2x - 8          a = 1 > 0,  so it opens upward",
                "",
                "  x    -3   -2   -1    0    1    2    3    4    5",
                "  y     7    0   -5   -8   -9   -8   -5    0    7",
                "                              |",
                "                        axis  x = 1",
                "",
                "the table is symmetric about x = 1:  y(-2) = y(4),  y(0) = y(2)",
            ]),
            ("example", ("y = -x² + 4x - 3",
                         "`a = -1`, so the curve opens downward. `f(0) = -3` gives the "
                         "y-intercept `(0, -3)`. Factoring, "
                         "`-x² + 4x - 3 = -(x - 1)(x - 3)`, so the x-intercepts are "
                         "`1` and `3`; the axis is `x = 2`, midway between them, and "
                         "`f(2) = 1`. The highest point of the graph is `(2, 1)`.")),
            ("p", "Sample points on both sides of the axis. A table for "
                  "`x = 0, 1, 2, 3` on a parabola whose axis is `x = -4` returns four "
                  "points from one arm, which join up into something that looks like a "
                  "line bending &mdash; a picture that is not wrong so much as "
                  "unrecognisable. Find the axis first, then choose the x-values."),
            ("p", "When a quadratic factors, `f(x) = a(x - r)(x - s)` is worth writing "
                  "down: the roots `r` and `s` are visible, the axis is at their "
                  "midpoint `(r + s)/2`, and `f(0) = a·r·s` gives the y-intercept "
                  "without expanding. The next lesson does the same job for the "
                  "quadratics that do not factor."),
        ],
        "lab": ("quadratic", {
            "mode": "graph",
            "panel_title": "Direction, intercepts, axis",
            "panel_intro": "Change `a` on its own and watch the direction and the "
                           "width; change `c` on its own and watch the whole curve "
                           "slide vertically with its shape untouched. The roots and "
                           "the vertex marked on the picture are the exact values "
                           "printed beside it, so the drawing cannot flatter the "
                           "algebra.",
        }),
        "steps_title": "Sketching y = ax² + bx + c",
        "steps_intro": "Five numbers give the sketch. Four of them come from arithmetic you have already done.",
        "steps": [
            ("Read the direction off a",
             "Positive opens upward, negative downward. Do this first: it tells you "
             "which side of the axis the curve lives on if it has no x-intercepts."),
            ("Plot the y-intercept (0, c)",
             "One substitution, `x = 0`, and it is free. Every parabola has exactly "
             "one."),
            ("Find the x-intercepts, or show there are none",
             "Solve `ax² + bx + c = 0` by whichever of lessons 2 to 5 is quickest, or "
             "compute `D` and stop there if it is negative."),
            ("Draw the axis x = -b/(2a), then use symmetry",
             "Plot the point on the axis, `(h, f(h))`, and reflect every other point "
             "you have across it. Two or three plotted points and the mirror line are "
             "enough for an honest sketch."),
        ],
        "worked": {
            "title": "Sketching y = x² - 2x - 8",
            "intro": [
                "`a = 1`, `b = -2`, `c = -8`. Nothing is plotted until the four "
                "features are written down."
            ],
            "lines": [
                "direction      a = 1 > 0                      opens upward",
                "",
                "y-intercept    f(0) = -8                      (0, -8)",
                "",
                "x-intercepts   x² - 2x - 8 = (x - 4)(x + 2)",
                "               x = 4   and   x = -2",
                "",
                "axis           x = -b/(2a) = 2/2 = 1          midpoint of -2 and 4",
                "",
                "point on it    f(1) = 1 - 2 - 8 = -9          (1, -9)",
                "",
                "symmetry check",
                "   f(-2) =  0  =  f(4)          both 3 units from x = 1     ✓",
                "   f( 0) = -8  =  f(2)          both 1 unit  from x = 1     ✓",
            ],
            "after": [
                "Five numbers determine the sketch: the direction, the y-intercept, "
                "two x-intercepts and the point on the axis. Everything else in the "
                "drawing is symmetry, not information.",
                "The point `(1, -9)` is the lowest point of this curve. It is called "
                "the vertex, and the next lesson gets it straight from the equation "
                "without solving anything or plotting anything.",
            ],
        },
        "quiz_title": "Reading the graph",
        "quiz": [
            {"q": "Which way does the graph of `y = -2x² + 3x + 1` open?",
             "a": ["Upward, because `c = 1` is positive",
                   "Downward, because `a = -2` is negative",
                   "Upward, because `b = 3` is positive",
                   "It depends on where the x-intercepts are"],
             "c": 1,
             "why": "Only the coefficient of `x²` decides. `b` and `c` move the "
                    "parabola around the plane; no value of either can turn it over."},
            {"q": "Where does the graph of `y = 3x² - 5x + 7` cross the y-axis?",
             "a": ["`(0, 7)`", "`(7, 0)`", "`(0, 3)`", "`(0, -5)`"],
             "c": 0,
             "why": "Put `x = 0`: `y = c = 7`. `(7, 0)` is a point on the x-axis, and "
                    "this graph has no x-intercepts at all, since "
                    "`D = 25 - 84 = -59`. The other two read off the wrong "
                    "coefficient."},
            {"q": "How many times does the graph of `y = x² + 2x + 5` meet the x-axis?",
             "a": ["Never", "Once", "Twice", "It cannot be told without drawing it"],
             "c": 0,
             "why": "`D = 4 - 20 = -16 &lt; 0`, so `x² + 2x + 5 = 0` has no real "
                    "solution and the curve has no x-intercept. The discriminant "
                    "settles it before any drawing, which is the point of having it."},
        ],
        "mistakes": [
            ("Deciding the direction from c, or from the roots",
             "The constant term moves the curve up and down and the roots say where it "
             "crosses. Neither turns it over: `y = x² - 100` opens upward even though "
             "`c` is very negative."),
            ("Sampling x-values on one side of the axis",
             "Four points from one arm look like a bending line. Compute "
             "`h = -b/(2a)` first and take values either side of it &mdash; and the "
             "pairs you get should have equal heights, which is a free check on the "
             "arithmetic."),
            ("Calling a parabola with no x-intercept a broken graph",
             "`y = x² + 1` is a perfectly ordinary function with a value at every real "
             "`x`. It never takes the value `0`, and no rule requires a function to. "
             "An x-intercept is where the output is zero, not a feature every curve "
             "must have."),
        ],
        "standard": ("Finish when you can sketch without a table of values.",
                     "Given any quadratic you should produce the direction, the "
                     "y-intercept, the x-intercepts or a reason there are none, and "
                     "the axis &mdash; from the coefficients alone. Plotted points "
                     "should confirm the sketch, never be the way you discover it."),
        "note": "The lowest or highest point has been treated so far as \"the point "
                "on the axis\", computed by substituting `h` into `f`. Lesson 11 gives "
                "it a name and a form of the equation that displays it, and lesson 12 "
                "turns that into the tool for optimisation problems.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "vertex-form-and-the-axis-of-symmetry",
        "title": "Vertex Form and the Axis of Symmetry",
        "module": "Parabolas",
        "one_line": "Reading the vertex straight off the equation.",
        "summary": (
            "`y = a(x - h)² + k` is the same function as `y = ax² + bx + c`, written "
            "so that the vertex `(h, k)` and the axis `x = h` can be read without "
            "solving anything. Completing the square is the conversion, and in a "
            "function it is done by adding and subtracting rather than by adding to "
            "both sides."
        ),
        "key": [
            "y = a(x - h)² + k          vertex (h, k),   axis  x = h",
            "h = -b/(2a)                k = f(h) = c - b²/(4a)",
            "a > 0: k is the smallest value      a < 0: k is the largest",
            "2(x - 3)² - 5   is   2x² - 12x + 13        the same function",
        ],
        "key_label": "Vertex form, and where h and k come from",
        "concepts_intro": (
            "One rewriting, and the two things it makes visible that standard form "
            "hides."
        ),
        "concepts": [
            ("Vertex form is a rewriting, not a new function",
             "Expanding `a(x - h)² + k` returns `ax² + bx + c`. The two expressions "
             "agree at every `x`, so nothing has been gained or lost except "
             "readability &mdash; which is the only reason to do it."),
            ("h is subtracted, so watch the sign",
             "`(x + 3)²` is `(x - (-3))²`, so `h = -3` and the axis is `x = -3`. The "
             "form has a minus sign built in, and reading `+3` off the bracket puts "
             "the vertex on the wrong side of the y-axis."),
            ("A function has one side, so you add and subtract",
             "In an equation you may add 9 to both sides. A function definition is not "
             "an equation with two sides to balance: to complete the square in "
             "`f(x) = x² + 6x + 1` you add 9 and subtract 9 in the same expression, "
             "leaving its value unchanged at every `x`."),
        ],
        "read_title": "Vertex form",
        "read_intro": "What the form shows, why it shows it, and how to reach it.",
        "body": [
            ("def", ("Vertex",
                     "The <strong>vertex</strong> of a parabola is the point where it "
                     "meets its axis of symmetry: the lowest point when the curve "
                     "opens upward, the highest when it opens downward. A parabola has "
                     "exactly one.")),
            ("def", ("Vertex form",
                     "`y = a(x - h)² + k`, with `a ≠ 0`. The vertex is `(h, k)` and "
                     "the axis of symmetry is the line `x = h`. The coefficient `a` is "
                     "the same `a` as in standard form and does the same two jobs.")),
            ("thm", ("Vertex form displays the extreme value",
                     "For `f(x) = a(x - h)² + k`: if `a &gt; 0` then `f(x) ≥ k` for "
                     "every `x`, with equality only at `x = h`; if `a &lt; 0` then "
                     "`f(x) ≤ k` for every `x`, with equality only at `x = h`.")),
            ("proof", [
                "`x - h` is a real number, so `(x - h)² ≥ 0`, and `(x - h)² = 0` "
                "exactly when `x = h`. That is the whole content of the theorem; the "
                "rest is one multiplication.",
                "If `a &gt; 0`, multiplying `(x - h)² ≥ 0` by `a` preserves the "
                "inequality: `a(x - h)² ≥ 0`. Adding `k` to both sides gives "
                "`f(x) ≥ k`, with equality exactly when `(x - h)² = 0`.",
                "If `a &lt; 0`, multiplying by `a` reverses it &mdash; the one rule "
                "of course 2, lesson 9 &mdash; so `a(x - h)² ≤ 0` and `f(x) ≤ k`, "
                "again with equality exactly at `x = h`.",
            ]),
            ("p", "That proof is worth more than the form. It says the vertex is the "
                  "optimum without any appeal to a picture, and lesson 12 uses it on "
                  "problems where there is no picture to appeal to."),
            ("h3", "Converting by completing the square"),
            ("math", [
                "y = 2x² - 12x + 13",
                "  = 2(x² - 6x) + 13                 factor 2 out of the x terms ONLY",
                "  = 2(x² - 6x + 9 - 9) + 13         half of -6 is -3, squared is 9",
                "  = 2((x - 3)² - 9) + 13",
                "  = 2(x - 3)² - 18 + 13             the -9 leaves the bracket as -18",
                "  = 2(x - 3)² - 5",
                "",
                "vertex (3, -5)      axis x = 3      a = 2 > 0, so -5 is the minimum",
            ]),
            ("p", "The fifth line is where this goes wrong. The `-9` sits inside a "
                  "bracket that is multiplied by `2`, so bringing it out costs `-18`, "
                  "not `-9`. Every conversion with `a ≠ 1` has that step in it, and "
                  "the check is instant: `f(3) = 18 - 36 + 13 = -5`, which is `k`."),
            ("p", "Note what was <em>not</em> done. The constant `13` was left alone "
                  "until the end, and the `9` was added and subtracted in the same "
                  "line. Writing `y + 9 = 2(x² - 6x + 9) + 13` looks like balancing "
                  "but is not: the `9` inside the bracket carries the factor `2`, so "
                  "the right side rises by 18 while the left rises by 9, and the line "
                  "defines `y = 2x² - 12x + 22` &mdash; a different function. Adding "
                  "and subtracting inside the expression is what removes the need to "
                  "match two sides at all."),
            ("h3", "Where h and k come from"),
            ("math", [
                "a(x - h)² + k  =  ax² - 2ahx + (ah² + k)",
                "compare with      ax² +   bx +      c",
                "",
                "   b = -2ah         ⟹    h = -b/(2a)",
                "   c = ah² + k      ⟹    k = c - ah² = c - b²/(4a)",
                "",
                "and since k = f(h), computing f(h) directly is usually easier",
            ]),
            ("p", "So there are two routes. Completing the square shows the work and "
                  "is the one procedure the course asks you to own; `h = -b/(2a)` "
                  "followed by `k = f(h)` is quicker and involves fewer fractions. "
                  "They agree, because the second was derived from the first."),
            ("example", ("y = -2x² + 8x - 5",
                         "`-2(x² - 4x) - 5 = -2((x - 2)² - 4) - 5 = "
                         "-2(x - 2)² + 8 - 5 = -2(x - 2)² + 3`. The vertex is `(2, 3)` "
                         "and `a = -2 &lt; 0`, so `3` is the largest value the "
                         "function takes. Check: `f(2) = -8 + 16 - 5 = 3`.")),
            ("example", ("y = x² - 3x + 1",
                         "`h = -b/(2a) = 3/2` and `k = f(3/2) = 9/4 - 9/2 + 1 = -5/4`, "
                         "so `y = (x - 3/2)² - 5/4`. Halving an odd `b` produces "
                         "halves and quarters; keep them. Multiplying through by 4 to "
                         "clear them would define a different function, four times as "
                         "tall.")),
            ("p", "Vertex form is also the transformation form of course 3, lesson 11. "
                  "`y = a(x - h)² + k` is the parabola `y = x²` stretched by a factor "
                  "`a`, shifted `h` to the right and `k` up &mdash; which is why every "
                  "parabola really is the same curve, seen at a different size and in "
                  "a different place."),
        ],
        "lab": ("quadratic", {
            "mode": "vertex",
            "panel_title": "Completing the square, line by line",
            "panel_intro": "Every step of the conversion is printed for the "
                           "coefficients you enter, ending in `a(x - h)² + k`. Compare "
                           "the `h` in that line with `-b/(2a)` in the panel beside it: "
                           "they are computed separately and they agree.",
        }),
        "steps_title": "Converting ax² + bx + c to vertex form",
        "steps_intro": "Four steps. The third is the one that is skipped, and it is the one with a in it.",
        "steps": [
            ("Factor a out of the x² and x terms only",
             "`2x² - 12x + 13` becomes `2(x² - 6x) + 13`. The constant stays outside "
             "the bracket, untouched."),
            ("Halve the coefficient of x inside, and square it",
             "Inside the bracket the coefficient is `-6`; half of it is `-3` and the "
             "square is `9`. That `9` is the number that completes the square, and it "
             "is the only number that does."),
            ("Add and subtract it inside, then take the subtraction out",
             "`2(x² - 6x + 9 - 9)` is `2((x - 3)² - 9)` is `2(x - 3)² - 18`. The `-9` "
             "is multiplied by `a` on the way out. Forgetting that multiplication is "
             "the standard error and it moves `k` by `a` times the square."),
            ("Read (h, k) and check with f(h)",
             "The bracket `(x - 3)` gives `h = 3`; the constant left over gives `k`. "
             "Substituting `h` back into the original is a two-line check that catches "
             "everything above."),
        ],
        "worked": {
            "title": "y = x² + 5x + 1 in vertex form",
            "intro": [
                "`a = 1`, so nothing has to be factored out and the arithmetic is "
                "purely in quarters."
            ],
            "lines": [
                "y = x² + 5x + 1",
                "",
                "  half of 5 is 5/2,   and   (5/2)² = 25/4",
                "",
                "  = (x² + 5x + 25/4 - 25/4) + 1        add and subtract 25/4",
                "  = (x + 5/2)² - 25/4 + 1",
                "  = (x + 5/2)² - 21/4                  since -25/4 + 4/4 = -21/4",
                "",
                "vertex   (-5/2, -21/4)          axis   x = -5/2",
                "",
                "check    h = -b/(2a) = -5/2                              ✓",
                "         k = f(-5/2) = 25/4 - 25/2 + 1 = -21/4           ✓",
            ],
            "after": [
                "The bracket reads `(x + 5/2)`, so `h = -5/2` and not `5/2`. Vertex "
                "form subtracts `h`, and a plus sign inside the bracket always means a "
                "negative `h`.",
                "Both halves of the check were computed from the original coefficients "
                "rather than from the vertex form, which is what makes the agreement "
                "worth something. `a = 1 &gt; 0`, so `-21/4` is the smallest value "
                "this function takes, and it takes it once.",
            ],
        },
        "quiz_title": "Vertex form",
        "quiz": [
            {"q": "What is the vertex of `y = (x + 4)² - 7`?",
             "a": ["`(4, -7)`", "`(-4, -7)`", "`(-4, 7)`", "`(4, 7)`"],
             "c": 1,
             "why": "The form is `a(x - h)² + k`, and `x + 4` is `x - (-4)`, so "
                    "`h = -4` while `k = -7` is read off directly. Choices that keep "
                    "`+4` mis-read the built-in minus sign; choices that flip `k` "
                    "negate a constant that needed no work at all."},
            {"q": "`y = -2(x - 5)² + 3` has:",
             "a": ["a minimum value of `3`, at `x = 5`",
                   "a maximum value of `3`, at `x = 5`",
                   "a maximum value of `5`, at `x = 3`",
                   "a minimum value of `-2`"],
             "c": 1,
             "why": "`a = -2 &lt; 0`, so the parabola opens downward and `k = 3` is "
                    "the largest value, reached at `x = h = 5`. Swapping `h` and `k` "
                    "gives the third choice; `-2` is the stretch factor and is not a "
                    "value of the function anywhere in particular."},
            {"q": "Written in vertex form, `y = x² + 5x + 1` is:",
             "a": ["`(x + 5/2)² - 21/4`", "`(x + 5/2)² + 21/4`",
                   "`(x + 5/2)² - 25/4`", "`(x + 5)² - 24`"],
             "c": 0,
             "why": "Half of `5` is `5/2` and `(5/2)² = 25/4`; that `25/4` must come "
                    "back out, and `1 - 25/4 = -21/4`. The third choice forgets the "
                    "`+1`, the fourth squares `5` instead of half of `5`, and the "
                    "second loses a sign that the check `f(-5/2) = -21/4` would have "
                    "caught."},
        ],
        "mistakes": [
            ("Bringing the subtracted square out without multiplying by a",
             "In `2(x² - 6x + 9 - 9) + 13` the `-9` is inside a bracket carrying a "
             "factor of `2`, so it emerges as `-18`. Writing `2(x - 3)² - 9 + 13` puts "
             "the vertex 9 units too high, and `f(3)` disagrees at once."),
            ("Reading h with the wrong sign",
             "`(x + 3)²` has its vertex at `x = -3`. The subtraction is part of the "
             "form, so a plus inside the bracket means a negative `h` &mdash; the same "
             "reversal that catches everyone in the transformations of course 3."),
            ("Adjusting one side of a function definition only",
             "`y + 9 = x² + 6x + 10` is still `y = x² + 6x + 1`, since subtracting 9 "
             "from both sides returns it, and `4y = 4x² + 24x + 4` divides back to it "
             "as well. The error is changing one side alone: `y = x² + 6x + 10` adds "
             "the completing-square constant to the right only, and "
             "`y = 4x² + 24x + 4` scales the right only, defining a function four "
             "times as tall. Inside a function definition the only legal move is "
             "one that leaves the value unchanged at every `x`, which is why "
             "completing the square there is add-and-subtract."),
        ],
        "standard": ("Finish when you can convert with a ≠ 1 and check it in two lines.",
                     "Take `y = 3x² + 12x + 5`, produce vertex form, and verify with "
                     "`h = -b/(2a)` and `k = f(h)` computed from the original "
                     "coefficients. If the two disagree, the factor `a` on the way out "
                     "of the bracket is the first place to look."),
        "note": "This is the same completing the square that derived the quadratic "
                "formula in lesson 5. One procedure, two payoffs: run it on "
                "`ax² + bx + c = 0` and it gives the formula, run it on "
                "`y = ax² + bx + c` and it gives the vertex. Lesson 12 spends that "
                "second payoff.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "maximum-and-minimum-problems",
        "title": "Maximum and Minimum Problems",
        "module": "Parabolas",
        "one_line": "Optimisation without calculus, using the vertex.",
        "summary": (
            "A quantity that depends quadratically on one variable is largest or "
            "smallest at the vertex, and the vertex is `x = -b/(2a)`. The algebra is "
            "three lines; the work is building the quadratic from the situation and "
            "respecting the values the variable is actually allowed to take."
        ),
        "key": [
            "a > 0   minimum at x = -b/(2a)        a < 0   maximum there",
            "the optimal VALUE is f(-b/(2a)),  not -b/(2a) itself",
            "restricted domain: check the endpoints as well as the vertex",
            "an upward parabola has no maximum at all on the whole line",
        ],
        "key_label": "Where the optimum is, and what it is",
        "concepts_intro": (
            "One turning point, so there is nothing to compare &mdash; provided the "
            "variable is free to take any value."
        ),
        "concepts": [
            ("A quadratic turns once, so the vertex is the answer",
             "There is no second candidate to check and no interior comparison to "
             "make. That is why this is the one optimisation problem school algebra "
             "can settle exactly, and why calculus is not needed for it."),
            ("Two different numbers are being asked for",
             "`x = -b/(2a)` says <em>where</em>; `f(-b/(2a))` says <em>how much</em>. "
             "\"How many should be sold\" and \"what is the greatest profit\" have "
             "different answers, and each is wrong in the other's place."),
            ("The situation restricts the variable",
             "A length is positive, a number of tickets is a whole number, a time "
             "after launch is not negative. If the vertex is outside the allowed set, "
             "it is not available, and the optimum sits at an endpoint instead."),
        ],
        "read_title": "Optimising with the vertex",
        "read_intro": "The theorem, the modelling, and the cases where the vertex is not the answer.",
        "body": [
            ("p", "Every problem in this lesson has the same shape: a quantity is "
                  "expressed as a quadratic in one variable, and the largest or "
                  "smallest value of that quadratic is wanted. Lesson 11 already "
                  "supplies the answer; what remains is getting to the quadratic and "
                  "reading the question correctly."),
            ("thm", ("The vertex is the only optimum",
                     "Let `f(x) = ax² + bx + c` with `a ≠ 0` and `h = -b/(2a)`. If "
                     "`a &gt; 0` then `f(x) &gt; f(h)` for every `x ≠ h`, so `f(h)` is "
                     "the smallest value `f` takes and there is no largest. If "
                     "`a &lt; 0` then `f(x) &lt; f(h)` for every `x ≠ h`, so `f(h)` is "
                     "the largest and there is no smallest.")),
            ("proof", [
                "Lesson 10 proved `f(h + t) = f(h) + at²` for every real `t`. Every "
                "real number `x` is `h + t` for exactly one `t`, namely `t = x - h`, "
                "so this covers all of them.",
                "`t² &gt; 0` whenever `t ≠ 0`. If `a &gt; 0` then `at² &gt; 0` and "
                "`f(x) &gt; f(h)`; if `a &lt; 0` then `at² &lt; 0` and "
                "`f(x) &lt; f(h)`. Either way the comparison is strict away from `h`, "
                "so the optimum is attained at `x = h` and nowhere else.",
                "For the other direction: with `a &gt; 0`, `f(h) + at²` grows without "
                "bound as `|t|` grows, so no number is an upper bound for `f` and "
                "there is no maximum.",
            ]),
            ("h3", "Building the quadratic"),
            ("ol", [
                "Name one variable, with its unit: \"let `x` be the width in metres\". "
                "One, not two &mdash; a second unknown has to be eliminated before "
                "anything else happens.",
                "Use the constraint to write every other quantity in terms of `x`. A "
                "perimeter of 80 makes the adjacent side `40 - x`, not a second "
                "letter.",
                "Write the quantity to be optimised as a function of `x`, and expand "
                "it into `ax² + bx + c` so that `a` and `b` are visible.",
                "State the values of `x` the situation permits, before computing "
                "anything.",
            ]),
            ("example", ("A rectangle of perimeter 80",
                         "Let `x` be one side in metres. The perimeter fixes the "
                         "adjacent side: `2x + 2y = 80` gives `y = 40 - x`. The area "
                         "is `A(x) = x(40 - x) = -x² + 40x`, so `a = -1` and `b = 40`.",
                         "`a &lt; 0`, so the vertex is a maximum, at "
                         "`x = -40/(2·(-1)) = 20`. Then `A(20) = 20 · 20 = 400`. The "
                         "permitted values are `0 &lt; x &lt; 40`, and `20` is among "
                         "them, so the greatest area is 400 square metres, from a "
                         "20 by 20 square.")),
            ("p", "The optimal rectangle came out square. That is not proved by this "
                  "example &mdash; one perimeter was tested, not all of them. Running "
                  "the same three lines with a perimeter `P` gives "
                  "`A(x) = x(P/2 - x)`, vertex at `x = P/4`, and the other side "
                  "`P/2 - P/4 = P/4` as well; doing it once with a letter is what "
                  "settles the general claim."),
            ("example", ("A projectile",
                         "A ball thrown upward has height "
                         "`h(t) = -5t² + 20t + 1` metres after `t` seconds. `a = -5`, "
                         "so the vertex is a maximum, at `t = -20/(2·(-5)) = 2` "
                         "seconds, and the greatest height is "
                         "`h(2) = -20 + 40 + 1 = 21` metres.",
                         "\"When does it land\" is a different question and needs the "
                         "formula, not the vertex: `-5t² + 20t + 1 = 0` gives "
                         "`t = 2 ± √105/5`, and only the positive root `2 + √105/5` "
                         "&mdash; about 4.05 seconds &mdash; is in the domain "
                         "`t ≥ 0`.")),
            ("h3", "When the vertex is not available"),
            ("p", "Suppose profit is `P(x) = -3x² + 30x - 12` in pounds from `x` "
                  "machines, and only 4 machines exist. The vertex is at `x = 5`, "
                  "outside the permitted `0 ≤ x ≤ 4`. By the identity "
                  "`P(h + t) = P(h) + at²` the function rises steadily as `x` climbs "
                  "towards 5, so on `0 ≤ x ≤ 4` the best allowed value is the "
                  "endpoint: `P(4) = -48 + 120 - 12 = 60`. The unreachable `P(5) = 63` "
                  "is not an answer to the question that was asked."),
            ("p", "Whole-number constraints work the same way. If `x` must be an "
                  "integer and the vertex sits at `x = 5/2`, compare the two integers "
                  "either side. For `f(x) = -x² + 5x` those are `f(2) = 6` and "
                  "`f(3) = 6`, equal &mdash; which the symmetry predicts, since 2 and "
                  "3 are the same distance from the axis `x = 5/2`. A vertex at "
                  "`x = 5/2` is not itself an answer when only whole numbers are "
                  "allowed."),
            ("p", "Finish by answering in a sentence with units. \"`x = 20`\" is not "
                  "an answer to \"what are the dimensions of the largest rectangle\"; "
                  "\"20 m by 20 m, with area 400 m²\" is."),
        ],
        "lab": ("quadratic", {
            "mode": "optimise",
            "panel_title": "The vertex is the optimum",
            "panel_intro": "Each preset is a model: an area, a profit, a height. The "
                           "vertex is marked on the curve and printed beside it, and "
                           "both come from the same `-b/(2a)`. Change `b` and watch "
                           "the optimum move sideways while its value changes too.",
        }),
        "steps_title": "Solving a maximum or minimum problem",
        "steps_intro": "The last step is where marks are lost, and it is not the algebra.",
        "steps": [
            ("Name one variable and eliminate the others",
             "Give it a letter and a unit. Use the constraint in the problem to write "
             "everything else in terms of it &mdash; that is what the constraint is "
             "for."),
            ("Write the quantity as a quadratic and read a and b",
             "Expand to `ax² + bx + c`. The sign of `a` tells you at once whether the "
             "vertex is a maximum or a minimum, so check it before computing "
             "anything."),
            ("State the permitted values of the variable",
             "Lengths are positive, counts are whole numbers, times are not negative. "
             "Write the interval down; it is part of the model, not an afterthought."),
            ("Take x = -b/(2a), test it against the domain, then answer the question",
             "If the vertex is permitted, it is the answer; if not, the optimum is at "
             "the nearer endpoint. Then decide whether the question wants the location "
             "or the value, and give it with units."),
        ],
        "worked": {
            "title": "Two numbers with sum 12 and the largest possible product",
            "intro": [
                "The constraint is used first, to get from two unknowns down to one. "
                "Nothing can be optimised while there are still two."
            ],
            "lines": [
                "the numbers are   x   and   12 - x",
                "",
                "P(x) = x(12 - x) = -x² + 12x            a = -1,  b = 12,  c = 0",
                "",
                "a = -1 < 0     the parabola opens downward, so the vertex is a MAXIMUM",
                "",
                "        -b         -12",
                "x  =  ------  =  --------  =  6",
                "        2a        2·(-1)",
                "",
                "P(6) = 6 · 6 = 36",
                "",
                "symmetry check     P(5) = 5 · 7 = 35",
                "                   P(7) = 7 · 5 = 35        equal, as they must be",
                "",
                "answer:  the numbers are 6 and 6, and the largest product is 36",
            ],
            "after": [
                "Both numbers were asked for, so `x = 6` on its own does not answer "
                "the question. Half of the work in these problems is noticing which of "
                "`h` and `f(h)` is wanted, and here it is neither: it is `x` and "
                "`12 - x` together.",
                "`P(5)` and `P(7)` agreeing is not luck. 5 and 7 are equidistant from "
                "the axis `x = 6`, so the symmetry of lesson 10 forces equal values "
                "&mdash; which makes it a cheap check on `h`. If those two came out "
                "different, `h` would be wrong.",
            ],
        },
        "quiz_title": "Optimising",
        "quiz": [
            {"q": "`P(x) = -3x² + 30x - 12` is a profit in pounds. At which `x` is the "
                  "profit greatest?",
             "a": ["`x = 5`", "`x = 63`", "`x = 10`", "`x = -5`"],
             "c": 0,
             "why": "`x = -b/(2a) = -30/(2·(-3)) = 5`. `63` is `P(5)`, the profit "
                    "itself and the answer to a different question; `10` is `-b/a`, "
                    "the sum of the roots rather than their midpoint; `-5` drops a "
                    "minus sign that the denominator already carries."},
            {"q": "`h(t) = -16t² + 64t + 5` gives height in feet after `t` seconds. "
                  "What is the greatest height reached?",
             "a": ["69 feet", "2 feet", "5 feet", "64 feet"],
             "c": 0,
             "why": "The vertex is at `t = -64/(2·(-16)) = 2`, and the height there is "
                    "`h(2) = -64 + 128 + 5 = 69`. `2` is when, not how high; `5` is "
                    "the height at launch; `64` is a coefficient, not a height."},
            {"q": "A quadratic model with `a &lt; 0` has its vertex at `x = 7`, but "
                  "the situation only permits `0 ≤ x ≤ 5`. Where is the maximum on "
                  "that interval?",
             "a": ["At `x = 7`", "At `x = 5`", "At `x = 0`",
                   "There is no maximum on that interval"],
             "c": 1,
             "why": "The function climbs all the way up to `x = 7`, so on "
                    "`0 ≤ x ≤ 5` it is still climbing at the right-hand end and the "
                    "largest permitted `x` gives the largest value. The vertex is "
                    "outside the domain, so it is not an answer that is available to "
                    "be given."},
        ],
        "mistakes": [
            ("Reporting the location when the value was wanted",
             "`-b/(2a)` is an `x`. The maximum profit, the greatest height and the "
             "largest area are all `f(-b/(2a))`. Read the question twice and write "
             "the answer as a sentence with units, which makes the confusion visible."),
            ("Ignoring the domain the situation imposes",
             "Vertices land at negative lengths, at fractional numbers of tickets and "
             "outside the interval the problem allows. When that happens the vertex is "
             "not the answer, and the endpoints or the neighbouring integers are."),
            ("Assuming the vertex is always a maximum",
             "With `a &gt; 0` it is a minimum, and the function has no maximum at all "
             "on the whole line &mdash; it grows without bound in both directions. "
             "\"Find the maximum of `x² - 4x + 7`\" has no answer unless a domain is "
             "supplied."),
        ],
        "standard": ("Finish when the model, not the algebra, is what takes the time.",
                     "Given a described situation you should produce the variable, the "
                     "constraint, the quadratic and the permitted values before "
                     "computing `-b/(2a)`. The vertex takes one line; if the setup "
                     "took no longer than the vertex did, something in the problem "
                     "was assumed rather than read."),
        "note": "Everything here rests on the identity `f(h + t) = f(h) + at²` from "
                "lesson 10, which is the whole reason a quadratic has exactly one "
                "turning point. Lesson 13 uses the same picture for a different "
                "question: not where the curve is highest, but where it is above or "
                "below zero.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "quadratic-inequalities",
        "title": "Quadratic Inequalities",
        "module": "Parabolas",
        "one_line": "Sign analysis, and reading the answer off the graph.",
        "summary": (
            "To solve `ax² + bx + c &gt; 0`, first solve `ax² + bx + c = 0`. The roots "
            "are the only places the sign can change, so testing one value in each "
            "interval they cut settles the whole line. The answer is a set, and the "
            "endpoints belong to it only when the inequality is not strict."
        ),
        "key": [
            "get 0 on one side first:   ax² + bx + c > 0",
            "solve = 0 for the roots, then test one value per interval",
            "a > 0 with roots r < s:  positive outside [r, s],  negative between",
            "strict > and <  exclude the roots;   ≥ and ≤  include them",
        ],
        "key_label": "The method in four lines",
        "concepts_intro": (
            "An inequality asks about a sign, and signs are exactly what a factored "
            "quadratic reports."
        ),
        "concepts": [
            ("The sign can only change at a root",
             "Between consecutive roots the expression keeps one sign, so a single "
             "test value speaks for a whole interval. That is what makes the method "
             "finite rather than a search."),
            ("Never divide by an expression containing the variable",
             "Dividing `x² &gt; 3x` by `x` assumes `x` is positive &mdash; and if `x` "
             "is negative the inequality reverses, while `x = 0` is deleted "
             "altogether. Move everything to one side and factor instead."),
            ("The answer is a set",
             "It is one interval, two intervals, all of the real line, or nothing at "
             "all. Deciding which endpoints belong is a separate question from finding "
             "them, and it is settled by whether the sign is strict."),
        ],
        "read_title": "Solving a quadratic inequality",
        "read_intro": "Roots first, signs second, endpoints last.",
        "body": [
            ("def", ("Quadratic inequality",
                     "An inequality that can be written `ax² + bx + c &gt; 0` with "
                     "`a ≠ 0`, or with `&lt;`, `≥` or `≤` in place of `&gt;`. A "
                     "solution is any real number that makes the statement true, and "
                     "solving means describing all of them.")),
            ("p", "Getting `0` on one side is not cosmetic. \"Greater than zero\" is a "
                  "question about a sign, and a factored expression reports signs one "
                  "factor at a time. \"Greater than 5\" reports nothing the factors "
                  "can answer: knowing that `x - 1` and `x + 4` are both positive "
                  "does not settle whether their product is above 5 or below it. "
                  "Rewrite `(x - 1)(x + 4) &gt; 5` as `x² + 3x - 9 &gt; 0` first, and "
                  "the factors of that expression do answer the question."),
            ("thm", ("Sign changes happen only at roots",
                     "Suppose `ax² + bx + c` has real roots `r ≤ s`, so that it equals "
                     "`a(x - r)(x - s)`. On each of `x &lt; r`, `r &lt; x &lt; s` and "
                     "`x &gt; s` the expression keeps a single sign, so one test value "
                     "chosen from an interval determines the sign on all of it.")),
            ("p", "The reason is the factored form. `(x - r)` is negative to the left "
                  "of `r` and positive to the right, and likewise for `(x - s)`; "
                  "neither factor changes sign anywhere else. A product changes sign "
                  "only when one of its factors does, so the only candidates are `r` "
                  "and `s`."),
            ("h3", "Method 1: a sign table"),
            ("math", [
                "                 x < -2     x = -2     -2 < x < 3     x = 3     x > 3",
                "  x + 2             -          0            +           +         +",
                "  x - 3             -          -            -           0         +",
                "  ------------------------------------------------------------------",
                "  (x + 2)(x - 3)    +          0            -           0         +",
                "",
                "  so  (x + 2)(x - 3) ≤ 0  on  -2 ≤ x ≤ 3,   which is  [-2, 3]",
                "  and (x + 2)(x - 3) > 0  on  x < -2  or  x > 3",
            ]),
            ("h3", "Method 2: read it off the parabola"),
            ("p", "The graph says the same thing in one picture. `y &gt; 0` is where "
                  "the curve is above the x-axis. An upward parabola with two roots "
                  "dips below the axis exactly between them, so `&gt; 0` gives the two "
                  "outer intervals and `&lt; 0` gives the middle one. A downward "
                  "parabola swaps those two answers, which is why the sign of `a` has "
                  "to be checked before anything is written down."),
            ("example", ("2x² + 5x > 3",
                         "Move everything to one side: `2x² + 5x - 3 &gt; 0`. Factor: "
                         "`(2x - 1)(x + 3) &gt; 0`, so the roots are `1/2` and `-3`. "
                         "`a = 2 &gt; 0`, so the expression is positive outside the "
                         "roots: `x &lt; -3` or `x &gt; 1/2`.",
                         "Test `x = 0`, which lies between the roots: "
                         "`2(0)² + 5(0) - 3 = -3`, and `-3 &gt; 0` is false. The "
                         "middle interval is correctly excluded.")),
            ("example", ("x² - 4x + 1 < 0",
                         "This does not factor over the integers, and it does not need "
                         "to. `D = 16 - 4 = 12`, so the roots are "
                         "`(4 ± √12)/2 = 2 ± √3`. `a = 1 &gt; 0`, so the expression is "
                         "negative between them: `2 - √3 &lt; x &lt; 2 + √3`.",
                         "Check with the easiest interior value, `x = 2`: "
                         "`4 - 8 + 1 = -3`, which is indeed negative. The roots are "
                         "all the method ever wanted; how they were found is not part "
                         "of the method.")),
            ("h3", "When there are fewer than two roots"),
            ("ul", [
                "<strong>`D &lt; 0`.</strong> The expression never reaches `0`, so it "
                "keeps one sign everywhere &mdash; the sign of `a`. `x² + x + 1 &gt; 0` "
                "is true for every real `x`; `x² + x + 1 &lt; 0` has no solutions at "
                "all. Both answers are complete answers.",
                "<strong>`D = 0`.</strong> There is one root and the curve touches the "
                "axis without crossing, so the sign is the same on both sides. "
                "`(x - 3)² &gt; 0` holds for every `x` except `3`; `(x - 3)² ≥ 0` "
                "holds for every `x`; `(x - 3)² ≤ 0` holds only at `x = 3`; "
                "`(x - 3)² &lt; 0` never holds.",
                "<strong>Endpoints.</strong> The roots make the expression `0`. With "
                "`≥` or `≤` they belong to the solution set, and with `&gt;` or "
                "`&lt;` they do not. Nothing else about the answer changes.",
            ]),
            ("p", "The one manipulation to refuse is division by an expression in `x`. "
                  "To solve `x² &gt; 3x`, do not cancel an `x`: that would assume "
                  "`x &gt; 0`, and it would lose `x = 0` besides. Instead "
                  "`x² - 3x &gt; 0`, so `x(x - 3) &gt; 0`, giving `x &lt; 0` or "
                  "`x &gt; 3`. Cancelling would have returned `x &gt; 3` alone, and "
                  "`x = -1` &mdash; where `1 &gt; -3` is true &mdash; shows what that "
                  "answer is missing."),
        ],
        "lab": ("inequality", {
            "mode": "quadratic",
            "panel_title": "Sign, interval by interval",
            "panel_intro": "Set the quadratic and the direction of the sign, then read "
                           "the solution set on the number line beneath the curve. "
                           "Switch between `&gt;` and `≥` and watch the endpoints join "
                           "or leave the set while the intervals themselves stay "
                           "exactly where they were.",
        }),
        "steps_title": "Solving ax² + bx + c > 0",
        "steps_intro": "Four steps. The first one is the one that gets skipped when the inequality already looks tidy.",
        "steps": [
            ("Move everything to one side",
             "The comparison must be with `0`. Do it by adding and subtracting only "
             "&mdash; never by dividing by something containing `x`, whose sign you do "
             "not know."),
            ("Solve the corresponding equation",
             "Factor it, or use the formula, or note that `D &lt; 0` and there are no "
             "roots at all. These roots are the only places the sign can change."),
            ("Test one value in each interval",
             "Mark the roots on a line and pick a convenient number from each piece "
             "&mdash; `0` whenever it is available. The sign of the expression there "
             "is its sign on the whole piece."),
            ("Write the set, then settle the endpoints",
             "Use interval notation from course 2, lesson 13. A square bracket for a "
             "root that satisfies the inequality, a round one for a root that does "
             "not, and \"or\" between two separate intervals."),
        ],
        "worked": {
            "title": "x² - x - 6 ≤ 0",
            "intro": [
                "Zero is already on the right. The roots come first and the inequality "
                "sign is dealt with last, which keeps the two decisions apart."
            ],
            "lines": [
                "x² - x - 6  =  (x - 3)(x + 2)          roots  x = 3  and  x = -2",
                "",
                "three intervals, one test value in each:",
                "",
                "   x = -3     (-6)(-1) =   6  > 0      NOT in the solution set",
                "   x =  0     (-3)( 2) =  -6  < 0      in the solution set",
                "   x =  4     ( 1)( 6) =   6  > 0      NOT in the solution set",
                "",
                "so the expression is negative exactly on   -2 < x < 3",
                "",
                "endpoints:  the inequality is ≤ , and both roots give 0,",
                "            and 0 ≤ 0 is true, so both are included",
                "",
                "solution set:    -2 ≤ x ≤ 3     which is     [-2, 3]",
            ],
            "after": [
                "The three test values are the evidence, not decoration: they are what "
                "establishes the sign on each interval. One value per interval is "
                "enough because the expression cannot change sign without passing "
                "through a root, and both roots are already accounted for.",
                "Had the inequality been `&lt; 0` rather than `≤ 0`, the same three "
                "lines of work would give `(-2, 3)`. The roots are found once; the "
                "brackets are chosen afterwards.",
            ],
        },
        "quiz_title": "Solving inequalities",
        "quiz": [
            {"q": "Solve `(x - 1)(x + 4) &lt; 0`.",
             "a": ["`-4 &lt; x &lt; 1`", "`x &lt; -4` or `x &gt; 1`",
                   "`-1 &lt; x &lt; 4`", "`-4 ≤ x ≤ 1`"],
             "c": 0,
             "why": "The parabola opens upward, so the product is negative between the "
                    "roots `-4` and `1`. The second choice is where it is positive; "
                    "the third reads the roots off with the wrong signs; the fourth "
                    "includes the endpoints, where the product is `0`, and `0 &lt; 0` "
                    "is false."},
            {"q": "What is the solution set of `x² + 4 &gt; 0`?",
             "a": ["There are no solutions", "`x &gt; 2` or `x &lt; -2`",
                   "All real numbers", "`x &gt; -2`"],
             "c": 2,
             "why": "`D = -16 &lt; 0` and `a &gt; 0`, so the expression is never zero "
                    "and never negative &mdash; its smallest value is `4`, at `x = 0`. "
                    "The second choice solves `x² - 4 &gt; 0`, which is a different "
                    "inequality."},
            {"q": "Solve `x² ≥ 9`.",
             "a": ["`x ≥ 3`", "`-3 ≤ x ≤ 3`", "`x ≤ -3` or `x ≥ 3`", "`x ≥ ±3`"],
             "c": 2,
             "why": "`x² - 9 = (x - 3)(x + 3) ≥ 0` outside the roots. Taking a square "
                    "root of both sides and writing `x ≥ 3` loses the whole negative "
                    "branch, `-3 ≤ x ≤ 3` solves `x² ≤ 9`, and `x ≥ ±3` does not "
                    "describe a set of numbers at all."},
        ],
        "mistakes": [
            ("Dividing both sides by x, or by a bracket",
             "The sign of the divisor is unknown, so you cannot know whether to "
             "reverse the inequality, and if the divisor can be `0` you have deleted a "
             "value as well. `x² &gt; 3x` gives `x &lt; 0` or `x &gt; 3`; cancelling "
             "the `x` returns half of that."),
            ("Writing a two-interval answer as one chain",
             "`3 &lt; x &lt; -2` says `x` is above 3 and below -2 at the same time, "
             "which nothing is: the chain notation always means an intersection. Two "
             "separate intervals need the word \"or\"."),
            ("Assuming the sign alternates across every root",
             "It alternates at a simple root and does not at a repeated one. "
             "`(x - 2)²` is positive on both sides of `2`, so `(x - 2)² &gt; 0` has "
             "solution \"every `x` except `2`\" &mdash; a set with a hole in it, which "
             "no amount of alternating would produce."),
        ],
        "standard": ("Finish when the answer is a set and you can say why each endpoint is in or out.",
                     "Solve `2x² - 5x - 3 ≥ 0` and write the result in interval "
                     "notation, then say what changes if the `≥` becomes `&gt;`. If "
                     "the endpoint decision needs re-solving rather than one look at "
                     "the sign, the two halves of the method have run together."),
        "note": "Sign analysis is the same tool course 5 used on rational expressions, "
                "with one addition there: the sign can also change where a denominator "
                "is zero, and that value is excluded rather than included. Here the "
                "expression is defined everywhere, so the roots are the only critical "
                "values.",
    },
    # ---------------------------------------------------------------- 14
    {
        "slug": "equations-reducible-to-quadratic-form",
        "title": "Equations Reducible to Quadratic Form",
        "module": "Parabolas",
        "one_line": "Substitution that turns a quartic into a quadratic.",
        "summary": (
            "If an equation can be written `au² + bu + c = 0` for some expression "
            "`u = f(x)`, the quadratic methods apply to it. Solving for `u` is only "
            "half the work: every value of `u` must be sent back through `f` to "
            "produce the values of `x`, and some of them produce none."
        ),
        "key": [
            "a[f(x)]² + b[f(x)] + c = 0        put  u = f(x)",
            "x⁴ - 5x² + 4 = 0         u = x²        4 is twice 2",
            "x - 5√x + 6 = 0          u = √x        1 is twice 1/2",
            "solve for u, then substitute BACK and solve for x",
        ],
        "key_label": "One substitution, then the usual quadratic",
        "concepts_intro": (
            "The pattern to look for, the renaming that exploits it, and the step "
            "everyone forgets."
        ),
        "concepts": [
            ("Look for one exponent that is twice another",
             "`x⁴` and `x²`, `x` and `√x`, `x⁻²` and `x⁻¹`, `x⁶` and `x³`. With a "
             "constant term as well, the equation is a quadratic in the smaller "
             "power, whatever that power happens to be."),
            ("u is a temporary name, not the answer",
             "The substitution renames part of the equation so that a known method "
             "applies. The question was about `x`, so the last step is always the "
             "return journey, and an answer left in terms of `u` is half an answer."),
            ("Some values of u give no real x",
             "If `u = x²` then `u` cannot be negative, and if `u = √x` then `u` cannot "
             "be negative either. A negative solution for `u` is discarded, so two "
             "values of `u` need not give four values of `x`."),
        ],
        "read_title": "Substitution into quadratic form",
        "read_intro": "The shape, the substitution, and the return journey.",
        "body": [
            ("p", "A quartic has no formula in this course, and course 4's rational "
                  "root search is a general tool that can miss irrational roots "
                  "entirely. But a quartic with no odd powers is not really a quartic: "
                  "it is a quadratic wearing `x²` where a quadratic wears `x`, and "
                  "renaming that part is enough to finish it exactly."),
            ("def", ("Quadratic form",
                     "An equation is in <strong>quadratic form</strong> if it can be "
                     "written `au² + bu + c = 0` with `a ≠ 0`, where `u = f(x)` is "
                     "some expression in `x`. The test is that one power appearing in "
                     "the equation is exactly twice another, with nothing else present "
                     "but a constant.")),
            ("math", [
                "x⁴ - 5x² + 4 = 0",
                "                              put  u = x²,  so  x⁴ = (x²)² = u²",
                "u² - 5u + 4 = 0",
                "(u - 1)(u - 4) = 0",
                "u = 1     or     u = 4",
                "                              now back to x",
                "x² = 1  →  x = ±1            x² = 4  →  x = ±2",
                "",
                "four solutions:   x = -2, -1, 1, 2",
            ]),
            ("p", "The substitution is legal because it is a renaming in both "
                  "directions. Every `x` satisfying the original gives a `u = x²` "
                  "satisfying the quadratic, and every `u` satisfying the quadratic "
                  "gives back exactly the `x` with `x² = u` &mdash; two of them, one, "
                  "or none, depending on the sign of `u`. Nothing has been done to the "
                  "equation; part of it has been given a shorter name."),
            ("h3", "Values of u that give no real x"),
            ("example", ("x⁴ - 3x² - 4 = 0",
                         "With `u = x²`: `u² - 3u - 4 = (u - 4)(u + 1) = 0`, so "
                         "`u = 4` or `u = -1`. Back-substituting, `x² = 4` gives "
                         "`x = ±2`, while `x² = -1` has no real solution, since a "
                         "square of a real number is never negative.",
                         "So this quartic has two real solutions, not four. The count "
                         "of `u` values and the count of `x` values are different "
                         "numbers, and only the second answers the question.")),
            ("p", "Over the complex numbers of lessons 7 to 9 the story is different: "
                  "`x² = -1` gives `x = ±i`, so the same quartic has four complex "
                  "solutions, `2`, `-2`, `i` and `-i`. Which answer is wanted depends "
                  "on which number system the question is asked in, and that is worth "
                  "stating in the answer."),
            ("h3", "Radicals and negative exponents"),
            ("example", ("x - 5√x + 6 = 0",
                         "Put `u = √x`, so `u² = x` and the equation is "
                         "`u² - 5u + 6 = 0`, giving `u = 2` or `u = 3`. Then "
                         "`√x = 2` gives `x = 4`, and `√x = 3` gives `x = 9`. Both "
                         "check: `4 - 10 + 6 = 0` and `9 - 15 + 6 = 0`.",
                         "The domain is `x ≥ 0` throughout, since `√x` is defined "
                         "nowhere else, and both answers respect it.")),
            ("p", "The restriction earns its keep in `x + √x - 6 = 0`. There "
                  "`u² + u - 6 = (u + 3)(u - 2) = 0` gives `u = 2` or `u = -3`, but "
                  "`√x` is never negative, so `u = -3` is discarded before it is "
                  "squared. Squaring it anyway would produce `x = 9`, and "
                  "`9 + 3 - 6 = 6`, not `0` &mdash; an extraneous solution of exactly "
                  "the kind course 5 warned about."),
            ("example", ("x⁻² - x⁻¹ - 6 = 0",
                         "Put `u = x⁻¹ = 1/x`, so `u² = x⁻²` and "
                         "`u² - u - 6 = (u - 3)(u + 2) = 0`, giving `u = 3` or "
                         "`u = -2`. Then `1/x = 3` gives `x = 1/3` and `1/x = -2` "
                         "gives `x = -1/2`. Here a negative `u` is perfectly "
                         "acceptable &mdash; the restriction that matters for this "
                         "substitution is `x ≠ 0`, not a sign.")),
            ("p", "The inner expression need not be a power. In "
                  "`(x² - 3)² - 2(x² - 3) - 8 = 0`, put `u = x² - 3`: then "
                  "`u² - 2u - 8 = (u - 4)(u + 2) = 0`, so `u = 4` or `u = -2`, giving "
                  "`x² = 7` and `x² = 1`. The four solutions are `±√7` and `±1`. "
                  "Expanding the brackets first would have produced the same quartic "
                  "the long way round."),
            ("p", "One manipulation to avoid: reducing the degree by dividing by a "
                  "power of `x`. `x⁴ = 4x²` becomes `x²(x² - 4) = 0` by factoring, "
                  "with solutions `0`, `2` and `-2`; dividing both sides by `x²` "
                  "returns `x² = 4` and silently loses `x = 0`. Dividing by something "
                  "that might be zero deletes solutions, in this course and in every "
                  "later one."),
            ("p", "A last check worth making: course 4 fixed that a polynomial of "
                  "degree `n` has at most `n` real solutions. A quartic that comes back "
                  "with five, or a solution that fails when substituted, means the "
                  "return journey went wrong &mdash; usually by squaring a rejected "
                  "`u` or by forgetting a `±`."),
        ],
        "lab": ("quadratic", {
            "mode": "reducible",
            "panel_title": "Substitute, solve, substitute back",
            "panel_intro": "The three coefficients are the quadratic in `u`; the "
                           "quartic in `x` and the back-substitution are shown "
                           "underneath. Choose a preset whose `u` comes out negative "
                           "and watch two of the four solutions disappear before they "
                           "are ever written down.",
        }),
        "steps_title": "Solving by substitution",
        "steps_intro": "Four steps, and the fourth is the one the whole lesson exists to insist on.",
        "steps": [
            ("Check the shape",
             "Is one exponent exactly twice another, with only a constant besides? "
             "`x⁶ - 9x³ + 8` qualifies with `6 = 2 · 3`; `x⁴ - 9x³ + 8` does not, and "
             "no substitution will make it."),
            ("Name the substitution and its restriction",
             "Write `u = x²` or `u = √x` explicitly, and next to it any condition it "
             "forces: `u ≥ 0` for both of those, `x ≠ 0` for `u = 1/x`. Recording it "
             "now is what makes step four quick."),
            ("Solve the quadratic in u",
             "Factor, complete the square, or use the formula &mdash; whichever of "
             "lessons 2 to 5 fits. Nothing about this step is new."),
            ("Substitute back, discard, and check",
             "For each `u`, solve `f(x) = u` for `x`. Discard the values of `u` the "
             "restriction forbids, and substitute every survivor into the original "
             "equation."),
        ],
        "worked": {
            "title": "x⁴ - 13x² + 36 = 0",
            "intro": [
                "The exponents are 4 and 2, and 4 is twice 2. That is the whole reason "
                "a substitution is available here."
            ],
            "lines": [
                "u = x²,   so   x⁴ = (x²)² = u²",
                "",
                "u² - 13u + 36 = 0",
                "(u - 4)(u - 9) = 0                -4 and -9: product 36, sum -13",
                "u = 4     or     u = 9",
                "",
                "back to x:",
                "   u = 4:    x² = 4    →    x = 2   or   x = -2",
                "   u = 9:    x² = 9    →    x = 3   or   x = -3",
                "",
                "check x =  3:    81 - 13(9) + 36 = 81 - 117 + 36 = 0        ✓",
                "check x = -2:    16 - 13(4) + 36 = 16 -  52 + 36 = 0        ✓",
                "",
                "solutions:   x = -3, -2, 2, 3",
            ],
            "after": [
                "Two values of `u` and four values of `x`. Stopping at `u = 4` and "
                "`u = 9` is the error this lesson exists to prevent: `u` was a name "
                "introduced for convenience, and the question was about `x`.",
                "Both checks used the original quartic rather than the quadratic in "
                "`u`, which is the only way to test the substitution itself. A degree "
                "4 equation has at most four real solutions, and this one has four, so "
                "there is nothing left to find.",
            ],
        },
        "quiz_title": "Substitutions",
        "quiz": [
            {"q": "How many real solutions does `x⁴ - 3x² - 4 = 0` have?",
             "a": ["Four", "Two", "Three", "None"],
             "c": 1,
             "why": "With `u = x²`, `(u - 4)(u + 1) = 0` gives `u = 4` and `u = -1`. "
                    "`x² = 4` gives `x = ±2`, but `x² = -1` has no real solution, so "
                    "two of the four candidate values never appear. Over the complex "
                    "numbers there would be four, `±2` and `±i`."},
            {"q": "Solving `x - 7√x + 12 = 0` with `u = √x` gives `u = 3` and "
                  "`u = 4`. The solutions for `x` are:",
             "a": ["`x = 3` and `x = 4`", "`x = 9` and `x = 16`",
                   "`x = ±3` and `x = ±4`", "`x = 9` only"],
             "c": 1,
             "why": "`u = √x`, so `x = u²`. The first choice stops at `u`; the third "
                    "attaches a `±` that `√x` cannot have, since a square root is "
                    "never negative; and both `9` and `16` check, giving "
                    "`9 - 21 + 12 = 0` and `16 - 28 + 12 = 0`."},
            {"q": "Which substitution turns `x⁶ - 9x³ + 8 = 0` into a quadratic?",
             "a": ["`u = x²`", "`u = x³`", "`u = x⁶`", "`u = √x`"],
             "c": 1,
             "why": "The larger exponent must be twice the smaller: `6 = 2 · 3`, so "
                    "`u = x³` gives `u² - 9u + 8 = 0`, with `u = 1` and `u = 8`, hence "
                    "`x = 1` and `x = 2`. `u = x²` would leave `x⁶ = u³`, a cubic, and "
                    "`u = x⁶` leaves `x³ = √u`, which is worse than the original."},
        ],
        "mistakes": [
            ("Stopping at u",
             "`u = 4` is not a solution of an equation in `x`. Every value of `u` has "
             "to be pushed back through the substitution, and writing the substitution "
             "down at the start is what makes that step hard to forget."),
            ("Keeping a value of u that no real x produces",
             "With `u = x²` a negative `u` gives nothing real; with `u = √x` a "
             "negative `u` gives nothing at all, and squaring it produces an "
             "extraneous solution that fails the original equation. Check the "
             "restriction before squaring, not after."),
            ("Dividing by a power of x to lower the degree",
             "`x⁴ = 4x²` has solutions `0`, `2` and `-2`. Dividing by `x²` loses "
             "`x = 0`, because dividing by an expression assumes it is not zero. "
             "Factor out `x²` and use the zero product property of lesson 1 instead."),
        ],
        "standard": ("Finish when the substitution is written down explicitly, with its restriction.",
                     "Solve `2x⁴ - 5x² + 2 = 0` and state how many real solutions it "
                     "has and why. Two lines of setup &mdash; `u = x²` and `u ≥ 0` "
                     "&mdash; make the rest routine; skipping them is what turns a "
                     "four-solution problem into a two-solution answer."),
        "note": "This is the end of the course, and the technique is the one that "
                "travels furthest. Course 7 solves `4ˣ - 5·2ˣ + 4 = 0` by putting "
                "`u = 2ˣ`, which is the same move on a different expression: recognise "
                "that one power is the square of another, name the smaller one, and a "
                "quadratic appears where there was none.",
    },
]
