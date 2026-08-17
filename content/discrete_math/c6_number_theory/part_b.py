"""Course 6, lessons 08-14 — congruences, theorems, and cryptography."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "modular-exponentiation",
        "title": "Modular Exponentiation",
        "module": "Congruences",
        "one_line": "Compute `aᵇ mod m` without ever forming `aᵇ`.",
        "summary": (
            "Repeated squaring computes `aᵇ mod m` in about `2 log₂ b` multiplications "
            "rather than `b` of them, reducing at every step so the numbers stay small. "
            "It is what makes RSA possible."
        ),
        "key": [
            "square and multiply:  read the exponent in binary",
            "reduce mod m at EVERY step",
            "cost: about 2·log₂(b) multiplications, not b",
            "7^128 mod 13 in 8 squarings, not 128 multiplications",
        ],
        "key_label": "Logarithmic, not linear",
        "concepts_intro": (
            "Two ideas, each essential: halve the exponent by squaring, and reduce the "
            "numbers by the modulus."
        ),
        "concepts": [
            ("Squaring halves the exponent",
             "`a^{2k} = (a^k)²`, so each squaring doubles the exponent reached. Reading "
             "`b` in binary tells you which squarings to multiply in."),
            ("Reducing keeps the numbers small",
             "Without reducing, `a^b` for a 1024-bit `b` has more digits than there are "
             "atoms in the universe. With reducing, every intermediate is below `m²`."),
            ("Both are necessary",
             "Fast exponentiation without reduction produces unrepresentable numbers; "
             "reduction without fast exponentiation takes `b` multiplications."),
        ],
        "read_title": "Square and multiply",
        "read_intro": "The algorithm, the cost, and why RSA depends on it.",
        "body": [
            ("math", [
                "MODPOW(a, b, m):",
                "    result = 1",
                "    base   = a mod m",
                "    while b > 0:",
                "        if b is odd:  result = (result · base) mod m",
                "        base = (base · base) mod m",
                "        b    = b div 2",
                "    return result",
            ]),
            ("p", "The loop reads `b` in binary from the least significant bit. `base` "
                  "holds `a^{2^i} mod m` at step `i`, and the result accumulates exactly "
                  "those powers whose bit is set. Since "
                  "`b = Σ bᵢ2ⁱ`, the product of the selected powers is `a^b`."),
            ("thm", ("Correctness",
                     "MODPOW returns `a^b mod m`.")),
            ("proof", [
                "The loop invariant is `result · base^b ≡ a^{b₀} (mod m)`, where `b₀` is "
                "the original exponent.",
                "Initially `result = 1` and `base = a`, so it holds. If `b` is even, "
                "`base^b = (base²)^{b/2}`, and the update preserves it. If `b` is odd, "
                "`base^b = base · (base²)^{(b−1)/2}`, and multiplying `result` by `base` "
                "before the halving preserves it.",
                "At exit `b = 0`, so the invariant reads `result ≡ a^{b₀}`.",
            ]),
            ("h3", "The cost"),
            ("p", "The loop runs `⌊log₂ b⌋ + 1` times, with one squaring per iteration and "
                  "at most one extra multiplication. So the total is at most about "
                  "`2 log₂ b` modular multiplications."),
            ("math", [
                "b = 128:      naive 128 multiplications,  fast 8 squarings",
                "b = 10⁶:      naive a million,            fast about 20 squarings",
                "b = 2¹⁰²⁴:    naive impossible,           fast about 1024 squarings",
            ]),
            ("example", ("`7^128 mod 13`",
                         "`7² = 49 ≡ 10`; `10² = 100 ≡ 9`; `9² = 81 ≡ 3`; `3² = 9`; "
                         "`9² = 81 ≡ 3`; `3² ≡ 9`; `9² ≡ 3`. Since `128 = 2⁷`, seven "
                         "squarings give `7^128 ≡ 3 (mod 13)`. No number above 144 ever "
                         "appeared.")),
            ("p", "That bound is the second essential point: every intermediate is a "
                  "product of two numbers below `m`, hence below `m²`. For a 2048-bit "
                  "modulus the intermediates are 4096 bits, which is entirely routine, "
                  "while `a^b` itself would have about `2^1024` bits."),
            ("h3", "Where it is used"),
            ("ul", [
                "<strong>RSA</strong> (lesson 14): both encryption and decryption are a "
                "single modular exponentiation, with 2048-bit exponents.",
                "<strong>Diffie&ndash;Hellman key exchange</strong> and the whole family of "
                "discrete-logarithm systems.",
                "<strong>Primality testing</strong>: Fermat and Miller&ndash;Rabin both "
                "compute `a^{n−1} mod n`, which is only feasible this way.",
            ]),
            ("p", "It is worth appreciating the asymmetry the algorithm creates. Computing "
                  "`a^b mod m` is fast; recovering `b` from `a`, `a^b mod m` and `m` "
                  "&mdash; the discrete logarithm &mdash; is believed hard. A great deal of "
                  "cryptography lives in that gap."),
        ],
        "lab": ("number", {
            "mode": "modexp",
            "panel_title": "Every squaring, traced",
            "panel_intro": "Each row is one bit of the exponent. The running result only "
                           "updates on set bits, and no intermediate ever exceeds `m²`.",
        }),
        "steps_title": "Computing a modular power",
        "steps_intro": "Binary exponent, reduce every step.",
        "steps": [
            ("Write the exponent in binary",
             "`100 = 1100100₂`. The set bits are the powers you will multiply in."),
            ("Square repeatedly, reducing each time",
             "`a`, `a²`, `a⁴`, `a⁸`, … each reduced mod `m`. Never let a value exceed `m²`."),
            ("Multiply in the powers matching set bits",
             "Reducing after every multiplication. The order does not matter."),
            ("Check the size of every intermediate",
             "If a number larger than `m²` appears, a reduction was skipped and the "
             "advantage is lost."),
        ],
        "worked": {
            "title": "`3^200 mod 50`",
            "intro": ["`200 = 11001000₂`, so the set bits are at positions 3, 6 and 7."],
            "lines": [
                "bit  power of 3      value mod 50     used?",
                " 0   3^1                 3             no",
                " 1   3^2                 9             no",
                " 2   3^4                31             no      (9² = 81 ≡ 31)",
                " 3   3^8                11             YES     (31² = 961 ≡ 11)",
                " 4   3^16               21             no      (11² = 121 ≡ 21)",
                " 5   3^32               41             no      (21² = 441 ≡ 41)",
                " 6   3^64               31             YES     (41² = 1681 ≡ 31)",
                " 7   3^128              11             YES     (31² ≡ 11)",
                "",
                "result = 11 · 31 · 11 mod 50",
                "       = 341 mod 50 · 11 = 41 · 11 = 451 ≡ 1  (mod 50)",
                "",
                "8 squarings and 3 multiplications, against 199 the naive way.",
            ],
            "after": [
                "The powers began repeating &mdash; `3^4 ≡ 3^64 ≡ 31` &mdash; because the "
                "multiplicative order of 3 modulo 50 divides `φ(50) = 20`. Lesson 11 "
                "explains that, and it is why the answer came out as 1."
            ],
        },
        "quiz_title": "Modular exponentiation",
        "quiz": [
            {"q": "About how many multiplications does `a^1000 mod m` need by square and multiply?",
             "a": ["1000", "about 20", "about 500", "about 100"],
             "c": 1,
             "why": "`2 log₂ 1000 ≈ 20`. Ten squarings and at most ten extra "
                    "multiplications, one per set bit."},
            {"q": "Why reduce mod `m` at every step?",
             "a": ["To get the right answer",
                   "To keep every intermediate below `m²` instead of astronomically large",
                   "It is optional",
                   "To make the exponent smaller"],
             "c": 1,
             "why": "The answer would be the same without reducing; the numbers would be "
                    "unrepresentable. Reduction is what makes it computable."},
            {"q": "RSA encryption of one block is:",
             "a": ["a factorisation", "a single modular exponentiation",
                   "a gcd computation", "a table lookup"],
             "c": 1,
             "why": "`c = m^e mod n`. Decryption is `c^d mod n`. Both are this algorithm "
                    "with 2048-bit exponents."},
        ],
        "mistakes": [
            ("Reducing the exponent modulo `m`",
             "Exponents reduce modulo `φ(m)`, not `m`, and only when the base is coprime "
             "to `m`. Lesson 11 states the rule."),
            ("Computing `a^b` before reducing",
             "The intermediate is astronomically large. Reducing at every step is the "
             "whole point."),
            ("Multiplying in the wrong powers",
             "Only the set bits of the exponent contribute. Writing `b` in binary first "
             "makes this mechanical."),
        ],
        "standard": ("Finish when you can trace the algorithm on paper.",
                     "Compute `5^117 mod 19` by square and multiply, writing 117 in binary "
                     "first. Seven squarings and four multiplications, and no intermediate "
                     "above 361."),
        "note": "The same algorithm works for any associative operation: matrix powers, "
                "compositions of functions, and group elements generally. The exponent's "
                "binary expansion is what is being exploited, and multiplication is "
                "incidental.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "linear-congruences",
        "title": "Linear Congruences",
        "module": "Congruences",
        "one_line": "`ax ≡ b (mod m)`: solvable exactly when `gcd(a,m)` divides `b`.",
        "summary": (
            "The modular analogue of a linear equation. It has either no solutions or "
            "exactly `gcd(a,m)` of them, and which case you are in is decided before any "
            "work is done."
        ),
        "key": [
            "ax ≡ b (mod m)   solvable  ⟺  g = gcd(a,m) divides b",
            "then there are EXACTLY g solutions mod m",
            "they are spaced m/g apart",
            "if g = 1 the solution is x ≡ a⁻¹b, unique",
        ],
        "key_label": "Zero, one, or several",
        "concepts_intro": (
            "Unlike a linear equation over the reals, this can have no solutions or many "
            "&mdash; and the gcd decides which."
        ),
        "concepts": [
            ("Solvability is a divisibility test",
             "`g = gcd(a,m)` must divide `b`. That check is one gcd computation and it "
             "settles the question."),
            ("The solution count is exactly `g`",
             "Not one, and not `m`. The solutions form one class modulo `m/g`, which "
             "splits into `g` classes modulo `m`."),
            ("Coprime is the clean case",
             "`gcd(a,m) = 1` gives a unique solution `x ≡ a⁻¹b`, computed by the extended "
             "algorithm of lesson 6."),
        ],
        "read_title": "Solving `ax ≡ b (mod m)`",
        "read_intro": "The criterion, the count, and the method.",
        "body": [
            ("thm", ("Solvability and count",
                     "Let `g = gcd(a, m)`. The congruence `ax ≡ b (mod m)` has a solution "
                     "if and only if `g | b`, and in that case it has exactly `g` solutions "
                     "modulo `m`.")),
            ("proof", [
                "`ax ≡ b (mod m)` means `ax − my = b` for some integer `y`. By Bézout the "
                "set of values `ax − my` is exactly the multiples of `g`, so a solution "
                "exists precisely when `g | b`.",
                "Suppose `g | b` and divide through: `(a/g)x ≡ (b/g) (mod m/g)`. Now "
                "`gcd(a/g, m/g) = 1`, so this reduced congruence has a unique solution "
                "`x₀` modulo `m/g`.",
                "Lifting back, the solutions modulo `m` are "
                "`x₀, x₀ + m/g, x₀ + 2m/g, …, x₀ + (g−1)m/g` &mdash; exactly `g` of them.",
            ]),
            ("example", ("No solution",
                         "`6x ≡ 7 (mod 15)`. `gcd(6,15) = 3` and `3 ∤ 7`, so there is no "
                         "solution at all. Note that this is decided in one line, before "
                         "any attempt to solve.")),
            ("example", ("Three solutions",
                         "`6x ≡ 9 (mod 15)`. `gcd(6,15) = 3` and `3 | 9`, so three "
                         "solutions exist. Divide through: `2x ≡ 3 (mod 5)`, and since "
                         "`2⁻¹ ≡ 3 (mod 5)`, `x ≡ 9 ≡ 4 (mod 5)`. Lifting: "
                         "`x ≡ 4, 9, 14 (mod 15)`. Check: `6·4 = 24 ≡ 9`, `6·9 = 54 ≡ 9`, "
                         "`6·14 = 84 ≡ 9`. All three work.")),
            ("example", ("One solution",
                         "`7x ≡ 3 (mod 26)`. `gcd(7,26) = 1`, so exactly one solution. The "
                         "inverse of 7 mod 26 is 15, since `7 · 15 = 105 = 4·26 + 1`. So "
                         "`x ≡ 45 ≡ 19 (mod 26)`.")),
            ("h3", "Why the count is the gcd"),
            ("p", "The reduced congruence lives modulo `m/g` and has one solution there. "
                  "Each class modulo `m/g` contains exactly `g` classes modulo `m`, so one "
                  "solution downstairs becomes `g` upstairs. Answering \"one\" or \"m\" "
                  "both miss this, and the count matters for the systems of lesson 10."),
            ("h3", "Comparison with ordinary linear equations"),
            ("math", [
                "over ℝ            ax = b            exactly one solution when a ≠ 0",
                "mod m             ax ≡ b (mod m)    zero, or exactly gcd(a,m) solutions",
                "",
                "The difference: ℝ is a field, so every nonzero a is invertible.",
                "ℤ_m is a field only when m is prime.",
            ]),
            ("p", "That is the structural explanation. Over a field every nonzero "
                  "coefficient can be divided out; modulo a composite `m` it cannot, and "
                  "the failure is measured exactly by the gcd."),
        ],
        "lab": ("number", {
            "mode": "congr",
            "panel_title": "Solve, or prove unsolvable",
            "panel_intro": "The lab reports the gcd first, because that decides everything. "
                           "Try `a = 6`, `b = 7`, `m = 15` for the unsolvable case and "
                           "`b = 9` for three solutions.",
        }),
        "steps_title": "Solving a linear congruence",
        "steps_intro": "Compute the gcd first; it answers most of the question.",
        "steps": [
            ("Compute `g = gcd(a, m)`",
             "One run of Euclid. If `g ∤ b`, there is no solution and you are finished."),
            ("Divide the congruence through by `g`",
             "All three of `a`, `b` and the modulus. The reduced coefficient is now coprime "
             "to the reduced modulus."),
            ("Invert and solve",
             "`x ≡ (a/g)⁻¹(b/g) (mod m/g)`, using the extended algorithm of lesson 6."),
            ("Lift to the original modulus",
             "Add multiples of `m/g` to produce all `g` solutions modulo `m`, and check at "
             "least one by substitution."),
        ],
        "worked": {
            "title": "`14x ≡ 30 (mod 100)`",
            "intro": ["A case with several solutions, worked in full."],
            "lines": [
                "g = gcd(14, 100) = 2,   and  2 | 30,  so TWO solutions exist.",
                "",
                "Divide through by 2:      7x ≡ 15 (mod 50)",
                "",
                "Invert 7 modulo 50:  7 · 43 = 301 = 6·50 + 1,  so 7⁻¹ ≡ 43",
                "",
                "   x ≡ 43 · 15 = 645 ≡ 645 − 12·50 = 45   (mod 50)",
                "",
                "Lift to modulus 100:      x ≡ 45  and  x ≡ 95",
                "",
                "CHECK   14 · 45 = 630 = 6·100 + 30      ✓",
                "        14 · 95 = 1330 = 13·100 + 30    ✓",
            ],
            "after": [
                "Both checks were worth doing: the lift is the step where a solution is "
                "most often lost. Reporting only `x ≡ 45` would be half an answer, and "
                "reporting `x ≡ 45 (mod 50)` would be a correct statement about the wrong "
                "modulus."
            ],
        },
        "quiz_title": "Linear congruences",
        "quiz": [
            {"q": "`4x ≡ 6 (mod 8)`. How many solutions modulo 8?",
             "a": ["0", "1", "2", "4"],
             "c": 0,
             "why": "`gcd(4,8) = 4` and `4 ∤ 6`, so there is no solution. `4x` is always "
                    "`0` or `4` modulo 8."},
            {"q": "`ax ≡ b (mod m)` with `gcd(a,m) = 3` and `3 | b`. The number of solutions is:",
             "a": ["1", "3", "`m`", "`m/3`"],
             "c": 1,
             "why": "Exactly `gcd(a,m) = 3` solutions modulo `m`, spaced `m/3` apart."},
            {"q": "When is the solution unique modulo `m`?",
             "a": ["always", "when `gcd(a,m) = 1`", "when `m` is prime", "when `b = 1`"],
             "c": 1,
             "why": "Coprimality makes `a` invertible, and the solution is `x ≡ a⁻¹b`. A "
                    "prime modulus guarantees it for every `a` not divisible by `m`."},
        ],
        "mistakes": [
            ("Reporting only one solution when there are `g`",
             "The lift back to modulus `m` produces `g` classes. Stopping after the reduced "
             "congruence gives a correct statement about the wrong modulus."),
            ("Attempting to solve before checking the gcd",
             "One gcd computation decides solvability. Without it you can search a long "
             "time for a solution that does not exist."),
            ("Dividing only the coefficient by `g`",
             "All three of `a`, `b` and `m` must be divided. Leaving the modulus alone "
             "gives the wrong solution set."),
        ],
        "standard": ("Finish when the gcd is the first thing you compute.",
                     "Solve `15x ≡ 25 (mod 35)`, stating the number of solutions before "
                     "finding any. `gcd(15,35) = 5` divides 25, so there are five, spaced "
                     "7 apart."),
        "note": "The same criterion governs the linear Diophantine equation `ax + by = c`, "
                "which is solvable in integers exactly when `gcd(a,b) | c`. The two "
                "statements are the same theorem written with and without congruence "
                "notation.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "chinese-remainder-theorem",
        "title": "The Chinese Remainder Theorem",
        "module": "Congruences",
        "one_line": "Simultaneous congruences with coprime moduli have exactly one solution.",
        "summary": (
            "Given remainders modulo pairwise coprime numbers, there is exactly one "
            "integer modulo their product with those remainders. It is constructive, and "
            "it is why RSA implementations run about four times faster than the naive "
            "method."
        ),
        "key": [
            "x ≡ a₁ (mod m₁), …, x ≡ a_k (mod m_k)   with mᵢ PAIRWISE COPRIME",
            "⟹  a unique solution modulo M = m₁⋯m_k",
            "x = Σ aᵢ Mᵢ yᵢ   where Mᵢ = M/mᵢ  and  yᵢ = Mᵢ⁻¹ mod mᵢ",
            "coprimality is essential",
        ],
        "key_label": "Existence and uniqueness",
        "concepts_intro": (
            "A number is determined by its remainders, provided the moduli share no "
            "factors."
        ),
        "concepts": [
            ("Coprimality is the hypothesis",
             "Without it the system may be inconsistent (`x ≡ 1 mod 4` and `x ≡ 2 mod 6`) "
             "or have several solutions."),
            ("The construction is explicit",
             "Each term contributes the right remainder to its own modulus and 0 to the "
             "others, so the sum has all the required remainders at once."),
            ("It splits a big modulus into small ones",
             "Working modulo `pq` is equivalent to working modulo `p` and modulo `q` "
             "separately, which is a real speed-up when `p` and `q` are large."),
        ],
        "read_title": "The theorem",
        "read_intro": "Statement, construction, proof, and the application to RSA.",
        "body": [
            ("thm", ("Chinese remainder theorem",
                     "Let `m₁, …, m_k` be pairwise coprime positive integers and "
                     "`M = m₁⋯m_k`. For any `a₁, …, a_k` the system `x ≡ aᵢ (mod mᵢ)` has "
                     "exactly one solution modulo `M`.")),
            ("proof", [
                "<strong>Construction.</strong> Let `Mᵢ = M/mᵢ`. Since the moduli are "
                "pairwise coprime, `gcd(Mᵢ, mᵢ) = 1`, so `Mᵢ` has an inverse `yᵢ` modulo "
                "`mᵢ`. Set `x = Σ aᵢ Mᵢ yᵢ`.",
                "Modulo `mⱼ`, every term with `i ≠ j` vanishes because `mⱼ | Mᵢ`. The "
                "remaining term is `aⱼ Mⱼ yⱼ ≡ aⱼ · 1 = aⱼ`. So `x` satisfies every "
                "congruence.",
                "<strong>Uniqueness.</strong> If `x` and `x'` both solve the system, then "
                "`mᵢ | (x − x')` for every `i`. Pairwise coprimality gives "
                "`M | (x − x')`, so `x ≡ x' (mod M)`.",
            ]),
            ("p", "The construction is the theorem's real content. Each term is built to be "
                  "invisible to every modulus but its own, so the terms do not interfere "
                  "and the sum can satisfy all the congruences simultaneously."),
            ("example", ("Sun Tzu's problem",
                         "\"There are things whose number is unknown. Divided by 3 the "
                         "remainder is 2; by 5 the remainder is 3; by 7 the remainder is "
                         "2.\" With `M = 105`: "
                         "`M₁ = 35, y₁ = 2`; `M₂ = 21, y₂ = 1`; `M₃ = 15, y₃ = 1`. So "
                         "`x = 2·35·2 + 3·21·1 + 2·15·1 = 140 + 63 + 30 = 233 ≡ 23 "
                         "(mod 105)`. Check: `23 = 7·3 + 2`, `23 = 4·5 + 3`, `23 = 3·7 + 2`. "
                         "The problem is from a Chinese text of the third century.")),
            ("h3", "Coprimality is not optional"),
            ("example", ("Inconsistent",
                         "`x ≡ 1 (mod 4)` and `x ≡ 2 (mod 6)` has no solution: the first "
                         "makes `x` odd and the second makes it even. `gcd(4,6) = 2` and "
                         "the remainders disagree modulo 2.")),
            ("example", ("Consistent but not unique modulo the product",
                         "`x ≡ 1 (mod 4)` and `x ≡ 3 (mod 6)` has solutions `x ≡ 9 "
                         "(mod 12)`, not modulo 24. The correct modulus for non-coprime "
                         "systems is the lcm, and consistency requires the remainders to "
                         "agree modulo every pairwise gcd.")),
            ("h3", "Why RSA implementations use it"),
            ("p", "Decryption computes `c^d mod n` with `n = pq`. By the theorem, that is "
                  "equivalent to computing `c^d mod p` and `c^d mod q` and recombining. "
                  "The two exponentiations use numbers half the size, and modular "
                  "multiplication costs roughly the square of the operand size &mdash; so "
                  "each is about four times cheaper, and two of them together about twice."),
            ("p", "In practice the exponents can also be reduced modulo `p − 1` and "
                  "`q − 1` by Fermat's theorem (lesson 11), which is where the rest of the "
                  "speed-up comes from. The overall gain is roughly a factor of four, and "
                  "essentially every RSA implementation does this."),
        ],
        "lab": ("number", {
            "mode": "crt",
            "panel_title": "Two coprime moduli",
            "panel_intro": "The lab uses `m` and `m+1`, which are always coprime, so the "
                           "theorem always applies. The contribution column shows each term "
                           "being invisible to the other modulus.",
        }),
        "steps_title": "Solving a system",
        "steps_intro": "Check coprimality, then build the solution term by term.",
        "steps": [
            ("Check the moduli are pairwise coprime",
             "If not, the system may be inconsistent, and if consistent the modulus of the "
             "answer is the lcm rather than the product."),
            ("Compute `M` and each `Mᵢ = M/mᵢ`",
             "`Mᵢ` is divisible by every modulus except the `i`th, which is what makes the "
             "terms independent."),
            ("Invert each `Mᵢ` modulo `mᵢ`",
             "By the extended algorithm. These are the `yᵢ`."),
            ("Sum and reduce",
             "`x = Σ aᵢMᵢyᵢ (mod M)`, then verify every original congruence."),
        ],
        "worked": {
            "title": "Three congruences",
            "intro": ["`x ≡ 2 (mod 3)`, `x ≡ 3 (mod 5)`, `x ≡ 2 (mod 7)`."],
            "lines": [
                "M = 3 · 5 · 7 = 105",
                "",
                "i   mᵢ   aᵢ   Mᵢ = M/mᵢ   yᵢ = Mᵢ⁻¹ mod mᵢ   term aᵢMᵢyᵢ",
                "1    3    2       35        35 ≡ 2, 2⁻¹ ≡ 2        140",
                "2    5    3       21        21 ≡ 1, 1⁻¹ ≡ 1         63",
                "3    7    2       15        15 ≡ 1, 1⁻¹ ≡ 1         30",
                "",
                "x = 140 + 63 + 30 = 233 ≡ 233 − 2·105 = 23   (mod 105)",
                "",
                "CHECK   23 mod 3 = 2      ✓",
                "        23 mod 5 = 3      ✓",
                "        23 mod 7 = 2      ✓",
            ],
            "after": [
                "Each `Mᵢ` was reduced modulo its own `mᵢ` before inverting, which keeps "
                "the numbers small: inverting 35 modulo 3 is inverting 2 modulo 3. The "
                "solution is unique modulo 105, so 23, 128, 233 and `−82` are all the same "
                "answer."
            ],
        },
        "quiz_title": "The Chinese remainder theorem",
        "quiz": [
            {"q": "The theorem requires the moduli to be:",
             "a": ["prime", "pairwise coprime", "distinct", "odd"],
             "c": 1,
             "why": "Pairwise coprime. They need not be prime &mdash; 4 and 9 work fine "
                    "&mdash; but they must share no common factor."},
            {"q": "`x ≡ 1 (mod 4)` and `x ≡ 2 (mod 6)` has:",
             "a": ["one solution mod 24", "no solution",
                   "two solutions", "one solution mod 12"],
             "c": 1,
             "why": "The first forces `x` odd and the second forces it even. The moduli "
                    "are not coprime and the remainders disagree modulo `gcd(4,6) = 2`."},
            {"q": "RSA implementations use the theorem to:",
             "a": ["factor `n`",
                   "decrypt modulo `p` and `q` separately and recombine, about four times faster",
                   "generate primes",
                   "verify signatures"],
             "c": 1,
             "why": "Two exponentiations on half-size numbers cost far less than one on "
                    "full-size, because modular multiplication scales quadratically."},
        ],
        "mistakes": [
            ("Applying it without checking coprimality",
             "Non-coprime moduli may be inconsistent, and when they are consistent the "
             "answer is unique modulo the lcm, not the product."),
            ("Inverting `Mᵢ` modulo the wrong thing",
             "`yᵢ` is the inverse of `Mᵢ` modulo `mᵢ`, not modulo `M`. Reducing `Mᵢ` first "
             "makes the inversion small."),
            ("Forgetting to reduce the final sum",
             "The construction gives a solution; the canonical answer lies in `[0, M)`."),
        ],
        "standard": ("Finish when you can construct the solution rather than search for it.",
                     "Solve `x ≡ 1 (mod 5)`, `x ≡ 2 (mod 7)`, `x ≡ 3 (mod 9)` by the "
                     "construction. Searching would take up to 315 trials; the construction "
                     "takes three inversions."),
        "note": "The theorem is an isomorphism: `ℤ_{mn} ≅ ℤ_m × ℤ_n` for coprime `m, n`, "
                "and it respects both addition and multiplication. That structural "
                "statement is why the RSA speed-up works &mdash; the arithmetic really does "
                "split.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "fermat-and-euler",
        "title": "Fermat's Little Theorem and Euler's Theorem",
        "module": "Congruences",
        "one_line": "Exponents reduce modulo `φ(m)`, not modulo `m`.",
        "summary": (
            "`a^{φ(m)} ≡ 1 (mod m)` when `gcd(a,m) = 1`, with Fermat's `a^{p−1} ≡ 1` the "
            "prime case. It collapses enormous exponents and it is the theorem that makes "
            "RSA decryption work."
        ),
        "key": [
            "Fermat:  a^{p−1} ≡ 1 (mod p)      p prime, p ∤ a",
            "Euler:   a^{φ(m)} ≡ 1 (mod m)     gcd(a, m) = 1",
            "φ(p) = p − 1,   φ(pq) = (p−1)(q−1)   for distinct primes",
            "so a^k ≡ a^{k mod φ(m)}  (mod m)",
        ],
        "key_label": "The exponent rule",
        "concepts_intro": (
            "One theorem, two names, and the single most useful computational fact in "
            "the course."
        ),
        "concepts": [
            ("`φ(m)` counts the units",
             "The integers in `1, …, m` coprime to `m`. They are exactly the invertible "
             "elements of `ℤ_m`, by lesson 6."),
            ("Exponents reduce modulo `φ(m)`",
             "Not modulo `m`. `7^100 mod 10` becomes `7^{100 mod 4} = 7^0 = 1`, because "
             "`φ(10) = 4`."),
            ("Coprimality is required",
             "`2^{φ(4)} = 2² = 4 ≡ 0 (mod 4)`, not 1. The theorem says nothing about bases "
             "sharing a factor with the modulus."),
        ],
        "read_title": "Fermat and Euler",
        "read_intro": "The totient, both theorems, the proof, and the consequences.",
        "body": [
            ("def", ("Euler's totient",
                     "`φ(m)` is the number of integers in `{1, …, m}` coprime to `m`. "
                     "`φ(1) = 1`.")),
            ("thm", ("Computing `φ`",
                     "`φ(p) = p − 1` for prime `p`; `φ(p^k) = p^k − p^{k−1}`; and `φ` is "
                     "multiplicative on coprime arguments, so "
                     "`φ(mn) = φ(m)φ(n)` when `gcd(m,n) = 1`. In general "
                     "`φ(n) = n Π_{p | n} (1 − 1/p)`.")),
            ("p", "The multiplicativity is the Chinese remainder theorem in disguise: "
                  "`ℤ_{mn} ≅ ℤ_m × ℤ_n` for coprime moduli, and an element is invertible in "
                  "the product exactly when both components are. The product formula is "
                  "inclusion and exclusion over the prime divisors, from course 4 lesson 9."),
            ("math", [
                "φ(7)  = 6              prime",
                "φ(9)  = 9 − 3 = 6      = 3² − 3",
                "φ(12) = 12(1−½)(1−⅓) = 4        {1, 5, 7, 11}",
                "φ(35) = φ(5)φ(7) = 4 · 6 = 24",
                "φ(3120) = φ(2⁴·3·5·13) = 8 · 2 · 4 · 12 = 768",
            ]),
            ("thm", ("Euler's theorem",
                     "If `gcd(a, m) = 1` then `a^{φ(m)} ≡ 1 (mod m)`.")),
            ("proof", [
                "Let `u₁, …, u_φ` be the units modulo `m` &mdash; the residues coprime to "
                "`m`. Multiplying each by `a` gives `au₁, …, au_φ`, which are again units "
                "(a product of units is a unit) and are distinct, since `a` is invertible "
                "and cancellation holds for units.",
                "So `{au₁, …, au_φ}` is the same set as `{u₁, …, u_φ}` modulo `m`, and "
                "their products agree: `a^φ · (u₁⋯u_φ) ≡ u₁⋯u_φ (mod m)`.",
                "The product of the units is itself a unit, so it may be cancelled, "
                "leaving `a^{φ(m)} ≡ 1`.",
            ]),
            ("thm", ("Fermat's little theorem",
                     "If `p` is prime and `p ∤ a` then `a^{p−1} ≡ 1 (mod p)`. Equivalently, "
                     "`a^p ≡ a (mod p)` for every `a`.")),
            ("p", "This is Euler with `m = p`, since `φ(p) = p − 1`. The second form holds "
                  "even when `p | a`, because both sides are then 0."),
            ("h3", "Reducing exponents"),
            ("thm", ("The exponent rule",
                     "If `gcd(a,m) = 1` then `a^k ≡ a^{k mod φ(m)} (mod m)`.")),
            ("example", ("A large exponent",
                         "`7^{1000} mod 13`. `φ(13) = 12` and `1000 = 83·12 + 4`, so "
                         "`7^{1000} ≡ 7⁴ (mod 13)`. And `7² = 49 ≡ 10`, `7⁴ ≡ 100 ≡ 9`. "
                         "The answer is 9, from two multiplications.")),
            ("p", "Combined with lesson 8's fast exponentiation this makes essentially any "
                  "modular power computable: reduce the exponent by `φ(m)` first, then "
                  "square and multiply."),
            ("h3", "Primality testing"),
            ("p", "Fermat's theorem gives a test: if `a^{n−1} ≢ 1 (mod n)` for some `a` "
                  "coprime to `n`, then `n` is definitely composite. The converse fails "
                  "&mdash; <strong>Carmichael numbers</strong> such as 561 pass for every "
                  "coprime base while being composite &mdash; which is why the "
                  "Miller&ndash;Rabin refinement is used in practice."),
            ("p", "This is what makes RSA key generation possible: random 1024-bit numbers "
                  "are tested until one passes, and about one in 700 does. Nothing "
                  "factorises anything."),
        ],
        "lab": ("number", {
            "mode": "fermat",
            "panel_title": "Powers, until they return to 1",
            "panel_intro": "The table shows the powers of `a` modulo `m` and marks where "
                           "they hit 1. Try a base sharing a factor with `m` &mdash; the "
                           "powers never reach 1, because the theorem does not apply.",
        }),
        "steps_title": "Using the theorems",
        "steps_intro": "Check coprimality, compute `φ`, reduce the exponent.",
        "steps": [
            ("Check `gcd(a, m) = 1`",
             "Without it neither theorem applies. The powers of a non-coprime base never "
             "return to 1."),
            ("Compute `φ(m)`",
             "From the factorisation of `m`, using multiplicativity and `φ(p^k) = "
             "p^k − p^{k−1}`."),
            ("Reduce the exponent modulo `φ(m)`",
             "`a^k ≡ a^{k mod φ(m)}`. This is the step that turns an impossible "
             "computation into a small one."),
            ("Compute the small power",
             "By square and multiply if it is still large. Usually it is trivial."),
        ],
        "worked": {
            "title": "`3^{1234567} mod 100`",
            "intro": ["An exponent with seven digits, reduced to one."],
            "lines": [
                "gcd(3, 100) = 1                                    ✓ theorem applies",
                "",
                "φ(100) = φ(2²)·φ(5²) = (4−2)·(25−5) = 2 · 20 = 40",
                "",
                "1234567 mod 40 = 7          (1234567 = 30864·40 + 7)",
                "",
                "So  3^{1234567} ≡ 3⁷  (mod 100)",
                "",
                "3⁷ = 2187 ≡ 87   (mod 100)",
                "",
                "The last two digits of 3^{1234567} are 87.",
                "That number has over half a million digits.",
            ],
            "after": [
                "Two facts made this possible: Euler reduced the exponent from 1 234 567 "
                "to 7, and modular reduction kept every intermediate below 10 000. Either "
                "alone would have been insufficient."
            ],
        },
        "quiz_title": "Fermat and Euler",
        "quiz": [
            {"q": "`φ(15)` equals:",
             "a": ["15", "14", "8", "7"],
             "c": 2,
             "why": "`φ(15) = φ(3)φ(5) = 2 · 4 = 8`. The units are 1, 2, 4, 7, 8, 11, 13, 14."},
            {"q": "`a^k mod m` with `gcd(a,m) = 1`. The exponent reduces modulo:",
             "a": ["`m`", "`φ(m)`", "`m − 1`", "`k`"],
             "c": 1,
             "why": "Euler's theorem gives `a^{φ(m)} ≡ 1`, so exponents cycle with period "
                    "dividing `φ(m)`. Reducing modulo `m` is the classic error."},
            {"q": "561 passes Fermat's test for every coprime base but is composite. Such numbers are called:",
             "a": ["pseudoprimes only", "Carmichael numbers", "Mersenne numbers", "impossible"],
             "c": 1,
             "why": "`561 = 3 · 11 · 17`. Carmichael numbers are why Miller&ndash;Rabin, "
                    "rather than the plain Fermat test, is used in practice."},
        ],
        "mistakes": [
            ("Reducing the exponent modulo `m`",
             "It reduces modulo `φ(m)`. For `m = 100` those are 100 and 40, and the answers "
             "differ."),
            ("Applying the theorem to a non-coprime base",
             "`2^{φ(4)} = 4 ≡ 0 (mod 4)`. Coprimality is a hypothesis, not a formality."),
            ("Assuming passing Fermat's test proves primality",
             "Carmichael numbers pass for every coprime base. The test proves compositeness "
             "when it fails and proves nothing when it passes."),
        ],
        "standard": ("Finish when you reduce the exponent before anything else.",
                     "Compute `2^{1000000} mod 77`. `φ(77) = 60`, so the exponent becomes "
                     "`1000000 mod 60 = 40`, and `2^40 mod 77` is a short square-and-multiply."),
        "note": "Euler's theorem is exactly what makes RSA work: choosing `d` with "
                "`ed ≡ 1 (mod φ(n))` means `m^{ed} = m^{1 + kφ(n)} ≡ m` for `m` coprime to "
                "`n`. Lesson 14 puts it to use.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "hashing-and-pseudorandom-numbers",
        "title": "Hashing and Pseudorandom Numbers",
        "module": "Applications",
        "one_line": "Two everyday uses of modular arithmetic.",
        "summary": (
            "Hash functions map keys to a small range with `mod`, and linear congruential "
            "generators produce pseudorandom sequences the same way. Both work because of "
            "number theory, and both fail in ways number theory predicts."
        ),
        "key": [
            "h(k) = k mod m                     a hash function",
            "collisions are unavoidable         (pigeonhole)",
            "xₙ₊₁ = (a·xₙ + c) mod m            linear congruential generator",
            "full period ⟺ Hull–Dobell conditions on a, c, m",
        ],
        "key_label": "Modular arithmetic, applied",
        "concepts_intro": (
            "Two applications where the choice of modulus decides whether the method "
            "works or fails badly."
        ),
        "concepts": [
            ("Collisions are guaranteed",
             "More keys than slots means some slot is shared &mdash; the pigeonhole "
             "principle. The design question is how collisions are handled, not whether "
             "they occur."),
            ("A prime modulus spreads better",
             "`k mod 2^r` uses only the low bits of the key, so structured keys collide "
             "heavily. A prime modulus uses all of them."),
            ("Pseudorandom is not random",
             "An LCG is completely determined by its seed. It looks random by some "
             "statistical measures and is entirely predictable, which matters for security."),
        ],
        "read_title": "Hashing and pseudorandomness",
        "read_intro": "Both constructions, the number theory behind them, and their failure modes.",
        "body": [
            ("h3", "Hash functions"),
            ("def", ("Hash function",
                     "A function `h` mapping a large key space into `{0, 1, …, m−1}`. The "
                     "simplest is `h(k) = k mod m`.")),
            ("p", "Since the key space is larger than the range, collisions are "
                  "unavoidable: by the pigeonhole principle of course 2 lesson 14, some "
                  "slot receives more than one key. A hash table is therefore designed "
                  "around collisions &mdash; by chaining, or by probing for another slot."),
            ("thm", ("Why the modulus should be prime",
                     "If `m = 2^r`, then `k mod m` depends only on the low `r` bits of `k`. "
                     "Keys sharing those bits &mdash; addresses aligned to a boundary, "
                     "identifiers with a common suffix &mdash; all collide. A prime modulus "
                     "has no such structure to exploit.")),
            ("example", ("A bad choice",
                         "Hashing memory addresses with `m = 16` when every address is a "
                         "multiple of 16 sends every key to slot 0. With `m = 17` the same "
                         "keys spread across all seventeen slots.")),
            ("p", "The birthday problem of course 5 lesson 2 gives the collision rate: with "
                  "`m` slots and `n` keys, collisions become likely once `n` is around "
                  "`√m`. A table of a million slots sees its first collision after about a "
                  "thousand insertions, which is why load factors are managed rather than "
                  "collisions avoided."),
            ("h3", "Linear congruential generators"),
            ("def", ("LCG",
                     "`x_{n+1} = (a·x_n + c) mod m`, from a seed `x₀`. The parameters "
                     "`a` (multiplier), `c` (increment) and `m` (modulus) determine the "
                     "whole sequence.")),
            ("p", "The sequence must eventually repeat, since there are only `m` possible "
                  "values &mdash; pigeonhole again. The <strong>period</strong> is how long "
                  "it takes, and it is at most `m`."),
            ("thm", ("Hull-Dobell theorem",
                     "An LCG has full period `m` for every seed if and only if: "
                     "`gcd(c, m) = 1`; `a − 1` is divisible by every prime dividing `m`; "
                     "and `a − 1` is divisible by 4 if `m` is.")),
            ("example", ("A bad generator",
                         "`a = 5`, `c = 3`, `m = 8`, seed 0: `0, 3, 2, 5, 4, 7, 6, 1, 0, …` "
                         "&mdash; full period 8, and the conditions hold. Change `a` to 4 "
                         "and the sequence is `0, 3, 7, 7, 7, …`: it collapses almost "
                         "immediately, because `a − 1 = 3` is not divisible by 2.")),
            ("p", "Even a full-period LCG is not statistically good. Consecutive values fall "
                  "on a small number of hyperplanes in higher dimensions &mdash; the "
                  "Marsaglia effect &mdash; and the low bits of a power-of-two-modulus LCG "
                  "have very short periods. RANDU, an LCG shipped by IBM in the 1960s, was "
                  "so bad in three dimensions that results computed with it were later "
                  "retracted."),
            ("h3", "Cryptographic requirements are different"),
            ("p", "An LCG is trivially predictable: observing a few outputs determines the "
                  "parameters and hence every future value. That is fine for a simulation "
                  "and fatal for a key or a session token. Cryptographic generators are "
                  "built so that predicting the next output is as hard as a problem "
                  "believed intractable &mdash; and \"looks random\" is not the same "
                  "requirement as \"cannot be predicted\"."),
        ],
        "lab": ("number", {
            "mode": "modtable",
            "panel_title": "Prime versus composite moduli",
            "panel_intro": "Set a prime modulus and note that every nonzero row of the "
                           "multiplication table is a permutation. With a composite "
                           "modulus some rows repeat values &mdash; which is exactly the "
                           "clustering a bad hash modulus produces.",
        }),
        "steps_title": "Choosing parameters",
        "steps_intro": "The modulus decides the behaviour.",
        "steps": [
            ("For a hash table, prefer a prime modulus",
             "It uses all the bits of the key. A power of two uses only the low ones, "
             "which is where structured keys collide."),
            ("Expect collisions and plan for them",
             "Chaining or open addressing. By the birthday argument they begin around "
             "`√m` insertions."),
            ("For an LCG, check the Hull-Dobell conditions",
             "They guarantee full period. Failing them can collapse the sequence to a "
             "handful of values."),
            ("Never use an LCG where prediction matters",
             "Session tokens, keys and nonces need a cryptographic generator. The "
             "distinction is about predictability, not about statistics."),
        ],
        "worked": {
            "title": "Two generators, same modulus",
            "intro": ["`m = 16`, seed 1, comparing a good and a bad multiplier."],
            "lines": [
                "a = 5, c = 3   Hull–Dobell:  gcd(3,16)=1 ✓   2 | (a−1)=4 ✓   4 | 4 ✓",
                "   1, 8, 11, 10, 5, 12, 15, 14, 9, 0, 3, 2, 13, 4, 7, 6, 1, …",
                "   period 16 — every value once                             ✓",
                "",
                "a = 6, c = 3   gcd(3,16)=1 ✓   but 2 ∤ (a−1)=5              ✗",
                "   1, 9, 9, 9, …",
                "   period 1 after the first step — the generator is dead",
                "",
                "One parameter changed by 1, and the sequence went from",
                "every value to a constant.",
            ],
            "after": [
                "This is why the theorem is worth having. The failure is not a degradation "
                "&mdash; it is total, and it would be easy to ship without noticing if the "
                "seed happened to look fine. The conditions are three divisibility checks."
            ],
        },
        "quiz_title": "Hashing and randomness",
        "quiz": [
            {"q": "Why are hash collisions unavoidable?",
             "a": ["Bad hash functions",
                   "More keys than slots — the pigeonhole principle",
                   "Modular arithmetic is imprecise",
                   "They are avoidable with a prime modulus"],
             "c": 1,
             "why": "A map from a larger set to a smaller one cannot be injective. The "
                    "design question is how collisions are handled."},
            {"q": "`h(k) = k mod 2^r` is a poor choice because:",
             "a": ["it is slow",
                   "it uses only the low `r` bits of the key",
                   "`2^r` is composite",
                   "it produces negative values"],
             "c": 1,
             "why": "Keys sharing their low bits &mdash; aligned addresses, common "
                    "suffixes &mdash; all collide. A prime modulus uses every bit."},
            {"q": "An LCG is unsuitable for cryptography because:",
             "a": ["its period is too short",
                   "observing a few outputs lets an attacker predict all the rest",
                   "it is too slow",
                   "it uses modular arithmetic"],
             "c": 1,
             "why": "It is entirely deterministic and its parameters are recoverable from "
                    "its output. Statistical quality is a different and weaker requirement."},
        ],
        "mistakes": [
            ("Using a power of two as a hash modulus with structured keys",
             "Only the low bits matter, so aligned or suffixed keys cluster. A prime "
             "modulus removes the structure."),
            ("Assuming a full-period LCG is statistically good",
             "Full period is necessary and far from sufficient. Consecutive tuples fall on "
             "hyperplanes, which broke real scientific results."),
            ("Using a general-purpose generator for security",
             "\"Looks random\" and \"cannot be predicted\" are different properties, and "
             "only the second matters for keys."),
        ],
        "standard": ("Finish when you can check the Hull-Dobell conditions.",
                     "For `m = 100`, find a multiplier and increment giving full period, "
                     "and one that fails. The three conditions are quick to verify and the "
                     "failure is dramatic."),
        "note": "Cryptographic hash functions &mdash; SHA-256 and the like &mdash; are a "
                "different object from the hash functions here: they must also be "
                "collision-resistant against an adversary who is trying, which is a "
                "requirement `k mod m` does not begin to meet.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "classical-ciphers",
        "title": "Classical Ciphers",
        "module": "Cryptography",
        "one_line": "Shift, affine and Vigenère — and why each one falls.",
        "summary": (
            "Three ciphers built from modular arithmetic, each broken by a different "
            "attack. They are worth studying because the reasons they fail are the "
            "requirements a real cipher must meet."
        ),
        "key": [
            "shift    E(x) = (x + k) mod 26            26 keys — brute force",
            "affine   E(x) = (ax + b) mod 26           needs gcd(a,26) = 1",
            "Vigenère repeating key of shifts          period found, then 26 shifts",
            "one-time pad: key as long as the message, never reused — unbreakable",
        ],
        "key_label": "Three ciphers, three breaks",
        "concepts_intro": (
            "Each cipher is modular arithmetic on letters. Each is broken, and the break "
            "teaches the design requirement."
        ),
        "concepts": [
            ("The key space must be large",
             "A shift cipher has 26 keys and falls to exhaustive search in seconds. Large "
             "key space is necessary and far from sufficient."),
            ("Structure survives substitution",
             "Any cipher mapping each letter to a fixed other letter preserves letter "
             "frequencies, and English frequencies are distinctive enough to break it."),
            ("Key reuse is the recurring fatal flaw",
             "Vigenère falls because the key repeats. The one-time pad is provably secure "
             "precisely because it never does."),
        ],
        "read_title": "Three ciphers",
        "read_intro": "Construction, decryption and attack for each.",
        "body": [
            ("h3", "The shift cipher"),
            ("def", ("Shift cipher",
                     "Encode letters as `0 … 25`. Encryption is `E(x) = (x + k) mod 26` and "
                     "decryption is `D(y) = (y − k) mod 26`. Caesar's cipher is `k = 3`.")),
            ("p", "There are 25 useful keys, so an attacker tries them all and reads the "
                  "output. This takes seconds by hand. The lesson is that a key space must "
                  "be far too large to enumerate &mdash; modern ciphers use `2¹²⁸` keys or "
                  "more."),
            ("h3", "The affine cipher"),
            ("def", ("Affine cipher",
                     "`E(x) = (ax + b) mod 26`, with `gcd(a, 26) = 1` so that `a` is "
                     "invertible. Decryption is `D(y) = a⁻¹(y − b) mod 26`.")),
            ("p", "The coprimality condition is exactly lesson 6's: without it the map is "
                  "not injective and decryption is impossible. Since `26 = 2 · 13`, the "
                  "valid multipliers are the twelve values coprime to 26, giving "
                  "`12 · 26 = 312` keys."),
            ("example", ("Encrypting and decrypting",
                         "`a = 5`, `b = 8`. The letter `H` is 7, so "
                         "`E(7) = 5·7 + 8 = 43 ≡ 17 = R`. To decrypt, `5⁻¹ ≡ 21 (mod 26)` "
                         "since `5 · 21 = 105 = 4·26 + 1`, so "
                         "`D(17) = 21(17 − 8) = 21 · 9 = 189 ≡ 7 = H`. ✓")),
            ("p", "312 keys is still trivially searchable, and the cipher has a worse "
                  "problem: it is a substitution, so letter frequencies survive. `E` is the "
                  "commonest letter in English at about 12%, and whatever it maps to will "
                  "be the commonest ciphertext letter. Two frequency matches determine `a` "
                  "and `b`."),
            ("h3", "The Vigenère cipher"),
            ("def", ("Vigenère cipher",
                     "A keyword gives a repeating sequence of shifts: the `i`th letter of "
                     "the message is shifted by the `(i mod L)`th letter of the key, where "
                     "`L` is the key length.")),
            ("p", "This defeats simple frequency analysis, because one plaintext letter "
                  "encrypts to different ciphertext letters depending on its position. It "
                  "was called <em>le chiffre indéchiffrable</em> for three centuries."),
            ("p", "It falls in two stages. First find the key length: repeated plaintext "
                  "fragments aligned with the same key position produce repeated ciphertext, "
                  "and the distances between repetitions are multiples of `L` "
                  "(Kasiski's method). Second, split the ciphertext into `L` columns, each "
                  "of which is a single shift cipher, and break each by frequency."),
            ("p", "The structural failure is key reuse. Once the period is known, a "
                  "message of any length gives as much frequency data as needed."),
            ("h3", "The one-time pad"),
            ("thm", ("Perfect secrecy",
                     "If the key is uniformly random, at least as long as the message, and "
                     "never reused, then the ciphertext gives an attacker no information "
                     "about the plaintext: every plaintext of that length is equally "
                     "consistent with the observed ciphertext.")),
            ("p", "This is Shannon's theorem, and the one-time pad is genuinely "
                  "unbreakable. It is also nearly unusable: the key is as long as the "
                  "message and must be distributed securely in advance, which is the "
                  "problem encryption was meant to solve."),
            ("p", "Reusing a one-time pad destroys it completely. Two messages encrypted "
                  "with the same key satisfy `c₁ ⊕ c₂ = m₁ ⊕ m₂`, from which both plaintexts "
                  "can usually be recovered &mdash; the failure that broke the Soviet "
                  "VENONA traffic."),
            ("p", "Lesson 14's RSA answers the key-distribution problem instead: no shared "
                  "secret is needed at all."),
        ],
        "lab": ("number", {
            "mode": "modtable",
            "panel_title": "Why `gcd(a, 26) = 1`",
            "panel_intro": "Set the modulus to 26 and look at the multiplication table. "
                           "Rows for multipliers sharing a factor with 26 repeat values, so "
                           "the affine cipher would map two letters to one.",
        }),
        "steps_title": "Encrypting and breaking",
        "steps_intro": "The requirement first, then the attack.",
        "steps": [
            ("Check the key is valid",
             "For an affine cipher `gcd(a, 26) = 1`, or the map is not invertible and "
             "decryption fails."),
            ("Encrypt letter by letter",
             "Convert to `0 … 25`, apply the map modulo 26, convert back."),
            ("To break a substitution, count letters",
             "English frequencies are distinctive: E about 12%, T 9%, A 8%. Two matches "
             "determine an affine key."),
            ("To break Vigenère, find the period first",
             "Repeated fragments give multiples of the key length. Then each column is a "
             "shift cipher."),
        ],
        "worked": {
            "title": "Breaking an affine cipher",
            "intro": ["Ciphertext frequency analysis gives the two commonest letters."],
            "lines": [
                "Suppose the two commonest ciphertext letters are R (17) and I (8),",
                "and the two commonest English letters are E (4) and T (19).",
                "",
                "Guess E → R and T → I:",
                "   4a + b ≡ 17   (mod 26)",
                "  19a + b ≡  8   (mod 26)",
                "",
                "Subtract:  15a ≡ −9 ≡ 17  (mod 26)",
                "   gcd(15,26) = 1, and 15⁻¹ ≡ 7  (since 15·7 = 105 ≡ 1)",
                "   a ≡ 7 · 17 = 119 ≡ 119 − 4·26 = 15   (mod 26)",
                "",
                "   b ≡ 17 − 4·15 = 17 − 60 = −43 ≡ 9    (mod 26)",
                "",
                "Key (a, b) = (15, 9).  gcd(15,26) = 1, so it is valid.",
                "Decrypt with a⁻¹ = 7:   D(y) = 7(y − 9) mod 26",
            ],
            "after": [
                "Two frequency guesses gave a linear system, which lesson 9 solves. If the "
                "decryption is nonsense the next guess is E→R, T→ something else, and there "
                "are only a few to try. The cipher offers no resistance beyond that."
            ],
        },
        "quiz_title": "Classical ciphers",
        "quiz": [
            {"q": "Why must `gcd(a, 26) = 1` in an affine cipher?",
             "a": ["To make encryption faster",
                   "So `a` is invertible modulo 26 and decryption is possible",
                   "To avoid negative values",
                   "It is not required"],
             "c": 1,
             "why": "Without it the map is not injective &mdash; two letters encrypt to "
                    "the same letter &mdash; and no decryption exists."},
            {"q": "The Vigenère cipher is broken by:",
             "a": ["trying all keys",
                   "finding the key length, then breaking each column as a shift cipher",
                   "factoring the key",
                   "it is unbreakable"],
             "c": 1,
             "why": "Repetitions in the ciphertext reveal the period; each column is then a "
                    "single shift, broken by frequency analysis."},
            {"q": "The one-time pad is unbreakable provided the key is:",
             "a": ["long", "random, at least as long as the message, and never reused",
                   "prime", "kept in a safe"],
             "c": 1,
             "why": "All three conditions are needed. Reuse in particular destroys the "
                    "security completely, as VENONA demonstrated."},
        ],
        "mistakes": [
            ("Choosing an affine multiplier sharing a factor with 26",
             "13, 2 and any even value make the map non-injective. Decryption becomes "
             "impossible, not merely difficult."),
            ("Believing a large key space is sufficient",
             "The affine cipher has 312 keys and would be broken by frequency analysis "
             "even with millions, because the structure survives."),
            ("Reusing a one-time pad",
             "Two messages under one key give `m₁ ⊕ m₂`, from which both are usually "
             "recoverable. The pad is secure only for a single use."),
        ],
        "standard": ("Finish when you can break an affine cipher from two frequencies.",
                     "Given that the two commonest ciphertext letters are K and D, solve "
                     "for `a` and `b` assuming they correspond to E and T. The system is "
                     "two linear congruences, which lesson 9 handles."),
        "note": "Every cipher here shares one weakness that lesson 14 removes: both parties "
                "need the key in advance. Public-key cryptography changed that, and it is "
                "the single most consequential idea in the subject.",
    },
    # ---------------------------------------------------------------- 14
    {
        "slug": "rsa-encryption",
        "title": "RSA Encryption",
        "module": "Cryptography",
        "one_line": "Public-key encryption from Euler's theorem — and what its security rests on.",
        "summary": (
            "Generate `n = pq`, choose `e` coprime to `φ(n)`, compute `d = e⁻¹ mod φ(n)`. "
            "Encryption is `m^e mod n` and decryption `c^d mod n`. Every step is a "
            "theorem from this course, and the security is one unproved assumption."
        ),
        "key": [
            "n = pq,  φ(n) = (p−1)(q−1),  gcd(e, φ(n)) = 1,  d = e⁻¹ mod φ(n)",
            "PUBLIC  (n, e)      PRIVATE  (d, and p, q)",
            "encrypt  c = m^e mod n        decrypt  m = c^d mod n",
            "security: factoring n is believed hard. It is not proved.",
        ],
        "key_label": "The whole system",
        "concepts_intro": (
            "RSA uses six results from this course and adds one assumption. Naming both "
            "lists is the honest way to present it."
        ),
        "concepts": [
            ("Correctness is Euler's theorem",
             "`ed ≡ 1 (mod φ(n))` makes `m^{ed} ≡ m (mod n)`, which is why decryption "
             "returns the message."),
            ("The public key reveals `n`, not `φ(n)`",
             "Knowing `φ(n) = (p−1)(q−1)` together with `n = pq` gives `p` and `q` "
             "immediately. So `φ(n)` is as secret as the factorisation."),
            ("Security is an assumption, not a theorem",
             "No proof exists that factoring is hard, and no proof exists that breaking "
             "RSA requires factoring. Both are believed and neither is established."),
        ],
        "read_title": "RSA",
        "read_intro": "Key generation, the correctness proof, the attacks, and the honest caveats.",
        "body": [
            ("h3", "Key generation"),
            ("math", [
                "1.  choose two large distinct primes  p, q",
                "2.  n = p·q",
                "3.  φ(n) = (p−1)(q−1)",
                "4.  choose e with 1 < e < φ(n) and gcd(e, φ(n)) = 1",
                "5.  compute d = e⁻¹ mod φ(n)          extended Euclid",
                "",
                "    PUBLIC KEY   (n, e)",
                "    PRIVATE KEY  (n, d)      and p, q, φ(n) must stay secret",
            ]),
            ("p", "Every step is a lesson from this course: primality testing from lesson "
                  "11, the totient formula from lesson 11, coprimality from lesson 4, and "
                  "the modular inverse from lesson 6."),
            ("h3", "Encryption and decryption"),
            ("p", "With the message encoded as an integer `m` with `0 ≤ m &lt; n`, "
                  "encryption is `c = m^e mod n` and decryption is `m = c^d mod n`. Both "
                  "are single modular exponentiations, computed by lesson 8's algorithm."),
            ("thm", ("Correctness",
                     "For `0 ≤ m &lt; n`, `(m^e)^d ≡ m (mod n)`.")),
            ("proof", [
                "`ed ≡ 1 (mod φ(n))` means `ed = 1 + kφ(n)` for some integer `k`, so "
                "`m^{ed} = m · (m^{φ(n)})^k`.",
                "If `gcd(m, n) = 1`, Euler's theorem gives `m^{φ(n)} ≡ 1 (mod n)`, so "
                "`m^{ed} ≡ m`.",
                "If `gcd(m, n) ≠ 1` the argument still works via the Chinese remainder "
                "theorem: modulo `p`, either `p | m` and both sides are 0, or Fermat gives "
                "`m^{p−1} ≡ 1` and `m^{ed} ≡ m`. The same holds modulo `q`, and since "
                "`p` and `q` are coprime the congruence holds modulo `n`.",
            ]),
            ("p", "Four of this course's theorems appear in that proof. RSA is not an "
                  "application of number theory so much as an assembly of it."),
            ("h3", "The standard example"),
            ("math", [
                "p = 61,  q = 53        n = 3233        φ(n) = 60 · 52 = 3120",
                "e = 17                 gcd(17, 3120) = 1                  ✓",
                "d = 17⁻¹ mod 3120 = 2753        (lesson 6 computed this)",
                "",
                "encrypt m = 65:   65^17 mod 3233 = 2790",
                "decrypt:        2790^2753 mod 3233 =   65        ✓",
            ]),
            ("h3", "What the security rests on"),
            ("p", "An attacker sees `n` and `e`. To find `d` they need `φ(n)`, and "
                  "computing `φ(n)` from `n` is equivalent to factoring `n`: knowing "
                  "`n = pq` and `φ(n) = (p−1)(q−1)` gives `p + q = n − φ(n) + 1`, and with "
                  "`pq = n` that is a quadratic whose roots are `p` and `q`."),
            ("p", "So RSA is secure only if factoring large numbers is hard. That is "
                  "<strong>believed</strong> and not proved. The best known general "
                  "algorithm, the number field sieve, is sub-exponential but not "
                  "polynomial; the largest RSA modulus factored publicly is 829 bits, "
                  "which took thousands of core-years."),
            ("p", "Two further caveats, both important. Nobody has proved that breaking "
                  "RSA <em>requires</em> factoring &mdash; there might be an easier attack "
                  "on the exponentiation itself. And Shor's algorithm factors in polynomial "
                  "time on a quantum computer, so RSA is broken outright if a large enough "
                  "one is ever built."),
            ("h3", "Why the lab can break its own key"),
            ("p", "The lab on this page factors the modulus it just generated, by trial "
                  "division, in microseconds &mdash; and recovers the private exponent. "
                  "Nothing about the method resists that; only the SIZE of the primes does. "
                  "Real keys use primes of about 1024 bits each, where the same trial "
                  "division would outlast the universe."),
            ("p", "One last honest note: <strong>textbook RSA as described here is not "
                  "secure to deploy</strong>. It is deterministic, so identical messages "
                  "produce identical ciphertexts and an attacker can test guesses; small "
                  "messages with small `e` can be recovered by taking an ordinary integer "
                  "root. Real systems use randomised padding (OAEP) for exactly these "
                  "reasons. The mathematics here is right and the engineering is not "
                  "present."),
        ],
        "lab": ("rsa", {
            "panel_title": "Generate, use, break",
            "panel_intro": "The default primes are the textbook ones. Change them and watch "
                           "the key change; then read the last paragraph of the status "
                           "line, where the lab factors `n` and recovers `d`.",
        }),
        "steps_title": "Using RSA",
        "steps_intro": "Each step is a theorem from this course.",
        "steps": [
            ("Choose two distinct primes and multiply",
             "`n = pq`. They must be distinct, or `φ(n) = p(p−1)` rather than `(p−1)²` and "
             "`n` is a square, trivially factorable."),
            ("Compute `φ(n) = (p−1)(q−1)`",
             "Multiplicativity of `φ` from lesson 11. This value must never be published."),
            ("Choose `e` coprime to `φ(n)` and invert it",
             "`gcd(e, φ(n)) = 1` by lesson 4, and `d = e⁻¹ mod φ(n)` by lesson 6. 65537 is "
             "the usual choice of `e`."),
            ("Exponentiate to encrypt and decrypt",
             "By lesson 8's square and multiply, which is what makes 2048-bit exponents "
             "practical."),
        ],
        "worked": {
            "title": "A complete small key",
            "intro": ["Every step, with the theorem that licenses it."],
            "lines": [
                "p = 11, q = 13                        two distinct primes",
                "n = 143",
                "φ(n) = 10 · 12 = 120                  multiplicativity of φ",
                "",
                "e = 7      gcd(7, 120) = 1            valid public exponent",
                "d = 7⁻¹ mod 120:",
                "    120 = 17·7 + 1   ⟹   1 = 120 − 17·7   ⟹   d ≡ −17 ≡ 103",
                "    check 7 · 103 = 721 = 6·120 + 1                      ✓",
                "",
                "encrypt m = 9:    9^7 mod 143",
                "    9² = 81      9⁴ = 81² = 6561 ≡ 126      (mod 143)",
                "    9^7 = 9⁴·9²·9 ≡ 126·81·9",
                "    126·81 = 10206 ≡ 48;   48·9 = 432 ≡ 3   (mod 143)",
                "    c = 3",
                "",
                "decrypt:  3^103 mod 143 = 9                              ✓",
            ],
            "after": [
                "The public key `(143, 7)` is enough to encrypt and useless for decrypting "
                "&mdash; unless you factor 143, which takes one division by 11. That is the "
                "whole security story, and the only thing that changes at 2048 bits is how "
                "long that division takes."
            ],
        },
        "quiz_title": "RSA",
        "quiz": [
            {"q": "In RSA, which value must remain secret?",
             "a": ["`n`", "`e`", "`φ(n)`", "the ciphertext"],
             "c": 2,
             "why": "`n` and `e` are public. Knowing `φ(n)` together with `n` yields `p` "
                    "and `q` immediately, so it is as secret as the factorisation."},
            {"q": "RSA decryption works because of:",
             "a": ["the Chinese remainder theorem alone",
                   "Euler's theorem: `ed ≡ 1 (mod φ(n))` gives `m^{ed} ≡ m`",
                   "the sieve of Eratosthenes",
                   "Bézout's identity alone"],
             "c": 1,
             "why": "Euler is the core, with Bézout supplying `d` and the Chinese remainder "
                    "theorem covering the case `gcd(m, n) ≠ 1`."},
            {"q": "RSA's security rests on:",
             "a": ["a proof that factoring is hard",
                   "the belief that factoring large numbers is hard — which is unproved",
                   "the secrecy of the algorithm",
                   "the size of the message"],
             "c": 1,
             "why": "No hardness proof exists, and it is also unproved that breaking RSA "
                    "requires factoring. Both are assumptions."},
        ],
        "mistakes": [
            ("Publishing or leaking `φ(n)`",
             "With `n` it gives `p + q` and hence the factorisation. It is as sensitive as "
             "the primes themselves."),
            ("Using equal or close primes",
             "`p = q` makes `n` a perfect square. Primes that are close make Fermat's "
             "factorisation method succeed quickly."),
            ("Deploying textbook RSA",
             "It is deterministic and malleable. Real systems randomise with OAEP padding, "
             "and the mathematics on this page is not the whole system."),
        ],
        "standard": ("Finish when you can generate a key and say what each step assumes.",
                     "Build a key from `p = 17`, `q = 23`, encrypt a small message, decrypt "
                     "it, and then factor `n` to recover `d`. Doing the attack yourself is "
                     "what makes the security argument concrete rather than asserted."),
        "note": "This course ends where cryptographic engineering begins. Padding schemes, "
                "key management, side-channel resistance and protocol design are all "
                "essential and none of them is number theory. What number theory supplies "
                "is the core operation and an honest account of what it does and does not "
                "guarantee.",
    },
]
