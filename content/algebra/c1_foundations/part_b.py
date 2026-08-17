"""Course 1, lessons 08-13 — rational exponents, and building expressions out of letters."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "rational-exponents",
        "title": "Rational Exponents",
        "module": "Exponents and radicals",
        "one_line": "Why x^(1/n) must mean the n-th root if the laws are to hold.",
        "summary": (
            "Nothing so far says what `x^(1/2)` means. Rather than invent a meaning, ask "
            "which meaning keeps the exponent laws of lesson 5 true &mdash; and there is "
            "only one. That answer is the n-th root, and everything about rational "
            "exponents follows from it."
        ),
        "key": [
            "(x^(1/n))ⁿ  =  x^(n·(1/n))  =  x¹  =  x   so x^(1/n) is an n-th root",
            "x^(p/q)   =  (the q-th root of x)^p       root first, numbers stay small",
            "          =  the q-th root of (x^p)       or power first, same answer",
            "x^(−p/q)  =  1 / x^(p/q)                  the minus inverts, never negates",
        ],
        "key_label": "One forced definition, and what follows",
        "concepts_intro": (
            "This lesson is an example of the commonest move in mathematics: a symbol is "
            "given a meaning not because it is natural but because every other meaning "
            "would break something already known to be true."
        ),
        "concepts": [
            ("The laws come first, the definition second",
             "Lesson 5 established `x^m · x^n = x^(m+n)` for whole numbers. If that "
             "sentence is to survive when `m` and `n` are fractions, then `x^(1/n)` "
             "raised to the power `n` has to be `x`. There is nothing left to choose "
             "about it."),
            ("A rational exponent is a root and a power, in either order",
             "`x^(p/q)` is the `q`-th root of `x`, raised to `p` &mdash; and it is also "
             "the `q`-th root of `x^p`. The two routes give the same number, and one of "
             "them usually involves far smaller arithmetic."),
            ("The base has to be non-negative, and that is not fussiness",
             "With a negative base the two routes can give different answers, and "
             "rewriting `2/6` as `1/3` changes the result again. The restriction `x ≥ 0` "
             "is what stops one expression having two values."),
        ],
        "read_title": "What the exponent laws force",
        "read_intro": "One derivation, one definition, and the single restriction the definition needs.",
        "body": [
            ("p", "Lesson 5 gave the exponent laws for whole-number exponents, and "
                  "extended them to `0` and to negatives by the same argument each time: "
                  "define the new symbol so that the old law keeps working. `x⁰ = 1` "
                  "because `x^n · x⁰` has to be `x^n`; `x^(−n) = 1/x^n` because "
                  "`x^n · x^(−n)` has to be `x⁰ = 1`. `x^(1/2)` is the next gap, and it "
                  "is filled the same way: ask what the laws would require of it, and "
                  "see whether anything is left over to decide."),
            ("thm", ("What a unit fraction exponent has to be",
                     "Let `n` be a whole number with `n ≥ 2`. If the law "
                     "`x^m · x^n = x^(m+n)` is to hold for fractional exponents, then "
                     "`(x^(1/n))ⁿ = x`.")),
            ("proof", [
                "`(x^(1/n))ⁿ` is `x^(1/n)` multiplied by itself `n` times.",
                "By the law, multiplying powers of `x` adds the exponents, so the product "
                "is `x` raised to `1/n + 1/n + ... + 1/n`, with `n` terms.",
                "That sum is `n · (1/n) = 1`, so the product is `x¹ = x`.",
            ]),
            ("p", "So `x^(1/n)` is a number whose `n`-th power is `x`. That is exactly "
                  "the definition of an `n`-th root of `x`, from lesson 7. The notation "
                  "was not chosen to be memorable; it was forced."),
            ("p", "One thing is still open. When `n` is even and `x` is positive there "
                  "are <em>two</em> real numbers whose `n`-th power is `x` &mdash; `2` and "
                  "`−2` both give `16` when raised to the fourth. The argument above "
                  "cannot distinguish them, so a convention has to. The convention is the "
                  "same one the radical sign uses: `x^(1/n)` denotes the non-negative "
                  "root. That part <em>is</em> arbitrary, and it is the only arbitrary "
                  "part."),
            ("def", ("Rational exponent",
                     "Let `x ≥ 0`, and let `p` and `q` be whole numbers with `q ≥ 2`. "
                     "Then `x^(p/q)` means `(x^(1/q))^p` &mdash; the `q`-th root of `x`, "
                     "raised to the power `p`.",
                     "By the power-of-a-power law this is also `(x^p)^(1/q)`, the `q`-th "
                     "root of `x^p`. Both descriptions name the same number, so you may "
                     "take whichever is easier to compute.",
                     "For a negative exponent, `x^(−p/q) = 1 / x^(p/q)`, exactly as in "
                     "lesson 5. The minus sign produces a reciprocal, never a negative "
                     "number.")),
            ("math", [
                "8^(2/3)      root first    cube root of 8 = 2,   then 2² = 4",
                "             power first   8² = 64,              then cube root of 64 = 4",
                "",
                "16^(−3/4)  =  1 / 16^(3/4)",
                "             4th root of 16 = 2,  then 2³ = 8,  so the answer is 1/8",
            ]),
            ("p", "Both routes are legal and they agree. Take the root first anyway. "
                  "`27^(4/3)` by root first is `3⁴ = 81`; by power first it is the cube "
                  "root of `27⁴ = 531441`, which is also `81` but asks you to handle a "
                  "six-digit number to get there."),
            ("h3", "Why the base has to be non-negative"),
            ("p", "Drop the restriction `x ≥ 0` and the notation stops naming one number. "
                  "Take `(−8)^(2/6)`:"),
            ("math", [
                "(−8)^(2/6)   root first    the 6th root of −8 is not a real number",
                "             power first   (−8)² = 64,  and the 6th root of 64 is 2",
                "",
                "(−8)^(1/3)   the cube root of −8 is −2,  and 2/6 = 1/3",
            ]),
            ("p", "Three readings of one symbol: no value, `2`, and `−2`. The fraction "
                  "`2/6` and the fraction `1/3` are the same rational number, so an "
                  "expression that depends on which of them you wrote is not "
                  "well defined. Restricting to `x ≥ 0` removes the problem at the "
                  "source, and it costs nothing: when you genuinely want the cube root of "
                  "`−8` you write it as a root, where it is unambiguously `−2`."),
            ("h3", "The laws, unchanged"),
            ("p", "The payoff is that every law from lesson 5 now applies to fractional "
                  "exponents with no new cases:"),
            ("math", [
                "x^(1/2) · x^(1/3)  =  x^(1/2 + 1/3)  =  x^(5/6)",
                "(x⁶)^(1/3)         =  x^(6/3)        =  x²",
                "x^(3/4) / x^(1/4)  =  x^(3/4 − 1/4)  =  x^(1/2)",
                "(8x⁶)^(2/3)        =  8^(2/3) · x⁴   =  4x⁴",
            ]),
            ("example", ("Two with fractions in them",
                         "`9^(−1/2)`: the minus gives `1 / 9^(1/2)`, and the square root "
                         "of `9` is `3`, so the value is `1/3` &mdash; positive. "
                         "`(25/4)^(3/2)`: the square root of `25/4` is `5/2`, and "
                         "`(5/2)³ = 125/8`.")),
        ],
        "lab": ("radicals", {
            "mode": "rational",
            "panel_title": "One power, computed both ways",
            "panel_intro": "Choose a base and an exponent `p/q`. The lab takes the root "
                           "first and then the power, and separately the power first and "
                           "then the root, and reports whether the two agree. Run "
                           "`(−8)^(2/6)` and then `(−8)^(1/3)` to see the restriction "
                           "earn its place.",
        }),
        "steps_title": "Evaluating a rational power",
        "steps_intro": "The negative sign and the fraction are handled separately, in this order.",
        "steps": [
            ("Deal with the minus sign first",
             "`x^(−p/q)` is `1 / x^(p/q)`. Write the reciprocal down straight away and "
             "then forget the minus; it has no further role. It does not make the answer "
             "negative."),
            ("Reduce the fraction, then check the base",
             "Put `p/q` in lowest terms. Then confirm the base is not negative &mdash; if "
             "it is, this notation does not apply and you should be working with a root "
             "sign instead."),
            ("Take the q-th root first",
             "The `q`-th root of the base, then raise the result to the power `p`. This "
             "is the route that keeps the numbers small: `27^(4/3)` is `3⁴`, not the cube "
             "root of `531441`."),
            ("Check by raising the answer back",
             "If `8^(2/3) = 4`, then `4³` should be `8² = 64`. It is. That check uses "
             "only whole-number powers, so it is independent of everything the fractional "
             "exponent did."),
        ],
        "worked": {
            "title": "Three powers, both routes",
            "intro": ["Each one is computed twice, so the arithmetic checks itself."],
            "lines": [
                "1.  8^(2/3)",
                "        root first    cube root of 8 = 2,      then 2² = 4",
                "        power first   8² = 64,                 then cube root of 64 = 4",
                "        answer        4",
                "",
                "2.  16^(−3/4)",
                "        the minus     16^(−3/4)  =  1 / 16^(3/4)",
                "        root first    4th root of 16 = 2,      then 2³ = 8",
                "        answer        1/8",
                "",
                "3.  27^(4/3)",
                "        root first    cube root of 27 = 3,     then 3⁴ = 81",
                "        power first   27⁴ = 531441,            then cube root of it = 81",
                "        answer        81",
                "",
                "check 1:  4³ = 64,  and 8² = 64                agrees",
                "check 3:  81³ = 531441,  and 27⁴ = 531441      agrees",
            ],
            "after": [
                "Line 3 is the argument for taking the root first, in one line of "
                "evidence: `3⁴` is arithmetic you can do in your head, and `27⁴` is not.",
                "The two routes agreeing is a check on this particular calculation and "
                "nothing more. What guarantees they always agree, for `x ≥ 0`, is the "
                "power-of-a-power law from lesson 5 &mdash; a general statement, proved "
                "there, which these three examples illustrate but do not establish.",
            ],
        },
        "quiz_title": "Roots as exponents",
        "quiz": [
            {"q": "Evaluate `8^(2/3)`.",
             "a": ["`2`", "`4`", "`16/3`", "`64`"],
             "c": 1,
             "why": "The cube root of `8` is `2`, and `2² = 4`. `2` is the answer you get "
                    "by taking the root and forgetting the power; `64` is `8²` with the "
                    "root forgotten; `16/3` is `8 × (2/3)`, which treats the exponent as "
                    "a multiplier."},
            {"q": "Evaluate `16^(−3/4)`.",
             "a": ["`−8`", "`8`", "`1/8`", "`1/64`"],
             "c": 2,
             "why": "The minus gives `1 / 16^(3/4)`; the 4th root of `16` is `2`, and "
                    "`2³ = 8`, so the value is `1/8`. `−8` reads the negative exponent as "
                    "a negative answer, `8` drops the minus altogether, and `1/64` uses "
                    "the square root instead of the fourth root."},
            {"q": "Which fact forces `x^(1/2)` to mean a square root of `x`?",
             "a": ["`x^(1/2) = x/2`, and halving is the inverse of doubling",
                   "`(x^(1/2))² = x^(2·(1/2)) = x¹`, so `x^(1/2)` squares to `x`",
                   "It is a definition adopted for convenience; no law requires it",
                   "Because `x^(1/2)` and `2^x` are two notations for the same thing"],
             "c": 1,
             "why": "Keeping the exponent laws true forces `x^(1/2)` to be a number whose "
                    "square is `x`. That narrows it to two candidates for `x &gt; 0`, "
                    "`√x` and `−√x`, and the non-negative one is then chosen by "
                    "convention &mdash; so the law does the work and the convention only "
                    "settles the sign."},
        ],
        "mistakes": [
            ("Reading the exponent as a multiplier",
             "`8^(2/3)` is not `8 × 2/3 = 16/3`. An exponent has never meant multiply by, "
             "and a fractional one does not start now: `2/3` still says root and power, "
             "not scale."),
            ("Thinking a negative exponent gives a negative answer",
             "`9^(−1/2) = 1/3`. The minus sign produces a reciprocal. A power of a "
             "positive base is positive whatever the exponent is, and no rearrangement "
             "can change that."),
            ("Applying rational exponents to a negative base",
             "`(−8)^(2/6)` comes out as `2` if you square first and has no real value if "
             "you take the sixth root first, while `(−8)^(1/3)` is `−2`. The definition "
             "requires `x ≥ 0` for exactly this reason; for a genuine cube root of a "
             "negative number, use the root sign."),
        ],
        "standard": ("Finish when you can say why the definition could not have been anything else.",
                     "Evaluating `16^(−3/4)` without hesitating is the easy half. The "
                     "other half is being able to answer someone who asks why `x^(1/2)` "
                     "is a square root rather than half of `x`: because the exponent law "
                     "leaves no alternative, and the only free choice left is which of "
                     "the two roots to take."),
        "note": "Every radical you meet from here on can be written as a rational power, "
                "and it is usually worth doing. Course 5 simplifies expressions like "
                "`√(x⁵)` by rewriting them as `x^(5/2)` and using the laws you already "
                "have, rather than by inventing separate rules for radicals.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "algebraic-expressions-and-terms",
        "title": "Algebraic Expressions and Terms",
        "module": "Building expressions",
        "one_line": "Variables, terms, coefficients, and the anatomy of an expression.",
        "summary": (
            "An expression is arithmetic with a letter standing in for a number. Before "
            "any rearranging is possible you have to be able to see its parts: where one "
            "term ends and the next begins, which sign belongs to which term, and what "
            "the coefficient of a term actually is."
        ),
        "key": [
            "3x² − 5x + 7        three terms:   3x²,   −5x,    7",
            "                    coefficients:   3,     −5,    7",
            "−x                  one term, coefficient −1, degree 1",
            "5(x + 2)            ONE term as written, two after expanding",
        ],
        "key_label": "Reading an expression",
        "concepts_intro": (
            "Almost every error in the next four lessons is an error of reading rather "
            "than of arithmetic: the wrong piece was treated as a unit."
        ),
        "concepts": [
            ("A letter is a number whose value is not being supplied",
             "It is not a new kind of object and it obeys no new rules. Everything in "
             "lessons 1 to 8 applies to `x` because whatever number `x` is, those "
             "statements are true of it."),
            ("Terms are separated by plus and minus signs, at the top level",
             "That is the whole rule for finding them, and it is why brackets matter so "
             "much: a plus sign inside a bracket does not separate terms. `5(x + 2)` is "
             "one term; `5x + 10` is two."),
            ("The sign in front of a term is part of the term",
             "In `3x² − 5x + 7` the second term is `−5x`, not `5x`. Subtraction is "
             "addition of a negative, so the expression is a sum of `3x²`, `−5x` and `7` "
             "&mdash; and reading it that way removes most sign errors before they happen."),
        ],
        "read_title": "The parts of an expression",
        "read_intro": "Variable, term, coefficient, factor and degree, each defined once and then used.",
        "body": [
            ("p", "An expression is a recipe for a number: it says what to do, and given "
                  "values for the letters it produces a value. It does not claim anything. "
                  "`2x + 5` is an expression; `2x + 5 = 11` is an equation, which does "
                  "make a claim and is course 2's subject. The distinction matters "
                  "immediately, because you can solve an equation and you cannot solve an "
                  "expression."),
            ("def", ("Variable, constant, expression",
                     "A <strong>variable</strong> is a letter standing for a number whose "
                     "value is not fixed. A <strong>constant</strong> is a number written "
                     "as itself. An <strong>algebraic expression</strong> is any "
                     "combination of variables and constants built with the operations of "
                     "arithmetic.",
                     "The word variable is slightly misleading: within one calculation "
                     "the letter stands for one number and does not change while you "
                     "work. It varies across problems, not across lines.")),
            ("def", ("Term",
                     "The <strong>terms</strong> of an expression are the pieces it "
                     "separates into at its top-level `+` and `−` signs. Top-level means "
                     "not inside any bracket.",
                     "The sign immediately in front of a piece belongs to that piece. An "
                     "expression is therefore always a <em>sum</em> of its terms, some of "
                     "which are negative.")),
            ("math", [
                "3x² − 5x + 7        =        3x²   +   (−5x)   +   7",
                "",
                "        term 1   3x²",
                "        term 2   −5x          the minus sign belongs to it",
                "        term 3   7",
            ]),
            ("p", "Writing the subtraction as an addition once, as above, is worth the "
                  "line. It is the reason `3x² − 5x + 7` and `−5x + 7 + 3x²` are the same "
                  "expression: terms can be reordered because addition is commutative "
                  "(lesson 2), and that permission covers the negative terms only if the "
                  "signs travel with them."),
            ("def", ("Coefficient and variable part",
                     "A term that is a number times a product of variables splits into a "
                     "<strong>coefficient</strong> &mdash; the numerical factor, sign "
                     "included &mdash; and a <strong>variable part</strong>, the letters "
                     "with their exponents.",
                     "In `−5x` the coefficient is `−5` and the variable part is `x`. In "
                     "`(2/3)x²` the coefficient is `2/3`. A term with no letters at all, "
                     "such as `7`, is a <strong>constant term</strong>.")),
            ("p", "Two coefficients are written invisibly and are misread constantly. "
                  "`x` means `1x`, so its coefficient is `1`. `−x` means `(−1)x`, so its "
                  "coefficient is `−1`. Neither is zero and neither is absent; the `1` is "
                  "simply not printed, because writing it would add nothing."),
            ("h3", "Terms and factors are different things"),
            ("p", "Terms are what an expression is added out of. <strong>Factors</strong> "
                  "are what a term is multiplied out of. `4xy` is a single term with "
                  "factors `4`, `x` and `y`. Confusing the two is what makes people "
                  "cancel across a plus sign, and it causes real damage in course 5."),
            ("p", "A bracket makes this visible. `5(x + 2)` is one term, because there is "
                  "no top-level `+` or `−` anywhere in it: it is a product of the two "
                  "factors `5` and `(x + 2)`. Multiply it out and you get `5x + 10`, "
                  "which is two terms. Both expressions have the same value for every "
                  "`x`; they do not have the same number of terms. So \"how many terms\" "
                  "is a question about a particular way of writing, and the honest answer "
                  "names the form: one as written, two expanded."),
            ("def", ("Degree",
                     "The <strong>degree of a term</strong> is the sum of the exponents "
                     "on its variables. The <strong>degree of an expression</strong> is "
                     "the largest degree of any of its terms, once like terms have been "
                     "combined.",
                     "`4xy` has degree `1 + 1 = 2`. A constant term such as `7` has "
                     "degree `0`, since `7 = 7x⁰`.")),
            ("p", "The qualification about combining matters. In `5x − 5x + 4` the "
                  "highest degree written on the page is `1`, but the two `x` terms sum "
                  "to `0` and the expression is `4`, of degree `0`. Degree describes the "
                  "expression, not the ink."),
            ("example", ("Two expressions, read part by part",
                         "`4xy − y² + 2` has three terms. Their coefficients are `4`, "
                         "`−1` and `2`; their degrees are `2`, `2` and `0`; the "
                         "expression has degree `2`. `−x + (2/3)x² − 5` has three terms "
                         "with coefficients `−1`, `2/3` and `−5`, and degree `2`. The "
                         "second is not written in descending order of degree, which is "
                         "legal and sometimes inconvenient.")),
        ],
        "lab": ("expression", {
            "mode": "terms",
            "panel_title": "Take an expression apart",
            "panel_intro": "Type an expression and the lab splits it at its top-level `+` "
                           "and `−` signs, naming the coefficient and degree of each term. "
                           "It also expands the expression and counts the terms again, so "
                           "feed it `5(x + 2)` and watch the two counts differ.",
        }),
        "steps_title": "Reading an expression correctly",
        "steps_intro": "Four passes. Do them in order; the bracket pass changes everything after it.",
        "steps": [
            ("Find the top-level plus and minus signs",
             "Ignore every sign inside a bracket. What is left between those signs are "
             "the terms, and their number is the number of terms as written."),
            ("Attach each sign to the term that follows it",
             "A term preceded by `−` is a negative term. Once the signs are attached, the "
             "expression is a sum and the terms may be written in any order."),
            ("Split each term into its coefficient and its variable part",
             "The coefficient carries the sign. A term with no printed number has "
             "coefficient `1` or `−1`; write it in if that helps, and then stop writing "
             "it in once it stops helping."),
            ("Read the degree, term by term",
             "Add the exponents within each term, then take the largest &mdash; but only "
             "after combining like terms, because cancellation can lower it."),
        ],
        "worked": {
            "title": "Taking two expressions apart",
            "intro": ["Nothing is being simplified here. This is reading, not working."],
            "lines": [
                "−x + (2/3)x² − 5",
                "",
                "        term 1   −x           coefficient −1    variable part x     degree 1",
                "        term 2   (2/3)x²      coefficient 2/3   variable part x²    degree 2",
                "        term 3   −5           coefficient −5    no variable part    degree 0",
                "",
                "        terms 3,   degree 2,   descending order: (2/3)x² − x − 5",
                "",
                "5(x + 2)",
                "",
                "        as written   ONE term,  factors 5 and (x + 2)",
                "        expanded     5x + 10,   TWO terms",
                "",
                "5x − 5x + 4",
                "",
                "        as written   three terms, highest degree written is 1",
                "        combined     4,  a single term of degree 0",
            ],
            "after": [
                "The coefficient `−1` in the first line is the one people leave blank or "
                "call `0`. It is neither. `−x` contributes `−1` of an `x` to every sum it "
                "is in, and in lesson 11 that `−1` has to be added to other coefficients "
                "like any other number.",
                "The last line shows why degree is read after combining and not before. "
                "Nothing about `5x − 5x + 4` looks like a constant until the middle step "
                "is done.",
            ],
        },
        "quiz_title": "Parts of an expression",
        "quiz": [
            {"q": "How many terms does `4xy − y² + 2` have?",
             "a": ["`1`", "`2`", "`3`", "`4`"],
             "c": 2,
             "why": "There are two top-level signs, so three terms: `4xy`, `−y²` and `2`. "
                    "`2` comes from ignoring the constant; `4` comes from counting `4` "
                    "and `xy` as separate terms, which confuses factors with terms; `1` "
                    "treats the whole expression as one term."},
            {"q": "What is the coefficient of `x` in `−x + (2/3)x² − 5`?",
             "a": ["`0`", "`1`", "`−1`", "`2/3`"],
             "c": 2,
             "why": "`−x` is `(−1)x`. The `1` is invisible but present, and the minus sign "
                    "is part of the coefficient. `0` reads the blank as nothing at all, "
                    "`1` drops the sign, and `2/3` belongs to the `x²` term."},
            {"q": "Which statement about `5(x + 2)` is correct?",
             "a": ["It has two terms, `5x` and `2`",
                   "It has two terms, `5` and `x + 2`",
                   "As written it is one term, a product of the factors `5` and "
                   "`(x + 2)`; expanded it is `5x + 10`, which is two terms",
                   "It is not a valid expression, because a bracket is not an operation"],
             "c": 2,
             "why": "The `+` is inside the bracket, so it separates nothing at the top "
                    "level. The first option is what distributing to only the first term "
                    "looks like; the second calls factors terms; the fourth is simply "
                    "false &mdash; brackets are part of the notation."},
        ],
        "mistakes": [
            ("Leaving the minus sign behind when naming a term",
             "In `3x² − 5x + 7` the second term is `−5x`. Calling it `5x` and remembering "
             "the sign separately works until the terms get reordered, and then the sign "
             "is attached to the wrong one."),
            ("Reading an invisible coefficient as zero or as nothing",
             "`x` has coefficient `1` and `−x` has coefficient `−1`. Treating either as "
             "`0` deletes a term; treating `−x` as having coefficient `1` loses a sign."),
            ("Counting the factors of a term as terms",
             "`4xy` is one term with three factors. Only a top-level `+` or `−` standing "
             "between two pieces starts a new term, and multiplication never does. Count "
             "the pieces, not the signs: `−x + (2/3)x² − 5` carries three signs and has "
             "three terms, because the leading `−` separates nothing."),
        ],
        "standard": ("Finish when you can point at every term, sign included, without pausing.",
                     "Given any expression you should be able to say how many terms it "
                     "has as written, give each coefficient with its sign, and say what "
                     "changes if the brackets are multiplied out. Lessons 10 to 13 assume "
                     "all of that is automatic, and every one of them breaks if a sign "
                     "gets attached to the wrong term."),
        "note": "The vocabulary here is not decoration. \"Combine like terms\" in lesson "
                "11, \"cancel a common factor\" in course 5 and \"the leading "
                "coefficient\" in course 4 are all instructions that name one of these "
                "parts, and following them requires having found the right part first.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "the-distributive-law",
        "title": "The Distributive Law",
        "module": "Building expressions",
        "one_line": "The one property that connects addition and multiplication.",
        "summary": (
            "Commutativity and associativity rearrange within a single operation. "
            "Distribution is the only property that lets multiplication and addition talk "
            "to each other, which makes it the licence behind expanding, factoring and "
            "very nearly every rearrangement you will make."
        ),
        "key": [
            "a(b + c)   =  ab + ac              the law",
            "a(b − c)   =  ab − ac              because b − c = b + (−c)",
            "−(x − 7)   =  −x + 7               the factor outside is −1",
            "(x + 6)/2  =  x/2 + 3   BUT   12/(x + 6) ≠ 12/x + 2",
        ],
        "key_label": "One law, and the shape that only looks like it",
        "concepts_intro": (
            "The difficulty with this law is not applying it. It is knowing where it "
            "stops, because several false rules have exactly the same shape."
        ),
        "concepts": [
            ("It is an axiom, not a consequence",
             "Nothing proves `a(b + c) = ab + ac` from the other properties &mdash; it is "
             "one of the assumed properties of the real numbers, stated in lesson 2. That "
             "is worth knowing, because it means the law is exactly as broad as it is "
             "stated and not one case broader."),
            ("The factor outside reaches every term inside",
             "Every term, not the first one. When the factor is an invisible `−1`, as in "
             "`−(x − 7)`, this is the single most common error in school algebra and it "
             "produces answers that look entirely reasonable."),
            ("Only multiplication distributes over addition",
             "Squaring does not, taking a root does not, and a sum in a denominator does "
             "not. Each of those has the shape of the law and none of them is the law; "
             "one numerical test settles each in seconds."),
        ],
        "read_title": "The law, and where it stops",
        "read_intro": "Where it comes from, how the minus sign uses it, and four things that resemble it and are false.",
        "body": [
            ("thm", ("The distributive law",
                     "For all real numbers `a`, `b` and `c`, `a(b + c) = ab + ac`.",
                     "Multiplication is commutative, so the same statement holds with the "
                     "factor on the other side: `(b + c)a = ba + ca`.")),
            ("p", "One picture, for anyone who wants the law to feel inevitable rather "
                  "than assumed: a rectangle `3` units high and `x + 4` units wide can be "
                  "cut into a `3` by `x` piece and a `3` by `4` piece. Its area is "
                  "`3(x + 4)` and it is also `3x + 12`. The picture is a reason to believe "
                  "the law, not a proof of it &mdash; it says nothing about negative or "
                  "fractional lengths, which the law covers and rectangles do not."),
            ("h3", "Subtraction, and the invisible minus one"),
            ("p", "The law is stated for addition, and that is enough, because "
                  "`b − c = b + (−c)`. Distributing over a subtraction is distributing "
                  "over the sum of `b` and `−c`:"),
            ("math", [
                "3(x + 4)     =  3·x + 3·4          =  3x + 12",
                "−2(x − 5)    =  (−2)·x + (−2)·(−5) =  −2x + 10",
                "−(x − 7)     =  (−1)·x + (−1)·(−7) =  −x + 7",
                "(1/2)(4x − 6) = (1/2)(4x) + (1/2)(−6) = 2x − 3",
            ]),
            ("p", "Line three is the one to study. A minus sign in front of a bracket is "
                  "a factor of `−1`, and it multiplies <em>every</em> term inside. "
                  "`−(x − 7)` is `−x + 7`; it is not `−x − 7`. Nothing here is being "
                  "remembered &mdash; each sign is computed, and `(−1)(−7) = +7` is a "
                  "fact from lesson 2."),
            ("p", "The habit worth forming is to write the `−1` in. It costs a symbol and "
                  "converts a sign question into a multiplication, which you can do."),
            ("h3", "More terms, and more factors"),
            ("p", "The law places no limit on how many terms are inside the bracket, "
                  "because it can be applied repeatedly:"),
            ("math", [
                "2(x + y + 3)   =  2x + 2y + 6",
                "",
                "(x + 2)(x − 3) =  x(x − 3) + 2(x − 3)        distribute the sum first",
                "               =  x² − 3x + 2x − 6",
                "               =  x² − x − 6                 then collect",
            ]),
            ("p", "The second line is the law used twice: once to split `(x + 2)` off, "
                  "and once inside each piece. There is no separate rule for multiplying "
                  "two brackets; there is this law, applied again. Course 4 does this at "
                  "length and gives it a name."),
            ("h3", "Four things that are not the distributive law"),
            ("ul", [
                "<strong>Squaring over a sum.</strong> `(a + b)²` is not `a² + b²`. At "
                "`a = 1, b = 3` the left side is `16` and the right side is `10`.",
                "<strong>Roots over a sum.</strong> `√(a + b)` is not `√a + √b`. At "
                "`a = 9, b = 16` the left side is `√25 = 5` and the right side is "
                "`3 + 4 = 7`.",
                "<strong>Multiplication over multiplication.</strong> `a(bc)` is not "
                "`(ab)(ac)`. At `a = 2, b = 3, c = 4` the left side is `24` and the right "
                "side is `48`. The law distributes multiplication over <em>addition</em>, "
                "and over nothing else.",
                "<strong>A sum in a denominator.</strong> `12/(x + 6)` is not "
                "`12/x + 12/6`. At `x = 6` the left side is `1` and the right side is "
                "`2 + 2 = 4`.",
            ]),
            ("p", "The last one deserves its own sentence, because division is where the "
                  "law is genuinely one-sided. `(x + 6)/2` <em>does</em> split, giving "
                  "`x/2 + 3`, and the reason is that dividing by `2` is multiplying by "
                  "`1/2`, so the law applies with `a = 1/2`. But `12/(x + 6)` is `12` "
                  "times `1/(x + 6)`, and `1/(x + 6)` is not `1/x + 1/6`. A sum you are "
                  "dividing splits; a sum you are dividing <em>by</em> does not."),
            ("example", ("The law read right to left",
                         "`ab + ac = a(b + c)` is the same statement written backwards, "
                         "and read that way it is called factoring. `6x + 15` is "
                         "`3(2x + 5)`, because both terms share a factor of `3`. Course 4 "
                         "is largely the study of how to find the `a` when nobody tells "
                         "you what it is.")),
        ],
        "lab": ("expression", {
            "mode": "distribute",
            "panel_title": "Two factors, every product",
            "panel_intro": "Enter the two factors and the lab multiplies every term of the "
                           "first by every term of the second, in a grid, before collecting. "
                           "Try `−1` against `x − 7` to see the minus sign reach both terms.",
        }),
        "steps_title": "Distributing without losing a sign",
        "steps_intro": "The first two steps exist entirely to make the third one arithmetic rather than memory.",
        "steps": [
            ("Write the outside factor with its sign",
             "If the bracket has nothing but a minus in front of it, write `(−1)`. An "
             "invisible factor is the one that gets applied to only half the bracket."),
            ("Rewrite every subtraction inside as an addition",
             "`x − 7` becomes `x + (−7)`. Now every term inside carries its own sign and "
             "there is no subtraction left to mishandle."),
            ("Multiply the outside factor by each term in turn",
             "One term at a time, left to right, writing each product down before moving "
             "on. Count the products against the number of terms in the bracket; they "
             "must match."),
            ("Check at one value",
             "Substitute a convenient number, `x = 1` usually, into the original and into "
             "your answer. Disagreement proves you are wrong; agreement is not a proof "
             "that you are right, but it catches nearly every sign error."),
        ],
        "worked": {
            "title": "Four brackets, and a check",
            "intro": ["Each line writes the outside factor explicitly, including where it "
                      "is an invisible `−1`."],
            "lines": [
                "1.  3(x + 4)        =  3·x + 3·4              =  3x + 12",
                "2.  −2(x − 5)       =  (−2)·x + (−2)·(−5)     =  −2x + 10",
                "3.  −(x − 7)        =  (−1)·x + (−1)·(−7)     =  −x + 7",
                "4.  (1/2)(4x − 6)   =  (1/2)(4x) + (1/2)(−6)  =  2x − 3",
                "",
                "check line 2 at x = 1:",
                "        original   −2(1 − 5)  =  −2(−4)  =  8",
                "        answer     −2(1) + 10 =  −2 + 10 =  8",
                "",
                "check line 3 at x = 1:",
                "        original   −(1 − 7)   =  −(−6)   =  6",
                "        answer     −1 + 7                =  6",
            ],
            "after": [
                "In lines 2 and 3 the sign that flipped is on the second term, and it "
                "flipped because a negative times a negative is positive. Writing "
                "`−2x − 10` or `−x − 7` is what happens when the outside factor is "
                "applied to the first term and then merely copied onto the second.",
                "The checks test one value of `x` each. That is enough to expose a wrong "
                "sign and not enough to establish that two expressions agree everywhere "
                "&mdash; what establishes that is the law itself, which is why the law is "
                "stated for all real numbers and the check is called a check.",
            ],
        },
        "quiz_title": "Distributing",
        "quiz": [
            {"q": "Expand `−2(x − 5)`.",
             "a": ["`−2x + 10`", "`−2x − 10`", "`−2x − 5`", "`2x − 10`"],
             "c": 0,
             "why": "`(−2)(x) = −2x` and `(−2)(−5) = +10`. `−2x − 10` keeps the sign of "
                    "the `−5` instead of multiplying it; `−2x − 5` distributes to the "
                    "first term only; `2x − 10` loses the minus on the outside factor."},
            {"q": "Simplify `−(x − 7)`.",
             "a": ["`−x − 7`", "`x − 7`", "`−x + 7`", "`x + 7`"],
             "c": 2,
             "why": "The factor outside is `−1`, and it multiplies both terms: `(−1)(x)` "
                    "and `(−1)(−7)`. At `x = 1` the original is `−(−6) = 6`, and only "
                    "`−x + 7` gives `6`. Every other option fails that one test."},
            {"q": "Which of these is NOT a correct rearrangement?",
             "a": ["`(x + 6)/2 = x/2 + 3`",
                   "`12/(x + 6) = 12/x + 2`",
                   "`−3(x − 2) = −3x + 6`",
                   "`(1/2)(4x − 6) = 2x − 3`"],
             "c": 1,
             "why": "A sum being divided splits, because dividing by `2` is multiplying "
                    "by `1/2` and the law applies. A sum in the denominator does not: at "
                    "`x = 6` the left side is `12/12 = 1` and the right side is `2 + 2 = "
                    "4`. The other three are the law used correctly."},
        ],
        "mistakes": [
            ("Distributing to the first term only",
             "`−2(x − 5)` is `−2x + 10`, not `−2x − 5`. The factor outside multiplies "
             "every term inside, and the terms after the first are the ones that get "
             "forgotten, because by then the eye has moved on."),
            ("Splitting a sum that is in the denominator",
             "`12/(x + 6)` is not `12/x + 2`. Reciprocals do not distribute over "
             "addition. `(x + 6)/2` does split, and the difference between the two shapes "
             "is which side of the fraction bar the sum is on."),
            ("Expecting squares and roots to distribute",
             "`(a + b)²` is `a² + 2ab + b²`, not `a² + b²`, and `√(a + b)` is not "
             "`√a + √b`. Both are checked in one line with small numbers, and both are "
             "wrong every time except in special cases such as `b = 0`."),
        ],
        "standard": ("Finish when `−(x − 3)` gives `−x + 3` with no pause and no doubt.",
                     "You should be able to expand any single bracket with a signed or "
                     "fractional factor in one step, and to say why a sum in a "
                     "denominator does not behave like a sum being divided. That "
                     "distinction is what keeps course 5 from becoming guesswork."),
        "note": "Read the law right to left and it becomes factoring, which is most of "
                "course 4. Read it left to right with two brackets and it becomes "
                "polynomial multiplication. Both directions are this one property, which "
                "is a reasonable argument for spending more time on it than it appears to "
                "deserve.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "combining-like-terms",
        "title": "Combining Like Terms",
        "module": "Building expressions",
        "one_line": "What makes two terms alike, and what does not.",
        "summary": (
            "Two terms can be added into one exactly when their variable parts are "
            "identical, and the licence to do it is the distributive law read backwards. "
            "The rule is short; the work is in seeing which terms qualify and in keeping "
            "the signs attached while you collect."
        ),
        "key": [
            "3x + 4y − x + 2y   =  2x + 6y        collected",
            "3xy + 2yx − xy     =  4xy            the order of the letters is irrelevant",
            "5x²y − 2xy²        already finished  x²y and xy² are not alike",
            "3x² + 5x²          =  8x²  NOT 8x⁴   the exponent is untouched",
        ],
        "key_label": "Three that combine, one that does not",
        "concepts_intro": (
            "Collecting like terms is the only simplification a sum offers, so the "
            "question of which terms are alike is the whole lesson."
        ),
        "concepts": [
            ("Like terms have identical variable parts",
             "The same letters, each to the same exponent. `3x²` and `−7x²` are alike; "
             "`3x²` and `3x³` are not, and no rearrangement will make them so. Both "
             "conditions, every time."),
            ("The coefficients have no say in it",
             "`100x³` and `x³` are like terms. `x³` and `x²` are not, however close they "
             "look. Whether two terms may be combined is decided entirely by the letters, "
             "and the numbers are what you then do arithmetic on."),
            ("Combining like terms is the distributive law backwards",
             "`3x² + 5x² = (3 + 5)x² = 8x²` is `ac + bc = (a + b)c` with `c = x²`. That "
             "is why no new rule is needed, and it is also why unlike terms cannot be "
             "combined: there is no common `c` to take out."),
        ],
        "read_title": "Which terms may be added",
        "read_intro": "The definition, the property that licenses it, and the four ways two terms fail to be alike.",
        "body": [
            ("def", ("Like terms",
                     "Two terms are <strong>like terms</strong> when their variable parts "
                     "are identical: the same variables, each raised to the same "
                     "exponent.",
                     "`5x²y` and `−2x²y` are like terms. `5x²y` and `5xy²` are not: the "
                     "letters match but the exponents are attached to different ones. "
                     "Constant terms are all alike, since each has an empty variable "
                     "part.")),
            ("p", "The order in which the letters are written does not affect anything, "
                  "because multiplication is commutative (lesson 2). `3xy` and `2yx` have "
                  "the same variable part written two ways, and they are like terms. "
                  "Sorting the letters alphabetically inside every term is a cheap habit "
                  "that makes this visible instead of a judgement call."),
            ("thm", ("Why like terms combine",
                     "For any numbers `a` and `b` and any variable part `v`, "
                     "`av + bv = (a + b)v`.")),
            ("proof", [
                "This is the distributive law `ac + bc = (a + b)c` of lesson 10, read "
                "from right to left, with `c` taken to be the variable part `v`.",
                "The law holds for all real numbers, and `v` stands for a real number "
                "whatever value the letters in it take, so the statement holds for every "
                "value of every variable involved.",
            ]),
            ("math", [
                "3x + 4y − x + 2y",
                "",
                "  x  terms :   3x + (−x)   =  (3 − 1)x   =  2x",
                "  y  terms :   4y + 2y     =  (4 + 2)y   =  6y",
                "",
                "  answer   :   2x + 6y",
            ]),
            ("p", "The `−x` contributes `−1`, not `−0` and not `+1`. This is the "
                  "invisible coefficient from lesson 9 doing real work: `3 − 1 = 2`, and "
                  "a reader who treats `−x` as contributing nothing gets `3x` instead."),
            ("h3", "Four ways two terms fail to be alike"),
            ("ul", [
                "<strong>Different exponent on the same letter.</strong> `x²` and `x³`. "
                "There is nothing to add: `x² + x³` is already as short as it gets.",
                "<strong>Different letters.</strong> `4x` and `4y`. Equal coefficients "
                "are irrelevant, and `4x + 4y` is finished.",
                "<strong>The same letters with the exponents swapped.</strong> `5x²y` and "
                "`2xy²`. At `x = 2, y = 3` the first is `60` and the second is `36`, so "
                "they are not even close to interchangeable.",
                "<strong>One inside a bracket that has not been expanded.</strong> "
                "`3x + 2(x + 1)` has no two like terms as it stands. Distribute first, "
                "getting `3x + 2x + 2`, and then there are.",
            ]),
            ("p", "That last case is the ordering rule for the whole subject: expand, "
                  "then collect. Collecting first is not wrong so much as premature, "
                  "because the terms you need are still hidden inside the bracket."),
            ("p", "Like terms are not a polynomial-only idea. `3√2 + 5√2 = 8√2` for "
                  "exactly the same reason, with `√2` playing the part of the variable "
                  "part &mdash; it is one fixed number, whatever it is. And `√2 + √3` "
                  "cannot be combined, for exactly the same reason `x + y` cannot."),
            ("example", ("Two collections, in full",
                         "`4a − 3b + 2a − b + 7` collects to `6a − 4b + 7`: the `a` terms "
                         "give `4 + 2 = 6`, the `b` terms give `−3 − 1 = −4`, and the `7` "
                         "has nothing to join. `2x + 3 − 5 − 2x` collects to `−2`: the "
                         "`x` terms give `2 − 2 = 0` and vanish, and `3 − 5 = −2` "
                         "remains.")),
        ],
        "lab": ("expression", {
            "mode": "like",
            "panel_title": "Group the terms by variable part",
            "panel_intro": "The lab sorts the letters inside each term and then groups "
                           "terms whose variable parts match exactly. Enter "
                           "`3xy + 2yx - xy` and then `5x^2y - 2xy^2` to see a group form "
                           "and a group refuse to.",
        }),
        "steps_title": "Collecting like terms",
        "steps_intro": "Step 1 is skipped more often than it is done, and step 1 is what makes the rest safe.",
        "steps": [
            ("Expand every bracket first",
             "Terms inside a bracket are not available to be collected. Distribute, using "
             "lesson 10, and only then look at what you have."),
            ("Attach every sign to the term that follows it",
             "Rewrite the expression as a sum of signed terms if that helps. A term "
             "carried across the page without its sign is the commonest way a correct "
             "grouping produces a wrong answer."),
            ("Group by variable part, sorting the letters within each term",
             "Write the letters of each term in alphabetical order, then gather the terms "
             "whose variable parts are now literally identical. Terms with no letters "
             "form their own group."),
            ("Add the coefficients within each group, and leave the variable part alone",
             "The exponent never changes: `3x² + 5x²` is `8x²`. If a group's coefficients "
             "sum to zero, that whole group disappears from the answer."),
        ],
        "worked": {
            "title": "One expression, grouped",
            "intro": ["`4a − 3b + 2a − b + 7`, with each group written out."],
            "lines": [
                "signs attached:   4a  +  (−3b)  +  2a  +  (−b)  +  7",
                "",
                "  a  terms :    4a + 2a        =  (4 + 2)a     =   6a",
                "  b  terms :   −3b + (−b)      =  (−3 − 1)b    =  −4b",
                "  constants:    7                                    7",
                "",
                "answer   6a − 4b + 7",
                "",
                "check at a = 1, b = 1:",
                "        original   4 − 3 + 2 − 1 + 7   =  9",
                "        answer     6 − 4 + 7           =  9",
            ],
            "after": [
                "The `b` group is where the arithmetic is. `−b` contributes `−1`, so the "
                "sum is `−3 − 1 = −4` and not `−3 − 0 = −3` or `−3 + 1 = −2`. Both of "
                "those wrong answers are produced by the same cause: the invisible `1` "
                "was not read.",
                "The check tests `a = 1, b = 1` only, which is enough to catch a dropped "
                "term or a wrong sign and is not a proof of equality. What proves it is "
                "the theorem above, which holds for every value of `a` and `b`.",
            ],
        },
        "quiz_title": "Alike or not",
        "quiz": [
            {"q": "Simplify `5x² + 2x − 3x² + x`.",
             "a": ["`2x² + 3x`", "`2x² + 2x`", "`8x² + 3x`", "`2x⁴ + 3x`"],
             "c": 0,
             "why": "`5 − 3 = 2` gives `2x²`, and `2 + 1 = 3` gives `3x` &mdash; the "
                    "lone `x` has coefficient `1`. `2x² + 2x` loses that invisible `1`, "
                    "`8x² + 3x` adds `5` and `3` instead of subtracting, and `2x⁴` adds "
                    "the exponents, which is the rule for multiplying, not adding."},
            {"q": "Which pair are like terms?",
             "a": ["`5x²y` and `2xy²`", "`3xy` and `2yx`", "`x²` and `x³`", "`4x` and `4y`"],
             "c": 1,
             "why": "`xy` and `yx` are the same product written in two orders, so the "
                    "variable parts are identical. The first pair has the exponents on "
                    "different letters, the third has different exponents, and the fourth "
                    "has different letters &mdash; equal coefficients count for nothing."},
            {"q": "Simplify `2x + 3 − 5 − 2x`.",
             "a": ["`4x − 2`", "`−2`", "`2`", "`0`"],
             "c": 1,
             "why": "The `x` terms give `2 − 2 = 0` and disappear; the constants give "
                    "`3 − 5 = −2`. `2` reverses that subtraction, `4x − 2` adds the two "
                    "`x` terms instead of subtracting, and `0` assumes the constants "
                    "cancel as well, which they do not."},
        ],
        "mistakes": [
            ("Adding the exponents instead of the coefficients",
             "`3x² + 5x² = 8x²`. Exponents add when powers are <em>multiplied</em>, which "
             "is lesson 5. Adding like terms leaves the variable part exactly as it was, "
             "and only the coefficients change."),
            ("Writing `3x + 4y = 7xy`",
             "There is nothing to combine: the variable parts differ, so no common factor "
             "can be taken out. Testing at `x = 1, y = 1` gives `7` on both sides and "
             "proves nothing; testing at `x = 2, y = 1` gives `10` against `14`."),
            ("Dropping the sign of a subtracted term",
             "In `5x² + 2x − 3x² + x` the third term is `−3x²`, so the `x²` group is "
             "`5 − 3 = 2`, not `5 + 3 = 8`. Attach every sign before grouping and this "
             "cannot happen."),
        ],
        "standard": ("Finish when you can say instantly whether two terms may be added, and why.",
                     "Given any expression you should expand, group and collect without "
                     "losing a sign or an invisible `1`, and be able to justify each "
                     "combination by naming the distributive law rather than by feel. "
                     "Course 2 solves equations by collecting on each side, and every "
                     "error made here survives into the answer there."),
        "note": "This is the last of the three reading skills. Lesson 9 found the terms, "
                "lesson 10 got them out of their brackets, and this lesson decides which "
                "may be merged. Course 4 does the same three things to polynomials and "
                "calls it addition.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "evaluating-expressions",
        "title": "Evaluating Expressions",
        "module": "Building expressions",
        "one_line": "Substitution done carefully, brackets and all.",
        "summary": (
            "Evaluating means replacing every occurrence of a letter with the same "
            "number and then doing arithmetic under the rules of lesson 3. One discipline "
            "removes almost every error: write the substituted value inside brackets, "
            "every time, whether it looks necessary or not."
        ),
        "key": [
            "x²    at x = −3    →   (−3)²   =    9",
            "−x²   at x = −3    →   −(−3)²  =   −9      the minus is not part of the base",
            "2x²   at x = 3     →   2·(3²)  =   18      not (2·3)² = 36",
            "1/(x − 2) at x = 2 →   1/0,  no value at all",
        ],
        "key_label": "Four substitutions, three traps",
        "concepts_intro": (
            "Substitution looks like the easiest thing in the course, and it produces "
            "wrong answers at a rate that says otherwise. The cause is always the same: "
            "the value went in without brackets."
        ),
        "concepts": [
            ("Substitution replaces the letter, not the structure",
             "Everything else about the expression stays exactly as it was &mdash; which "
             "operations, in which order, with which brackets. Putting the value in "
             "brackets is how you guarantee that, because a negative value squeezed in "
             "bare can change what the next operator applies to."),
            ("Every occurrence of a letter takes the same value",
             "In `x² − x` at `x = −3`, both `x`s are `−3`. A letter names one number "
             "throughout a single evaluation; if two quantities can differ, they need two "
             "letters."),
            ("Not every expression has a value at every number",
             "`1/(x − 2)` has a value at every `x` except `2`, where the substitution "
             "produces a division by zero. \"Undefined\" is a legitimate and complete "
             "answer, and course 3 gives the set of numbers that do work a name."),
        ],
        "read_title": "Substituting a number for a letter",
        "read_intro": "One discipline, and the three places it is what saves you.",
        "body": [
            ("def", ("Evaluate",
                     "To <strong>evaluate</strong> an expression at given values is to "
                     "replace every occurrence of each variable by its value and then "
                     "carry out the arithmetic, using the order of operations from "
                     "lesson 3.",
                     "The result is a single number, or else a statement that the "
                     "expression has no value there.")),
            ("p", "The discipline: <strong>write the value inside brackets</strong>. Not "
                  "as a precaution to be dropped once you are confident &mdash; as the "
                  "method. The brackets say that the whole value, sign included, is what "
                  "the surrounding operation applies to, and without them the sign can "
                  "escape."),
            ("math", [
                "x²  at  x = −3",
                "",
                "  with brackets     (−3)²   =  (−3)·(−3)  =   9        correct",
                "  without them      −3²     =  −(3·3)     =  −9        a different value",
            ]),
            ("p", "The second line is not a slip of the pen; it is a correct evaluation "
                  "of a different string. In `−3²` the exponent binds more tightly than "
                  "the minus sign, so it means `−(3²)`. Lesson 3 settled that, and "
                  "substitution is where the ruling has consequences."),
            ("h3", "The minus sign that is part of the expression"),
            ("p", "Compare two expressions that differ only by brackets. At `x = −3`:"),
            ("math", [
                "−x²    means  −(x²)      →   −((−3)²)   =  −(9)   =  −9",
                "(−x)²  means  (−x)·(−x)  →   (−(−3))²   =  (3)²   =   9",
            ]),
            ("p", "Both evaluations are right. They are answers to different questions, "
                  "and neither is a misreading of the other. In `−x²` the minus is "
                  "applied after the squaring, so a negative `x` gives a negative result; "
                  "in `(−x)²` the negation happens first and the square is positive. "
                  "Knowing which expression you were handed is the whole of it."),
            ("h3", "Operations that are not written down"),
            ("p", "`3x` means `3 · x`, so at `x = 4` it is `3(4) = 12` and never `34`. "
                  "This is the clearest reason to bracket the substituted value: without "
                  "brackets the multiplication sign that was invisible when there was a "
                  "letter there becomes invisible when there is a digit there, and digits "
                  "written next to each other mean something else entirely. A coefficient "
                  "is also not part of the base: `2x²` is `2·(x²)`, because the exponent "
                  "attaches only to the `x` immediately under it."),
            ("math", [
                "2x²   at x = 3    →   2·(3²)   =  2·9   =  18",
                "(2x)² at x = 3    →   (2·3)²   =  6²    =  36",
            ]),
            ("h3", "Several letters, and values that do not exist"),
            ("p", "With more than one letter, substitute all of them before doing any "
                  "arithmetic, then evaluate the resulting numerical expression in the "
                  "usual order:"),
            ("math", [
                "x² − y²    at  x = −3, y = 2     →   (−3)² − (2)²   =  9 − 4  =  5",
                "5 − 2x     at  x = −4            →   5 − 2(−4)      =  5 + 8  =  13",
                "1/(x − 2)  at  x = 2             →   1/(2 − 2)  =  1/0,  undefined",
            ]),
            ("p", "The third line is not a failure of the method. Division by zero has no "
                  "value, so the expression has no value at `x = 2`, and the correct "
                  "answer to \"evaluate it there\" is that you cannot. Every other real "
                  "number works. Course 3 calls the set of inputs that work the domain "
                  "and makes finding it a routine step."),
            ("example", ("A fraction substituted",
                         "`2x² − 3x + 1` at `x = −1/2`. In brackets: "
                         "`2(−1/2)² − 3(−1/2) + 1`. The square is `1/4`, so the first "
                         "term is `2 · 1/4 = 1/2`. The second is `−3 · (−1/2) = 3/2`. "
                         "Then `1/2 + 3/2 = 2`, and `2 + 1 = 3`. The value is `3` "
                         "&mdash; exact, with no decimal anywhere in the working.")),
        ],
        "lab": ("expression", {
            "mode": "evaluate",
            "panel_title": "Substitute, with brackets and without",
            "panel_intro": "Choose an expression and values for its letters. The lab does "
                           "the substitution twice, bracketing the values in one pass and "
                           "not the other, and shows where the two answers part company. "
                           "Try `-x^2` at `x = -3`.",
        }),
        "steps_title": "Evaluating an expression",
        "steps_intro": "Four steps, and the first one is the only one that is a habit rather than arithmetic.",
        "steps": [
            ("Copy the expression out, replacing each letter with a bracketed value",
             "`(−3)`, not `−3`. Do this for every occurrence of every letter, and change "
             "nothing else about the expression while you do it."),
            ("Restore the invisible multiplication signs",
             "`3x` becomes `3(4)`, which is a product. If you find yourself looking at "
             "two digits written next to each other, a multiplication sign has gone "
             "missing."),
            ("Work out the value under the order of operations",
             "Brackets, then exponents, then multiplication and division left to right, "
             "then addition and subtraction left to right. Lesson 3 gave the rule; "
             "substitution does not amend it."),
            ("Say so if there is no value",
             "A division by zero, or an even root of a negative number, means the "
             "expression is undefined at that input. Write that down rather than "
             "producing a number."),
        ],
        "worked": {
            "title": "Two evaluations that people get wrong",
            "intro": ["The first is a fraction; the second is the sign trap."],
            "lines": [
                "1.  2x² − 3x + 1   at  x = −1/2",
                "",
                "        substitute    2(−1/2)² − 3(−1/2) + 1",
                "        exponent      (−1/2)²  =  1/4",
                "        multiply      2 · 1/4      =  1/2",
                "        multiply      −3 · (−1/2)  =  3/2",
                "        add           1/2 + 3/2  =  2",
                "        add           2 + 1      =  3",
                "        answer        3",
                "",
                "2.  −x²  and  (−x)²   at  x = −3",
                "",
                "        −x²    =  −((−3)²)   =  −(9)    =  −9",
                "        (−x)²  =  (−(−3))²   =  (3)²    =   9",
            ],
            "after": [
                "In part 1 the sign work is all in the second multiplication: `−3` times "
                "`−1/2` is `+3/2`, and dropping that sign gives `0` instead of `3`. "
                "Everything stays an exact fraction, so nothing is lost to rounding.",
                "Part 2 shows two expressions and two answers, not one expression and a "
                "choice. Which one you are evaluating is decided by the brackets printed "
                "in the question, and the only way to keep them straight is to carry them "
                "through the substitution.",
            ],
        },
        "quiz_title": "Substitution",
        "quiz": [
            {"q": "Evaluate `−x²` at `x = −3`.",
             "a": ["`9`", "`−9`", "`6`", "`−6`"],
             "c": 1,
             "why": "`−x²` means `−(x²)`, so square first: `(−3)² = 9`, then apply the "
                    "minus, giving `−9`. `9` is the value of `(−x)²`, a different "
                    "expression; `6` and `−6` come from multiplying by `2` instead of "
                    "squaring."},
            {"q": "Evaluate `2x² − 3x + 1` at `x = −1/2`.",
             "a": ["`0`", "`2`", "`3`", "`7/2`"],
             "c": 2,
             "why": "`2(1/4) = 1/2`, `−3(−1/2) = 3/2`, and `1/2 + 3/2 + 1 = 3`. `0` comes "
                    "from dropping the sign on `−3x`; `2` from reading `(−1/2)²` as "
                    "`−1/4`; `7/2` from computing `(2x)²` instead of `2x²`."},
            {"q": "Evaluate `1/(x − 2)` at `x = 2`.",
             "a": ["`0`", "`1`", "`1/2`", "It has no value: the substitution gives `1/0`"],
             "c": 3,
             "why": "The denominator becomes `2 − 2 = 0`, and division by zero has no "
                    "result, so the expression is undefined at `x = 2`. `0` and `1` are "
                    "guesses at what dividing by zero \"should\" give; `1/2` substitutes "
                    "into the wrong place."},
        ],
        "mistakes": [
            ("Substituting a negative value without brackets",
             "`x²` at `x = −3` written as `−3²` evaluates to `−9`, because the exponent "
             "binds tighter than the minus. The brackets in `(−3)²` are what keep the "
             "sign inside the base, and they are not optional."),
            ("Treating the coefficient as part of the base",
             "`2x²` at `x = 3` is `18`, not `36`. The exponent applies to the `x` alone. "
             "`(2x)²` is the expression that gives `36`, and it is a different one."),
            ("Assuming a value always exists",
             "`1/(x − 2)` has no value at `x = 2`, and `√(x − 5)` has no real value at "
             "`x = 1`. Producing a number anyway &mdash; usually `0` &mdash; is worse "
             "than writing \"undefined\", because it is a wrong answer rather than a "
             "correct one."),
        ],
        "standard": ("Finish when the brackets go in without you deciding to put them there.",
                     "You should be able to evaluate an expression at a negative fraction "
                     "and get the sign right first time, and to say without hesitating "
                     "how `−x²` and `(−x)²` differ. Course 3 evaluates expressions "
                     "thousands of times under the name `f(x)`, and it assumes this is "
                     "already reflex."),
        "note": "Evaluating at a single value is also the cheapest check you have. If two "
                "expressions are supposed to be equal and they disagree at one number, "
                "one of them is wrong &mdash; a complete disproof from one line of "
                "arithmetic. Agreement at one number is not a proof of anything, which is "
                "why a check is a check and not a demonstration.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "translating-words-into-algebra",
        "title": "Translating Words into Algebra",
        "module": "Building expressions",
        "one_line": "Turning a sentence into an expression, and naming the unknown.",
        "summary": (
            "Most word-problem errors are made before any algebra happens, in deciding "
            "what the letter stands for and which way round a subtraction goes. The "
            "translation itself is a short vocabulary plus two rules: which phrases "
            "reverse the order, and which phrases create a bracket."
        ),
        "key": [
            "five less than a number n         n − 5        not 5 − n",
            "twice the sum of n and 3          2(n + 3)",
            "the sum of twice n and 3          2n + 3",
            "three less than the square of n   n² − 3       not (n − 3)²",
        ],
        "key_label": "Four phrases, and the two they are confused with",
        "concepts_intro": (
            "English is ambiguous and algebra is not, so translating always loses "
            "something. The skill is knowing which of the possible readings the sentence "
            "actually licenses."
        ),
        "concepts": [
            ("Name the unknown before writing anything",
             "\"Let `n` be the number of quarters\" is a definition you can check against "
             "later. \"Let `n` be the quarters\" is not, because it does not say whether "
             "`n` counts coins or measures money. Half the errors in course 2 are made in "
             "this sentence and inherited by everything after it."),
            ("Addition and multiplication do not care about order; subtraction and division do",
             "`n + 5` and `5 + n` are the same expression, so no phrase involving \"sum\" "
             "can be got wrong by ordering. `n − 5` and `5 − n` are different, so every "
             "phrase involving \"less than\" or \"subtracted from\" has to be read "
             "carefully."),
            ("A bracket is what \"the sum of\" and \"the quantity\" produce",
             "\"Twice the sum of `n` and 3\" is `2(n + 3)`: the phrase names one quantity "
             "and then doubles it. \"The sum of twice `n` and 3\" is `2n + 3`. Word order "
             "is doing the work brackets do in algebra, and it does it less clearly."),
        ],
        "read_title": "From a sentence to an expression",
        "read_intro": "Naming the unknown, the vocabulary, the phrases that reverse, and the phrases that bracket.",
        "body": [
            ("h3", "Name the unknown first, with its units"),
            ("p", "Before translating anything, write a sentence of the form \"let `n` be "
                  "the number of ...\" or \"let `c` be the cost in dollars of ...\". It takes "
                  "a line and it settles two things that otherwise stay vague: what is "
                  "being counted or measured, and in what units. "
                  "The reason is that expressions are checked by substituting, and you "
                  "cannot check `25n` unless you know whether `n` is a number of quarters "
                  "or an amount of money. If `n` is the number of quarters then `25n` is "
                  "the value in cents and the expression is right; if `n` is already an "
                  "amount in dollars then `25n` is meaningless."),
            ("h3", "The vocabulary"),
            ("math", [
                "the sum of a and b            a + b",
                "a increased by b              a + b",
                "the difference of a and b     a − b",
                "a decreased by b              a − b",
                "the product of a and b        ab",
                "twice a,  a doubled           2a",
                "the quotient of a and b       a/b",
                "half of a                     a/2",
                "the square of a               a²",
                "a more than b                 b + a",
                "a less than b                 b − a          note the order",
            ]),
            ("p", "Every line above is a convention of English, not of mathematics. They "
                  "are worth learning because everyone writing problems uses them the "
                  "same way, and worth distrusting whenever a sentence is unusual: when "
                  "the English is genuinely ambiguous, the right move is to say which "
                  "reading you took, not to guess silently."),
            ("h3", "The phrases that reverse the order"),
            ("p", "Division carries this hazard too: \"the quotient of `n` and 4\" is "
                  "`n/4`, and so is \"4 divided into `n`\", but \"`n` divided into 4\" "
                  "is `4/n` &mdash; whenever a phrase uses \"into\", read it twice. "
                  "Subtraction is where it bites most often, because \"less than\" and "
                  "\"subtracted from\" name the second quantity first:"),
            ("math", [
                "five less than a number n        n − 5",
                "n less than five                 5 − n",
                "five subtracted from n           n − 5",
                "",
                "test at n = 8:   five less than 8 is 3,   and   8 − 5 = 3",
                "                 5 − 8 = −3,  so 5 − n is the other phrase",
            ]),
            ("h3", "The phrases that create a bracket"),
            ("p", "\"The sum of `n` and 3\" packages two things into one quantity. "
                  "Anything applied to that package applies to all of it, which in algebra "
                  "means a bracket:"),
            ("math", [
                "twice the sum of n and 3          2(n + 3)",
                "the sum of twice n and 3          2n + 3",
                "",
                "test at n = 5:   the sum is 8, twice it is 16      2(5 + 3) = 16",
                "                 twice 5 is 10, plus 3 is 13       2(5) + 3 = 13",
                "",
                "three less than the square of n   n² − 3",
                "the square of three less than n   (n − 3)²",
                "",
                "test at n = 5:   the square is 25, three less is 22    5² − 3 = 22",
                "                 three less than 5 is 2, squared is 4  (5 − 3)² = 4",
            ]),
            ("p", "In each pair the words are almost the same and the expressions are not "
                  "close: at `n = 5` they differ by `3` in the first pair and by `18` in "
                  "the second. The bracket is carrying the meaning, and dropping it does "
                  "not produce a slightly different answer, it produces a different "
                  "quantity."),
            ("h3", "Quantities that come in families"),
            ("p", "Some phrases describe several unknowns at once, and the point of "
                  "algebra is that one letter covers them all:"),
            ("ul", [
                "Three consecutive integers, the smallest being `n`: `n`, `n + 1`, "
                "`n + 2`.",
                "Three consecutive even integers, the smallest being `n`: `n`, `n + 2`, "
                "`n + 4`. The `n` itself has to be even, which is a condition on the "
                "letter and not part of the expression.",
                "A rectangle `3` cm longer than it is wide, width `w` cm: length `w + 3`, "
                "perimeter `2w + 2(w + 3) = 4w + 6`, area `w(w + 3)`.",
                "The value in cents of `q` quarters and `d` dimes: `25q + 10d`. Two "
                "unknowns need two letters, and the units have to match before the terms "
                "may be added.",
            ]),
            ("example", ("Checking a translation",
                         "Pick a number, read the English sentence aloud with that number "
                         "in it, and compare with your expression evaluated there. For "
                         "\"twice the sum of `n` and 3\" at `n = 5`: the sentence says "
                         "the sum is `8` and twice that is `16`; `2(n + 3)` gives `16` "
                         "and `2n + 3` gives `13`. That test rules out `2n + 3`. It does "
                         "not prove `2(n + 3)` is right &mdash; agreement at one number "
                         "never does &mdash; but a wrong translation almost always fails "
                         "it.")),
        ],
        "lab": ("expression", {
            "mode": "translate",
            "panel_title": "Two readings of one phrase",
            "panel_intro": "Choose a phrase and edit the expression in `n` you think it "
                           "means. The lab evaluates your reading and the rival reading at "
                           "seven values of `n` and reports where they disagree, which is "
                           "the check worth copying by hand.",
        }),
        "steps_title": "Translating a sentence",
        "steps_intro": "The first two steps produce no algebra at all, and skipping them is what goes wrong.",
        "steps": [
            ("Write down what the letter stands for, with units",
             "\"Let `w` be the width in centimetres.\" One line, and every later "
             "expression can be checked against it. If the problem has two independent "
             "unknowns, it needs two letters."),
            ("Express every other quantity in terms of that letter",
             "The length is `w + 3`; the second integer is `n + 1`; the number of dimes "
             "in a purse of 20 coins holding `q` quarters is `20 − q`. Do this before "
             "assembling anything, so that the final expression is built from pieces you "
             "have already justified."),
            ("Translate phrase by phrase, bracketing anything the English packages",
             "Work outward from the innermost quantity. Wherever the sentence says \"the "
             "sum of\" or \"the quantity\", put a bracket round it, and only then apply "
             "whatever is done to it."),
            ("Test with one number, chosen to separate the readings",
             "Substitute a value and compute the sentence in English alongside your "
             "expression. Avoid `0` and `1`, which make too many wrong expressions agree "
             "with the right one, and then check that the value you picked does separate "
             "the two readings in front of you: `n = 5` is no use for \"five less than "
             "`n`\", because `n − 5` and `5 − n` are both `0` there."),
        ],
        "worked": {
            "title": "Four phrases, translated and tested",
            "intro": ["Each translation is followed by the test value that rules out the "
                      "usual rival reading."],
            "lines": [
                "1.  five less than a number n            n − 5",
                "        test n = 8    the phrase says 3,      n − 5 = 3",
                "                      5 − n = −3,             so 5 − n is not it",
                "",
                "2.  twice the sum of n and 3             2(n + 3)",
                "        test n = 5    the sum is 8, twice is 16,   2(5 + 3) = 16",
                "                      2n + 3 = 13,            so the bracket is needed",
                "",
                "3.  the sum of twice n and 3             2n + 3",
                "        test n = 5    twice 5 is 10, plus 3 is 13,  2(5) + 3 = 13",
                "",
                "4.  three less than the square of n      n² − 3",
                "        test n = 5    the square is 25, three less is 22,  5² − 3 = 22",
                "                      (n − 3)² = 4,           a different quantity",
            ],
            "after": [
                "Phrases 2 and 3 use the same seven words in a different order and mean "
                "different things. English marks the difference with word order alone; "
                "algebra marks it with a bracket, which is one reason the translation is "
                "worth doing early rather than carrying the sentence around in your head.",
                "Every test above rules a rival reading out. None of them proves the "
                "chosen reading correct, because two different expressions can agree at "
                "one value &mdash; `n − 5` and `5 − n` both give `0` at `n = 5`, which is "
                "exactly why `n = 5` would have been a bad test for phrase 1.",
            ],
        },
        "quiz_title": "English into algebra",
        "quiz": [
            {"q": "Which expression is \"five less than a number `n`\"?",
             "a": ["`5 − n`", "`n − 5`", "`5n`", "`n/5`"],
             "c": 1,
             "why": "\"Less than\" names the amount subtracted first and the thing "
                    "subtracted from second. At `n = 8` the phrase means `3`, and only "
                    "`n − 5` gives it; `5 − n` gives `−3`. The other two translate "
                    "\"times\" and \"divided by\"."},
            {"q": "Which expression is \"twice the sum of `n` and 3\"?",
             "a": ["`2n + 3`", "`2(n + 3)`", "`n + 6`", "`2 + n + 3`"],
             "c": 1,
             "why": "\"The sum of `n` and 3\" is one quantity, so it takes a bracket, and "
                    "\"twice\" applies to all of it. At `n = 5` the phrase means `16`; "
                    "`2n + 3` gives `13`, `n + 6` doubles only the `3`, and `2 + n + 3` "
                    "reads \"twice\" as \"add two\"."},
            {"q": "A rectangle is 3 cm longer than it is wide. Its width is `w` cm. Which "
                  "expression is its perimeter, in centimetres?",
             "a": ["`4w + 6`", "`4w + 3`", "`2w + 3`", "`w(w + 3)`"],
             "c": 0,
             "why": "The length is `w + 3`, so the perimeter is `2w + 2(w + 3) = 4w + 6`. "
                    "`4w + 3` adds the `3` once instead of twice, `2w + 3` adds one width "
                    "and one length only, and `w(w + 3)` is the area &mdash; a different "
                    "quantity, measured in square centimetres."},
        ],
        "mistakes": [
            ("Writing \"five less than n\" as `5 − n`",
             "The English puts the subtracted amount first and algebra puts it second. "
             "Subtraction is not commutative, so the two expressions differ at every `n` "
             "except `n = 5`, where both are `0`."),
            ("Dropping the bracket that \"the sum of\" asks for",
             "\"Twice the sum of `n` and 3\" is `2(n + 3)`, not `2n + 3`. The phrase "
             "names a single quantity and then doubles it, and without the bracket only "
             "the first part gets doubled."),
            ("Not saying what the letter stands for",
             "\"Let `n` be the money\" cannot be checked: `n` might be dollars or cents, "
             "and `25n` is right in one reading and nonsense in the other. Name the "
             "quantity and its units in a full sentence before any expression is "
             "written."),
        ],
        "standard": ("Finish when you write the \"let n be ...\" line without being asked.",
                     "Given a sentence you should produce a named unknown with units, an "
                     "expression for every other quantity in terms of it, and a test "
                     "value that separates your reading from the obvious rival. That is "
                     "the whole of what course 2 calls setting up a word problem; solving "
                     "the equation afterwards is the easy half."),
        "note": "This is the last lesson of the course, and it is the one that gets used "
                "first. Course 2 turns these expressions into equations by setting two of "
                "them equal, and every technique it teaches for solving is worthless if "
                "the equation was written from a misread sentence.",
    },
]
