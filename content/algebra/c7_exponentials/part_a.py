"""Course 7, lessons 01-06 — exponential functions, e, and the logarithm defined."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "exponential-functions",
        "title": "Exponential Functions",
        "module": "Exponential functions",
        "one_line": "The variable moves into the exponent.",
        "summary": (
            "In every function so far the variable sat in the base: `x²`, `x³`, "
            "`√x`. An exponential function puts it in the exponent instead, and "
            "that one move changes what the values do &mdash; a constant ratio "
            "between steps, where a line has a constant difference."
        ),
        "key": [
            "f(x) = a·b^x        a ≠ 0,   b > 0,   b ≠ 1",
            "f(0) = a            f(x + 1) / f(x) = b   at every x",
            "b^x > 0  for every real x    ⟹    y = 0 is never reached",
            "3·2^x :   3, 6, 12, 24, 48        ratios  2, 2, 2, 2",
        ],
        "key_label": "The definition, and what it forces",
        "concepts_intro": (
            "Three things carry the lesson: where the variable sits, what the base "
            "is not allowed to be, and the one number that separates an exponential "
            "from a line."
        ),
        "concepts": [
            ("The variable is the exponent, not the base",
             "`x²` and `2^x` agree at `x = 2` and at very little else. In `x²` the "
             "exponent is fixed and the base moves; in `2^x` the base is fixed and "
             "the exponent moves. Only the second is an exponential function."),
            ("A line adds, an exponential multiplies",
             "Raise `x` by one and a linear function gains a fixed amount. An "
             "exponential is multiplied by a fixed amount. That multiplier is `b`, "
             "and it is the only thing needed to recognise one from a table."),
            ("The base is fenced in, and each fence excludes a real failure",
             "`b` must be positive, or the function has no value at `x = 1/2`. `b` "
             "must not be `1`, or the function is the constant `a`. Neither "
             "restriction is decoration; each removes something that genuinely "
             "breaks."),
        ],
        "read_title": "The definition, and the two restrictions",
        "read_intro": "What an exponential function is, why the base is fenced in, "
                      "and what the graph therefore has to look like.",
        "body": [
            ("def", ("Exponential function",
                     "An <strong>exponential function</strong> is a function of the "
                     "form `f(x) = a·b^x` with `a ≠ 0`, `b &gt; 0` and `b ≠ 1`. The "
                     "number `b` is the <strong>base</strong>, and `a` is the value "
                     "at `x = 0`.")),
            ("p", "Course 1 gave `b^x` a meaning for every rational `x`: whole "
                  "exponents by repeated multiplication, negative ones by "
                  "reciprocal, and `b^(p/q)` as the `q`-th root of `b^p`. For an "
                  "irrational exponent &mdash; `2^√2` &mdash; the value is the number "
                  "that the rational exponents close in on. This course takes that "
                  "for granted and treats the domain as every real number."),
            ("h3", "Why the base must be positive"),
            ("p", "Take `b = −4`. Then `b^1 = −4` and `b^2 = 16` are perfectly good "
                  "numbers, and so is `b^(1/3) = −∛4`. But `b^(1/2) = √(−4)` is not "
                  "real, and neither is `b^(1/4)`. What survives is a scattered set "
                  "of rationals with no interval anywhere in it, so there is no curve "
                  "to draw. Excluding a negative base is not squeamishness; it is the "
                  "only way the function gets a domain worth having."),
            ("p", "`b = 0` fails differently: `0^x` is `0` for every positive "
                  "`x`, has no value at all for negative `x`, and `0^0` is a "
                  "convention rather than something the laws force. And `b = 1` does "
                  "not fail at all "
                  "&mdash; `1^x = 1` for every `x` &mdash; it simply gives the "
                  "constant function `f(x) = a`, a horizontal line. It is excluded "
                  "because calling that exponential would make every statement in "
                  "lesson 2 false."),
            ("h3", "Constant ratio, not constant difference"),
            ("thm", ("The ratio is the base",
                     "For `f(x) = a·b^x`, the quotient `f(x + 1) / f(x)` equals `b` "
                     "at every `x`. A linear function has `g(x + 1) − g(x)` constant "
                     "instead. Given values at equally spaced inputs, computing both "
                     "columns settles which kind of function you are looking at "
                     "&mdash; if it is either.")),
            ("proof", [
                "`f(x + 1) / f(x) = (a·b^(x+1)) / (a·b^x)`. Both `a` and `b^x` are "
                "non-zero, so the quotient is defined. The exponent law "
                "`b^(x+1) = b^x·b` reduces it to `b`, and `b` does not depend on `x`, "
                "which is the whole content of the claim.",
            ]),
            ("math", [
                "x         −3     −2     −1      0      1      2      3",
                "2^x      1/8    1/4    1/2      1      2      4      8",
                "",
                "every entry is positive, and the left end is getting small,",
                "not getting to zero",
            ]),
            ("h3", "The line the curve never touches"),
            ("p", "Every value of `b^x` is positive, so `f(x) = a·b^x` never takes "
                  "the value `0`. For `b &gt; 1`, as `x` runs off to the left the "
                  "values shrink without limit and the curve settles toward the "
                  "horizontal line `y = 0` without arriving. That line is the "
                  "horizontal asymptote, and the reason the curve never reaches it is "
                  "not that it runs out of room &mdash; it is that no real exponent "
                  "makes a positive base give `0`."),
            ("def", ("Horizontal asymptote",
                     "A horizontal line `y = k` is a <strong>horizontal "
                     "asymptote</strong> of `f` when the values of `f(x)` get and "
                     "stay arbitrarily close to `k` as `x` runs off to one end. For "
                     "`f(x) = a·b^x + k` the asymptote is `y = k`: the power part "
                     "shrinks toward `0`, and `k` is what is left.")),
            ("example", ("Three formulas, read without drawing",
                         "`f(x) = 2^x` has `a = 1`, base `2`, `f(0) = 1`, asymptote "
                         "`y = 0`, and range every positive number. "
                         "`f(x) = 2^x + 3` is the same curve lifted by `3`: asymptote "
                         "`y = 3`, `f(0) = 4`, range every number above `3`. "
                         "`f(x) = 3·(1/2)^x` has `f(0) = 3` and values "
                         "`3, 3/2, 3/4, 3/8, 3/16` at `x = 0, 1, 2, 3, 4` &mdash; "
                         "still a constant ratio, and the ratio is `1/2`.")),
        ],
        "lab": ("expo", {
            "mode": "intro",
            "panel_title": "Ratio against difference",
            "panel_intro": "Set `a` and `b` and read the two columns under the plot. "
                           "The straight line drawn beside the curve passes through "
                           "`f(0)` and `f(1)`, so the two agree at the first two "
                           "points and nowhere after. Try base `−2` and watch the "
                           "table keep going while the curve fails.",
        }),
        "steps_title": "Identifying an exponential function",
        "steps_intro": "Four checks. The first two settle what it is; the last two "
                       "get the numbers out.",
        "steps": [
            ("Find where the variable sits",
             "Variable in the exponent with a fixed base: exponential. Variable in "
             "the base with a fixed exponent &mdash; `x³`, `x^(1/2)` &mdash; not "
             "exponential, whatever the exponent is. `x^x` has it in both places and "
             "is neither; it is outside this course."),
            ("Check the base against the two restrictions",
             "Positive, and not `1`. A negative base has no curve to draw, and "
             "`b = 1` is a horizontal line wearing exponential notation."),
            ("Read a off at x = 0",
             "`b^0 = 1` for every allowed base, so `f(0) = a`. It is the fastest "
             "number to extract from a formula and the first one to test against a "
             "table."),
            ("Divide neighbouring values, do not subtract them",
             "For values at equally spaced inputs, form the ratios. A constant ratio "
             "means exponential and names `b`; a constant difference means linear. "
             "Doing both costs one line and removes the guess."),
        ],
        "worked": {
            "title": "One table, two functions",
            "intro": ["Both functions pass through `(0, 3)` and `(1, 6)`. After that "
                      "they have nothing in common, and the ratio column is where you "
                      "see it first."],
            "lines": [
                "x                 0      1      2      3      4",
                "─────────────────────────────────────────────────",
                "g(x) = 3 + 3x     3      6      9     12     15",
                "   difference            3      3      3      3      constant",
                "   ratio                 2    3/2    4/3    5/4      not constant",
                "",
                "f(x) = 3·2^x      3      6     12     24     48",
                "   difference            3      6     12     24      not constant",
                "   ratio                 2      2      2      2      constant",
                "",
                "so   f is exponential with a = 3, b = 2",
                "     g is linear with intercept 3 and slope 3",
            ],
            "after": [
                "At `x = 4` the two are `48` and `15`. They were equal three steps "
                "earlier, at `x = 1`, which is why two matching points prove nothing: "
                "a line and an exponential can always be made to agree at two points, "
                "and they part immediately afterwards.",
                "The ratio row for `g` is worth reading. `2, 3/2, 4/3, 5/4` is not "
                "constant, and it is drifting toward `1` &mdash; a line eventually "
                "grows by a smaller and smaller <em>proportion</em>, while an "
                "exponential never does.",
            ],
        },
        "quiz_title": "Which function is which",
        "quiz": [
            {"q": "Which of these is an exponential function?",
             "a": ["`f(x) = x⁵`", "`f(x) = 5x`", "`f(x) = 5^x`", "`f(x) = x^x`"],
             "c": 2,
             "why": "Only `5^x` has a fixed base with the variable in the exponent. "
                    "`x⁵` has the variable in the base, `5x` is linear, and `x^x` has "
                    "it in both places, which makes it neither."},
            {"q": "For `f(x) = 7·3^x`, what is `f(0)`?",
             "a": ["`21`", "`7`", "`1`", "`0`"],
             "c": 1,
             "why": "`3^0 = 1`, so `f(0) = 7·1 = 7`. `21` treats the coefficient as "
                    "part of the base, which is what `(7·3)^x` would give at `x = 1`; "
                    "`1` drops the coefficient; `0` reads `3^0` as `0`."},
            {"q": "What is the range of `f(x) = 2^x − 5`?",
             "a": ["Every real number",
                   "Every real number greater than `0`",
                   "Every real number greater than `−5`",
                   "Every real number greater than or equal to `−5`"],
             "c": 2,
             "why": "`2^x` takes every positive value and no other, so `2^x − 5` "
                    "takes every value above `−5` and nothing at or below it. "
                    "Reaching `−5` would need `2^x = 0`, which no real `x` does, so "
                    "the inequality is strict."},
        ],
        "mistakes": [
            ("Reading 2^x as 2x",
             "At `x = 1` and `x = 2` they agree &mdash; `2` and `4` &mdash; which is "
             "exactly why the habit survives past the first example. At `x = 5` they "
             "are `32` and `10`."),
            ("Treating a·b^x as (a·b)^x",
             "`3·2^x` at `x = 2` is `3·4 = 12`, while `(3·2)^2 = 36`. Order of "
             "operations does the power first: the coefficient multiplies the power "
             "and is not part of the base."),
            ("Saying the curve reaches its asymptote",
             "`2^(−20) = 1/1048576`. That is small and it is not `0`, and there is no "
             "input further out that does better in kind. The asymptote is approached, "
             "never attained."),
        ],
        "standard": ("Finish when a table tells you the kind of function in one line.",
                     "Given values at equally spaced inputs you should form the ratios "
                     "first, name `b` if they are constant, and state `a`. Given a "
                     "formula you should state the base, `f(0)` and the horizontal "
                     "asymptote without drawing anything."),
        "note": "The restrictions `b &gt; 0` and `b ≠ 1` are what make the next "
                "four lessons possible. A positive base other than `1` takes every "
                "positive value exactly once, which is what lets lesson 4 define a "
                "logarithm as the exponent that produces a given number &mdash; the "
                "exponent, singular.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "growth-and-decay",
        "title": "Growth and Decay",
        "module": "Exponential functions",
        "one_line": "One model, two behaviours, decided by the base.",
        "summary": (
            "The same formula `a·b^x` describes a quantity that keeps multiplying up "
            "and one that keeps shrinking. Which of the two you have is decided by "
            "the base and by nothing else in the formula, and the percentage in the "
            "problem statement is the base in disguise."
        ),
        "key": [
            "f(x) = a·b^x    with   a > 0",
            "b > 1        growth      up by (b − 1)·100% each step",
            "0 < b < 1    decay       down by (1 − b)·100% each step",
            "b = 1        neither     the constant a, for ever",
        ],
        "key_label": "One formula, three regimes",
        "concepts_intro": (
            "The base does all the work. The starting value scales the picture and "
            "changes nothing about its shape."
        ),
        "concepts": [
            ("The base carries the whole story",
             "`a` is the value at `x = 0` and nothing more; it stretches the curve "
             "vertically. Growth against decay, and how fast, are questions about `b` "
             "alone."),
            ("A percentage change is a multiplier",
             "Up 5% means multiply by `21/20`. Down 20% means multiply by `4/5`. "
             "Writing `b = 1 + r` for a rise and `b = 1 − r` for a fall is the step "
             "that turns a sentence about percentages into a function."),
            ("Constant percentage, changing amounts",
             "A quantity growing 8% a year gains more each year than it did the year "
             "before, because 8% is taken of a larger number every time. The "
             "percentage is what stays fixed; the amount is what does not, and "
             "confusing the two is the error the worked example is about."),
        ],
        "read_title": "Growth, decay, and how fast",
        "read_intro": "Reading the base, writing a percentage as a multiplier, and "
                      "the two different things people mean by how fast.",
        "body": [
            ("def", ("Growth factor",
                     "In `f(x) = a·b^x` with `a &gt; 0`, the base `b` is the "
                     "<strong>growth factor</strong>. If `b &gt; 1` the function "
                     "increases and the model is one of <strong>growth</strong>; if "
                     "`0 &lt; b &lt; 1` it decreases and the model is one of "
                     "<strong>decay</strong>. `b = 1` gives the constant `a`, which "
                     "is neither.")),
            ("p", "One step multiplies by `b`, so the change across one step is "
                  "`f(x + 1) − f(x) = a·b^x·(b − 1) = (b − 1)·f(x)`. Divide by "
                  "`f(x)`: the change is the fraction `b − 1` of the current value, "
                  "the same fraction at every `x`. Written as a percentage, that "
                  "fraction is the <strong>rate</strong>."),
            ("math", [
                "up 5%       b = 1 + 5/100   = 21/20",
                "up 1%       b = 1 + 1/100   = 101/100",
                "up 100%     b = 1 + 1       = 2            doubling each step",
                "down 20%    b = 1 − 20/100  = 4/5",
                "down 10%    b = 1 − 10/100  = 9/10",
                "down 100%   b = 0                          not an exponential",
            ]),
            ("p", "Keep the base as a fraction. `21/20` raised to a power is exact; "
                  "`1.05` raised to a power on a machine is not, and the difference "
                  "shows in the fourth or fifth place after ten steps."),
            ("h3", "Doubling time and half-life"),
            ("def", ("Doubling time and half-life",
                     "The <strong>doubling time</strong> of a growth model is the "
                     "number of steps `n` with `b^n = 2`. The "
                     "<strong>half-life</strong> of a decay model is the `n` with "
                     "`b^n = 1/2`. Both depend on `b` alone.")),
            ("proof", [
                "`f(x + n) = a·b^(x+n) = a·b^x·b^n = f(x)·b^n`. So `f(x + n)` is "
                "`2·f(x)` exactly when `b^n = 2`, whatever `x` is and whatever `a` "
                "is. A quantity therefore takes exactly as long to go from `1000` to "
                "`2000` as from `1` to `2`, and the doubling time is a property of "
                "the base rather than of where you started.",
            ]),
            ("p", "`b^n = 2` rarely has a whole-number solution. For "
                  "`b = 101/100` the powers step across `2` between `n = 69` and "
                  "`n = 70`: `(101/100)^69 ≈ 1.9869` and `(101/100)^70 ≈ 2.0068`, "
                  "both rounded to four places. The exact answer is irrational, near "
                  "`69.6607`. Solving `b^n = 2` for `n` is what lesson 9 does, and it "
                  "needs a logarithm."),
            ("example", ("The rule of 70",
                         "For a rise of `r` percent a step, the doubling time is "
                         "close to `70/r`. At 1% that gives `70` against a true "
                         "`69.6607`; at 5% it gives `14` against `14.2067`; at 10% it "
                         "gives `7` against `7.2725`. The `70` is a convenient "
                         "rounding of `100·ln 2 ≈ 69.3147`, a quantity lesson 7 will "
                         "name. The rule runs slightly high below about 2% a step and "
                         "slightly low above it, and by 20% a step it offers `3.5` "
                         "against a true `3.8018`.")),
            ("h3", "Decay is growth reflected"),
            ("p", "`(1/b)^x = b^(−x)`, so the decay curve with base `1/b` is the "
                  "growth curve with base `b` reflected in the vertical axis. There "
                  "is one shape here seen twice, not two shapes. It also means decay "
                  "never reaches zero: `b^n` is a positive fraction for every `n`, "
                  "however large, so a substance losing 10% a year still has "
                  "`(9/10)^100` of itself left after a century."),
            ("p", "This is the point where an exponential model and a linear one give "
                  "genuinely different answers, not just different numbers. Something "
                  "losing `10 g` a year from `100 g` is empty in ten years. Something "
                  "losing 10% a year never is."),
        ],
        "lab": ("expo", {
            "mode": "growth",
            "panel_title": "The base, and how long a factor of two takes",
            "panel_intro": "Change `b` and watch the percentage column stay put while "
                           "the amount column does not. The lab finds the first whole "
                           "`n` with `b^n ≥ 2` by exact search and then prints the "
                           "true doubling time as the rounded irrational it is; the "
                           "two numbers are different and both are labelled.",
        }),
        "steps_title": "Setting up a growth or decay model",
        "steps_intro": "The modelling is four decisions. None of them is arithmetic.",
        "steps": [
            ("Name the starting amount",
             "`a = f(0)`: the value before any step has been taken. If the data "
             "begins at year 3, either shift the input or say plainly that `x` counts "
             "steps from there."),
            ("Turn the percentage into a base",
             "Up `r` percent gives `b = 1 + r/100`; down `r` percent gives "
             "`b = 1 − r/100`. Write it as a fraction and the powers stay exact."),
            ("Check the direction before computing anything",
             "`b &gt; 1` has to go with a quantity you expect to grow. If you wrote "
             "`b = 0.05` for a 5% rise, the model loses 95% a step and the first two "
             "values will show it."),
            ("Say what one step is",
             "`b` is the multiplier per step, and a step is a year, an hour or a "
             "half-life &mdash; whatever the problem says. Nothing in `a·b^x` records "
             "the unit, so the answer has to."),
        ],
        "worked": {
            "title": "500 g losing 20% a year",
            "intro": ["The base first, then the table, then the half-life. The last "
                      "column is the one the lesson is about."],
            "lines": [
                "starting amount    a = 500 g",
                "down 20% a year    b = 1 − 20/100 = 4/5",
                "",
                "A(n) = 500·(4/5)^n",
                "",
                "n      A(n) exactly            lost during year n",
                "──────────────────────────────────────────────────",
                "0      500",
                "1      400                     100",
                "2      320                      80",
                "3      256                      64",
                "4      1024/5   = 204.8         51.2",
                "5      4096/25  = 163.84        40.96",
                "",
                "half-life:   (4/5)³ = 64/125  = 0.512     still above half",
                "             (4/5)⁴ = 256/625 = 0.4096    below half",
                "",
                "  so the first whole year at or under half is n = 4,",
                "  and the exact half-life is irrational, ≈ 3.1063 years",
            ],
            "after": [
                "The right-hand column is the point. The percentage lost is `20` in "
                "every single year; the amount lost falls from `100 g` to `40.96 g` "
                "across five years, because 20% of a smaller number is a smaller "
                "number.",
                "A reader who models this as \"loses 100 g a year\" gets year one "
                "right and year five badly wrong: that model is at `0 g` after five "
                "years, and the true figure is `163.84 g`. The two answers are not "
                "close, and they were built from the same sentence."
            ],
        },
        "quiz_title": "Base, direction, amount",
        "quiz": [
            {"q": "A town grows 5% a year. Its population after `t` years is `P·b^t`. "
                  "What is `b`?",
             "a": ["`5`", "`1/20`", "`21/20`", "`6/5`"],
             "c": 2,
             "why": "`b = 1 + 5/100 = 21/20`. `1/20` is the rate on its own, and "
                    "using it as the base would shrink the town to a twentieth of "
                    "itself every year; `6/5` is a rise of 20%; `5` is a rise of 400% "
                    "a year."},
            {"q": "`100 g` of a substance falls by 10% a year. How much is left after "
                  "3 years?",
             "a": ["`70 g`", "`72.9 g`", "`81 g`", "`27.1 g`"],
             "c": 1,
             "why": "`100·(9/10)³ = 100·729/1000 = 72.9 g` exactly: the 10% is taken "
                    "of `100`, then of `90`, then of `81`. `70 g` removes 10% of the "
                    "original `100` three times, which is a linear model; `81 g` "
                    "stops a year early; `27.1 g` is the amount lost rather than the "
                    "amount left."},
            {"q": "Which base gives decay?",
             "a": ["`b = 1.03`", "`b = 0.97`", "`b = −0.97`", "`b = 3`"],
             "c": 1,
             "why": "Decay is `0 &lt; b &lt; 1`, and `0.97` is a fall of 3% a step. "
                    "`1.03` and `3` both exceed `1` and grow. A negative base is not "
                    "allowed at all: `(−0.97)^(1/2)` is not a real number, so there "
                    "is no function to call decaying."},
        ],
        "mistakes": [
            ("Taking the percentage of the original each time",
             "Down 20% from `500` is `400`; down 20% again is `320`, not `300`. The "
             "second reduction is taken from `400`. Repeated percentage change is "
             "multiplication, and it multiplies the current value."),
            ("Using the rate as the base",
             "A 5% rise is `b = 1.05`, not `b = 0.05` and not `b = 5`. The `1` is the "
             "amount you keep and the `0.05` is what is added to it; dropping the `1` "
             "converts a small rise into a near-total collapse."),
            ("Mixing the unit of the base with the unit of the exponent",
             "If `b = 21/20` is per year, then `x = 18` means eighteen years. Going "
             "monthly is not dividing 5% by 12: it is finding the `c` with "
             "`c¹² = 21/20`, which is a different number. Lesson 11 gives that "
             "distinction its own name."),
        ],
        "standard": ("Finish when a sentence turns into a base without hesitation.",
                     "Given \"falls 12% an hour from 90 mg\" you should write "
                     "`A(t) = 90·(22/25)^t` with `t` in hours, say that it decays, and "
                     "say that it never reaches `0`. If the base takes you more than a "
                     "line, the percentage-to-multiplier step is what to drill."),
        "note": "Every model here changes by a fixed factor per whole step. Lesson 3 "
                "asks what happens when the step is cut smaller and smaller instead "
                "&mdash; the same 100% rise, applied twice a year, then monthly, then "
                "daily &mdash; and the answer to that question is a specific number.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "the-number-e",
        "title": "The Number e",
        "module": "Exponential functions",
        "one_line": "Where e comes from, by compounding faster and faster.",
        "summary": (
            "Pay 100% interest once a year and a dollar becomes two. Pay it in "
            "smaller instalments more often and the year-end total climbs &mdash; but "
            "not without limit. It settles toward one irrational number, `2.718281828…`, "
            "and that number is `e`."
        ),
        "key": [
            "(1 + 1/n)^n   climbs toward e as n grows",
            "n = 1   2.000000     n = 12   2.613035     n = 365   2.714567",
            "e = 1 + 1/1! + 1/2! + 1/3! + …",
            "e ≈ 2.718281828459045     irrational: every decimal is a rounding",
        ],
        "key_label": "One limit, and the number it names",
        "concepts_intro": (
            "`e` is not a new kind of object. It is a number, arrived at by a "
            "specific process, and the process is worth watching because two "
            "reasonable readings of it give two different wrong answers."
        ),
        "concepts": [
            ("e is a limit, and no term of the sequence equals it",
             "Every `(1 + 1/n)^n` is a rational number &mdash; `(1 + 1/4)^4` is "
             "exactly `625/256`. `e` is irrational, so the sequence approaches a "
             "value it never takes, however large `n` gets."),
            ("Two plausible readings, both wrong",
             "`1 + 1/n` tends to `1`, and `1` to any power is `1`. Equally, `n` "
             "copies of `1/n` add to `1`, which suggests `2`. Each argument freezes "
             "one part of the expression while moving the other, and they disagree "
             "&mdash; which is the signal that the move is not legal."),
            ("e^x is an ordinary exponential",
             "`e` is between `2.718` and `2.719`, so `y = e^x` sits between `y = 2^x` "
             "and `y = 3^x` and behaves exactly like them: increasing, positive, "
             "asymptote `y = 0`, and obedient to every exponent law. No algebra in "
             "this course changes because the base is `e`."),
        ],
        "read_title": "Where e comes from",
        "read_intro": "One dollar, one year, 100% interest, and the question of how "
                      "often it is paid.",
        "body": [
            ("p", "Lend a dollar for a year at 100%. Paid once at the end, you have "
                  "`2`. Paid as 50% twice, the second payment earns on the first: "
                  "`(1 + 1/2)² = 9/4 = 2.25`. Four payments of 25% give "
                  "`(1 + 1/4)⁴ = 625/256 = 2.44140625` exactly. The pattern is "
                  "`n` payments of `1/n`, and the year-end total is `(1 + 1/n)^n`."),
            ("math", [
                "n          (1 + 1/n)^n              exact         to 12 places",
                "──────────────────────────────────────────────────────────────",
                "1          (2/1)^1                  2             2.000000000000",
                "2          (3/2)^2                  9/4           2.250000000000",
                "3          (4/3)^3                  64/27         2.370370370370",
                "4          (5/4)^4                  625/256       2.441406250000",
                "12         (13/12)^12                             2.613035290225",
                "365        (366/365)^365                          2.714567482022",
                "1000       (1001/1000)^1000                       2.716923932236",
                "──────────────────────────────────────────────────────────────",
                "e                                                 2.718281828459",
            ]),
            ("p", "The totals rise, and the rises get smaller. Going from once a year "
                  "to twice adds `0.25`; going from daily to a thousand times a year "
                  "adds about `0.0024`. Compounding more often is worth less and less, "
                  "and there is a ceiling."),
            ("def", ("The number e",
                     "<strong>`e`</strong> is the number that `(1 + 1/n)^n` "
                     "approaches as `n` grows without bound. To fifteen places, "
                     "`e ≈ 2.718281828459045`. It is irrational, so no decimal "
                     "expansion of it terminates or repeats, and every printed value "
                     "of `e` &mdash; here, on a calculator, in the lab &mdash; is a "
                     "rounding of something that has no finite decimal form.")),
            ("thm", ("The limit exists",
                     "The sequence `(1 + 1/n)^n` is increasing, and no term of it "
                     "exceeds `3`. An increasing sequence with a ceiling has a limit, "
                     "and that limit is `e`. Both facts are established in analysis "
                     "rather than here, and neither can be got from a table &mdash; a "
                     "table shows finitely many terms and says nothing about the "
                     "rest.")),
            ("p", "At `n = 365` the two shortcuts give `1` and `2`, while the true "
                  "value is `2.714567…`. Both readings are off, in opposite "
                  "directions, on every single row. That is what makes the limit worth "
                  "computing rather than reasoning about informally."),
            ("h3", "A faster route to the same number"),
            ("p", "The same number is the sum of `1/k!` over all `k ≥ 0`. The partial "
                  "sums arrive far more quickly than the compounding sequence does, "
                  "because each new term is smaller than the last by a factor of `k`."),
            ("math", [
                "terms                      partial sum",
                "───────────────────────────────────────────────",
                "1                          1.000000000000",
                "1 + 1                      2.000000000000",
                "  + 1/2                    2.500000000000",
                "  + 1/6                    2.666666666667",
                "  + 1/24                   2.708333333333",
                "  + 1/120                  2.716666666667",
                "  + 1/720                  2.718055555556",
                "  + 1/5040                 2.718253968254",
                "───────────────────────────────────────────────",
                "e                          2.718281828459",
            ]),
            ("p", "Eight terms of the series agree with `e` to four decimal places. "
                  "The compounding sequence at `n = 1000` agrees to two. To get `k` "
                  "correct digits from `(1 + 1/n)^n` you need `n` of roughly `10^k`; "
                  "the series needs about `k` terms. The limit is the definition; the "
                  "series is how the digits are actually produced."),
            ("h3", "The function e^x"),
            ("p", "`f(x) = e^x` is the exponential function with base `e`. "
                  "`f(0) = 1`, `f(1) = e ≈ 2.718282`, `f(2) = e² ≈ 7.389056`, and "
                  "`f(−1) = 1/e ≈ 0.367879`. Every one of those decimals is rounded; "
                  "the exact values are `1`, `e`, `e²`, `1/e`, and those are the forms "
                  "to carry through a calculation."),
            ("example", ("The same money, two ways",
                         "`1000` at 5% for 10 years, compounded once a year, is "
                         "`1000·(21/20)^10 ≈ 1628.89`. Compounded continuously it is "
                         "`1000·e^(0.05·10) = 1000·e^(1/2) ≈ 1648.72`, both rounded to "
                         "the cent. The gap of about `19.83` is the whole of what "
                         "continuous compounding buys over annual at this rate. Lesson "
                         "11 derives the formula `A = P·e^(rt)` from the table above.")),
        ],
        "lab": ("expo", {
            "mode": "e",
            "panel_title": "Computed, not quoted",
            "panel_intro": "The rows are `(1 + 1/n)^n` as exact fractions, beside the "
                           "partial sums of the series, with the two wrong readings as "
                           "their own columns so you can watch them be wrong on every "
                           "row. The value of `e` in the last box was summed in this "
                           "browser and rounded once, at the end.",
        }),
        "steps_title": "Working with e",
        "steps_intro": "It is a number. Four habits keep it from being treated as "
                       "anything stranger.",
        "steps": [
            ("Treat e as a fixed number",
             "It lies between `2.7182` and `2.7183`. `e²` is a number near `7.389`; "
             "it is not `e` squared in some special sense, and no exponent law changes "
             "because the base is `e`."),
            ("Keep it exact until the last line",
             "Write the answer as `1000·e^(1/2)` and round once at the end. Rounding "
             "`e` to `2.72` first and then raising it to a power throws away places "
             "you cannot get back."),
            ("Say where you rounded",
             "`e ≈ 2.71828` is a true statement; `e = 2.71828` is a false one. Every "
             "decimal here and in the lab carries the number of places it was rounded "
             "to, and yours should too."),
            ("Do not compute e from the limit",
             "`(1 + 1/n)^n` needs roughly `10^k` terms for `k` correct digits; the "
             "series needs about `k`. The limit is what `e` means, and the series is "
             "what you sum."),
        ],
        "worked": {
            "title": "One dollar, compounded more and more often",
            "intro": ["The first four rows are exact fractions, so they can be checked "
                      "by hand. The rest are rounded, and say so."],
            "lines": [
                "$1 at 100% for one year, paid in n instalments of 1/n:",
                "",
                "  once           (1 + 1/1)^1     = 2               $2.00",
                "  twice          (1 + 1/2)^2     = 9/4             $2.25",
                "  quarterly      (1 + 1/4)^4     = 625/256         $2.4414…",
                "  monthly        (1 + 1/12)^12   ≈ 2.613035        $2.6130…",
                "  weekly         (1 + 1/52)^52   ≈ 2.692597        $2.6925…",
                "  daily          (1 + 1/365)^365 ≈ 2.714567        $2.7145…",
                "  every second   n = 31 536 000  ≈ 2.71828179      $2.7182…",
                "",
                "  the ceiling    e               ≈ 2.71828182846   $2.7182…",
                "",
                "differences between consecutive rows:",
                "  0.25,  0.1914…,  0.1716…,  0.0796…,  0.0220…,  0.0037…",
                "",
                "each extra subdivision buys less than the one before it",
            ],
            "after": [
                "The quarterly figure is `625/256`, exactly. That is worth doing by "
                "hand once: `(5/4)⁴ = 5⁴/4⁴ = 625/256`, and `625/256 = 2.44140625` "
                "with no rounding at all, because the denominator is a power of two.",
                "The last two rows agree to six decimal places, which is closer "
                "than any bank cares about, and that is the practical content of "
                "`e`: past a certain frequency, "
                "compounding more often changes the answer in places nobody is "
                "counting. What it does buy is a formula that no longer mentions "
                "`n` at all.",
            ],
        },
        "quiz_title": "What e is",
        "quiz": [
            {"q": "As `n` grows, `(1 + 1/n)^n`:",
             "a": ["Tends to `1`, because `1 + 1/n` tends to `1`",
                   "Tends to `2`, because the `n` outside cancels the `1/n` inside",
                   "Climbs toward `e ≈ 2.718281828`, without ever reaching it",
                   "Grows without bound"],
             "c": 2,
             "why": "The first two answers each hold one part of the expression still "
                    "while the other moves, and they disagree, which is how you know "
                    "the move is illegal. The sequence increases and stays under `3`, "
                    "so it has a limit; no term equals that limit, because every term "
                    "is rational and `e` is not."},
            {"q": "What is `(1 + 1/4)⁴` exactly?",
             "a": ["`625/256`", "`125/64`", "`5/4`", "`2`"],
             "c": 0,
             "why": "`(5/4)⁴ = 5⁴/4⁴ = 625/256`, which is `2.44140625` with nothing "
                    "rounded. `125/64` is `(5/4)³`, one power short; `5/4` is the base "
                    "with the exponent dropped."},
            {"q": "Which statement about `e` is correct?",
             "a": ["`e = 2.71828`",
                   "`e` is irrational, so every decimal written for it is a rounding",
                   "`e = 22/7`",
                   "`e` is the value of `(1 + 1/n)^n` at `n = 1000000`"],
             "c": 1,
             "why": "`2.71828` is `e` rounded to five places. "
                    "`(1 + 1/1000000)^1000000 ≈ 2.718280` is a rational number that "
                    "agrees with `e` to five places and is not `e`. `22/7` is a rough "
                    "value for `π`, and it is rational too."},
        ],
        "mistakes": [
            ("Writing e = 2.718",
             "`2.718` is `e` to three places, and the difference surfaces quickly: "
             "`2.718^10 ≈ 22003.6` against the true `e^10 ≈ 22026.5`. Round at the "
             "end of a calculation, not at the start of one."),
            ("Arguing the limit is 1 because the base tends to 1",
             "The base tends to `1` and the exponent grows without bound at the same "
             "time. Taking the limit of one while the other is held fixed gives `1` "
             "in one order and `2` in the other; two answers from one expression means "
             "the method is broken, not that the answer is ambiguous."),
            ("Treating a term of the sequence as the value",
             "`(1 + 1/1000000)^1000000` is a rational number correct to five decimal "
             "places and is not `e`. `e` is what the sequence approaches; it is not "
             "any entry in the table."),
        ],
        "standard": ("Finish when e is just a number to you, with a known origin.",
                     "You should be able to say in one sentence where `e` comes from, "
                     "give it to five places, call it irrational without hedging, and "
                     "use `e^x` without pausing over the base. If `e` still reads as a "
                     "special symbol rather than a number near `2.718`, the "
                     "compounding table is the thing to redo by hand."),
        "note": "Lesson 7 gives base `e` its own notation, `ln`, and lesson 11 derives "
                "`A = P·e^(rt)` from exactly the table above. Why `e` and not `2` or "
                "`10` is the natural base for calculus is a question this course "
                "deliberately does not answer; compounding is an honest and complete "
                "reason for algebra.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "what-a-logarithm-is",
        "title": "What a Logarithm Is",
        "module": "Logarithms",
        "one_line": "A logarithm is an exponent. That sentence is the lesson.",
        "summary": (
            "`log_b(x)` is the exponent you put on `b` to get `x`. Everything later "
            "in this course &mdash; the graphs, the three laws, both kinds of equation "
            "&mdash; is that one sentence applied, and nearly every error is a step "
            "taken without it."
        ),
        "key": [
            "log_b(x) = y      means exactly      b^y = x",
            "                  with  b > 0,  b ≠ 1,  x > 0",
            "log_2(8) = 3      because   2³ = 8",
            "log_9(3) = 1/2    because   9^(1/2) = 3",
        ],
        "key_label": "One fact, written two ways",
        "concepts_intro": (
            "Say the definition out loud until it is automatic. Everything in this "
            "lesson is a consequence of it, including the two restrictions."
        ),
        "concepts": [
            ("A logarithm is an exponent",
             "Not a length, not an operation on digits, not a button. `log_5(125)` is "
             "the answer to \"5 to what power gives 125?\", and the answer is `3`. "
             "Read every logarithm you meet as that question."),
            ("The two forms carry identical information",
             "`b^y = x` and `log_b(x) = y` are the same statement. Moving between them "
             "is not a step in a calculation, it is a change of notation, and it costs "
             "nothing."),
            ("The argument must be positive",
             "`b^y` is positive for every real `y`, so no exponent produces `0` and "
             "none produces a negative number. `log_2(0)` and `log_2(−8)` name nothing "
             "&mdash; not because they are difficult, but because the question they "
             "ask has no answer."),
        ],
        "read_title": "The definition, read in both directions",
        "read_intro": "One definition, the restrictions that come with it, and the "
                      "evaluations you should be able to do without a calculator.",
        "body": [
            ("def", ("Logarithm",
                     "For `b &gt; 0` with `b ≠ 1`, and for `x &gt; 0`, "
                     "<strong>`log_b(x)`</strong> is the unique real number `y` with "
                     "`b^y = x`. The number `b` is the <strong>base</strong> of the "
                     "logarithm and `x` is its <strong>argument</strong>.")),
            ("p", "The word <em>unique</em> is carrying weight. Lesson 1 fenced the "
                  "base in so that `b^y` is strictly increasing (when `b &gt; 1`) or "
                  "strictly decreasing (when `0 &lt; b &lt; 1`). Either way it takes "
                  "each positive value exactly once, so there is one `y` and not two. "
                  "That is also why `b = 1` is barred: `1^y = 1` for every `y`, so "
                  "`log_1(1)` would have every number as an answer and `log_1(5)` "
                  "would have none."),
            ("math", [
                "exponential form         logarithmic form",
                "────────────────────────────────────────────────",
                "b^y = x                  log_b(x) = y",
                "2³ = 8                   log_2(8) = 3",
                "10^(−3) = 1/1000         log_10(1/1000) = −3",
                "5^0 = 1                  log_5(1) = 0",
                "7^1 = 7                  log_7(7) = 1",
                "9^(1/2) = 3              log_9(3) = 1/2",
            ]),
            ("p", "Read the table left to right and you are converting a power into a "
                  "logarithm; read it right to left and you are doing the reverse. "
                  "Three roles move around: the base of the power stays the base of "
                  "the logarithm, the result of the power becomes the argument, and "
                  "the exponent becomes the value. Nothing else happens."),
            ("thm", ("The two cancellation identities",
                     "`b^(log_b(x)) = x` for every `x &gt; 0`, and `log_b(b^y) = y` "
                     "for every real `y`. The first says that raising `b` to the "
                     "exponent which produces `x` produces `x`. The second says that "
                     "the exponent which produces `b^y` is `y`. Both are the "
                     "definition said aloud, and lesson 5 restates them as the "
                     "statement that the two functions are inverse.")),
            ("h3", "Evaluating without a calculator"),
            ("p", "Ask the question. `log_3(81)`: three to what power is `81`? "
                  "`3⁴ = 81`, so the value is `4`. When the answer is not a whole "
                  "number the same question still works, provided both numbers can be "
                  "written as powers of one common base."),
            ("example", ("log_8(4), in full",
                         "Both `8` and `4` are powers of `2`: `8 = 2³` and `4 = 2²`. "
                         "If `8^y = 4` then `(2³)^y = 2²`, so `2^(3y) = 2²`. Since "
                         "`2^t` takes each value exactly once, `3y = 2` and `y = 2/3`. "
                         "Check: `8^(2/3) = (∛8)² = 2² = 4`, so `log_8(4) = 2/3`.")),
            ("p", "With a base greater than `1`, a logarithm is negative exactly "
                  "when the argument lies strictly between `0` and `1`; with a base "
                  "below `1` it is negative exactly when the argument is above `1`. "
                  "`log_5(1/25) = −2`, because `5^(−2) = 1/25`. The restriction is on "
                  "the argument; the value is free to be any real number at all."),
            ("p", "Most logarithms are irrational. `log_2(10)` sits between `3` and "
                  "`4`, because `2³ = 8` and `2⁴ = 16` bracket `10`, and its value is "
                  "`3.321928…` &mdash; a number with no exact decimal form. The exact "
                  "statement is `2^(log_2(10)) = 10`; the decimal is a rounding, and "
                  "lesson 8 is about producing it."),
            ("p", "Notation. The base is written as a subscript, and the argument gets "
                  "brackets whenever there is any doubt: `log_2(x + 1)` and "
                  "`log_2(x) + 1` are different numbers. Two bases are used so often "
                  "that they drop the subscript &mdash; base 10 and base `e` &mdash; "
                  "and lesson 7 introduces that shorthand."),
        ],
        "lab": ("logarithm", {
            "mode": "define",
            "panel_title": "The same fact, both ways round",
            "panel_intro": "Type a base and an argument and the lab answers by "
                           "searching for a rational exponent `p/q` with `b^p = x^q`, "
                           "in exact integer arithmetic. So `log_9(3)` comes back as "
                           "`1/2` rather than `0.5`, and when no such fraction exists "
                           "the lab says so before it prints anything rounded.",
        }),
        "steps_title": "Evaluating a logarithm by hand",
        "steps_intro": "Four steps, and the last one is the one that catches a flipped "
                       "fraction.",
        "steps": [
            ("Write the question as an equation",
             "`log_b(x)` asks \"`b` to what power is `x`?\". Put it in exponential "
             "form, `b^y = x`, with `y` the unknown. Everything after this is ordinary "
             "algebra."),
            ("Write both sides as powers of one base",
             "`log_8(4)` becomes `2^(3y) = 2²`. Whenever `b` and `x` are powers of a "
             "common number this works, and the answer comes out as a fraction."),
            ("Match the exponents",
             "`b^m = b^n` forces `m = n` when `b &gt; 0` and `b ≠ 1`, because such an "
             "exponential takes each value exactly once. Solve the linear equation "
             "that leaves."),
            ("Check by raising the base to your answer",
             "`8^(2/3) = 4`. One line, and it catches the inverted fraction, which is "
             "the usual way this goes wrong."),
        ],
        "worked": {
            "title": "Eight logarithms, by asking the question",
            "intro": ["No calculator is used or needed. The middle column is the "
                      "question; the right column is the answer to it."],
            "lines": [
                "log_2(8)          2 to what power is 8?         2³ = 8            3",
                "log_3(81)         3 to what power is 81?        3⁴ = 81           4",
                "log_5(1/25)       5 to what power is 1/25?      5^(−2) = 1/25    −2",
                "log_9(3)          9 to what power is 3?         9^(1/2) = 3     1/2",
                "log_8(4)          8 to what power is 4?         8^(2/3) = 4     2/3",
                "log_(1/2)(8)      1/2 to what power is 8?       (1/2)^(−3) = 8   −3",
                "log_6(1)          6 to what power is 1?         6^0 = 1           0",
                "log_7(−7)         7 to what power is −7?        nothing works    undefined",
                "",
                "checks:   9^(1/2) = √9 = 3                     ✓",
                "          8^(2/3) = (∛8)² = 2² = 4             ✓",
                "          (1/2)^(−3) = 2³ = 8                  ✓",
            ],
            "after": [
                "The sixth line is the one that surprises people. A base below `1` "
                "gives a negative logarithm for an argument above `1`, and a positive "
                "one for an argument below `1` &mdash; the whole scale runs backwards, "
                "which is exactly what lesson 5 sees as a decreasing curve.",
                "The last line is not a hard case, it is an impossible one. `7^y` is "
                "positive for every real `y`, so no exponent gives `−7`. Logarithms of "
                "negative numbers are not covered in this course and are not merely "
                "difficult here; within the real numbers there is nothing to compute.",
            ],
        },
        "quiz_title": "Reading the definition",
        "quiz": [
            {"q": "What is `log_4(8)`?",
             "a": ["`2`", "`3/2`", "`2/3`", "`32`"],
             "c": 1,
             "why": "`4^y = 8` gives `2^(2y) = 2³`, so `2y = 3` and `y = 3/2`; "
                    "`4^(3/2) = (√4)³ = 8` confirms it. `2` is `log_4(16)`; `2/3` is "
                    "`log_8(4)`, the same two numbers the other way round; `32` is "
                    "`4·8`, which is not a logarithm of anything here."},
            {"q": "What is `log_7(0)`?",
             "a": ["`0`", "`1`",
                   "It does not exist: no exponent makes `7^y` equal `0`", "`−7`"],
             "c": 2,
             "why": "`7^y` is positive for every real `y`. It gets small as `y` falls "
                    "&mdash; `7^(−10) = 1/282475249` &mdash; and never arrives at `0`. "
                    "Choice one confuses `log_7(0)` with `log_7(1)`, which is `0` "
                    "because `7^0 = 1`."},
            {"q": "Written as a logarithm, `5³ = 125` is:",
             "a": ["`log_5(125) = 3`", "`log_3(125) = 5`", "`log_125(5) = 3`",
                   "`log_5(3) = 125`"],
             "c": 0,
             "why": "The base of the power stays the base of the logarithm, the result "
                    "becomes the argument, and the exponent becomes the value. The "
                    "other three permute those roles; `log_125(5)` is in fact `1/3`, "
                    "not `3`."},
        ],
        "mistakes": [
            ("Swapping the base and the argument",
             "`log_2(8) = 3` and `log_8(2) = 1/3`. They are reciprocals, not equals. "
             "Say the base out loud when you read the symbol: it is the number being "
             "raised to a power."),
            ("Expecting log_b(0) to be 0, or −∞",
             "No real exponent makes `2^y` equal `0`; the values shrink without ever "
             "arriving. `log_2(0)` is undefined, and `−∞` is not a real number that "
             "can serve as an answer."),
            ("Refusing a negative logarithm",
             "`log_5(1/25) = −2` is an ordinary value. The positivity restriction is "
             "on the argument. The output of a logarithm runs over every real number, "
             "negatives included, which is the range statement of lesson 5."),
        ],
        "standard": ("Finish when you convert between the two forms without thinking.",
                     "Given `log_4(x) = 3/2` you should write `4^(3/2) = x` and get "
                     "`8` in one line. Given `3^y = 1/27` you should write "
                     "`y = log_3(1/27) = −3` in one. If either takes a moment of "
                     "translation, the definition is not yet automatic and the laws "
                     "in lesson 6 will feel arbitrary."),
        "note": "Every exact logarithm the lab reports was found by searching for a "
                "rational exponent, never by calling a logarithm function. That is the "
                "honest shape of the subject: `log_2(8)` is `3` exactly, and "
                "`log_2(10)` is a number that can only be bracketed and then rounded.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "logarithmic-functions-and-their-graphs",
        "title": "Logarithmic Functions and Their Graphs",
        "module": "Logarithms",
        "one_line": "The inverse of an exponential, reflected in y = x.",
        "summary": (
            "`g(x) = log_b(x)` is the inverse of `f(x) = b^x`, so its graph is that "
            "curve reflected in the line `y = x`. The domain, the range, the "
            "asymptote and the slowness of the climb are all consequences of the "
            "reflection rather than separate facts to memorise."
        ),
        "key": [
            "g(x) = log_b(x)   is the inverse of   f(x) = b^x",
            "domain  x > 0             range  every real number",
            "(p, q) on b^x     ⟺     (q, p) on log_b(x)",
            "asymptote x = 0     always through (1, 0) and (b, 1)",
        ],
        "key_label": "The inverse, and what it inherits",
        "concepts_intro": (
            "One picture and one table serve both functions. Read the table down for "
            "the exponential and across for the logarithm."
        ),
        "concepts": [
            ("Reflection in y = x swaps the coordinates",
             "If `(p, q)` lies on the graph of an invertible function, `(q, p)` lies "
             "on the graph of its inverse. `2³ = 8` puts `(3, 8)` on `y = 2^x` and "
             "`(8, 3)` on `y = log_2(x)`. There is one set of pairs here, read in two "
             "directions."),
            ("Domain and range trade places",
             "`b^x` accepts every real number and returns only positive ones. So "
             "`log_b(x)` accepts only positive numbers and returns every real one. "
             "The exclusion of `x ≤ 0` is not an extra rule bolted on; it is the range "
             "of the exponential seen from the other side."),
            ("The asymptote turns through a right angle",
             "`y = b^x` flattens toward the horizontal line `y = 0`. Reflecting that "
             "line in `y = x` gives the vertical line `x = 0`, and that is the "
             "logarithm's asymptote: the curve plunges without bound as `x` comes down "
             "toward `0` from the right."),
        ],
        "read_title": "The inverse curve",
        "read_intro": "Why the reflection is the whole picture, and what can be read "
                      "off it before anything is plotted.",
        "body": [
            ("p", "Course 3 defined an inverse function: `g` undoes `f` when "
                  "`g(f(x)) = x` and `f(g(x)) = x`, and a function has one only if it "
                  "is one-to-one. `f(x) = b^x` is strictly increasing when `b &gt; 1` "
                  "and strictly decreasing when `0 &lt; b &lt; 1`, so it never repeats "
                  "a value and the inverse exists without any restriction of the "
                  "domain &mdash; which is unusual, and is why logarithms are as "
                  "well-behaved as they are."),
            ("def", ("Logarithmic function",
                     "For `b &gt; 0` with `b ≠ 1`, the <strong>logarithmic "
                     "function</strong> with base `b` is `g(x) = log_b(x)`, defined "
                     "for `x &gt; 0`. It is the inverse of `f(x) = b^x`: "
                     "`log_b(b^x) = x` for every real `x`, and `b^(log_b(x)) = x` for "
                     "every `x &gt; 0`.")),
            ("math", [
                "f(x) = 2^x                       g(x) = log_2(x)",
                "",
                "  x      f(x)                       x       g(x)",
                "  −3     1/8                        1/8     −3",
                "  −2     1/4                        1/4     −2",
                "  −1     1/2                        1/2     −1",
                "   0     1                          1        0",
                "   1     2                          2        1",
                "   2     4                          4        2",
                "   3     8                          8        3",
                "",
                "the same seven pairs, with the two columns exchanged",
            ]),
            ("h3", "What to read off the graph"),
            ("ul", [
                "<strong>Domain `x &gt; 0`.</strong> There is no curve at all to the "
                "left of the vertical axis, and none on it.",
                "<strong>Range: every real number.</strong> The curve has no ceiling "
                "and no floor; each height is reached exactly once.",
                "<strong>Through `(1, 0)`.</strong> `b^0 = 1` for every allowed base, "
                "so `log_b(1) = 0`. Every logarithmic curve crosses the horizontal "
                "axis at `1`, whatever the base.",
                "<strong>Through `(b, 1)`.</strong> `b^1 = b`. This is the point that "
                "tells two bases apart on a drawing.",
                "<strong>No vertical intercept.</strong> `x = 0` is outside the "
                "domain, so the curve never meets the vertical axis.",
                "<strong>Increasing for `b &gt; 1`, decreasing for `0 &lt; b &lt; 1`.</strong> "
                "The direction is inherited from the exponential it reflects.",
            ]),
            ("h3", "It rises without bound, and it rises slowly"),
            ("p", "Both halves of that sentence matter. To lift `log_10(x)` by one "
                  "you must multiply `x` by ten, so the output crawls while the input "
                  "explodes. But there is no height it fails to reach eventually."),
            ("math", [
                "x            1     10    100   1000    10⁶     10¹⁰⁰",
                "log_10(x)    0      1      2      3       6       100",
                "",
                "the input is multiplied by 10 to move the output by 1",
            ]),
            ("p", "That last line is the reason decibels, pH and earthquake magnitude "
                  "are logarithms, which is lesson 12. It is also why a logarithmic "
                  "curve looks flat on any drawing wide enough to be interesting "
                  "&mdash; flat is not level, and the two are easy to confuse by eye."),
            ("h3", "Shifting the curve moves the asymptote with it"),
            ("p", "`log_b(x − h)` is the same curve moved `h` to the right, and the "
                  "asymptote goes with it to `x = h`. The domain becomes `x &gt; h`. "
                  "This is the commonest source of a wrong domain in the whole course, "
                  "because the shift is invisible unless you look inside the brackets."),
            ("example", ("y = log_3(x − 5)",
                         "The argument must be positive: `x − 5 &gt; 0`, so the domain "
                         "is `x &gt; 5` and the asymptote is the vertical line `x = 5`. "
                         "The curve passes through `(6, 0)`, because `x − 5 = 1` there "
                         "and `log_3(1) = 0`, and through `(8, 1)`, because `x − 5 = 3` "
                         "and `log_3(3) = 1`. It is the standard shape, five units to "
                         "the right.")),
            ("p", "One case worth having met early: the domain is decided by the "
                  "argument being positive, not by `x` being positive. `log_2(x²)` is "
                  "defined for every `x ≠ 0`, negative values included, because `x²` "
                  "is positive there. Lesson 6 shows why that makes one of the three "
                  "laws need a careful statement."),
        ],
        "lab": ("logarithm", {
            "mode": "graph",
            "panel_title": "Two curves and the mirror between them",
            "panel_intro": "Pick a base and the lab draws `b^x` and `log_b(x)` with "
                           "`y = x` between them, each carrying the asymptote the "
                           "other one's line became. Move a point on one curve and "
                           "watch its mirror move on the other.",
        }),
        "steps_title": "Sketching y = log_b(x)",
        "steps_intro": "Four marks on the page, in this order, and the shape is fixed.",
        "steps": [
            ("Draw the asymptote first, dashed",
             "`x = 0`, or `x = h` if the argument is `x − h`. Putting it down before "
             "the curve stops the sketch from wandering into a region where the "
             "function does not exist."),
            ("Plot the two free points",
             "`(1, 0)` and `(b, 1)` lie on every logarithmic curve, straight from the "
             "definition. For base `3` they are `(1, 0)` and `(3, 1)`; shift both if "
             "the argument is shifted."),
            ("Add one point on the other side of x = 1",
             "`(1/b, −1)`. Without it the sketch tends to stop at the axis instead of "
             "diving, and the diving part is the half that carries the asymptote."),
            ("Write the domain beside the sketch",
             "`x &gt; 0`, or whatever makes the argument positive. A logarithmic graph "
             "without its domain is the half of the answer that gets marked wrong, and "
             "it is the half lesson 10 depends on."),
        ],
        "worked": {
            "title": "Base 2, then the same curve shifted",
            "intro": ["The first block is one table read twice. The second is what "
                      "happens to every one of those facts when the argument changes."],
            "lines": [
                "y = 2^x                          y = log_2(x)",
                "  (−3, 1/8)                        (1/8, −3)",
                "  (−1, 1/2)                        (1/2, −1)",
                "  ( 0, 1)                          (1, 0)",
                "  ( 1, 2)                          (2, 1)",
                "  ( 3, 8)                          (8, 3)",
                "",
                "  domain: all real x               domain: x > 0",
                "  range:  y > 0                    range:  all real y",
                "  asymptote y = 0                  asymptote x = 0",
                "",
                "now   y = log_2(x − 5)",
                "",
                "  argument positive    x − 5 > 0    ⟹    x > 5",
                "  asymptote            x = 5",
                "  x − 5 = 1            x = 6                y = 0",
                "  x − 5 = 2            x = 7                y = 1",
                "  x − 5 = 4            x = 9                y = 2",
                "  x − 5 = 1/2          x = 11/2             y = −1",
            ],
            "after": [
                "The domain `x &gt; 5` is not a decoration on the answer. "
                "`log_2(2 − 5) = log_2(−3)` names no real number, so the curve has "
                "nothing at all to the left of `5`, and a candidate solution of "
                "`x = 2` to any equation built from this expression is not a solution. "
                "Lesson 10 is built on precisely that check.",
                "Note that the shift moved the two free points too. `(1, 0)` became "
                "`(6, 0)` and `(2, 1)` became `(7, 1)`. Nothing about the shape "
                "changed; every landmark moved five to the right, the asymptote "
                "included.",
            ],
        },
        "quiz_title": "Domain, points, direction",
        "quiz": [
            {"q": "What is the domain of `g(x) = log_3(x − 5)`?",
             "a": ["`x &gt; 0`", "`x &gt; 5`", "`x ≥ 5`",
                   "Every real number except `5`"],
             "c": 1,
             "why": "The argument has to be positive: `x − 5 &gt; 0` gives `x &gt; 5`. "
                    "`x = 5` itself would give `log_3(0)`, which is undefined, so the "
                    "inequality is strict. The first choice reads the domain off the "
                    "unshifted `log_3(x)` and ignores what is inside the brackets."},
            {"q": "Every graph `y = log_b(x)` passes through which point?",
             "a": ["`(0, 1)`", "`(0, 0)`", "`(1, 0)`", "`(b, 0)`"],
             "c": 2,
             "why": "`b^0 = 1` for every allowed base, so `log_b(1) = 0`. `x = 0` is "
                    "outside the domain, which rules out the first two outright, and "
                    "the other guaranteed point is `(b, 1)` rather than `(b, 0)`."},
            {"q": "`log_10(x) = 6` when `x` is:",
             "a": ["`60`", "`600000`", "`1000000`", "`60466176`"],
             "c": 2,
             "why": "`10⁶ = 1000000`. `60` multiplies the base by the value; `600000` "
                    "is `6·10⁵`, a place short; `60466176` is `6¹⁰`, the base and the "
                    "exponent swapped over."},
        ],
        "mistakes": [
            ("Giving the domain of log_b(x − 5) as x > 0",
             "The rule is that the argument is positive, and the argument here is "
             "`x − 5`. Solve `x − 5 &gt; 0`. Reading the domain off the bare "
             "`log_b(x)` skips the shift, and the shift is the only thing that "
             "changed."),
            ("Expecting the curve to level off",
             "`log_b(x)` has no upper bound. It climbs slowly &mdash; `log_10` needs "
             "an input of `10¹⁰⁰` to reach `100` &mdash; but every height is reached "
             "in the end. Slow is not the same as bounded, and on a drawing they look "
             "identical."),
            ("Reflecting in the wrong line",
             "The inverse is the reflection in `y = x`, which exchanges the "
             "coordinates. Reflecting in the horizontal axis gives `y = −b^x` and "
             "reflecting in the vertical axis gives `y = b^(−x)`. Neither is a "
             "logarithm, and neither has a vertical asymptote."),
        ],
        "standard": ("Finish when you state domain, asymptote and two points before "
                     "drawing anything.",
                     "Given `y = log_5(x + 2)` you should say: domain `x &gt; −2`, "
                     "asymptote `x = −2`, through `(−1, 0)` and `(3, 1)`, increasing. "
                     "If you need a table of values to get there, the reflection has "
                     "not landed as a fact you can use."),
        "note": "The lab draws both curves from one base with `y = x` between them, so "
                "the reflection is something you watch rather than something you take "
                "on trust. If a sketch of yours disagrees with the picture there, it is "
                "worth finding out which landmark you moved &mdash; it is almost always "
                "the asymptote.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "the-laws-of-logarithms",
        "title": "The Laws of Logarithms",
        "module": "Logarithms",
        "one_line": "Three laws, which are the exponent laws read backwards.",
        "summary": (
            "Three laws turn a product into a sum, a quotient into a difference, and "
            "a power into a multiple. Each one is a single exponent law from course 1 "
            "written in the other notation, and each is proved in two lines from the "
            "definition. Two more rules that look like laws are not."
        ),
        "key": [
            "log_b(M·N)  =  log_b M + log_b N      from   b^m · b^n = b^(m+n)",
            "log_b(M/N)  =  log_b M − log_b N      from   b^m / b^n = b^(m−n)",
            "log_b(M^p)  =  p · log_b M            from   (b^m)^p  = b^(mp)",
            "NOT laws:   log(M + N),    log M / log N,    (log M)(log N)",
        ],
        "key_label": "Three laws, and three things that are not",
        "concepts_intro": (
            "Nothing here is new mathematics. It is the exponent laws you already "
            "have, said in the notation of lesson 4."
        ),
        "concepts": [
            ("The laws are the exponent laws in other clothes",
             "Multiplying powers of the same base adds the exponents. A logarithm is "
             "an exponent. So the logarithm of a product is the sum of the logarithms "
             "&mdash; not a coincidence and not a separate fact, but the same "
             "statement written twice."),
            ("There is no law for a sum",
             "`log_b(M + N)` does not simplify. Not to `log_b M + log_b N`, not to "
             "anything. Addition inside the argument has no counterpart outside it, "
             "and inventing one is the most expensive habit available in this course."),
            ("Every law needs positive arguments",
             "`log_b(M·N) = log_b M + log_b N` requires `M &gt; 0` and `N &gt; 0`, or "
             "the right-hand side names nothing. The usual casualty is "
             "`log_b(x²) = 2·log_b(x)`, which fails for negative `x`: the correct "
             "identity is `log_b(x²) = 2·log_b|x|`."),
        ],
        "read_title": "Three laws and their proofs",
        "read_intro": "Where each law comes from, what it is allowed to touch, and the "
                      "two rules people invent in their place.",
        "body": [
            ("p", "Fix a base `b` and take `M &gt; 0`, `N &gt; 0`. Write "
                  "`m = log_b M` and `n = log_b N`, which by the definition means "
                  "`M = b^m` and `N = b^n`. Every proof below is that substitution "
                  "followed by one exponent law."),
            ("thm", ("The product law",
                     "`log_b(M·N) = log_b(M) + log_b(N)` for all `M &gt; 0` and "
                     "`N &gt; 0`.")),
            ("proof", [
                "`M·N = b^m·b^n = b^(m+n)` by the exponent law for a product. So "
                "`m + n` is the exponent that produces `M·N`, and by the definition of "
                "a logarithm that is exactly what `log_b(M·N)` means. Hence "
                "`log_b(M·N) = m + n = log_b M + log_b N`.",
            ]),
            ("thm", ("The quotient law",
                     "`log_b(M/N) = log_b(M) − log_b(N)` for all `M &gt; 0` and "
                     "`N &gt; 0`.")),
            ("proof", [
                "`M/N = b^m/b^n = b^(m−n)`. So `m − n` is the exponent that produces "
                "`M/N`, which gives `log_b(M/N) = m − n = log_b M − log_b N`. The "
                "subtraction on the right is where the sign is lost in practice, and "
                "the order matters: `log_b(N/M)` is the negative of this.",
            ]),
            ("thm", ("The power law",
                     "`log_b(M^p) = p·log_b(M)` for all `M &gt; 0` and every real `p`.")),
            ("proof", [
                "`M^p = (b^m)^p = b^(mp)` by the exponent law for a power of a power. "
                "So `mp` is the exponent that produces `M^p`, and "
                "`log_b(M^p) = mp = p·log_b M`. Note that `p` is unrestricted: it may "
                "be negative, or a fraction, which is what lets a root come out as a "
                "coefficient.",
            ]),
            ("p", "A number check is not a proof, but it is a fast way to catch a "
                  "misremembered law. `log_2(8·4) = log_2(32) = 5`, and "
                  "`log_2(8) + log_2(4) = 3 + 2 = 5`. If a rule you are about to use "
                  "fails on numbers you can evaluate by hand, it is not a rule."),
            ("h3", "The two invented laws"),
            ("math", [
                "log_2(8 + 8)  =  log_2(16)  =  4",
                "log_2(8) + log_2(8)         =  3 + 3  =  6        not equal",
                "",
                "log_2(8/4)    =  log_2(2)   =  1",
                "log_2(8) / log_2(4)         =  3/2               not equal",
            ]),
            ("p", "The first is the sum error and there is nothing to rescue in it. "
                  "The second is more interesting, because the quotient "
                  "`log_b(M)/log_b(N)` is not meaningless &mdash; it equals "
                  "`log_N(M)`. Here `log_2(8)/log_2(4) = 3/2`, and `log_4(8)` is "
                  "indeed `3/2`. A ratio of two logarithms is a change of base, which "
                  "lesson 8 makes into a rule; it is not the logarithm of a ratio."),
            ("h3", "Expanding and condensing"),
            ("p", "Expanding means using the laws left to right, until every logarithm "
                  "has a single letter inside it. Condensing means the reverse: "
                  "coefficients go back up as exponents, sums become products, "
                  "differences become quotients, and the whole expression ends as one "
                  "logarithm. Both directions are needed &mdash; expanding to "
                  "differentiate later, condensing to solve equations in lesson 10."),
            ("example", ("A restriction that is easy to lose",
                         "`log_b(x²) = 2·log_b(x)` is true for `x &gt; 0` and false "
                         "for `x &lt; 0`. At `x = −5` the left side is `log_b(25)`, a "
                         "perfectly good number, and the right side is `2·log_b(−5)`, "
                         "which is not defined at all. The identity that holds "
                         "everywhere except `x = 0` is `log_b(x²) = 2·log_b|x|`. "
                         "Expanding a logarithm can shrink its domain, and the answer "
                         "should say so.")),
        ],
        "lab": ("logarithm", {
            "mode": "laws",
            "panel_title": "Each law, checked on your numbers",
            "panel_intro": "Enter a base and two arguments and the lab evaluates both "
                           "sides of each law exactly. The two invented rules, "
                           "`log(M + N) = log M + log N` and "
                           "`log(M/N) = log M / log N`, are computed alongside and "
                           "shown failing on the same numbers rather than merely "
                           "warned about.",
        }),
        "steps_title": "Expanding a logarithm",
        "steps_intro": "Work from the outside in. Doing it the other way re-creates "
                       "brackets you then have to remove.",
        "steps": [
            ("Split the outermost structure first",
             "If the argument is a quotient, use the quotient law before anything "
             "else; then split the products; only then bring exponents down. The "
             "outermost operation is the one the logarithm is applied to."),
            ("Write every root as an exponent",
             "`√y` is `y^(1/2)` and `∛y` is `y^(1/3)`. The power law does not "
             "recognise a root sign, so convert first &mdash; the coefficient `1/2` "
             "comes out of that conversion, not out of nowhere."),
            ("Bring each exponent down as a coefficient",
             "`log_b(x³)` becomes `3·log_b(x)`. The exponent must sit on the whole "
             "argument of that logarithm: in `log_b((x + 1)³)` the cube is on the "
             "bracket and comes down, while in `log_b(x³ + 1)` it is on `x` alone and "
             "nothing comes down."),
            ("State the restriction",
             "The expansion is valid where every logarithm in it is defined. For "
             "`log_b(x³·√y / z²)` that means `x &gt; 0`, `y &gt; 0` and `z &gt; 0`, "
             "and the answer is incomplete without it."),
        ],
        "worked": {
            "title": "One expansion, checked on numbers, then reversed",
            "intro": ["The expansion is four lines. The check is four more, and it is "
                      "worth every one of them."],
            "lines": [
                "expand      log_b( x³·√y / z² ),     x > 0,  y > 0,  z > 0",
                "",
                "  quotient law    log_b(x³·√y) − log_b(z²)",
                "  product law     log_b(x³) + log_b(√y) − log_b(z²)",
                "  root as power   log_b(x³) + log_b(y^(1/2)) − log_b(z²)",
                "  power law       3·log_b(x) + (1/2)·log_b(y) − 2·log_b(z)",
                "",
                "check on numbers:   b = 2,   x = 8,   y = 16,   z = 4",
                "",
                "  inside      8³ = 512      √16 = 4      4² = 16",
                "              512 · 4 / 16  =  128",
                "  left        log_2(128)  =  7",
                "  right       3·log_2(8) + (1/2)·log_2(16) − 2·log_2(4)",
                "            = 3·3        + (1/2)·4        − 2·2",
                "            = 9 + 2 − 4",
                "            = 7                                        ✓",
                "",
                "condense    2·log_b(x) + (1/3)·log_b(y) − log_b(z)",
                "",
                "  power law       log_b(x²) + log_b(y^(1/3)) − log_b(z)",
                "  product law     log_b(x²·∛y) − log_b(z)",
                "  quotient law    log_b( x²·∛y / z )",
            ],
            "after": [
                "The check catches the two failures worth catching: a coefficient that "
                "never came down, and a sign lost on the quotient. If the right-hand "
                "column had come to `15` you would know the `−2·log_2(4)` had been "
                "added instead of subtracted, before the mistake travelled any further.",
                "It confirms the expansion at one point and nowhere else. The proof "
                "that it holds for every positive `x`, `y` and `z` is the two-line "
                "derivation of each law above &mdash; a numeric check can refute a "
                "false rule but cannot establish a true one.",
            ],
        },
        "quiz_title": "Laws, and things that are not laws",
        "quiz": [
            {"q": "What is `log_2(8 + 8)`?",
             "a": ["`6`", "`4`", "`9`", "`16`"],
             "c": 1,
             "why": "`8 + 8 = 16` and `2⁴ = 16`, so the value is `4`. `6` is what the "
                    "invented sum law gives, `log_2 8 + log_2 8 = 3 + 3`; `9` "
                    "multiplies the two logarithms instead; `16` is the argument "
                    "itself, not its logarithm."},
            {"q": "For `x &gt; 0` and `y &gt; 0`, `log_b(x³/y)` expands to:",
             "a": ["`3·log_b(x) − log_b(y)`", "`3·log_b(x) / log_b(y)`",
                   "`log_b(3x) − log_b(y)`", "`3·(log_b(x) − log_b(y))`"],
             "c": 0,
             "why": "Quotient law first, then the power law on `x³`. The second choice "
                    "divides where the law subtracts; the third turns a power into a "
                    "coefficient inside the argument; the fourth distributes the `3` "
                    "across the subtraction, which produces `−3·log_b(y)` where "
                    "`−log_b(y)` belongs."},
            {"q": "Condensed into a single logarithm, `log 5 + 2·log 3` is:",
             "a": ["`log 11`", "`log 45`", "`log 30`", "`log 225`"],
             "c": 1,
             "why": "`2·log 3 = log 3² = log 9`, and `log 5 + log 9 = log(5·9) = "
                    "log 45`. `log 11` comes from adding `5 + 2·3`; `log 30` from "
                    "multiplying by the coefficient, `5·3·2`, rather than raising to "
                    "it; `log 225` from squaring the whole product, `(5·3)²`."},
        ],
        "mistakes": [
            ("Splitting the logarithm of a sum",
             "`log_b(x + 3)` is not `log_b(x) + log_b(3)`. Test it once with numbers "
             "you can evaluate: `log_2(8 + 8) = 4` while `log_2(8) + log_2(8) = 6`. "
             "There is no law for addition inside the argument, and no amount of "
             "rearranging produces one."),
            ("Turning a quotient of logarithms into a logarithm of a quotient",
             "`log_b(M)/log_b(N)` is not `log_b(M/N)`. On numbers: "
             "`log_2(8)/log_2(4) = 3/2` while `log_2(8/4) = 1`. The quotient of two "
             "logarithms is a change of base &mdash; it equals `log_N(M)` &mdash; and "
             "lesson 8 puts that to work rather than throwing it away."),
            ("Bringing down an exponent that is not on the whole argument",
             "In `log_b(x² + 1)` the square sits on `x`, so the power law does not "
             "apply and the expression does not expand at all. The law needs the "
             "exponent on everything the logarithm is applied to, as in "
             "`log_b((x + 1)²) = 2·log_b(x + 1)`."),
        ],
        "standard": ("Finish when you can go both directions and state the "
                     "restriction.",
                     "Given `log_b(x²·√y / z³)` you should produce "
                     "`2·log_b(x) + (1/2)·log_b(y) − 3·log_b(z)` with "
                     "`x, y, z &gt; 0`, and turn it back again. If the order of the "
                     "laws is ever in doubt, work outermost first and the doubt does "
                     "not arise."),
        "note": "Lesson 7 gives base 10 and base `e` their own notation, `log` and "
                "`ln`, and lesson 8 turns the ratio `log_c(x)/log_c(b)` into the "
                "change-of-base rule. These three laws hold in every base, so nothing "
                "written here has to be relearned when the subscript disappears.",
    },
]
