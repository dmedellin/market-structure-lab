"""Course 7, lessons 07-12 — the two named bases, both kinds of equation, and the models."""

LESSONS = [
    # ---------------------------------------------------------------- 07
    {
        "slug": "common-and-natural-logarithms",
        "title": "Common and Natural Logarithms",
        "module": "Logarithms",
        "one_line": "Base 10 and base e, and the notation for each.",
        "summary": (
            "Two bases are used often enough to get their own notation: `log x` means "
            "base 10 and `ln x` means base `e`. Neither is a new function &mdash; both "
            "are the logarithm of lesson 4 &mdash; but the abbreviations mean different "
            "things in different subjects, and the split of `log(a · 10^k)` into an "
            "exact integer and an irrational remainder is worth doing once by hand."
        ),
        "key": [
            "log x  =  log_10(x)      the common logarithm",
            "ln x   =  log_e(x)       the natural logarithm,  e = 2.71828…",
            "log 4500 = log(4.5 · 10^3) = 3 + 0.6532…    integer + remainder",
            "ln x = ln 10 · log x ≈ 2.302585 · log x     one constant apart",
        ],
        "key_label": "Two abbreviations, one definition",
        "concepts_intro": (
            "Neither notation adds a rule. Each names a base that comes up often enough "
            "to be worth an abbreviation."
        ),
        "concepts": [
            ("log means base 10 here, and that is a convention",
             "Written with no base at all, `log` is base 10 in this course, on a "
             "calculator key, and in school algebra generally. In an analysis text it "
             "usually means base `e`; in a complexity bound it usually means base 2. "
             "The symbol does not carry its base, the subject does, and the convention "
             "is arbitrary."),
            ("ln is the logarithm of the compounding base",
             "`ln x` means `log_e(x)`, with `e = 2.71828…` produced in lesson 3 by "
             "compounding faster and faster. Anything written with `e` &mdash; "
             "`A = P · e^(rt)` in lesson 11, every continuous decay &mdash; is undone "
             "by `ln` and by nothing else."),
            ("The integer part of a common logarithm is free",
             "`log(4.5 · 10^3) = 3 + log 4.5`. The `3` is exact and comes from the "
             "power of ten; the remainder lies in `[0, 1)` and is the part that cannot "
             "be written down exactly. That split is why a printed logarithm table "
             "needed only the digits from `1.00` to `9.99`."),
        ],
        "read_title": "Two named bases",
        "read_intro": "The definitions, the identities they inherit, and the one piece of arithmetic worth doing by hand.",
        "body": [
            ("def", ("Common logarithm",
                     "`log x`, written with no base, means `log_10(x)`: the exponent to "
                     "which `10` must be raised to give `x`. Its domain is `x &gt; 0`, "
                     "as for every logarithm.")),
            ("def", ("Natural logarithm",
                     "`ln x` means `log_e(x)`, where `e = 2.71828…` is the number lesson "
                     "3 obtained as a limit. The name is historical &mdash; "
                     "<em>logarithmus naturalis</em> &mdash; and `e` is not a more "
                     "natural base for arithmetic than any other. It is the base in "
                     "which continuous growth is written, which is the only reason this "
                     "course needs it.")),
            ("p", "Nothing about the two definitions is new. Every statement from lesson "
                  "4 onwards applies to them unchanged, because they are instances of "
                  "the same definition and not a second kind of object."),
            ("math", [
                "log 10 = 1              ln e = 1",
                "log 1  = 0              ln 1 = 0",
                "log(10^k) = k           ln(e^k) = k        for every real k",
                "10^(log x) = x          e^(ln x) = x       for every x > 0",
            ]),
            ("p", "The two bottom lines are the same fact in the two possible orders, "
                  "and they carry different conditions for a reason. `log(10^k) = k` "
                  "holds for every real `k` because `10^k` is positive whatever `k` is. "
                  "`10^(log x) = x` needs `x &gt; 0` first, because otherwise `log x` "
                  "does not exist to be exponentiated."),
            ("h3", "The integer part and the remainder"),
            ("p", "Write a positive number in scientific notation as `a · 10^k` with "
                  "`1 ≤ a &lt; 10` and `k` an integer. The product law of lesson 6 then "
                  "splits its common logarithm into two pieces: `log(a · 10^k) = "
                  "log a + k`. The `k` is an exact integer. The `log a` lies between `0` "
                  "and `1`, and for a rational `a` other than `1` it is irrational, so it "
                  "is a decimal that has been rounded and should be labelled as such."),
            ("p", "The two pieces have names that survive from the era of printed tables. "
                  "`k` is the <strong>characteristic</strong> and `log a` is the "
                  "<strong>mantissa</strong>. A table listed mantissas only: every number "
                  "with the digits `45` shares one, and the power of ten was supplied by "
                  "the reader."),
            ("example", ("Three numbers, one mantissa",
                         "`log 4.5 ≈ 0.6532`. Then `log 45 ≈ 1.6532`, `log 4500 ≈ 3.6532` "
                         "and `log 450000 ≈ 5.6532`. Only the characteristic moved, "
                         "because only the power of ten changed.")),
            ("p", "Below `1` the arithmetic stops being cosmetic. "
                  "`log 0.00045 = log(4.5 · 10^−4) = −4 + 0.6532 = −3.3468`, and the "
                  "digits `6532` are nowhere in the answer. Tables wrote such a value as "
                  "a negative characteristic with a positive mantissa kept separate, "
                  "precisely so that the shared `0.6532` stayed visible."),
            ("p", "One use of the characteristic outlives the tables. The number of "
                  "digits in a positive integer `N` is `⌊log N⌋ + 1`, where the brackets "
                  "mean round down to an integer. So `2^100` has "
                  "`⌊100 · log 2⌋ + 1 = ⌊30.103⌋ + 1 = 31` digits &mdash; a fact about a "
                  "31-digit number obtained without writing any of it down."),
            ("thm", ("The two logarithms are proportional",
                     "For every `x &gt; 0`, `ln x = ln 10 · log x`, and `ln 10 ≈ 2.302585`.",
                     "So the natural logarithm of a number is always about `2.3` times "
                     "its common logarithm: `log 500 ≈ 2.6990` and `ln 500 ≈ 6.2146`. "
                     "Lesson 8 shows that every pair of bases is related by a constant of "
                     "exactly this kind, and derives it in two lines.")),
            ("p", "That proportionality is also the practical reason the two abbreviations "
                  "are enough. A calculator offers `log` and `ln` and no other base; "
                  "everything else is computed from one of them."),
        ],
        "lab": ("logarithm", {
            "mode": "common",
            "panel_title": "The exact part and the rounded part",
            "panel_intro": "Enter a number and watch its common logarithm split: the "
                           "power of ten is found as an integer and is exact, and what "
                           "remains is printed as a rounding and says so. The base-e "
                           "column beside it is the same number needing a different "
                           "exponent.",
        }),
        "steps_title": "Reading a common logarithm off a number",
        "steps_intro": "Four steps, and the first one decides the only exact digit in the answer.",
        "steps": [
            ("Write the number in scientific notation",
             "`a · 10^k` with `1 ≤ a &lt; 10` and `k` an integer. This is what fixes the "
             "characteristic; a number written as `45 · 10^2` gives the wrong one."),
            ("Take the logarithm of each factor",
             "`log(a · 10^k) = log a + log(10^k) = log a + k`, by the product law and "
             "then by the definition. The second term needs no computation at all."),
            ("Get the mantissa from a table or a calculator",
             "`0 ≤ log a &lt; 1` always, because `1 ≤ a &lt; 10`. For a rational `a` "
             "other than `1` this value is irrational, so whatever you write is rounded "
             "and the number of places should be stated."),
            ("Add, keeping the characteristic's sign on the characteristic",
             "For `a · 10^−4` the sum is `−4 + (mantissa)`, not `−(4 + mantissa)`. The "
             "printed decimal will not show the mantissa's digits, and that is correct."),
        ],
        "worked": {
            "title": "One mantissa, three numbers",
            "intro": [
                "`log 4.5 = 0.6532` to four places. Every number whose digits are `45` "
                "shares that value; only the power of ten changes.",
            ],
            "lines": [
                "log 45      = log(4.5 · 10^1)  =   1 + 0.6532  =   1.6532",
                "log 4500    = log(4.5 · 10^3)  =   3 + 0.6532  =   3.6532",
                "log 0.00045 = log(4.5 · 10^−4) =  −4 + 0.6532  =  −3.3468",
                "                                  ↑      ↑",
                "                                  |      mantissa: rounded, in [0, 1)",
                "                                  characteristic: an exact integer",
                "",
                "check the last line:   10^−4 < 0.00045 < 10^−3",
                "                       so the logarithm lies between −4 and −3   ✓",
            ],
            "after": [
                "The third line is the one to slow down on. Adding a positive mantissa to "
                "a negative characteristic gives `−3.3468`, and none of the digits "
                "`6532` appear in it. Read too quickly, the answer looks like a "
                "different mantissa, which is exactly why tables kept the two pieces "
                "apart instead of adding them.",
                "The bracket at the bottom is the check that costs nothing. Any number "
                "between `10^−4` and `10^−3` has a common logarithm between `−4` and "
                "`−3`, so an answer of `−4.6532` can be rejected before the "
                "arithmetic is looked at. It does not catch everything: `−3.6532` "
                "does lie between `−4` and `−3`, and only the addition "
                "`−4 + 0.6532 = −3.3468` rules that one out.",
            ],
        },
        "quiz_title": "Which base, and what value",
        "quiz": [
            {"q": "What is `log 1000`?",
             "a": ["`100`", "`3`", "`10^3`", "`1/3`"],
             "c": 1,
             "why": "`log` with no base means base 10, and `10^3 = 1000`, so the "
                    "logarithm is the exponent `3`. `100` divides by `10` instead of "
                    "asking for an exponent, and `10^3` is the number you started with "
                    "rather than its logarithm."},
            {"q": "`ln(e^7)` is:",
             "a": ["`7`", "`e^7`", "`7e`", "`ln 7`"],
             "c": 0,
             "why": "`ln` and `e^x` undo one another: `ln(e^k) = k` for every real `k`. "
                    "Nothing is computed and nothing is rounded. `7e` multiplies where "
                    "the identity cancels, and `ln 7 ≈ 1.9459` is the logarithm of the "
                    "exponent rather than the exponent itself."},
            {"q": "Given `log 4.5 ≈ 0.6532`, what is `log 0.00045`?",
             "a": ["`−3.6532`", "`−3.3468`", "`−4.6532`", "`3.3468`"],
             "c": 1,
             "why": "`0.00045 = 4.5 · 10^−4`, so the value is `−4 + 0.6532 = −3.3468`. "
                    "`−4.6532` subtracts the mantissa instead of adding it; `−3.6532` "
                    "writes the mantissa's digits after the point of the answer; "
                    "`3.3468` drops the sign of the characteristic. The bracket "
                    "`10^−4 &lt; 0.00045 &lt; 10^−3` rejects `−4.6532` and "
                    "`3.3468` outright; `−3.6532` lies between `−4` and `−3` and "
                    "survives the bracket, so only the addition rules it out."},
        ],
        "mistakes": [
            ("Assuming a bare log means base 10 everywhere",
             "It does here and on a calculator. It means base `e` in most analysis and "
             "base 2 in most of computer science. The values differ by a constant "
             "factor, so a formula carried across that boundary is wrong by that factor "
             "and looks entirely plausible."),
            ("Treating ln as a function with its own rules",
             "`ln` is `log_e` and nothing else. Every law of lesson 6 applies to it "
             "unchanged: `ln(MN) = ln M + ln N`, `ln(M^p) = p · ln M`. There is no "
             "second set of laws to learn, and the invented ones are invented for `ln` "
             "too."),
            ("Splitting a logarithm below 1 into the wrong two pieces",
             "`log 0.00045` is `−4 + 0.6532`. It is not `−4 − 0.6532` and not "
             "`−(4 + 0.6532)`. The mantissa is non-negative by construction, since "
             "`1 ≤ a &lt; 10` forces `0 ≤ log a &lt; 1`; only the characteristic can "
             "be negative."),
        ],
        "standard": ("Finish when you can say what base a bare log has, and give the exact part of one.",
                     "Given `log 6.3 ≈ 0.7993`, you should be able to write "
                     "`log 63000 ≈ 4.7993` and `log 0.0000063 ≈ −5.2007` without a "
                     "calculator, and say which digits of each are exact and which "
                     "are a rounding. Producing the decimal without knowing which half "
                     "is which is the habit this lesson is trying to break."),
        "note": "The constant `2.302585…` relating `ln` and `log` is not a special fact "
                "about `10` and `e`. Every pair of legal bases is related by a constant "
                "of the same shape, and the next lesson produces it from the definition "
                "in two lines.",
    },
    # ---------------------------------------------------------------- 08
    {
        "slug": "change-of-base",
        "title": "Change of Base",
        "module": "Logarithms",
        "one_line": "Computing a logarithm in any base from one you have.",
        "summary": (
            "A calculator offers two bases and there are infinitely many. One identity "
            "closes the gap: `log_b(x) = log_c(x) / log_c(b)` for any base `c` you can "
            "actually compute. It follows in two lines from the definition and the power "
            "law, and the derivation is what keeps the argument and the base the right "
            "way up."
        ),
        "key": [
            "log_b(x) = log_c(x) / log_c(b)        for any c > 0, c ≠ 1",
            "log_2(10) = ln 10 / ln 2 = log 10 / log 2 ≈ 3.321928",
            "log_b(x) = 1 / log_x(b)               the case c = x",
            "NOT log_c(x/b)   and NOT log_c(x) − log_c(b)",
        ],
        "key_label": "The identity, one corollary, and the trap",
        "concepts_intro": (
            "One theorem, proved from the definition, plus a clear view of the two "
            "expressions it is constantly confused with."
        ),
        "concepts": [
            ("The identity is a division, not a subtraction",
             "`log_c(x) / log_c(b)` is a quotient of two logarithms. Lesson 6 has no law "
             "for such a quotient: it is not `log_c(x/b)`, and it is not "
             "`log_c(x) − log_c(b)`. Writing the division deliberately, with the base of "
             "the answer underneath, is most of the work of this lesson."),
            ("Every logarithm is a constant multiple of every other",
             "Take `c = e` and the identity reads `log_b(x) = (1 / ln b) · ln x`. So the "
             "graph of any logarithm is the graph of `ln` stretched vertically by a fixed "
             "factor &mdash; and reflected as well when `0 &lt; b &lt; 1`, since `ln b` "
             "is then negative. The bases differ by a scale, never by a shape."),
            ("The helper base is free, so it is also a check",
             "The identity holds for every legal `c`. Three different helper bases give "
             "three quotients that look nothing alike and must agree to every digit. "
             "When a numeric answer looks wrong, that is the cheapest test available."),
        ],
        "read_title": "Changing the base of a logarithm",
        "read_intro": "The statement, its two-line proof, the corollaries, and what it is not.",
        "body": [
            ("p", "`log_2(10)` is a perfectly definite number: the exponent that turns "
                  "`2` into `10`. It is between `3` and `4`, since `2^3 = 8` and "
                  "`2^4 = 16`. No calculator has a base-2 logarithm key, and no table "
                  "was ever printed for base 2. The identity below is how the number is "
                  "obtained anyway."),
            ("thm", ("Change of base",
                     "Let `b` and `c` be positive with `b ≠ 1` and `c ≠ 1`, and let "
                     "`x &gt; 0`. Then `log_b(x) = log_c(x) / log_c(b)`.")),
            ("proof", [
                "Let `y = log_b(x)`. By the definition in lesson 4, that says exactly "
                "`b^y = x`.",
                "Equal numbers have equal logarithms, so apply `log_c` to both sides: "
                "`log_c(b^y) = log_c(x)`. The power law of lesson 6 turns the left side "
                "into `y · log_c(b)`.",
                "Divide both sides by `log_c(b)`. That step is legal because "
                "`log_c(b) = 0` happens only when `b = 1`, and the hypothesis excluded "
                "it. What is left is `y = log_c(x) / log_c(b)`, which is the claim.",
            ]),
            ("p", "Read the result once more for placement. The <em>argument</em> goes "
                  "on top and the <em>base of the answer</em> goes underneath. "
                  "`log_2(10)` is `ln 10 / ln 2`, not `ln 2 / ln 10`. Both quotients are "
                  "real numbers and neither looks broken: the first is about `3.3219` "
                  "and the second about `0.3010`."),
            ("math", [
                "log_2(10) = log 10 / log 2 = 1.000000 / 0.301030 ≈ 3.321928",
                "          = ln 10  / ln 2  = 2.302585 / 0.693147 ≈ 3.321928",
                "",
                "check:  2^3 = 8 < 10 < 16 = 2^4     so the answer lies between 3 and 4",
                "",
                "the reversed quotient:  ln 2 / ln 10 ≈ 0.301030 = log_10(2)",
            ]),
            ("h3", "Two corollaries"),
            ("p", "Put `c = x`. Then `log_x(x) = 1`, and the identity collapses to "
                  "`log_b(x) = 1 / log_x(b)`. The pair `log_2(8) = 3` and "
                  "`log_8(2) = 1/3` is that statement with numbers in it, and it is a "
                  "useful sanity check whenever a logarithm and its mirror image both "
                  "appear in a problem."),
            ("p", "Put `c = e`. Then `log_b(x) = ln x / ln b = (1 / ln b) · ln x`, so "
                  "each logarithm function is a fixed multiple of the natural one. For "
                  "base 2 that multiple is `1 / ln 2 ≈ 1.442695`; for base 10 it is "
                  "`1 / ln 10 ≈ 0.434294`. Lesson 7's `ln x ≈ 2.302585 · log x` is the "
                  "same statement with the two bases swapped."),
            ("example", ("An exact answer stays exact",
                         "`log_8(32)` is not a decimal problem. Both numbers are powers "
                         "of `2`, so change to base 2: "
                         "`log_8(32) = log_2(32) / log_2(8) = 5/3`. Check it against the "
                         "definition: `8^(5/3) = (2^3)^(5/3) = 2^5 = 32`. Changing base "
                         "does not force an approximation; choosing a helper base in "
                         "which both numbers are recognisable powers avoids one.")),
            ("p", "Now the trap, on numbers. Take `log_5(40)`. The identity gives "
                  "`log 40 / log 5 = 1.602060 / 0.698970 ≈ 2.292030`. The two "
                  "expressions it is confused with are `log(40/5) = log 8 ≈ 0.903090` "
                  "and `log 40 − log 5`, which is the same `log 8`. Neither is close to "
                  "the answer, and neither is a law."),
            ("p", "There is one more reason to know the identity even on a calculator "
                  "that accepts any base. It is what proves that two people computing "
                  "the same logarithm in different bases must agree, and in lesson 9 it "
                  "is what turns `x = log_5(17)` from a name for the answer into a "
                  "number."),
        ],
        "lab": ("logarithm", {
            "mode": "base",
            "panel_title": "Three helper bases, one value",
            "panel_intro": "The identity is derived on the page and then checked: the "
                           "same logarithm is computed through three different helper "
                           "bases, which must agree. Exact answers are found as "
                           "fractions before any decimal is printed.",
        }),
        "steps_title": "Evaluating a logarithm in an unfamiliar base",
        "steps_intro": "Four steps, and the first one often ends the problem with an exact fraction.",
        "steps": [
            ("Ask whether the answer is exact",
             "Write `x` and `b` as powers of one common base. `log_8(32)` becomes "
             "`log_2(2^5) / log_2(2^3) = 5/3`, with no decimal anywhere."),
            ("Otherwise pick a helper base you can compute",
             "On a calculator that means `10` or `e`; either is fine and both give the "
             "same value. By hand it means whichever base makes the two numbers "
             "recognisable."),
            ("Put the argument on top and the base underneath",
             "`log_b(x) = log_c(x) / log_c(b)`. Say it in that order before writing it. "
             "The reversed quotient is a real number and the calculator will not object, "
             "so nothing downstream will look wrong."),
            ("Bracket the answer between two integer powers",
             "Find `k` with `b^k &lt; x &lt; b^(k+1)`; the logarithm lies between `k` "
             "and `k + 1`. This catches a reversed quotient immediately, since the "
             "reciprocal is almost never in the same interval."),
        ],
        "worked": {
            "title": "log_5(40), computed three ways",
            "intro": [
                "`40` is not a power of `5`, so no exact answer exists and a decimal is "
                "the honest output. Three helper bases must still produce the same one.",
            ],
            "lines": [
                "bracket first:   5^2 = 25 < 40 < 125 = 5^3",
                "                 so log_5(40) lies between 2 and 3",
                "",
                "base 10:   log 40   / log 5   = 1.602060 / 0.698970 ≈ 2.292030",
                "base e:    ln 40    / ln 5    = 3.688879 / 1.609438 ≈ 2.292030",
                "base 2:    log_2(40)/ log_2(5)= 5.321928 / 2.321928 ≈ 2.292030",
                "",
                "the reversed quotient:  log 5 / log 40 ≈ 0.436295   = log_40(5)",
                "the invented law:       log(40/5) = log 8 ≈ 0.903090",
            ],
            "after": [
                "The three quotients agree to every digit shown, which is what the "
                "theorem promises: the helper base cancels out of the answer. All six "
                "logarithms on those three lines are irrational, and every decimal here "
                "is rounded to six places.",
                "The last two lines are not near-misses, they are answers to different "
                "questions. `log_40(5)` is the reciprocal &mdash; the exponent that "
                "turns `40` into `5` &mdash; and `log 8` is the logarithm of a quotient "
                "rather than a quotient of logarithms. The bracket at the top rejects "
                "both without any arithmetic: neither lies between `2` and `3`.",
            ],
        },
        "quiz_title": "Changing base",
        "quiz": [
            {"q": "Which expression equals `log_5(40)`?",
             "a": ["`(ln 40) / (ln 5)`", "`(ln 5) / (ln 40)`", "`ln 40 − ln 5`",
                   "`ln 35`"],
             "c": 0,
             "why": "Argument on top, base underneath. The second is the reciprocal, "
                    "which is `log_40(5) ≈ 0.4363`. The third turns a quotient of "
                    "logarithms into the logarithm of a quotient: `ln 40 − ln 5 = ln 8 "
                    "≈ 2.0794`, close enough to `2.2920` to survive a careless glance. "
                    "The fourth subtracts the arguments, for which there is no law at all."},
            {"q": "`log_8(32)` is exactly:",
             "a": ["`4`", "`5/3`", "`2`", "`3/5`"],
             "c": 1,
             "why": "`32 = 2^5` and `8 = 2^3`, so changing to base 2 gives `5/3`, and "
                    "`8^(5/3) = 2^5 = 32` confirms it. `4` divides the numbers instead of "
                    "their exponents; `2` subtracts the exponents, which is `log_2(32/8)` "
                    "and not this; `3/5` is the quotient upside down, and it equals "
                    "`log_32(8)`."},
            {"q": "Why does the derivation require `b ≠ 1`?",
             "a": ["Because `log_c(1)` is undefined",
                   "Because the last step divides by `log_c(b)`, which is `0` exactly when `b = 1`",
                   "Because `1^y` is undefined",
                   "Because a base of `1` would make the logarithm negative"],
             "c": 1,
             "why": "`log_c(1) = 0`: it is perfectly well defined, and that is the "
                    "problem, because the derivation divides by it. Base `1` was already "
                    "excluded when logarithms were defined, since `1^y = 1` for every `y` "
                    "and can never equal any other `x`."},
        ],
        "mistakes": [
            ("Putting the base on top",
             "`log_b(x) = log x / log b`. Reversed, you get `log_x(b)`, the reciprocal. "
             "It is a real number, the calculator returns it without complaint, and only "
             "a bracket check or the derivation will tell you it is the wrong one."),
            ("Turning the quotient into a difference",
             "`log_c(x) / log_c(b)` is not `log_c(x) − log_c(b)`. For `x = 40` and "
             "`b = 5` in base `e` the two are `2.2920` and `2.0794`: near enough to look "
             "right, far enough to be wrong. There is a law for the logarithm of a "
             "quotient and none for a quotient of logarithms."),
            ("Producing a decimal where a fraction was available",
             "A calculator returns `1.6666667` for `log_8(32)`. The answer is `5/3`, and "
             "every later step that uses it stays exact if you keep the fraction. Look "
             "for a common base before reaching for the keys."),
        ],
        "standard": ("Finish when you can state the identity with the argument and base in the right places, and prove it in two lines.",
                     "The proof is the protection. If you can get there from `b^y = x` "
                     "and the power law, you cannot put `log b` on top by accident, "
                     "because the derivation shows where the denominator came from. "
                     "Memorising the fraction alone leaves a fifty-fifty guess."),
        "note": "This identity is what makes the next lesson finish. Solving `5^x = 17` "
                "gives `x = log_5(17)` straight from the definition, which names the "
                "answer without evaluating it; change of base turns that name into "
                "`ln 17 / ln 5 ≈ 1.760374`.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "solving-exponential-equations",
        "title": "Solving Exponential Equations",
        "module": "Solving",
        "one_line": "Taking a logarithm of both sides to bring the variable down.",
        "summary": (
            "Two methods and one decision. If both sides can be written as powers of the "
            "same base, match the exponents and the answer is exact. If they cannot, "
            "take a logarithm of both sides: the power law is the only tool in this "
            "course that moves a variable out of an exponent."
        ),
        "key": [
            "b^u = b^v   ⟹   u = v            for b > 0, b ≠ 1",
            "b^x = k     ⟹   x = log_b(k) = ln k / ln b      needs k > 0",
            "5 · 2^x = 40   →   2^x = 8   →   x = 3          isolate first",
            "2^x = −8    no solution:  2^x > 0 for every real x",
        ],
        "key_label": "Two methods and two guards",
        "concepts_intro": (
            "Everything here rests on one property of the exponential function and one "
            "law of logarithms."
        ),
        "concepts": [
            ("An exponential function is one-to-one",
             "For `b &gt; 0` with `b ≠ 1`, `b^u = b^v` forces `u = v`. That is what "
             "licenses cancelling the base and comparing exponents. It is the same "
             "property that gave the exponential an inverse in lesson 5, and it fails at "
             "`b = 1`, where `1^u = 1^v` for every pair of exponents."),
            ("The power law is what moves the variable",
             "`log(M^p) = p · log M` takes the exponent and writes it in front. Nothing "
             "else in algebra does this: dividing, factoring and squaring all leave `x` "
             "exactly where it was. When the same-base method fails, this law is the "
             "only route left."),
            ("Isolate the power before taking a logarithm",
             "Taking `log` of both sides of `5 · 2^x = 40` is legal and gives "
             "`log 5 + x · log 2 = log 40`, which does solve. It is also the line where "
             "`log(5 · 2^x)` gets expanded wrongly. Dividing by `5` first leaves "
             "`2^x = 8`, where the power law has a clean target and there is nothing to "
             "invent."),
        ],
        "read_title": "Bringing the variable down",
        "read_intro": "The same-base method, the logarithm method, the substitution that hides a quadratic, and the equations with no solution at all.",
        "body": [
            ("p", "Every equation before this course put the unknown in the base: "
                  "`x² = 9`, `x³ − x = 0`. `3^(2x − 1) = 81` puts it in the exponent, and "
                  "no amount of dividing, factoring or root-taking will move it. Two "
                  "methods do."),
            ("thm", ("Exponentials are one-to-one",
                     "For `b &gt; 0` with `b ≠ 1`: `b^u = b^v` if and only if `u = v`.",
                     "The forward direction is what solves equations. The reverse "
                     "direction is why substituting an answer back in works. Both "
                     "statements fail for `b = 1`, which is why that base is excluded "
                     "everywhere in this course.")),
            ("example", ("Matching powers",
                         "`3^(2x − 1) = 81`. Since `81 = 3^4`, both sides are powers of "
                         "`3`: `3^(2x − 1) = 3^4`. One-to-one gives `2x − 1 = 4`, so "
                         "`x = 5/2`. The answer is exact and no logarithm was needed. "
                         "Check: `2 · (5/2) − 1 = 4` and `3^4 = 81`.")),
            ("p", "That method needs both sides to be recognisable powers of one base. "
                  "`5^x = 17` is not such an equation. `17` lies between `5^1 = 5` and "
                  "`5^2 = 25`, and it is not a rational power of `5` at all: "
                  "`5^(p/q) = 17` would mean `5^p = 17^q`, which no positive integers "
                  "satisfy, since one side is divisible by `5` and the other is not."),
            ("thm", ("Taking a logarithm of both sides",
                     "If `M = N` and both are positive, then `log_c(M) = log_c(N)` for "
                     "every legal base `c`; and conversely, `log_c(M) = log_c(N)` forces "
                     "`M = N`.",
                     "So a logarithm may be applied to both sides of an equation exactly "
                     "as `5` may be added to both sides. The two-way statement matters: "
                     "it is what guarantees the new equation has the same solutions as "
                     "the old one, so nothing is gained or lost by the step.")),
            ("math", [
                "5^x = 17",
                "ln(5^x) = ln 17          take ln of both sides; both sides are positive",
                "x · ln 5 = ln 17         power law: the exponent comes down in front",
                "x = ln 17 / ln 5         divide by ln 5, which is not 0",
                "x ≈ 1.760374             rounded to six places",
                "",
                "check:  5^1 = 5 < 17 < 25 = 5^2,   so x lies between 1 and 2   ✓",
            ]),
            ("p", "The exact answer is the quotient `ln 17 / ln 5`, which is "
                  "`log_5(17)` written in a base that can be computed &mdash; lesson 8, "
                  "doing the job it was derived for. The decimal is a rounding of it, "
                  "and any later step should use the quotient."),
            ("h3", "The unknown on both sides"),
            ("p", "When the two sides have different bases and both carry the unknown, "
                  "take a logarithm anyway and then collect. The equation that results is "
                  "linear in `x`, with logarithms as its coefficients."),
            ("math", [
                "4^(x + 1) = 3^(2x)",
                "(x + 1) · ln 4 = 2x · ln 3      ln of both sides, power law twice",
                "x · ln 4 + ln 4 = 2x · ln 3     expand the left side",
                "ln 4 = 2x · ln 3 − x · ln 4     collect the x terms on one side",
                "ln 4 = x · (2 · ln 3 − ln 4)    factor out x",
                "x = ln 4 / (2 · ln 3 − ln 4)",
                "  = ln 4 / ln(9/4)              since 2 ln 3 − ln 4 = ln(9/4)",
                "  ≈ 1.709511",
            ]),
            ("h3", "Equations that hide a quadratic"),
            ("p", "`e^(2x) − e^x − 6 = 0` contains only one exponential, twice: "
                  "`e^(2x) = (e^x)²`. Substituting `u = e^x` turns it into "
                  "`u² − u − 6 = 0`, which factors as `(u − 3)(u + 2) = 0`. So `u = 3` "
                  "or `u = −2`."),
            ("p", "Now undo the substitution, and one candidate dies. `u = e^x` is "
                  "positive for every real `x`, so `u = −2` is impossible &mdash; not "
                  "because of a domain restriction on a logarithm, but because the range "
                  "of the exponential is `(0, ∞)`. From `u = 3`, `x = ln 3 ≈ 1.098612`, "
                  "and that is the whole solution set."),
            ("p", "The same range fact settles two shapes on sight. `b^x = 0` has no "
                  "solution: the horizontal asymptote `y = 0` from lesson 1 is "
                  "approached and never reached. `b^x = k` with `k &lt; 0` has no "
                  "solution either. In both cases the algebra will not object &mdash; "
                  "`ln(−8)` simply does not exist &mdash; so the check has to be made "
                  "before the logarithm, not after."),
        ],
        "lab": ("logarithm", {
            "mode": "solveexp",
            "panel_title": "Match powers, or take a logarithm",
            "panel_intro": "Each equation is attempted both ways: the lab searches for a "
                           "common base and reports the exact exponent when one exists, "
                           "and falls back to logarithms when it does not. The equations "
                           "with no solution are in the list on purpose.",
        }),
        "steps_title": "Solving an exponential equation",
        "steps_intro": "Four steps. The decision in step two is the one that determines whether the answer is exact.",
        "steps": [
            ("Isolate the exponential",
             "Get the power alone on one side. Constants added to it move first, then "
             "coefficients multiplying it &mdash; the same order as in a linear "
             "equation, and for the same reason."),
            ("Ask whether the other side is a power of the same base",
             "If it is, rewrite both sides over that base and set the exponents equal. "
             "The answer is exact, and no rounding enters the problem."),
            ("Otherwise take a logarithm of both sides",
             "Any base works; use `ln` or `log` because they can be evaluated. The power "
             "law brings the whole exponent down in front as a factor, so bracket it "
             "before you write it: `(2x − 1) · ln 3`, never `2x − 1 · ln 3`."),
            ("Solve what is left, and check the sign of the isolated power",
             "After the logarithm the equation is linear in `x` with numeric "
             "coefficients. If the isolated exponential equalled `0` or a negative "
             "number, stop earlier: there is no real solution to find."),
        ],
        "worked": {
            "title": "Three equations, three fates",
            "intro": [
                "The same four steps each time. What differs is where they stop.",
            ],
            "lines": [
                "(1)  3^(2x − 1) = 81",
                "     3^(2x − 1) = 3^4          81 = 3^4: both sides are powers of 3",
                "     2x − 1 = 4                exponentials are one-to-one",
                "     x = 5/2                   exact",
                "     check   3^(2 · 5/2 − 1) = 3^4 = 81                        ✓",
                "",
                "(2)  5 · 2^x + 3 = 43",
                "     5 · 2^x = 40              isolate: subtract 3",
                "     2^x = 8                   isolate: divide by 5",
                "     x = 3                     8 = 2^3, so match the exponents",
                "     check   5 · 2^3 + 3 = 40 + 3 = 43                         ✓",
                "",
                "(3)  7^x = 30",
                "     x · ln 7 = ln 30          30 is not a power of 7; take ln",
                "     x = ln 30 / ln 7          exact",
                "     x ≈ 1.747870              rounded to six places",
                "     check   7^1 = 7 < 30 < 49 = 7^2,  so x is between 1 and 2  ✓",
            ],
            "after": [
                "Equation (2) is the one worth studying. Two isolating steps happen "
                "before anything logarithmic is considered, and once the power stands "
                "alone the right side turns out to be `2^3`, so no logarithm is needed "
                "at all. Taking `log` of `5 · 2^x + 3 = 43` as a first move is legal and "
                "leads nowhere useful, because `log(5 · 2^x + 3)` cannot be expanded: "
                "there is no law for the logarithm of a sum.",
                "In equation (3) the answer is `ln 30 / ln 7`. The decimal is a rounding "
                "of that quotient to six places, and it is not the answer &mdash; if the "
                "value feeds into anything else, carry the quotient and round once, at "
                "the end.",
            ],
        },
        "quiz_title": "Solving for an exponent",
        "quiz": [
            {"q": "Solve `3^(x − 1) = 27^x`.",
             "a": ["`x = −1/2`", "`x = 1/4`", "`x = 1/2`",
                   "No solution &mdash; the `x` terms cancel"],
             "c": 0,
             "why": "`27 = 3^3`, so `27^x = 3^(3x)` and matching exponents gives "
                    "`x − 1 = 3x`, hence `2x = −1` and `x = −1/2`. Check: "
                    "`3^(−3/2) = 27^(−1/2) ≈ 0.19245`. `1/4` comes from moving `3x` to "
                    "the left with the wrong sign; `1/2` from a sign slip in the final "
                    "division; the last option comes from reading `27^x` as `3^(3 + x)`, "
                    "adding exponents where the power-of-a-power law multiplies them."},
            {"q": "`2^x = 20`. Which expression is `x`?",
             "a": ["`ln 20 / ln 2`", "`ln 2 / ln 20`", "`ln 20 − ln 2`", "`10`"],
             "c": 0,
             "why": "`x · ln 2 = ln 20`, so `x = ln 20 / ln 2 ≈ 4.3219`. The reciprocal "
                    "`≈ 0.2314` is `log_20(2)`; `ln 20 − ln 2 = ln 10 ≈ 2.3026` replaces "
                    "a quotient of logarithms with the logarithm of a quotient; `10` "
                    "divides `20` by the base, which does nothing to an exponent. The "
                    "bracket `2^4 = 16 &lt; 20 &lt; 32 = 2^5` identifies the right one."},
            {"q": "Why does `2^x = −8` have no real solution?",
             "a": ["Because `−8` is not a power of `2`",
                   "Because `2^x` is positive for every real `x`",
                   "Because `x = −3` gives `1/8` rather than `−8`",
                   "Because the logarithm of a negative number is negative"],
             "c": 1,
             "why": "The range of `2^x` is `(0, ∞)`, so no real `x` produces a negative "
                    "value. The first option is true but is not a reason: `20` is not a "
                    "power of `2` either, and `2^x = 20` does have a solution. The last "
                    "option is false &mdash; `log(−8)` is not defined at all, negative "
                    "or otherwise."},
        ],
        "mistakes": [
            ("Treating the base as a coefficient",
             "From `3^(2x) = 9`, dividing both sides by `3` does not give `2x = 3`. "
             "`3^(2x)` is not `3 · 2x`; the `3` is not multiplying anything, so there is "
             "nothing to divide out. Either match powers or take a logarithm."),
            ("Solving for the substitution and stopping",
             "In `e^(2x) − e^x − 6 = 0` the quadratic gives `u = 3`. That is `e^x`, not "
             "`x`. The answer is `x = ln 3`, and a solution reported as `3` answers a "
             "question nobody asked. Write down what the letter stands for when you "
             "introduce it."),
            ("Expanding the logarithm of a product wrongly",
             "`log(5 · 2^x)` is `log 5 + x · log 2`. It is not `log 5 · x log 2` and it "
             "is not `5 · log(2^x)`. Isolating the power before taking any logarithm "
             "removes the chance to make this one."),
        ],
        "standard": ("Finish when you decide between the two methods before writing anything down.",
                     "Given ten equations you should be able to sort them without solving "
                     "any: these have both sides as powers of one base and give exact "
                     "answers, these need a logarithm, and these have no solution because "
                     "the isolated exponential is not positive. The sorting is the skill. "
                     "The algebra after it is one or two lines."),
        "note": "Every equation here had the unknown in an exponent and nowhere else. "
                "The next lesson turns the situation around &mdash; the unknown inside a "
                "logarithm &mdash; and its second move is this lesson run backwards: "
                "make both sides exponents of the same base.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "solving-logarithmic-equations",
        "title": "Solving Logarithmic Equations",
        "module": "Solving",
        "one_line": "Condensing, exponentiating, and checking the domain.",
        "summary": (
            "Condense to a single logarithm, convert to exponential form, solve, and then "
            "test every candidate in the original equation. That last step is not "
            "diligence, it is arithmetic: condensing enlarges the set of values the "
            "expression accepts, so it can manufacture solutions the original never had."
        ),
        "key": [
            "log_b(u) = c         ⟹   u = b^c        then check u > 0",
            "log_b(M) = log_b(N)  ⟹   M = N          both must be positive",
            "log_2(x) + log_2(x − 2) = 3   →   x = 4      (x = −2 rejected)",
            "log M + log N = log(MN)   holds on a SMALLER set than the right side",
        ],
        "key_label": "Two conversions and the reason for the check",
        "concepts_intro": (
            "Two moves solve every equation in this lesson, and one property of the "
            "first move explains every wrong answer."
        ),
        "concepts": [
            ("Solving means undoing, not cancelling",
             "There are two moves. Condense several logarithms into one with the laws of "
             "lesson 6, then convert `log_b(u) = c` into `u = b^c` by the definition in "
             "lesson 4. Nothing is cancelled and nothing is divided by; the definition "
             "is quoted, in the direction that removes the logarithm."),
            ("Condensing widens the domain",
             "`log M + log N` requires `M &gt; 0` and `N &gt; 0`. `log(MN)` requires only "
             "`MN &gt; 0`, which two negatives also satisfy. The two agree wherever both "
             "are defined, and the second is defined in more places. Every extraneous "
             "solution in this lesson enters through exactly that gap."),
            ("The test is on the arguments, not on the sign of x",
             "A candidate is rejected when it makes some argument of some logarithm zero "
             "or negative. `x = −3/2` solves `log_3(x + 6) − log_3(x + 2) = 2` "
             "perfectly well, because at that value the arguments are `9/2` and `1/2`. "
             "Rejecting negative candidates on sight throws away correct answers."),
        ],
        "read_title": "Condensing, exponentiating, and the domain check",
        "read_intro": "Two solving moves, the precise reason a false answer can appear, and the three ways the solution set can come out empty.",
        "body": [
            ("p", "In the last lesson the unknown sat in an exponent and a logarithm "
                  "brought it down. Here the unknown sits inside a logarithm, and an "
                  "exponential takes it out. The two lessons are the same manoeuvre in "
                  "opposite directions, with one asymmetry: an exponential accepts every "
                  "real number, and a logarithm does not."),
            ("def", ("Logarithmic equation",
                     "An equation in which the unknown appears in the argument or the "
                     "base of a logarithm. Its <strong>domain</strong> is the set of "
                     "values making every argument positive (and every base positive and "
                     "not `1`). The domain is fixed by the equation as given, and no "
                     "later step may enlarge it.")),
            ("thm", ("The two conversions",
                     "For `b &gt; 0`, `b ≠ 1`: `log_b(u) = c` if and only if `u = b^c`, "
                     "for `u &gt; 0` and any real `c`.",
                     "And `log_b(M) = log_b(N)` if and only if `M = N`, for `M, N &gt; 0`. "
                     "The second is the first applied twice, and it is the statement "
                     "that lets two matching logarithms be dropped from an equation.")),
            ("p", "The method follows from the two conversions. Condense until each side "
                  "is a single logarithm or a constant. If both sides are logarithms in "
                  "the same base, drop them. If one side is a constant, convert. Then "
                  "solve whatever is left, which is usually linear or quadratic."),
            ("math", [
                "log_2(x − 1) + log_2(x + 2) = 2",
                "log_2((x − 1)(x + 2)) = 2         product law, used right to left",
                "(x − 1)(x + 2) = 2^2 = 4          definition of a logarithm",
                "x² + x − 2 = 4",
                "x² + x − 6 = 0",
                "(x + 3)(x − 2) = 0                candidates x = −3 and x = 2",
                "",
                "domain:  x − 1 > 0  and  x + 2 > 0    ⟹    x > 1",
                "x = 2  survives      log_2(1) + log_2(4) = 0 + 2 = 2      ✓",
                "x = −3 does not      log_2(−4) is not defined             ✗",
            ]),
            ("p", "Look at why `x = −3` appeared at all. The condensed equation asks only "
                  "that `(x − 1)(x + 2)` equal `4`, and at `x = −3` those factors are "
                  "`−4` and `−1`, whose product is `4`. Two negatives passed a test that "
                  "was written for their product. The original equation asks for the "
                  "logarithm of each factor separately, and neither exists."),
            ("example", ("A negative solution that is not extraneous",
                         "`log_3(x + 6) − log_3(x + 2) = 2` condenses to "
                         "`log_3((x + 6)/(x + 2)) = 2`, so `(x + 6)/(x + 2) = 9`, giving "
                         "`x + 6 = 9x + 18` and `x = −3/2`. The arguments there are "
                         "`9/2` and `1/2`, both positive, so the candidate stands. "
                         "Check: `log_3(9/2) − log_3(1/2) = log_3(9) = 2`.")),
            ("example", ("Every candidate rejected",
                         "`log_2(x) − log_2(x + 1) = 3` condenses to "
                         "`x/(x + 1) = 2^3 = 8`, so `x = 8x + 8` and `x = −8/7`. That "
                         "value makes both arguments negative, so it is rejected and "
                         "nothing else is available. The solution set is empty, and no "
                         "step along the way was wrong.")),
            ("p", "A third ending is possible: the condensed equation can be a "
                  "contradiction. `log(3x + 1) = log x + log 3` becomes "
                  "`log(3x + 1) = log(3x)`, hence `3x + 1 = 3x`, hence `1 = 0`. No "
                  "candidate is ever produced, and the solution set is empty for a "
                  "reason that has nothing to do with domains."),
            ("h3", "What a check can and cannot do"),
            ("p", "Substitute into the equation you were given, never into the condensed "
                  "form. The condensed form is precisely the form that accepts "
                  "extraneous values, so it will confirm them cheerfully. Checking there "
                  "proves nothing at all."),
            ("p", "An equation may also carry the unknown in the base. `log_x(16) = 2` "
                  "converts to `x² = 16`, so `x = 4` or `x = −4`. A base must be positive "
                  "and not `1`, so `−4` is rejected and `x = 4` is the answer. The same "
                  "discipline applies: convert by the definition, then test each "
                  "candidate against the conditions the definition imposes."),
        ],
        "lab": ("logarithm", {
            "mode": "solvelog",
            "panel_title": "Candidates, and which survive",
            "panel_intro": "The domain is computed from the equation as typed, before "
                           "any condensing happens, and every candidate is then reported "
                           "as kept or rejected with the argument that decided it. An "
                           "empty solution set is a normal outcome here.",
        }),
        "steps_title": "Solving a logarithmic equation",
        "steps_intro": "Four steps. The first one is written before any algebra and used after all of it.",
        "steps": [
            ("Write the domain from the original equation",
             "Every argument must be positive; intersect those conditions. Do it now, "
             "because the condensed equation has forgotten what the conditions were and "
             "cannot be asked."),
            ("Condense each side to a single logarithm",
             "Use the three laws of lesson 6 from right to left. A coefficient goes back "
             "up as a power first: `2 log x` becomes `log(x²)`, and only then can it "
             "join a sum."),
            ("Convert, and solve what remains",
             "Two logarithms in the same base: drop both and equate the arguments. A "
             "logarithm equal to a constant: apply the definition, `u = b^c`. What is "
             "left is an ordinary equation with no logarithms in it."),
            ("Test every candidate against the domain, then the original",
             "Keep the candidates inside the domain and discard the rest, naming the "
             "argument that went non-positive. If nothing survives, the solution set is "
             "empty and that is the answer."),
        ],
        "worked": {
            "title": "log_2(x) + log_2(x − 2) = 3, in full",
            "intro": [
                "The domain line costs one line at the top and does all the deciding at "
                "the bottom.",
            ],
            "lines": [
                "log_2(x) + log_2(x − 2) = 3",
                "",
                "domain:   x > 0  and  x − 2 > 0     ⟹     x > 2",
                "",
                "log_2(x(x − 2)) = 3                 product law, right to left",
                "x(x − 2) = 2^3 = 8                  definition of a logarithm",
                "x² − 2x − 8 = 0",
                "(x − 4)(x + 2) = 0                  candidates x = 4 and x = −2",
                "",
                "x = 4     4 > 2 ✓     log_2(4) + log_2(2) = 2 + 1 = 3        kept",
                "x = −2    −2 > 2 ✗    log_2(−2) is not defined               rejected",
                "",
                "solution set:  { 4 }",
            ],
            "after": [
                "The rejected candidate is not a mistake in the algebra. At `x = −2` the "
                "two factors are `−2` and `−4`, and their product is `8` exactly as the "
                "condensed equation demands. It satisfies every line below the "
                "condensing step and none of the equation above it.",
                "Note what the check is testing. Not \"is `−2` negative\" but \"are the "
                "arguments `x` and `x − 2` positive at `x = −2`\". Those are different "
                "questions, and only the second one is the domain condition: the "
                "reading's `x = −3/2` is a negative candidate that passes it and is a "
                "genuine solution.",
            ],
        },
        "quiz_title": "Candidates and survivors",
        "quiz": [
            {"q": "Solve `log_3(x) + log_3(x − 2) = 1`.",
             "a": ["`x = 3` only", "`x = 3` and `x = −1`", "`x = −1` only",
                   "No solution"],
             "c": 0,
             "why": "Condensing gives `log_3(x(x − 2)) = 1`, so `x² − 2x = 3` and "
                    "`(x − 3)(x + 1) = 0`. The domain is `x &gt; 2`, so `x = −1` is "
                    "rejected: it makes both arguments negative. The survivor checks out, "
                    "`log_3(3) + log_3(1) = 1 + 0 = 1`. Keeping both candidates is the "
                    "commonest wrong answer here."},
            {"q": "Why can condensing produce a value that is not a solution?",
             "a": ["Because the laws of logarithms are approximations",
                   "Because `log M + log N = log(MN)` is defined in more places than its left side",
                   "Because squaring both sides introduces extra roots",
                   "Because the base changes during the condensing"],
             "c": 1,
             "why": "The left side needs `M &gt; 0` and `N &gt; 0`; the right side needs "
                    "only `MN &gt; 0`, which two negatives also satisfy. The condensed "
                    "equation is therefore a slightly different question, and its extra "
                    "answers have to be discarded. The laws themselves are exact wherever "
                    "both sides are defined, and no squaring occurred."},
            {"q": "`log_3(x + 6) − log_3(x + 2) = 2` produces the candidate `x = −3/2`. What should you do with it?",
             "a": ["Reject it: a logarithmic equation cannot have a negative solution",
                   "Keep it: the arguments are `9/2` and `1/2`, both positive",
                   "Reject it: the quotient law does not apply to a difference",
                   "Keep it only if the base is greater than `1`"],
             "c": 1,
             "why": "The domain condition is on the arguments, not on `x`. At `x = −3/2` "
                    "they are `9/2` and `1/2`, so both logarithms exist, and "
                    "`log_3(9/2) − log_3(1/2) = log_3(9) = 2`. The quotient law is "
                    "exactly the law for a difference of logarithms, and the base plays "
                    "no part in the domain."},
        ],
        "mistakes": [
            ("Checking in the condensed equation",
             "The condensed form is the one that accepts extraneous values by "
             "construction: `x = −2` satisfies `x(x − 2) = 8` perfectly. A check has to "
             "be run in the equation as it was given, or it confirms the wrong answer "
             "with complete confidence."),
            ("Rejecting every negative candidate",
             "The condition is on arguments. `log_3(x + 6)` is defined for every "
             "`x &gt; −6`, and most of those numbers are negative. A rule of thumb that "
             "says \"logarithms hate negatives, so discard negative answers\" discards "
             "correct ones."),
            ("Condensing a sum of logarithms into the logarithm of a sum",
             "`log M + log N` is `log(MN)`, never `log(M + N)`. Test it once on numbers "
             "and it stops being tempting: `log 10 + log 100 = 1 + 2 = 3`, while "
             "`log 110 ≈ 2.0414`. The entire method depends on getting this one right."),
        ],
        "standard": ("Finish when the domain line is written before the first algebraic step, every time.",
                     "Given `log(x − 3) + log x = 1`, you should write `x &gt; 3` before "
                     "condensing anything, and then be able to say in advance that one of "
                     "the two candidates from `x² − 3x − 10 = 0` will fail it. It does: "
                     "`x = 5` is the solution and `x = −2` is rejected."),
        "note": "Both halves of the course now solve. Lesson 9 applied a logarithm to "
                "both sides to bring a variable down; this lesson made both sides "
                "exponents to lift a variable out. The last two lessons stop solving and "
                "start applying &mdash; compound interest, and the scales that are "
                "logarithms in ordinary clothes.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "compound-interest-and-continuous-growth",
        "title": "Compound Interest and Continuous Growth",
        "module": "Applications",
        "one_line": "Where the two exponential formulas come from.",
        "summary": (
            "Two formulas that look like conventions until they are built. "
            "`A = P(1 + r/n)^(nt)` is one multiplication repeated `nt` times, and "
            "`A = P · e^(rt)` is the value that expression settles down to as `n` grows. "
            "The second is lesson 3's limit with letters in it, and no new fact about "
            "money is involved."
        ),
        "key": [
            "A = P(1 + r/n)^(nt)     n compoundings a year, over t years",
            "A = P · e^(rt)          compounded continuously",
            "r is a DECIMAL per year:   5% → r = 0.05 = 1/20",
            "$1000 at 5% for 10 yr:  yearly 1628.89  monthly 1647.01  cont. 1648.72",
        ],
        "key_label": "Two formulas and what they pay",
        "concepts_intro": (
            "One idea builds the first formula, one limit builds the second, and one "
            "habit of units keeps both of them right."
        ),
        "concepts": [
            ("Each period multiplies, it does not add",
             "One period at rate `r/n` turns `P` into `P(1 + r/n)`. A second period "
             "multiplies by that same factor again. After `nt` periods the factor has "
             "been applied `nt` times, which is the entire derivation of "
             "`A = P(1 + r/n)^(nt)`."),
            ("More frequent compounding converges, it does not explode",
             "On `$1000` at `5%` for `10` years, moving from yearly to monthly gains "
             "`$18.11`; moving from monthly to continuous gains `$1.71` more. The "
             "sequence increases with `n` but is bounded, and its limit is the "
             "continuous value."),
            ("The continuous formula is lesson 3's limit, relabelled",
             "`(1 + 1/m)^m → e`. Put `m = n/r`, and "
             "`(1 + r/n)^(nt) = [(1 + 1/m)^m]^(rt)`, which tends to `e^(rt)`. `e` was "
             "not introduced for finance; finance is where the limit was first noticed."),
        ],
        "read_title": "Where the two formulas come from",
        "read_intro": "One repeated multiplication, one limit, and the units that make both of them wrong when they are wrong.",
        "body": [
            ("p", "A principal `P` is invested at a nominal annual rate `r`, compounded "
                  "`n` times a year, for `t` years. Every quantity in that sentence has "
                  "a unit attached, and most errors with these formulas are unit errors "
                  "rather than algebra errors."),
            ("def", ("Nominal rate",
                     "The <strong>nominal</strong> annual rate `r` is quoted per year and "
                     "split evenly among the `n` periods, so one period carries the rate "
                     "`r/n`. A nominal `5%` compounded monthly means `5/12` of a percent "
                     "a month. It is a name for twelve times the monthly rate, not the "
                     "growth actually achieved over a year.")),
            ("p", "The first formula is a repeated multiplication and nothing more. "
                  "Each period multiplies the balance by `1 + r/n`, so the balances "
                  "form a geometric sequence."),
            ("math", [
                "after 1 period     P(1 + r/n)",
                "after 2 periods    P(1 + r/n)²",
                "after k periods    P(1 + r/n)^k",
                "",
                "t years is nt periods, so     A = P(1 + r/n)^(nt)",
            ]),
            ("def", ("Effective annual rate",
                     "The <strong>effective</strong> annual rate is "
                     "`(1 + r/n)^n − 1`: the single yearly rate that would produce the "
                     "same balance after one year. For a nominal `5%` compounded "
                     "monthly it is `(1 + 0.05/12)^12 − 1 ≈ 0.051162`, that is "
                     "`5.1162%`. Two accounts quoted at different frequencies can only "
                     "be compared through this number.")),
            ("p", "Now increase `n` and watch. The numbers below are `$1000` at a "
                  "nominal `5%` for `10` years, each rounded to the nearest cent."),
            ("math", [
                "n = 1     yearly        1000(1.05)^10           =  1628.89",
                "n = 2     half-yearly   1000(1.025)^20          =  1638.62",
                "n = 4     quarterly     1000(1.0125)^40         =  1643.62",
                "n = 12    monthly       1000(1 + 0.05/12)^120   =  1647.01",
                "n = 365   daily         1000(1 + 0.05/365)^3650 =  1648.66",
                "n → ∞     continuous    1000 · e^0.5            =  1648.72",
                "",
                "          simple interest, for scale   1000(1 + 0.05 · 10)  =  1500.00",
            ]),
            ("p", "The column climbs and then stops climbing. Daily and continuous "
                  "differ by about six cents over ten years on a thousand dollars. "
                  "\"Compounded continuously\" is not a claim about speed &mdash; it is "
                  "the ceiling of the process, and the last few frequencies are already "
                  "sitting against it."),
            ("thm", ("The continuous limit",
                     "As `n → ∞`, `P(1 + r/n)^(nt) → P · e^(rt)`.",
                     "Substitute `m = n/r`, so that `r/n = 1/m` and `nt = m · rt`. The "
                     "expression becomes `P[(1 + 1/m)^m]^(rt)`, and `m → ∞` as "
                     "`n → ∞`. The inner bracket tends to `e` by lesson 3, so the whole "
                     "expression tends to `P · e^(rt)`.")),
            ("h3", "Solving for the other letters"),
            ("p", "`P` and `A` come out by dividing. `r` and `t` sit in the exponent, so "
                  "they need lesson 9. To double a balance under continuous growth, set "
                  "`2P = P · e^(rt)`; the `P` cancels, `2 = e^(rt)`, and `rt = ln 2`, so "
                  "`t = ln 2 / r`."),
            ("p", "That the principal cancels is the characteristic property of "
                  "exponential growth from lesson 2: the time to double does not depend "
                  "on where you start. At `5%` continuous it is "
                  "`ln 2 / 0.05 ≈ 13.86` years, and compounded yearly instead it is "
                  "`ln 2 / ln(1.05) ≈ 14.21` years."),
            ("p", "The banker's shortcut follows from `ln 2 ≈ 0.6931`. Doubling time is "
                  "roughly `70` divided by the rate as a percent, which at `5%` gives "
                  "`14` years against a true `13.86`. It is an approximation of a "
                  "logarithm, and it drifts at large rates: at `20%` the rule says "
                  "`3.5` years and the continuous answer is `3.47`, but at `100%` it "
                  "says `0.7` and the answer is `0.69`."),
            ("example", ("What a percent sign costs",
                         "Entering `5` instead of `0.05` for a monthly-compounded "
                         "account makes the monthly factor `1 + 5/12`, a rate of `500%` "
                         "a year. Over ten years `$1000` becomes about "
                         "`1.4 · 10^21` dollars. The formula reports it without complaint, "
                         "because nothing in the algebra knows what a percent is.")),
        ],
        "lab": ("expo", {
            "mode": "interest",
            "panel_title": "Six frequencies and the ceiling",
            "panel_intro": "Set a principal, a rate and a term; every frequency is then "
                           "computed from those three numbers, exactly as a fraction "
                           "whenever `n · t` is a whole number. Simple interest sits "
                           "alongside as the method that quietly loses money.",
        }),
        "steps_title": "Using the compound interest formula",
        "steps_intro": "Four steps, and two of them are about units rather than algebra.",
        "steps": [
            ("Convert the rate to a decimal per year",
             "`5%` is `0.05`. Entered as `5` it is a rate of `500%`, and every later "
             "step will run perfectly and return a number that is wrong by a factor of "
             "billions."),
            ("Count periods, not years",
             "`n` is periods per year and `t` is years, so the exponent is their "
             "product. Quarterly for five years is `20` periods &mdash; not `5`, and "
             "not `4`."),
            ("Build the base, then raise it once",
             "Compute `1 + r/n` exactly if you can: `1 + 0.06/4 = 1.015` is exact, while "
             "`1 + 0.05/12` is not. Rounding the base before raising it to the `120`th "
             "power moves the error up into the dollars."),
            ("Compare accounts by effective annual rate",
             "`(1 + r/n)^n − 1` for periodic compounding, `e^r − 1` for continuous. Two "
             "nominal rates quoted at different frequencies cannot be compared as they "
             "stand."),
        ],
        "worked": {
            "title": "$1000 at a nominal 6% for 5 years, compounded quarterly",
            "intro": [
                "Four numbers go in. The only thinking is which of them belongs where.",
            ],
            "lines": [
                "P = 1000     r = 6/100 = 0.06     n = 4     t = 5",
                "",
                "r/n = 0.06/4 = 0.015              the rate for ONE quarter",
                "n · t = 4 · 5 = 20                the number of quarters",
                "",
                "A = 1000(1 + 0.015)^20",
                "  = 1000(1.015)^20",
                "  ≈ 1346.86                       to the nearest cent",
                "",
                "for comparison:",
                "  yearly       1000(1.06)^5     ≈ 1338.23",
                "  continuous   1000 · e^(0.30)  ≈ 1349.86",
                "  effective annual rate   (1.015)^4 − 1 ≈ 0.061364  =  6.1364%",
            ],
            "after": [
                "Quarterly beats yearly by `$8.63` and loses to continuous by `$3.00`. "
                "Both gaps are small next to the `$346.86` of interest itself, which is "
                "the honest summary of compounding frequency: it matters, and it matters "
                "far less than the rate and the term.",
                "The effective rate is what makes the account comparable with anything "
                "else. A flat `6.1%` paid once a year sounds better than `6%`, and it is "
                "not: `6%` compounded quarterly earns `6.1364%` a year.",
            ],
        },
        "quiz_title": "Rates, periods and limits",
        "quiz": [
            {"q": "`$2000` at a nominal `8%` compounded semi-annually for `3` years. Which expression is `A`?",
             "a": ["`2000(1.08)^3`", "`2000(1.04)^6`", "`2000(1.04)^3`",
                   "`2000(1 + 8/2)^6`"],
             "c": 1,
             "why": "`r/n = 0.08/2 = 0.04` per half-year and `n · t = 6` half-years, so "
                    "`A = 2000(1.04)^6 ≈ 2530.64`. The first ignores the compounding "
                    "frequency entirely; the third uses the period rate with the number "
                    "of years; the fourth enters `8` rather than `0.08`, which is a rate "
                    "of `800%`."},
            {"q": "Under continuous growth the doubling time is `t = ln 2 / r`. What does it depend on?",
             "a": ["The rate only", "The principal and the rate", "The principal only",
                   "The rate and the final amount"],
             "c": 0,
             "why": "Setting `2P = P · e^(rt)` cancels `P` before any logarithm is taken. "
                    "Doubling `$100` and doubling `$100` million take the same time, "
                    "which is the property that defines exponential growth. At "
                    "`r = 0.05` it is `ln 2 / 0.05 ≈ 13.86` years, whatever the balance."},
            {"q": "On `$1000` at `5%` for `10` years, which gain is larger: yearly to monthly compounding, or monthly to continuous?",
             "a": ["Yearly to monthly, by about `$16`",
                   "Monthly to continuous, by about `$16`",
                   "The two gains are equal",
                   "Monthly to continuous, since continuous growth is unbounded"],
             "c": 0,
             "why": "Yearly pays `1628.89`, monthly `1647.01`, continuous `1648.72`. The "
                    "first step gains `$18.11` and the second `$1.71`, a difference of "
                    "about `$16.40`. The sequence increases with `n` but is bounded above "
                    "by the continuous value, so the returns to frequency shrink."},
        ],
        "mistakes": [
            ("Entering the rate as a percent",
             "`5` instead of `0.05` makes the monthly factor `1 + 5/12` and turns "
             "`$1000` into about `1.4 · 10^21` dollars over ten years. Nothing in the formula "
             "can detect it, because a formula does not know that `r` was meant to be a "
             "proportion."),
            ("Using t where nt belongs",
             "Quarterly for five years is `20` compoundings. `1000(1.015)^5` prices five "
             "quarters &mdash; fifteen months &mdash; and comes to `$1077.28` against "
             "the correct `$1346.86`. The exponent is periods, and the periods are "
             "`n · t`."),
            ("Comparing two nominal rates directly",
             "`6%` compounded monthly and `6.1%` compounded yearly do not rank the way "
             "the quoted numbers do. The first has effective rate "
             "`(1 + 0.06/12)^12 − 1 ≈ 6.1678%`, so it is the better of the two. Convert "
             "both to effective rates and then compare."),
        ],
        "standard": ("Finish when you can build the formula instead of recalling it.",
                     "Asked for a monthly-compounded balance, you should be able to write "
                     "`1 + r/12` for one month and `12t` for the number of months, and "
                     "assemble `A = P(1 + r/12)^(12t)` from those two facts alone. A "
                     "recalled formula with `n` and `t` in the wrong places looks exactly "
                     "like a correct one until the money is wrong."),
        "note": "`e` entered this course in lesson 3 as the limit of `(1 + 1/n)^n`, with "
                "no application attached to it. This is the application, and it is also "
                "the historical order: the limit was first met by asking what happens to "
                "an account compounded more and more often.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "logarithmic-scales",
        "title": "Logarithmic Scales",
        "module": "Applications",
        "one_line": "Why decibels, pH and magnitude are logarithms.",
        "summary": (
            "Decibels, pH and earthquake magnitude are one construction used three "
            "times: report the logarithm of a ratio instead of the ratio. Equal steps on "
            "the scale then stand for equal factors on the quantity, which is what lets "
            "a range of fourteen powers of ten fit on one axis."
        ),
        "key": [
            "pH = −log[H+]              one unit down  =  10× more H+",
            "dB = 10 · log(I / I₀)      +10 dB = 10× intensity;  2× = +3.01 dB",
            "M  = log(A / A₀)           +2 magnitude = 100× amplitude",
            "adding on the scale  =  multiplying the quantity",
        ],
        "key_label": "Three scales, one construction",
        "concepts_intro": (
            "Three definitions that differ only in a reference value and a multiplier, "
            "and one rule for the arithmetic that is legal on them."
        ),
        "concepts": [
            ("A reading on a log scale is an exponent",
             "`pH 5` is not an amount of anything. It says the hydrogen ion "
             "concentration is `10^−5` moles per litre, and the scale reports the `−5`. "
             "That is why the reading moves by `1` when the quantity moves by a factor "
             "of `10`."),
            ("Equal distances are equal ratios",
             "On a logarithmic axis the gap from `1` to `2` is the same as the gap from "
             "`10` to `20` and from `100` to `200`, because each is `log 2 ≈ 0.30103`. "
             "Distances add where the quantities multiply, which is the product law of "
             "lesson 6 drawn as a picture."),
            ("Differences are the only arithmetic that transfers",
             "Two magnitudes cannot be averaged and two pH readings cannot be added, "
             "because the quantities underneath do not combine that way. What a "
             "difference means is fixed and reference-free: two magnitudes apart is "
             "`10² = 100` times the amplitude, on any seismograph."),
        ],
        "read_title": "Scales that report a logarithm",
        "read_intro": "Three definitions, the property they share, and what the arithmetic on them does and does not mean.",
        "body": [
            ("p", "Audible sound intensities run from about `10^−12` watts per square "
                  "metre at the threshold of hearing to about `10^2` at the point of "
                  "damage: fourteen powers of ten. On a linear axis the quiet end of "
                  "that range is invisible. Reporting the exponent instead of the "
                  "quantity turns the whole range into the interval from `0` to `140`."),
            ("def", ("Decibel",
                     "`L = 10 · log(I / I₀)`, where `I` is intensity and "
                     "`I₀ = 10^−12` watts per square metre is a fixed reference. `L` "
                     "carries no units: it is ten times the exponent of a ratio. The "
                     "factor of ten is arbitrary &mdash; the unit is one tenth of a "
                     "<em>bel</em>, and the bel alone was too coarse to be useful.")),
            ("def", ("pH",
                     "`pH = −log[H+]`, where `[H+]` is the hydrogen ion concentration in "
                     "moles per litre. The minus sign exists so that ordinary solutions "
                     "get positive readings: `[H+] = 10^−7` gives `pH 7`. It also "
                     "reverses the direction, so a lower pH means more hydrogen ions.")),
            ("def", ("Magnitude",
                     "`M = log(A / A₀)`, where `A` is the amplitude recorded and `A₀` a "
                     "fixed reference amplitude. Magnitude `6` is ten times the "
                     "amplitude of magnitude `5`. The energy released is separately "
                     "found to scale as `10^(1.5 · M)`, which is an empirical relation "
                     "rather than part of the definition.")),
            ("p", "All three have the shape `S = k · log(Q / Q₀)`. The reference `Q₀` "
                  "makes the argument a pure number, which it must be before a logarithm "
                  "can touch it. The multiplier `k` sets the size of one step: `1` for "
                  "magnitude, `10` for decibels, `−1` for pH."),
            ("thm", ("A difference on the scale is a ratio of quantities",
                     "If `S = k · log(Q / Q₀)` then "
                     "`S₂ − S₁ = k · log(Q₂ / Q₁)`, and so "
                     "`Q₂ / Q₁ = 10^((S₂ − S₁) / k)`.",
                     "The reference cancels, by the quotient law of lesson 6. This is "
                     "why two readings can be compared by anyone, while a single reading "
                     "means nothing until the reference is stated.")),
            ("math", [
                "decibels, k = 10",
                "  +10 dB  →  10^1   =  10× the intensity",
                "  +30 dB  →  10^3   =  1000× the intensity",
                "  doubling the intensity  →  10 · log 2 ≈ 3.0103 dB",
                "",
                "pH, k = −1",
                "  pH 6 down to pH 3  →  10^((3 − 6)/(−1)) = 10^3 = 1000× the [H+]",
                "",
                "magnitude, k = 1",
                "  5.0 up to 7.0      →  10^2 = 100× the amplitude",
                "                        10^(1.5 · 2) = 1000× the energy",
            ]),
            ("h3", "Why the sum of two sources is not double the reading"),
            ("p", "Two identical machines each measured at `60` dB run together. The "
                  "intensities add, so the total is `2I`, and the level is "
                  "`10 · log(2I / I₀) = 60 + 10 · log 2 ≈ 63.01` dB. Ten identical "
                  "machines give exactly `70` dB, since `10 · log 10 = 10`. Adding the "
                  "readings instead &mdash; `60 + 60 = 120` &mdash; would correspond to "
                  "multiplying the intensities, which is what a sum of logarithms means."),
            ("p", "A caution about the word loud. An increase of `10` dB is ten times "
                  "the intensity and is usually reported as sounding about twice as "
                  "loud. Perceived loudness is a psychological measurement with its own "
                  "scale; everything in this lesson is about intensity, which is the "
                  "quantity actually inside the logarithm."),
            ("h3", "Reading a logarithmic axis"),
            ("p", "On a log axis the gridlines within each decade are unevenly spaced "
                  "and the spacing repeats. Between `1` and `10`, the mark for `2` sits "
                  "`30.1%` of the way along and the mark for `5` sits `69.9%` along, "
                  "because `log 2 ≈ 0.30103` and `log 5 ≈ 0.69897`. The identical "
                  "pattern appears between `10` and `100`, and between `100` and `1000`."),
            ("p", "One consequence is worth carrying away. If `y = a · b^x`, then "
                  "`log y = log a + x · log b`, which is a linear function of `x`. So an "
                  "exponential plotted with a logarithmic vertical axis is a straight "
                  "line, and its slope is `log b`. A straight line on such a plot is "
                  "evidence of a constant ratio per step, which is exactly the "
                  "definition of exponential from lesson 1."),
            ("example", ("A number you can check",
                         "Normal conversation is about `60` dB and a jet engine at close "
                         "range about `140` dB. The gap of `80` on the scale is a factor "
                         "of `10^8` in intensity: a hundred million. That compression is "
                         "the whole point of the construction, and it is also why the "
                         "gap sounds much smaller than it is.")),
        ],
        "lab": ("logarithm", {
            "mode": "scale",
            "panel_title": "From a factor to a step, and back",
            "panel_intro": "Move a quantity and watch the reading, then move the reading "
                           "and watch the quantity. The panel also adds two equal "
                           "sources, which lands about `3` decibels up rather than "
                           "twice as high.",
        }),
        "steps_title": "Comparing two readings on a log scale",
        "steps_intro": "Four steps. The reference value is never needed, and that is the point of step two.",
        "steps": [
            ("Identify the multiplier in front of the logarithm",
             "`1` for magnitude, `10` for decibels, `−1` for pH. Everything else in the "
             "comparison follows from that number."),
            ("Subtract the two readings",
             "The difference is what carries the information. The reference cancels out "
             "of it by the quotient law, so nothing about `I₀` or `A₀` needs to be "
             "known."),
            ("Divide by the multiplier and raise 10 to the result",
             "`Q₂ / Q₁ = 10^((S₂ − S₁) / k)`. For pH the negative `k` flips the "
             "direction, which is the arithmetic behind \"lower pH, more acid\"."),
            ("Report a factor, not a difference",
             "The answer is \"a thousand times the concentration\", not \"three more "
             "acidic\". If the answer still has the units of the scale on it, the "
             "conversion has not happened yet."),
        ],
        "worked": {
            "title": "Four comparisons, one method",
            "intro": [
                "Each one is a subtraction, a division by `k`, and a power of ten.",
            ],
            "lines": [
                "(1)  60 dB up to 90 dB          k = 10",
                "     difference 30              ratio = 10^(30/10) = 10^3",
                "     the intensity is 1000 times as large",
                "",
                "(2)  pH 6 down to pH 3          k = −1",
                "     difference −3              ratio = 10^(−3 / −1) = 10^3",
                "     1000 times the [H+];  pH 3 is the more acidic",
                "",
                "(3)  magnitude 5.0 up to 7.0    k = 1",
                "     difference 2               amplitude ratio = 10^2 = 100",
                "                                energy ratio = 10^(1.5 · 2) = 1000",
                "",
                "(4)  two 60 dB sources together",
                "     the intensities add:  2I",
                "     new level = 60 + 10 · log 2 ≈ 63.01 dB      not 120",
            ],
            "after": [
                "None of the first three used a reference value. `I₀`, `A₀` and the mole "
                "never appeared, because `k · log(Q₂/Q₀) − k · log(Q₁/Q₀) = "
                "k · log(Q₂/Q₁)` &mdash; the quotient law removing the thing both "
                "readings had in common.",
                "Line (4) is the one that surprises people. Two identical sources are "
                "three decibels up, not double the reading and not double anything on "
                "the scale. Ten identical sources are exactly ten decibels up. The "
                "quantities double and decuple; the readings, which are logarithms, add "
                "`log 2` and `log 10` worth of steps.",
            ],
        },
        "quiz_title": "Steps and factors",
        "quiz": [
            {"q": "A sound rises from `60` dB to `90` dB. The intensity has been multiplied by:",
             "a": ["`30`", "`1000`", "`10^30`", "`1.5`"],
             "c": 1,
             "why": "`10^((90 − 60)/10) = 10^3 = 1000`. `30` reports the difference as "
                    "though the scale were linear; `10^30` forgets to divide by the `10` "
                    "in front of the logarithm; `1.5` divides one reading by the other, "
                    "which is an operation on exponents and means nothing here."},
            {"q": "Which is more acidic, pH 4 or pH 7, and by how much?",
             "a": ["pH 7, by a factor of `3`", "pH 4, by a factor of `3`",
                   "pH 4, by a factor of `1000`", "pH 7, by a factor of `1000`"],
             "c": 2,
             "why": "`pH = −log[H+]`, so the concentrations are `10^−4` and `10^−7`: the "
                    "lower reading is the higher concentration, by a factor of `1000`. "
                    "The minus sign in the definition is what reverses the direction, and "
                    "a difference of `3` on the scale is never a factor of `3`."},
            {"q": "Two identical machines, each measured at `70` dB, run together. The level is about:",
             "a": ["`140` dB", "`73` dB", "`70` dB", "`80` dB"],
             "c": 1,
             "why": "Intensities add, so the total is `2I` and the level rises by "
                    "`10 · log 2 ≈ 3.01` dB. `140` adds the two readings, which "
                    "corresponds to multiplying the intensities; `80` would need ten "
                    "machines, since `10 · log 10 = 10` exactly."},
        ],
        "mistakes": [
            ("Reading a difference as a factor",
             "Magnitude `7` is not \"two more\" than magnitude `5` in any physical "
             "sense, and it is certainly not twice as large. It is `100` times the "
             "amplitude and about `1000` times the energy. The reading is an exponent, "
             "and the exponent is the thing that went up by two."),
            ("Adding readings when the quantities add",
             "Two `60` dB sources make about `63` dB, not `120`. Adding logarithms "
             "multiplies the quantities underneath, so `60 + 60` describes the ratio "
             "`(I₁/I₀) · (I₂/I₀) = 10^12`, a product of two ratios rather than a sum of "
             "two intensities. Add the intensities first, then take the logarithm once."),
            ("Reading pH in the intuitive direction",
             "The minus sign makes the scale run backwards against intuition: pH `2` is "
             "more acidic than pH `6`, and a higher pH means fewer hydrogen ions. There "
             "is no way to feel your way to this. Write the definition down and follow "
             "it."),
        ],
        "standard": ("Finish when you turn a difference into a factor without looking anything up.",
                     "Given two readings on any of the three scales, you should be able "
                     "to name the multiplier `k`, subtract, and report "
                     "`10^((S₂ − S₁)/k)` as a factor on the quantity. If the answer "
                     "comes out carrying the units of the scale, the conversion has not "
                     "been done."),
        "note": "This is the last lesson of the course, and it is lesson 4's definition "
                "doing ordinary work: every reading on these scales is an exponent, and "
                "every legal manipulation of them is one of the three laws of lesson 6 "
                "read in the other direction. Course 8 picks up the sequences that these "
                "constant-ratio quantities have been all along.",
    },
]
