"""Course 5, lessons 07-12 — random variables and distributions."""

LESSONS = [
    # ---------------------------------------------------------------- 07
    {
        "slug": "random-variables",
        "title": "Random Variables",
        "module": "Random variables",
        "one_line": "A number attached to each outcome.",
        "summary": (
            "A random variable is a function from the sample space to the reals. Its "
            "distribution collects the probabilities of its values, and it is neither "
            "random nor a variable."
        ),
        "key": [
            "X : S → ℝ            a FUNCTION on outcomes",
            "P(X = k) = P({s ∈ S : X(s) = k})",
            "Σ_k P(X = k) = 1     the distribution sums to 1",
            "Different X can share a distribution.",
        ],
        "key_label": "A function, not a variable",
        "concepts_intro": (
            "Random variables let one sample space answer many questions, by attaching "
            "different numbers to the same outcomes."
        ),
        "concepts": [
            ("It is a function",
             "`X(s)` is a number for each outcome `s`. Nothing about it is random; the "
             "randomness is in which `s` occurs."),
            ("The distribution is a summary",
             "`P(X = k)` for each value `k`. It discards which outcomes gave that value, "
             "which is usually exactly what you want."),
            ("Different variables can share a distribution",
             "The number of heads in three flips and the number of tails have the same "
             "distribution and are different functions."),
        ],
        "read_title": "Random variables and distributions",
        "read_intro": "The definition, the distribution, and how several variables interact.",
        "body": [
            ("def", ("Random variable",
                     "A <strong>random variable</strong> on a sample space `S` is a "
                     "function `X : S → ℝ`. The event `X = k` is "
                     "`{s ∈ S : X(s) = k}`, and `P(X = k)` is its probability.")),
            ("p", "The name is doubly misleading, as is traditional. `X` is a function and "
                  "it is completely determined; what varies is which outcome occurs. "
                  "Reading `X` as a function on outcomes removes most of the confusion this "
                  "topic causes."),
            ("def", ("Probability distribution",
                     "The <strong>distribution</strong> of a discrete random variable `X` "
                     "is the list of pairs `(k, P(X = k))` over the values `X` takes. The "
                     "probabilities are non-negative and sum to 1.")),
            ("example", ("Sum of two dice",
                         "`S` is the 36 pairs and `X(a,b) = a + b`. Then "
                         "`P(X = 2) = 1/36`, `P(X = 7) = 6/36`, and so on. The distribution "
                         "is the familiar triangle: `1,2,3,4,5,6,5,4,3,2,1` over 36.")),
            ("math", [
                "k     2    3    4    5    6    7    6    5    4    3    2",
                "      ↑ counts of ordered pairs summing to k+1 … (k = 2 … 12)",
                "",
                "P(X=k):  1/36 2/36 3/36 4/36 5/36 6/36 5/36 4/36 3/36 2/36 1/36",
                "sum = 36/36 = 1                                        ✓",
            ]),
            ("h3", "Indicator variables"),
            ("def", ("Indicator",
                     "For an event `A`, the <strong>indicator</strong> `I_A` is the random "
                     "variable equal to 1 when `A` occurs and 0 otherwise. Its distribution "
                     "is `P(I_A = 1) = P(A)`.")),
            ("p", "Indicators look trivial and are the single most useful tool in lesson 9. "
                  "Any count can be written as a sum of indicators, and expectation adds "
                  "over sums regardless of dependence."),
            ("h3", "Several variables together"),
            ("def", ("Joint distribution and independence",
                     "The <strong>joint distribution</strong> of `X` and `Y` is "
                     "`P(X = a, Y = b)` for all `a, b`. They are "
                     "<strong>independent</strong> when "
                     "`P(X = a, Y = b) = P(X = a)P(Y = b)` for every pair.")),
            ("example", ("Dependent by construction",
                         "Roll two dice; let `X` be the first die and `Y` the sum. These "
                         "are dependent: `P(Y = 2 | X = 3) = 0` while `P(Y = 2) = 1/36`. "
                         "Knowing `X` restricts `Y` sharply.")),
            ("p", "Functions of random variables are random variables: `X²`, `X + Y` and "
                  "`max(X, Y)` are all functions on `S`. Their distributions are computed "
                  "by collecting the outcomes, which is the only method available and is "
                  "usually enough."),
        ],
        "lab": ("distribution", {
            "kind": "dice",
            "panel_title": "A distribution, listed",
            "panel_intro": "The bars are `P(X = k)` and the table lists them with their "
                           "contributions to the expectation. The sum of the probability "
                           "column must be 1, and it is shown.",
        }),
        "steps_title": "Working with a random variable",
        "steps_intro": "Define the function before computing anything about it.",
        "steps": [
            ("Say what `X(s)` is for each outcome",
             "\"The number of heads\", \"the sum\", \"1 if it rains\". A random variable "
             "with no stated rule is not defined."),
            ("Collect the outcomes by value",
             "`P(X = k)` is the probability of the set of outcomes giving `k`. This is "
             "course 4's counting again."),
            ("Check the distribution sums to 1",
             "Every outcome contributes to exactly one value, so the probabilities must "
             "total 1. A free check that catches missed cases."),
            ("For several variables, build the joint table",
             "Independence is a statement about every entry of it, not about a summary."),
        ],
        "worked": {
            "title": "Three coins, two variables",
            "intro": ["`S = {HHH, HHT, HTH, HTT, THH, THT, TTH, TTT}`, each `1/8`."],
            "lines": [
                "X = number of heads          Y = 1 if the first flip is heads, else 0",
                "",
                "outcome  HHH HHT HTH HTT THH THT TTH TTT",
                "X          3   2   2   1   2   1   1   0",
                "Y          1   1   1   1   0   0   0   0",
                "",
                "Distribution of X:  P(0)=1/8  P(1)=3/8  P(2)=3/8  P(3)=1/8   sum 1  ✓",
                "Distribution of Y:  P(0)=1/2  P(1)=1/2                       sum 1  ✓",
                "",
                "Independent?   P(X=3, Y=1) = 1/8",
                "               P(X=3)P(Y=1) = (1/8)(1/2) = 1/16      NOT equal",
                "               ⟹ dependent, as expected: Y is part of X.",
            ],
            "after": [
                "`Y` is an indicator, and `X` is the sum of three such indicators &mdash; "
                "one per flip. That decomposition is what lesson 9 exploits, and it works "
                "even though the indicators here are visibly not independent of `X`."
            ],
        },
        "quiz_title": "Random variables",
        "quiz": [
            {"q": "A random variable is:",
             "a": ["a variable that changes randomly",
                   "a function from the sample space to the reals",
                   "a probability", "an event"],
             "c": 1,
             "why": "It is a completely determined function. The randomness is in which "
                    "outcome occurs, not in `X` itself."},
            {"q": "The probabilities in a distribution must:",
             "a": ["be equal", "sum to 1", "be less than 1/2", "be integers"],
             "c": 1,
             "why": "Every outcome maps to exactly one value, so the values partition `S` "
                    "and their probabilities total 1."},
            {"q": "An indicator variable `I_A` takes values:",
             "a": ["0 and 1", "−1 and 1", "any real", "0 only"],
             "c": 0,
             "why": "1 when `A` occurs, 0 otherwise. Its expectation is `P(A)`, which "
                    "lesson 9 uses constantly."},
        ],
        "mistakes": [
            ("Treating `X` as random rather than as a function",
             "`X` is fixed. Which outcome occurs is what varies, and keeping that straight "
             "makes joint distributions readable."),
            ("Confusing the value with the event",
             "`X = 3` is an event &mdash; a set of outcomes. `P(X = 3)` is the probability "
             "of that set."),
            ("Assuming variables on the same space are independent",
             "The first die and the sum live on one sample space and are strongly "
             "dependent. Independence must be checked on the joint distribution."),
        ],
        "standard": ("Finish when you can build a distribution from a sample space unaided.",
                     "Roll two dice and let `X` be the larger of the two values. Write the "
                     "distribution of `X` and check it sums to 1. `P(X = k)` is "
                     "`(2k − 1)/36`, and deriving that is the exercise."),
        "note": "Random variables are how one probability space answers many questions: "
                "the 36 dice outcomes support the sum, the maximum, the difference, and "
                "any other function you care to define, each with its own distribution.",
    },
    # ---------------------------------------------------------------- 08
    {
        "slug": "expected-value",
        "title": "Expected Value",
        "module": "Random variables",
        "one_line": "The probability-weighted average, and what it does not mean.",
        "summary": (
            "`E[X] = Σ k·P(X = k)`. It is the long-run average, it need not be a "
            "possible value, and it is not the most likely outcome. Those three "
            "clarifications prevent most misuse."
        ),
        "key": [
            "E[X] = Σ_k k · P(X = k)",
            "E[X] need not be a value X can take",
            "E[X] is NOT the most likely value",
            "E[aX + b] = a·E[X] + b",
        ],
        "key_label": "The definition and three cautions",
        "concepts_intro": (
            "Expectation is a one-line definition whose interpretation is where the "
            "difficulty lies."
        ),
        "concepts": [
            ("It is a weighted average",
             "Each value weighted by its probability. For equally likely outcomes it is "
             "the ordinary mean."),
            ("It need not be attainable",
             "The expected value of a die roll is 3.5, and no die shows 3.5. The "
             "expectation summarises the distribution, not any single outcome."),
            ("It is not the mode",
             "The most likely value and the average are different summaries and often "
             "differ, especially for skewed distributions."),
        ],
        "read_title": "Expectation",
        "read_intro": "The definition, the linear rule, and the games it settles.",
        "body": [
            ("def", ("Expected value",
                     "For a discrete random variable `X` taking finitely many values, "
                     "`E[X] = Σ_k k · P(X = k)`, summed over the values `X` takes. "
                     "Equivalently `E[X] = Σ_{s ∈ S} X(s)P(s)`.")),
            ("p", "The second form is often more useful: sum over outcomes rather than "
                  "over values. It makes the linearity of lesson 9 immediate."),
            ("example", ("A fair die",
                         "`E[X] = (1+2+3+4+5+6)/6 = 3.5`. Not a value the die can show, and "
                         "that is not a defect: it is the long-run average of many rolls.")),
            ("thm", ("Linear transformation",
                     "`E[aX + b] = aE[X] + b` for constants `a, b`.")),
            ("proof", [
                "`E[aX + b] = Σ_s (aX(s) + b)P(s) = a Σ_s X(s)P(s) + b Σ_s P(s) = "
                "aE[X] + b`, using that the probabilities sum to 1.",
            ]),
            ("thm", ("Expectation of a function",
                     "`E[g(X)] = Σ_k g(k)P(X = k)`. Note `E[g(X)] ≠ g(E[X])` in general: "
                     "for a fair die `E[X²] = 91/6 ≈ 15.17` while `(E[X])² = 12.25`.")),
            ("p", "That inequality is not a curiosity; it is the reason variance is defined "
                  "the way lesson 10 defines it, and it is behind the general fact that "
                  "averaging and transforming do not commute."),
            ("h3", "Fair games and expected winnings"),
            ("example", ("A carnival game",
                         "Pay £2 to roll a die and win £`X` where `X` is the face shown. "
                         "`E[winnings] = 3.5 − 2 = £1.50` per play in your favour, so the "
                         "game is not one anybody would offer.")),
            ("example", ("Roulette",
                         "European roulette has 37 pockets. A £1 bet on a single number "
                         "pays 35 to 1. `E[profit] = 35 · (1/37) − 1 · (36/37) = −1/37 ≈ "
                         "−£0.027` per pound staked. Every bet on the wheel has the same "
                         "expectation, which is the design.")),
            ("def", ("Fair game",
                     "A game is <strong>fair</strong> when the expected net gain is 0. "
                     "Casino games are deliberately unfair by a small margin, and the "
                     "margin is what the house relies on over many plays.")),
            ("h3", "What expectation does not tell you"),
            ("ul", [
                "<strong>Not the most likely outcome.</strong> The expected number of "
                "heads in 3 flips is 1.5, which is impossible.",
                "<strong>Not a guarantee.</strong> A game with positive expectation can "
                "lose for a long time; lesson 10's variance is what measures that.",
                "<strong>Not enough to compare two options.</strong> Two bets with equal "
                "expectation can differ enormously in risk, and expectation alone cannot "
                "see it.",
            ]),
        ],
        "lab": ("distribution", {
            "kind": "binomial",
            "panel_title": "Summed, then compared",
            "panel_intro": "`E[X]` is computed by summing `k·P(X = k)` down the table, and "
                           "shown beside the closed form. The dashed line marks it on the "
                           "distribution &mdash; often between two bars.",
        }),
        "steps_title": "Computing an expectation",
        "steps_intro": "From the definition first; formulas afterwards.",
        "steps": [
            ("List the values and their probabilities",
             "The distribution. If it does not sum to 1, stop and fix it."),
            ("Multiply each value by its probability and sum",
             "That is the definition, and for small distributions it is the fastest route."),
            ("Use linearity where it applies",
             "`E[aX + b] = aE[X] + b` avoids recomputing a whole distribution after a "
             "shift or a scaling."),
            ("Sanity-check the position",
             "The expectation lies between the smallest and largest values, and near the "
               "bulk of the probability. Anything outside that range is an error."),
        ],
        "worked": {
            "title": "An insurance calculation",
            "intro": ["A policy pays £10 000 on an event with probability 0.002, and the premium is £30."],
            "lines": [
                "From the insurer's point of view, let X be the net gain on one policy.",
                "",
                "   no claim:   X = +30       P = 0.998",
                "   claim:      X = 30 − 10000 = −9970    P = 0.002",
                "",
                "   E[X] = 30(0.998) + (−9970)(0.002)",
                "        = 29.94 − 19.94",
                "        = £10.00 per policy",
                "",
                "The customer's expectation is exactly −£10.",
                "The insurer's edge comes from selling MANY policies, where the",
                "average approaches the expectation — which is lesson 10's subject.",
            ],
            "after": [
                "Both parties can be acting sensibly. The customer accepts a negative "
                "expectation to remove a large downside they could not absorb; the insurer "
                "accepts the risk because across many policies the variance of the average "
                "collapses. Expectation alone explains neither decision."
            ],
        },
        "quiz_title": "Expectation",
        "quiz": [
            {"q": "`E[X]` for a fair six-sided die is:",
             "a": ["3", "3.5", "4", "6"],
             "c": 1,
             "why": "`(1+2+3+4+5+6)/6 = 3.5`. It is not a value the die can show, which is "
                    "normal for an average."},
            {"q": "`E[X] = 2.7`. What does that tell you about the most likely value?",
             "a": ["It is 3", "It is 2.7", "Nothing directly", "It is 2 or 3"],
             "c": 2,
             "why": "The mean and the mode are different summaries. A distribution with "
                    "mean 2.7 can easily have its highest probability at 1."},
            {"q": "`E[X²]` versus `(E[X])²`:",
             "a": ["always equal", "`E[X²] ≥ (E[X])²`", "`E[X²] ≤ (E[X])²`", "unrelated"],
             "c": 1,
             "why": "Their difference is the variance, which is non-negative. That is "
                    "exactly lesson 10's computational formula."},
        ],
        "mistakes": [
            ("Expecting the expectation to be attainable",
             "3.5 for a die and 1.5 heads in three flips are both fine. The expectation "
             "summarises the distribution."),
            ("Reading the expectation as the typical outcome",
             "For skewed distributions the mean can be far from anything likely. The "
             "geometric distribution in lesson 12 is the standard example."),
            ("Applying a function inside the expectation",
             "`E[g(X)] ≠ g(E[X])` unless `g` is linear. This is the source of many wrong "
             "risk calculations."),
        ],
        "standard": ("Finish when you can compute an expectation and say what it does not "
                     "claim.",
                     "Compute the expected number of heads in five fair flips from the "
                     "definition, then state in one sentence why 2.5 is a sensible answer "
                     "for a quantity that must be an integer."),
        "note": "Lesson 9 gives a much faster route to most expectations. Linearity holds "
                "without independence, which makes decomposing a complicated variable into "
                "indicators the dominant technique in the rest of this course.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "linearity-of-expectation",
        "title": "Linearity of Expectation",
        "module": "Random variables",
        "one_line": "`E[X + Y] = E[X] + E[Y]`, whether or not they are independent.",
        "summary": (
            "The most useful fact in elementary probability. It needs no independence, "
            "which lets a complicated count be decomposed into indicators and summed "
            "term by term."
        ),
        "key": [
            "E[X + Y] = E[X] + E[Y]           ALWAYS",
            "E[c₁X₁ + … + cₙXₙ] = Σ cᵢE[Xᵢ]",
            "E[XY] = E[X]E[Y]  only when independent",
            "Decompose into INDICATORS and sum.",
        ],
        "key_label": "No independence required",
        "concepts_intro": (
            "Linearity is what makes hard expectations easy: split the variable into "
            "simple pieces and add."
        ),
        "concepts": [
            ("Independence is not needed",
             "`E[X + Y] = E[X] + E[Y]` holds for any two random variables on the same "
             "space, however entangled."),
            ("Indicators are the workhorse",
             "Write a count as a sum of indicators, one per thing being counted. Each "
             "indicator's expectation is a probability."),
            ("Products are different",
             "`E[XY] = E[X]E[Y]` requires independence. Confusing the two rules is the "
             "one real trap here."),
        ],
        "read_title": "Linearity",
        "read_intro": "The theorem, why independence is irrelevant, and four applications.",
        "body": [
            ("thm", ("Linearity of expectation",
                     "For random variables `X, Y` on the same sample space and constants "
                     "`a, b`: `E[aX + bY] = aE[X] + bE[Y]`. No independence assumption is "
                     "needed.")),
            ("proof", [
                "Summing over outcomes, "
                "`E[aX + bY] = Σ_s (aX(s) + bY(s))P(s) = a Σ_s X(s)P(s) + b Σ_s Y(s)P(s) "
                "= aE[X] + bE[Y]`.",
                "Nothing about the joint behaviour of `X` and `Y` entered, which is exactly "
                "why independence is not required.",
            ]),
            ("p", "The proof is three lines and the consequence is enormous. `E[XY]` by "
                  "contrast genuinely depends on the joint distribution, and the two facts "
                  "are worth keeping apart deliberately."),
            ("h3", "Indicator decomposition"),
            ("thm", ("Expectation of an indicator",
                     "`E[I_A] = 1 · P(A) + 0 · P(Ā) = P(A)`.")),
            ("p", "So if `X` counts how many of the events `A₁, …, A_n` occur, then "
                  "`X = I_{A₁} + ⋯ + I_{A_n}` and `E[X] = Σ P(Aᵢ)`. The events may overlap, "
                  "depend on each other, or be governed by anything at all."),
            ("example", ("Heads in `n` flips",
                         "`X = Σ Iᵢ` where `Iᵢ` indicates heads on flip `i`. Each has "
                         "expectation `p`, so `E[X] = np` &mdash; without computing the "
                         "binomial distribution at all.")),
            ("example", ("Fixed points of a random permutation",
                         "`X` counts the elements left in place. `X = Σ Iᵢ` where `Iᵢ` "
                         "indicates that `i` is fixed, and `P(Iᵢ = 1) = 1/n`. So "
                         "`E[X] = n · (1/n) = 1`, for every `n`. The indicators are "
                         "dependent &mdash; knowing `n − 1` elements are fixed forces the "
                         "last &mdash; and linearity does not care.")),
            ("p", "That result is worth pausing on. On average exactly one person gets "
                  "their own hat back, whether there are 5 people or 5 million. Computing "
                  "it from the derangement distribution of course 4 would be considerably "
                  "harder."),
            ("example", ("The coupon collector",
                         "There are `n` distinct coupons, one per box at random. How many "
                         "boxes to collect them all? Let `Xᵢ` be the number of boxes bought "
                         "while holding exactly `i − 1` distinct coupons. Then "
                         "`E[Xᵢ] = n/(n − i + 1)` (lesson 12 supplies that), so "
                         "`E[total] = n(1 + 1/2 + ⋯ + 1/n) ≈ n ln n`. For `n = 50` that is "
                         "about 225 boxes.")),
            ("example", ("Matching pairs",
                         "Two shuffled decks are dealt face up side by side. The expected "
                         "number of positions where the cards match is "
                         "`52 · (1/52) = 1`. Same computation as the hat problem, and again "
                         "the indicators are dependent.")),
            ("thm", ("Products need independence",
                     "If `X` and `Y` are independent then `E[XY] = E[X]E[Y]`. Without "
                     "independence this fails: take `Y = X` with `X` a fair coin scored 0 "
                     "or 1, so `E[X] = 1/2` and `E[XY] = E[X²] = 1/2 ≠ 1/4`.")),
        ],
        "lab": ("distribution", {
            "kind": "binomial",
            "panel_title": "`np`, from the definition and from linearity",
            "panel_intro": "The lab sums `k·P(X = k)` term by term and compares it with "
                           "`np`. Linearity gives `np` in one line, without the "
                           "distribution.",
        }),
        "steps_title": "Using linearity",
        "steps_intro": "Decompose, then add.",
        "steps": [
            ("Write the variable as a sum",
             "Usually one indicator per item, position or event being counted."),
            ("Compute the expectation of one piece",
             "For an indicator this is a single probability, and symmetry often makes all "
             "the pieces identical."),
            ("Add, without checking independence",
             "Linearity holds regardless. This is the step that saves the work."),
            ("Do not use it for products",
             "`E[XY]` needs independence. If the quantity is a product, this technique "
             "does not apply."),
        ],
        "worked": {
            "title": "Expected number of matching pairs",
            "intro": ["Two shuffled decks of `n` cards, dealt side by side. How many positions match?"],
            "lines": [
                "Let Iⱼ = 1 if position j matches, 0 otherwise.   X = I₁ + … + Iₙ",
                "",
                "P(Iⱼ = 1) = 1/n     — whatever is in the first deck at position j,",
                "                      the second deck has 1 chance in n of matching",
                "",
                "By linearity:",
                "   E[X] = Σⱼ E[Iⱼ] = n · (1/n) = 1",
                "",
                "The Iⱼ are NOT independent: if n−1 positions match, the last must.",
                "Linearity does not care.",
                "",
                "Computing this from the distribution of X would require the",
                "derangement numbers of course 4 lesson 10 — for one number.",
            ],
            "after": [
                "The answer is 1 for every `n`, which connects directly to derangements: "
                "the distribution of the number of matches converges to a Poisson "
                "distribution with mean 1, and `P(no match) → 1/e` is exactly the "
                "derangement limit."
            ],
        },
        "quiz_title": "Linearity",
        "quiz": [
            {"q": "`E[X + Y] = E[X] + E[Y]` requires:",
             "a": ["independence", "nothing", "`X` and `Y` disjoint", "identical distributions"],
             "c": 1,
             "why": "It holds for any two random variables on the same space. That is what "
                    "makes indicator decomposition so powerful."},
            {"q": "Expected number of fixed points of a random permutation of `n` elements:",
             "a": ["`n`", "1", "`n/2`", "`1/n`"],
             "c": 1,
             "why": "`n` indicators each with probability `1/n`, so the sum is 1 &mdash; "
                    "for every `n`."},
            {"q": "`E[XY] = E[X]E[Y]` requires:",
             "a": ["nothing", "independence", "`X = Y`", "both non-negative"],
             "c": 1,
             "why": "Products are where independence is needed. Sums are not, and keeping "
                    "the two rules apart is the whole caution of this lesson."},
        ],
        "mistakes": [
            ("Checking independence before adding",
             "Unnecessary, and the habit obscures how general linearity is. Add first."),
            ("Applying linearity to a product",
             "`E[XY]` depends on the joint distribution. Linearity says nothing about it."),
            ("Not looking for an indicator decomposition",
             "Most counting expectations become one line this way. If a distribution looks "
             "hard, ask what is being counted."),
        ],
        "standard": ("Finish when decomposition into indicators is your first move.",
                     "Compute the expected number of runs of consecutive heads in `n` fair "
                     "flips, using one indicator per position for \"a run starts here\". "
                     "The answer is `(n+1)/4`, and the indicators overlap heavily."),
        "note": "Linearity is the reason expectation is more tractable than probability. "
                "`P(X = k)` for a complicated `X` may be very hard while `E[X]` is a sum of "
                "`n` easy probabilities, which is why so many arguments compute the mean "
                "and never touch the distribution.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "variance",
        "title": "Variance and Standard Deviation",
        "module": "Random variables",
        "one_line": "How far from the mean, on average — squared.",
        "summary": (
            "Variance is the expected squared deviation from the mean, and it measures "
            "spread. It adds over independent variables, and its square root has the "
            "same units as `X`."
        ),
        "key": [
            "Var(X) = E[(X − E[X])²] = E[X²] − (E[X])²",
            "σ(X) = √Var(X)                  same units as X",
            "Var(aX + b) = a²·Var(X)         shifts do not matter",
            "Var(X + Y) = Var(X) + Var(Y)    only when INDEPENDENT",
        ],
        "key_label": "Spread, and its one caveat",
        "concepts_intro": (
            "Expectation locates a distribution; variance says how tightly it is packed "
            "around that location."
        ),
        "concepts": [
            ("Squaring makes deviations positive",
             "`E[X − E[X]] = 0` always, so deviations must be squared before averaging or "
             "they cancel."),
            ("The computational formula is faster",
             "`Var(X) = E[X²] − (E[X])²`. Two expectations rather than a new distribution "
             "of deviations."),
            ("Variance adds only for independent variables",
             "Unlike expectation. `Var(X + X) = 4Var(X)`, not `2Var(X)` &mdash; and that "
             "is the case where dependence is total."),
        ],
        "read_title": "Measuring spread",
        "read_intro": "The definition, the shortcut, the rules, and what a standard deviation buys you.",
        "body": [
            ("def", ("Variance and standard deviation",
                     "`Var(X) = E[(X − μ)²]` where `μ = E[X]`. The "
                     "<strong>standard deviation</strong> is `σ(X) = √Var(X)`.")),
            ("thm", ("Computational formula",
                     "`Var(X) = E[X²] − (E[X])²`.")),
            ("proof", [
                "`E[(X − μ)²] = E[X² − 2μX + μ²] = E[X²] − 2μE[X] + μ² = E[X²] − 2μ² + μ² "
                "= E[X²] − μ²`, using linearity and `E[X] = μ`.",
            ]),
            ("p", "Two consequences drop out. Variance is non-negative, so "
                  "`E[X²] ≥ (E[X])²` always &mdash; the inequality noticed in lesson 8. And "
                  "`Var(X) = 0` exactly when `X` is constant."),
            ("thm", ("Scaling and shifting",
                     "`Var(aX + b) = a²Var(X)`. Adding a constant moves the distribution "
                     "without changing its spread; scaling by `a` scales the spread by "
                     "`|a|` and the variance by `a²`.")),
            ("thm", ("Variance of a sum",
                     "If `X` and `Y` are independent, `Var(X + Y) = Var(X) + Var(Y)`. "
                     "Without independence, `Var(X + Y) = Var(X) + Var(Y) + 2Cov(X,Y)`.")),
            ("p", "This is the difference from expectation, and it is worth stating "
                  "plainly: sums of expectations never need independence, sums of variances "
                  "always do. Adding `X` to itself makes the point &mdash; "
                  "`Var(2X) = 4Var(X)`, not `2Var(X)`."),
            ("example", ("A fair die",
                         "`E[X] = 3.5` and `E[X²] = (1+4+9+16+25+36)/6 = 91/6 ≈ 15.167`. So "
                         "`Var(X) = 91/6 − 49/4 = 35/12 ≈ 2.917` and `σ ≈ 1.708`.")),
            ("example", ("Two bets, one expectation",
                         "Bet A wins £1 or loses £1 on a fair coin: `E = 0`, `Var = 1`. "
                         "Bet B wins £1000 or loses £1000: `E = 0`, `Var = 1 000 000`. Equal "
                         "expectations, and no one would treat them as equivalent. "
                         "Expectation alone cannot distinguish them; variance can.")),
            ("h3", "Why variance shrinks when you average"),
            ("thm", ("Variance of an average",
                     "For independent `X₁, …, X_n` each with variance `σ²`, the average "
                     "`X̄ = (X₁ + ⋯ + X_n)/n` has `Var(X̄) = σ²/n` and standard deviation "
                     "`σ/√n`.")),
            ("proof", [
                "The sum has variance `nσ²` by independence, and dividing by `n` scales the "
                "variance by `1/n²`, giving `σ²/n`.",
            ]),
            ("p", "The `√n` is why the insurer of lesson 8 sells many policies. It also "
                  "explains why halving the uncertainty of an estimate requires four times "
                  "the data &mdash; the most consequential single fact in applied "
                  "statistics."),
            ("thm", ("Chebyshev's inequality",
                     "For any `k &gt; 0`, `P(|X − μ| ≥ kσ) ≤ 1/k²`. At most a quarter of "
                     "any distribution lies more than two standard deviations from its "
                     "mean, and at most a ninth beyond three.")),
            ("p", "Chebyshev is weak &mdash; for most real distributions the true tails are "
                  "far thinner &mdash; and it holds for every distribution with a finite "
                  "variance, with no shape assumption at all. That generality is what makes "
                  "it worth having."),
        ],
        "lab": ("distribution", {
            "kind": "uniform",
            "panel_title": "Spread, computed",
            "panel_intro": "`Var(X) = E[X²] − (E[X])²` is computed by summing both "
                           "expectations from the table. Change `n` and watch the "
                           "expectation stay central while the spread grows.",
        }),
        "steps_title": "Computing a variance",
        "steps_intro": "Two expectations, then subtract.",
        "steps": [
            ("Compute `E[X]`",
             "The weighted average, as in lesson 8."),
            ("Compute `E[X²]`",
             "Same distribution, values squared: `Σ k²P(X = k)`. Not `(E[X])²`."),
            ("Subtract",
             "`Var(X) = E[X²] − (E[X])²`. If the result is negative, one of the two "
               "expectations is wrong."),
            ("Take the square root for interpretation",
             "`σ` is in the same units as `X` and is what to quote. Variance is in squared "
             "units and is what adds."),
        ],
        "worked": {
            "title": "Variance of a sum, with and without independence",
            "intro": ["Two fair dice, `X` and `Y`, each with variance `35/12`."],
            "lines": [
                "INDEPENDENT — X and Y are two separate dice:",
                "   Var(X + Y) = Var(X) + Var(Y) = 35/12 + 35/12 = 35/6 ≈ 5.833",
                "   σ(X+Y) ≈ 2.415",
                "",
                "DEPENDENT — the same die counted twice, so Y = X:",
                "   X + Y = 2X",
                "   Var(2X) = 4·Var(X) = 4 · 35/12 = 35/3 ≈ 11.667",
                "   σ(2X) ≈ 3.416",
                "",
                "Both sums have expectation 7.  Their spreads differ by a factor",
                "of two in the variance, because in the second the two",
                "contributions cannot cancel.",
            ],
            "after": [
                "This is the concrete reason variance needs independence and expectation "
                "does not. Two independent dice can offset each other &mdash; a high one "
                "with a low one &mdash; while a doubled die cannot, so the spread is "
                "strictly larger."
            ],
        },
        "quiz_title": "Variance",
        "quiz": [
            {"q": "`Var(X) = E[X²] − (E[X])²`. Why is it never negative?",
             "a": ["By convention",
                   "Because it is the expectation of a square",
                   "Because `E[X] ≥ 0`",
                   "It can be negative"],
             "c": 1,
             "why": "It equals `E[(X − μ)²]`, an average of non-negative numbers. So "
                    "`E[X²] ≥ (E[X])²` always."},
            {"q": "`Var(3X + 5)` equals:",
             "a": ["`3Var(X) + 5`", "`9Var(X)`", "`9Var(X) + 25`", "`3Var(X)`"],
             "c": 1,
             "why": "Shifts do not change spread and scaling by 3 multiplies the variance "
                    "by 9."},
            {"q": "`Var(X + Y) = Var(X) + Var(Y)` requires:",
             "a": ["nothing", "independence", "`X = Y`", "equal variances"],
             "c": 1,
             "why": "Unlike expectation, variance needs independence &mdash; or a "
                    "covariance term. `Var(2X) = 4Var(X)` shows the difference."},
        ],
        "mistakes": [
            ("Computing `(E[X])²` where `E[X²]` is wanted",
             "They differ by exactly the variance. Squaring the values and then averaging "
             "is not averaging and then squaring."),
            ("Adding variances of dependent variables",
             "`Var(X + Y)` needs the covariance term unless they are independent. This is "
             "the main asymmetry with expectation."),
            ("Quoting variance where a standard deviation is meant",
             "Variance is in squared units. `σ` is comparable with the values themselves "
             "and is what to report."),
        ],
        "standard": ("Finish when you can say why averaging reduces spread by `√n`.",
                     "Compute the variance of the average of `n` independent fair dice, "
                     "and state what happens to `σ` as `n` grows. That single fact "
                     "underlies polling margins, insurance, and repeated measurement."),
        "note": "Chebyshev's inequality is the bridge from variance to the law of large "
                "numbers: as `n` grows, `Var(X̄) = σ²/n → 0`, so Chebyshev forces the "
                "average to concentrate at the mean. That is a proof of the weak law, in "
                "two lines, from this lesson's material.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "binomial-distribution",
        "title": "Bernoulli Trials and the Binomial Distribution",
        "module": "Distributions",
        "one_line": "Counting successes in a fixed number of independent trials.",
        "summary": (
            "`n` independent trials, each succeeding with probability `p`. The number of "
            "successes has `P(X = k) = C(n,k)p^k(1−p)^{n−k}`, mean `np` and variance "
            "`np(1−p)`."
        ),
        "key": [
            "P(X = k) = C(n,k) pᵏ (1−p)ⁿ⁻ᵏ",
            "E[X]   = np",
            "Var(X) = np(1−p)",
            "requires: FIXED n, INDEPENDENT trials, CONSTANT p",
        ],
        "key_label": "The most-used discrete distribution",
        "concepts_intro": (
            "Three assumptions define it. When they hold the formula applies exactly; "
            "when they do not it can be badly wrong."
        ),
        "concepts": [
            ("The coefficient counts the positions",
             "`C(n,k)` is the number of ways the `k` successes can be arranged, and "
               "`p^k(1−p)^{n−k}` is the probability of any one such arrangement."),
            ("The mean is `np` by linearity",
             "Write `X` as a sum of `n` indicators each with expectation `p`. No "
             "summation over the distribution is needed."),
            ("The assumptions are the fragile part",
             "Fixed `n`, independent trials, constant `p`. Sampling without replacement "
             "violates the last two and needs the hypergeometric distribution instead."),
        ],
        "read_title": "The binomial distribution",
        "read_intro": "Derivation, moments, and where the assumptions fail.",
        "body": [
            ("def", ("Bernoulli trial",
                     "A single experiment with two outcomes, success with probability `p` "
                     "and failure with probability `1 − p`. Its indicator has mean `p` and "
                     "variance `p(1−p)`.")),
            ("thm", ("Binomial distribution",
                     "If `X` counts the successes in `n` independent Bernoulli trials each "
                     "with probability `p`, then "
                     "`P(X = k) = C(n,k)p^k(1−p)^{n−k}` for `k = 0, …, n`.")),
            ("proof", [
                "One particular sequence with `k` successes and `n − k` failures has "
                "probability `p^k(1−p)^{n−k}`, by independence.",
                "The number of such sequences is the number of ways to choose which `k` "
                "trials succeed, which is `C(n,k)`.",
                "The sequences are disjoint events, so the sum rule gives the product.",
            ]),
            ("p", "The distribution sums to 1 by the binomial theorem of course 4 lesson 6: "
                  "`Σ_k C(n,k)p^k(1−p)^{n−k} = (p + (1−p))ⁿ = 1`. That is the theorem doing "
                  "genuine work, not an analogy."),
            ("thm", ("Mean and variance",
                     "`E[X] = np` and `Var(X) = np(1−p)`.")),
            ("proof", [
                "Write `X = I₁ + ⋯ + I_n` with `Iⱼ` indicating success on trial `j`. Then "
                "`E[X] = Σ E[Iⱼ] = np` by linearity &mdash; no independence needed for this "
                "step.",
                "For the variance, independence IS needed: "
                "`Var(X) = Σ Var(Iⱼ) = np(1−p)`, since each indicator has variance "
                "`p(1−p)`.",
            ]),
            ("p", "The variance is largest at `p = 1/2`, where it is `n/4`, and vanishes at "
                  "`p = 0` and `p = 1`. That is exactly right: a trial that always succeeds "
                  "or always fails has no spread."),
            ("example", ("Ten coin flips",
                         "`n = 10`, `p = 1/2`. `P(exactly 5 heads) = C(10,5)/2¹⁰ = "
                         "252/1024 ≈ 0.246`. Slightly under a quarter, which surprises "
                         "people who expect the most likely value to be likely.")),
            ("example", ("Quality control",
                         "A process produces 2% defectives. In a batch of 100, "
                         "`E[defects] = 2` and `P(no defects) = 0.98¹⁰⁰ ≈ 0.133`. So "
                         "about one batch in eight is clean.")),
            ("h3", "Where the assumptions fail"),
            ("ul", [
                "<strong>Sampling without replacement.</strong> Drawing 5 cards from a "
                "deck, the probability of an ace changes with each draw. The correct "
                "distribution is hypergeometric; the binomial is an approximation that is "
                "good when the sample is small relative to the population.",
                "<strong>Dependent trials.</strong> Weather on consecutive days is not "
                "independent, so counting rainy days with a binomial understates the "
                "chance of long runs.",
                "<strong>Varying `p`.</strong> If the success probability drifts, the "
                "distribution is not binomial even though the trials are independent.",
            ]),
            ("p", "The failure mode is characteristic: the mean stays about right while the "
                  "variance is wrong, usually understated. That makes the extremes far more "
                  "likely than the model predicts, which is precisely where a wrong model "
                  "does damage."),
        ],
        "lab": ("distribution", {
            "kind": "binomial",
            "panel_title": "Shape, mean and variance",
            "panel_intro": "Move `p` away from 1/2 and watch the distribution skew while "
                           "the variance falls. The summed expectation and the closed form "
                           "`np` are shown side by side.",
        }),
        "steps_title": "Applying the binomial",
        "steps_intro": "Check the three assumptions before using the formula.",
        "steps": [
            ("Confirm `n` is fixed in advance",
             "If the number of trials depends on the results, this is not a binomial "
             "&mdash; lesson 12 handles the commonest such case."),
            ("Confirm the trials are independent",
             "Sampling without replacement is the standard violation, and it matters when "
             "the sample is a substantial fraction of the population."),
            ("Confirm `p` is constant",
             "Same probability every trial. Drift breaks the model even when the trials "
             "are independent."),
            ("Then compute",
             "`C(n,k)p^k(1−p)^{n−k}` for a single `k`, or sum over a range for \"at "
             "least\" questions &mdash; often via the complement."),
        ],
        "worked": {
            "title": "A multiple-choice test",
            "intro": ["20 questions, 4 options each, answered at random. `n = 20`, `p = 1/4`."],
            "lines": [
                "E[X]   = 20 × 0.25 = 5",
                "Var(X) = 20 × 0.25 × 0.75 = 3.75,   σ ≈ 1.94",
                "",
                "P(exactly 5) = C(20,5)(0.25)⁵(0.75)¹⁵ ≈ 0.2023",
                "",
                "P(at least 10) = 1 − P(X ≤ 9)",
                "               ≈ 1 − 0.9861  =  0.0139",
                "",
                "So passing at 50% by guessing happens about once in 72 attempts.",
                "Note 10 is about 2.6σ above the mean; Chebyshev would only",
                "guarantee ≤ 1/2.6² ≈ 15%, and the true answer is 1.4%.",
            ],
            "after": [
                "The comparison with Chebyshev is worth noticing. The general bound is "
                "correct and roughly ten times too generous, which is the usual situation: "
                "distribution-free bounds are safe and loose, and knowing the distribution "
                "buys precision."
            ],
        },
        "quiz_title": "Binomial",
        "quiz": [
            {"q": "`n = 10`, `p = 0.3`. `E[X]` equals:",
             "a": ["3", "0.3", "10", "2.1"],
             "c": 0,
             "why": "`np = 10 × 0.3 = 3`, by linearity over ten indicators."},
            {"q": "The binomial requires all of the following EXCEPT:",
             "a": ["a fixed number of trials", "independent trials",
                   "constant success probability", "`p = 1/2`"],
             "c": 3,
             "why": "Any `p` in `[0,1]` is fine. The other three are the defining "
                    "assumptions."},
            {"q": "Drawing 5 cards from a deck and counting aces is:",
             "a": ["binomial with `p = 4/52`",
                   "not binomial — the draws are dependent",
                   "binomial with `p = 1/13`",
                   "geometric"],
             "c": 1,
             "why": "Without replacement the probability changes after each draw. The "
                    "correct distribution is hypergeometric."},
        ],
        "mistakes": [
            ("Using it for sampling without replacement",
             "The trials are dependent. When the sample is a small fraction of the "
             "population the error is small; when it is not, it is large."),
            ("Forgetting the binomial coefficient",
             "`p^k(1−p)^{n−k}` is the probability of ONE arrangement. `C(n,k)` counts them."),
            ("Assuming the mean is the likely value",
             "`P(X = np)` shrinks like `1/√n`. At `n = 100`, `p = 1/2`, the chance of "
             "exactly 50 heads is about 8%."),
        ],
        "standard": ("Finish when you check the three assumptions first.",
                     "For each of: coin flips, cards drawn without replacement, defects in "
                     "a production run, and rainy days in a week &mdash; say which of the "
                     "three assumptions hold and whether the binomial applies."),
        "note": "For large `n` the binomial is well approximated by the normal "
                "distribution, and for large `n` with small `np` by the Poisson. Both are "
                "continuous-probability topics; what matters here is that the exact "
                "formula is computable and the approximations exist because it becomes "
                "unwieldy.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "geometric-distribution",
        "title": "The Geometric Distribution and Waiting Times",
        "module": "Distributions",
        "one_line": "How long until the first success — and why the average misleads.",
        "summary": (
            "`P(X = k) = (1−p)^{k−1}p` for the trial of the first success. Its mean is "
            "`1/p`, its distribution is heavily skewed, and it is memoryless &mdash; "
            "which is the property people find hardest to accept."
        ),
        "key": [
            "P(X = k) = (1−p)^{k−1} p        first success on trial k",
            "E[X]   = 1/p",
            "Var(X) = (1−p)/p²",
            "MEMORYLESS:  P(X > m+n | X > m) = P(X > n)",
        ],
        "key_label": "Waiting for a success",
        "concepts_intro": (
            "The last distribution on this course, and the one whose mean is least "
            "representative of a typical outcome."
        ),
        "concepts": [
            ("The number of trials is not fixed",
             "That is what separates it from the binomial. The sample space is countably "
             "infinite, which is why the axioms had to be stated in general."),
            ("The mean is `1/p`, and it is not typical",
             "A 1-in-6 event takes 6 attempts on average, and yet the single most likely "
             "outcome is the very first attempt."),
            ("It is memoryless",
             "Having failed 20 times does not improve the next attempt. The distribution "
             "of the remaining wait is unchanged."),
        ],
        "read_title": "Waiting times",
        "read_intro": "The distribution, its mean, memorylessness, and the coupon collector.",
        "body": [
            ("thm", ("Geometric distribution",
                     "In independent trials with success probability `p &gt; 0`, let `X` be "
                     "the number of the trial on which the first success occurs. Then "
                     "`P(X = k) = (1−p)^{k−1}p` for `k = 1, 2, 3, …`")),
            ("proof", [
                "The first success on trial `k` means `k − 1` failures followed by a "
                "success. By independence that probability is `(1−p)^{k−1}p`.",
                "These sum to 1 by the geometric series of course 3 lesson 3: "
                "`Σ_{k≥1} (1−p)^{k−1}p = p/(1 − (1−p)) = 1`.",
            ]),
            ("thm", ("Mean and variance",
                     "`E[X] = 1/p` and `Var(X) = (1−p)/p²`.")),
            ("proof", [
                "Condition on the first trial. With probability `p` it succeeds and `X = 1`; "
                "with probability `1 − p` it fails and the remaining wait has the same "
                "distribution as `X`. So `E[X] = p·1 + (1−p)(1 + E[X])`.",
                "Expanding: `E[X] = 1 + (1−p)E[X]`, hence `pE[X] = 1` and `E[X] = 1/p`.",
            ]),
            ("p", "That conditioning argument is worth more than the formula. It avoids "
                  "summing an infinite series entirely, and the same trick handles many "
                  "waiting-time problems where no series is available."),
            ("thm", ("Memorylessness",
                     "`P(X &gt; m + n | X &gt; m) = P(X &gt; n)` for all `m, n ≥ 0`. The "
                     "geometric is the only discrete distribution with this property.")),
            ("proof", [
                "`P(X &gt; k) = (1−p)^k`, since it means the first `k` trials all failed. "
                "Then `P(X &gt; m+n | X &gt; m) = (1−p)^{m+n} / (1−p)^m = (1−p)^n = "
                "P(X &gt; n)`.",
            ]),
            ("p", "This is the gambler's fallacy stated correctly. A roulette wheel that "
                  "has come up red twenty times is exactly as likely to come up red next "
                  "spin; the past failures are already accounted for and change nothing. "
                  "The distribution has no memory because the trials are independent, and "
                  "independence is what the model assumed."),
            ("h3", "Why the mean misleads"),
            ("math", [
                "p = 1/6:   E[X] = 6",
                "",
                "   P(X = 1) = 0.167        the single most likely value",
                "   P(X ≤ 3) = 0.421",
                "   P(X ≤ 6) = 0.665        so 2/3 of the time you finish by the mean",
                "   P(X > 12) = 0.112       and 1 in 9 waits more than twice as long",
                "   P(X > 20) = 0.026",
            ]),
            ("p", "The distribution is strictly decreasing: the most likely single outcome "
                  "is always `k = 1`, whatever `p` is. \"On average 6\" describes a long "
                  "right tail balanced against a mode at 1, and quoting the mean alone "
                  "hides both facts."),
            ("h3", "The coupon collector"),
            ("thm", ("Collecting all `n` coupons",
                     "With `n` equally likely coupons, the expected number of purchases to "
                     "collect all of them is `n(1 + 1/2 + ⋯ + 1/n) ≈ n ln n + 0.577n`.")),
            ("proof", [
                "Split the process into stages: stage `i` runs while you hold exactly "
                "`i − 1` distinct coupons. The chance a purchase is new during that stage "
                "is `(n − i + 1)/n`, so the wait is geometric with that `p` and mean "
                "`n/(n − i + 1)`.",
                "By linearity of expectation the total is "
                "`Σ_{i=1}^{n} n/(n−i+1) = n Σ_{j=1}^{n} 1/j`.",
            ]),
            ("p", "For `n = 50` that is about 225 purchases, and the last coupon alone "
                  "accounts for 50 of them on average. The final stages dominate, which is "
                  "the structural reason collecting the last few of anything takes so long."),
        ],
        "lab": ("distribution", {
            "kind": "geometric",
            "panel_title": "The shape behind the mean",
            "panel_intro": "The bars fall from the very first value, whatever `p` is, while "
                           "the dashed mean line sits well to the right. That gap is the "
                           "whole caution of this lesson.",
        }),
        "steps_title": "Working with waiting times",
        "steps_intro": "Identify what is fixed: the trials, or the successes.",
        "steps": [
            ("Check whether `n` is fixed",
             "Fixed trials, count successes: binomial. Fixed target, count trials: "
             "geometric."),
            ("Use `E[X] = 1/p`",
             "And derive it by conditioning on the first trial if you want to check it. "
             "The series is unnecessary."),
            ("Report the spread as well as the mean",
             "The distribution is skewed enough that the mean alone misinforms. "
             "`P(X &gt; k) = (1−p)^k` is the clean way to describe the tail."),
            ("Decompose staged waits by linearity",
             "The coupon collector is a sum of geometric waits, and linearity handles it "
             "without any joint distribution."),
        ],
        "worked": {
            "title": "Rolling for a six",
            "intro": ["`p = 1/6`. How long until the first six?"],
            "lines": [
                "E[X] = 1/p = 6 rolls",
                "Var(X) = (1−p)/p² = (5/6)/(1/36) = 30,   σ ≈ 5.48",
                "",
                "P(X = 1)  = 1/6                    ≈ 0.1667   ← the most likely value",
                "P(X = 6)  = (5/6)⁵(1/6)            ≈ 0.0670",
                "P(X ≤ 6)  = 1 − (5/6)⁶             ≈ 0.6651",
                "P(X > 12) = (5/6)¹²                ≈ 0.1122",
                "",
                "The standard deviation (5.48) is nearly as large as the mean (6),",
                "which is a distribution nobody should summarise with one number.",
            ],
            "after": [
                "Two thirds of the time you finish within the mean, and one time in nine "
                "you wait more than twice it. Both facts follow from `P(X > k) = (5/6)^k`, "
                "which is a better summary of this distribution than its expectation."
            ],
        },
        "quiz_title": "Geometric",
        "quiz": [
            {"q": "`p = 0.2`. The expected number of trials until the first success is:",
             "a": ["0.2", "5", "0.8", "20"],
             "c": 1,
             "why": "`1/p = 1/0.2 = 5`."},
            {"q": "You have failed 20 times with `p = 0.1`. The probability the next trial succeeds is:",
             "a": ["higher than 0.1", "0.1", "lower than 0.1", "1"],
             "c": 1,
             "why": "Memorylessness. The trials are independent, so the past changes "
                    "nothing &mdash; and believing otherwise is the gambler's fallacy."},
            {"q": "For a geometric distribution the most likely single value is:",
             "a": ["`1/p`", "`k = 1`, always", "`p`", "it depends on `p`"],
             "c": 1,
             "why": "`P(X = k) = (1−p)^{k−1}p` is strictly decreasing in `k`, so the mode "
                    "is 1 for every `p` &mdash; however large the mean is."},
        ],
        "mistakes": [
            ("Confusing it with the binomial",
             "Fixed trials counting successes is binomial; fixed target counting trials is "
             "geometric. The question decides, not the setting."),
            ("Believing a long run of failures improves the odds",
             "Memorylessness says otherwise, and it is a theorem about the model rather "
             "than a claim about luck."),
            ("Reporting only the mean",
             "With `σ` nearly equal to the mean, a single number conceals both the mode at "
             "1 and the long tail."),
        ],
        "standard": ("Finish when you can derive `E[X] = 1/p` by conditioning.",
                     "Write the one-line argument: with probability `p` you finish "
                     "immediately, otherwise you have used one trial and face the same "
                     "problem. That technique solves waiting-time problems where no series "
                     "is available."),
        "note": "This course ends where several others begin. The geometric distribution "
                "is the discrete analogue of the exponential, memorylessness characterises "
                "both, and the coupon collector is the first example most people meet of a "
                "process whose expected time is dominated by its final stages.",
    },
]
