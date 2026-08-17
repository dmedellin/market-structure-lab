"""Course 2, lessons 01-07 — solving linear equations, and the moves that are allowed."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "what-it-means-to-solve-an-equation",
        "title": "What It Means to Solve an Equation",
        "module": "Equations",
        "one_line": "A solution is a value that makes the statement true.",
        "summary": (
            "An equation is a statement that two expressions are equal, and it is neither "
            "true nor false until the variable has a value. A solution is a value that "
            "makes it true, and substitution is the only thing that settles it. Solving is "
            "a chain of moves chosen so that the set of values passing that test never "
            "changes."
        ),
        "key": [
            "3x − 4 = 11    at x = 5:      3·5 − 4 = 11      TRUE    5 is a solution",
            "               at x = 4:      3·4 − 4 = 8       FALSE   4 is not",
            "3x = 1         at x = 0.333:  999/1000 ≠ 1      FALSE",
            "               at x = 1/3:    1 = 1             TRUE",
        ],
        "key_label": "A value is tested, not guessed",
        "concepts_intro": (
            "Everything on this course rests on one definition, and the definition is "
            "about truth rather than about procedure."
        ),
        "concepts": [
            ("An equation is a statement that can be true or false",
             "`3x − 4 = 11` claims that two expressions have the same value. Until `x` is "
             "given a value the claim is neither true nor false &mdash; it is waiting. "
             "That is the whole difference between an equation and an expression: "
             "`3x − 4` on its own has nothing to be true about."),
            ("A solution is a value that makes the statement true",
             "It is not \"whatever comes out of the procedure\". The procedure is a fast "
             "way of producing a candidate; substitution is what decides whether the "
             "candidate is a solution. Those are two different jobs and later lessons "
             "will produce candidates that fail."),
            ("Solving is a chain of equations with the same solutions",
             "Every legal move replaces an equation by another one with exactly the same "
             "solution set. That is the only reason the last line of the working, `x = 5`, "
             "says anything at all about the first."),
        ],
        "read_title": "Statements, solutions, and equivalence",
        "read_intro": "What an equation claims, what a solution is, and which moves are guaranteed to keep one.",
        "body": [
            ("def", ("Equation, solution, solution set",
                     "An <strong>equation</strong> is a statement that two expressions are "
                     "equal. A <strong>solution</strong> of an equation in `x` is a number "
                     "which, written in place of every `x`, makes the statement true. The "
                     "<strong>solution set</strong> is the set of all such numbers.",
                     "To <strong>solve</strong> an equation is to find its solution set "
                     "&mdash; all of it, and nothing that does not belong in it.")),
            ("p", "An expression such as `3x − 4` names a number as soon as `x` is known. "
                  "An equation such as `3x − 4 = 11` makes a claim about two such names. "
                  "Only the second kind of thing can be true or false, and only the second "
                  "kind of thing can be solved."),
            ("h3", "Checking a value"),
            ("p", "To test a candidate: substitute it into the <em>original</em> equation, "
                  "evaluate the left side down to one number, evaluate the right side down "
                  "to one number, and compare. Each side is worked on alone. Nothing "
                  "crosses the equals sign during a check, because a check is not a "
                  "solve."),
            ("math", [
                "3x − 4 = 11        test x = 5",
                "        left    3·5 − 4  =  15 − 4  =  11",
                "        right   11",
                "        11 = 11                TRUE",
                "",
                "3x − 4 = 11        test x = 4",
                "        left    3·4 − 4  =  12 − 4  =  8",
                "        right   11",
                "        8 ≠ 11                 FALSE",
            ]),
            ("p", "The second test is as informative as the first. It establishes "
                  "something definite: `4` is not a solution. \"Not a solution\" is a "
                  "result, and most of the values you will ever test are of that kind."),
            ("h3", "Exact arithmetic, and why it is not fussiness"),
            ("p", "`0.333` and `1/3` are different numbers. The first is `333/1000`. Put "
                  "each into `3x = 1` and the difference shows up immediately:"),
            ("math", [
                "3 · 333/1000  =  999/1000        999/1000 ≠ 1      FALSE",
                "3 · 1/3       =  1               1 = 1             TRUE",
            ]),
            ("p", "So `x = 0.333` is not a solution of `3x = 1`, and no amount of rounding "
                  "makes it one. This is why every answer on this course is written as an "
                  "exact fraction. A decimal that happens to terminate, such as `0.25`, is "
                  "exact and perfectly acceptable; a decimal that has been cut short is a "
                  "different number wearing the answer's clothes."),
            ("def", ("Equivalent equations",
                     "Two equations are <strong>equivalent</strong> when they have exactly "
                     "the same solution set.",
                     "`3x − 4 = 11`, `3x = 15` and `x = 5` are three equivalent equations. "
                     "The third is the useful one only because it is equivalent to the "
                     "first.")),
            ("thm", ("The two properties of equality",
                     "If `a = b`, then `a + c = b + c` for any number `c`.",
                     "If `a = b`, then `ac = bc` for any number `c`; and if `c ≠ 0`, then "
                     "`a/c = b/c` as well.",
                     "Applied to both sides of an equation, adding or subtracting any "
                     "number, and multiplying or dividing by any <em>nonzero</em> number, "
                     "produce an equivalent equation.")),
            ("p", "The reason those moves are safe is that each one can be undone by "
                  "another move of the same kind. Adding `4` is undone by subtracting `4`; "
                  "multiplying by `3` is undone by dividing by `3`. A move that can be "
                  "reversed cannot lose a solution, because the reverse move would have to "
                  "put it back, and it cannot invent one either, for the same reason."),
            ("p", "Multiplying by zero is the move that fails this test, and it fails "
                  "loudly. From `2x = 6`, multiplying both sides by `0` gives `0 = 0` "
                  "&mdash; a statement that is true for every value of `x`. The original "
                  "was true for one value only. Nothing can undo the multiplication, and "
                  "the information is gone. That is why the theorem says `c ≠ 0` and why "
                  "the restriction is not decoration."),
            ("example", ("What a single check does and does not establish",
                         "Substituting `x = 5` into `3x − 4 = 11` and getting `11 = 11` "
                         "proves that `5` is a solution. It proves nothing whatever about "
                         "whether there are others. For this equation there are none, but "
                         "that is a separate argument &mdash; it comes from the chain of "
                         "equivalent equations, and lesson 6 states it exactly.")),
        ],
        "lab": ("equation", {
            "mode": "check",
            "panel_title": "Substitute, then read the verdict",
            "panel_intro": "Type an equation and one value. The lab evaluates each side at "
                           "that value in exact fractions and reports true or false; it "
                           "never solves anything. Run `3x = 1` at `0.333`, then at `1/3`.",
        }),
        "steps_title": "Testing a candidate value",
        "steps_intro": "Four moves, none of which involves solving anything.",
        "steps": [
            ("Write the original equation out again",
             "Not the third line of your working. If an earlier step was wrong, a check "
             "against that line will happily confirm a wrong answer, which is precisely "
             "the failure a check exists to catch."),
            ("Substitute the value everywhere the variable appears",
             "Every occurrence, and put brackets round the value whenever it is negative "
             "or a fraction: `3(−2) − 4`, never `3−2 − 4`. The missing bracket is the "
             "commonest way a correct answer fails its own check."),
            ("Evaluate the two sides separately, in exact arithmetic",
             "Left side to a single number; right side to a single number. Fractions stay "
             "fractions. Nothing moves across the equals sign, because at this point there "
             "is nothing to rearrange."),
            ("Compare the two numbers and state which it is",
             "Equal means the value is a solution of this equation. Unequal means it is "
             "not. Report the outcome either way; a failed check is a finding, not a "
             "dead end."),
        ],
        "worked": {
            "title": "Four checks, two of them failures",
            "intro": ["Nothing here is solved. Each line takes a value that has been "
                      "handed to it and asks whether the statement is true."],
            "lines": [
                "1.  3x − 4 = 11      x = 5",
                "        left    3·5 − 4  =  11          right   11",
                "        11 = 11      TRUE       5 is a solution",
                "",
                "2.  3x − 4 = 11      x = 4",
                "        left    3·4 − 4  =  8           right   11",
                "        8 ≠ 11       FALSE      4 is not a solution",
                "",
                "3.  3x = 1           x = 0.333  =  333/1000",
                "        left    3 · 333/1000  =  999/1000       right   1",
                "        999/1000 ≠ 1      FALSE",
                "",
                "4.  3x = 1           x = 1/3",
                "        left    3 · 1/3  =  1                   right   1",
                "        1 = 1        TRUE       1/3 is a solution",
            ],
            "after": [
                "Line 3 is the one worth sitting with. `0.333` is a good approximation to "
                "`1/3` and it is not a solution of `3x = 1`, because the definition asks "
                "for a value that makes the statement true and `999/1000 = 1` is false. "
                "Approximation is a separate subject with its own rules; solving is not "
                "part of it.",
                "Lines 1 and 4 each establish exactly one thing: that particular value "
                "passes. Whether any other value also passes is a question these checks do "
                "not touch.",
            ],
        },
        "quiz_title": "Solutions and checks",
        "quiz": [
            {"q": "Which value makes `5x + 2 = 17` true?",
             "a": ["`x = 3`", "`x = 19/5`", "`x = 15`", "`x = 17/5`"],
             "c": 0,
             "why": "`5·3 + 2 = 17`. `19/5` comes from adding 2 to both sides instead of "
                    "subtracting it; `15` from reading the equation as `x + 2 = 17` and "
                    "ignoring the coefficient; `17/5` from dividing by 5 and forgetting "
                    "the `+ 2` altogether."},
            {"q": "Is `x = 0.333` a solution of `3x = 1`?",
             "a": ["Yes, because `0.333` rounds to `1/3`",
                   "No: `3 · 0.333 = 0.999`, and `0.999 ≠ 1`",
                   "Yes, because `0.333` and `1/3` are the same number",
                   "It cannot be decided without a calculator"],
             "c": 1,
             "why": "The test is whether the statement comes out true, and it does not: "
                    "`999/1000` is not `1`. `0.333` and `1/3` are different numbers, which "
                    "is why one of them solves the equation and the other does not."},
            {"q": "Both sides of `2x = 6` are multiplied by `0`. What is the result?",
             "a": ["`0 = 0`, which is true for every `x` &mdash; the move destroyed the information",
                   "`x = 0`",
                   "`2x = 0`, so `x = 0`",
                   "`0 = 6`, so there is no solution"],
             "c": 0,
             "why": "Both sides become `0`, and `0 = 0` is true whatever `x` is. The move "
                    "cannot be undone &mdash; dividing by `0` is not available &mdash; so "
                    "it is not on the list of legal moves. The multiplication property "
                    "requires a nonzero multiplier for exactly this reason."},
        ],
        "mistakes": [
            ("Checking against your own working rather than the original equation",
             "If line 3 already contains a slip, your answer will satisfy line 3 and the "
             "check will pass. Substituting into the equation as it was given is the only "
             "version that catches an error made along the way."),
            ("Reporting a rounded decimal as the solution",
             "`x = 0.333` fails the test that `x = 1/3` passes. Round at the end of a "
             "physical calculation if you must; never inside an algebraic answer."),
            ("Running the equals sign as a connective between steps",
             "Writing `3x − 4 = 11 = 15 = 5` claims that `11`, `15` and `5` are the same "
             "number. Each step is its own equation and belongs on its own line, and "
             "keeping them separate is what makes the chain of equivalences readable."),
        ],
        "standard": ("Finish when you can decide, in exact arithmetic, whether a given number is a solution.",
                     "Handed any equation and any candidate you should substitute into the "
                     "original, evaluate both sides in fractions, and report true or false "
                     "without hesitating &mdash; and you should be able to say why "
                     "multiplying both sides by zero is not on the list of legal moves. "
                     "Every lesson from here produces candidates; this is how you find out "
                     "what they are worth."),
        "note": "Lesson 2 starts producing candidates instead of testing them, using "
                "exactly the two properties stated above. Notice that the properties never "
                "mention `x`: they are facts about numbers, and that is why they apply to "
                "whatever the two sides of your equation happen to be.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "one-and-two-step-equations",
        "title": "One- and Two-Step Equations",
        "module": "Equations",
        "one_line": "Undoing operations in the reverse of the order they were applied.",
        "summary": (
            "An expression like `3x − 4` is built from `x` by a sequence of operations, and "
            "isolating `x` means undoing them in the opposite order. Every step is one "
            "operation applied to both sides, and the answer is an exact fraction, checked "
            "in the original equation."
        ),
        "key": [
            "3x − 4 = 11     x was multiplied by 3,   then 4 was subtracted",
            "                so undo in reverse:      add 4,   then divide by 3",
            "",
            "3x − 4 = 11  →  3x = 15  →  x = 5        check:  3·5 − 4 = 11",
        ],
        "key_label": "Last operation applied, first operation undone",
        "concepts_intro": (
            "There is one idea here and it is borrowed from the order of operations: what "
            "was done last has to be undone first."
        ),
        "concepts": [
            ("Each step is one named operation applied to both sides",
             "\"Add 4 to both sides\", \"divide both sides by 3\". If you cannot name the "
             "operation you are performing, you cannot check that it is one of the legal "
             "ones, and the step is a guess."),
            ("Undo in the reverse of the order the operations were applied",
             "`3x − 4` multiplies by 3 and then subtracts 4. Reversing that means adding 4 "
             "and then dividing by 3. This is the order of operations run backwards, and "
             "it is the only thing you have to remember."),
            ("The coefficient carries its sign into the division",
             "From `−2x = 12` the last move is division by `−2`, not by `2`. Dropping the "
             "sign here produces `6` instead of `−6` and the check catches it &mdash; but "
             "only if you do the check."),
        ],
        "read_title": "Isolating the variable",
        "read_intro": "The one-step shapes, the two-step routine, and what to do when the answer is not a whole number.",
        "body": [
            ("p", "Read `3x − 4` as a recipe applied to `x`: multiply by 3, then subtract "
                  "4. Solving reverses the recipe. Because the subtraction happened last, "
                  "it is undone first. The four one-step equations are the recipe with a "
                  "single instruction in it, and each is undone by the one operation that "
                  "reverses it, applied to both sides:"),
            ("math", [
                "x + 7 = 2       subtract 7 from both sides     x = −5",
                "x − 7 = 2       add 7 to both sides            x = 9",
                "7x    = 2       divide both sides by 7         x = 2/7",
                "x/7   = 2       multiply both sides by 7       x = 14",
            ]),
            ("p", "The third line is the one people rewrite. `x = 2/7` is a finished "
                  "answer. Turning it into `0.2857` makes it a different number, and "
                  "lesson 1 showed what happens to a different number in the check."),
            ("h3", "Two steps"),
            ("p", "With both a coefficient and a constant, deal with the constant first:"),
            ("math", [
                "3x − 4 = 11",
                "     add 4 to both sides        3x = 15",
                "     divide both sides by 3      x = 5",
                "",
                "check    3·5 − 4  =  15 − 4  =  11         and the right side is 11",
            ]),
            ("p", "Doing it the other way round is legal and gives the same answer with "
                  "worse arithmetic: dividing first turns `3x − 4 = 11` into "
                  "`x − 4/3 = 11/3`, and then adding `4/3` gives `x = 15/3 = 5`. The "
                  "constant-first order is a convention chosen because it postpones "
                  "fractions, not because the other route is wrong."),
            ("h3", "Brackets"),
            ("p", "`2(x + 3) = 14` can be started in either of two ways, and both are "
                  "legal moves on the whole side:"),
            ("math", [
                "2(x + 3) = 14      divide both sides by 2      x + 3 = 7     x = 4",
                "2(x + 3) = 14      distribute first            2x + 6 = 14   x = 4",
            ]),
            ("p", "What does not work is subtracting 3 from both sides in the hope of "
                  "stripping the bracket. The move itself is legal &mdash; the addition "
                  "property allows any number &mdash; but it does not do what it looks "
                  "like it does. The `3` is inside the bracket, so it is not a term of "
                  "the left side; the left side is a single product. Subtracting 3 from "
                  "`2(x + 3)` gives `2(x + 3) − 3`, that is `2x + 3`, not `2x`."),
            ("h3", "Negative coefficients"),
            ("p", "The coefficient is the number multiplying `x`, and its sign belongs to "
                  "it:"),
            ("math", [
                "7 − 2x = 19",
                "     subtract 7 from both sides      −2x = 12",
                "     divide both sides by −2           x = −6",
                "",
                "check    7 − 2·(−6)  =  7 + 12  =  19",
            ]),
            ("thm", ("What the last step needs",
                     "An equation of the form `px = q` with `p ≠ 0` has exactly one "
                     "solution, `x = q/p`.",
                     "Division by `p` is legal because `p ≠ 0`, and it is reversible, so "
                     "the solution set does not change. What happens when `p = 0` is the "
                     "subject of lesson 6.")),
            ("example", ("A fraction that is the answer",
                         "`(3/4)x + 1/2 = 5/4`. Subtract `1/2` from both sides: "
                         "`(3/4)x = 3/4`, since `5/4 − 1/2 = 5/4 − 2/4 = 3/4`. Divide both "
                         "sides by `3/4`: `x = 1`. Lesson 4 shows a route through this "
                         "kind of equation that avoids fractional arithmetic entirely.")),
        ],
        "lab": ("equation", {
            "mode": "solve",
            "panel_title": "One operation per row",
            "panel_intro": "Type any linear equation. Each row of the trace is a single "
                           "operation applied to both sides, named as it happens, and the "
                           "last table puts the answer back into the equation exactly as "
                           "you typed it.",
        }),
        "steps_title": "Solving a one- or two-step equation",
        "steps_intro": "Simplify before you undo anything; then undo in reverse order.",
        "steps": [
            ("Simplify each side on its own",
             "Multiply out brackets and combine like terms, left side and right side "
             "separately. You cannot reliably see which operations were applied to `x` "
             "until each side is a tidy expression."),
            ("Undo the addition or subtraction first",
             "Whatever constant is attached to the variable term, remove it by doing the "
             "opposite to both sides. It was applied last, so it comes off first."),
            ("Divide both sides by the coefficient, sign included",
             "`−2x = 12` becomes `x = −6`. Write the answer as an exact fraction if it is "
             "not a whole number: `x = 7/3`, not `2.33`."),
            ("Substitute the answer into the original equation",
             "Both sides, evaluated separately, must come out to the same number. This is "
             "the step that turns a candidate into an answer, and it takes about ten "
             "seconds."),
        ],
        "worked": {
            "title": "Three equations, each with its check",
            "intro": ["Every row names the operation that produced it."],
            "lines": [
                "A.  3x − 4 = 11",
                "        + 4 both sides       3x = 15",
                "        ÷ 3 both sides        x = 5",
                "    check   3·5 − 4 = 11      right side 11        agrees",
                "",
                "B.  7 − 2x = 19",
                "        − 7 both sides      −2x = 12",
                "        ÷ (−2) both sides     x = −6",
                "    check   7 − 2·(−6) = 7 + 12 = 19               agrees",
                "",
                "C.  x/4 + 3 = 1",
                "        − 3 both sides      x/4 = −2",
                "        × 4 both sides        x = −8",
                "    check   (−8)/4 + 3 = −2 + 3 = 1                agrees",
            ],
            "after": [
                "In B the division is by `−2`, and it is the only place the sign can be "
                "lost. Dividing by `2` instead gives `x = 6`, and the check then reads "
                "`7 − 12 = −5`, which is not `19`. The error is invisible in the working "
                "and obvious in the check.",
                "In C the bracket in `(−8)/4` matters when you write the check out. "
                "Substituting a negative value without brackets is how a correct answer "
                "gets rejected by its own verification.",
            ],
        },
        "quiz_title": "Undoing operations",
        "quiz": [
            {"q": "Solve `4x + 9 = 1`.",
             "a": ["`x = −2`", "`x = 5/2`", "`x = 2`", "`x = −35/4`"],
             "c": 0,
             "why": "Subtract 9: `4x = −8`; divide by 4: `x = −2`. `5/2` comes from adding "
                    "9 instead of subtracting it; `2` from losing the sign in the "
                    "division; `−35/4` from dividing by 4 first but leaving the `9` "
                    "undivided."},
            {"q": "Solve `7 − 2x = 19`.",
             "a": ["`x = −6`", "`x = 6`", "`x = −13`", "`x = 13`"],
             "c": 0,
             "why": "Subtracting 7 gives `−2x = 12`, and dividing by `−2` gives `−6`. "
                    "Dividing by `2` gives `6` and loses the coefficient's sign. Writing "
                    "`−2x = 19 + 7` in place of `19 − 7` gives `−2x = 26`, and then `−13` "
                    "or `13` according to whether the sign survives the division."},
            {"q": "Which of these first lines of working on `2(x + 3) = 14` is wrong?",
             "a": ["Divide both sides by 2, giving `x + 3 = 7`",
                   "Multiply out the bracket, giving `2x + 6 = 14`",
                   "Subtract 3 from both sides, giving `2x = 11`",
                   "Subtract 14 from both sides, giving `2(x + 3) − 14 = 0`"],
             "c": 2,
             "why": "Subtracting 3 from both sides is a legal move, but it does not give "
                    "`2x = 11`. The `3` sits inside a product, so it is not a term of the "
                    "left side: subtracting 3 from `2(x + 3)` leaves `2x + 6 − 3`, that is "
                    "`2x + 3`, so the line should read `2x + 3 = 11`. The other three "
                    "lines are correct &mdash; the first reaches `x = 4` in one more "
                    "step and the second in two more, and subtracting 14 is valid but "
                    "gets no closer to an answer."},
        ],
        "mistakes": [
            ("Applying the operation to one side only",
             "Going from `3x − 4 = 11` to `3x = 11` adds 4 on the left and nothing on the "
             "right. The property of equality says both sides, and the two sides stop "
             "being equal the moment you treat them differently."),
            ("Dividing by the coefficient without its sign",
             "`−2x = 12` gives `x = −6`. The minus is part of the number you are dividing "
             "by, not a decoration on the term, and this is the single most common "
             "arithmetic slip in the lesson."),
            ("Rounding an exact answer to a decimal",
             "`x = 7/3` is the answer; `2.33` is a nearby number that fails the check. "
             "Fractions are exact, they are not harder to substitute, and the rest of this "
             "path expects them."),
        ],
        "standard": ("Finish when you can name every operation you apply and check the result without being asked.",
                     "Given a two-step equation you should reach the answer in two named "
                     "moves, keep the sign of a negative coefficient, write the result as "
                     "an exact fraction, and substitute it back into the original as a "
                     "matter of habit. Everything in lessons 3 to 5 adds new opening moves "
                     "and finishes exactly like this."),
        "note": "The lab shows one operation per row on purpose. When an equation goes "
                "wrong it is almost never the strategy that failed &mdash; it is one row, "
                "and a trace where every row is named tells you which one. Lesson 3 adds "
                "the only genuinely new move on the course: subtracting a variable term.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "variables-on-both-sides",
        "title": "Variables on Both Sides",
        "module": "Equations",
        "one_line": "Collecting the unknown on one side without losing a sign.",
        "summary": (
            "When `x` appears on both sides, no amount of arithmetic on one side alone will "
            "finish the job. The new move is to subtract a whole variable term from both "
            "sides, which is the addition property with an expression in place of a number, "
            "and the side you collect on is your choice."
        ),
        "key": [
            "5x + 2 = 3x − 8     subtract 3x     2x + 2 = −8      x collected left",
            "5x + 2 = 3x − 8     subtract 5x          2 = −2x − 8  x collected right",
            "",
            "both routes end at x = −5;  the side you pick only decides a sign",
        ],
        "key_label": "One equation, two legal routes",
        "concepts_intro": (
            "The move that makes this work is not new. What is new is applying it to "
            "something that contains the variable."
        ),
        "concepts": [
            ("A variable term can be subtracted from both sides like any other quantity",
             "Once `x` has a value, `3x` is a number. The addition property of equality "
             "was stated for numbers and it never asked where the number came from, so "
             "\"subtract `3x` from both sides\" is the same licence as \"subtract 4 from "
             "both sides\"."),
            ("Which side you collect on is free",
             "Both choices give the same solution. Collecting on the side that already has "
             "the larger coefficient leaves you dividing by a positive number at the end, "
             "which is worth a few seconds of thought before you start."),
            ("Simplify each side completely before moving anything across",
             "Brackets multiplied out, like terms combined, on both sides. Moving a term "
             "out of an unsimplified side is how a term gets counted twice or dropped."),
        ],
        "read_title": "Getting the unknown onto one side",
        "read_intro": "Why the move is legal, why either direction works, and the sign that goes wrong.",
        "body": [
            ("p", "`5x + 2 = 3x − 8` cannot be finished by lesson 2's routine. Undoing the "
                  "`+ 2` leaves `5x = 3x − 10`, which still has `x` in two places. "
                  "Something has to remove one of them."),
            ("thm", ("Subtracting an expression from both sides",
                     "If `A = B` then `A − C = B − C`, whatever expression `C` is.",
                     "For any particular value of `x`, `A`, `B` and `C` are numbers, and "
                     "the statement is then the ordinary addition property of equality. "
                     "The move is reversible &mdash; add `C` back &mdash; so the solution "
                     "set is unchanged.")),
            ("p", "Take `C = 3x` and the equation loses its right-hand variable term:"),
            ("math", [
                "5x + 2 = 3x − 8",
                "     − 3x both sides       2x + 2 = −8",
                "     − 2  both sides       2x     = −10",
                "     ÷ 2  both sides        x     = −5",
                "",
                "check    left   5·(−5) + 2  =  −25 + 2  =  −23",
                "         right  3·(−5) − 8  =  −15 − 8  =  −23",
            ]),
            ("p", "Now the same equation collecting on the right instead. Subtract `5x` "
                  "from both sides:"),
            ("math", [
                "5x + 2 = 3x − 8",
                "     − 5x both sides       2  = −2x − 8",
                "     + 8  both sides      10  = −2x",
                "     ÷ (−2) both sides    −5  = x",
            ]),
            ("p", "Same answer, one extra sign to keep track of. `−5 = x` and `x = −5` say "
                  "the same thing; an equation may be read in either direction."),
            ("h3", "Choosing the side"),
            ("p", "Subtract the smaller of the two coefficients and the one that survives "
                  "is positive. In `3x − 7 = 8x + 3` the coefficients are `3` and `8`, so "
                  "subtracting `3x` leaves `−7 = 5x + 3` and a division by `+5`. "
                  "Subtracting `8x` leaves `−5x − 7 = 3` and a division by `−5`. Both are "
                  "correct; one has fewer places to lose a minus sign."),
            ("h3", "Simplify first"),
            ("p", "Brackets and like terms come before any collecting, and the minus sign "
                  "in front of a bracket reaches every term inside it:"),
            ("math", [
                "2(x − 3) + 4 = 3(x + 1) − 5",
                "     left    2x − 6 + 4  =  2x − 2",
                "     right   3x + 3 − 5  =  3x − 2",
                "",
                "     2x − 2 = 3x − 2",
                "     − 2x both sides      −2 = x − 2",
                "     + 2  both sides       0 = x",
                "",
                "check    left   2(0 − 3) + 4  =  −6 + 4  =  −2",
                "         right  3(0 + 1) − 5  =  3 − 5   =  −2",
            ]),
            ("p", "`x = 0` is a solution like any other. It is a specific number that makes "
                  "the statement true, and it is not the same as \"no solution\" &mdash; a "
                  "confusion lesson 6 exists to clear up."),
            ("p", "The subtraction trap is `3x − (x − 4)`. The minus applies to the whole "
                  "bracket: `3x − x + 4 = 2x + 4`. Writing `3x − x − 4` changes the "
                  "equation, and it is the error most likely to survive unnoticed, because "
                  "the answer it produces looks perfectly ordinary."),
            ("example", ("When every x disappears",
                         "Collecting on `6x + 1 = 6x − 4` gives `1 = −4`, with no `x` left "
                         "anywhere. Nothing has gone wrong: the equation is telling you it "
                         "has no solution, since `1` is not `−4` whatever `x` is. Compare "
                         "`6x + 1 = 6x + 1`, which collapses to `0 = 0` and is true for "
                         "every number. Lesson 6 is about reading those two lines "
                         "correctly.")),
        ],
        "lab": ("equation", {
            "mode": "sides",
            "panel_title": "Both routes, side by side",
            "panel_intro": "The lab solves the same equation twice &mdash; collecting the "
                           "variable on the left, then on the right &mdash; and reports "
                           "whether the two routes agree. Watch which of the two divides "
                           "by a negative number.",
        }),
        "steps_title": "Solving with the variable on both sides",
        "steps_intro": "One extra step at the front; the rest is lesson 2 unchanged.",
        "steps": [
            ("Simplify both sides separately",
             "Multiply out every bracket, distributing any minus sign in front of one over "
             "all of its terms, then combine like terms. Do this on both sides before "
             "anything moves."),
            ("Pick a side for the variable and subtract that variable term from both sides",
             "Subtracting the smaller coefficient keeps the surviving one positive. Write "
             "the operation down: \"subtract `3x` from both sides\" is a step you can "
             "check."),
            ("Move the constants the other way",
             "Add or subtract so that every plain number is on the side without the "
             "variable. You are now looking at `px = q`, which is lesson 2's last line."),
            ("Divide by the coefficient and check in the original",
             "Sign included. Then substitute into the equation as it was first written "
             "&mdash; both sides had a variable in them, so both sides have to be "
             "evaluated."),
        ],
        "worked": {
            "title": "One equation twice, and one with brackets",
            "intro": ["The first is solved both ways to show the answer does not depend on "
                      "the choice. There is one answer, so it is checked once."],
            "lines": [
                "A.  5x + 2 = 3x − 8",
                "    collecting on the LEFT              collecting on the RIGHT",
                "        − 3x    2x + 2 = −8                 − 5x     2 = −2x − 8",
                "        − 2     2x     = −10                + 8     10 = −2x",
                "        ÷ 2      x     = −5                 ÷ (−2)  −5 = x",
                "",
                "    check   left   5·(−5) + 2 = −23",
                "            right  3·(−5) − 8 = −23        agrees",
                "",
                "B.  2(x − 3) + 4 = 3(x + 1) − 5",
                "        expand      2x − 2 = 3x − 2",
                "        − 2x            −2 = x − 2",
                "        + 2              0 = x",
                "",
                "    check   left   2(0 − 3) + 4 = −2",
                "            right  3(0 + 1) − 5 = −2        agrees",
            ],
            "after": [
                "In A the two routes differ only in the final division: by `2` on the left "
                "route, by `−2` on the right. That is the whole cost of the choice, and it "
                "is why collecting where the coefficient is larger is worth doing.",
                "In B the answer is `x = 0`. The check evaluates both sides at `0` and "
                "gets `−2` twice, which is what makes it a solution. A reader who expected "
                "\"no solution\" from seeing a zero has misread the result, not the "
                "algebra.",
            ],
        },
        "quiz_title": "Collecting the unknown",
        "quiz": [
            {"q": "Solve `3x − 7 = 8x + 3`.",
             "a": ["`x = −2`", "`x = 2`", "`x = −4/5`", "`x = −10`"],
             "c": 0,
             "why": "Subtracting `3x` gives `−7 = 5x + 3`, then `−10 = 5x`, so `x = −2`. "
                    "`2` comes from writing `3x − 8x = 5x`; `−4/5` from adding the 3 "
                    "instead of subtracting it; `−10` from stopping at `5x = −10` and "
                    "never dividing."},
            {"q": "Solve `2 − x = 4 − 3x`.",
             "a": ["`x = 1`", "`x = 3`", "`x = −1/2`", "`x = 1/2`"],
             "c": 0,
             "why": "Adding `3x` gives `2 + 2x = 4`, then `2x = 2` and `x = 1`. `3` comes "
                    "from writing `2x = 4 + 2`; `−1/2` from subtracting `3x` on the left "
                    "while cancelling it on the right, which leaves `2 − 4x = 4`; `1/2` "
                    "from that same slip with the sign lost in the division."},
            {"q": "After simplifying, an equation reads `2x − 2 = 3x − 2`. What is its solution?",
             "a": ["`x = 0`", "There is no solution", "Every number is a solution", "`x = −2`"],
             "c": 0,
             "why": "Subtracting `2x` leaves `−2 = x − 2`, and adding 2 gives `x = 0`. "
                    "Zero is a value like any other, and reaching it is not the same as "
                    "reaching a contradiction &mdash; substituting `0` into both sides "
                    "gives `−2` and `−2`."},
        ],
        "mistakes": [
            ("Adding a variable term to one side and subtracting it from the other",
             "The property says the same operation on both sides. Going from "
             "`5x + 2 = 3x − 8` to `8x + 2 = −8` has added `3x` on the left and subtracted "
             "it on the right, and the resulting equation has a different solution."),
            ("Distributing a minus sign over only the first term of a bracket",
             "`3x − (x − 4)` is `3x − x + 4`, that is `2x + 4`. Writing `3x − x − 4` is a "
             "different expression, and everything downstream of it is answering a "
             "different question."),
            ("Reading x = 0 as \"no solution\"",
             "They are different results. `x = 0` says exactly one number works and names "
             "it; \"no solution\" says none does. Lesson 6 gives the line of working that "
             "genuinely means the second thing, and it does not look like `x = 0`."),
        ],
        "standard": ("Finish when the choice of side is deliberate and every sign survives the collecting.",
                     "You should look at the two coefficients, decide which term to "
                     "subtract, say why, and carry the equation to `x = ` a number with "
                     "the brackets expanded correctly on the way. You should also be able "
                     "to solve the same equation the other way round and get the same "
                     "answer, which is the cheapest possible test of your own signs."),
        "note": "The lab runs both routes at once precisely so that the answer can be seen "
                "not to depend on the choice. If the two columns ever disagreed, one of "
                "them would contain an illegal step &mdash; and that is a useful way to "
                "think about what \"legal\" means here: a legal move is one that cannot "
                "change the answer.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "equations-with-fractions",
        "title": "Equations with Fractions",
        "module": "Equations",
        "one_line": "Clearing denominators with the least common denominator.",
        "summary": (
            "Multiplying both sides by a common denominator turns an equation full of "
            "fractions into one with none. The move is the multiplication property with a "
            "convenient constant, so it changes nothing about the answer &mdash; provided "
            "the multiplier reaches every term on both sides."
        ),
        "key": [
            "x/2 + x/3 = 5            denominators 2 and 3   →   LCD = 6",
            "6·(x/2) + 6·(x/3) = 6·5  multiply EVERY term, both sides",
            "3x + 2x = 30             not one fraction left",
            "5x = 30  →  x = 6        check:  6/2 + 6/3 = 3 + 2 = 5",
        ],
        "key_label": "One multiplication, applied everywhere",
        "concepts_intro": (
            "Nothing here is a new rule about fractions. It is one application of the "
            "multiplication property, chosen so that the arithmetic afterwards is easy."
        ),
        "concepts": [
            ("Clearing denominators is the multiplication property in disguise",
             "Multiplying both sides by a nonzero number produces an equivalent equation. "
             "The LCD is just a well-chosen value of that number, and the equation you get "
             "has exactly the same solutions as the one you started with."),
            ("The multiplier reaches every term on both sides",
             "Including the terms that have no denominator. Multiplying `x/2 + x/3 = 5` by "
             "6 and leaving the `5` alone gives `3x + 2x = 5`, an equation about something "
             "else entirely."),
            ("The least common denominator is a convenience, not a requirement",
             "Any common multiple of the denominators clears them. `12` works on `x/2` and "
             "`x/3` as well as `6` does; it merely doubles every number in the rest of the "
             "problem. Choosing the least one is a habit, not a law."),
        ],
        "read_title": "Removing the denominators",
        "read_intro": "Finding the multiplier, applying it to every term, and the two places the brackets matter.",
        "body": [
            ("def", ("Least common denominator",
                     "The <strong>least common denominator</strong> of a set of fractions "
                     "is the smallest positive number that every denominator divides "
                     "exactly &mdash; the least common multiple of the denominators.",
                     "For `2` and `3` it is `6`. For `4` and `6` it is `12`, not `24`: "
                     "`24` is the product, and the product is a common multiple but not "
                     "usually the least one.")),
            ("math", [
                "x/2 + x/3 = 5",
                "     × 6 both sides      6·(x/2) + 6·(x/3) = 6·5",
                "                                3x  +  2x  =  30",
                "                                        5x  =  30",
                "                                         x  =  6",
                "",
                "check    6/2 + 6/3  =  3 + 2  =  5",
            ]),
            ("p", "Using `12` instead gives `6x + 4x = 60`, so `10x = 60` and `x = 6`. The "
                  "same answer, reached through larger numbers. That is the only penalty "
                  "for not using the least common denominator."),
            ("h3", "A numerator with more than one term"),
            ("p", "`(x + 1)/3` is the whole of `x + 1` divided by 3. When the multiplier "
                  "arrives, the bracket has to stay:"),
            ("math", [
                "(x + 1)/3 − (x − 2)/4 = 1              LCD of 3 and 4 is 12",
                "",
                "     × 12      4(x + 1) − 3(x − 2) = 12",
                "     expand    4x + 4 − 3x + 6    = 12",
                "     collect        x + 10        = 12",
                "                            x     = 2",
                "",
                "check    (2 + 1)/3 − (2 − 2)/4  =  1 − 0  =  1",
            ]),
            ("p", "Two things happen in the expansion and both are worth naming. "
                  "`12 · (x + 1)/3` is `4(x + 1)`, which is `4x + 4` &mdash; not `4x + 1`. "
                  "And `−3(x − 2)` is `−3x + 6`, because the minus reaches both terms "
                  "inside the bracket."),
            ("h3", "Decimals are fractions"),
            ("p", "`0.2` is `1/5`, `1.5` is `3/2` and `3.1` is `31/10`. Multiplying by a "
                  "power of ten clears them all at once: use `10` for one decimal place, "
                  "`100` for two, and so on for the longest one present."),
            ("math", [
                "0.2x + 1.5 = 3.1",
                "     × 10        2x + 15 = 31",
                "                 2x      = 16",
                "                  x      = 8",
                "",
                "check    0.2·8 + 1.5  =  1.6 + 1.5  =  3.1",
            ]),
            ("h3", "What clearing does not change"),
            ("p", "The multiplier here is a fixed nonzero number, so the move is "
                  "reversible: divide by it and you are back where you started. The "
                  "solution set therefore cannot change, and no candidate needs to be "
                  "thrown out afterwards."),
            ("p", "That guarantee depends on the multiplier being a number. When a "
                  "denominator contains the variable &mdash; `3/(x − 2)` &mdash; the "
                  "multiplier is zero for one value of `x`, the move is not reversible "
                  "there, and a candidate can appear that solves nothing. Lesson 7 meets "
                  "the first case of that, and course 5 treats it properly."),
            ("example", ("When the fractions cancel completely",
                         "`x/6 + x/3 = x/2`, multiplied through by 6, becomes "
                         "`x + 2x = 3x`, that is `3x = 3x`. Every `x` cancels and `0 = 0` "
                         "is left. The two sides were the same expression written "
                         "differently &mdash; `x/6 + x/3 = x/6 + 2x/6 = 3x/6 = x/2` "
                         "&mdash; so every number is a solution. Lesson 6 names this "
                         "outcome.")),
        ],
        "lab": ("equation", {
            "mode": "fractions",
            "panel_title": "Every written term, multiplied",
            "panel_intro": "The lab lists the denominators it found, reports the LCD, and "
                           "multiplies each term you wrote by it on its own row. Decimals "
                           "count as fractions: type `0.2x + 1.5 = 3.1` and watch the "
                           "multiplier come out as 10.",
        }),
        "steps_title": "Clearing the denominators",
        "steps_intro": "Find the multiplier first, then use it on everything without exception.",
        "steps": [
            ("List the denominators, converting any decimals",
             "`0.2` counts as `1/5`. Write the denominators down rather than holding them "
             "in your head; the list is what the next step works from."),
            ("Take the least common multiple of that list",
             "That is the LCD. Any common multiple works, so if the least one is not "
             "obvious, the product of the denominators is a safe fallback that costs only "
             "larger arithmetic."),
            ("Multiply every term on both sides by it, keeping brackets on multi-term numerators",
             "Count the terms first and count them again afterwards. `12 · (x + 1)/3` is "
             "`4(x + 1)`; the bracket is not optional, and neither is multiplying the "
             "terms that had no denominator."),
            ("Solve the fraction-free equation, then check in the original",
             "The check goes back into the equation with the fractions in it. That is the "
             "one that was asked, and it is the only version that can confirm the clearing "
             "step itself."),
        ],
        "worked": {
            "title": "Two clearings, with the traps marked",
            "intro": ["The first has multi-term numerators and a subtraction; the second "
                      "is decimals."],
            "lines": [
                "A.  (x + 1)/3 − (x − 2)/4 = 1",
                "        denominators   3, 4        LCD = 12",
                "        × 12 term by term:",
                "            12 · (x + 1)/3   =   4(x + 1)      <-- bracket kept",
                "            12 · (x − 2)/4   =   3(x − 2)",
                "            12 · 1           =   12            <-- the right side too",
                "",
                "        4(x + 1) − 3(x − 2) = 12",
                "        4x + 4 − 3x + 6     = 12               <-- −3(x − 2) = −3x + 6",
                "        x + 10              = 12",
                "        x                   = 2",
                "",
                "    check   (2 + 1)/3 − (2 − 2)/4  =  1 − 0  =  1        agrees",
                "",
                "B.  0.2x + 1.5 = 3.1",
                "        one decimal place, so multiply by 10",
                "        2x + 15 = 31",
                "        2x      = 16",
                "        x       = 8",
                "",
                "    check   0.2·8 + 1.5  =  1.6 + 1.5  =  3.1            agrees",
            ],
            "after": [
                "Three terms went into the multiplication in A and three came out. That "
                "count is the fastest guard against the standard error, which is "
                "multiplying the fractions and leaving the `1` on the right untouched.",
                "The sign on `−3(x − 2)` is the second trap. It produces `+6`, and writing "
                "`−6` instead gives `x = 14` &mdash; an answer that survives every later "
                "step and fails the check.",
            ],
        },
        "quiz_title": "Denominators",
        "quiz": [
            {"q": "Solve `x/6 + x/4 = 1`.",
             "a": ["`x = 12/5`", "`x = 1/5`", "`x = 10`", "`x = 5/12`"],
             "c": 0,
             "why": "The LCD of 6 and 4 is 12, giving `2x + 3x = 12`, so `5x = 12` and "
                    "`x = 12/5`. `1/5` comes from leaving the right side unmultiplied; "
                    "`10` from adding the denominators into `x/10 = 1`; `5/12` from "
                    "inverting the last division."},
            {"q": "Solve `(x + 1)/3 − (x − 2)/4 = 1`.",
             "a": ["`x = 2`", "`x = 14`", "`x = −9`", "`x = 9`"],
             "c": 0,
             "why": "`4(x + 1) − 3(x − 2) = 12` gives `x + 10 = 12`. `14` is what you get "
                    "from `−3(x − 2) = −3x − 6`; `−9` from forgetting to multiply the "
                    "right side; `9` from dropping both brackets and writing "
                    "`4x + 1 − (3x − 2) = 12`."},
            {"q": "Why does multiplying an equation through by the LCD never change its solutions?",
             "a": ["Because the LCD is the smallest such number",
                   "Because the LCD is a nonzero number, so the multiplication can be undone by dividing",
                   "Because fractions and whole numbers have the same solutions",
                   "It can change them, which is why the answer must be checked"],
             "c": 1,
             "why": "Reversibility is the whole argument, and it needs only that the "
                    "multiplier is not zero. Being least is a convenience. The last option "
                    "describes what happens when the multiplier contains the variable, "
                    "which is a different situation and belongs to lesson 7 and course 5."},
        ],
        "mistakes": [
            ("Multiplying only the terms that have denominators",
             "In `x/2 + x/3 = 5` the `5` gets multiplied too. Leaving it alone produces "
             "`5x = 5` and the answer `1`, which fails the check on the very first "
             "substitution."),
            ("Dropping the bracket on a numerator with two terms",
             "`12 · (x + 1)/3` is `4(x + 1) = 4x + 4`, not `4x + 1`. The fraction bar acts "
             "as a bracket, and it disappears at exactly the moment the bracket becomes "
             "necessary."),
            ("Losing the sign when a fraction is subtracted",
             "`−3(x − 2)` is `−3x + 6`. The minus in front of the fraction belongs to the "
             "whole numerator, so it reaches both terms once the denominator has gone."),
        ],
        "standard": ("Finish when you can clear any set of denominators in one multiplication and account for every term.",
                     "Given an equation with fractions or decimals you should name the "
                     "denominators, state the LCD, multiply every term including the ones "
                     "on the right, keep brackets around multi-term numerators, and check "
                     "in the original. The term count before and after should be the first "
                     "thing you verify."),
        "note": "Lesson 5 rearranges formulas, where the fractions are made of letters "
                "rather than numbers and exactly the same multiplication clears them. The "
                "condition that the multiplier be nonzero, which is free here, becomes the "
                "main thing to state there.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "literal-equations-and-formulas",
        "title": "Literal Equations and Formulas",
        "module": "Equations",
        "one_line": "Solving for one letter among several.",
        "summary": (
            "A formula is an equation with several letters, and rearranging it uses the "
            "same four moves as any other equation. Two things are genuinely new: the "
            "answer is an expression rather than a number, and dividing by a letter is "
            "legal only when that letter is not zero."
        ),
        "key": [
            "F = (9/5)C + 32     →     C = (5/9)(F − 32)",
            "",
            "S = C + rC          the target appears twice: collect, then factor",
            "S = C(1 + r)        →     C = S/(1 + r)      valid when 1 + r ≠ 0",
        ],
        "key_label": "Two rearrangements, one condition",
        "concepts_intro": (
            "The steps are the ones you already have. What changes is what counts as an "
            "answer and what has to be said about it."
        ),
        "concepts": [
            ("One letter is the unknown; every other letter is a number you were not told",
             "Decide which letter you are solving for before you write anything. In "
             "`A = P(1 + rt)` solving for `r` and solving for `t` are different problems "
             "with different answers, and the algebra only knows which one you mean "
             "because you decided."),
            ("The answer is an expression, and it is finished when the target is alone",
             "The target letter must stand by itself on one side and appear nowhere on the "
             "other. `C = S − rC` is not an answer &mdash; `C` is still on the right "
             "&mdash; even though it is a true statement."),
            ("Dividing by a letter carries a condition, and the condition is part of the answer",
             "`C = S/(1 + r)` is correct exactly when `1 + r ≠ 0`. Nothing in the algebra "
             "will remind you; you have to write it down at the moment you divide."),
        ],
        "read_title": "Rearranging a formula",
        "read_intro": "The ordinary steps with letters, the case where the target appears twice, and the condition on the last division.",
        "body": [
            ("def", ("Literal equation",
                     "A <strong>literal equation</strong> is an equation containing more "
                     "than one letter. To <strong>solve it for</strong> a named letter is "
                     "to produce an equivalent equation with that letter alone on one side "
                     "and absent from the other.",
                     "Formulas are the usual example, which is why the two words get used "
                     "interchangeably.")),
            ("p", "The reason to rearrange rather than substitute is economy. Converting "
                  "twenty temperatures from Fahrenheit to Celsius by solving "
                  "`F = (9/5)C + 32` twenty times is twenty problems; rearranging once "
                  "gives a formula you then evaluate twenty times."),
            ("math", [
                "F = (9/5)C + 32                 solve for C",
                "",
                "     − 32 both sides            F − 32 = (9/5)C",
                "     × (5/9) both sides    (5/9)(F − 32) = C",
                "",
                "answer   C = (5/9)(F − 32)",
                "",
                "check    C = 100  gives  F = (9/5)(100) + 32 = 180 + 32 = 212",
                "         and      (5/9)(212 − 32) = (5/9)(180) = 100",
            ]),
            ("p", "Every step is one of the four operations applied to both sides, named "
                  "as it happens, exactly as in lesson 2. The letters change nothing about "
                  "which moves are available."),
            ("h3", "When the target appears more than once"),
            ("p", "Undoing operations one at a time cannot isolate a letter that occurs in "
                  "two places. Gather every term containing the target on one side, then "
                  "factor it out:"),
            ("math", [
                "S = C + rC                      solve for C",
                "",
                "S = C(1 + r)                    factor: the distributive law, backwards",
                "S/(1 + r) = C                   divide by (1 + r)",
                "",
                "answer   C = S/(1 + r),   provided 1 + r ≠ 0",
            ]),
            ("p", "The factoring step is `ab + ac = a(b + c)` read from right to left, "
                  "with `a = C`, `b = 1` and `c = r`. Note the `1`: `C` on its own is "
                  "`1·C`, and forgetting it produces `S = C(r)`, which is a different "
                  "formula."),
            ("thm", ("Every linear rearrangement ends the same way",
                     "If an equation can be written `px = q`, where neither `p` nor `q` "
                     "contains `x`, then `x = q/p` whenever `p ≠ 0`.",
                     "Collecting and factoring is how you get a formula into that shape. "
                     "The letter you are solving for plays the part of `x`; every other "
                     "letter is swept into `p` and `q`. What happens when `p = 0` is "
                     "lesson 6.")),
            ("h3", "The condition on the division"),
            ("p", "`A = (1/2)bh` solved for `h` gives `h = 2A/b`, and that statement is "
                  "silent about `b = 0`, where it says nothing at all. The restriction is "
                  "not pedantry: a triangle with no base is not a triangle, and the formula "
                  "is telling you so."),
            ("p", "Sometimes the condition is invisible until you write it. In "
                  "`C = S/(1 + r)` the forbidden value is `r = −1`, not `r = 0`, because "
                  "it is `1 + r` that gets divided by. Read the divisor, not the letter."),
            ("example", ("A formula this method cannot rearrange",
                         "`A = s²` solved for `s` is not a rearrangement of this kind. "
                         "Adding, subtracting, multiplying and dividing undo a linear "
                         "relationship, and `s²` is not linear in `s`. Undoing a square "
                         "needs a square root, and for `A &gt; 0` it produces two answers, "
                         "`s = ±√A`, which is course 6's subject &mdash; and for a length "
                         "one of the two is then discarded on physical grounds, not "
                         "algebraic ones.")),
        ],
        "lab": ("equation", {
            "mode": "literal",
            "panel_title": "Name the letter, read the condition",
            "panel_intro": "Enter a formula and name the letter to solve for. The answer "
                           "comes back as an expression in the others, with the condition "
                           "under which the final division was legal, and it is checked at "
                           "exact values of the remaining letters.",
        }),
        "steps_title": "Solving for a named letter",
        "steps_intro": "Decide what the unknown is first; after that every other letter behaves like a number.",
        "steps": [
            ("Name the target letter and treat every other letter as a constant",
             "Write the target at the top of the page if it helps. Half the errors in this "
             "lesson are answers to a different question &mdash; solving for `t` when `r` "
             "was asked for."),
            ("Clear fractions and brackets",
             "Multiply through by any denominator, expand any bracket that hides the "
             "target. `A = P(1 + rt)` becomes `A = P + Prt`, and only then is it obvious "
             "where `r` lives."),
            ("Gather every term containing the target on one side",
             "Everything else goes to the other side. If the target appears only once, "
             "this is the ordinary collecting of lesson 3."),
            ("Factor the target out, divide by its coefficient, and state the condition",
             "The coefficient is whatever multiplies the target after factoring. Divide by "
             "it, and write down that the answer holds when that expression is not zero."),
        ],
        "worked": {
            "title": "Two rearrangements, with numerical spot checks",
            "intro": ["The first has the target in two places; the second has it inside a "
                      "bracket."],
            "lines": [
                "A.  S = C + rC          solve for C",
                "        S = C(1 + r)                   factor C out; C is 1·C",
                "        S/(1 + r) = C                  ÷ (1 + r)",
                "    answer   C = S/(1 + r),   provided 1 + r ≠ 0",
                "",
                "    spot check at r = 1/4, C = 80:",
                "        S = 80 + (1/4)(80) = 80 + 20 = 100",
                "        S/(1 + r) = 100/(5/4) = 80              returns C",
                "",
                "B.  A = P(1 + rt)       solve for r",
                "        A = P + Prt                    expand first",
                "        A − P = Prt                    − P both sides",
                "        (A − P)/(Pt) = r               ÷ Pt",
                "    answer   r = (A − P)/(Pt),   provided P ≠ 0 and t ≠ 0",
                "",
                "    spot check at P = 200, t = 3, r = 1/20:",
                "        A = 200(1 + 3/20) = 200·(23/20) = 230",
                "        (230 − 200)/(200·3) = 30/600 = 1/20     returns r",
            ],
            "after": [
                "The spot check is worth doing once for every formula you rearrange. It "
                "confirms that the rearrangement returns the right value at those "
                "particular numbers, which is enough to expose a dropped sign or an "
                "inverted fraction. It is not a proof that the algebra is right for all "
                "values &mdash; the named steps are the argument for that.",
                "In B, `(A − P)/(Pt)` cannot be shortened by cancelling the two `P`s. The "
                "`P` in the numerator is part of the term `A − P`, not a factor of it. "
                "What you may write instead is `(A/P − 1)/t`, which is the same expression "
                "with the division done first.",
            ],
        },
        "quiz_title": "Rearranging",
        "quiz": [
            {"q": "Solve `A = (1/2)bh` for `h`.",
             "a": ["`h = 2A/b`", "`h = A/(2b)`", "`h = 2A − b`", "`h = b/(2A)`"],
             "c": 0,
             "why": "Multiply both sides by 2, then divide by `b`. `A/(2b)` comes from "
                    "dividing by 2 instead of multiplying; `2A − b` from subtracting `b` "
                    "when it is a factor, not a term; `b/(2A)` from inverting the last "
                    "division."},
            {"q": "Solve `S = C + rC` for `C`.",
             "a": ["`C = S/(1 + r)`", "`C = S − rC`", "`C = S − r`", "`C = S(1 + r)`"],
             "c": 0,
             "why": "Factoring gives `S = C(1 + r)`, and dividing isolates `C`. `S − rC` "
                    "still contains `C`, so nothing has been solved; `S − r` comes from "
                    "cancelling one `C` out of `C + rC`, which is not a legal cancellation "
                    "in a sum; `S(1 + r)` multiplies where it should divide."},
            {"q": "`ax + b = c` rearranges to `x = (c − b)/a`. When is that answer valid?",
             "a": ["For every `a`, `b` and `c`",
                   "Exactly when `a ≠ 0`",
                   "Exactly when `c ≠ b`",
                   "Exactly when `a`, `b` and `c` are whole numbers"],
             "c": 1,
             "why": "The last step divided by `a`, which requires `a ≠ 0`. If `a = 0` the "
                    "equation is `b = c`, which contains no `x` and is either true for "
                    "every number or for none &mdash; the two outcomes of lesson 6. "
                    "`c = b` merely makes the answer `0`, which is a perfectly good "
                    "value."},
        ],
        "mistakes": [
            ("Cancelling a letter that is a term rather than a factor",
             "In `(A − P)/(Pt)` the `P` on top is one term of a difference, not a factor "
             "of the whole numerator. Crossing it out to get `(A − 1)/t` gives `229/3` at "
             "`A = 230, P = 200, t = 3`, where the true value is `1/20`. Dividing the "
             "<em>whole</em> numerator by `P` is legal, and it gives `(A/P − 1)/t`, which "
             "does return `1/20`."),
            ("Stopping while the target letter is still on both sides",
             "`C = S − rC` looks like an answer because `C` is alone on the left. It is "
             "not one: to use it you would already need to know `C`. Collect and factor "
             "instead."),
            ("Dividing by a letter without saying when it is nonzero",
             "Every division by an expression containing letters comes with a condition. "
             "Writing `h = 2A/b` and not writing `b ≠ 0` leaves the answer claiming "
             "something about a case where it says nothing."),
        ],
        "standard": ("Finish when you can isolate any letter, including one that appears twice, and state the condition.",
                     "Given a formula and a named letter you should clear fractions, "
                     "expand, collect the target's terms, factor, divide, and write the "
                     "condition on the divisor without being prompted. A numerical spot "
                     "check on the result should be automatic, and you should be able to "
                     "say what it does and does not establish."),
        "note": "The condition `p ≠ 0` has now appeared in three lessons in three "
                "disguises: the multiplication property in lesson 1, the final division in "
                "lesson 2, and the divisor here. Lesson 6 asks what an equation is saying "
                "when `p` really is zero, and the answer turns out to be one of exactly "
                "two things.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "identities-and-contradictions",
        "title": "Identities and Contradictions",
        "module": "Equations",
        "one_line": "When every number works, and when none does.",
        "summary": (
            "Solving an equation can end with the variable gone. If what is left is true, "
            "every number is a solution; if it is false, none is. Neither outcome is a "
            "mistake, and neither of them says `x = 0`."
        ),
        "key": [
            "2(x + 3) = 2x + 6   →   0 = 0    always true    identity, every number",
            "2(x + 3) = 2x + 5   →   6 = 5    always false   contradiction, no solution",
            "2(x + 3) = x + 5    →   x = −1   true once      conditional, one number",
            "0 = 0 does not say x = 0.        0 = 5 does not say x = 5.",
        ],
        "key_label": "The three things a linear equation can be",
        "concepts_intro": (
            "An equation is a claim, and a claim about every value of `x` can be true "
            "always, false always, or true for some values only. There is no fourth "
            "possibility for a linear equation."
        ),
        "concepts": [
            ("The variable disappearing is information, not failure",
             "When the `x` terms cancel, the equation has finished telling you what it "
             "knows. What remains is a statement about numbers with no `x` in it, and that "
             "statement is either true or false &mdash; which is the answer."),
            ("An identity is two ways of writing the same expression",
             "`2(x + 3)` and `2x + 6` are the same expression; the distributive law says "
             "so. An equation between them is true for every value because there was only "
             "ever one expression in the room."),
            ("A linear equation has none, one, or all of them, never exactly two",
             "Reduce it to `px = q`. If `p ≠ 0` there is exactly one solution. If `p = 0` "
             "the statement is `0 = q`, which does not mention `x` and so holds for every "
             "number or for no number at all."),
        ],
        "read_title": "Three outcomes, told apart",
        "read_intro": "The names, the theorem behind them, and the two lines of working that get misread.",
        "body": [
            ("def", ("Conditional, identity, contradiction",
                     "An equation is <strong>conditional</strong> when some values of the "
                     "variable make it true and some make it false. It is an "
                     "<strong>identity</strong> when every value makes it true. It is a "
                     "<strong>contradiction</strong> when no value does.",
                     "The solution sets are, in order: some particular numbers; every real "
                     "number; and nothing at all.")),
            ("thm", ("The three outcomes are the only ones",
                     "Every linear equation in `x` can be rewritten as `px = q` with `p` "
                     "and `q` numbers. If `p ≠ 0` it has exactly one solution, `q/p`. If "
                     "`p = 0` and `q = 0` every number is a solution. If `p = 0` and "
                     "`q ≠ 0` there are none.")),
            ("proof", [
                "Simplify both sides and subtract the right side from both. Every term is "
                "either a multiple of `x` or a constant, so what is left is `px − q = 0` "
                "for some numbers `p` and `q`, that is `px = q`.",
                "If `p ≠ 0`, divide both sides by `p`. Division by a nonzero number is "
                "reversible, so `x = q/p` is equivalent to the original and is the only "
                "solution.",
                "If `p = 0` the statement reads `0 = q`. It contains no `x`, so its truth "
                "does not depend on `x`: it is true for every number when `q = 0`, and "
                "false for every number otherwise.",
            ]),
            ("p", "So the working itself tells you which case you are in. Simplify, "
                  "subtract, and look at what survives."),
            ("math", [
                "2(x + 3) = 2x + 6        2x + 6 = 2x + 6      − 2x     6 = 6      identity",
                "2(x + 3) = 2x + 5        2x + 6 = 2x + 5      − 2x     6 = 5      contradiction",
                "2(x + 3) = x + 5         2x + 6 =  x + 5      −  x     x = −1     conditional",
            ]),
            ("p", "Read the first line as: whatever `x` is, the two sides are the same "
                  "number, so the claim holds. Read the second as: whatever `x` is, the "
                  "left side is exactly `1` more than the right, so the claim never holds. "
                  "The third constrains `x` to a single value."),
            ("h3", "The two misreadings"),
            ("p", "`0 = 0` is not `x = 0`. It is a true statement with no `x` in it, and "
                  "the correct answer is \"every real number\". Reporting `x = 0` names one "
                  "solution out of infinitely many and rejects all the rest."),
            ("p", "`0 = 5` is not `x = 5`, and it is not `x = 0` either. It is a false "
                  "statement with no `x` in it, and the correct answer is \"no solution\". "
                  "Both misreadings come from the same habit &mdash; expecting the last "
                  "line of the working to have the shape `x = ` something."),
            ("h3", "The picture"),
            ("p", "Draw each side as a graph, as the lab does. A conditional equation is "
                  "two lines crossing at one point; an identity is one line drawn twice; a "
                  "contradiction is two parallel lines that never meet. The graphs are a "
                  "preview &mdash; lines are course 3 &mdash; and the argument above does "
                  "not depend on them."),
            ("p", "Two cautions about identities. First, an identity is what you are "
                  "proving every time you expand a bracket, so they are not exotic. "
                  "Second, `x/2 + x/3 = (5/6)x` is an identity because "
                  "`1/2 + 1/3 = 3/6 + 2/6 = 5/6`, and the only way to be sure of that is "
                  "to do the addition."),
            ("example", ("An equation that only looks like an identity",
                         "`3x + 5 = 3x + 5 + x`. The two sides begin identically, which "
                         "invites the answer \"every number\". Subtracting `3x + 5` from "
                         "both sides leaves `0 = x`, so it is conditional with the single "
                         "solution `x = 0`. Check: at `x = 0` both sides are `5`; at "
                         "`x = 1` the left is `8` and the right is `9`. The extra term on "
                         "the right is the whole story, and only simplifying finds it.")),
        ],
        "lab": ("equation", {
            "mode": "type",
            "panel_title": "Identity, contradiction, or one answer",
            "panel_intro": "The lab subtracts one side from the other and shows exactly "
                           "what is left. Take the preset `2(x + 3) = 2x + 6` and change "
                           "the `6` to a `5`: an identity becomes a contradiction, and the "
                           "difference between them is one constant.",
        }),
        "steps_title": "Deciding which of the three it is",
        "steps_intro": "Do not judge by appearance. Simplify, subtract, then read.",
        "steps": [
            ("Simplify each side completely",
             "Brackets out, like terms combined, fractions cleared if there are any. Two "
             "sides that look alike may differ by a term you have not multiplied out yet."),
            ("Subtract one whole side from the other",
             "Everything on one side, `0` on the other. This is the step the theorem "
             "describes, and it is what produces `px = q` in a readable form."),
            ("Read what is left",
             "Still a term in `x`: conditional, so finish solving it. `0 = 0` or any true "
             "numerical statement: identity. A false numerical statement such as `6 = 5`: "
             "contradiction."),
            ("Write the answer in words, not as a pretend value",
             "\"Every real number\", \"no solution\", or the number itself. Never `x = 0` "
             "for an identity and never `x = 5` for `0 = 5`. Then test a couple of values "
             "in the original to confirm the verdict."),
        ],
        "worked": {
            "title": "The same left side, three right sides",
            "intro": ["Between A and B only the right-hand constant changes, and that alone "
                      "turns an identity into a contradiction. C changes the coefficient "
                      "of `x` on the right, which is what makes a conditional equation "
                      "possible at all."],
            "lines": [
                "A.  2(x + 3) = 2x + 6",
                "        2x + 6 = 2x + 6        − 2x      6 = 6      true, no x left",
                "    answer   identity: every real number is a solution",
                "    test     x = 0:  6 = 6      x = −4:  −2 = −2      x = 7/3:  32/3 = 32/3",
                "",
                "B.  2(x + 3) = 2x + 5",
                "        2x + 6 = 2x + 5        − 2x      6 = 5      false, no x left",
                "    answer   contradiction: no solution",
                "    test     x = 0:  6 ≠ 5      x = −4:  −2 ≠ −3",
                "",
                "C.  2(x + 3) = x + 5",
                "        2x + 6 = x + 5         − x       x + 6 = 5      x = −1",
                "    answer   conditional: exactly one solution, x = −1",
                "    check    left  2(−1 + 3) = 4        right  −1 + 5 = 4",
                "",
                "D.  3x − (x − 4) = 2(x + 2)",
                "        3x − x + 4 = 2x + 4    both sides are 2x + 4",
                "    answer   identity: every real number is a solution",
            ],
            "after": [
                "In B the tests do not prove there is no solution &mdash; two failed values "
                "leave infinitely many untested. The proof is the line `6 = 5`, which "
                "contains no `x` and is false, so no value of `x` can rescue it. The tests "
                "are there to catch an arithmetic slip in the simplifying.",
                "D is the one to watch for. Distributing the minus correctly gives "
                "`3x − x + 4`; distributing it over the first term only gives "
                "`3x − x − 4 = 2x − 4`, and the equation would then look like a "
                "contradiction. A sign error can manufacture any of the three outcomes, "
                "which is why the simplifying comes first and gets checked.",
            ],
        },
        "quiz_title": "Three outcomes",
        "quiz": [
            {"q": "What is the solution set of `4(x + 1) = 4x + 4`?",
             "a": ["Every real number", "`x = 0`", "There is no solution", "`x = 1`"],
             "c": 0,
             "why": "Expanding the left gives `4x + 4`, the same expression as the right, "
                    "so the statement is true whatever `x` is. It is an identity, and "
                    "answering `x = 0` would name one solution and discard all the "
                    "others."},
            {"q": "A correct piece of working ends at `0 = 7`. What does that mean?",
             "a": ["The equation has no solution",
                   "`x = 7`",
                   "`x = 0`",
                   "Every number is a solution"],
             "c": 0,
             "why": "`0 = 7` is a false statement containing no `x`, so no value of `x` "
                    "makes the original true. The answer is \"no solution\". The two "
                    "middle options read a value off a line that has no variable in it at "
                    "all."},
            {"q": "Which of these is a contradiction?",
             "a": ["`x + 1 = x + 2`", "`x + 1 = 1 + x`", "`2x + 1 = x + 1`", "`2(x + 1) = 2x + 2`"],
             "c": 0,
             "why": "Subtracting `x` from the first leaves `1 = 2`, which is false, so no "
                    "value works. The second and fourth are identities &mdash; both sides "
                    "are the same expression &mdash; and the third is conditional, with "
                    "the single solution `x = 0`."},
        ],
        "mistakes": [
            ("Writing x = 0 when the working ends at 0 = 0",
             "`0 = 0` has no `x` in it, so it cannot be an equation for `x`. It means the "
             "original placed no constraint at all, and the solution set is every real "
             "number &mdash; the largest possible answer, reported as the smallest."),
            ("Reading a contradiction as a value",
             "`0 = 5` is not `x = 5`, and `6 = 5` is not `x = 1`. A false statement about "
             "numbers means the solution set is empty; there is nothing to read off it."),
            ("Deciding by appearance before simplifying",
             "`3x + 5 = 3x + 5 + x` has matching starts and is conditional, with solution "
             "`x = 0`. `3x − (x − 4) = 2(x + 2)` looks unlike itself and is an identity. "
             "Neither verdict is visible until both sides are expanded and collected."),
        ],
        "standard": ("Finish when a vanished variable tells you something instead of worrying you.",
                     "You should simplify, subtract, and name the outcome in words &mdash; "
                     "\"every real number\", \"no solution\", or the value &mdash; without "
                     "reaching for an `x = ` that is not there. You should also be able to "
                     "say why a linear equation can never have exactly two solutions, and "
                     "the reason is the theorem above, not experience."),
        "note": "Every method later on can produce these two lines, and they always mean "
                "the same thing. In course 8 a system of equations collapsing to `0 = 0` "
                "means the two equations were the same line, and one collapsing to `0 = 5` "
                "means the lines are parallel &mdash; the same reading, one dimension up.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "ratio-proportion-and-percent",
        "title": "Ratio, Proportion and Percent",
        "module": "Applying equations",
        "one_line": "Three applications that are one equation in disguise.",
        "summary": (
            "A ratio is a quotient, a proportion is an equation between two of them, and a "
            "percent is a ratio whose denominator is 100. Cross-multiplying is not a new "
            "rule: it is multiplying both sides by both denominators, which is legal only "
            "where neither of them is zero."
        ),
        "key": [
            "a/b = c/d   ⟺   ad = bc          provided b ≠ 0 and d ≠ 0",
            "",
            "x/4 = 3/8   →   8x = 12   →   x = 3/2",
            "part/whole = p/100               every percent question, once named",
        ],
        "key_label": "One identity, three uses",
        "concepts_intro": (
            "These three topics are usually taught as three sets of rules. They are one "
            "equation, and the work is in setting it up rather than in solving it."
        ),
        "concepts": [
            ("A ratio is a quotient and a proportion is an equation between two of them",
             "`a : b` means the number `a/b`, which requires `b ≠ 0`. A proportion says two "
             "such numbers are equal, so it is an ordinary equation and every move you "
             "already have applies to it."),
            ("Cross-multiplying is one multiplication, not a rule of its own",
             "Multiply both sides of `a/b = c/d` by `bd` and the denominators cancel, "
             "leaving `ad = bc`. Knowing that is what tells you when it is allowed: `b` "
             "and `d` must not be zero, which matters as soon as a denominator contains "
             "the variable."),
            ("Percent is a ratio with denominator 100",
             "`15%` is the number `15/100`, that is `3/20`. Every percent question is "
             "`part/whole = p/100` with one of the three quantities missing, and the only "
             "difficulty is deciding which number is the whole."),
        ],
        "read_title": "Ratios, proportions and percents",
        "read_intro": "What each one is, why cross-multiplication works, and the values that have to be excluded first.",
        "body": [
            ("def", ("Ratio and proportion",
                     "A <strong>ratio</strong> of `a` to `b`, written `a : b` or `a/b`, is "
                     "the quotient of the two, and requires `b ≠ 0`. A "
                     "<strong>proportion</strong> is a statement that two ratios are equal.",
                     "A ratio compares two quantities of the same kind, or forms a rate "
                     "from two of different kinds &mdash; kilometres per litre. The units "
                     "decide what a correct set-up looks like.")),
            ("thm", ("Cross products",
                     "If `b ≠ 0` and `d ≠ 0`, then `a/b = c/d` is equivalent to "
                     "`ad = bc`.")),
            ("proof", [
                "Since `b ≠ 0` and `d ≠ 0`, the number `bd` is not zero. Multiplying both "
                "sides of `a/b = c/d` by `bd` gives `(a/b)·bd = (c/d)·bd`, which "
                "simplifies to `ad = bc`.",
                "Dividing `ad = bc` by the nonzero number `bd` returns `a/b = c/d`, so the "
                "move is reversible and the two statements have the same solutions.",
            ]),
            ("p", "The proof is where the conditions come from. When both denominators are "
                  "plain numbers there is nothing to worry about. When one contains the "
                  "variable, the values making it zero must be excluded before you solve, "
                  "and a candidate that turns out to be one of them is not a solution."),
            ("math", [
                "x/(x − 2) = 2/(x − 2)         the denominator is 0 at x = 2, so x ≠ 2",
                "",
                "     × (x − 2) both sides,  legal only where x ≠ 2",
                "     x = 2",
                "",
                "the only candidate is the excluded value      →   no solution",
            ]),
            ("h3", "Setting one up"),
            ("p", "The two ratios must be built the same way round: if the left side is "
                  "kilometres over litres, so is the right. A car covers 150 km on 12 L; "
                  "how far on 18 L?"),
            ("math", [
                "150/12 = d/18        km over litres on both sides",
                "     × (12·18)       150·18 = 12d",
                "                      2700  = 12d",
                "                         d  = 225",
                "",
                "check    225/18 = 25/2    and    150/12 = 25/2",
            ]),
            ("p", "Writing `150/12 = 18/d` instead compares kilometres per litre with "
                  "litres per kilometre. It is a different equation with a different "
                  "answer, and the units are what tell you so before you solve it."),
            ("h3", "Percent"),
            ("def", ("Percent",
                     "`p` <strong>percent</strong>, written `p%`, is the number `p/100`.",
                     "So `15%` is `15/100 = 3/20`, and \"15% of 80\" means `(15/100)·80`. "
                     "The word is a unit of measurement for ratios, nothing more.")),
            ("p", "All three of the standard questions are the proportion "
                  "`part/whole = p/100` with a different letter missing:"),
            ("ul", [
                "<strong>Find the part.</strong> \"What is 15% of 80?\" &mdash; "
                "`part/80 = 15/100`, so `100·part = 1200` and the part is `12`.",
                "<strong>Find the percent.</strong> \"42 is what percent of 120?\" &mdash; "
                "`42/120 = p/100`, so `120p = 4200` and `p = 35`.",
                "<strong>Find the whole.</strong> \"30 is 12% of what?\" &mdash; "
                "`30/whole = 12/100`, so `12·whole = 3000` and the whole is `250`.",
            ]),
            ("p", "For a change rather than a share, the whole is the <em>original</em> "
                  "amount: `(new − old)/old = p/100`. A price going from 60 to 75 is a "
                  "rise of 15 on a base of 60, and `15/60 = 25/100`, so 25%. Dividing by "
                  "the new price instead gives `15/75 = 20/100` and answers a question "
                  "nobody asked."),
            ("example", ("Why percents do not cancel out",
                         "A price of 100 rises by 20% to 120, then falls by 20%. The fall "
                         "is 20% of 120, which is 24, so the price lands at 96, not 100. "
                         "The two percentages are taken on different bases. This is not a "
                         "trick question &mdash; it is the reason a percent is meaningless "
                         "until you say what it is a percent of.")),
        ],
        "lab": ("equation", {
            "mode": "proportion",
            "panel_title": "Cross-multiply, after excluding",
            "panel_intro": "Enter the four parts of a proportion; the denominators may "
                           "contain the variable. The lab finds every value that would "
                           "make a denominator zero before it solves, then tests each "
                           "candidate against that list.",
        }),
        "steps_title": "Solving a proportion",
        "steps_intro": "Most of the work is done before the algebra starts.",
        "steps": [
            ("Say what each ratio compares, and put the two in the same order",
             "Kilometres over litres on both sides, or part over whole on both sides. A "
             "proportion built out of order is a correctly solved answer to the wrong "
             "question."),
            ("Write down any value that would make a denominator zero",
             "If both denominators are numbers there are none. If one contains the "
             "variable, solve \"denominator = 0\" first and keep the list beside you."),
            ("Multiply both sides by both denominators and solve",
             "This is cross-multiplication, and it produces `ad = bc`. What follows is a "
             "linear equation of the kind lesson 3 handles."),
            ("Check the candidate against the excluded list, then in the original",
             "A candidate on the excluded list is not a solution and there may then be "
             "none. A candidate that survives still has to make the original proportion "
             "true, and substituting is what confirms it."),
        ],
        "worked": {
            "title": "A proportion, an exclusion, and the three percent questions",
            "intro": ["The first has numerical denominators; the second does not."],
            "lines": [
                "A.  (x + 1)/3 = (x − 2)/5        denominators 3 and 5, never zero",
                "        × 15      5(x + 1) = 3(x − 2)",
                "                  5x + 5   = 3x − 6",
                "                  2x       = −11",
                "                  x        = −11/2",
                "",
                "    check   left   (−11/2 + 1)/3 = (−9/2)/3  = −3/2",
                "            right  (−11/2 − 2)/5 = (−15/2)/5 = −3/2        agrees",
                "",
                "B.  x/(x − 2) = 2/(x − 2)        x = 2 makes both denominators 0",
                "        excluded first:  x ≠ 2",
                "        × (x − 2), legal only where x ≠ 2:   x = 2",
                "    answer   no solution: the only candidate was excluded",
                "",
                "C.  15% of 80        part/80 = 15/100      100·part = 1200    part = 12",
                "    42 of 120        42/120 = p/100        120p = 4200        p = 35",
                "    30 is 12% of     30/w = 12/100         12w = 3000         w = 250",
            ],
            "after": [
                "B is the case that makes the exclusion worth doing first. The algebra "
                "produces `x = 2` quite happily; it is the denominator, not the algebra, "
                "that rules it out. Substituting `2` into the original gives `2/0` on both "
                "sides, and that is not a number: neither side has a value at `x = 2`, so "
                "the equation cannot be true there.",
                "In C the three lines are the same equation with a different unknown. "
                "Naming the whole is the entire difficulty: in the third line the whole is "
                "the thing being asked for, which is why `30` goes on top.",
            ],
        },
        "quiz_title": "Proportions and percents",
        "quiz": [
            {"q": "Solve `5/x = 15/9`.",
             "a": ["`x = 3`", "`x = 27`", "`x = 25/3`", "`x = 45`"],
             "c": 0,
             "why": "Cross products give `5·9 = 15x`, so `45 = 15x` and `x = 3`. `27` "
                    "solves `5/9 = 15/x`, which pairs the numbers differently; `25/3` "
                    "comes from multiplying numerator by numerator; `45` is the cross "
                    "product itself, reported before the division by 15."},
            {"q": "A price rises from 60 to 75. What is the percentage increase?",
             "a": ["25%", "125%", "20%", "15%"],
             "c": 0,
             "why": "The increase is 15 and the base is the original 60, so "
                    "`15/60 = 25/100`. `125%` is the new price as a percentage of the old, "
                    "which is 100 more than the increase; `20%` divides by the new price "
                    "instead of the old; `15%` reports the increase in currency as though "
                    "it were a percentage."},
            {"q": "What is the solution of `x/(x − 5) = 5/(x − 5)`?",
             "a": ["`x = 5`",
                   "No solution: the only candidate is the value that makes the denominators zero",
                   "Every number except 5",
                   "`x = 0`"],
             "c": 1,
             "why": "Multiplying by `x − 5` is legal only where `x ≠ 5`, and it gives "
                    "`x = 5` &mdash; the one value that step excluded. Substituting `5` "
                    "into the original produces `5/0`, which is not a number, so `5` is "
                    "not a solution and there is no other candidate."},
        ],
        "mistakes": [
            ("Cross-multiplying before looking at the denominators",
             "The step is only valid where both denominators are nonzero. Skipping the "
             "exclusion list makes `x/(x − 2) = 2/(x − 2)` look as though it has the "
             "solution `x = 2`, which substitution immediately refuses."),
            ("Building the two ratios in opposite orders",
             "`150/12 = d/18` compares km per litre on both sides. `150/12 = 18/d` "
             "compares km per litre with litres per km, and gives `d = 36/25` &mdash; a "
             "clean answer to a question about the wrong quantity. Write the units beside "
             "each ratio."),
            ("Taking a percent of the wrong base",
             "A 20% rise followed by a 20% fall leaves 96 out of 100, because the fall is "
             "20% of 120. For a change, the base is always the original amount, and "
             "`(new − old)/old` says so explicitly."),
        ],
        "standard": ("Finish when you set the proportion up with the units matching and exclude before you solve.",
                     "You should be able to turn a rate or a percent question into "
                     "`a/b = c/d`, name what each ratio compares, list any value that kills "
                     "a denominator, cross-multiply, solve and check. For a percent "
                     "question you should be able to say which number is the whole before "
                     "writing anything down."),
        "note": "Lesson 8 takes the same step &mdash; turning a described situation into "
                "an equation &mdash; without the proportion to hang it on, which makes "
                "naming the unknown the main decision. The excluded-value habit built here "
                "returns in course 5, where every rational equation begins with it.",
    },
]
