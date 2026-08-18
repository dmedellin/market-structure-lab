"""Course 9, lessons 01-06 - sequences, sigma notation, the two families, partial sums."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "sequences-and-recursion",
        "title": "Sequences and Recursion",
        "module": "Sequences",
        "one_line": "A function on the positive integers, defined two ways.",
        "summary": (
            "A sequence is a function whose inputs are the positive integers: a first "
            "term, a second term, and no last one. It can be given by a formula for the "
            "n-th term, or by a starting value and a rule for the next one, and the two "
            "forms are not interchangeable."
        ),
        "key": [
            "a₁, a₂, a₃, …        aₙ is the n-th term; n is an index, not a value",
            "explicit    aₙ = 5·2ⁿ⁻¹         give it n, it gives you the term",
            "recursive   a₁ = 5,             each term from the one before",
            "            aₙ = 2aₙ₋₁          both parts are required",
        ],
        "key_label": "One sequence, two ways to define it",
        "concepts_intro": (
            "There is one genuinely new idea here and it is the notation. The object "
            "itself is a function, and functions were course 3."
        ),
        "concepts": [
            ("A sequence is a function on the positive integers",
             "`aₙ` is `f(n)` written differently: hand it `4` and it returns the fourth "
             "term. The domain is `1, 2, 3, …` rather than an interval, so the graph is "
             "a row of separate dots rather than a curve. Nothing about one input "
             "giving one output has changed."),
            ("Explicit hands you any term; recursive makes you walk",
             "From `aₙ = 5·2ⁿ⁻¹` you get `a₃₀` in one line. From `a₁ = 5`, "
             "`aₙ = 2aₙ₋₁` you get `a₃₀` after computing the twenty-nine terms before "
             "it. The recursive form is often the one a situation hands you; the "
             "explicit form is the one you want."),
            ("Where the indexing starts is arbitrary",
             "Some sequences are numbered from `a₁` and some from `a₀`, and both "
             "conventions are in use. This course starts at `a₁`. The trap is a formula "
             "written for one convention and read under the other: `aₙ = 2ⁿ` gives "
             "`2, 4, 8, …` from `n = 1` and `1, 2, 4, …` from `n = 0`."),
        ],
        "read_title": "Sequences, and the two kinds of definition",
        "read_intro": "What the subscript means, what a recursion needs to be complete, and why five terms prove nothing.",
        "body": [
            ("def", ("Sequence",
                     "A <strong>sequence</strong> is a function whose domain is the "
                     "positive integers. Its outputs are its <strong>terms</strong>, "
                     "written `a₁, a₂, a₃, …`, and `aₙ` is the <strong>n-th term</strong> "
                     "or general term. A sequence that stops is <strong>finite</strong>; "
                     "one that does not is <strong>infinite</strong>.")),
            ("p", "The subscript is an index, not a multiplication and not a value: "
                  "`a₃` is the third term, whatever number that happens to be. In the "
                  "sequence `7, 7, 7, …` every term is `7` and `a₃ = 7`; in "
                  "`10, 20, 30, …`, `a₃ = 30`, not `3`."),
            ("p", "A sequence is not a set. Order is part of it and repetition is "
                  "allowed: `1, 0, 1, 0, …` has two distinct values and infinitely many "
                  "terms, and `1, 2, 3` and `3, 2, 1` are different sequences built "
                  "from the same three numbers."),
            ("example", ("Three sequences given explicitly",
                         "`aₙ = 3n - 1` gives `2, 5, 8, 11, 14, …` . "
                         "`bₙ = (-1)ⁿ` gives `-1, 1, -1, 1, …` , which is how an "
                         "alternating sign is usually produced. "
                         "`cₙ = 1/n` gives `1, 1/2, 1/3, 1/4, …` , whose terms shrink "
                         "toward `0` without ever reaching it.")),
            ("def", ("Recursive definition",
                     "A <strong>recursive definition</strong> of a sequence has two "
                     "parts: one or more <strong>initial terms</strong>, and a "
                     "<strong>recurrence</strong> giving `aₙ` in terms of earlier "
                     "terms. Both parts are needed. The recurrence alone does not "
                     "identify a sequence.")),
            ("p", "That last sentence is the one to take seriously. The rule "
                  "`aₙ = 2aₙ₋₁` is satisfied by `5, 10, 20, 40, …`, by "
                  "`3, 6, 12, 24, …` and by `0, 0, 0, …` . It says how to move, not "
                  "where to start, and a definition missing its initial term is not "
                  "incomplete in a small way &mdash; it names infinitely many "
                  "different sequences."),
            ("example", ("The same sequence, both ways",
                         "`a₁ = 5` with `aₙ = 2aₙ₋₁` gives `5, 10, 20, 40, 80, …` . So "
                         "does `aₙ = 5·2ⁿ⁻¹`, because doubling `n - 1` times from `5` "
                         "is what that formula does. Lesson 4 shows this is the "
                         "general shape of a geometric sequence.")),
            ("example", ("Two recursions worth knowing",
                         "Fibonacci: `F₁ = 1`, `F₂ = 1`, `Fₙ = Fₙ₋₁ + Fₙ₋₂`, giving "
                         "`1, 1, 2, 3, 5, 8, 13, 21, 34, 55, …` . It needs two initial "
                         "terms because the rule reaches back two. "
                         "Factorial: `0! = 1` and `n! = n·(n - 1)!`, giving "
                         "`1, 1, 2, 6, 24, 120, …` . Lesson 10 uses the second one "
                         "throughout.")),
            ("h3", "From a recursion to a formula, and the check that is not a proof"),
            ("p", "There is no general method for turning a recursion into an explicit "
                  "formula. What there is, at this level, is a procedure: compute "
                  "several terms, look for a pattern, write a candidate formula, and "
                  "test it on terms you did not use to build it."),
            ("p", "Testing is not proving. The sequence `1, 2, 4, 8, 16, …` looks "
                  "settled after five terms, and here is a sequence that starts that "
                  "way and then does not continue: mark `n` points on a circle, join "
                  "every pair by a chord with no three chords meeting at a point, and "
                  "count the regions the disc is cut into. For `n = 1` through `5` the "
                  "counts are `1, 2, 4, 8, 16`. For `n = 6` the count is `31`."),
            ("p", "So a formula that matches the first five terms of a recursion is a "
                  "candidate, not a fact. Establishing that it matches for every `n` "
                  "requires mathematical induction, which this path does not cover: it "
                  "is the subject of the Induction and Recursion course on the Discrete "
                  "Mathematics path. Within this course, say \"this formula agrees with "
                  "the first six terms\" and mean exactly that."),
        ],
        "lab": ("sequence", {
            "mode": "define",
            "panel_title": "Two definitions, one list",
            "panel_intro": "Enter an explicit formula or a recursion with its initial "
                           "term, and the lab prints the terms and plots them. Enter "
                           "both forms of the same sequence and check that the two "
                           "lists agree term by term.",
        }),
        "steps_title": "Working with a sequence you have been handed",
        "steps_intro": "Before any formula, the terms. Writing them out costs a minute and catches an index error at once.",
        "steps": [
            ("Decide which kind of definition it is",
             "A formula mentioning only `n` is explicit. A formula mentioning `aₙ₋₁` "
             "or earlier terms is a recurrence, and it needs initial terms to be a "
             "definition at all."),
            ("Write out the first four or five terms",
             "Substitute `n = 1, 2, 3, 4` and record what comes out. If the sequence "
             "was described in words, this is where a misreading shows up while it is "
             "still cheap."),
            ("Check the recursion has enough initial terms",
             "A rule reaching back one step needs one; a rule reaching back two, like "
             "Fibonacci, needs two. Too few and the sequence is not determined; too "
             "many and they may contradict the rule."),
            ("If you need a distant term, look for a closed form",
             "Guess from the terms, then test the guess on a term you have not used. "
             "Report it as a formula that agrees with the terms you checked, unless "
             "you can prove more."),
        ],
        "worked": {
            "title": "a₁ = 3,  aₙ = 2aₙ₋₁ + 1",
            "intro": [
                "The recursion is easy to run and the pattern is visible once the terms "
                "are written next to the powers of 2."
            ],
            "lines": [
                "a₁ = 3",
                "a₂ = 2(3)  + 1 = 7",
                "a₃ = 2(7)  + 1 = 15",
                "a₄ = 2(15) + 1 = 31",
                "a₅ = 2(31) + 1 = 63",
                "",
                "terms          3    7    15    31    63",
                "one more       4    8    16    32    64",
                "               2²   2³   2⁴    2⁵    2⁶",
                "",
                "guess    aₙ = 2ⁿ⁺¹ - 1",
                "",
                "test     n = 1:   2² - 1 = 4 - 1 = 3          ✓",
                "         n = 4:   2⁵ - 1 = 32 - 1 = 31        ✓",
                "         n = 6:   2⁷ - 1 = 128 - 1 = 127,",
                "                  and the recursion gives 2(63) + 1 = 127    ✓",
            ],
            "after": [
                "The `n = 6` line is the only one doing real work. The first two use "
                "terms the guess was built from; the third predicts a term first and "
                "then checks it, which is the only kind of test that can fail.",
                "It still is not a proof. What would settle it is the argument that "
                "assumes `aₖ = 2ᵏ⁺¹ - 1` and shows the recurrence forces "
                "`aₖ₊₁ = 2(2ᵏ⁺¹ - 1) + 1 = 2ᵏ⁺² - 1`, so that the formula, once true "
                "anywhere, is true for ever after. That is induction, and it is the "
                "Discrete Mathematics path's business rather than this one's.",
            ],
        },
        "quiz_title": "Terms and definitions",
        "quiz": [
            {"q": "A sequence is defined by `aₙ = 4n - 7` for `n ≥ 1`. What is its third term?",
             "a": ["`-3`", "`1`", "`5`", "`9`"],
             "c": 2,
             "why": "The third term is `a₃ = 4(3) - 7 = 5`. `-3` is `a₁` and `1` is "
                    "`a₂`; `9` comes from substituting `n = 4`, the off-by-one you get "
                    "by counting the first term as `a₀`."},
            {"q": "`a₁ = 2` and `aₙ = 3aₙ₋₁ - 1`. What is `a₄`?",
             "a": ["`14`", "`41`", "`53`", "`122`"],
             "c": 1,
             "why": "`a₂ = 5`, `a₃ = 14`, `a₄ = 41`. `14` is `a₃`, one step short. `53` "
                    "is `2·3³ - 1`, which subtracts the `1` only once instead of at "
                    "every step. `122` is `a₅`, one step too far."},
            {"q": "Why is `aₙ = 2aₙ₋₁` not a definition of a sequence?",
             "a": ["Because it does not say what `a₀` is",
                   "Because no initial term is given, so infinitely many sequences satisfy it",
                   "Because it cannot be turned into an explicit formula",
                   "Because doubling has no closed form"],
             "c": 1,
             "why": "`5, 10, 20, …`, `3, 6, 12, …` and `0, 0, 0, …` all obey that rule. "
                    "The recurrence says how to move, not where to start, and the "
                    "missing piece is any one term, not specifically `a₀`."},
        ],
        "mistakes": [
            ("Reading `a₃` as a product or as the number 3",
             "The subscript names a position. In `10, 20, 30, …` the third term is `30` "
             "and the index `3` appears nowhere in the answer. The same habit makes "
             "`aₙ₋₁` look like `aₙ - 1`, which it is not: it is the previous term, and "
             "in `3, 7, 15, 31, …` at `n = 4` they are `15` and `30`."),
            ("Off-by-one from an assumed starting index",
             "A formula written for `n` starting at `1` produces every term one place "
             "out when read as though it started at `0`. Any answer that is close but "
             "shifted by one position is this error, and writing out `a₁` explicitly "
             "before anything else catches it."),
            ("Treating a pattern in the first few terms as settled",
             "The chord-and-regions sequence begins `1, 2, 4, 8, 16` and continues "
             "`31`. Five agreements are evidence about the sixth term and nothing "
             "more, and the honest report says which terms were checked."),
        ],
        "standard": ("Finish when a recursion without an initial term reads as incomplete, not as terse.",
                     "You should be able to run any recursion out to five terms without "
                     "error, convert between the explicit and recursive forms of a "
                     "doubling sequence, and state what your explicit formula has "
                     "actually been checked against."),
        "note": "Two families of sequence have both forms available and a sum that can "
                "be written down exactly. Lesson 3 takes the ones built by adding a "
                "fixed number, lesson 4 the ones built by multiplying by a fixed "
                "number &mdash; and the second of those has a surprise in it, which is "
                "that infinitely many terms can add up to a finite number.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "sigma-notation",
        "title": "Sigma Notation",
        "module": "Sequences",
        "one_line": "Writing a sum without writing every term, and shifting the index.",
        "summary": (
            "Sigma notation stores a sum as two separate things: a rule for the terms "
            "and a range for the index. Reading one means expanding it, and writing one "
            "means choosing where the index starts, so the same sum has many correct "
            "sigmas. The manipulation worth learning is the shift, which moves the "
            "limits and the summand together and leaves the value alone."
        ),
        "key": [
            "      n",
            "      Σ  aₖ  =  a₁ + a₂ + … + aₙ        k is the index",
            "     k=1                                k=m to k=n is n - m + 1 terms",
            "                                        the letter k is private to the sum",
        ],
        "key_label": "The parts of a sigma, and how many terms it has",
        "concepts_intro": (
            "Nothing new is being computed here. What is new is that the rule for the "
            "terms and the range of the index are now written in different places."
        ),
        "concepts": [
            ("Sigma is an instruction, not an operation",
             "`Σ` says: substitute each integer of the range into the expression beside "
             "it, and add the results. Every sigma with whole-number limits could be "
             "written out with plus signs instead. It is worth having because it keeps "
             "the rule for the terms apart from how many of them there are."),
            ("The index is private to the sum",
             "The letter is a placeholder that exists between the limits and nowhere "
             "else. Summing `2k - 1` over `k` from `1` to `5` and summing `2j - 1` over "
             "`j` from `1` to `5` are the same number, `25`, written twice. Outside the "
             "sigma the letter means nothing, which is why the next sum on the page may "
             "reuse it."),
            ("The number of terms is `n - m + 1`",
             "From `k = 1` to `k = n` there are `n` terms, which is the case that hides "
             "the rule. From `k = 4` to `k = 11` there are `8`, not `7`. Both endpoints "
             "are included, so subtracting the limits counts the gaps between terms "
             "rather than the terms."),
        ],
        "read_title": "Reading a sigma, writing one, and shifting the index",
        "read_intro": "The four parts of the symbol, the three rules it obeys, and the substitution that moves the limits.",
        "body": [
            ("def", ("Sigma notation",
                     "For a sequence `aₖ` and integers `m ≤ n`, the symbol `Σ aₖ` with "
                     "`k` running from `m` to `n` means "
                     "`aₘ + aₘ₊₁ + … + aₙ`. The letter `k` is the <strong>index of "
                     "summation</strong>, `m` is the <strong>lower limit</strong>, `n` "
                     "the <strong>upper limit</strong>, and the expression being summed "
                     "is the <strong>summand</strong>.",
                     "Displayed, the limits sit under and over the `Σ`. In a line of "
                     "prose there is no room for that, so this course writes the `Σ`, "
                     "then the summand, and says the range in words. If the upper limit "
                     "is below the lower one there are no terms and the sum is `0`, "
                     "which is the number you have when you have added nothing.")),
            ("p", "The first thing to do with a sigma you have not met is expand it. "
                  "Substituting every value of the index in turn is slow and it is also "
                  "the definition, so it can never be wrong."),
            ("math", [
                "  5",
                "  Σ  k²  =  1² + 2² + 3² + 4² + 5²",
                " k=1",
                "         =  1 + 4 + 9 + 16 + 25",
                "         =  55",
            ]),
            ("p", "Two things the notation permits that are easy to miss. The summand "
                  "need not mention the index, in which case every term is the same and "
                  "the limits alone decide how many. And the lower limit need not be "
                  "`1`: starting at `0` is common, and starting at `2` is what you have "
                  "left after peeling the first term off something else."),
            ("example", ("Three sigmas expanded",
                         "`Σ 7` over `k` from `1` to `4` is `7 + 7 + 7 + 7 = 28`. The "
                         "`k` appears nowhere in the summand, and four terms is what the "
                         "limits asked for. "
                         "`Σ 2ᵏ` over `k` from `0` to `3` is `1 + 2 + 4 + 8 = 15`, and "
                         "the first term is `2⁰ = 1` rather than `2`. "
                         "`Σ (-1)ᵏ k` over `k` from `2` to `5` is "
                         "`2 - 3 + 4 - 5 = -2`, where the `(-1)ᵏ` is doing nothing but "
                         "setting signs.")),
            ("h3", "Writing a sum in sigma notation"),
            ("p", "Going the other way has two halves. Find a formula that produces the "
                  "terms from an index, then choose limits that produce exactly the "
                  "terms you want and no others. The second half is where the choice "
                  "lies, because a sum has no single correct sigma."),
            ("example", ("One sum, three sigmas",
                         "`3 + 5 + 7 + 9 + 11` is `35`, and all three of these produce "
                         "it: `Σ (2k + 1)` over `k` from `1` to `5`; `Σ (2k + 3)` over "
                         "`k` from `0` to `4`; `Σ (2k - 3)` over `k` from `3` to `7`. "
                         "Each has five terms, each starts at `3` and ends at `11`. "
                         "Which one you write is a matter of where you chose to start "
                         "counting, and nothing else.")),
            ("thm", ("What passes through a sigma",
                     "For any sequences `aₖ` and `bₖ`, any constant `c`, and any range "
                     "of `k` from `m` to `n`: `Σ c·aₖ = c·Σ aₖ`, and "
                     "`Σ (aₖ + bₖ) = Σ aₖ + Σ bₖ`, and `Σ c = (n - m + 1)c`.",
                     "The first two are the distributive law and the freedom to "
                     "reorder a finite sum, written for many terms at once. The third is "
                     "the constant summand: one `c` per value of the index, so the "
                     "multiplier is the term count and not `n`.")),
            ("p", "What is not on that list is a rule for products, and it is the one "
                  "people reach for. `Σ (aₖbₖ)` is not `(Σ aₖ)(Σ bₖ)`: take `k = 1, 2` with "
                  "`aₖ = bₖ = k`, and the left side is `1 + 4 = 5` while the right side "
                  "is `3 · 3 = 9`. Nor does a reciprocal pass through &mdash; with terms "
                  "`1` and `2`, `Σ (1/aₖ)` is `1 + 1/2 = 3/2` and `1/(Σ aₖ)` is `1/3`. "
                  "Sigma abbreviates addition, so addition and constant multiples pass "
                  "through it; a product, a quotient or a power of the terms has to be "
                  "expanded before anything can be said about it."),
            ("h3", "Shifting the index"),
            ("p", "Two sums can only be combined term by term when their indices run "
                  "over the same range, and most closed formulas are written for a sum "
                  "starting at `1`. Both situations call for the same move: change which "
                  "integers the index runs over without changing which numbers are added."),
            ("math", [
                "      7",
                "      Σ  (k - 2)  =  1 + 2 + 3 + 4 + 5  =  15",
                "     k=3",
                "",
                "  put k = j + 2:    k = 3 gives j = 1,   k = 7 gives j = 5",
                "                    the summand k - 2 becomes (j + 2) - 2 = j",
                "",
                "      5",
                "      Σ  j  =  1 + 2 + 3 + 4 + 5  =  15",
                "     j=1",
                "",
                "  limits down by 2, the index inside up by 2, terms unchanged",
            ]),
            ("p", "That is the whole rule: `k = j + c` sends the limits `m` and `n` to "
                  "`m - c` and `n - c`, and the summand `f(k)` to `f(j + c)`. Both "
                  "halves move or neither does. Expanding the first term of each form "
                  "and comparing is the check, and a shift made in the wrong direction "
                  "misses by exactly the amount shifted &mdash; obvious there, invisible "
                  "afterwards."),
        ],
        "lab": ("sequence", {
            "mode": "sigma",
            "panel_title": "Expand it, then shift it",
            "panel_intro": "Type a summand and a pair of limits, and the lab expands the "
                           "sum term by term and adds it exactly. Turn the shift dial and "
                           "the re-indexed sigma is printed beside the original, term "
                           "against term &mdash; next to the near miss that moves the "
                           "limits and leaves the summand alone, so you can read off what "
                           "that costs.",
        }),
        "steps_title": "Reading and rewriting a sigma",
        "steps_intro": "Four steps, and the first three are done before any adding starts.",
        "steps": [
            ("Name the four parts",
             "Index letter, lower limit, upper limit, summand. Writing them down "
             "separately is what makes you notice that the index is absent from the "
             "summand, or that the sum does not start at `1`."),
            ("Count the terms",
             "`n - m + 1`, before evaluating anything. The count is what you check the "
             "expansion against, and a wrong count is an error that leaves every line "
             "of the arithmetic looking perfectly normal."),
            ("Write the first two terms and the last one",
             "Substitute `m`, `m + 1` and `n`. A misread summand shows up in the first "
             "term, and a misread upper limit shows up in the last, both while they are "
             "still cheap to fix."),
            ("Shift only by substitution",
             "To move the lower limit, put `k = j + c` and rewrite the limits and the "
             "summand in the same step. Then expand the first term of the new form and "
             "confirm it equals the first term of the old one."),
        ],
        "worked": {
            "title": "Expanding, summing and shifting Σ (3k - 1) from k=2 to k=6",
            "intro": [
                "One sigma, three jobs: count its terms, add them, and rewrite it to "
                "start at `k = 1` without changing a single number."
            ],
            "lines": [
                "      6",
                "      Σ  (3k - 1)",
                "     k=2",
                "",
                "how many terms?    6 - 2 + 1 = 5          not 4",
                "",
                "k=2    3(2) - 1 =  5",
                "k=3    3(3) - 1 =  8",
                "k=4    3(4) - 1 = 11",
                "k=5    3(5) - 1 = 14",
                "k=6    3(6) - 1 = 17",
                "",
                "sum    5 + 8 + 11 + 14 + 17 = 55",
                "",
                "shift to start at 1:   put k = j + 1",
                "                       k = 2 gives j = 1,   k = 6 gives j = 5",
                "                       3k - 1 = 3(j + 1) - 1 = 3j + 2",
                "",
                "      5",
                "      Σ  (3j + 2)      j=1: 5    j=2: 8    j=3: 11",
                "     j=1               j=4: 14   j=5: 17",
                "",
                "                       the same five numbers, so the sum is 55    ✓",
            ],
            "after": [
                "The term count is the line that catches people. `6 - 2` is `4`, and "
                "there are five terms, because `k = 2` and `k = 6` are both included. "
                "Every wrong answer built on four terms is wrong by one whole term, "
                "which for this sum is between `5` and `17`.",
                "The shift moved the limits down by `1` and the index inside up by `1`. "
                "The value survived because `k = j + 1` renames the integers fed to the "
                "summand without changing which numbers come out. The check did not "
                "establish that; it established that this particular shift was carried "
                "out correctly.",
            ],
        },
        "quiz_title": "Reading, writing and shifting",
        "quiz": [
            {"q": "How many terms does `Σ aₖ` have when `k` runs from `4` to `11`?",
             "a": ["`7`", "`8`", "`11`", "`12`"],
             "c": 1,
             "why": "From `k = m` to `k = n` there are `n - m + 1` terms: "
                    "`11 - 4 + 1 = 8`. `7` is `11 - 4`, which counts the gaps between "
                    "terms. `11` reads the upper limit as the count, which is only right "
                    "when the sum starts at `k = 1`. `12` counts as though it started at "
                    "`k = 0`."},
            {"q": "What is `Σ (k² - k)` for `k` from `1` to `4`?",
             "a": ["`12`", "`20`", "`26`", "`30`"],
             "c": 1,
             "why": "The terms are `0, 2, 6, 12`, adding to `20`. `12` is the summand at "
                    "`k = 4` and nothing else, the last term reported as the sum. `30` "
                    "is `Σ k²` with the `- k` dropped. `26` is that `30` with the `k` "
                    "subtracted once at the end, using the upper limit, instead of inside "
                    "every term."},
            {"q": "`Σ (k + 4)` runs over `k` from `1` to `6`. Rewritten so the index runs from `0` to `5`, what is the summand?",
             "a": ["`j + 3`", "`j + 4`", "`j + 5`", "`j + 6`"],
             "c": 2,
             "why": "The limits went down by `1`, so put `k = j + 1` and the summand "
                    "`k + 4` becomes `j + 5`. Checking one term settles it: the original "
                    "first term is `k = 1` giving `5`, and `j = 0` must also give `5`. "
                    "`j + 4` moves the limits and leaves the summand alone, which drops "
                    "the value from `45` to `39`. `j + 3` shifts in the wrong direction "
                    "and `j + 6` shifts twice."},
        ],
        "mistakes": [
            ("Counting `n - m` terms instead of `n - m + 1`",
             "From `k = 4` to `k = 11` is `8` terms. The error is always by exactly one "
             "term and it is silent: the expansion looks reasonable and every formula "
             "applied to the wrong count inherits it. Counting `k = 1` to `k = 3` on "
             "your fingers recovers the rule when it goes."),
            ("Moving the limits and leaving the summand alone",
             "`Σ (k + 4)` over `k` from `1` to `6` is `45`. Changing the range to `0` to "
             "`5` and keeping `k + 4` gives `39`. Nothing on the page looks wrong, the "
             "term count is still `6`, and the value has moved by `6`. A shift is one "
             "substitution applied to both halves, never a decision to renumber."),
            ("Expecting a product or a reciprocal to pass through the `Σ`",
             "With `k = 1, 2` and `aₖ = bₖ = k`, `Σ (aₖbₖ)` is `5` and `(Σ aₖ)(Σ bₖ)` is "
             "`9`. A constant factor comes out and two sums add termwise; a product of "
             "the terms is a different sequence and has to be summed as one."),
        ],
        "standard": ("Finish when you can expand a sigma and shift its index without changing a single term.",
                     "You should be able to state a sum's term count before evaluating "
                     "it, write a given list of numbers in sigma notation in at least two "
                     "ways, and move a lower limit to `1` by substitution. Expanding the "
                     "first term of both forms is the check, and it costs one line."),
        "note": "Every sum from here on is written this way. Lesson 3 finds `Σ aₖ` for "
                "the sequences whose terms rise by a fixed amount, by pairing the list "
                "with its own reversal; lesson 4 does it for a fixed ratio, by "
                "subtracting `rSₙ` from `Sₙ`. Both arguments reorder the terms of a "
                "finite sum, which is legal precisely because the sum is finite &mdash; "
                "the point where that stops being safe is lesson 6.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "arithmetic-sequences-and-series",
        "title": "Arithmetic Sequences and Series",
        "module": "Sequences",
        "one_line": "A constant difference, and Gauss's trick for the sum.",
        "summary": (
            "An arithmetic sequence adds the same number to get from each term to the "
            "next. That one fact gives a formula for the n-th term, and a pairing "
            "argument gives the sum of any number of terms without adding them up."
        ),
        "key": [
            "d = aₙ₊₁ - aₙ        the same number for every n",
            "aₙ = a₁ + (n - 1)d              n - 1 steps, not n",
            "Sₙ = n(a₁ + aₙ)/2  =  (n/2)[2a₁ + (n - 1)d]",
            "1 + 2 + … + 100  =  100(1 + 100)/2  =  5050",
        ],
        "key_label": "The term formula, the sum formula, and Gauss's example",
        "concepts_intro": (
            "Two formulas, and one habit of checking. The habit is what keeps the "
            "formulas from being applied to sequences that do not qualify."
        ),
        "concepts": [
            ("The difference has to be constant, and one difference is not a check",
             "`d = a₂ - a₁` is a guess until `a₃ - a₂` and `a₄ - a₃` agree with it. "
             "`2, 4, 8, 16` has first difference `2` and is not arithmetic; `1, 4, 9, "
             "16` has differences `3, 5, 7` and is not either, though both look "
             "orderly."),
            ("`n - 1`, not `n`",
             "Getting to `a₁` takes no steps, to `a₂` one step, to `a₁₀` nine. The "
             "formula counts steps, and every off-by-one in this lesson is the "
             "difference between counting steps and counting terms."),
            ("A series is a sum, and `Sₙ` is a single number",
             "The sequence `5, 9, 13, …` is a list; `S₃ = 27` is one number. Asking for "
             "\"the 20th term\" and \"the sum of the first 20 terms\" are different "
             "questions with different answers &mdash; `81` and `860` for the sequence "
             "in the worked example."),
        ],
        "read_title": "Constant difference, and the sum of n terms",
        "read_intro": "The n-th term by counting steps, then the sum by writing it out twice.",
        "body": [
            ("def", ("Arithmetic sequence",
                     "A sequence in which the difference between consecutive terms is "
                     "the same throughout. That number is the <strong>common "
                     "difference</strong> `d`, and the recursive definition is "
                     "`aₙ = aₙ₋₁ + d` together with a first term `a₁`.")),
            ("p", "`3, 7, 11, 15, …` has `d = 4`. `20, 17, 14, 11, …` has `d = -3`; a "
                  "negative common difference is ordinary and the formulas do not "
                  "change. `5, 5, 5, 5, …` has `d = 0` and is arithmetic, which is a "
                  "useful edge case rather than a trick."),
            ("p", "Reaching `aₙ` from `a₁` means adding `d` a certain number of times, "
                  "and the number of times is the number of steps between the two "
                  "positions:"),
            ("math", [
                "a₁ = a₁",
                "a₂ = a₁ + d",
                "a₃ = a₁ + 2d",
                "a₄ = a₁ + 3d",
                "…",
                "aₙ = a₁ + (n - 1)d          the coefficient is one less than",
                "                            the index, every time",
            ]),
            ("thm", ("The n-th term of an arithmetic sequence",
                     "If `a₁` is the first term and `d` the common difference, then "
                     "`aₙ = a₁ + (n - 1)d` for every `n ≥ 1`. Rearranged, "
                     "`d = (aₙ - a₁)/(n - 1)`, which recovers the common difference "
                     "from the first term and any one other term. From two terms in "
                     "general positions it is `d = (aₙ - aₘ)/(n - m)`.")),
            ("p", "Plotted, an arithmetic sequence is a row of dots lying on a straight "
                  "line of slope `d` &mdash; course 3's slope, sampled at the integers. "
                  "`aₙ = a₁ + (n - 1)d` is `y = mx + c` with the letters renamed, which "
                  "is why a sequence with a constant difference is called linear."),
            ("def", ("Series and partial sum",
                     "A <strong>series</strong> is the sum of the terms of a sequence. "
                     "The sum of the first `n` terms is the <strong>n-th partial "
                     "sum</strong> `Sₙ = a₁ + a₂ + … + aₙ`, also written "
                     "`Sₙ = Σ aₖ` with `k` running from `1` to `n`. It is a number, not "
                     "a list.")),
            ("thm", ("The sum of an arithmetic series",
                     "`Sₙ = n(a₁ + aₙ)/2`. Substituting `aₙ = a₁ + (n - 1)d` gives the "
                     "equivalent form `Sₙ = (n/2)[2a₁ + (n - 1)d]`. The first is "
                     "convenient when the last term is known, the second when only "
                     "`a₁` and `d` are.")),
            ("proof", [
                "Write the sum out, and then write it out again in the opposite order: "
                "`Sₙ = a₁ + (a₁ + d) + … + (aₙ - d) + aₙ` and "
                "`Sₙ = aₙ + (aₙ - d) + … + (a₁ + d) + a₁`.",
                "Add the two lines column by column. The first column gives "
                "`a₁ + aₙ`. The second gives `(a₁ + d) + (aₙ - d) = a₁ + aₙ`. Every "
                "column gives the same total, because each step of `+d` down the first "
                "line is matched by a step of `-d` up the second.",
                "There are `n` columns and each totals `a₁ + aₙ`, so "
                "`2Sₙ = n(a₁ + aₙ)`, and dividing by `2` gives the formula. Nothing "
                "here depends on `n` being even or on the terms being positive.",
            ]),
            ("example", ("Gauss's sum",
                         "`1 + 2 + 3 + … + 100` is arithmetic with `a₁ = 1`, `d = 1`, "
                         "`a₁₀₀ = 100`. So `S₁₀₀ = 100(1 + 100)/2 = 50(101) = 5050`. "
                         "The story is that Gauss found this at school by pairing `1` "
                         "with `100`, `2` with `99`, and so on: fifty pairs, each "
                         "totalling `101`.")),
            ("example", ("The first n odd numbers",
                         "`1, 3, 5, 7, …` is arithmetic with `a₁ = 1` and `d = 2`, so "
                         "the n-th odd number is `1 + 2(n - 1) = 2n - 1` and "
                         "`Sₙ = n(1 + 2n - 1)/2 = n²`. The first five partial sums are "
                         "`1, 4, 9, 16, 25`, which is the fact that the odd numbers add "
                         "up to the squares.")),
            ("p", "One last check that costs nothing: `Sₙ = n(a₁ + aₙ)/2` says the sum "
                  "is `n` times the average of the first and last terms. If `20` terms "
                  "run from `5` to `81`, the average is `43` and the sum should be near "
                  "`860` &mdash; and it is exactly `860`, because for an arithmetic "
                  "sequence that average is exact rather than approximate."),
        ],
        "lab": ("sequence", {
            "mode": "arithmetic",
            "panel_title": "Terms, and the running total",
            "panel_intro": "Set `a₁` and `d` and the lab lists the terms with the "
                           "partial sums beside them, and compares each partial sum "
                           "with the formula. Set `d` negative and watch the sum turn "
                           "around.",
        }),
        "steps_title": "Answering a question about an arithmetic sequence",
        "steps_intro": "Establish that it is arithmetic first. The formulas are false for anything else.",
        "steps": [
            ("Check at least three consecutive differences",
             "Compute `a₂ - a₁`, `a₃ - a₂`, `a₄ - a₃`. If they disagree, the sequence "
             "is not arithmetic and nothing below applies."),
            ("Write down a₁ and d",
             "Both explicitly, before substituting anything. Most wrong answers in "
             "this topic come from the wrong `d`, and the commonest wrong `d` is the "
             "one with the sign flipped in a decreasing sequence."),
            ("For a term, use aₙ = a₁ + (n - 1)d",
             "For the sum, get `aₙ` first and then `Sₙ = n(a₁ + aₙ)/2`; or use "
             "`Sₙ = (n/2)[2a₁ + (n - 1)d]` and skip the intermediate term."),
            ("Check the size against the average",
             "`Sₙ` should equal `n` times the midpoint of the first and last terms. A "
             "sum that is roughly double or half what that suggests is a dropped `/2` "
             "or a doubled one."),
        ],
        "worked": {
            "title": "The 20th term and the sum of the first 20 terms of 5, 9, 13, 17, …",
            "intro": [
                "Two questions that are often confused with each other, answered from "
                "the same two numbers."
            ],
            "lines": [
                "differences   9 - 5 = 4    13 - 9 = 4    17 - 13 = 4",
                "              arithmetic, with d = 4 and a₁ = 5",
                "",
                "aₙ  = a₁ + (n - 1)d = 5 + 4(n - 1) = 4n + 1",
                "a₂₀ = 5 + 4(19) = 5 + 76 = 81",
                "                  19, not 20:  a₂₀ is nineteen steps past a₁",
                "",
                "S₂₀ = 20(a₁ + a₂₀)/2 = 20(5 + 81)/2 = 10(86) = 860",
                "",
                "the other form, without computing a₂₀ first",
                "S₂₀ = (20/2)[2(5) + 19(4)] = 10[10 + 76] = 10(86) = 860",
                "",
                "check   the average of first and last is (5 + 81)/2 = 43",
                "        and 20(43) = 860                                ✓",
            ],
            "after": [
                "The two forms of the sum formula are the same formula, and they agree "
                "here as they must. Which one to use is a question of what the problem "
                "gave you: a last term, or a common difference.",
                "`81` and `860` are the answers to two different questions. \"The 20th "
                "term\" is one term of the list; \"the sum of the first 20 terms\" adds "
                "all twenty. Reading the question twice is cheaper than computing the "
                "wrong one correctly.",
            ],
        },
        "quiz_title": "Terms and sums",
        "quiz": [
            {"q": "An arithmetic sequence has `a₁ = 7` and `d = -3`. What is `a₁₂`?",
             "a": ["`-23`", "`-26`", "`-29`", "`26`"],
             "c": 1,
             "why": "`a₁₂ = 7 + 11(-3) = 7 - 33 = -26`. `-29` uses `12` steps instead of "
                    "`11`; `-23` uses `10`; `26` loses the sign of `d` somewhere and "
                    "then the sign of the answer."},
            {"q": "What is the sum of the first 30 terms of `4, 7, 10, 13, …`?",
             "a": ["`1365`", "`1425`", "`1470`", "`2850`"],
             "c": 1,
             "why": "`a₃₀ = 4 + 29(3) = 91`, so `S₃₀ = 30(4 + 91)/2 = 1425`. `1470` "
                    "comes from `a₃₀ = 4 + 30(3) = 94`; `2850` from forgetting to "
                    "divide by `2`; `1365` from using `30(91)/2` and leaving out `a₁`."},
            {"q": "Which of these sequences is arithmetic?",
             "a": ["`1, 4, 9, 16, 25`", "`3, 7, 11, 15`", "`2, 6, 18, 54`",
                   "`1, 1, 2, 3, 5`"],
             "c": 1,
             "why": "Its differences are `4, 4, 4`. The squares have differences "
                    "`3, 5, 7`; `2, 6, 18, 54` triples each time and is geometric; the "
                    "last is Fibonacci, whose differences are `0, 1, 1, 2`."},
        ],
        "mistakes": [
            ("Writing `a₁ + nd` instead of `a₁ + (n - 1)d`",
             "It gives the term after the one asked for, so the answer is wrong by "
             "exactly `d` and looks entirely reasonable. Substituting `n = 1` into your "
             "own formula catches it at once: it must return `a₁`."),
            ("Calling a sequence arithmetic on the strength of one difference",
             "`2, 4, 8, 16` starts with a difference of `2` and never repeats it. "
             "Checking the second and third differences takes five seconds and is the "
             "only thing standing between you and applying a formula that does not "
             "hold."),
            ("Confusing aₙ with Sₙ",
             "In the worked example these are `81` and `860`. The wording that decides "
             "it is \"the n-th term\" against \"the sum of the first n terms\", and a "
             "problem about total seats in a theatre wants the second even though it "
             "describes the rows one at a time."),
        ],
        "standard": ("Finish when you count steps rather than terms without thinking about it.",
                     "Given any three of `a₁`, `d`, `n`, `aₙ`, `Sₙ` you should be able "
                     "to produce the others, and to say which of the two sum formulas "
                     "the given information calls for. The pairing argument should be "
                     "reproducible from memory: it is three lines and it is the reason "
                     "the formula is true."),
        "note": "Replacing \"add `d`\" by \"multiply by `r`\" gives the other family of "
                "sequences with exact formulas, and it changes the shape completely: "
                "linear growth becomes exponential, and the sum of infinitely many "
                "terms &mdash; which for an arithmetic sequence never settles on a "
                "number unless every term is zero &mdash; becomes possible. That is "
                "lesson 4.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "geometric-sequences-and-series",
        "title": "Geometric Sequences and Series",
        "module": "Sequences",
        "one_line": "A constant ratio, and a sum that can be infinite.",
        "summary": (
            "A geometric sequence multiplies by the same number at every step. The n-th "
            "term is `a₁rⁿ⁻¹`, and the sum of `n` terms comes from one line of algebra. "
            "When `|r| &lt; 1`, all infinitely many terms add up to a finite number."
        ),
        "key": [
            "r = aₙ₊₁/aₙ          the same number for every n",
            "aₙ = a₁rⁿ⁻¹                        n - 1 multiplications",
            "Sₙ = a₁(1 - rⁿ)/(1 - r)            needs r ≠ 1",
            "S∞ = a₁/(1 - r)                    only when |r| < 1",
        ],
        "key_label": "Two formulas, and the condition on the third",
        "concepts_intro": (
            "The first two formulas are the arithmetic ones with multiplication in "
            "place of addition. The third is genuinely new and it comes with a "
            "condition that is not decoration."
        ),
        "concepts": [
            ("The ratio is a quotient, not a difference",
             "`r = a₂/a₁`, checked against `a₃/a₂` and `a₄/a₃`. Reaching for a "
             "subtraction here is the reflex left over from lesson 3: `3, 6, 12, 24` "
             "has differences `3, 6, 12` and ratios `2, 2, 2`, and only the second list "
             "being constant makes it geometric."),
            ("`rⁿ⁻¹`, for the same reason as `(n - 1)d`",
             "`a₁` has been multiplied by `r` no times, `a₂` once, `aₙ` exactly "
             "`n - 1` times. The exponent counts steps, and `a₁rⁿ` is the term after "
             "the one you wanted."),
            ("`|r| < 1` is a condition, not a formality",
             "Outside it the expression `a₁/(1 - r)` still produces a number, and that "
             "number is not the sum of anything. For `2 + 6 + 18 + …` it produces `-1`: "
             "a negative value for a series of positive terms, which is what applying a "
             "formula outside its range looks like."),
        ],
        "read_title": "Constant ratio, finite sums, and infinite ones",
        "read_intro": "The n-th term, the sum of n terms by a cancelling trick, and the one case where infinitely many terms have a total.",
        "body": [
            ("def", ("Geometric sequence",
                     "A sequence in which the ratio of consecutive terms is the same "
                     "throughout. That number is the <strong>common ratio</strong> `r`, "
                     "and the recursive definition is `aₙ = r·aₙ₋₁` with a first term "
                     "`a₁`. Neither `a₁` nor `r` may be `0`, or the ratios stop being "
                     "defined.")),
            ("p", "`3, 6, 12, 24, …` has `r = 2`. `81, 27, 9, 3, …` has `r = 1/3` and "
                  "shrinks. `5, -10, 20, -40, …` has `r = -2`, and a negative ratio is "
                  "how a sequence alternates in sign: odd-numbered terms keep the sign "
                  "of `a₁` and even-numbered ones flip it."),
            ("thm", ("The n-th term of a geometric sequence",
                     "`aₙ = a₁rⁿ⁻¹` for every `n ≥ 1`. Getting from `a₁` to `aₙ` is "
                     "`n - 1` multiplications by `r`, exactly as getting there in an "
                     "arithmetic sequence was `n - 1` additions of `d`.")),
            ("p", "Plotted, the terms lie on an exponential curve rather than a line: "
                  "`a₁rⁿ⁻¹` is course 7's `a·bˣ` sampled at the integers. `|r| &gt; 1` "
                  "gives growth, `|r| &lt; 1` gives decay, `r &lt; 0` makes the sign "
                  "alternate, and `r = 1` gives a constant sequence."),
            ("def", ("Geometric series",
                     "The sum of the terms of a geometric sequence. `Sₙ` denotes the "
                     "sum of the first `n` terms, `a₁ + a₁r + … + a₁rⁿ⁻¹`.")),
            ("thm", ("The sum of n terms",
                     "For `r ≠ 1`, `Sₙ = a₁(1 - rⁿ)/(1 - r)`. For `r = 1` every term "
                     "equals `a₁` and `Sₙ = na₁`.")),
            ("proof", [
                "Write `Sₙ = a₁ + a₁r + a₁r² + … + a₁rⁿ⁻¹`, and multiply the whole line "
                "by `r`: `rSₙ = a₁r + a₁r² + … + a₁rⁿ⁻¹ + a₁rⁿ`.",
                "Subtract the second line from the first. Every term of `rSₙ` also "
                "appears in `Sₙ` except the last, and every term of `Sₙ` appears in "
                "`rSₙ` except the first, so all but two cancel: "
                "`Sₙ - rSₙ = a₁ - a₁rⁿ`.",
                "Factor both sides: `Sₙ(1 - r) = a₁(1 - rⁿ)`. Dividing by `1 - r` "
                "requires `r ≠ 1`, which is precisely the case the theorem handles "
                "separately, and there the sum is `na₁` by inspection.",
            ]),
            ("h3", "Adding infinitely many terms"),
            ("p", "Take `4 + 2 + 1 + 1/2 + 1/4 + …` , with `a₁ = 4` and `r = 1/2`. The "
                  "partial sums are `4, 6, 7, 7.5, 7.75, 7.875, …` . They increase, "
                  "they never reach `8`, and they get as close to `8` as you please. "
                  "The formula shows why: `Sₙ = 4(1 - (1/2)ⁿ)/(1/2) = 8(1 - (1/2)ⁿ)`, "
                  "and `(1/2)ⁿ` is being driven toward zero."),
            ("p", "How small is `rⁿ` really? For `r = 1/2` and `n = 20` it is "
                  "`1/1048576`. That is what \"the `rⁿ` term stops mattering\" means "
                  "concretely: the partial sum differs from `8` by eight millionths at "
                  "the twentieth term, and by less at every term after it."),
            ("thm", ("The sum of an infinite geometric series",
                     "If `|r| &lt; 1`, the partial sums approach the single number "
                     "`a₁/(1 - r)`, and can be brought as close to it as desired by "
                     "taking enough terms. That number is written `S∞` and is called "
                     "the sum of the series.",
                     "If `|r| ≥ 1` there is no sum. The terms do not shrink toward "
                     "zero, so the partial sums cannot settle: for `|r| &gt; 1` they "
                     "grow without bound, for `r = 1` they are `na₁`, and for `r = -1` "
                     "they alternate between `a₁` and `0` for ever.")),
            ("example", ("0.999… is exactly 1",
                         "The decimal `0.999…` means "
                         "`9/10 + 9/100 + 9/1000 + …` , a geometric series with "
                         "`a₁ = 9/10` and `r = 1/10`. Since `|r| &lt; 1`, "
                         "`S∞ = (9/10)/(1 - 1/10) = (9/10)/(9/10) = 1`. The two "
                         "notations name the same number; there is no gap for anything "
                         "to sit in.")),
        ],
        "lab": ("sequence", {
            "mode": "geometric",
            "panel_title": "Partial sums, and where they go",
            "panel_intro": "Set `a₁` and `r` and the lab plots the partial sums against "
                           "the value `a₁/(1 - r)`. Push `r` past `1` and watch the "
                           "partial sums leave the line behind while the formula keeps "
                           "returning a number.",
        }),
        "steps_title": "Answering a question about a geometric sequence",
        "steps_intro": "Four steps, and the fourth begins with a test rather than a formula.",
        "steps": [
            ("Confirm the ratio is constant",
             "Divide at least twice: `a₂/a₁` and `a₃/a₂`. Write `r` as an exact "
             "fraction, not a decimal &mdash; `r = 1/3` raised to the tenth power is "
             "exact, and `0.333` raised to the tenth power is not."),
            ("Use aₙ = a₁rⁿ⁻¹ for a term",
             "Compute the power first, then multiply by `a₁`. With a negative `r`, "
             "settle the sign by the parity of the exponent before touching the "
             "arithmetic."),
            ("Use Sₙ = a₁(1 - rⁿ)/(1 - r) for a finite sum",
             "Both `1 - rⁿ` and `1 - r` may be negative; a negative divided by a "
             "negative is what makes a growing series come out positive."),
            ("For an infinite sum, test |r| < 1 before anything else",
             "If `|r| ≥ 1` the answer is that the series has no sum, and that is a "
             "complete answer. Only if the test passes does `S∞ = a₁/(1 - r)` mean "
             "anything."),
        ],
        "worked": {
            "title": "The 10th term and the sums of 3, 6, 12, 24, …",
            "intro": [
                "One sequence, three questions: a term, a finite sum, and whether the "
                "whole series adds up to anything."
            ],
            "lines": [
                "ratios   6/3 = 2     12/6 = 2     24/12 = 2",
                "         geometric, with r = 2 and a₁ = 3",
                "",
                "aₙ  = 3·2ⁿ⁻¹",
                "a₁₀ = 3·2⁹ = 3(512) = 1536         not 3·2¹⁰ = 3072",
                "",
                "S₁₀ = 3(1 - 2¹⁰)/(1 - 2) = 3(1 - 1024)/(-1) = 3(1023) = 3069",
                "",
                "check by adding the ten terms",
                "3 + 6 + 12 + 24 + 48 + 96 + 192 + 384 + 768 + 1536 = 3069    ✓",
                "",
                "an infinite sum?    |r| = 2, and 2 ≥ 1, so there is none.",
                "the partial sums    3, 9, 21, 45, 93, 189, …  grow without bound",
                "the formula anyway  a₁/(1 - r) = 3/(1 - 2) = -3",
            ],
            "after": [
                "That last line is the trap this lesson exists to set off in advance. "
                "`-3` is a perfectly good number and it is not the sum of "
                "`3 + 6 + 12 + …` , which has no sum: every partial sum is positive and "
                "each is larger than the last. The formula was derived for `|r| &lt; 1` "
                "and it returns nonsense politely, without any error message.",
                "The check by hand is worth doing once. Ten terms added directly agree "
                "with the formula exactly, which verifies this one instance &mdash; "
                "`a₁ = 3`, `r = 2`, `n = 10`. What makes the formula true for every "
                "`a₁`, every `r ≠ 1` and every `n` is the `Sₙ - rSₙ` cancellation, "
                "not the check.",
            ],
        },
        "quiz_title": "Ratios and sums",
        "quiz": [
            {"q": "For the sequence `5, -10, 20, -40, …` , what is `a₇`?",
             "a": ["`320`", "`-320`", "`-640`", "`640`"],
             "c": 0,
             "why": "`r = -2`, so `a₇ = 5(-2)⁶ = 5(64) = 320`. `-320` treats an even "
                    "power of a negative as negative; `-640` uses the exponent `7` "
                    "instead of `6`, and it is `a₈`; `640` makes both errors at once."},
            {"q": "What is the sum of the infinite series `6 + 4 + 8/3 + 16/9 + …` ?",
             "a": ["`3`", "`9`", "`18`", "It has no sum"],
             "c": 2,
             "why": "`r = 4/6 = 2/3` and `|r| &lt; 1`, so "
                    "`S∞ = 6/(1 - 2/3) = 6/(1/3) = 18`. `3` is `1/(1 - r)` with `a₁` "
                    "left out; `9` is `a₁/r`."},
            {"q": "Does `2 + 6 + 18 + 54 + …` have a sum?",
             "a": ["Yes: `a₁/(1 - r) = 2/(1 - 3) = -1`",
                   "Yes: `2/(3 - 1) = 1`",
                   "No: `|r| = 3 ≥ 1`, and the partial sums grow without bound",
                   "No: a series of infinitely many positive terms cannot total a finite number"],
             "c": 2,
             "why": "The first two apply the formula where it does not hold, and the "
                    "second also flips the denominator to avoid the negative answer the "
                    "first produced. The fourth is contradicted by "
                    "`4 + 2 + 1 + … = 8`, where infinitely many positive terms do have "
                    "a finite total."},
        ],
        "mistakes": [
            ("Using `S∞ = a₁/(1 - r)` without testing `|r| < 1`",
             "The formula answers whether or not it applies, and it answers wrongly "
             "when it does not. The symptom to watch for is a negative sum for a series "
             "of positive terms, but a wrong positive answer is just as easy to produce "
             "and shows nothing on its face."),
            ("Writing `a₁rⁿ` for the n-th term",
             "That is `aₙ₊₁`, so every answer is one step too far and off by a factor "
             "of `r`. The same check as in lesson 3 applies: your formula must return "
             "`a₁` when `n = 1`."),
            ("Finding `r` by subtracting, or checking only one ratio",
             "`2, 4, 6` and `2, 4, 8` both begin with a difference of `2` and a ratio "
             "of `2`, and the third term decides which family each belongs to. Two "
             "ratios are the minimum test, and three is better."),
        ],
        "standard": ("Finish when the |r| < 1 test happens before the formula, every time.",
                     "You should be able to find `r`, produce any term, sum any number "
                     "of terms, and answer \"is there an infinite sum\" with a reason "
                     "rather than a formula. Reproducing the `Sₙ - rSₙ` cancellation "
                     "should take three lines and no hesitation."),
        "note": "The `0.999…` example generalises: every repeating decimal is a "
                "terminating decimal plus a geometric series with `|r| &lt; 1`, so "
                "every repeating decimal is a fraction. Course 1 asserted that when it "
                "sorted the real numbers into rational and irrational; this is the argument behind the assertion, "
                "and it needed an infinite sum to state.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "partial-sums-and-telescoping",
        "title": "Partial Sums and Telescoping",
        "module": "Arithmetic and geometric",
        "one_line": "The sequence of sums, and the ones that collapse.",
        "summary": (
            "Stopping a series at every possible place produces one number for each "
            "stopping place, and those numbers form a sequence of their own. Subtracting "
            "consecutive members of it returns the original terms, and a series whose "
            "terms are themselves differences collapses to the two ends."
        ),
        "key": [
            "Sₙ = a₁ + a₂ + … + aₙ           S₁, S₂, S₃, … is itself a sequence",
            "aₙ = Sₙ - Sₙ₋₁   for n ≥ 2      the terms come back by subtracting",
            "Σ (bₖ - bₖ₊₁)  =  b₁ - bₙ₊₁     everything between cancels in pairs",
            "1/(k(k+1)) = 1/k - 1/(k+1)      so Sₙ = 1 - 1/(n+1) = n/(n+1)",
        ],
        "key_label": "The sequence of sums, and the sum that collapses",
        "concepts_intro": (
            "One shift of attention and one technique. The shift is from a single sum to "
            "the list of all of them."
        ),
        "concepts": [
            ("For a fixed `n`, `Sₙ` is a number; letting `n` run gives a sequence",
             "Lesson 3 was emphatic that `S₂₀ = 860` is one number and not a list, and "
             "that is still true. But there is an `S₁`, an `S₂`, an `S₃`, one for each "
             "`n`, and a rule assigning one number to each positive integer is a "
             "sequence by lesson 1's definition &mdash; recursion and all."),
            ("The terms can be recovered from the sums",
             "`Sₙ` contains `Sₙ₋₁` plus one extra term, so `aₙ = Sₙ - Sₙ₋₁`. A formula "
             "for the sums therefore determines the sequence, and the two directions are "
             "an addition and a subtraction. The catch is `n = 1`, where there is no "
             "`Sₙ₋₁` to subtract."),
            ("Telescoping engineers the cancellation rather than hoping for it",
             "If every term can be written as `bₖ - bₖ₊₁` for some sequence `b`, the "
             "sum of `n` of them is `b₁ - bₙ₊₁` and everything between has cancelled in "
             "pairs. Lesson 4's `Sₙ - rSₙ` argument was exactly this. Finding the `bₖ` "
             "is the hard part, and there is no procedure for it."),
        ],
        "read_title": "The sequence of partial sums, and sums that collapse",
        "read_intro": "One number for each stopping place, the subtraction that undoes the adding, and series whose middle cancels.",
        "body": [
            ("def", ("Sequence of partial sums",
                     "Given a sequence `a₁, a₂, a₃, …` , its <strong>partial "
                     "sums</strong> are `S₁ = a₁`, `S₂ = a₁ + a₂`, and in general "
                     "`Sₙ = Σ aₖ` with `k` running from `1` to `n`. The list "
                     "`S₁, S₂, S₃, …` is the <strong>sequence of partial sums</strong> "
                     "of the series.",
                     "A series and its sequence of partial sums are two names for one "
                     "situation. Every question about the series &mdash; how big does it "
                     "get, does it settle &mdash; is a question about this sequence.")),
            ("p", "The partial sums have a recursion, and it is the cheapest way to "
                  "build a table of them: `S₁ = a₁` and `Sₙ = Sₙ₋₁ + aₙ`. Each new "
                  "partial sum costs one addition rather than `n` of them, which is what "
                  "makes computing twenty of them by hand a reasonable thing to do."),
            ("math", [
                "n           1     2     3     4     5     6",
                "aₙ          1     3     5     7     9    11        the odd numbers",
                "Sₙ          1     4     9    16    25    36        the squares",
                "",
                "Sₙ - Sₙ₋₁         3     5     7     9    11        = aₙ, every time",
            ]),
            ("thm", ("Recovering the terms from the sums",
                     "`a₁ = S₁`, and `aₙ = Sₙ - Sₙ₋₁` for every `n ≥ 2`.",
                     "The proof is one line: `Sₙ = (a₁ + … + aₙ₋₁) + aₙ = Sₙ₋₁ + aₙ`, "
                     "and subtracting `Sₙ₋₁` from both sides gives the statement. The "
                     "restriction to `n ≥ 2` is not fussiness &mdash; `S₀` was never "
                     "given a value.")),
            ("p", "So a formula for `Sₙ` determines the terms, and the first one has to "
                  "be handled on its own. Take `Sₙ = n² + 5`. For `n ≥ 2`, "
                  "`aₙ = (n² + 5) - ((n - 1)² + 5) = n² - (n - 1)² = 2n - 1`. But "
                  "`a₁ = S₁ = 6`, and `2n - 1` at `n = 1` is `1`, so the sequence is "
                  "`6, 3, 5, 7, 9, …` with a genuinely exceptional first term. With "
                  "`Sₙ = n²` the same computation gives `2n - 1` again and `a₁ = S₁ = 1` "
                  "does match it. Which of the two happens has to be checked."),
            ("h3", "Telescoping"),
            ("def", ("Telescoping sum",
                     "A sum whose terms are the differences of consecutive members of "
                     "one sequence: `aₖ = bₖ - bₖ₊₁` for every `k` in the range. The "
                     "name is the instrument &mdash; the sum closes up on itself and "
                     "only the two ends are left showing.")),
            ("math", [
                "   n",
                "   Σ  (bₖ - bₖ₊₁)  =  (b₁ - b₂) + (b₂ - b₃) + … + (bₙ - bₙ₊₁)",
                "  k=1",
                "",
                "                       b₂ appears with a minus, then with a plus",
                "                       b₃ appears with a minus, then with a plus",
                "                       and so on up to bₙ",
                "",
                "                  =  b₁ - bₙ₊₁",
            ]),
            ("thm", ("Telescoping",
                     "For any sequence `b` whatever, `Σ (bₖ - bₖ₊₁) = b₁ - bₙ₊₁` with "
                     "`k` running from `1` to `n`. In the other orientation, "
                     "`Σ (bₖ₊₁ - bₖ) = bₙ₊₁ - b₁`; it is the same statement with every "
                     "sign reversed.",
                     "No condition is placed on `b`. It need not be arithmetic, "
                     "geometric, positive or increasing.")),
            ("proof", [
                "Write the sum as `n` brackets: `(b₁ - b₂) + (b₂ - b₃) + … + "
                "(bₙ - bₙ₊₁)`. Take any `bₘ` with `2 ≤ m ≤ n`. It occurs twice: as the "
                "subtracted half of bracket `m - 1`, and as the added half of bracket "
                "`m`. Those two occurrences cancel.",
                "What has no partner is the added `b₁` in the first bracket and the "
                "subtracted `bₙ₊₁` in the last. So the total is `b₁ - bₙ₊₁`.",
                "The only property used is that a finite sum may be regrouped freely, "
                "which is the associative law applied finitely many times. There are "
                "`n` brackets and `2n` terms, and the finiteness is what makes the "
                "argument legal.",
            ]),
            ("example", ("The sum of 1/(k(k+1))",
                         "First check the split rather than asserting it: "
                         "`1/k - 1/(k + 1) = ((k + 1) - k)/(k(k + 1)) = 1/(k(k + 1))`. "
                         "So with `bₖ = 1/k`, the term `1/(k(k + 1))` is exactly "
                         "`bₖ - bₖ₊₁`, and the sum from `k = 1` to `n` is "
                         "`b₁ - bₙ₊₁ = 1 - 1/(n + 1) = n/(n + 1)`. For `n = 1, 2, 3, 4` "
                         "that predicts `1/2, 2/3, 3/4, 4/5`, and adding the terms by "
                         "hand gives the same four numbers.")),
            ("p", "The geometric sum formula was a telescoping in disguise. Put "
                  "`bₖ = a₁rᵏ⁻¹`, the `k`-th term of the sequence. Then "
                  "`bₖ - bₖ₊₁ = a₁rᵏ⁻¹ - a₁rᵏ = a₁rᵏ⁻¹(1 - r)`, so summing from `1` to "
                  "`n` gives `(1 - r)Sₙ` on one side and `b₁ - bₙ₊₁ = a₁ - a₁rⁿ` on the "
                  "other. That is `Sₙ(1 - r) = a₁(1 - rⁿ)`, which is where lesson 4 "
                  "arrived by multiplying the sum by `r` and subtracting. The two routes "
                  "are the same cancellation described differently."),
            ("p", "The difficulty is always finding `bₖ`, and there is no method. "
                  "Single fractions with a factorable denominator are the usual "
                  "candidates, and the test is whether the split recombines: if "
                  "`bₖ - bₖ₊₁` does not simplify back to `aₖ`, the split is wrong. One "
                  "more that works: with `bₖ = (k - 1)²`, `bₖ₊₁ - bₖ` is "
                  "`k² - (k - 1)² = 2k - 1`, so the first `n` odd numbers sum to "
                  "`bₙ₊₁ - b₁ = n² - 0 = n²` &mdash; a second derivation of a result "
                  "lesson 3 reached by pairing. Strictly, every series telescopes: "
                  "`bₖ = -Sₖ₋₁` satisfies `bₖ - bₖ₊₁ = aₖ` for any sequence at all. It "
                  "is no help, because it requires the sums you were trying to find."),
        ],
        "lab": ("sequence", {
            "mode": "partial",
            "panel_title": "Terms, sums, and the differences back",
            "panel_intro": "Enter a term `a(n)` and the lab lists the terms with the "
                           "partial sums beside them. Enter a partner `b(n)` as well and it "
                           "tests your claim that `a(n) = b(n) - b(n+1)` at every `n` "
                           "before collapsing anything, then computes `Sₙ` twice: by adding, "
                           "and as `b(1) - b(n+1)`. Hand it a split that is wrong and it "
                           "says which `n` the claim fails at.",
        }),
        "steps_title": "Working through a series by its partial sums",
        "steps_intro": "Four steps. The third has no procedure behind it, and the fourth is what tells you whether it worked.",
        "steps": [
            ("Build the first four partial sums",
             "`S₁ = a₁`, then add one term at a time. Four numbers cost four additions "
             "and show at once whether the sums are climbing, falling, settling or "
             "oscillating."),
            ("If you were handed Sₙ, subtract to get the terms",
             "`aₙ = Sₙ - Sₙ₋₁` for `n ≥ 2`. Then compute `a₁ = S₁` on its own and check "
             "whether your formula also produces it. Sometimes it does; when it does "
             "not, say so, because the first term really is exceptional."),
            ("Look for a bₖ with aₖ = bₖ - bₖ₊₁",
             "Split the term, then combine the split back over a common denominator. "
             "If it does not return the term you started with, the split is wrong. A "
             "denominator that factors into consecutive things is the case that usually "
             "yields; nothing else is guaranteed to."),
            ("Cancel, then test the answer on n = 1 and n = 2",
             "The result is `b₁ - bₙ₊₁`, and the commonest error puts `bₙ` there "
             "instead. Evaluating your closed form at `n = 1` and `n = 2` against the "
             "sums added by hand catches an index error at either end."),
        ],
        "worked": {
            "title": "The sum of 1/(k(k+1)) from k=1 to n, added and then telescoped",
            "intro": [
                "The terms are `1/2, 1/6, 1/12, 1/20, …` and nothing about them suggests "
                "a formula. Splitting each one into a difference is what turns the sum "
                "into two numbers."
            ],
            "lines": [
                "check the split first",
                "  1/k - 1/(k + 1)  =  ((k + 1) - k)/(k(k + 1))  =  1/(k(k + 1))    ✓",
                "",
                "so with bₖ = 1/k,   aₖ = bₖ - bₖ₊₁",
                "",
                "   n                    n",
                "   Σ  1/(k(k+1))   =    Σ  (bₖ - bₖ₊₁)   =   b₁ - bₙ₊₁",
                "  k=1                  k=1",
                "",
                "                    =   1 - 1/(n + 1)   =   n/(n + 1)",
                "",
                "check by adding the terms",
                "n=1   1/2                                  n/(n+1) = 1/2     ✓",
                "n=2   1/2 + 1/6  =  3/6 + 1/6  =  2/3      n/(n+1) = 2/3     ✓",
                "n=3   2/3 + 1/12 =  8/12 + 1/12 =  3/4     n/(n+1) = 3/4     ✓",
                "n=4   3/4 + 1/20 = 15/20 + 1/20 =  4/5     n/(n+1) = 4/5     ✓",
                "",
                "the surviving ends:  b₁ = 1     and     bₙ₊₁ = 1/(n + 1)",
            ],
            "after": [
                "The four checks establish the formula at `n = 1, 2, 3, 4` and nothing "
                "beyond that. What makes it true for every `n` is the telescoping "
                "argument: written out, the sum is "
                "`(1/1 - 1/2) + (1/2 - 1/3) + … + (1/n - 1/(n + 1))`, every interior "
                "fraction appears once with each sign, and `1` and `1/(n + 1)` are left.",
                "The last survivor is `1/(n + 1)` and not `1/n`. There are `n` brackets, "
                "the last is `1/n - 1/(n + 1)`, and it is the second half of that "
                "bracket that has no partner. Writing `1 - 1/n` gives `(n - 1)/n`, wrong "
                "by `1/(n(n + 1))` and entirely plausible on the page.",
                "The partial sums `1/2, 2/3, 3/4, 4/5, …` climb and every one is below "
                "`1`. Whether they add up to `1` is the next lesson's question, and "
                "having `n/(n + 1)` in closed form is what makes it answerable.",
            ],
        },
        "quiz_title": "Sums, terms and cancellations",
        "quiz": [
            {"q": "A series has partial sums `Sₙ = 3n² + n`. What is `a₄`?",
             "a": ["`22`", "`28`", "`30`", "`52`"],
             "c": 0,
             "why": "`a₄ = S₄ - S₃ = 52 - 30 = 22`. `52` is `S₄`, the sum of four terms "
                    "reported as the fourth term. `30` is `S₃`. `28` is `S₅ - S₄`, the "
                    "same subtraction one place too far along."},
            {"q": "What is `Σ (1/k - 1/(k + 1))` for `k` from `1` to `20`?",
             "a": ["`0`", "`19/20`", "`20/21`", "`21/20`"],
             "c": 2,
             "why": "The sum is `b₁ - b₂₁` with `bₖ = 1/k`, which is `1 - 1/21 = 20/21`. "
                    "`19/20` stops one bracket early: the last bracket is `1/20 - 1/21`, "
                    "so `1/21` survives. `0` assumes everything cancels, which the two "
                    "ends do not. `21/20` is `1 + 1/20`: the wrong survivor, and added "
                    "rather than subtracted."},
            {"q": "A series has partial sums `Sₙ = n² + 5`. Which statement is correct?",
             "a": ["`aₙ = 2n - 1` for every `n ≥ 1`",
                   "`aₙ = 2n - 1` for `n ≥ 2`, and `a₁ = 6`",
                   "`aₙ = 2n - 1` for `n ≥ 2`, and `a₁ = 5`",
                   "`aₙ = 2n + 4` for every `n ≥ 1`"],
             "c": 1,
             "why": "`a₁ = S₁ = 6`, whatever the later pattern suggests. For `n ≥ 2`, "
                    "`aₙ = (n² + 5) - ((n - 1)² + 5) = 2n - 1`, which at `n = 1` would "
                    "give `1`: the first choice extends that formula back to the one "
                    "case it was not derived for. The third reports `a₁ = 5`, which is "
                    "`n² + 5` at `n = 0` rather than at `n = 1`. `2n + 4` subtracts "
                    "`(n - 1)²` but forgets the `+ 5` inside "
                    "`Sₙ₋₁`; at `n = 2` it gives `8`, while `S₂ - S₁ = 9 - 6 = 3`."},
        ],
        "mistakes": [
            ("Extending the formula for aₙ back to n = 1 without checking S₁",
             "`aₙ = Sₙ - Sₙ₋₁` is derived for `n ≥ 2`, and whether it survives at "
             "`n = 1` depends on the particular `Sₙ`. For `Sₙ = n²` it does; for "
             "`Sₙ = n² + 5` it does not, and the sequence starts `6, 3, 5, 7, …` . "
             "Computing `S₁` and comparing costs one substitution."),
            ("Leaving bₙ rather than bₙ₊₁ at the far end",
             "With `n` brackets the last one is `bₙ - bₙ₊₁`, so the unpartnered term is "
             "`bₙ₊₁`. For `Σ 1/(k(k+1))` that is the difference between `n/(n + 1)` and "
             "`(n - 1)/n`, two formulas that agree to within `1/(n(n + 1))` and are "
             "impossible to tell apart by eye. Testing at `n = 1` separates them "
             "immediately: the sum is `1/2` and the wrong form gives `0`."),
            ("Assuming a sum telescopes because its terms are fractions",
             "`1/(k(k + 1))` splits because `1/k - 1/(k + 1)` recombines to it. `1/k²` "
             "does not split into consecutive differences of anything elementary, and "
             "the partial sums of `Σ 1/k²` have no closed form at this level. The test "
             "is mechanical: write the proposed `bₖ - bₖ₊₁` over a common denominator "
             "and see whether `aₖ` comes back."),
        ],
        "standard": ("Finish when you can go from Sₙ to aₙ and back without losing the first term.",
                     "You should be able to build four partial sums of any sequence, "
                     "recover `aₙ` from a given `Sₙ` and check `a₁` against `S₁` "
                     "separately, and cancel a telescoping sum to two surviving values "
                     "with the right index on each. The `Σ 1/(k(k+1))` derivation should "
                     "follow from the split alone."),
        "note": "The partial sums of `Σ 1/(k(k+1))` are `1/2, 2/3, 3/4, 4/5, …` and "
                "every one is below `1`. Those of the geometric series with `a₁ = 4` and "
                "`r = 1/2` are `4, 6, 7, 15/2, …` and every one is below `8`. Both have "
                "a formula for `Sₙ` with `n` still in it, and lesson 6 asks what happens "
                "to that formula as `n` grows without bound &mdash; a question about the "
                "sequence `Sₙ`, not about carrying out infinitely many additions.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "infinite-geometric-series",
        "title": "Infinite Geometric Series",
        "module": "Infinite series",
        "one_line": "When adding forever gives a finite answer, and when it does not.",
        "summary": (
            "The sum of an infinite series is a definition, not a longer addition: it is "
            "the number the partial sums approach, and a series with no such number has "
            "no sum. For a geometric series the whole question reduces to the size of "
            "`rⁿ`, which settles it completely and in one line."
        ),
        "key": [
            "S∞      the number S₁, S₂, S₃, … approaches, if there is one",
            "Sₙ = a₁/(1 - r) - [a₁/(1 - r)]rⁿ      the only n sits on the r",
            "|r| < 1     rⁿ is driven to 0, so S∞ = a₁/(1 - r)",
            "|r| ≥ 1     no sum: the partial sums never settle on a number",
        ],
        "key_label": "What S∞ means, and the one condition on it",
        "concepts_intro": (
            "The formula was already stated in lesson 4. What was not stated is what the "
            "word \"sum\" means once the list of terms has no end."
        ),
        "concepts": [
            ("The sum of an infinite series is defined, not performed",
             "Nobody adds infinitely many numbers, and no definition asks them to. `S∞` "
             "is the number the sequence `S₁, S₂, S₃, …` approaches; if that sequence "
             "approaches nothing, the series has no sum and the expression naming it "
             "names nothing. Almost everything that sounds paradoxical here comes from "
             "reading the `+ …` as an instruction to be carried out."),
            ("`|r| < 1` is a statement about `rⁿ` and nothing else",
             "Write `Sₙ = a₁/(1 - r) - [a₁/(1 - r)]rⁿ`. The first piece does not depend "
             "on `n` at all, and the second is that same constant times `rⁿ`. So the "
             "entire question is whether `rⁿ` is driven to `0`, and for `|r| &lt; 1` it "
             "is, at a rate you can compute."),
            ("Approaching is a quantitative claim",
             "For `4 + 2 + 1 + 1/2 + …` the gap is exact: `8 - Sₙ = 8(1/2)ⁿ`. Getting "
             "within `1/1000` of `8` takes `13` terms and no fewer, since "
             "`8 - S₁₂ = 1/512` and `8 - S₁₃ = 1/1024`. \"Approaches `8`\" means every "
             "distance you name has a term count attached."),
        ],
        "read_title": "Partial sums, limits, and the geometric case settled",
        "read_intro": "What an infinite sum is defined to be, why `|r| &lt; 1` is the whole condition, and the three ways it fails on the other side.",
        "body": [
            ("p", "Lesson 5 made `S₁, S₂, S₃, …` a sequence in its own right. This "
                  "lesson asks one question about that sequence, and the answer to it is "
                  "what the phrase \"the sum of an infinite series\" is defined to mean."),
            ("def", ("Convergent and divergent series",
                     "Given `a₁ + a₂ + a₃ + …` , form the partial sums `Sₙ`. If there is "
                     "a number `S` such that the partial sums can be brought within any "
                     "distance you name of `S` by taking `n` large enough, and stay "
                     "within it for every larger `n`, the series <strong>converges</strong> "
                     "and `S` is its <strong>sum</strong>, written `S∞`. Otherwise the "
                     "series <strong>diverges</strong> and has no sum.",
                     "The definition is about a sequence of numbers, each of which is an "
                     "ordinary finite sum. At no point does anything infinite get "
                     "added.")),
            ("p", "The sum of a convergent series is also written `Σ aₖ` with `k` "
                  "running from `1` to `∞`. Writing the symbol does not bring the number "
                  "into existence: for a divergent series it is notation with nothing "
                  "behind it. Lesson 4's `2 + 6 + 18 + …` is the case in point &mdash; a "
                  "formula that returns `-1`, and a series with no sum."),
            ("math", [
                "Sₙ  =  a₁(1 - rⁿ)/(1 - r)                        r ≠ 1",
                "",
                "    =  a₁/(1 - r)  -  [a₁/(1 - r)]·rⁿ            split the numerator",
                "       constant           constant · rⁿ",
                "",
                "how fast does rⁿ shrink when |r| < 1?",
                "",
                "   r = 1/2      (1/2)¹⁰  =  1/1024",
                "                (1/2)²⁰  =  1/1048576",
                "",
                "   r = 9/10     (9/10)¹⁰⁰  is smaller than 1/37000",
                "",
                "so Sₙ closes in on a₁/(1 - r), and the gap is that constant times rⁿ",
            ]),
            ("thm", ("The geometric series, settled",
                     "Let `a₁ ≠ 0`. The series `a₁ + a₁r + a₁r² + …` converges if and "
                     "only if `|r| &lt; 1`, and in that case `S∞ = a₁/(1 - r)`.",
                     "`a₁ ≠ 0` is not an extra condition. Lesson 4's definition already "
                     "excludes `a₁ = 0` and `r = 0`, because with either of them a "
                     "ratio of consecutive terms is `0/0` and there is no `r` to "
                     "compare with `1`. So the theorem decides every geometric series "
                     "this course admits.")),
            ("proof", [
                "Take `r ≠ 1`, so that `Sₙ = a₁/(1 - r) - [a₁/(1 - r)]rⁿ`. Only `rⁿ` "
                "depends on `n`.",
                "Suppose `0 &lt; |r| &lt; 1`, and write `|r| = 1/(1 + h)` with "
                "`h &gt; 0`. Multiplying out `(1 + h)ⁿ` gives `1 + nh` together with "
                "further terms, all positive, so `(1 + h)ⁿ ≥ 1 + nh` and "
                "`|r|ⁿ ≤ 1/(1 + nh)`. Name any distance `d &gt; 0`: every `n` beyond "
                "`(1/d - 1)/h` puts `|r|ⁿ` below `d`, and it stays below for every "
                "larger `n`. So `rⁿ` is driven to `0`, the second piece of `Sₙ` with it, "
                "and the partial sums converge to `a₁/(1 - r)`. There is no separate "
                "case `r = 0` to treat: the definition excludes it, so `|r| &lt; 1` and "
                "`0 &lt; |r| &lt; 1` describe the same series here.",
                "Suppose instead `|r| &gt; 1`. Then `|aₙ| = |a₁||r|ⁿ⁻¹` grows without "
                "bound, and by lesson 5 the gap between consecutive partial sums is "
                "`aₙ`. Partial sums moving further and further apart cannot be settling "
                "on a number. For `r = 1`, `Sₙ = na₁`, which runs away; for `r = -1`, "
                "`Sₙ` is `a₁, 0, a₁, 0, …` , visiting two values for ever and "
                "approaching neither. Those three exhaust `|r| ≥ 1`.",
            ]),
            ("h3", "How close, after how many terms"),
            ("math", [
                "4 + 2 + 1 + 1/2 + …          a₁ = 4,  r = 1/2,  S∞ = 4/(1 - 1/2) = 8",
                "",
                "Sₙ = 8(1 - (1/2)ⁿ)     so     8 - Sₙ = 8(1/2)ⁿ        exactly",
                "",
                "n =  4     S₄  = 15/2        8 - S₄  = 1/2",
                "n = 10     S₁₀ = 1023/128    8 - S₁₀ = 1/128",
                "n = 12     S₁₂ = 4095/512    8 - S₁₂ = 1/512      not yet below 1/1000",
                "n = 13     S₁₃ = 8191/1024   8 - S₁₃ = 1/1024     below 1/1000",
                "",
                "13 terms for 1/1000, and a term count for every distance you name",
            ]),
            ("p", "The gap `8(1/2)ⁿ` is positive for every `n`, so no partial sum ever "
                  "equals `8` and none exceeds it. `S∞ = 8` holds anyway, because "
                  "\"sum\" was defined as the number approached and not a number "
                  "reached. This is where `0.999… = 1` stops being surprising: that no "
                  "truncation of it equals `1` is a fact about truncations."),
            ("example", ("One series, three wrong answers",
                         "`1 - 1 + 1 - 1 + …` is geometric with `a₁ = 1` and `r = -1`, "
                         "so `|r| = 1` and it has no sum; its partial sums are "
                         "`1, 0, 1, 0, …` . Bracketing it as `(1 - 1) + (1 - 1) + …` "
                         "suggests `0`. Bracketing it as `1 - (1 - 1) - (1 - 1) - …` "
                         "suggests `1`. The formula `a₁/(1 - r)` returns `1/2`. Three "
                         "manipulations, three answers, and none of the three is "
                         "licensed: brackets may be moved around a finite sum, and this "
                         "is not one.")),
            ("p", "If a series converges then `aₙ = Sₙ - Sₙ₋₁` approaches `0`, since "
                  "both partial sums approach the same number. The converse is false. In "
                  "the harmonic series `1 + 1/2 + 1/3 + 1/4 + …` the terms shrink to "
                  "`0`; but group the finite partial sum `S₁₆` as "
                  "`1 + 1/2 + (1/3 + 1/4) + (1/5 + … + 1/8) + (1/9 + … + 1/16)` and each "
                  "bracket exceeds `1/2`, so `S₁₆ &gt; 3`, and every doubling of `n` adds "
                  "more than another `1/2`. The partial sums pass every bound. Each step "
                  "there regroups one finite sum, which is what the previous example was "
                  "not entitled to do."),
            ("p", "For a geometric series the question is now closed: find `r`, "
                  "compare `|r|` with `1`, and either write `a₁/(1 - r)` or say there is "
                  "no sum. The general question &mdash; hand me a series, does it "
                  "converge &mdash; has no one-line answer of that kind, and it is the "
                  "business of calculus."),
        ],
        "lab": ("sequence", {
            "mode": "infinite",
            "panel_title": "How close, after how many terms",
            "panel_intro": "Set `a₁` and `r`, and choose a distance. The lab prints every "
                           "partial sum twice &mdash; added, and by `a₁(1 - rⁿ)/(1 - r)` "
                           "&mdash; with the exact gap to the limit beside them, and says "
                           "how many terms it takes to come within the distance you chose. "
                           "Set `r = 3/2` or `r = -1` and it refuses to name a sum at all.",
        }),
        "steps_title": "Deciding an infinite geometric series",
        "steps_intro": "The first step is a test, and when it fails, \"there is no sum\" is the complete answer rather than a failure to finish.",
        "steps": [
            ("Confirm it is geometric and find r exactly",
             "Divide consecutive terms at least twice and check the quotients agree. "
             "Write `r` as a fraction: `(2/3)ⁿ` is exact and `(0.667)ⁿ` is not, and the "
             "difference compounds with every power."),
            ("Compare |r| with 1 before writing any formula",
             "If `|r| ≥ 1` there is no sum and `a₁/(1 - r)` must not be written down "
             "at all: it returns a number regardless, and that number is not the sum of "
             "anything. Only `|r| &lt; 1` licenses the next step."),
            ("Identify a₁ as the first term of the series you were given",
             "If the series starts at `k = 0`, or the first few terms were peeled off "
             "and handled separately, `a₁` is the first term of what remains. The "
             "formula sums from its own first term onward and knows nothing about what "
             "came before it."),
            ("Compute a₁/(1 - r) and check it against two partial sums",
             "With positive terms the sum must exceed every partial sum. With `r` "
             "negative the partial sums alternate around it, so the sum lies between "
             "`S₁` and `S₂`. Either check catches a sign lost in `1 - r`."),
        ],
        "worked": {
            "title": "1/2 - 1/4 + 1/8 - 1/16 + … , and the gap at every step",
            "intro": [
                "A negative ratio, so the partial sums come at the answer from both "
                "sides. The point of the example is the third column: the exact distance "
                "from each partial sum to the sum."
            ],
            "lines": [
                "ratios     (-1/4)/(1/2) = -1/2      (1/8)/(-1/4) = -1/2      geometric",
                "           a₁ = 1/2,   r = -1/2,   |r| = 1/2 < 1   so there is a sum",
                "",
                "S∞  =  a₁/(1 - r)  =  (1/2)/(1 + 1/2)  =  (1/2)/(3/2)  =  1/3",
                "",
                "partial sums, added one term at a time        the gap 1/3 - Sₙ",
                "S₁ = 1/2                                          -1/6",
                "S₂ = 1/2  - 1/4  =  1/4                            1/12",
                "S₃ = 1/4  + 1/8  =  3/8                           -1/24",
                "S₄ = 3/8  - 1/16 =  5/16                           1/48",
                "S₅ = 5/16 + 1/32 = 11/32                          -1/96",
                "S₆ = 11/32 - 1/64 = 21/64                          1/192",
                "",
                "the same S₆ by the closed form",
                "S₆ = (1/2)(1 - (-1/2)⁶)/(3/2) = (1/2)(63/64)(2/3) = 21/64        ✓",
                "",
                "the gap in closed form:   1/3 - Sₙ = (1/3)(-1/2)ⁿ",
                "                          halving in size, changing sign each step",
            ],
            "after": [
                "The gap column is the lesson. It is never `0`, so no partial sum "
                "equals `1/3`; its size halves at every step, so naming any distance "
                "names a term beyond which every partial sum is closer than that. `1/3` "
                "is the sum of this series in that sense and in no other.",
                "Adding six terms by hand and computing `S₆` from the closed form agree "
                "at `21/64`, which checks this one instance &mdash; `a₁ = 1/2`, "
                "`r = -1/2`, `n = 6`. Lesson 4's cancellation is what makes "
                "`Sₙ = a₁(1 - rⁿ)/(1 - r)` true in general, and `(-1/2)ⁿ` being driven "
                "to `0` is what makes `S∞ = 1/3` true.",
                "Because `r` is negative, `S∞` is not larger than every partial sum: "
                "`S₁ = 1/2` overshoots, `S₂ = 1/4` undershoots, and `1/3` stays caught "
                "between consecutive partial sums for ever. Step 4's check has to be "
                "read in the form matching the sign of `r`.",
            ],
        },
        "quiz_title": "Convergence, and what the number means",
        "quiz": [
            {"q": "What is the sum of `10 - 4 + 8/5 - 16/25 + …` ?",
             "a": ["`-50/7`", "`50/7`", "`50/3`", "It has no sum"],
             "c": 1,
             "why": "`r = -4/10 = -2/5` and `|r| = 2/5 &lt; 1`, so "
                    "`S∞ = 10/(1 - (-2/5)) = 10/(7/5) = 50/7`. `50/3` loses the sign of "
                    "`r` and computes `10/(1 - 2/5)`. `-50/7` divides by `r - 1` rather "
                    "than `1 - r`. There is a sum: a negative `r` makes the terms "
                    "alternate, which is not what the condition tests."},
            {"q": "The partial sums of `4 + 2 + 1 + 1/2 + …` are `4, 6, 7, 15/2, …` and its sum is `8`. Which statement is correct?",
             "a": ["Some partial sum equals `8`, and every later one equals `8` as well",
                   "No partial sum equals `8`; `8` is the number they can be brought arbitrarily close to",
                   "The partial sums rise past `8` and then come back down to it",
                   "`8` is an approximation, accurate to more places the more terms you take"],
             "c": 1,
             "why": "`8 - Sₙ = 8(1/2)ⁿ` is positive for every `n`: no partial sum "
                    "reaches `8` and none passes it. Nor is `8` an approximation. It is "
                    "exact, and it is the sum by the definition of the word."},
            {"q": "Which of these series has a sum?",
             "a": ["`1 + 1/2 + 1/3 + 1/4 + …`",
                   "`1 - 1 + 1 - 1 + …`",
                   "`3 + 18/5 + 108/25 + …`",
                   "`1/2 + 1/6 + 1/18 + 1/54 + …`"],
             "c": 3,
             "why": "Only the last is geometric with `|r| &lt; 1`: `r = 1/3`, so "
                    "`S∞ = (1/2)/(1 - 1/3) = 3/4`. The third has `r = 6/5`, above `1`. "
                    "The second has `r = -1` and partial sums `1, 0, 1, 0, …` for ever. "
                    "The first is not geometric; its terms shrink to `0`, which is "
                    "necessary and not sufficient, and its sums pass every bound."},
        ],
        "mistakes": [
            ("Concluding there is a sum because the terms are getting smaller",
             "Shrinking terms are necessary and nowhere near sufficient: "
             "`1 + 1/2 + 1/3 + …` shrinks and has no sum. The test is `|r| &lt; 1` for a "
             "series that is geometric to begin with, and \"the terms are getting "
             "smaller\" establishes neither half of it."),
            ("Reading S∞ as a value the running total eventually reaches",
             "For `4 + 2 + 1 + …` the gap to `8` is `8(1/2)ⁿ`, never `0`. Taking "
             "`S∞ = 8` to mean the running total is `8` after enough terms makes "
             "`0.999… = 1` look like a rounding claim. It is not one: the sum is the "
             "number approached, and on that definition it is exactly `8`."),
            ("Regrouping the terms of a divergent series",
             "`(1 - 1) + (1 - 1) + …` gives `0` and `1 - (1 - 1) - (1 - 1) - …` gives "
             "`1`, for the same series. Every derivation on this course regrouped a "
             "<em>finite</em> sum, which is licensed; carrying the habit past the end of "
             "a divergent series produces two answers, and the two answers are the proof "
             "that it was never allowed."),
        ],
        "standard": ("Finish when |r| < 1 is a question about rⁿ and S∞ is a question about a sequence.",
                     "You should be able to say what `S∞` means without using the word "
                     "\"add\", decide any geometric series in a line, compute how many "
                     "terms bring a partial sum within a stated distance of the limit, "
                     "and name what goes wrong in each of the three divergent cases "
                     "`|r| &gt; 1`, `r = 1` and `r = -1`."),
        "note": "Lesson 7 turns this into a machine for repeating decimals. `0.4272727…` "
                "is `0.4` plus a geometric series with `r = 1/100`, and the fraction it "
                "equals falls out of `a₁/(1 - r)`. It is the same formula with `|r|` far "
                "enough below `1` that convergence is never in doubt &mdash; which is "
                "the argument behind course 1's claim that a repeating decimal is always "
                "rational.",
    },
]
