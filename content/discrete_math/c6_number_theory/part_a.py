"""Course 6, lessons 01-07 — divisibility, gcd and modular arithmetic."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "divisibility-and-the-division-algorithm",
        "title": "Divisibility and the Division Algorithm",
        "module": "Divisibility",
        "one_line": "Every division leaves a unique quotient and remainder.",
        "summary": (
            "`a = qb + r` with `0 ≤ r < b`, and both `q` and `r` are unique. That single "
            "theorem is the foundation of everything else in this course."
        ),
        "key": [
            "b | a   means   a = bk  for some integer k",
            "a = qb + r  with  0 ≤ r < b        q, r UNIQUE",
            "the remainder is never negative",
            "−7 = (−3)(3) + 2,  so  −7 mod 3 = 2",
        ],
        "key_label": "One theorem, used everywhere",
        "concepts_intro": (
            "Divisibility is a relation on the integers, and the division algorithm is "
            "what makes it computable."
        ),
        "concepts": [
            ("Divisibility is exact",
             "`b | a` means the division leaves no remainder. It is a statement about "
             "integers, not an operation."),
            ("The remainder is unique and non-negative",
             "That convention is what makes `mod` a function. `−7 mod 3` is 2, not `−1`."),
            ("Divisibility is transitive and additive",
             "`d | a` and `d | b` imply `d | (ax + by)` for any integers `x, y`. Almost "
             "every proof in this course uses that one line."),
        ],
        "read_title": "Divisibility and division",
        "read_intro": "The definition, the theorem, and the properties everything else rests on.",
        "body": [
            ("def", ("Divisibility",
                     "For integers `a` and `b` with `b ≠ 0`, `b | a` (\"`b` divides `a`\") "
                     "means there is an integer `k` with `a = bk`. Then `b` is a "
                     "<strong>divisor</strong> or <strong>factor</strong> of `a`.")),
            ("thm", ("Basic properties",
                     "For integers `a, b, c, d`: if `d | a` and `d | b` then "
                     "`d | (ax + by)` for all integers `x, y`; if `a | b` and `b | c` then "
                     "`a | c`; and `d | a` with `a ≠ 0` implies `|d| ≤ |a|`.")),
            ("proof", [
                "For the first: `a = dm` and `b = dn`, so `ax + by = d(mx + ny)`, and "
                "`mx + ny` is an integer.",
                "For the second: `b = am` and `c = bn`, so `c = a(mn)`.",
                "For the third: `a = dk` with `a ≠ 0` forces `k ≠ 0`, so `|k| ≥ 1` and "
                "`|a| = |d||k| ≥ |d|`.",
            ]),
            ("p", "The first property is the workhorse. It is what lets the Euclidean "
                  "algorithm work, what proves Euclid's theorem on primes, and what makes "
                  "Bézout's identity useful &mdash; and it is one line."),
            ("thm", ("Division algorithm",
                     "For any integer `a` and any positive integer `b`, there are unique "
                     "integers `q` and `r` with `a = qb + r` and `0 ≤ r &lt; b`.")),
            ("proof", [
                "<strong>Existence.</strong> Let `S = {a − qb : q ∈ ℤ, a − qb ≥ 0}`. It is "
                "nonempty (take `q` very negative) and consists of non-negative integers, "
                "so by well-ordering it has a least element `r = a − qb`.",
                "If `r ≥ b` then `r − b = a − (q+1)b` is in `S` and smaller than `r`, "
                "contradicting minimality. So `0 ≤ r &lt; b`.",
                "<strong>Uniqueness.</strong> If `a = qb + r = q'b + r'` with both "
                "remainders in `[0, b)`, then `b(q − q') = r' − r`. The right side has "
                "absolute value less than `b`, and the left is a multiple of `b`, so both "
                "are 0. Hence `r = r'` and `q = q'`.",
            ]),
            ("p", "Uniqueness is what makes the notation legitimate: `a div b` and "
                  "`a mod b` name specific integers rather than one of several "
                  "possibilities."),
            ("h3", "Negative dividends"),
            ("example", ("`−7` divided by 3",
                         "`−7 = (−3)(3) + 2`, so `q = −3` and `r = 2`. Not "
                         "`(−2)(3) + (−1)`, because the theorem requires `0 ≤ r &lt; b`. "
                         "The quotient rounds toward negative infinity, not toward zero.")),
            ("p", "Many programming languages disagree with the theorem here: C-style `%` "
                  "returns `−1` for `−7 % 3`, while Python returns 2. The mathematical "
                  "convention is Python's, and it is the one that makes modular arithmetic "
                  "work &mdash; classes should not depend on the sign of a representative."),
            ("def", ("The mod operator",
                     "`a mod b` denotes the unique remainder `r` from the division "
                     "algorithm, so `0 ≤ a mod b &lt; b` always.")),
        ],
        "lab": ("number", {
            "mode": "div",
            "panel_title": "The division algorithm",
            "panel_intro": "Try a negative `a`. The remainder stays non-negative, which is "
                           "the theorem's requirement and the reason modular arithmetic is "
                           "well defined.",
        }),
        "steps_title": "Working with divisibility",
        "steps_intro": "Replace the statement by the equation it abbreviates.",
        "steps": [
            ("Translate `b | a` into `a = bk`",
             "Divisibility claims are unusable until unfolded. Almost every proof in this "
             "course starts here."),
            ("Use the linear-combination property",
             "`d | a` and `d | b` give `d | (ax + by)`. This is the step that appears in "
             "nearly every argument."),
            ("Apply the division algorithm when a remainder is needed",
             "`a = qb + r` with `0 ≤ r &lt; b`, and both are unique."),
            ("Watch the sign",
             "The remainder is never negative. If a computation produces one, add `b`."),
        ],
        "worked": {
            "title": "Divisibility by 3, from the digits",
            "intro": ["Why the digit-sum test works."],
            "lines": [
                "Write n in base 10:   n = Σ dᵢ · 10ⁱ",
                "",
                "Note 10 = 9 + 1, so 10ⁱ = (9+1)ⁱ leaves remainder 1 on division by 3:",
                "   10ⁱ ≡ 1 (mod 3)      for every i ≥ 0",
                "",
                "Therefore  n ≡ Σ dᵢ · 1 = Σ dᵢ  (mod 3)",
                "",
                "So 3 | n  ⟺  3 divides the digit sum.",
                "",
                "Example:  4 728  →  4+7+2+8 = 21  →  2+1 = 3   ⟹ divisible by 3",
                "Check:    4728 = 3 × 1576                        ✓",
            ],
            "after": [
                "The same argument gives the test for 9, since `10ⁱ ≡ 1 (mod 9)` too. For "
                "11 the powers alternate &mdash; `10ⁱ ≡ (−1)ⁱ` &mdash; which is why that "
                "test uses an alternating digit sum. The notation used here is lesson 7's, "
                "arriving early because it makes the argument short."
            ],
        },
        "quiz_title": "Divisibility",
        "quiz": [
            {"q": "What is `−17 mod 5`?",
             "a": ["`−2`", "3", "2", "`−17`"],
             "c": 1,
             "why": "`−17 = (−4)(5) + 3` with `0 ≤ 3 &lt; 5`. The remainder is never "
                    "negative, so `−2` is not an answer the theorem permits."},
            {"q": "`d | a` and `d | b`. What follows?",
             "a": ["`d | ab` only", "`d | (a + b)` and `d | (a − b)`",
                   "`d = 1`", "`a = b`"],
             "c": 1,
             "why": "Both are instances of `d | (ax + by)`, the linear-combination "
                    "property, with `(x,y) = (1,1)` and `(1,−1)`."},
            {"q": "The division algorithm guarantees:",
             "a": ["`r` exists", "`r` exists and is unique, with `0 ≤ r &lt; b`",
                   "`b | a`", "`q` is positive"],
             "c": 1,
             "why": "Existence and uniqueness together. Uniqueness is what makes `mod` a "
                    "function rather than a relation."},
        ],
        "mistakes": [
            ("Allowing a negative remainder",
             "`−7 mod 3 = 2`. Some programming languages disagree with the mathematical "
             "convention, and mixing the two silently breaks modular arithmetic."),
            ("Confusing `b | a` with `b/a`",
             "The first is a statement (true or false); the second is a number. `3 | 12` "
             "is true and `3/12` is a quarter."),
            ("Forgetting `b ≠ 0`",
             "Divisibility by zero is undefined, and the division algorithm requires "
             "`b &gt; 0` as stated."),
        ],
        "standard": ("Finish when the linear-combination property is automatic.",
                     "Prove that if `d | (a + b)` and `d | a` then `d | b`. It is one "
                     "application of the property, and it is the shape of argument the "
                     "next five lessons repeat."),
        "note": "Everything in this course is a consequence of the division algorithm. "
                "The Euclidean algorithm is it applied repeatedly, modular arithmetic is "
                "its remainder, and RSA is modular arithmetic with large primes.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "primes-and-factorisation",
        "title": "Primes and Unique Factorisation",
        "module": "Divisibility",
        "one_line": "Every integer above 1 factors into primes, in exactly one way.",
        "summary": (
            "The fundamental theorem of arithmetic. Primes are the multiplicative atoms, "
            "there are infinitely many, and the uniqueness of the factorisation is what "
            "makes almost every later argument possible."
        ),
        "key": [
            "prime: exactly two positive divisors, 1 and itself.  1 is NOT prime.",
            "every n > 1 is a product of primes, uniquely up to order",
            "there are infinitely many primes                    (Euclid)",
            "if n is composite it has a prime factor ≤ √n",
        ],
        "key_label": "The atoms of multiplication",
        "concepts_intro": (
            "Existence of a factorisation is easy; uniqueness is the theorem, and it is "
            "what everything else uses."
        ),
        "concepts": [
            ("1 is not prime, by decision",
             "Because uniqueness of factorisation would fail: `6 = 2·3 = 1·2·3 = 1·1·2·3`. "
             "The definition is chosen to make the theorem true."),
            ("Uniqueness is the substantive half",
             "Existence follows from strong induction in three lines. Uniqueness needs "
             "Euclid's lemma, which needs Bézout."),
            ("Trial division stops at `√n`",
             "A composite `n` has a factor at most `√n`, so testing beyond that is "
             "unnecessary &mdash; and it is why the sieve of lesson 3 stops where it does."),
        ],
        "read_title": "Primes",
        "read_intro": "The definition, both halves of the fundamental theorem, and Euclid's proof.",
        "body": [
            ("def", ("Prime and composite",
                     "An integer `p &gt; 1` is <strong>prime</strong> if its only positive "
                     "divisors are 1 and `p`. An integer `n &gt; 1` that is not prime is "
                     "<strong>composite</strong>. The number 1 is neither.")),
            ("p", "Excluding 1 is a convention chosen to make the fundamental theorem "
                  "clean. If 1 were prime, `6` would factor as `2·3`, `1·2·3`, `1·1·2·3` "
                  "and so on, and uniqueness would need an awkward qualification."),
            ("thm", ("Fundamental theorem of arithmetic",
                     "Every integer `n &gt; 1` can be written as a product of primes, and "
                     "the factorisation is unique up to the order of the factors.")),
            ("proof", [
                "<strong>Existence</strong>, by strong induction. If `n` is prime it is a "
                "product of one prime. Otherwise `n = ab` with `1 &lt; a, b &lt; n`, and by "
                "the inductive hypothesis both factor into primes; concatenating the two "
                "factorisations gives one for `n`.",
                "<strong>Uniqueness</strong> requires Euclid's lemma (lesson 6): if a prime "
                "`p` divides `ab` then `p | a` or `p | b`. Given two factorisations of `n`, "
                "the first prime of one divides the product forming the other, hence "
                "divides one of its primes, hence equals it. Cancelling and repeating "
                "matches the factorisations term by term.",
            ]),
            ("p", "Uniqueness is not obvious and it is not universal. In the number system "
                  "`{a + b√−5}` the number 6 factors as `2 · 3` and as "
                  "`(1 + √−5)(1 − √−5)`, with all four factors irreducible. Unique "
                  "factorisation is a property of `ℤ`, and it is what course 6 relies on "
                  "throughout."),
            ("thm", ("Euclid: infinitely many primes",
                     "For any finite list of primes there is a prime not on it.")),
            ("proof", [
                "Given primes `p₁, …, p_k`, let `N = p₁p₂⋯p_k + 1`. Since `N &gt; 1` it has "
                "a prime factor `q`.",
                "If `q` were some `pᵢ`, it would divide both `p₁⋯p_k` and `N`, hence their "
                "difference 1 &mdash; impossible for a prime. So `q` is not on the list.",
            ]),
            ("p", "`N` itself need not be prime: `2·3·5·7·11·13 + 1 = 30031 = 59 · 509`. "
                  "The proof produces a prime not on the list, not necessarily `N`, and "
                  "misremembering that is the standard error."),
            ("thm", ("Trial division bound",
                     "If `n &gt; 1` is composite, it has a prime factor `p ≤ √n`.")),
            ("proof", [
                "Write `n = ab` with `1 &lt; a ≤ b &lt; n`. If both exceeded `√n` their "
                "product would exceed `n`, so `a ≤ √n`. Any prime factor of `a` is a prime "
                "factor of `n` and is at most `a ≤ √n`.",
            ]),
            ("p", "So testing 101 for primality needs only the primes up to 10: 2, 3, 5, 7. "
                  "None divides it, so it is prime. That is four divisions rather than "
                  "ninety-nine."),
            ("h3", "How the primes are distributed"),
            ("p", "There are 25 primes below 100, 168 below 1000, and 78 498 below a "
                  "million. The prime number theorem says the count below `n` is "
                  "approximately `n / ln n`, so primes thin out slowly &mdash; near `10¹⁰⁰` "
                  "roughly one number in 230 is prime. That density is what makes RSA key "
                  "generation practical: random large numbers can be tested until one is "
                  "prime."),
        ],
        "lab": ("number", {
            "mode": "factor",
            "panel_title": "Factorisation, step by step",
            "panel_intro": "Trial division from 2 upward, stopping at `√n`. The divisor "
                           "count comes from the exponents, which is the fundamental "
                           "theorem being used rather than quoted.",
        }),
        "steps_title": "Factoring and testing",
        "steps_intro": "Small primes first, stop at the square root.",
        "steps": [
            ("Divide out the small primes in order",
             "2, then 3, then 5, and so on, taking each as many times as it goes."),
            ("Stop when the divisor exceeds `√(remaining)`",
             "Whatever is left is then prime. This is the bound above, and it is what "
             "keeps hand factorisation feasible."),
            ("Count divisors from the exponents",
             "If `n = p₁^{e₁}⋯p_k^{e_k}` then `n` has `(e₁+1)⋯(e_k+1)` positive divisors, "
             "since each exponent is chosen independently from 0 to `eᵢ`."),
            ("To test primality, divide by primes up to `√n`",
             "If none divides, it is prime. For large numbers this is hopeless and "
             "probabilistic tests are used instead."),
        ],
        "worked": {
            "title": "Factor 360 and count its divisors",
            "intro": ["Trial division, then the divisor formula."],
            "lines": [
                "360 / 2 = 180        360 / 4  = 90        360 / 8 = 45",
                "  45 / 3 =  15        45 / 9  =  5",
                "   5 is prime, and 5 > √5 stops the search",
                "",
                "   360 = 2³ · 3² · 5",
                "",
                "Divisors:  (3+1)(2+1)(1+1) = 4 · 3 · 2 = 24",
                "",
                "Check by listing:  1,2,3,4,5,6,8,9,10,12,15,18,20,24,30,36,40,45,",
                "                   60,72,90,120,180,360        — 24 of them   ✓",
            ],
            "after": [
                "The divisor count is a product rule application: a divisor is determined "
                "by choosing an exponent for each prime independently, from 0 up to its "
                "exponent in `n`. Course 4 lesson 1 is doing the work, and the fundamental "
                "theorem is what guarantees the choice determines the divisor uniquely."
            ],
        },
        "quiz_title": "Primes",
        "quiz": [
            {"q": "Why is 1 not considered prime?",
             "a": ["It is too small",
                   "Uniqueness of prime factorisation would fail",
                   "It has no divisors",
                   "It is composite"],
             "c": 1,
             "why": "Allowing 1 would let any factorisation be padded with 1s. The "
                    "definition is chosen to make the fundamental theorem clean."},
            {"q": "To test whether 149 is prime, you must divide by primes up to:",
             "a": ["74", "12", "149", "50"],
             "c": 1,
             "why": "`√149 ≈ 12.2`, so the primes 2, 3, 5, 7, 11 suffice. A composite has a "
                    "factor at most its square root."},
            {"q": "In Euclid's proof, `N = p₁⋯p_k + 1` is:",
             "a": ["always prime",
                   "not necessarily prime, but it has a prime factor not on the list",
                   "always composite",
                   "equal to the next prime"],
             "c": 1,
             "why": "`2·3·5·7·11·13 + 1 = 30031 = 59 · 509`. The proof produces a new "
                    "prime, not necessarily `N` itself."},
        ],
        "mistakes": [
            ("Calling 1 prime",
             "It is neither prime nor composite, and the exclusion is what makes unique "
             "factorisation stateable."),
            ("Believing Euclid's `N` is always prime",
             "It has a prime factor outside the list, which is all the proof needs and all "
             "it claims."),
            ("Trial dividing past the square root",
             "Unnecessary. If nothing up to `√n` divides `n`, nothing above it does either."),
        ],
        "standard": ("Finish when you can factor a four-digit number and count its divisors.",
                     "Factor 2520 completely and predict its divisor count from the "
                     "exponents before listing anything. `2520 = 2³·3²·5·7`, so there are "
                     "`4·3·2·2 = 48` divisors."),
        "note": "Factoring is easy for small numbers and believed hard for large ones, and "
                "that asymmetry is the entire basis of RSA in lesson 14. The best known "
                "general algorithms are sub-exponential but not polynomial, and no proof "
                "exists that factoring is genuinely hard.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "the-sieve-of-eratosthenes",
        "title": "The Sieve of Eratosthenes",
        "module": "Divisibility",
        "one_line": "Cross out the multiples; what survives is prime.",
        "summary": (
            "The oldest algorithm still in use. It finds every prime up to `n` by "
            "removing multiples, stops at `√n` for the reason lesson 2 gave, and costs "
            "far less than testing each number separately."
        ),
        "key": [
            "for each prime p ≤ √n:  cross out 2p, 3p, … — starting at p²",
            "whatever is left uncrossed is prime",
            "start at p²: smaller multiples were removed by smaller primes",
            "cost ≈ n log log n operations",
        ],
        "key_label": "One pass per small prime",
        "concepts_intro": (
            "The sieve is the standard example of an algorithm that beats the obvious "
            "approach by reorganising the work."
        ),
        "concepts": [
            ("Crossing out is cheaper than testing",
             "Testing each number separately repeats work. The sieve marks each composite "
             "once per distinct prime factor and no more."),
            ("Start at `p²`",
             "Multiples of `p` below `p²` have a smaller prime factor and were already "
             "crossed out. Starting at `2p` is correct and wasteful."),
            ("Stop at `√n`",
             "After sieving by every prime up to `√n`, anything uncrossed has no factor "
             "below its square root and is prime, by lesson 2's bound."),
        ],
        "read_title": "The sieve",
        "read_intro": "The algorithm, its two optimisations, and its cost.",
        "body": [
            ("math", [
                "SIEVE(n):",
                "    mark 2 … n as candidates",
                "    for p = 2, 3, 4, … while p·p ≤ n:",
                "        if p is still a candidate:            # then p is prime",
                "            for q = p², p²+p, p²+2p, … ≤ n:",
                "                cross out q",
                "    the surviving candidates are the primes ≤ n",
            ]),
            ("p", "Two things make it efficient. The outer loop stops at `√n` because "
                  "anything surviving that far has no prime factor below its own square "
                  "root. The inner loop starts at `p²` because a multiple `kp` with "
                  "`k &lt; p` has the prime factor `k` or a factor of it, and was removed "
                  "earlier."),
            ("thm", ("Correctness",
                     "After the sieve, an integer `m` in `2, …, n` is uncrossed if and only "
                     "if it is prime.")),
            ("proof", [
                "A prime is never crossed out: it is only removed as a multiple `kp` with "
                "`k ≥ p ≥ 2`, so any crossed-out number is composite.",
                "A composite `m` has a prime factor `p ≤ √m ≤ √n` by lesson 2. When the "
                "outer loop reaches `p`, `p` is still a candidate (it is prime), and "
                "`m = p·(m/p)` with `m/p ≥ p`, so `m ≥ p²` and `m` is a multiple of `p` at "
                "or beyond `p²`. It is crossed out.",
            ]),
            ("h3", "Cost"),
            ("p", "The inner loop for prime `p` performs about `n/p` operations, so the "
                  "total is roughly `n Σ_{p ≤ √n} 1/p`. The sum of reciprocals of primes up "
                  "to `x` grows like `ln ln x`, giving `Θ(n log log n)` &mdash; very nearly "
                  "linear, and `log log n` is under 5 for any `n` anyone will run."),
            ("p", "Compare with testing each number by trial division: about `√m` divisions "
                  "for each `m`, giving `Θ(n^{3/2}/log n)` overall. At `n = 10⁶` the sieve "
                  "does a few million operations and trial division does roughly a "
                  "hundred million."),
            ("math", [
                "primes below n:",
                "        10        4",
                "       100       25",
                "     1 000      168",
                "    10 000    1 229",
                "   100 000    9 592",
                " 1 000 000   78 498          n/ln n predicts 72 382",
            ]),
            ("p", "The prime number theorem says the count is asymptotically `n / ln n`, "
                  "and the table shows the approximation improving slowly. A better "
                  "estimate is the logarithmic integral, which at `10⁶` gives 78 628 "
                  "against the true 78 498."),
            ("h3", "Limits"),
            ("p", "The sieve finds all primes up to `n` and needs memory proportional to "
                  "`n`. For the 1024-bit primes RSA needs, sieving is hopeless: there are "
                  "more candidates than atoms in the universe. Those primes are found by "
                  "testing random numbers with probabilistic tests such as "
                  "Miller&ndash;Rabin, which decide primality without producing factors."),
        ],
        "lab": ("number", {
            "mode": "sieve",
            "panel_title": "Sieving, with provenance",
            "panel_intro": "Every crossed-out number records which prime removed it. Hover "
                           "one and see the smallest prime factor &mdash; and note nothing "
                           "beyond `√N` ever removes anything new.",
        }),
        "steps_title": "Running the sieve",
        "steps_intro": "One pass per prime, starting at its square.",
        "steps": [
            ("List the candidates",
             "2 through `n`. The number 1 is excluded from the start."),
            ("Take the smallest uncrossed number",
             "It is prime, because nothing smaller divides it."),
            ("Cross out its multiples from `p²` upward",
             "Smaller multiples already went. This is the optimisation that halves the "
             "work at small primes."),
            ("Stop when `p² > n`",
             "Everything still uncrossed is prime, by the trial-division bound."),
        ],
        "worked": {
            "title": "Sieving to 30",
            "intro": ["`√30 ≈ 5.5`, so only 2, 3 and 5 need passes."],
            "lines": [
                "start   2 3 4 5 6 7 8 9 10 … 30",
                "",
                "p = 2   cross 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30",
                "p = 3   cross 9, 15, 21, 27          (6, 12, 18, 24, 30 already gone)",
                "p = 5   cross 25                     (10, 15, 20, 30 already gone)",
                "p = 7   7² = 49 > 30  ⟹  STOP",
                "",
                "surviving: 2 3 5 7 11 13 17 19 23 29        — 10 primes",
                "",
                "Note the p = 3 pass started at 9, not 6, and the p = 5 pass at 25.",
            ],
            "after": [
                "The p = 5 pass crossed out exactly one number. That is typical: nearly all "
                "the work happens at the smallest primes, which is why the total cost is "
                "`n log log n` rather than `n log n`."
            ],
        },
        "quiz_title": "The sieve",
        "quiz": [
            {"q": "Sieving to 100, the largest prime you need a pass for is:",
             "a": ["97", "50", "7", "10"],
             "c": 2,
             "why": "`√100 = 10`, so passes are needed for primes up to 10: 2, 3, 5, 7. "
                    "Anything surviving those is prime."},
            {"q": "Why does the inner loop start at `p²`?",
             "a": ["To save memory",
                   "Multiples of `p` below `p²` have a smaller prime factor and are already crossed out",
                   "`p²` is prime",
                   "It is required for correctness"],
             "c": 1,
             "why": "Correctness is unaffected &mdash; starting at `2p` also works. Starting "
                    "at `p²` avoids repeating work."},
            {"q": "The sieve costs approximately:",
             "a": ["`n²`", "`n log log n`", "`n!`", "`2ⁿ`"],
             "c": 1,
             "why": "`n Σ_{p ≤ √n} 1/p`, and the sum of prime reciprocals grows like "
                    "`log log`. Very nearly linear in practice."},
        ],
        "mistakes": [
            ("Sieving past `√n`",
             "Passes for larger primes remove nothing new. The bound is the same one that "
             "limits trial division."),
            ("Starting the inner loop at `2p`",
             "Correct but wasteful: those multiples have already been removed by smaller "
             "primes."),
            ("Expecting the sieve to scale to cryptographic sizes",
             "It needs memory proportional to `n`. Finding a 1024-bit prime uses "
             "probabilistic testing, not sieving."),
        ],
        "standard": ("Finish when you can predict the passes and the stopping point.",
                     "Before sieving to 200, say which primes need passes and roughly how "
                     "many numbers each will cross out. Then run it and compare &mdash; the "
                     "prediction is the understanding."),
        "note": "The sieve is over two thousand years old and is still the fastest way to "
                "enumerate the primes in a range. Modern variants (segmented sieves, the "
                "sieve of Atkin) improve the constants and the memory profile without "
                "changing the idea.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "greatest-common-divisor",
        "title": "Greatest Common Divisor",
        "module": "The Euclidean algorithm",
        "one_line": "The largest number dividing both, and how not to find it.",
        "summary": (
            "`gcd(a,b)` is the largest common divisor. Computing it from prime "
            "factorisations is correct and impractical; lesson 5's algorithm is what "
            "makes it fast."
        ),
        "key": [
            "gcd(a,b)  largest d with d | a and d | b",
            "lcm(a,b)  smallest positive m with a | m and b | m",
            "gcd(a,b) · lcm(a,b) = |a·b|",
            "coprime:  gcd(a,b) = 1",
        ],
        "key_label": "Two quantities, one identity",
        "concepts_intro": (
            "The definition is immediate; the interesting question is how to compute it "
            "without factoring."
        ),
        "concepts": [
            ("Factorisation gives a formula",
             "Take the minimum exponent of each prime for the gcd, and the maximum for "
             "the lcm. Correct, and it requires factoring both numbers."),
            ("The product identity is exact",
             "`gcd · lcm = |ab|`, because min and max exponents together account for both "
             "exponents at each prime."),
            ("Coprime means no shared factor",
             "`gcd(a,b) = 1`. Consecutive integers are always coprime, which is the fact "
             "the Chinese remainder theorem uses in lesson 10."),
        ],
        "read_title": "gcd and lcm",
        "read_intro": "The definitions, the factorisation formulas, and why they are not the method.",
        "body": [
            ("def", ("Greatest common divisor",
                     "For integers `a, b` not both zero, `gcd(a,b)` is the largest positive "
                     "integer dividing both. `gcd(a, 0) = |a|`.")),
            ("def", ("Least common multiple",
                     "For nonzero `a, b`, `lcm(a,b)` is the smallest positive integer "
                     "divisible by both.")),
            ("thm", ("From the factorisations",
                     "If `a = Π p^{aᵢ}` and `b = Π p^{bᵢ}` over the same set of primes "
                     "(with zero exponents allowed), then "
                     "`gcd(a,b) = Π p^{min(aᵢ,bᵢ)}` and `lcm(a,b) = Π p^{max(aᵢ,bᵢ)}`.")),
            ("proof", [
                "A common divisor may use each prime at most as often as the smaller "
                "exponent allows, and taking exactly that many gives the largest such "
                "divisor. The lcm argument is the mirror image with maxima.",
            ]),
            ("thm", ("The product identity",
                     "`gcd(a,b) · lcm(a,b) = |a · b|`.")),
            ("proof", [
                "At each prime, `min(aᵢ,bᵢ) + max(aᵢ,bᵢ) = aᵢ + bᵢ`. Multiplying over all "
                "primes gives the identity.",
            ]),
            ("p", "The identity is the practical way to get an lcm: compute the gcd by "
                  "Euclid's algorithm and divide. Finding the lcm directly would require "
                  "the factorisations."),
            ("example", ("Both, from factorisations",
                         "`48 = 2⁴·3` and `180 = 2²·3²·5`. "
                         "`gcd = 2^{min(4,2)}·3^{min(1,2)}·5^{min(0,1)} = 4·3 = 12`. "
                         "`lcm = 2⁴·3²·5 = 720`. Check: `12 · 720 = 8640 = 48 · 180`.")),
            ("h3", "Why factorisation is not the method"),
            ("p", "The formula requires factoring both numbers, and factoring is hard. For "
                  "two 100-digit numbers no known method factors them in reasonable time, "
                  "yet Euclid's algorithm computes their gcd in a few hundred divisions."),
            ("p", "This gap is worth noticing. Computing the gcd is easy and factoring is "
                  "hard, even though the formula above expresses the gcd in terms of the "
                  "factorisations. An easy problem can have a hard-looking definition, and "
                  "lesson 5 is the reason this one is easy."),
            ("def", ("Coprime",
                     "`a` and `b` are <strong>coprime</strong> (relatively prime) when "
                     "`gcd(a,b) = 1`: they share no prime factor. A set is "
                     "<strong>pairwise coprime</strong> when every two of its members are.")),
            ("thm", ("Consecutive integers are coprime",
                     "`gcd(n, n+1) = 1` for every `n`.")),
            ("proof", [
                "Any common divisor `d` divides the difference `(n+1) − n = 1`, so "
                "`d = 1`. This is the linear-combination property of lesson 1.",
            ]),
        ],
        "lab": ("number", {
            "mode": "euclid",
            "panel_title": "gcd without factoring",
            "panel_intro": "Enter two large numbers. The algorithm finds the gcd in a "
                           "handful of divisions, having factored neither &mdash; which is "
                           "the point of lesson 5.",
        }),
        "steps_title": "Computing gcd and lcm",
        "steps_intro": "Euclid for the gcd; the identity for the lcm.",
        "steps": [
            ("Use Euclid's algorithm for the gcd",
             "Never factorisation, unless the numbers are tiny or the factorisations are "
             "already known."),
            ("Get the lcm from the identity",
             "`lcm(a,b) = |ab| / gcd(a,b)`. Divide before multiplying to keep the numbers "
             "small."),
            ("Extend to several numbers by associativity",
             "`gcd(a,b,c) = gcd(gcd(a,b), c)`, and similarly for lcm. Note the product "
             "identity does NOT extend to three numbers."),
            ("Check divisibility both ways",
             "The gcd divides both inputs; both inputs divide the lcm. Two free checks."),
        ],
        "worked": {
            "title": "gcd and lcm of 84 and 264",
            "intro": ["Two routes, and a warning about the second."],
            "lines": [
                "BY EUCLID",
                "   264 = 3·84 + 12",
                "    84 = 7·12 +  0     ⟹  gcd = 12",
                "",
                "   lcm = 84 · 264 / 12 = 22176 / 12 = 1848",
                "",
                "BY FACTORISATION (as a check)",
                "    84 = 2² · 3 · 7",
                "   264 = 2³ · 3 · 11",
                "   gcd = 2² · 3 = 12                              ✓",
                "   lcm = 2³ · 3 · 7 · 11 = 1848                   ✓",
                "",
                "Euclid took TWO divisions.  Factorisation took eight, and would",
                "be impossible for 100-digit inputs.",
            ],
            "after": [
                "For three numbers the product identity fails: `gcd(2,4,8) = 2` and "
                "`lcm(2,4,8) = 8`, while the product is 64. The gcd and lcm still extend "
                "by associativity; only the identity relating them does not."
            ],
        },
        "quiz_title": "gcd and lcm",
        "quiz": [
            {"q": "`gcd(12, 18)` equals:",
             "a": ["2", "3", "6", "36"],
             "c": 2,
             "why": "`12 = 2²·3` and `18 = 2·3²`, so the gcd takes `2¹·3¹ = 6`."},
            {"q": "`gcd(a,b) = 4` and `lcm(a,b) = 60`. What is `ab`?",
             "a": ["64", "240", "15", "cannot be determined"],
             "c": 1,
             "why": "`gcd · lcm = |ab| = 240`. The identity determines the product but not "
                    "`a` and `b` individually."},
            {"q": "Why is factorisation a poor method for computing gcds?",
             "a": ["It gives the wrong answer",
                   "Factoring large numbers is computationally hard, while Euclid's algorithm is fast",
                   "It only works for primes",
                   "It requires a computer"],
             "c": 1,
             "why": "The formula is correct. Euclid computes gcds of 100-digit numbers "
                    "instantly; factoring them is beyond any known method."},
        ],
        "mistakes": [
            ("Computing gcds by factoring",
             "Correct and impractical. Euclid's algorithm is the method, and lesson 5 "
             "shows why it terminates so quickly."),
            ("Extending the product identity to three numbers",
             "`gcd(a,b,c)·lcm(a,b,c) ≠ abc` in general. `gcd(2,4,8)` and `lcm(2,4,8)` "
             "multiply to 16, not 64."),
            ("Forgetting `gcd(a,0) = |a|`",
             "It is the base case of Euclid's algorithm, so getting it wrong breaks the "
             "recursion."),
        ],
        "standard": ("Finish when Euclid is your reflex for any gcd.",
                     "Compute `gcd(1071, 462)` and `lcm(1071, 462)` without factoring "
                     "either number. The gcd takes three divisions and the lcm follows "
                     "from the identity."),
        "note": "The gap between computing gcds and factoring is one of the oldest known "
                "examples of two closely related problems with very different difficulty. "
                "RSA in lesson 14 depends on that gap remaining.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "the-euclidean-algorithm",
        "title": "The Euclidean Algorithm",
        "module": "The Euclidean algorithm",
        "one_line": "Replace `(a, b)` by `(b, a mod b)` until the remainder is zero.",
        "summary": (
            "One identity &mdash; `gcd(a,b) = gcd(b, a mod b)` &mdash; repeated. It "
            "terminates quickly, provably: consecutive Fibonacci numbers are the worst "
            "case and the number of steps is logarithmic."
        ),
        "key": [
            "gcd(a, b) = gcd(b, a mod b)          the whole algorithm",
            "gcd(a, 0) = a                        the base case",
            "worst case: consecutive Fibonacci numbers",
            "steps = O(log min(a,b))",
        ],
        "key_label": "One identity, applied repeatedly",
        "concepts_intro": (
            "The algorithm is two lines. The interesting parts are why it is correct and "
            "why it is fast."
        ),
        "concepts": [
            ("The key identity is a one-line proof",
             "Any common divisor of `a` and `b` divides `a − qb`, and conversely. So the "
             "two pairs have the same common divisors, hence the same greatest one."),
            ("It terminates because remainders shrink",
             "Each remainder is strictly smaller than the previous divisor and "
             "non-negative, so the sequence must reach 0."),
            ("It is fast, provably",
             "Two steps at least halve the larger number, so the count is logarithmic. "
             "The worst case is consecutive Fibonacci numbers."),
        ],
        "read_title": "The algorithm",
        "read_intro": "The identity, the correctness proof, and the running-time analysis.",
        "body": [
            ("thm", ("The key identity",
                     "For `b &gt; 0`, `gcd(a, b) = gcd(b, a mod b)`.")),
            ("proof", [
                "Write `a = qb + r` with `r = a mod b`. If `d` divides `a` and `b`, then it "
                "divides `a − qb = r`, so it is a common divisor of `b` and `r`.",
                "Conversely if `d` divides `b` and `r`, then it divides `qb + r = a`, so it "
                "is a common divisor of `a` and `b`.",
                "The two pairs therefore have exactly the same common divisors, so the "
                "greatest is the same.",
            ]),
            ("math", [
                "GCD(a, b):",
                "    while b ≠ 0:",
                "        (a, b) = (b, a mod b)",
                "    return a",
            ]),
            ("p", "<strong>Correctness</strong> is the loop invariant of course 3 lesson "
                  "12: `gcd(a, b)` never changes, by the identity. <strong>Termination</strong> "
                  "holds because `b` strictly decreases and is a non-negative integer. At "
                  "exit `b = 0` and `gcd(a, 0) = a`."),
            ("h3", "How fast"),
            ("thm", ("Two steps halve",
                     "In two iterations, the first argument is at least halved.")),
            ("proof", [
                "If `b ≤ a/2` then `a mod b &lt; b ≤ a/2` and one step suffices. Otherwise "
                "`b &gt; a/2`, so `a = 1·b + (a − b)` and `a mod b = a − b &lt; a/2`.",
                "Either way the value two steps later is below `a/2`, so the number of "
                "iterations is `O(log a)`.",
            ]),
            ("thm", ("Lamé's theorem",
                     "The number of division steps is at most five times the number of "
                     "decimal digits of the smaller input, and the worst case occurs "
                     "exactly for consecutive Fibonacci numbers.")),
            ("p", "Fibonacci inputs are worst because every quotient is 1 &mdash; the "
                  "slowest possible progress. `gcd(F_{n+1}, F_n)` takes `n − 1` steps, and "
                  "since `F_n` grows like `φⁿ`, that is logarithmic in the input. Course 3 "
                  "lesson 10 supplied the growth rate."),
            ("math", [
                "gcd(89, 55):    89 = 1·55 + 34",
                "                55 = 1·34 + 21",
                "                34 = 1·21 + 13",
                "                21 = 1·13 +  8",
                "                13 = 1· 8 +  5",
                "                 8 = 1· 5 +  3",
                "                 5 = 1· 3 +  2",
                "                 3 = 1· 2 +  1",
                "                 2 = 2· 1 +  0     ⟹  gcd = 1",
                "",
                "Every quotient is 1 — the slowest the algorithm can ever go.",
            ]),
            ("p", "By contrast `gcd(1071, 462)` takes three steps despite the numbers being "
                  "much larger. Size is not what determines the step count; the pattern of "
                  "quotients is."),
            ("h3", "In practice"),
            ("p", "Euclid's algorithm computes gcds of thousand-digit numbers in "
                  "milliseconds and is used inside every implementation of RSA, in "
                  "reducing fractions, and in computer algebra generally. It is among the "
                  "oldest algorithms still in daily use, and it has not been improved on "
                  "asymptotically for the general case."),
        ],
        "lab": ("number", {
            "mode": "euclid",
            "panel_title": "Every division, shown",
            "panel_intro": "Try `a = 89`, `b = 55` &mdash; consecutive Fibonacci numbers, "
                           "the worst case, where every quotient is 1. Then try two "
                           "numbers ten times larger and count the steps.",
        }),
        "steps_title": "Running the algorithm",
        "steps_intro": "Divide, keep the remainder, repeat.",
        "steps": [
            ("Divide the larger by the smaller",
             "Record the quotient and the remainder. The quotient is not needed for the "
             "gcd but is needed for lesson 6."),
            ("Replace the pair",
             "`(a, b)` becomes `(b, r)`. The gcd is unchanged, by the identity."),
            ("Repeat until the remainder is 0",
             "The remainders strictly decrease, so this happens."),
            ("Read off the last nonzero remainder",
             "That is the gcd. Equivalently, it is the value of `a` when `b` reaches 0."),
        ],
        "worked": {
            "title": "`gcd(1071, 462)`",
            "intro": ["Three divisions, and a check."],
            "lines": [
                "1071 = 2 · 462 + 147",
                " 462 = 3 · 147 +  21",
                " 147 = 7 ·  21 +   0",
                "",
                "   ⟹  gcd(1071, 462) = 21",
                "",
                "CHECK    1071 = 21 · 51        462 = 21 · 22",
                "         gcd(51, 22) = 1, so 21 is the greatest common divisor.",
                "",
                "By factorisation:  1071 = 3 · 7 · 51 = 3² · 7 · 17",
                "                    462 = 2 · 3 · 7 · 11",
                "                    common: 3 · 7 = 21                    ✓",
            ],
            "after": [
                "Three divisions against the eight or so needed to factor both numbers "
                "&mdash; and the gap widens without limit as the inputs grow. That "
                "asymmetry is the practical content of lesson 4's warning."
            ],
        },
        "quiz_title": "Euclid",
        "quiz": [
            {"q": "`gcd(a, b) = gcd(b, a mod b)` because:",
             "a": ["remainders are smaller",
                   "the two pairs have exactly the same common divisors",
                   "`a mod b &lt; b`",
                   "it is an axiom"],
             "c": 1,
             "why": "Any common divisor of `a` and `b` divides `a − qb = r`, and "
                    "conversely. Same divisor set, same greatest element."},
            {"q": "The worst case for the algorithm is:",
             "a": ["two primes", "consecutive Fibonacci numbers",
                   "powers of 2", "equal numbers"],
             "c": 1,
             "why": "Every quotient is 1, which is the slowest possible progress. "
                    "`gcd(F_{n+1}, F_n)` takes `n − 1` steps."},
            {"q": "The number of steps grows like:",
             "a": ["`√a`", "`log a`", "`a`", "`a²`"],
             "c": 1,
             "why": "Two iterations at least halve the larger argument, so the count is "
                    "logarithmic in the input."},
        ],
        "mistakes": [
            ("Stopping at the wrong point",
             "The gcd is the last NONZERO remainder, which is `a` when `b` becomes 0. "
             "Returning 0 is the classic off-by-one."),
            ("Requiring `a > b` to start",
             "One extra step fixes it automatically: if `a &lt; b` the first division swaps "
             "them."),
            ("Assuming big numbers mean many steps",
             "`gcd(1071, 462)` takes three steps; `gcd(89, 55)` takes nine. The quotients "
             "decide, not the magnitudes."),
        ],
        "standard": ("Finish when you can predict the step count.",
                     "Run the algorithm on `gcd(144, 89)` and count the divisions before "
                     "starting. Consecutive Fibonacci numbers give the maximum, and knowing "
                     "that in advance is the analysis working."),
        "note": "Lesson 6 runs the same divisions backwards to produce Bézout's "
                "coefficients, which is where modular inverses come from &mdash; and "
                "therefore where RSA's private key comes from. The quotients recorded here "
                "are exactly what that needs.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "bezout-and-modular-inverses",
        "title": "Bézout's Identity and Modular Inverses",
        "module": "The Euclidean algorithm",
        "one_line": "The gcd is a linear combination — and that gives inverses.",
        "summary": (
            "`gcd(a,b) = ax + by` for some integers `x, y`, found by running Euclid's "
            "algorithm backwards. When `gcd(a,m) = 1` the coefficient of `a` is its "
            "inverse modulo `m`."
        ),
        "key": [
            "gcd(a,b) = ax + by            Bézout's identity",
            "extended Euclid produces x and y",
            "gcd(a,m) = 1  ⟹  ax ≡ 1 (mod m),  so x = a⁻¹",
            "Euclid's lemma:  p | ab  ⟹  p | a  or  p | b",
        ],
        "key_label": "The gcd, constructively",
        "concepts_intro": (
            "Bézout upgrades the gcd from a number to an identity, and the identity is "
            "what produces inverses and proves unique factorisation."
        ),
        "concepts": [
            ("The gcd is the smallest positive combination",
             "`{ax + by}` over all integers `x, y` is exactly the set of multiples of "
             "`gcd(a,b)`, so the gcd is its smallest positive member."),
            ("The coefficients come from running Euclid backwards",
             "Each division `a = qb + r` gives `r = a − qb`; substituting upward expresses "
             "the gcd in terms of the original inputs."),
            ("Coprimality gives an inverse",
             "`ax + my = 1` reduces mod `m` to `ax ≡ 1`, so `x` is `a⁻¹`. This is where "
             "every modular inverse in this course comes from."),
        ],
        "read_title": "Bézout",
        "read_intro": "The identity, the extended algorithm, and the two theorems it unlocks.",
        "body": [
            ("thm", ("Bézout's identity",
                     "For integers `a, b` not both zero there are integers `x, y` with "
                     "`ax + by = gcd(a,b)`. Moreover `gcd(a,b)` is the smallest positive "
                     "integer expressible in that form.")),
            ("proof", [
                "Let `S = {ax + by : x, y ∈ ℤ, ax + by &gt; 0}`, which is nonempty (it "
                "contains `|a|`). By well-ordering it has a least element `d = ax₀ + by₀`.",
                "Divide: `a = qd + r` with `0 ≤ r &lt; d`. Then "
                "`r = a − qd = a(1 − qx₀) + b(−qy₀)`, which is of the required form. Since "
                "`0 ≤ r &lt; d` and `d` is the smallest positive such value, `r = 0`, so "
                "`d | a`. Similarly `d | b`, so `d` is a common divisor.",
                "Any common divisor `c` of `a` and `b` divides `ax₀ + by₀ = d`, so "
                "`c ≤ d`. Hence `d = gcd(a,b)`.",
            ]),
            ("h3", "The extended Euclidean algorithm"),
            ("p", "The proof establishes existence; the algorithm produces the "
                  "coefficients. Run Euclid forward recording the quotients, then "
                  "substitute backwards."),
            ("math", [
                "gcd(1071, 462):",
                "   1071 = 2·462 + 147        ⟹  147 = 1071 − 2·462",
                "    462 = 3·147 +  21        ⟹   21 =  462 − 3·147",
                "    147 = 7· 21 +   0",
                "",
                "Back-substitute:",
                "    21 = 462 − 3·147",
                "       = 462 − 3(1071 − 2·462)",
                "       = 462 − 3·1071 + 6·462",
                "       = 7·462 − 3·1071",
                "",
                "So  1071·(−3) + 462·(7) = 21 = gcd.        ✓",
            ]),
            ("p", "The iterative form maintains the coefficients as it goes and avoids the "
                  "back-substitution entirely; it is what the lab runs and what every "
                  "implementation uses."),
            ("thm", ("Modular inverses",
                     "`a` has an inverse modulo `m` &mdash; an `x` with `ax ≡ 1 (mod m)` "
                     "&mdash; if and only if `gcd(a, m) = 1`. The inverse is then unique "
                     "modulo `m`.")),
            ("proof", [
                "If `gcd(a,m) = 1`, Bézout gives `ax + my = 1`, and reducing modulo `m` "
                "leaves `ax ≡ 1`.",
                "Conversely if `ax ≡ 1 (mod m)` then `ax − 1 = my` for some `y`, so "
                "`ax − my = 1`, and any common divisor of `a` and `m` divides 1.",
                "For uniqueness: if `ax ≡ ax' ≡ 1` then `x ≡ x(ax') = (xa)x' ≡ x'`.",
            ]),
            ("p", "This is the theorem RSA runs on. The private exponent `d` is the inverse "
                  "of the public exponent `e` modulo `φ(n)`, and it is computed by exactly "
                  "this algorithm."),
            ("thm", ("Euclid's lemma",
                     "If a prime `p` divides `ab`, then `p | a` or `p | b`.")),
            ("proof", [
                "Suppose `p ∤ a`. Since `p` is prime, `gcd(p, a) = 1`, so Bézout gives "
                "`px + ay = 1`. Multiplying by `b`: `pbx + aby = b`.",
                "`p` divides `pbx`, and `p` divides `ab` hence `aby`. So `p` divides their "
                "sum, which is `b`.",
            ]),
            ("p", "Euclid's lemma is what makes prime factorisation unique, so lesson 2's "
                  "fundamental theorem rests on Bézout, which rests on well-ordering. The "
                  "chain of dependency is worth noticing: the most familiar fact in the "
                  "course has the deepest justification."),
        ],
        "lab": ("number", {
            "mode": "bezout",
            "panel_title": "The coefficients, computed",
            "panel_intro": "The lab prints `x` and `y` with the identity verified. Try "
                           "coprime inputs and note that `x` is then the inverse of `a` "
                           "modulo `b`.",
        }),
        "steps_title": "Finding Bézout coefficients",
        "steps_intro": "Forward for the gcd, backward for the coefficients.",
        "steps": [
            ("Run Euclid and record every quotient",
             "Each line `a = qb + r` will be rearranged as `r = a − qb`."),
            ("Start from the last nonzero remainder",
             "That is the gcd. Express it using the line that produced it."),
            ("Substitute upward, one line at a time",
             "Replace each remainder by its expression in earlier terms, collecting "
             "coefficients as you go."),
            ("Verify the identity",
             "Compute `ax + by` and check it equals the gcd. A sign error here is easy and "
             "the check is one multiplication."),
        ],
        "worked": {
            "title": "The inverse of 17 modulo 3120",
            "intro": ["The computation RSA needs, on the standard textbook key."],
            "lines": [
                "3120 = 183·17 + 9",
                "  17 =   1· 9 + 8",
                "   9 =   1· 8 + 1",
                "   8 =   8· 1 + 0        ⟹  gcd = 1, so an inverse exists",
                "",
                "Back-substitute:",
                "   1 = 9 − 1·8",
                "     = 9 − 1(17 − 1·9)          = 2·9 − 1·17",
                "     = 2(3120 − 183·17) − 1·17  = 2·3120 − 367·17",
                "",
                "So  −367 · 17 ≡ 1 (mod 3120),  and  −367 + 3120 = 2753",
                "",
                "   17 · 2753 = 46 801 = 15 · 3120 + 1        ✓",
                "",
                "2753 is the private exponent d for the RSA key in lesson 14.",
            ],
            "after": [
                "The negative coefficient is normal and is corrected by adding the modulus. "
                "This calculation is the entire key-generation step of RSA: everything else "
                "is multiplication and exponentiation."
            ],
        },
        "quiz_title": "Bézout",
        "quiz": [
            {"q": "`a` has an inverse modulo `m` if and only if:",
             "a": ["`a &lt; m`", "`gcd(a, m) = 1`", "`m` is prime", "`a` is prime"],
             "c": 1,
             "why": "Bézout gives `ax + my = 1` exactly when the gcd is 1, and reducing "
                    "mod `m` makes `x` the inverse."},
            {"q": "Bézout's identity says `gcd(a,b)` is:",
             "a": ["the product of `a` and `b`",
                   "expressible as `ax + by` for some integers `x, y`",
                   "always 1",
                   "the smallest of `a` and `b`"],
             "c": 1,
             "why": "And it is the smallest positive such combination, which is how the "
                    "proof identifies it."},
            {"q": "Euclid's lemma is needed to prove:",
             "a": ["the division algorithm",
                   "uniqueness of prime factorisation",
                   "that there are infinitely many primes",
                   "the sieve is correct"],
             "c": 1,
             "why": "Existence of a factorisation is straightforward induction; uniqueness "
                    "needs the lemma, which needs Bézout."},
        ],
        "mistakes": [
            ("Leaving a negative inverse unreduced",
             "`−367` is correct and `2753` is the representative in `[0, m)`. Both satisfy "
             "the congruence; only one is conventional."),
            ("Looking for an inverse when the gcd is not 1",
             "None exists. Checking the gcd first costs one run of Euclid and saves the "
             "search."),
            ("Making a sign error in back-substitution",
             "Verify `ax + by = gcd` at the end. One multiplication, and it catches the "
             "error every time."),
        ],
        "standard": ("Finish when you can produce a modular inverse on demand.",
                     "Find the inverse of 7 modulo 26 by the extended algorithm and verify "
                     "it. That is the decryption key for the affine cipher in lesson 13, "
                     "and the same computation scaled up is RSA's private exponent."),
        "note": "Bézout is the constructive content of the gcd. Knowing that a common "
                "divisor is greatest is a fact; knowing how to write it as a combination "
                "is a tool, and every modular inverse in cryptography comes from it.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "modular-arithmetic",
        "title": "Modular Arithmetic",
        "module": "Congruences",
        "one_line": "Arithmetic on remainders, and why it is well defined.",
        "summary": (
            "`a ≡ b (mod m)` when `m | (a − b)`. Congruence is an equivalence relation, "
            "addition and multiplication respect it, and cancellation is where it stops "
            "behaving like ordinary arithmetic."
        ),
        "key": [
            "a ≡ b (mod m)   ⟺   m | (a − b)",
            "congruences ADD and MULTIPLY like equations",
            "CANCELLATION FAILS:  2·3 ≡ 2·8 (mod 10) but 3 ≢ 8",
            "cancel a only when gcd(a, m) = 1",
        ],
        "key_label": "Almost ordinary arithmetic",
        "concepts_intro": (
            "Congruence is course 2's equivalence relation applied to the integers, and "
            "the classes support arithmetic."
        ),
        "concepts": [
            ("Congruence is an equivalence relation",
             "Reflexive, symmetric, transitive &mdash; so it partitions `ℤ` into `m` "
             "classes, one per remainder."),
            ("Addition and multiplication are well defined",
             "The result's class depends only on the inputs' classes, which is what makes "
             "arithmetic on classes legitimate."),
            ("Cancellation needs coprimality",
             "`ac ≡ bc (mod m)` gives `a ≡ b` only when `gcd(c, m) = 1`. This is the one "
             "familiar rule that fails."),
        ],
        "read_title": "Congruence",
        "read_intro": "The definition, the well-definedness proof, and the rule that fails.",
        "body": [
            ("def", ("Congruence",
                     "For `m &gt; 0`, `a ≡ b (mod m)` means `m | (a − b)`; equivalently, "
                     "`a` and `b` leave the same remainder on division by `m`.")),
            ("thm", ("Congruence is an equivalence relation",
                     "It is reflexive (`m | 0`), symmetric (`m | (a−b)` gives `m | (b−a)`) "
                     "and transitive (`m | (a−b)` and `m | (b−c)` give `m | (a−c)` by the "
                     "linear-combination property).")),
            ("p", "By course 2 lesson 8 it therefore partitions `ℤ` into equivalence "
                  "classes. There are exactly `m` of them, one for each remainder "
                  "`0, 1, …, m−1`, and the set of classes is written `ℤ/mℤ` or `ℤ_m`."),
            ("thm", ("Arithmetic is well defined",
                     "If `a ≡ b (mod m)` and `c ≡ d (mod m)`, then `a + c ≡ b + d` and "
                     "`ac ≡ bd (mod m)`.")),
            ("proof", [
                "Write `a = b + ms` and `c = d + mt`. Then "
                "`a + c = (b + d) + m(s + t)`, so the sums are congruent.",
                "And `ac = (b + ms)(d + mt) = bd + m(bt + ds + mst)`, so the products are "
                "congruent.",
            ]),
            ("p", "This is the well-definedness check course 2 lesson 10 warned about, "
                  "carried out. It says arithmetic on classes is legitimate: the answer "
                  "does not depend on which representatives were used, so `[3] + [4] = [7]` "
                  "is a statement about classes rather than about the numbers 3 and 4."),
            ("p", "The practical consequence is that a computation may be reduced at any "
                  "point. To find `17 · 23 (mod 5)`, reduce first: `2 · 3 = 6 ≡ 1`, rather "
                  "than computing 391 and dividing."),
            ("h3", "Where it stops being ordinary arithmetic"),
            ("example", ("Cancellation fails",
                         "`2 · 3 = 6 ≡ 16 = 2 · 8 (mod 10)`, and yet `3 ≢ 8 (mod 10)`. The "
                         "factor 2 cannot be cancelled because `gcd(2, 10) = 2 ≠ 1`.")),
            ("thm", ("Cancellation law",
                     "If `ac ≡ bc (mod m)` and `gcd(c, m) = 1`, then `a ≡ b (mod m)`.")),
            ("proof", [
                "`gcd(c,m) = 1` gives an inverse `c⁻¹` by lesson 6. Multiplying both sides "
                "by it leaves `a ≡ b`.",
            ]),
            ("example", ("Zero divisors",
                         "`2 · 5 = 10 ≡ 0 (mod 10)` with neither factor zero. In `ℤ_10` "
                         "there are nonzero elements whose product is zero &mdash; "
                         "impossible in `ℤ`, and the reason `ℤ_10` is not a field.")),
            ("thm", ("Prime moduli behave best",
                     "`ℤ_p` for prime `p` has no zero divisors and every nonzero element "
                     "has an inverse: it is a field. For composite `m`, exactly the "
                     "elements coprime to `m` are invertible, and there are `φ(m)` of them.")),
            ("h3", "Casting out nines"),
            ("example", ("A check on arithmetic",
                         "Since `10 ≡ 1 (mod 9)`, any number is congruent mod 9 to its "
                         "digit sum. To check `4321 × 5678 = 24 534 638`: digit sums are "
                         "10 ≡ 1 and 26 ≡ 8, product `8`; the claimed answer has digit sum "
                         "35 ≡ 8. Consistent &mdash; and the check would catch most single "
                         "digit errors, though not a transposition.")),
        ],
        "lab": ("number", {
            "mode": "modtable",
            "panel_title": "The tables",
            "panel_intro": "Compare a prime modulus with a composite one. In the prime "
                           "case every nonzero row of the multiplication table is a "
                           "permutation; in the composite case some rows contain zeros.",
        }),
        "steps_title": "Computing modulo `m`",
        "steps_intro": "Reduce early and often.",
        "steps": [
            ("Reduce the inputs first",
             "`17 · 23 (mod 5)` is `2 · 3 (mod 5)`. Well-definedness is what makes this "
             "legitimate and it keeps the numbers small."),
            ("Add and multiply freely",
             "Both operations respect congruence. Subtraction too, since it is addition of "
             "a negative."),
            ("Do not cancel without checking the gcd",
             "`ac ≡ bc` gives `a ≡ b` only when `gcd(c,m) = 1`. This is the rule that "
             "catches people."),
            ("Reduce the final answer into `[0, m)`",
             "Add `m` if the result is negative. Conventional representatives make answers "
             "comparable."),
        ],
        "worked": {
            "title": "The last digit of `7¹⁰⁰`",
            "intro": ["That is `7¹⁰⁰ mod 10`, and the powers cycle."],
            "lines": [
                "7¹ ≡ 7      7² ≡ 49 ≡ 9      7³ ≡ 63 ≡ 3      7⁴ ≡ 21 ≡ 1  (mod 10)",
                "",
                "The powers cycle with period 4:  7, 9, 3, 1, 7, 9, 3, 1, …",
                "",
                "100 = 4 · 25,  so  7¹⁰⁰ = (7⁴)²⁵ ≡ 1²⁵ = 1  (mod 10)",
                "",
                "The last digit of 7¹⁰⁰ is 1.",
                "",
                "7¹⁰⁰ has 85 digits.  We found its last one with four multiplications",
                "and a division.",
            ],
            "after": [
                "The cycle length 4 is not a coincidence: `φ(10) = 4`, and Euler's theorem "
                "in lesson 11 guarantees `7^{φ(10)} ≡ 1` whenever `gcd(7,10) = 1`. Lesson "
                "8 turns this into a general algorithm."
            ],
        },
        "quiz_title": "Modular arithmetic",
        "quiz": [
            {"q": "`17 ≡ ? (mod 5)`",
             "a": ["3", "2", "12", "17"],
             "c": 1,
             "why": "`17 = 3·5 + 2`, so `17 ≡ 2 (mod 5)`."},
            {"q": "`6a ≡ 6b (mod 9)`. Can you conclude `a ≡ b (mod 9)`?",
             "a": ["Yes", "No, because `gcd(6, 9) = 3 ≠ 1`",
                   "Only if `a` and `b` are positive", "Only if 9 is prime"],
             "c": 1,
             "why": "Cancellation needs the factor coprime to the modulus. Here "
                    "`6·1 ≡ 6·4 (mod 9)` while `1 ≢ 4`."},
            {"q": "In `ℤ_12`, which elements have multiplicative inverses?",
             "a": ["all of them", "the primes", "1, 5, 7, 11", "only 1"],
             "c": 2,
             "why": "Exactly those coprime to 12, and there are `φ(12) = 4` of them."},
        ],
        "mistakes": [
            ("Cancelling a common factor without checking the gcd",
             "The one familiar rule that fails. `2·3 ≡ 2·8 (mod 10)` with `3 ≢ 8`."),
            ("Reducing exponents modulo `m`",
             "`a^b (mod m)` does not let you reduce `b` mod `m`. Exponents reduce modulo "
             "`φ(m)`, which is lesson 11."),
            ("Leaving negative representatives",
             "Correct but unconventional. Add `m` to land in `[0, m)`."),
        ],
        "standard": ("Finish when you reduce before multiplying, automatically.",
                     "Compute `123 · 456 (mod 7)` by reducing each factor first. Two small "
                     "multiplications rather than one large one, and the answer is the same "
                     "because congruence respects multiplication."),
        "note": "Modular arithmetic is the arithmetic of `ℤ/mℤ`, the quotient of the "
                "integers by an equivalence relation. Course 2 lesson 8 built exactly that "
                "structure; this course computes in it.",
    },
]
