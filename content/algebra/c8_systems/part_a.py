"""Course 8, lessons 01-07 — systems solved by hand, then the matrix machinery."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "systems-of-two-linear-equations",
        "title": "Systems of Two Linear Equations",
        "module": "Systems",
        "one_line": "Two lines, and the three things they can do.",
        "summary": (
            "A system asks which pairs satisfy several equations at once, and a "
            "solution has to satisfy every one of them. Two lines cross once, never, "
            "or everywhere &mdash; and those three cases are the whole classification."
        ),
        "key": [
            "one solution      the lines cross once     consistent, independent",
            "no solution       parallel and distinct    inconsistent",
            "infinitely many   one line written twice   consistent, dependent",
            "a₁b₂ − a₂b₁ ≠ 0   ⟺   the first case, exactly one solution",
        ],
        "key_label": "Three cases, and nothing else",
        "concepts_intro": (
            "A system is a question about several equations at once. Two things have "
            "to be settled before any method: what a solution is, and how many there "
            "can be."
        ),
        "concepts": [
            ("A solution satisfies every equation",
             "An ordered pair `(x, y)` solves the system only if substituting it makes "
             "both equations true. Satisfying one of them is not partial credit; it is "
             "not a solution at all."),
            ("There are exactly three possibilities",
             "One, none, or infinitely many. Two lines cannot cross in exactly two "
             "points, because two distinct points already determine a single line "
             "&mdash; so sharing two points means sharing all of them."),
            ("A graph names the case; it does not give the answer",
             "The lines `2x + y = 4` and `x − y = 1` cross at `(5/3, 2/3)`. A careful "
             "drawing puts the crossing near `(1.7, 0.7)`, and no drawing distinguishes "
             "`5/3` from `1.7`."),
        ],
        "read_title": "Systems, solutions, and the three cases",
        "read_intro": "One definition, then the complete list of what two lines can do.",
        "body": [
            ("def", ("System of two linear equations",
                     "A <strong>linear equation</strong> in `x` and `y` is one that can "
                     "be written `ax + by = c` with `a` and `b` not both zero. A "
                     "<strong>system</strong> is two or more such equations considered "
                     "together, and a <strong>solution</strong> of the system is an "
                     "ordered pair `(x, y)` that satisfies every equation in it.",
                     "The <strong>solution set</strong> is the set of all such pairs. "
                     "Solving the system means describing that set, which is not always "
                     "a matter of naming one pair.")),
            ("p", "\"Considered together\" is where the content is. On its own, "
                  "`2x + y = 4` has infinitely many solutions &mdash; one for every "
                  "value of `x`. The system asks for the pairs the two equations have "
                  "in common, so the solution set of the system is the "
                  "<em>intersection</em> of the two solution sets, never their union."),
            ("p", "Course 3 established that the graph of `ax + by = c` is a line. So "
                  "the solution set of a two-equation system is the set of points lying "
                  "on both lines, and the question \"how many solutions\" becomes the "
                  "question \"how do two lines meet\"."),
            ("thm", ("Two lines meet in nothing, one point, or a whole line",
                     "Two lines in the plane share no point, exactly one point, or every "
                     "point of the line. No other count is possible &mdash; in "
                     "particular no system of two linear equations has exactly two "
                     "solutions.")),
            ("proof", [
                "Suppose the two lines share two distinct points `P` and `Q`. There is "
                "exactly one line through `P` and `Q`, so the two lines are the same "
                "line, and then every point of one lies on the other.",
                "So if the lines share more than one point they share all of them. The "
                "remaining possibilities are one shared point and none.",
            ]),
            ("p", "The three cases carry names. A system with at least one solution is "
                  "<strong>consistent</strong>; one with none is "
                  "<strong>inconsistent</strong>. A consistent system whose equations "
                  "describe the same line is <strong>dependent</strong>; one with "
                  "exactly one solution is <strong>independent</strong>."),
            ("h3", "Telling the cases apart without drawing"),
            ("p", "Put both equations in slope-intercept form. Different slopes means "
                  "the lines cross once. Equal slopes with different intercepts means "
                  "parallel and distinct, so no solution. Equal slopes and equal "
                  "intercepts means one line written two ways, so infinitely many."),
            ("math", [
                "2x + 3y = 6      y = −(2/3)x + 2       slope −2/3,  intercept 2",
                "4x + 6y = 7      y = −(2/3)x + 7/6     slope −2/3,  intercept 7/6",
                "",
                "same slope, different intercept   →   parallel, distinct   →   none",
            ]),
            ("p", "There is a test that skips the rearranging. For `a₁x + b₁y = c₁` and "
                  "`a₂x + b₂y = c₂`, the system has exactly one solution precisely when "
                  "`a₁b₂ − a₂b₁ ≠ 0`. When that number is zero the lines are parallel, "
                  "and comparing the constants settles which of the two remaining cases "
                  "you are in. Lesson 8 gives this number its name: it is the "
                  "determinant."),
            ("example", ("The same line, written twice",
                         "`x − 2y = 4` and `−3x + 6y = −12`. The second equation is "
                         "`−3` times the first, so every pair satisfying one satisfies "
                         "the other and the solution set is the whole line "
                         "`{(x, y) : x − 2y = 4}`.",
                         "Infinitely many is not the same as \"all pairs\". `(0, 0)` "
                         "fails both equations, and so does most of the plane.")),
            ("p", "Checking a candidate is not optional and takes ten seconds: "
                  "substitute the pair into <em>every</em> original equation. A pair "
                  "produced by an error usually satisfies the last equation you touched, "
                  "which is exactly the one that will not catch it."),
        ],
        "lab": ("system", {
            "mode": "graph",
            "panel_title": "Two lines at once",
            "panel_intro": "Move the coefficients and watch the crossing point. Set the "
                           "second line's slope equal to the first: the intersection "
                           "leaves the plane entirely, and that is what an inconsistent "
                           "system looks like before any algebra.",
        }),
        "steps_title": "Reading a system before solving it",
        "steps_intro": "Four questions, in this order. The first three often finish the job.",
        "steps": [
            ("Write both equations the same way",
             "Either both as `ax + by = c` or both as `y = mx + b`, with the terms in "
             "the same order. Two equations written in different shapes cannot be "
             "compared, and comparing them is the next three steps."),
            ("Compare the slopes",
             "Different slopes means exactly one solution: stop classifying and go and "
             "find it. Equal slopes means the system is one of the two degenerate "
             "cases."),
            ("If the slopes agree, compare the intercepts",
             "Different intercepts: parallel and distinct, no solution. Same intercept: "
             "the two equations describe one line, and the solution set is that line."),
            ("Solve, then substitute into both originals",
             "The pair must be tested in every equation of the system, including the "
             "ones you stopped using early. A solution that satisfies one equation is "
             "not a solution."),
        ],
        "worked": {
            "title": "Classifying three systems",
            "intro": [
                "Each pair is put into slope-intercept form and read off. The count of "
                "solutions is settled before any solving happens, and in two of the "
                "three cases no solving is possible."
            ],
            "lines": [
                "(a)   2x − y = 1       y = 2x − 1         slope  2",
                "      x + y = 5        y = −x + 5         slope −1     slopes differ",
                "",
                "      2x − 1 = −x + 5   →   3x = 6   →   x = 2,   y = 3",
                "      one solution   (2, 3)      check   4 − 3 = 1 ✓   2 + 3 = 5 ✓",
                "",
                "(b)   2x + 3y = 6      y = −(2/3)x + 2",
                "      4x + 6y = 7      y = −(2/3)x + 7/6",
                "      same slope, different intercept   →   no solution",
                "",
                "(c)   x − 2y = 4       y = (1/2)x − 2",
                "      −3x + 6y = −12   y = (1/2)x − 2",
                "      the same line   →   infinitely many:  {(x, y) : x − 2y = 4}",
            ],
            "after": [
                "System (b) has no solution, and that is a complete answer. Pushing on "
                "with algebra produces a false statement &mdash; doubling the first equation "
                "gives `4x + 6y = 12` against `4x + 6y = 7`, so `0 = 5` &mdash; which is "
                "the signature the next two lessons teach you to read rather than to fear.",
                "System (c) is the one that gets reported wrongly. The answer is a "
                "line, and it has to be written as a line &mdash; either as the equation "
                "`x − 2y = 4` or in the parameter form `(2t + 4, t)`. \"Infinitely "
                "many\" on its own says how many and not which.",
            ],
        },
        "quiz_title": "Systems and their solutions",
        "quiz": [
            {"q": "Which ordered pair is a solution of the system `x + 2y = 1`, "
                  "`2x − y = 7`?",
             "a": ["`(1, 0)`", "`(4, 1)`", "`(3, −1)`", "`(3, 1)`"],
             "c": 2,
             "why": "`3 + 2(−1) = 1` and `2(3) − (−1) = 7`, so it satisfies both. "
                    "`(1, 0)` satisfies the first equation only and `(4, 1)` the second "
                    "only &mdash; each is what you get by solving one equation and "
                    "forgetting the other. `(3, 1)` satisfies neither."},
            {"q": "How many solutions does `2x + 3y = 6`, `4x + 6y = 7` have?",
             "a": ["Exactly one",
                   "None",
                   "Infinitely many, since the left-hand sides are proportional",
                   "Two"],
             "c": 1,
             "why": "Both lines have slope `−2/3`, and the intercepts `2` and `7/6` "
                    "differ, so the lines are parallel and distinct. Proportional "
                    "left-hand sides alone do not give infinitely many solutions: the "
                    "constants must be in the same proportion, and `6` and `7` are not."},
            {"q": "The lines `2x + y = 4` and `x − y = 1` are drawn carefully, and they "
                  "appear to cross near `(1.7, 0.7)`. What has the drawing "
                  "established?",
             "a": ["That the solution is `(1.7, 0.7)`",
                   "That there is exactly one solution, whose exact value the drawing "
                   "cannot supply",
                   "That the system is inconsistent",
                   "Nothing whatever"],
             "c": 1,
             "why": "Crossing lines settle the case &mdash; one solution &mdash; and "
                    "locate it roughly, which is worth having. The exact pair is "
                    "`(5/3, 2/3)`, and no drawing separates `5/3` from `1.7`; only "
                    "the algebra of the next two lessons does."},
        ],
        "mistakes": [
            ("Reporting x and stopping",
             "The solution of a two-variable system is a pair. `x = 2` is half an "
             "answer, and the missing half is where the sign errors live."),
            ("Checking the answer in one equation only",
             "If `y` was found by substituting into the second equation, that equation "
             "will check out however badly the first step went. The equation you have "
             "not used since the beginning is the one that catches the error."),
            ("Calling a dependent system's solution set everything",
             "`x − 2y = 4` and `−3x + 6y = −12` are satisfied by infinitely many pairs, "
             "but `(0, 0)` is not one of them. The solution set is a line, not the "
             "plane, and it has to be described."),
        ],
        "standard": ("Finish when you can name the case before you solve.",
                     "From the coefficients alone you should be able to say whether a "
                     "system has one solution, none, or infinitely many, and only then "
                     "produce the pair and check it in both equations. Naming the case "
                     "first is what turns an inconsistent system into a two-line answer "
                     "instead of a page of algebra ending in `0 = 14`."),
        "note": "The three cases survive every enlargement of the problem. Lesson 4 has "
                "three variables and the same three answers; lesson 6 reads them "
                "straight off a row-reduced matrix without any geometry at all. The "
                "single number that separates the first case from the other two, "
                "`a₁b₂ − a₂b₁`, is the subject of lesson 8.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "solving-by-substitution",
        "title": "Solving by Substitution",
        "module": "Systems",
        "one_line": "Replacing one unknown with an expression in the other.",
        "summary": (
            "Solve one equation for one unknown, put that expression into the other "
            "equation, and a system in two variables becomes an equation in one. The "
            "method always works; the choice of what to isolate decides whether it is "
            "pleasant."
        ),
        "key": [
            "x − y = 1        →   x = y + 1              isolate",
            "2x + 3y = 12     →   2(y + 1) + 3y = 12     substitute into the OTHER one",
            "                     5y = 10  →  y = 2      solve",
            "                     x = 2 + 1 = 3          back-substitute:  (3, 2)",
        ],
        "key_label": "Isolate, substitute, solve, back-substitute",
        "concepts_intro": (
            "One equation of the system is turned into a name for a variable, and that "
            "name is then used everywhere else. The reason this is allowed is worth "
            "stating once, plainly."
        ),
        "concepts": [
            ("Substitution is legal because the two expressions name one number",
             "If `x = y + 1` holds, then `x` and `y + 1` are two names for the same "
             "number, and either may be written where the other stands. That is the "
             "entire justification, and it is why the expression must go into the "
             "equation you have not used."),
            ("The target is one equation in one unknown",
             "Everything else is bookkeeping. Course 2 already solves any linear "
             "equation in one variable; this lesson is about manufacturing one."),
            ("What you isolate is a free choice with consequences",
             "A variable whose coefficient is `1` or `−1` isolates with no division. "
             "Any other choice produces a fraction, which is survivable &mdash; "
             "multiply through and it clears &mdash; but it is extra work chosen, not "
             "imposed."),
        ],
        "read_title": "The method, and why it is allowed",
        "read_intro": "Four moves, the theorem that licenses them, and the two ways the variable can vanish.",
        "body": [
            ("p", "The method has four moves. Solve one of the equations for one of its "
                  "variables. Substitute the resulting expression into the other "
                  "equation, which then contains one variable. Solve it. Put that value "
                  "back into the isolated equation to get the partner, and check the "
                  "pair in both originals."),
            ("thm", ("Substitution preserves the solution set",
                     "Let a system consist of `x = E`, where `E` is an expression in "
                     "`y`, together with a second equation. Replacing every `x` in the "
                     "second equation by `E` produces a system with exactly the same "
                     "solutions, provided `x = E` is kept.")),
            ("proof", [
                "Take a pair `(x, y)` satisfying both original equations. It satisfies "
                "`x = E`, so `x` and `E` are the same number, and putting one in place "
                "of the other in a true equation leaves a true equation. So the pair "
                "satisfies the substituted equation as well.",
                "Now take a pair satisfying `x = E` and the substituted equation. The "
                "same argument, run with `E` replaced by `x`, returns the original "
                "second equation. Neither direction loses a pair, so the two systems "
                "have the same solution set.",
            ]),
            ("p", "The proviso is not decoration. The isolated equation stays part of "
                  "the system, and it is what produces the value of `x` at the end. "
                  "Dropping it once the substitution is made leaves a single equation "
                  "in one variable, which has a different solution set from the system "
                  "you started with."),
            ("h3", "Choosing what to isolate"),
            ("p", "Look for a coefficient of `1` or `−1`. In `5x − 2y = 4` and "
                  "`3x + y = 9`, the `y` in the second equation has coefficient `1`, so "
                  "`y = 9 − 3x` arrives without a division. If no coefficient is `1` or "
                  "`−1`, pick whichever looks smallest and accept the fraction."),
            ("math", [
                "3x + 2y = 4          no coefficient is 1 or −1;  isolate x below",
                "2x − 5y = 9      →   x = (9 + 5y)/2",
                "",
                "3(9 + 5y)/2 + 2y = 4          substitute into the FIRST equation",
                "3(9 + 5y) + 4y = 8            × 2, clearing the denominator",
                "27 + 15y + 4y = 8",
                "19y = −19    →    y = −1",
                "x = (9 + 5(−1))/2 = 4/2 = 2",
                "",
                "check    3(2) + 2(−1) = 6 − 2 = 4    ✓",
                "         2(2) − 5(−1) = 4 + 5 = 9    ✓",
            ]),
            ("p", "Substituting into the first equation is not a preference. Putting "
                  "`x = (9 + 5y)/2` back into `2x − 5y = 9` gives `9 = 9`: true, and "
                  "completely uninformative, because that equation was used to build the "
                  "expression in the first place. Information comes from the equation "
                  "that has not yet been spent."),
            ("h3", "When the variable disappears"),
            ("p", "Sometimes the substitution removes both variables and leaves a "
                  "statement about numbers. Course 2 met these as contradictions and "
                  "identities, and they mean here exactly what they meant there: a "
                  "false statement means no pair works, a true one means the equation "
                  "placed no new restriction and the whole line survives."),
            ("math", [
                "x − 2y = 3     →   x = 2y + 3",
                "2x − 4y = 1        2(2y + 3) − 4y = 1   →   4y + 6 − 4y = 1   →   6 = 1",
                "                   FALSE   →   no solution; the lines are parallel",
                "",
                "x − 2y = 3     →   x = 2y + 3",
                "2x − 4y = 6        2(2y + 3) − 4y = 6   →   6 = 6",
                "                   TRUE for every y   →   infinitely many",
                "                   solution set   {(2t + 3, t) : t real}",
            ]),
            ("example", ("Reading a parameter form",
                         "`{(2t + 3, t)}` is a recipe: choose `t`, get a pair. `t = 0` "
                         "gives `(3, 0)`, `t = 1` gives `(5, 1)`, `t = 5` gives "
                         "`(13, 5)`. Each satisfies `x − 2y = 3` and `2x − 4y = 6`.",
                         "The letter is arbitrary and the description is not unique: "
                         "`{(s, (s − 3)/2)}` describes the same line. Any correct "
                         "description of the set is a correct answer.")),
            ("p", "The check at the end is a check of both original equations. This is "
                  "the same discipline as lesson 1 and for the same reason: an "
                  "arithmetic slip in the substitution produces a pair that fits the "
                  "equation it came out of."),
        ],
        "lab": ("system", {
            "mode": "substitution",
            "panel_title": "Watch the substitution",
            "panel_intro": "Enter a system and the lab isolates one variable and shows "
                           "the single-variable equation that results. Switch which "
                           "variable it isolates and compare the two routes: the same "
                           "pair at the end, and not the same fractions on the way.",
        }),
        "steps_title": "Substituting without losing a solution",
        "steps_intro": "Four moves. The third is where the sign errors are.",
        "steps": [
            ("Pick the variable with coefficient 1 or minus 1",
             "It isolates without division and keeps the next line clean. If no "
             "coefficient qualifies, choose any variable and expect one fraction, which "
             "will clear when you multiply through."),
            ("Isolate it, and keep that equation",
             "Write `y = 9 − 3x` down on its own line. It is still one of the two "
             "equations of the system, and it is the one that supplies the second "
             "coordinate at the end."),
            ("Substitute into the other equation, in brackets",
             "The whole expression replaces the variable. In `5x − 2y = 4` the `y` "
             "becomes `(9 − 3x)` inside brackets, so the `−2` multiplies both terms: "
             "`−2(9 − 3x) = −18 + 6x`."),
            ("Back-substitute, then check in both originals",
             "Put the number into the isolated equation to get the partner. Then test "
             "the pair in the two equations you were given, not in anything you have "
             "derived."),
        ],
        "worked": {
            "title": "5x − 2y = 4 and 3x + y = 9",
            "intro": [
                "The second equation has a `y` with coefficient `1`, so that is what to "
                "isolate. Everything after that is one-variable algebra from course 2."
            ],
            "lines": [
                "5x − 2y = 4",
                "3x + y = 9        →     y = 9 − 3x",
                "",
                "5x − 2(9 − 3x) = 4          substitute into the first equation",
                "5x − 18 + 6x = 4            −2 multiplies BOTH terms in the bracket",
                "11x = 22",
                "x = 2",
                "y = 9 − 3(2) = 3",
                "",
                "check    5(2) − 2(3) = 10 − 6 = 4    ✓",
                "         3(2) + 3    = 6 + 3  = 9    ✓",
                "solution   (2, 3)",
            ],
            "after": [
                "The second line of the substitution is the one that goes wrong. "
                "`−2` times `−3x` is `+6x`; writing `5x − 18 − 6x = 4` instead gives "
                "`−x = 22` and `x = −22`, which fails the very first check. The bracket "
                "is what prevents it, and the bracket costs nothing.",
                "Isolating `x` from the first equation instead is legitimate and gives "
                "`x = (4 + 2y)/5`. The same pair comes out. The fifths are the price of "
                "ignoring the coefficient of `1` sitting in the other equation.",
            ],
        },
        "quiz_title": "Substitution",
        "quiz": [
            {"q": "Substituting `y = 9 − 3x` into `5x − 2y = 4` gives:",
             "a": ["`5x − 18 − 6x = 4`", "`5x − 18 + 6x = 4`",
                   "`5x − 2 · 9 − 3x = 4`", "`5x − 9 + 3x = 4`"],
             "c": 1,
             "why": "`−2(9 − 3x) = −18 + 6x`. The first choice loses the sign on the "
                    "second product, the third drops the bracket so the `−2` never "
                    "reaches the `3x`, and the fourth multiplies by `−1` instead of "
                    "`−2`."},
            {"q": "A substitution leads to `6 = 1`. The system:",
             "a": ["has the solution `(6, 1)`",
                   "has no solution",
                   "has infinitely many solutions",
                   "has been solved incorrectly, necessarily"],
             "c": 1,
             "why": "A statement with no variable left in it is either true or false. "
                    "False means no pair can satisfy both equations, so the lines are "
                    "parallel and distinct. Reading the two numbers off as a pair "
                    "manufactures a solution out of a contradiction; `6 = 6` would mean "
                    "the opposite of all of it, every pair on the line working."},
            {"q": "In the system `4x − y = 7`, `3x + 5y = 1`, which isolation avoids "
                  "fractions?",
             "a": ["`x` from the first", "`y` from the first",
                   "`y` from the second", "`x` from the second"],
             "c": 1,
             "why": "`y` has coefficient `−1` in the first equation, so `y = 4x − 7` "
                    "needs no division. The other three choices divide by `4`, `5` and "
                    "`3` respectively."},
        ],
        "mistakes": [
            ("Substituting back into the equation you isolated from",
             "`y = 9 − 3x` returned to `3x + y = 9` gives `9 = 9`. That is true and it "
             "is not evidence of anything &mdash; in particular it does not mean the "
             "system is dependent. The substitution goes into the equation that has not "
             "been used."),
            ("Dropping the brackets",
             "`−2y` with `y = 9 − 3x` is `−2(9 − 3x)`. Written without brackets the "
             "`−2` reaches only the `9`, the `x` term keeps the wrong sign, and the "
             "answer that follows is confidently wrong."),
            ("Stopping at one number",
             "`x = 2` is not a solution of a two-variable system. Back-substitution is "
             "a step of the method, not a flourish, and the pair is the answer."),
        ],
        "standard": ("Finish when the fractions do not stop you.",
                     "Isolating a variable whose coefficient is `2` or `−5` produces an "
                     "expression such as `(9 + 5y)/2`, and the method carries on "
                     "unchanged: multiply through and the denominator goes. The standard "
                     "is a system in which no coefficient is `1`, solved in exact "
                     "fractions, with the pair checked in both original equations."),
        "note": "Substitution is the method that generalises furthest. It is how lesson "
                "4 finishes a three-variable system once elimination has done the "
                "reduction, and it is what \"back-substitution\" means in lesson 6. "
                "Elimination, next, is usually quicker when both equations are already "
                "in standard form &mdash; and slower when one variable is sitting there "
                "with a coefficient of `1`.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "solving-by-elimination",
        "title": "Solving by Elimination",
        "module": "Systems",
        "one_line": "Adding equations to make an unknown disappear.",
        "summary": (
            "Adding one equation to another is legal, and if the multiples are chosen "
            "so that the coefficients of one variable are opposites, that variable "
            "leaves. What remains is one equation in one unknown, and the system you "
            "now have is the system you started with."
        ),
        "key": [
            "3x + 4y = 10                 3x + 4y = 10",
            "5x − 2y = 8      × 2    →   10x − 4y = 16",
            "                            ---------------      add",
            "                            13x = 26   →   x = 2,   then   y = 1",
        ],
        "key_label": "One multiplication, one addition, one unknown gone",
        "concepts_intro": (
            "Two operations are used, and both need a reason. The reason is the same "
            "in each case: the step can be undone."
        ),
        "concepts": [
            ("Adding two equations adds equals to equals",
             "If `a = b` and `c = d`, then `a + c = b + d`. Elimination is that one "
             "fact applied to two equations, and it is why the sum of two true "
             "equations is a true equation."),
            ("Multiplying an equation by a nonzero number changes nothing",
             "The solution set survives, because dividing by the same number puts the "
             "equation back. Multiplying by `0` is forbidden: `0 = 0` is satisfied by "
             "every pair, and there is no operation that recovers what was there."),
            ("The new system is equivalent, not merely implied",
             "Replacing the second equation by second plus `k` times first can be "
             "undone by subtracting `k` times the first. Nothing is lost and nothing is "
             "invented. Operations that cannot be undone &mdash; squaring both sides, "
             "in course 5 &mdash; are exactly the ones that produce solutions that were "
             "never there."),
        ],
        "read_title": "Elimination, and why the new system is equivalent",
        "read_intro": "Two operations, the theorem that licenses them, and the three endings.",
        "body": [
            ("p", "To eliminate a variable, multiply one or both equations by constants "
                  "chosen so that the coefficients of that variable become opposites, "
                  "then add the equations. The variable cancels, the sum is a new "
                  "equation in the other variable alone, and solving it gives one "
                  "coordinate."),
            ("thm", ("Elimination preserves the solution set",
                     "Let `E₁` and `E₂` be equations and let `k` be any number. The "
                     "systems `{E₁, E₂}` and `{E₁, E₂ + kE₁}` have exactly the same "
                     "solutions. If `k ≠ 0`, the systems `{E₁, E₂}` and `{E₁, kE₂}` "
                     "have exactly the same solutions.")),
            ("proof", [
                "Suppose the pair `(x, y)` satisfies `E₁` and `E₂`. Then the two sides "
                "of `E₁` are equal numbers at that pair, so `k` times them are equal, "
                "and adding equal quantities to the two sides of `E₂` leaves a true "
                "equation. So the pair satisfies `E₂ + kE₁`, and it still satisfies "
                "`E₁`, which was not touched.",
                "Suppose instead the pair satisfies `E₁` and `E₂ + kE₁`. Run the same "
                "argument with `−k`: adding `−k` times `E₁` to `E₂ + kE₁` gives `E₂`, "
                "so the pair satisfies `E₂`. Every solution of either system is a "
                "solution of the other.",
                "For the second claim, multiplying `E₂` by `k` is undone by multiplying "
                "by `1/k`, which exists exactly when `k ≠ 0`.",
            ]),
            ("p", "Keeping `E₁` unchanged is what makes the argument run in both "
                  "directions. Replacing both equations at once by two combinations is "
                  "not covered by this theorem, and it is genuinely unsafe: from "
                  "`x = 1` and `y = 1` you may add each to the other and reach "
                  "`x + y = 2` twice, which has a whole line of solutions. One equation "
                  "at a time, always."),
            ("h3", "Choosing the multipliers"),
            ("p", "Look at the coefficients of the variable you want to remove. If one "
                  "divides the other, multiply the smaller equation and you are done. "
                  "Otherwise take the least common multiple of the two coefficients: "
                  "for `3y` and `−2y` that is `6`, so multiply by `2` and `3`. The sign "
                  "of one multiplier is chosen to make the two coefficients opposite."),
            ("math", [
                "2x + 3y = 5      × 2    →    4x + 6y =  10",
                "5x − 2y = −16    × 3    →   15x − 6y = −48",
                "                             -------------------      add",
                "                             19x = −38    →    x = −2",
                "",
                "2(−2) + 3y = 5    →    3y = 9    →    y = 3",
                "",
                "check    5(−2) − 2(3) = −10 − 6 = −16    ✓",
                "solution   (−2, 3)",
            ]),
            ("p", "Either variable may be eliminated, and the answer does not depend on "
                  "which. The work does. Before starting, look at all four coefficients "
                  "and pick the variable that costs one multiplication rather than two."),
            ("h3", "When both variables disappear"),
            ("p", "The sum can lose both variables at once, leaving a statement about "
                  "numbers. A false one means the system is inconsistent. A true one "
                  "means the second equation carried no information the first did not "
                  "already have, and the solution set is the whole line."),
            ("math", [
                "2x − 6y = 4                   2x − 6y =  4",
                "−x + 3y = 5      × 2    →    −2x + 6y = 10",
                "                              ---------------      add",
                "                              0 = 14      FALSE   →   no solution",
                "",
                "2x − 6y = 4                   2x − 6y =  4",
                "−x + 3y = −2     × 2    →    −2x + 6y = −4",
                "                              ---------------      add",
                "                              0 = 0       TRUE    →   infinitely many",
            ]),
            ("example", ("Describing the dependent solution set",
                         "The second system above is `x − 3y = 2` multiplied by `2` and "
                         "by `−1`, so its solution set is that line: `{(3t + 2, t)}`. At `t = 0` the "
                         "pair is `(2, 0)` and at `t = 1` it is `(5, 1)`, and both "
                         "satisfy `2x − 6y = 4` and `−x + 3y = −2`.",
                         "`(0, 0)` is not among them. \"Infinitely many\" is a count, "
                         "and the answer is a set.")),
            ("p", "Between the two methods: elimination is quicker when both equations "
                  "are in standard form and no coefficient is `1`, which is most of the "
                  "time. Substitution wins when a variable is already isolated or has a "
                  "coefficient of `1`. Neither is more correct, and the choice is worth "
                  "five seconds before the pen moves."),
        ],
        "lab": ("system", {
            "mode": "elimination",
            "panel_title": "Pick the multipliers",
            "panel_intro": "Choose which variable to eliminate and the lab shows the "
                           "multiplied equations and their sum. Run the same system "
                           "twice, once for each variable: two routes, one pair, and "
                           "usually one of them is half the arithmetic.",
        }),
        "steps_title": "Eliminating a variable",
        "steps_intro": "Four moves. The first is the one people skip and then pay for.",
        "steps": [
            ("Line both equations up in standard form",
             "`ax + by = c`, with the `x` term above the `x` term and the constants on "
             "the right. Elimination adds columns, and columns that are not aligned add "
             "the wrong things together."),
            ("Choose the variable and the two multipliers",
             "Take the least common multiple of its two coefficients and give one "
             "equation the sign that makes them opposites. Choosing the cheaper "
             "variable here is the whole of the skill."),
            ("Add the equations and solve what is left",
             "One variable, one equation, course 2. If both variables vanish, read the "
             "numeric statement instead: false means no solution, true means infinitely "
             "many and the answer is a line."),
            ("Back-substitute into an original equation, then check in both",
             "Use an equation you were given rather than one you multiplied &mdash; "
             "fewer chances to carry a stray factor. Then test the pair in both "
             "originals."),
        ],
        "worked": {
            "title": "3x + 4y = 10 and 5x − 2y = 8",
            "intro": [
                "The `y` coefficients are `4` and `−2`. Doubling the second equation "
                "makes them `4` and `−4`, so one multiplication is enough and `y` goes "
                "on the first addition."
            ],
            "lines": [
                "3x + 4y = 10                     3x + 4y = 10",
                "5x − 2y = 8       × 2      →    10x − 4y = 16",
                "                                 ----------------      add",
                "                                 13x = 26",
                "                                 x = 2",
                "",
                "3(2) + 4y = 10    →    4y = 4    →    y = 1",
                "",
                "check    3(2) + 4(1) = 6 + 4  = 10    ✓",
                "         5(2) − 2(1) = 10 − 2 = 8     ✓",
                "solution   (2, 1)",
            ],
            "after": [
                "Eliminating `x` instead reaches the same pair by a longer road: "
                "multiply the first equation by `5` and the second by `−3` to get "
                "`15x + 20y = 50` and `−15x + 6y = −24`, whose sum is `26y = 26`. Two "
                "multiplications against one, with larger numbers in both. That "
                "difference is visible before any work is done, which is why the choice "
                "belongs at the start.",
                "The `16` on the right of the doubled equation is the entry most often "
                "left behind. Multiplying an equation means multiplying the constant "
                "too, and a check in both originals catches the omission immediately.",
            ],
        },
        "quiz_title": "Elimination",
        "quiz": [
            {"q": "To eliminate `y` from `3x + 4y = 10` and `5x − 2y = 8`, you can:",
             "a": ["multiply the second equation by `2` and add",
                   "multiply the second equation by `2` and subtract",
                   "multiply the first equation by `2` and add",
                   "multiply the second equation by `−2` and add"],
             "c": 0,
             "why": "Doubling the second gives `−4y`, the opposite of `4y`, so adding "
                    "cancels it. Subtracting instead leaves `8y`; multiplying by `−2` "
                    "gives `+4y`, which also adds to `8y`; doubling the first gives "
                    "`8y` against `−2y`, which cancels nothing."},
            {"q": "Multiplying an equation through by `0` is forbidden because:",
             "a": ["the resulting statement `0 = 0` is false",
                   "the step cannot be undone, and `0 = 0` is satisfied by every pair",
                   "zero is not a number you are allowed to multiply by",
                   "it changes the slope of the line"],
             "c": 1,
             "why": "Every step here has to be reversible, and dividing by `k` undoes "
                    "multiplying by `k` only when `k ≠ 0`. `0 = 0` is perfectly true "
                    "&mdash; that is the trouble with it. It has lost every restriction "
                    "the original equation imposed."},
            {"q": "Elimination on a system ends with `0 = 14`. The solution set is:",
             "a": ["`{(0, 14)}`", "empty",
                   "every pair on either of the two lines", "`{14}`"],
             "c": 1,
             "why": "`0 = 14` is false for every `x` and every `y`, so no pair "
                    "satisfies both equations and the lines are parallel and distinct. "
                    "`0 = 0` is the other degenerate ending and means the opposite: a "
                    "whole line of solutions."},
        ],
        "mistakes": [
            ("Adding equations that are not aligned",
             "`3x + 4y = 10` written above `8 = 5x − 2y` invites adding `4y` to `5x`. "
             "Standard form first, every time; the alignment is what makes the addition "
             "mean anything."),
            ("Multiplying only the left-hand side",
             "`5x − 2y = 8` doubled is `10x − 4y = 16`. The `16` is the part that gets "
             "left behind, and the resulting system is a different system that happens "
             "to look like the right one."),
            ("Reading 0 = 0 as x = 0",
             "It is a true statement with no variable in it, so the system is dependent "
             "and its solution set is a line. Reporting `(0, 0)` names a single pair "
             "which, for `2x − 6y = 4`, is not even on that line."),
        ],
        "standard": ("Finish when you choose the cheaper variable before starting.",
                     "Look at the four coefficients, decide which variable costs one "
                     "multiplication instead of two, and carry it through in exact "
                     "fractions. Both routes give the same pair; being able to say which "
                     "is shorter, and why, is the judgement that survives into lesson 6, "
                     "where the choice is made for you by position on the page."),
        "note": "Elimination is the rest of this half of the course. Lesson 4 performs "
                "it twice to remove one variable from a three-equation system; lesson 5 "
                "writes it without the letters, as operations on the rows of a matrix; "
                "lesson 6 turns it into an algorithm with no decisions left in it.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "systems-in-three-variables",
        "title": "Systems in Three Variables",
        "module": "Systems",
        "one_line": "Three planes, and elimination done twice.",
        "summary": (
            "A solution is now an ordered triple, and each equation describes a plane. "
            "The method is elimination used twice: remove one variable from two "
            "different pairs of equations, solve the two-variable system that remains, "
            "and back-substitute."
        ),
        "key": [
            " x +  y +  z =  6     E1",
            "2x −  y + 3z =  9     E2      E2 − 2E1 :   −3y +  z = −3",
            "−x + 2y + 4z = 15     E3      E3 +  E1 :    3y + 5z = 21",
            "                              add      :         6z = 18   →   (1, 2, 3)",
        ],
        "key_label": "Eliminate x twice, then solve what is left",
        "concepts_intro": (
            "Nothing new is needed. What is new is the bookkeeping, and one decision "
            "that is easy to get wrong."
        ),
        "concepts": [
            ("A solution is a triple that satisfies all three equations",
             "`(1, 2, 3)` means `x = 1`, `y = 2`, `z = 3`, together. A triple that "
             "satisfies two of the three equations is not a partial solution; it is not "
             "a solution."),
            ("Eliminate the same variable from two different pairs",
             "This is the step that goes wrong. Removing `x` from one pair and `y` from "
             "another leaves two equations containing three unknowns between them, and "
             "nothing has been reduced."),
            ("The three cases return, with more geometry behind them",
             "One solution, none, or infinitely many. In three variables the infinite "
             "case can be a line or a plane, and the algebra reports which by how many "
             "variables are left free."),
        ],
        "read_title": "Three equations, three unknowns",
        "read_intro": "The reduction to a two-variable system, the geometry of each outcome, and the bookkeeping that keeps it honest.",
        "body": [
            ("def", ("Linear equation in three variables",
                     "An equation that can be written `ax + by + cz = d` with `a`, `b`, "
                     "`c` not all zero. Its graph is a plane in space. A "
                     "<strong>solution</strong> of a system of such equations is an "
                     "ordered triple `(x, y, z)` satisfying every equation in the "
                     "system.")),
            ("p", "The method: choose a variable, eliminate it from two different pairs "
                  "of equations, and you are left with two equations in the remaining "
                  "two unknowns &mdash; the situation of lesson 3. Solve that, then "
                  "back-substitute into any original equation to recover the variable "
                  "that was eliminated."),
            ("thm", ("The reduction finds every solution and no others",
                     "Suppose `x` is eliminated from `E₁` and `E₂` to give `A`, and "
                     "from `E₁` and `E₃` to give `B`, where the coefficient of `x` in "
                     "`E₁` is not zero. Then every solution of the original system "
                     "satisfies `A` and `B`; and for each pair `(y, z)` satisfying `A` "
                     "and `B`, equation `E₁` determines exactly one `x`, and the "
                     "resulting triple solves the original system.")),
            ("p", "The theorem is lesson 3's theorem used twice, which is why every "
                  "elimination must keep `E₁` intact and combine it with something "
                  "else. It also explains the requirement that the two new equations "
                  "come from different pairs: two combinations of `E₁` and `E₂` alone "
                  "tell you only what `E₁` and `E₂` already said, and `E₃` never enters "
                  "the calculation."),
            ("h3", "What the three planes are doing"),
            ("ul", [
                "<strong>Exactly one solution.</strong> The three planes have a single "
                "common point, the way two walls and a floor meet in a corner.",
                "<strong>No solution.</strong> Two of the planes may be parallel and "
                "distinct; or the three may meet in pairs along three parallel lines, "
                "like the sides of a triangular prism, with no point on all three.",
                "<strong>Infinitely many.</strong> The planes may share a whole line "
                "&mdash; one free variable &mdash; or all three equations may describe "
                "the same plane, in which case two variables are free.",
            ]),
            ("p", "That picture is worth having and is not worth relying on. Nobody "
                  "reads a triple off a drawing of three planes, and the prism case in "
                  "particular is invisible until the algebra produces a false "
                  "statement. The algebra is the arbiter here even more completely than "
                  "in lesson 1."),
            ("example", ("A third equation that adds nothing",
                         "Replace `E₃` above by `3x + 4z = 15`, which is `E₁ + E₂`. "
                         "Eliminating `x` twice now ends in `0 = 0`, and the solution "
                         "set is a line: `(9 − 4t, t, 3t − 3)`.",
                         "At `t = 1` the triple is `(5, 1, 0)`, and `5 + 1 + 0 = 6`, "
                         "`10 − 1 + 0 = 9`, `15 + 0 = 15`. At `t = 2` it is `(1, 2, 3)`, "
                         "the solution the original system had on its own. One equation "
                         "of the three was never carrying any information.")),
            ("p", "A false statement means the opposite. `x + y + z = 3` together with "
                  "`2x + 2y + 2z = 7` gives `0 = 1` on the first elimination, and the "
                  "system is inconsistent no matter what the third equation says."),
            ("h3", "Bookkeeping"),
            ("ul", [
                "Number the equations `E1`, `E2`, `E3` and write beside every new "
                "equation the combination that produced it &mdash; `E2 − 2E1`. Without "
                "that record an error cannot be located, only redone.",
                "Keep the columns aligned and write a `0` for any variable missing from "
                "an equation. A missing term is information, not an absence.",
                "Do the back-substitution in the reverse order of the elimination: the "
                "last variable found first, then the second, then the one that left "
                "first.",
            ]),
            ("p", "This bookkeeping is the entire content of the next lesson. Once the "
                  "columns are aligned and every coefficient has a fixed position, the "
                  "letters `x`, `y`, `z` are doing no work, and deleting them costs "
                  "nothing."),
        ],
        "lab": ("system", {
            "mode": "three",
            "panel_title": "Three equations at once",
            "panel_intro": "Set the nine coefficients and three constants; the lab "
                           "reports the triple, or reports that the system is "
                           "inconsistent or dependent. Make the third equation the sum "
                           "of the first two and watch a single solution become a line.",
        }),
        "steps_title": "Solving a three-variable system by hand",
        "steps_intro": "Four moves. Write the plan down before doing any arithmetic.",
        "steps": [
            ("Number the equations and put them in standard form",
             "`x`, `y`, `z` in that order in every equation, constants on the right, "
             "and a `0` written in for any variable that does not appear. Alignment "
             "errors account for most of the wrong answers in this lesson."),
            ("Choose the variable that is cheapest to eliminate",
             "Look for a coefficient of `1` or `−1`, or two coefficients that are "
             "already opposites. Ten seconds spent here saves a page."),
            ("Eliminate it from two different pairs",
             "`E1` with `E2`, and `E1` with `E3`, is the standard choice and uses all "
             "three equations. Label each result with the combination that made it."),
            ("Solve the two-variable system, back-substitute, check in all three",
             "The third check is not ceremonial: it is the only test of the arithmetic "
             "you did during the elimination itself."),
        ],
        "worked": {
            "title": "A three-variable system, start to finish",
            "intro": [
                "`x` has coefficients `1`, `2`, `−1`, so it is the cheap variable to "
                "remove: `E2 − 2E1` and `E3 + E1`, both against `E1`."
            ],
            "lines": [
                "E1     x +  y +  z =  6",
                "E2    2x −  y + 3z =  9",
                "E3    −x + 2y + 4z = 15",
                "",
                "E2 − 2E1 :   (2 − 2)x + (−1 − 2)y + (3 − 2)z = 9 − 12",
                "        A :   −3y +  z = −3",
                "",
                "E3 +  E1 :   (−1 + 1)x + (2 + 1)y + (4 + 1)z = 15 + 6",
                "        B :    3y + 5z = 21",
                "",
                "A + B    :   6z = 18      →      z = 3",
                "A        :   −3y + 3 = −3   →   −3y = −6   →   y = 2",
                "E1       :   x + 2 + 3 = 6   →   x = 1",
                "",
                "check    E1 :   1 + 2 + 3     =  6    ✓",
                "         E2 :   2 − 2 + 9     =  9    ✓",
                "         E3 :  −1 + 4 + 12    = 15    ✓",
                "solution   (1, 2, 3)",
            ],
            "after": [
                "Both eliminations removed `x`, which is the point of the whole "
                "exercise. `E2 + 2E3` would also have been acceptable &mdash; a "
                "different pair, the same variable, giving `3y + 11z = 39`. What is "
                "not acceptable is removing a different variable the second time: "
                "`2E2 + E3` gives `3x + 10z = 33`, "
                "a perfectly true equation in `x` and `z`, which together with `A` in "
                "`y` and `z` involves three unknowns and leaves the system exactly as "
                "large as it was.",
                "The back-substitution runs backwards through the work: `z` from the "
                "sum, `y` from `A`, `x` from `E1`. Substituting into `E2` or `E3` "
                "instead is equally valid and slightly more arithmetic; what matters is "
                "that all three are used for the final check.",
            ],
        },
        "quiz_title": "Three variables",
        "quiz": [
            {"q": "You eliminate `x` from `E1` and `E2`, then `y` from `E1` and `E3`. "
                  "What do you have?",
             "a": ["A two-variable system ready to solve",
                   "Two equations involving three unknowns between them, which is no "
                   "reduction",
                   "A contradiction",
                   "The solution, up to back-substitution"],
             "c": 1,
             "why": "Reduction happens only when the same variable leaves both new "
                    "equations. One equation in `y` and `z` beside another in `x` and "
                    "`z` needs a third equation to go further, and all three have "
                    "already been used."},
            {"q": "In the worked example, `A` is `−3y + z = −3` and `z = 3`. Then `y` "
                  "is:",
             "a": ["`−2`", "`2`", "`0`", "`−6`"],
             "c": 1,
             "why": "`−3y + 3 = −3` gives `−3y = −6`, so `y = 2`. `−2` comes from "
                    "dividing `−6` by `3` rather than by `−3`, `−6` from not dividing "
                    "at all, and `0` from adding the `3` to the right-hand side instead "
                    "of subtracting it."},
            {"q": "A three-variable system reduces to `0 = 0` at the last step, with no "
                  "false statement anywhere. The solution set is:",
             "a": ["empty", "a single triple", "a line of triples, one variable free",
                   "the whole of space"],
             "c": 2,
             "why": "A true statement with no variables left removes a restriction "
                    "rather than adding one: one variable may be chosen freely and the "
                    "other two follow from it. The whole of space would require every "
                    "equation to have been `0 = 0` from the start."},
        ],
        "mistakes": [
            ("Eliminating a different variable the second time",
             "The two new equations must be in the same two unknowns. This single "
             "error turns a five-minute exercise into an afternoon, and it is invisible "
             "until the two-variable system refuses to solve."),
            ("Combining the same pair twice",
             "A second combination of `E1` and `E2` alone follows from the first and "
             "says nothing new. All three equations must take part, or the information "
             "in the one left out never reaches the answer."),
            ("Checking only in the equations you finished with",
             "The triple satisfies `A` and `B` by construction, so testing it there "
             "proves nothing about the elimination that produced them. Substitute into "
             "`E1`, `E2` and `E3` as they were given."),
        ],
        "standard": ("Finish when the plan is written before the arithmetic starts.",
                     "State which variable is leaving and which two pairs will remove "
                     "it, then execute in exact fractions and check in all three "
                     "original equations. A three-variable system solved by improvising "
                     "comes out right about half the time; solved to a plan it is "
                     "routine, and the plan is precisely what lesson 6 automates."),
        "note": "From here to lesson 9 this is the same arithmetic with the letters "
                "deleted. The next lesson writes `x + y + z = 6` as the row `1 1 1 | 6` "
                "and `E2 − 2E1` as `R2 − 2R1`; nothing about the numbers changes, which "
                "is exactly why it is worth having done one of these by hand first.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "matrices-and-row-operations",
        "title": "Matrices and Row Operations",
        "module": "Matrices",
        "one_line": "The same elimination, with the letters removed.",
        "summary": (
            "An augmented matrix is a system with the variable names deleted: one row "
            "per equation, one column per variable, one column for the constants. The "
            "three row operations are the three things you were already doing to "
            "equations, and each of them is reversible."
        ),
        "key": [
            " x +  y +  z =  6            1   1   1 |  6",
            "2x −  y + 3z =  9      →     2  −1   3 |  9",
            "−x + 2y + 4z = 15           −1   2   4 | 15",
            "R1 ↔ R2       kR2 → R2  (k ≠ 0)       R3 + kR1 → R3",
        ],
        "key_label": "The system, the matrix, the three legal moves",
        "concepts_intro": (
            "Nothing is proved in this lesson that was not proved in lesson 3. What is "
            "new is a notation, and the discipline the notation demands."
        ),
        "concepts": [
            ("A matrix is bookkeeping, not a new idea",
             "Every row is an equation, every column is a variable, and the bar stands "
             "for the equals sign. Deleting the letters removes the one part of the "
             "page that was never doing any work."),
            ("Position carries all the meaning",
             "In the row `2 −1 3 | 9` the `−1` means `−1y` because it sits in the "
             "second column and for no other reason. A missing term must be written "
             "as `0`, and an equation not in standard form produces a row that means "
             "something other than the equation."),
            ("The three row operations are exactly the reversible ones",
             "Swap two rows; multiply a row by a nonzero number; add a multiple of one "
             "row to another. Each has an inverse of the same kind, and that is the "
             "whole reason the solution set survives them."),
        ],
        "read_title": "Writing a system as a matrix",
        "read_intro": "The definitions, the translation in both directions, and three operations with their inverses.",
        "body": [
            ("def", ("Matrix",
                     "A <strong>matrix</strong> is a rectangular array of numbers. One "
                     "with `m` rows and `n` columns is an `m × n` matrix &mdash; rows "
                     "first, always, and the convention is arbitrary but universal.",
                     "Entries are named by position: `a₂₃` is the entry in row `2`, "
                     "column `3`. Row index first, again by convention.")),
            ("def", ("Coefficient matrix, augmented matrix",
                     "For a system written in standard form, the <strong>coefficient "
                     "matrix</strong> holds the coefficients: one row per equation, one "
                     "column per variable. The <strong>augmented matrix</strong> adds a "
                     "final column holding the constants, usually separated by a "
                     "vertical bar.",
                     "The bar is a reading aid and nothing more. It marks where the "
                     "equals signs were.")),
            ("p", "The translation runs both ways and is entirely mechanical, on one "
                  "condition: every equation is in standard form, with the same "
                  "variables in the same order. Meeting that condition is the reader's "
                  "job, and the matrix cannot check it."),
            ("math", [
                "2y − 5 = 3x − z       →     −3x + 2y +  z = 5     →    −3   2   1 | 5",
                "x + 4z = 0            →       x + 0y + 4z = 0     →     1   0   4 | 0",
            ]),
            ("p", "The `0` in the second row is not padding. In a three-variable system "
                  "every row has four entries; a row with three entries is a row whose "
                  "columns no longer line up with anybody else's, and every subsequent "
                  "operation is then adding the wrong numbers together."),
            ("h3", "The three elementary row operations"),
            ("ul", [
                "<strong>Swap.</strong> `R1 ↔ R3` exchanges two rows. Its inverse is "
                "itself. This corresponds to writing the equations in a different "
                "order, which changes nothing about what is being asked.",
                "<strong>Scale.</strong> `kR2 → R2` multiplies every entry of a row, "
                "including the constant, by `k ≠ 0`. Its inverse is `(1/k)R2 → R2`.",
                "<strong>Replace.</strong> `R3 + kR1 → R3` adds `k` times one row to "
                "another and stores the result in the second. Its inverse is "
                "`R3 − kR1 → R3`. Only the row named on the right of the arrow changes.",
            ]),
            ("thm", ("Row operations preserve the solution set",
                     "If one augmented matrix is obtained from another by a sequence of "
                     "elementary row operations, the two systems they represent have "
                     "exactly the same solution set. Such matrices are called "
                     "<strong>row equivalent</strong>.")),
            ("proof", [
                "Each of the three operations is a restatement of something already "
                "settled. Swapping two rows reorders the equations, and a solution "
                "satisfies a set of equations regardless of the order they are written "
                "in. Scaling a row by `k ≠ 0` is lesson 3's second claim. Replacing "
                "`R3` by `R3 + kR1` is lesson 3's first claim, with `R1` left in place "
                "as that theorem requires.",
                "Each operation has an inverse of the same kind, so any solution "
                "of the new system is a solution of the old one as well. A sequence of "
                "reversible steps is reversible: undo them in the opposite order.",
            ]),
            ("p", "Three things are not row operations. Multiplying a row by `0` "
                  "destroys an equation and cannot be undone. Operating on columns "
                  "renames variables: exchanging two columns produces a matrix whose "
                  "answers are attached to the wrong letters, with nothing on the page "
                  "to record the swap. And two operations performed at once are not a "
                  "sequence of operations &mdash; from the rows `1 0 | 1` and "
                  "`0 1 | 1`, adding each to the other simultaneously gives `1 1 | 2` "
                  "twice, turning a unique solution into a line."),
            ("example", ("Two operations, written out",
                         "Start from the augmented matrix of the lesson-4 system. "
                         "`R2 − 2R1 → R2` gives the row `0 −3 1 | −3`, and "
                         "`R3 + R1 → R3` gives `0 3 5 | 21`.",
                         "Those are the equations `A` and `B` of lesson 4, entry for "
                         "entry. The matrix has not made the arithmetic easier; it has "
                         "made the position of every number decidable in advance.")),
            ("p", "Write each operation beside the row it produces, exactly as the "
                  "combinations were labelled in lesson 4. The next lesson performs "
                  "eight or ten of these in a row, and an unlabelled sequence of "
                  "matrices is impossible to debug."),
        ],
        "lab": ("matrix", {
            "mode": "rows",
            "panel_title": "Apply one operation",
            "panel_intro": "Type an augmented matrix and apply a single row operation at "
                           "a time. Run the operations from lesson 4 &mdash; `R2 − 2R1` "
                           "and `R3 + R1` &mdash; and compare the entries with the "
                           "equations there: the same numbers, in fixed places.",
        }),
        "steps_title": "From a system to a matrix and back",
        "steps_intro": "Four moves. The first two are where the meaning is fixed.",
        "steps": [
            ("Put every equation in standard form",
             "Variables on the left in one agreed order, constant alone on the right. "
             "The order is a choice, and once made it binds every row."),
            ("Write one row per equation, with a zero for every absent variable",
             "In an `n`-variable system every row has `n + 1` entries, without "
             "exception. A short row is a row that has lost its alignment."),
            ("Operate on rows only, one operation at a time",
             "Name the operation as you perform it: `R2 − 2R1 → R2`. The row named "
             "after the arrow is the only row that changes, and the row read from is "
             "left exactly as it was."),
            ("Translate back before believing the answer",
             "A matrix is shorthand for equations. The answer is a triple, and it is "
             "checked by substituting into the original equations &mdash; not by "
             "admiring the final matrix."),
        ],
        "worked": {
            "title": "The lesson-4 system, as a matrix",
            "intro": [
                "The same two eliminations as lesson 4, written without letters. Every "
                "number below appears in the worked example there; only the layout has "
                "changed."
            ],
            "lines": [
                " x +  y +  z =  6            1   1   1 |  6      R1",
                "2x −  y + 3z =  9      →     2  −1   3 |  9      R2",
                "−x + 2y + 4z = 15           −1   2   4 | 15      R3",
                "",
                "R2 − 2R1 → R2       2 − 2(1) = 0     −1 − 2(1) = −3",
                "                    3 − 2(1) = 1      9 − 2(6) = −3",
                "",
                "R3 +  R1 → R3      −1 + 1    = 0      2 + 1    =  3",
                "                    4 + 1    = 5     15 + 6    = 21",
                "",
                "                             1   1   1 |  6",
                "                             0  −3   1 | −3",
                "                             0   3   5 | 21",
            ],
            "after": [
                "The constant column takes part in every operation. `9 − 2(6) = −3` is "
                "the right-hand side of `E2 − 2E1` from lesson 4, and omitting it is the "
                "commonest way to end up with a matrix that no longer represents the "
                "system it started as &mdash; a matrix which then reduces perfectly and "
                "reports a wrong triple.",
                "Notice what the two operations achieved: the first column below the top "
                "row is now zero. That is `x` eliminated, and it is the first column "
                "rather than the first variable only because of where it was written."
            ],
        },
        "quiz_title": "Matrices and row operations",
        "quiz": [
            {"q": "With the columns in the order `x, y, z`, the equation "
                  "`2y − 5 = 3x − z` becomes which row?",
             "a": ["`2 −5 3 | −1`", "`−3 2 1 | 5`", "`3 −2 −1 | 5`", "`0 2 0 | −5`"],
             "c": 1,
             "why": "Standard form first: `−3x + 2y + z = 5`. The row then reads the "
                    "coefficients in column order with the constant last. The third "
                    "choice is that rearrangement with every sign taken from the wrong "
                    "side, and the first is the numbers taken in the order they "
                    "happened to be written down."},
            {"q": "Which of these is not an elementary row operation?",
             "a": ["`R1 ↔ R3`", "`−4R2 → R2`", "`0 · R2 → R2`", "`R3 + 5R1 → R3`"],
             "c": 2,
             "why": "Scaling must be by a nonzero number. Multiplying a row by `0` "
                    "replaces an equation with `0 = 0`, which every triple satisfies, "
                    "and no operation puts the lost equation back. Scaling by `−4` is "
                    "fine: its inverse is scaling by `−1/4`."},
            {"q": "Performing `R2 − 2R1 → R2` changes:",
             "a": ["both `R1` and `R2`", "`R2` only", "`R1` only",
                   "every row, since the matrix is a single object"],
             "c": 1,
             "why": "One elementary operation writes one new row. `R1` is read and left "
                    "alone &mdash; and if it were altered at the same time the step "
                    "would not be reversible, which is exactly the simultaneous-operation "
                    "trap."},
        ],
        "mistakes": [
            ("Leaving the constant column out of the operation",
             "A row operation applies to the whole row. Doubling `2 −1 3 | 9` gives "
             "`4 −2 6 | 18`, and a matrix whose left half was scaled and whose right "
             "half was not represents a system nobody asked about."),
            ("Building a row from an equation not in standard form",
             "`3x = 2y + 5` is not the row `3 2 | 5`. Until the variables are on the "
             "left in the agreed order and the constant is alone on the right, the "
             "positions do not mean what the matrix claims they mean."),
            ("Swapping columns",
             "Rows are equations and may be recombined freely. Columns are variables. "
             "Exchanging two columns silently renames two unknowns, and the numbers "
             "that emerge are attached to the wrong letters with no record of it "
             "anywhere on the page."),
        ],
        "standard": ("Finish when you can translate both ways without thinking.",
                     "Given a system, write its augmented matrix with every zero in "
                     "place; given a matrix, write the system back. Then perform three "
                     "row operations and name the inverse of each. If you cannot name "
                     "the inverse, the step you performed was probably not one of the "
                     "three."),
        "note": "Nothing has been gained yet: this is the same arithmetic in less ink. "
                "What it buys is the next lesson. With the letters gone there is an "
                "obvious order in which to do the operations &mdash; leftmost column "
                "first, then the next &mdash; and an order that obvious is an algorithm "
                "rather than a decision.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "gaussian-elimination",
        "title": "Gaussian Elimination",
        "module": "Matrices",
        "one_line": "Row reduction to echelon form, mechanically.",
        "summary": (
            "Row reduction drives any augmented matrix into one shape, working a "
            "column at a time from the left. The procedure never has to guess which "
            "variable to eliminate, and the number of solutions is read off the result "
            "rather than deduced."
        ),
        "key": [
            "each pivot is 1 and alone in its column     reduced row echelon form",
            "a pivot in every variable column            exactly one solution",
            "a variable column with no pivot             that variable is free",
            "a row  0 0 0 | k  with k ≠ 0                no solution",
        ],
        "key_label": "Reading the answer off the shape",
        "concepts_intro": (
            "One shape, one procedure for reaching it, and one reading of the result. "
            "The reading is the part worth memorising."
        ),
        "concepts": [
            ("Echelon form is a shape, not an answer",
             "Pivots step to the right as you go down, and everything below a pivot in "
             "its column is zero. Getting there is mechanical: take the leftmost "
             "column that still needs work and clear it."),
            ("The three cases are read off, not worked out",
             "Count pivots. A pivot in the constant column means no solution. "
             "Otherwise, variable columns without a pivot are the free ones, and no "
             "free variable means exactly one solution."),
            ("The reduced form is unique",
             "Two people reducing the same matrix by different routes pass through "
             "different intermediate matrices and arrive at the same reduced row "
             "echelon form. The route is a matter of taste; the destination is not."),
        ],
        "read_title": "Row reduction, from any matrix to one shape",
        "read_intro": "Two forms, one algorithm, and what the result says in each of the three cases.",
        "body": [
            ("def", ("Leading entry, row echelon form",
                     "The <strong>leading entry</strong> or <strong>pivot</strong> of a "
                     "nonzero row is its first nonzero entry, reading left to right. A "
                     "matrix is in <strong>row echelon form</strong> when every all-zero "
                     "row lies below every nonzero row, and each pivot lies strictly to "
                     "the right of the pivot in the row above it.")),
            ("p", "The staircase shape has a consequence worth stating separately: "
                  "everything below a pivot, in that pivot's column, is zero. That is "
                  "what \"the variable has been eliminated from the equations below\" "
                  "looks like once the letters are gone."),
            ("def", ("Reduced row echelon form",
                     "A matrix in row echelon form is in <strong>reduced row echelon "
                     "form</strong> when, in addition, every pivot is `1` and is the "
                     "only nonzero entry in its column.",
                     "Row echelon form is enough to finish by back-substitution. The "
                     "reduced form finishes the back-substitution for you: the answer "
                     "is sitting in the constant column.")),
            ("thm", ("Uniqueness of the reduced form",
                     "Every matrix is row equivalent to exactly one matrix in reduced "
                     "row echelon form. Row echelon form is not unique &mdash; the "
                     "route changes it &mdash; but the reduced form does not depend on "
                     "the operations chosen.",
                     "The proof belongs to a linear algebra course. What it buys here "
                     "is practical: two people who disagree about a reduced form have "
                     "an arithmetic error between them, not a difference of method.")),
            ("h3", "The algorithm"),
            ("ol", [
                "Find the leftmost column that is not entirely zero in the rows still "
                "being worked on. That is the pivot column.",
                "If its top entry (in the first unworked row) is zero, swap a row from "
                "below into that position. If the whole column is zero, move right.",
                "Divide the pivot row by its pivot, making the pivot `1`. Keep the "
                "result in exact fractions.",
                "Clear the column: for every other row, subtract that row's entry in "
                "the pivot column times the pivot row.",
                "Cover the pivot row and repeat on the rows below. When no columns are "
                "left, the matrix is in reduced row echelon form.",
            ]),
            ("p", "Clearing only the entries <em>below</em> each pivot gives row "
                  "echelon form, and the system is then finished by back-substitution "
                  "from the bottom row upward &mdash; this is Gaussian elimination in "
                  "its narrow sense. Clearing above as well gives the reduced form "
                  "directly, and is called Gauss-Jordan elimination. The arithmetic "
                  "totals are close; use whichever you can carry out without errors."),
            ("p", "Fractions arrive at step 3 and are not a sign that anything has gone "
                  "wrong. A pivot of `3` produces thirds immediately. Keep them exact: "
                  "`−1/3` written as `−0.33` moves the final answer by about a "
                  "hundredth, and there is nothing in the method that flags which digit "
                  "went bad."),
            ("h3", "Reading the answer"),
            ("ul", [
                "<strong>A row `0 0 … 0 | k` with `k ≠ 0`.</strong> That row says "
                "`0 = k`, so the system has no solution. Stop; nothing further will "
                "improve it.",
                "<strong>A pivot in every variable column.</strong> Exactly one "
                "solution, and in reduced form it is the constant column read off "
                "directly.",
                "<strong>A variable column with no pivot.</strong> That variable is "
                "<strong>free</strong>: give it a parameter and express the pivot "
                "variables in terms of it. The solution set is infinite, with one "
                "parameter for each free variable.",
            ]),
            ("example", ("A free variable, written out",
                         "`x + 2y + 3z = 5` and `2x + 4y + 8z = 14` reduce to the rows "
                         "`1 2 0 | −1` and `0 0 1 | 2`. Column two has no pivot, so `y` "
                         "is free: put `y = t`.",
                         "Then `x + 2t = −1` and `z = 2`, so the solution set is "
                         "`{(−1 − 2t, t, 2)}`. At `t = 1` the triple is `(−3, 1, 2)`, "
                         "and `−3 + 2 + 6 = 5` with `−6 + 4 + 16 = 14`.")),
            ("example", ("An inconsistent pair",
                         "`x + y = 2` and `2x + 2y = 5`. One operation, `R2 − 2R1`, "
                         "produces the row `0 0 | 1`, which reads `0x + 0y = 1`.",
                         "No pair satisfies that, so the system has no solution. "
                         "Reducing further is possible and pointless: the question has "
                         "been answered.")),
            ("p", "The final check is a substitution into the original equations. A "
                  "reduced matrix is self-consistent by construction &mdash; it agrees "
                  "with whatever arithmetic produced it &mdash; so it cannot detect an "
                  "error made on the way down."),
        ],
        "lab": ("matrix", {
            "mode": "rref",
            "panel_title": "Reduce, one column at a time",
            "panel_intro": "Step the reduction forward and watch which column is being "
                           "cleared and which row is the pivot row. Feed it a system "
                           "whose third equation is the sum of the other two, and watch "
                           "a row of zeros arrive at the bottom.",
        }),
        "steps_title": "Row reducing a matrix",
        "steps_intro": "Four moves, repeated. There is no decision in them beyond which row to swap up.",
        "steps": [
            ("Work the columns left to right",
             "One pivot per column at most, and once a column is cleared it is never "
             "revisited. Jumping about is how entries that were already zero become "
             "nonzero again."),
            ("Get a nonzero entry into the pivot position, then make it 1",
             "Swap a row up if the entry is zero. Divide the pivot row once, at the "
             "pivot, and keep the fractions exact from that point on."),
            ("Clear the rest of the column",
             "Every other row loses its entry in that column: `Ri − (that entry) · "
             "Rpivot`. When the step is done the column holds a single `1` and zeros."),
            ("Stop when the shape is right, then read",
             "Look first for a row `0 0 … 0 | k` with `k ≠ 0`. Then count pivots, name "
             "the free variables, and write the solution set &mdash; a triple, or a "
             "parameter form, or the empty set."),
        ],
        "worked": {
            "title": "Reducing the lesson-4 matrix to the answer",
            "intro": [
                "The same system once more, carried all the way to reduced row echelon "
                "form. Compare the first two operations with lesson 5 and the whole of "
                "it with lesson 4."
            ],
            "lines": [
                "                     1   1   1 |  6",
                "                     2  −1   3 |  9",
                "                    −1   2   4 | 15",
                "",
                "R2 − 2R1 → R2        1   1   1 |  6",
                "R3 +  R1 → R3        0  −3   1 | −3",
                "                     0   3   5 | 21",
                "",
                "R3 +  R2 → R3        1   1   1 |  6",
                "                     0  −3   1 | −3",
                "                     0   0   6 | 18",
                "",
                "(−1/3)R2 → R2        1   1     1 |  6",
                "(1/6)R3  → R3        0   1  −1/3 |  1",
                "                     0   0     1 |  3",
                "",
                "R1 − R2 → R1         1   0   4/3 |  5",
                "                     0   1  −1/3 |  1",
                "                     0   0     1 |  3",
                "",
                "R1 − (4/3)R3 → R1    1   0   0 |  1",
                "R2 + (1/3)R3 → R2    0   1   0 |  2",
                "                     0   0   1 |  3",
                "",
                "x = 1,   y = 2,   z = 3",
            ],
            "after": [
                "The `−1/3` in the middle row is not a mistake and is not worth "
                "avoiding: it cancels two steps later. Replacing it with `−0.33` sends "
                "the final row for `y` to `1.99` and the row for `x` to `1.01`, and the "
                "matrix looks exactly as convincing as the correct one.",
                "Every pivot column ends with a single `1`, so all three variables are "
                "pivot variables, none is free, and there is exactly one solution. That "
                "reading was available three stages earlier, the moment the third row "
                "read `0 0 6 | 18`: three pivots for three variables, and no row of "
                "zeros.",
            ],
        },
        "quiz_title": "Row reduction",
        "quiz": [
            {"q": "A row reduction produces the row `0 0 0 | 4`. The system has:",
             "a": ["the solution `x = 0`, `y = 0`, `z = 4`",
                   "no solution",
                   "infinitely many solutions",
                   "`z = 4`, with two free variables"],
             "c": 1,
             "why": "The row says `0x + 0y + 0z = 4`, and no triple satisfies it. "
                    "Further reduction cannot repair the system; the correct move is to "
                    "stop and report that it is inconsistent."},
            {"q": "A three-variable system reduces to two pivots and one all-zero row, "
                  "with no row of the form `0 0 0 | k` for `k ≠ 0`. How many solutions?",
             "a": ["None", "Exactly one", "Infinitely many, with one free variable",
                   "Exactly two"],
             "c": 2,
             "why": "Three variable columns and two pivots leave one column without a "
                    "pivot, so that variable takes any value and the other two follow. "
                    "The absence of a `0 0 0 | k` row is what guarantees the system is "
                    "consistent in the first place."},
            {"q": "Two students reduce the same augmented matrix by different sequences "
                  "of row operations. Their final reduced row echelon forms:",
             "a": ["may differ, since the routes differ",
                   "are the same",
                   "are the same only if both avoided fractions",
                   "are the same only if neither swapped rows"],
             "c": 1,
             "why": "The reduced form is unique: it depends on the matrix and not on "
                    "the route. Intermediate row echelon forms genuinely do differ, "
                    "which is why the reduced form is the one worth agreeing on."},
        ],
        "mistakes": [
            ("Reducing past an inconsistent row",
             "Once `0 0 0 | 4` has appeared the system has no solution. Continuing "
             "produces a tidy matrix that means nothing, and tidy matrices are "
             "persuasive."),
            ("Rounding a pivot",
             "Dividing by `3` gives thirds, and `0.33` is not a third. The error grows "
             "with every operation that follows, and the final matrix carries no sign "
             "of it &mdash; which is the reason this course insists on exact "
             "fractions."),
            ("Treating a free variable as zero",
             "A column without a pivot means that variable is unrestricted, not that it "
             "equals `0`. Setting it to zero reports one triple out of infinitely many "
             "and hides the shape of the answer entirely."),
        ],
        "standard": ("Finish when you reduce without deciding anything.",
                     "The algorithm contains no choices beyond which row to swap "
                     "upward: leftmost column, pivot, clear, move on. Carry a `3 × 4` "
                     "augmented matrix to reduced row echelon form in exact fractions, "
                     "and name which of the three cases you are in before writing any "
                     "solution down."),
        "note": "Lesson 7 leaves systems for a moment and asks what else can be done "
                "with a matrix: added, scaled, and multiplied. The product is what lets "
                "a whole system be written `Ax = b`, and lessons 8 and 9 answer the "
                "question this lesson leaves open &mdash; which coefficient matrices "
                "give exactly one solution, and whether the answer can be had in one "
                "step instead of ten.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "matrix-arithmetic",
        "title": "Matrix Arithmetic",
        "module": "Matrices",
        "one_line": "Addition, scalar multiples, and the product that is not elementwise.",
        "summary": (
            "Matrices of the same size add entry by entry and scale entry by entry, "
            "which is the easy half. The product is not entrywise: the entry in row `i` "
            "and column `j` of `AB` is built from the whole of row `i` and the whole of "
            "column `j`, and the order of the factors changes the answer."
        ),
        "key": [
            "A + B                       same size, entry by entry",
            "kA                          every entry multiplied by k",
            "A (m × n)  times  B (n × p)  =  AB (m × p)     inner sizes must agree",
            "AB in row i, column j  =  row i of A against column j of B",
        ],
        "key_label": "Three operations, and the shape rule",
        "concepts_intro": (
            "Two of the three operations behave exactly as the notation suggests. The "
            "third does not, and most of this lesson is about the third."
        ),
        "concepts": [
            ("Addition is entrywise and needs matching sizes",
             "`A + B` exists only when `A` and `B` have the same number of rows and the "
             "same number of columns, and then it is what it looks like. Every rule of "
             "addition from course 1 carries over, one position at a time."),
            ("The product runs rows against columns",
             "Multiply each entry of row `i` of `A` by the matching entry of column `j` "
             "of `B` and add the results. The row length of `A` must equal the column "
             "height of `B`, and that requirement is the whole of the shape rule."),
            ("AB and BA are different questions",
             "They can have different sizes; one can exist while the other does not; "
             "and even when both are `n × n` they are usually different matrices. Every "
             "rearrangement that quietly used commutativity has to be re-earned here."),
        ],
        "read_title": "Adding, scaling and multiplying matrices",
        "read_intro": "Two operations that behave, one that does not, and the familiar laws that stop holding.",
        "body": [
            ("def", ("Size and equality",
                     "An `m × n` matrix has `m` rows and `n` columns. Two matrices are "
                     "<strong>equal</strong> when they have the same size and agree in "
                     "every position. There is no notion of two matrices of different "
                     "sizes being equal.")),
            ("def", ("Sum and scalar multiple",
                     "For matrices of the same size, `A + B` is the matrix whose entry "
                     "in each position is the sum of the entries of `A` and `B` in that "
                     "position. For a number `k`, the matrix `kA` has every entry of "
                     "`A` multiplied by `k`.",
                     "A number acting on a matrix this way is called a "
                     "<strong>scalar</strong>, to distinguish it from a `1 × 1` matrix, "
                     "which is a different object.")),
            ("math", [
                "A =   2  −1   0          B =   1   6  −2",
                "      4   3   5                0  −3   1",
                "",
                "A + B =   3   5  −2          3A =    6  −3    0",
                "          4   0   6                 12   9   15",
            ]),
            ("p", "Addition inherits everything from the numbers, position by position: "
                  "`A + B = B + A`, `(A + B) + C = A + (B + C)`, the zero matrix of the "
                  "right size adds nothing, and `A + (−A)` is that zero matrix. Nothing "
                  "here requires attention."),
            ("h3", "The product"),
            ("def", ("Matrix product",
                     "Let `A` be `m × n` and `B` be `n × p`. The product `AB` is the "
                     "`m × p` matrix whose entry in row `i`, column `j` is "
                     "`a₁b₁ + a₂b₂ + … + aₙbₙ`, where `a₁, …, aₙ` is row `i` of `A` and "
                     "`b₁, …, bₙ` is column `j` of `B`.",
                     "If the row length of `A` is not the column height of `B`, the "
                     "product does not exist. It is not zero and it is not "
                     "approximately anything: there is no such matrix.")),
            ("p", "The shape rule is easier to use than to state. Write the two sizes "
                  "side by side, `(m × n)(n × p)`. If the inner pair match, they cancel "
                  "and the outer pair give the size of the answer. If they do not "
                  "match, stop."),
            ("math", [
                "C =   1   2   0          D =    2    1",
                "      3  −1   4                 0   −3",
                "                                5    2",
                "",
                "C is 2 × 3,  D is 3 × 2   →   CD is 2 × 2",
                "",
                "row 1, col 1 :   1(2)  +  2(0)   +  0(5)  =   2",
                "row 1, col 2 :   1(1)  +  2(−3)  +  0(2)  =  −5",
                "row 2, col 1 :   3(2)  + (−1)(0) +  4(5)  =  26",
                "row 2, col 2 :   3(1)  + (−1)(−3) + 4(2)  =  14",
                "",
                "CD =    2  −5             DC exists too, and is 3 × 3",
                "       26  14",
            ]),
            ("p", "The definition looks arbitrary until a system is written with it. "
                  "Take the coefficient matrix of the lesson-4 system, a column of the "
                  "three unknowns, and a column of the three constants. The product of "
                  "the first two is a column whose entries are the left-hand sides of "
                  "the three equations, so the whole system is the single statement "
                  "`Ax = b`."),
            ("math", [
                " 1   1   1     x            6",
                " 2  −1   3     y     =      9",
                "−1   2   4     z           15",
                "",
                "at (1, 2, 3):    1(1) + 1(2) + 1(3)  =   6    ✓",
                "                 2(1) − 1(2) + 3(3)  =   9    ✓",
                "                −1(1) + 2(2) + 4(3)  =  15    ✓",
            ]),
            ("thm", ("What survives, and what does not",
                     "Matrix multiplication is associative, `(AB)C = A(BC)`, and "
                     "distributes over addition on both sides: `A(B + C) = AB + AC` and "
                     "`(A + B)C = AC + BC`. Scalars pull out: `k(AB) = (kA)B = A(kB)`.",
                     "Commutativity fails. `AB` and `BA` need not be equal, need not "
                     "have the same size, and need not both exist. Nothing in the "
                     "notation warns you, so the order must be preserved in every step "
                     "of every rearrangement.")),
            ("def", ("Identity matrix",
                     "`Iₙ` is the `n × n` matrix with `1` in every position on the main "
                     "diagonal and `0` everywhere else. It satisfies `IA = A` and "
                     "`AI = A` whenever the sizes allow, which is what makes it the "
                     "matrix analogue of the number `1`.")),
            ("example", ("A product of two nonzero matrices that is zero",
                         "Let `P` have rows `(1, 1)` and `(1, 1)`, and let `Q` have "
                         "rows `(1, −1)` and `(−1, 1)`. Each entry of `PQ` is either "
                         "`1(1) + 1(−1)` or `1(−1) + 1(1)`, so all four are `0` and "
                         "`PQ` is the zero matrix while neither factor is zero.",
                         "The zero-product property that solves every quadratic in "
                         "course 6 is a fact about numbers. It does not hold here, and "
                         "no argument that depends on it may be used on matrices.")),
            ("p", "Cancellation fails for the same reason. From `AB = AC` you may not "
                  "conclude `B = C`: with `A` having rows `(1, 0)` and `(0, 0)`, `B` "
                  "having rows `(1, 2)` and `(3, 4)`, and `C` having rows `(1, 2)` and "
                  "`(9, 9)`, both products have rows `(1, 2)` and `(0, 0)` while `B` "
                  "and `C` are plainly different. Lesson 9 says exactly which matrices "
                  "may be cancelled, and why most may not."),
        ],
        "lab": ("matrix", {
            "mode": "arith",
            "panel_title": "Multiply two matrices",
            "panel_intro": "Set the two sizes first: the lab refuses a product whose "
                           "inner dimensions disagree, which is the shape rule delivered "
                           "as an error message. Then swap the factors and compare `AB` "
                           "with `BA`.",
        }),
        "steps_title": "Computing a product",
        "steps_intro": "Four moves. The first one is written down, not done in your head.",
        "steps": [
            ("Check the sizes and write down the size of the answer",
             "`(m × n)(n × p)` gives `m × p`. If the inner numbers differ there is "
             "nothing to compute, and \"the product does not exist\" is the complete "
             "answer."),
            ("Take one row and one column at a time",
             "For the entry in row `i`, column `j`, run along row `i` of the left "
             "matrix and down column `j` of the right one, multiplying in pairs. Say "
             "the position out loud before starting it."),
            ("Add the products and place the entry",
             "The number of products equals the shared inner dimension, so an inner "
             "dimension of `3` means three products every time. Counting them is a free "
             "check on whether a term was skipped."),
            ("Never assume AB equals BA",
             "If the question asks for `BA`, compute `BA`. Swapping the factors is not "
             "a simplification; it is a different calculation with a different answer."),
        ],
        "worked": {
            "title": "AB and BA for two 2 by 2 matrices",
            "intro": [
                "Both matrices are `2 × 2`, so both products exist and both are "
                "`2 × 2`. They are still not the same matrix."
            ],
            "lines": [
                "A =   1   2           B =   0   1",
                "      3   4                 1   0",
                "",
                "AB row 1 :   1(0) + 2(1) = 2        1(1) + 2(0) = 1",
                "AB row 2 :   3(0) + 4(1) = 4        3(1) + 4(0) = 3",
                "",
                "AB =   2   1",
                "       4   3",
                "",
                "BA row 1 :   0(1) + 1(3) = 3        0(2) + 1(4) = 4",
                "BA row 2 :   1(1) + 0(3) = 1        1(2) + 0(4) = 2",
                "",
                "BA =   3   4",
                "       1   2",
            ],
            "after": [
                "`B` here is a swapper. Multiplying `A` on the right by it exchanged the "
                "columns of `A`; multiplying on the left exchanged the rows. That is a "
                "fair picture of the general situation &mdash; which side you multiply "
                "on decides whether rows or columns are acted on &mdash; and it is why "
                "the order is part of the expression rather than a detail of how it was "
                "written down.",
                "Neither product is the entrywise one, which would have been `0`, `2`, "
                "`3`, `0`. That matrix is not `AB`, is not `BA`, and answers no question "
                "asked in this course.",
            ],
        },
        "quiz_title": "Matrix arithmetic",
        "quiz": [
            {"q": "`A` is `2 × 3` and `B` is `3 × 4`. Which products are defined?",
             "a": ["`AB` only, and it is `2 × 4`",
                   "`BA` only, and it is `3 × 3`",
                   "Both, and both are `2 × 4`",
                   "Neither"],
             "c": 0,
             "why": "For `AB` the inner numbers are `3` and `3`, which agree, leaving "
                    "the outer pair `2 × 4`. For `BA` they are `4` and `2`, which do "
                    "not agree, so `BA` does not exist &mdash; it is not zero, it is "
                    "undefined."},
            {"q": "`A` has rows `(1, 2)` and `(3, 4)`; `B` has rows `(5, 6)` and "
                  "`(7, 8)`. The entry of `AB` in row 2, column 1 is:",
             "a": ["`15`", "`19`", "`21`", "`43`"],
             "c": 3,
             "why": "Row 2 of `A` is `(3, 4)` and column 1 of `B` is `(5, 7)`, so the "
                    "entry is `3(5) + 4(7) = 43`. `19` is the row 1, column 1 entry, "
                    "which is what using the first row instead of the second gives; "
                    "`21` is the entrywise product `3 × 7`; `15` is the first of the "
                    "two products with the second forgotten."},
            {"q": "`AB` is the zero matrix. What follows?",
             "a": ["`A = 0` or `B = 0`",
                   "Nothing: two nonzero matrices can have a zero product",
                   "`A` and `B` have the same size",
                   "`BA` is the zero matrix as well"],
             "c": 1,
             "why": "The matrix with rows `(1, 1)`, `(1, 1)` times the matrix with rows "
                    "`(1, −1)`, `(−1, 1)` is zero with neither factor zero. `BA` need "
                    "not vanish either: for `A` with rows `(1, 0)`, `(0, 0)` and `B` "
                    "with rows `(0, 0)`, `(1, 0)`, `AB` is zero and `BA` is not."},
        ],
        "mistakes": [
            ("Multiplying entry by entry",
             "The matrix of products of matching entries is a real operation with real "
             "uses, and it is not `AB`. For the two matrices in the worked example it "
             "would give `0`, `2`, `3`, `0`, which is neither product."),
            ("Cancelling a matrix from both sides",
             "`AB = AC` does not give `B = C`, because `A` may destroy the difference "
             "between `B` and `C`. Cancellation is legal only for the matrices lesson 9 "
             "identifies, and assuming it earlier produces answers that survive every "
             "check except a numerical one."),
            ("Assuming AB exists because BA does",
             "A `3 × 2` times a `2 × 5` is fine; the same two matrices in the other "
             "order pair `5` against `3` and there is no product at all. Write the two "
             "sizes down before reaching for the arithmetic."),
        ],
        "standard": ("Finish when the size of the answer is the first thing you write.",
                     "Before computing a single entry, write `m × p` down. It catches an "
                     "impossible product before any arithmetic happens, it tells you how "
                     "many entries you owe, and it is the habit that makes `Ax = b` in "
                     "lesson 9 read as one equation rather than as three."),
        "note": "Writing a system as `Ax = b` invites the obvious move: divide by `A`. "
                "There is no division of matrices, but there is sometimes a matrix "
                "`A⁻¹` with `A⁻¹A = I`, and then `x = A⁻¹b`. Lesson 8 produces the "
                "single number that decides whether such a matrix exists, and lesson 9 "
                "constructs it by row reduction &mdash; which is the reason this course "
                "did lesson 6 first.",
    },
]
