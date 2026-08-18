"""Course 8, lessons 08-10 — determinants, inverses, and linear programming."""

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
                "first half in service of a question it could not have asked. This is "
                "the last lesson of the course; course 9 takes up objects that are "
                "ordered lists rather than solution sets.",
    },
]
