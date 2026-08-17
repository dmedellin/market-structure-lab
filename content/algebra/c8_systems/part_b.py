"""Course 8, lessons 08-14 — determinants, inverses, linear programming, sequences and series."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "determinants-and-cramers-rule",
        "title": "Determinants and Cramer's Rule",
        "module": "Matrices",
        "one_line": "One number that decides whether a system has one solution.",
        "summary": (
            "The determinant of a square matrix is one number built from its entries, "
            "and for a system with as many equations as unknowns it decides whether "
            "there is exactly one solution. Cramer's rule then writes that solution as "
            "a ratio of determinants."
        ),
        "key": [
            "     | a  b |",
            "D  = | c  d |  =  ad - bc        four entries, one number",
            "D ≠ 0    exactly one solution     x = Dx/D,   y = Dy/D",
            "D = 0    none or infinitely many  and D cannot say which",
        ],
        "key_label": "The 2 by 2 determinant, and what it decides",
        "concepts_intro": (
            "A determinant is not a matrix and not a solution. It is one number, and "
            "what it reports is a yes-or-no fact about the system it came from."
        ),
        "concepts": [
            ("A matrix is an array, a determinant is a number",
             "The array `[ a  b ; c  d ]` &mdash; two rows, written on one line with "
             "a semicolon between them &mdash; is a matrix; the number `ad - bc` is its "
             "determinant, written `det A` or with vertical bars. Only square matrices "
             "have one. The notation is worth keeping straight: brackets hold an array, "
             "bars produce a number."),
            ("`D ≠ 0` is exactly the condition for a unique solution",
             "For `n` equations in `n` unknowns, the system has exactly one solution "
             "when `D ≠ 0` and does not when `D = 0`. Lesson 1 said a system does one "
             "of three things; the determinant separates the first from the other two "
             "without solving anything."),
            ("`D = 0` is where the determinant stops helping",
             "It rules out uniqueness and says nothing else. Inconsistent and dependent "
             "systems both have `D = 0`, so the only way to tell which one you are "
             "holding is to go back to elimination."),
        ],
        "read_title": "The determinant, and the rule built on it",
        "read_intro": "Two sizes computed by hand, then a formula for the solution and the condition it needs.",
        "body": [
            ("p", "Lesson 6 solved a system by carrying its augmented matrix to echelon "
                  "form, and by the end of the reduction you knew how many solutions "
                  "there were. The determinant answers that question in advance, from "
                  "the coefficients alone, in a single number."),
            ("def", ("Determinant of a 2 by 2 matrix",
                     "For `A = [ a  b ; c  d ]`, the <strong>determinant</strong> is "
                     "`det A = ad - bc`: the product down the main diagonal minus the "
                     "product up the other one. It is written `det A` or `|A|`, and the "
                     "bar notation is applied directly to the array of entries.")),
            ("math", [
                "| 3   5 |                                | 2   6 |",
                "| 1   4 |  =  (3)(4) - (5)(1) = 7         | 1   3 |  =  6 - 6 = 0",
                "",
                "the second matrix has a second row that is half the first,",
                "and a determinant of zero is what that always produces",
            ]),
            ("p", "For a 3 by 3 matrix the determinant is built from three 2 by 2 "
                  "determinants. Take each entry of the first row, cross out the row and "
                  "column it sits in, and multiply the entry by the determinant of what "
                  "is left. The three results are then combined with alternating signs: "
                  "plus, minus, plus."),
            ("math", [
                "| 2   1   3 |",
                "| 0   4  -1 |",
                "| 5   2   0 |",
                "",
                "     | 4  -1 |         | 0  -1 |         | 0   4 |",
                "= 2· | 2   0 |  -  1·  | 5   0 |  +  3·  | 5   2 |",
                "",
                "= 2(0 - (-2))  -  1(0 - (-5))  +  3(0 - 20)",
                "= 2(2) - 1(5) + 3(-20)",
                "= 4 - 5 - 60  =  -61",
            ]),
            ("p", "The alternating signs are not decoration and they are not optional. "
                  "The middle term is subtracted, and forgetting that is the single most "
                  "common way a 3 by 3 determinant comes out wrong. The expansion can be "
                  "taken along any row or column with the same sign pattern started in "
                  "the right place; the first row is the usual choice, and a row "
                  "containing a zero is the smart one, because that term vanishes."),
            ("p", "There is a diagonal shortcut for 3 by 3 determinants, sometimes "
                  "called Sarrus's rule. It gives the same answer, and it works for 3 by "
                  "3 matrices and for no other size. The expansion above is the method "
                  "that keeps working, so it is the one to learn."),
            ("thm", ("The determinant decides uniqueness",
                     "A system of `n` linear equations in `n` unknowns has exactly one "
                     "solution if and only if the determinant `D` of its coefficient "
                     "matrix is not zero. When `D = 0` the system has either no solution "
                     "or infinitely many.")),
            ("def", ("Cramer's rule",
                     "Write the system in standard form and let `D` be the determinant "
                     "of the coefficient matrix. Let `Dx` be the same determinant with "
                     "the `x` column replaced by the column of constants, and `Dy` the "
                     "same with the `y` column replaced. If `D ≠ 0` then "
                     "`x = Dx/D` and `y = Dy/D`.",
                     "The rule extends to any size: for each unknown, replace that "
                     "unknown's column by the constants and divide by `D`. A system in "
                     "three unknowns therefore needs four 3 by 3 determinants.")),
            ("example", ("Two systems with the same D",
                         "`x + y = 1` with `2x + 2y = 5` has `D = (1)(2) - (1)(2) = 0`. "
                         "So does `x + y = 1` with `2x + 2y = 2`. The first is "
                         "inconsistent &mdash; doubling the first equation gives "
                         "`2x + 2y = 2`, which contradicts `2x + 2y = 5` &mdash; and the "
                         "second is the same equation twice, with infinitely many "
                         "solutions. One determinant, two different outcomes: `D = 0` "
                         "genuinely cannot tell them apart.")),
            ("p", "Cramer's rule is a formula, not a strategy. For a 2 by 2 system it is "
                  "quick, and for coefficients that are letters rather than numbers it "
                  "is often the clearest thing available. For a 4 by 4 system it asks "
                  "for five 4 by 4 determinants, where one row reduction would have "
                  "finished the job. Lesson 6 remains the method; this lesson is the "
                  "criterion."),
        ],
        "lab": ("matrix", {
            "mode": "det",
            "panel_title": "Move one entry, watch D",
            "panel_intro": "Edit the coefficients and the lab recomputes `D`, `Dx` and "
                           "`Dy` in exact fractions. Make the second row a multiple of "
                           "the first and watch `D` drop to `0` while the unique "
                           "solution disappears.",
        }),
        "steps_title": "Using Cramer's rule",
        "steps_intro": "Four steps, and the third one is a stop sign rather than a step.",
        "steps": [
            ("Put the system in standard form",
             "Same variable order in every equation, constants alone on the right. A "
             "missing variable is a coefficient of `0` and must be written as one: in "
             "`3x = 12` paired with `2x + 5y = 4`, the first row is `3  0`, not `3`."),
            ("Compute D from the coefficient matrix",
             "The constants play no part here. `D` depends only on the left-hand "
             "sides, which is why it describes the system's shape rather than its "
             "answer."),
            ("If D = 0, stop",
             "There is no unique solution to find, and dividing by `D` is dividing by "
             "zero. Row reduce instead, and let the reduction tell you whether the "
             "system is inconsistent or dependent."),
            ("Replace one column at a time, then divide",
             "`Dx` replaces the `x` column with the constants and leaves everything "
             "else alone; `Dy` replaces the `y` column. Divide each by `D`, keep the "
             "fractions exact, and substitute back into both original equations."),
        ],
        "worked": {
            "title": "Cramer's rule on 2x + 3y = 7,  5x - y = 3",
            "intro": [
                "The system is already in standard form, so the coefficient matrix can "
                "be read straight off it. Note that `-y` contributes `-1`, not `1`."
            ],
            "lines": [
                "2x + 3y = 7            coefficient matrix   [ 2   3 ]",
                "5x -  y = 3                                 [ 5  -1 ]",
                "",
                "     | 2   3 |",
                "D  = | 5  -1 |  =  (2)(-1) - (3)(5)  =  -2 - 15  =  -17",
                "",
                "D ≠ 0, so there is exactly one solution.",
                "",
                "     | 7   3 |",
                "Dx = | 3  -1 |  =  (7)(-1) - (3)(3)  =  -7 - 9   =  -16",
                "                    x column replaced by the constants",
                "",
                "     | 2   7 |",
                "Dy = | 5   3 |  =  (2)(3)  - (7)(5)  =   6 - 35  =  -29",
                "                    y column replaced by the constants",
                "",
                "x = Dx/D = -16/-17 = 16/17          y = Dy/D = -29/-17 = 29/17",
                "",
                "check   2(16/17) + 3(29/17) = (32 + 87)/17 = 119/17 = 7    ✓",
                "        5(16/17) -  (29/17) = (80 - 29)/17 =  51/17 = 3    ✓",
            ],
            "after": [
                "Nothing in the question announced seventeenths, and they are not a "
                "sign of a slip. Whole-number coefficients produce fractional solutions "
                "as a matter of course, and the denominator is always `D`.",
                "Rounding is where this goes wrong. Taking `x ≈ 0.94` and `y ≈ 1.71` "
                "and substituting gives `2(0.94) + 3(1.71) = 7.01`, which is close "
                "enough to look like an arithmetic error somewhere and is in fact the "
                "rounding. Exact fractions check exactly; decimals do not.",
            ],
        },
        "quiz_title": "Determinants and the condition",
        "quiz": [
            {"q": "What is the determinant of `[ 3  -2 ; 4  5 ]` (rows separated by a semicolon)?",
             "a": ["`7`", "`23`", "`-23`", "`-7`"],
             "c": 1,
             "why": "`ad - bc = (3)(5) - (-2)(4) = 15 - (-8) = 23`. Getting `7` means "
                    "the minus sign on `-2` was dropped and `15 - 8` computed; `-23` is "
                    "`bc - ad`, the two products in the wrong order; `-7` is both slips "
                    "at once."},
            {"q": "A system of two equations in two unknowns has `D = 0`. What follows?",
             "a": ["It has infinitely many solutions",
                   "It has no solution",
                   "It has exactly one solution, and `x = 0`",
                   "It has either no solution or infinitely many, and `D` cannot say which"],
             "c": 3,
             "why": "`D = 0` rules out uniqueness and nothing more. `x + y = 1` with "
                    "`2x + 2y = 5` and `x + y = 1` with `2x + 2y = 2` both have `D = 0`, "
                    "and one is inconsistent while the other is dependent."},
            {"q": "In Cramer's rule, `Dy` is the determinant of the coefficient matrix with:",
             "a": ["the second row replaced by the constants",
                   "the second column replaced by the constants",
                   "both columns replaced by the constants",
                   "the first column replaced by the constants"],
             "c": 1,
             "why": "Each unknown owns a column, and its determinant replaces that "
                    "column. Replacing the row instead is the usual slip: in the "
                    "worked example it would give the determinant of `[ 2  3 ; 7  3 ]`, "
                    "which is `-15` and not `-29`."},
        ],
        "mistakes": [
            ("Reading coefficients off equations that are not in standard form",
             "`3y + 2x = 7` contributes the row `2  3`, not `3  2`, and a constant "
             "still sitting on the left has to be moved before anything is read. The "
             "determinant of the wrong array is a perfectly good number attached to a "
             "different system."),
            ("Adding all three terms of a 3 by 3 expansion",
             "The signs run plus, minus, plus. In the worked expansion above, adding "
             "the middle term instead of subtracting it gives `4 + 5 - 60 = -51` "
             "instead of `-61` &mdash; a wrong answer with no visible symptom."),
            ("Announcing infinitely many solutions because `D = 0`",
             "That conclusion needs the reduction, not the determinant. Half the "
             "systems with `D = 0` have no solution at all, and there is no way to tell "
             "from `D` which half you are in."),
        ],
        "standard": ("Finish when D = 0 sends you back to row reduction rather than to a conclusion.",
                     "You should be able to compute a 2 by 2 determinant instantly, a 3 "
                     "by 3 by expansion without a sign error, and to state what `D ≠ 0` "
                     "means for the system in one sentence. The test is a system with "
                     "`D = 0`: the right answer is \"not exactly one solution, and I "
                     "need to reduce it to say more\"."),
        "note": "`D ≠ 0` is about to appear under a second name. Lesson 9 shows that it "
                "is exactly the condition for the coefficient matrix to have an "
                "inverse, so three statements &mdash; the system has one solution, the "
                "matrix is invertible, the determinant is nonzero &mdash; turn out to "
                "be one statement in three costumes.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "inverse-matrices",
        "title": "Inverse Matrices",
        "module": "Matrices",
        "one_line": "The matrix that undoes another, and when there is not one.",
        "summary": (
            "The inverse of `A` is the matrix that multiplies with it to give the "
            "identity, and it turns `AX = B` into `X = A⁻¹B`. Unlike numbers, where "
            "only zero has no reciprocal, a square matrix can fail to have an inverse "
            "without being the zero matrix &mdash; and the determinant decides which "
            "matrices do."
        ),
        "key": [
            "A A⁻¹  =  A⁻¹ A  =  I           I  =  [ 1  0 ; 0  1 ]",
            "[ a  b ]⁻¹         1       [  d  -b ]",
            "[ c  d ]      = ------- ·  [ -c   a ]      swap a and d,",
            "                 ad - bc                   negate b and c",
        ],
        "key_label": "The identity, and the inverse of a 2 by 2",
        "concepts_intro": (
            "The inverse is defined by what it does, not by the formula that finds it. "
            "The formula is a convenience for one size of matrix; the definition is the "
            "thing that transfers."
        ),
        "concepts": [
            ("The inverse is defined by a product, not by a recipe",
             "`A⁻¹` is the matrix with `AA⁻¹ = A⁻¹A = I`. Both orders are written into "
             "the definition because matrix multiplication does not commute, as lesson "
             "7 established. For square matrices one product turns out to force the "
             "other, but that is a theorem and not something to assume."),
            ("A matrix can fail to have an inverse without being zero",
             "Among numbers only `0` lacks a reciprocal. Among matrices, every one with "
             "determinant `0` lacks an inverse, and `[ 2  3 ; 4  6 ]` has no zero entry "
             "anywhere. Such a matrix is called <strong>singular</strong>; the word for "
             "one that does have an inverse is <strong>nonsingular</strong>."),
            ("`X = A⁻¹B` is a formula for the solution, not the fastest route to it",
             "Finding `A⁻¹` costs a full row reduction, and then a multiplication. "
             "Solving one system directly costs the row reduction alone. The inverse "
             "earns its keep when the same `A` is used with several different `B`s."),
        ],
        "read_title": "The identity, the inverse, and the two ways to find one",
        "read_intro": "A definition, a formula that works for 2 by 2, and a method that works for any size.",
        "body": [
            ("p", "Lesson 7 gave matrix multiplication, and with it a way to write a "
                  "whole system as one equation. The system `4x + 7y = 1`, `2x + 6y = 8` "
                  "becomes `AX = B` with `A = [ 4  7 ; 2  6 ]`, `X = [ x ; y ]` and "
                  "`B = [ 1 ; 8 ]`. Written that way it looks like a single equation "
                  "asking to be divided by `A`."),
            ("p", "There is no division of matrices. What replaces it is multiplication "
                  "by an inverse, and the first job is to say what an inverse is."),
            ("def", ("Identity matrix",
                     "`Iₙ` is the `n` by `n` matrix with `1` down the main diagonal and "
                     "`0` everywhere else. For any matrix `A` of matching size, "
                     "`AI = IA = A`. It is the matrix that behaves the way `1` behaves "
                     "among numbers.")),
            ("def", ("Inverse matrix",
                     "For a square matrix `A`, an <strong>inverse</strong> is a matrix "
                     "`A⁻¹` of the same size with `AA⁻¹ = A⁻¹A = I`. A matrix has at "
                     "most one inverse. Non-square matrices are excluded outright: "
                     "`AA⁻¹` and `A⁻¹A` cannot both be defined unless `A` is square.")),
            ("thm", ("The 2 by 2 inverse",
                     "If `A = [ a  b ; c  d ]` and `ad - bc ≠ 0` then "
                     "`A⁻¹ = (1/(ad - bc))[ d  -b ; -c  a ]`. If `ad - bc = 0`, `A` has "
                     "no inverse. Note what moves: `a` and `d` change places, while `b` "
                     "and `c` stay where they are and change sign.")),
            ("proof", [
                "Multiply the two arrays before dividing by anything: "
                "`[ a  b ; c  d ][ d  -b ; -c  a ]` has top-left entry `ad - bc`, "
                "top-right `-ab + ba = 0`, bottom-left `cd - dc = 0` and bottom-right "
                "`-cb + da = ad - bc`.",
                "So the product is `(ad - bc)I`. If `ad - bc ≠ 0`, dividing every entry "
                "of the second array by `ad - bc` gives a product of exactly `I`, and "
                "multiplying in the other order gives `(ad - bc)I` as well. If "
                "`ad - bc = 0` the product is the zero matrix, which is never `I`, so "
                "no scaling of that array can help.",
                "Nor can any other matrix. Suppose some `B` had `AB = BA = I`. "
                "Multiplying `A[ d  -b ; -c  a ] = 0` on the left by `B` gives "
                "`(BA)[ d  -b ; -c  a ] = [ d  -b ; -c  a ] = 0`, so "
                "`a = b = c = d = 0` and `A` is the zero matrix &mdash; but then "
                "`AB = 0`, not `I`. So no `B` inverts `A` when `ad - bc = 0`.",
            ]),
            ("example", ("The inverse of [ 4  7 ; 2  6 ]",
                         "`ad - bc = 24 - 14 = 10`. Swapping the diagonal and negating "
                         "the other two entries gives `[ 6  -7 ; -2  4 ]`, and dividing "
                         "by `10` gives `A⁻¹ = [ 3/5  -7/10 ; -1/5  2/5 ]`. Checking one "
                         "entry: the top-left of `AA⁻¹` is "
                         "`4(3/5) + 7(-1/5) = 12/5 - 7/5 = 1`.")),
            ("h3", "Any size: augment with I and row reduce"),
            ("p", "There is a 3 by 3 inverse formula. It is long, it is easy to "
                  "misremember, and it is unnecessary, because the row reduction of "
                  "lesson 6 already does the work. Write `A` and the identity side by "
                  "side as `[ A | I ]`, reduce the left half to `I`, and the right half "
                  "becomes `A⁻¹`."),
            ("p", "The reason is that every row operation is itself a multiplication by "
                  "some matrix, and the operations that carry `A` to `I` are exactly the "
                  "operations that carry `I` to `A⁻¹`. Carrying them out on both halves "
                  "at once records the whole sequence. If the left half cannot be "
                  "reduced to `I` &mdash; a row of zeros appears &mdash; then `A` is "
                  "singular, and the attempt has proved it."),
            ("thm", ("Solving a system with an inverse",
                     "If `A` is invertible, `AX = B` has the unique solution "
                     "`X = A⁻¹B`. Multiplying both sides on the left by `A⁻¹` gives "
                     "`A⁻¹AX = A⁻¹B`, and `A⁻¹A = I`, so `IX = X = A⁻¹B`. The "
                     "multiplication must be on the left on both sides: `XA⁻¹` is a "
                     "different product and is usually not even defined.")),
            ("example", ("A singular matrix, and the two systems behind it",
                         "`A = [ 2  3 ; 4  6 ]` has `ad - bc = 12 - 12 = 0`, so there is "
                         "no `A⁻¹`. Reducing `[ A | I ]` produces a zero row on the "
                         "left, which is the same failure. And the systems agree: "
                         "`2x + 3y = 1` with `4x + 6y = 2` has infinitely many "
                         "solutions, while `2x + 3y = 1` with `4x + 6y = 5` has none. "
                         "No single matrix `A⁻¹` could deliver both answers.")),
            ("thm", ("The inverse of a product reverses the order",
                     "If `A` and `B` are invertible and the same size, "
                     "`(AB)⁻¹ = B⁻¹A⁻¹`. Check it: "
                     "`(AB)(B⁻¹A⁻¹) = A(BB⁻¹)A⁻¹ = AIA⁻¹ = AA⁻¹ = I`. The order "
                     "reverses for the same reason socks come off after shoes.")),
        ],
        "lab": ("matrix", {
            "mode": "inverse",
            "panel_title": "Invert, then check the product",
            "panel_intro": "Enter a matrix and the lab reduces `[ A | I ]` one row "
                           "operation at a time, then multiplies `A` by the result to "
                           "show `I`. Try a matrix whose second row is a multiple of "
                           "the first and watch the reduction stall.",
        }),
        "steps_title": "Inverting a 2 by 2 and using it",
        "steps_intro": "The determinant comes first, because it decides whether the rest happens.",
        "steps": [
            ("Compute ad - bc",
             "If it is `0`, stop: there is no inverse, and the system it came from "
             "does not have a unique solution either. Everything below assumes it is "
             "not zero."),
            ("Swap the diagonal, negate the other two",
             "`a` and `d` trade places. `b` and `c` stay where they are and change "
             "sign. Only one of those two things is a swap, and mixing them up is the "
             "commonest error in the formula."),
            ("Divide every entry by the determinant",
             "All four entries, not just the first. Keep exact fractions: `-7/10` is "
             "the entry, and `-0.7` will be wrong by the time it has been multiplied "
             "twice."),
            ("Multiply back, then solve",
             "`AA⁻¹` must come out as `[ 1  0 ; 0  1 ]` exactly. Then "
             "`X = A⁻¹B`, with `A⁻¹` written on the left of `B`."),
        ],
        "worked": {
            "title": "Inverting [ 4  7 ; 2  6 ] by row reduction",
            "intro": [
                "The formula already gave the answer for this matrix. Doing it again by "
                "reduction is the point: this is the method that still works at 3 by 3, "
                "where there is no formula worth carrying."
            ],
            "lines": [
                "[ 4  7 | 1  0 ]        A on the left, the identity on the right",
                "[ 2  6 | 0  1 ]",
                "",
                "R1 → R1/4",
                "[ 1  7/4 | 1/4   0 ]",
                "[ 2  6   | 0     1 ]",
                "",
                "R2 → R2 - 2R1          6 - 2(7/4) = 6 - 7/2 = 5/2",
                "[ 1  7/4 | 1/4    0 ]",
                "[ 0  5/2 | -1/2   1 ]",
                "",
                "R2 → (2/5)R2",
                "[ 1  7/4 | 1/4    0  ]",
                "[ 0  1   | -1/5  2/5 ]",
                "",
                "R1 → R1 - (7/4)R2      1/4 + 7/20 = 3/5,   -(7/4)(2/5) = -7/10",
                "[ 1  0 | 3/5   -7/10 ]",
                "[ 0  1 | -1/5   2/5  ]",
                "",
                "         [  3/5  -7/10 ]",
                "A⁻¹  =   [ -1/5   2/5  ]",
                "",
                "solving  4x + 7y = 1,  2x + 6y = 8:",
                "x = (3/5)(1) + (-7/10)(8) = 3/5 - 28/5 = -5",
                "y = (-1/5)(1) + (2/5)(8)  = -1/5 + 16/5 = 3",
                "check   4(-5) + 7(3) = -20 + 21 = 1     ✓",
                "        2(-5) + 6(3) = -10 + 18 = 8     ✓",
            ],
            "after": [
                "The two methods agree entry for entry, which is the only kind of "
                "agreement worth having. The reduction produced quarters at the first "
                "step and never left the fractions, and that is normal: a matrix of "
                "whole numbers has an inverse of fractions unless its determinant "
                "happens to be `1` or `-1`.",
                "One `B` was solved here, so the inverse was not the cheap route. Solve "
                "`AX = B` for five different right-hand sides and it is.",
            ],
        },
        "quiz_title": "Inverses",
        "quiz": [
            {"q": "What is the inverse of `[ 3  4 ; 1  2 ]` (rows separated by a semicolon)?",
             "a": ["`[ 2  -4 ; -1  3 ]`",
                   "`[ 1  -2 ; -1/2  3/2 ]`",
                   "`[ 3/2  -2 ; -1/2  1 ]`",
                   "`[ 1/3  1/4 ; 1  1/2 ]`"],
             "c": 1,
             "why": "`ad - bc = 6 - 4 = 2`. Swapping the diagonal and negating the other "
                    "pair gives `[ 2  -4 ; -1  3 ]`, and every entry is then divided by "
                    "`2`. The first choice skips that division; the third negates "
                    "correctly but never swapped `a` and `d`; the fourth inverts each "
                    "entry separately, which is not an operation on matrices."},
            {"q": "Which of these matrices has no inverse?",
             "a": ["`[ 1  2 ; 3  4 ]`", "`[ 0  1 ; 1  0 ]`",
                   "`[ 2  3 ; 4  6 ]`", "`[ 5  0 ; 0  5 ]`"],
             "c": 2,
             "why": "Its determinant is `12 - 12 = 0`; the others are `-2`, `-1` and "
                    "`25`. Nothing about the entries looks degenerate, which is the "
                    "point: singularity is a fact about the determinant, not about "
                    "whether zeros appear."},
            {"q": "`A` and `B` are invertible matrices of the same size. What is `(AB)⁻¹`?",
             "a": ["`A⁻¹B⁻¹`", "`B⁻¹A⁻¹`", "`A⁻¹ + B⁻¹`",
                   "There is no formula; multiply `AB` out and invert the result"],
             "c": 1,
             "why": "`(AB)(B⁻¹A⁻¹) = A(BB⁻¹)A⁻¹ = I`, and the middle cancellation only "
                    "happens in that order. `A⁻¹B⁻¹` is what you get by forgetting that "
                    "matrix multiplication does not commute; it is the inverse of `BA`."},
        ],
        "mistakes": [
            ("Writing `B/A` or `1/A`",
             "There is no matrix division and no reciprocal of a matrix. There is "
             "multiplication by `A⁻¹`, and it has a side: `A⁻¹B` and `BA⁻¹` are "
             "different products, and for a column `B` only the first is defined."),
            ("Negating the diagonal instead of the off-diagonal",
             "In the 2 by 2 formula, `a` and `d` swap places and keep their signs; `b` "
             "and `c` keep their places and lose theirs. Doing it the other way round "
             "gives a matrix whose product with `A` is not `I`, which is why the check "
             "in step 4 exists."),
            ("Forgetting to divide all four entries by the determinant",
             "`[ 6  -7 ; -2  4 ]` is not the inverse of `[ 4  7 ; 2  6 ]`; it is ten "
             "times the inverse. The product comes out as `10I` rather than `I`, and "
             "every solution is then ten times too large."),
        ],
        "standard": ("Finish when the determinant is the first thing you compute, not the last.",
                     "You should be able to invert a 2 by 2 from the formula, invert a "
                     "3 by 3 by reducing `[ A | I ]`, and say in one sentence why "
                     "`[ 2  3 ; 4  6 ]` has no inverse. The check `AA⁻¹ = I` should be "
                     "automatic; it costs four multiplications and catches every sign "
                     "error."),
        "note": "Three conditions have now collapsed into one. `det A ≠ 0`, `A` has an "
                "inverse, and `AX = B` has exactly one solution for every `B` are the "
                "same statement about the same matrix. Lesson 10 leaves exact equations "
                "behind for inequalities, where the answer is a region rather than a "
                "point &mdash; and where finding the corners of that region is a 2 by 2 "
                "system all over again.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "systems-of-inequalities-and-linear-programming",
        "title": "Systems of Inequalities and Linear Programming",
        "module": "Matrices",
        "one_line": "A feasible region, and where the optimum has to be.",
        "summary": (
            "A linear inequality in two variables is satisfied by a half-plane, and a "
            "system of them by the region where the half-planes overlap. Linear "
            "programming asks for the largest value of a linear expression on that "
            "region, and the answer always sits at a corner."
        ),
        "key": [
            "one inequality      a half-plane, boundary solid for ≤ and ≥",
            "several            the overlap: every constraint holds at once",
            "corners            solve the boundary lines in pairs, then test",
            "max and min of ax + by on a bounded region:  at a corner",
        ],
        "key_label": "From a region to a finite list of candidates",
        "concepts_intro": (
            "The whole subject rests on one theorem. Without it there would be "
            "infinitely many points to check and no method at all."
        ),
        "concepts": [
            ("One inequality, one half-plane",
             "The line `ax + by = c` splits the plane in two. On one side "
             "`ax + by &gt; c`, on the other `ax + by &lt; c`, and on the line itself "
             "they are equal. So a single test point decides the entire side, and the "
             "boundary belongs to the solution for `≤` and `≥` and not for `&lt;` and "
             "`&gt;`."),
            ("The feasible region is an intersection, not a union",
             "A point is feasible only if it satisfies <em>every</em> constraint. Two "
             "boundary lines crossing somewhere is not enough to make that crossing a "
             "corner of the region; it has to survive all the other constraints as "
             "well."),
            ("The corner point theorem is what makes this finite",
             "A linear objective on a region that is closed and bounded attains its "
             "largest and smallest values at corners. That is why the method is "
             "\"list the corners and evaluate\" rather than a search, and it is the "
             "only non-obvious statement in the lesson."),
        ],
        "read_title": "Feasible regions and the corner point theorem",
        "read_intro": "Shading by test point, finding corners by elimination, and the theorem that says corners are enough.",
        "body": [
            ("p", "Course 3 ended with a single linear inequality in two variables: draw "
                  "the boundary line, decide which side, shade it. Everything here is "
                  "that, done several times on one set of axes, and then asked a "
                  "question."),
            ("def", ("Solution of a linear inequality in two variables",
                     "The set of points `(x, y)` making the statement true. For a "
                     "linear inequality it is a <strong>half-plane</strong>: everything "
                     "on one side of the line `ax + by = c`, with the line included "
                     "when the inequality is `≤` or `≥` and excluded when it is "
                     "`&lt;` or `&gt;`.")),
            ("p", "One test point settles the shading. Pick any point not on the "
                  "boundary &mdash; the origin, unless the line passes through it "
                  "&mdash; and substitute. If the statement is true, shade that side; "
                  "if false, shade the other. This works because `ax + by - c` keeps "
                  "one sign throughout each side and only changes sign by passing "
                  "through the line."),
            ("math", [
                "x + y ≤ 8       boundary  x + y = 8      solid: ≤ includes it",
                "test (0, 0):    0 + 0 = 0 ≤ 8    true    shade the origin side",
                "",
                "2x + y ≤ 10     boundary  2x + y = 10    solid",
                "test (0, 0):    0 ≤ 10           true    shade the origin side",
                "",
                "2x - 3y ≥ 6     boundary  2x - 3y = 6    solid",
                "test (0, 0):    0 ≥ 6            false   shade the other side",
            ]),
            ("def", ("Feasible region",
                     "Given a system of linear inequalities, the "
                     "<strong>feasible region</strong> is the set of points satisfying "
                     "all of them at once: the intersection of the half-planes. It may "
                     "be empty, it may be a bounded polygon, and it may run off to "
                     "infinity.")),
            ("example", ("A region with four corners",
                         "`x ≥ 0`, `y ≥ 0`, `x + y ≤ 8`, `2x + y ≤ 10`. The first two "
                         "confine everything to the first quadrant; the last two cut it "
                         "with two lines. What survives is a four-sided region with "
                         "corners at `(0, 0)`, `(5, 0)`, `(2, 6)` and `(0, 8)`, and the "
                         "worked example below finds those corners rather than reading "
                         "them off a picture.")),
            ("h3", "Asking for the best point in the region"),
            ("def", ("Linear programming problem",
                     "A linear <strong>objective function</strong> `P = ax + by`, "
                     "together with a system of linear inequalities called the "
                     "<strong>constraints</strong>. The problem is to find the point of "
                     "the feasible region at which `P` is largest, or smallest. Such a "
                     "point is called <strong>optimal</strong>.")),
            ("thm", ("The corner point theorem",
                     "If the feasible region is not empty and is bounded, then a linear "
                     "objective function attains both a maximum and a minimum on it, "
                     "and each occurs at a corner. If the same optimal value occurs at "
                     "two corners, then every point of the edge joining them is optimal "
                     "as well.",
                     "If the region is unbounded, an optimum may fail to exist; when "
                     "one does exist, it is still at a corner.")),
            ("p", "The reason is worth seeing even though the proof is not given here. "
                  "The points where `ax + by` takes some fixed value `k` form a line, "
                  "and different values of `k` give parallel lines. Increasing `k` "
                  "slides that line across the plane in one direction. The largest `k` "
                  "for which the line still touches the region is the one where it is "
                  "just about to leave &mdash; and a straight line leaving a polygon "
                  "leaves through a corner, or along a whole edge if it happens to be "
                  "parallel to one."),
            ("p", "That is the entire method. Infinitely many feasible points, and the "
                  "theorem says four of them need checking. Nothing about it survives "
                  "if the objective is not linear: `P = xy` on the region above is "
                  "largest at `(2.5, 5)`, which is not a corner of anything."),
            ("example", ("An unbounded region has no maximum",
                         "Take `x ≥ 0`, `y ≥ 0`, `x + y ≥ 4`. The region is everything "
                         "in the first quadrant on or above the line `x + y = 4`, and "
                         "it runs off to infinity. `C = 2x + 3y` has a minimum of `8` "
                         "at the corner `(4, 0)` &mdash; the other corner `(0, 4)` "
                         "gives `12` &mdash; but no maximum at all, because `2x + 3y` "
                         "grows without bound as you travel out along the region.")),
            ("p", "Two practical cautions. A strict inequality removes its boundary "
                  "line from the region, so an optimum sitting on that line is "
                  "approached but never reached; applied problems are stated with `≤` "
                  "and `≥` for exactly this reason. And if the quantities are things "
                  "like whole machines or whole people, the corner may be fractional, "
                  "and rounding it is not guaranteed to give the best whole-number "
                  "answer &mdash; that is a different subject."),
        ],
        "lab": ("system", {
            "mode": "linprog",
            "panel_title": "Drag a constraint, watch the corner move",
            "panel_intro": "Change a constraint and the lab redraws the feasible "
                           "region, recomputes every corner, and evaluates the "
                           "objective at each. Watch which corner wins as you tilt the "
                           "objective from `5x + 4y` toward `3x + 4y`.",
        }),
        "steps_title": "Solving a linear programming problem",
        "steps_intro": "Four steps. The third is where the answers are lost.",
        "steps": [
            ("Graph every boundary line",
             "Replace each inequality sign by `=` and draw the line, solid for `≤` and "
             "`≥`, dashed for `&lt;` and `&gt;`. Do not skip `x ≥ 0` and `y ≥ 0`; they "
             "are constraints like any other and they contribute corners."),
            ("Shade with a test point",
             "One point per inequality, the origin where possible. The feasible region "
             "is what all the shadings have in common, and it is worth outlining once "
             "it is clear."),
            ("Find the corners, then check each one",
             "Every corner is the intersection of two boundary lines, so solve those "
             "two equations together &mdash; elimination, from lesson 3. Then test the "
             "point against every other constraint and discard it if it fails one."),
            ("Evaluate the objective at each surviving corner",
             "Tabulate the values and pick the largest or the smallest, as asked. There "
             "is no need to look anywhere else, and no interior point can beat them."),
        ],
        "worked": {
            "title": "Maximise P = 5x + 4y subject to x ≥ 0, y ≥ 0, x + y ≤ 8, 2x + y ≤ 10",
            "intro": [
                "Four constraints give four boundary lines, and four lines cross in six "
                "places. Two of those six crossings are not corners of the region, and "
                "both of them would give a larger `P` than the true answer."
            ],
            "lines": [
                "boundaries   x = 0,   y = 0,   x + y = 8,   2x + y = 10",
                "",
                "the six crossings, each tested against the other constraints",
                "  x = 0,        y = 0           (0, 0)    feasible",
                "  y = 0,        2x + y = 10     (5, 0)    x + y = 5  ≤ 8    ok",
                "  x + y = 8,    2x + y = 10     (2, 6)    both hold exactly",
                "  x = 0,        x + y = 8       (0, 8)    2x + y = 8 ≤ 10   ok",
                "  y = 0,        x + y = 8       (8, 0)    2x + y = 16 > 10  OUT",
                "  x = 0,        2x + y = 10     (0, 10)   x + y = 10 > 8    OUT",
                "",
                "the third crossing, by elimination",
                "   2x + y = 10",
                " -( x + y =  8)",
                "    x      =  2      then  2 + y = 8,  so  y = 6",
                "",
                "objective at the four corners",
                "  (0, 0)    P = 0",
                "  (5, 0)    P = 25",
                "  (2, 6)    P = 10 + 24 = 34      maximum",
                "  (0, 8)    P = 0 + 32  = 32",
                "",
                "at the two rejected crossings   P = 40 at (8, 0) and at (0, 10)",
            ],
            "after": [
                "The last line is why step 3 ends with a test rather than a corner. "
                "Both rejected crossings give `P = 40`, comfortably larger than the "
                "true maximum of `34`. An unchecked crossing does not add a harmless "
                "extra candidate to the list; it wins, and the answer is then a point "
                "at which one of the constraints is false.",
                "The maximum is `34`, attained at `x = 2`, `y = 6`. Report the point as "
                "well as the value: \"34\" alone does not say what to do.",
            ],
        },
        "quiz_title": "Regions and corners",
        "quiz": [
            {"q": "Which points satisfy `2x - 3y ≥ 6`?",
             "a": ["The line `2x - 3y = 6` and nothing else",
                   "The side of that line containing the origin, boundary included",
                   "The side of that line not containing the origin, boundary included",
                   "The side not containing the origin, boundary excluded"],
             "c": 2,
             "why": "Test `(0, 0)`: `2(0) - 3(0) = 0`, and `0 ≥ 6` is false, so the "
                    "origin is on the wrong side. The sign is `≥`, so the boundary "
                    "line is part of the solution and is drawn solid."},
            {"q": "On the region with corners `(0, 0)`, `(5, 0)`, `(2, 6)`, `(0, 8)`, where is `P = 3x + 4y` largest?",
             "a": ["At `(2, 6)`, where `P = 30`", "At `(0, 8)`, where `P = 32`",
                   "At `(5, 0)`, where `P = 15`",
                   "In the middle of the region, where all constraints have room"],
             "c": 1,
             "why": "The four values are `0`, `15`, `30` and `32`. Changing the "
                    "objective changed the winning corner &mdash; `5x + 4y` was largest "
                    "at `(2, 6)` &mdash; while the list of corners stayed exactly the "
                    "same. The corners come from the constraints alone."},
            {"q": "The region `x ≥ 0`, `y ≥ 0`, `x + y ≥ 4` is unbounded. What can be said about `C = 2x + 3y` on it?",
             "a": ["It has a maximum and a minimum, both at corners",
                   "It has a minimum of `8` at `(4, 0)` and no maximum",
                   "It has neither a maximum nor a minimum",
                   "It has a maximum of `12` at `(0, 4)`"],
             "c": 1,
             "why": "The corners are `(4, 0)` and `(0, 4)`, giving `8` and `12`. "
                    "Travelling out along the region makes `2x + 3y` as large as you "
                    "like, so no maximum exists; the minimum survives and, as the "
                    "theorem promises, sits at a corner."},
        ],
        "mistakes": [
            ("Treating every crossing of two boundary lines as a corner",
             "In the worked example `(8, 0)` is where two boundaries meet and it "
             "violates `2x + y ≤ 10`. It is not in the region, and it gives a bigger "
             "objective value than the real answer, so leaving it in produces a "
             "confident wrong answer rather than a visible error."),
            ("Losing the direction of the inequality while solving for y",
             "`-2x + y ≤ 6` rearranges to `y ≤ 2x + 6`, but `2x - y ≤ 6` rearranges to "
             "`y ≥ 2x - 6`: dividing by `-1` reverses the sign. The safer route is not "
             "to rearrange at all &mdash; draw the boundary and test a point."),
            ("Looking for the optimum inside the region",
             "The best point is never strictly inside a region for a linear objective, "
             "because moving in the direction that increases `ax + by` always keeps "
             "increasing it until a boundary stops you. Checking a few feasible points "
             "at random and taking the best is not the method."),
        ],
        "standard": ("Finish when finding a corner means solving a 2 by 2 system and then testing it.",
                     "Given four or five constraints you should be able to produce the "
                     "corner list without a graph, discard the crossings that fail a "
                     "constraint, and name the optimal point and its value. Saying "
                     "\"the maximum is 34\" without saying where is half an answer."),
        "note": "Everything expensive in this lesson was elimination: each corner is a "
                "2 by 2 system, solved exactly as in lesson 3. That is the course's "
                "first half in service of a question it could not have asked. Lesson 11 "
                "starts the second half, where the objects are ordered lists rather "
                "than solution sets.",
    },
    # ---------------------------------------------------------------- 11
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
                         "is what that formula does. Lesson 13 shows this is the "
                         "general shape of a geometric sequence.")),
            ("example", ("Two recursions worth knowing",
                         "Fibonacci: `F₁ = 1`, `F₂ = 1`, `Fₙ = Fₙ₋₁ + Fₙ₋₂`, giving "
                         "`1, 1, 2, 3, 5, 8, 13, 21, 34, 55, …` . It needs two initial "
                         "terms because the rule reaches back two. "
                         "Factorial: `0! = 1` and `n! = n·(n - 1)!`, giving "
                         "`1, 1, 2, 6, 24, 120, …` . Lesson 14 uses the second one "
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
                "be written down exactly. Lesson 12 takes the ones built by adding a "
                "fixed number, lesson 13 the ones built by multiplying by a fixed "
                "number &mdash; and the second of those has a surprise in it, which is "
                "that infinitely many terms can add up to a finite number.",
    },
    # ---------------------------------------------------------------- 12
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
                "lesson 13.",
    },
    # ---------------------------------------------------------------- 13
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
             "subtraction here is the reflex left over from lesson 12: `3, 6, 12, 24` "
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
             "of `r`. The same check as in lesson 12 applies: your formula must return "
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
                "geometric series with `|r| &lt; 1`, so every repeating decimal is a "
                "fraction. Course 1 asserted that when it sorted the real numbers into "
                "rational and irrational; this is the argument behind the assertion, "
                "and it needed an infinite sum to state.",
    },
    # ---------------------------------------------------------------- 14
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
                     "pair of brackets. The factorials are the ones from lesson 11, "
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
        "note": "This is the last lesson of the course and of the path, and it ends "
                "where counting begins: `C(n,k)` was defined here as a formula and used "
                "as a count, and the Combinatorics and Counting course on the Discrete "
                "Mathematics path takes it up as a subject in its own right. The "
                "algebra was the point, though. Every step of this course &mdash; "
                "elimination, row reduction, the determinant, the corner points, the "
                "two sequence families &mdash; was legal because some property of the "
                "real numbers said so, which is the thing course 1 opened with.",
    },
]
