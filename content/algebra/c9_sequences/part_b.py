"""Course 9, lessons 07-11 - infinite series, an application, and the binomial theorem."""

LESSONS = [
    # ---------------------------------------------------------------- 07
    {
        "slug": "repeating-decimals-as-series",
        "title": "Repeating Decimals as Series",
        "module": "Infinite series",
        "one_line": "Why 0.999... is 1, settled by the sum formula.",
        "summary": (
            "A decimal expansion is a series: `0.d₁d₂d₃…` is shorthand for "
            "`d₁/10 + d₂/100 + d₃/1000 + …` . When a block of digits repeats, that "
            "series is geometric with `|r| &lt; 1`, so it has a sum and the sum is a "
            "fraction. The same argument settles `0.999… = 1`, which turns out to be a "
            "fact about notation rather than a paradox."
        ),
        "key": [
            "0.d₁d₂d₃…  =  d₁/10 + d₂/100 + d₃/1000 + …",
            "a block of p digits repeating:   a₁ = block/10ᵖ,   r = 1/10ᵖ",
            "0.454545…  =  (45/100)/(1 - 1/100)  =  45/99  =  5/11",
            "0.999…     =  (9/10)/(1 - 1/10)     =  1",
        ],
        "key_label": "A decimal is a series, and a repeating one is geometric",
        "concepts_intro": (
            "Nothing new is proved here. The infinite geometric sum is applied to the "
            "notation everyone has been using for numbers since primary school."
        ),
        "concepts": [
            ("A decimal expansion is already an infinite sum",
             "`0.333…` is not a number waiting to be finished; it is the series "
             "`3/10 + 3/100 + 3/1000 + …` , and its value is the number the partial "
             "sums `0.3, 0.33, 0.333, …` approach. Finite decimals are the same "
             "statement with all but a few digits equal to `0`."),
            ("A repeating block always gives |r| < 1",
             "If the block is `p` digits long, the ratio is `1/10ᵖ`, and `1/10ᵖ` is "
             "less than `1` for every `p ≥ 1`. So the convergence test never fails for "
             "a repeating decimal: the sum exists, whatever the digits are, and it is "
             "a ratio of whole numbers."),
            ("0.999… = 1 is an equality between two names",
             "The two strings of symbols denote the same real number, in the way that "
             "`1/2` and `2/4` do. There is no last `9`, so there is no gap of "
             "`0.000…1` &mdash; that string does not name a real number, because a "
             "positive number smaller than every `1/10ⁿ` does not exist."),
        ],
        "read_title": "What a decimal means, and what repeating does to it",
        "read_intro": "Place value written as a series, the block conversion in "
                      "both directions, and the one number with two decimal names.",
        "body": [
            ("def", ("Decimal expansion",
                     "For digits `d₁, d₂, d₃, …` each in `0` to `9`, the notation "
                     "`0.d₁d₂d₃…` denotes the sum of the series "
                     "`d₁/10 + d₂/100 + d₃/1000 + …` , that is, the number its partial "
                     "sums approach. The expansion <strong>terminates</strong> if every "
                     "digit from some point on is `0`, and <strong>repeats</strong> if "
                     "from some point on a fixed block of digits recurs for ever.")),
            ("p", "This is what place value has always meant. `0.25` is "
                  "`2/10 + 5/100 = 1/4`, a sum of two terms, and `0.333…` is the same "
                  "kind of sum with no last term. The only difference is that the "
                  "second one needs the partial sums to settle before it denotes "
                  "anything, and the infinite geometric series is exactly the tool that "
                  "says when they do. Notation for the repeating block varies: a bar "
                  "over the block, a dot over each end of it, or an ellipsis after two "
                  "or three copies. All three are in use and the choice between them is "
                  "arbitrary. This course writes the block out two or three "
                  "times and then `…` , so `0.454545…` means the `45` goes on "
                  "for ever."),
            ("h3", "A repeating block is a geometric series"),
            ("p", "Take `0.454545…` . The block `45` occupies the first two decimal "
                  "places, then the next two, then the next two, so the series is "
                  "`45/100 + 45/10000 + 45/1000000 + …` . Each term is the one before "
                  "divided by `100`."),
            ("math", [
                "0.454545…  =  45/100 + 45/100² + 45/100³ + …",
                "",
                "a₁ = 45/100     r = 1/100     |r| < 1, so there is a sum",
                "",
                "S∞ = (45/100)/(1 - 1/100)  =  (45/100)/(99/100)  =  45/99  =  5/11",
                "",
                "partial sums   0.45,  0.4545,  0.454545,  …   climbing toward 5/11",
            ]),
            ("thm", ("Every repeating decimal is a rational number",
                     "Suppose the expansion repeats a block `B` of `p` digits, starting "
                     "immediately after the decimal point. Then the number is "
                     "`B/(10ᵖ - 1)`: the series has `a₁ = B/10ᵖ` and `r = 1/10ᵖ`, and "
                     "`|r| &lt; 1` holds for every `p ≥ 1`.",
                     "If a few fixed digits come first, the repeating tail is divided "
                     "by a further power of ten and the fixed part is added back, which "
                     "changes the arithmetic but not the conclusion.")),
            ("proof", [
                "With `a₁ = B/10ᵖ` and `r = 1/10ᵖ`, the sum formula gives "
                "`S∞ = (B/10ᵖ)/(1 - 1/10ᵖ)`. Multiply numerator and denominator by "
                "`10ᵖ`: the numerator becomes `B` and the denominator becomes "
                "`10ᵖ - 1`, which is the string of `p` nines.",
                "Both `B` and `10ᵖ - 1` are whole numbers and `10ᵖ - 1` is not zero, so "
                "the sum is a ratio of whole numbers. Adding the fixed head, itself a "
                "terminating decimal and so a fraction, keeps it one.",
            ]),
            ("p", "The school method &mdash; call the number `x`, multiply by a power "
                  "of ten, subtract &mdash; is this proof compressed. Multiplying "
                  "`0.454545…` by `100` shifts the whole tail one block to the left, so "
                  "`100x` and `x` have identical tails and everything cancels except "
                  "the block that falls out in front. It is the `Sₙ - rSₙ` manoeuvre "
                  "with the shift run the other way: there the second line was `r` "
                  "times the first, here it is `1/r` times."),
            ("math", [
                "x = 0.BBBBB…              B is a block of p digits",
                "10ᵖx = B.BBBBB…           the tail is unchanged, one block earlier",
                "10ᵖx - x = B              the two tails cancel exactly",
                "(10ᵖ - 1)x = B",
                "x = B/(10ᵖ - 1)           p nines underneath",
            ]),
            ("h3", "0.999… and the number it is"),
            ("example", ("0.999… = 1, three ways of seeing the same fact",
                         "By the formula: `a₁ = 9/10`, `r = 1/10`, so "
                         "`S∞ = (9/10)/(9/10) = 1`. By the block rule: `B = 9` and "
                         "`p = 1`, so the value is `9/9 = 1`. By thirds: `0.333… = 1/3` "
                         "is uncontroversial, and multiplying both sides by `3` gives "
                         "`0.999… = 1`.")),
            ("p", "The objection people raise is that the partial sums "
                  "`0.9, 0.99, 0.999, …` are all less than `1`, so the total must be "
                  "too. Every one of those partial sums is indeed less than `1`. The "
                  "sum of the series is not one of them; it is the number they "
                  "approach. The gap `1 - 0.99…9` with `n` nines is exactly `1/10ⁿ`, "
                  "and no positive number is smaller than every `1/10ⁿ`, so a number "
                  "differing from `1` by less than all of them differs from it by `0`. A consequence is that "
                  "decimal names are not quite unique: every "
                  "terminating decimal has a second name ending in repeating nines, "
                  "`0.25 = 0.24999…` , since `24/100 + (9/1000)/(1 - 1/10)` is "
                  "`6/25 + 1/100 = 1/4`. This is the only ambiguity there is &mdash; a "
                  "number with no terminating expansion has exactly one decimal name."),
            ("h3", "The other direction: which fractions repeat"),
            ("p", "Dividing a whole number by `q` by hand produces a remainder at "
                  "every step, and each remainder is one of `0, 1, …, q - 1`. Either "
                  "`0` turns up, and the expansion terminates, or within `q` steps some "
                  "earlier remainder recurs &mdash; and once a remainder recurs the "
                  "digits after it repeat exactly as they did before, because the same "
                  "remainder produces the same next digit. So every fraction terminates "
                  "or repeats, with a block shorter than `q`; there is no third "
                  "behaviour."),
            ("example", ("Three divisions",
                         "`1/7 = 0.142857142857…` , a block of six, which is the longest "
                         "a denominator of `7` allows. `1/13 = 0.076923076923…` , also "
                         "six. `3/40 = 0.075` exactly, because `40 = 2³·5` and a "
                         "denominator built only from `2`s and `5`s can be turned into "
                         "a power of ten: `3/40 = 75/1000`.")),
            ("p", "Putting the two directions together: a number is rational exactly "
                  "when its decimal expansion terminates or repeats. Course 1 sorted "
                  "the reals into rational and irrational and asserted this; the "
                  "geometric series is what turns the assertion into an argument. It "
                  "also gives a way to write down an irrational number on demand &mdash; "
                  "`0.101001000100001…` , with one more zero in each gap, never repeats "
                  "and so cannot be a fraction."),
        ],
        "lab": ("sequence", {
            "mode": "repeating",
            "panel_title": "Digits in, fraction out",
            "panel_intro": "Enter a repeating decimal and the lab writes it as a "
                           "geometric series, adds the partial sums one at a time, and "
                           "computes `a₁/(1 - r)` beside them, printing both. Leave the "
                           "first box empty, put `9` in the repeating block, and watch "
                           "`0.9, 0.99, 0.999` climb toward the `1` the formula returns.",
        }),
        "steps_title": "Turning a repeating decimal into a fraction",
        "steps_intro": "The work is in the first step. Once the head and the tail "
                       "are separated the rest is the sum formula.",
        "steps": [
            ("Split the fixed head from the repeating tail",
             "In `0.2454545…` the head is `0.2` and the tail is the block `45` starting "
             "at the third decimal place. Count the digits in each: one fixed digit and "
             "a block of two."),
            ("Write the tail as a geometric series",
             "Its first term is the block over `10` to the power of the position it "
             "ends at, and its ratio is `1/10ᵖ` where `p` is the length of the block. "
             "For `0.2454545…` that is `a₁ = 45/1000` and `r = 1/100`."),
            ("Sum the tail and add the head back",
             "`S∞ = a₁/(1 - r)`, then add the head as a fraction. Clear the compound "
             "fraction by multiplying numerator and denominator by `10ᵖ` rather than "
             "reaching for decimals."),
            ("Divide the answer back out",
             "Long division of the fraction you produced must reproduce the digits you "
             "started from. It is the one check that tests the calculation end to end, "
             "and it catches a misplaced power of ten immediately."),
        ],
        "worked": {
            "title": "0.2454545… as a fraction, two ways",
            "intro": [
                "One fixed digit and then a two-digit block. Both routes are worked in "
                "full because the second is the first one compressed, and it is worth "
                "seeing that they are the same calculation.",
            ],
            "lines": [
                "x = 0.2454545…        head 2,  then the block 45 repeating",
                "",
                "as a series",
                "  x = 2/10 + 45/1000 + 45/100000 + 45/10000000 + …",
                "            tail:  a₁ = 45/1000,   r = 1/100,   |r| < 1",
                "",
                "  tail = (45/1000)/(1 - 1/100) = (45/1000)/(99/100)",
                "       = (45/1000)·(100/99) = 4500/99000 = 45/990 = 1/22",
                "",
                "  x = 1/5 + 1/22 = 22/110 + 5/110 = 27/110",
                "",
                "by shifting and subtracting",
                "     10x =   2.454545…        the block now starts at the point",
                "   1000x = 245.454545…        one whole block further along",
                "   1000x - 10x = 245 - 2 = 243        the tails cancel",
                "   990x = 243",
                "   x = 243/990 = 27/110                          ✓ agrees",
                "",
                "check by dividing back",
                "   110 into 27.000…  gives  0.2454545…           ✓",
                "   partial sums  0.245,  0.24545,  0.2454545,  …",
            ],
            "after": [
                "Both routes were carried out and both produced `27/110`, which is one "
                "instance checked rather than a rule established; what makes the method "
                "correct in general is the cancellation in the proof above.",
                "The denominator explains itself. `990 = 99·10`: the `99` is the two "
                "nines belonging to a two-digit block, and the `10` is the single fixed "
                "digit delaying it. After cancelling, `110 = 2·5·11`, and the `11` is "
                "the reason this decimal repeats at all &mdash; a denominator carrying "
                "any prime other than `2` and `5` cannot be written over a power of "
                "ten.",
            ],
        },
        "quiz_title": "Decimals and fractions",
        "quiz": [
            {"q": "Write `0.727272…` as a fraction in lowest terms.",
             "a": ["`18/25`", "`8/11`", "`8/111`", "`4/5`"],
             "c": 1,
             "why": "The block is `72`, two digits, so `a₁ = 72/100` and `r = 1/100`, "
                    "giving `(72/100)/(99/100) = 72/99 = 8/11`. `18/25` is `72/100`, "
                    "the first term on its own &mdash; the value of `0.72`. `8/111` is "
                    "`72/999`, which uses three nines for a two-digit block. `4/5` is "
                    "`72/90`, the denominator that belongs to one fixed digit followed "
                    "by one repeating digit, applied here with nothing subtracted from "
                    "the numerator either."},
            {"q": "Which statement about `0.999…` is correct?",
             "a": ["It is the largest real number less than `1`.",
                   "It differs from `1` by `0.000…1`, a positive number smaller than every fraction.",
                   "It equals `1`: the partial sums `0.9, 0.99, 0.999, …` approach "
                   "`1`, and the sum of the series is defined to be that value.",
                   "It gets closer and closer to `1` without reaching it, so the two are different numbers."],
             "c": 2,
             "why": "There is no largest real number below `1`, since the average of "
                    "any candidate and `1` would be larger. `0.000…1` names nothing: a "
                    "positive number below every `1/10ⁿ` does not exist. The fourth "
                    "confuses the partial sums with the series; the partial sums do "
                    "climb without reaching `1`, and the sum is the number they climb "
                    "toward."},
            {"q": "Which of these fractions has a terminating decimal expansion?",
             "a": ["`7/12`", "`3/40`", "`5/11`", "`1/6`"],
             "c": 1,
             "why": "In lowest terms an expansion terminates exactly when the "
                    "denominator has no prime factor other than `2` and `5`, because "
                    "only then can it be written over a power of ten. `40 = 2³·5`, and "
                    "`3/40 = 75/1000 = 0.075`. The others carry a `3`, an `11` and a "
                    "`3`, and repeat: `0.58333…` , `0.454545…` and `0.1666…` ."},
        ],
        "mistakes": [
            ("Using the wrong number of nines for the block",
             "`0.123123…` is `123/999`, which reduces to `41/333`. Writing `123/99` "
             "uses two nines for a three-digit block and `123/1000` treats the decimal "
             "as terminating. The count of nines is the length of the block, not the "
             "size of the number in it."),
            ("Leaving the fixed head in the numerator",
             "The compressed form of the calculation for `0.2454545…` is "
             "`(245 - 2)/990`: the digits up to the end of the first block, minus the "
             "digits that do not repeat. Writing `245/990` instead gives `49/198`, "
             "which is `0.2474747…` &mdash; a different number, and one close enough to "
             "the original to survive a glance."),
            ("Arguing that 0.999… is below 1 because every partial sum is",
             "Each partial sum `0.99…9` really is less than `1`, by exactly `1/10ⁿ`. "
             "The property does not carry over to the number they approach, any more "
             "than every term of `1/n` being positive makes the value they approach "
             "positive. What is true of every partial sum need not be true of the sum."),
        ],
        "standard": ("Finish when a repeating decimal reads as a geometric series without any translation.",
                     "You should be able to convert either way between a repeating "
                     "decimal and a fraction, in both the plain and the delayed-block "
                     "cases, and defend `0.999… = 1` without appealing to authority. "
                     "Being able to say why `1/7` repeats and `3/40` does not is part "
                     "of it."),
        "note": "Everything so far has summed abstract terms. The next lesson spends "
                "the same two formulas on money: a payment made at the end of every "
                "period, each one earning interest for a different length of time, is a "
                "geometric series in disguise, and the question of what a stream of "
                "payments continuing for ever is worth today is an `|r| &lt; 1` "
                "question with a bank behind it.",
    },
    # ---------------------------------------------------------------- 08
    {
        "slug": "annuities-and-accumulated-payments",
        "title": "Annuities and Accumulated Payments",
        "module": "Applications",
        "one_line": "A stream of payments is a geometric series.",
        "summary": (
            "Equal payments made at equal intervals, each earning interest for a "
            "different length of time, accumulate to a geometric series with "
            "`r = 1 + i`. Discounting the same payments back to today instead gives "
            "`r = 1/(1 + i)`, and letting them run for ever is the one case that needs "
            "`|r| &lt; 1`. All three are the same sum formula."
        ),
        "key": [
            "n payments of P, rate i per period, paid at the end of each period",
            "accumulated    S = P[(1 + i)ⁿ - 1]/i        r = 1 + i,  greater than 1",
            "present value  A = P[1 - (1 + i)⁻ⁿ]/i       r = 1/(1 + i),  less than 1",
            "for ever       A = P/i                      the case that needs |r| < 1",
        ],
        "key_label": "One stream of payments, three questions",
        "concepts_intro": (
            "No new mathematics appears in this lesson. What is new is reading a "
            "situation and recognising which geometric series it is."
        ),
        "concepts": [
            ("Every payment has its own clock",
             "A payment made at the end of period `k` sits in the account for the "
             "remaining `n - k` periods, so it is worth `P(1 + i)ⁿ⁻ᵏ` at the end. The "
             "last payment earns nothing at all. Listing the payments from the last "
             "backwards gives `P, P(1 + i), P(1 + i)², …` , which is geometric with "
             "first term `P`."),
            ("r = 1 + i is greater than 1, and that is allowed",
             "The condition `|r| &lt; 1` belongs to the infinite sum and to nothing "
             "else. `Sₙ = a₁(1 - rⁿ)/(1 - r)` needs only `r ≠ 1`, and an accumulation "
             "over `n` periods is a sum of `n` terms. Refusing the formula because "
             "`r &gt; 1` is an overcorrection: it withholds an exact answer to a "
             "question that has one."),
            ("The rate must be the rate per payment period",
             "If payments are monthly, `i` is a monthly rate and `n` counts months. "
             "Quoting `12%` a year and using `1%` a month is a convention &mdash; the "
             "nominal rate convention &mdash; and not a mathematical fact: `1%` a month "
             "compounds to about `12.68%` over a year, not `12%`. Which convention is "
             "in force has to come from the problem."),
        ],
        "read_title": "Payments, interest, and the two directions of time",
        "read_intro": "The accumulation of a stream of payments, the present value "
                      "of the same stream, and the payments that never stop.",
        "body": [
            ("def", ("Annuity",
                     "A sequence of equal payments made at equal intervals. In an "
                     "<strong>ordinary annuity</strong> each payment falls at the "
                     "<em>end</em> of its period; in an <strong>annuity-due</strong> "
                     "each falls at the beginning. The <strong>rate per period</strong> "
                     "`i` is the interest one period earns, written as a fraction: "
                     "`10%` is `i = 1/10`.",
                     "Everything below is stated for an ordinary annuity, which is the "
                     "usual convention for a savings plan or a loan repayment.")),
            ("p", "Take five payments of `1000`, one at the end of each year, into an "
                  "account paying `10%` a year. The first payment is deposited at the "
                  "end of year 1 and then sits there for four more years; the last is "
                  "deposited at the moment the account is closed and earns nothing."),
            ("math", [
                "P = 1000,  i = 1/10,  n = 5        value at the end of year 5",
                "",
                "payment 1   deposited end of year 1   1000(11/10)⁴ = 1464.10",
                "payment 2                             1000(11/10)³ = 1331.00",
                "payment 3                             1000(11/10)² = 1210.00",
                "payment 4                             1000(11/10)  = 1100.00",
                "payment 5   deposited at the close    1000          = 1000.00",
                "",
                "read from the bottom up:  1000, 1100, 1210, 1331, 1464.10",
                "a geometric sequence with a₁ = 1000 and r = 11/10",
            ]),
            ("p", "Reading the list from the last payment backwards is the whole trick. "
                  "In that order the first term is `P` and the ratio is `1 + i`, and "
                  "the sum of `n` such terms is what the sum formula already gives."),
            ("thm", ("Accumulated value of an ordinary annuity",
                     "`n` payments of `P`, one at the end of each period, at rate `i` "
                     "per period with `i ≠ 0`, are worth "
                     "`S = P[(1 + i)ⁿ - 1]/i` at the end of the last period.")),
            ("proof", [
                "The payments are worth `P, P(1 + i), …, P(1 + i)ⁿ⁻¹` at the close, "
                "which is geometric with `a₁ = P` and `r = 1 + i`. Since `i ≠ 0` we "
                "have `r ≠ 1`, so `Sₙ = a₁(1 - rⁿ)/(1 - r)` applies.",
                "Substituting, `1 - r = 1 - (1 + i) = -i`, so "
                "`S = P[1 - (1 + i)ⁿ]/(-i)`. Multiplying the numerator and the "
                "denominator by `-1` turns that into `P[(1 + i)ⁿ - 1]/i`, which is the "
                "same expression with both signs flipped rather than a different "
                "formula. The `Sₙ - rSₙ` cancellation is doing all the work; only the "
                "letters have changed.",
            ]),
            ("p", "Two checks are free. Putting `n = 1` gives "
                  "`S = P[(1 + i) - 1]/i = P`, the single payment itself. And at a "
                  "positive rate every payment is worth at least `P` at the close, so "
                  "`S` cannot come out below `nP` &mdash; here `5000` &mdash; which "
                  "rules out a whole class of arithmetic slips at a glance."),
            ("h3", "The same payments, valued today"),
            ("p", "The other question a stream of payments raises is what it is worth "
                  "now. A payment of `P` arriving in `k` periods is worth "
                  "`P/(1 + i)ᵏ` today, because that amount, left to compound, becomes "
                  "`P` in `k` periods. Adding those gives a geometric series again, "
                  "with first term `P/(1 + i)` and ratio `1/(1 + i)`."),
            ("math", [
                "A = P/(1 + i) + P/(1 + i)² + … + P/(1 + i)ⁿ",
                "",
                "a₁ = P/(1 + i)      r = 1/(1 + i)      1 - r = i/(1 + i)",
                "",
                "A = [P/(1 + i)]·[1 - (1 + i)⁻ⁿ]·[(1 + i)/i]",
                "  = P[1 - (1 + i)⁻ⁿ]/i",
            ]),
            ("example", ("Two payments of 100, at 25% a period",
                         "`i = 1/4`, `n = 2`. The payments are worth `100/(5/4) = 80` "
                         "and `100/(5/4)² = 64` today, totalling `144`. The formula "
                         "gives `100[1 - (4/5)²]/(1/4) = 100(9/25)(4) = 144`, the same "
                         "number. A rate that large is chosen so the arithmetic stays "
                         "exact; nothing in the derivation cares how big `i` is.")),
            ("h3", "Payments that never stop"),
            ("p", "A <strong>perpetuity</strong> pays `P` at the end of every period "
                  "for ever. Its present value is the infinite series "
                  "`P/(1 + i) + P/(1 + i)² + …` , and here the condition finally "
                  "matters: `r = 1/(1 + i)`, which is less than `1` whenever `i &gt; 0`. "
                  "So the sum exists, and it is "
                  "`[P/(1 + i)]/[i/(1 + i)] = P/i`."),
            ("example", ("1000 a year for ever, at 10%",
                         "`P/i = 1000/(1/10) = 10000`. That number is not a rounding of "
                         "an infinite total; it is the value the partial sums approach. "
                         "The first ten payments are worth about `6144.57` today, the "
                         "first fifty about `9914.81`, and the fiftieth payment alone "
                         "about `8.52` &mdash; the later payments contribute less and "
                         "less, which is why the total stays finite. Those three "
                         "figures are rounded to the cent; the underlying values are "
                         "exact fractions.")),
            ("p", "One practical warning about exactness. `(11/10)⁵` is "
                  "`161051/100000`, an exact fraction, and every figure in this lesson "
                  "is exact. A rate of `7%` a year over `30` years is equally exact and "
                  "far uglier, and it is tempting to round each term to the cent on the "
                  "way through. Round once, at the end: each of `360` monthly terms "
                  "rounded to the cent can be half a cent out, and `360` half-cents "
                  "is `1.80` &mdash; small, but enough for two people doing the same "
                  "calculation to disagree."),
        ],
        "lab": ("sequence", {
            "mode": "annuity",
            "panel_title": "Payments, and what they grow to",
            "panel_intro": "Set the payment, the rate per period and the number of "
                           "periods; the lab lists what each payment is worth at the "
                           "close, adds them term by term, and prints "
                           "`P[(1 + i)ⁿ - 1]/i` beside the total. Set the rate to `0` and "
                           "watch the total fall back to `nP`, the same payments with "
                           "no interest on any of them.",
        }),
        "steps_title": "Answering a question about a stream of payments",
        "steps_intro": "Two decisions come before any formula: what a period is, "
                       "and which end of the timeline the answer is wanted at.",
        "steps": [
            ("Fix the period and put the rate in its units",
             "Monthly payments mean a monthly `i` and an `n` counted in months. Convert "
             "before substituting, and say which convention you used if the problem "
             "quotes an annual rate."),
            ("Decide whether the answer is an accumulation or a present value",
             "\"What will it be worth when I stop paying\" is `P[(1 + i)ⁿ - 1]/i`. "
             "\"What is it worth now\" and \"how much can I borrow against it\" are "
             "`P[1 - (1 + i)⁻ⁿ]/i`. They differ by a factor of `(1 + i)ⁿ`."),
            ("Read off a₁ and r, then use the sum formula",
             "For an accumulation, `a₁ = P` and `r = 1 + i` with the payments listed "
             "backwards. For a present value, `a₁ = P/(1 + i)` and `r = 1/(1 + i)`. "
             "Only a perpetuity needs the `|r| &lt; 1` test, and it passes it for every "
             "positive rate."),
            ("Check the total against nP",
             "At a positive rate an accumulated value is at least `nP` and a present "
             "value is at most `nP`, the gap being the interest. An answer on the wrong side of "
             "`nP` is a discounting factor applied the wrong way up."),
        ],
        "worked": {
            "title": "1000 paid at the end of each year for 5 years, at 10% a year",
            "intro": [
                "The sum is computed twice: once by valuing each payment and adding the "
                "five numbers, once by the closed form. Both are carried through to a "
                "figure in cents.",
            ],
            "lines": [
                "P = 1000    i = 1/10    n = 5    ordinary annuity",
                "",
                "adding the terms",
                "  payment 1   1000(11/10)⁴ = 1000(14641/10000) = 1464.10",
                "  payment 2   1000(11/10)³ = 1000(1331/1000)   = 1331.00",
                "  payment 3   1000(11/10)² = 1000(121/100)     = 1210.00",
                "  payment 4   1000(11/10)                      = 1100.00",
                "  payment 5   1000                             = 1000.00",
                "                                                 --------",
                "  total                                          6105.10",
                "",
                "by the closed form",
                "  S = P[(1 + i)ⁿ - 1]/i",
                "    = 1000[(11/10)⁵ - 1]/(1/10)",
                "    = 1000[161051/100000 - 1]·10",
                "    = 10000·(61051/100000)",
                "    = 61051/10  =  6105.10                      ✓ both agree",
                "",
                "size check   5 payments of 1000 is 5000, and 6105.10 > 5000",
                "             the difference, 1105.10, is the interest earned",
            ],
            "after": [
                "The two computations agree, which checks this one case: `P = 1000`, "
                "`i = 1/10`, `n = 5`. The formula holds for every `P`, every `i ≠ 0` "
                "and every `n` because of the cancellation it was derived from, not "
                "because of this agreement.",
                "The exponent on the first payment is `4`, not `5`. It is deposited at "
                "the end of the first year, so it earns interest for the four years "
                "that remain, and the same `n - 1` that appeared in `a₁rⁿ⁻¹` is here "
                "wearing a calendar. Raising every exponent by one instead gives "
                "`6715.61`, which is the answer to the annuity-due question &mdash; "
                "payments at the start of each year &mdash; and is exactly `11/10` "
                "times this one.",
            ],
        },
        "quiz_title": "Streams of payments",
        "quiz": [
            {"q": "`100` is paid at the end of each year for 3 years into an account "
                  "earning `10%` a year. What is in the account immediately after the "
                  "third payment?",
             "a": ["`300`", "`331`", "`364.10`", "`133.10`"],
             "c": 1,
             "why": "The three payments are worth `121`, `110` and `100` at that "
                    "moment, totalling `331`, and "
                    "`100[(11/10)³ - 1]/(1/10) = 331` agrees. `300` ignores the "
                    "interest. `364.10` is `331·(11/10)`, the annuity-due answer, which "
                    "gives every payment one extra year. `133.10` is `100(11/10)³`, one "
                    "payment compounded for three years instead of three payments."},
            {"q": "A perpetuity pays `600` at the end of every year for ever, and "
                  "the rate is `4%` a year. What is it worth today?",
             "a": ["`24`", "`625`", "`15000`", "`15600`"],
             "c": 2,
             "why": "`r = 1/(1 + 1/25)`, so `|r| &lt; 1` and the value is "
                    "`P/i = 600/(1/25) = 15000`. `24` multiplies by the rate instead of "
                    "dividing by it. `625` divides by `1 - i` rather than by `i`. "
                    "`15600` is `15000(1 + 1/25)`, the value if the first payment "
                    "arrived today rather than in a year."},
            {"q": "The accumulated value of an annuity is a geometric series with "
                  "`r = 1 + i`, which is greater than `1`. Why is that not a violation "
                  "of the `|r| &lt; 1` condition?",
             "a": ["It is a violation, so the formula is only an approximation when `i &gt; 0`.",
                   "`|r| &lt; 1` is needed only for a sum of infinitely many terms; a "
                   "sum of `n` terms needs only `r ≠ 1`.",
                   "The condition applies to the rate `i`, and `i &lt; 1` for any realistic rate.",
                   "Rates are small, so `r` is close enough to `1` for the condition to hold."],
             "c": 1,
             "why": "`Sₙ = a₁(1 - rⁿ)/(1 - r)` was derived by cancellation and needs "
                    "nothing but `r ≠ 1`; `|r| &lt; 1` entered only when `rⁿ` had to be "
                    "driven to zero. The first choice invents an inaccuracy that is not "
                    "there. The third moves the condition onto the wrong quantity. The "
                    "fourth confuses being close to `1` with being less than `1` in "
                    "size, and `1.04` fails the condition as thoroughly as `2` does."},
        ],
        "mistakes": [
            ("Giving the last payment a period of interest",
             "In an ordinary annuity the final payment arrives at the moment of "
             "valuation and is multiplied by `(1 + i)⁰ = 1`. Compounding every payment "
             "one period too long multiplies the whole answer by `(1 + i)`, turning "
             "`6105.10` into `6715.61`. That figure is not nonsense &mdash; it is the "
             "answer to the annuity-due question &mdash; which is why it survives a "
             "casual glance."),
            ("Using an annual rate with a monthly count",
             "`300` monthly payments of `100` at `i = 1/200` accumulate to about "
             "`69299`. Substituting the annual `6%` as `i` while leaving `n` at `300` "
             "months returns a number near `65` billion. The error is not subtle once "
             "it is computed, and it is invisible until then: the rate and the period "
             "count have to be in the same units before anything is substituted."),
            ("Rounding each term to the cent on the way through",
             "Each of `360` terms rounded to the cent can be half a cent out, and "
             "`360` half-cents is `1.80`. That is enough for two people doing the "
             "same calculation to disagree about the answer. Keep the fractions, and "
             "round the single figure at the end."),
        ],
        "standard": ("Finish when you can say, before computing, which end of the timeline the question is asking about.",
                     "You should be able to derive `P[(1 + i)ⁿ - 1]/i` from "
                     "`a₁ = P, r = 1 + i` without looking it up, produce a present value "
                     "from the same series read the other way, and explain why a "
                     "perpetuity has a finite value while an annuity with `r &gt; 1` "
                     "still has a perfectly good finite sum over `n` periods."),
        "note": "That is the last of the sums. The remaining lessons follow a different "
                "pattern &mdash; the numbers that appear when a single bracket is raised "
                "to a power &mdash; and the link back is that those numbers, like the "
                "terms of a series, count something definite. The next lesson builds the "
                "table of them by addition alone, before any formula for computing one "
                "directly is given.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "pascals-triangle",
        "title": "Pascal's Triangle",
        "module": "The binomial theorem",
        "one_line": "Each entry the sum of the two above it, and what that counts.",
        "summary": (
            "Start with a single `1` and make every entry the sum of the two above it. "
            "The rows that come out are the coefficients of `(a + b)ⁿ`, and each entry "
            "counts something exact: the number of ways to choose `k` things from `n`. "
            "This lesson builds the triangle and establishes what its entries count; "
            "the formula for computing one without building the rows above it comes "
            "next."
        ),
        "key": [
            "row 4      1   4   6   4   1      each entry the sum of the two above",
            "C(n,k)     entry k of row n, both counted from 0",
            "C(n,k)  =  C(n-1,k-1) + C(n-1,k)  the building rule, in symbols",
            "row n adds up to 2ⁿ               1 + 4 + 6 + 4 + 1 = 16",
        ],
        "key_label": "The rule, the notation, and the check",
        "concepts_intro": (
            "One construction, one counting interpretation, and one indexing "
            "convention that is where most of the errors start."
        ),
        "concepts": [
            ("Rows and positions are both counted from 0",
             "The apex is row `0`, and the leftmost entry of any row is position `0`. "
             "So row `n` has `n + 1` entries, and the third number in row 6 is "
             "`C(6,2) = 15` rather than `C(6,3)`. The convention is arbitrary, but it "
             "is universal and it matches the exponents in `(a + b)ⁿ`."),
            ("The building rule is a statement about choosing",
             "An entry counts the ways of choosing `k` objects out of `n`. Single out "
             "one object: either it is chosen, and the remaining `k - 1` come from the "
             "other `n - 1`, or it is not, and all `k` do. Those two cases are separate "
             "and cover everything, so the counts add &mdash; which is the "
             "sum-of-the-two-above rule."),
            ("The triangle is symmetric, and that halves the work",
             "`C(n,k) = C(n,n-k)`, because naming the `k` objects to take is the same "
             "act as naming the `n - k` to leave. Row 8 is written once you know "
             "`1, 8, 28, 56, 70`: the rest is `56, 28, 8, 1`, the first four of those "
             "read backwards, with the central `70` written once."),
        ],
        "read_title": "Building the triangle, and what its entries count",
        "read_intro": "The construction rule, the counting problem the entries "
                      "answer, and the patterns worth trusting.",
        "body": [
            ("def", ("Pascal's triangle",
                     "The array of numbers whose row `0` is a single `1`, in which "
                     "every row begins and ends with `1`, and in which every other "
                     "entry is the sum of the two entries immediately above it. Rows "
                     "are numbered from `0` downwards and positions within a row from "
                     "`0` from the left.",
                     "The name is a historical accident: the array appears in Chinese, "
                     "Indian and Persian mathematics centuries before Pascal, who "
                     "wrote a treatise on it in the 1650s.")),
            ("math", [
                "row 0                    1",
                "row 1                  1   1",
                "row 2                1   2   1",
                "row 3              1   3   3   1",
                "row 4            1   4   6   4   1",
                "row 5          1   5  10  10   5   1",
                "",
                "each 10 in row 5 is the sum of the 4 and the 6 above it",
                "the 1s down each edge have only one entry above them, so",
                "nothing is added to them",
            ]),
            ("p", "Write `C(n,k)` for the entry in row `n` at position `k`. In this "
                  "lesson that is all the symbol means &mdash; a name for a number read "
                  "off the array &mdash; and the building rule is "
                  "`C(n,k) = C(n-1,k-1) + C(n-1,k)` for `0 &lt; k &lt; n`, with "
                  "`C(n,0) = C(n,n) = 1`. The next lesson gives a formula in factorials "
                  "that produces `C(n,k)` directly, without the rows above it."),
            ("h3", "What the entries count"),
            ("p", "Here is a question with nothing to do with triangles. A group of "
                  "three people, `A`, `B` and `C`, must send a delegation. How many "
                  "different delegations are there of each size?"),
            ("math", [
                "size 0    { }                                     1 way",
                "size 1    {A}       {B}       {C}                 3 ways",
                "size 2    {A,B}     {A,C}     {B,C}               3 ways",
                "size 3    {A,B,C}                                 1 way",
                "                                       total      8 = 2³",
                "",
                "1, 3, 3, 1  is row 3 of the triangle",
            ]),
            ("thm", ("The entries are counts",
                     "The number of ways to choose `k` objects from a set of `n` "
                     "distinct objects is `C(n,k)`, the entry in row `n` at position "
                     "`k`.")),
            ("proof", [
                "Let `N(n,k)` be the number of ways to choose `k` from `n`. There is "
                "one way to choose none and one way to choose all, so "
                "`N(n,0) = N(n,n) = 1`, matching the edges of the triangle.",
                "Now fix one particular object. The selections that include it are "
                "completed by choosing `k - 1` from the other `n - 1`, and there are "
                "`N(n-1,k-1)` of those. The selections that exclude it are choices of "
                "`k` from the other `n - 1`, and there are `N(n-1,k)`. No selection is "
                "in both groups and none is outside them, so "
                "`N(n,k) = N(n-1,k-1) + N(n-1,k)`.",
                "So `N` starts as the triangle does and grows by the same rule, which "
                "forces the two tables to agree row by row. Stating that last step "
                "properly is what mathematical induction is for, and the Discrete "
                "Mathematics path does it; the two rules and the two starting rows are "
                "what this course checks.",
            ]),
            ("p", "There is a second count in the same picture. Start at the apex and "
                  "walk down, going left or right at each step. The number of routes "
                  "that reach a given entry is that entry, because every route arrives "
                  "from one of the two entries above it. A route of `n` steps that "
                  "lands at position `k` went right `k` times, so the routes are "
                  "another way of choosing which `k` of the `n` steps go right."),
            ("h3", "Patterns in the array"),
            ("p", "Row `n` adds up to `2ⁿ`. The reason is the delegation table above: "
                  "sorting all the subsets of an `n`-element set by size counts each "
                  "subset exactly once, and a set of `n` things has `2ⁿ` subsets, one "
                  "for each way of saying yes or no to each thing. Row 6 gives "
                  "`1 + 6 + 15 + 20 + 15 + 6 + 1 = 64`, and `2⁶ = 64`."),
            ("p", "With alternating signs the same rows give `0`, for every `n ≥ 1`. "
                  "Row 4 gives `1 - 4 + 6 - 4 + 1 = 0` and row 7 gives "
                  "`1 - 7 + 21 - 35 + 35 - 21 + 7 - 1 = 0`. For odd `n` the symmetry "
                  "pairs each entry with an equal one of the opposite sign, which "
                  "settles that case; for even `n` the cancellation is real but the "
                  "clean reason for it is the binomial theorem with `a = 1` and "
                  "`b = -1`, which is the next lesson."),
            ("math", [
                "reading down the diagonals",
                "",
                "k = 0     1   1   1   1   1   1   1",
                "k = 1     1   2   3   4   5   6         the counting numbers",
                "k = 2     1   3   6  10  15  21         the triangular numbers",
                "k = 3     1   4  10  20  35             not 1, 4, 9, 16",
            ]),
            ("example", ("Adding down a diagonal",
                         "`1 + 3 + 6 + 10 + 15 = 35`, and `35` is `C(7,3)`, one row "
                         "below and one place to the right of the `15`. It follows from "
                         "applying the building rule over and over: "
                         "`C(7,3) = C(6,2) + C(6,3)`, then `C(6,3) = C(5,2) + C(5,3)`, "
                         "and so on until the last piece is `C(3,3) = 1`. Splitting "
                         "`35` as `15 + 10 + 6 + 3 + 1` is that chain written out.")),
            ("example", ("The rows are the powers of 11",
                         "`11⁰ = 1`, `11¹ = 11`, `11² = 121`, `11³ = 1331`, "
                         "`11⁴ = 14641`. Row 5 is `1, 5, 10, 10, 5, 1`, and carrying the "
                         "two-digit entries turns that into `161051`, which is `11⁵`. "
                         "The pattern does not break at row 5; the digit-by-digit "
                         "reading of it does. `11ⁿ` is `(10 + 1)ⁿ`, so the row is the "
                         "list of coefficients of the powers of ten, and coefficients "
                         "above `9` have to be carried like any other column of "
                         "addition.")),
            ("p", "The entries grow quickly: `C(20,10) = 184756`, and reaching it by "
                  "addition means building twenty rows, one hundred and ninety "
                  "additions. That is the argument for a formula, and it is what the next "
                  "lesson supplies."),
        ],
        "lab": ("sequence", {
            "mode": "pascal",
            "panel_title": "Rows, and what they add to",
            "panel_intro": "The lab builds the triangle one row at a time from the "
                           "addition rule, and prints beside each row both the total of "
                           "its entries added up and the value of `2ⁿ`, so the two can "
                           "be compared. Build it to row 10, highlight the entry `k = 3` "
                           "in that row, and read off the number of ways to choose "
                           "three people out of ten.",
        }),
        "steps_title": "Getting an entry out of the triangle",
        "steps_intro": "Four steps, and the last one costs one line of addition "
                       "and is worth doing every time.",
        "steps": [
            ("Number the rows and positions from 0",
             "Write the index above each entry before reading anything off. For "
             "`C(8,3)` you want row 8, and the fourth number along it, because position "
             "`3` follows positions `0, 1, 2`."),
            ("Build down from a row you are sure of",
             "Each new row starts and ends with `1`; every entry between them is the "
             "sum of the pair above. Take the row you trust, not the row you half "
             "remember."),
            ("Use the symmetry once you are past the middle",
             "`C(n,k) = C(n,n-k)`, so the second half of a row is the first half "
             "reversed. In an odd-numbered row the two central entries are equal; in an "
             "even-numbered row there is a single central entry."),
            ("Check the row against 2ⁿ",
             "Add the entries. A row that does not total `2ⁿ` contains an error. A row "
             "that does may still contain two errors that cancel, so the symmetry is "
             "worth a second look."),
        ],
        "worked": {
            "title": "Rows 6, 7 and 8, and the number of ways to choose 3 people from 8",
            "intro": [
                "Three rows built by addition from row 5, each checked by adding it up "
                "and comparing with the power of two it should be.",
            ],
            "lines": [
                "row 5      1    5   10   10    5    1            (starting point)",
                "",
                "row 6      1    6   15   20   15    6    1",
                "             1+5  5+10 10+10 10+5  5+1",
                "",
                "row 7      1    7   21   35   35   21    7    1",
                "             1+6  6+15 15+20 20+15 15+6  6+1",
                "",
                "row 8      1    8   28   56   70   56   28    8    1",
                "             1+7  7+21 21+35 35+35 35+21 21+7  7+1",
                "",
                "check each row by adding it",
                "  row 6   1+6+15+20+15+6+1              =  64  = 2⁶      ✓",
                "  row 7   1+7+21+35+35+21+7+1           = 128  = 2⁷      ✓",
                "  row 8   1+8+28+56+70+56+28+8+1        = 256  = 2⁸      ✓",
                "",
                "C(8,3)  is entry 3 of row 8, counting 1, 8, 28, 56 from position 0",
                "        = 56 ways to choose 3 people from 8",
                "",
                "symmetry   C(8,5) = 56 as well: choosing which 3 to send is the",
                "           same act as choosing which 5 to leave behind",
            ],
            "after": [
                "Each row was produced one way and checked another, which is what the "
                "`2ⁿ` line is for. It establishes that the entries of that row total "
                "the right amount; it does not establish that every entry is right, "
                "since two compensating errors would pass. Reading the row backwards "
                "and finding the same numbers is a second, independent check.",
                "`56` answers a question about people with no obvious triangle in it. "
                "The connection is the argument above: the delegations of size `3` from "
                "`8` either include a particular person or do not, which is the same "
                "split that built the row.",
            ],
        },
        "quiz_title": "Rows, entries and counts",
        "quiz": [
            {"q": "Row 6 of Pascal's triangle is `1, 6, 15, 20, 15, 6, 1`. What is "
                  "the entry of row 7 that sits directly below the `15` and the `20`?",
             "a": ["`21`", "`30`", "`35`", "`56`"],
             "c": 2,
             "why": "It is `15 + 20 = 35`. `21` is `6 + 15`, the entry one place to its "
                    "left in the same row. `30` doubles the `15` instead of adding its "
                    "right-hand neighbour. `56` is in row 8, one row too far down."},
            {"q": "What do the entries of row 8 add up to?",
             "a": ["`128`", "`255`", "`256`", "`512`"],
             "c": 2,
             "why": "Row `n` totals `2ⁿ`, and row 8 is "
                    "`1 + 8 + 28 + 56 + 70 + 56 + 28 + 8 + 1 = 256`. `128` is `2⁷`, the "
                    "row above. `512` is `2⁹`, from using the nine entries of the row as "
                    "the exponent instead of the row number. `255` is the total with one "
                    "of the two end `1`s left out."},
            {"q": "A club of 7 members must send 3 of them to a meeting. How many "
                  "different groups of 3 are possible?",
             "a": ["`21`", "`35`", "`210`", "`343`"],
             "c": 1,
             "why": "It is `C(7,3)`, entry 3 of row 7 `1, 7, 21, 35, …` , so `35`. `21` "
                    "is entry 2, the number of groups of two. `210` is `7·6·5`, which "
                    "counts each group once for every order it could be picked in, and "
                    "`210/6 = 35`. `343` is `7³`, which would count three picks made "
                    "independently, allowing the same member twice."},
        ],
        "mistakes": [
            ("Counting rows or positions from 1",
             "Row 4 is the fifth row written down, and `C(6,2) = 15` is the third "
             "number in its row. Every off-by-one in this lesson is this convention "
             "being applied on one side of a calculation and not the other. Writing the "
             "position numbers above the entries removes it."),
            ("Adding the wrong pair, or treating the edges as a special rule",
             "An interior entry uses the two entries immediately above, not the two "
             "nearest numbers on the page. The edge `1`s are not an exception bolted "
             "on: there is only one entry above them, and the missing neighbour counts "
             "as `0`."),
            ("Assuming a diagonal continues the way it started",
             "The `k = 3` diagonal begins `1, 4, 10` and the next entry is `20`, not "
             "`16`; it is not the squares, though its first two terms match them. This "
             "is the same warning as the chord-and-regions sequence at the start of the "
             "course: the building rule decides what comes next, and a guessed pattern "
             "does not."),
        ],
        "standard": ("Finish when you can extend the triangle five rows and check each one as you go.",
                     "You should be able to produce row 8 from row 5 without error, "
                     "read `C(8,3)` off it with the positions counted correctly, and "
                     "say why the entry is the answer to a question about choosing "
                     "delegations. The `2ⁿ` check should be automatic."),
        "note": "So far the triangle is a table with a counting interpretation. The next "
                "lesson connects it to algebra: expanding `(a + b)ⁿ` means choosing an "
                "`a` or a `b` from each of `n` brackets, which is the same choosing "
                "problem, so row `n` turns out to be the list of coefficients. Having "
                "the rows already in hand is what makes that lesson short.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "the-binomial-theorem",
        "title": "The Binomial Theorem",
        "module": "Sequences",
        "one_line": "Expanding (a+b)^n without multiplying it out.",
        "summary": (
            "Multiplying out `(a + b)ⁿ` means expanding `2ⁿ` products and collecting "
            "them. The binomial theorem writes the answer down directly: the "
            "coefficients are the binomial coefficients `C(n, k)`, and they are there "
            "because expanding brackets is a counting problem."
        ),
        "key": [
            "(a + b)ⁿ  =  Σ C(n,k) aⁿ⁻ᵏ bᵏ        k from 0 to n",
            "C(n,k) = n!/(k!(n - k)!)             row n of Pascal's triangle",
            "the term with bᵏ is C(n,k) aⁿ⁻ᵏ bᵏ   exponents always total n",
            "1  4  6  4  1   →   (a+b)⁴ = a⁴ + 4a³b + 6a²b² + 4ab³ + b⁴",
        ],
        "key_label": "The expansion, and where its numbers come from",
        "concepts_intro": (
            "The formula is short and the reason behind it is shorter: every "
            "coefficient is a count of something."
        ),
        "concepts": [
            ("The coefficients count, they are not a pattern",
             "`(a + b)ⁿ` is `n` brackets multiplied together. Expanding means choosing "
             "`a` or `b` from each bracket in every possible way; a product with "
             "exactly `k` factors of `b` comes from choosing which `k` brackets "
             "supplied it, and there are `C(n, k)` ways to do that. Pascal's triangle "
             "appears here because it is a table of those counts."),
            ("Exponents sum to `n` in every term",
             "The term is `aⁿ⁻ᵏbᵏ`, and `(n - k) + k = n`. It is a free check on every "
             "line you write: `a³b³` cannot appear in the expansion of `(a + b)⁵`. "
             "There are `n + 1` terms, one for each `k` from `0` to `n`."),
            ("The signs in `(a - b)ⁿ` are not a separate rule",
             "`(a - b)ⁿ` is `(a + (-b))ⁿ`, so the term is `C(n,k)aⁿ⁻ᵏ(-b)ᵏ` and the "
             "sign is `(-1)ᵏ`. The signs alternate starting from `+`, and the terms "
             "with an even power of `b` keep their sign."),
        ],
        "read_title": "Pascal's triangle and the binomial theorem",
        "read_intro": "The coefficients, the formula that produces them, and the reason they are counts.",
        "body": [
            ("p", "Course 4 expanded `(a + b)²` and `(a + b)³` by hand. `(a + b)⁵` is "
                  "possible with patience, and `(a + b)¹²` is not: multiplying out "
                  "twelve brackets means `2¹² = 4096` products before any collecting "
                  "starts. The theorem below skips all of it."),
            ("math", [
                "(a + b)⁰ = 1",
                "(a + b)¹ = a + b",
                "(a + b)² = a² + 2ab + b²",
                "(a + b)³ = a³ + 3a²b + 3ab² + b³",
                "(a + b)⁴ = a⁴ + 4a³b + 6a²b² + 4ab³ + b⁴",
                "",
                "in every line the power of a falls and the power of b rises,",
                "and the two always total the exponent on the left",
            ]),
            ("p", "Stripping out the coefficients leaves a triangle in which every "
                  "entry is the sum of the two directly above it, with `1`s down both "
                  "edges. It is called Pascal's triangle, and row `n` holds the "
                  "coefficients of `(a + b)ⁿ`."),
            ("math", [
                "n = 0                    1",
                "n = 1                  1   1",
                "n = 2                1   2   1",
                "n = 3              1   3   3   1",
                "n = 4            1   4   6   4   1",
                "n = 5          1   5  10  10   5   1",
                "n = 6        1   6  15  20  15   6   1",
                "",
                "15 = 5 + 10:  each entry is the sum of the two above it",
            ]),
            ("def", ("Binomial coefficient",
                     "For integers `0 ≤ k ≤ n`, `C(n, k) = n!/(k!(n - k)!)`, read \"`n` "
                     "choose `k`\". It is also written with `n` above `k` in a single "
                     "pair of brackets. The factorials are the ones from lesson 1, "
                     "with `0! = 1`.")),
            ("example", ("Computing C(9, 4) without computing 9!",
                         "`C(9,4) = 9!/(4!5!)`. The `5!` cancels most of the `9!`, "
                         "leaving `(9·8·7·6)/(4·3·2·1) = 3024/24 = 126`. Four factors "
                         "on top because `k = 4`, and four below. The cancelling is not "
                         "a shortcut for the lazy: `9!` is `362880`, and there is no "
                         "reason to write it down.")),
            ("thm", ("The binomial theorem",
                     "For any numbers `a`, `b` and any positive integer `n`, "
                     "`(a + b)ⁿ = Σ C(n,k) aⁿ⁻ᵏ bᵏ`, the sum running over `k` from `0` "
                     "to `n`. Written out, that is "
                     "`aⁿ + C(n,1)aⁿ⁻¹b + C(n,2)aⁿ⁻²b² + … + C(n,n-1)abⁿ⁻¹ + bⁿ`.")),
            ("p", "Why the coefficient of `aⁿ⁻ᵏbᵏ` is `C(n,k)`: expanding `n` brackets "
                  "means taking one letter from each and multiplying, then adding every "
                  "such product. A product ends up as `aⁿ⁻ᵏbᵏ` exactly when the `b` was "
                  "taken from `k` of the brackets, and the number of ways to choose "
                  "which `k` is `C(n,k)`. Every one of those choices contributes `1`, "
                  "so they add to `C(n,k)`."),
            ("p", "That is also why the triangle's rule works: a choice of `k` brackets "
                  "out of `n` either uses the last bracket, leaving `k - 1` to choose "
                  "from the first `n - 1`, or does not, leaving `k` to choose from "
                  "`n - 1`. So `C(n,k) = C(n-1,k-1) + C(n-1,k)`, which is the "
                  "sum-of-the-two-above rule stated in symbols. The triangle is also "
                  "symmetric, because `C(n,k) = C(n,n-k)`: choosing `k` brackets to "
                  "give `b` is the same act as choosing the other `n - k` to give `a`."),
            ("p", "The theorem also gives one term on its own, which is where it earns "
                  "its keep. The term containing `x⁵` in `(x + 2)⁸` has `a = x`, so "
                  "`8 - k = 5` and `k = 3`, making it `C(8,3)x⁵2³ = 56·8·x⁵ = 448x⁵`. "
                  "No other term of that expansion had to be computed."),
            ("example", ("The signs of (a - b)⁴",
                         "`(a - b)⁴ = a⁴ - 4a³b + 6a²b² - 4ab³ + b⁴`. The coefficients "
                         "are row 4 unchanged; the signs come from `(-b)ᵏ`, so terms "
                         "with odd `k` are negative. The last term is `(-b)⁴ = +b⁴`, "
                         "which is the one people expect to be negative.")),
            ("p", "Setting `a = b = 1` turns the theorem into "
                  "`2ⁿ = C(n,0) + C(n,1) + … + C(n,n)`: each row of Pascal's triangle "
                  "adds up to a power of two. Row 5 is `1, 5, 10, 10, 5, 1`, totalling "
                  "`32`. It is a check on a row you have just written, and it is also "
                  "the statement that a set of `n` things has `2ⁿ` subsets."),
        ],
        "lab": ("sequence", {
            "mode": "binomial",
            "panel_title": "One row at a time",
            "panel_intro": "Build Pascal's triangle row by row and expand any "
                           "`(a + b)ⁿ` beside it. Ask the lab for a single term of a "
                           "large expansion and check it against `C(n,k)` computed by "
                           "hand.",
        }),
        "steps_title": "Expanding a binomial power",
        "steps_intro": "Four steps. The third is the one that decides whether the signs come out right.",
        "steps": [
            ("Name a, b and n",
             "In `(2x - 3)⁴`: `a = 2x`, `b = -3`, `n = 4`. The minus sign belongs to "
             "`b`, not to the expansion. Deciding this on paper before expanding is "
             "what keeps the signs honest."),
            ("Write the coefficients",
             "Row `n` of Pascal's triangle if `n` is small, `C(n,k)` otherwise. For "
             "`n = 4` they are `1, 4, 6, 4, 1`, and the row is symmetric, which halves "
             "the work."),
            ("Write the powers before simplifying",
             "`aⁿ⁻ᵏbᵏ` for `k = 0, 1, …, n`, exponents totalling `n` in every term. "
             "Getting the skeleton down first stops a dropped term in the middle of a "
             "long expansion."),
            ("Apply each exponent to the whole of a and b",
             "`(2x)³` is `8x³`, not `2x³`, and `(-3)²` is `9`, not `-9`. Then collect. "
             "Finally substitute `x = 1`: the expansion should equal the original "
             "expression evaluated there."),
        ],
        "worked": {
            "title": "Expanding (2x - 3)⁴",
            "intro": [
                "Both parts are compound: `a` carries a coefficient and `b` carries a "
                "sign. Every error in this expansion is one of those two being applied "
                "to only part of the term."
            ],
            "lines": [
                "a = 2x,   b = -3,   n = 4",
                "row 4 of Pascal's triangle:   1   4   6   4   1",
                "",
                "k=0   1·(2x)⁴        = 1·16x⁴         =   16x⁴",
                "k=1   4·(2x)³(-3)    = 4·8x³·(-3)     =  -96x³",
                "k=2   6·(2x)²(-3)²   = 6·4x²·9        =  216x²",
                "k=3   4·(2x)(-3)³    = 4·2x·(-27)     = -216x",
                "k=4   1·(-3)⁴        = 1·81           =   81",
                "",
                "(2x - 3)⁴ = 16x⁴ - 96x³ + 216x² - 216x + 81",
                "",
                "check at x = 1",
                "  left   (2 - 3)⁴ = (-1)⁴ = 1",
                "  right  16 - 96 + 216 - 216 + 81 = 1              ✓",
            ],
            "after": [
                "The check costs one line and catches almost everything, because "
                "substituting `x = 1` turns the expansion into the sum of its "
                "coefficients. A dropped sign, a missing term or a mishandled `(2x)³` "
                "will all show up in it.",
                "Notice that the coefficients `16, -96, 216, -216, 81` are not "
                "symmetric even though row 4 is. The symmetry belongs to `C(n,k)`; "
                "`(2x)` and `(-3)` are different sizes, and the powers of each pull the "
                "numbers out of balance.",
            ],
        },
        "quiz_title": "Coefficients and terms",
        "quiz": [
            {"q": "What is the coefficient of `x³` in the expansion of `(x + 2)⁵`?",
             "a": ["`10`", "`32`", "`40`", "`80`"],
             "c": 2,
             "why": "`a = x`, so `x³` needs `5 - k = 3`, giving `k = 2`, and the "
                    "coefficient is `C(5,2)·2² = 10·4 = 40`. `10` is `C(5,2)` with the "
                    "`2²` forgotten; `80` uses `k = 3`, which is the term in `x²`."},
            {"q": "How many terms does the expansion of `(a + b)¹²` have, after collecting?",
             "a": ["`12`", "`13`", "`14`", "`24`"],
             "c": 1,
             "why": "One term for each `k` from `0` to `12`, which is `13` values. The "
                    "count is `n + 1`, and `12` is the answer you get by counting the "
                    "exponent instead of the terms."},
            {"q": "In the expansion of `(a + b)⁹`, which term contains `b⁴`?",
             "a": ["`36a⁵b⁴`", "`84a⁵b⁴`", "`126a⁵b⁴`", "`126a⁴b⁵`"],
             "c": 2,
             "why": "`k = 4`, so the coefficient is `C(9,4) = 126` and the power of `a` "
                    "is `9 - 4 = 5`. `84` is `C(9,3)` and `36` is `C(9,2)`, the "
                    "off-by-one and off-by-two; the last choice has the right "
                    "coefficient with the exponents swapped."},
        ],
        "mistakes": [
            ("Raising only part of a term to the power",
             "In `(2x - 3)⁴` the `k = 1` term is `4(2x)³(-3)`, and `(2x)³ = 8x³`. "
             "Writing `2x³` loses a factor of `4` in that term alone, so the expansion "
             "fails the `x = 1` check while every other term is correct."),
            ("Alternating the signs by habit instead of from `(-b)ᵏ`",
             "The rule is `(-1)ᵏ`, so the first term is positive and the last term of "
             "`(a - b)⁴` is `+b⁴`. Expansions of odd powers end negative and even "
             "powers end positive, and guessing rather than computing `(-b)ᵏ` gets one "
             "of those two cases wrong."),
            ("Confusing \"the k-th term\" with \"the term containing bᵏ\"",
             "The term containing `bᵏ` is the `(k + 1)`-th, because `k` starts at `0` "
             "while the counting of terms starts at `1`. Say which of the two you mean, "
             "and prefer to describe a term by the power it contains."),
        ],
        "standard": ("Finish when you can write one term of a large expansion without writing the rest.",
                     "You should be able to produce row 6 of Pascal's triangle from "
                     "row 5, expand `(2x - 3)⁴` correctly including signs, and pick out "
                     "the term in `x⁵` of `(x + 2)⁸` in a single line. The `x = 1` check "
                     "should be automatic."),
        "note": "This is the last new idea of the course &mdash; lesson 11 turns it "
                "into a way of picking a single term out of an expansion &mdash; and "
                "it ends where counting begins: `C(n,k)` was defined here as a formula and used "
                "as a count, and the Combinatorics and Counting course on the Discrete "
                "Mathematics path takes it up as a subject in its own right. The "
                "algebra was the point, though. Every step of this path &mdash; "
                "elimination, row reduction, the determinant and the corner points in "
                "course 8, the two sequence families here &mdash; was legal because "
                "some property of the real numbers said so, which is the thing "
                "course 1 opened with.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "the-general-term-of-an-expansion",
        "title": "The General Term of an Expansion",
        "module": "The binomial theorem",
        "one_line": "Picking one term out of an expansion without writing the rest.",
        "summary": (
            "Most questions about an expansion want one term of it: the term in `x⁵`, "
            "the constant term, the middle term. The general term `C(n,k)aⁿ⁻ᵏbᵏ` "
            "answers them by solving one small equation for `k`. When that equation has "
            "no whole-number solution in range, the honest answer is that the term does "
            "not exist."
        ),
        "key": [
            "general term    C(n,k) aⁿ⁻ᵏ bᵏ        for k = 0, 1, …, n",
            "it is term number k + 1               k counts from 0, terms from 1",
            "to find one term: collect the power of x and solve for k",
            "k must be a whole number in 0…n, or there is no such term",
        ],
        "key_label": "One term, found by solving for k",
        "concepts_intro": (
            "One expression and one equation. The difficulty is entirely in the "
            "bookkeeping, and the bookkeeping has three places to go wrong."
        ),
        "concepts": [
            ("k is the number of bs, and it fixes everything else",
             "Choose `k` and the term is settled: the coefficient is `C(n,k)`, the "
             "power of `a` is `n - k`, the power of `b` is `k`, and if `b` is negative "
             "the sign is `(-1)ᵏ`. Every question in this lesson is the question of "
             "which `k` is wanted."),
            ("Finding a term means solving an equation",
             "When `a` and `b` carry powers of `x`, both contribute to the power of `x` "
             "in the term. In `(2x² - 3/x)⁹` the `a` part contributes `2(9 - k)` and "
             "the `b` part contributes `-k`, so the term holds `x¹⁸⁻³ᵏ`. Asking for a "
             "particular power of `x` is asking for the `k` that makes `18 - 3k` equal "
             "to it."),
            ("A k outside 0…n or not a whole number means no such term",
             "The equation is exact and `k` counts brackets, so `k = 16/3` is not a "
             "near miss to be rounded. It says the expansion contains no such term at "
             "all, which is a complete answer to the question that was asked."),
        ],
        "read_title": "One term, without the others",
        "read_intro": "The general term, the exponent equation it leads to, and the "
                      "cases where the term asked for is not there.",
        "body": [
            ("def", ("General term of a binomial expansion",
                     "In the expansion of `(a + b)ⁿ`, the <strong>general term</strong> "
                     "is `C(n,k)aⁿ⁻ᵏbᵏ`, where `k` runs from `0` to `n`. Written in "
                     "descending powers of `a`, it is the `(k + 1)`-th term of the "
                     "expansion.")),
            ("p", "The `k + 1` is not decoration. `k` is a count of `b`s and starts at "
                  "`0`; the terms of a written-out expansion are counted from `1`. Some "
                  "books index the general term by the term number instead, putting "
                  "`r - 1` everywhere this course puts `k`. Both conventions are in "
                  "use, and the safest habit is to describe a term by the power it "
                  "contains rather than by its position."),
            ("h3", "When a and b carry powers of x"),
            ("p", "If `a` and `b` are more than single letters, each contributes to the "
                  "power of `x` in the term, and the two contributions have to be "
                  "collected before anything can be solved. Take `(x + 2/x)⁶`, small "
                  "enough to expand completely and check."),
            ("math", [
                "general term   C(6,k) x⁶⁻ᵏ (2/x)ᵏ  =  C(6,k)·2ᵏ·x⁶⁻ᵏ·x⁻ᵏ",
                "                                   =  C(6,k)·2ᵏ·x⁶⁻²ᵏ",
                "",
                "k     C(6,k)   2ᵏ    coefficient    power of x",
                "0        1      1          1            6",
                "1        6      2         12            4",
                "2       15      4         60            2",
                "3       20      8        160            0",
                "4       15     16        240           -2",
                "5        6     32        192           -4",
                "6        1     64         64           -6",
                "",
                "sum of the coefficients   1+12+60+160+240+192+64 = 729 = 3⁶",
                "and at x = 1 the bracket is (1 + 2)⁶ = 729           ✓",
            ]),
            ("example", ("The constant term of (x + 2/x)⁶",
                         "The power of `x` is `6 - 2k`, which is `0` when `k = 3`. The "
                         "term is `C(6,3)·2³ = 20·8 = 160`, and the table above shows "
                         "the same `160` in the row for `k = 3`. Six of the seven terms "
                         "never had to be computed to answer the question.")),
            ("p", "The equation to solve is always the same shape. Collect the power of "
                  "`x` in the general term, set it equal to the power wanted, and "
                  "solve. The exponent is linear in `k`, and unless `a` and `b` carry "
                  "the same power of `x` &mdash; in which case every term carries it "
                  "too, and there is nothing to solve &mdash; there is exactly one "
                  "candidate. It then has to survive two tests: it must be a whole "
                  "number, and it must lie between `0` and `n`."),
            ("example", ("An expansion with no constant term",
                         "In `(x² + 1/x)⁸` the general term is "
                         "`C(8,k)x¹⁶⁻²ᵏx⁻ᵏ = C(8,k)x¹⁶⁻³ᵏ`. Setting `16 - 3k = 0` gives "
                         "`k = 16/3`, which is not a whole number. The powers of `x` in "
                         "the nine terms run `16, 13, 10, 7, 4, 1, -2, -5, -8`, "
                         "stepping over `0` between the sixth and seventh terms. The "
                         "expansion has no constant term, and that is the answer.")),
            ("h3", "Middle terms"),
            ("p", "An expansion of `(a + b)ⁿ` has `n + 1` terms. If `n` is even there "
                  "is a single middle term, at `k = n/2`. If `n` is odd there are two, "
                  "at `k = (n - 1)/2` and `k = (n + 1)/2`, and their binomial "
                  "coefficients are equal by the symmetry of the triangle &mdash; but "
                  "the terms themselves need not be, once `a` and `b` carry numbers."),
            ("example", ("The two middle terms of (2x - 1)⁷",
                         "`n = 7`, so the middle terms are `k = 3` and `k = 4`, and "
                         "`C(7,3) = C(7,4) = 35`. At `k = 3`: "
                         "`35(2x)⁴(-1)³ = 35·16·(-1)x⁴ = -560x⁴`. At `k = 4`: "
                         "`35(2x)³(-1)⁴ = 35·8x³ = 280x³`. Equal binomial "
                         "coefficients, and terms differing in size and in sign: the "
                         "symmetry belongs to `C(n,k)`, and `(2x)⁴` against `(2x)³`, "
                         "`(-1)³` against `(-1)⁴`, breaks it.")),
            ("p", "Signs come from `b` and nowhere else. Writing `b = -3` rather than "
                  "carrying a minus sign outside means the factor `(-3)ᵏ` handles the "
                  "alternation with no separate rule to remember, and an even `k` "
                  "returns a positive contribution however negative `b` is."),
            ("p", "One caution about checking. Substituting `x = 1` turns the whole "
                  "expansion into the sum of its coefficients, and comparing that with "
                  "the bracket evaluated at `x = 1` is a strong check on a complete "
                  "expansion. It says nothing about a single term computed on its own: "
                  "if you have written down one term out of ten, there is nothing for "
                  "the substitution to check against. What checks a single term is "
                  "recomputing its exponent from the two factors separately."),
        ],
        "lab": ("sequence", {
            "mode": "genterm",
            "panel_title": "One term, both ways",
            "panel_intro": "Put the two parts of the bracket in the `a` and `b` boxes "
                           "and set the exponent; solve the exponent equation for `k` "
                           "yourself and set that too, and the lab builds the one term "
                           "from `C(n,k)aⁿ⁻ᵏbᵏ` and then expands the whole bracket to "
                           "show where the term sits in it. Set `k` past the exponent "
                           "and read what it reports about a term that is not there.",
        }),
        "steps_title": "Finding the term you were asked for",
        "steps_intro": "Four steps. The third can end the question with the answer that no such term exists.",
        "steps": [
            ("Name a, b and n, signs included",
             "In `(2x² - 3/x)⁹`: `a = 2x²`, `b = -3/x`, `n = 9`. The minus belongs to "
             "`b`. Writing this line down before anything else is what keeps the sign "
             "out of the coefficient."),
            ("Write the general term and collect the power of x",
             "`C(n,k)aⁿ⁻ᵏbᵏ`, then take the numbers and the powers of `x` apart. Both "
             "`a` and `b` contribute to the exponent, and the total is a linear "
             "expression in `k`."),
            ("Set that exponent equal to the power wanted and solve for k",
             "Then check the solution twice: it must be a whole number, and it must lie "
             "in `0` to `n`. If it fails either test, the expansion has no such term "
             "and the question is answered."),
            ("Substitute k back and evaluate the three pieces separately",
             "The binomial coefficient, the power of the numerical part of `a`, and the "
             "power of `b` including its sign. Multiplying them in that order keeps the "
             "arithmetic small and makes a wrong sign visible."),
        ],
        "worked": {
            "title": "The constant term of (2x² - 3/x)⁹",
            "intro": [
                "A constant term is the term whose power of `x` is `0`. Nothing else in "
                "this expansion has to be computed, and the ten terms it contains would "
                "take a page.",
            ],
            "lines": [
                "a = 2x²,    b = -3/x,    n = 9",
                "",
                "general term    C(9,k) (2x²)⁹⁻ᵏ (-3/x)ᵏ",
                "",
                "the numbers      C(9,k) · 2⁹⁻ᵏ · (-3)ᵏ",
                "the power of x   from (2x²)⁹⁻ᵏ :  2(9 - k)",
                "                 from (-3/x)ᵏ  :  -k",
                "                 total:  2(9 - k) - k  =  18 - 3k",
                "",
                "constant term    18 - 3k = 0,  so k = 6",
                "                 6 is a whole number and 0 ≤ 6 ≤ 9         ✓",
                "",
                "row 9    1   9   36   84   126   126   84   36   9   1",
                "         C(9,6) = 84, entry 6 counting from 0, equal to C(9,3)",
                "",
                "term  =  84 · 2³ · (-3)⁶",
                "      =  84 · 8 · 729",
                "      =  672 · 729",
                "      =  489888",
                "",
                "exponent check   (2x²)³ = 8x⁶   and   (-3/x)⁶ = 729/x⁶",
                "                 x⁶ · x⁻⁶ = x⁰, so the term is constant    ✓",
            ],
            "after": [
                "The exponent check is the one that matters, because it recomputes the "
                "power of `x` from the two factors separately rather than reusing the "
                "expression `18 - 3k` that produced `k = 6`. A slip in collecting the "
                "exponent would survive the first calculation and fail this one.",
                "Checking the size of the number would not have helped here. The `k = 5` "
                "term of the same expansion is `-489888x³`: the same magnitude with the "
                "opposite sign, because `C(9,5)·2⁴·3⁵ = 126·16·243` is also `489888`. "
                "Two adjacent terms happening to agree in size is a coincidence of this "
                "expansion, and it is a good reason to pin `k` by the exponent rather "
                "than by recognising a number.",
            ],
        },
        "quiz_title": "Single terms",
        "quiz": [
            {"q": "What is the coefficient of `x⁷` in the expansion of `(x + 3)¹⁰`?",
             "a": ["`120`", "`1080`", "`3240`", "`9720`"],
             "c": 2,
             "why": "`a = x`, so `x⁷` needs `10 - k = 7` and `k = 3`; the term is "
                    "`C(10,3)x⁷3³ = 120·27·x⁷ = 3240x⁷`. `120` is `C(10,3)` with the "
                    "`3³` dropped. `1080` uses `3²` and `9720` uses `3⁴`, off by one in "
                    "each direction &mdash; the exponent on the `3` has to equal `k`."},
            {"q": "In the expansion of `(a + b)¹²`, written in descending powers of "
                  "`a`, the term containing `b⁵` is which term?",
             "a": ["the 5th", "the 6th", "the 8th", "the 13th"],
             "c": 1,
             "why": "`k = 5`, and the term number is `k + 1 = 6`, because `k` starts at "
                    "`0` and the terms are counted from `1`. \"The 5th\" reads `k` "
                    "itself as the term number. The 8th term is the one containing "
                    "`a⁵`, counted from the other end. `13` is the number of terms in "
                    "the expansion, `n + 1`."},
            {"q": "What is the constant term in the expansion of `(x² + 1/x)⁸`?",
             "a": ["`28`", "`56`", "`70`", "There is no constant term."],
             "c": 3,
             "why": "The general term is `C(8,k)x¹⁶⁻³ᵏ`, and `16 - 3k = 0` gives "
                    "`k = 16/3`, which is not a whole number; the powers of `x` run "
                    "`16, 13, 10, 7, 4, 1, -2, -5, -8` and skip `0`. `56` is `C(8,5)` "
                    "and `28` is `C(8,6)`, the two entries reached by rounding "
                    "`k = 16/3` down and up; `28` is also the constant term of "
                    "`(x³ + 1/x)⁸`, where `24 - 4k = 0` does have a whole-number "
                    "solution. `70` is `C(8,4)`, the coefficient of the middle term "
                    "`70x⁴`, which answers a different question."},
        ],
        "mistakes": [
            ("Taking the power of x from only one of the two parts",
             "In `(2x² - 3/x)⁹` the `1/x` contributes `-k` to the exponent. Leaving it "
             "out gives `18 - 2k` and a constant term at `k = 9`, which is a term of "
             "the expansion &mdash; it is `-19683x⁻⁹` &mdash; but not a constant one. "
             "The error produces a plausible answer rather than an impossible one."),
            ("Rounding a k that comes out fractional",
             "`k = 16/3` is not `5` or `6`; it is the statement that the exponents jump "
             "from `1` to `-2` without passing through `0`. Rounding it returns the "
             "coefficient of some other power of `x`, correctly computed for a question "
             "nobody asked."),
            ("Putting k on a and n - k on b",
             "The exponents are `n - k` on `a` and `k` on `b`, and swapping them gives "
             "the mirror term. In `(x + 3)¹⁰` that turns the coefficient of `x⁷` from "
             "`3240` into `262440`, which is the coefficient of `x³`. Both are entries "
             "of the same expansion, so neither the size nor the sign looks wrong."),
        ],
        "standard": ("Finish when a question about one term becomes an equation in k without any expanding.",
                     "You should be able to write the general term of any bracket, "
                     "collect its power of `x` from both parts, solve for `k`, and say "
                     "plainly when no such term exists. Getting `C(n,k)` from a row of "
                     "the triangle or from the factorial formula, and the sign from "
                     "`(-1)ᵏ`, should be routine by now."),
        "note": "That closes the course. It began with a sequence as a function on the "
                "positive integers, moved to the sums of their terms, and needed a "
                "limit of partial sums before an infinite one could mean anything; it ends "
                "with a coefficient that is a count. The three habits worth keeping are "
                "the ones the course kept insisting on: derive the closed form rather "
                "than reciting it, check the condition before applying the formula, and "
                "say exactly what a check has established and what it has not.",
    },
]
