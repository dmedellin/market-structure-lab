"""Course 5, lessons 07-12 — rational graphs, then radicals end to end."""

LESSONS = [
    # ---------------------------------------------------------------- 07
    {
        "slug": "graphs-and-asymptotes",
        "title": "Graphs and Asymptotes",
        "module": "Rational functions",
        "one_line": "Asymptotes, holes, and what the degrees tell you.",
        "summary": (
            "Every feature of the graph is already written in the factored form. A "
            "factor that cancels gives a hole, a factor left in the denominator gives "
            "a vertical asymptote, and the two degrees give the end behaviour &mdash; "
            "three different readings of the same factorisation."
        ),
        "key": [
            "f(x) = (x − 3)(x + 2) / [(x − 3)(x + 1)]",
            "x = 3    factor cancels         HOLE at (3, 5/4)",
            "x = −1   denominator only       VERTICAL ASYMPTOTE",
            "deg top = deg bottom            y = 1   (leading coefficients)",
        ],
        "key_label": "One function, every feature",
        "concepts_intro": (
            "The graph is not sketched by plotting points. It is read off the factored "
            "form, and the reading takes three passes."
        ),
        "concepts": [
            ("Factor before you look at anything",
             "Vertical asymptotes, holes and zeros are all statements about factors. "
             "None of them can be seen in `(x² − x − 6)/(x² − 2x − 3)`, "
             "and all of them are obvious once it is factored."),
            ("A hole and an asymptote are different failures",
             "Both are values the domain never contained. At an asymptote the function "
             "runs off to infinity; at a hole it approaches an ordinary number and "
             "simply is not defined there. Cancelling the factor does not put the "
             "point back."),
            ("End behaviour is a comparison of degrees",
             "You do not need a limit to find the horizontal asymptote. For large "
             "`|x|` only the leading terms matter, so the answer depends on which "
             "degree is bigger and, in the tie, on the leading coefficients."),
        ],
        "read_title": "Reading a rational graph off its factors",
        "read_intro": "Four features, each one a different question asked of the same factorisation.",
        "body": [
            ("def", ("Rational function",
                     "A <strong>rational function</strong> is a quotient `f(x) = p(x)/q(x)` "
                     "of two polynomials with `q` not the zero polynomial. Its domain is "
                     "every real number except the zeros of `q` &mdash; and that is decided "
                     "by the ORIGINAL `q`, before any cancelling.")),
            ("p", "Lesson 1 established the domain rule and lesson 2 established that you "
                  "may cancel a common <em>factor</em>. Put them together and a question "
                  "appears: if `x = 3` was excluded and the factor `(x − 3)` then "
                  "cancels, what does the graph do at `x = 3`? It does something quite "
                  "specific, and it is not the same as what it does at a zero of the "
                  "denominator that survives."),
            ("def", ("Vertical asymptote",
                     "If, after cancelling every common factor, `(x − a)` still "
                     "divides the denominator and does not divide the numerator, the "
                     "line `x = a` is a <strong>vertical asymptote</strong>: as `x` "
                     "approaches `a` the values of `f` grow without bound in one "
                     "direction or the other.")),
            ("def", ("Hole",
                     "If `(x − a)` divides the numerator and the denominator to the "
                     "same multiplicity, so that it cancels completely, then `a` is still "
                     "outside the domain but the reduced function has an ordinary value "
                     "there. The graph is the graph of the reduced function with the "
                     "single point `(a, r(a))` removed &mdash; a <strong>hole</strong>.")),
            ("p", "The hole is the honest picture of what cancelling did. The reduced "
                  "expression `r(x)` agrees with `f(x)` at every point of `f`'s domain "
                  "and is defined at one point more. Two functions that differ at one "
                  "point are different functions, which is exactly why lesson 1 insisted "
                  "the excluded values be written down before the algebra started."),
            ("thm", ("Horizontal asymptotes by degree",
                     "Let `n` be the degree of the numerator and `m` the degree of the "
                     "denominator, with leading coefficients `a` and `b`.",
                     "If `n &lt; m`, the horizontal asymptote is `y = 0`. If `n = m`, it "
                     "is `y = a/b`. If `n &gt; m`, there is no horizontal asymptote.")),
            ("p", "The reason is a one-line calculation, not a rule to memorise. Divide "
                  "top and bottom by `x` raised to the larger degree; every term with a "
                  "power of `x` underneath goes to `0` for large `|x|`, and what survives "
                  "is the comparison above."),
            ("example", ("Three end behaviours",
                         "`(2x + 1)/(x² − 4)` has `1 &lt; 2`, so `y = 0`. "
                         "`(3x² + 1)/(x² − 4)` has a tie, so `y = 3/1 = 3`. "
                         "`(x² + 1)/(x − 1)` has `2 &gt; 1`, so no horizontal "
                         "asymptote at all.")),
            ("p", "In that last case long division writes the function as "
                  "`x + 1 + 2/(x − 1)`, and the graph approaches the line "
                  "`y = x + 1`. That is a slant asymptote. It is mentioned here because "
                  "the division makes it visible; this course does not pursue it, and "
                  "nothing later depends on it."),
            ("h3", "Zeros, and the one condition on them"),
            ("p", "A rational function is zero exactly where its numerator is zero AND "
                  "the point is in the domain. `x = 3` makes the numerator of our example "
                  "zero, but `3` was never in the domain, so it is a hole rather than a "
                  "zero. A fraction is zero when its top is zero and its bottom is not."),
        ],
        "lab": ("rationalfn", {
            "mode": "graph",
            "panel_title": "Factors in, features out",
            "panel_intro": "Change a factor and watch which feature moves. Every "
                           "asymptote, hole and intercept drawn here was computed from "
                           "the factored form in exact arithmetic, not read off the "
                           "picture.",
        }),
        "steps_title": "Reading a rational graph",
        "steps_intro": "Five passes over the factored form, in this order. The order is what keeps holes and asymptotes apart.",
        "steps": [
            ("Factor the numerator and the denominator completely",
             "Nothing below this line can be done to a sum. If the factoring is wrong "
             "every feature will be wrong, so this is the step to check twice."),
            ("Write the domain from the ORIGINAL denominator",
             "Every zero of the denominator you started with is excluded, whether or not "
             "its factor is about to cancel. This list cannot be recovered later."),
            ("Cancel common factors and record a hole for each",
             "A factor `(x − a)` that cancels gives a hole. Its height is the "
             "reduced function evaluated at `a` &mdash; substitute into what is LEFT, "
             "not into the original."),
            ("The surviving denominator zeros are the vertical asymptotes",
             "Each one is a line `x = a`. To see which way the graph goes, test a value "
             "just to each side; the sign of the reduced expression decides it."),
            ("Compare the degrees for the end behaviour",
             "Use the degrees of the ORIGINAL function &mdash; cancelling a common factor "
             "lowers both by the same amount, so the comparison is unchanged either way."),
        ],
        "worked": {
            "title": "Every feature of one function",
            "intro": [
                "Take `f(x) = (x² − x − 6)/(x² − 2x − 3)`. Nothing "
                "about the graph is visible in that form, and everything is visible two "
                "lines later.",
            ],
            "lines": [
                "f(x) = (x² − x − 6) / (x² − 2x − 3)",
                "",
                "1.  Factor       f(x) = (x − 3)(x + 2) / [(x − 3)(x + 1)]",
                "",
                "2.  Domain       x − 3 = 0  or  x + 1 = 0",
                "                 x ≠ 3  and  x ≠ −1          ← recorded BEFORE cancelling",
                "",
                "3.  Cancel       f(x) = (x + 2)/(x + 1),   with x ≠ 3 still attached",
                "",
                "4.  Hole         (x − 3) cancelled, so x = 3 is a hole",
                "                 height = (3 + 2)/(3 + 1) = 5/4",
                "                 open circle at (3, 5/4)",
                "",
                "5.  Asymptote    (x + 1) survives; at x = −1 the top is −1 + 2 = 1 ≠ 0",
                "                 vertical asymptote  x = −1",
                "",
                "6.  Zero         x + 2 = 0 → x = −2,  and −2 is in the domain    ✓",
                "",
                "7.  End          deg top = 2 = deg bottom,  leading coefficients 1 and 1",
                "                 horizontal asymptote  y = 1",
            ],
            "after": [
                "Both `3` and `−1` are outside the domain, and the graph treats them "
                "completely differently. Near `x = −1` the values run to `±∞`; near "
                "`x = 3` they approach `5/4` from both sides and the function is simply "
                "not defined at the single point.",
                "Note where the hole's height came from. Substituting `3` into the "
                "original gives `0/0`, which says nothing. The height is `(3 + 2)/(3 + 1)`, "
                "computed in the reduced expression &mdash; the one that agrees with `f` "
                "everywhere `f` exists.",
            ],
        },
        "quiz_title": "Asymptote or hole",
        "quiz": [
            {"q": "For `f(x) = (x² − 4)/(x² − 5x + 6)`, what happens at `x = 2`?",
             "a": ["A vertical asymptote", "A hole at `(2, −4)`",
                   "A zero of the function", "Nothing &mdash; `2` is an ordinary point"],
             "c": 1,
             "why": "It factors as `(x − 2)(x + 2)/[(x − 2)(x − 3)]`. The "
                    "factor `(x − 2)` cancels, so `x = 2` is a hole, and its height "
                    "is `(2 + 2)/(2 − 3) = −4`."},
            {"q": "Which gives the horizontal asymptote of `(3x² + 1)/(x² − 4)`?",
             "a": ["`y = 0`, because the denominator factors",
                   "`y = 3`, the ratio of the leading coefficients",
                   "There is none, because the degrees are equal",
                   "`y = 1/4`, from the constant terms"],
             "c": 1,
             "why": "Equal degrees means the leading terms dominate for large `|x|`, and "
                    "`3x²/x² = 3`. The constant terms have no effect on end behaviour."},
            {"q": "A rational function has a numerator zero at `x = 5`. Is `5` a zero of the function?",
             "a": ["Yes, always", "Only if `5` is also in the domain",
                   "No, numerator zeros are asymptotes",
                   "Only if the denominator is constant"],
             "c": 1,
             "why": "A fraction is zero when its top is zero and its bottom is not. If the "
                    "denominator also vanishes at `5`, the point is a hole or an asymptote "
                    "instead &mdash; never a zero."},
        ],
        "mistakes": [
            ("Taking the domain from the cancelled form",
             "Once `(x − 3)` is gone the expression looks perfectly happy at `x = 3`. "
             "The exclusion came from the original denominator and survives every legal "
             "simplification."),
            ("Substituting into the original to find a hole's height",
             "That gives `0/0`, which is not a number and not a height. Cancel first, then "
             "substitute into what remains."),
            ("Assuming the graph never crosses its horizontal asymptote",
             "A horizontal asymptote describes behaviour for large `|x|` only. A graph may "
             "cross it near the origin as often as it likes; the vertical asymptote is the "
             "one it can never touch."),
        ],
        "standard": ("Finish when you can produce every feature without plotting a single point.",
                     "Given a rational function you should be able to name the domain, "
                     "each hole with its height, each vertical asymptote, each zero and "
                     "the end behaviour &mdash; and say which line of the factorisation "
                     "each one came from. A sketch that is right by accident does not "
                     "transfer to the next function."),
        "note": "This is the last lesson on rational expressions. The pattern it leaves "
                "you with &mdash; write the domain down first, then simplify, and expect "
                "the simplified form to have forgotten something &mdash; is exactly the "
                "pattern the radical half of the course repeats from lesson 8, with "
                "squaring in place of cancelling.",
    },
    # ---------------------------------------------------------------- 08
    {
        "slug": "simplifying-radical-expressions",
        "title": "Simplifying Radical Expressions",
        "module": "Radicals",
        "one_line": "nth roots, the principal root, and why √(x²) is |x|.",
        "summary": (
            "The second half of the course opens the way the first did: with the values "
            "that are not allowed. An even root demands a non-negative radicand, the "
            "principal root is a single number rather than two, and both facts show up "
            "in the identity `√(x²) = |x|`."
        ),
        "key": [
            "√(a²) = |a|            not a",
            "ⁿ√a · ⁿ√b = ⁿ√(ab)     n even requires a ≥ 0 and b ≥ 0",
            "√200 = √(100 · 2) = 10√2",
            "n even → radicand ≥ 0;   n odd → any real",
        ],
        "key_label": "Four facts about roots",
        "concepts_intro": (
            "A radical sign is not an instruction to find every number that works. It "
            "names one specific number, and which one depends on whether the index is "
            "even or odd."
        ),
        "concepts": [
            ("The radical sign names the principal root",
             "`√9` is `3`, not `±3`. Both `3` and `−3` square to `9`, but the "
             "symbol denotes the non-negative one so that `√` is a function. The `±` in "
             "the quadratic formula is written explicitly because the symbol does not "
             "supply it."),
            ("Even and odd indices behave differently",
             "An even power is never negative, so `√(−4)` names nothing real and "
             "`−4` is outside the domain. An odd power keeps its sign, so `∛(−8)` "
             "is `−2` with no difficulty at all."),
            ("Simplifying means extracting perfect powers",
             "`√200` is not made simpler by a decimal. It is made simpler by writing "
             "`200 = 100 · 2` and taking the perfect square out, leaving `10√2` &mdash; an "
             "exact value in a form that can be compared and combined."),
        ],
        "read_title": "Roots, principal values and the product rule",
        "read_intro": "The definitions first, then the two rules that do the simplifying and the condition attached to them.",
        "body": [
            ("def", ("nth root",
                     "For an integer `n ≥ 2`, `b` is an <strong>nth root</strong> of `a` "
                     "if `bⁿ = a`. In `ⁿ√a` the number `n` is the <strong>index</strong> "
                     "and `a` is the <strong>radicand</strong>. With no index written, "
                     "the index is `2`.")),
            ("def", ("Principal root",
                     "When `n` is even and `a ≥ 0`, `ⁿ√a` denotes the <strong>non-negative</strong> "
                     "root. When `n` is odd, `ⁿ√a` denotes the unique real root, which has "
                     "the same sign as `a`. When `n` is even and `a &lt; 0`, `ⁿ√a` is not "
                     "a real number.")),
            ("p", "That last clause is the radical half's version of \"the denominator is "
                  "not zero\". It is a restriction on the domain, it is decided before any "
                  "algebra happens, and no manipulation later can be allowed to lose it. "
                  "`√(−4)` is treated here as undefined; course 6 introduces `i` and "
                  "gives it a value."),
            ("thm", ("The identity that catches everyone",
                     "For every real `x`, `√(x²) = |x|`.",
                     "The left side is non-negative by definition of the principal root, "
                     "so the right side must be too. Writing `√(x²) = x` asserts something "
                     "false for every negative `x`: at `x = −5` the left side is `5` "
                     "and the right side is `−5`.")),
            ("p", "More generally `ⁿ√(xⁿ)` is `|x|` when `n` is even and `x` when `n` is "
                  "odd. The absolute value is not decoration. It is the price of an even "
                  "power destroying sign information that the root then cannot restore."),
            ("thm", ("Product and quotient rules",
                     "`ⁿ√a · ⁿ√b = ⁿ√(ab)` and `ⁿ√a / ⁿ√b = ⁿ√(a/b)`, provided every "
                     "radical named is defined &mdash; for even `n` that means `a ≥ 0` and "
                     "`b ≥ 0`, and `b ≠ 0` in the quotient.",
                     "The condition is not fine print. Without it one could write "
                     "`√(−4) · √(−9) = √36 = 6`, and the left side is not a real "
                     "number at all.")),
            ("p", "Notice what is absent: there is no rule for `ⁿ√(a + b)`. Roots "
                  "distribute over multiplication and division and over nothing else. "
                  "`√(9 + 16)` is `√25 = 5`, while `√9 + √16` is `7`. This is the same "
                  "shape of error as cancelling a term rather than a factor in lesson 2."),
            ("h3", "Simplified form"),
            ("ul", [
                "<strong>No perfect nth power left under the radical.</strong> `√72` "
                "becomes `6√2` because `72 = 36 · 2`.",
                "<strong>No fraction under the radical</strong> and no radical in a "
                "denominator &mdash; lesson 10 handles the second half of that.",
                "<strong>The index as small as it will go.</strong> `⁴√(9)` is `√3`, "
                "since `9 = 3²`.",
            ]),
            ("example", ("Variables under an even root",
                         "`√(50x³)` simplifies to `5x√(2x)`. No absolute value is needed: "
                         "for the expression to be defined at all, `50x³ ≥ 0` forces "
                         "`x ≥ 0`, and a non-negative `x` is its own absolute value. The "
                         "domain did the work that `| |` would otherwise have to do.")),
        ],
        "lab": ("radicals", {
            "mode": "reduce",
            "panel_title": "Pulling out perfect powers",
            "panel_intro": "The factorisation of the radicand is shown as it is found, so "
                           "you can see which factor came out and which one had to stay. "
                           "The decimal is printed only as a check on the exact form.",
        }),
        "steps_title": "Simplifying a radical",
        "steps_intro": "Four steps. The first decides whether there is anything to do at all.",
        "steps": [
            ("Check the index and the sign of the radicand",
             "Even index with a negative radicand: stop, it is undefined here. Odd index: "
             "any real number is fine, and a negative sign may be brought out front."),
            ("Factor the radicand into perfect nth powers times the rest",
             "For a square root look for the largest perfect square that divides it; "
             "`200 = 100 · 2` in one step beats `200 = 4 · 50` in three."),
            ("Take each perfect power out, one factor at a time",
             "`ⁿ√(cⁿ · d) = c · ⁿ√d` by the product rule. For an even index with a "
             "variable base, this is where `|x|` appears unless the domain already "
             "forces the base non-negative."),
            ("Confirm nothing extractable is left",
             "Look at what remains under the radical: if any factor is still a perfect "
             "nth power, or the index and every exponent share a common factor, there "
             "is another step to take."),
        ],
        "worked": {
            "title": "Three radicals, three different obstacles",
            "intro": [
                "One numeric square root, one odd index with a negative radicand, and one "
                "with variables.",
            ],
            "lines": [
                "(a)  √200",
                "     200 = 100 · 2,  and 100 = 10²",
                "     √200 = √100 · √2 = 10√2                 check: 10 × 1.41421… = 14.1421…",
                "",
                "(b)  ∛(−108)",
                "     index 3 is odd, so a negative radicand is fine",
                "     −108 = (−27) · 4,  and −27 = (−3)³",
                "     ∛(−108) = ∛(−27) · ∛4 = −3∛4            check: −3 × 1.5874… = −4.7622…",
                "",
                "(c)  √(48x⁵y⁴)          defined only where 48x⁵y⁴ ≥ 0, so x ≥ 0",
                "     48x⁵y⁴ = (16x⁴y⁴) · (3x)",
                "     √(48x⁵y⁴) = 4x²y²√(3x)",
                "",
                "     no absolute values needed:  x², y² ≥ 0 always;  x ≥ 0 only keeps √(3x) defined",
            ],
            "after": [
                "In (b) the sign came out with the root because the index is odd. Had the "
                "index been even, there would have been nothing to do &mdash; the "
                "expression would not name a real number and the work would stop at the "
                "first line.",
                "In (c) the domain restriction was written down before the simplifying, "
                "exactly as in lesson 1, and it is what makes `√(3x)` defined at all. It "
                "is not what removes the absolute value bars: `√(x⁴) = x²` and "
                "`√(y⁴) = y²` hold for every real `x` and `y`, because an even power "
                "is already non-negative. The bars are genuinely at stake in the earlier "
                "`√(50x³) = 5x√(2x)`, where the extracted factor is `x` to the first "
                "power and `√(x²) = |x|` needs `x ≥ 0` before it can be dropped.",
            ],
        },
        "quiz_title": "Roots and their conditions",
        "quiz": [
            {"q": "What is `√(x²)` for every real `x`?",
             "a": ["`x`", "`±x`", "`|x|`", "`x²`"],
             "c": 2,
             "why": "The principal square root is never negative, so at `x = −5` the "
                    "value is `5`. Only `|x|` is correct for every real `x`."},
            {"q": "Which of these is not a real number?",
             "a": ["`∛(−8)`", "`√(−16)`", "`−√16`", "`∛(−1)`"],
             "c": 1,
             "why": "An even index needs a non-negative radicand. `−√16` is fine &mdash; "
                    "it is `−4`, the negative of a perfectly good root &mdash; and odd "
                    "indices accept negatives."},
            {"q": "`√72` in simplified form is:",
             "a": ["`8√1`", "`2√18`", "`6√2`", "`36√2`"],
             "c": 2,
             "why": "`72 = 36 · 2` with `36` a perfect square, giving `6√2`. `2√18` is "
                    "equal in value but not simplified: `18` still contains the perfect "
                    "square `9`."},
            {"q": "Why does the product rule `√a · √b = √(ab)` carry the condition `a, b ≥ 0`?",
             "a": ["Because otherwise the product is irrational",
                   "Because for negative radicands the left side is not a real number",
                   "Because the rule only holds for square roots",
                   "Because `ab` might not be a perfect square"],
             "c": 1,
             "why": "With `a = −4` and `b = −9` the right side is `√36 = 6` while "
                    "the left side names nothing real. The condition keeps both sides "
                    "defined before it claims they are equal."},
        ],
        "mistakes": [
            ("Writing `√(x²) = x`",
             "True only for `x ≥ 0`. It is the same class of error as cancelling without "
             "recording the domain: a step that gives the right answer on the examples "
             "you tried is not thereby a valid rule."),
            ("Distributing a root over a sum",
             "`√(a + b)` is not `√a + √b`. Test it once with `9` and `16` and the habit "
             "dies: `5` against `7`."),
            ("Reading `√9` as `±3`",
             "The symbol names one number. The two solutions of `x² = 9` come from the "
             "square root property, which supplies the `±` explicitly &mdash; the radical "
             "sign never does."),
        ],
        "standard": ("Finish when you can state the condition alongside every rule you use.",
                     "Given any radical you should be able to say whether it is defined, "
                     "simplify it exactly, and justify each extraction by the product or "
                     "quotient rule with its hypothesis checked. Knowing that `√200 = 10√2` "
                     "matters less than knowing why `√(−4) · √(−9)` is not `6`."),
        "note": "Everything in the next four lessons rests on this one. Adding radicals "
                "needs simplified form to see which are alike, rationalizing needs the "
                "product rule, and radical equations need the domain restriction that "
                "the even index imposes here.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "operations-with-radicals",
        "title": "Adding, Subtracting and Multiplying Radicals",
        "module": "Radicals",
        "one_line": "Like radicals combine; unlike radicals simply do not.",
        "summary": (
            "Addition of radicals is the collecting of like terms wearing a disguise: "
            "only radicals with the same index and the same radicand may be combined, "
            "and you cannot tell which those are until everything is simplified. "
            "Multiplication is friendlier, and the conjugate pair is the case worth "
            "memorising."
        ),
        "key": [
            "√8 + √18 = 2√2 + 3√2 = 5√2         simplify FIRST, then combine",
            "√2 + √3 ≠ √5",
            "(2 + √3)(2 − √3) = 4 − 3 = 1        conjugates: the root disappears",
            "(√5 + √2)² = 7 + 2√10               the middle term does not",
        ],
        "key_label": "What combines and what does not",
        "concepts_intro": (
            "Three rules govern the arithmetic, and two of them are rules about when "
            "you are NOT allowed to do the obvious thing."
        ),
        "concepts": [
            ("Like radicals are like terms",
             "`3√2 + 5√2 = 8√2` for the same reason `3k + 5k = 8k`. The radical is "
             "just a number you have not evaluated, and the distributive law does the "
             "work: `3√2 + 5√2 = (3 + 5)√2`."),
            ("Simplify before deciding what is alike",
             "`√8` and `√18` look unrelated and are both multiples of `√2`. Any judgement "
             "about which radicals combine, made before simplifying, is a guess."),
            ("Multiplication has no such restriction",
             "`√2 · √3 = √6` needs nothing to match, only the product rule and "
             "non-negative radicands. Sums are the difficult direction, which is why "
             "the conjugate trick &mdash; turning a sum into a product &mdash; is worth "
             "so much in lesson 10."),
        ],
        "read_title": "Combining radicals, and the two ways it goes wrong",
        "read_intro": "Addition first, because it is the one with a condition; then multiplication and the two special products.",
        "body": [
            ("def", ("Like radicals",
                     "Two radicals are <strong>like</strong> if they have the same index "
                     "and the same radicand: `3√2` and `−7√2` are like, `√2` and "
                     "`√3` are not, and `√2` and `∛2` are not.")),
            ("thm", ("Adding like radicals",
                     "`a·ⁿ√c + b·ⁿ√c = (a + b)·ⁿ√c`.",
                     "This is the distributive law with `ⁿ√c` in the role of a common "
                     "factor. There is no corresponding rule for unlike radicals, because "
                     "there is no common factor to take out.")),
            ("p", "So `√2 + √3` is already in simplest form. It cannot be written as a "
                  "single radical, and in particular it is not `√5`: numerically "
                  "`√2 + √3 ≈ 3.1463` while `√5 ≈ 2.2361`. An expression being unfinished "
                  "to the eye does not mean there is a step left."),
            ("example", ("Alike after simplifying",
                         "`√8 + √18` looks like two unlike radicals. Simplify: "
                         "`√8 = 2√2` and `√18 = 3√2`, so the sum is `5√2`. The same "
                         "expression, one line later, is a single term.")),
            ("h3", "Multiplying"),
            ("p", "The product rule handles it: multiply the outside parts, multiply the "
                  "radicands, then simplify what results. `3√2 · 4√6 = 12√12`, and `√12` "
                  "is not simplified &mdash; `12 = 4 · 3`, so `12√12 = 12 · 2√3 = 24√3`. "
                  "The last simplification is the step most often skipped."),
            ("p", "With sums, distribute exactly as with polynomials. Nothing new happens; "
                  "the terms are simply irrational."),
            ("thm", ("The conjugate product",
                     "`(a + √b)(a − √b) = a² − b`, and more generally "
                     "`(√a + √b)(√a − √b) = a − b` for `a, b ≥ 0`.",
                     "It is the difference of two squares from course 4, and squaring is "
                     "exactly what removes a square root. The result contains no radical "
                     "at all &mdash; which is the whole reason lesson 10 works.")),
            ("example", ("Two products, one with a middle term and one without",
                         "`(2 + √3)(2 − √3) = 4 − 3 = 1`: the cross terms "
                         "`−2√3` and `+2√3` cancel. But `(√5 + √2)² = 5 + 2√10 + 2 = "
                         "7 + 2√10`: here the cross terms are equal and ADD. Squaring a "
                         "binomial never loses its middle term.")),
            ("p", "That contrast is worth holding on to. `(a + b)² = a² + b²` is false for "
                  "numbers and stays false for radicals, and lesson 11 turns on it: "
                  "squaring `√x + 1` gives `x + 2√x + 1`, so squaring an equation with two "
                  "terms on a side does not remove the root."),
        ],
        "lab": ("radicals", {
            "mode": "operate",
            "panel_title": "Combine, or explain why not",
            "panel_intro": "Each term is simplified first and the like radicals are "
                           "grouped in front of you. When two terms will not combine, the "
                           "lab says which condition fails rather than leaving the "
                           "expression alone.",
        }),
        "steps_title": "Working an expression with several radicals",
        "steps_intro": "Simplification comes first in every case. Until it is done you cannot see what you have.",
        "steps": [
            ("Simplify every radical in the expression",
             "Extract perfect powers, reduce indices, and clear fractions from under the "
             "signs. Only now is it visible which radicals are alike."),
            ("Group the like radicals and add their coefficients",
             "Same index and same radicand. Treat each distinct radical the way you would "
             "treat a distinct variable when collecting like terms."),
            ("For products, distribute and use the product rule",
             "Multiply coefficients together and radicands together. FOIL applies "
             "unchanged to two binomials; a conjugate pair is the case where the middle "
             "terms cancel."),
            ("Simplify the result, then stop",
             "A product often produces a new radicand with a perfect power in it. Leave "
             "unlike radicals side by side &mdash; an answer such as `7 + 2√10` is finished."),
        ],
        "worked": {
            "title": "Four expressions worth the practice",
            "intro": ["Two sums and two products. Watch which step is doing the work."],
            "lines": [
                "(a)  √8 + √18",
                "     = 2√2 + 3√2                     both simplify to multiples of √2",
                "     = 5√2                           check: 2.8284… + 4.2426… = 7.0710…",
                "",
                "(b)  √50 − √18",
                "     = 5√2 − 3√2  =  2√2             check: 7.0710… − 4.2426… = 2.8284…",
                "",
                "(c)  3√2 · 4√6",
                "     = 12√12                         multiply outsides, multiply radicands",
                "     = 12 · 2√3  =  24√3             12 = 4 · 3, so √12 = 2√3",
                "                                     check: 41.5692… both ways",
                "",
                "(d)  (√5 + √2)²",
                "     = (√5)² + 2·√5·√2 + (√2)²       square of a binomial, middle term kept",
                "     = 5 + 2√10 + 2",
                "     = 7 + 2√10                      check: 13.3245… both ways",
            ],
            "after": [
                "In (c) the answer `12√12` is correct and unfinished. A radical answer is "
                "not simplified until nothing extractable remains under the sign, and "
                "`√12` still hides a `4`.",
                "Compare (d) with `(2 + √3)(2 − √3) = 1`. Same shape of expression, "
                "opposite outcome: with a conjugate the middle terms cancel and the root "
                "vanishes, with a square they reinforce and the root survives. Lesson 10 "
                "uses the first; lesson 11 is made difficult by the second.",
            ],
        },
        "quiz_title": "Combine or leave",
        "quiz": [
            {"q": "`√2 + √3` equals:",
             "a": ["`√5`", "`√6`", "`2√5`", "It cannot be combined"],
             "c": 3,
             "why": "The radicands differ, so the radicals are not alike and there is no "
                    "common factor to take out. Numerically `√2 + √3 ≈ 3.146`, while "
                    "`√5 ≈ 2.236`."},
            {"q": "`√50 − √18` equals:",
             "a": ["`√32`", "`2√2`", "`8√2`", "`√68`"],
             "c": 1,
             "why": "Simplify first: `5√2 − 3√2 = 2√2`. Subtracting radicands "
                    "(`50 − 18 = 32`) is not a legal step and gives `√32 = 4√2`, a "
                    "different number."},
            {"q": "`(3 + √5)(3 − √5)` equals:",
             "a": ["`9 + 5`", "`4`", "`9 − 5√5`", "`14 − 6√5`"],
             "c": 1,
             "why": "A conjugate pair: `a² − b = 9 − 5 = 4`. The cross terms "
                    "`−3√5` and `+3√5` cancel, which is what leaves no radical."},
            {"q": "`(1 + √3)²` equals:",
             "a": ["`1 + 3 = 4`", "`4 + 2√3`", "`1 + 2√3`", "`4 − 2√3`"],
             "c": 1,
             "why": "`1 + 2√3 + 3 = 4 + 2√3`. Squaring a binomial keeps its middle term "
                    "&mdash; the error of dropping it is the same one that makes "
                    "`(a + b)² = a² + b²` false."},
        ],
        "mistakes": [
            ("Adding the radicands",
             "`√50 − √18` is not `√32`. Radicals add like terms, not like numbers "
             "inside a box; simplify each one and combine the coefficients."),
            ("Judging likeness before simplifying",
             "`√8` and `√18` are alike and do not look it. Every decision about combining "
             "belongs after the simplification step, never before."),
            ("Losing the middle term when squaring",
             "`(√5 + √2)²` is `7 + 2√10`, not `7`. The cross terms cancel only for a "
             "conjugate PAIR, where the signs differ."),
        ],
        "standard": ("Finish when you can say, for any two radical terms, whether they "
                     "combine and why.",
                     "Given an expression mixing sums and products you should be able to "
                     "simplify every term, combine exactly the like ones, and leave the "
                     "rest alone without discomfort. `7 + 2√10` is a finished answer, and "
                     "treating it as unfinished is what produces an invented step."),
        "note": "The conjugate product proved here is used immediately. Lesson 10 needs a "
                "multiplier that clears a two-term radical denominator, and the "
                "difference of squares is the only thing that does it in one step.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "rationalizing-denominators",
        "title": "Rationalizing Denominators",
        "module": "Radicals",
        "one_line": "Multiply by 1, chosen so the root leaves the bottom.",
        "summary": (
            "A radical in a denominator is removed by multiplying the fraction by a "
            "carefully chosen form of `1`. For one term the multiplier is the radical "
            "itself; for two terms it is the conjugate, and the difference of squares "
            "does the rest. The value never changes &mdash; that is what makes the move "
            "legal."
        ),
        "key": [
            "3/√7 = 3√7 / 7                        multiply by √7/√7",
            "1/∛2 = ∛4 / 2                         needs ∛4, not ∛2",
            "6/(√5 − √2) = 6(√5 + √2)/3 = 2(√5 + √2)",
            "conjugate of a + √b is a − √b",
        ],
        "key_label": "One multiplier per shape of denominator",
        "concepts_intro": (
            "The technique is one idea used three ways, and the idea is that multiplying "
            "by `1` is always allowed."
        ),
        "concepts": [
            ("Multiplying by a form of 1 changes the form, not the value",
             "`√7/√7` is `1`, so `(3/√7)·(√7/√7)` is the same number as `3/√7`. This is "
             "the same licence used to build a common denominator in lesson 4; nothing "
             "is being added to or removed from the expression."),
            ("Choose the multiplier to complete a perfect power",
             "For `√7` you need one more `√7` to make `7`. For `∛2` you need `∛4`, "
             "because `∛2 · ∛4 = ∛8 = 2`. The question is always: what does this "
             "radicand need in order to become an exact nth power?"),
            ("Two terms need the conjugate",
             "Multiplying `√5 − √2` by itself makes things worse. Multiplying by "
             "`√5 + √2` gives `5 − 2 = 3` by the difference of squares, and the "
             "denominator is rational in one step."),
        ],
        "read_title": "Clearing a radical from a denominator",
        "read_intro": "Three shapes of denominator: one square root, one higher-index root, and a two-term sum.",
        "body": [
            ("p", "Why bother? Two reasons, and neither is that the unrationalized form "
                  "is wrong. `3/√7` is a perfectly good number. But `3√7/7` is easier to "
                  "estimate by hand, and &mdash; the reason that survives &mdash; a single "
                  "agreed form lets two answers be compared. Three students with "
                  "`3/√7`, `3√7/7` and `(3/7)√7` have written the same number three ways."),
            ("def", ("Rationalizing the denominator",
                     "To <strong>rationalize</strong> a denominator is to rewrite the "
                     "fraction as an equal fraction whose denominator contains no "
                     "radical.")),
            ("h3", "One square root in the denominator"),
            ("p", "Multiply top and bottom by that radical. `3/√7 = (3·√7)/(√7·√7) = 3√7/7`, "
                  "since `√7 · √7 = 7`. The radical did not disappear &mdash; it moved to "
                  "the numerator, where the convention allows it."),
            ("h3", "A higher index"),
            ("p", "Here the reflex fails. For `1/∛2`, multiplying by `∛2/∛2` gives "
                  "`∛2/∛4`, which is no better. You need the denominator to become a "
                  "perfect CUBE, so multiply by `∛4/∛4`: `1/∛2 = ∛4/∛8 = ∛4/2`. Ask what "
                  "the radicand is missing, not what it already is."),
            ("thm", ("Two terms: multiply by the conjugate",
                     "For a denominator `a + √b`, multiply top and bottom by `a − √b`; "
                     "the new denominator is `a² − b`, which contains no radical.",
                     "For `√a + √b` the conjugate is `√a − √b` and the new "
                     "denominator is `a − b`. Both are the difference of two squares, "
                     "and squaring is what defeats a square root.")),
            ("example", ("A conjugate in full",
                         "`6/(√5 − √2)`. Multiply above and below by `√5 + √2`. The "
                         "denominator becomes `(√5)² − (√2)² = 5 − 2 = 3`, and "
                         "the fraction becomes `6(√5 + √2)/3 = 2(√5 + √2)`. Both sides "
                         "evaluate to `7.3006…`.")),
            ("p", "The conjugate multiplier is never zero for a denominator that was "
                  "legal to begin with, so no value is being smuggled into or out of the "
                  "domain. That matters: unlike the next lesson's squaring, rationalizing "
                  "is fully reversible, and it can neither create a solution nor destroy "
                  "one. It is a change of clothes."),
            ("p", "One warning about signs. The conjugate of `√5 − √2` is "
                  "`√5 + √2`, and the conjugate of `3 − √2` is `3 + √2`. Only the "
                  "sign BETWEEN the terms flips; flipping the sign of the whole "
                  "expression instead gives `−(√5 − √2)`, whose product with "
                  "the original is `−(5 − 2√10 + 2)`, still full of radicals."),
        ],
        "lab": ("radicals", {
            "mode": "rationalize",
            "panel_title": "The multiplier, and why that one",
            "panel_intro": "The lab shows the form of `1` it chose and the product it "
                           "produces in the denominator. Both the original and the "
                           "rationalized fraction are evaluated, so you can see the value "
                           "has not moved.",
        }),
        "steps_title": "Rationalizing a denominator",
        "steps_intro": "Identify the shape of the denominator first; the shape names the multiplier.",
        "steps": [
            ("Simplify the fraction as it stands",
             "Extract perfect powers and reduce the fraction first. Rationalizing a "
             "denominator that was about to simplify anyway creates work and larger "
             "numbers."),
            ("Read the shape of the denominator",
             "One radical term, or two terms with a radical? A single `ⁿ√` takes the "
             "completing multiplier; a two-term denominator takes the conjugate."),
            ("Multiply top and bottom by the chosen form of 1",
             "For `ⁿ√(cᵏ)` multiply by `ⁿ√(cⁿ⁻ᵏ)` so the exponents sum to `n`. For "
             "`a ± √b` multiply by `a ∓ √b`, changing only the sign between the terms."),
            ("Expand, simplify, and reduce the fraction",
             "The denominator should now be rational; expand the numerator fully and "
             "cancel any common factor. `6(√5 + √2)/3` is not finished until it is "
             "`2(√5 + √2)`."),
        ],
        "worked": {
            "title": "Three denominators, three multipliers",
            "intro": ["A square root, a cube root, and a conjugate pair."],
            "lines": [
                "(a)  3/√7",
                "     multiply by √7/√7          because √7 · √7 = 7",
                "     = 3√7 / 7                  check: 1.13389… both ways",
                "",
                "(b)  1/∛2",
                "     multiply by ∛4/∛4          because ∛2 · ∛4 = ∛8 = 2   (NOT ∛2/∛2)",
                "     = ∛4 / 2                   check: 0.79370… both ways",
                "",
                "(c)  6/(√5 − √2)",
                "     conjugate is √5 + √2       flip only the middle sign",
                "     denominator: (√5 − √2)(√5 + √2) = 5 − 2 = 3",
                "     = 6(√5 + √2)/3",
                "     = 2(√5 + √2)               check: 7.30056… both ways",
            ],
            "after": [
                "Step (b) is the one that separates the technique from the reflex. "
                "Multiplying by `∛2/∛2` is a legal move that accomplishes nothing; the "
                "denominator must be completed to `∛(2³)`, so the missing factor is `∛4`.",
                "In (c) the final cancellation matters. `6(√5 + √2)/3` and `2(√5 + √2)` "
                "are the same number, but only the second is in simplified form, and the "
                "`3` in the denominator came from the conjugate product rather than from "
                "anything in the original fraction.",
            ],
        },
        "quiz_title": "Choosing the multiplier",
        "quiz": [
            {"q": "To rationalize `5/√3`, multiply top and bottom by:",
             "a": ["`3`", "`√3`", "`√5`", "`√15`"],
             "c": 1,
             "why": "`√3 · √3 = 3`, giving `5√3/3`. Multiplying by `3` leaves `15/(3√3)`, "
                    "which still has a radical below; so does multiplying by `√15`, the "
                    "root of numerator times radicand, which leaves `5√15/(3√5)`."},
            {"q": "To rationalize `1/∛5`, multiply top and bottom by:",
             "a": ["`∛5`", "`∛25`", "`5`", "`√5`"],
             "c": 1,
             "why": "The denominator must become a perfect cube: `∛5 · ∛25 = ∛125 = 5`. "
                    "Multiplying by `∛5` only gives `∛25` underneath, which is no "
                    "improvement."},
            {"q": "The conjugate of `4 − √7` is:",
             "a": ["`−4 + √7`", "`4 + √7`", "`−4 − √7`", "`4 − √7`"],
             "c": 1,
             "why": "Only the sign between the terms changes. The product is then "
                    "`16 − 7 = 9`, with no radical left. `4 − √7` is the expression "
                    "itself, and multiplying by that gives `23 − 8√7`, a denominator with "
                    "more radical in it than before."},
            {"q": "Rationalizing a denominator can change the solution set of an equation:",
             "a": ["True &mdash; it can introduce extraneous roots",
                   "False &mdash; it multiplies by `1`, so the value is unchanged",
                   "True &mdash; it changes the domain",
                   "Only when the denominator is a conjugate"],
             "c": 1,
             "why": "The multiplier is a non-zero form of `1`, so the expression's value "
                    "and domain are untouched and the step is reversible. The move that "
                    "does create extraneous roots is squaring, in the next lesson."},
        ],
        "mistakes": [
            ("Multiplying a cube root denominator by itself",
             "`∛2 · ∛2 = ∛4`, not `2`. Ask what power the radicand is short of, then "
             "supply exactly that."),
            ("Negating the whole denominator instead of one sign",
             "The conjugate of `√5 − √2` is `√5 + √2`. Writing `−√5 + √2` "
             "changes the sign of both terms and rationalizes nothing."),
            ("Multiplying only the denominator",
             "Multiplying the bottom alone by `√7` changes the number. The multiplier "
             "must be applied to top and bottom, because only then is it `1`."),
        ],
        "standard": ("Finish when the shape of the denominator tells you the multiplier "
                     "immediately.",
                     "Given any of the three shapes you should be able to name the form "
                     "of `1` before doing any arithmetic, and say what the denominator "
                     "will become. You should also be able to say why this step, unlike "
                     "the next lesson's, can never affect a solution set."),
        "note": "Rationalizing is the last technique in this course that is a pure "
                "rewriting &mdash; guaranteed to preserve value and domain. Lesson 11 "
                "uses a step that preserves neither, and the contrast is the point of "
                "meeting them in this order.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "solving-radical-equations",
        "title": "Solving Radical Equations",
        "module": "Radicals",
        "one_line": "Raise both sides, solve, then check every candidate.",
        "summary": (
            "Isolate the radical and raise both sides to the index. The step is legal "
            "and it is not reversible, so it can produce numbers that solve the new "
            "equation and not the original. The check is not proofreading &mdash; it is "
            "the final step of the method."
        ),
        "key": [
            "√(x + 7) = x − 5",
            "x + 7 = x² − 10x + 25          squaring: legal, NOT reversible",
            "x² − 11x + 18 = 0  →  x = 2  or  x = 9",
            "x = 9 checks;   x = 2 is EXTRANEOUS",
        ],
        "key_label": "Two candidates, one solution",
        "concepts_intro": (
            "One implication runs forwards and not backwards, and every difficulty in "
            "this lesson follows from that."
        ),
        "concepts": [
            ("Squaring is a one-way implication",
             "If `a = b` then `a² = b²` &mdash; always. The converse fails: `a² = b²` "
             "allows `a = −b`. So every solution of the original survives the "
             "squaring, but the squared equation may have picked up solutions of "
             "`a = −b` as well."),
            ("The extraneous root is not a mistake",
             "It is the correct consequence of a legal step. No amount of care in the "
             "algebra prevents it, which is why the method has a checking step built in "
             "rather than a warning attached."),
            ("Check against the ORIGINAL equation",
             "Substituting into a line partway down verifies your arithmetic from that "
             "line onwards, and that is not what is at issue. Only the original "
             "distinguishes a solution from an artefact of squaring."),
        ],
        "read_title": "Solving equations that contain a radical",
        "read_intro": "The method, the reason it needs a check, and the case of two radicals.",
        "body": [
            ("p", "Lesson 6 met extraneous solutions when clearing denominators: "
                  "multiplying by an expression that could be zero can create a root. "
                  "This lesson meets them again from a different direction, and the cure "
                  "is identical &mdash; substitute into the original."),
            ("def", ("Radical equation",
                     "A <strong>radical equation</strong> is one in which the variable "
                     "appears under a radical sign. `√(x + 7) = x − 5` is one; "
                     "`√7 · x = 5` is not, since the variable is outside.")),
            ("thm", ("Raising both sides to a power",
                     "If `a = b` then `aⁿ = bⁿ` for every positive integer `n`. The "
                     "converse holds for odd `n`, and fails for even `n`.",
                     "For even `n`, `aⁿ = bⁿ` gives `a = ±b`. Squaring an equation "
                     "therefore solves `a = b` and `a = −b` at once, and the two "
                     "solution sets come back mixed together.")),
            ("p", "Follow the key example. `√(x + 7) = x − 5` squares to "
                  "`x + 7 = x² − 10x + 25`, which rearranges to "
                  "`x² − 11x + 18 = 0` and factors as `(x − 2)(x − 9) = 0`. "
                  "The candidates are `2` and `9`."),
            ("p", "At `x = 9`: the left side is `√16 = 4` and the right side is `4`. It "
                  "solves the equation. At `x = 2`: the left side is `√9 = 3` and the "
                  "right side is `−3`. It does not &mdash; but it does solve "
                  "`√(x + 7) = −(x − 5)`, which is the other equation squaring "
                  "silently included."),
            ("example", ("Seen without any algebra",
                         "`√(x + 1) = −3` has no solution, and no work is needed to "
                         "say so: a principal square root is never negative. Squaring it "
                         "produces `x + 1 = 9` and the confident answer `x = 8`, which is "
                         "entirely extraneous. The equation was unsolvable before the "
                         "first step.")),
            ("h3", "Two radicals"),
            ("p", "Isolate one radical on its own side before squaring, even if another "
                  "remains. Squaring a side with two terms is where lesson 9's middle "
                  "term returns: `(1 + √x)² = 1 + 2√x + x` still contains a root, so "
                  "nothing has been gained."),
            ("p", "For `√(x + 5) − √x = 1`, move `√x` across to get "
                  "`√(x + 5) = 1 + √x`. Squaring gives `x + 5 = 1 + 2√x + x`, so "
                  "`4 = 2√x` and `√x = 2`, hence `x = 4`. Check in the original: "
                  "`√9 − √4 = 3 − 2 = 1` ✓. Two squarings, one surviving "
                  "solution."),
            ("p", "For an odd index there is no extraneous-root problem, because cubing "
                  "is reversible: `a³ = b³` forces `a = b` for real numbers. The check is "
                  "still worth doing as arithmetic insurance, but it is no longer part of "
                  "the logic of the method."),
        ],
        "lab": ("radicals", {
            "mode": "solve",
            "panel_title": "Every candidate, substituted",
            "panel_intro": "The lab solves the squared equation and then substitutes each "
                           "candidate back into the ORIGINAL, showing both sides. An "
                           "extraneous root is displayed failing that check rather than "
                           "quietly dropped.",
        }),
        "steps_title": "Solving a radical equation",
        "steps_intro": "Five steps, and the last one is not optional.",
        "steps": [
            ("Isolate one radical on one side",
             "Get a single radical alone before raising anything to a power. If two "
             "radicals are present, isolate the more complicated one first."),
            ("Raise both sides to the index",
             "Square for a square root, cube for a cube root. Square the whole side, not "
             "term by term: `(x − 5)²` is `x² − 10x + 25`."),
            ("Repeat if a radical remains",
             "Isolate and raise again. Each pass removes one radical, and a second "
             "squaring does not add a second layer of extraneous risk beyond what the "
             "final check handles."),
            ("Solve the resulting equation",
             "It is usually linear or quadratic, and the factoring from course 4 "
             "handles it. These are candidates, not yet solutions."),
            ("Substitute every candidate into the ORIGINAL equation",
             "Keep the ones that make it true and discard the rest. State the discarded "
             "ones as extraneous &mdash; an answer of \"no solution\" is a legitimate and "
             "complete result."),
        ],
        "worked": {
            "title": "One equation with an extraneous root, one with two radicals",
            "intro": [
                "In (a) the algebra is flawless and one of the two answers is still not a "
                "solution.",
            ],
            "lines": [
                "(a)  √(x + 7) = x − 5",
                "",
                "     square both sides    x + 7 = (x − 5)² = x² − 10x + 25",
                "     rearrange            0 = x² − 11x + 18",
                "     factor               0 = (x − 2)(x − 9)",
                "     candidates           x = 2,  x = 9",
                "",
                "     CHECK in the original:",
                "       x = 9:   √(9 + 7) = √16 = 4     and   9 − 5 = 4      ✓",
                "       x = 2:   √(2 + 7) = √9  = 3     and   2 − 5 = −3     ✗",
                "",
                "     solution set:  { 9 }",
                "",
                "(b)  √(x + 5) − √x = 1",
                "",
                "     isolate              √(x + 5) = 1 + √x",
                "     square               x + 5 = 1 + 2√x + x        ← middle term kept",
                "     simplify             4 = 2√x,   so  √x = 2",
                "     square again         x = 4",
                "",
                "     CHECK:   √(4 + 5) − √4 = 3 − 2 = 1               ✓",
                "",
                "     solution set:  { 4 }",
            ],
            "after": [
                "In (a), `x = 2` satisfies `x² − 11x + 18 = 0` exactly. It is a real "
                "solution of the squared equation and not of the original, because "
                "squaring merged `√(x + 7) = x − 5` with "
                "`√(x + 7) = −(x − 5)` &mdash; and `2` solves the second one.",
                "There is a shortcut worth noticing in (a): the left side is a principal "
                "square root, so it is never negative, so `x − 5 ≥ 0` and `x ≥ 5` "
                "before any work is done. That condition alone rejects `x = 2`. Writing "
                "the domain restriction first is the same habit lesson 1 asked for.",
            ],
        },
        "quiz_title": "Which candidates survive",
        "quiz": [
            {"q": "Solving `√(3x + 1) = x − 3` gives candidates `x = 1` and `x = 8`. Which solve it?",
             "a": ["Both", "Only `x = 1`", "Only `x = 8`", "Neither"],
             "c": 2,
             "why": "At `x = 8`: `√25 = 5` and `8 − 3 = 5` ✓. At `x = 1`: `√4 = 2` "
                    "but `1 − 3 = −2` ✗. A principal root cannot equal a "
                    "negative number."},
            {"q": "Why can squaring both sides create a solution that is not one?",
             "a": ["Because squaring is not always defined",
                   "Because `a² = b²` allows `a = −b` as well as `a = b`",
                   "Because the domain of a square root is restricted",
                   "Because the arithmetic gets harder"],
             "c": 1,
             "why": "The implication runs one way only. Squaring keeps every original "
                    "solution and also admits the solutions of `a = −b`, which come "
                    "back indistinguishable from the rest."},
            {"q": "`√(x + 1) = −3` has:",
             "a": ["The solution `x = 8`", "The solution `x = 10`",
                   "No solution", "Two solutions"],
             "c": 2,
             "why": "A principal square root is never negative, so no `x` can satisfy it. "
                    "Squaring produces the candidate `x = 8`, which fails the check &mdash; "
                    "it is entirely an artefact of the step."},
            {"q": "You should substitute your candidates into:",
             "a": ["The squared equation", "The original equation",
                   "The factored quadratic", "Any line, they are equivalent"],
             "c": 1,
             "why": "The lines after squaring are not equivalent to the original &mdash; "
                    "that is precisely the problem. Only the original separates solutions "
                    "from extraneous roots."},
        ],
        "mistakes": [
            ("Squaring term by term",
             "`√(x + 7) = x − 5` does not become `x + 7 = x² − 25`. The whole "
             "side is squared, and `(x − 5)² = x² − 10x + 25` keeps its middle "
             "term."),
            ("Squaring before isolating",
             "With `√(x + 5) − √x = 1`, squaring immediately leaves a cross term "
             "containing `√(x² + 5x)`. Isolate one radical first and the second squaring "
             "is straightforward."),
            ("Treating the check as optional tidying",
             "It is a step of the method, not a courtesy. Without it the answer to "
             "example (a) is \"`2` and `9`\", which is wrong, and nothing earlier in "
             "the working reveals it."),
        ],
        "standard": ("Finish when you can say WHY a candidate failed, not merely that it did.",
                     "Given a radical equation you should be able to solve it, check both "
                     "candidates in the original, and name the equation the extraneous "
                     "root actually satisfies. You should also be able to spot, before "
                     "starting, when a sign condition makes some candidates impossible."),
        "note": "This lesson and lesson 6 are the same lesson in two costumes. Clearing a "
                "denominator and squaring both sides are both legal, both irreversible, "
                "and both handled by the identical discipline: solve, then test every "
                "candidate against the equation you were given.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "radical-functions-and-their-graphs",
        "title": "Radical Functions and Their Graphs",
        "module": "Radicals",
        "one_line": "Solve an inequality to find the domain, then graph.",
        "summary": (
            "A radical function's domain is not read off &mdash; it is solved for. An "
            "even index turns the requirement \"radicand ≥ 0\" into an inequality, and "
            "the answer to that inequality is the domain. The graph then follows from "
            "the domain, the range and a handful of exact points."
        ),
        "key": [
            "f(x) = √(x − 3)      domain x ≥ 3,      range y ≥ 0",
            "g(x) = ∛x            domain all reals,  range all reals",
            "h(x) = √(x² − 9)     domain x ≤ −3 or x ≥ 3",
            "even index  →  solve  radicand ≥ 0",
        ],
        "key_label": "Three functions, three domains",
        "concepts_intro": (
            "The course ends where it began: with the values that are not allowed, "
            "found before anything is drawn."
        ),
        "concepts": [
            ("The domain is the solution of an inequality",
             "For an even index, `f(x) = ⁿ√(g(x))` is defined exactly where `g(x) ≥ 0`. "
             "Finding the domain is therefore an inequality problem from course 2, and "
             "when `g` is a quadratic it is a sign-analysis problem from course 4."),
            ("Odd indices have no domain restriction",
             "`∛x` is defined for every real number, negatives included, and its range "
             "is every real number too. The whole difficulty of this lesson is a feature "
             "of even indices only."),
            ("The range comes from the principal root",
             "`√(anything)` is never negative, so the basic square-root function has "
             "range `y ≥ 0` &mdash; it is half of a sideways parabola, not all of one. "
             "A vertical shift moves that floor; a reflection turns it into a ceiling."),
        ],
        "read_title": "Domain, range and shape",
        "read_intro": "How to find the domain, what the graph looks like, and what the transformations do to both.",
        "body": [
            ("def", ("Radical function",
                     "A <strong>radical function</strong> is one whose rule places the "
                     "variable under a radical: `f(x) = ⁿ√(g(x))`. For even `n` its "
                     "domain is `{ x : g(x) ≥ 0 }`; for odd `n` it is the domain of `g`.")),
            ("p", "Compare this with lesson 1. There the domain was found by setting a "
                  "denominator equal to zero and excluding the roots &mdash; an equation. "
                  "Here it is found by requiring a radicand to be non-negative &mdash; an "
                  "inequality. A denominator excludes isolated points; an even radical "
                  "excludes whole intervals."),
            ("example", ("Three domains",
                         "`√(x − 3)` needs `x − 3 ≥ 0`, so `x ≥ 3`. "
                         "`√(5 − x)` needs `5 − x ≥ 0`, so `x ≤ 5` &mdash; the "
                         "inequality reverses, exactly as in course 2. `∛(x − 3)` "
                         "needs nothing: its domain is all real numbers.")),
            ("h3", "When the radicand is a quadratic"),
            ("p", "For `h(x) = √(x² − 9)` the requirement is `x² − 9 ≥ 0`, "
                  "that is `(x − 3)(x + 3) ≥ 0`. A product of two factors is "
                  "non-negative when both have the same sign, which happens for `x ≤ −3` "
                  "and for `x ≥ 3`. The domain is two separate rays, and the graph has a "
                  "gap between `−3` and `3` where the function does not exist."),
            ("p", "This is worth pausing on. The formula `√(x² − 9)` gives no "
                  "warning that it is undefined on an interval six units wide. Only "
                  "solving the inequality reveals it, and a plot made by sampling "
                  "convenient integers would show the gap without explaining it."),
            ("thm", ("The graph of the square-root function",
                     "`y = √x` has domain `x ≥ 0` and range `y ≥ 0`. It starts at the "
                     "origin, rises, and flattens: it is the upper half of the parabola "
                     "`x = y²`.",
                     "It is the reflection of `y = x²` restricted to `x ≥ 0` in the line "
                     "`y = x`, which is what makes it that function's inverse &mdash; and "
                     "why the restriction is needed at all.")),
            ("p", "The transformations from course 3 apply unchanged. In "
                  "`y = a·√(x − h) + k` the graph starts at `(h, k)` instead of the "
                  "origin; `h` shifts the domain to `x ≥ h`, `k` shifts the range to "
                  "`y ≥ k`, and a negative `a` flips it downwards so the range becomes "
                  "`y ≤ k`. The endpoint is the one point worth plotting exactly."),
            ("p", "One last connection back to lesson 8. The function `f(x) = √(x²)` is "
                  "defined for every real `x`, since `x²` is never negative &mdash; but "
                  "its graph is not the line `y = x`. It is `y = |x|`, a V with its "
                  "vertex at the origin. The identity from lesson 8, drawn."),
            ("p", "Everywhere in this course `√(−4)` has been outside the domain, "
                  "and every domain here has been a set of real numbers. Course 6 "
                  "introduces `i` and gives negative radicands values; nothing in this "
                  "course anticipates that, and the domains stated here are the correct "
                  "ones for real-valued functions."),
        ],
        "lab": ("grapher", {
            "mode": "radical",
            "panel_title": "The domain, then the curve",
            "panel_intro": "The inequality is solved before anything is drawn, and the "
                           "excluded interval is shaded rather than merely left blank. "
                           "The endpoint is marked at its exact coordinates.",
        }),
        "steps_title": "Analysing a radical function",
        "steps_intro": "Domain first. Everything else is easier once it is known, and wrong if it is skipped.",
        "steps": [
            ("Check whether the index is even or odd",
             "Odd index: the domain is everything `g` allows, and you are done with this "
             "question. Even index: continue to the inequality."),
            ("Set the radicand ≥ 0 and solve",
             "A linear radicand gives a single ray &mdash; remember to reverse the "
             "inequality when dividing by a negative. A quadratic radicand needs "
             "factoring and a sign analysis, and may give two rays or an interval."),
            ("Find the endpoint and the range",
             "The radical equals `0` at the boundary of the domain, so the endpoint is "
             "where the graph starts. From there `√` only increases, giving a range "
             "bounded below &mdash; unless a reflection turns it round."),
            ("Plot exact points and join them",
             "Choose values that make the radicand a perfect power: for `√(x − 3)` "
             "take `x = 3, 4, 7, 12` to get `y = 0, 1, 2, 3`. Four exact points beat "
             "twenty decimals."),
        ],
        "worked": {
            "title": "Two domains and one graph",
            "intro": [
                "One linear radicand, one quadratic, and then the curve for the first.",
            ],
            "lines": [
                "(a)  f(x) = √(2x + 8)",
                "     require   2x + 8 ≥ 0",
                "               2x ≥ −8",
                "                x ≥ −4                domain:  x ≥ −4",
                "     endpoint  f(−4) = √0 = 0         starts at (−4, 0)",
                "     range     y ≥ 0",
                "",
                "(b)  h(x) = √(x² − 9)",
                "     require   x² − 9 ≥ 0",
                "               (x − 3)(x + 3) ≥ 0     product non-negative ⇒ same signs",
                "               x ≤ −3   or   x ≥ 3    domain: two rays, gap between",
                "     check     x = 0 gives √(−9),  undefined       ✓ gap is real",
                "     check     x = 3 gives √0 = 0,  defined        ✓ endpoints included",
                "",
                "(c)  graph of y = √(x − 3)            exact points, radicand a perfect square",
                "        x  |  3    4    7    12   19",
                "     y = √ |  0    1    2     3    4",
                "",
                "     starts at (3, 0), rises, flattens; nothing left of x = 3",
            ],
            "after": [
                "In (b) the two checks are not decoration. `x = 0` confirms the gap is "
                "genuine rather than an artefact of the factoring, and `x = 3` confirms "
                "the endpoints belong to the domain &mdash; `≥` rather than `&gt;`, "
                "because `√0` is perfectly well defined.",
                "In (c) the `x` values were chosen so the radicand is `0, 1, 4, 9, 16`. "
                "Picking `x = 5` instead gives `y = √2 ≈ 1.414`, a point you cannot place "
                "accurately by hand. Choosing inputs that make the radicand a perfect "
                "power is the difference between a sketch and a guess.",
            ],
        },
        "quiz_title": "Domains of radical functions",
        "quiz": [
            {"q": "The domain of `f(x) = √(5 − x)` is:",
             "a": ["`x ≥ 5`", "`x ≤ 5`", "`x ≥ −5`", "All real numbers"],
             "c": 1,
             "why": "`5 − x ≥ 0` gives `5 ≥ x`, that is `x ≤ 5`. The `x` has a "
                    "negative coefficient, so the inequality reverses when it is isolated."},
            {"q": "The domain of `g(x) = ∛(x − 4)` is:",
             "a": ["`x ≥ 4`", "`x ≤ 4`", "All real numbers", "`x ≠ 4`"],
             "c": 2,
             "why": "The index is odd, so the radicand may be negative: `∛(−8) = −2` "
                    "is a perfectly good real number. Only even indices restrict the domain."},
            {"q": "The domain of `h(x) = √(x² − 9)` is:",
             "a": ["`−3 ≤ x ≤ 3`", "`x ≤ −3` or `x ≥ 3`",
                   "All real numbers", "`x ≥ 3`"],
             "c": 1,
             "why": "`(x − 3)(x + 3) ≥ 0` needs the two factors to share a sign, "
                    "which happens outside the roots. At `x = 0` the radicand is "
                    "`−9`, so the middle interval is excluded."},
            {"q": "The graph of `f(x) = √(x²)` is:",
             "a": ["The line `y = x`", "The V-shaped graph of `y = |x|`",
                   "A parabola", "Half a parabola, for `x ≥ 0` only"],
             "c": 1,
             "why": "`√(x²) = |x|` for every real `x`, from lesson 8. The domain is all "
                    "reals because `x²` is never negative, and the output is never "
                    "negative either &mdash; hence the V."},
        ],
        "mistakes": [
            ("Reading the domain off the formula instead of solving for it",
             "`√(x² − 9)` looks defined everywhere because a square looks harmless. "
             "The inequality `x² − 9 ≥ 0` is the only thing that reveals the gap "
             "between `−3` and `3`."),
            ("Forgetting to reverse the inequality",
             "`5 − x ≥ 0` gives `x ≤ 5`, not `x ≥ 5`. Dividing or multiplying an "
             "inequality by a negative flips it, exactly as in course 2."),
            ("Excluding the endpoint",
             "The condition is radicand `≥ 0`, not `&gt; 0`. `√0 = 0` is defined, so the "
             "endpoint belongs to the domain and the graph starts with a closed point."),
        ],
        "standard": ("Finish when the domain is the first thing you write and the graph is "
                     "the last.",
                     "Given any radical function you should be able to decide the domain "
                     "by solving an inequality, state the range from the principal-root "
                     "convention, locate the endpoint exactly, and sketch the curve from "
                     "points you chose to be exact. A graph drawn before the domain is "
                     "known is a graph that will be drawn over an interval where the "
                     "function does not exist."),
        "note": "That closes the course, and it closes it on the sentence it opened with: "
                "find the values that are not allowed, and find them first. A denominator "
                "gave isolated exclusions, an even radical gives whole intervals, and both "
                "are invisible in an answer that was simplified before the domain was "
                "written down.",
    },
]
