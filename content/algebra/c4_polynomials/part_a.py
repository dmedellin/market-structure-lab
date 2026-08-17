"""Course 4, lessons 01-07 — polynomial arithmetic, and the first factoring techniques."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "polynomials-degree-and-standard-form",
        "title": "Polynomials, Degree and Standard Form",
        "module": "Polynomial arithmetic",
        "one_line": "What counts as a polynomial, and what does not.",
        "summary": (
            "A polynomial is a finite sum of terms, each a number times a whole-number "
            "power of the variable. Establish which expressions qualify, why `1/x` and "
            "`√x` do not, and what degree measures once they do."
        ),
        "key": [
            "3x⁴ − 5x² + x − 7     polynomial: degree 4, leading coefficient 3",
            "2/x  =  2x⁻¹          NOT a polynomial (negative exponent)",
            "√x   =  x^(1/2)       NOT a polynomial (fractional exponent)",
            "2ˣ                    NOT a polynomial (variable in the exponent)",
        ],
        "key_label": "Four expressions, one polynomial",
        "concepts_intro": (
            "Every rule in this course is stated for polynomials and is guaranteed only "
            "for polynomials. So the first job is to say exactly which expressions those "
            "are."
        ),
        "concepts": [
            ("The exponents are whole numbers",
             "`0, 1, 2, 3, …` and nothing else. That single restriction is what makes "
             "the whole course work: it is why like terms exist, why degree behaves "
             "predictably, and why every technique here terminates."),
            ("Degree is the handle on the whole expression",
             "One number, read off the highest power, that predicts how the expression "
             "behaves under addition and multiplication and how many roots it can have. "
             "Most decisions in this course start by looking at it."),
            ("Standard form is a convention, not a rule of algebra",
             "Writing terms in descending degree changes nothing about the expression. "
             "It is worth doing because every later procedure &mdash; division in "
             "lesson 10 especially &mdash; assumes the terms are in that order."),
        ],
        "read_title": "What a polynomial is",
        "read_intro": "One definition, the three ways an expression fails it, and the vocabulary that follows.",
        "body": [
            ("def", ("Polynomial in one variable",
                     "A <strong>polynomial in `x`</strong> is an expression that can be "
                     "written as a finite sum `aₙxⁿ + aₙ₋₁xⁿ⁻¹ + … + a₁x + a₀`, where "
                     "`n` is a whole number and the <strong>coefficients</strong> "
                     "`aₙ, …, a₀` are numbers.",
                     "\"Can be written as\" matters: `x(x + 1)` is a polynomial, because "
                     "multiplying it out gives `x² + x`.")),
            ("p", "Each `aₖxᵏ` is a <strong>term</strong>. The number `aₖ` is the "
                  "coefficient of that term, and `a₀` &mdash; the term with no `x` "
                  "&mdash; is the <strong>constant term</strong>."),
            ("p", "Three kinds of expression fail the definition, each for the same "
                  "underlying reason: the exponent is not a whole number."),
            ("ul", [
                "<strong>Negative exponents.</strong> `2/x` is `2x⁻¹`, and `−1` is not a "
                "whole number. Expressions like this are <em>rational</em>, and course 5 "
                "handles them.",
                "<strong>Fractional exponents.</strong> `√x` is `x^(1/2)`. This is a "
                "<em>radical</em> expression, also course 5.",
                "<strong>The variable in the exponent.</strong> `2ˣ` has a constant base "
                "and a variable exponent, which is the exact reverse of `x²`. That is an "
                "<em>exponential</em>, and course 7 is about it.",
            ]),
            ("p", "A polynomial may contain more than one variable: `4x²y − 3xy + y³` is "
                  "a polynomial in `x` and `y`. The same restriction applies to every "
                  "variable in every term."),
            ("def", ("Degree, leading coefficient, standard form",
                     "The <strong>degree</strong> of a polynomial is the largest exponent "
                     "appearing on the variable, once like terms are combined. The "
                     "coefficient of that term is the <strong>leading coefficient</strong>. "
                     "A polynomial is in <strong>standard form</strong> when its terms are "
                     "written in descending order of degree.",
                     "For a term in several variables, the degree of that term is the "
                     "<em>sum</em> of the exponents: `4x²y` has degree 3.")),
            ("p", "\"Once like terms are combined\" is not a decoration. In "
                  "`x³ + 5x − x³` the highest power written is 3, but the `x³` terms "
                  "cancel and the polynomial is `5x`, of degree 1. Degree is a property "
                  "of the polynomial, not of the way it happens to be written."),
            ("p", "Two cases at the bottom of the scale. A nonzero constant such as `7` "
                  "is `7x⁰`, so it has degree 0. The zero polynomial has no degree at all "
                  "&mdash; there is no highest power to point at, and every convention "
                  "for assigning it one exists only to keep later statements tidy."),
            ("p", "Short polynomials are named by their number of terms: one term is a "
                  "<strong>monomial</strong>, two a <strong>binomial</strong>, three a "
                  "<strong>trinomial</strong>. Beyond three, nobody bothers."),
            ("example", ("Reading a polynomial",
                         "`−2x³ + 5x + 8` is a trinomial in standard form. Degree 3, "
                         "leading coefficient `−2`, constant term `8`. The coefficient of "
                         "`x²` is `0`, which is worth saying out loud &mdash; lesson 10 "
                         "will make you write that zero down.")),
        ],
        "lab": ("polynomial", {
            "mode": "form",
            "panel_title": "Type a polynomial, see it sorted",
            "panel_intro": "The lab combines like terms and orders by degree, then reports "
                           "the degree and leading coefficient of what is left. Feed it "
                           "`x^3 + 5x - x^3` and watch the degree drop to 1.",
        }),
        "steps_title": "Putting an expression in standard form",
        "steps_intro": "Four moves, in this order. The first one can end the exercise.",
        "steps": [
            ("Check that it is a polynomial at all",
             "Look at every exponent on every variable. A negative one, a fractional one, "
             "or a variable sitting in an exponent means the techniques in this course do "
             "not apply, and a different course does."),
            ("Multiply out anything in brackets",
             "The definition asks whether the expression <em>can be</em> written as a sum "
             "of terms, so `x(x + 1)` qualifies. You cannot read the degree off a "
             "factored form reliably until lesson 3."),
            ("Combine like terms",
             "Terms with the same power of the same variable add together. Do this before "
             "reading the degree, because cancellation can lower it."),
            ("Order the terms downward, then read off the data",
             "Highest power first. The degree and the leading coefficient are then the "
             "first thing you see, which is the whole point of the convention."),
        ],
        "worked": {
            "title": "Classify, then standardise",
            "intro": ["Five expressions. Say whether each is a polynomial, and give the "
                      "reason when it is not."],
            "lines": [
                "1.  5x − 3x³ + 8 + x³      polynomial",
                "        combine:  −3x³ + x³ = −2x³",
                "        standard: −2x³ + 5x + 8    degree 3, leading coefficient −2",
                "",
                "2.  4x²y − 3xy + y³        polynomial in x and y, degree 3",
                "        (4x²y has degree 2 + 1 = 3;  y³ has degree 3)",
                "",
                "3.  x² + 3/x               NOT a polynomial:  3/x = 3x⁻¹",
                "4.  √x + 1                 NOT a polynomial:  √x = x^(1/2)",
                "5.  7                      polynomial, degree 0  (it is 7x⁰)",
            ],
            "after": [
                "Line 1 is the one that catches people. Written as it stands, the highest "
                "power on the page is 3 and the leading coefficient looks like `−3`. "
                "Neither reading survives combining like terms, and combining like terms "
                "is not optional &mdash; it is how you find out what the polynomial "
                "actually is."
            ],
        },
        "quiz_title": "Polynomial or not",
        "quiz": [
            {"q": "Which expression is a polynomial?",
             "a": ["`x² + 2ˣ`", "`3x⁵ − x + 1/2`", "`4/x² + x`", "`√x + x²`"],
             "c": 1,
             "why": "Every exponent on `x` is a whole number. A <em>coefficient</em> may "
                    "be any number at all &mdash; the `1/2` is fine. The restriction is "
                    "on exponents, not on coefficients."},
            {"q": "What is the degree of `x³ + 4x² − x³ + 7`?",
             "a": ["3", "2", "1", "0"],
             "c": 1,
             "why": "The `x³` terms cancel, leaving `4x² + 7`. Degree is read after "
                    "combining like terms, not from the longest-looking term on the page."},
            {"q": "`−2x³ + 5x + 8` is in standard form. What is its leading coefficient?",
             "a": ["8", "5", "3", "−2"],
             "c": 3,
             "why": "The leading coefficient belongs to the highest-degree term, which is "
                    "`−2x³`. The sign is part of it. `8` is the constant term and `3` is "
                    "the degree, not a coefficient at all."},
        ],
        "mistakes": [
            ("Reading the degree off the first term written",
             "Standard form makes that reliable; nothing else does. `5x − 3x³ + 8 + x³` "
             "has degree 3 with leading coefficient `−2`, and you can only know that after "
             "combining."),
            ("Thinking a fractional coefficient disqualifies an expression",
             "`(1/2)x³ − 0.7x` is a perfectly good polynomial. The definition restricts "
             "the exponents; the coefficients can be any numbers."),
            ("Calling a factored expression \"not a polynomial\"",
             "`(x + 1)(x − 4)` is a polynomial, because it <em>can be</em> written as "
             "`x² − 3x − 4`. The definition asks what the expression equals, not how it "
             "is currently printed."),
        ],
        "standard": ("Finish when you can reject a non-polynomial and name the exponent that spoils it.",
                     "Given a mixed list you should sort it without hesitating, and for "
                     "each rejection point at the specific exponent &mdash; negative, "
                     "fractional, or variable &mdash; that fails the definition. That "
                     "habit is what stops you applying a factoring technique to `1/x + x` "
                     "in course 5 and getting nonsense."),
        "note": "The lab reports the degree after combining, which is why it is worth "
                "typing in something that cancels. Degree is the number this whole course "
                "steers by: it bounds how many roots a polynomial can have (lesson 13) and "
                "it tells you when polynomial division has finished (lesson 10).",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "adding-and-subtracting-polynomials",
        "title": "Adding and Subtracting Polynomials",
        "module": "Polynomial arithmetic",
        "one_line": "Like terms combine; everything else stays where it is.",
        "summary": (
            "Addition collects like terms, and the licence to do it is the distributive "
            "law read backwards. Subtraction is the same operation after the minus sign "
            "has been distributed over every term &mdash; which is where the errors live."
        ),
        "key": [
            "axⁿ + bxⁿ  =  (a + b)xⁿ        like terms combine",
            "x² + x³    stays as it is      NOT like terms",
            "",
            "A − (B + C)  =  A − B − C      the minus reaches every term",
        ],
        "key_label": "One legal move, and one trap",
        "concepts_intro": (
            "There is only one new idea here, and it is not \"add the numbers\". It is "
            "the question of when you are allowed to."
        ),
        "concepts": [
            ("Like terms are terms with the identical variable part",
             "`3x²` and `−7x²` are like terms. `3x²` and `3x³` are not, and no amount of "
             "rearranging will make them so. Same variable, same exponent &mdash; both "
             "conditions, every time."),
            ("Combining like terms IS the distributive law",
             "`3x² + 5x² = (3 + 5)x² = 8x²` because `ab + ac = a(b + c)` with `a = x²`. "
             "You are not inventing a rule for polynomials; you are using the one rule "
             "arithmetic already gave you."),
            ("Subtraction distributes over every term, not just the first",
             "`(A) − (B + C)` is `A − B − C`. Missing the second sign flip is the most "
             "common single error in this course, and it produces an answer that looks "
             "entirely reasonable."),
        ],
        "read_title": "Collecting what can be collected",
        "read_intro": "Why like terms combine, why unlike terms cannot, and what subtraction really is.",
        "body": [
            ("def", ("Like terms",
                     "Two terms are <strong>like terms</strong> when their variable parts "
                     "are identical &mdash; the same variables raised to the same "
                     "exponents. `5x²y` and `−2x²y` are like terms; `5x²y` and `5xy²` "
                     "are not.")),
            ("p", "The coefficients play no part in deciding. `100x³` and `x³` are like "
                  "terms; `x³` and `x²` are not, however close the exponents look."),
            ("thm", ("Why like terms combine",
                     "For any number `a`, `b` and any whole number `n`, "
                     "`axⁿ + bxⁿ = (a + b)xⁿ`.",
                     "This is the distributive law `ac + bc = (a + b)c` with `c = xⁿ`. It "
                     "is not a special rule about polynomials, and that is exactly why it "
                     "is safe.")),
            ("p", "Turn the theorem around and you can see why `x² + x³` cannot be "
                  "collected: there is no common `c` to pull out other than `x²`, and "
                  "pulling that out gives `x²(1 + x)` &mdash; a product, not a shorter "
                  "sum. It is a legitimate move, and it is factoring, which starts in "
                  "lesson 5. It just is not addition."),
            ("h3", "Subtraction"),
            ("p", "Subtracting a polynomial means adding its negative, and the negative "
                  "of a polynomial has <em>every</em> sign flipped:"),
            ("math", [
                "−(x² − 5x − 2)  =  −x² + 5x + 2",
                "",
                "         not     −x² − 5x − 2",
            ]),
            ("p", "The left-hand form is the distributive law with `−1`: "
                  "`−1 · (x² − 5x − 2) = (−1)x² + (−1)(−5x) + (−1)(−2)`. Nothing is being "
                  "remembered here; every sign is computed."),
            ("p", "The safest habit is to write the negated polynomial out as its own line "
                  "before adding anything. It costs one line and removes the error class "
                  "entirely."),
            ("h3", "What happens to the degree"),
            ("p", "The degree of a sum is <em>at most</em> the larger of the two degrees. "
                  "Usually it equals it &mdash; but if the leading terms cancel, the "
                  "degree drops:"),
            ("math", [
                "(5x⁴ − 2x² + x) + (−5x⁴ + 2x² + 3)  =  x + 3",
                "",
                "degree 4  +  degree 4   →   degree 1",
            ]),
            ("p", "This is why lesson 1 insisted that degree is read after combining. "
                  "Addition can lower a degree; it can never raise one."),
            ("example", ("Adding in one line",
                         "`(3x³ − 5x + 2) + (x³ + 4x² − 5)`. The `x³` terms give `4x³`; "
                         "there is only one `x²` term, `4x²`; only one `x` term, `−5x`; "
                         "the constants give `2 − 5 = −3`. Result: "
                         "`4x³ + 4x² − 5x − 3`.")),
        ],
        "lab": ("polynomial", {
            "mode": "arith",
            "panel_title": "Add or subtract two polynomials",
            "panel_intro": "Enter two polynomials and pick the operation. The lab shows the "
                           "negated second polynomial as its own line before it collects, "
                           "which is the step worth copying.",
        }),
        "steps_title": "Adding or subtracting, without sign errors",
        "steps_intro": "For subtraction, step 1 is the whole battle.",
        "steps": [
            ("If it is a subtraction, negate the second polynomial first",
             "Write `−(…)` out in full with every sign flipped, on its own line, before "
             "you collect anything. Then the problem is an addition and stays one."),
            ("Put both polynomials in standard form",
             "Descending degree, both of them. Like terms then line up in columns and you "
             "can see at a glance which powers are present."),
            ("Collect one power at a time, highest first",
             "Take all the `x³` terms, then all the `x²` terms, and so on. Working by "
             "power rather than left to right is what stops a term being used twice or "
             "skipped."),
            ("Read the degree off the answer, not off the inputs",
             "If the leading terms cancelled, the answer has a lower degree than either "
             "input. That is a legitimate result, not a mistake."),
        ],
        "worked": {
            "title": "One subtraction, in full",
            "intro": ["`(4x² − 3x + 6) − (x² − 5x − 2)`, with the negation written out."],
            "lines": [
                "step 1   negate the second polynomial",
                "         −(x² − 5x − 2)  =  −x² + 5x + 2",
                "",
                "step 2   now it is an addition",
                "         (4x² − 3x + 6) + (−x² + 5x + 2)",
                "",
                "step 3   collect by power",
                "         x² :   4 + (−1)  =  3     →   3x²",
                "         x  :  −3 + 5     =  2     →   2x",
                "         1  :   6 + 2     =  8     →   8",
                "",
                "answer   3x² + 2x + 8",
            ],
            "after": [
                "The two signs that flipped were on `−5x` and `−2`, and both became "
                "positive. Skipping step 1 and writing `4x² − 3x + 6 − x² − 5x − 2` gives "
                "`3x² − 8x + 4`: a tidy-looking answer, and wrong in two places.",
                "Check any result by substituting a number into the original and into the "
                "answer. At `x = 1` the original is `7 − (−6) = 13`, and the answer is "
                "`3 + 2 + 8 = 13`. One substitution catches nearly every sign error.",
            ],
        },
        "quiz_title": "Collect and subtract",
        "quiz": [
            {"q": "Simplify `(2x³ + x) + (x³ − 4x + 5)`.",
             "a": ["`3x³ − 3x + 5`", "`3x⁶ − 3x + 5`", "`2x³ − 3x + 5`", "`3x³ + 5x + 5`"],
             "c": 0,
             "why": "`2x³ + x³ = 3x³` &mdash; the coefficients add and the exponent is "
                    "untouched, because `axⁿ + bxⁿ = (a + b)xⁿ`. Then `x − 4x = −3x`."},
            {"q": "Simplify `(x² + 2x − 1) − (3x² − 2x + 4)`.",
             "a": ["`−2x² + 4x − 5`", "`−2x² + 4x + 3`", "`−2x² + 0x + 3`", "`4x² + 4x − 5`"],
             "c": 0,
             "why": "Negating gives `−3x² + 2x − 4`. Then `1 − 3 = −2`, `2 + 2 = 4`, and "
                    "`−1 − 4 = −5`. The distractors each keep one sign from the original "
                    "second polynomial."},
            {"q": "Both polynomials have degree 5. What can you say about the degree of their sum?",
             "a": ["It is exactly 5", "It is 10", "It is at most 5", "It is at least 5"],
             "c": 2,
             "why": "Usually 5, but if the two `x⁵` terms cancel the degree drops &mdash; "
                    "possibly a long way. Addition can never raise the degree, so 5 is a "
                    "ceiling, not a value."},
        ],
        "mistakes": [
            ("Distributing the minus sign to the first term only",
             "`A − (B + C)` is `A − B − C`. This single error accounts for more wrong "
             "answers than every other mistake in the course combined, which is why the "
             "negation deserves its own line."),
            ("Adding the exponents when adding like terms",
             "`3x² + 5x² = 8x²`, not `8x⁴`. Exponents add when terms are "
             "<em>multiplied</em> &mdash; that is lesson 3, and mixing the two rules is "
             "easy once both are in your hands."),
            ("Forcing unlike terms together",
             "`x² + x³` is finished; it is not `x⁵` and not `2x⁵`. If the variable parts "
             "differ at all, the sum is already as short as it gets."),
        ],
        "standard": ("Finish when a subtraction is as safe for you as an addition.",
                     "You should be able to take a difference of two quartics and get "
                     "every sign right first time, because you write the negation on its "
                     "own line rather than doing it in your head. Substituting `x = 1` "
                     "into both the question and your answer should be automatic."),
        "note": "The `x = 1` check is worth making a habit now. It costs seconds, it "
                "catches sign errors and dropped terms, and it is the same idea &mdash; "
                "evaluating a polynomial at a number &mdash; that becomes the remainder "
                "theorem in lesson 11.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "multiplying-polynomials",
        "title": "Multiplying Polynomials",
        "module": "Polynomial arithmetic",
        "one_line": "Every term times every term, then collect.",
        "summary": (
            "One rule covers every polynomial product: distribute until no brackets "
            "remain. FOIL is that rule applied to two binomials and is not worth "
            "memorising as a separate fact."
        ),
        "key": [
            "xᵐ · xⁿ  =  xᵐ⁺ⁿ                exponents ADD when multiplying",
            "",
            "(a + b)(c + d)  =  ac + ad + bc + bd",
            "",
            "m terms × n terms  →  mn products, before collecting",
        ],
        "key_label": "Distribution, and the count it produces",
        "concepts_intro": (
            "Multiplication looks harder than addition and involves one more idea. It is "
            "also more mechanical: there is nothing to decide."
        ),
        "concepts": [
            ("Coefficients multiply, exponents add",
             "`(3x²)(4x⁵) = 12x⁷`. The coefficients are just numbers, so they multiply. "
             "The powers add because `x²·x⁵` is two `x`s times five `x`s &mdash; seven "
             "`x`s. That is course 1's exponent law, unchanged."),
            ("The distributive law is the entire method",
             "Multiply each term of the first polynomial by each term of the second, then "
             "collect like terms. Every layout &mdash; FOIL, the grid, the vertical "
             "arrangement &mdash; is bookkeeping for that one instruction."),
            ("The product's degree is the sum of the degrees",
             "Degree 3 times degree 4 gives degree 7, always. The leading terms multiply "
             "to give the leading term, and two nonzero numbers cannot multiply to zero, "
             "so it can never cancel away."),
        ],
        "read_title": "Multiplying, from one term to many",
        "read_intro": "Monomials first, then the general rule, then how to keep track of the pieces.",
        "body": [
            ("h3", "A single term times a single term"),
            ("p", "Multiply the coefficients; add the exponents of each variable "
                  "separately."),
            ("math", [
                "(3x²)(4x⁵)     =  12x⁷",
                "(−2x³y)(5xy⁴)  =  −10x⁴y⁵",
            ]),
            ("p", "In the second line the `x` exponents give `3 + 1 = 4` and the `y` "
                  "exponents give `1 + 4 = 5`. Each variable is tracked on its own; they "
                  "never mix."),
            ("h3", "A term times a polynomial"),
            ("p", "This is the distributive law directly: `a(b + c) = ab + ac`, with as "
                  "many terms inside the bracket as you like."),
            ("math", [
                "3x(2x² − 5x + 4)  =  6x³ − 15x² + 12x",
            ]),
            ("p", "The `3x` reaches every term inside the bracket &mdash; the same "
                  "\"reaches every term\" discipline as the minus sign in lesson 2."),
            ("h3", "A polynomial times a polynomial"),
            ("thm", ("The general product",
                     "To multiply two polynomials, multiply each term of the first by each "
                     "term of the second and add all the results.",
                     "A polynomial with `m` terms times one with `n` terms produces `mn` "
                     "products before any collecting. Counting them first tells you when "
                     "you have finished.")),
            ("p", "For two binomials that count is `2 × 2 = 4`, and the four products are "
                  "traditionally remembered as <strong>FOIL</strong> &mdash; First, "
                  "Outer, Inner, Last:"),
            ("math", [
                "(x + 4)(x − 7)",
                "",
                "  First   x · x    =   x²",
                "  Outer   x ·(−7)  =  −7x",
                "  Inner   4 · x    =   4x",
                "  Last    4 ·(−7)  = −28",
                "",
                "  collect          =   x² − 3x − 28",
            ]),
            ("p", "FOIL is worth knowing as a memory aid and worth distrusting as a "
                  "method, because it describes only the `2 × 2` case. Asked for "
                  "`(2x − 3)(x² + 4x − 5)` there is no \"outer\" and \"inner\" to speak of "
                  "&mdash; there are `2 × 3 = 6` products. The counting rule survives "
                  "where the acronym does not."),
            ("h3", "Keeping track"),
            ("p", "Take the terms of the first polynomial one at a time and distribute "
                  "each across the whole second polynomial. Write each partial product on "
                  "its own line, then collect down the columns. Six products written on "
                  "two lines are far easier to check than six products written in a row."),
            ("example", ("Degree, predicted",
                         "`(2x − 3)(x² + 4x − 5)` has degree `1 + 2 = 3`, and its leading "
                         "term is `2x · x² = 2x³` before you multiply anything else. If "
                         "your answer is not a cubic starting `2x³`, something went wrong "
                         "&mdash; and you know it without checking the rest.")),
        ],
        "lab": ("polynomial", {
            "mode": "multiply",
            "panel_title": "Multiply two polynomials",
            "panel_intro": "The lab lists every partial product before collecting, so the "
                           "`mn` count is visible. Multiply a trinomial by a trinomial and "
                           "count the nine products.",
        }),
        "steps_title": "Multiplying two polynomials",
        "steps_intro": "Predict the shape of the answer first; it makes the check free.",
        "steps": [
            ("Predict the degree and the leading term",
             "Add the degrees; multiply the leading coefficients. You now know the first "
             "term of the answer before doing any work, and you will know immediately if "
             "the result is malformed."),
            ("Count the products you owe",
             "`m` terms times `n` terms is `mn` products. Write the number down. Missing "
             "one term is the second most common error here, and a count catches it."),
            ("Distribute one term at a time, on its own line",
             "Take the first term of the first polynomial across the whole of the second, "
             "then the next. Never work two terms at once in your head."),
            ("Collect like terms and put the answer in standard form",
             "Collect by power, highest first, exactly as in lesson 2. Then check the "
             "leading term against your prediction from step 1."),
        ],
        "worked": {
            "title": "A binomial times a trinomial",
            "intro": ["`(2x − 3)(x² + 4x − 5)`. Degree `1 + 2 = 3`; leading term `2x³`; "
                      "`2 × 3 = 6` products owed."],
            "lines": [
                "2x  across the trinomial:",
                "        2x · x²   =  2x³",
                "        2x · 4x   =  8x²",
                "        2x ·(−5)  = −10x",
                "",
                "−3  across the trinomial:",
                "       −3 · x²    = −3x²",
                "       −3 · 4x    = −12x",
                "       −3 ·(−5)   = +15",
                "",
                "collect:  2x³ + (8 − 3)x² + (−10 − 12)x + 15",
                "",
                "answer    2x³ + 5x² − 22x + 15",
            ],
            "after": [
                "Six products written, six products owed. The leading term is `2x³` as "
                "predicted, and the constant term is `(−3)(−5) = 15` &mdash; which is "
                "always just the product of the two constant terms, another free check.",
                "At `x = 1`: the factors give `(2 − 3)(1 + 4 − 5) = (−1)(0) = 0`, and the "
                "answer gives `2 + 5 − 22 + 15 = 0`. Agreement.",
            ],
        },
        "quiz_title": "Products",
        "quiz": [
            {"q": "Simplify `(3x²)(4x⁵)`.",
             "a": ["`12x¹⁰`", "`12x⁷`", "`7x⁷`", "`12x³`"],
             "c": 1,
             "why": "Coefficients multiply: `3 × 4 = 12`. Exponents add: `2 + 5 = 7`. "
                    "Multiplying the exponents gives `x¹⁰` and is the standard confusion; "
                    "adding the coefficients gives `7x⁷`."},
            {"q": "Expand `(3x + 2)(2x − 5)`.",
             "a": ["`6x² − 10`", "`6x² − 11x − 10`", "`6x² + 11x − 10`", "`6x² − 19x − 10`"],
             "c": 1,
             "why": "The four products are `6x²`, `−15x`, `+4x`, `−10`, and "
                    "`−15x + 4x = −11x`. The first option keeps only First and Last, which "
                    "is what forgetting the middle terms looks like."},
            {"q": "How many products before collecting, for a trinomial times a four-term polynomial?",
             "a": ["7", "12", "9", "It depends on the coefficients"],
             "c": 1,
             "why": "`3 × 4 = 12`. Every term of the first meets every term of the second, "
                    "and the coefficients have nothing to do with it &mdash; they affect "
                    "how many survive collecting, not how many are produced."},
        ],
        "mistakes": [
            ("Multiplying the exponents instead of adding them",
             "`x²·x⁵ = x⁷`, not `x¹⁰`. Multiplying exponents is the rule for a power of a "
             "power, `(x²)⁵ = x¹⁰`, and the two get swapped under pressure."),
            ("Trusting FOIL beyond two binomials",
             "FOIL names the four products of a `2 × 2` case. For anything larger it "
             "quietly suggests you are finished when you are not. Count `mn` instead."),
            ("Forgetting to collect after distributing",
             "`(x + 4)(x − 7)` is not `x² − 7x + 4x − 28` as a final answer. The middle "
             "terms are like terms and must be combined: `x² − 3x − 28`."),
        ],
        "standard": ("Finish when you can state the degree and leading term before you multiply.",
                     "For any product you should be able to say the degree, the leading "
                     "term, the constant term and the number of partial products before "
                     "writing a line of working &mdash; and then use all four to check the "
                     "result. That is what makes lesson 5 onward, where you run this "
                     "process backwards, feel like a search rather than a guess."),
        "note": "Everything from here to lesson 9 is this lesson in reverse. Factoring is "
                "asking which two polynomials would multiply to give the one in front of "
                "you, so the fluency you build expanding is exactly the fluency that makes "
                "factoring checkable.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "special-products",
        "title": "Special Products",
        "module": "Polynomial arithmetic",
        "one_line": "Four patterns worth recognising instead of expanding.",
        "summary": (
            "The difference of squares, the two square-of-a-binomial forms and the cube "
            "patterns are ordinary products of lesson 3. They are singled out because "
            "each one runs backwards in lesson 9, where recognition is the whole method."
        ),
        "key": [
            "(a + b)(a − b)  =  a² − b²",
            "(a + b)²        =  a² + 2ab + b²",
            "(a − b)²        =  a² − 2ab + b²",
            "",
            "(a + b)(a² − ab + b²)  =  a³ + b³",
            "(a − b)(a² + ab + b²)  =  a³ − b³",
        ],
        "key_label": "The patterns, forwards",
        "concepts_intro": (
            "Nothing here is new mathematics. What is new is reading a product backwards "
            "&mdash; seeing `9x² − 25` and thinking \"difference of squares\" rather than "
            "\"a quadratic\"."
        ),
        "concepts": [
            ("These are theorems, not conventions",
             "Each identity is proved in one line by distributing. If you ever doubt a "
             "sign, expand it &mdash; the derivation is shorter than the doubt."),
            ("The middle term is the whole difficulty",
             "`(a + b)²` is `a² + 2ab + b²`, not `a² + b²`. Squaring distributes over "
             "multiplication but never over addition, and this is the error that survives "
             "longest into later courses."),
            ("Recognition is what you are training",
             "`a` and `b` stand for whole expressions, not just letters. In `(3x + 5)"
             "(3x − 5)` you have `a = 3x` and `b = 5`, and the answer `9x² − 25` needs no "
             "working at all."),
        ],
        "read_title": "The patterns and where they come from",
        "read_intro": "Each derived once, then read as a shape you can spot.",
        "body": [
            ("thm", ("Difference of squares",
                     "`(a + b)(a − b) = a² − b²` for all `a` and `b`.")),
            ("proof", [
                "Distribute the four products: `(a + b)(a − b) = a² − ab + ba − b²`.",
                "The middle terms `−ab` and `+ba` are like terms with opposite signs, so "
                "they sum to zero, leaving `a² − b²`.",
            ]),
            ("p", "The cancellation of the middle is the entire content. It happens "
                  "because the two brackets differ only in one sign, which is why the "
                  "pattern is worth naming: three terms collapse to two."),
            ("thm", ("Square of a binomial",
                     "`(a + b)² = a² + 2ab + b²` and `(a − b)² = a² − 2ab + b²`.")),
            ("proof", [
                "`(a + b)² = (a + b)(a + b) = a² + ab + ba + b² = a² + 2ab + b²`.",
                "For the second, replace `b` by `−b`: the `b²` term is unchanged because "
                "`(−b)² = b²`, and the middle term becomes `−2ab`.",
            ]),
            ("p", "So the two forms are one result. The last term is <em>always</em> "
                  "positive &mdash; it is a square &mdash; and only the middle sign "
                  "follows the sign in the bracket."),
            ("p", "The claim `(a + b)² = a² + b²` is false, and one number settles it: at "
                  "`a = 1, b = 3` the left side is `(1 + 3)² = 16` and the right side is "
                  "`1 + 9 = 10`. Whenever you are unsure of an algebraic identity, test it "
                  "on small numbers. A single counterexample is a complete disproof."),
            ("h3", "The cube patterns"),
            ("p", "Two more, used in lesson 9 and rarely anywhere else:"),
            ("math", [
                "(a + b)(a² − ab + b²)  =  a³ + b³",
                "(a − b)(a² + ab + b²)  =  a³ − b³",
            ]),
            ("proof", [
                "For the first: distributing gives "
                "`a³ − a²b + ab² + a²b − ab² + b³`. The `a²b` terms cancel and the `ab²` "
                "terms cancel, leaving `a³ + b³`. The second is the same computation with "
                "`b` replaced by `−b`.",
            ]),
            ("p", "Note the signs, because they are counter-intuitive: the binomial "
                  "carries the same sign as the answer, and the middle term of the "
                  "trinomial carries the opposite one. The trinomial factor is "
                  "<em>not</em> a perfect square &mdash; it has `ab`, not `2ab`."),
            ("p", "Also worth having: `(a + b)³ = a³ + 3a²b + 3ab² + b³`, which is what "
                  "you get by multiplying `(a + b)²` by `(a + b)` once more."),
            ("example", ("Recognition in practice",
                         "`(3x + 5)(3x − 5)`: same terms, opposite signs, so it is a "
                         "difference of squares with `a = 3x`, `b = 5`, giving "
                         "`9x² − 25`. `(2x − 7)²`: a square of a binomial with `a = 2x`, "
                         "`b = 7`, giving `4x² − 28x + 49` &mdash; the middle term is "
                         "`2·(2x)·7 = 28x`, subtracted.")),
        ],
        "lab": ("polynomial", {
            "mode": "special",
            "panel_title": "The patterns, both directions",
            "panel_intro": "Pick a pattern and choose `a` and `b`. The lab expands it in "
                           "full so you can watch which middle terms cancel and which "
                           "double.",
        }),
        "steps_title": "Spotting a special product",
        "steps_intro": "Three questions. If all three fail, expand it the ordinary way.",
        "steps": [
            ("Are the two brackets identical except for one sign?",
             "If so it is a difference of squares: square the first term, square the "
             "second, subtract. The middle vanishes."),
            ("Is it a bracket squared?",
             "Then it is `a² ± 2ab + b²`. Identify `a` and `b`, and remember the middle "
             "term is <em>twice</em> their product &mdash; that factor of 2 is the part "
             "people drop."),
            ("Is it a binomial times a trinomial with no doubled middle term?",
             "Check for the cube pattern: `a² ∓ ab + b²` alongside `a ± b`. If the "
             "trinomial has `2ab` rather than `ab`, it is not this pattern."),
            ("Otherwise, distribute",
             "The patterns are shortcuts, not obligations. An ordinary product expanded "
             "carefully is always right; a pattern applied to something that does not "
             "match never is."),
        ],
        "worked": {
            "title": "Four products, by pattern",
            "intro": ["Each one names its pattern first, and only then substitutes."],
            "lines": [
                "1.  (3x + 5)(3x − 5)      difference of squares, a = 3x, b = 5",
                "        =  (3x)² − 5²  =  9x² − 25",
                "",
                "2.  (2x − 7)²             square of a binomial, a = 2x, b = 7",
                "        =  (2x)² − 2(2x)(7) + 7²  =  4x² − 28x + 49",
                "",
                "3.  (x + 3)²              a = x, b = 3",
                "        =  x² + 6x + 9        NOT x² + 9",
                "        check at x = 1:   (1 + 3)² = 16,  and  1 + 6 + 9 = 16",
                "",
                "4.  (x + 2)(x² − 2x + 4)  sum of cubes, a = x, b = 2",
                "        =  x³ + 8",
            ],
            "after": [
                "Line 3 is the one to fix in memory. The two sides of the false identity "
                "differ by `6x`, and at `x = 1` that is the difference between 16 and 10.",
                "Line 4 is worth expanding by hand once, to watch the four middle terms "
                "annihilate each other. After that you can use it as a pattern with a "
                "clear conscience.",
            ],
        },
        "quiz_title": "Patterns",
        "quiz": [
            {"q": "Expand `(4x − 3)(4x + 3)`.",
             "a": ["`16x² − 9`", "`16x² + 9`", "`16x² − 24x − 9`", "`16x² − 12x − 9`"],
             "c": 0,
             "why": "Same terms, opposite signs: a difference of squares. `(4x)² = 16x²` "
                    "and `3² = 9`, subtracted. The middle terms `+12x` and `−12x` cancel, "
                    "which is exactly what the pattern is for."},
            {"q": "Expand `(x + 5)²`.",
             "a": ["`x² + 25`", "`x² + 5x + 25`", "`x² + 10x + 25`", "`x² + 10x + 10`"],
             "c": 2,
             "why": "The middle term is `2ab = 2·x·5 = 10x`. Testing at `x = 1` separates "
                    "the options at once: the true value is `36`, and only "
                    "`1 + 10 + 25` gives it."},
            {"q": "Which product is NOT a difference of squares?",
             "a": ["`(x − 6)(x + 6)`", "`(2y + 1)(2y − 1)`", "`(x + 4)(x + 4)`",
                   "`(5 − x)(5 + x)`"],
             "c": 2,
             "why": "The pattern needs the two brackets to differ in exactly one sign. "
                    "`(x + 4)(x + 4)` is `(x + 4)²`, a square of a binomial, giving "
                    "`x² + 8x + 16` &mdash; with a middle term that does not cancel."},
        ],
        "mistakes": [
            ("Writing `(a + b)² = a² + b²`",
             "The missing `2ab` is the most persistent error in school algebra. Squaring "
             "does not distribute over addition, and one numerical test exposes it every "
             "time."),
            ("Halving or dropping the 2 in the middle term",
             "`(2x − 7)²` has middle term `2·(2x)·7 = 28x`, not `14x`. Both `a` and `b` "
             "go in, and so does the 2."),
            ("Expecting `a² + ab + b²` to be a perfect square",
             "It is not: the square has `2ab`. The trinomial in the cube patterns is "
             "deliberately not a perfect square, and treating it as one sends you looking "
             "for a factorisation that is not there."),
        ],
        "standard": ("Finish when you produce `9x² − 25` without writing a middle term at all.",
                     "Recognition should be immediate in both directions: given "
                     "`(3x + 5)(3x − 5)` you write `9x² − 25`, and given `9x² − 25` you "
                     "should already be uneasy that it factors. Lesson 9 turns that unease "
                     "into a method."),
        "note": "These five identities are the only things in the course worth committing "
                "to memory, and even they can be re-derived in a line. Everything else "
                "&mdash; every factorisation from here on &mdash; is produced by a search "
                "you can carry out, not by a fact you must recall.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "factoring-out-the-greatest-common-factor",
        "title": "Factoring Out the Greatest Common Factor",
        "module": "Factoring",
        "one_line": "The first move on every factoring problem, without exception.",
        "summary": (
            "Factoring is the distributive law read right to left. The greatest common "
            "factor is what every term shares &mdash; the gcd of the coefficients and the "
            "lowest power of each common variable &mdash; and taking it out first is what "
            "keeps every later technique usable."
        ),
        "key": [
            "ab + ac  =  a(b + c)          the distributive law, backwards",
            "",
            "GCF  =  gcd of the coefficients  ×  lowest power of each common variable",
            "",
            "12x⁴y − 18x³y² + 6x³y  =  6x³y(2x − 3y + 1)",
        ],
        "key_label": "One law, one recipe",
        "concepts_intro": (
            "Factoring asks a different kind of question from anything so far: not "
            "\"what does this equal\" but \"what would multiply to give this\". The answer "
            "is a product, and it is checkable in seconds."
        ),
        "concepts": [
            ("Factoring is multiplication in reverse",
             "Every factorisation can be verified by expanding it. This is the only topic "
             "on the path where checking your answer is faster than producing it, so "
             "there is never a reason to submit an unchecked one."),
            ("The GCF must divide EVERY term",
             "Not most of them. A factor shared by two terms out of three is not a common "
             "factor of the polynomial, and pulling it out anyway leaves a fraction "
             "behind."),
            ("Take it out first, always",
             "Every technique in lessons 6 to 9 assumes the easy factor is gone. Skipping "
             "this step is what turns a one-line problem into a trinomial with coefficients "
             "too large to search sensibly."),
        ],
        "read_title": "Finding what every term shares",
        "read_intro": "What factoring means, how the GCF is computed, and the two details that go wrong.",
        "body": [
            ("def", ("Factoring",
                     "To <strong>factor</strong> a polynomial is to write it as a product "
                     "of two or more polynomials. A factorisation is "
                     "<strong>complete</strong> when no factor can be factored further.",
                     "`x² + 5x` factors as `x(x + 5)`. The result is not simpler to look "
                     "at &mdash; it is more useful, because a product tells you when the "
                     "whole thing is zero, and a sum does not.")),
            ("p", "The licence is the distributive law, `ab + ac = a(b + c)`, used from "
                  "right to left. Nothing else is happening, and nothing else is needed."),
            ("def", ("Greatest common factor",
                     "The <strong>GCF</strong> of a set of terms is the largest monomial "
                     "that divides all of them. Its coefficient is the greatest common "
                     "divisor of the coefficients, and each variable appears to the "
                     "<em>lowest</em> power with which it appears in every term.",
                     "A variable that is missing from even one term is missing from the "
                     "GCF entirely.")),
            ("p", "Take `12x⁴y − 18x³y² + 6x³y`. The coefficients are `12`, `18`, `6`, "
                  "whose gcd is `6`. Every term has an `x`, to powers `4`, `3`, `3`, so "
                  "`x³` is shared. Every term has a `y`, to powers `1`, `2`, `1`, so `y` "
                  "is shared. The GCF is `6x³y`."),
            ("p", "The word <em>lowest</em> is the one to hold on to. `x³` is common "
                  "because a term with only three `x`s cannot supply four; the shared part "
                  "is limited by the poorest term, exactly as it is with the coefficients."),
            ("h3", "The term that leaves a 1 behind"),
            ("p", "When a term <em>is</em> the GCF, dividing it by the GCF leaves `1`, and "
                  "that `1` must be written:"),
            ("math", [
                "5x² + 5x  =  5x(x + 1)          not  5x(x)",
                "",
                "12x⁴y − 18x³y² + 6x³y  =  6x³y(2x − 3y + 1)",
            ]),
            ("p", "Dropping the `1` changes the polynomial. Expand `5x(x)` and you get "
                  "`5x²`, which is not what you started with &mdash; and the expansion "
                  "check catches it immediately."),
            ("h3", "Factoring out a negative"),
            ("p", "When the leading coefficient is negative it is usually worth taking the "
                  "minus sign out with the GCF, because the techniques in the next lessons "
                  "are stated for a positive leading term:"),
            ("math", [
                "−4x³ + 8x² − 12x  =  −4x(x² − 2x + 3)",
            ]),
            ("p", "Every sign inside the bracket flips, for the same reason as in "
                  "lesson 2. Check by expanding: `−4x · x² = −4x³`, `−4x · (−2x) = +8x²`, "
                  "`−4x · 3 = −12x`. Correct."),
            ("thm", ("Why \"greatest\" matters",
                     "If you factor out a common factor that is not the greatest, the "
                     "remaining bracket still contains a common factor.",
                     "`12x² + 18x = 2x(6x + 9)` is a true statement and an incomplete "
                     "factorisation: `6x + 9` still has a `3` in it. The full answer is "
                     "`6x(2x + 3)`.")),
            ("example", ("A factor that is not common",
                         "In `6x³ + 9x² + 4x` the coefficients `6`, `9`, `4` have gcd `1`, "
                         "and although two terms carry `x²` the third has only `x`. The GCF "
                         "is `x`, giving `x(6x² + 9x + 4)` &mdash; and no more. Seeing "
                         "`6` and `9` and pulling out a `3` would leave `4/3`, which is "
                         "not a polynomial coefficient the technique allows.")),
        ],
        "lab": ("factoring", {
            "mode": "gcf",
            "panel_title": "The decision list starts here",
            "panel_intro": "Type any polynomial. The lab computes the gcd of the "
                           "coefficients and the lowest power of each variable, shows the "
                           "GCF it found, and expands the result back to prove it.",
        }),
        "steps_title": "Taking out the greatest common factor",
        "steps_intro": "Coefficients and variables are handled separately, then combined.",
        "steps": [
            ("Find the gcd of the coefficients",
             "Ignore the variables entirely and take the greatest common divisor of the "
             "numbers, signs aside. If it is 1, the GCF has no numerical part."),
            ("For each variable, take the lowest power that appears in every term",
             "Every term, not most terms. A variable absent from one term does not appear "
             "in the GCF at all."),
            ("Divide each term by the GCF to get the bracket",
             "Term by term. Where a term equals the GCF exactly, the quotient is `1` and "
             "you write it. The bracket must have as many terms as the original."),
            ("Expand to check, then keep going",
             "Multiply back out; it must reproduce the original exactly. Then look at the "
             "bracket &mdash; the GCF is the first step of the decision list, not the last, "
             "and what remains is usually factorable further."),
        ],
        "worked": {
            "title": "A three-term GCF, in full",
            "intro": ["`12x⁴y − 18x³y² + 6x³y`. Coefficients, then `x`, then `y`."],
            "lines": [
                "coefficients   gcd(12, 18, 6)  =  6",
                "x              powers 4, 3, 3   →  lowest is x³",
                "y              powers 1, 2, 1   →  lowest is y",
                "GCF            6x³y",
                "",
                "divide each term by 6x³y:",
                "        12x⁴y   / 6x³y  =   2x",
                "       −18x³y²  / 6x³y  =  −3y",
                "         6x³y   / 6x³y  =   1        <-- write the 1",
                "",
                "answer   6x³y(2x − 3y + 1)",
                "",
                "check    6x³y·2x = 12x⁴y",
                "         6x³y·(−3y) = −18x³y²",
                "         6x³y·1 = 6x³y                 all three match",
            ],
            "after": [
                "Three terms in, three terms in the bracket. That count is the fastest "
                "check that nothing was dropped, and the third term &mdash; the `1` "
                "&mdash; is the one at risk.",
                "Had the `y` been missing from any single term, the GCF would have been "
                "`6x³` and the bracket would have carried the `y`s instead. The poorest "
                "term always decides.",
            ],
        },
        "quiz_title": "Common factors",
        "quiz": [
            {"q": "Factor `8x³ + 12x²`.",
             "a": ["`4x²(2x + 3)`", "`2x²(4x + 6)`", "`4x³(2 + 3x)`", "`4x²(2x + 3x)`"],
             "c": 0,
             "why": "`gcd(8, 12) = 4` and the lowest power of `x` is `x²`. The second "
                    "option is true but incomplete &mdash; `4x + 6` still has a common `2`, "
                    "which is what \"greatest\" rules out."},
            {"q": "Factor `7x² + 7x`.",
             "a": ["`7x(x)`", "`7x(x + 1)`", "`7x²(1 + x)`", "`7(x² + x)`"],
             "c": 1,
             "why": "Dividing `7x` by the GCF `7x` gives `1`, and it must be written. "
                    "Expanding `7x(x)` gives `7x²`, which is missing a whole term. The "
                    "last option is true but has not taken out the `x`."},
            {"q": "What is the GCF of `10x³y`, `15x²`, and `25x²y²`?",
             "a": ["`5x²y`", "`5x³y²`", "`5x²`", "`x²`"],
             "c": 2,
             "why": "`gcd(10, 15, 25) = 5`, and the lowest power of `x` is `x²`. There is "
                    "no `y` in `15x²`, so `y` cannot appear in a factor common to all "
                    "three."},
        ],
        "mistakes": [
            ("Dropping the 1 when a term is the GCF",
             "`5x² + 5x = 5x(x + 1)`. Writing `5x(x)` silently deletes a term, and the "
             "expansion check finds it in one line."),
            ("Taking out a factor that is missing from one term",
             "A variable or number must divide <em>every</em> term, and the two cases "
             "fail differently. Pulling `x²` out of `6x³ + 9x² + 4x` leaves "
             "`6x + 9 + 4x⁻¹`, whose negative exponent makes the bracket not a "
             "polynomial. Pulling a `3` out of the same polynomial leaves "
             "`2x³ + 3x² + (4/3)x`, which <em>is</em> a polynomial &mdash; "
             "coefficients may be any numbers &mdash; so the signal there is narrower: "
             "the `4/3` is a coefficient outside the integers, which is not one the "
             "technique allows."),
            ("Stopping at a common factor that is not the greatest",
             "`12x² + 18x = 2x(6x + 9)` leaves a `3` inside. Always look at the bracket "
             "after the step and ask whether it still has something in common."),
        ],
        "standard": ("Finish when the GCF is automatic and the bracket is always checked.",
                     "Given any polynomial you should take the GCF out without thinking "
                     "about it, keep the term count right, and then look at what remains "
                     "and ask which technique comes next. Lessons 6 to 9 all begin from "
                     "the bracket this step produces."),
        "note": "The lab puts this first in its decision list for a reason worth stating "
                "plainly: a trinomial like `6x² + 15x + 6` looks like hard work until the "
                "`3` comes out and leaves `2x² + 5x + 2`. The same problem, with a search "
                "space several times smaller.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "factoring-by-grouping",
        "title": "Factoring by Grouping",
        "module": "Factoring",
        "one_line": "Four terms, two pairs, one shared bracket.",
        "summary": (
            "With four terms and no common factor, split into pairs, take the GCF out of "
            "each, and hope the same binomial is left behind. What makes the method work "
            "is that the shared binomial is itself a common factor."
        ),
        "key": [
            "x³ + 3x² − 4x − 12",
            "  =  x²(x + 3) − 4(x + 3)        both pairs leave (x + 3)",
            "  =  (x + 3)(x² − 4)             the binomial is the common factor",
            "  =  (x + 3)(x − 2)(x + 2)       keep going until nothing factors",
        ],
        "key_label": "The method in four lines",
        "concepts_intro": (
            "Grouping is the first technique with a condition attached. It applies when "
            "the pairs cooperate, and knowing when they do not is as important as the "
            "method itself."
        ),
        "concepts": [
            ("The shared binomial is an ordinary common factor",
             "After the first step you have `x²·P − 4·P` with `P = (x + 3)`. That is "
             "`ab + ac` again, with `a = P`. Nothing new is being assumed &mdash; the "
             "common factor just happens to be a bracket."),
            ("It only works if BOTH pairs leave the same binomial",
             "If one pair leaves `(x + 3)` and the other `(x − 3)`, there is no common "
             "factor and the step has failed. You may not adjust one of them to match; "
             "you regroup, or you conclude this technique does not apply."),
            ("Failure of the method is not failure to factor",
             "If no pairing works, all you have learned is that grouping did not crack "
             "it. Whether the polynomial factors at all is settled by the root theorems in "
             "lessons 11 and 12, not here."),
        ],
        "read_title": "Pairing terms so a common factor appears",
        "read_intro": "The method, the sign trap in the second pair, and what to do when the brackets disagree.",
        "body": [
            ("p", "Grouping is the standard move for four terms. Take the GCF out of the "
                  "first two and out of the last two, and if the same binomial is left in "
                  "both places, take <em>that</em> out."),
            ("math", [
                "x³ + 3x² − 4x − 12",
                "",
                "  (x³ + 3x²)  +  (−4x − 12)      pair them",
                "   x²(x + 3)  +  (−4)(x + 3)     GCF of each pair",
                "   (x + 3)(x² − 4)               (x + 3) is common",
            ]),
            ("thm", ("Why the last step is legal",
                     "For any polynomials `A`, `B` and `P`, `A·P + B·P = (A + B)·P`.",
                     "This is the distributive law with the common factor `P` a binomial "
                     "rather than a monomial. The law never cared what `P` was.")),
            ("h3", "The sign in the second pair"),
            ("p", "When the third term is negative, take the negative out with the GCF. "
                  "In the example above the second pair is `−4x − 12`; factoring out `−4` "
                  "rather than `4` gives `−4(x + 3)`, which matches the first bracket. "
                  "Factoring out `+4` gives `4(−x − 3)`, which does not &mdash; and the "
                  "method appears to fail when it has not."),
            ("p", "The rule of thumb: make the second bracket match the first. If it "
                  "cannot be made to match by choosing the sign, the pairing is genuinely "
                  "wrong."),
            ("h3", "Regrouping"),
            ("p", "The order of the terms is yours to choose, and sometimes the given "
                  "order is unhelpful. Consider `ax + by + ay + bx`. Pairing as given "
                  "leaves `a`-something and `b`-something with nothing shared. Reorder:"),
            ("math", [
                "ax + ay + bx + by  =  a(x + y) + b(x + y)  =  (x + y)(a + b)",
            ]),
            ("p", "Rearranging terms of a sum is always legal, so trying another pairing "
                  "costs nothing but a line. With four terms there are only three "
                  "genuinely different pairings, so the search is short and finite."),
            ("h3", "Finish the job"),
            ("p", "A factorisation is complete only when no factor factors further. In "
                  "the worked example `(x + 3)(x² − 4)` is not the end: `x² − 4` is a "
                  "difference of squares, so the complete answer is "
                  "`(x + 3)(x − 2)(x + 2)`."),
            ("p", "Stopping early is the most common way to lose marks on a factoring "
                  "question that was otherwise done correctly. After every step, look at "
                  "each factor again."),
            ("example", ("When grouping does not apply",
                         "`x³ + x² + 2x + 6` gives `x²(x + 1) + 2(x + 3)`. The brackets "
                         "differ, and no reordering fixes it. The honest conclusion is "
                         "\"grouping fails here\" &mdash; not \"this does not factor\". "
                         "That second claim needs lesson 12.")),
        ],
        "lab": ("factoring", {
            "mode": "grouping",
            "panel_title": "Pair, factor, compare",
            "panel_intro": "The lab tries each pairing of a four-term polynomial, shows the "
                           "binomial each pair leaves, and says plainly when no pairing "
                           "produces a match.",
        }),
        "steps_title": "Factoring four terms by grouping",
        "steps_intro": "Step 1 is the same as it was in lesson 5, and it is still not optional.",
        "steps": [
            ("Take out the overall GCF first",
             "Grouping is stated for a polynomial with no common factor across all four "
             "terms. If there is one, remove it and group what is left."),
            ("Pair the terms and take the GCF of each pair",
             "Usually first-two and last-two. Where the second pair begins with a minus, "
             "factor out the negative so the bracket has a chance of matching."),
            ("Compare the two brackets",
             "Identical brackets mean the method has worked. Different brackets mean try "
             "another pairing &mdash; there are only three &mdash; before concluding "
             "anything."),
            ("Take out the shared binomial, then factor each factor",
             "`A·P + B·P = (A + B)·P`. Then look at both results: a difference of squares "
             "or a factorable trinomial often remains, and the answer is not complete "
             "until nothing factors."),
        ],
        "worked": {
            "title": "Two groupings, one with a sign trap",
            "intro": ["The first needs the negative taken out of the second pair; the "
                      "second is clean but finishes early."],
            "lines": [
                "A.  x³ + 3x² − 4x − 12",
                "        (x³ + 3x²) + (−4x − 12)",
                "        x²(x + 3)  + (−4)(x + 3)      take out −4, not +4",
                "        (x + 3)(x² − 4)",
                "        (x + 3)(x − 2)(x + 2)         x² − 4 is a difference of squares",
                "",
                "    check at x = 1:   1 + 3 − 4 − 12 = −12",
                "                      (4)(−1)(3)     = −12",
                "",
                "B.  6x³ − 9x² + 4x − 6",
                "        3x²(2x − 3) + 2(2x − 3)",
                "        (2x − 3)(3x² + 2)",
                "",
                "    3x² + 2 has no real roots, so this is complete.",
            ],
            "after": [
                "In A, factoring `+4` out of the second pair would have given "
                "`4(−x − 3)`, and the two brackets would not have matched. The method "
                "would have looked broken; only the sign choice was.",
                "In B the second factor `3x² + 2` cannot be factored over the reals "
                "&mdash; it is positive for every `x`, so it has no root and therefore no "
                "linear factor. Recognising when to stop is part of the technique.",
            ],
        },
        "quiz_title": "Grouping",
        "quiz": [
            {"q": "Factor `x³ + 2x² + 5x + 10`.",
             "a": ["`(x + 2)(x² + 5)`", "`(x² + 2)(x + 5)`", "`(x + 2)(x² − 5)`",
                   "It does not factor by grouping"],
             "c": 0,
             "why": "`x²(x + 2) + 5(x + 2)`, so the shared binomial is `(x + 2)` and the "
                    "other factor is what multiplied it: `x² + 5`. Expanding confirms it."},
            {"q": "In `x³ + 4x² − 3x − 12`, what should be factored out of the last two terms?",
             "a": ["`3`", "`−3`", "`−1`", "`x`"],
             "c": 1,
             "why": "`−3x − 12 = −3(x + 4)`, which matches the `(x + 4)` from "
                    "`x²(x + 4)`. Taking out `+3` gives `3(−x − 4)` and the brackets no "
                    "longer agree."},
            {"q": "Grouping leaves `x²(x + 1) + 2(x + 3)`. What follows?",
             "a": ["The answer is `(x + 1)(x + 3)`",
                   "The polynomial has no factors at all",
                   "The brackets differ, so try another pairing before concluding anything",
                   "Average the brackets to `(x + 2)`"],
             "c": 2,
             "why": "There is no common factor to take out, so this pairing failed. Only "
                    "after every pairing fails can you say grouping does not apply &mdash; "
                    "and even then, whether the polynomial factors is a question for "
                    "lesson 12."},
        ],
        "mistakes": [
            ("Factoring `+` out of a negative second pair",
             "`−4x − 12` should give `−4(x + 3)`. Taking out `+4` produces a bracket that "
             "cannot match, and the method is abandoned for no reason."),
            ("Forcing two different brackets to be the same",
             "`(x + 3)` and `(x − 3)` are different polynomials. If the pairs do not "
             "agree, regroup; never adjust one bracket to fit."),
            ("Stopping at the first product",
             "`(x + 3)(x² − 4)` is a factorisation but not a complete one. Check every "
             "factor for a further factorisation before you call it finished."),
        ],
        "standard": ("Finish when four terms make you reach for a pairing automatically.",
                     "You should try the pairings without hesitation, get the sign right "
                     "on the second pair first time, and always look again at both factors "
                     "afterwards. You should also be comfortable saying \"grouping does not "
                     "work here\" without claiming more than that."),
        "note": "Grouping earns its place twice. Here it handles four terms, and in "
                "lesson 8 the AC method deliberately splits a three-term polynomial into "
                "four so that this technique can be used on it. Getting the signs "
                "reliable now pays for itself two lessons from now.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "factoring-simple-trinomials",
        "title": "Factoring Simple Trinomials",
        "module": "Factoring",
        "one_line": "Two numbers with the right product and the right sum.",
        "summary": (
            "For `x² + bx + c` the whole problem reduces to finding two integers whose "
            "product is `c` and whose sum is `b`. The candidate list is finite, so the "
            "search either succeeds or proves that no integer factorisation exists."
        ),
        "key": [
            "(x + p)(x + q)  =  x² + (p + q)x + pq",
            "",
            "so for x² + bx + c    find p, q  with   p·q = c   and   p + q = b",
            "",
            "x² − 7x + 12   →   (−3)(−4) = 12,  (−3) + (−4) = −7   →  (x − 3)(x − 4)",
        ],
        "key_label": "One identity, read backwards",
        "concepts_intro": (
            "This is the first genuine search on the course: a finite list of candidates, "
            "tested one at a time, with a definite answer either way."
        ),
        "concepts": [
            ("The identity tells you exactly what to look for",
             "Expanding `(x + p)(x + q)` gives `x² + (p + q)x + pq`. Matching coefficients "
             "turns factoring into two simultaneous conditions on two numbers &mdash; "
             "product `c`, sum `b` &mdash; and nothing else."),
            ("The candidate list is finite, so the search is complete",
             "`p` must divide `c`, and a nonzero integer has finitely many divisors. List "
             "the divisor pairs, check the sums, and you have either found the answer or "
             "shown there is none."),
            ("\"It does not factor\" is a result, not a surrender",
             "`x² + x + 1` has divisor pairs `(1, 1)` and `(−1, −1)`, with sums `2` and "
             "`−2`. Neither is `1`, so no integer factorisation exists. That is a proved "
             "statement, and it is the correct final answer."),
        ],
        "read_title": "Product and sum",
        "read_intro": "Where the two conditions come from, how the signs narrow the search, and when to stop.",
        "body": [
            ("p", "Multiply out `(x + p)(x + q)` and compare with `x² + bx + c`:"),
            ("math", [
                "(x + p)(x + q)  =  x² + qx + px + pq  =  x² + (p + q)x + pq",
                "",
                "                       x² +    b x   +  c",
            ]),
            ("thm", ("The factoring condition",
                     "A monic trinomial `x² + bx + c` factors as `(x + p)(x + q)` with `p` "
                     "and `q` integers exactly when there are integers `p`, `q` with "
                     "`pq = c` and `p + q = b`.",
                     "Two coefficients, two conditions. Because `p` must divide `c`, only "
                     "finitely many `p` need testing.")),
            ("p", "This applies when the leading coefficient is `1`. When it is not, "
                  "either take it out as a common factor if you can, or use the AC method "
                  "of lesson 8."),
            ("h3", "Reading the signs before you search"),
            ("p", "The two conditions constrain the signs, so you never need to test the "
                  "whole list blindly:"),
            ("ul", [
                "<strong>`c &gt; 0`.</strong> The product is positive, so `p` and `q` have "
                "the <em>same</em> sign &mdash; and that sign is the sign of `b`, since "
                "they must sum to it. In `x² − 7x + 12`, both are negative.",
                "<strong>`c &lt; 0`.</strong> The product is negative, so `p` and `q` have "
                "<em>opposite</em> signs. The one with the larger absolute value carries "
                "the sign of `b`.",
                "<strong>`c = 0`.</strong> There is no trinomial to search: `x² + bx` has "
                "a common factor `x`, and lesson 5 already handled it.",
            ]),
            ("p", "These are not extra rules to memorise. Each one is read straight off "
                  "`pq = c` and `p + q = b`, and deriving them on the spot is safer than "
                  "recalling them."),
            ("h3", "Why a finite search settles the question"),
            ("p", "Suppose no pair on the list works. Could there still be a factorisation "
                  "using fractions &mdash; something like `(x + 1/2)(x + 8)`? For a monic "
                  "trinomial the answer is no. If `x² + bx + c` with integer coefficients "
                  "factors into linear factors with rational numbers, those numbers are "
                  "necessarily integers, so they are already on the list."),
            ("p", "Lesson 12 proves this as part of the rational root theorem. For now, "
                  "take it as the reason the search is trustworthy: an empty result means "
                  "the trinomial does not factor over the rationals, not merely that you "
                  "did not find how."),
            ("example", ("A complete search that fails",
                         "`x² + x + 1`. The divisor pairs of `1` are `(1, 1)` and "
                         "`(−1, −1)`, giving sums `2` and `−2`. Neither equals `1`, and "
                         "the list is exhausted. The trinomial is irreducible over the "
                         "integers, and by the paragraph above, over the rationals too.")),
        ],
        "lab": ("factoring", {
            "mode": "trinomial",
            "panel_title": "The divisor-pair search",
            "panel_intro": "Enter `b` and `c`. The lab lists every divisor pair of `c` with "
                           "its sum, marks the pair that works, and reports an empty search "
                           "as a result. Try `b = 1`, `c = 1`.",
        }),
        "steps_title": "Factoring x² + bx + c",
        "steps_intro": "The search is short if you use the signs to prune it first.",
        "steps": [
            ("Check the leading coefficient is 1, and take out any GCF",
             "If the polynomial is `2x² + 10x + 12`, factor out the `2` first: "
             "`2(x² + 5x + 6)`. If the leading coefficient survives that, this lesson does "
             "not apply and lesson 8 does."),
            ("Use the sign of c, then the sign of b",
             "`c` positive means both numbers share the sign of `b`; `c` negative means "
             "opposite signs. This halves the list before you test anything."),
            ("List the divisor pairs of c and add each one",
             "Work systematically from `1` upward so nothing is skipped. Stop at the first "
             "pair whose sum is `b` &mdash; there cannot be a second."),
            ("Write the factors and expand to check; if the list is empty, say so",
             "The pair `p`, `q` gives `(x + p)(x + q)`, and expanding must return the "
             "original. If no pair summed to `b`, the answer is that it does not factor "
             "over the integers."),
        ],
        "worked": {
            "title": "Two searches that succeed, one that does not",
            "intro": ["Every divisor pair listed, so you can see the searches finish."],
            "lines": [
                "A.  x² − 7x + 12        c > 0, b < 0  →  both numbers negative",
                "        (−1)(−12)   sum −13",
                "        (−2)(−6)    sum −8",
                "        (−3)(−4)    sum −7      <-- match",
                "    answer  (x − 3)(x − 4)",
                "    check   x² − 4x − 3x + 12 = x² − 7x + 12",
                "",
                "B.  x² + 2x − 15       c < 0  →  opposite signs",
                "        (1)(−15)    sum −14",
                "        (−1)(15)    sum  14",
                "        (3)(−5)     sum  −2",
                "        (−3)(5)     sum   2      <-- match",
                "    answer  (x − 3)(x + 5)",
                "",
                "C.  x² + x + 1         c > 0, b > 0  →  both positive",
                "        (1)(1)      sum   2      only pair; 2 ≠ 1",
                "    answer  does not factor over the integers",
            ],
            "after": [
                "In B the pair `(−3, 5)` has the larger number positive, matching `b = +2`, "
                "exactly as the sign reading predicted. Listing all four pairs takes "
                "seconds and removes any guesswork about which arrangement is right.",
                "C is the important one. The search ended not because it got difficult but "
                "because the list ran out, and an exhausted list is a proof. Compare "
                "`x² + 2x + 1`, where the pair `(1, 1)` sums to `2` and the answer is "
                "`(x + 1)²`.",
            ],
        },
        "quiz_title": "Product and sum",
        "quiz": [
            {"q": "Factor `x² + 9x + 20`.",
             "a": ["`(x + 4)(x + 5)`", "`(x + 2)(x + 10)`", "`(x − 4)(x − 5)`",
                   "`(x + 1)(x + 20)`"],
             "c": 0,
             "why": "`4 × 5 = 20` and `4 + 5 = 9`. The other positive pairs of 20 are "
                    "`(1, 20)` and `(2, 10)`, summing to 21 and 12. `(x − 4)(x − 5)` has "
                    "the right product but sum `−9`."},
            {"q": "Factor `x² − x − 20`.",
             "a": ["`(x − 4)(x + 5)`", "`(x + 4)(x − 5)`", "`(x − 2)(x + 10)`",
                   "`(x + 4)(x + 5)`"],
             "c": 1,
             "why": "`c` is negative, so the signs are opposite; `b = −1` is negative, so "
                    "the larger number is negative. `4 × (−5) = −20` and "
                    "`4 + (−5) = −1`."},
            {"q": "`x² + 3x + 5` &mdash; what is the correct conclusion?",
             "a": ["`(x + 1)(x + 5)`",
                   "The divisor pairs of 5 give sums 6 and −6, so it does not factor over the integers",
                   "It needs a fractional pair such as `(x + 3/2)(x + 10/3)`",
                   "The search cannot be completed"],
             "c": 1,
             "why": "The only divisor pairs of `5` are `(1, 5)` and `(−1, −5)`, summing to "
                    "`6` and `−6`. Neither is `3`, the list is exhausted, and for a monic "
                    "trinomial no rational pair can succeed where the integer list failed."},
        ],
        "mistakes": [
            ("Matching the product but not the sum",
             "Both conditions must hold. `(x + 2)(x + 10)` has product `20` but sum `12`, "
             "so it is not a factorisation of `x² + 9x + 20` &mdash; and expanding it says "
             "so immediately."),
            ("Guessing signs instead of reading them off",
             "The sign of `c` decides whether the numbers agree in sign and the sign of "
             "`b` decides which way. Derived in two seconds, this removes the most common "
             "source of near-miss answers."),
            ("Treating an unsuccessful search as an unfinished one",
             "When every divisor pair has been tested and none works, the trinomial does "
             "not factor over the integers. Writing that is the complete answer; hunting "
             "for a cleverer pair is not."),
        ],
        "standard": ("Finish when you can factor by search and defend a negative result.",
                     "Given `x² + bx + c` you should list the divisor pairs of `c` in "
                     "order, use the signs to skip half of them, and either produce the "
                     "factors or state that none exist &mdash; naming the pairs you tested "
                     "as your evidence. That habit is exactly what lesson 12 formalises for "
                     "polynomials of any degree."),
        "note": "The lab shows the whole candidate list, including the sums that miss. "
                "That display is the point of it: watching a complete search come back "
                "empty on `x² + x + 1` is what turns \"I cannot factor this\" into \"this "
                "does not factor\", which are very different statements.",
    },
]
