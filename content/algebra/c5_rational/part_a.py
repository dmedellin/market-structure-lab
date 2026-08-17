"""Course 5, lessons 01-06 — rational expressions, from the domain to the equation."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "rational-expressions-and-their-domains",
        "title": "Rational Expressions and Their Domains",
        "module": "Rational expressions",
        "one_line": "The values a denominator forbids, found before anything is simplified.",
        "summary": (
            "A rational expression is one polynomial over another, and it means "
            "nothing at all where the bottom is zero. Those excluded values come "
            "from the denominator you were handed &mdash; never from the tidier one "
            "you end up with."
        ),
        "key": [
            "P(x)/Q(x)     P, Q polynomials,  Q not the zero polynomial",
            "domain:  every real x with  Q(x) ≠ 0",
            "(x² − 4)/(x − 2)  is UNDEFINED at x = 2  —  it is not 4",
            "the exclusions come from the ORIGINAL denominator",
        ],
        "key_label": "One expression, one forbidden value",
        "concepts_intro": (
            "Everything in the first half of this course is a rule about factors, and "
            "every one of those rules is false at a value where the expression does not "
            "exist. So the domain comes first, on its own line."
        ),
        "concepts": [
            ("A rational expression is a quotient of polynomials",
             "`(3x + 1)/(x² − 5)` is one; so is `x + 2`, with denominator `1`. What is "
             "<em>not</em> one is anything with a variable under a root or in an "
             "exponent &mdash; those arrive in lesson 8 and in course 7."),
            ("The denominator alone decides the domain",
             "The numerator may be anything, zero included. `(x − 4)/(x + 1)` is "
             "perfectly well defined at `x = 4`, where its value is `0`. It is `x = −1` "
             "that is excluded."),
            ("Undefined is not a value",
             "`0/0` is not `0`, not `1`, and not \"infinity\". Division is defined as "
             "the inverse of multiplication, and no number times `0` gives `4`, while "
             "<em>every</em> number times `0` gives `0`. Neither case yields an answer."),
        ],
        "read_title": "What the expression is, and where it lives",
        "read_intro": "The definition, then the question you ask before any algebra.",
        "body": [
            ("def", ("Rational expression",
                     "A <strong>rational expression</strong> is a quotient `P(x)/Q(x)` "
                     "of two polynomials in which `Q` is not the zero polynomial. It is "
                     "the algebraic version of a fraction, and it obeys the same rules "
                     "for the same reasons.")),
            ("p", "The condition on `Q` is about the <em>polynomial</em>, not about `x`. "
                  "`Q(x) = x − 2` is a perfectly good denominator even though it takes "
                  "the value zero somewhere; what is forbidden is `Q(x) = 0` for every "
                  "`x`, which would leave nothing to divide by anywhere."),
            ("def", ("Domain",
                     "The <strong>domain</strong> of a rational expression is the set of "
                     "real numbers `x` for which `Q(x) ≠ 0`. A number `c` with `Q(c) = 0` "
                     "is an <strong>excluded value</strong>: the expression assigns "
                     "nothing to it.")),
            ("p", "Finding the domain is therefore a factoring problem and nothing else. "
                  "Factor the denominator, set each factor to zero, and collect the "
                  "solutions. This is the first of many places in this course where an "
                  "unfactored denominator hides the answer."),
            ("example", ("Two exclusions",
                         "For `(x + 1)/(x² − x − 6)`, factor the bottom: "
                         "`x² − x − 6 = (x − 3)(x + 2)`. It is zero when `x = 3` and when "
                         "`x = −2`, so the domain is every real number except those two. "
                         "The numerator's zero at `x = −1` excludes nothing &mdash; the "
                         "expression is simply `0` there.")),
            ("p", "Now the case that gives this lesson its point. `(x² − 4)/(x − 2)` has "
                  "denominator zero at `x = 2`, so `2` is excluded. Factor the top and "
                  "the expression becomes `((x − 2)(x + 2))/(x − 2)`, which for every "
                  "`x ≠ 2` equals `x + 2`. At `x = 2` it equals nothing: the substitution "
                  "gives `0/0`."),
            ("math", [
                "x        1.9      1.99     2        2.01     2.1",
                "value    3.9      3.99     ——       4.01     4.1",
            ]),
            ("p", "The values approach `4` from both sides and the expression still has "
                  "no value at `2`. That gap is called a <strong>hole</strong>, and "
                  "lesson 7 puts it on a graph. What matters now is that `x + 2` "
                  "&mdash; the answer to the simplification &mdash; carries no record of "
                  "it. The exclusion is a fact about where you started."),
            ("thm", ("Equality of rational expressions",
                     "Two rational expressions are equal when they agree at every value "
                     "in the domain of <em>both</em>. So `(x² − 4)/(x − 2) = x + 2` is a "
                     "true statement for `x ≠ 2`, and writing it without that condition "
                     "is writing something false at one point.")),
        ],
        "lab": ("rationalfn", {
            "mode": "domain",
            "panel_title": "Where the expression stops existing",
            "panel_intro": "Type a denominator and watch the excluded values appear as "
                           "you factor it. The lab factors over the rationals and "
                           "reports every zero exactly.",
        }),
        "steps_title": "Finding the domain",
        "steps_intro": "Four steps, and the first one is not optional.",
        "steps": [
            ("Factor the denominator completely",
             "An unfactored quadratic hides its zeros. `x² − x − 6` looks harmless; "
             "`(x − 3)(x + 2)` says exactly which two numbers are forbidden."),
            ("Set each distinct factor to zero",
             "One linear equation per factor. A repeated factor such as `(x + 2)²` "
             "contributes the single value `x = −2`, not two of them."),
            ("Solve, and exclude every solution",
             "Each solution leaves the domain. Note that you never test the numerator: "
             "it has no say in whether the expression exists."),
            ("Write the exclusions down before simplifying",
             "Put `x ≠ 3, x ≠ −2` beside the expression now. After you cancel, the "
             "surviving form may be defined at those values, and you will have no way "
             "to recover them."),
        ],
        "worked": {
            "title": "The domain of (x + 1)/(x² − x − 6)",
            "intro": ["Factor, solve, exclude. The check at the end costs one line and "
                      "catches a mis-factored denominator immediately."],
            "lines": [
                "(x + 1)/(x² − x − 6)",
                "",
                "x² − x − 6   =   (x − 3)(x + 2)",
                "",
                "x − 3 = 0    ⟹    x = 3",
                "x + 2 = 0    ⟹    x = −2",
                "",
                "domain:   all real x   with   x ≠ 3   and   x ≠ −2",
                "",
                "check   x = 3 :    9 − 3 − 6  =  0    ✓ excluded",
                "check   x = −2 :   4 + 2 − 6  =  0    ✓ excluded",
                "check   x = −1 :   1 + 1 − 6  =  −4   defined, value 0",
            ],
            "after": [
                "The last line is the one students skip. `x = −1` makes the "
                "<em>numerator</em> zero, and a beginner who has learned \"zero is a "
                "problem\" excludes it. It is not a problem: `0/(−4) = 0`, an ordinary "
                "value at an ordinary point of the domain."
            ],
        },
        "quiz_title": "Domain first",
        "quiz": [
            {"q": "What is the domain of `(x − 5)/(x² − 16)`?",
             "a": ["All real x with x ≠ 5",
                   "All real x with x ≠ 4 and x ≠ −4",
                   "All real x with x ≠ 16",
                   "All real x"],
             "c": 1,
             "why": "`x² − 16 = (x − 4)(x + 4)`, which is zero at `4` and at `−4`. The "
                    "numerator's zero at `x = 5` excludes nothing &mdash; the expression "
                    "is defined there and equals `0`."},
            {"q": "`(x² − 4)/(x − 2)` at `x = 2` is:",
             "a": ["4", "0", "Undefined", "Equal to 1, since the numerator and "
                   "denominator both vanish"],
             "c": 2,
             "why": "Substituting gives `0/0`, which names no number. The expression "
                    "equals `x + 2` at every other value, and `x + 2` equals `4` at "
                    "`x = 2` &mdash; but that is a different expression with a larger "
                    "domain."},
            {"q": "Which denominator excludes exactly one value?",
             "a": ["`(x + 3)²`", "`x² − 9`", "`x² + 9`", "`x(x − 3)`"],
             "c": 0,
             "why": "`(x + 3)²` is zero only at `x = −3`; repeating a factor does not "
                    "repeat the exclusion. `x² − 9` excludes two values, `x(x − 3)` "
                    "excludes two, and `x² + 9` is never zero for real `x`, so it "
                    "excludes none."},
        ],
        "mistakes": [
            ("Excluding the values that make the numerator zero",
             "A zero on top is a zero for the whole expression, which is a perfectly good "
             "output. Only the bottom can destroy the expression."),
            ("Reading the domain off the simplified form",
             "`(x² − 4)/(x − 2)` simplifies to `x + 2`, whose natural domain is every "
             "real number. The original excluded `2`, and it still does. Simplifying "
             "changes the formula, not the expression you were asked about."),
            ("Treating `0/0` as a number",
             "It is not `0`, `1`, or `∞`. Both of the usual arguments for a value "
             "&mdash; `0/n = 0` and `n/n = 1` &mdash; apply and disagree, which is "
             "precisely why the case is left undefined."),
        ],
        "standard": ("Finish when you write the exclusions before you write anything else.",
                     "Given any rational expression you should produce its domain in one "
                     "line, from the factored denominator, without simplifying first. If "
                     "your habit is to simplify and then look for trouble, you will lose "
                     "an exclusion in lesson 2 and an extraneous root in lesson 6."),
        "note": "The lab factors the denominator over the rationals and lists the "
                "excluded values exactly, as fractions where they are fractions. It "
                "will not report `x ≠ 0.333` for `3x − 1`; that root is `1/3`, and a "
                "domain stated in decimals is a domain stated wrongly.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "simplifying-rational-expressions",
        "title": "Simplifying Rational Expressions",
        "module": "Rational expressions",
        "one_line": "Cancel factors, never terms, and keep the domain you started with.",
        "summary": (
            "One rule does all the work: a factor common to the top and the bottom may "
            "be removed. A term may not. The difference between those two words is the "
            "most expensive distinction in school algebra."
        ),
        "key": [
            "(PK)/(QK)  =  P/Q        provided K ≠ 0",
            "(x² − 9)/(x² + x − 12)  =  (x + 3)/(x + 4),   x ≠ 3",
            "(3 − x)/(x − 3)  =  −1          since 3 − x = −(x − 3)",
            "(x + 3)/x  is ALREADY lowest terms  —  3 is a term",
        ],
        "key_label": "One legal cancellation, one illegal one",
        "concepts_intro": (
            "Simplifying is a single theorem applied carefully. Nearly every error here "
            "is the same error: applying it to something that is not a factor."
        ),
        "concepts": [
            ("Only a common factor cancels",
             "A <em>factor</em> is joined to the rest by multiplication; a <em>term</em> "
             "is joined by addition. `(2x)/(2y)` cancels to `x/y`. `(2 + x)/(2 + y)` "
             "cancels to nothing at all."),
            ("So factoring is not optional",
             "The rule is stated in terms of factors, so an expression that is not "
             "factored cannot be simplified &mdash; you cannot see the common factor "
             "in `(x² − 9)/(x² + x − 12)`, and it is there."),
            ("Cancelling changes the formula, not the domain",
             "The simplified form is equal to the original only where the original "
             "exists. Carry the exclusions across; they are part of the answer."),
        ],
        "read_title": "Lowest terms, and the one rule that gets you there",
        "read_intro": "Why the rule is true, and exactly what it does not permit.",
        "body": [
            ("thm", ("The fundamental principle of fractions",
                     "For polynomials `P`, `Q`, `K` with `Q ≠ 0` and `K ≠ 0`, "
                     "`(PK)/(QK) = P/Q`. It holds because `K/K = 1` and multiplying by "
                     "`1` changes nothing &mdash; which is also why the condition `K ≠ 0` "
                     "cannot be dropped: `0/0` is not `1`.")),
            ("p", "Read the statement carefully. `K` multiplies `P`, and `K` multiplies "
                  "`Q`. Nothing in the theorem lets you remove something that is "
                  "<em>added</em> to `P`, and there is no companion theorem that does."),
            ("def", ("Lowest terms",
                     "A rational expression is in <strong>lowest terms</strong> when its "
                     "numerator and denominator have no common polynomial factor other "
                     "than a constant.")),
            ("p", "The method follows from the theorem. Factor the numerator completely, "
                  "factor the denominator completely, record the excluded values, then "
                  "strike out the factors that appear in both."),
            ("example", ("A cancellation that is legal",
                         "`(x² − 9)/(x² + x − 12)` factors as "
                         "`((x − 3)(x + 3))/((x + 4)(x − 3))`. The denominator is zero at "
                         "`x = 3` and `x = −4`, so both are excluded. The factor `x − 3` "
                         "is common, and removing it leaves `(x + 3)/(x + 4)`, valid for "
                         "`x ≠ 3` and `x ≠ −4`.")),
            ("p", "Notice what happened to `x = 3`. It is still excluded, because it was "
                  "excluded from the expression we were given, but `(x + 3)/(x + 4)` is "
                  "quite happy there, taking the value `6/7`. The two expressions agree "
                  "everywhere except at that single point, where one exists and the "
                  "other does not."),
            ("def", ("Opposite factors",
                     "`a − b` and `b − a` differ by a sign: `a − b = −(b − a)`. So a "
                     "numerator and denominator that look like opposites do share a "
                     "factor, and their quotient is `−1`.")),
            ("example", ("The sign case",
                         "`(3 − x)/(x − 3)`. Write the top as `−(x − 3)`; the expression "
                         "becomes `(−(x − 3))/(x − 3) = −1`, for every `x ≠ 3`. Checking "
                         "at `x = 0` gives `3/(−3) = −1`, which agrees.")),
            ("p", "Finally, the error the whole lesson is aimed at. In `(x + 3)/x` the "
                  "`x` on the bottom is a factor of the denominator but only a "
                  "<em>term</em> of the numerator, so nothing cancels and the expression "
                  "is already in lowest terms."),
            ("math", [
                "at x = 1 :   (x + 3)/x  =  4/1  =  4        3 is not the answer",
                "at x = 3 :   (x + 3)/x  =  6/3  =  2        3 is not the answer",
            ]),
            ("p", "One numerical test would have caught it. That is worth remembering "
                  "as a general habit: a proposed simplification is an identity, and an "
                  "identity that fails at `x = 1` is not an identity."),
        ],
        "lab": ("rationalfn", {
            "mode": "simplify",
            "panel_title": "Factor, then cancel",
            "panel_intro": "The lab factors both parts, marks the common factors, and "
                           "keeps the original exclusions beside the reduced form so you "
                           "can see what the answer no longer records.",
        }),
        "steps_title": "Reducing to lowest terms",
        "steps_intro": "The order is fixed: exclusions are recorded before anything is struck out.",
        "steps": [
            ("Factor the numerator and the denominator",
             "Completely, and separately. Greatest common factor first, then the "
             "patterns from course 4 &mdash; difference of squares, trinomials, grouping."),
            ("Write down the excluded values",
             "From the factored denominator, before you cancel. This is the only moment "
             "at which they are visible."),
            ("Cancel the common factors",
             "One at a time, and only whole factors. If a factor pair differs by a sign, "
             "pull `−1` out of one of them first so the match is exact."),
            ("Check at one convenient value",
             "Pick any `x` in the domain, usually `0` or `1`, and evaluate both forms. "
             "They must agree. This catches a cancelled term in seconds."),
        ],
        "worked": {
            "title": "Simplify (x² − 9)/(x² + x − 12)",
            "intro": ["Two factorisations, one shared factor, and a check that the "
                      "result really is the same expression."],
            "lines": [
                "(x² − 9)/(x² + x − 12)",
                "",
                "top:      x² − 9        =  (x − 3)(x + 3)",
                "bottom:   x² + x − 12   =  (x + 4)(x − 3)",
                "",
                "exclusions FIRST:   x ≠ 3,   x ≠ −4",
                "",
                "=  ((x − 3)(x + 3)) / ((x + 4)(x − 3))",
                "=  (x + 3)/(x + 4),        x ≠ 3,  x ≠ −4",
                "",
                "check at x = 0 :   −9/−12  =  3/4      and   3/4      ✓",
                "check at x = 1 :   −8/−10  =  4/5      and   4/5      ✓",
                "at x = 3 :   original undefined,   (x + 3)/(x + 4) = 6/7",
            ],
            "after": [
                "The final line is the reason the exclusion is written twice. The "
                "reduced form is defined at `x = 3` and gives a perfectly reasonable "
                "number there, so nothing about `6/7` announces that it should not "
                "exist. Only the condition you carried tells you."
            ],
        },
        "quiz_title": "Factor or term",
        "quiz": [
            {"q": "Simplify `(x² − 25)/(x² − 10x + 25)`.",
             "a": ["`(x + 5)/(x − 5)`, with `x ≠ 5`",
                   "`(x − 5)/(x + 5)`, with `x ≠ −5`",
                   "`−1`",
                   "It is already in lowest terms"],
             "c": 0,
             "why": "The top is `(x − 5)(x + 5)` and the bottom is `(x − 5)²`. One factor "
                    "of `x − 5` cancels, leaving `(x + 5)/(x − 5)`. The denominator was "
                    "zero only at `x = 5`, so that is the single exclusion."},
            {"q": "Which of these is a legal cancellation?",
             "a": ["`(x + 4)/4 = x`",
                   "`(x² + 1)/x = x + 1`",
                   "`(5(x − 1))/(7(x − 1)) = 5/7`, for `x ≠ 1`",
                   "`(x + 6)/(x + 3) = 2`"],
             "c": 2,
             "why": "Only the third has `x − 1` as a genuine factor of both parts. The "
                    "others cancel across a `+`, which the fundamental principle never "
                    "permits &mdash; test the last one at `x = 0`: `6/3 = 2` is true "
                    "there and false at `x = 1`, where it gives `7/4`."},
            {"q": "`(2 − x)/(x − 2)` equals:",
             "a": ["`1`", "`−1`", "`0`", "`−1/(x − 2)`"],
             "c": 1,
             "why": "`2 − x = −(x − 2)`, so the quotient is `−1` for every `x ≠ 2`. "
                    "Numerator and denominator are opposites, not equals; the sign is "
                    "the whole content of the answer. `−1/(x − 2)` is a cancellation "
                    "carried out on one line only: the `x − 2` is struck out of the "
                    "numerator and left standing in the denominator, and a factor "
                    "removed from one line has not been cancelled."},
        ],
        "mistakes": [
            ("Cancelling a term because it appears on both lines",
             "`(x + 3)/(x + 4)` does not become `3/4`. The `x` is added, not multiplied, "
             "and one substitution &mdash; `x = 1` gives `4/5` &mdash; disposes of it."),
            ("Dropping the exclusions on the way to the answer",
             "`(x² − 4)/(x − 2) = x + 2` is only true for `x ≠ 2`. Without that "
             "condition the statement is false at exactly one point, and lesson 7 draws "
             "the hole it leaves."),
            ("Missing an opposite pair",
             "`(4 − x²)/(x − 2)` looks unfactorable against its denominator until you "
             "write `4 − x² = −(x − 2)(x + 2)`. The answer is `−(x + 2)`, not \"no "
             "common factor\"."),
        ],
        "standard": ("Finish when you can justify each cancellation by naming the factor.",
                     "For any expression you reduce, you should be able to point at the "
                     "polynomial you removed and say that it multiplied both the "
                     "numerator and the denominator. If you cannot name it, you have not "
                     "cancelled &mdash; you have invented a rule that happens to work on "
                     "this example."),
        "note": "A numerical check is not a proof, and on this path it is never offered "
                "as one: an identity can survive a lucky value. But a single "
                "disagreement is conclusive in the other direction, and that is what "
                "makes the habit worth having &mdash; it cannot confirm your answer, and "
                "it will reliably refute a wrong one.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "multiplying-and-dividing-rational-expressions",
        "title": "Multiplying and Dividing Rational Expressions",
        "module": "Rational expressions",
        "one_line": "Multiply straight across, divide by flipping, and factor before either.",
        "summary": (
            "Multiplication of algebraic fractions is exactly multiplication of "
            "numerical ones, and division is multiplication by the reciprocal. The only "
            "genuinely new thing is that dividing forbids more values than it looks like "
            "it forbids."
        ),
        "key": [
            "a/b · c/d  =  (ac)/(bd)",
            "a/b ÷ c/d  =  a/b · d/c",
            "the division excludes zeros of b, of d, AND of c",
            "factor everything, cancel across, multiply last",
        ],
        "key_label": "Two rules, three sources of exclusions",
        "concepts_intro": (
            "No common denominator is needed here &mdash; that is lesson 4's problem. "
            "What this lesson demands is that you factor first and that you account for "
            "a divisor which may itself be zero."
        ),
        "concepts": [
            ("Multiplication is across the top and across the bottom",
             "`a/b · c/d = (ac)/(bd)`, with no adjustment of denominators. It is the one "
             "fraction operation that needs no preparation, which is why division is "
             "converted into it."),
            ("Division is multiplication by the reciprocal",
             "`a/b ÷ c/d = a/b · d/c`. Dividing by `c/d` asks what you must multiply "
             "`c/d` by to reach `a/b`, and `d/c` undoes `c/d` because their product "
             "is `1`."),
            ("Cancel before you multiply, not after",
             "The factors are already visible before multiplying and buried afterwards. "
             "Expanding `(x − 2)(x + 2)(x + 3)` first turns a one-line cancellation into "
             "a cubic you then have to factor again."),
        ],
        "read_title": "Products, quotients, and the exclusion that hides",
        "read_intro": "Two theorems, then the value that only division forbids.",
        "body": [
            ("thm", ("Product rule",
                     "For rational expressions with `b ≠ 0` and `d ≠ 0`, "
                     "`(a/b)·(c/d) = (ac)/(bd)`. The domain of the product excludes every "
                     "zero of `b` and every zero of `d`.")),
            ("thm", ("Quotient rule",
                     "For `b ≠ 0`, `d ≠ 0` and `c ≠ 0`, "
                     "`(a/b) ÷ (c/d) = (a/b)·(d/c) = (ad)/(bc)`. The three conditions are "
                     "each doing work, and the third is the one that is easy to lose.")),
            ("p", "Why `c ≠ 0`? Because `a/b ÷ c/d` means dividing by the number `c/d`, "
                  "and that number is zero exactly when `c` is zero. Dividing by zero is "
                  "undefined whether the zero arrives as a plain `0` or as a fraction "
                  "with a zero on top."),
            ("example", ("The hidden exclusion",
                         "In `(x² − 4)/(x² + 6x + 9) ÷ (x − 2)/(x + 3)`, the visible "
                         "denominators `(x + 3)²` and `x + 3` forbid `x = −3`. But the "
                         "divisor `(x − 2)/(x + 3)` is zero at `x = 2`, so `x = 2` is "
                         "forbidden too &mdash; and after you flip, `x − 2` sits in a "
                         "denominator where you can finally see it.")),
            ("p", "This is the general pattern: flipping the divisor turns its numerator "
                  "into a denominator, and a denominator is something you already know "
                  "how to read. Record the exclusion at the moment of flipping, because "
                  "the factor `x − 2` is about to cancel and disappear."),
            ("p", "With the exclusions safely written down, the mechanical part is "
                  "short. Factor every numerator and denominator, cancel any factor that "
                  "appears on both levels of the combined fraction, and only then write "
                  "the product."),
            ("example", ("A product",
                         "`(x + 1)/(x − 5) · (x − 5)/(x + 2)`. The factor `x − 5` is on "
                         "top of the second and on the bottom of the first, so it "
                         "cancels: the answer is `(x + 1)/(x + 2)` with `x ≠ 5` and "
                         "`x ≠ −2`. Multiplying first would have produced "
                         "`(x² − 4x − 5)/(x² − 3x − 10)` and the same cancellation, "
                         "harder.")),
            ("p", "There is no rule about numerators here to match the one about "
                  "denominators in lesson 4. A product needs no common denominator, so "
                  "the temptation to find one is worth resisting: it is extra work that "
                  "cannot help."),
        ],
        "lab": ("rationalfn", {
            "mode": "multiply",
            "panel_title": "Cancel across the product",
            "panel_intro": "Enter two expressions and choose multiply or divide. The lab "
                           "flips the divisor, lists every exclusion including the one "
                           "the divisor contributes, and cancels factor by factor.",
        }),
        "steps_title": "Multiplying or dividing",
        "steps_intro": "For division, step one is the flip; everything after is the same.",
        "steps": [
            ("If it is a division, flip the divisor now",
             "Rewrite `÷ c/d` as `· d/c` before doing anything else, so that the rest of "
             "the problem is a single product."),
            ("Factor all four polynomials",
             "Every numerator and every denominator, completely. Nothing can be "
             "cancelled until this is done."),
            ("List the exclusions, divisor included",
             "Zeros of both original denominators, plus the zeros of the divisor's "
             "numerator if you divided. That last group vanishes from the answer."),
            ("Cancel, then multiply what is left",
             "Strike common factors across the whole product, then write the remaining "
             "factors on each level. Leave the answer factored."),
        ],
        "worked": {
            "title": "Divide (x² − 4)/(x² + 6x + 9) by (x − 2)/(x + 3)",
            "intro": ["A division with three separate exclusions, one of which is "
                      "invisible in the final answer."],
            "lines": [
                "(x² − 4)/(x² + 6x + 9)   ÷   (x − 2)/(x + 3)",
                "",
                "flip the divisor:",
                "=  (x² − 4)/(x² + 6x + 9)   ·   (x + 3)/(x − 2)",
                "",
                "factor:   x² − 4 = (x − 2)(x + 2)      x² + 6x + 9 = (x + 3)²",
                "",
                "exclusions:   x ≠ −3   (denominators)     x ≠ 2   (divisor)",
                "",
                "=  ((x − 2)(x + 2)(x + 3)) / ((x + 3)²(x − 2))",
                "=  (x + 2)/(x + 3),        x ≠ −3,  x ≠ 2",
                "",
                "check at x = 0 :   (−4/9) ÷ (−2/3)  =  (−4/9)(−3/2)  =  2/3",
                "                   (x + 2)/(x + 3)  =  2/3        ✓",
            ],
            "after": [
                "Both `x − 2` and one `x + 3` cancelled, and with them went every trace "
                "of why `2` is not allowed. `(x + 2)/(x + 3)` evaluated at `x = 2` gives "
                "`4/5`, a number the original division cannot produce, because at "
                "`x = 2` it asks you to divide by `0`."
            ],
        },
        "quiz_title": "Across, or flipped",
        "quiz": [
            {"q": "`(x/3) ÷ (x/5)` equals, for `x ≠ 0`:",
             "a": ["`x²/15`", "`5/3`", "`3/5`", "`5x/3`"],
             "c": 1,
             "why": "Flip the divisor: `(x/3)·(5/x) = (5x)/(3x) = 5/3`. The `x` cancels "
                    "as a genuine common factor. The exclusion `x ≠ 0` comes from the "
                    "divisor being zero there, and nothing in `5/3` records it."},
            {"q": "`(x + 1)/(x + 4) ÷ (x − 7)/(x + 4)` simplifies to `(x + 1)/(x − 7)`. "
                  "Which exclusion is no longer visible in that answer?",
             "a": ["`x = −4`", "`x = 7`", "`x = −1`", "`x = 4`"],
             "c": 0,
             "why": "Both original denominators are `x + 4`, so `x = −4` is excluded; "
                    "that factor cancels and the answer says nothing about it. `x = 7` "
                    "is excluded too &mdash; the divisor is zero there &mdash; but it "
                    "survives as the denominator of the answer, so that one still "
                    "announces itself."},
            {"q": "Before multiplying `((x² − 1)/(x + 3)) · ((x + 3)/(x − 1))`, the "
                  "efficient first move is:",
             "a": ["Expand both numerators",
                   "Find a common denominator",
                   "Factor `x² − 1` as `(x − 1)(x + 1)` and cancel",
                   "Cross-multiply"],
             "c": 2,
             "why": "Factoring exposes `x − 1` and `x + 3` as common factors, and the "
                    "product collapses to `x + 1` in one step. A common denominator is "
                    "for addition, and cross-multiplication is for equations &mdash; "
                    "this is neither."},
        ],
        "mistakes": [
            ("Forgetting that the divisor may be zero",
             "In `a/b ÷ c/d` the zeros of `c` are excluded, and they usually cancel out "
             "of sight during the simplification. Write them down when you flip."),
            ("Looking for a common denominator",
             "Products and quotients never need one. Building it wastes time and, worse, "
             "invites you to add the numerators out of habit."),
            ("Multiplying everything out before cancelling",
             "Expanding first is legal and almost always a mistake: it turns visible "
             "factors into a polynomial you must factor again to finish."),
        ],
        "standard": ("Finish when division is automatic and its extra exclusion is too.",
                     "You should convert a division to a product without thinking, and "
                     "still stop to record the zeros of the divisor's numerator. The "
                     "arithmetic here is the easiest in the course; the bookkeeping is "
                     "what distinguishes a correct answer from a nearly correct one."),
        "note": "The lab shows the flip as its own step rather than folding it into the "
                "cancellation, and it labels each exclusion with the factor that caused "
                "it. When a factor cancels, its exclusion stays on the list in a dimmed "
                "row &mdash; the answer changes, the domain does not.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "adding-and-subtracting-rational-expressions",
        "title": "Adding and Subtracting Rational Expressions",
        "module": "Rational expressions",
        "one_line": "A common denominator built from factors, and a minus sign that reaches every term.",
        "summary": (
            "Fractions can only be added when they are counted in the same units, so "
            "the work is all in the denominator. Building the least one is a factoring "
            "problem, and the subtraction that follows is where the sign errors live."
        ),
        "key": [
            "a/c + b/c  =  (a + b)/c        same denominator, add the tops",
            "LCD:  every distinct factor, each to its HIGHEST power",
            "(x + 2)(x + 3)  and  (x + 2)²   ⟹   LCD = (x + 2)²(x + 3)",
            "a/c − b/c  =  (a − b)/c        subtract ALL of b, not its first term",
        ],
        "key_label": "One denominator, built from factors",
        "concepts_intro": (
            "Adding is the only one of the four operations that cannot be done a piece "
            "at a time. Both fractions must first be rewritten over one denominator, "
            "and that denominator is chosen, not stumbled upon."
        ),
        "concepts": [
            ("Only like denominators can be added",
             "`2/7 + 3/7 = 5/7` because both count sevenths. `a/c + b/d` counts two "
             "different things, and there is no rule that adds them directly &mdash; in "
             "particular `a/c + b/d` is not `(a + b)/(c + d)`."),
            ("The LCD is assembled from factors",
             "Factor each denominator, then take every distinct factor to the highest "
             "power it reaches in any one of them. The product of the denominators "
             "always works, but it is often larger than necessary."),
            ("Subtraction distributes over the whole numerator",
             "`a/c − (b + d)/c` is `(a − b − d)/c`. The bar acts as a bracket, and the "
             "moment you write the numerators on one line that bracket has to be "
             "written explicitly or it is lost."),
        ],
        "read_title": "Building the denominator, then the numerators",
        "read_intro": "Why a common denominator is required, and how to find the least one.",
        "body": [
            ("p", "With a common denominator the rule is immediate: "
                  "`a/c + b/c = (a + b)/c`. Everything difficult about this lesson is in "
                  "arranging for that situation to hold."),
            ("def", ("Least common denominator",
                     "The <strong>LCD</strong> of two rational expressions is the product "
                     "of every distinct factor appearing in either denominator, each "
                     "raised to the highest power with which it appears in a single "
                     "denominator.")),
            ("example", ("Building an LCD",
                         "For `5/((x + 2)(x + 3))` and `3/(x + 2)²` the distinct factors "
                         "are `x + 2` and `x + 3`. The highest power of `x + 2` in one "
                         "denominator is `2`, and of `x + 3` is `1`, so the LCD is "
                         "`(x + 2)²(x + 3)` &mdash; not the product of the two "
                         "denominators, which would carry `(x + 2)³`.")),
            ("p", "Multiplying the denominators together is never wrong, only wasteful: "
                  "the extra factor cancels at the end, after you have carried it through "
                  "every line. On a two-term sum that is a nuisance; in lesson 6, where "
                  "the LCD multiplies an entire equation, it is a real cost."),
            ("p", "Once the LCD is chosen, each fraction is rebuilt to sit over it. "
                  "Multiply the numerator and the denominator of each by whatever factors "
                  "the LCD has and it lacks &mdash; legal by the fundamental principle "
                  "of lesson 2, since you are multiplying by a form of `1`."),
            ("math", [
                "5/((x + 2)(x + 3))  +  3/(x + 2)²           LCD (x + 2)²(x + 3)",
                "",
                "=  5(x + 2)/LCD   +   3(x + 3)/LCD",
                "=  (5x + 10 + 3x + 9)/LCD",
                "=  (8x + 19)/((x + 2)²(x + 3))",
            ]),
            ("p", "Now subtraction, and the error that this lesson exists to prevent. "
                  "When the second numerator has more than one term, the minus sign in "
                  "front of the fraction applies to <em>all</em> of it."),
            ("example", ("Where the sign goes",
                         "`x/(x² − 9) − 2/(x + 3)` becomes, over the LCD "
                         "`(x − 3)(x + 3)`, the numerator `x − 2(x − 3)`. That is "
                         "`x − 2x + 6 = 6 − x`. Writing `x − 2x − 6` instead &mdash; "
                         "distributing the minus to the first term only &mdash; gives "
                         "`−x − 6`, and every later step is wrong.")),
            ("p", "The reliable defence is mechanical: put the entire second numerator "
                  "in brackets before you subtract, and only then distribute. It costs "
                  "one pair of brackets and removes the most common source of lost marks "
                  "in the whole topic."),
            ("p", "Finally, the answer's domain is inherited from the denominators you "
                  "started with, exactly as in lesson 2. `(6 − x)/((x − 3)(x + 3))` "
                  "excludes `3` and `−3`, and would still exclude them if the numerator "
                  "had cancelled a factor away."),
        ],
        "lab": ("rationalfn", {
            "mode": "add",
            "panel_title": "The least common denominator",
            "panel_intro": "The lab factors both denominators, builds the LCD factor by "
                           "factor, and shows the bracketed numerator before it "
                           "distributes &mdash; the step where the sign is usually lost.",
        }),
        "steps_title": "Adding or subtracting",
        "steps_intro": "Five minutes on the denominator saves the numerator.",
        "steps": [
            ("Factor every denominator",
             "The LCD is defined in terms of factors, so it cannot be built from "
             "`x² − 9`. It can be built from `(x − 3)(x + 3)`."),
            ("Assemble the LCD",
             "Each distinct factor once, to the highest power it reaches in any single "
             "denominator. Check it is divisible by each original denominator."),
            ("Rebuild each fraction over the LCD",
             "Multiply top and bottom by the missing factors. Leave the numerator "
             "unexpanded for the moment, in brackets."),
            ("Combine the numerators, then simplify",
             "Distribute the sign, collect like terms, and factor the result to see "
             "whether anything cancels &mdash; carrying the original exclusions forward."),
        ],
        "worked": {
            "title": "Simplify x/(x² − 9) − 2/(x + 3)",
            "intro": ["The brackets in line four are the entire point of the example."],
            "lines": [
                "x/(x² − 9)  −  2/(x + 3)",
                "",
                "x² − 9  =  (x − 3)(x + 3)          LCD = (x − 3)(x + 3)",
                "exclusions:   x ≠ 3,   x ≠ −3",
                "",
                "=  x/((x − 3)(x + 3))  −  2(x − 3)/((x − 3)(x + 3))",
                "=  [x − (2x − 6)] / ((x − 3)(x + 3))",
                "=  (x − 2x + 6) / ((x − 3)(x + 3))",
                "=  (6 − x)/((x − 3)(x + 3)),        x ≠ 3,  x ≠ −3",
                "",
                "check at x = 0 :    0 − 2/3   =   −2/3",
                "                    6/((−3)(3))  =  6/(−9)  =  −2/3     ✓",
            ],
            "after": [
                "Note that `6 − x` shares no factor with the denominator, so the answer "
                "is already in lowest terms. Note also that it is <em>not</em> `−1` "
                "times something familiar: `6 − x` and `x − 3` are not opposites, and "
                "the sign trick from lesson 2 does not apply here."
            ],
        },
        "quiz_title": "Denominators and signs",
        "quiz": [
            {"q": "What is the LCD of `1/(x² − 4)` and `1/(x² + 4x + 4)`?",
             "a": ["`(x − 2)(x + 2)²`",
                   "`(x² − 4)(x² + 4x + 4)`",
                   "`(x − 2)(x + 2)`",
                   "`(x + 2)²`"],
             "c": 0,
             "why": "The denominators factor as `(x − 2)(x + 2)` and `(x + 2)²`. The "
                    "distinct factors are `x − 2` and `x + 2`, and the highest power of "
                    "`x + 2` is `2`. The product of the denominators is a common "
                    "denominator but carries an extra `x + 2`."},
            {"q": "`3/x − (x + 1)/x` equals:",
             "a": ["`(2 − x)/x`", "`(4 + x)/x`", "`(3 − x + 1)/x`", "`(2 + x)/x`"],
             "c": 0,
             "why": "The numerator is `3 − (x + 1) = 3 − x − 1 = 2 − x`. Subtracting only "
                    "the `x` and leaving `+1` alone gives `(4 − x)/x`, which is the "
                    "standard error &mdash; the minus applies to the whole of `x + 1`."},
            {"q": "Is `a/c + b/d = (a + b)/(c + d)` ever a valid rule?",
             "a": ["Yes, whenever `c` and `d` are non-zero",
                   "Yes, it is how fractions are added",
                   "No, and `1/2 + 1/2` refutes it at once",
                   "Only when `c = d`"],
             "c": 2,
             "why": "`1/2 + 1/2 = 1`, while the proposed rule gives `2/4 = 1/2`. Adding "
                    "denominators is not an operation on fractions at all; the "
                    "denominator names the unit being counted, and the unit does not "
                    "change when you count more of them."},
        ],
        "mistakes": [
            ("Subtracting only the first term of the numerator",
             "`a/c − (b + d)/c` is `(a − b − d)/c`. Bracket the numerator before you "
             "subtract and the error becomes impossible rather than merely unlikely."),
            ("Adding the denominators",
             "`a/c + b/d` is not `(a + b)/(c + d)`. One numerical instance settles it "
             "for good, and it is worth doing once so the rule never returns."),
            ("Cancelling a factor of the new denominator against one term on top",
             "In `(8x + 19)/((x + 2)²(x + 3))` nothing cancels, because `8x + 19` is not "
             "divisible by either factor. A factor must divide the whole numerator, not "
             "part of it."),
        ],
        "standard": ("Finish when the LCD is built from factors and the sign survives.",
                     "You should be able to state the LCD of two factored denominators "
                     "immediately, and to subtract two fractions whose numerators are "
                     "binomials without dropping a sign. Those are the two skills lesson "
                     "5 assumes and lesson 6 runs on."),
        "note": "The lab writes the numerator in brackets and pauses there before "
                "distributing, because that intermediate line is the one nobody writes "
                "and everybody needs. The exclusions shown are those of the original "
                "denominators, which is why they can outnumber the factors visible in "
                "the answer.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "complex-fractions",
        "title": "Complex Fractions",
        "module": "Rational expressions",
        "one_line": "A fraction whose parts are themselves fractions, cleared two different ways.",
        "summary": (
            "Nothing new is needed here &mdash; only lessons 3 and 4 applied in one of "
            "two orders. The second order, multiplying through by the LCD of the small "
            "denominators, is usually much shorter, and both must agree."
        ),
        "key": [
            "method 1:  combine the top, combine the bottom, then divide",
            "method 2:  multiply top and bottom by the LCD of the small parts",
            "(1/x − 1/3)/(x − 3)  =  −1/(3x)",
            "every small denominator contributes its own exclusion",
        ],
        "key_label": "One expression, two routes, one answer",
        "concepts_intro": (
            "A complex fraction is not a new object. It is a division, written "
            "vertically, whose two halves happen to need simplifying first."
        ),
        "concepts": [
            ("The main bar is a division",
             "`(A)/(B)` means `A ÷ B` no matter how complicated `A` and `B` are. Once "
             "each is a single fraction, lesson 3 finishes the job by flipping `B`."),
            ("Multiplying top and bottom by the LCD is legal",
             "It is the fundamental principle of lesson 2 again: multiplying both parts "
             "by the same non-zero expression leaves the value unchanged, and choosing "
             "the LCD clears every small denominator at once."),
            ("Exclusions come from every level",
             "The small denominators, the main denominator, and any value making the "
             "whole lower half zero are all excluded. The simplified answer typically "
             "shows none of them."),
        ],
        "read_title": "Two methods, and why they agree",
        "read_intro": "The slow reliable route, then the fast one, on the same expression.",
        "body": [
            ("def", ("Complex fraction",
                     "A <strong>complex fraction</strong> is a rational expression in "
                     "which the numerator, the denominator, or both, themselves contain "
                     "fractions. `(1/x − 1/3)/(x − 3)` and `(1/x + 1/y)/(1/x − 1/y)` are "
                     "typical.")),
            ("p", "<strong>Method 1</strong> treats the bar as what it is. Combine the "
                  "numerator into a single fraction using lesson 4, do the same to the "
                  "denominator, and then divide the one by the other using lesson 3. It "
                  "always works and it is often long."),
            ("p", "<strong>Method 2</strong> removes the small fractions before they can "
                  "cause trouble. Find the LCD of every small denominator that appears "
                  "anywhere in the expression, and multiply both the whole numerator and "
                  "the whole denominator by it."),
            ("thm", ("Why method 2 is legal",
                     "For any non-zero expression `M`, `(A)/(B) = (AM)/(BM)`. Choosing "
                     "`M` to be the LCD of the small denominators makes `AM` and `BM` "
                     "free of fractions, because each small denominator divides `M`.")),
            ("example", ("The same expression, both ways",
                         "Take `(1/x − 1/3)/(x − 3)`. Method 1: the top is "
                         "`(3 − x)/(3x)`, so the whole thing is "
                         "`(3 − x)/(3x) ÷ (x − 3) = (3 − x)/(3x(x − 3))`. Method 2: "
                         "multiply top and bottom by `3x` to get `(3 − x)/(3x(x − 3))` "
                         "directly. Same expression, one step fewer.")),
            ("p", "Either way the finish is the sign observation from lesson 2: "
                  "`3 − x = −(x − 3)`, so the quotient is `−(x − 3)/(3x(x − 3))`, which "
                  "reduces to `−1/(3x)`."),
            ("p", "That answer is startlingly simple, and it is where the domain "
                  "discipline pays. `−1/(3x)` looks like it excludes only `x = 0`. The "
                  "original excluded `x = 0`, because of `1/x`, and `x = 3`, because the "
                  "main denominator `x − 3` was zero there. Both conditions belong to "
                  "the answer."),
            ("example", ("Two variables",
                         "`(1/x + 1/y)/(1/x − 1/y)`. The LCD of the small denominators "
                         "is `xy`. Multiplying top and bottom by it gives "
                         "`(y + x)/(y − x)`, valid when `x ≠ 0`, `y ≠ 0` and `x ≠ y` "
                         "&mdash; the last because the original lower half is zero when "
                         "`1/x = 1/y`.")),
            ("p", "That third condition is the one worth pausing on. It does not come "
                  "from a denominator at all; it comes from the requirement that the "
                  "thing you are dividing by is not zero. In a complex fraction the "
                  "divisor is an expression, so you have to ask when that expression "
                  "vanishes."),
        ],
        "lab": ("rationalfn", {
            "mode": "complex",
            "panel_title": "Both methods, side by side",
            "panel_intro": "The lab clears the same complex fraction twice &mdash; "
                           "combine-then-divide, and multiply-through-by-the-LCD "
                           "&mdash; and prints the two results for comparison.",
        }),
        "steps_title": "Clearing a complex fraction",
        "steps_intro": "Method 2, which is the one to reach for by default.",
        "steps": [
            ("Find every small denominator",
             "Look in the numerator and the denominator both. In "
             "`(1/x − 1/3)/(x − 3)` they are `x` and `3`; the `x − 3` is the main "
             "denominator, not a small one."),
            ("Take their LCD and record the exclusions",
             "Here the LCD is `3x`. Every small denominator's zeros are excluded, and so "
             "are the zeros of the whole lower half."),
            ("Multiply the whole top and the whole bottom by it",
             "Both halves, in their entirety &mdash; brackets around each before you "
             "distribute. Every small fraction disappears in this one step."),
            ("Simplify what is left",
             "You now have an ordinary rational expression. Factor, cancel, and attach "
             "the exclusions from step two."),
        ],
        "worked": {
            "title": "Simplify (1/x − 1/3)/(x − 3)",
            "intro": ["Method 2, with the sign flip at the end and a numerical check."],
            "lines": [
                "(1/x − 1/3) / (x − 3)",
                "",
                "small denominators:  x  and  3        LCD = 3x",
                "exclusions:   x ≠ 0   (from 1/x)      x ≠ 3   (main denominator)",
                "",
                "multiply top and bottom by 3x:",
                "=  (3x·(1/x) − 3x·(1/3)) / (3x(x − 3))",
                "=  (3 − x) / (3x(x − 3))",
                "",
                "3 − x  =  −(x − 3)",
                "=  −(x − 3) / (3x(x − 3))",
                "=  −1/(3x),          x ≠ 0,  x ≠ 3",
                "",
                "check at x = 1 :   (1 − 1/3)/(1 − 3)  =  (2/3)/(−2)  =  −1/3",
                "                   −1/(3·1)  =  −1/3       ✓",
            ],
            "after": [
                "The answer is a single small fraction with no memory of where it came "
                "from. Nothing in `−1/(3x)` suggests that `x = 3` is forbidden, and it "
                "is: at `x = 3` the original asks you to divide by `0`."
            ],
        },
        "quiz_title": "Clearing the small fractions",
        "quiz": [
            {"q": "By what should you multiply top and bottom to clear "
                  "`(1/2 + 1/x)/(1/4 − 1/x)`?",
             "a": ["`x`", "`4x`", "`2x`", "`8x`"],
             "c": 1,
             "why": "The small denominators are `2`, `x` and `4`. Their LCD is `4x`, "
                    "which every one of them divides. Multiplying by `2x` would leave "
                    "the `1/4` as a half, and `8x` works but drags a factor of `2` "
                    "through the rest of the problem."},
            {"q": "`(1/x + 1/y)/(1/x − 1/y)` simplifies to `(y + x)/(y − x)`. Which "
                  "restriction does NOT come from a denominator of the original?",
             "a": ["`x ≠ 0`", "`y ≠ 0`", "`x ≠ y`", "All three come from denominators"],
             "c": 2,
             "why": "`x ≠ 0` and `y ≠ 0` come from the small fractions. `x ≠ y` comes "
                    "from the lower half `1/x − 1/y` being zero when `x = y` &mdash; you "
                    "would be dividing by zero, even though no single denominator "
                    "vanishes."},
            {"q": "Why may you multiply the numerator and denominator of a complex "
                  "fraction by the same expression?",
             "a": ["Because multiplying an equation by anything is allowed",
                   "Because `(A)/(B) = (AM)/(BM)` for any non-zero `M`",
                   "Because the fractions cancel anyway",
                   "Because it is the same as adding `M` to both parts"],
             "c": 1,
             "why": "It is the fundamental principle of lesson 2. The condition `M ≠ 0` "
                    "matters: it is why the values that make the LCD zero must be "
                    "excluded rather than quietly used. And this is an expression, not "
                    "an equation &mdash; there are no two sides here."},
        ],
        "mistakes": [
            ("Multiplying only part of the numerator by the LCD",
             "The LCD multiplies the whole of the top and the whole of the bottom. "
             "Bracket each half first; `3x·(1/x − 1/3)` is `3 − x`, not `3 − 1/3`."),
            ("Losing the main denominator's exclusion",
             "In `(1/x − 1/3)/(x − 3)` the value `x = 3` is excluded even though `x − 3` "
             "never appears in the final `−1/(3x)`. It was the divisor."),
            ("Forgetting that the lower half can be zero without a denominator being zero",
             "`1/x − 1/y` is zero when `x = y`, and dividing by it is undefined there. "
             "The rule is about the divisor's value, not about its denominators."),
        ],
        "standard": ("Finish when you can do one both ways and get the same thing twice.",
                     "Take any complex fraction, clear it by combining and dividing, then "
                     "clear it again by multiplying through by the LCD, and confirm the "
                     "two answers agree. Being able to check yourself without a solution "
                     "key is the point; the two methods are independent."),
        "note": "The lab runs both methods on whatever you type and prints the results "
                "side by side. They were computed separately, so agreement is evidence "
                "rather than decoration &mdash; and where the answers look different, "
                "they are the same expression written two ways, which is itself worth "
                "seeing.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "solving-rational-equations",
        "title": "Solving Rational Equations",
        "module": "Rational equations",
        "one_line": "Clear the denominators, solve, then test every candidate in the original equation.",
        "summary": (
            "Multiplying an equation by the LCD turns it into a polynomial equation you "
            "can already solve. That step is legal and it is not reversible, so it can "
            "hand you numbers that solve the new equation and not the old one."
        ),
        "key": [
            "multiply BOTH sides by the LCD  ⟹  a polynomial equation",
            "the step is not reversible where the LCD is zero",
            "a candidate equal to an excluded value is EXTRANEOUS",
            "the check is part of the method, not politeness",
        ],
        "key_label": "One legal step that costs you a check",
        "concepts_intro": (
            "This is the first lesson where an entirely correct piece of algebra can "
            "produce a wrong answer. Understanding why is more useful than remembering "
            "to check."
        ),
        "concepts": [
            ("Clearing denominators is the whole method",
             "Multiply every term on both sides by the LCD. The denominators cancel and "
             "you are left with a linear or quadratic equation from courses 2 and 6."),
            ("The step only runs one way",
             "If `A = B` then `A·M = B·M`, for any `M` at all. The converse needs "
             "`M ≠ 0`, because `A·0 = B·0` holds for every `A` and `B`. So solutions of "
             "the cleared equation need not be solutions of the original."),
            ("An extraneous root is not a mistake",
             "It is the predictable residue of a legal step. You cannot avoid it by "
             "being careful; you can only detect it, by substituting into the equation "
             "you were actually given."),
        ],
        "read_title": "Clearing denominators, and what it costs",
        "read_intro": "The method, the reason it leaks, and the check that plugs it.",
        "body": [
            ("p", "The method is short. Factor every denominator, list the excluded "
                  "values, multiply both sides by the LCD, solve whatever polynomial "
                  "equation appears, and then test each candidate in the original."),
            ("def", ("Extraneous solution",
                     "An <strong>extraneous solution</strong> is a value that satisfies "
                     "an equation derived from the original but not the original itself. "
                     "For rational equations these are precisely the candidates that are "
                     "excluded values.")),
            ("p", "The mechanism is worth stating exactly. Multiplying both sides by the "
                  "LCD is multiplication by an expression whose value depends on `x`. At "
                  "an excluded value that expression is `0`, and multiplying an equation "
                  "by `0` produces `0 = 0` &mdash; true regardless of what the original "
                  "said."),
            ("thm", ("Why the check is required",
                     "`A = B` implies `AM = BM` always. `AM = BM` implies `A = B` only "
                     "when `M ≠ 0`. Clearing denominators uses the first implication, so "
                     "the solution set can only grow, never shrink. Every candidate must "
                     "be tested against the original.")),
            ("example", ("An equation with no solution at all",
                         "`x/(x − 3) = 3/(x − 3) + 2`. The LCD is `x − 3`, and `x = 3` is "
                         "excluded. Clearing gives `x = 3 + 2(x − 3)`, so `x = 2x − 3` "
                         "and `x = 3`. The only candidate is the excluded value, so it is "
                         "extraneous and the equation has no solution.")),
            ("p", "Nothing went wrong there. The algebra is correct at every line; the "
                  "equation simply has no solution, and the method's honest report of "
                  "that fact takes the form of a candidate you must throw away."),
            ("p", "A quadratic can produce two candidates of which only one survives, "
                  "and that is the case worth practising, because discarding both is "
                  "easy and discarding neither is easier still."),
            ("example", ("One survivor",
                         "`1/(x − 2) + 1/x = (x² + x − 4)/(x(x − 2))` has LCD "
                         "`x(x − 2)` and exclusions `x ≠ 0`, `x ≠ 2`. Clearing gives "
                         "`x + (x − 2) = x² + x − 4`, that is `x² − x − 2 = 0`, or "
                         "`(x − 2)(x + 1) = 0`. The candidates are `2` and `−1`; `2` is "
                         "excluded, `−1` checks out, and the solution set is `{−1}`.")),
            ("p", "Substitute into the <em>original</em> equation, never into the cleared "
                  "one. Every candidate satisfies the cleared equation by construction, "
                  "so checking there confirms nothing at all &mdash; it is the one test "
                  "guaranteed to pass."),
            ("p", "One special case deserves a name. When both sides have the same "
                  "denominator, or the equation is a single fraction equal to a single "
                  "fraction, clearing is the familiar cross-multiplication: "
                  "`a/b = c/d` becomes `ad = bc`. It is the same step, with the same "
                  "obligation to check."),
        ],
        "lab": ("rationalfn", {
            "mode": "solve",
            "panel_title": "Every candidate, substituted back",
            "panel_intro": "The lab clears the denominators, solves exactly, and then "
                           "substitutes each candidate into the ORIGINAL equation. An "
                           "extraneous root is shown failing that test, not dropped.",
        }),
        "steps_title": "Solving a rational equation",
        "steps_intro": "Four steps, and the fourth is not optional.",
        "steps": [
            ("Factor the denominators and list the exclusions",
             "Before any solving. These are the values that will disqualify a candidate "
             "later, and they are easiest to find now."),
            ("Multiply both sides by the LCD",
             "Every term on both sides, including terms that are not fractions. Bracket "
             "each numerator as you go, exactly as in lesson 4."),
            ("Solve the polynomial equation",
             "Linear, or quadratic by factoring or the formula. This part uses nothing "
             "from this course."),
            ("Test every candidate in the original",
             "Any candidate on the exclusion list is extraneous and is discarded. State "
             "the surviving solution set, which may be empty."),
        ],
        "worked": {
            "title": "Solve 1/(x − 2) + 1/x = (x² + x − 4)/(x(x − 2))",
            "intro": ["Two candidates come out of the quadratic. One of them is not a "
                      "solution of the equation we were given."],
            "lines": [
                "1/(x − 2) + 1/x  =  (x² + x − 4)/(x(x − 2))",
                "",
                "exclusions:   x ≠ 0,   x ≠ 2          LCD = x(x − 2)",
                "",
                "multiply both sides by x(x − 2):",
                "x + (x − 2)  =  x² + x − 4",
                "2x − 2  =  x² + x − 4",
                "0  =  x² − x − 2",
                "0  =  (x − 2)(x + 1)",
                "",
                "candidates:   x = 2   and   x = −1",
                "",
                "x = 2  is an excluded value   ⟹   EXTRANEOUS, discard",
                "",
                "x = −1 :   LHS  =  1/(−3) + 1/(−1)  =  −1/3 − 1  =  −4/3",
                "           RHS  =  (1 − 1 − 4)/((−1)(−3))  =  −4/3     ✓",
                "",
                "solution set:   { −1 }",
            ],
            "after": [
                "The candidate `x = 2` is not a slip. It is the value at which the LCD "
                "`x(x − 2)` is zero, so it is exactly the value at which multiplying "
                "through stopped being reversible. The method predicts where its own "
                "failures will appear, which is why the exclusion list is written first.",
                "Course 5 does this twice: lesson 11 squares both sides of a radical "
                "equation, which is legal in the same one-way manner and produces "
                "extraneous roots for the same structural reason.",
            ],
        },
        "quiz_title": "Candidates and solutions",
        "quiz": [
            {"q": "Solving `x/(x − 4) = 4/(x − 4) + 3` gives the single candidate "
                  "`x = 4`. The solution set is:",
             "a": ["`{4}`", "The empty set", "`{0}`", "All real numbers"],
             "c": 1,
             "why": "`x = 4` makes the denominator `x − 4` zero, so it is an excluded "
                    "value and the candidate is extraneous. With no candidates left the "
                    "equation has no solution, which is a complete and correct answer."},
            {"q": "Why can clearing denominators introduce a false solution?",
             "a": ["Because the arithmetic gets harder",
                   "Because you multiplied by an expression that is zero at that value",
                   "Because quadratics always have two roots",
                   "Because the LCD was not the least one"],
             "c": 1,
             "why": "`AM = BM` gives back `A = B` only when `M ≠ 0`. At an excluded "
                    "value the LCD is zero, the cleared equation holds automatically, "
                    "and the original may say nothing of the kind."},
            {"q": "Where should a candidate be substituted to check it?",
             "a": ["Into the cleared polynomial equation",
                   "Into the original rational equation",
                   "Into either &mdash; they have the same solutions",
                   "Into the LCD"],
             "c": 1,
             "why": "Every candidate satisfies the cleared equation by construction, so "
                    "that test always passes and tells you nothing. Only the original "
                    "can reject an extraneous root, because only the original has the "
                    "denominators that exclude it."},
        ],
        "mistakes": [
            ("Skipping the check because the algebra looked clean",
             "The algebra usually is clean. Extraneous roots come from a correct step, "
             "not a careless one, so tidy work is no evidence at all that a candidate "
             "is genuine."),
            ("Checking in the cleared equation",
             "That equation was built to be satisfied by every candidate. It is the one "
             "place where the test cannot fail and therefore cannot help."),
            ("Reporting no solution as an error",
             "An equation may genuinely have no solution. \"No solution\" is the answer "
             "in those cases, and it is not the same as \"I could not solve it\"."),
        ],
        "standard": ("Finish when you can explain the extraneous root, not just remove it.",
                     "Given a rational equation you should list the exclusions before "
                     "solving, clear correctly, test each candidate in the original, and "
                     "say why the discarded one appeared &mdash; naming the value at "
                     "which the LCD was zero. That explanation is what transfers to "
                     "lesson 11."),
        "note": "The lab never silently drops a root. Each candidate is substituted into "
                "the original equation in front of you and the two sides are printed as "
                "exact fractions, so an extraneous root is seen failing rather than "
                "asserted to fail &mdash; and a genuine one is seen passing.",
    },
]
