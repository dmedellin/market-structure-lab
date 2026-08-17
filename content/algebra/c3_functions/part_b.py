"""Course 3, lessons 08-14 - notation, domain, shape, composition, inverse, and inequalities."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "function-notation",
        "title": "Function Notation",
        "module": "Functions",
        "one_line": "f(x) is a value, not a product.",
        "summary": (
            "`f(x)` names the output that the function `f` produces from the input "
            "`x`. It is one number, not `f` multiplied by `x`, and once that is "
            "settled the notation answers two different questions: evaluate, and "
            "solve."
        ),
        "key": [
            "f(x)      the output of f at x        NOT f times x",
            "f(3)      EVALUATE: put 3 where x is",
            "f(x) = 3  SOLVE:    which inputs give 3",
            "f(a + b)  is not  f(a) + f(b)",
        ],
        "key_label": "Four lines that prevent most of the errors",
        "concepts_intro": (
            "Lesson 7 established that an input has exactly one output. This lesson "
            "gives that output a name, which is what makes every later lesson "
            "writable."
        ),
        "concepts": [
            ("The whole symbol names one number",
             "`f(3)` is a single value. The letter `f` is the name of the rule, the "
             "brackets are not multiplication, and `x` is a slot. Read `f(3)` as "
             "\"f of 3\", never as \"f times 3\", because the second reading makes "
             "`f(a + b) = fa + fb` look like the distributive law."),
            ("Evaluating is substitution, with brackets",
             "To find `f(−2)` for `f(x) = x² − 4x + 5`, write `(−2)² − 4(−2) + 5`. "
             "Every occurrence of `x` becomes `(−2)`, brackets and all. The brackets "
             "are what stop `(−2)²` from collapsing to `−4`."),
            ("Evaluate and solve are opposite questions",
             "`f(3)` hands you an input and asks for the output; there is exactly one "
             "answer. `f(x) = 3` hands you an output and asks for the inputs; there "
             "may be none, one, or many. Confusing the two is the most common error "
             "in this lesson, and both notations use the same three symbols."),
        ],
        "read_title": "Reading and using the notation",
        "read_intro": "What the symbol means, how to substitute safely, and the two questions it can pose.",
        "body": [
            ("def", ("Function notation",
                     "If `f` is a function and `x` is an input in its domain, "
                     "<strong>`f(x)`</strong> denotes the output that `f` assigns to "
                     "`x`. The letter naming the function and the letter naming the "
                     "input are both arbitrary: `f(x) = 2x + 1`, `g(t) = 2t + 1` and "
                     "`h(u) = 2u + 1` are three names for one function.",
                     "The brackets are borrowed from the brackets of multiplication, "
                     "and that is an accident of history, not a hint. Nothing in "
                     "`f(x)` is being multiplied. The notation is roughly three "
                     "hundred years old and predates any convention that would have "
                     "made it unambiguous, so the ambiguity is permanent and the only "
                     "defence is reading the whole symbol as one name.")),
            ("h3", "Evaluating at a number"),
            ("p", "Take `f(x) = x² − 4x + 5`. Substituting means replacing every `x` "
                  "with the input, wrapped in brackets, and only then simplifying."),
            ("math", [
                "f(x) = x^2 - 4x + 5",
                "",
                "f(3)  = (3)^2  - 4(3)  + 5 =  9 - 12 + 5 =  2",
                "f(0)  = (0)^2  - 4(0)  + 5 =  0 -  0 + 5 =  5",
                "f(-2) = (-2)^2 - 4(-2) + 5 =  4 +  8 + 5 = 17",
            ]),
            ("p", "The third line is where brackets earn their place. Without them "
                  "the first term reads `−2²`, which is `−4`, and the second reads "
                  "`−4·2`, which is `−8`; the total comes out `−7` instead of `17`. "
                  "Both slips are silent, because `−7` is a perfectly ordinary "
                  "number and nothing in the working looks wrong."),
            ("h3", "Evaluating at an expression"),
            ("p", "The slot accepts anything, including another expression. The "
                  "procedure does not change: replace every `x` by the whole "
                  "expression in brackets, expand, collect."),
            ("math", [
                "f(a + 1) = (a + 1)^2 - 4(a + 1) + 5",
                "         = a^2 + 2a + 1 - 4a - 4 + 5",
                "         = a^2 - 2a + 2",
                "",
                "check at a = 2:   f(3) = 2        and   2^2 - 2(2) + 2 = 2",
            ]),
            ("p", "Compare that with `f(a) + f(1)`, which is `a² − 4a + 5` plus `2`, "
                  "or `a² − 4a + 7`. The two differ at every value of `a` except "
                  "where `a² − 2a + 2 = a² − 4a + 7`, that is `2a = 5`, so they agree "
                  "only at `a = 5/2`. A function does not distribute over addition, "
                  "and a single accidental agreement is not evidence that it does."),
            ("thm", ("Functions do not distribute",
                     "For a general function `f`, `f(a + b)` and `f(a) + f(b)` are "
                     "different numbers. The error survives because it is correct for "
                     "`f(x) = cx`, the family met first: `c(a + b) = ca + cb` really "
                     "is the distributive law. A constant term is enough to break it. "
                     "For `f(x) = 2x + 1`, `f(1 + 1) = 5` while `f(1) + f(1) = 6`.")),
            ("h3", "The two questions"),
            ("ul", [
                "<strong>Evaluate.</strong> `f(3)` is a command: substitute `3`. The "
                "answer is one number, guaranteed by the definition of a function.",
                "<strong>Solve.</strong> `f(x) = 5` is an equation: find every input "
                "whose output is `5`. Here `x² − 4x + 5 = 5` gives `x² − 4x = 0`, so "
                "`x(x − 4) = 0` and the answers are `x = 0` and `x = 4`.",
                "<strong>Neither is guaranteed to have an answer.</strong> "
                "`f(x) = 0` means `x² − 4x + 5 = 0`, whose discriminant is "
                "`16 − 20 = −4`. No real input is sent to `0`.",
            ]),
            ("example", ("Reading values off a graph",
                         "A point `(3, 2)` on the graph of `f` says `f(3) = 2`, "
                         "because the graph is the set of pairs "
                         "`(input, output)`. Finding `f(3)` means reading up from "
                         "`3` on the horizontal axis; solving `f(x) = 2` means "
                         "reading across from `2` on the vertical axis and "
                         "collecting every `x` beneath. One vertical sweep, one "
                         "horizontal sweep, and they can return different numbers "
                         "of answers.")),
            ("h3", "The difference quotient"),
            ("p", "One expression is worth meeting now because it uses the notation "
                  "at full stretch and returns in calculus. For the same `f`, "
                  "`(f(x + h) − f(x))/h` measures the average rate of change between "
                  "`x` and `x + h`, which is the slope of lesson 3 with the two "
                  "points named by the function. Predict one thing before expanding: "
                  "`f(x + 0)` is `f(x)`, so the difference must vanish when `h` does, "
                  "and therefore every surviving term has to carry a factor of `h`. "
                  "If the terms without an `h` fail to cancel, the expansion is wrong."),
            ("math", [
                "f(x + h) = (x + h)^2 - 4(x + h) + 5",
                "         = x^2 + 2xh + h^2 - 4x - 4h + 5",
                "",
                "f(x + h) - f(x) = 2xh + h^2 - 4h",
                "",
                "divide by h  (h is not 0):     2x + h - 4",
            ]),
        ],
        "lab": ("funcops", {
            "mode": "notation",
            "panel_title": "Evaluate, then solve",
            "panel_intro": "Type a rule for `f` and an input; the lab shows the "
                           "substitution with the brackets in place before it "
                           "simplifies. Switch to solve mode to enter an output "
                           "instead, and watch the number of answers change.",
        }),
        "steps_title": "Evaluating without losing a sign",
        "steps_intro": "Four moves. The third is the one that goes wrong.",
        "steps": [
            ("Decide which question is being asked",
             "An input inside the brackets means evaluate. An equals sign after the "
             "brackets means solve. Answering the wrong one produces a confident, "
             "irrelevant number."),
            ("Rewrite the rule with the slot empty",
             "For `f(x) = x² − 4x + 5`, write `( )² − 4( ) + 5`. This takes five "
             "seconds and makes it impossible to substitute into some occurrences of "
             "`x` and not others."),
            ("Drop the input into every slot, brackets included",
             "`(−2)²`, not `−2²`. `−4(−2)`, not `−4−2`. When the input is negative or "
             "is itself an expression, the brackets are carrying the arithmetic, not "
             "decorating it."),
            ("Simplify, then check with a number",
             "For a symbolic answer such as `f(a + 1) = a² − 2a + 2`, put `a = 2` in "
             "both the original and the result. If `f(3)` and the new expression "
             "disagree, the expansion is wrong and you have found it in one line."),
        ],
        "worked": {
            "title": "One function, five questions",
            "intro": ["Throughout, `f(x) = x² − 4x + 5`. The questions look alike and "
                      "are not alike."],
            "lines": [
                "1.  f(3)                 (3)^2 - 4(3) + 5                    = 2",
                "",
                "2.  f(-2)                (-2)^2 - 4(-2) + 5 = 4 + 8 + 5      = 17",
                "        careless:        -2^2 - 4*2 + 5     = -4 - 8 + 5     = -7   WRONG",
                "",
                "3.  f(x) = 5             x^2 - 4x + 5 = 5",
                "                         x^2 - 4x = 0",
                "                         x(x - 4) = 0            x = 0  or  x = 4",
                "",
                "4.  f(x) = 0             x^2 - 4x + 5 = 0",
                "                         discriminant 16 - 20 = -4    no real solution",
                "",
                "5.  f(a + 1)             (a + 1)^2 - 4(a + 1) + 5",
                "                         a^2 + 2a + 1 - 4a - 4 + 5",
                "                                                    = a^2 - 2a + 2",
                "        check a = 2:     f(3) = 2      4 - 4 + 2 = 2           agrees",
            ],
            "after": [
                "Questions 1 and 3 are the pair to keep apart. Both mention `f`, `x` "
                "and a number; one has a single answer by definition, the other "
                "turned out to have two.",
                "Question 4 shows that solving can fail. The smallest value this "
                "function takes is `1`, at `x = 2`, so no input is sent to `0` and "
                "the discriminant records that fact in one number.",
                "Question 5 is worth repeating with `f(a) + f(1) = a² − 4a + 7`. The "
                "two expressions agree only at `a = 5/2`, so a spot check at that one "
                "value would wrongly suggest the shortcut works &mdash; which is why "
                "the check above uses `a = 2`.",
            ],
        },
        "quiz_title": "Notation, evaluated and solved",
        "quiz": [
            {"q": "For `f(x) = x² − 4x + 5`, what is `f(−2)`?",
             "a": ["`17`", "`1`", "`−7`", "`−1`"],
             "c": 0,
             "why": "`(−2)² − 4(−2) + 5 = 4 + 8 + 5 = 17`. `1` comes from keeping the "
                    "sign in the squared term but dropping it in the linear term, "
                    "`4 − 8 + 5`. `−7` comes from writing `−2²` without brackets, so "
                    "the square is `−4` and the linear term is `−8`. `−1` is `−f(2)`, "
                    "which treats the minus sign as something applied after the "
                    "function rather than to the input."},
            {"q": "For the same `f`, what does `f(x) = 5` give?",
             "a": ["`x = 5`",
                   "`x = 0` and `x = 4`",
                   "`x = 0` only",
                   "No real solution, since the discriminant of `x² − 4x + 5` is `−4`"],
             "c": 1,
             "why": "`x² − 4x + 5 = 5` gives `x² − 4x = 0`, so `x(x − 4) = 0` and both "
                    "`0` and `4` work. `x = 5` reads the equation as if the `5` were "
                    "the input. `x = 0` only is what is left after dividing both sides "
                    "by `x`, which discards the root `x = 4`. The last choice computes "
                    "the discriminant of `f(x) = 0`, a different equation; the "
                    "constant `5` must be moved across first."},
            {"q": "For the same `f`, which expression equals `f(a + 1)`?",
             "a": ["`a² − 2a + 2`", "`a² − 4a + 6`", "`a² − 2a + 6`", "`a² − 4a + 7`"],
             "c": 0,
             "why": "`(a + 1)² − 4(a + 1) + 5 = a² + 2a + 1 − 4a − 4 + 5 = a² − 2a + 2`, "
                    "and at `a = 2` it gives `2`, matching `f(3)`. `a² − 4a + 6` is "
                    "`f(a) + 1`, adding to the output instead of the input. "
                    "`a² − 2a + 6` distributes the `−4` onto the `a` but not the `1`. "
                    "`a² − 4a + 7` is `f(a) + f(1)`, the assumption that `f` "
                    "distributes over addition."},
        ],
        "mistakes": [
            ("Reading f(x) as f times x",
             "It is the single most productive error in the subject: it makes "
             "`f(a + b) = f(a) + f(b)` look like distribution and `f(2x) = 2f(x)` look "
             "like factoring. Neither holds for a general `f`. The brackets attach a "
             "name to an input; they never multiply."),
            ("Substituting a negative without brackets",
             "`f(−2)` with `f(x) = x²` is `(−2)² = 4`, not `−2² = −4`. The written "
             "form `−2²` means the square is taken first and then negated, so leaving "
             "the brackets out silently changes the question."),
            ("Answering the other question",
             "Asked for `f(3)`, some readers solve `f(x) = 3`; asked to solve "
             "`f(x) = 5`, some evaluate `f(5)`. The giveaway is the shape of the "
             "answer: evaluating returns one number, solving returns a set that may "
             "be empty."),
        ],
        "standard": ("Finish when you can evaluate at a number or an expression "
                     "without losing a bracket, and can tell an evaluation from an "
                     "equation on sight.",
                     "Given `f(x) = x² − 4x + 5` you should produce `f(−2) = 17` and "
                     "`f(a + 1) = a² − 2a + 2` cleanly, solve `f(x) = 5` to get "
                     "`x = 0` and `x = 4`, and explain why `f(x) = 0` has no answer. "
                     "The difference quotient `2x + h − 4` is the stretch goal, and it "
                     "is the one that pays off in lesson 12 and again in calculus."),
        "note": "Every lesson from here on is written in this notation, so the habit "
                "of reading `f(x)` as one name rather than two factors is worth "
                "forming now. Lesson 9 asks which inputs the slot is allowed to "
                "accept, which is the first question the notation makes it possible "
                "to state precisely.",
    },

    # ---------------------------------------------------------------- 09
    {
        "slug": "domain-and-range",
        "title": "Domain and Range",
        "module": "Functions",
        "one_line": "What goes in, what comes out, and what is excluded.",
        "summary": (
            "The domain is the set of inputs a function accepts; the range is the "
            "set of outputs it actually produces. In algebra only two things force "
            "an input out of the domain &mdash; a zero denominator and an even root "
            "of a negative &mdash; and the range is the harder of the two to find."
        ),
        "key": [
            "domain = every input the rule accepts",
            "range  = every output the rule produces",
            "exclude:  denominator = 0     even root of a negative",
            "[a, b] includes the ends    (a, b) excludes them    U joins pieces",
        ],
        "key_label": "The two sets, and the only two exclusions",
        "concepts_intro": (
            "Lesson 7 said a function must give an output for each input it claims. "
            "This lesson is about stating exactly what it claims."
        ),
        "concepts": [
            ("The domain is part of the function",
             "A function is a rule together with the set it accepts. `f(x) = x²` on "
             "every real number and `f(x) = x²` on `x ≥ 0` are different functions "
             "with the same formula, and lesson 13 depends on the difference. When no "
             "domain is stated, the convention is the largest set of real numbers for "
             "which the formula gives a real value."),
            ("Only two things exclude an input",
             "In this course a real input fails for one of two reasons: it makes a "
             "denominator zero, or it puts a negative number under a square root or "
             "any other even root. Everything else &mdash; adding, multiplying, "
             "cubing, taking an odd root &mdash; accepts every real number."),
            ("The range is what actually comes out",
             "The domain can be read off the formula by inspection. The range usually "
             "cannot: it needs the shape of the graph, or a completed square, or an "
             "argument about which outputs are reachable. `f(x) = x² − 6x + 7` accepts "
             "every real number but produces only values from `−2` upward."),
        ],
        "read_title": "Finding the domain, then the range",
        "read_intro": "Two exclusions to test for, interval notation to write the answer in, and the reason ranges are harder.",
        "body": [
            ("def", ("Domain and range",
                     "The <strong>domain</strong> of a function is the set of inputs "
                     "it is defined on. The <strong>range</strong> is the set of "
                     "outputs it produces: every value `y` for which some `x` in the "
                     "domain has `f(x) = y`. The range is a set of values actually "
                     "attained, not a set of values that look permitted.")),
            ("p", "When a function arrives as a bare formula, the domain is not "
                  "stated and has to be inferred. The convention is the <em>natural "
                  "domain</em>: every real number for which the formula produces a "
                  "real value. This is a convention, chosen because it is the "
                  "largest sensible default, and a problem is free to override it by "
                  "naming a smaller set."),
            ("h3", "The two exclusions"),
            ("ul", [
                "<strong>A zero denominator.</strong> Division by zero is undefined, "
                "so set every denominator equal to zero, solve, and exclude the "
                "solutions. For `(x + 2)/(x² − 5x + 6)`, factor the bottom as "
                "`(x − 2)(x − 3)`; the excluded inputs are `2` and `3`.",
                "<strong>An even root of a negative.</strong> `√(2x − 7)` needs "
                "`2x − 7 ≥ 0`, so `x ≥ 7/2`. Write the exact fraction, not `3.5`. "
                "Fourth roots, sixth roots and so on behave the same way; cube roots "
                "do not: the cube root of `−8` is `−2`, a perfectly real value.",
            ]),
            ("p", "When both appear, both conditions must hold at once. For "
                  "`√(x + 4)/(x − 1)` the numerator demands `x ≥ −4` and the "
                  "denominator forbids `x = 1`, so the domain is `[−4, 1) ∪ (1, ∞)`. "
                  "Note that `−4` is included: `√0 = 0` is a perfectly good output. "
                  "It is the denominator, not the root, that produces an open end."),
            ("math", [
                "f(x) = (x + 2)/(x^2 - 5x + 6)     bottom = (x - 2)(x - 3)",
                "                                  domain: x =/= 2, x =/= 3",
                "",
                "g(x) = sqrt(2x - 7)               2x - 7 >= 0   ->  x >= 7/2",
                "",
                "h(x) = sqrt(x + 4)/(x - 1)        x >= -4  AND  x =/= 1",
                "                                  domain: [-4, 1) U (1, inf)",
                "",
                "k(x) = sqrt(9 - x^2)              9 - x^2 >= 0  ->  -3 <= x <= 3",
            ]),
            ("p", "The last one is worth slowing down for. `9 − x² ≥ 0` is `x² ≤ 9`, "
                  "and the inputs whose square is at most `9` are those between `−3` "
                  "and `3` inclusive. Taking a square root of both sides of `x² ≤ 9` "
                  "and writing `x ≤ 3` loses the whole left half of the answer; this "
                  "is the absolute value inequality from course 2, lesson 12, in a "
                  "new costume."),
            ("h3", "Why the range is harder"),
            ("p", "The domain is a question about the formula: which inputs does it "
                  "choke on. The range is a question about the function's behaviour "
                  "across its whole domain, and there is no equivalent checklist. "
                  "Three tools cover most cases at this level."),
            ("ol", [
                "<strong>Completing the square,</strong> for a quadratic. "
                "`x² − 6x + 7 = (x − 3)² − 2`. A square is never negative, so the "
                "output is never below `−2`, and it equals `−2` when `x = 3`. The "
                "range is `[−2, ∞)`.",
                "<strong>Tracking the outer operation,</strong> for a root. "
                "`√(9 − x²)` takes the square root of something running from `0` up "
                "to `9`, so the outputs run from `0` to `3`, giving `[0, 3]`.",
                "<strong>Solving for the input,</strong> in general. Ask which `y` "
                "make `f(x) = y` solvable. For `f(x) = 1/(x − 3)`, solving gives "
                "`x = 3 + 1/y`, which needs `y ≠ 0`; the range is every real number "
                "except `0`.",
            ]),
            ("example", ("A hole that the formula hides",
                         "`q(x) = (x² − 9)/(x − 3)` cancels to `x + 3`, but only "
                         "where the cancellation is legal. The domain is still "
                         "`x ≠ 3`, because the original expression divides by `x − 3` "
                         "before any simplifying happens. The graph is the line "
                         "`y = x + 3` with the single point `(3, 6)` removed, so the "
                         "range is every real number except `6`. Simplifying an "
                         "expression can change its domain; it never changes the "
                         "function that was written down.")),
            ("h3", "Writing the answer"),
            ("p", "Interval notation from course 2, lesson 13, is the expected form. "
                  "A square bracket includes the endpoint, a round bracket excludes "
                  "it, and `∞` always takes a round bracket because it is not a "
                  "number that can be attained. Use `∪` to join the pieces when an "
                  "excluded point splits the domain, and list the pieces in "
                  "increasing order."),
            ("p", "One habit is worth building: after writing a domain, test a value "
                  "just inside each end and one value that should be excluded. For "
                  "`[−4, 1) ∪ (1, ∞)` try `x = −4`, which gives `0/(−5) = 0`, and "
                  "`x = 1`, which divides by zero. Two substitutions confirm both "
                  "boundary decisions in about ten seconds."),
        ],
        "lab": ("funcops", {
            "mode": "domain",
            "panel_title": "Excluded inputs, shown",
            "panel_intro": "Enter a formula; the lab marks the inputs it refuses and "
                           "says which of the two exclusions caused each one. Try "
                           "`sqrt(x+4)/(x-1)` and watch the left end stay closed "
                           "while `1` opens up.",
        }),
        "steps_title": "Finding a domain in four passes",
        "steps_intro": "Scan for each exclusion separately, then combine. Combining first is where answers go missing.",
        "steps": [
            ("List every denominator",
             "Including denominators buried inside a root or a compound fraction. Set "
             "each to zero, solve, and mark those inputs as excluded. Factor first: "
             "`x² − 5x + 6` hides two exclusions until it becomes `(x − 2)(x − 3)`."),
            ("List every even root",
             "Square roots, fourth roots, and any rational exponent with an even "
             "denominator. Each contributes an inequality of the form "
             "\"the inside is at least zero\". Odd roots contribute nothing."),
            ("Solve each condition on its own",
             "Keep the conditions separate while you solve them. `9 − x² ≥ 0` needs "
             "the two-sided answer `−3 ≤ x ≤ 3`, and mixing it with another "
             "condition before it is solved is how one half of it disappears."),
            ("Intersect, then write it in intervals",
             "Every condition must hold at once, so take the overlap, not the union. "
             "The union symbol appears in the written answer only because excluded "
             "points cut the overlap into pieces."),
        ],
        "worked": {
            "title": "Four domains and two ranges",
            "intro": ["The domains first, since they are mechanical. The ranges "
                      "afterwards, since they are not."],
            "lines": [
                "1.  f(x) = (x + 2)/(x^2 - 5x + 6)",
                "        x^2 - 5x + 6 = (x - 2)(x - 3) = 0   ->  x = 2, x = 3",
                "        domain   (-inf, 2) U (2, 3) U (3, inf)",
                "",
                "2.  g(x) = sqrt(2x - 7)",
                "        2x - 7 >= 0  ->  x >= 7/2",
                "        domain   [7/2, inf)              note 7/2, not 3.5",
                "",
                "3.  h(x) = sqrt(x + 4)/(x - 1)",
                "        x + 4 >= 0  ->  x >= -4          x - 1 =/= 0  ->  x =/= 1",
                "        domain   [-4, 1) U (1, inf)",
                "        check    x = -4:  0/(-5) = 0     defined, so -4 is IN",
                "                 x = 1:   division by 0  excluded",
                "",
                "4.  k(x) = sqrt(9 - x^2)",
                "        9 - x^2 >= 0  ->  x^2 <= 9  ->  -3 <= x <= 3",
                "        domain   [-3, 3]",
                "",
                "ranges",
                "",
                "5.  p(x) = x^2 - 6x + 7 = (x - 3)^2 - 2",
                "        (x - 3)^2 >= 0, and equals 0 at x = 3",
                "        range    [-2, inf)               p(3) = 9 - 18 + 7 = -2",
                "",
                "6.  k(x) = sqrt(9 - x^2)   on  [-3, 3]",
                "        9 - x^2 runs from 0 (at x = +-3) up to 9 (at x = 0)",
                "        range    [0, 3]",
            ],
            "after": [
                "Line 3 is the one that decides whether the technique has been "
                "understood. Both exclusions are present, they come from different "
                "parts of the expression, and the left end is closed while the "
                "interior point is open. Reading `[−4, 1) ∪ (1, ∞)` back out loud as "
                "\"from `−4` inclusive, everything except `1`\" is a fair test.",
                "Line 5 shows the range depending on a rewrite. In the form "
                "`x² − 6x + 7` nothing about `−2` is visible; in the form "
                "`(x − 3)² − 2` it is the only constant in sight. The two "
                "expressions are equal at every input, and the second answers a "
                "question the first cannot.",
                "Line 6 reuses the domain found in line 4. A range can only be found "
                "over a known domain, so the order is never optional: domain first, "
                "always.",
            ],
        },
        "quiz_title": "In, out and excluded",
        "quiz": [
            {"q": "What is the domain of `f(x) = √(x + 4)/(x − 1)`?",
             "a": ["`[−4, ∞)`",
                   "`[−4, 1) ∪ (1, ∞)`",
                   "`(−4, 1) ∪ (1, ∞)`",
                   "`(−∞, −4] ∪ (1, ∞)`"],
             "c": 1,
             "why": "Two conditions hold at once: `x + 4 ≥ 0` gives `x ≥ −4`, and "
                    "`x − 1 ≠ 0` removes `1`. The first choice solves the root and "
                    "forgets the denominator. The third wrongly opens the left end, "
                    "but `x = −4` gives `√0/(−5) = 0`, a perfectly good output. The "
                    "fourth solves `x + 4 ≥ 0` backwards, keeping the inputs that "
                    "make the root imaginary."},
            {"q": "What is the range of `f(x) = x² − 6x + 7`?",
             "a": ["`[−2, ∞)`", "`[0, ∞)`", "`[3, ∞)`", "`(−∞, −2]`"],
             "c": 0,
             "why": "`x² − 6x + 7 = (x − 3)² − 2`, and `(x − 3)²` is never negative "
                    "and is `0` at `x = 3`, so the smallest output is `−2`. `[0, ∞)` "
                    "assumes the square alone controls the sign and ignores the `−2`. "
                    "`[3, ∞)` quotes the input at which the minimum happens rather "
                    "than the output. `(−∞, −2]` has the right boundary and the wrong "
                    "direction; the parabola opens upward, since the coefficient of "
                    "`x²` is positive."},
            {"q": "`g(x) = (x² − 9)/(x − 3)` simplifies to `x + 3`. What is its range?",
             "a": ["Every real number",
                   "Every real number except `3`",
                   "Every real number except `6`",
                   "Every real number except `0`"],
             "c": 2,
             "why": "Cancelling changes the expression, not the function: `x = 3` is "
                    "still divided out, so it is still excluded, and the output it "
                    "would have produced is `3 + 3 = 6`. The first choice reads the "
                    "range off the simplified line and misses the hole. The second "
                    "copies the excluded <em>input</em> into the range. The fourth "
                    "assumes `0` is missing, but `x = −3` gives `0` and `−3` is in "
                    "the domain."},
        ],
        "mistakes": [
            ("Simplifying first and reading the domain second",
             "`(x² − 9)/(x − 3)` is undefined at `3` no matter how the expression is "
             "rewritten. Find the domain from the expression as written, then "
             "simplify. Doing it the other way round invents inputs the function "
             "never accepted."),
            ("Opening an endpoint that a root leaves closed",
             "`√(x + 4)` is defined at `x = −4`, because `√0 = 0`. Only a strict "
             "inequality or a zero denominator opens an end, and a square root "
             "produces a non-strict one."),
            ("Losing half of a squared inequality",
             "`9 − x² ≥ 0` is `x² ≤ 9`, which is `−3 ≤ x ≤ 3`. Rooting both sides to "
             "get `x ≤ 3` keeps every large negative input, all of which make the "
             "inside negative. Solve it as an absolute value inequality: `|x| ≤ 3`."),
        ],
        "standard": ("Finish when you can state a domain from the formula in one "
                     "pass, and can find the range of a quadratic or a simple root "
                     "with a reason attached.",
                     "Given a mixture of rational and radical expressions you should "
                     "produce the domain in interval notation, with the right "
                     "bracket at each end, and be able to justify each excluded input "
                     "by naming which of the two exclusions caused it. For ranges, "
                     "completing the square and tracking the outer operation should "
                     "be automatic; the general method of solving `f(x) = y` for `x` "
                     "is the one that carries into lesson 13."),
        "note": "Domain restrictions are the reason lesson 13 needs a restriction at "
                "all, and the reason a composite in lesson 12 can have a smaller "
                "domain than either function it was built from. Lesson 10 takes the "
                "idea one step further: a function whose domain is deliberately cut "
                "into pieces, with a different formula on each.",
    },

    # ---------------------------------------------------------------- 10
    {
        "slug": "piecewise-functions",
        "title": "Piecewise Functions",
        "module": "Functions",
        "one_line": "One function, several formulas, and the joins between them.",
        "summary": (
            "A piecewise function splits its domain into pieces and gives a separate "
            "formula on each. It is one function, not several: the conditions decide "
            "which formula applies, and they must cover each input exactly once."
        ),
        "key": [
            "          -x - 1     if x < -1",
            "f(x) =     x^2       if -1 <= x < 2",
            "          8 - 2x     if x >= 2",
            "conditions must not overlap, or the rule is not a function",
        ],
        "key_label": "One function in three lines",
        "concepts_intro": (
            "The definition in lesson 7 says nothing about a function being given by "
            "a single formula. It never did; this lesson takes the permission."
        ),
        "concepts": [
            ("The conditions do the choosing",
             "To evaluate, first read the conditions and find the one your input "
             "satisfies; only then use the matching formula. Evaluating first and "
             "checking the condition afterwards produces an answer from the wrong "
             "branch, and it will look reasonable."),
            ("The pieces must not overlap",
             "If two conditions accept the same input and the formulas disagree "
             "there, the rule assigns two outputs and is not a function. Watch the "
             "endpoints: `x ≤ 3` and `x ≥ 3` overlap at `3`, while `x &lt; 3` and "
             "`x ≥ 3` do not. One symbol is the whole difference."),
            ("A gap is legal; it just shrinks the domain",
             "`x &lt; 3` paired with `x &gt; 3` defines a perfectly good function "
             "whose domain omits `3`. That is a domain statement, not an error. Only "
             "an overlap with disagreeing values breaks the definition."),
        ],
        "read_title": "Reading, evaluating and drawing a piecewise rule",
        "read_intro": "The notation, the endpoint discipline, and what happens where two pieces meet.",
        "body": [
            ("def", ("Piecewise function",
                     "A <strong>piecewise</strong> function is defined by splitting "
                     "its domain into pieces and giving a formula for each piece. "
                     "For the rule to be a function, each input in the domain must "
                     "satisfy exactly one condition &mdash; the conditions partition "
                     "the domain.")),
            ("p", "The most familiar example was written down long before the "
                  "notation was: absolute value. `|x|` is `x` when `x` is at least "
                  "zero and `−x` when `x` is negative, which is two formulas and a "
                  "condition. Course 1, lesson 4 called the two cases a definition; "
                  "the piecewise brace is that definition typeset."),
            ("math", [
                "          x      if x >= 0",
                "|x| =",
                "         -x      if x < 0",
                "",
                "|-7| = -(-7) = 7        the second line, because -7 < 0",
                "| 7| =    7            the first line",
            ]),
            ("p", "Note that the second formula, `−x`, produces positive outputs. It "
                  "looks as though it should produce negative ones, and that reading "
                  "is what makes `|x| = −x` seem wrong. The minus sign is applied to "
                  "an input that is already negative."),
            ("h3", "A three-piece example"),
            ("p", "Take the function in the box at the top of this page: `−x − 1` "
                  "below `−1`, `x²` from `−1` up to but not including `2`, and "
                  "`8 − 2x` from `2` upward. The conditions cover every real number "
                  "once, so the domain is every real number."),
            ("math", [
                "f(-3) = -(-3) - 1 = 2          -3 < -1        first piece",
                "f(-1) = (-1)^2    = 1          -1 <= -1 < 2   second piece",
                "f( 0) = 0^2       = 0                         second piece",
                "f( 2) = 8 - 2(2)  = 4           2 >= 2        third piece",
                "f( 5) = 8 - 2(5)  = -2                        third piece",
                "",
                "the wrong branch at x = -1:  8 - 2(-1) = 10   condition fails",
            ]),
            ("p", "The last line is the error this lesson exists to prevent. `10` is "
                  "a real number produced by a real formula belonging to this very "
                  "function, and nothing about it looks suspect. Only the condition "
                  "`x ≥ 2` rules it out, and the condition is the part that gets "
                  "skipped."),
            ("h3", "What happens at a join"),
            ("p", "At `x = −1` the two neighbouring formulas disagree. Approaching "
                  "from the left, `−x − 1` heads toward `0`; the value the function "
                  "actually takes there is `(−1)² = 1`. The graph steps up by `1`, "
                  "and it is drawn with an open circle at `(−1, 0)` and a filled "
                  "circle at `(−1, 1)`."),
            ("p", "At `x = 2` they agree. The left formula `x²` heads toward `4`, and "
                  "the right formula gives `8 − 2(2) = 4`. The two pieces meet, so "
                  "the graph connects with no break and no circles are needed. "
                  "Whether a join is a step or a connection is settled by arithmetic, "
                  "not by how the formulas look."),
            ("math", [
                "join at x = -1        left formula -x - 1  ->   0",
                "                      value used   x^2     ->   1      step of 1",
                "",
                "join at x =  2        left formula x^2     ->   4",
                "                      value used   8 - 2x  ->   4      they meet",
            ]),
            ("h3", "Endpoints, and where the dot goes"),
            ("ul", [
                "<strong>A filled circle</strong> marks a point the function attains. "
                "Every input in the domain gets exactly one filled circle in the "
                "whole picture.",
                "<strong>An open circle</strong> marks a point the graph approaches "
                "but does not include, because the condition on that piece excluded "
                "the endpoint.",
                "<strong>A vertical stack of two filled circles is impossible.</strong> "
                "Two filled circles above the same input would be two outputs, and "
                "the vertical line test from lesson 7 rules it out on sight.",
            ]),
            ("example", ("Overlap, gap, and neither",
                         "`{x + 1 if x ≤ 3; 2x if x ≥ 3}` is not a function: at `3` "
                         "the first line says `4` and the second says `6`. "
                         "`{x + 1 if x &lt; 3; 2x if x &gt; 3}` is a function whose "
                         "domain omits `3`. `{x + 1 if x ≤ 3; 2x if x &gt; 3}` is a "
                         "function on every real number. Three rules, one symbol "
                         "apart, and only the first is broken.")),
            ("p", "An overlap is harmless when the formulas happen to agree on it. "
                  "`{2x if x ≤ 3; x + 3 if x ≥ 3}` names `3` twice, but both lines "
                  "give `6`, so each input still has one output. This is worth "
                  "knowing and not worth relying on: writing the conditions so they "
                  "cannot overlap removes the need to check."),
        ],
        "lab": ("funcops", {
            "mode": "piecewise",
            "panel_title": "Set the pieces, watch the joins",
            "panel_intro": "Edit the formulas and the cut points; the lab draws each "
                           "piece over its own condition and reports the size of the "
                           "step at every join. A join of size `0` is where the graph "
                           "connects.",
        }),
        "steps_title": "Evaluating and sketching a piecewise rule",
        "steps_intro": "The order is condition, then formula. Reversing it is the whole error.",
        "steps": [
            ("Check the conditions cover the input once",
             "Before anything else, confirm that the pieces do not overlap and see "
             "where they leave gaps. A gap tells you the domain; an overlap with "
             "disagreeing formulas tells you the rule is not a function."),
            ("Find the condition your input satisfies",
             "Compare the input against each condition in turn. Write down which "
             "piece won before evaluating anything, so the choice is a decision "
             "rather than an assumption."),
            ("Evaluate only the matching formula",
             "The other formulas are not merely unhelpful, they are not part of the "
             "answer. At `x = −1` the third piece returns `10`, and `10` is not a "
             "value this function takes anywhere."),
            ("At each join, evaluate both neighbours",
             "Compute the left formula and the right formula at the cut point. Equal "
             "values mean the graph connects; different values give the size of the "
             "step, and tell you which endpoint gets the open circle."),
        ],
        "worked": {
            "title": "One three-piece function, evaluated and joined",
            "intro": ["The function from the top of the page, at six inputs and both "
                      "of its joins."],
            "lines": [
                "          -x - 1     if x < -1",
                "f(x) =     x^2       if -1 <= x < 2",
                "          8 - 2x     if x >= 2",
                "",
                "input      condition met        formula          value",
                "-----      -------------        -------          -----",
                "  -3       -3 < -1              -(-3) - 1          2",
                "  -2       -2 < -1              -(-2) - 1          1",
                "  -1       -1 <= -1 < 2         (-1)^2             1",
                "   0       -1 <=  0 < 2         0^2                0",
                "   2        2 >= 2              8 - 2(2)           4",
                "   5        5 >= 2              8 - 2(5)          -2",
                "",
                "joins",
                "",
                "  x = -1   left  -x - 1 ->  0      open circle at (-1, 0)",
                "           value  x^2   ->  1      filled circle at (-1, 1)",
                "           the graph steps up by 1",
                "",
                "  x =  2   left   x^2   ->  4",
                "           value 8 - 2x ->  4      the pieces meet; no circles",
            ],
            "after": [
                "The row for `x = −1` is the one to check twice. It sits on the "
                "boundary, and the condition that wins is the one written with `≤`. "
                "Change that symbol to `&lt;` and `−1` leaves the domain entirely.",
                "The two joins behave differently for a reason visible in the "
                "arithmetic and nowhere else. `−x − 1` and `x²` disagree at `−1`; "
                "`x²` and `8 − 2x` agree at `2`. Nothing about the shapes of the "
                "formulas predicts this, so both joins have to be computed.",
                "Reading a range off the picture: the third piece runs from `4` "
                "downward without bound, and the first piece runs from just above "
                "`0` upward without bound, so between them every real number is "
                "produced. The range is every real number, even though no single "
                "piece has that range.",
            ],
        },
        "quiz_title": "Which piece, and what happens there",
        "quiz": [
            {"q": "For `f` above, what is `f(−1)`?",
             "a": ["`1`", "`0`", "`10`", "Undefined, since two conditions mention `−1`"],
             "c": 0,
             "why": "`−1` satisfies `−1 ≤ x &lt; 2`, so the second piece applies and "
                    "`(−1)² = 1`. `0` comes from the first piece, `−x − 1`, whose "
                    "condition `x &lt; −1` `−1` does not satisfy. `10` comes from the "
                    "third piece, `8 − 2(−1)`, which is further out of range still. "
                    "The last choice misreads the conditions: `−1` appears in two of "
                    "them as a boundary, but satisfies only one."},
            {"q": "Where does the graph of `f` have a step?",
             "a": ["At `x = −1` only", "At `x = 2` only", "At both joins", "At neither join"],
             "c": 0,
             "why": "At `x = −1` the left formula gives `−(−1) − 1 = 0` while the "
                    "value taken is `(−1)² = 1`, a step of `1`. At `x = 2` the left "
                    "formula gives `2² = 4` and the right gives `8 − 2(2) = 4`, so "
                    "the pieces meet. A join is a step or not according to whether "
                    "the two numbers differ, and here one join does and one does not."},
            {"q": "Which of these fails to define a function?",
             "a": ["`{x + 1 if x ≤ 3; 2x if x &gt; 3}`",
                   "`{x + 1 if x ≤ 3; 2x if x ≥ 3}`",
                   "`{x + 1 if x &lt; 3; 2x if x &gt; 3}`",
                   "`{x + 1 if x &lt; 3; 2x if x ≥ 3}`"],
             "c": 1,
             "why": "In the second, `x = 3` satisfies both conditions, and the two "
                    "formulas give `4` and `6`. One input, two outputs, so it is not "
                    "a function. The third also treats `3` unusually, but by leaving "
                    "it out: that is a function whose domain omits `3`, which is "
                    "legal. The first and fourth each assign `3` to exactly one "
                    "piece."},
        ],
        "mistakes": [
            ("Evaluating first and checking the condition afterwards",
             "Substituting into whichever formula is nearest gives a plausible number "
             "from the wrong branch. At `x = −1` the third piece returns `10`, a "
             "value this function never takes. Read the conditions first, every time."),
            ("Writing both endpoint conditions with a non-strict sign",
             "`x ≤ 3` beside `x ≥ 3` claims `3` twice. If the formulas disagree "
             "there, the rule is not a function at all. Exactly one of the two "
             "conditions at each cut point should include the endpoint."),
            ("Assuming a join is a break",
             "Two different formulas can meet. At `x = 2`, `x²` and `8 − 2x` both "
             "give `4`, so the graph connects and neither endpoint needs a circle. "
             "Evaluate both sides rather than drawing a jump because the formulas "
             "look different."),
        ],
        "standard": ("Finish when you evaluate by reading the condition first, and "
                     "can say at each join whether the graph steps or connects, with "
                     "the two numbers that settle it.",
                     "Given a two- or three-piece definition you should evaluate at "
                     "any input including the cut points, decide whether the "
                     "conditions partition the domain, sketch the graph with open and "
                     "filled circles in the right places, and state the domain and "
                     "range. Recognising `|x|` as a piecewise function is the check "
                     "that the idea has landed."),
        "note": "Piecewise definitions are how a domain restriction becomes visible "
                "in a formula, and lesson 13 uses exactly that device: a function is "
                "cut down to a piece on which it can be inverted. Lesson 11 leaves "
                "formulas alone and asks a different question: what moving the graph "
                "does to the rule.",
    },

    # ---------------------------------------------------------------- 11
    {
        "slug": "transformations-of-graphs",
        "title": "Transformations of Graphs",
        "module": "Functions",
        "one_line": "Shift, stretch and reflect, from the parent curve.",
        "summary": (
            "Changing a formula in four standard ways moves its graph in four "
            "predictable ways. Everything done outside the function acts on the "
            "output and behaves as written; everything done inside acts on the input "
            "and behaves in the opposite direction."
        ),
        "key": [
            "y = a f(b(x - h)) + k",
            "outside x:  a stretches by |a|,  k shifts up      as written",
            "inside  x:  b squashes by 1/|b|, h shifts right   the other way",
            "a < 0 flips over the x-axis     b < 0 flips over the y-axis",
        ],
        "key_label": "One template, four controls",
        "concepts_intro": (
            "A handful of parent curves and four moves generate most of the graphs "
            "in the rest of this path, so the moves are worth understanding rather "
            "than memorising."
        ),
        "concepts": [
            ("Outside acts on the output, and reads normally",
             "In `2f(x) + 5` the function runs first and the result is doubled and "
             "raised by `5`. Output changes are vertical, and they do what the "
             "symbols suggest: `+5` is up, `×2` is taller, a minus sign flips the "
             "picture over the horizontal axis."),
            ("Inside acts on the input, and reads backwards",
             "In `f(x − 3)` the input is altered before `f` sees it. The new graph at "
             "`x = 5` shows the old value at `2`, so the whole picture moves right by "
             "`3`, not left. Every horizontal effect is inverted this way, and it "
             "catches everyone the first time."),
            ("Factor the inside before reading it",
             "`f(2x + 6)` is not a shift by `6`. Writing it as `f(2(x + 3))` shows a "
             "squash by `1/2` and a shift left by `3`. Until `b` is factored out, the "
             "number next to it is not the shift."),
        ],
        "read_title": "The four moves and the order they compose in",
        "read_intro": "Why inside and outside behave differently, what each constant does, and how to read a formula that combines them.",
        "body": [
            ("def", ("Parent function",
                     "A <strong>parent function</strong> is the simplest member of a "
                     "family, carrying the family's shape and nothing else: `x`, "
                     "`x²`, `|x|`, `√x`, `1/x`, `x³`. Every graph in this lesson is "
                     "described as a parent plus a list of moves, which is shorter "
                     "and more reliable than plotting points.")),
            ("h3", "Why inside is backwards"),
            ("p", "This is the one point in the lesson that repays a proof rather "
                  "than a rule. Nothing about the graph of `f` changes; what changes "
                  "is which input is asked for."),
            ("proof", [
                "Let `g(x) = f(x − 3)`. Take any point `(t, f(t))` on the graph of "
                "`f`. Ask where `g` takes that same value: `g(x) = f(t)` as soon as "
                "`x − 3 = t`, which is `x = t + 3`.",
                "So the point `(t, f(t))` on the graph of `f` corresponds to the "
                "point `(t + 3, f(t))` on the graph of `g`. Same height, input three "
                "larger. Every point moves three to the right, so the graph does.",
                "The subtraction inside produces an addition to the coordinate "
                "because the equation `x − 3 = t` is solved for `x`. That single "
                "rearrangement is the entire reason horizontal effects are inverted, "
                "and it applies equally to the stretch: `g(x) = f(2x)` takes the "
                "value `f(t)` at `x = t/2`, so distances from the vertical axis are "
                "halved.",
            ]),
            ("h3", "The four moves"),
            ("ul", [
                "<strong>`f(x) + k`.</strong> Vertical shift. Up if `k` is positive, "
                "down if negative. The `x`-values are untouched.",
                "<strong>`a f(x)`.</strong> Vertical stretch by `|a|`, and a "
                "reflection over the horizontal axis when `a` is negative. Points on "
                "the horizontal axis stay put, since `a·0 = 0`.",
                "<strong>`f(x − h)`.</strong> Horizontal shift, right by `h`. Written "
                "with a minus sign inside, so `f(x + 4)` is `h = −4` and moves left.",
                "<strong>`f(bx)`.</strong> Horizontal squash toward the vertical axis "
                "by a factor of `1/|b|`, and a reflection over the vertical axis when "
                "`b` is negative. `f(2x)` is half as wide, not twice as wide.",
            ]),
            ("p", "The two reflections are worth separating. `−f(x)` negates the "
                  "output and turns the picture upside down; `f(−x)` negates the "
                  "input and turns it left to right. For `f(x) = x²` they do not "
                  "agree: `−f(x) = −x²` is the parabola upside down, while "
                  "`f(−x) = (−x)² = x²` is the original curve unchanged, because a "
                  "parabola is already symmetric about the vertical axis. It is the "
                  "horizontal flip leaving no visible trace that makes `x²` a poor "
                  "curve to learn reflections on. Try them on `√x` instead: `−√x` "
                  "sits below the axis, while `√(−x)` sits to the left of it."),
            ("h3", "Reading a combined formula"),
            ("p", "Take `y = −2(x − 3)² + 5`, a parabola in the template's shape with "
                  "`a = −2`, `b = 1`, `h = 3`, `k = 5`. From the parent `x²`: move "
                  "right `3`, stretch vertically by `2`, flip over the horizontal "
                  "axis, move up `5`. The vertex, which sits at `(0, 0)` on the "
                  "parent, lands at `(3, 5)`."),
            ("math", [
                "y = -2(x - 3)^2 + 5          vertex (3, 5), opening downward",
                "",
                "x        0     1     2     3     4     5     6",
                "y      -13    -3     3     5     3    -3   -13",
                "",
                "symmetric about x = 3: the values at 2 and 4 agree, as do 1 and 5",
                "",
                "y-intercept   x = 0:   -2(0 - 3)^2 + 5 = -2(9) + 5 = -13",
                "x-intercepts  y = 0:   (x - 3)^2 = 5/2    x = 3 +- sqrt(10)/2",
            ]),
            ("p", "The `y`-intercept is where two arithmetic slips hide. Squaring "
                  "term by term turns `(0 − 3)²` into `0 − 9`, giving `+23`; "
                  "multiplying the `−2` in before squaring turns the whole bracket "
                  "into `(6)²`, giving `41`. They are wrong for different reasons: "
                  "the first distributes the exponent across a subtraction, and "
                  "`(a − b)²` is not `a² − b²`; the second multiplies before "
                  "squaring, where the exponent binds tighter than the "
                  "multiplication in front of it. What both miss is that the square "
                  "applies to the whole bracket, which has to be evaluated first."),
            ("h3", "When a horizontal stretch and a shift are combined"),
            ("p", "`y = √(2x + 6)` is the case that separates rule-following from "
                  "understanding. The `6` is not a shift. Factor the `2` out of the "
                  "whole input first: `√(2(x + 3))`, so the shift is `3`, matching "
                  "the domain `2x + 6 ≥ 0`, that is `x ≥ −3`."),
            ("math", [
                "sqrt(2x + 6) = sqrt(2(x + 3))       domain x >= -3",
                "",
                "squash by 1/2, then left 3      sqrt(2(x + 3)) = sqrt(2x + 6)   yes",
                "left 6, then squash by 1/2      sqrt(2x + 6)                    yes",
                "left 3, then squash by 1/2      sqrt(2x + 3)                    no",
                "squash by 1/2, then left 6      sqrt(2(x + 6)) = sqrt(2x + 12)  no",
                "",
                "the starting point (0, 0) moves to (-3, 0)",
            ]),
            ("p", "Two of those four orders reach the right graph and two do not, so "
                  "the order and the numbers have to be quoted together. Shifting "
                  "before squashing needs the raw `6`; squashing before shifting "
                  "needs the factored `3`. A description that names one order and "
                  "the other order's number is simply a different graph."),
            ("example", ("Same shape, four ways to say it",
                         "`y = |x − 2| + 1` is `|x|` moved right `2` and up `1`, with "
                         "its corner at `(2, 1)`. `y = −|x − 2| + 1` flips it "
                         "downward about the horizontal axis, keeping the corner at "
                         "`(2, 1)`, since the flip happens after the shift right and "
                         "the corner already has output `0` before the `+1`. Check "
                         "one point rather than trusting the sentence: at `x = 4`, "
                         "the first gives `2 + 1 = 3` and the second `−2 + 1 = −1`.")),
        ],
        "lab": ("transform", {
            "mode": "all",
            "panel_title": "Four sliders, one parent",
            "panel_intro": "Pick a parent curve and move `a`, `b`, `h` and `k`. The "
                           "parent stays on screen in outline, so the effect of each "
                           "constant is visible on its own. Watch `h` while it is "
                           "positive: the curve goes right.",
        }),
        "steps_title": "Describing a graph from its formula",
        "steps_intro": "Identify the parent, factor the input, then read the constants in a fixed order.",
        "steps": [
            ("Name the parent",
             "Strip every constant and see what shape is left: `x²`, `√x`, `|x|`, "
             "`1/x`, `x³`. Everything after this step is a description of how that "
             "one shape has been moved."),
            ("Factor the coefficient out of the input",
             "Turn `f(2x + 6)` into `f(2(x + 3))` before reading anything horizontal. "
             "Skipping this is the single most common source of a wrong shift, "
             "because `6` is sitting there looking like the answer."),
            ("Read the outside constants as written",
             "`a` scales the output and flips it when negative; `k` raises it. These "
             "need no reinterpretation, which is why doing the vertical part first "
             "builds confidence for the horizontal part."),
            ("Read the inside constants backwards, then verify one point",
             "`h` shifts right when it is subtracted; `b` squashes by `1/|b|`. Then "
             "substitute a single input into the original formula and check the point "
             "lands where the description predicts. One substitution catches almost "
             "every misread."),
        ],
        "worked": {
            "title": "Two formulas, described and checked",
            "intro": ["The first combines every vertical move; the second is the "
                      "horizontal case that has to be factored."],
            "lines": [
                "1.  y = -2(x - 3)^2 + 5        parent  y = x^2",
                "",
                "        a = -2   b = 1   h = 3   k = 5",
                "        right 3, stretch vertically by 2, flip down, up 5",
                "        vertex (0, 0)  ->  (3, 5)",
                "",
                "        check   x = 4:   -2(4 - 3)^2 + 5 = -2(1) + 5 =  3",
                "                x = 2:   -2(2 - 3)^2 + 5 = -2(1) + 5 =  3",
                "                x = 0:   -2(0 - 3)^2 + 5 = -2(9) + 5 = -13",
                "",
                "        wrong ways to get the last one:",
                "                -2(0^2 - 3^2) + 5 = -2(-9) + 5 =  23     squared termwise",
                "                (-2(0 - 3))^2 + 5 =     6^2  + 5 =  41   multiplied first",
                "",
                "2.  y = sqrt(2x + 6) - 1       parent  y = sqrt(x)",
                "",
                "        factor:  sqrt(2(x + 3)) - 1",
                "        a = 1   b = 2   h = -3   k = -1",
                "        squash horizontally by 1/2, left 3, down 1",
                "        start   (0, 0)  ->  (-3, -1)",
                "",
                "        check   x = -3:  sqrt(0) - 1 = -1                 the endpoint",
                "                x = -1:  sqrt(4) - 1 =  1",
                "                x =  5:  sqrt(16) - 1 = 3",
                "        domain  2x + 6 >= 0  ->  x >= -3   agrees with left 3",
            ],
            "after": [
                "In the first formula the vertex is readable without any arithmetic, "
                "which is the point of the template form. In the second the domain "
                "and the shift are two views of one fact, and they agree: the curve "
                "starts at `x = −3` because it has been moved three to the left.",
                "The two wrong lines under the first example produce `23` and `41`, "
                "both from misplacing the square. Neither is a sign error, so "
                "checking the sign of the answer would not catch either one. "
                "Substituting a second input, `x = 6`, gives `−13` again and confirms "
                "the symmetry about `x = 3`.",
                "The domain check in the second example is the cheapest verification "
                "available for any horizontal transformation of a root. If the domain "
                "and the described shift disagree, the factoring was wrong.",
            ],
        },
        "quiz_title": "Which way does it move",
        "quiz": [
            {"q": "The graph of `y = f(x − 4)` is the graph of `y = f(x)` moved which way?",
             "a": ["Right `4`", "Left `4`", "Up `4`", "Down `4`"],
             "c": 0,
             "why": "The point `(t, f(t))` reappears where `x − 4 = t`, that is at "
                    "`x = t + 4`, so every point moves four to the right. The minus "
                    "sign suggests left, which is why this is the most missed fact in "
                    "the lesson. Up and down are changes made outside the function, "
                    "and `−4` is inside it."},
            {"q": "What is the `y`-intercept of `y = −2(x − 3)² + 5`?",
             "a": ["`−13`", "`23`", "`41`", "`5`"],
             "c": 0,
             "why": "At `x = 0`, `(0 − 3)² = 9`, so `−2(9) + 5 = −13`. `23` comes "
                    "from squaring term by term, `0² − 3² = −9`, then `−2(−9) + 5`. "
                    "`41` comes from multiplying the `−2` in before squaring, giving "
                    "`(6)² + 5`. `5` is the output at the vertex, `x = 3`, not at "
                    "`x = 0`."},
            {"q": "Starting from `y = √x`, which description reaches `y = √(2x + 6)`?",
             "a": ["Squash horizontally by a factor of `1/2`, then shift left `3`",
                   "Shift left `3`, then squash horizontally by a factor of `1/2`",
                   "Squash horizontally by a factor of `1/2`, then shift left `6`",
                   "Stretch horizontally by a factor of `2`, then shift left `3`"],
             "c": 0,
             "why": "`√(2x + 6) = √(2(x + 3))`, so once the `2` is factored out the "
                    "shift is `3`. Shifting first gives `√(x + 3)` and then "
                    "`√(2x + 3)`. Squashing first and shifting `6` gives "
                    "`√(2(x + 6)) = √(2x + 12)`. Stretching instead of squashing "
                    "gives `√((x + 3)/2)`. Shifting left `6` <em>first</em> and "
                    "squashing second also lands on `√(2x + 6)`, which is why the "
                    "order and the number have to be quoted together."},
        ],
        "mistakes": [
            ("Reading a subtraction inside as a shift left",
             "`f(x − 3)` moves right. The rule cannot be fixed by memorising it "
             "harder; solve `x − 3 = t` for `x` and the `+3` appears. Any time the "
             "direction is in doubt, that one line settles it."),
            ("Reading the number beside x as the shift",
             "In `f(2x + 6)` the shift is `3`, not `6`, because the input must be "
             "written as `2(x + 3)` first. For a root there is a free check: the "
             "domain of `√(2x + 6)` starts at `−3`, and a shift of `6` would have "
             "started it at `−6`."),
            ("Calling f(2x) a stretch by 2",
             "It is a squash by `1/2`. The graph reaches at `x = 1` what the parent "
             "reached at `x = 2`, so horizontal distances are halved. The factor "
             "that describes the picture is `1/b`, never `b`."),
        ],
        "standard": ("Finish when you can go from formula to described graph and "
                     "back, including the case where the input has a coefficient.",
                     "Given `y = a f(b(x − h)) + k` you should name the parent, list "
                     "the four moves with directions and factors, and locate the "
                     "image of one landmark point such as a vertex, a corner or an "
                     "endpoint. Given a described graph you should produce the "
                     "formula. The test of real understanding is `√(2x + 6)`: shift "
                     "`3` after factoring, confirmed by a domain starting at `−3`."),
        "note": "Every transformation here is a composition in disguise: `f(x − 3)` "
                "is `f` applied to the output of the rule that sends `x` to `x − 3`. "
                "Lesson 12 makes that "
                "explicit and general, which is why the horizontal moves will stop "
                "feeling like an exception once composition is in place.",
    },

    # ---------------------------------------------------------------- 12
    {
        "slug": "composition-of-functions",
        "title": "Composition of Functions",
        "module": "Functions",
        "one_line": "Feeding one function into another, in a fixed order.",
        "summary": (
            "Composition runs one function on the output of another: `(f ∘ g)(x)` "
            "means `f(g(x))`, with `g` first. The order is not a convention that can "
            "be swapped, and the composite's domain can be smaller than either "
            "function's."
        ),
        "key": [
            "(f o g)(x) = f(g(x))          g runs FIRST",
            "(f o g) and (g o f) are different functions",
            "domain: x must suit g, AND g(x) must suit f",
            "the circle is not multiplication",
        ],
        "key_label": "The definition and its three consequences",
        "concepts_intro": (
            "Lesson 11's horizontal shifts were compositions written informally. "
            "Here the operation gets its own symbol and its own rules."
        ),
        "concepts": [
            ("The inner function runs first",
             "In `(f ∘ g)(x)` the function nearest the input is `g`, and it goes "
             "first. The notation reads right to left, which is the reverse of "
             "English reading order, and that mismatch is the whole difficulty. "
             "`f(g(x))` is the same statement with the order visible."),
            ("Order changes the answer",
             "With `f(x) = 2x + 3` and `g(x) = x² − 1`, `(f ∘ g)(x) = 2x² + 1` and "
             "`(g ∘ f)(x) = 4x² + 12x + 8`. At `x = 2` they give `9` and `48`. "
             "Composition is not commutative, and the two composites usually do not "
             "even have the same shape."),
            ("The domain is decided in two stages",
             "An input must first be acceptable to `g`, and then `g(x)` must be "
             "acceptable to `f`. Both tests happen on the original expression, "
             "before any simplification, because simplifying can erase the evidence "
             "of the first stage."),
        ],
        "read_title": "Building a composite and finding where it is defined",
        "read_intro": "The definition, why order matters, how the domain is assembled, and how to take a composite apart.",
        "body": [
            ("def", ("Composition",
                     "Given functions `f` and `g`, the <strong>composite</strong> "
                     "`f ∘ g` is defined by `(f ∘ g)(x) = f(g(x))`. Its domain is "
                     "the set of inputs `x` in the domain of `g` for which `g(x)` "
                     "lies in the domain of `f`. The symbol is read \"f circle g\" "
                     "or \"f after g\".",
                     "\"After\" is the reading worth adopting, because it says the "
                     "order out loud. `f ∘ g` is `f` after `g`: `g` happens, then `f` "
                     "happens to the result. The alternative reading, \"f of g\", "
                     "is also correct but is easier to say without thinking about "
                     "which one moves first.")),
            ("h3", "Computing a composite"),
            ("p", "Substitution again, exactly as in lesson 8, with a whole function "
                  "in the slot. Take `f(x) = 2x + 3` and `g(x) = x² − 1`."),
            ("math", [
                "(f o g)(x) = f(g(x)) = f(x^2 - 1)",
                "           = 2(x^2 - 1) + 3",
                "           = 2x^2 - 2 + 3   =   2x^2 + 1",
                "",
                "(g o f)(x) = g(f(x)) = g(2x + 3)",
                "           = (2x + 3)^2 - 1",
                "           = 4x^2 + 12x + 9 - 1   =   4x^2 + 12x + 8",
                "",
                "at x = 2     g(2) = 3,  f(3) = 9        (f o g)(2) = 9",
                "             f(2) = 7,  g(7) = 48       (g o f)(2) = 48",
            ]),
            ("p", "Both composites are quadratics and neither is the other. The "
                  "check at `x = 2` is worth doing every time a composite is built: "
                  "evaluate step by step through the two functions, then evaluate the "
                  "combined formula, and confirm they agree. Nine against nine "
                  "catches an expansion error immediately."),
            ("thm", ("Composition is associative but not commutative",
                     "`(f ∘ g) ∘ h` and `f ∘ (g ∘ h)` are the same function: both "
                     "send `x` to `f(g(h(x)))`, so brackets around a chain of "
                     "compositions never matter. `f ∘ g` and `g ∘ f`, by contrast, "
                     "are usually different, and when they do agree it is a fact "
                     "about those particular functions &mdash; as in lesson 13, where "
                     "agreeing on both sides is the definition of an inverse.")),
            ("h3", "The domain of a composite"),
            ("p", "Two conditions, applied in order. The input must be legal for the "
                  "inner function, and the inner function's output must be legal for "
                  "the outer one."),
            ("math", [
                "f(x) = sqrt(x)        g(x) = x - 5",
                "",
                "(f o g)(x) = sqrt(x - 5)      need x - 5 >= 0     domain [5, inf)",
                "(g o f)(x) = sqrt(x) - 5      need x >= 0         domain [0, inf)",
                "",
                "at x = 9:   sqrt(9 - 5) = 2          sqrt(9) - 5 = -2",
            ]),
            ("p", "Same two functions, two different domains, two different outputs. "
                  "In the first, the subtraction happens before the root, so the root "
                  "restricts which inputs survive. In the second the root goes first "
                  "and the subtraction cannot cause a failure, so only the root's own "
                  "condition applies."),
            ("h3", "The trap: simplifying before finding the domain"),
            ("p", "Take `f(x) = 1/(x − 1)` and `g(x) = 1/x`. The composite simplifies "
                  "to something whose formula has forgotten where it came from."),
            ("math", [
                "(f o g)(x) = f(1/x) = 1/((1/x) - 1)",
                "                    = 1/((1 - x)/x)",
                "                    = x/(1 - x)",
                "",
                "check x = 2:   1/((1/2) - 1) = 1/(-1/2) = -2        2/(1 - 2) = -2",
                "",
                "domain     x =/= 0    g needs it",
                "           x =/= 1    g(x) = 1 there, and f rejects 1",
                "",
                "but x/(1 - x) at x = 0 returns 0, an input the composite never had",
            ]),
            ("p", "The simplified formula accepts `0` and the composite does not. "
                  "This is the same phenomenon as the cancelled factor in lesson 9, "
                  "and the same rule applies: the domain belongs to the expression as "
                  "originally built, not to whatever it tidies into. Find the domain "
                  "before simplifying, or find it from the two-stage test, but never "
                  "from the final line."),
            ("h3", "Taking a composite apart"),
            ("example", ("Three decompositions",
                         "The reverse skill matters in calculus, where the chain rule "
                         "needs the decomposition rather than the composite. Given "
                         "`h(x) = √(3x + 1)`, ask what happens last: a square root. "
                         "That is the outer function, and what it acts on, `3x + 1`, "
                         "is the inner one.",
                         "`h(x) = √(3x + 1)` is `f(g(x))` with `g(x) = 3x + 1` and "
                         "`f(x) = √x`. `h(x) = (x² + 1)³` is `f(g(x))` with "
                         "`g(x) = x² + 1` and `f(x) = x³`. `h(x) = 1/(x + 4)²` is "
                         "`f(g(x))` with `g(x) = x + 4` and `f(x) = 1/x²`. "
                         "Decompositions are not unique &mdash; the last one is also "
                         "`f(x) = 1/x` after `g(x) = (x + 4)²` &mdash; so any pair "
                         "that recomposes correctly is a right answer.")),
        ],
        "lab": ("funcops", {
            "mode": "compose",
            "panel_title": "Both orders, side by side",
            "panel_intro": "Enter `f` and `g`; the lab builds `f ∘ g` and `g ∘ f` "
                           "together and traces a chosen input through each chain one "
                           "step at a time. The domain readout shows which of the two "
                           "stages rejected an input.",
        }),
        "steps_title": "Building a composite safely",
        "steps_intro": "Four steps. The domain step comes before the simplifying step, and that ordering is the point.",
        "steps": [
            ("Write the composite with the inner function in brackets",
             "`f(g(x))` first, on its own line, before any substitution. For "
             "`(f ∘ g)` with `g(x) = x² − 1`, that is `f(x² − 1)`. Seeing the inner "
             "expression sitting in the slot prevents the order from flipping."),
            ("Substitute into every occurrence of the variable",
             "Same discipline as lesson 8: brackets around the whole inner "
             "expression, in every slot. `(2x + 3)² − 1`, not `2x + 3² − 1`."),
            ("Find the domain from the unsimplified form",
             "Ask which inputs `g` rejects, then which of `g`'s outputs `f` rejects. "
             "For `f(x) = 1/(x − 1)` after `g(x) = 1/x`, that is `x ≠ 0` from the "
             "first test and `x ≠ 1` from the second."),
            ("Simplify, then check one input end to end",
             "Now expand and collect. Then pick an input, run it through `g` and `f` "
             "separately, and compare with the simplified formula. Disagreement "
             "means the expansion is wrong; agreement at one point is not a proof, "
             "but it catches nearly every algebra slip."),
        ],
        "worked": {
            "title": "Two composites, both orders, and a domain that hides",
            "intro": ["The first pair shows that order matters. The second shows that "
                      "the simplified formula cannot be trusted for a domain."],
            "lines": [
                "f(x) = 2x + 3        g(x) = x^2 - 1",
                "",
                "(f o g)(x) = f(x^2 - 1) = 2(x^2 - 1) + 3 = 2x^2 + 1",
                "(g o f)(x) = g(2x + 3) = (2x + 3)^2 - 1 = 4x^2 + 12x + 8",
                "",
                "         x        (f o g)(x)       (g o f)(x)",
                "         0             1                8",
                "         2             9               48",
                "        -1             3                0",
                "",
                "step by step at x = 2:   g(2) = 3   then f(3) = 9        agrees",
                "                         f(2) = 7   then g(7) = 48       agrees",
                "",
                "both are defined for every real number: no roots, no denominators",
                "",
                "-----------------------------------------------------------------",
                "",
                "f(x) = 1/(x - 1)     g(x) = 1/x",
                "",
                "(f o g)(x) = 1/((1/x) - 1) = 1/((1 - x)/x) = x/(1 - x)",
                "",
                "domain, stage 1:   g needs x =/= 0",
                "domain, stage 2:   f rejects input 1, and g(x) = 1 when x = 1",
                "domain:            every x except 0 and 1",
                "",
                "check x = 2:  g(2) = 1/2,  f(1/2) = 1/(-1/2) = -2",
                "              x/(1 - x) = 2/(-1) = -2                    agrees",
            ],
            "after": [
                "The table is the honest way to show that order matters: at three "
                "inputs the two composites give six different-looking numbers, and "
                "they agree nowhere in the table. Setting `2x² + 1 = 4x² + 12x + 8` "
                "gives `2x² + 12x + 7 = 0`, whose discriminant is "
                "`144 − 56 = 88`, so the two curves do cross at two irrational "
                "inputs. Different functions can still share points. The `0` in the "
                "last row is not one of them: `4x² + 12x + 8` factors as "
                "`4(x + 1)(x + 2)`, so `x = −1` is a root of `g ∘ f` alone.",
                "In the second example the simplified formula `x/(1 − x)` is "
                "perfectly happy at `x = 0`, returning `0`. The composite is not "
                "defined there at all, because `g(0)` does not exist and `f` is never "
                "reached. This is why stage 1 of the domain test is not optional.",
                "Both checks were done by running an input through the two functions "
                "in sequence. That is slower than trusting the algebra and it is the "
                "only verification that tests the order as well as the expansion.",
            ],
        },
        "quiz_title": "Order, value and domain",
        "quiz": [
            {"q": "With `f(x) = 2x + 3` and `g(x) = x² − 1`, what is `(f ∘ g)(2)`?",
             "a": ["`9`", "`48`", "`21`", "`10`"],
             "c": 0,
             "why": "`g` runs first: `g(2) = 3`, then `f(3) = 9`. `48` is "
                    "`(g ∘ f)(2)`, the same two functions in the wrong order. `21` is "
                    "`f(2)·g(2) = 7·3`, reading the circle as multiplication. `10` is "
                    "`f(2) + g(2) = 7 + 3`, reading it as addition."},
            {"q": "With `f(x) = √x` and `g(x) = x − 5`, what is the domain of `f ∘ g`?",
             "a": ["`[5, ∞)`", "`[0, ∞)`", "`(−∞, 5]`", "`[−5, ∞)`"],
             "c": 0,
             "why": "`(f ∘ g)(x) = √(x − 5)`, which needs `x − 5 ≥ 0`, so `x ≥ 5`. "
                    "`[0, ∞)` is the domain of the other order, `√x − 5`. "
                    "`(−∞, 5]` solves the inequality with the direction reversed. "
                    "`[−5, ∞)` composes the wrong way inside the root, as though the "
                    "composite were `√(x + 5)`."},
            {"q": "With `f(x) = 1/(x − 1)` and `g(x) = 1/x`, the composite `f ∘ g` "
                  "simplifies to `x/(1 − x)`. What is its domain?",
             "a": ["Every `x` with `x ≠ 1`",
                   "Every `x` with `x ≠ 0` and `x ≠ 1`",
                   "Every `x` with `x ≠ 0`",
                   "Every real number"],
             "c": 1,
             "why": "Two stages exclude two inputs. `g` is undefined at `0`, so the "
                    "chain never starts there; and `g(1) = 1`, which `f` rejects. The "
                    "first choice reads the domain off the simplified formula, which "
                    "has lost the `x ≠ 0` and would happily return `0` at `x = 0`. "
                    "The third keeps only the inner condition. The fourth ignores "
                    "both."},
        ],
        "mistakes": [
            ("Composing in the written order",
             "`(f ∘ g)` applies `g` first, even though `f` is written first. The "
             "notation reads right to left. Saying \"f after g\" out loud before "
             "computing puts the order back the right way."),
            ("Treating the circle as multiplication",
             "`(f ∘ g)(2)` is `9` for the functions above, while `f(2)·g(2)` is `21`. "
             "The circle is a small raised ring and the multiplication dot is a small "
             "raised dot, which does not help; the difference is in what the symbol "
             "does, not how it looks."),
            ("Reading the composite's domain off the simplified formula",
             "Simplifying can cancel exactly the factor that recorded a restriction. "
             "`x/(1 − x)` accepts `0`; the composite it came from does not, because "
             "`g(0)` is undefined. Test the two stages on the original expressions."),
        ],
        "standard": ("Finish when you can build either composite, state its domain "
                     "from the two-stage test rather than from the simplified "
                     "formula, and decompose a given function into an inner and an "
                     "outer part.",
                     "Given two functions you should produce `f ∘ g` and `g ∘ f`, "
                     "show they differ by evaluating both at a specific input, and "
                     "give each domain with the excluded values justified by which "
                     "stage rejected them. Decomposing `√(3x + 1)` into `√x` after "
                     "`3x + 1` should be immediate; it is the skill the chain rule "
                     "will assume."),
        "note": "Composition is the machinery lesson 13 needs. An inverse is defined "
                "by what it does under composition &mdash; `f⁻¹ ∘ f` and `f ∘ f⁻¹` "
                "both have to be the function that leaves its input alone &mdash; so "
                "the order sensitivity established here is what makes that definition "
                "say something.",
    },

    # ---------------------------------------------------------------- 13
    {
        "slug": "inverse-functions",
        "title": "Inverse Functions",
        "module": "Functions",
        "one_line": "Undoing a function, and the restriction that is usually needed.",
        "summary": (
            "An inverse sends every output back to the input it came from. It exists "
            "only when no two inputs share an output, so most functions have to be "
            "cut down to a piece before they have one. The superscript `−1` is a "
            "label, not an exponent."
        ),
        "key": [
            "f⁻¹ undoes f:     f⁻¹(f(x)) = x     and     f(f⁻¹(x)) = x",
            "exists  ⟺  f is one-to-one   (horizontal line test)",
            "method:  swap x and y, then solve for y",
            "domain of f⁻¹ = range of f        f⁻¹(x) is NOT 1/f(x)",
        ],
        "key_label": "What an inverse is, when it exists, how to find it",
        "concepts_intro": (
            "Composition gave the language for undoing. This lesson asks which "
            "functions can be undone, and what to do about the ones that cannot."
        ),
        "concepts": [
            ("An inverse is defined by composition",
             "`f⁻¹` is the function for which `f⁻¹(f(x)) = x` for every `x` in the "
             "domain of `f`, and `f(f⁻¹(x)) = x` for every `x` in the domain of "
             "`f⁻¹`. Both directions are part of the definition, and checking both is "
             "how a candidate inverse is verified."),
            ("It exists exactly when f is one-to-one",
             "If two inputs share an output, the inverse would have to send that one "
             "output back to two places, and lesson 7 ruled that out. `f(x) = x²` "
             "sends `2` and `−2` both to `4`, so on all real numbers it has no "
             "inverse. On a graph, the horizontal line test decides it."),
            ("Restricting the domain is the usual repair",
             "Cutting the domain down until no output repeats gives a function that "
             "does have an inverse. `x²` on `x ≥ 0` inverts to `√x`; the same formula "
             "on `x ≤ 0` inverts to `−√x`. The restriction is a choice, and different "
             "choices give different inverses."),
        ],
        "read_title": "One-to-one, the swap method, and the restriction",
        "read_intro": "What the notation promises, the test that decides existence, the procedure, and the part that is usually left out.",
        "body": [
            ("def", ("One-to-one, and the inverse",
                     "A function is <strong>one-to-one</strong> if different inputs "
                     "always give different outputs: `f(a) = f(b)` forces `a = b`. "
                     "For a one-to-one `f`, the <strong>inverse</strong> `f⁻¹` is the "
                     "function with domain equal to the range of `f` that sends each "
                     "output back to the unique input it came from.",
                     "The notation is unfortunate and permanent. In `f⁻¹` the `−1` is "
                     "not an exponent, so `f⁻¹(x)` is not `1/f(x)` and the two are "
                     "almost never equal. For `f(x) = 3x − 7` the inverse is "
                     "`(x + 7)/3` and the reciprocal is `1/(3x − 7)`; at `x = −1` "
                     "they give `2` and `−1/10`. Nothing about the symbol warns you, "
                     "so this is a fact to hold separately.")),
            ("h3", "The horizontal line test"),
            ("thm", ("Horizontal line test",
                     "A function has an inverse if and only if no horizontal line "
                     "meets its graph more than once. A horizontal line is the set of "
                     "points sharing one output, so two intersections are two inputs "
                     "with the same output &mdash; exactly what one-to-one forbids.")),
            ("p", "The pairing with lesson 7 is exact. The vertical line test asks "
                  "whether a graph is a function at all; the horizontal line test "
                  "asks whether that function can be run backwards. A graph that "
                  "passes both is a function with an inverse, and the second test "
                  "says nothing about the first."),
            ("h3", "The swap method"),
            ("p", "Write `y = f(x)`, exchange `x` and `y`, and solve the result for "
                  "`y`. The swap is doing something specific: the graph of `f⁻¹` is "
                  "the graph of `f` reflected in the line `y = x`, and exchanging the "
                  "letters is that reflection performed on the equation."),
            ("math", [
                "f(x) = 3x - 7",
                "",
                "  y = 3x - 7          write y for the output",
                "  x = 3y - 7          swap x and y",
                "  x + 7 = 3y          solve for y",
                "  y = (x + 7)/3",
                "",
                "f⁻¹(x) = (x + 7)/3",
                "",
                "check   f(2) = -1        f⁻¹(-1) = 6/3 = 2        back to 2",
                "        f⁻¹(5) = 4       f(4) = 5                 back to 5",
            ]),
            ("p", "Both checks are needed in principle, and for a formula like this "
                  "one they will not disagree. They start to matter as soon as a "
                  "restriction is involved, because a candidate can undo `f` on part "
                  "of the domain and fail elsewhere."),
            ("h3", "A rational example"),
            ("p", "The same three lines work when `y` appears in a denominator; the "
                  "only extra step is collecting the `y` terms on one side and "
                  "factoring."),
            ("math", [
                "f(x) = (2x + 1)/(x - 3)          domain x =/= 3",
                "",
                "  x = (2y + 1)/(y - 3)           swap",
                "  x(y - 3) = 2y + 1              clear the denominator",
                "  xy - 3x = 2y + 1",
                "  xy - 2y = 3x + 1               all y terms on the left",
                "  y(x - 2) = 3x + 1              factor",
                "  y = (3x + 1)/(x - 2)",
                "",
                "f⁻¹(x) = (3x + 1)/(x - 2)        domain x =/= 2",
                "",
                "check   f(4) = 9/1 = 9          f⁻¹(9) = 28/7 = 4",
                "        f(5) = 11/2             f⁻¹(11/2) = (35/2)/(7/2) = 5",
            ]),
            ("p", "The excluded value moved from `3` to `2`, and that is not a "
                  "coincidence. The range of `f` is every value except `2`: setting "
                  "`(2x + 1)/(x − 3) = 2` gives `2x + 1 = 2x − 6`, that is `1 = −6`, "
                  "which no input satisfies. Since the domain of `f⁻¹` is the range "
                  "of `f`, the `2` had to appear. When the two sets fail to match, "
                  "one of them has been computed wrongly."),
            ("h3", "When the inverse does not exist"),
            ("p", "`f(x) = x²` on all real numbers fails the horizontal line test at "
                  "every positive height. The output `4` came from `2` and from `−2`, "
                  "and an inverse would have to choose. Writing `√x` and calling it "
                  "the inverse of `x²` quietly makes that choice without saying so."),
            ("example", ("Restricting a parabola",
                         "`f(x) = (x − 2)² + 1` on `x ≥ 2` is one-to-one, since the "
                         "restriction keeps only the right half of the parabola. "
                         "Swapping gives `x = (y − 2)² + 1`, so `(y − 2)² = x − 1` and "
                         "`y − 2 = ±√(x − 1)`. The restriction `y ≥ 2` selects the "
                         "positive root, so `f⁻¹(x) = 2 + √(x − 1)`, with domain "
                         "`x ≥ 1`. Check: `f(5) = 10` and `2 + √9 = 5`. On the other "
                         "half, `x ≤ 2`, the same working selects the negative root "
                         "and gives `f⁻¹(x) = 2 − √(x − 1)`; there `f(−1) = 10` and "
                         "`2 − √9 = −1`.",
                         "The `±` is where the restriction does its work. Without a "
                         "stated domain there is no way to choose a sign, and the two "
                         "choices are genuinely different functions undoing genuinely "
                         "different halves of the parabola. Both are correct "
                         "inverses; neither is the inverse of the unrestricted `f`, "
                         "which has none.")),
            ("ul", [
                "<strong>Every line except a horizontal one is one-to-one.</strong> "
                "`y = mx + b` with `m ≠ 0` passes the test, and its inverse is "
                "another line with slope `1/m`.",
                "<strong>A horizontal line is not.</strong> `f(x) = 4` sends every "
                "input to `4`, so nothing can be recovered.",
                "<strong>Even powers and absolute value are not,</strong> without a "
                "restriction. `x²` and `|x|` both pair `a` with `−a`, and every "
                "even power does the same.",
                "<strong>Odd powers are.</strong> `x³` is one-to-one on all real "
                "numbers, and its inverse is the cube root, with no restriction "
                "needed anywhere.",
            ]),
        ],
        "lab": ("funcops", {
            "mode": "inverse",
            "panel_title": "Reflect in the line y = x",
            "panel_intro": "Enter a function; the lab draws it, draws the reflection "
                           "in `y = x`, and reports whether that reflection is itself "
                           "a function. Drag the domain markers to restrict `f` and "
                           "watch the reflection become one.",
        }),
        "steps_title": "Finding an inverse",
        "steps_intro": "Test first, then swap. Finding a formula for something that does not exist is the failure this order prevents.",
        "steps": [
            ("Check that f is one-to-one",
             "Use the horizontal line test on the graph, or argue from the formula: "
             "a line with non-zero slope and an odd power pass, an even power and an "
             "absolute value fail. If it fails, restrict the domain and record the "
             "restriction you chose."),
            ("Write y = f(x) and swap the letters",
             "Every `x` becomes `y` and every `y` becomes `x`, all at once. This is "
             "the reflection in `y = x` carried out on the equation, and it is the "
             "only step where the two letters change roles."),
            ("Solve for y",
             "Standard rearranging. When `y` appears more than once, as in a "
             "rational function, collect the `y` terms on one side and factor. When a "
             "square appears, the `±` arrives here, and the restriction from step 1 "
             "decides the sign."),
            ("State the domain, and verify both compositions",
             "The domain of `f⁻¹` is the range of `f`, which is a check as much as a "
             "statement: if the two do not match, something earlier is wrong. Then "
             "confirm `f⁻¹(f(a)) = a` and `f(f⁻¹(b)) = b` at one value each."),
        ],
        "worked": {
            "title": "Three inverses, one of them needing a restriction",
            "intro": ["A line, a rational function, and a parabola that has to be cut "
                      "in half first."],
            "lines": [
                "1.  f(x) = 3x - 7",
                "",
                "        y = 3x - 7   ->   x = 3y - 7   ->   y = (x + 7)/3",
                "        f⁻¹(x) = (x + 7)/3",
                "        domain and range of both: every real number",
                "        check   f(2) = -1    f⁻¹(-1) = 6/3 = 2",
                "",
                "        NOT the inverse:  1/(3x - 7)   at x = -1 gives -1/10",
                "        NOT the inverse:  (x - 7)/3    at x = -1 gives -8/3",
                "",
                "2.  f(x) = (2x + 1)/(x - 3)          domain x =/= 3",
                "",
                "        x = (2y + 1)/(y - 3)             swap x and y",
                "        x(y - 3) = 2y + 1",
                "        xy - 3x  = 2y + 1",
                "        xy - 2y  = 3x + 1",
                "        y(x - 2) = 3x + 1",
                "        f⁻¹(x) = (3x + 1)/(x - 2)    domain x =/= 2",
                "",
                "        range of f is every value except 2:",
                "            (2x + 1)/(x - 3) = 2  ->  2x + 1 = 2x - 6  ->  1 = -6",
                "        so domain of f⁻¹ = range of f, as required",
                "",
                "        check   f(4) = 9       f⁻¹(9) = 28/7 = 4",
                "",
                "3.  f(x) = (x - 2)^2 + 1        on x >= 2",
                "",
                "        x = (y - 2)^2 + 1",
                "        (y - 2)^2 = x - 1",
                "        y - 2 = +- sqrt(x - 1)         restriction y >= 2 picks +",
                "        f⁻¹(x) = 2 + sqrt(x - 1)       domain x >= 1",
                "",
                "        check   f(5) = 9 + 1 = 10     f⁻¹(10) = 2 + 3 = 5",
                "                f(2) = 1              f⁻¹(1) = 2 + 0 = 2",
                "",
                "        on x <= 2 instead:  f⁻¹(x) = 2 - sqrt(x - 1)",
                "                f(-1) = 9 + 1 = 10      2 - sqrt(9) = -1",
            ],
            "after": [
                "The two rejected candidates in the first example fail in two "
                "different ways. `1/(3x − 7)` reads the `−1` as an "
                "exponent. `(x − 7)/3` does take the `7` first, which is the right "
                "order, but keeps the sign it arrived with: the `7` was subtracted "
                "last, so it must be <em>added</em> back first. At `x = −1` that "
                "candidate gives `−8/3` where the inverse gives `2`.",
                "In the second example the range of `f` was computed independently "
                "and then matched against the domain of `f⁻¹`. That is the cheapest "
                "available check on the whole calculation, and it uses the third tool "
                "from lesson 9 with the roles of the letters swapped.",
                "The third example produces two different inverses from one formula. "
                "Both check out, and which one is correct depends entirely on the "
                "restriction that was stated. An answer of `f⁻¹(x) = 2 + √(x − 1)` "
                "without a domain attached to `f` is incomplete, not merely untidy.",
            ],
        },
        "quiz_title": "Undoing, and when it is possible",
        "quiz": [
            {"q": "Why does `f(x) = x²` on all real numbers have no inverse?",
             "a": ["Because `x²` is never negative",
                   "Because `4` comes from both `2` and `−2`, so an inverse would "
                   "have to send `4` to two places",
                   "Because `f(0) = 0`",
                   "Because `x²` is not a linear function"],
             "c": 1,
             "why": "One-to-one fails: two inputs share an output, so running the "
                    "assignment backwards produces two outputs for the input `4`, "
                    "which lesson 7 forbids. The first choice describes the range and "
                    "is true but irrelevant &mdash; `x³` has range every real number "
                    "and `√x` has range `[0, ∞)`, and both are invertible. The third "
                    "is a single value. The fourth is false as a criterion: `x³` is "
                    "not linear and does have an inverse."},
            {"q": "For `f(x) = (2x + 1)/(x − 3)`, what is `f⁻¹(x)`?",
             "a": ["`(3x + 1)/(x − 2)`",
                   "`(x − 3)/(2x + 1)`",
                   "`(3x − 1)/(x + 2)`",
                   "`(x + 3)/(2x − 1)`"],
             "c": 0,
             "why": "Swapping and solving gives `y(x − 2) = 3x + 1`. Test it: "
                    "`f(4) = 9` and `(3·9 + 1)/(9 − 2) = 28/7 = 4`. The second choice "
                    "is `1/f(x)`, the reciprocal rather than the inverse; at `x = 9` "
                    "it gives `6/19`. The third and fourth flip individual signs "
                    "during the rearrangement and give `26/11` and `12/17` at `x = 9` "
                    "instead of `4`."},
            {"q": "`f(x) = (x − 2)² + 1` is restricted to `x ≥ 2`. What is `f⁻¹`?",
             "a": ["`f⁻¹(x) = 2 + √(x − 1)`",
                   "`f⁻¹(x) = 2 − √(x − 1)`",
                   "`f⁻¹(x) = √(x − 1) − 2`",
                   "`f⁻¹(x) = √(x + 1) − 2`"],
             "c": 0,
             "why": "`(y − 2)² = x − 1` gives `y = 2 ± √(x − 1)`, and `y ≥ 2` selects "
                    "the plus sign. Check with `f(5) = 10`: `2 + √9 = 5`. The second "
                    "choice is the inverse of the other restriction, `x ≤ 2`, where "
                    "`f(−1) = 10` and `2 − √9 = −1`. The third subtracts the `2` "
                    "instead of adding it, giving `1` at `x = 10`. The fourth also "
                    "shifts the wrong constant inside the root."},
        ],
        "mistakes": [
            ("Reading the superscript as an exponent",
             "`f⁻¹(x)` is not `1/f(x)`. For `f(x) = 3x − 7` the inverse is "
             "`(x + 7)/3` and the reciprocal is `1/(3x − 7)`; at `x = −1` they give "
             "`2` and `−1/10`. The notation collides with negative exponents and "
             "there is no fixing it, only remembering it."),
            ("Undoing the operations in the order they were applied",
             "`3x − 7` multiplies first and subtracts second, so the inverse adds "
             "first and divides second: `(x + 7)/3`. Writing `x/3 + 7` inverts both "
             "operations but applies them in the order `f` applied them, and it "
             "fails the check at the first value tried: `f(2) = −1`, while "
             "`−1/3 + 7 = 20/3`, not `2`."),
            ("Dropping the restriction",
             "Calling `√x` the inverse of `x²` is only true once `x²` has been cut "
             "down to `x ≥ 0`. Without that sentence the claim is false, since the "
             "unrestricted `x²` has no inverse at all, and the omission hides the "
             "fact that `x ≤ 0` would have given `−√x` instead."),
        ],
        "standard": ("Finish when you test for one-to-one before hunting for a "
                     "formula, and can produce an inverse together with its domain "
                     "and the restriction it required.",
                     "Given a line, a rational function or a restricted quadratic you "
                     "should apply the swap method cleanly, including the collect-"
                     "and-factor step when `y` appears twice and the sign choice when "
                     "a square root appears. Quoting the domain of `f⁻¹` as the range "
                     "of `f` and verifying both compositions at one value each is "
                     "what turns a plausible formula into a checked one."),
        "note": "That completes the toolkit the course promised: notation, domain, "
                "shape, composition and inverse. Lesson 14 returns to lines for one "
                "last question, where the answer is not a curve but a region, and it "
                "is the bridge into the systems of course 8.",
    },

    # ---------------------------------------------------------------- 14
    {
        "slug": "linear-inequalities-in-two-variables",
        "title": "Linear Inequalities in Two Variables",
        "module": "Lines",
        "one_line": "A boundary line, and which side of it is the answer.",
        "summary": (
            "Replacing the equals sign in a linear equation with an inequality turns "
            "a line into a half-plane. The line itself is the boundary, solid or "
            "dashed according to the symbol, and a single test point decides which "
            "side gets shaded."
        ),
        "key": [
            "boundary: replace the inequality sign with =",
            "solid line for <= or >=      dashed line for < or >",
            "test any point off the line; true means shade that side",
            "dividing by a negative reverses the inequality",
        ],
        "key_label": "Three decisions and the rule that catches people",
        "concepts_intro": (
            "A linear equation in two unknowns had a line for its solution set. An "
            "inequality has half the plane, and finding which half is one "
            "substitution."
        ),
        "concepts": [
            ("The solution set is a region",
             "A solution is still an ordered pair that makes the statement true, "
             "exactly as in lesson 1. There are simply infinitely many of them "
             "filling an area rather than lying along a line, and shading is how an "
             "infinite set gets drawn."),
            ("The boundary is in or out, and the symbol says which",
             "`≤` and `≥` include the line, drawn solid. `&lt;` and `&gt;` exclude "
             "it, drawn dashed. The dashed line is not decoration: `(0, −4)` "
             "satisfies `4x − 2y ≥ 8` and fails `4x − 2y &gt; 8`, and the drawing has "
             "to record that difference."),
            ("Test a point rather than guessing a side",
             "Substitute one point that is not on the line. A true statement means "
             "that point's side is the solution set; a false one means the other "
             "side. `(0, 0)` is the easiest test point whenever the boundary misses "
             "the origin, and when the boundary passes through it, any other point "
             "will do."),
        ],
        "read_title": "Boundary, side, and the sign that flips",
        "read_intro": "How to draw the region, why the test point is more reliable than the symbol, and the one algebraic move that reverses an inequality.",
        "body": [
            ("def", ("Linear inequality in two variables",
                     "A <strong>linear inequality in two variables</strong> is a "
                     "statement of the form `Ax + By &lt; C`, with `≤`, `&gt;` or "
                     "`≥` equally allowed and `A` and `B` not both zero. Its "
                     "<strong>solution set</strong> is the set of ordered pairs "
                     "making it true, which is a <strong>half-plane</strong>, "
                     "including its edge or not.")),
            ("p", "The line `Ax + By = C` splits the plane into two open regions. "
                  "Every point in one region makes `Ax + By` larger than `C`, every "
                  "point in the other makes it smaller, and points on the line make "
                  "it equal. That is why one test point settles the whole region: the "
                  "expression cannot change which side of `C` it falls on without "
                  "crossing the line."),
            ("h3", "Drawing the region"),
            ("ol", [
                "<strong>Replace the inequality sign with an equals sign</strong> and "
                "graph that line, by intercepts or by slope-intercept form, whichever "
                "lesson 2's methods make easier here.",
                "<strong>Make it solid or dashed.</strong> Solid for `≤` and `≥`, "
                "since those points are solutions; dashed for `&lt;` and `&gt;`, "
                "since they are not.",
                "<strong>Test one point off the line,</strong> preferably `(0, 0)`. "
                "Substitute both coordinates into the original inequality.",
                "<strong>Shade the side that won.</strong> If the test point made the "
                "statement true, shade its side; if false, shade the other.",
            ]),
            ("p", "For `2x + 3y ≤ 12` the boundary meets the axes at `(6, 0)` and "
                  "`(0, 4)`, and it is solid. Testing `(0, 0)` gives `0 ≤ 12`, which "
                  "is true, so the shaded half-plane is the one containing the "
                  "origin: the side below and to the left of the line."),
            ("h3", "Why the symbol alone cannot tell you the side"),
            ("p", "It is tempting to read `&gt;` as \"above\" and `&lt;` as \"below\". "
                  "That works only when the inequality has already been solved for "
                  "`y` with a positive coefficient, and it fails as soon as the "
                  "coefficient of `y` is negative."),
            ("math", [
                "4x - 2y > 8",
                "",
                "     -2y > -4x + 8",
                "      y  <  2x - 4          divided by -2, so the sign FLIPPED",
                "",
                "test (0, 0):    4(0) - 2(0) = 0        0 > 8 is FALSE",
                "test (3, 1):    4(3) - 2(1) = 10      10 > 8 is TRUE",
                "test (0, -10):  4(0) - 2(-10) = 20    20 > 8 is TRUE",
                "",
                "the symbol says >, the shaded region is BELOW the line y = 2x - 4",
            ]),
            ("p", "The written symbol is `&gt;` and the region is below. Both facts "
                  "are correct, and they are consistent because solving for `y` "
                  "required dividing by `−2`, which reversed the inequality into "
                  "`y &lt; 2x − 4`. A test point reaches the same conclusion without "
                  "needing the rearrangement at all, which is why it is the more "
                  "reliable method."),
            ("thm", ("Multiplying or dividing by a negative reverses the sign",
                     "If `a &lt; b` and `c` is negative then `ac &gt; bc`. This is "
                     "the single rule from course 2, lesson 9 that survives into two "
                     "variables, and it is where a correct boundary line ends up with "
                     "the wrong side shaded. Adding or subtracting anything, and "
                     "multiplying by a positive, leave the direction alone.")),
            ("h3", "When the boundary passes through the origin"),
            ("p", "`y &lt; 3x` has the origin on its boundary, so `(0, 0)` cannot be "
                  "the test point: it satisfies the equation, not the inequality, and "
                  "it lies on the edge rather than in either region. Any other point "
                  "works. Testing `(1, 0)` gives `0 &lt; 3`, which is true, so the "
                  "shaded region is the one containing `(1, 0)`, below and to the "
                  "right of the line."),
            ("example", ("Four points against one inequality",
                         "For `4x − 2y &gt; 8`: `(0, 0)` gives `0`, false. `(3, 1)` "
                         "gives `10`, true. `(0, −4)` gives `8`, and `8 &gt; 8` is "
                         "false, so this point sits exactly on the dashed boundary "
                         "and is not a solution. `(1, 2)` gives `0`, false. Only "
                         "`(3, 1)` is in the solution set, and `(0, −4)` is the one "
                         "worth pausing on: it would be a solution if the symbol were "
                         "`≥`.")),
            ("h3", "Reading a region back into an inequality"),
            ("p", "The reverse direction appears in modelling and in course 8. Find "
                  "the boundary line's equation from two of its points, choose `≤` or "
                  "`&lt;` from whether the line is solid or dashed, and then fix the "
                  "direction by testing a point taken from inside the shaded region. "
                  "The last step is the same substitution as before, run with the "
                  "answer known and the symbol unknown."),
        ],
        "lab": ("system", {
            "mode": "inequalities",
            "panel_title": "Boundary, then side",
            "panel_intro": "Type an inequality; the lab draws the boundary solid or "
                           "dashed and shades the half-plane. Click anywhere to test "
                           "that point and see the substitution written out, "
                           "including points that land on the boundary itself.",
        }),
        "steps_title": "Graphing a linear inequality",
        "steps_intro": "Boundary, style, test, shade. Doing the test before choosing a side keeps the symbol from misleading you.",
        "steps": [
            ("Graph the boundary",
             "Swap the inequality for an equals sign and draw that line. Intercepts "
             "are usually quickest: for `4x − 2y = 8` they are `(2, 0)` and `(0, −4)`."),
            ("Choose solid or dashed",
             "Solid when the symbol includes equality, dashed when it does not. Make "
             "this decision from the original inequality, before any rearranging, so "
             "a flipped sign cannot change it. Rearranging never changes whether the "
             "boundary is included."),
            ("Substitute a test point",
             "Use `(0, 0)` unless the boundary passes through it, in which case pick "
             "any convenient point off the line. Substitute into the original "
             "inequality and evaluate to a true or false statement."),
            ("Shade the winning side, then confirm",
             "True means shade the test point's side; false means shade the other. "
             "Then test one point from inside the shaded region: it must satisfy the "
             "inequality. That second substitution is the check that catches a "
             "reversed sign."),
        ],
        "worked": {
            "title": "Two inequalities, graphed and checked",
            "intro": ["The first is straightforward. The second has a negative "
                      "coefficient on `y`, which is where the shading goes wrong."],
            "lines": [
                "1.  2x + 3y <= 12",
                "",
                "        boundary   2x + 3y = 12        SOLID  (<= includes it)",
                "        intercepts (6, 0)  and  (0, 4)",
                "        test (0, 0):  2(0) + 3(0) = 0      0 <= 12   TRUE",
                "        shade the side containing the origin",
                "",
                "        confirm    (1, 1):   2 + 3 = 5     5 <= 12   TRUE",
                "                   (6, 4):  12 + 12 = 24  24 <= 12  FALSE, other side",
                "",
                "2.  4x - 2y > 8",
                "",
                "        boundary   4x - 2y = 8         DASHED (> excludes it)",
                "        intercepts (2, 0)  and  (0, -4)",
                "        test (0, 0):  4(0) - 2(0) = 0      0 > 8     FALSE",
                "        shade the side NOT containing the origin",
                "",
                "        in slope-intercept form:",
                "            -2y > -4x + 8",
                "             y  <  2x - 4              divide by -2, flip the sign",
                "        so the region is BELOW the line, although the symbol is >",
                "",
                "        confirm    (0, -10):  0 + 20 = 20    20 > 8    TRUE",
                "                   (3, 1):   12 -  2 = 10    10 > 8    TRUE",
                "                   (0, -4):   0 +  8 =  8     8 > 8    FALSE, on the edge",
            ],
            "after": [
                "The second example is the whole lesson in one picture. The symbol is "
                "`&gt;`, the region is below, and there is no contradiction: solving "
                "for `y` divided by `−2` and flipped the sign to `&lt;`. Anyone "
                "shading above has applied a rule that is only valid after the "
                "rearrangement has been done.",
                "The point `(0, −4)` is on the boundary and gives `8 &gt; 8`, which "
                "is false. With `≥` in place of `&gt;` it would be a solution and the "
                "line would be solid. One symbol changes the status of every point on "
                "the line and no other point in the plane.",
                "Both confirmations tested a point from inside the shaded region "
                "rather than re-reading the picture. Shading is easy to draw on the "
                "wrong side of a correctly drawn line, and only a substitution "
                "catches it.",
            ],
        },
        "quiz_title": "Boundaries and sides",
        "quiz": [
            {"q": "Which point satisfies `4x − 2y &gt; 8`?",
             "a": ["`(0, 0)`", "`(3, 1)`", "`(0, −4)`", "`(1, 2)`"],
             "c": 1,
             "why": "`4(3) − 2(1) = 10`, and `10 &gt; 8` is true. `(0, 0)` gives `0`, "
                    "and `(1, 2)` gives `4 − 4 = 0`; both are on the far side. "
                    "`(0, −4)` gives exactly `8`, and `8 &gt; 8` is false: that point "
                    "lies on the boundary, which a strict inequality excludes. It "
                    "would be a solution if the symbol were `≥`."},
            {"q": "Solving `4x − 2y &gt; 8` for `y` gives which inequality?",
             "a": ["`y &gt; 2x − 4`", "`y &lt; 2x − 4`", "`y &gt; −2x + 4`", "`y &lt; −2x − 4`"],
             "c": 1,
             "why": "`−2y &gt; −4x + 8`, and dividing by `−2` reverses the direction, "
                    "giving `y &lt; 2x − 4`. The first choice divides by `−2` without "
                    "flipping, and it disagrees with the original at almost every "
                    "point: `(0, −10)` satisfies `4x − 2y &gt; 8` but not "
                    "`y &gt; 2x − 4`. The third and fourth also mishandle the signs "
                    "when moving `4x` across."},
            {"q": "A boundary line passes through the origin. Why can `(0, 0)` not be "
                  "used as the test point?",
             "a": ["Because the origin belongs to no quadrant",
                   "Because a point on the boundary makes the two sides equal, so it "
                   "cannot distinguish the regions",
                   "Because the origin satisfies every linear inequality",
                   "Because the inequality must be solved for `y` first"],
             "c": 1,
             "why": "The test works by asking which side of the line a point falls "
                    "on, and a point on the line falls on neither. Substituting it "
                    "gives a statement about equality that is the same whichever "
                    "region is intended. The first is true of the origin but "
                    "irrelevant. The third is false: `(0, 0)` fails `x + y &gt; 1`. "
                    "The fourth describes an optional rearrangement, not a "
                    "requirement."},
        ],
        "mistakes": [
            ("Forgetting to flip when dividing by a negative",
             "`4x − 2y &gt; 8` becomes `y &lt; 2x − 4`, not `y &gt; 2x − 4`. The "
             "boundary line is identical either way, so the graph looks right and the "
             "shading is on the wrong side. Testing `(0, −10)`, which satisfies the "
             "original, exposes it in one line."),
            ("Reading the side off the symbol",
             "`&gt;` does not mean above. It means above only after the inequality "
             "has been solved for `y` and the coefficient of `y` was positive. For "
             "`4x − 2y &gt; 8` the region is below the boundary. A test point never "
             "depends on the form the inequality happens to be written in."),
            ("Drawing a solid line for a strict inequality",
             "`&lt;` and `&gt;` exclude the boundary, so it is dashed. The "
             "difference is real: `(0, −4)` satisfies `4x − 2y ≥ 8` and fails "
             "`4x − 2y &gt; 8`, and a solid line claims every point of the boundary "
             "as a solution."),
        ],
        "standard": ("Finish when you can graph any linear inequality with the right "
                     "line style and the right side shaded, and can justify the side "
                     "by a substitution rather than by the symbol.",
                     "Given `4x − 2y &gt; 8` you should draw a dashed line through "
                     "`(2, 0)` and `(0, −4)`, shade below it, and explain that the "
                     "region is below although the symbol is `&gt;` because solving "
                     "for `y` divides by `−2`. You should also handle a boundary "
                     "through the origin by choosing a different test point, and read "
                     "an inequality back off a shaded picture."),
        "note": "That closes the course. Lines came first, then the definition of a "
                "function and everything a function has, and this last lesson puts "
                "the two together by asking a line to describe a region instead of a "
                "path. Course 8 stacks several of these regions on one set of axes; "
                "the overlap of the shaded half-planes is the feasible set that "
                "linear programming optimises over.",
    },
]
