"""Course 6, lessons 01-07 — solving quadratics four ways, counting the solutions, and defining i."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "quadratic-equations-and-the-zero-product-property",
        "title": "Quadratic Equations and the Zero Product Property",
        "module": "Solving quadratics",
        "one_line": "Why a product being zero is the whole method.",
        "summary": (
            "A quadratic equation is one that can be written `ax² + bx + c = 0` with "
            "`a ≠ 0`. Every method in this course ends at the same place: a product "
            "equal to zero, where the factors can be taken one at a time. The property "
            "that licenses that step holds for zero and for no other number."
        ),
        "key": [
            "ab = 0    ⟺    a = 0  or  b = 0",
            "(x - 3)(x + 5) = 0    →    x = 3  or  x = -5",
            "(x - 3)(x + 5) = 9    →    nothing follows",
            "ax² + bx + c = 0,  a ≠ 0        the equation being solved",
        ],
        "key_label": "The property, and the number it needs",
        "concepts_intro": (
            "The manipulation in this lesson is one line long. Knowing when that line "
            "is legal is the lesson."
        ),
        "concepts": [
            ("A quadratic equation is a shape, not a look",
             "`3x² = 5x - 2` and `(x + 1)(x - 4) = 6` are both quadratic, because each "
             "can be rearranged into `ax² + bx + c = 0` with `a ≠ 0`. The rearranging is "
             "not cosmetic: every method in this course is stated for that form and "
             "guaranteed only for it."),
            ("Zero is the only number this works for",
             "`ab = 0` forces one of the two to be zero. `ab = 12` forces nothing at "
             "all: `3 · 4`, `2 · 6` and `24 · (1/2)` are all 12. What is special about "
             "zero is that a product cannot arrive there unless a factor is already "
             "there."),
            ("Solving still means finding every value that works",
             "Course 2 defined a solution as a value that makes the statement true, and "
             "nothing changes. A quadratic usually has two solutions, so an answer "
             "carrying one number is usually half an answer, and the check is the same "
             "as it always was: substitute, and see."),
        ],
        "read_title": "Products, and the one number that gives them away",
        "read_intro": "The definition, the property, its one-line proof, and the two places it gets misapplied.",
        "body": [
            ("def", ("Quadratic equation",
                     "A <strong>quadratic equation in `x`</strong> is one that can be "
                     "written `ax² + bx + c = 0`, where `a`, `b` and `c` are numbers and "
                     "`a ≠ 0`. That arrangement is called <strong>standard "
                     "form</strong>.",
                     "The condition `a ≠ 0` is what makes the equation quadratic rather "
                     "than linear. If `a` were `0` the `x²` term would disappear and "
                     "course 2 would already have solved what was left.")),
            ("p", "`b` or `c` may be zero, and often are. `x² - 9 = 0` has `b = 0`; "
                  "`x² + 3x = 0` has `c = 0`. Both are quadratic, and each of those two "
                  "shapes gets a method of its own later in the course."),
            ("thm", ("The zero product property",
                     "For real numbers `a` and `b`, `ab = 0` if and only if `a = 0` or "
                     "`b = 0`.",
                     "The \"or\" is inclusive: both may be zero, as in `0 · 0 = 0`. The "
                     "statement rules out only the case where neither is.")),
            ("proof", [
                "One direction is arithmetic. If `a = 0` then `ab = 0 · b = 0`, and the "
                "same for `b = 0`. So a product with a zero factor is zero.",
                "The other direction is the useful one. Suppose `ab = 0` and `a ≠ 0`. "
                "Because `a` is a non-zero real number it has a reciprocal `1/a`, so "
                "both sides may be multiplied by it: `(1/a)(ab) = (1/a) · 0`.",
                "The right-hand side is `0`. The left-hand side regroups, by "
                "associativity, as `((1/a) · a)b = 1 · b = b`. So `b = 0`. Assuming "
                "`a ≠ 0` forced `b = 0`, which is exactly the claim that `a = 0` or "
                "`b = 0`.",
            ]),
            ("p", "The proof leaned on one property of the real numbers that is easy to "
                  "take for granted: every non-zero number has a reciprocal. The rule can "
                  "fail in systems without that property. In arithmetic modulo 12 "
                  "&mdash; clock arithmetic &mdash; `3 · 4 = 12`, which is `0` on that "
                  "clock, and neither `3` nor `4` is zero there. So the zero product "
                  "property is a fact about the numbers you are using, not a fact about "
                  "algebra in general."),
            ("h3", "Why the zero has to be on one side"),
            ("p", "`(x - 3)(x + 5) = 9` is a perfectly good equation, and the property "
                  "says nothing whatever about it. Setting `x - 3 = 9` gives `x = 12`, "
                  "and substituting back gives `(12 - 3)(12 + 5) = 9 · 17 = 153`, not "
                  "`9`. That was not an arithmetic slip. It was an appeal to a theorem "
                  "whose hypothesis had not been met."),
            ("p", "The repair is always the same: expand, move everything to one side, "
                  "and produce a zero. `(x - 3)(x + 5) = 9` becomes `x² + 2x - 15 = 9`, "
                  "then `x² + 2x - 24 = 0`, and lesson 2 finishes it."),
            ("h3", "More than two factors"),
            ("p", "The property extends to any finite number of factors by being applied "
                  "repeatedly: `abc = 0` means `a = 0` or `bc = 0`, and the second case "
                  "splits again. So `x(x - 2)(x + 7) = 0` has the three solutions `0`, "
                  "`2` and `-7`, found one bracket at a time."),
            ("h3", "Dividing by something that might be zero"),
            ("p", "`x² = 5x` invites you to divide both sides by `x`, giving `x = 5`. "
                  "But `x = 0` also satisfies the original equation, since `0² = 5 · 0`. "
                  "Dividing by `x` quietly assumed `x ≠ 0`, and the solution that broke "
                  "the assumption was thrown away by the step that made it."),
            ("p", "Division by a variable is legal only when you know the variable is "
                  "not zero, and in an equation you are still solving you do not know "
                  "that &mdash; finding out is the point. Move everything to one side "
                  "instead: `x² - 5x = 0`, so `x(x - 5) = 0`, so `x = 0` or `x = 5`. "
                  "Nothing is lost, and the method is one line longer."),
            ("example", ("Two factors, two solutions",
                         "`(2x - 1)(x + 4) = 0`. The property gives `2x - 1 = 0` or "
                         "`x + 4 = 0`, which are two linear equations of the kind course "
                         "2 solved in a line each. The first gives `x = 1/2`, the second "
                         "`x = -4`.",
                         "Those are the only solutions. Any other value of `x` makes "
                         "both brackets non-zero, and a product of two non-zero real "
                         "numbers is not zero &mdash; which is the first direction of "
                         "the theorem, read as a guarantee that nothing has been "
                         "missed.")),
        ],
        "lab": ("quadratic", {
            "mode": "zero",
            "panel_title": "Factors in, solutions out",
            "panel_intro": "Set the two factors and the number on the right. With `0` "
                           "there, the lab splits the equation and solves each factor. "
                           "With anything else there it refuses, and shows what "
                           "substituting the false answer actually produces.",
        }),
        "steps_title": "Using the zero product property",
        "steps_intro": "Four steps, and the first two exist only to make the third legal.",
        "steps": [
            ("Get a zero on one side",
             "Expand any brackets, then move every term to the same side. Until the "
             "other side reads `0`, no factorisation you write down is of any use."),
            ("Factor the side that is not zero",
             "Course 4 supplies the techniques and lesson 2 applies them. What you need "
             "is a product of polynomials; a sum, however tidy, cannot be split by this "
             "property."),
            ("Set each factor equal to zero, separately",
             "One factor at a time, each giving its own small equation. A constant "
             "factor such as the `5` in `5(x - 2)(x + 3) = 0` yields nothing, because "
             "`5 = 0` is false."),
            ("Solve each small equation, then check every answer in the original",
             "Each factor is linear, so course 2 finishes it. Substitute back into the "
             "equation you were given, not the rearranged one &mdash; that is what "
             "catches an illegal rearrangement as well as an arithmetic slip."),
        ],
        "worked": {
            "title": "One equation done twice, once illegally",
            "intro": ["`(x - 3)(x + 5) = 9`. The left-hand side arrives already "
                      "factored, which is exactly what makes the wrong route "
                      "attractive."],
            "lines": [
                "WRONG",
                "    (x - 3)(x + 5) = 9",
                "     x - 3 = 9      or      x + 5 = 9",
                "     x = 12         or      x = 4",
                "",
                "    check x = 12:   (12 - 3)(12 + 5)  =  9 · 17  =  153,  not 9",
                "",
                "RIGHT",
                "    (x - 3)(x + 5) = 9",
                "     x² + 2x - 15 = 9              expand the left side",
                "     x² + 2x - 24 = 0              subtract 9 from both sides",
                "     (x + 6)(x - 4) = 0            factor (lesson 2)",
                "     x + 6 = 0      or      x - 4 = 0",
                "     x = -6         or      x = 4",
                "",
                "    check x = -6:   (-6 - 3)(-6 + 5)  =  (-9)(-1)  =  9",
                "    check x =  4:   ( 4 - 3)( 4 + 5)  =  (1)(9)    =  9",
            ],
            "after": [
                "The wrong route returned `x = 4`, which is a genuine solution, "
                "alongside `x = 12`, which is not. That coincidence is worth sitting "
                "with. A method that happens to produce a correct answer has not been "
                "validated by producing it, and here only the check separates the two "
                "numbers.",
                "Notice what the right route did with the factored form it was handed: "
                "it threw it away and expanded. That looks wasteful and is not, because "
                "the factorisation you need is the one whose product is zero, not the "
                "one you happened to be given.",
            ],
        },
        "quiz_title": "Products and zeros",
        "quiz": [
            {"q": "The solutions of `(x - 4)(x + 2) = 0` are:",
             "a": ["`x = 4` or `x = -2`", "`x = -4` or `x = 2`", "`x = 4` or `x = 2`",
                   "`x = -4` or `x = -2`"],
             "c": 0,
             "why": "Each bracket becomes its own equation: `x - 4 = 0` gives `x = 4`, "
                    "and `x + 2 = 0` gives `x = -2`. The signs come out reversed from "
                    "the ones printed inside the brackets, which is where the second "
                    "option comes from &mdash; it copies the numbers instead of solving "
                    "for them."},
            {"q": "From `(x - 1)(x - 6) = 14`, what may be concluded immediately?",
             "a": ["`x - 1 = 14` or `x - 6 = 14`",
                   "`x - 1 = 2` and `x - 6 = 7`, since `2 · 7 = 14`",
                   "Nothing yet &mdash; expand, subtract 14, then factor again",
                   "`x = 1` or `x = 6`"],
             "c": 2,
             "why": "The property needs a zero, and `14` is not one. The first option "
                    "splits anyway and gives `x = 15`, which substitutes to "
                    "`(14)(9) = 126`, not `14`. The second picks one factorisation of "
                    "`14` out of infinitely many, and it needs `x` to be `3` and `13` "
                    "at once. The fourth copies the numbers out of the brackets. "
                    "Expanding and subtracting gives `x² - 7x - 8 = 0`, which factors "
                    "as `(x - 8)(x + 1)`, so the actual solutions are `8` and `-1` "
                    "&mdash; neither of them visible in the original brackets."},
            {"q": "Which step is illegal when solving `x² = 5x`?",
             "a": ["Subtracting `5x` from both sides", "Dividing both sides by `x`",
                   "Factoring `x² - 5x` as `x(x - 5)`",
                   "Setting `x = 0` and `x - 5 = 0` separately"],
             "c": 1,
             "why": "Dividing by `x` assumes `x ≠ 0`, and `x = 0` is one of the two "
                    "solutions: `0² = 5 · 0` is true. The division deletes it without "
                    "any warning. The other three steps are all legal, and together "
                    "they give `x = 0` or `x = 5`."},
        ],
        "mistakes": [
            ("Splitting a product that is not equal to zero",
             "`(x - 3)(x + 5) = 9` does not give `x - 3 = 9`. The theorem assumes the "
             "product is `0`; with any other number on the right there is no conclusion "
             "to draw, because `9` has many factorisations and the equation does not say "
             "which one is in play."),
            ("Dividing both sides by a variable",
             "From `x² = 5x`, dividing by `x` gives `x = 5` and loses `x = 0`. You may "
             "divide by a number you know is not zero. You may not divide by an unknown "
             "whose value is the thing you are trying to find."),
            ("Reading solutions off the brackets without changing the sign",
             "`(x - 4)(x + 2) = 0` gives `x = 4` and `x = -2`, not `x = -4` and `x = 2`. "
             "Each bracket is a small equation to be solved, not a label to be copied "
             "with the sign flipped by reflex."),
        ],
        "standard": ("Finish when you refuse to split a product unless the other side is zero.",
                     "Given any equation with a factored side you should look at the "
                     "right-hand side before doing anything else, and rearrange whenever "
                     "it is not `0`. You should also be able to give the one-line "
                     "argument with the reciprocal, because that argument is what tells "
                     "you the property cannot be stretched to cover `ab = 12`."),
        "note": "Every method in this course reaches either a product equal to zero or a "
                "square equal to a number, and the second is the first in disguise: for "
                "`k ≥ 0`, `x² = k` is `(x - √k)(x + √k) = 0`. Lesson 2 reaches the "
                "product by factoring; lessons 3 to 5 reach the square instead, and this "
                "property is what finishes every one of them.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "solving-by-factoring",
        "title": "Solving by Factoring",
        "module": "Solving quadratics",
        "one_line": "The quickest method, when it applies.",
        "summary": (
            "With a zero on one side and a factorisation on the other, the zero product "
            "property finishes the job in a line. All the work is in the factoring, "
            "which is course 4's, and in the two things the finished answer can hide: a "
            "constant factor that contributes nothing, and a repeated factor that "
            "contributes one solution rather than two."
        ),
        "key": [
            "x² + 3x - 10 = 0          standard form first",
            "(x + 5)(x - 2) = 0        factor",
            "x + 5 = 0  or  x - 2 = 0  zero product property",
            "x = -5     or  x = 2      two solutions, both substituted back",
        ],
        "key_label": "The method, in four lines",
        "concepts_intro": (
            "Nothing here is new. This is course 4's factoring followed by lesson 1's "
            "property, plus one decision: how long to keep trying."
        ),
        "concepts": [
            ("Standard form comes first, every time",
             "`3x² = 5x - 2` has to become `3x² - 5x + 2 = 0` before anything is "
             "factored. Factoring one side of an equation whose other side is not zero "
             "achieves nothing at all, however neat the result looks."),
            ("A repeated factor gives one solution",
             "`(2x - 3)² = 0` produces the equation `2x - 3 = 0` twice, so it produces "
             "`x = 3/2` once. Calling that a <strong>double root</strong> is a counting "
             "convention that keeps later statements tidy; as a solution of the equation "
             "it is one number."),
            ("Factoring is a method, not the method",
             "It is the fastest route when the coefficients cooperate and useless when "
             "they do not. `x² - 4x + 1 = 0` has two perfectly ordinary solutions that "
             "no integer factorisation will ever produce. Lessons 4 and 5 exist for "
             "those."),
        ],
        "read_title": "From a factorisation to a solution set",
        "read_intro": "The procedure, the factors that contribute nothing, and what to do when the factoring will not come.",
        "body": [
            ("p", "Lesson 1 supplied the licence and course 4 supplied the technique. "
                  "Put together: write the equation as `(something)(something) = 0`, "
                  "then set each factor to zero."),
            ("math", [
                "x² + 3x = 10",
                "x² + 3x - 10 = 0            subtract 10 from both sides",
                "(x + 5)(x - 2) = 0          two numbers, product -10 and sum 3:  5, -2",
                "x + 5 = 0   or   x - 2 = 0",
                "x = -5      or   x = 2",
            ]),
            ("h3", "Take the common factor out, then ignore it"),
            ("p", "`2x² - 8x = 0` factors as `2x(x - 4) = 0`. Three factors are written "
                  "down &mdash; `2`, `x` and `x - 4` &mdash; but the first contributes "
                  "nothing, because `2 = 0` is a false statement with no solutions. The "
                  "answers are `x = 0` and `x = 4`."),
            ("p", "A constant factor never creates a solution and never destroys one. "
                  "That is worth knowing in both directions: multiplying an equation "
                  "through by `3` leaves its solution set alone, and so does dividing by "
                  "`3`. Only multiplying or dividing by something that could be zero is "
                  "dangerous, which is the warning from lesson 1."),
            ("h3", "Repeated factors"),
            ("p", "`4x² - 12x + 9 = 0` is `(2x - 3)² = 0`, so the only equation to solve "
                  "is `2x - 3 = 0` and the only solution is `x = 3/2`. Substituting: "
                  "`4(9/4) - 12(3/2) + 9 = 9 - 18 + 9 = 0`."),
            ("p", "It is standard to say this equation has a double root at `3/2`, or a "
                  "root of multiplicity 2. That is a statement about the factorisation, "
                  "not about the solution set &mdash; the equation has exactly one "
                  "solution. The convention earns its keep in lesson 6 and in course 4's "
                  "lesson 13, where counting roots with multiplicity is what makes the "
                  "statements come out clean."),
            ("thm", ("What a factorisation says about the solutions",
                     "Suppose `ax² + bx + c = a(x - r)(x - s)` for every value of `x`, "
                     "with `a ≠ 0`. Then the solutions of `ax² + bx + c = 0` are exactly "
                     "`r` and `s`.",
                     "Both directions are needed and both are short. Each of `r` and `s` "
                     "makes a bracket zero, so each is a solution. Any other value makes "
                     "both brackets non-zero, and `a` is non-zero, so the product is "
                     "non-zero and that value is not a solution. There is nothing else "
                     "to check and nothing else to find.")),
            ("h3", "When the leading coefficient is not 1"),
            ("p", "Course 4's AC method still applies unchanged. For `6x² + x - 12 = 0`, "
                  "take `ac = 6 · (-12) = -72` and look for two numbers with product "
                  "`-72` and sum `1`. They are `9` and `-8`."),
            ("math", [
                "6x² + x - 12 = 0",
                "6x² + 9x - 8x - 12 = 0            split the middle term",
                "3x(2x + 3) - 4(2x + 3) = 0        group in pairs",
                "(2x + 3)(3x - 4) = 0",
                "2x + 3 = 0   or   3x - 4 = 0",
                "x = -3/2     or   x = 4/3",
            ]),
            ("p", "Both answers are fractions and both are exact. `-3/2` is the "
                  "solution; `-1.5` is a decimal that happens to equal it, and `4/3` has "
                  "no decimal that equals it at all. Exact fractions are the standard on "
                  "this path for that reason."),
            ("h3", "When the factoring will not come"),
            ("p", "A complete search that fails is a result about integer factorisation "
                  "and nothing more. `x² - 4x + 1 = 0` has no pair of integers with "
                  "product `1` and sum `-4`, so it does not factor over the integers. It "
                  "still has two solutions, `2 + √3` and `2 - √3`, which lesson 4 "
                  "produces. \"It does not factor\" and \"it has no solutions\" are "
                  "different sentences, and only the first one has been established."),
            ("example", ("Running the method backwards",
                         "To build an equation whose solutions are `-5` and `2`, start "
                         "from `(x + 5)(x - 2) = 0` and expand: `x² + 3x - 10 = 0`. "
                         "Multiplying through by any non-zero constant gives another "
                         "equation with the same two solutions, so `2x² + 6x - 20 = 0` "
                         "works equally well.",
                         "There is therefore no such thing as <em>the</em> equation with "
                         "a given pair of solutions. Any two quadratics with the same "
                         "roots differ by a constant multiple, which is the same "
                         "observation as \"a constant factor contributes nothing\", read "
                         "the other way round.")),
        ],
        "lab": ("quadratic", {
            "mode": "factor",
            "panel_title": "Factor, split, check",
            "panel_intro": "Enter the coefficients. The lab puts the equation in "
                           "standard form, factors it over the integers when that is "
                           "possible, splits it, and substitutes both answers back. When "
                           "no integer factorisation exists it says so rather than "
                           "guessing.",
        }),
        "steps_title": "Solving a quadratic by factoring",
        "steps_intro": "Steps 1 and 2 hold all the work; step 3 is a single line.",
        "steps": [
            ("Put the equation in standard form",
             "Expand the brackets, clear any fractions, and move every term to one side "
             "so the other reads `0`. Arrange in descending powers, so that `a`, `b` and "
             "`c` can be seen."),
            ("Factor completely, common factor first",
             "Take out the GCF, as course 4 lesson 5 insists, then factor what is left. "
             "A monic trinomial needs a product-and-sum pair from lesson 7 of that "
             "course; anything else needs the AC method of lesson 8."),
            ("Set each non-constant factor to zero and solve",
             "Each one gives a linear equation. Skip any constant factor, which can "
             "never be zero. A repeated factor gives its solution once, not twice."),
            ("Substitute every answer into the original equation",
             "Into the equation as given, not the rearranged one, which may already "
             "carry the error. Two substitutions cost a line each and confirm the whole "
             "chain of reasoning above them."),
        ],
        "worked": {
            "title": "Three equations, three shapes",
            "intro": ["One needing rearrangement, one with a leading coefficient, and "
                      "one with a repeated factor."],
            "lines": [
                "A.  x² + 3x = 10",
                "        x² + 3x - 10 = 0          subtract 10",
                "        (x + 5)(x - 2) = 0        product -10, sum 3:  5 and -2",
                "        x = -5   or   x = 2",
                "",
                "    check  x = -5:   25 - 15 = 10",
                "           x =  2:    4 +  6 = 10",
                "",
                "B.  6x² + x - 12 = 0              ac = -72,  9 · (-8) = -72,  9 + (-8) = 1",
                "        6x² + 9x - 8x - 12 = 0",
                "        3x(2x + 3) - 4(2x + 3) = 0",
                "        (2x + 3)(3x - 4) = 0",
                "        x = -3/2   or   x = 4/3",
                "",
                "    check  x = -3/2:   6(9/4) - 3/2 - 12  =  27/2 - 3/2 - 12  =  0",
                "           x =  4/3:   6(16/9) + 4/3 - 12 =  32/3 + 4/3 - 12  =  0",
                "",
                "C.  4x² - 12x + 9 = 0",
                "        (2x - 3)² = 0             a perfect square trinomial",
                "        2x - 3 = 0",
                "        x = 3/2                   one solution, counted twice",
                "",
                "    check  x = 3/2:   9 - 18 + 9 = 0",
            ],
            "after": [
                "In A the check was carried out on `x² + 3x = 10`, the equation as "
                "given. Checking against `x² + 3x - 10 = 0` instead would agree with "
                "itself even if the subtraction had gone wrong, which is the one thing a "
                "check is supposed to catch.",
                "C has one solution, and nothing was lost in getting there. `(2x - 3)²` "
                "gives the equation `2x - 3 = 0` twice, and solving the same equation "
                "twice returns the same number twice. Lesson 10 shows what this looks "
                "like on a graph: a curve that touches the x-axis instead of crossing "
                "it.",
            ],
        },
        "quiz_title": "Factor and split",
        "quiz": [
            {"q": "Solve `x² - 7x + 12 = 0`.",
             "a": ["`x = 3` or `x = 4`", "`x = -3` or `x = -4`", "`x = 2` or `x = 6`",
                   "`x = 1` or `x = 12`"],
             "c": 0,
             "why": "Two numbers with product `12` and sum `-7`: `-3` and `-4`. So the "
                    "factors are `(x - 3)(x - 4)` and the solutions are the values that "
                    "make them zero. The second option reverses both signs; the last two "
                    "use divisor pairs of `12` whose sums are `8` and `13`, not `7`."},
            {"q": "Solve `3x² = 12x`.",
             "a": ["`x = 4` only", "`x = 0` or `x = 4`", "`x = 0` or `x = -4`",
                   "`x = 2` or `x = -2`"],
             "c": 1,
             "why": "`3x² - 12x = 0` gives `3x(x - 4) = 0`. The `3` contributes nothing, "
                    "and both `x = 0` and `x = 4` satisfy the original. Dividing both "
                    "sides by `3x` at the start produces the first option, which is the "
                    "right answer with one solution deleted."},
            {"q": "Why does `5(x - 2)(x + 7) = 0` have two solutions rather than three?",
             "a": ["The constant factor gives nothing, since `5 = 0` is false",
                   "The `5` has to be divided out first, and that costs a solution",
                   "It does have three: `x = 5`, `x = 2` and `x = -7`",
                   "A quadratic has at most two, so one of the three is dropped"],
             "c": 0,
             "why": "Setting each factor to zero gives `5 = 0`, `x - 2 = 0` and "
                    "`x + 7 = 0`. The first is false for every `x`, so it contributes no "
                    "solutions. Dividing by `5` is legal and changes nothing, which is "
                    "what makes the second option wrong about the cost."},
        ],
        "mistakes": [
            ("Factoring before there is a zero on the other side",
             "`x² + 3x = 10` factors as `x(x + 3) = 10`, and that is a dead end. "
             "Standard form is not a tidiness convention here; it is the hypothesis of "
             "the theorem you are about to use."),
            ("Inverting a factor instead of solving it",
             "`3x - 4 = 0` gives `x = 4/3`, not `x = 3/4` and not `x = -4/3`. Solve the "
             "small equation properly: add `4`, then divide by `3`. Reading the "
             "numerator and denominator off the bracket is a habit that works by "
             "accident on `(x - 4)` and fails everywhere else."),
            ("Reporting \"does not factor\" as \"no solutions\"",
             "`x² - 4x + 1 = 0` has no integer factorisation and two real solutions, "
             "`2 ± √3`. The failure of a search over the integers says nothing at all "
             "about whether solutions exist."),
        ],
        "standard": ("Finish when factoring is a first attempt you abandon quickly.",
                     "You should reach standard form without thinking, spend a few "
                     "seconds looking for an integer factorisation, and move to lesson 4 "
                     "or 5 without regret when none appears. Every answer checked in the "
                     "original equation, and a repeated factor reported as one solution."),
        "note": "Factoring is the fastest method and the least reliable, because it "
                "works only when the coefficients were chosen to let it. The next three "
                "lessons remove the condition a piece at a time: the square root "
                "property handles anything with no `x` term, completing the square "
                "handles everything, and the formula is completing the square carried "
                "out once and kept.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "the-square-root-property",
        "title": "The Square Root Property",
        "module": "Solving quadratics",
        "one_line": "Two roots, and the plus-or-minus that is not optional.",
        "summary": (
            "If `x² = k` with `k` positive there are two solutions, `√k` and `-√k`. The "
            "symbol `√k` names one number, the non-negative one; the second solution "
            "comes from the property and not from the symbol. Keeping those two things "
            "apart is what stops half the answer going missing."
        ),
        "key": [
            "x² = k,  k > 0     →    x = √k   or   x = -√k",
            "x² = 0             →    x = 0                     one solution",
            "x² = k,  k < 0     →    no real solution",
            "(x - h)² = k       →    x = h ± √k",
        ],
        "key_label": "One equation shape, three cases",
        "concepts_intro": (
            "This method applies to any quadratic with no plain `x` term, and to any "
            "equation already written as a square. Both are more common than they look."
        ),
        "concepts": [
            ("The radical sign names one number",
             "`√25` is `5`. It is not `±5` and it is not `-5`. The symbol is defined to "
             "return the non-negative root, so that taking a square root is a function "
             "with one output, and course 1 fixed that convention. The `±` in a solution "
             "is put there by you, deliberately."),
            ("The property is the zero product property in disguise",
             "`x² = k` is `x² - k = 0`, and for `k ≥ 0` that is `(x - √k)(x + √k) = 0` "
             "by the difference of squares. Nothing new is being assumed here; lesson 1 "
             "is still doing the work, one layer down."),
            ("A negative on the right means no real solution",
             "The square of any real number is `0` or positive, so `x² = -9` cannot hold "
             "for a real `x`. It is not that the answer is hard to find &mdash; there is "
             "none among the real numbers. Lesson 7 builds a system in which there is "
             "one."),
        ],
        "read_title": "Undoing a square",
        "read_intro": "The property, its proof, why the plus-or-minus lives outside the symbol, and the shifted form lesson 4 needs.",
        "body": [
            ("thm", ("The square root property",
                     "Let `k` be a real number. The equation `x² = k` has two real "
                     "solutions, `x = √k` and `x = -√k`, when `k &gt; 0`; the single "
                     "solution `x = 0` when `k = 0`; and no real solution when "
                     "`k &lt; 0`.")),
            ("proof", [
                "Suppose `k &gt; 0`. Then `√k` is defined and positive, and "
                "`k = (√k)²`. So `x² = k` is `x² - (√k)² = 0`, which factors as "
                "`(x - √k)(x + √k) = 0` by the difference of squares. Lesson 1 splits "
                "it into `x = √k` or `x = -√k`, and those are two different numbers "
                "because `√k` is not `0`.",
                "If `k = 0` the same factorisation reads `x · x = 0`, so `x = 0` is the "
                "only solution &mdash; the two brackets have collapsed onto each other.",
                "If `k &lt; 0`, suppose some real `x` satisfied `x² = k`. Every real "
                "number has `x² ≥ 0`, so `k ≥ 0`, contradicting `k &lt; 0`. No such `x` "
                "exists.",
            ]),
            ("p", "The `±` is notation, not an operation. `x = ±√k` abbreviates the "
                  "sentence \"`x` is `√k`, or `x` is `-√k`\". Writing it saves a line. "
                  "Forgetting it loses a solution, and the answer that remains looks "
                  "complete."),
            ("h3", "Why √(x²) is not x"),
            ("p", "Taking the square root of both sides is often described as "
                  "\"square-rooting\", which hides a real difficulty. `√(x²)` is `|x|`, "
                  "not `x`: at `x = -3` the left side is `√9 = 3` and `x` itself is "
                  "`-3`. So `x² = k` gives `|x| = √k`, and course 2's absolute value "
                  "equations then split that into the two cases `x = √k` and `x = -√k`."),
            ("p", "Both routes &mdash; the factoring one and the absolute value one "
                  "&mdash; arrive at the same pair, and both of them make the second "
                  "sign a consequence of the algebra rather than a decoration added at "
                  "the end."),
            ("h3", "Isolate the square first"),
            ("p", "The property is stated for `x² = k`, so anything standing between the "
                  "square and the equals sign has to be cleared before it can be used."),
            ("math", [
                "3x² - 75 = 0",
                "    3x² = 75            add 75 to both sides",
                "     x² = 25            divide both sides by 3",
                "      x = 5    or    x = -5",
            ]),
            ("p", "Clearing the coefficient first is not the only legal order. Taking "
                  "the root of both sides of `3x² = 75` gives `|x|√3 = 5√3`, which "
                  "reduces to `|x| = 5` and the same pair of answers. It is simply the "
                  "order that keeps the arithmetic in plain sight, and it is the one to "
                  "use."),
            ("h3", "The shifted form"),
            ("p", "The property does not care what is being squared. If `(x - h)² = k` "
                  "then `x - h` is one of the two square roots of `k`, so `x - h = ±√k` "
                  "and `x = h ± √k`. That is the form every completed square arrives at, "
                  "which is why the whole of lesson 4 depends on this one."),
            ("example", ("A shifted square, with a radical to simplify",
                         "`(x - 4)² = 20`. So `x - 4 = ±√20`, and `√20 = √(4 · 5) = 2√5` "
                         "by course 5. The solutions are `x = 4 + 2√5` and "
                         "`x = 4 - 2√5`, usually written together as `x = 4 ± 2√5`.",
                         "Check the first: `(4 + 2√5 - 4)² = (2√5)² = 4 · 5 = 20`. The "
                         "`4`s cancel before anything is squared, which is what makes "
                         "checking a shifted square quick.")),
            ("p", "Two habits are worth fixing here. Simplify the radical, because "
                  "`2√5` is the standard form of `√20` and course 5 said so. And leave "
                  "it as a radical: `2√5` is a number, and replacing it with a rounded "
                  "decimal replaces the answer with something that is not a solution of "
                  "the equation."),
            ("example", ("No real solution",
                         "`x² + 9 = 0` gives `x² = -9`, and no real number squares to a "
                         "negative. The complete and honest answer at this point in the "
                         "course is \"no real solution\".",
                         "Lesson 7 introduces a number whose square is `-1`, and lesson "
                         "9 solves the quadratics this lesson had to set aside. The "
                         "answer here becomes `x = 3i` or `x = -3i`, which is again a "
                         "pair, and again produced by this property.")),
        ],
        "lab": ("quadratic", {
            "mode": "sqrt",
            "panel_title": "Isolate the square, then take both roots",
            "panel_intro": "Build an equation of the form `a(x - h)² + c = 0` and watch "
                           "the isolation happen a step at a time. The lab prints both "
                           "roots exactly, and reports a negative right-hand side as \"no "
                           "real solution\" rather than as an error.",
        }),
        "steps_title": "Solving by the square root property",
        "steps_intro": "The method applies when there is no loose x term, or when the square is already assembled.",
        "steps": [
            ("Check the shape",
             "`4x² - 9 = 0` and `2(x + 1)² = 18` both qualify: a square, a constant, and "
             "no separate `x` term. `x² + 6x - 7 = 0` does not, and lesson 4 exists to "
             "convert it into one that does."),
            ("Isolate the squared quantity",
             "Undo the additions and subtractions first, then the multiplication, "
             "exactly as course 2 did with linear equations. What is left must read "
             "`(something)² = k`, with nothing else on that side."),
            ("Write both roots, with the ± in place",
             "`something = ±√k`. Write the `±` in the same movement as the radical, not "
             "afterwards, because afterwards is when it goes missing and because "
             "attaching it later attaches it to the wrong quantity."),
            ("Simplify the radical, solve for x, and check both answers",
             "Reduce `√k` to standard form, then finish the linear equation that is "
             "left. Substitute both answers into the original; a shifted square checks "
             "quickly, because the shift cancels before the squaring."),
        ],
        "worked": {
            "title": "Three isolations, one with fractions",
            "intro": ["Each one clears everything from around the square before any root "
                      "is taken."],
            "lines": [
                "A.  3x² - 75 = 0",
                "        3x² = 75",
                "         x² = 25",
                "          x = 5    or    x = -5",
                "",
                "    check   3(25) - 75 = 0,  and (-5)² = 25 too, so both work",
                "",
                "B.  (x - 4)² = 20",
                "        x - 4 = ±√20 = ±2√5           √20 = √(4·5) = 2√5",
                "            x = 4 ± 2√5",
                "",
                "    check   (4 + 2√5 - 4)² = ( 2√5)² = 4·5 = 20",
                "            (4 - 2√5 - 4)² = (-2√5)² = 4·5 = 20",
                "",
                "C.  2(x + 3)² - 5 = 0",
                "        2(x + 3)² = 5",
                "         (x + 3)² = 5/2",
                "            x + 3 = ±√(5/2) = ±√10/2   since √5/√2 = √10/2",
                "                x = -3 ± √10/2",
                "",
                "    check   (√10/2)² = 10/4 = 5/2,  and 2(5/2) - 5 = 0",
            ],
            "after": [
                "In C the denominator was cleared by course 5's method: "
                "`√5/√2 = (√5 · √2)/2 = √10/2`. Leaving the answer as `-3 ± √(5/2)` is "
                "not wrong, but `√10/2` is the standard form, and standard form is what "
                "makes two answers comparable.",
                "A produced a symmetric pair and B and C did not. The reason is "
                "structural: A involves only `x²`, so the equation cannot tell `x` from "
                "`-x` and its solutions must be negatives of one another. In B and C the "
                "square is shifted, and the pair is symmetric about `4` and about `-3` "
                "instead. Lesson 11 gives that centre a name.",
            ],
        },
        "quiz_title": "Roots, both of them",
        "quiz": [
            {"q": "Solve `x² = 49`.",
             "a": ["`x = 7`", "`x = 7` or `x = -7`", "`x = -7`", "`x = 49/2`"],
             "c": 1,
             "why": "`7² = 49` and `(-7)² = 49`, so both are solutions, and the property "
                    "guarantees there are no others. Reporting only `x = 7` is the "
                    "standard loss of half the answer; `49/2` comes from halving instead "
                    "of taking a root."},
            {"q": "Which statement is correct?",
             "a": ["`√16 = ±4`",
                   "`√16 = 4`, and `x² = 16` has the two solutions `4` and `-4`",
                   "`√16 = -4`",
                   "`x² = 16` has the single solution `x = 4`"],
             "c": 1,
             "why": "The radical sign returns the non-negative root, so `√16` is the one "
                    "number `4`. The equation is a different object from the symbol, and "
                    "it has two solutions. Options one and four each collapse the two "
                    "objects into one, in opposite directions."},
            {"q": "Solve `(x + 2)² = 9`.",
             "a": ["`x = 1` or `x = -5`", "`x = 5` or `x = -1`", "`x = 3` or `x = -3`",
                   "`x = 1`"],
             "c": 0,
             "why": "`x + 2 = ±3`, so `x = -2 + 3 = 1` or `x = -2 - 3 = -5`. The second "
                    "option adds `2` where it should subtract, the third forgets the "
                    "shift altogether, and the fourth drops the negative root."},
        ],
        "mistakes": [
            ("Writing only the positive root",
             "`x² = 49` has two solutions. The `±` has to be written at the moment the "
             "root is taken. Attaching it afterwards is worse than useless: "
             "`(x + 2)² = 9` gives `x = 1` or `x = -5`, so solving `x + 2 = 3` and then "
             "writing `x = ±1` produces one right answer and one wrong one."),
            ("Writing `√9 = ±3`",
             "The radical sign is a function and returns a single value. The second "
             "solution of `x² = 9` comes from the property, which supplies the sign; the "
             "symbol never does. Keeping them apart matters in lesson 5, where the "
             "formula writes the `±` explicitly in front of the radical for exactly this "
             "reason."),
            ("Taking the root of each term separately",
             "From `x² + 9 = 25` you may not conclude `x + 3 = 5`. The correct route "
             "gives `x² = 16` and `x = ±4`, and the shortcut's answer `x = 2` fails the "
             "check: `4 + 9 = 13`, not `25`. A square root does not distribute over a "
             "sum, for the same reason a square does not."),
        ],
        "standard": ("Finish when the ± appears at the same moment the radical does.",
                     "Given `2(x + 3)² - 5 = 0` you should isolate, take both roots in "
                     "one written step, simplify the radical exactly, and check. You "
                     "should also be able to say why `√k` on its own is not the answer: "
                     "the symbol is a function, and the equation has two solutions."),
        "note": "This property looks narrow, because it needs an equation with no `x` "
                "term, and lesson 4 makes it universal. Completing the square turns any "
                "quadratic into `(x - h)² = k`, and from there this is the property that "
                "finishes it. Everything in the next lesson exists to reach the shape "
                "this one can already solve.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "completing-the-square",
        "title": "Completing the Square",
        "module": "Solving quadratics",
        "one_line": "Turning any quadratic into a perfect square plus a constant.",
        "summary": (
            "Adding the square of half the coefficient of `x` turns `x² + bx` into a "
            "perfect square. That one move converts any quadratic into a form the square "
            "root property can finish, and carried out on `ax² + bx + c = 0` with "
            "letters instead of numbers it is the proof of the quadratic formula."
        ),
        "key": [
            "x² + bx + (b/2)²  =  (x + b/2)²      halve b, then square it",
            "x² + 6x = 7           add (6/2)² = 9 to BOTH sides",
            "x² + 6x + 9 = 16      the left side is now a square",
            "(x + 3)² = 16    →    x + 3 = ±4    →    x = 1  or  x = -7",
        ],
        "key_label": "The constant, and what it buys",
        "concepts_intro": (
            "One number does all the work: half the coefficient of `x`, squared. The "
            "rest of the lesson is bookkeeping about where that number is allowed to go."
        ),
        "concepts": [
            ("Half, then square, in that order",
             "`(x + p)² = x² + 2px + p²`, so the coefficient of `x` is `2p` and the "
             "constant is `p²`. Given a coefficient `b`, the number `p` is `b/2` and the "
             "constant is `(b/2)² = b²/4`. Squaring first and halving afterwards gives "
             "`b²/2`, which is a different number for every `b` except `0`."),
            ("Adding to both sides is legal; adding to one side is not",
             "In an equation you may add `9` to both sides, and that is exactly what "
             "this method does. In an expression there are no sides, so you add `9` and "
             "subtract `9` in the same place, for a net change of nothing. The two "
             "versions look different on the page and are the same idea."),
            ("It always works",
             "Factoring needs cooperative coefficients. This does not. Every quadratic "
             "completes, including the ones whose answers are irrational and the ones "
             "with no real solution at all &mdash; those end at a negative number on the "
             "right, and the square root property reports that honestly."),
        ],
        "read_title": "Manufacturing a perfect square",
        "read_intro": "Where the constant comes from, the procedure on an equation, the extra step when a is not 1, and the difference between an equation and an expression.",
        "body": [
            ("p", "Lesson 3 solves `(x - h)² = k` in two lines. Completing the square is "
                  "the process that puts an arbitrary quadratic into that shape, so that "
                  "those two lines are always available."),
            ("h3", "The constant that completes the square"),
            ("math", [
                "(x + p)²  =  x² + 2px + p²",
                "",
                "so if the coefficient of x is  b = 2p,",
                "then  p = b/2   and the constant needed is  p² = (b/2)²",
            ]),
            ("p", "In words: halve the coefficient of `x`, then square it. For "
                  "`x² + 6x` the coefficient is `6`, half of it is `3`, and `3² = 9`, so "
                  "`x² + 6x + 9` is a perfect square and equals `(x + 3)²`. The sign "
                  "looks after itself: for `x² - 5x` half of `-5` is `-5/2`, its square "
                  "is `25/4`, which is positive, and the minus survives inside the "
                  "bracket as `(x - 5/2)²`. The constant added is always positive, "
                  "because it is a square."),
            ("h3", "Solving an equation"),
            ("math", [
                "x² + 6x - 7 = 0",
                "x² + 6x = 7                  move the constant to the right",
                "x² + 6x + 9 = 7 + 9          add 9 to BOTH sides",
                "(x + 3)² = 16                the left side is now a square",
                "x + 3 = ±4                   square root property, lesson 3",
                "x = 1   or   x = -7",
            ]),
            ("p", "The `+ 9` on the right is what keeps the equation true. Adding `9` to "
                  "the left alone would produce a different equation with different "
                  "solutions, and the fact that its left side factors more nicely would "
                  "be no consolation at all."),
            ("h3", "When the leading coefficient is not 1"),
            ("p", "The identity `(x + p)² = x² + 2px + p²` has a leading coefficient of "
                  "`1` in it, and says nothing about `2x² + 8x`. So `a` has to go first. "
                  "In an equation, divide every term by `a` &mdash; always legal, "
                  "because `a ≠ 0` is part of the definition."),
            ("math", [
                "2x² + 8x - 10 = 0",
                " x² + 4x -  5 = 0            divide every term by 2",
                " x² + 4x = 5",
                " x² + 4x + 4 = 5 + 4         half of 4 is 2, and 2² = 4",
                "     (x + 2)² = 9",
                "        x + 2 = ±3",
                "            x = 1   or   x = -5",
                "",
                "check   2(1) + 8(1) - 10 = 0        2(25) - 40 - 10 = 0",
            ]),
            ("h3", "Fractions are normal"),
            ("math", [
                "x² - 5x + 3 = 0",
                "x² - 5x = -3",
                "x² - 5x + 25/4 = -3 + 25/4       half of -5 is -5/2, and (-5/2)² = 25/4",
                "   (x - 5/2)² = 13/4             -3 + 25/4 = -12/4 + 25/4 = 13/4",
                "      x - 5/2 = ±√13 / 2         √(13/4) = √13 / 2",
                "            x = (5 ± √13) / 2",
            ]),
            ("p", "Nothing guarantees that `b` is even, and fractions arriving here are "
                  "not a sign that something has gone wrong. They are what the method "
                  "produces whenever `b` is odd, and `(5 ± √13)/2` is the exact answer. "
                  "A quadratic that completes to a negative number on the right, such as "
                  "`(x - 1)² = -2/3`, has no real solution, and that is a finished answer "
                  "too."),
            ("h3", "An expression has no sides"),
            ("p", "Completing the square on `x² + 6x + 1`, where there is no equals sign, "
                  "cannot be done by adding `9` to both sides &mdash; there is only one "
                  "side. Instead add `9` and subtract `9` in the same expression, which "
                  "changes its value nowhere:"),
            ("math", [
                "x² + 6x + 1  =  (x² + 6x + 9) - 9 + 1        add 9 and subtract 9",
                "             =  (x + 3)² - 8",
                "",
                "check at x = 0:   0 + 0 + 1 = 1     and   (0 + 3)² - 8 = 9 - 8 = 1",
                "check at x = 1:   1 + 6 + 1 = 8     and   (1 + 3)² - 8 = 16 - 8 = 8",
            ]),
        ],
        "lab": ("quadratic", {
            "mode": "complete",
            "panel_title": "Half of b, squared",
            "panel_intro": "Set the coefficients and step through the completion one "
                           "line at a time. The lab shows the constant it adds and where "
                           "it adds it, and keeps every number as an exact fraction, so "
                           "an odd `b` shows you what it really costs.",
        }),
        "steps_title": "Completing the square on an equation",
        "steps_intro": "Four steps, and the order is not negotiable: step 1 always precedes step 3.",
        "steps": [
            ("Divide every term by a, if a is not 1",
             "The identity being used assumes a leading coefficient of `1`. Dividing is "
             "legal because `a ≠ 0`, and any fractions it produces should be carried "
             "exactly rather than rounded."),
            ("Move the constant to the other side",
             "You want `x² + bx` alone on the left, with nothing added to it, so that "
             "there is room for the constant that completes it."),
            ("Add (b/2)² to both sides",
             "Halve the coefficient of `x`, square it, and write it on both sides in the "
             "same line. Then write the left side as `(x + b/2)²` immediately, before "
             "the arithmetic on the right has a chance to distract you."),
            ("Finish with the square root property, then check",
             "`(x + b/2)² = k` gives `x + b/2 = ±√k`. A negative `k` means no real "
             "solution, and the work is over. Otherwise simplify the radical, solve, and "
             "substitute both answers into the original equation."),
        ],
        "worked": {
            "title": "Four completions, one of each kind",
            "intro": ["An even b, an odd b, a leading coefficient to clear, and one that "
                      "ends negative."],
            "lines": [
                "A.  x² + 6x - 7 = 0",
                "        x² + 6x = 7",
                "        x² + 6x + 9 = 7 + 9          half of 6 is 3;  3² = 9",
                "        (x + 3)² = 16",
                "        x + 3 = ±4",
                "        x = 1   or   x = -7",
                "    check   1 + 6 - 7 = 0            49 - 42 - 7 = 0",
                "",
                "B.  x² - 5x + 3 = 0",
                "        x² - 5x = -3",
                "        x² - 5x + 25/4 = -3 + 25/4   half of -5 is -5/2;  (-5/2)² = 25/4",
                "        (x - 5/2)² = 13/4            -12/4 + 25/4 = 13/4",
                "        x - 5/2 = ±√13 / 2",
                "        x = (5 ± √13) / 2",
                "",
                "C.  2x² + 8x - 10 = 0",
                "        x² + 4x - 5 = 0              divide every term by 2",
                "        x² + 4x = 5",
                "        x² + 4x + 4 = 5 + 4          half of 4 is 2;  2² = 4",
                "        (x + 2)² = 9",
                "        x = -2 ± 3   →   x = 1  or  x = -5",
                "    check   2(1) + 8(1) - 10 = 0     2(25) - 40 - 10 = 0",
                "",
                "D.  3x² - 6x + 5 = 0",
                "        x² - 2x + 5/3 = 0            divide every term by 3",
                "        x² - 2x = -5/3",
                "        x² - 2x + 1 = -5/3 + 1       half of -2 is -1;  (-1)² = 1",
                "        (x - 1)² = -2/3              -5/3 + 3/3 = -2/3",
                "        no real solution",
            ],
            "after": [
                "B is the general case and A is the lucky one. Half of an odd number is "
                "a fraction, its square has a `4` underneath, and the right-hand side "
                "then needs a common denominator. None of that is a mistake; it is what "
                "the method does. Lesson 5 performs exactly this arithmetic once, with "
                "letters, so that it never has to be performed again.",
                "D stopped at `(x - 1)² = -2/3`, and that was the complete answer. No "
                "real number squares to a negative, so there is nothing further to try. "
                "The method reported the absence of a real solution; it did not fail to "
                "find one.",
            ],
        },
        "quiz_title": "Completing the square",
        "quiz": [
            {"q": "What constant makes `x² - 12x + ___` a perfect square?",
             "a": ["`36`", "`-36`", "`144`", "`6`"],
             "c": 0,
             "why": "Half of `-12` is `-6`, and `(-6)² = 36`, giving `(x - 6)²`. The "
                    "constant is always positive, because it is a square, which is what "
                    "rules out `-36`; `144` is `b²` with no halving; and `6` is half of "
                    "`12` with no squaring and no sign."},
            {"q": "To solve `x² + 5x = 2` by completing the square, what is added to both sides?",
             "a": ["`25/4`", "`5/2`", "`25`", "`25/2`"],
             "c": 0,
             "why": "Half of `5` is `5/2`, and `(5/2)² = 25/4`. `5/2` halves without "
                    "squaring, `25` squares without halving, and `25/2` squares first "
                    "and halves afterwards &mdash; the same two operations in the wrong "
                    "order."},
            {"q": "What is the first step in solving `3x² + 12x - 2 = 0` by completing the square?",
             "a": ["Divide every term by `3`", "Add `36` to both sides",
                   "Add `6` to both sides", "Multiply every term by `3`"],
             "c": 0,
             "why": "The completion identity assumes a leading coefficient of `1`. "
                    "Adding `36` treats `12` as the `x` coefficient of a monic quadratic "
                    "when it is not: after dividing by `3` the coefficient is `4`, and "
                    "the constant to add is `4`."},
        ],
        "mistakes": [
            ("Adding the constant to one side of an equation only",
             "`x² + 6x = 7` becomes `x² + 6x + 9 = 16`, not `x² + 6x + 9 = 7`. The "
             "second is a different equation, with solutions `-3 ± √7`, and they are not "
             "the ones you were asked for."),
            ("Completing before dividing by a",
             "For `3x² + 12x - 2 = 0` the coefficient to halve is `4`, not `12`. The "
             "identity `x² + bx + (b/2)² = (x + b/2)²` describes a monic quadratic, and "
             "using it on `3x² + 12x` applies a theorem outside its hypotheses."),
            ("Losing the subtracted constant when rewriting an expression",
             "`x² + 6x + 1` is `(x + 3)² - 8`, not `(x + 3)² + 1`. Adding `9` inside the "
             "square has to be paid for outside it, and one substitution settles it: at "
             "`x = 0` the original is `1`, the correct form gives `1`, and the version "
             "without the `-9` gives `10`."),
        ],
        "standard": ("Finish when an odd b does not slow you down.",
                     "Take a quadratic with `a ≠ 1` and an odd `b`, complete the square "
                     "in exact fractions, and finish with the square root property. If "
                     "you can do that reliably you can also derive the quadratic "
                     "formula, which is the next lesson and is this procedure carried "
                     "out once on `ax² + bx + c = 0`."),
        "note": "This is the most valuable procedure in the course, and it pays twice. "
                "Run it on `ax² + bx + c = 0` and it produces the quadratic formula, in "
                "lesson 5. Run it on `y = ax² + bx + c`, using the add-and-subtract form "
                "so that the left side stays as `y`, and it produces the vertex, in "
                "lesson 11.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "the-quadratic-formula",
        "title": "The Quadratic Formula",
        "module": "Solving quadratics",
        "one_line": "Completing the square once, in general, and keeping the result.",
        "summary": (
            "Completing the square on `ax² + bx + c = 0` with letters instead of numbers "
            "produces one formula that solves every quadratic. Deriving it once is worth "
            "more than memorising it, because the derivation is what shows why standard "
            "form is required and why the sign of `b` has to be carried."
        ),
        "key": [
            "ax² + bx + c = 0,  a ≠ 0        standard form, signs included",
            "        -b ± √(b² - 4ac)",
            "   x =  ------------------      both signs, one denominator",
            "               2a",
        ],
        "key_label": "One formula, for every quadratic",
        "concepts_intro": (
            "The formula is a theorem with a proof you can carry out yourself, and the "
            "proof is lesson 4 done with letters."
        ),
        "concepts": [
            ("Standard form is part of the formula",
             "`a`, `b` and `c` are the coefficients of `ax² + bx + c = 0`. `3x² = 5x - 2` "
             "has `b = -5` and `c = 2`, and neither can be read until the rearrangement "
             "is done. Reading them off the equation as printed is the commonest way to "
             "get a wrong answer out of a right formula."),
            ("The signs belong to the coefficients",
             "If `b = -7` then `-b = 7` and `b² = 49`. Both of those catch people, and "
             "they catch them in opposite directions: one drops a sign that should "
             "survive, the other keeps a sign that should not."),
            ("It finishes, and it says when there is nothing to find",
             "If `b² - 4ac` is negative the formula asks for the square root of a "
             "negative number, and no real number supplies one. That is not a breakdown "
             "&mdash; it is the formula reporting that there is no real solution, which "
             "lesson 6 learns to read off before any work is done."),
        ],
        "read_title": "Deriving the formula once",
        "read_intro": "The proof, the one subtlety inside it, and how to use the result without manufacturing sign errors.",
        "body": [
            ("p", "Lesson 4 completes the square on any particular quadratic. Doing it "
                  "on `ax² + bx + c = 0`, with letters in place of numbers, does it for "
                  "all of them at once and leaves a formula behind."),
            ("thm", ("The quadratic formula",
                     "Let `a`, `b` and `c` be real with `a ≠ 0`. If `b² - 4ac ≥ 0`, the "
                     "real solutions of `ax² + bx + c = 0` are exactly "
                     "`x = (-b + √(b² - 4ac))/(2a)` and `x = (-b - √(b² - 4ac))/(2a)`. "
                     "If `b² - 4ac &lt; 0` there are no real solutions.")),
            ("proof", [
                "Divide through by `a`, which is allowed because `a ≠ 0`: "
                "`x² + (b/a)x + c/a = 0`. Move the constant across: "
                "`x² + (b/a)x = -c/a`.",
                "Half the coefficient of `x` is `b/(2a)`, and its square is `b²/(4a²)`. "
                "Add that to both sides: `x² + (b/a)x + b²/(4a²) = -c/a + b²/(4a²)`.",
                "The left side is now `(x + b/(2a))²`. On the right, put both terms over "
                "`4a²`: since `-c/a = -4ac/(4a²)`, the right side is `(b² - 4ac)/(4a²)`.",
                "`4a²` is positive, so the right side has the same sign as `b² - 4ac`. "
                "By the square root property there is a real solution exactly when "
                "`b² - 4ac ≥ 0`, and then "
                "`x + b/(2a) = ±√(b² - 4ac) / √(4a²)`.",
                "Now `√(4a²) = 2|a|`, not `2a`, because a square root is never negative. "
                "But the numerator already carries a `±`, so the two numbers produced by "
                "dividing by `2|a|` are the same two numbers produced by dividing by "
                "`2a` &mdash; listed in the other order when `a` is negative. Writing "
                "`2a` is therefore safe, and it is what keeps the formula short.",
                "Subtracting `b/(2a)` gives `x = -b/(2a) ± √(b² - 4ac)/(2a)`, and the "
                "two terms share a denominator: `x = (-b ± √(b² - 4ac))/(2a)`.",
            ]),
            ("p", "The quantity `b² - 4ac` appeared without being asked for, and it "
                  "decides everything about the answer. Lesson 6 is about that quantity "
                  "alone."),
            ("h3", "Using it"),
            ("p", "Three things are worth doing in a fixed order every single time: "
                  "rearrange into standard form, write `a`, `b` and `c` down with their "
                  "signs, and compute `b² - 4ac` on its own line before substituting "
                  "anything else."),
            ("math", [
                "2x² - 7x + 3 = 0            a = 2,   b = -7,   c = 3",
                "",
                "b² - 4ac  =  (-7)² - 4(2)(3)  =  49 - 24  =  25",
                "",
                "      7 ± √25       7 ± 5",
                "x  =  --------  =  -------     →    x = 12/4 = 3    or    x = 2/4 = 1/2",
                "         4            4",
            ]),
            ("p", "`-b` was `-(-7) = 7`, and `b²` was `(-7)² = 49`. Writing `b = -7` on "
                  "its own line first is what makes both of those automatic rather than "
                  "remembered."),
            ("p", "This one can be checked independently, because it happens to factor: "
                  "`2x² - 7x + 3 = (2x - 1)(x - 3)`, giving `x = 1/2` and `x = 3`. Two "
                  "methods, computed separately, agreeing."),
            ("h3", "Simplifying the result"),
            ("p", "The formula frequently hands back an unreduced fraction, and the "
                  "reduction has to divide every term of the numerator, not the "
                  "convenient one:"),
            ("math", [
                "x² + 4x + 1 = 0             a = 1,   b = 4,   c = 1",
                "",
                "b² - 4ac  =  16 - 4(1)(1)  =  12",
                "",
                "     -4 ± √12       -4 ± 2√3",
                "x =  ---------  =  ----------  =  -2 ± √3       divide BOTH terms by 2",
                "         2              2",
                "",
                "     not  -4 ± √3,   and not  -2 ± 2√3",
            ]),
            ("p", "`√12 = 2√3` by course 5, and then the `2` underneath divides into "
                  "`-4` and into `2√3` alike. Cancelling from one term only produces a "
                  "number that is not a solution: substituting `-4 + √3` into "
                  "`x² + 4x + 1` gives `4 - 4√3`, which is not `0`."),
            ("h3", "A negative leading coefficient"),
            ("p", "`a` may be negative and the formula does not mind. `-x² + 5x - 6 = 0` "
                  "has `a = -1`, `b = 5`, `c = -6`, so `b² - 4ac = 25 - 4(-1)(-6) = "
                  "25 - 24 = 1` and `x = (-5 ± 1)/(-2)`, giving `x = 2` and `x = 3`. "
                  "Multiplying the equation through by `-1` first gives "
                  "`x² - 5x + 6 = 0` and the same two solutions with far less sign "
                  "handling, which is a free simplification worth taking."),
            ("example", ("When the formula is the wrong tool",
                         "`x² - 9 = 0` has `b = 0`, and the formula gives "
                         "`x = ±√36 / 2 = ±3`. Correct, and slower than the square root "
                         "property, which reads `x² = 9` and stops.",
                         "The formula always works. It is not always the shortest route, "
                         "and one line of lesson 6 usually tells you which route to "
                         "take.")),
        ],
        "lab": ("quadratic", {
            "mode": "formula",
            "panel_title": "Coefficients in, exact roots out",
            "panel_intro": "Set `a`, `b` and `c` and watch the substitution happen with "
                           "every sign shown. The lab keeps the answer as an exact "
                           "radical and then reduces it, so you can see which terms of "
                           "the numerator the denominator actually divides.",
        }),
        "steps_title": "Applying the quadratic formula",
        "steps_intro": "The first two steps hold the errors; the last two are arithmetic.",
        "steps": [
            ("Rearrange into ax² + bx + c = 0",
             "Every term on one side in descending powers, zero on the other. Nothing "
             "can be read off the equation until this is done."),
            ("Write a, b and c with their signs, on their own line",
             "`3x² - 5x - 2 = 0` gives `a = 3`, `b = -5`, `c = -2`. That line costs "
             "three seconds and removes the two commonest errors in the course."),
            ("Compute b² - 4ac next, with brackets",
             "`(-5)² - 4(3)(-2) = 25 + 24 = 49`. Brackets round a negative coefficient "
             "cost nothing. If the result is negative, stop: there is no real solution."),
            ("Substitute, simplify the radical, then divide every term",
             "`√49 = 7`, so `x = (5 ± 7)/6`, which is `2` or `-1/3`. When the radical "
             "does not reduce to an integer, cancel only by a factor that divides the "
             "whole numerator."),
        ],
        "worked": {
            "title": "The formula three times",
            "intro": ["One that also factors, one that does not, and one with a negative "
                      "leading coefficient."],
            "lines": [
                "A.  2x² - 7x + 3 = 0             a = 2,   b = -7,   c = 3",
                "        b² - 4ac = (-7)² - 4(2)(3) = 49 - 24 = 25",
                "        x = (7 ± 5) / 4",
                "        x = 12/4 = 3     or     x = 2/4 = 1/2",
                "    check by factoring:  (2x - 1)(x - 3) = 2x² - 7x + 3",
                "",
                "B.  x² + 4x + 1 = 0              a = 1,   b = 4,   c = 1",
                "        b² - 4ac = 16 - 4(1)(1) = 12",
                "        x = (-4 ± √12)/2 = (-4 ± 2√3)/2 = -2 ± √3",
                "    check x = -2 + √3:",
                "        (-2 + √3)² = 4 - 4√3 + 3 = 7 - 4√3",
                "        4(-2 + √3)              = -8 + 4√3",
                "        (7 - 4√3) + (-8 + 4√3) + 1 = 0",
                "",
                "C.  -x² + 5x - 6 = 0             a = -1,  b = 5,   c = -6",
                "        b² - 4ac = 25 - 4(-1)(-6) = 25 - 24 = 1",
                "        x = (-5 ± 1) / (-2)",
                "        x = (-4)/(-2) = 2       or     x = (-6)/(-2) = 3",
                "    check   -(4) + 10 - 6 = 0        -(9) + 15 - 6 = 0",
            ],
            "after": [
                "In C the term `-4ac` was `-4(-1)(-6)`, a product of three negative "
                "factors and therefore negative: `-24`. That single sign is the "
                "difference between `b² - 4ac = 1` and `b² - 4ac = 49`, and between the "
                "answers `2` and `3` and the answers `-1` and `6`.",
                "B is the case the formula exists for. `x² + 4x + 1` has no integer "
                "factorisation, the answers are irrational, and completing the square "
                "would have produced them in about the same number of lines &mdash; "
                "which is precisely what the derivation predicts, since the formula is "
                "that completion, already done.",
            ],
        },
        "quiz_title": "Coefficients and roots",
        "quiz": [
            {"q": "For `3x² = 5x + 2`, what are `a`, `b` and `c`?",
             "a": ["`a = 3`, `b = 5`, `c = 2`", "`a = 3`, `b = -5`, `c = -2`",
                   "`a = 3`, `b = -5`, `c = 2`", "`a = 3`, `b = 5`, `c = -2`"],
             "c": 1,
             "why": "Standard form first: `3x² - 5x - 2 = 0`. Both terms changed sign as "
                    "they crossed the equals sign, so `b = -5` and `c = -2`. The first "
                    "option reads the coefficients off the equation as printed, which is "
                    "the error this step exists to prevent."},
            {"q": "Solve `2x² - 7x + 3 = 0`.",
             "a": ["`x = 3` or `x = 1/2`", "`x = -3` or `x = -1/2`",
                   "`x = 1/3` or `x = 2`", "`x = 3` or `x = -1/2`"],
             "c": 0,
             "why": "`b² - 4ac = 49 - 24 = 25`, so `x = (7 ± 5)/4`, which is `3` or "
                    "`1/2`. The second option uses `-b = -7` instead of `+7`; the third "
                    "inverts both answers, which is the reflex that reads a root off a "
                    "factor upside down."},
            {"q": "`x = (-4 ± 2√3)/2` simplifies to:",
             "a": ["`-2 ± √3`", "`-2 ± 2√3`", "`-4 ± √3`", "`-2 ± √3/2`"],
             "c": 0,
             "why": "The `2` underneath divides `-4` and `2√3` alike. The second and "
                    "third options divide one term and leave the other, which gives "
                    "numbers that are not solutions; the fourth divides the radical term "
                    "by `2` twice."},
        ],
        "mistakes": [
            ("Reading a, b and c before reaching standard form",
             "`3x² = 5x + 2` has `b = -5` and `c = -2`. Nothing may be substituted until "
             "every term is on one side, and the signs that change while crossing are "
             "exactly the ones that matter."),
            ("Writing b² as a negative number",
             "If `b = -7` then `b² = 49`. Read without brackets, `-7²` means `-(7²)` and "
             "gives `-49`, which turns `b² - 4ac = 25` into `-73` and converts two real "
             "solutions into none. Brackets round a negative `b` settle it."),
            ("Dividing only part of the numerator by 2a",
             "`(-4 ± 2√3)/2` is `-2 ± √3`. Writing `-4 ± √3` leaves every answer two out: "
             "substituting `-4 + √3` into `x² + 4x + 1` gives `4 - 4√3`, not `0`."),
        ],
        "standard": ("Finish when you can derive the formula, not only quote it.",
                     "Take `ax² + bx + c = 0` and complete the square on it from memory, "
                     "reaching the formula in six or seven lines. Then use it with `a`, "
                     "`b` and `c` written out separately every time, and reduce the "
                     "result by dividing the whole numerator."),
        "note": "The formula is the last of the four solution methods, and it subsumes "
                "the others rather than replacing them: factoring is faster when it "
                "works, and the square root property is faster when `b = 0`. What the "
                "formula adds is a guarantee that no quadratic on this course can go "
                "unfinished &mdash; and the quantity `b² - 4ac` that fell out of the "
                "derivation is the whole of the next lesson.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "the-discriminant",
        "title": "The Discriminant",
        "module": "Solving quadratics",
        "one_line": "Counting the solutions before finding them.",
        "summary": (
            "`b² - 4ac` is the quantity under the radical in the quadratic formula, and "
            "its sign decides how many real solutions there are: two, one or none. "
            "Computing it first costs one line and tells you what kind of answer to "
            "expect, or that there is nothing to look for."
        ),
        "key": [
            "D = b² - 4ac",
            "D > 0     two distinct real solutions",
            "D = 0     exactly one real solution,  x = -b/(2a)",
            "D < 0     no real solution",
        ],
        "key_label": "One number, three cases",
        "concepts_intro": (
            "Nothing new is computed here. The discriminant is a piece of the formula, "
            "given a name and read on its own."
        ),
        "concepts": [
            ("The sign is the whole message",
             "`D` sits under a square root, and a square root of a negative number is "
             "not real. That is the entire reason there are three cases, and it is why "
             "the size of `D` matters far less than its sign."),
            ("D = 0 means one solution, not none",
             "The formula becomes `x = (-b ± 0)/(2a)`, and both branches give "
             "`-b/(2a)`. So the equation has exactly one solution and the quadratic is a "
             "constant times a perfect square. \"No solutions\" is the `D &lt; 0` case, "
             "and the two are not neighbours."),
            ("For integer coefficients, a perfect square means it factors",
             "If `a`, `b`, `c` are integers and `D` is the square of an integer, then "
             "`√D` is an integer and both solutions are rational, so the quadratic "
             "factors over the rationals. That turns \"should I try factoring?\" into a "
             "calculation instead of a guess."),
        ],
        "read_title": "Reading the answer before finding it",
        "read_intro": "The definition, the three cases with their proofs, and the extra thing a perfect square tells you.",
        "body": [
            ("def", ("Discriminant",
                     "For `ax² + bx + c = 0` with `a ≠ 0`, the "
                     "<strong>discriminant</strong> is `D = b² - 4ac`.",
                     "It is the quantity under the radical in the quadratic formula, and "
                     "it is computed from the coefficients of the standard form, signs "
                     "included.")),
            ("thm", ("What the sign of D decides",
                     "Let `a`, `b`, `c` be real with `a ≠ 0`, and let `D = b² - 4ac`. If "
                     "`D &gt; 0` then `ax² + bx + c = 0` has two distinct real "
                     "solutions. If `D = 0` it has exactly one. If `D &lt; 0` it has "
                     "none.")),
            ("proof", [
                "Lesson 5 showed the equation is equivalent to "
                "`(x + b/(2a))² = D/(4a²)`, and `4a²` is positive, so the right-hand "
                "side has the same sign as `D`.",
                "If `D &gt; 0` the square root property gives two solutions, "
                "`x = -b/(2a) ± √D/(2a)`. They are distinct because `√D` is not `0` and "
                "`2a` is not `0`.",
                "If `D = 0` the equation reads `(x + b/(2a))² = 0`, whose only solution "
                "is `x = -b/(2a)`.",
                "If `D &lt; 0` the right-hand side is negative, and no real number has a "
                "negative square. There is no real solution.",
            ]),
            ("p", "The three cases are exhaustive and they do not overlap, so the "
                  "discriminant always answers the question, and never answers it "
                  "twice."),
            ("h3", "What D = 0 looks like"),
            ("p", "`4x² - 12x + 9 = 0` has `D = 144 - 144 = 0`, and its factorisation is "
                  "`(2x - 3)²`. The two facts travel together: `D = 0` exactly when the "
                  "quadratic is a constant times a perfect square, and then the single "
                  "solution is the double root of lesson 2."),
            ("h3", "Perfect squares and rational solutions"),
            ("thm", ("When a quadratic with integer coefficients factors",
                     "Let `a`, `b` and `c` be integers with `a ≠ 0`. The equation "
                     "`ax² + bx + c = 0` has rational solutions if and only if "
                     "`D = b² - 4ac` is the square of an integer.")),
            ("proof", [
                "Suppose `D = m²` for some integer `m ≥ 0`. Then `√D = m`, and the "
                "solutions `(-b ± m)/(2a)` are quotients of integers with a non-zero "
                "denominator, so both are rational.",
                "Conversely, suppose some solution `x` is rational. Multiplying "
                "`(x + b/(2a))² = D/(4a²)` through by `4a²` gives `(2ax + b)² = D`, so "
                "`D` is the square of the rational number `2ax + b`. A rational number "
                "whose square is an integer is itself an integer &mdash; the same fact "
                "course 4's rational root theorem rests on &mdash; so `2ax + b` is an "
                "integer and `D` is the square of one.",
            ]),
            ("p", "So the search of course 4, lesson 7 can be called off before it "
                  "starts. `x² - 4x + 1 = 0` has `D = 16 - 4 = 12`, which is not a "
                  "perfect square, so no rational factorisation exists and no amount of "
                  "looking will produce one. `x² - 5x + 6 = 0` has `D = 1`, so one does, "
                  "and it is `(x - 2)(x - 3)`."),
            ("h3", "What the discriminant does not tell you"),
            ("p", "It gives the number of real solutions, and for integer coefficients "
                  "whether they are rational. It does not give the solutions, it does "
                  "not say whether they are positive or negative, and its size carries "
                  "no message about difficulty: `D = 1` and `D = 10000` both mean \"two "
                  "real solutions\"."),
            ("p", "One derived fact is worth keeping. The two solutions are "
                  "`-b/(2a) ± √D/(2a)`, so they differ by `√D/|a|`. The gap depends on "
                  "`a` as well: with `a` held fixed, a larger `D` puts the two answers "
                  "further apart, which is a statement about the graph in lesson 10 "
                  "rather than about the solving."),
            ("example", ("Four discriminants",
                         "`x² - 5x + 6`: `D = 25 - 24 = 1`, positive and a perfect "
                         "square, so two rational solutions, `2` and `3`. "
                         "`4x² - 12x + 9`: `D = 0`, so one solution, `3/2`. "
                         "`x² - 4x + 1`: `D = 12`, positive and not a perfect square, so "
                         "two irrational solutions, `2 ± √3`. `x² + x + 1`: `D = -3`, so "
                         "no real solution.",
                         "Each of the four took one line to classify, and three of them "
                         "took longer than that to solve.")),
            ("p", "The habit worth building is to compute `D` on every quadratic before "
                  "choosing a method. A perfect square sends you to factoring, a `D` of "
                  "`0` tells you to expect a single answer, and a negative `D` ends the "
                  "work at this point in the course."),
        ],
        "lab": ("quadratic", {
            "mode": "discriminant",
            "panel_title": "The sign, before the solving",
            "panel_intro": "Move the coefficients and watch `D` change sign. The lab "
                           "names the case, says whether `D` is a perfect square, and "
                           "only then shows the solutions &mdash; so the prediction can "
                           "be made before the answer appears.",
        }),
        "steps_title": "Using the discriminant first",
        "steps_intro": "One line of arithmetic, then a decision about which method to use.",
        "steps": [
            ("Reach standard form and read a, b, c with their signs",
             "The same first step as lesson 5, for the same reason. A `D` computed from "
             "the wrong coefficients answers a question about a different equation."),
            ("Compute D with brackets",
             "For `2x² - 4x - 3 = 0`, `D = (-4)² - 4(2)(-3) = 16 + 24 = 40`, not "
             "`16 - 24`. With `a` positive, a negative `c` makes `-4ac` positive, and "
             "this is where the sign goes missing."),
            ("Read the case off the sign",
             "Positive gives two real solutions, zero gives one, negative gives none "
             "&mdash; and in the last case the answer is already complete."),
            ("If D is positive and the coefficients are integers, test for a perfect square",
             "If it is one, factoring will work and is probably quicker. If it is not, "
             "go straight to the formula and expect an irrational answer."),
        ],
        "worked": {
            "title": "Four quadratics, classified then solved",
            "intro": ["D is computed on the first line each time, and the method is "
                      "chosen from it."],
            "lines": [
                "A.  x² - 5x + 6 = 0          a = 1,  b = -5,  c = 6",
                "        D = 25 - 24 = 1      positive, and 1 = 1²  →  two rational roots",
                "        factor:  (x - 2)(x - 3) = 0",
                "        x = 2   or   x = 3",
                "",
                "B.  4x² - 12x + 9 = 0        a = 4,  b = -12,  c = 9",
                "        D = 144 - 144 = 0    →  exactly one solution",
                "        x = -b/(2a) = 12/8 = 3/2",
                "        and indeed  4x² - 12x + 9 = (2x - 3)²",
                "",
                "C.  x² - 4x + 1 = 0          a = 1,  b = -4,  c = 1",
                "        D = 16 - 4 = 12      positive, not a perfect square",
                "                             →  two irrational roots, no factorisation",
                "        x = (4 ± √12)/2 = (4 ± 2√3)/2 = 2 ± √3",
                "",
                "D.  x² + x + 1 = 0           a = 1,  b = 1,  c = 1",
                "        D = 1 - 4 = -3       negative  →  no real solution",
            ],
            "after": [
                "C is the one that pays. Course 4's product-and-sum search over the "
                "divisors of `1` would have been tried and would have failed, and "
                "`D = 12` says in advance that it must: `12` is not a perfect square, so "
                "no rational factorisation exists. One line replaced a search.",
                "D was settled by a single subtraction. Lesson 9 supplies the method "
                "that finishes it, and the two non-real solutions are `-1/2 ± (√3/2)i`. "
                "Nothing in this lesson changes when they arrive &mdash; `D &lt; 0` will "
                "still mean \"no real solution\", which is why the word <em>real</em> is "
                "worth writing now.",
            ],
        },
        "quiz_title": "Counting before solving",
        "quiz": [
            {"q": "How many real solutions does `2x² + 3x + 5 = 0` have?",
             "a": ["Two", "One", "None", "It cannot be decided without solving it"],
             "c": 2,
             "why": "`D = 9 - 4(2)(5) = 9 - 40 = -31`, which is negative, so no real "
                    "number satisfies the equation. Deciding this without solving is "
                    "exactly what the discriminant is for, which rules out the last "
                    "option."},
            {"q": "A quadratic equation has `D = 0`. What follows?",
             "a": ["It has no real solutions", "It has exactly one real solution",
                   "It has two solutions that are negatives of one another",
                   "It is not really a quadratic"],
             "c": 1,
             "why": "The formula becomes `x = (-b ± 0)/(2a)`, and both signs give "
                    "`-b/(2a)`. The quadratic is a constant times a perfect square, and "
                    "in lesson 10 its graph touches the x-axis once instead of crossing "
                    "it twice."},
            {"q": "`x² - 7x + 10 = 0` has `D = 9`. Beyond the count of solutions, what does that say?",
             "a": ["The two solutions are `9` apart",
                   "`9` is a perfect square, so both solutions are rational and it factors",
                   "The solutions are irrational", "One of the solutions is `9`"],
             "c": 1,
             "why": "`D = 49 - 40 = 9 = 3²`, so `√D` is an integer and `(7 ± 3)/2` gives "
                    "`5` and `2`, with `(x - 5)(x - 2)` as the factorisation. The two "
                    "solutions are `3` apart, not `9`: the gap is `√D/|a|`, and "
                    "confusing `D` with its root is the error the first option names."},
        ],
        "mistakes": [
            ("Dropping the sign in -4ac",
             "When `a` and `c` have opposite signs, `-4ac` is positive and `D` grows. "
             "For `2x² - 4x - 3 = 0`, `D = 16 + 24 = 40`, not `16 - 24 = -8` &mdash; "
             "the difference between two real solutions and none at all."),
            ("Reading D = 0 as \"no solutions\"",
             "`D = 0` gives exactly one solution, `-b/(2a)`. It is the boundary between "
             "two and none, and it belongs to neither of them."),
            ("Saying \"no solutions\" when \"no real solutions\" is meant",
             "Before lesson 7 the two phrases look interchangeable, and they are not. "
             "`x² + 1 = 0` has no real solution and two complex ones. The sentence you "
             "write today should still be true three lessons from now."),
        ],
        "standard": ("Finish when D is the first thing you compute on any quadratic.",
                     "Given the coefficients you should produce `D`, name the case, say "
                     "whether the answers will be rational, and only then pick a method. "
                     "Getting the sign of `-4ac` right when `c` is negative is the single "
                     "skill that makes the whole habit reliable."),
        "note": "The discriminant is the last thing this course does with real numbers "
                "alone. `D &lt; 0` is not the end of the story: lesson 7 defines a number "
                "whose square is `-1`, lesson 9 returns to every equation this lesson "
                "dismissed, and lesson 10 shows what a negative discriminant looks like "
                "&mdash; a parabola that misses the x-axis entirely.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "complex-numbers",
        "title": "Complex Numbers",
        "module": "Complex numbers",
        "one_line": "Defining i, and what a complex number is.",
        "summary": (
            "`x² = -1` has no real solution, so a number `i` with `i² = -1` is defined "
            "and joined to the reals. A complex number is `a + bi` with `a` and `b` "
            "real; every real number is one of them, and the system is built so that all "
            "the algebra of courses 1 to 5 keeps working unchanged."
        ),
        "key": [
            "i² = -1                      the defining property",
            "a + bi,  a and b real        real part a,  imaginary part b",
            "√(-9) = 3i                   since (3i)² = 9i² = -9",
            "a + bi = c + di    ⟺    a = c  and  b = d",
        ],
        "key_label": "The definition, and what follows from it",
        "concepts_intro": (
            "Extending the number system to solve an equation is not a new move. It has "
            "happened three times already on this path, and every time for the same "
            "reason."
        ),
        "concepts": [
            ("i is defined by exactly one property",
             "`i² = -1`, and nothing else about it is assumed. Everything else &mdash; "
             "how to add, multiply and divide with it &mdash; follows from that one "
             "equation together with the ordinary laws of algebra, which is what lesson "
             "8 works out."),
            ("A complex number has two real parts",
             "In `a + bi`, both `a` and `b` are real numbers. The imaginary part of "
             "`3 - 7i` is `-7`, not `-7i`: it is a real number by universal convention, "
             "and the convention exists so that \"imaginary part\" names a coordinate "
             "you can compare and equate."),
            ("Every real number is complex",
             "`5` is `5 + 0i`. The reals are not replaced or contradicted; they sit "
             "inside the complex numbers as the ones with imaginary part `0`. Everything "
             "proved in courses 1 to 5 goes on holding, for exactly the numbers it held "
             "for before."),
        ],
        "read_title": "A number whose square is negative",
        "read_intro": "Why the extension is legitimate, what the objects are, and how to write a root of a negative number.",
        "body": [
            ("p", "Lesson 6 ended with `D &lt; 0` and the answer \"no real solution\". "
                  "The word carrying the weight in that phrase is <em>real</em>. "
                  "`x² + 1 = 0` needs a number whose square is `-1`, and no point on the "
                  "number line has one, because the square of a real number is `0` or "
                  "positive."),
            ("h3", "This has happened before"),
            ("p", "Each earlier number system was extended for the same reason: an "
                  "equation with no solution inside it."),
            ("ul", [
                "`x + 3 = 1` has no solution among the counting numbers. The negative "
                "integers were joined on, and subtraction became always possible.",
                "`3x = 1` has no solution among the integers. The fractions were joined "
                "on, and division by a non-zero number became always possible.",
                "`x² = 2` has no solution among the rationals. The irrationals were "
                "joined on, and the number line was filled in.",
                "`x² = -1` has no solution among the reals. This lesson joins on `i`, "
                "and every quadratic acquires solutions.",
            ]),
            ("p", "At each stage the new numbers were called unnatural, then absurd, "
                  "then irrational, then imaginary, and each time the name stuck while "
                  "the objection did not. \"Imaginary\" is a seventeenth-century insult "
                  "that hardened into a technical term. It does not mean these numbers "
                  "are less legitimate than the others, and nothing in the arithmetic "
                  "treats them as such."),
            ("def", ("The imaginary unit",
                     "`i` is the number defined by the property `i² = -1`. It is not a "
                     "real number.",
                     "That `i` is not real is a consequence rather than an assumption: "
                     "every real number `r` satisfies `r² ≥ 0`, and `-1 &lt; 0`.")),
            ("def", ("Complex number",
                     "A <strong>complex number</strong> is one that can be written "
                     "`a + bi` with `a` and `b` real. `a` is the <strong>real "
                     "part</strong> and `b` is the <strong>imaginary part</strong>, and "
                     "both of them are real numbers.",
                     "`a + bi` is called <strong>standard form</strong>. A complex "
                     "number with `b = 0` is real; one with `a = 0` and `b ≠ 0` is "
                     "called <strong>pure imaginary</strong>.")),
            ("p", "So `3 - 7i` has real part `3` and imaginary part `-7`. Calling the "
                  "imaginary part `-7i` is a common slip and a consequential one: the "
                  "two coordinates of a complex number are both real numbers, and that "
                  "is what makes the next theorem sayable."),
            ("thm", ("Equality of complex numbers",
                     "For real `a`, `b`, `c` and `d`: `a + bi = c + di` if and only if "
                     "`a = c` and `b = d`.")),
            ("proof", [
                "If `a = c` and `b = d` the two expressions are identical, so they are "
                "equal.",
                "Conversely, suppose `a + bi = c + di`. Rearranging gives "
                "`a - c = (d - b)i`. If `d - b` were not `0`, dividing by it would give "
                "`i = (a - c)/(d - b)`, a quotient of two real numbers with a non-zero "
                "denominator and therefore itself real &mdash; and `i` is not real. So "
                "`d - b = 0`, that is `b = d`; and then `a - c = 0`, that is `a = c`.",
            ]),
            ("p", "One equation between complex numbers is therefore two equations "
                  "between real numbers. That is used constantly from here on, and it is "
                  "why complex numbers behave like points in a plane: `a + bi` "
                  "corresponds to the point `(a, b)`, with the real numbers lying along "
                  "the horizontal axis and the pure imaginary ones up the vertical."),
            ("p", "The plane picture also explains an absence. No ordering of the "
                  "complex numbers is compatible with their arithmetic, so the words "
                  "\"positive\", \"greater than\" and \"between\" are not available for "
                  "them, and neither are the signs `&lt;` and `≤`. Points in a plane do "
                  "not come in an order. From here on, those words are used only where "
                  "the numbers involved are real."),
            ("h3", "Square roots of negative numbers"),
            ("def", ("The root of a negative number",
                     "For a positive real number `k`, `√(-k)` is defined to be `i√k`.",
                     "One line checks it: `(i√k)² = i²(√k)² = (-1)k = -k`. The other "
                     "square root of `-k` is `-i√k`, exactly as a positive number has "
                     "two real square roots and the symbol names one of them.",
                     "Convert to `i` before doing anything else with the expression. The "
                     "rule `√a · √b = √(ab)` is stated for non-negative `a` and `b` and "
                     "does not survive down here, as lesson 8 shows in detail.")),
            ("math", [
                "√(-9)  = 3i          since (3i)²  = 9i²   = -9",
                "√(-25) = 5i          since (5i)²  = 25i²  = -25",
                "√(-12) = 2i√3        since √12 = 2√3, and (2i√3)² = 4·3·i² = -12",
            ]),
            ("example", ("The shape a quadratic produces",
                         "Applied to an equation with `D &lt; 0`, the formula hands back "
                         "something like `(-6 + √(-8))/2`. Convert the root first: "
                         "`√(-8) = 2i√2`. Then `(-6 + 2i√2)/2 = -3 + i√2`, which is "
                         "standard form with real part `-3` and imaginary part `√2`.",
                         "Both terms of the numerator were divided by `2`, exactly as in "
                         "lesson 5. Lesson 9 does this systematically; the point here is "
                         "only that the result is an ordinary complex number, of the "
                         "shape this lesson defined.")),
        ],
        "lab": ("complex", {
            "mode": "intro",
            "panel_title": "The plane the reals sit inside",
            "panel_intro": "Set the real and the imaginary part and watch the point "
                           "move. Setting the imaginary part to `0` puts the point back "
                           "on the horizontal axis, which is the number line of course "
                           "1, unchanged and still there.",
        }),
        "steps_title": "Writing a complex number in standard form",
        "steps_intro": "Standard form is a + bi with a and b real. Four moves get anything there.",
        "steps": [
            ("Convert every root of a negative number to i first",
             "`√(-12)` becomes `i√12`. Do this before any multiplying: the radical laws "
             "of course 5 assume non-negative radicands, and they stop being reliable "
             "the moment a negative goes under a root."),
            ("Simplify the radical that is left",
             "`√12 = 2√3` by course 5, so `i√12` becomes `2i√3`. An unsimplified radical "
             "is as unfinished here as it was there."),
            ("Separate the real and the imaginary parts",
             "Collect everything without an `i` into `a` and everything with one into "
             "`bi`. A real number is `a + 0i` and a pure imaginary is `0 + bi`; both are "
             "in standard form once written that way."),
            ("Divide through if there is a denominator",
             "`(-6 + 2i√2)/2` is `-3 + i√2`. Every term of the numerator gets divided, "
             "which is the same reduction lesson 5 needed and the same place it goes "
             "wrong."),
        ],
        "worked": {
            "title": "Five numbers, put into standard form",
            "intro": ["Each one ends as a + bi, with a and b named and both of them "
                      "real."],
            "lines": [
                "1.  √(-25)       =  5i        =  0 + 5i         a = 0,   b = 5",
                "",
                "2.  7                         =  7 + 0i         a = 7,   b = 0",
                "",
                "3.  √(-12)       =  2i√3      =  0 + 2√3 i      a = 0,   b = 2√3",
                "",
                "4.  (-6 + √(-8)) / 2",
                "        √(-8) = 2i√2                            convert the root first",
                "        (-6 + 2i√2)/2  =  -3 + i√2              a = -3,  b = √2",
                "",
                "5.  x² = -49     →  x = 7i  or  x = -7i         (7i)² = 49i² = -49",
            ],
            "after": [
                "Line 2 is the one worth pausing on. `7` is a complex number, with "
                "imaginary part `0`. Nothing about it changed in this lesson; the "
                "definition was written so as to include it.",
                "Line 5 is the square root property of lesson 3, applied where it "
                "previously reported nothing. `x² = -49` has two solutions among the "
                "complex numbers, and they are negatives of one another, exactly as "
                "`x² = 49` had two real ones. Lesson 9 shows that the pairing is not a "
                "coincidence.",
            ],
        },
        "quiz_title": "i and standard form",
        "quiz": [
            {"q": "`√(-16)` equals:",
             "a": ["`4i`", "`-4`", "`16i`", "`4`"],
             "c": 0,
             "why": "`√(-16) = i√16 = 4i`, and the check is `(4i)² = 16i² = -16`. `-4` "
                    "squares to `+16`, so it is a square root of `16` and not of `-16`; "
                    "`16i` squares to `-256`."},
            {"q": "The imaginary part of `3 - 7i` is:",
             "a": ["`-7i`", "`-7`", "`7`", "`3`"],
             "c": 1,
             "why": "By definition the imaginary part of `a + bi` is the real number "
                    "`b`, and here `b = -7`; the minus sign belongs to it. Calling it "
                    "`-7i` is the usual slip, and it breaks the equality rule, which "
                    "compares one real number on each side."},
            {"q": "If `x + yi = 5 - 2i`, with `x` and `y` real, then:",
             "a": ["`x = 5` and `y = -2`", "`x = 5` and `y = 2`",
                   "`x = 5` and `y = -2i`", "There is not enough information"],
             "c": 0,
             "why": "Equality of complex numbers is equality of both parts, so `x = 5` "
                    "and `y = -2`. `y` was stated to be real, which rules out `-2i`; and "
                    "one complex equation always pins down two real unknowns, which "
                    "rules out the last option."},
        ],
        "mistakes": [
            ("Writing `√(-9) = -3`",
             "`(-3)² = 9`, not `-9`, so `-3` is not a square root of `-9` at all. The "
             "minus sign under the radical comes out as `i`, not as a minus in front: "
             "`√(-9) = 3i`."),
            ("Calling the imaginary part `bi`",
             "The imaginary part of `3 - 7i` is `-7`, a real number. This is a "
             "convention and it is universal, and keeping to it is what makes \"equate "
             "the real parts, then the imaginary parts\" a statement about real numbers "
             "rather than a circular one."),
            ("Treating the reals and the complex numbers as rival systems",
             "Every real number is complex, with imaginary part `0`. `x² - 4 = 0` does "
             "not acquire new solutions in the larger system &mdash; it still has "
             "exactly `2` and `-2`. Extending the numbers adds objects; it does not "
             "disturb anything that was already true."),
        ],
        "standard": ("Finish when a + bi is the only form you leave an answer in.",
                     "Convert any root of a negative number to `i` immediately, simplify "
                     "the radical, and name the real and imaginary parts as real "
                     "numbers. You should also be able to say what `i` is defined by "
                     "&mdash; one equation, `i² = -1` &mdash; and resist the idea that "
                     "anything further about it has been assumed."),
        "note": "This lesson defines the objects. Lesson 8 gives them arithmetic, and "
                "lesson 9 sends them back to the quadratics lesson 6 had to set aside. "
                "The pattern worth keeping in view is the one all four extensions share: "
                "the system grows exactly enough to solve the equation that defeated it, "
                "and nothing that was true beforehand stops being true.",
    },
]
