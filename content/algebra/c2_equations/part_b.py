"""Course 2, lessons 08-13 — modelling, inequalities, absolute value, and writing a solution set down."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "modelling-with-linear-equations",
        "title": "Modelling with Linear Equations",
        "module": "Applying equations",
        "one_line": "From a described situation to an equation you can solve.",
        "summary": (
            "The algebra in this lesson is lesson 3's, unchanged. The work is everything "
            "around it: naming the unknown as a number, finding the one quantity the "
            "words describe twice, and deciding whether the number the equation produces "
            "is an answer the situation will accept."
        ),
        "key": [
            "let m = the number of units       m is a NUMBER, not a thing",
            "20 + 0.15m  =  35 + 0.10m         one quantity, written twice",
            "m = 300                           solve, then check in the equation",
            "does m = 300 fit the words?       judge, then answer what was asked",
        ],
        "key_label": "Four stages, and only one of them is algebra",
        "concepts_intro": (
            "Three habits separate a model that works from an equation that merely has "
            "the right numbers in it."
        ),
        "concepts": [
            ("The unknown is a number, and its name says so",
             "Write `let m = the number of months`, not `let m = months`. If `m` is a "
             "thing rather than a count then `20 + 0.15m` means nothing, and no step "
             "afterwards can repair it. Every unknown gets a noun phrase and a unit."),
            ("An equation comes from one quantity measured two ways",
             "The equals sign has to be earned. Find a single quantity &mdash; a cost, a "
             "total, a length &mdash; that the situation describes twice, write both "
             "descriptions, and set them equal. Without that sentence there is nothing "
             "to write."),
            ("The equation's answer and the question's answer are different things",
             "`m = 300` is what the algebra produces. Whether the situation accepts 300, "
             "and whether 300 is what was asked for, are two further questions. A model "
             "that skips them reports nonsense with confidence."),
        ],
        "read_title": "From words to an equation, and back",
        "read_intro": "Naming the unknown, building both sides, and the two judgements at the end that the algebra cannot make for you.",
        "body": [
            ("p", "Nothing here is a new manipulation. Every equation in this lesson is "
                  "solved by the steps of lessons 2 to 4. What is new is that the equation "
                  "has to be produced from a paragraph of English, and then handed back to "
                  "that paragraph at the end."),
            ("h3", "Naming the unknown"),
            ("def", ("Model",
                     "A <strong>model</strong> is an equation whose letters stand for "
                     "named quantities in a described situation, together with a statement "
                     "of what each letter means and what unit it is measured in.",
                     "The statement of meaning is part of the model, not a courtesy. An "
                     "equation whose letters are undefined cannot be checked against the "
                     "situation, and that check is the only thing that makes it a model "
                     "rather than an exercise.")),
            ("p", "Choose as the unknown the quantity that the others are described "
                  "relative to. In <em>the length is 3 cm more than twice the width</em>, "
                  "the width is the one to name: the length is then `2w + 3` and nothing "
                  "else has to be invented. Naming the length instead is legal and gives "
                  "a width of `(l − 3)/2`, which is more to carry."),
            ("ul", [
                "Name it in a sentence: `let w = the width in centimetres`. The unit is "
                "part of the sentence.",
                "Write every other quantity in terms of that letter, one at a time, "
                "before writing any equals sign.",
                "Keep one unit throughout. Pounds on the left and pence on the right is "
                "not an equation about anything.",
            ]),
            ("h3", "Building the two sides"),
            ("p", "An equation says two expressions have the same value. So the sentence "
                  "you are looking for in the problem is the one that says two quantities "
                  "are equal, or asks when they will be. Everything before that sentence "
                  "builds the two expressions; the sentence itself supplies the `=`."),
            ("example", ("Two payment plans",
                         "Plan A charges 20 up front and 0.15 for each unit. Plan B "
                         "charges 35 up front and 0.10 for each unit. Let `m` be the "
                         "number of units. Plan A's total cost is `20 + 0.15m` and plan "
                         "B's is `35 + 0.10m`. The question &mdash; at how many units do "
                         "they cost the same? &mdash; is what supplies the equals sign.")),
            ("math", [
                "20 + 0.15m  =  35 + 0.10m",
                "",
                "subtract 0.10m     20 + 0.05m  =  35",
                "subtract 20             0.05m  =  15",
                "divide by 0.05              m  =  300",
                "",
                "check   20 + 0.15(300)  =  20 + 45  =  65",
                "        35 + 0.10(300)  =  35 + 30  =  65      ✓",
            ]),
            ("p", "The decimals are fractions: `0.15 = 3/20` and `0.10 = 1/10 = 2/20`, so "
                  "the coefficient of `m` on the left exceeds the one on the right by "
                  "`1/20`. Lesson 4's clearing move applies unchanged &mdash; multiply "
                  "every term by 20 and the equation becomes `400 + 3m = 700 + 2m`, with "
                  "no decimals in it at all."),
            ("h3", "The number the equation gives, and the answer the question wants"),
            ("example", ("Three consecutive whole numbers adding to 48",
                         "Call the first `n`. The three are `n`, `n + 1` and `n + 2`, and "
                         "their sum is `3n + 3`. So `3n + 3 = 48`, giving `n = 15` and the "
                         "numbers `15, 16, 17`. If the question asked for the largest, the "
                         "answer is `17` &mdash; `n` was defined as the first, and the "
                         "definition is what you read at the end.")),
            ("p", "Change the total to 50 and the same model gives `3n + 3 = 50`, so "
                  "`n = 47/3`. The equation is solved and the model is not: there is no "
                  "run of three consecutive whole numbers with sum 50. The fraction is the "
                  "algebra reporting that fact, not failing to produce an answer."),
            ("ul", [
                "<strong>A value the situation cannot hold.</strong> A negative count, a "
                "negative length, a fractional number of people.",
                "<strong>A value outside a stated range.</strong> A percentage above 100, "
                "a time before the situation starts.",
                "<strong>A correct value for a different quantity.</strong> You solved for "
                "the first number and the question wanted the last. This one is the "
                "hardest to notice, because every check you can run on the equation "
                "passes.",
            ]),
        ],
        "lab": ("equation", {
            "mode": "model",
            "panel_title": "Build it, solve it, then judge it",
            "panel_intro": "Pick a scenario and change its numbers. The lab rebuilds the "
                           "equation from what you typed, solves it in exact fractions, "
                           "and hands the answer back to the situation to be accepted or "
                           "rejected. Run the two mixture presets one after the other.",
        }),
        "steps_title": "Turning a described situation into an answer",
        "steps_intro": "The equation is written in step 3 and solved in step 4. Steps 1 and 2 are where models are won, and step 4's second half is where they are lost.",
        "steps": [
            ("Name the unknown in a full sentence, with its unit",
             "`let x = the number of litres added`, not `let x = litres`. Pick the "
             "quantity the others are described relative to, so that the rest of the "
             "problem can be written down without inventing a second letter."),
            ("Write every other quantity in terms of that letter",
             "One at a time, in words first if it helps. <em>Twice the width plus 3</em> "
             "becomes `2w + 3`. Do this before you look for the equation; half the errors "
             "in modelling are translation errors made in a hurry."),
            ("Find the quantity the words describe twice, and set the two descriptions equal",
             "This is the only place an equals sign can legitimately come from. If you "
             "cannot say in English which quantity is being measured twice, you do not "
             "yet have an equation."),
            ("Solve, check in the equation, then judge against the words",
             "Substituting back proves the arithmetic. It says nothing about whether "
             "`−100` litres can be poured or whether the question wanted the first number "
             "or the last. Those are separate, and they are the point of modelling."),
        ],
        "worked": {
            "title": "A mixture accepted, and the same mixture refused",
            "intro": ["You have 20 litres of a 10% solution and add `x` litres of a 50% "
                      "solution. What must `x` be to finish at 25%, and what happens if "
                      "you aim at 60% instead?"],
            "lines": [
                "unknown   x = the number of litres of 50% solution added",
                "",
                "pure substance afterwards, counted two ways:",
                "        what was there plus what was added   0.50x + 0.10(20)",
                "        25% of the new volume                0.25(x + 20)",
                "",
                "        0.5x + 2  =  0.25(x + 20)",
                "        0.5x + 2  =  0.25x + 5",
                "       0.25x      =  3",
                "            x     =  12",
                "",
                "check   0.5(12) + 2    =  6 + 2    =  8",
                "        0.25(12 + 20)  =  0.25(32)  =  8      ✓",
                "judge   12 litres can be poured                accept",
                "",
                "----------------------------------------------------------",
                "same numbers, aiming at 60%:",
                "",
                "        0.5x + 2  =  0.60(x + 20)",
                "        0.5x + 2  =  0.6x + 12",
                "      -0.1x       =  10",
                "            x     =  -100",
                "",
                "check   0.5(-100) + 2   =  -50 + 2   =  -48",
                "        0.6(-100 + 20)  =  0.6(-80)  =  -48    ✓",
                "judge   -100 litres cannot be poured           reject",
            ],
            "after": [
                "The second solve is correct algebra. Every step is legal and the "
                "substitution confirms the value: `x = −100` really does satisfy the "
                "equation. What it does not do is answer the question, because there is "
                "no such thing as pouring `−100` litres into a tank.",
                "The reason is visible without algebra. Mixing a 10% solution with a 50% "
                "solution always lands somewhere between 10% and 50%, and 60% is outside "
                "that range. The negative answer is the model reporting an impossible "
                "request. A write-up that stopped at `x = −100` would have reported it as "
                "a recipe.",
            ],
        },
        "quiz_title": "Building and judging",
        "quiz": [
            {"q": "A rectangle has perimeter 54 cm, and its length is 3 cm more than twice "
                  "its width. With `w` the width in cm, which equation says so?",
             "a": ["`2w + 2(2w + 3) = 54`", "`2w + (2w + 3) = 54`", "`w(2w + 3) = 54`",
                   "`2w + 2(3w + 2) = 54`"],
             "c": 0,
             "why": "The perimeter is twice the width plus twice the length, and the "
                    "length is `2w + 3`. The second option doubles the width but not "
                    "the length, the third is the area, and the fourth reads the "
                    "description as <em>2 more "
                    "than 3 times</em>. Solving the right one gives `w = 8` and length "
                    "`19`, and `16 + 38 = 54`."},
            {"q": "Three consecutive whole numbers add to 48. What is the largest of them?",
             "a": ["15", "16", "17", "18"],
             "c": 2,
             "why": "`3n + 3 = 48` gives `n = 15`, and `n` was the first number, so the "
                    "three are `15, 16, 17`. `15` is the equation's answer rather than the "
                    "question's, `16` is the middle number, and `18` comes from dropping "
                    "the `+ 3`: `3n = 48` gives `n = 16`, and the largest of "
                    "`16, 17, 18` is `18`."},
            {"q": "Aiming a 10% solution and a 50% solution at 60% gives the equation an "
                  "answer of `x = −100` litres. What is the correct conclusion?",
             "a": ["The arithmetic must be wrong, because a mixture cannot come out negative",
                   "`x = −100`, measured in litres, is the answer",
                   "The equation is solved correctly and the situation has no answer: "
                   "mixing 10% with 50% can never exceed 50%",
                   "Take the size of it and add 100 litres"],
             "c": 2,
             "why": "Substituting `−100` into the equation gives `−48` on both sides, so "
                    "the algebra is right. The model is what rejects it, and it rejects it "
                    "for a reason you can state in words before solving anything."},
        ],
        "mistakes": [
            ("Naming an object instead of a number",
             "`let c = chairs` leaves you no way to read `c + 4`. Write `let c = the "
             "number of chairs`. The unit belongs in the sentence too: `let t = the time "
             "in hours` and `let t = the time in minutes` produce different equations from "
             "the same paragraph."),
            ("Answering the equation instead of the question",
             "The consecutive-numbers model gives `n = 15`, and `15` is the first of the "
             "three. If the question asked for the largest, the answer is `17`. Write down "
             "what the letter means when you name it, and read that sentence again before "
             "you write the final line."),
            ("Setting two different units equal",
             "`20 + 0.15m` in pounds cannot be set equal to `3500 + 10m` in pence, even "
             "though the first describes plan A correctly and the second describes plan B "
             "correctly. In pounds plan B is `35 + 0.10m`, and that is the expression the "
             "left side has to be set equal to. State the unit of each side out loud "
             "before writing the equals sign; the two sides must measure the same quantity "
             "in the same unit."),
        ],
        "standard": ("Finish when you can say, in English, which quantity the problem measures twice.",
                     "That sentence is the model; the algebra after it is lesson 3. You "
                     "should also be able to state what your letter means and what unit it "
                     "carries, and to reject a solved value on the grounds of the "
                     "situation rather than the arithmetic."),
        "note": "Situations often say <em>at least</em>, <em>no more than</em> or <em>at "
                "most</em> rather than <em>exactly</em>. Those words give an inequality "
                "instead of an equation, and the rest of this course builds the machinery "
                "for them. The naming and building stages here are unchanged by that.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "linear-inequalities",
        "title": "Linear Inequalities",
        "module": "Inequalities",
        "one_line": "Solving, and the one rule that reverses the sign.",
        "summary": (
            "An inequality is solved by the same operations as an equation, with one "
            "exception: multiplying or dividing both sides by a negative number reverses "
            "the relation. The answer is a set of numbers rather than a single number, "
            "and that changes how it is written and how it is checked."
        ),
        "key": [
            "a < b             ⟹  a + c < b + c     adding never reverses",
            "a < b,  c > 0     ⟹  ac < bc           a positive multiplier: unchanged",
            "a < b,  c < 0     ⟹  ac > bc           a negative multiplier: REVERSED",
            "the answer is a set of numbers, not one number",
        ],
        "key_label": "Three operations, and what each does to the sign",
        "concepts_intro": (
            "One thing is genuinely different from solving an equation, and one thing "
            "that looks different is not."
        ),
        "concepts": [
            ("The answer is a set",
             "`3x − 4 &lt; 11` is true at `x = 0`, at `x = 4`, at `x = 49/10` and at every "
             "number below 5; it is false from 5 upward. The answer is `x &lt; 5`, a "
             "description of infinitely many numbers. There is no single value to report "
             "and writing `x = 5` reports the one number that fails."),
            ("Adding is always safe; multiplying is not",
             "You may add or subtract anything at all, including an expression containing "
             "`x`, and the relation is untouched. Multiplication and division are safe "
             "only when you know the sign of what you are multiplying by &mdash; which is "
             "why you may never divide by `x`."),
            ("The reversal is a theorem, not a convention",
             "Multiplying by a negative turns the relation round, and it follows from "
             "`a &lt; b` meaning `b − a` is positive together with the fact that a "
             "positive times a positive is positive. It is proved below in three lines, "
             "and knowing the proof is what stops you applying it at the wrong step."),
        ],
        "read_title": "The same steps, and the step that is different",
        "read_intro": "The four relations, the operations that preserve them, and the single case that turns a statement round.",
        "body": [
            ("def", ("Linear inequality",
                     "A <strong>linear inequality</strong> in `x` is a statement of the "
                     "form `ax + b &lt; c`, or the same with `≤`, `&gt;` or `≥` in place "
                     "of `&lt;`. Its <strong>solution set</strong> is the set of all "
                     "numbers that make the statement true.",
                     "Two statements are <strong>equivalent</strong> when they have the "
                     "same solution set. Solving means writing a chain of equivalent "
                     "statements ending in one whose solution set can be read off.")),
            ("p", "`&lt;` is strict and `≤` is not. The distinction is not decoration: "
                  "`x ≤ 5` contains 5 and `x &lt; 5` does not. It shows up as a filled or "
                  "a hollow endpoint on the number line, and as a square or a round "
                  "bracket in lesson 13."),
            ("h3", "What you may do to both sides"),
            ("ul", [
                "<strong>Add or subtract</strong> any number, or any expression in `x`. "
                "The relation is unchanged.",
                "<strong>Multiply or divide by a positive number.</strong> Unchanged.",
                "<strong>Multiply or divide by a negative number.</strong> The relation "
                "<strong>reverses</strong>: `&lt;` becomes `&gt;`, and `≤` becomes `≥`.",
                "<strong>Multiply or divide by an expression whose sign you do not "
                "know</strong> &mdash; anything containing `x`. Not permitted at all, "
                "because you cannot say which of the two rules above applies.",
            ]),
            ("p", "One example makes the third rule concrete. `3 &lt; 5` is true. Multiply "
                  "both sides by `−1`: `−3` and `−5`. On the number line `−3` sits to the "
                  "right of `−5`, so `−3 &gt; −5`. The relation had to turn round or the "
                  "statement would have become false."),
            ("thm", ("The reversal rule",
                     "If `a &lt; b` and `c &lt; 0`, then `ac &gt; bc`.",
                     "The same holds with `≤` and `≥` throughout. Dividing by `c` is "
                     "multiplying by `1/c`, which has the same sign as `c`, so division by "
                     "a negative reverses the relation too.")),
            ("proof", [
                "`a &lt; b` means `b − a` is positive. `c &lt; 0` means `−c` is positive.",
                "The product of two positive numbers is positive, so `(b − a)(−c) &gt; 0`. "
                "Expanding the left side gives `−bc + ac`, which is `ac − bc`.",
                "So `ac − bc &gt; 0`, and that is exactly the statement `ac &gt; bc`.",
            ]),
            ("h3", "Why you cannot divide by x"),
            ("math", [
                "3x  >  5x",
                "",
                "divide by x   →   3 > 5      false, so \"no solutions\"        WRONG",
                "subtract 3x   →   0 > 2x     divide by 2   →   0 > x       x < 0",
                "",
                "check  x = -1:   3(-1) = -3   and   5(-1) = -5,   -3 > -5    ✓",
            ]),
            ("p", "The first route divides by `x`, whose sign is unknown, and reaches the "
                  "conclusion that no number works. The second route only subtracts and "
                  "then divides by `2`, and finds that every negative number works. The "
                  "check settles it. Whenever a step would divide by something containing "
                  "the variable, collect terms instead."),
            ("h3", "Choosing the side that avoids the reversal"),
            ("math", [
                "5 - 3x  ≥  2x + 15",
                "",
                "route A   add 3x           5  ≥  5x + 15",
                "          subtract 15    -10  ≥  5x",
                "          divide by 5     -2  ≥  x           read it:  x ≤ -2",
                "",
                "route B   subtract 2x    5 - 5x  ≥  15",
                "          subtract 5        -5x  ≥  10",
                "          divide by -5        x  ≤  -2       sign REVERSED",
                "",
                "check  x = -2:   5 + 6 = 11   and   2(-2) + 15 = 11,   11 ≥ 11   ✓",
                "       x =  0:   5            and   15,                 5 ≥ 15   false  ✓",
            ]),
            ("p", "Both routes are correct and both give `x ≤ −2`. Route A never divides "
                  "by a negative, because collecting the variable on the side where its "
                  "coefficient is larger leaves that coefficient positive. What route A "
                  "asks instead is that you read `−2 ≥ x` correctly: turning a statement "
                  "round left-to-right reverses the relation, exactly as multiplying by "
                  "`−1` does."),
            ("example", ("The two degenerate cases",
                         "`2x + 1 &gt; 2x` reduces to `1 &gt; 0`, which is true whatever "
                         "`x` is: every real number is a solution. `2x + 1 &lt; 2x` "
                         "reduces to `1 &lt; 0`, which is false whatever `x` is: no number "
                         "is a solution. These are lesson 6's identity and contradiction "
                         "with a relation in place of the equals sign, and they are read "
                         "the same way.")),
        ],
        "lab": ("inequality", {
            "mode": "linear",
            "panel_title": "One inequality, solved and drawn",
            "panel_intro": "The trace names every operation and gives the reversal its own "
                           "row with its reason, and the table underneath tests sample "
                           "numbers against the statement you typed. Start with "
                           "`-2x &gt; 6`, then change the `-2` to `2` and watch the "
                           "reversal row disappear.",
        }),
        "steps_title": "Solving a linear inequality",
        "steps_intro": "Steps 1 to 3 are lesson 3 unchanged. Step 4 is what the relation adds.",
        "steps": [
            ("Clear brackets and fractions exactly as for an equation",
             "Multiplying every term by a positive common denominator is safe and leaves "
             "the relation alone. A negative common denominator would reverse it, so "
             "choose a positive one and the question never arises."),
            ("Collect the variable on the side that leaves its coefficient positive",
             "Compare the two coefficients and move the smaller one across. This is "
             "optional, and it removes the reversal step entirely, which is worth the two "
             "seconds of thought it costs."),
            ("Divide by the coefficient, and reverse if and only if that coefficient is negative",
             "Adding and subtracting never reverse. Dividing by a positive never reverses. "
             "Only a negative multiplier or divisor does, and when it does, it always "
             "does."),
            ("Test one number from inside your answer and one from outside, in the original statement",
             "A reversed sign is invisible in the algebra and obvious in the test. The "
             "inside number must make the original statement true and the outside number "
             "must make it false; testing only inside numbers cannot detect an answer "
             "that is too large."),
        ],
        "worked": {
            "title": "Fractions first, then the sign",
            "intro": ["`(1/2)x + 1 ≤ (1/3)x`. The least common denominator of `2` and `3` "
                      "is `6`, and `6` is positive, so clearing it changes nothing about "
                      "the relation."],
            "lines": [
                "(1/2)x + 1  ≤  (1/3)x",
                "",
                "multiply by 6      3x + 6  ≤  2x        6 > 0, so the sign stands",
                "subtract 2x         x + 6  ≤  0",
                "subtract 6              x  ≤  -6",
                "",
                "solution set   x ≤ -6",
                "",
                "test  x =  -6    (1/2)(-6) + 1 = -2     (1/3)(-6) = -2     -2 ≤ -2   ✓",
                "test  x = -12    (1/2)(-12) + 1 = -5    (1/3)(-12) = -4    -5 ≤ -4   ✓",
                "test  x =   0    (1/2)(0) + 1 = 1       (1/3)(0) = 0        1 ≤ 0    false  ✓",
            ],
            "after": [
                "Three tests, not one. `x = −6` is the boundary and confirms that `≤` "
                "rather than `&lt;` is right. `x = −12` is inside the answer and must "
                "work. `x = 0` is outside it and must fail; without that third test an "
                "answer that is too large looks exactly like a correct one.",
                "Multiply the original statement through by `−1` and it becomes "
                "`−(1/2)x − 1 ≥ −(1/3)x`, with the relation turned round. Clearing that "
                "one by multiplying by `−6` turns the relation round a second time and "
                "returns `3x + 6 ≤ 2x`. Two reversals cancel, which is a useful thing to "
                "have seen once.",
            ],
        },
        "quiz_title": "Sign and set",
        "quiz": [
            {"q": "Solve `−3x ≥ 12`.",
             "a": ["`x ≤ −4`", "`x ≥ −4`", "`x ≤ 4`", "`x ≥ 4`"],
             "c": 0,
             "why": "Dividing by `−3` reverses `≥` to `≤`, giving `x ≤ −4`. The second "
                    "option is what you get by not reversing; the last two divide by `3` "
                    "and lose the minus sign. At `x = −5`, `−3(−5) = 15 ≥ 12`, and at "
                    "`x = 0` the statement is false."},
            {"q": "Solve `4 − x &lt; 9`.",
             "a": ["`x &gt; −5`", "`x &lt; −5`", "`x &lt; 5`", "`x &gt; 5`"],
             "c": 0,
             "why": "Subtract 4 to get `−x &lt; 5`, then multiply by `−1` and reverse: "
                    "`x &gt; −5`. The second option forgets the reversal; the last two "
                    "lose the minus sign on the `5` as well, one of them reversing and one "
                    "not. At `x = 0` the "
                    "original reads `4 &lt; 9`, true, and `0 &gt; −5`; at `x = −6` it "
                    "reads `10 &lt; 9`, false."},
            {"q": "Which one of these operations forces the relation to reverse?",
             "a": ["Subtracting `7` from both sides", "Multiplying both sides by `−1/3`",
                   "Multiplying both sides by `6`", "Adding `2x` to both sides"],
             "c": 1,
             "why": "Only multiplication or division by a negative number reverses, and "
                    "`−1/3` is negative. Adding or subtracting never does, whether the "
                    "thing added is a number or an expression in `x`, and multiplying by "
                    "the positive number `6` does not either."},
        ],
        "mistakes": [
            ("Reversing because a minus sign appeared somewhere",
             "`x + 5 &lt; 2` becomes `x &lt; −3`, and nothing reverses: the operation was "
             "subtracting 5. The rule is about the sign of what you multiply or divide "
             "<em>by</em>, not about whether a negative number is on the page."),
            ("Dividing by an expression containing the variable",
             "From `3x &gt; 5x`, dividing by `x` gives `3 &gt; 5` and the false conclusion "
             "that there are no solutions. The truth is `x &lt; 0`: at `x = −1` the two "
             "sides are `−3` and `−5`, and `−3 &gt; −5`. You never know the sign of `x`, "
             "so you may never divide by it."),
            ("Turning a statement round without turning the relation round",
             "`−2 ≥ x` and `x ≥ −2` are different statements with different solution sets. "
             "`−2 ≥ x` says `x ≤ −2`. Swapping the two sides of an inequality reverses the "
             "relation, for the same reason multiplying by `−1` does."),
        ],
        "standard": ("Finish when you can say, before you divide, whether the sign will reverse.",
                     "For any linear inequality you should reach the solution set and be "
                     "able to point at the single step that reversed it, or state that no "
                     "step did. Then test one number from each side of the boundary "
                     "against the original statement, not against a line halfway down "
                     "your working."),
        "note": "The answer above was written `x ≤ −6`. Lesson 13 writes the same set as "
                "`(−∞, −6]` and as `{ x ∈ ℝ : x ≤ −6 }`, and all three say the same thing. "
                "The next three lessons produce solution sets in two pieces, which is "
                "where those notations stop being optional.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "compound-inequalities",
        "title": "Compound Inequalities",
        "module": "Inequalities",
        "one_line": "And and or, intersection and union.",
        "summary": (
            "Two inequalities joined by a word. <em>And</em> keeps the numbers satisfying "
            "both, which is the intersection of the two solution sets; <em>or</em> keeps "
            "the numbers satisfying at least one, which is the union. Everything else is "
            "lesson 9 done twice."
        ),
        "key": [
            "A and B      both true         intersection    ∩",
            "A or  B      at least one      union           ∪",
            "a < x < b    means  a < x  AND  x < b          never an or",
            "x < 4 or x > 1   is every real number",
        ],
        "key_label": "Two connectors, two set operations",
        "concepts_intro": (
            "The solving is lesson 9. The lesson is what the connecting word does to two "
            "answers once you have them."
        ),
        "concepts": [
            ("And is intersection",
             "`x ≥ 2 and x &lt; 4` is true at exactly the numbers lying in both solution "
             "sets. Solve the two statements separately, then keep the overlap. That "
             "overlap can be an interval, one of the two sets entire, a single number, or "
             "nothing at all."),
            ("Or is inclusive",
             "`A or B` is true when `A` holds, when `B` holds, and when both hold. "
             "Mathematical <em>or</em> is never exclusive, and that is why "
             "`x &lt; 4 or x &gt; 1` is every real number rather than the numbers outside "
             "the overlap."),
            ("The three-part form always means and",
             "`3 &lt; 2x + 1 ≤ 9` is a compact way of writing two statements that hold "
             "together. There is no corresponding compact form for <em>or</em>, and "
             "inventing one produces a statement describing nothing at all."),
        ],
        "read_title": "Both, or at least one",
        "read_intro": "Solving two inequalities at once, combining the two answers, and the shapes the combination can take.",
        "body": [
            ("def", ("Compound inequality",
                     "A <strong>compound inequality</strong> is two inequalities joined by "
                     "<em>and</em> or by <em>or</em>. Its solution set is the "
                     "<strong>intersection</strong> of the two solution sets when the "
                     "connector is <em>and</em>, and their <strong>union</strong> when the "
                     "connector is <em>or</em>.",
                     "`∩` denotes intersection, the numbers lying in both sets. `∪` "
                     "denotes union, the numbers lying in at least one.")),
            ("p", "The method is the definition. Solve each inequality on its own by "
                  "lesson 9, draw both solution sets against the same number line, and "
                  "read off the overlap or the combination. Almost every error in this "
                  "lesson is an error made before the drawing or instead of it."),
            ("h3", "The three-part form"),
            ("p", "When both statements trap the variable between two numbers they are "
                  "usually written as one. `3 &lt; 2x + 1 ≤ 9` means `3 &lt; 2x + 1` and "
                  "`2x + 1 ≤ 9`. It is solved by operating on all three parts at once."),
            ("math", [
                "3  <  2x + 1  ≤  9",
                "",
                "subtract 1      2  <  2x  ≤  8",
                "divide by 2     1  <   x  ≤  4",
                "",
                "check   x = 2    2(2) + 1 = 5      3 < 5 ≤ 9     ✓",
                "        x = 1    2(1) + 1 = 3      3 < 3         false  ✓",
                "        x = 4    2(4) + 1 = 9          9 ≤ 9     ✓",
            ]),
            ("p", "Every operation applies to all three parts, because each of the two "
                  "statements the compact form stands for needs it. Operating on two "
                  "parts and forgetting the third breaks the equivalence, and there is "
                  "nothing on the page to warn you."),
            ("p", "The compact form is usable only when the connector is <em>and</em> and "
                  "the variable sits alone in the middle. `x &lt; −2 or x ≥ 3` cannot be "
                  "compressed: writing `3 ≤ x &lt; −2` asks for a number that is at once "
                  "at least 3 and below −2, and there is none. The compact form for that "
                  "solution set is `(−∞, −2) ∪ [3, ∞)`, and lesson 13 is about it."),
            ("h3", "The four shapes an intersection can take"),
            ("ul", [
                "<strong>An interval.</strong> `x ≥ 2 and x &lt; 4` gives the numbers from "
                "2 up to but not including 4.",
                "<strong>One of the two, entire.</strong> `x &gt; 1 and x &gt; 5` gives "
                "`x &gt; 5`. The stronger condition already implies the weaker one, so the "
                "weaker one adds nothing.",
                "<strong>A single number.</strong> `x ≥ 3 and x ≤ 3` is true only at "
                "`x = 3`.",
                "<strong>Nothing.</strong> `x &gt; 5 and x &lt; 2` has no solutions. The "
                "empty set is a legitimate answer and is written `∅`.",
            ]),
            ("h3", "The three shapes a union can take"),
            ("ul", [
                "<strong>Two separated pieces.</strong> `x &lt; −2 or x ≥ 3`. Most "
                "absolute-value inequalities land here, which is what lesson 12 is about.",
                "<strong>One piece.</strong> `x &lt; 4 or x &lt; 1` is `x &lt; 4`, because "
                "everything in the second set is already in the first.",
                "<strong>Every real number.</strong> `x &lt; 4 or x &gt; 1`. Take any "
                "number: if it is below 4 the first statement holds, and if it is not "
                "below 4 then it is at least 4, so it is above 1 and the second holds. "
                "Nothing is left out.",
            ]),
            ("example", ("Two statements, both connectors",
                         "`2x + 1 ≥ 5` solves to `x ≥ 2`, and `x − 4 &lt; 0` solves to "
                         "`x &lt; 4`. Joined by <em>and</em> the answer is "
                         "`2 ≤ x &lt; 4`. Joined by <em>or</em> the answer is every real "
                         "number, because a number below 2 satisfies the second and a "
                         "number at or above 2 satisfies the first. Same two statements; "
                         "the connector alone decides.")),
        ],
        "lab": ("inequality", {
            "mode": "compound",
            "panel_title": "Two statements, three number lines",
            "panel_intro": "The lab draws each solution set and then the combination, so "
                           "the overlap is something you see rather than something you "
                           "are told. Solve one pair with `and`, then switch the connector "
                           "to `or` and change nothing else.",
        }),
        "steps_title": "Solving a compound inequality",
        "steps_intro": "The two halves are solved independently. The connector is applied once, at the end, to the two answers.",
        "steps": [
            ("Write down which two statements you have",
             "A three-part statement `a &lt; f(x) &lt; b` is two statements. You may keep "
             "it compact and operate on all three parts at once, but you must know which "
             "two statements those parts stand for."),
            ("Solve each one on its own, by lesson 9",
             "Each half gets its own reversal check. A negative coefficient in one half "
             "says nothing whatever about the other, and the two halves may well need "
             "different treatment."),
            ("Draw both solution sets against one number line",
             "Two marked regions above the same axis. Filled endpoints for `≤` and `≥`, "
             "hollow for `&lt;` and `&gt;`. This is the step that turns the combination "
             "into something you read off instead of something you reason about."),
            ("Take the overlap for and, everything covered for or, then check the endpoints",
             "For an <em>and</em>, an endpoint belongs only if the statement that "
             "produced it includes it. For an <em>or</em>, test it against both "
             "statements, because the other one may cover it even when its own does not. "
             "Then test a number from each region against the original pair."),
        ],
        "worked": {
            "title": "The same pair, joined two ways",
            "intro": ["`2x + 1 ≥ 5` and `x − 4 &lt; 0`, then the identical two statements "
                      "joined by <em>or</em>."],
            "lines": [
                "first      2x + 1  ≥  5           second      x - 4  <  0",
                "           2x      ≥  4                       x      <  4",
                "            x      ≥  2",
                "",
                "sets       A = { x : x ≥ 2 }      B = { x : x < 4 }",
                "",
                "A and B    the numbers in both            2 ≤ x < 4",
                "A or  B    the numbers in at least one    every real number",
                "",
                "check the and answer",
                "   x = 2     2(2) + 1 = 5 ≥ 5  true     2 - 4 = -2 < 0  true      in",
                "   x = 4     2(4) + 1 = 9 ≥ 5  true     4 - 4 =  0 < 0  FALSE     out",
                "   x = 1     2(1) + 1 = 3 ≥ 5  FALSE    1 - 4 = -3 < 0  true      out",
                "",
                "check the or answer",
                "   x = 0     first FALSE                second true               in",
                "   x = 9     first true                 second FALSE              in",
            ],
            "after": [
                "In the <em>and</em> answer the two endpoints behave differently, and "
                "each is settled by the statement it came from. `2` came from `x ≥ 2`, "
                "which includes it, so `2` is in. `4` came from `x &lt; 4`, which excludes "
                "it, so `4` is out. In the <em>or</em> answer `4` is back in, because "
                "`4 ≥ 2` makes the first statement true there: an endpoint is settled by "
                "the statement that produced it only when it is an endpoint of the "
                "combined set.",
                "The <em>or</em> answer is worth dwelling on. Every real number is either "
                "less than 2 or at least 2. If it is less than 2 it is certainly less "
                "than 4, so the second statement holds; if it is at least 2, the first "
                "holds. Nothing is left out, and the union is the whole line even though "
                "neither statement is true everywhere on its own.",
            ],
        },
        "quiz_title": "And, or, and what is left",
        "quiz": [
            {"q": "Solve `−1 ≤ 3x + 2 &lt; 11`.",
             "a": ["`−1 ≤ x &lt; 3`", "`−3 ≤ x &lt; 9`", "`−1 &lt; x ≤ 3`", "`x ≥ −1`"],
             "c": 0,
             "why": "Subtract 2 from all three parts to get `−3 ≤ 3x &lt; 9`, then divide "
                    "all three by 3. The second option stops after the subtraction, the "
                    "third moves the strictness to the wrong end, and the fourth keeps "
                    "only the left half of the statement."},
            {"q": "Which numbers satisfy `x &lt; 4 or x &gt; 1`?",
             "a": ["Every real number", "Only the numbers strictly between 1 and 4",
                   "No numbers at all", "Every number except those between 1 and 4"],
             "c": 0,
             "why": "Any number below 4 satisfies the first statement, and any number not "
                    "below 4 is at least 4 and so satisfies the second. The numbers "
                    "between 1 and 4 satisfy both, and <em>or</em> keeps them &mdash; "
                    "which is what the fourth option gets backwards."},
            {"q": "What is the solution set of `x ≥ 3 and x ≤ 3`?",
             "a": ["Every real number", "No numbers at all", "Exactly one number, `x = 3`",
                   "Every number except `3`"],
             "c": 2,
             "why": "The two sets overlap at the single point 3, and both relations include "
                    "their endpoint. Change either `≤` or `≥` to a strict relation and the "
                    "intersection becomes empty, which is the sharpest demonstration of "
                    "what the strictness does."},
        ],
        "mistakes": [
            ("Writing an or as a three-part statement",
             "`x &lt; −2 or x ≥ 3` is not `3 ≤ x &lt; −2`. The three-part form always "
             "means <em>and</em>, so that line asks for numbers at once at least 3 and "
             "below −2. A solution set with two infinite pieces has been written down as "
             "the empty set."),
            ("Operating on two of the three parts",
             "In `3 &lt; 2x + 1 ≤ 9`, subtracting 1 gives `2 &lt; 2x ≤ 8` &mdash; every "
             "part changes. The compact form stands for two statements, and both of them "
             "need the subtraction if the result is to be equivalent."),
            ("Reading or as exclusive",
             "In `x &lt; 4 or x &gt; 1` the numbers between 1 and 4 satisfy both "
             "statements, and mathematical <em>or</em> keeps them. The solution set is "
             "every real number, not the numbers outside the overlap and not the overlap "
             "itself."),
        ],
        "standard": ("Finish when you can predict the shape of the answer before you combine.",
                     "Given two solved inequalities you should be able to say from the "
                     "picture whether an <em>and</em> will give an interval, a single "
                     "point or nothing, and whether an <em>or</em> will give two pieces, "
                     "one piece or the whole line &mdash; and then settle each endpoint "
                     "by testing it against both statements."),
        "note": "The connector decides everything here, and the next two lessons supply "
                "it automatically: `|X| &lt; k` produces an <em>and</em> and "
                "`|X| &gt; k` produces an <em>or</em>. That is the reason absolute value "
                "is treated after this lesson rather than before it.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "absolute-value-equations",
        "title": "Absolute Value Equations",
        "module": "Absolute value",
        "one_line": "Two cases, and when there are none.",
        "summary": (
            "`|X| = k` says the expression `X` sits at distance `k` from zero, and for a "
            "positive `k` there are exactly two places it can be. That is the whole "
            "method: isolate the bars, split into two equations, and substitute every "
            "candidate back into the original."
        ),
        "key": [
            "|X| = k,  k > 0    ⟹   X = k   or   X = -k      two equations",
            "|X| = 0            ⟹   X = 0                    one solution",
            "|X| = k,  k < 0        no solution",
            "|X| = an expression in x    split, then CHECK every candidate",
        ],
        "key_label": "One equation, and the number of solutions it has",
        "concepts_intro": (
            "Everything follows from one reading of the bars, and one discipline about "
            "when the rule may be applied."
        ),
        "concepts": [
            ("Absolute value is a distance",
             "`|X|` is how far `X` lies from zero, with no direction attached. Course 1 "
             "defined it in two cases; here the distance reading is the useful one, "
             "because `|X| = 5` then says that `X` is 5 away from 0, and there are "
             "exactly two such places."),
            ("Two cases means two equations, joined by or",
             "`|x − 3| = 5` becomes `x − 3 = 5` or `x − 3 = −5`. Both get solved and both "
             "answers count. This is not a choice between two possibilities; it is two "
             "equations whose solution sets are combined."),
            ("The bars must be alone before you split",
             "The rule is stated for `|X| = k`, not for `3|X| + 2 = k`. Isolating the "
             "absolute value is a step of the method, not a tidying-up, and splitting "
             "early produces numbers that fail the check."),
        ],
        "read_title": "Distance, and the two places it can be",
        "read_intro": "The two-case rule, where it comes from, and the situations in which the number of solutions is not two.",
        "body": [
            ("def", ("Absolute value",
                     "`|a|` is the distance from `a` to `0` on the number line. In cases, "
                     "`|a| = a` when `a ≥ 0`, and `|a| = −a` when `a &lt; 0`.",
                     "The second case is easy to misread. `−a` is not a negative number "
                     "when `a` is itself negative: `|−4| = −(−4) = 4`. The minus sign "
                     "there reverses a sign; it does not impose one.")),
            ("thm", ("The two-case rule",
                     "For `k &gt; 0`, the equation `|X| = k` is true exactly when `X = k` "
                     "or `X = −k`.",
                     "For `k = 0` it is true exactly when `X = 0`, a single case. For "
                     "`k &lt; 0` it is never true, because a distance is never negative.")),
            ("p", "Read the theorem on the number line. The numbers at distance 5 from 0 "
                  "are `5` and `−5`, and there are no others. `X` may be any expression "
                  "&mdash; `x − 3`, `2x + 1`, anything at all &mdash; and the rule applies "
                  "to the whole of what the bars enclose, not to `x`."),
            ("h3", "Isolating the bars first"),
            ("math", [
                "3|x - 1| + 2  =  14",
                "",
                "subtract 2        3|x - 1|  =  12",
                "divide by 3        |x - 1|  =   4      the bars are now alone",
                "",
                "split         x - 1 = 4       or       x - 1 = -4",
                "                  x = 5       or           x = -3",
                "",
                "check   x =  5:   3|5 - 1| + 2  = 3(4) + 2 = 14    ✓",
                "        x = -3:   3|-3 - 1| + 2 = 3(4) + 2 = 14    ✓",
            ]),
            ("p", "Both candidates survive, and both belong in the answer: the solution "
                  "set is `{ 5, −3 }`. Reporting one of them is not a smaller answer, it "
                  "is a wrong one, because the question asked which numbers make the "
                  "statement true and two of them do."),
            ("h3", "When the count is not two"),
            ("ul", [
                "`|2x + 1| = 0`. A distance of zero happens in one place only, so "
                "`2x + 1 = 0` and `x = −1/2`. One solution.",
                "`|x + 4| = −2`. No number sits at distance `−2` from anything. There are "
                "no solutions, and saying so is the complete answer.",
                "`|x − 3| = |2x + 1|`. Two absolute values are equal when the expressions "
                "are equal or opposite: `x − 3 = 2x + 1` or `x − 3 = −(2x + 1)`, giving "
                "`x = −4` and `x = 2/3`. Both check.",
            ]),
            ("p", "The middle case repays a closer look. Splitting `|x + 4| = −2` "
                  "mechanically gives `x + 4 = −2` and `x + 4 = 2`, so `x = −6` and "
                  "`x = −2`. Substituting: `|−6 + 4| = 2` and `|−2 + 4| = 2`, and neither "
                  "equals `−2`. The split produced two numbers and neither is a solution, "
                  "which is exactly what the check exists to discover."),
            ("h3", "A variable on the right"),
            ("p", "When the right side contains `x`, its sign is not known in advance, and "
                  "the theorem &mdash; stated for a positive `k` &mdash; carries no "
                  "guarantee that the two cases will deliver solutions. Split anyway, then "
                  "substitute every candidate into the original equation. Here the check "
                  "is not a safeguard; it is part of the method."),
            ("example", ("Both candidates survive",
                         "`|2x − 1| = x + 3`. Case one: `2x − 1 = x + 3`, so `x = 4`; then "
                         "the left side is `|7| = 7` and the right side is `4 + 3 = 7`. "
                         "Case two: `2x − 1 = −(x + 3) = −x − 3`, so `3x = −2` and "
                         "`x = −2/3`; then the left side is `|−7/3| = 7/3` and the right "
                         "side is `−2/3 + 3 = 7/3`. Both check, and the solution set has "
                         "two members.")),
            ("p", "A candidate thrown out by the check is called <strong>extraneous</strong>. "
                  "It is not the mark of an arithmetic slip: the splitting step can produce "
                  "equations with solutions the original never had, and only substitution "
                  "finds out which. The same phenomenon returns in course 5, when both "
                  "sides of an equation get squared."),
        ],
        "lab": ("equation", {
            "mode": "absolute",
            "panel_title": "Two cases, and a check that can throw one out",
            "panel_intro": "The lab runs both cases and substitutes each candidate back "
                           "into the equation as you typed it, marking the survivors in "
                           "green and the rejects in red. Put `x - 5` on the right and "
                           "watch both candidates fail.",
        }),
        "steps_title": "Solving an absolute value equation",
        "steps_intro": "Step 1 comes before everything else, and step 4 is not a formality.",
        "steps": [
            ("Isolate the absolute value",
             "Reach `|X| = (something)` with nothing multiplying the bars and nothing "
             "added to them. Until that is done there is no rule available to apply, and "
             "applying one anyway is the commonest way to get this topic wrong."),
            ("Look at the right side before you split",
             "A negative number: no solutions, and you are finished. Zero: one case, "
             "`X = 0`. A positive number: two cases. An expression containing `x`: split, "
             "and rely on step 4 to sort the candidates out."),
            ("Write the two equations and solve each by lessons 2 and 3",
             "`X = k` and `X = −k`. Write the second with a bracket &mdash; `X = −(k)` "
             "&mdash; so that a right side with several terms gets every one of its signs "
             "flipped."),
            ("Substitute every candidate into the ORIGINAL equation",
             "Not into a line halfway down your working, which has already had the bars "
             "removed. The splitting step is where extraneous values enter, and only the "
             "original statement can reject them."),
        ],
        "worked": {
            "title": "Two cases, both thrown out",
            "intro": ["`|2x − 1| = x − 5`. The right side contains `x`, so the check is "
                      "what decides the answer."],
            "lines": [
                "case 1     2x - 1  =  x - 5",
                "                x  =  -4",
                "",
                "case 2     2x - 1  =  -(x - 5)  =  -x + 5",
                "               3x  =  6",
                "                x  =  2",
                "",
                "check  x = -4     left   |2(-4) - 1|  =  |-9|  =  9",
                "                  right    (-4) - 5   =  -9",
                "                  9 = -9 ?   no                 REJECT",
                "",
                "check  x =  2     left   |2(2) - 1|   =  |3|   =  3",
                "                  right     2 - 5     =  -3",
                "                  3 = -3 ?   no                 REJECT",
                "",
                "solution set   empty",
            ],
            "after": [
                "Both candidates fail and the equation has no solutions. That is a "
                "complete answer, not an unfinished one, and writing <em>no solutions</em> "
                "is the correct final line.",
                "The failure was predictable. `|2x − 1|` is never negative, so any "
                "solution would need `x − 5 ≥ 0`, that is `x ≥ 5`. Both candidates are "
                "below 5, so neither could have worked. Checking the sign of the right "
                "side first would have saved two substitutions &mdash; but it is the "
                "substitutions that establish the rejection, and the sign argument only "
                "predicts it.",
                "Change the right side to `x + 3` and the same two cases produce `x = 4` "
                "and `x = −2/3`, and both survive. The algebra of the split is identical; "
                "everything that differs is in the check.",
            ],
        },
        "quiz_title": "Cases and candidates",
        "quiz": [
            {"q": "Solve `|x − 3| = 5`.",
             "a": ["`x = 8` or `x = −2`", "`x = 8` only", "`x = 8` or `x = −8`",
                   "`x = 2` or `x = −8`"],
             "c": 0,
             "why": "`x − 3 = 5` gives `x = 8`, and `x − 3 = −5` gives `x = −2`. The second "
                    "option keeps only the first case. The third negates the answer instead "
                    "of the expression inside the bars. The fourth subtracts the 3 in both "
                    "cases where it should be added."},
            {"q": "How many solutions does `|3x + 7| = −4` have?",
             "a": ["None", "One", "Two", "Infinitely many"],
             "c": 0,
             "why": "An absolute value is a distance and is never negative, so nothing can "
                    "make the left side `−4`. Splitting anyway produces `x = −11/3` and "
                    "`x = −1`, and substituting either gives a left side of `4`, not `−4`."},
            {"q": "What is the solution set of `|2x − 1| = x − 5`?",
             "a": ["`x = −4` and `x = 2`", "`x = 2` only", "`x = −4` only",
                   "There are no solutions"],
             "c": 3,
             "why": "Both cases produce a candidate and both candidates fail the "
                    "substitution: at `x = −4` the two sides are `9` and `−9`, and at "
                    "`x = 2` they are `3` and `−3`. A left side that is never negative "
                    "cannot equal `x − 5` unless `x ≥ 5`, and neither candidate is."},
        ],
        "mistakes": [
            ("Splitting before the bars are alone",
             "`|x| + 3 = 7` is not `x + 3 = 7 or x + 3 = −7`. That gives `x = 4` and "
             "`x = −10`, and `|−10| + 3 = 13`. Isolate first: `|x| = 4`, so `x = 4` or "
             "`x = −4`. The two cases apply to what the bars enclose, never to a whole "
             "side of the equation."),
            ("Reporting one case",
             "`|x − 3| = 5` has two solutions. Producing `x = 8` and stopping there is "
             "half an answer, and it is the most common way to lose a question you "
             "understood completely."),
            ("Trusting the split when the right side is not a positive number",
             "The theorem was stated for `k &gt; 0`. When the right side is negative or "
             "contains `x`, the split still produces candidates, and some or all of them "
             "may be extraneous. Only substitution into the original equation says which."),
        ],
        "standard": ("Finish when the substitution is part of the method rather than a habit.",
                     "You should isolate the bars, read the right side and say how many "
                     "cases there are, solve them, and substitute every candidate into the "
                     "original equation &mdash; and be willing to write <em>no "
                     "solutions</em> as a final answer when both candidates fail."),
        "note": "The same distance reading drives the next lesson. `|X| = 5` picks out two "
                "points; `|X| &lt; 5` picks out everything between them and `|X| &gt; 5` "
                "everything outside them, which is where lesson 10's <em>and</em> and "
                "<em>or</em> come from.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "absolute-value-inequalities",
        "title": "Absolute Value Inequalities",
        "module": "Absolute value",
        "one_line": "Less-than gives an interval, greater-than gives two.",
        "summary": (
            "`|X| &lt; k` says `X` is within `k` of zero, which is one interval and an "
            "<em>and</em>. `|X| &gt; k` says `X` is further than `k` from zero, which is "
            "two rays and an <em>or</em>. The connector is not a convention to memorise; "
            "it is what the distance reading gives."
        ),
        "key": [
            "|X| < k,  k > 0   ⟺   -k < X < k             one interval   (and)",
            "|X| > k,  k > 0   ⟺   X < -k  or  X > k      two rays       (or)",
            "|X| < a negative number       no solutions",
            "|X| > a negative number       every real number",
        ],
        "key_label": "A band, or everything outside one",
        "concepts_intro": (
            "Two rules, one picture they both come from, and a set of right-hand sides "
            "that settle the question before any splitting."
        ),
        "concepts": [
            ("Within k of zero, or beyond k from zero",
             "`|X| &lt; 5` says the distance from `X` to `0` is under 5, so `X` lies "
             "between `−5` and `5`. `|X| &gt; 5` says the distance is over 5, so `X` lies "
             "outside that band. The two solution sets are complementary except at the "
             "two boundary points, where the distance is exactly 5 and neither strict "
             "statement holds."),
            ("The connector follows from the picture",
             "A band is one region described by two conditions holding together: an "
             "<em>and</em>. Two rays are separate regions, and a number in either one "
             "qualifies: an <em>or</em>. Deriving the connector from the picture takes a "
             "second and is safer than recalling which word goes with which relation."),
            ("The degenerate right sides are settled without splitting",
             "A distance is never negative and can be zero. `|X| &lt; −1` has no "
             "solutions, `|X| &gt; −1` has every real number, and `|X| ≤ 0` holds only "
             "where `X = 0`. None of these needs a case split, and none of them is a "
             "special rule &mdash; each is read off what an absolute value is."),
        ],
        "read_title": "A band, or everything outside one",
        "read_intro": "The two rules, the picture each comes from, and the right-hand sides that end the question before it starts.",
        "body": [
            ("thm", ("The less-than rule",
                     "For `k &gt; 0`, `|X| &lt; k` is true exactly when "
                     "`−k &lt; X &lt; k`.",
                     "With `≤` throughout: `|X| ≤ k` is true exactly when "
                     "`−k ≤ X ≤ k`. The three-part form is legitimate here because the "
                     "connector genuinely is <em>and</em>.")),
            ("thm", ("The greater-than rule",
                     "For `k &gt; 0`, `|X| &gt; k` is true exactly when `X &lt; −k` or "
                     "`X &gt; k`.",
                     "With `≥`: `X ≤ −k` or `X ≥ k`. There is no three-part form for this "
                     "one, and writing one is the standard error of the topic.")),
            ("p", "Both are read straight off the number line. The numbers less than 5 "
                  "away from 0 are those strictly between `−5` and `5`; the numbers more "
                  "than 5 away are those below `−5` together with those above `5`. `X` may "
                  "be any expression, and the rule applies to the whole of what the bars "
                  "enclose."),
            ("h3", "A worked band"),
            ("math", [
                "|x - 2|  <  5",
                "",
                "                 -5  <  x - 2  <  5",
                "add 2            -3  <    x    <  7",
                "",
                "test  x =  0    |0 - 2|  = 2 < 5   ✓        -3 < 0 < 7    ✓",
                "test  x =  7    |7 - 2|  = 5 < 5   false    7 < 7 false   ✓",
                "test  x = -4    |-4 - 2| = 6 < 5   false    -3 < -4 false ✓",
            ]),
            ("p", "Turn the relation round and the same two numbers reappear on the "
                  "outside. `|x − 2| &gt; 5` gives `x − 2 &lt; −5` or `x − 2 &gt; 5`, that "
                  "is `x &lt; −3` or `x &gt; 7`. The two solution sets do not overlap and "
                  "do not quite cover the line: at `x = −3` and at `x = 7` the distance is "
                  "exactly 5, so both strict statements fail."),
            ("h3", "Isolating the bars first"),
            ("math", [
                "2|x - 1| + 5  >  11",
                "",
                "subtract 5        2|x - 1|  >  6",
                "divide by 2        |x - 1|  >  3      the bars are now alone",
                "",
                "split        x - 1 < -3     or     x - 1 > 3",
                "                 x < -2     or         x > 4",
                "",
                "test  x = 5     2|5 - 1| + 5 = 2(4) + 5 = 13  > 11   ✓",
                "test  x = 0     2|0 - 1| + 5 = 2(1) + 5 =  7  > 11   false  ✓",
            ]),
            ("p", "The divisor there was `2`, a positive number, so the relation stood. "
                  "Had the statement been `−2|x − 1| &gt; −6`, dividing by `−2` would "
                  "reverse it to `|x − 1| &lt; 3` &mdash; a band rather than two rays, and "
                  "a different answer entirely. Lesson 9's rule applies to the step that "
                  "isolates the bars, before any case split exists."),
            ("h3", "Right-hand sides that end the question"),
            ("ul", [
                "`|2x + 1| ≤ 0`. A distance is never negative, so the only possibility is "
                "`2x + 1 = 0`, giving `x = −1/2`. The solution set has one member.",
                "`|x + 3| &lt; −1`. Nothing at all. The solution set is `∅`.",
                "`|x + 3| &gt; −1`. Everything. Every absolute value is at least `0`, and "
                "`0 &gt; −1`.",
                "`|2x + 1| &gt; 0`. Every number except the one where the inside is zero: "
                "all `x` other than `x = −1/2`.",
            ]),
            ("p", "None of these four needs a split, and none of them is a rule to "
                  "memorise. Each is read off the two facts that an absolute value is "
                  "never negative and is zero only where the inside is zero. The two "
                  "theorems above were stated for `k &gt; 0`, and reading the right-hand "
                  "side first is how you stay inside the range they were stated for."),
            ("example", ("The band and its outside",
                         "`|x − 2| &lt; 5` gives `−3 &lt; x &lt; 7`, and `|x − 2| &gt; 5` "
                         "gives `x &lt; −3` or `x &gt; 7`. Between them they account for "
                         "every real number except `−3` and `7`. Replace both relations by "
                         "`≤` and `≥` and the two answers instead overlap at exactly those "
                         "two points, which is where the distance is exactly 5.")),
        ],
        "lab": ("inequality", {
            "mode": "absolute",
            "panel_title": "The band and the two rays, drawn",
            "panel_intro": "The lab plots the absolute value against the constant, shades "
                           "where the statement holds, and draws the solution set on the "
                           "number line. Run the two presets with a negative right-hand "
                           "side before you trust the two-case rule anywhere.",
        }),
        "steps_title": "Solving an absolute value inequality",
        "steps_intro": "The first two steps decide which rule you are about to use, or whether you need one at all.",
        "steps": [
            ("Isolate the absolute value",
             "Reach `|X| &lt; k` or `|X| &gt; k` with the bars alone on one side. Any "
             "multiplication or division you perform here obeys lesson 9: a negative "
             "multiplier reverses the relation, and it does so before any case split "
             "exists."),
            ("Look at the right side",
             "Negative with `&lt;` or `≤`: no solutions. Negative with `&gt;` or `≥`: "
             "every real number. Zero: `|X| ≤ 0` means `X = 0`, and `|X| &gt; 0` means "
             "everywhere except where `X = 0`. Positive: go on to step 3."),
            ("Write the band for less-than and the two rays for greater-than",
             "`|X| &lt; k` becomes `−k &lt; X &lt; k`, one statement, connector "
             "<em>and</em>. `|X| &gt; k` becomes `X &lt; −k` or `X &gt; k`, two "
             "statements, connector <em>or</em>. Keep `≤` and `≥` if that is what you "
             "started with."),
            ("Solve each part by lesson 9, then test",
             "Each part is an ordinary linear inequality with its own reversal check. "
             "Finish by testing a number from inside the answer and one from outside "
             "against the original statement, with the bars still in it."),
        ],
        "worked": {
            "title": "A negative coefficient inside the bars",
            "intro": ["`|3 − 2x| ≥ 7`. The relation is a greater-than, so the connector is "
                      "<em>or</em>, and both cases divide by a negative number."],
            "lines": [
                "|3 - 2x|  ≥  7           right side is positive: two rays",
                "",
                "case 1      3 - 2x  ≤  -7          case 2      3 - 2x  ≥  7",
                "               -2x  ≤  -10                        -2x  ≥  4",
                "                 x  ≥  5                            x  ≤  -2",
                "         (divide by -2, REVERSE)          (divide by -2, REVERSE)",
                "",
                "solution set     x ≤ -2   or   x ≥ 5",
                "",
                "test  x = -2     |3 - 2(-2)| = |7|  = 7  ≥ 7   ✓        in",
                "test  x =  5     |3 - 2(5)|  = |-7| = 7  ≥ 7   ✓        in",
                "test  x =  6     |3 - 2(6)|  = |-9| = 9  ≥ 7   ✓        in",
                "test  x =  0     |3 - 2(0)|  = |3|  = 3  ≥ 7   false    out",
            ],
            "after": [
                "Two reversals, one in each case, and they have nothing to do with the "
                "<em>or</em> that joined the cases. The connector came from the `≥` "
                "outside the bars; the reversals came from the `−2` inside them. Mixing "
                "the two up is how this exercise usually goes wrong.",
                "Both boundary numbers are in the answer because the relation is `≥` "
                "rather than `&gt;`: at `x = −2` the inside is `7` and at `x = 5` it is "
                "`−7`, both of absolute value 7. Change the statement to "
                "`|3 − 2x| &gt; 7` and the answer becomes `x &lt; −2` or `x &gt; 5`, with "
                "the same two numbers now excluded.",
            ],
        },
        "quiz_title": "Bands and rays",
        "quiz": [
            {"q": "Solve `|x + 1| ≤ 4`.",
             "a": ["`−5 ≤ x ≤ 3`", "`−3 ≤ x ≤ 5`", "`x ≤ −5` or `x ≥ 3`", "`−4 ≤ x ≤ 4`"],
             "c": 0,
             "why": "A less-than gives a band: `−4 ≤ x + 1 ≤ 4`, then subtract 1 from all "
                    "three parts. The second option adds 1 instead of subtracting, the "
                    "third uses the greater-than rule, and the fourth never deals with the "
                    "`+ 1` at all."},
            {"q": "Solve `|2x − 6| &gt; 4`.",
             "a": ["`x &lt; 1` or `x &gt; 5`", "`1 &lt; x &lt; 5`", "`x &gt; 5`",
                   "`x &lt; −1` or `x &gt; 5`"],
             "c": 0,
             "why": "`2x − 6 &lt; −4` gives `x &lt; 1`, and `2x − 6 &gt; 4` gives "
                    "`x &gt; 5`. The second option applies the less-than rule, so every "
                    "number in it fails the statement &mdash; and so do the two endpoints "
                    "`1` and `5` that it leaves out. The third drops a case. The fourth "
                    "negates the answer of the first case instead of the right-hand side "
                    "of the split."},
            {"q": "What is the solution set of `|x − 4| &gt; −3`?",
             "a": ["Every real number", "No numbers at all", "`x &lt; 1` or `x &gt; 7`",
                   "`x = 4` only"],
             "c": 0,
             "why": "Every absolute value is at least `0`, and `0 &gt; −3`, so every `x` "
                    "works &mdash; including `x = 4`, where the left side is `0`. The "
                    "third option is what you get by treating the right side as `3`, and "
                    "the second is the answer to `|x − 4| &lt; −3`."},
        ],
        "mistakes": [
            ("Using or for a less-than",
             "`|x| &lt; 3` is `−3 &lt; x &lt; 3`, both conditions at once. Writing "
             "`x &lt; 3 or x &gt; −3` gives every real number, which is the answer to a "
             "different question. A band is an <em>and</em>."),
            ("Compressing a greater-than into a three-part form",
             "`|x| &gt; 3` is `x &lt; −3 or x &gt; 3`. Writing `3 &lt; x &lt; −3` asks "
             "for a number above 3 and below −3 at the same time, so a solution set with "
             "two infinite pieces has been written down as the empty set."),
            ("Splitting before the bars are alone",
             "`2|x − 1| + 5 &gt; 11` is not `2(x − 1) + 5 &gt; 11 or 2(x − 1) + 5 &lt; "
             "−11`, which gives `x &lt; −7 or x &gt; 4`. Reduce to `|x − 1| &gt; 3` "
             "first; the correct answer is `x &lt; −2 or x &gt; 4`, and `x = −5` is the "
             "number that tells the two apart."),
        ],
        "standard": ("Finish when you can name the connector before you split, and say why.",
                     "Given `|X| &lt; k` or `|X| &gt; k` you should produce <em>and</em> "
                     "or <em>or</em> from the distance reading rather than from memory, "
                     "handle a negative or zero right-hand side without splitting at all, "
                     "and test the answer against the statement with the bars still in "
                     "it."),
        "note": "Two of the answers in this lesson &mdash; `x ≤ −2 or x ≥ 5`, and every "
                "real number &mdash; are awkward to write in the notation used so far. The "
                "last lesson supplies interval and set-builder notation, in which they "
                "become `(−∞, −2] ∪ [5, ∞)` and `(−∞, ∞)`.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "interval-and-set-builder-notation",
        "title": "Interval and Set-Builder Notation",
        "module": "Inequalities",
        "one_line": "Writing a solution set so a reader knows exactly what it holds.",
        "summary": (
            "Two standard ways of writing a set of numbers down: interval notation, which "
            "names the two ends and says whether each is included, and set-builder "
            "notation, which states the condition a number must satisfy. Both are exact, "
            "and both have a small number of forms that describe nothing."
        ),
        "key": [
            "[a, b]     a ≤ x ≤ b        both ends included",
            "(a, b)     a < x < b        neither end included",
            "[a, ∞)     a ≤ x            ∞ is never included: never a square bracket",
            "{ x ∈ ℝ : x ≥ 2 }           set-builder: the condition, written out",
        ],
        "key_label": "Two notations for one set",
        "concepts_intro": (
            "The notation carries very little, and every part of it is load-bearing."
        ),
        "concepts": [
            ("The bracket is the whole content of the notation",
             "A square bracket includes the endpoint and a round one excludes it. `[2, 5)` "
             "contains 2 and does not contain 5. Mixing the two in one interval is "
             "ordinary rather than a mistake &mdash; it is exactly what <em>at least 2 and "
             "less than 5</em> says."),
            ("Infinity is a direction, not a number",
             "`∞` marks an end that never arrives. There is no number there to include, so "
             "the bracket beside it is always round: `[2, ∞)` and never `[2, ∞]`. The same "
             "holds for `−∞` at the left end."),
            ("Set-builder notation states a condition",
             "`{ x ∈ ℝ : x ≥ 2 }` reads <em>the set of real numbers `x` such that "
             "`x ≥ 2`</em>. It can express sets interval notation cannot &mdash; "
             "`{ x ∈ ℝ : x is rational }` for one, which is not a union of finitely "
             "many intervals &mdash; and it makes explicit which numbers are being "
             "drawn from."),
        ],
        "read_title": "Writing a solution set down",
        "read_intro": "Four ways to say the same thing, the pieces each notation is made of, and the handful of written forms that mean nothing.",
        "body": [
            ("p", "Every answer in the last four lessons was a set of numbers written as "
                  "an inequality. That is a perfectly good way to write a set, and it "
                  "becomes clumsy the moment the set has two pieces. It also says nothing "
                  "about which numbers were on the table to begin with. Two standard "
                  "notations address both."),
            ("def", ("Interval notation",
                     "For `a ≤ b`: `[a, b]` is the set of `x` with `a ≤ x ≤ b`; `(a, b)` "
                     "is the set with `a &lt; x &lt; b`; `[a, b)` and `(a, b]` include one "
                     "end each. A square bracket includes its endpoint and a round bracket "
                     "excludes it.",
                     "Unbounded ends use `∞` and `−∞`, always with a round bracket: "
                     "`[a, ∞)`, `(−∞, b]`, and `(−∞, ∞)` for the whole line.")),
            ("def", ("Set-builder notation",
                     "`{ x ∈ ℝ : P(x) }` is the set of all real numbers `x` for which the "
                     "condition `P(x)` is true. The colon is read <em>such that</em>, and "
                     "a vertical bar is used for the same purpose: `{ x ∈ ℝ | x ≥ 2 }`.",
                     "`∈` is read <em>is an element of</em>. Naming the set the numbers "
                     "come from matters: `{ x ∈ ℝ : 2 ≤ x ≤ 5 }` is an interval, while "
                     "`{ x ∈ ℤ : 2 ≤ x ≤ 5 }` is the four numbers `2, 3, 4, 5`.")),
            ("h3", "One set, four ways"),
            ("math", [
                "inequality      -1 ≤ x < 3",
                "interval        [-1, 3)",
                "set-builder     { x ∈ ℝ : -1 ≤ x < 3 }",
                "number line     filled dot at -1, hollow dot at 3, shaded between",
            ]),
            ("p", "The filled and hollow ends on the line are the brackets. A filled dot "
                  "is a square bracket and a hollow one is round, and reading between the "
                  "two representations should become automatic; the lab prints all four "
                  "from one structure so that they cannot disagree."),
            ("h3", "Unions, and sets in two pieces"),
            ("p", "`x ≤ −2 or x ≥ 5` is two pieces, and interval notation writes it as a "
                  "union: `(−∞, −2] ∪ [5, ∞)`. That `∪` is lesson 10's <em>or</em>. The "
                  "intersection sign `∩` appears far less often, because an <em>and</em> "
                  "of two intervals is itself an interval and gets written as one."),
            ("h3", "The forms that describe nothing"),
            ("ul", [
                "`[3, ∞]`. Infinity is not a number, so it cannot be an element of "
                "anything. Write `[3, ∞)`.",
                "`[5, 2]`. Interval notation names the smaller end first. Read literally "
                "it asks for numbers that are at least 5 and at most 2, of which there are "
                "none.",
                "`(4, 4)`. Both ends excluded and equal, so there is no number strictly "
                "between them: this is the empty set. Compare `[4, 4]`, which is the "
                "one-element set `{ 4 }`.",
                "`x = [2, 5)`. `x` is a number and `[2, 5)` is a set, so they cannot be "
                "equal. Write `x ∈ [2, 5)`, or say that the solution set is `[2, 5)`.",
            ]),
            ("p", "The empty set is written `∅`, or `{ }`. It is not `{ 0 }` and it is not "
                  "`0`: `{ 0 }` is a set with one element in it, and `∅` is a set with "
                  "none. An inequality with no solutions has solution set `∅`, and writing "
                  "`0` claims that `0` is a solution."),
            ("p", "`(2, 5)` is also how a point in the plane is written, in course 3. The "
                  "two notations share their symbols and are told apart by context: an "
                  "interval is a set of numbers on a line, and a point is a pair of "
                  "coordinates. Where both are in play, saying which you mean is worth the "
                  "words."),
            ("example", ("Reading a set back",
                         "`(−∞, −2] ∪ [5, ∞)`. Two pieces. The left one runs for ever "
                         "downward and stops at `−2`, which it includes. The right one "
                         "starts at `5`, which it includes, and runs for ever upward. In "
                         "set-builder notation it is `{ x ∈ ℝ : x ≤ −2 or x ≥ 5 }`. "
                         "Nothing strictly between `−2` and `5` belongs to it, and both "
                         "`−2` and `5` do.")),
            ("p", "One further form is worth having. A set small enough to list is listed: "
                  "`{ 5, −3 }` is the solution set of `3|x − 1| + 2 = 14` from lesson 11, "
                  "and the list is the readable form. Interval notation does reach it, as "
                  "`[−3, −3] ∪ [5, 5]`, and reaches it clumsily. Listing, interval notation "
                  "and set-builder notation are three tools, and the set decides which of "
                  "them is readable."),
        ],
        "lab": ("inequality", {
            "mode": "notation",
            "panel_title": "Type an interval, read it four ways",
            "panel_intro": "Set the two endpoints and their brackets, and the lab prints "
                           "the interval, the inequality, the set-builder form and the "
                           "number line from a single structure. Try putting a square "
                           "bracket on infinity, and try the two endpoints the wrong way "
                           "round.",
        }),
        "steps_title": "Writing a solution set down",
        "steps_intro": "Four checks, in this order. The last one catches a bracket copied from the wrong side.",
        "steps": [
            ("Decide how many pieces the set has",
             "One piece is a single interval. Two or more are a union of intervals joined "
             "by `∪`. A set small enough to list goes in braces. Nothing at all is `∅`."),
            ("Write the smaller end first, then the larger",
             "Interval notation is ordered. `[−2, 5]` is an interval and `[5, −2]` "
             "describes nothing, and the two are one transposition apart with no warning "
             "in between."),
            ("Choose each bracket from the relation that produced it",
             "`&lt;` and `&gt;` give round brackets; `≤` and `≥` give square ones. The two "
             "ends are decided independently of each other, which is why `[2, 5)` is a "
             "perfectly ordinary interval."),
            ("Check one endpoint and one interior value against the original statement",
             "Take the endpoint your notation claims is included and confirm that the "
             "original statement is true there. Then take a number from inside. A bracket "
             "written the wrong way round survives every other check and fails this one."),
        ],
        "worked": {
            "title": "Three answers from this course, written down",
            "intro": ["The solution sets from lessons 9, 10 and 12, in each notation."],
            "lines": [
                "from lesson 9     x ≤ -6",
                "   interval       (-∞, -6]",
                "   set-builder    { x ∈ ℝ : x ≤ -6 }",
                "   number line    filled dot at -6, shading running left",
                "",
                "from lesson 10    2 ≤ x < 4",
                "   interval       [2, 4)",
                "   set-builder    { x ∈ ℝ : 2 ≤ x < 4 }",
                "   number line    filled dot at 2, hollow dot at 4, shaded between",
                "",
                "from lesson 12    x ≤ -2  or  x ≥ 5",
                "   interval       (-∞, -2] ∪ [5, ∞)",
                "   set-builder    { x ∈ ℝ : x ≤ -2 or x ≥ 5 }",
                "   number line    two shaded rays, filled dots at -2 and 5",
                "",
                "degenerate        no solutions        ∅",
                "                  every real number   (-∞, ∞)   or   ℝ",
            ],
            "after": [
                "The bracket beside `−6` is square because the relation that produced it "
                "was `≤`. The bracket beside `−∞` is round because there is nothing there "
                "to include, and that bracket is round in every interval unbounded on the "
                "left, without exception.",
                "The third set is the one that needs the union. Written as an inequality "
                "it takes a word, <em>or</em>; written as an interval it takes a symbol, "
                "`∪`. Both are exact, and the interval form is the one that scales: "
                "however many pieces a set has, it is a list of intervals joined by `∪`.",
            ],
        },
        "quiz_title": "Brackets and ends",
        "quiz": [
            {"q": "Which interval is the set of `x` with `−3 &lt; x ≤ 4`?",
             "a": ["`(−3, 4]`", "`[−3, 4)`", "`(−3, 4)`", "`[−3, 4]`"],
             "c": 0,
             "why": "The strict `&lt;` at the left end gives a round bracket and the `≤` "
                    "at the right end gives a square one. The second option puts both "
                    "brackets on the wrong ends, and the last two make the two ends match "
                    "when the statement does not."},
            {"q": "What is wrong with `[2, ∞]`?",
             "a": ["Nothing; it is a correct way of writing `x ≥ 2`",
                   "The two endpoints are in the wrong order",
                   "The square bracket on `∞` claims infinity is a number in the set, and "
                   "it is not a number at all; the correct form is `[2, ∞)`",
                   "The bracket at `2` should be round, because an interval running to "
                   "infinity cannot include its left endpoint"],
             "c": 2,
             "why": "Infinity marks an end that never arrives, so there is nothing there "
                    "to include and its bracket is always round. The bracket at `2` is "
                    "decided by the relation `≥`, which includes 2; the far end has no "
                    "say in it."},
            {"q": "What set is `(4, 4)`?",
             "a": ["The empty set", "The single number `4`", "Every number except `4`",
                   "It is not valid interval notation"],
             "c": 0,
             "why": "Both ends are excluded and they are the same number, so no number "
                    "lies strictly between them. `[4, 4]` is the set `{ 4 }`, and opening "
                    "either bracket empties it. The notation is valid; the set it names "
                    "has nothing in it."},
        ],
        "mistakes": [
            ("Putting a square bracket on infinity",
             "`(−∞, 3]` is right and `[−∞, 3]` is not. There is no number at the infinite "
             "end to include or exclude, so the bracket there is round in every interval, "
             "always."),
            ("Writing the two ends in the wrong order",
             "`[5, 2]` is not another way of writing `[2, 5]`. Read as a condition it says "
             "`5 ≤ x ≤ 2`, and no number satisfies that. Interval notation is ordered, and "
             "nothing on the page announces when the order has gone."),
            ("Confusing the empty set with a set containing zero",
             "`∅` has no elements. `{ 0 }` has one element, the number `0`. An inequality "
             "with no solutions has solution set `∅`, and writing `0` or `{ 0 }` instead "
             "claims that `0` is a solution."),
        ],
        "standard": ("Finish when you can move between the four representations without stopping to think.",
                     "Given an inequality you should produce the interval, the set-builder "
                     "form and the number line; given any one of those you should produce "
                     "the other three &mdash; including for a set in two pieces and for "
                     "the empty set. Every solution set you write from here on is expected "
                     "in one of these forms."),
        "note": "This closes the course. Every solution set of an inequality here has been "
                "an interval or a union of two intervals, because each statement reduces to "
                "at most two linear ones and a linear statement changes from true to false "
                "at most once along the line. Course 6 solves quadratic inequalities, where "
                "the answer is regularly the two pieces lying outside a pair of roots, and "
                "this notation is what keeps those answers readable.",
    },
]
