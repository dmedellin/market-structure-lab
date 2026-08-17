"""Course 3, lessons 01-07 — the plane, the line, and the definition of a function."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "the-coordinate-plane",
        "title": "The Coordinate Plane",
        "module": "The coordinate plane",
        "one_line": "Ordered pairs, axes and quadrants: where a graph lives.",
        "summary": (
            "Two number lines at right angles turn a pair of numbers into a point, "
            "and an equation in `x` and `y` into a picture. The order inside the "
            "pair is not a formality &mdash; it is the whole content of the idea."
        ),
        "key": [
            "(x, y)          x across first, then y up",
            "(3, 5) ≠ (5, 3)          the pair is ORDERED",
            "QI (+,+)   QII (−,+)   QIII (−,−)   QIV (+,−)",
            "on an axis  →  in no quadrant at all",
        ],
        "key_label": "The plane in four lines",
        "concepts_intro": (
            "Course 2 solved equations in one unknown, and an answer there was a "
            "number on a line. An equation in two unknowns has pairs for answers, "
            "and pairs need two dimensions to be drawn."
        ),
        "concepts": [
            ("A point is an ordered pair",
             "`(3, 5)` and `(5, 3)` are different points. The first number always "
             "measures horizontal position and the second always vertical, and no "
             "context ever overrides that."),
            ("A graph is a solution set, drawn",
             "The graph of `2x + 3y = 12` is the set of every pair that makes the "
             "equation true. A point is on the graph exactly when substituting its "
             "coordinates gives a true statement &mdash; that is the only test."),
            ("The axes belong to no quadrant",
             "A quadrant is an open region. `(0, −3)` and `(−5, 0)` sit on an axis, "
             "so the answer to \"which quadrant?\" is none, not the nearest one."),
        ],
        "read_title": "Naming a point",
        "read_intro": "Two number lines, one convention about order, and four regions.",
        "body": [
            ("def", ("Coordinate plane",
                     "Two perpendicular number lines &mdash; the <strong>x-axis</strong> "
                     "horizontal, the <strong>y-axis</strong> vertical &mdash; crossing at "
                     "the <strong>origin</strong> `(0, 0)`. Every point of the plane is "
                     "named by exactly one pair of numbers, and every pair names exactly "
                     "one point.")),
            ("p", "That last sentence is doing real work. The naming is a perfect "
                  "matching in both directions, which is why a question about points can "
                  "be answered with algebra and a question about algebra can be answered "
                  "with a picture. The rest of this course lives on that exchange."),
            ("def", ("Coordinates",
                     "In the pair `(x, y)`, the <strong>x-coordinate</strong> is the "
                     "signed distance from the y-axis (right positive) and the "
                     "<strong>y-coordinate</strong> is the signed distance from the "
                     "x-axis (up positive).")),
            ("p", "The order is fixed by convention: across first, then up. `(3, 5)` is "
                  "three right and five up; `(5, 3)` is five right and three up. These "
                  "are two different points, and writing a pair backwards is the most "
                  "common way a correct calculation ends up drawn in the wrong place."),
            ("example", ("Six points",
                         "`(3, 5)` right 3, up 5. `(−4, 2)` left 4, up 2. `(−3, −1)` "
                         "left 3, down 1. `(2, −4)` right 2, down 4. `(0, −3)` on the "
                         "y-axis, 3 below the origin. `(−5, 0)` on the x-axis, 5 to the "
                         "left.")),
            ("h3", "Quadrants"),
            ("p", "The two axes cut the plane into four regions, numbered "
                  "anticlockwise starting from the upper right. Each is fixed by the "
                  "pair of signs, and nothing else needs to be remembered:"),
            ("ul", [
                "<strong>Quadrant I</strong> &mdash; `x &gt; 0`, `y &gt; 0`. Upper right.",
                "<strong>Quadrant II</strong> &mdash; `x &lt; 0`, `y &gt; 0`. Upper left.",
                "<strong>Quadrant III</strong> &mdash; `x &lt; 0`, `y &lt; 0`. Lower left.",
                "<strong>Quadrant IV</strong> &mdash; `x &gt; 0`, `y &lt; 0`. Lower right.",
            ]),
            ("p", "Every inequality there is strict, so a point with a zero coordinate "
                  "lies on an axis and in no quadrant. The origin lies on both axes. "
                  "This is not pedantry: in lesson 9 the same strictness decides whether "
                  "an endpoint belongs to a domain."),
            ("h3", "The graph of an equation"),
            ("def", ("Graph",
                     "The <strong>graph</strong> of an equation in `x` and `y` is the set "
                     "of all points `(x, y)` whose coordinates satisfy it. A point is on "
                     "the graph if and only if substituting makes the equation true.")),
            ("p", "So membership is decided by arithmetic, never by how the picture "
                  "looks. Take `2x + 3y = 12`. Substituting `(3, 2)` gives `6 + 6 = 12`, "
                  "true, so `(3, 2)` is on the graph. Substituting `(1, 4)` gives "
                  "`2 + 12 = 14`, false, so it is not &mdash; and no amount of it looking "
                  "close changes that."),
            ("example", ("Testing four pairs against 2x + 3y = 12",
                         "`(6, 0)`: `12 + 0 = 12` &mdash; on. `(0, 4)`: `0 + 12 = 12` "
                         "&mdash; on. `(−3, 6)`: `−6 + 18 = 12` &mdash; on. `(1, 4)`: "
                         "`2 + 12 = 14` &mdash; off.")),
            ("p", "One more practical point: the scale on the two axes need not match, "
                  "and a graph drawn with a stretched axis is still correct. What a "
                  "changed scale does distort is the <em>appearance</em> of steepness, "
                  "which is exactly why lesson 3 defines slope as a ratio of numbers "
                  "rather than as an angle you could measure with a protractor."),
        ],
        "lab": ("grapher", {
            "mode": "plane",
            "panel_title": "Place a point, read its pair",
            "panel_intro": "Drag the point and watch the two coordinates change sign as "
                           "it crosses an axis. The quadrant label is computed from the "
                           "signs, so it reports none the moment a coordinate is zero.",
        }),
        "steps_title": "Plotting a point",
        "steps_intro": "Four moves. The first one is where the errors are.",
        "steps": [
            ("Read the pair in order",
             "First number is horizontal, second is vertical. If the pair came out of "
             "a table or a substitution, confirm which column was which before moving."),
            ("Start at the origin",
             "Both coordinates are measured from `(0, 0)`, not from the last point you "
             "plotted."),
            ("Move along x, then parallel to y",
             "Right for positive, left for negative; then up for positive, down for "
             "negative. Doing it in the other order lands in the same place, but doing "
             "it in a mixed order does not."),
            ("Check the signs against the quadrant",
             "A point you expected in the lower left had better have two negative "
             "coordinates. This catches a swapped pair immediately."),
        ],
        "worked": {
            "title": "Six points, placed and classified",
            "intro": ["Plot each point, then name the region from the signs alone."],
            "lines": [
                "( 3,  5)     right 3, up 5        QI    (+, +)",
                "(-4,  2)     left 4,  up 2        QII   (-, +)",
                "(-3, -1)     left 3,  down 1      QIII  (-, -)",
                "( 2, -4)     right 2, down 4      QIV   (+, -)",
                "( 0, -3)     on the y-axis        no quadrant",
                "(-5,  0)     on the x-axis        no quadrant",
                "",
                "and the pair that is not the same point:",
                "( 3,  5)  ≠  ( 5,  3)             both in QI, different points",
            ],
            "after": [
                "The last line is worth the space it takes. Both points are in quadrant "
                "I and both are built from the digits 3 and 5, so a swap survives every "
                "check that looks only at signs. The only defence is reading the pair in "
                "order the first time."
            ],
        },
        "quiz_title": "Points and regions",
        "quiz": [
            {"q": "In which quadrant does `(−6, 2)` lie?",
             "a": ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"],
             "c": 1,
             "why": "`x` is negative and `y` is positive, which is the upper left. "
                    "Quadrant III would need both negative."},
            {"q": "Is `(−3, 6)` on the graph of `2x + 3y = 12`?",
             "a": ["Yes, because `−6 + 18 = 12`",
                   "No, because `x` is negative",
                   "No, because it is not in quadrant I",
                   "Only if the axes use the same scale"],
             "c": 0,
             "why": "Membership is decided by substitution and nothing else. The sign of "
                    "a coordinate and the scale of the drawing are both irrelevant."},
            {"q": "Which quadrant contains `(0, −3)`?",
             "a": ["Quadrant III", "Quadrant IV", "None &mdash; it is on an axis",
                   "Both III and IV"],
             "c": 2,
             "why": "The quadrant conditions are strict inequalities. A zero coordinate "
                    "puts the point on an axis, which is in no quadrant."},
        ],
        "mistakes": [
            ("Reading the pair as (up, across)",
             "`(2, 7)` is 2 across and 7 up. The swap produces a point that is often "
             "still plausible-looking, which is what makes it dangerous."),
            ("Putting an axis point in a quadrant",
             "\"Closest quadrant\" is not a thing. If either coordinate is zero the "
             "point is on an axis, and the honest answer is that it is in none."),
            ("Deciding membership by eye",
             "A point that looks like it is on the line may not be. Substitute. The "
             "picture is a summary of the arithmetic, never a replacement for it."),
        ],
        "standard": ("Finish when you can plot a point, name its quadrant, and decide "
                     "membership of a graph by substituting rather than by looking.",
                     "Given six pairs and an equation you should be able to place all "
                     "six, classify each by sign, and say which are on the graph with "
                     "the arithmetic that proves it. That substitution test is the "
                     "definition every later lesson leans on, from the intercepts in "
                     "lesson 2 to the inverse in lesson 13."),
        "note": "The convention that `x` comes first is arbitrary but universal, and it "
                "is the same convention that makes `f(x)` in lesson 8 an input and the "
                "value it returns an output. Once a pair is written `(input, output)` "
                "the whole course reads in one direction.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "graphing-a-linear-equation",
        "title": "Graphing a Linear Equation",
        "module": "The coordinate plane",
        "one_line": "From a table of solutions to a straight line, and the intercept shortcut.",
        "summary": (
            "An equation in two unknowns has infinitely many solutions; plotting a few "
            "of them reveals the pattern. When the equation is linear, that pattern is "
            "a straight line, and two well-chosen points are enough to draw it."
        ),
        "key": [
            "solutions of ax + by = c  →  a straight line",
            "x-intercept:  set y = 0,  solve for x",
            "y-intercept:  set x = 0,  solve for y",
            "x = a  vertical          y = b  horizontal",
        ],
        "key_label": "Drawing a line from its equation",
        "concepts_intro": (
            "In course 2 an equation in one unknown usually had one answer. The same "
            "sentence with a second unknown has endlessly many, and the graph is how "
            "you hold all of them at once."
        ),
        "concepts": [
            ("A linear equation has infinitely many solutions",
             "`2x + 3y = 12` is satisfied by `(6, 0)`, `(0, 4)`, `(3, 2)` and by every "
             "other pair on one straight line. Solving it means describing that whole "
             "set, not finding \"the\" answer."),
            ("Two points determine the line, three points check it",
             "Geometry says two distinct points fix a line, so two solutions suffice. "
             "Plot a third anyway: if it misses, one of the three is wrong, and you "
             "find out now rather than in the next lesson."),
            ("Intercepts are the cheapest two points",
             "Setting `y = 0` and then `x = 0` each collapses the equation to one "
             "unknown, which is the case course 2 already solved. No other pair of "
             "points is easier to get."),
        ],
        "read_title": "Turning an equation into a line",
        "read_intro": "A table always works. Intercepts are faster. Two shapes are special.",
        "body": [
            ("def", ("Linear equation in two variables",
                     "An equation that can be written `ax + by = c` with `a` and `b` not "
                     "both zero. Its graph is a straight line, and every straight line "
                     "is the graph of such an equation.")),
            ("p", "The word linear earns its name here rather than in course 2: what is "
                  "straight is the graph. The defining feature on the algebra side is "
                  "that `x` and `y` each appear to the first power only, never "
                  "multiplied together, never inside a root or a denominator. `xy = 6` "
                  "and `y = x²` are equations in two variables that are not linear, and "
                  "their graphs are not lines."),
            ("h3", "The table method"),
            ("p", "Choose a value for `x`, substitute, solve the resulting one-unknown "
                  "equation for `y`, and record the pair. Repeat. This never fails and "
                  "needs no new technique, which makes it the method to fall back on "
                  "whenever a shortcut is not available or not remembered."),
            ("math", [
                "y = -2x + 1",
                "",
                "   x  │  -2x + 1        │   y   │  point",
                "  ────┼─────────────────┼───────┼──────────",
                "  -1  │  -2(-1) + 1 = 3 │    3  │  (-1,  3)",
                "   0  │  -2( 0) + 1 = 1 │    1  │  ( 0,  1)",
                "   1  │  -2( 1) + 1 = -1│   -1  │  ( 1, -1)",
                "   2  │  -2( 2) + 1 = -3│   -3  │  ( 2, -3)",
            ]),
            ("p", "Four points, and they fall in a line: each step of one to the right "
                  "drops `y` by two. That constant drop is the subject of lesson 3."),
            ("h3", "The intercept method"),
            ("def", ("Intercepts",
                     "The <strong>x-intercept</strong> is where the graph meets the "
                     "x-axis, found by setting `y = 0`. The <strong>y-intercept</strong> "
                     "is where it meets the y-axis, found by setting `x = 0`.")),
            ("p", "The rule is easy to state backwards, so anchor it to the picture: "
                  "every point on the x-axis has `y = 0`, so to land on the x-axis you "
                  "impose `y = 0`. The intercept you get is an x-value."),
            ("example", ("2x + 3y = 12 by intercepts",
                         "Set `y = 0`: `2x = 12`, so `x = 6` and the x-intercept is "
                         "`(6, 0)`. Set `x = 0`: `3y = 12`, so `y = 4` and the "
                         "y-intercept is `(0, 4)`. Check with a third: `(3, 2)` gives "
                         "`6 + 6 = 12`, true.")),
            ("p", "The method degrades gracefully rather than failing. A line through "
                  "the origin has both intercepts at `(0, 0)` &mdash; one point, not "
                  "two &mdash; so you take a second point from a table instead."),
            ("h3", "The two special shapes"),
            ("p", "When one of the coefficients is zero the equation loses a variable, "
                  "and the graph is a line parallel to an axis:"),
            ("ul", [
                "<strong>`x = a`</strong> &mdash; every point with x-coordinate `a`, "
                "whatever `y` is. A <em>vertical</em> line.",
                "<strong>`y = b`</strong> &mdash; every point with y-coordinate `b`, "
                "whatever `x` is. A <em>horizontal</em> line.",
            ]),
            ("p", "Both are genuine linear equations under the definition above: `x = a` "
                  "is `1·x + 0·y = a`. The instinct that `x = −2` should be a single "
                  "point comes from course 2, where it was one; with a second variable "
                  "present, `y` is unconstrained and the solution set is a whole line."),
            ("p", "Keep `x = −2` in view. It is the one shape that will fail the test in "
                  "lesson 7, and knowing what it looks like now is what makes that test "
                  "obvious later."),
        ],
        "lab": ("line", {
            "mode": "graph",
            "panel_title": "Two points, and everything that follows from them",
            "panel_intro": "The line, its two intercepts and the table of values are all "
                           "computed from the points you choose, so moving a point moves "
                           "all three together. The vertical preset shows what happens to "
                           "a table when one x-value has to serve every y.",
        }),
        "steps_title": "Graphing ax + by = c",
        "steps_intro": "Intercepts first, table as the fallback, third point always.",
        "steps": [
            ("Check for a missing variable",
             "If only `x` appears the line is vertical; if only `y`, horizontal. Draw it "
             "and stop &mdash; no table is needed."),
            ("Set y = 0 and solve for x",
             "This is a one-unknown equation of the kind course 2 handled. The result is "
             "the x-intercept `(x, 0)`."),
            ("Set x = 0 and solve for y",
             "Same again, giving `(0, y)`. If both intercepts came out at the origin, "
             "pick any other `x` and get a second point from the equation."),
            ("Plot a third point, then draw",
             "Any convenient `x`. If the three are not in a line, recheck the arithmetic "
             "before drawing anything; a ruler laid across two correct points and one "
             "wrong one hides the error."),
        ],
        "worked": {
            "title": "Graphing 2x + 3y = 12",
            "intro": ["Both intercepts, then a third point as the check."],
            "lines": [
                "y = 0:    2x + 3(0) = 12      2x = 12       x = 6     (6, 0)",
                "x = 0:    2(0) + 3y = 12      3y = 12       y = 4     (0, 4)",
                "",
                "check x = 3:",
                "          2(3) + 3y = 12      3y = 6        y = 2     (3, 2)",
                "",
                "the three points:",
                "          (6, 0)   (0, 4)   (3, 2)",
                "",
                "and (3, 2) is halfway between the other two, in both coordinates:",
                "          x:  (6 + 0)/2 = 3        y:  (0 + 4)/2 = 2",
            ],
            "after": [
                "The check point landing exactly midway is not luck. Equal steps in `x` "
                "produce equal steps in `y` on a line, which is the property lesson 3 "
                "isolates and names. What it confirms is that the three points are "
                "collinear &mdash; consistent with each other &mdash; and not that any "
                "of them satisfies `2x + 3y = 12`. Misread the constant as `24` and you "
                "get `(12, 0)`, `(0, 8)` and `(6, 4)`, which pass the midway check just "
                "as cleanly while every one of them is wrong for this equation. "
                "Correctness still rests on the substitutions: a third point can reveal "
                "an error, not certify its absence."
            ],
        },
        "quiz_title": "Lines from equations",
        "quiz": [
            {"q": "What is the x-intercept of `3x − 4y = 24`?",
             "a": ["`(0, −6)`", "`(8, 0)`", "`(0, 8)`", "`(−6, 0)`"],
             "c": 1,
             "why": "Set `y = 0`: `3x = 24`, so `x = 8`, giving `(8, 0)`. Setting `x = 0` "
                    "instead would give the y-intercept `(0, −6)`."},
            {"q": "What does the graph of `x = 5` look like?",
             "a": ["A single point at `(5, 0)`",
                   "A horizontal line through `(0, 5)`",
                   "A vertical line through `(5, 0)`",
                   "It is not a linear equation"],
             "c": 2,
             "why": "Every pair with x-coordinate 5 satisfies it, whatever `y` is, so the "
                    "solution set is a vertical line. It is linear: `1·x + 0·y = 5`."},
            {"q": "You plot three solutions of a linear equation and they are not in a "
                  "line. What follows?",
             "a": ["The equation has no graph",
                   "At least one of the three is wrong",
                   "The axes are scaled differently",
                   "The equation must be non-linear"],
             "c": 1,
             "why": "A linear equation's solutions always lie on one line, and unequal "
                    "axis scales stretch a line but never bend it. The arithmetic on at "
                    "least one point is wrong."},
        ],
        "mistakes": [
            ("Swapping which variable to zero",
             "For the x-intercept you set `y = 0`. Setting `x = 0` and calling the answer "
             "an x-intercept is the single most common slip here; tie the rule to the "
             "picture, since every point on the x-axis has height zero."),
            ("Drawing the line through only two points",
             "Two points always look consistent, because two points always lie on a "
             "line. The third point is the only one that can reveal an error."),
            ("Reading `x = −2` as a point",
             "With two variables in play the equation constrains `x` and says nothing "
             "about `y`, so the solution set is a vertical line. The one-variable habit "
             "from course 2 is what needs unlearning."),
        ],
        "standard": ("Finish when you can graph any `ax + by = c` from its intercepts and "
                     "know when to fall back on a table.",
                     "Given five equations including one vertical, one horizontal and one "
                     "through the origin, you should produce a correct line for each and "
                     "say which method you used and why. Recognising that the "
                     "through-the-origin case defeats the intercept shortcut is the part "
                     "that distinguishes a method from a memorised procedure."),
        "note": "Notice what the table in this lesson showed: a step of one in `x` always "
                "changed `y` by the same amount. That number is the entire subject of "
                "lesson 3, and every form of a line in lessons 4 and 5 is built around "
                "it.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "slope",
        "title": "Slope",
        "module": "Lines",
        "one_line": "One number for steepness and direction, and why it does not depend on the two points you pick.",
        "summary": (
            "Slope is the constant ratio of vertical change to horizontal change along "
            "a line. Getting it right is a matter of subtracting in a consistent order, "
            "and of keeping zero and undefined firmly apart."
        ),
        "key": [
            "m = (y₂ − y₁)/(x₂ − x₁)          rise over run",
            "same order top and bottom, or the sign flips",
            "horizontal:  m = 0          vertical:  m undefined",
            "m > 0 rises left to right,  m < 0 falls",
        ],
        "key_label": "Slope in four lines",
        "concepts_intro": (
            "Lesson 2 noticed that equal steps in `x` gave equal steps in `y`. Slope is "
            "that observation turned into a number that can be computed and compared."
        ),
        "concepts": [
            ("Slope is a ratio, not an angle",
             "It is a quotient of two differences, so it survives any rescaling of the "
             "drawing. This is why slope is the reliable measure of steepness and the "
             "visual impression is not."),
            ("The answer does not depend on the two points",
             "Pick any two distinct points on a line and the ratio comes out the same. "
             "Similar triangles are the reason, and it is what makes \"the\" slope of a "
             "line a well-defined thing at all."),
            ("Zero and undefined are opposite situations",
             "A horizontal line has `m = 0`: the rise is zero. A vertical line has no "
             "slope at all: the run is zero and the division is illegal. Calling a "
             "vertical line's slope zero merges the two flattest and steepest cases."),
        ],
        "read_title": "Measuring steepness",
        "read_intro": "One formula, one ordering rule, and two special cases.",
        "body": [
            ("def", ("Slope",
                     "For two distinct points `(x₁, y₁)` and `(x₂, y₂)` on a line with "
                     "`x₁ ≠ x₂`, the <strong>slope</strong> is "
                     "`m = (y₂ − y₁)/(x₂ − x₁)`, the <strong>rise</strong> divided by the "
                     "<strong>run</strong>.")),
            ("p", "Read it as a rate: `m` is how much `y` changes per unit increase in "
                  "`x`. A slope of `3/2` means that going 2 to the right takes you 3 up, "
                  "and equally that going 1 to the right takes you `3/2` up. Both "
                  "readings are useful and they are the same statement."),
            ("thm", ("Slope is well defined",
                     "Any two distinct points on a line give the same slope. Two choices "
                     "of point pair produce similar right triangles &mdash; equal angles, "
                     "because the hypotenuses lie along the same line and the legs are "
                     "parallel to the axes &mdash; and similar triangles have "
                     "proportional sides, so the ratio rise/run agrees.")),
            ("p", "Without that theorem the phrase \"the slope of the line\" would be "
                  "meaningless, because different people would compute different numbers "
                  "for the same line. It is the reason a single number can stand in for "
                  "a whole line's steepness in every formula that follows."),
            ("h3", "The ordering rule"),
            ("p", "The subtraction must run in the same direction in the numerator and "
                  "the denominator. Both `(y₂ − y₁)/(x₂ − x₁)` and `(y₁ − y₂)/(x₁ − x₂)` "
                  "are correct and equal, because negating both parts of a fraction "
                  "leaves it unchanged. What is wrong is mixing them:"),
            ("math", [
                "points  (-2, 1)  and  (4, 10)",
                "",
                "correct    (10 - 1) / (4 - (-2))   =   9 /  6   =   3/2",
                "correct    (1 - 10) / (-2 - 4)     =  -9 / -6   =   3/2",
                "",
                "WRONG      (10 - 1) / (-2 - 4)     =   9 / -6   =  -3/2",
                "                                              sign flipped",
            ]),
            ("p", "The wrong version is not a small error. It reports a line that falls "
                  "where the real one rises, and every later form built on that slope "
                  "inherits the mistake. Fix the order once, at the point of writing the "
                  "fraction: decide which point is first and use it first in both "
                  "differences."),
            ("h3", "Sign and the two special cases"),
            ("ul", [
                "<strong>`m &gt; 0`</strong> &mdash; the line rises from left to right.",
                "<strong>`m &lt; 0`</strong> &mdash; the line falls from left to right.",
                "<strong>`m = 0`</strong> &mdash; horizontal. The rise is zero for every "
                "pair of points, so the quotient is zero.",
                "<strong>undefined</strong> &mdash; vertical. The run is zero, and "
                "division by zero is not an operation.",
            ]),
            ("p", "The last two are worth separating carefully, because English blurs "
                  "them. \"No slope\" is ambiguous and best avoided; say `m = 0` for "
                  "horizontal and \"slope undefined\" for vertical. The distinction "
                  "returns with consequences in lesson 6, where the perpendicular rule "
                  "needs both slopes to exist, and again in lesson 7."),
            ("example", ("Four slopes",
                         "`(−2, 1)` to `(4, 10)`: `9/6 = 3/2`, rising. `(1, 7)` to "
                         "`(3, 1)`: `−6/2 = −3`, falling. `(−3, 4)` to `(6, 4)`: "
                         "`0/9 = 0`, horizontal. `(5, 2)` to `(5, 9)`: run is `0`, so "
                         "the slope is undefined.")),
            ("p", "One habit worth forming now: after computing a slope, glance at the "
                  "two points and ask whether the sign is plausible. Going from "
                  "`(1, 7)` to `(3, 1)` clearly moves right and down, so a negative "
                  "answer is expected and `−3` passes the glance. This catches the "
                  "ordering error in the time it takes to read."),
        ],
        "lab": ("line", {
            "mode": "slope",
            "panel_title": "Move two points, watch the ratio",
            "panel_intro": "Drag either point and the rise, the run and the quotient are "
                           "recomputed exactly. Slide the two points along the line "
                           "without leaving it and the slope does not move &mdash; that "
                           "is the well-definedness theorem, checked rather than asserted.",
        }),
        "steps_title": "Computing a slope from two points",
        "steps_intro": "Label, subtract in order, simplify, sanity-check the sign.",
        "steps": [
            ("Label the points",
             "Write `(x₁, y₁)` and `(x₂, y₂)` above the numbers. Which point you call "
             "first does not matter; that you then stay with the choice does."),
            ("Check for a vertical line first",
             "If `x₁ = x₂` the run is zero and the slope is undefined. Stop here rather "
             "than writing a fraction with zero underneath."),
            ("Subtract in the same order top and bottom",
             "`(y₂ − y₁)` over `(x₂ − x₁)`. Watch the double negatives: subtracting a "
             "negative x-coordinate adds."),
            ("Simplify, then check the sign against the picture",
             "Reduce the fraction. Then confirm: right-and-up or left-and-down means "
             "positive, right-and-down means negative."),
        ],
        "worked": {
            "title": "The slope through (−2, 1) and (4, 10), three ways",
            "intro": ["Once in each order, then from a third point on the same line, to "
                      "see that all three agree."],
            "lines": [
                "taking (-2, 1) first:",
                "     m = (10 - 1) / (4 - (-2))  =  9 / (4 + 2)  =  9/6  =  3/2",
                "",
                "taking (4, 10) first:",
                "     m = (1 - 10) / (-2 - 4)    =  -9 / -6      =  9/6  =  3/2",
                "",
                "the point (0, 4) is on this line too, since  3/2 · 0 + 4 = 4:",
                "     with (-2, 1):   (4 - 1) / (0 - (-2))   =  3/2",
                "     with (4, 10):   (10 - 4) / (4 - 0)     =  6/4  =  3/2",
                "",
                "all four computations:   3/2",
            ],
            "after": [
                "The step `4 − (−2) = 6` is where arithmetic errors cluster. Subtracting "
                "a negative adds, and writing the parentheses rather than doing it in "
                "your head is what keeps the run from coming out as 2.",
                "That every pair gives `3/2` is the theorem in action. It is also the "
                "reason lesson 5 can build the line from whichever point is convenient.",
            ],
        },
        "quiz_title": "Rise over run",
        "quiz": [
            {"q": "What is the slope through `(1, 7)` and `(3, 1)`?",
             "a": ["`3`", "`−3`", "`−1/3`", "`1/3`"],
             "c": 1,
             "why": "`(1 − 7)/(3 − 1) = −6/2 = −3`. The points move right and down, so a "
                    "negative slope is expected; `−1/3` inverts the ratio."},
            {"q": "What is the slope of the line through `(5, 2)` and `(5, 9)`?",
             "a": ["`0`", "`7`", "Undefined", "`1`"],
             "c": 2,
             "why": "The run is `5 − 5 = 0`, and division by zero is not defined. This is "
                    "a vertical line. Zero would be the answer for a horizontal one."},
            {"q": "A student computes `(y₂ − y₁)/(x₁ − x₂)`. What is wrong with the answer?",
             "a": ["Nothing &mdash; it is an equivalent form",
                   "It is the reciprocal of the correct slope",
                   "It has the correct magnitude but the wrong sign",
                   "It is only wrong when the slope is negative"],
             "c": 2,
             "why": "The denominator has been negated but the numerator has not, so the "
                    "whole fraction is negated. The size is right and the direction is "
                    "reversed, whatever the true sign happens to be."},
        ],
        "mistakes": [
            ("Mixing the order of subtraction",
             "Consistency is the whole rule. `(y₂ − y₁)/(x₂ − x₁)` and "
             "`(y₁ − y₂)/(x₁ − x₂)` are both fine; one of each is a sign error that the "
             "answer alone will not reveal."),
            ("Writing run over rise",
             "The definition is vertical change divided by horizontal change. Inverting "
             "it turns a slope of `3` into `1/3`, which is a genuinely different line "
             "and, as lesson 6 shows, not even the perpendicular one."),
            ("Saying a vertical line has slope zero",
             "Zero rise gives `m = 0` and describes a horizontal line. Zero run gives no "
             "slope at all. Merging them makes the flattest and the steepest lines "
             "indistinguishable in every formula that takes `m` as input."),
        ],
        "standard": ("Finish when you can compute a slope from any two points, including "
                     "negative coordinates, and classify the two degenerate cases "
                     "correctly.",
                     "Given eight point pairs, some with negative coordinates, one "
                     "horizontal and one vertical, you should produce eight correct "
                     "answers with the right signs and the word \"undefined\" exactly "
                     "once. Slope feeds every form in lessons 4 and 5, so a sign error "
                     "here is a wrong line there."),
        "note": "Slope is the first rate of change in this library. The same quotient, "
                "taken between two points that are brought closer and closer together, "
                "is the derivative &mdash; which is calculus and out of scope here. What "
                "makes the linear case special is that the ratio is the same for every "
                "pair of points, so one number describes the whole line.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "slope-intercept-form",
        "title": "Slope-Intercept Form",
        "module": "Lines",
        "one_line": "y = mx + b, and reading a line straight off its equation.",
        "summary": (
            "Solving a linear equation for `y` puts the slope and the y-intercept in "
            "plain sight, which makes graphing immediate and comparison between two "
            "lines a matter of looking."
        ),
        "key": [
            "y = mx + b        m = slope,  b = y-intercept",
            "to get there:  solve for y",
            "graph:  plot (0, b), then step by the slope",
            "y = 4        m = 0        a horizontal line",
        ],
        "key_label": "The form you graph from",
        "concepts_intro": (
            "The same line has many equations. This one is arranged so that the two "
            "numbers you need in order to draw it are simply there to be read."
        ),
        "concepts": [
            ("The form exposes what you need",
             "In `y = mx + b`, the coefficient of `x` is the slope and the constant is "
             "the y-intercept. No work is required to extract them &mdash; which is the "
             "entire reason for rearranging into this shape."),
            ("Getting there is one goal: isolate y",
             "Whatever the equation looks like, the procedure is course 2's: undo the "
             "additions, then undo the multiplication. The only new demand is finishing "
             "in exactly the shape `mx + b`."),
            ("Every non-vertical line has one such equation",
             "Vertical lines are the sole exception, since they cannot be solved for `y` "
             "at all. That exception is not an inconvenience; it is a signal, and lesson "
             "7 explains what it signals."),
        ],
        "read_title": "Solving for y, and what that buys",
        "read_intro": "The rearrangement, the reading, and the graphing method it enables.",
        "body": [
            ("def", ("Slope-intercept form",
                     "A non-vertical line written `y = mx + b`, where `m` is the slope "
                     "and `(0, b)` is the y-intercept.")),
            ("p", "Why `b` is the y-intercept takes one substitution rather than "
                  "memory: the y-intercept is where `x = 0`, and putting `x = 0` into "
                  "`y = mx + b` gives `y = b`. Why `m` is the slope takes two: at "
                  "`x = 0` the height is `b`, at `x = 1` it is `m + b`, so a run of 1 "
                  "produces a rise of `m`."),
            ("h3", "Rearranging into the form"),
            ("p", "The work is course 2's, applied to an equation that keeps `x` around "
                  "as a passenger. Move every term that is not `y` to the other side, "
                  "then divide by whatever multiplies `y` &mdash; dividing the "
                  "<em>whole</em> side, every term:"),
            ("math", [
                "2x + 3y = 12",
                "     3y = -2x + 12          subtract 2x from both sides",
                "      y = (-2x + 12)/3      divide both sides by 3",
                "      y = -(2/3)x + 4       divide EACH term",
                "",
                "                  m = -2/3        b = 4",
            ]),
            ("p", "The last step is where a term gets dropped. `(-2x + 12)/3` is "
                  "`-(2/3)x + 4`, not `-(2/3)x + 12`: the divisor applies to every term "
                  "of the numerator. Checking against lesson 2 settles it &mdash; the "
                  "intercepts there were `(0, 4)` and `(6, 0)`, and `-(2/3)(6) + 4 = 0` "
                  "confirms both."),
            ("example", ("4x − 2y = 10",
                         "`−2y = −4x + 10`, then dividing by `−2` gives `y = 2x − 5`. "
                         "Both signs change, because both terms are divided by a negative. "
                         "Check with `(3, 1)`: the original gives `12 − 2 = 10`, and the "
                         "new form gives `2(3) − 5 = 1`.")),
            ("p", "Dividing by a negative is the reliable source of errors in this "
                  "lesson. It changes the sign of every term it touches, and changing "
                  "only the first is a mistake that leaves a plausible-looking equation "
                  "behind. The check by substitution costs a few seconds and catches it."),
            ("h3", "Graphing from the form"),
            ("p", "Plot `(0, b)`. Then use the slope as a set of instructions: write it "
                  "as a fraction rise/run, move that run to the right and that rise up "
                  "(down, if the slope is negative), and mark the point you land on. Two "
                  "points, and the line is drawn."),
            ("example", ("Graphing y = −(3/4)x + 2",
                         "Start at `(0, 2)`. The slope `−3/4` says: run 4 right, rise "
                         "`−3`, meaning 3 down. That lands on `(4, −1)`, and indeed "
                         "`−(3/4)(4) + 2 = −3 + 2 = −1`.")),
            ("p", "A whole-number slope is a fraction too: `m = 2` is `2/1`, so the "
                  "instruction is 1 right and 2 up. Forgetting the invisible denominator "
                  "is what turns a slope of 2 into a step of 2 right and 2 up, which is a "
                  "line of slope 1."),
            ("p", "The form also makes comparison trivial, and that is what lesson 6 "
                  "will use: two lines written this way can be checked for parallelism "
                  "by looking at two coefficients, with no computation at all."),
        ],
        "lab": ("line", {
            "mode": "forms",
            "panel_title": "Slope-intercept, beside the alternatives",
            "panel_intro": "Each form is derived from your two points independently and "
                           "then checked by substituting both points back in. Watch the "
                           "slope and the y-intercept appear in `y = mx + b` as the two "
                           "numbers you can simply read, and nowhere else so plainly.",
        }),
        "steps_title": "Putting a line into y = mx + b",
        "steps_intro": "Isolate `y`, then read the two numbers off.",
        "steps": [
            ("Check that it can be done",
             "If the equation has no `y` at all it is vertical, and this form does not "
             "exist for it. Say so rather than forcing it."),
            ("Move everything but the y-term across",
             "Add or subtract from both sides. The `x`-term goes to the right; the "
             "constant that was with `y` goes with it."),
            ("Divide every term by the coefficient of y",
             "Every term, not just the first. If that coefficient is negative, expect "
             "every sign on the right to change."),
            ("Read m and b, then check one point",
             "The coefficient of `x` is `m`; the constant is `b`. Substitute any "
             "convenient `x` into both the original and the new equation and confirm the "
             "same `y` comes out."),
        ],
        "worked": {
            "title": "4x − 2y = 10, rearranged, read and checked",
            "intro": ["Isolate `y`, extract the two numbers, then verify against the "
                      "original equation."],
            "lines": [
                "4x - 2y = 10",
                "    -2y = -4x + 10           subtract 4x",
                "      y = 2x - 5             divide EVERY term by -2",
                "",
                "read off:      m = 2         b = -5        y-intercept (0, -5)",
                "",
                "check (0, -5):    original   4(0) - 2(-5) = 0 + 10 = 10   TRUE",
                "check x = 3:      new form   y = 2(3) - 5 = 1",
                "                  original   4(3) - 2(1) = 12 - 2 = 10    TRUE",
                "",
                "graph:  from (0, -5), slope 2 = 2/1, so 1 right and 2 up  ->  (1, -3)",
            ],
            "after": [
                "Dividing `−2y = −4x + 10` by `−2` changes both signs on the right: "
                "`−4x` becomes `+2x` and `+10` becomes `−5`. Changing one and not the "
                "other gives `y = 2x + 5`, which passes no substitution check at all.",
                "The two verifications are different in kind. The first confirms the "
                "intercept is a genuine solution; the second confirms the two equations "
                "have the same solutions, which is what rearranging is supposed to "
                "preserve.",
            ],
        },
        "quiz_title": "Reading m and b",
        "quiz": [
            {"q": "Put `6x + 2y = 8` into slope-intercept form.",
             "a": ["`y = −3x + 4`", "`y = 3x + 4`", "`y = −6x + 8`", "`y = −3x + 8`"],
             "c": 0,
             "why": "`2y = −6x + 8`, then dividing every term by 2 gives `y = −3x + 4`. "
                    "The last option divides the `x`-term but forgets the constant."},
            {"q": "What is the slope of `y = 7`?",
             "a": ["`7`", "`0`", "Undefined", "`1`"],
             "c": 1,
             "why": "It is `y = 0·x + 7`, so `m = 0` and the line is horizontal. Slope 7 "
                    "would need `x` to appear with coefficient 7."},
            {"q": "Which line cannot be written as `y = mx + b`?",
             "a": ["A horizontal line", "A line through the origin",
                   "A vertical line", "A line with negative slope"],
             "c": 2,
             "why": "A vertical line `x = a` cannot be solved for `y`, since `y` does not "
                    "appear in it. A horizontal line is the case `m = 0`, and a line "
                    "through the origin is `b = 0`."},
        ],
        "mistakes": [
            ("Dividing only the first term",
             "`(−2x + 12)/3` is `−(2/3)x + 4`. Leaving the constant undivided is the "
             "commonest slip in the rearrangement, and it moves the line without "
             "changing its slope, so the graph looks reasonable."),
            ("Losing a sign when dividing by a negative",
             "Dividing by `−2` flips the sign of every term on the other side. Flipping "
             "one of them produces an equation that is wrong at every point except where "
             "the two lines happen to cross."),
            ("Reading `m` off before solving for y",
             "In `2x + 3y = 12` the slope is not 2. The coefficient of `x` is only the "
             "slope once `y` stands alone with coefficient 1; here the slope is `−2/3`."),
        ],
        "standard": ("Finish when you can convert any non-vertical line to `y = mx + b` "
                     "and graph it from the two numbers without a table.",
                     "Given five equations in mixed arrangements, including one with a "
                     "negative `y`-coefficient and one horizontal, you should produce "
                     "correct slope-intercept forms and sketch each from `(0, b)` and a "
                     "slope step. Lesson 6 compares lines in this form, so fluency here "
                     "is what makes parallel and perpendicular a matter of looking."),
        "note": "This form is the one to reach for when the question is \"what does the "
                "line look like\" or \"how do two lines compare\". When the question "
                "instead hands you a point and a slope, lesson 5's point-slope form gets "
                "there with less algebra &mdash; the forms are tools, and part of the "
                "skill is picking one.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "point-slope-and-standard-form",
        "title": "Point-Slope and Standard Form",
        "module": "Lines",
        "one_line": "Building a line from a point and a slope, and the form that treats x and y alike.",
        "summary": (
            "Point-slope form writes down a line the moment you have one point and a "
            "slope, with no solving. Standard form keeps `x` and `y` symmetric, which is "
            "what systems and intercepts want. Neither replaces the other."
        ),
        "key": [
            "y − y₁ = m(x − x₁)          point-slope",
            "Ax + By = C                 standard",
            "two points  →  find m  →  point-slope  →  simplify",
            "either point works; the line is the same",
        ],
        "key_label": "Two more forms, and when each wins",
        "concepts_intro": (
            "A line is pinned down by a point and a direction, or by two points. Each "
            "form below is the shortest route from one of those starting positions to an "
            "equation."
        ),
        "concepts": [
            ("Point-slope is the definition of slope, rearranged",
             "Slope from `(x₁, y₁)` to a general point `(x, y)` is "
             "`(y − y₁)/(x − x₁) = m`. Multiplying up gives the form. It is not a new "
             "fact to memorise, it is lesson 3 with the fraction cleared."),
            ("Either point gives the same line",
             "Given two points you may build from whichever you prefer. The two "
             "equations look different and simplify to the same thing, which is worth "
             "seeing once so that a mismatch with a textbook answer does not read as an "
             "error."),
            ("Standard form is symmetric, and that is its use",
             "`Ax + By = C` treats the two variables alike, so it covers vertical lines, "
             "hands you both intercepts cheaply, and is the shape course 8 needs for "
             "elimination. It hides the slope, which is the price."),
        ],
        "read_title": "Two forms and the choice between them",
        "read_intro": "Where each comes from, what each makes easy, and how to convert.",
        "body": [
            ("def", ("Point-slope form",
                     "The line through `(x₁, y₁)` with slope `m` is "
                     "`y − y₁ = m(x − x₁)`.")),
            ("thm", ("Why the form is what it is",
                     "Let `(x, y)` be any other point on the line. By lesson 3 the slope "
                     "computed from `(x₁, y₁)` to `(x, y)` must equal `m`, so "
                     "`(y − y₁)/(x − x₁) = m`. Multiplying both sides by `(x − x₁)` "
                     "gives `y − y₁ = m(x − x₁)`. The multiplication also admits the "
                     "point `(x₁, y₁)` itself, which the fraction had to exclude.")),
            ("p", "That derivation is worth following once, because it explains the "
                  "minus signs. The form contains `x − x₁`, so a point with a negative "
                  "coordinate produces a double negative: through `(−2, 1)` the form is "
                  "`y − 1 = m(x − (−2))`, that is, `y − 1 = m(x + 2)`. Writing the "
                  "substitution before simplifying is what keeps that straight."),
            ("h3", "From two points"),
            ("p", "Two points is the most common starting position, and it is handled in "
                  "two moves: compute the slope by lesson 3, then feed it and either "
                  "point into point-slope. Nothing else is needed."),
            ("math", [
                "through (-2, 1) and (4, 10)",
                "",
                "slope       m = (10 - 1)/(4 - (-2)) = 9/6 = 3/2",
                "",
                "using (-2, 1):     y - 1  = (3/2)(x + 2)",
                "                   y - 1  = (3/2)x + 3",
                "                       y  = (3/2)x + 4",
                "",
                "using (4, 10):     y - 10 = (3/2)(x - 4)",
                "                   y - 10 = (3/2)x - 6",
                "                       y  = (3/2)x + 4        the same line",
            ]),
            ("p", "The two routes converge, as the concept above promised. If yours does "
                  "not converge with a printed answer, put both into slope-intercept form "
                  "and compare there &mdash; that form is unique for a given line, so it "
                  "settles the question."),
            ("h3", "Standard form"),
            ("def", ("Standard form",
                     "`Ax + By = C` with `A`, `B`, `C` integers, `A` and `B` not both "
                     "zero. It is conventional to clear fractions and to take `A` "
                     "positive.")),
            ("p", "Converting into it means clearing denominators and collecting both "
                  "variables on the left. From `y = (3/2)x + 4`: multiply by 2 to get "
                  "`2y = 3x + 8`, then move the `x`-term across for `−3x + 2y = 8`, and "
                  "finally negate throughout so that `A` is positive: `3x − 2y = −8`. "
                  "Negating an equation changes no solutions."),
            ("example", ("Checking the conversion",
                         "`3x − 2y = −8` at `(−2, 1)`: `−6 − 2 = −8`, true. At `(4, 10)`: "
                         "`12 − 20 = −8`, true. Both original points satisfy the "
                         "converted equation, which is what a conversion has to preserve.")),
            ("p", "Standard form is the only one of the three that copes with every "
                  "line: `x = 5` is `1·x + 0·y = 5`. Point-slope needs a slope to exist "
                  "and slope-intercept needs to be solvable for `y`, so both fail on "
                  "vertical lines, while standard form does not notice the difference."),
            ("p", "Choosing between the forms is part of the skill. Point and slope, or "
                  "two points, go to point-slope. A question about shape, steepness or "
                  "comparison goes to slope-intercept. Intercepts, or a system to be "
                  "solved by elimination in course 8, go to standard."),
        ],
        "lab": ("line", {
            "mode": "pointslope",
            "panel_title": "Built from each point in turn",
            "panel_intro": "Point-slope form is written from both of your points, "
                           "expanded, and the two results compared. They are derived "
                           "separately, so their agreement is evidence that either point "
                           "may be used &mdash; not a restatement of the claim.",
        }),
        "steps_title": "Finding the equation of a line through two points",
        "steps_intro": "Slope, substitute, simplify, verify with the point you did not use.",
        "steps": [
            ("Compute the slope",
             "`m = (y₂ − y₁)/(x₂ − x₁)`, in a consistent order. If the two `x`-values "
             "agree the line is vertical and the answer is `x = x₁`; stop there."),
            ("Substitute into point-slope",
             "`y − y₁ = m(x − x₁)` with either point. Write the substitution out, "
             "including the brackets around a negative coordinate, before touching it."),
            ("Simplify to the form the question wants",
             "Distribute `m`, then isolate `y` for slope-intercept, or clear fractions "
             "and collect terms for standard form."),
            ("Check with the other point",
             "Substitute the point you did not build from. It must satisfy the final "
             "equation &mdash; this is the check that catches a slope or sign error, "
             "because that point played no part in producing the answer."),
        ],
        "worked": {
            "title": "The line through (−2, 1) and (4, 10), in all three forms",
            "intro": ["Slope first, then point-slope, then the two simplified forms, then "
                      "a check that uses both points."],
            "lines": [
                "1.  slope",
                "        m = (10 - 1) / (4 - (-2)) = 9/6 = 3/2",
                "",
                "2.  point-slope, from (-2, 1)",
                "        y - 1 = (3/2)(x - (-2))",
                "        y - 1 = (3/2)(x + 2)",
                "3.  slope-intercept",
                "        y - 1 = (3/2)x + 3",
                "            y = (3/2)x + 4",
                "",
                "4.  standard",
                "           2y = 3x + 8            multiply through by 2",
                "     -3x + 2y = 8                 collect on the left",
                "      3x - 2y = -8                negate so that A > 0",
                "5.  check BOTH points in the final form",
                "        (-2, 1):   3(-2) - 2(1)  = -6 - 2  = -8   TRUE",
                "        ( 4, 10):  3(4)  - 2(10) = 12 - 20 = -8   TRUE",
            ],
            "after": [
                "Step 2 is where the sign errors live. The form subtracts `x₁`, and `x₁` "
                "is `−2`, so the bracket becomes `x + 2`. Writing `x − 2` here produces a "
                "line parallel to the right one and through neither point.",
                "Step 5 is the reason to trust the answer. The point `(4, 10)` was never "
                "used after step 1, so its satisfying the final equation is genuine "
                "evidence rather than a restatement of the work.",
            ],
        },
        "quiz_title": "Building a line",
        "quiz": [
            {"q": "What is the equation of the line through `(2, 5)` with slope `−4`?",
             "a": ["`y = −4x + 13`", "`y = −4x + 5`", "`y = −4x − 3`", "`y = −4x + 22`"],
             "c": 0,
             "why": "`y − 5 = −4(x − 2)` gives `y − 5 = −4x + 8`, so `y = −4x + 13`. "
                    "Check: `−4(2) + 13 = 5`. The third option distributes `−4` over "
                    "`x − 2` as `−4x − 8`."},
            {"q": "You build a line from two points, once from each point. What should "
                  "happen?",
             "a": ["The two equations describe different lines",
                   "The two equations simplify to the same line",
                   "Only the first point gives a valid equation",
                   "The slopes will differ by a sign"],
             "c": 1,
             "why": "Both equations describe the unique line through the two points, so "
                    "they must simplify to the same thing even though the unsimplified "
                    "forms look different."},
            {"q": "Which form can represent the vertical line `x = 5`?",
             "a": ["Slope-intercept only", "Point-slope only",
                   "Standard form", "None of the three"],
             "c": 2,
             "why": "`x = 5` is `1·x + 0·y = 5`. The other two forms both require a "
                    "slope, and a vertical line has none."},
        ],
        "mistakes": [
            ("Dropping the minus signs built into the form",
             "The form is `y − y₁ = m(x − x₁)`. Through `(−2, 1)` that is "
             "`y − 1 = m(x + 2)`. Substituting a negative coordinate without brackets is "
             "how `x + 2` becomes `x − 2` and the line moves."),
            ("Distributing over only the first term",
             "`−4(x − 2)` is `−4x + 8`. Getting `−4x − 8` shifts the line by 16 and "
             "still produces a straight, plausible answer, which is why the check with "
             "the unused point matters."),
            ("Treating standard form as a normal form",
             "`3x − 2y = −8` and `6x − 4y = −16` are the same line. Two standard forms "
             "can differ by a constant multiple, so comparing lines is a job for "
             "slope-intercept, which is unique."),
        ],
        "standard": ("Finish when two points, or a point and a slope, become an equation "
                     "in any requested form without hesitation.",
                     "Given six lines specified in mixed ways &mdash; two points, a point "
                     "and a slope, one vertical &mdash; you should produce the requested "
                     "form each time and verify with a point that was not used in the "
                     "construction. That verification habit is what makes the answer "
                     "yours rather than the back of the book's."),
        "note": "Point-slope is the form that generalises furthest. Later courses write "
                "the tangent to a curve at a point in exactly this shape, because a point "
                "and a direction is all a tangent is; what changes is where the slope "
                "comes from, not the form it feeds.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "parallel-and-perpendicular-lines",
        "title": "Parallel and Perpendicular Lines",
        "module": "Lines",
        "one_line": "Two slope tests, and the vertical case that neither test covers.",
        "summary": (
            "Parallel lines have equal slopes; perpendicular lines have slopes whose "
            "product is `−1`. Both tests are stated for lines that have slopes, which "
            "leaves the vertical case to be handled separately and deliberately."
        ),
        "key": [
            "parallel:        m₁ = m₂   (and different intercepts)",
            "perpendicular:   m₁m₂ = −1",
            "so m₂ = −1/m₁    the NEGATIVE RECIPROCAL",
            "x = a ⊥ y = b    true, but not by the product rule",
        ],
        "key_label": "Two tests and one exception",
        "concepts_intro": (
            "Both relationships are about direction alone, and slope is exactly the "
            "number that captures direction. That is why both tests are one line long."
        ),
        "concepts": [
            ("Equal slopes mean parallel, provided the lines are different",
             "If the intercepts also agree the two equations describe one line, which is "
             "not usually what \"parallel\" is meant to include. Check `b` as well as "
             "`m` before answering."),
            ("Perpendicular means negative reciprocal",
             "Flip the fraction and change the sign: `2/3` becomes `−3/2`. Doing only "
             "one of the two operations is the standard error, and each alone leaves a "
             "line that is not perpendicular to anything relevant."),
            ("The vertical case sits outside both tests",
             "`m₁m₂ = −1` presupposes two slopes. A vertical and a horizontal line are "
             "perpendicular by geometry, but no product can show it because one slope "
             "does not exist."),
        ],
        "read_title": "Comparing two lines",
        "read_intro": "One test for each relationship, then the case the tests exclude.",
        "body": [
            ("def", ("Parallel",
                     "Two distinct lines are <strong>parallel</strong> when they never "
                     "meet. For non-vertical lines this happens exactly when their "
                     "slopes are equal.")),
            ("p", "The connection to slope is easy to believe and easy to justify: equal "
                  "slopes mean equal rise per unit run, so the vertical gap between the "
                  "lines is the same at every `x`. If that gap is zero the lines "
                  "coincide, and if it is anything else they never touch."),
            ("p", "In slope-intercept form the test is pure inspection. `y = 2x + 1` and "
                  "`y = 2x − 5` are parallel: same `m`, different `b`. This is what "
                  "lesson 4 was buying &mdash; and note that `4x − 2y = 10` is the second "
                  "of those lines in disguise, which no amount of staring at the "
                  "standard form would reveal."),
            ("def", ("Perpendicular",
                     "Two lines are <strong>perpendicular</strong> when they meet at a "
                     "right angle. For lines with slopes `m₁` and `m₂`, this happens "
                     "exactly when `m₁m₂ = −1`, equivalently `m₂ = −1/m₁`.")),
            ("p", "The negative and the reciprocal do separate jobs, and separating them "
                  "is what makes the rule stick. The reciprocal exchanges rise and run "
                  "&mdash; a quarter turn swaps the horizontal and vertical legs of the "
                  "slope triangle &mdash; and the negative sign reverses direction, "
                  "because a quarter turn sends a rising line to a falling one."),
            ("math", [
                "m1        perpendicular m2        product",
                "-------   --------------------    -------",
                "  2           -1/2                  -1",
                " -3            1/3                  -1",
                "  3/4         -4/3                  -1",
                " -2/3          3/2                  -1",
                "  1           -1                    -1",
            ]),
            ("p", "Every line of that table is one calculation: flip, then negate. The "
                  "last row is the one to remember as a picture &mdash; `y = x` and "
                  "`y = −x` visibly cross at a right angle, and their slopes multiply to "
                  "`−1`."),
            ("h3", "The vertical exception"),
            ("p", "A vertical line `x = a` and a horizontal line `y = b` are "
                  "perpendicular; you can see the right angle. But the horizontal line "
                  "has `m = 0` and the vertical line has no slope, so the product test "
                  "cannot be applied: there is no second number to multiply, and `0` "
                  "times anything is `0`, never `−1`."),
            ("p", "This is not a flaw in the rule, it is the rule's stated scope. The "
                  "theorem is about lines that have slopes. Handle vertical lines by "
                  "recognising them first: perpendicular to a vertical line means "
                  "horizontal, and perpendicular to a horizontal line means vertical, "
                  "both settled without any arithmetic."),
            ("example", ("Through (1, 2), parallel and perpendicular to y = −3x + 7",
                         "Parallel: same slope `−3`, so `y − 2 = −3(x − 1)` gives "
                         "`y = −3x + 5`. Perpendicular: slope `1/3`, so "
                         "`y − 2 = (1/3)(x − 1)` gives `y = (1/3)x + 5/3`. Both pass "
                         "through `(1, 2)`, and `−3 × 1/3 = −1`.")),
            ("p", "Notice the shape of both answers: identify the required slope, then "
                  "hand it to lesson 5's point-slope form. Every question of this type "
                  "reduces to those two moves, and the only new content in this lesson "
                  "is how to get the slope."),
        ],
        "lab": ("line", {
            "mode": "parallel",
            "panel_title": "Two lines, one relationship",
            "panel_intro": "Change the first slope and the partner line updates to stay "
                           "parallel or perpendicular, with the product printed as an "
                           "exact fraction. Drive the first line towards vertical and "
                           "watch the product stop being computable.",
        }),
        "steps_title": "Finding a line through a point, parallel or perpendicular to a given line",
        "steps_intro": "Get the given slope, transform it, then it is lesson 5.",
        "steps": [
            ("Put the given line into slope-intercept form",
             "Solve for `y` and read `m`. If there is no `y` the given line is vertical "
             "&mdash; jump to the exception and answer `y = k` or `x = k` directly."),
            ("Decide the slope you need",
             "Parallel: the same `m`. Perpendicular: flip the fraction and change the "
             "sign. Do both operations, and say the new slope aloud before using it."),
            ("Use point-slope with the given point",
             "`y − y₁ = m(x − x₁)`. The point comes from the question and is not "
             "affected by which relationship was asked for."),
            ("Check the point and the relationship",
             "Substitute the point into your final equation, then confirm the slopes are "
             "equal, or that their product is `−1`. Two checks, because there are two "
             "ways to get this wrong."),
        ],
        "worked": {
            "title": "Through (1, 2), parallel and perpendicular to y = −3x + 7",
            "intro": ["The given line is already in slope-intercept form, so `m = −3` is "
                      "there to be read."],
            "lines": [
                "PARALLEL          required slope  m = -3",
                "     y - 2 = -3(x - 1)",
                "     y - 2 = -3x + 3",
                "         y = -3x + 5",
                "     check (1, 2):   -3(1) + 5 = 2      TRUE",
                "     check slopes:   -3 = -3            parallel",
                "",
                "PERPENDICULAR     required slope  m = -1/(-3) = 1/3",
                "     y - 2 = (1/3)(x - 1)",
                "     y - 2 = (1/3)x - 1/3",
                "         y = (1/3)x + 5/3",
                "     check (1, 2):   1/3 + 5/3 = 6/3 = 2    TRUE",
                "     check product:  -3 · 1/3 = -1          perpendicular",
                "",
                "the two answers are NOT parallel to each other, and both pass through (1, 2)",
            ],
            "after": [
                "The constant in the perpendicular case comes out as `2 − 1/3 = 5/3`. "
                "Fractions are the normal result here and rounding them to `1.67` throws "
                "away the exactness that made the check `6/3 = 2` conclusive.",
                "Both checks are worth doing. The point check catches an arithmetic slip "
                "in the simplification; the slope check catches having flipped without "
                "negating, which the point check would happily pass.",
            ],
        },
        "quiz_title": "Slopes compared",
        "quiz": [
            {"q": "What is the slope of a line perpendicular to `y = (2/5)x + 1`?",
             "a": ["`2/5`", "`5/2`", "`−5/2`", "`−2/5`"],
             "c": 2,
             "why": "Flip and negate: `2/5` becomes `−5/2`, and `(2/5)(−5/2) = −1`. "
                    "Option 2 flips without negating; option 4 negates without flipping."},
            {"q": "Are `y = 2x + 1` and `4x − 2y = 10` parallel?",
             "a": ["Yes &mdash; both have slope 2 and different intercepts",
                   "No &mdash; the second has slope 4",
                   "No &mdash; they are the same line",
                   "No &mdash; they are perpendicular"],
             "c": 0,
             "why": "`4x − 2y = 10` rearranges to `y = 2x − 5`. Same slope, and the "
                    "intercepts `1` and `−5` differ, so the lines are parallel and "
                    "distinct."},
            {"q": "Why does the product test fail to show that `x = 3` and `y = 4` are "
                  "perpendicular?",
             "a": ["They are not actually perpendicular",
                   "`x = 3` has no slope, so there is no product to form",
                   "Their slopes multiply to `0`, not `−1`",
                   "The test only works for lines through the origin"],
             "c": 1,
             "why": "They are perpendicular, but a vertical line has no slope at all. The "
                    "test is stated for lines that have slopes, and this pair falls "
                    "outside its scope rather than failing it."},
        ],
        "mistakes": [
            ("Flipping without negating, or negating without flipping",
             "Perpendicular to slope `3/4` is `−4/3`. `4/3` and `−3/4` are each half of "
             "the operation, and neither line is perpendicular to the original."),
            ("Calling two identical lines parallel",
             "`y = 2x + 1` and `2y = 4x + 2` have the same slope because they are the "
             "same line. Compare intercepts after comparing slopes, and say coincident "
             "when that is what they are."),
            ("Forcing the product rule onto a vertical line",
             "There is no number to multiply. Recognise the vertical line first: its "
             "perpendiculars are exactly the horizontal lines, and the answer needs no "
             "arithmetic."),
        ],
        "standard": ("Finish when you can produce the parallel and the perpendicular line "
                     "through a given point, and handle a vertical given line without "
                     "reaching for the formula.",
                     "Given four lines &mdash; one in standard form, one vertical, one "
                     "horizontal, one with a fractional slope &mdash; and a point, you "
                     "should produce both companions for each and justify the vertical "
                     "case in words. Knowing why the product test does not apply there is "
                     "the difference between using a theorem and reciting it."),
        "note": "Course 8 solves pairs of linear equations. The three possible outcomes "
                "there &mdash; one solution, none, or infinitely many &mdash; are exactly "
                "the three cases here: different slopes, equal slopes with different "
                "intercepts, and the same line twice. The algebra in that course is "
                "counting what this lesson sees.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "what-a-function-is",
        "title": "What a Function Is",
        "module": "Functions",
        "one_line": "Exactly one output for each input, and the test that checks it.",
        "summary": (
            "A function is a rule that assigns to each input exactly one output. The "
            "definition is short, the word doing the work is \"exactly\", and on a graph "
            "the whole condition can be checked by eye with the vertical line test."
        ),
        "key": [
            "each input  →  EXACTLY ONE output",
            "two inputs may share an output      (fine)",
            "one input with two outputs          (not a function)",
            "vertical line test:  no vertical line may cross twice",
        ],
        "key_label": "The definition, and what it does not forbid",
        "concepts_intro": (
            "Lessons 1 to 6 were about one particular shape. This lesson names the idea "
            "that organises every shape in the rest of the course."
        ),
        "concepts": [
            ("Exactly one means at least one and at most one",
             "The rule must produce an output for each input it claims to accept, and it "
             "must never produce two. Both halves can fail, and lesson 9 is largely "
             "about the first half."),
            ("Many-to-one is allowed; one-to-many is not",
             "`f(x) = x²` sends both `3` and `−3` to `9`, and that is a function. "
             "`y² = x` sends `4` to both `2` and `−2`, and that is not. The asymmetry is "
             "the definition, not a convention."),
            ("The vertical line test is the definition, drawn",
             "A vertical line is the set of points sharing one `x`. If it meets a graph "
             "twice, that single input has two outputs. The test is not a separate fact "
             "to remember &mdash; it is what the definition looks like on paper."),
        ],
        "read_title": "The definition and its test",
        "read_intro": "What must hold, what is permitted, and how to check each representation.",
        "body": [
            ("def", ("Function",
                     "A <strong>function</strong> from a set of inputs to a set of "
                     "outputs is a rule assigning to <em>each</em> input "
                     "<em>exactly one</em> output. The input set is the "
                     "<strong>domain</strong>; the outputs form the "
                     "<strong>range</strong>.")),
            ("p", "Every word is load-bearing. \"Each\" forbids an input the rule cannot "
                  "handle. \"Exactly one\" forbids an input with two answers. A rule that "
                  "fails either is not a function, and calling it one anyway breaks "
                  "everything downstream &mdash; notation in lesson 8 assumes `f(3)` "
                  "names a single number, and an inverse in lesson 13 assumes the "
                  "assignment can be run backwards."),
            ("h3", "What the definition permits"),
            ("p", "The asymmetry surprises people, so state it plainly: outputs may "
                  "repeat, inputs may not. Several inputs sharing one output is ordinary "
                  "and useful. One input with several outputs is a contradiction, because "
                  "then \"the\" output of that input does not exist."),
            ("math", [
                "f(x) = x^2                 x^2 + y^2 = 25",
                "",
                "   3  ->   9                 x = 3  ->  y = 4  AND  y = -4",
                "  -3  ->   9                 x = 0  ->  y = 5  AND  y = -5",
                "                             ",
                "  two inputs, one output     ONE input, two outputs",
                "  a function                 NOT a function",
            ]),
            ("p", "The circle is the clearest failure because it fails at almost every "
                  "input, not at some awkward exception. It is a perfectly good curve and "
                  "a perfectly good equation; it is simply not a function of `x`, which "
                  "is why the course notes list conic sections as out of scope."),
            ("h3", "The vertical line test"),
            ("thm", ("Vertical line test",
                     "A graph in the plane is the graph of a function of `x` if and only "
                     "if no vertical line meets it more than once. A vertical line "
                     "consists of all points with one fixed `x`, so two intersections are "
                     "exactly one input with two outputs.")),
            ("p", "This is where lesson 2's vertical line returns. The graph of `x = 5` "
                  "is itself a vertical line, so a vertical line meets it infinitely "
                  "often: the input `5` has every number as an output. Of all the lines "
                  "in this course, the vertical ones are precisely the non-functions "
                  "&mdash; which is the same exception that blocked slope in lesson 3 and "
                  "slope-intercept form in lesson 4, now explained rather than noted."),
            ("h3", "Checking the other representations"),
            ("ul", [
                "<strong>A table.</strong> Look for a repeated input with different "
                "outputs. A repeated output is irrelevant.",
                "<strong>A set of pairs.</strong> Same test: two pairs with the same "
                "first coordinate and different second coordinates disqualify it.",
                "<strong>An equation.</strong> Solve for `y` if you can. If solving "
                "forces a `±`, as with `y² = x`, the rule is not a function.",
                "<strong>A graph.</strong> The vertical line test.",
            ]),
            ("example", ("Six rules",
                         "`y = 2x + 1` function. `y = x²` function. `y = |x|` function, "
                         "since `|−7|` and `|7|` are both `7` and each input still gets "
                         "one output. `y² = x` not a function. `x = 5` not a function. "
                         "`x² + y² = 25` not a function.")),
            ("p", "One caution about the phrase \"function of `x`\". The circle fails as "
                  "a function of `x`, and the vertical line `x = 5` fails as a function "
                  "of `x` while being a perfectly good function of `y`. The test is "
                  "always relative to which variable is the input, and the vertical line "
                  "test presumes the usual choice of `x` across and `y` up."),
        ],
        "lab": ("funcops", {
            "mode": "definition",
            "panel_title": "Sweep the vertical line",
            "panel_intro": "Type a relation and drag the vertical line across it; the "
                           "lab counts intersections at each position and reports the "
                           "first input it finds with two outputs. Try `y^2 = x` and "
                           "`x^2 + y^2 = 25`.",
        }),
        "steps_title": "Deciding whether a rule is a function",
        "steps_intro": "Four questions, in this order. The first \"no\" settles it.",
        "steps": [
            ("Identify the input",
             "Usually `x`, but not always. Every later question depends on this choice, "
             "so make it explicit before testing anything."),
            ("Ask whether any input gets two outputs",
             "In a table, look for a repeated input. In an equation, solve for the output "
             "and watch for a `±` or an even root. On a graph, sweep a vertical line."),
            ("Ask whether any claimed input gets none",
             "A rule that says nothing about some input in its stated domain is not a "
             "function on that domain. Lesson 9 turns this into finding the domain."),
            ("If it fails, name the input that breaks it",
             "\"Not a function\" is half an answer. \"Not a function: `x = 4` gives both "
             "`2` and `−2`\" is the whole one, and it is the form that transfers to every "
             "later lesson."),
        ],
        "worked": {
            "title": "Six rules, classified with reasons",
            "intro": ["Give the verdict and the witness &mdash; the specific input that "
                      "breaks the rule, when there is one."],
            "lines": [
                "1.  y = 2x + 1          function       one output per x",
                "2.  y = x^2             function       -3 and 3 both give 9; allowed",
                "3.  y = |x|             function       -7 and 7 both give 7; allowed",
                "4.  y^2 = x             NOT            x = 4 gives y = 2 and y = -2",
                "5.  x = 5               NOT            x = 5 gives every y at once",
                "6.  x^2 + y^2 = 25      NOT            x = 3 gives y = 4 and y = -4",
                "",
                "and a table:",
                "     x  |  1   2   3   2                x = 2 appears twice,",
                "     y  |  5   7   9   8                with 7 and 8      NOT a function",
                "",
                "     x  |  1   2   3   4                every input once,",
                "     y  |  5   5   5   5                outputs repeat     function",
            ],
            "after": [
                "Lines 2 and 3 are the ones to dwell on. Both send two different inputs "
                "to one output, and both are functions. The rule constrains what leaves "
                "an input, not what arrives at an output.",
                "The two tables make the same point in the representation where it is "
                "easiest to misread. A repeated row of outputs looks suspicious and is "
                "fine; a repeated input is the only thing that disqualifies.",
            ],
        },
        "quiz_title": "Function or not",
        "quiz": [
            {"q": "Which of these is NOT a function of `x`?",
             "a": ["`y = x²`", "`y = |x|`", "`y² = x`", "`y = 2x + 1`"],
             "c": 2,
             "why": "`y² = x` gives two outputs at every positive input &mdash; `x = 4` "
                    "yields `y = 2` and `y = −2`. The first two send several inputs to "
                    "one output, which the definition permits."},
            {"q": "A table lists the pairs `(1, 5)`, `(2, 5)`, `(3, 5)`. Is it a function?",
             "a": ["No, the outputs repeat",
                   "Yes, each input has exactly one output",
                   "No, the range has only one element",
                   "Only if the inputs are consecutive"],
             "c": 1,
             "why": "Repeated outputs are permitted. Each of `1`, `2` and `3` is assigned "
                    "exactly one value, so this is a function &mdash; a constant one."},
            {"q": "Why is the vertical line test the right test?",
             "a": ["Vertical lines are the only lines with undefined slope",
                   "A vertical line collects all points with the same `x`, so two hits "
                   "means one input with two outputs",
                   "It is a convention that follows from the axes' orientation",
                   "It checks that the graph passes through the origin"],
             "c": 1,
             "why": "The test is the definition restated geometrically. Two intersections "
                    "are two points sharing an `x`-coordinate and differing in `y`, which "
                    "is precisely one input with two outputs."},
        ],
        "mistakes": [
            ("Thinking repeated outputs break the definition",
             "`y = x²` sends `3` and `−3` to `9` and is a function. Only a repeated "
             "<em>input</em> with different outputs disqualifies a rule."),
            ("Applying the horizontal line test to decide functionhood",
             "A horizontal line meeting a graph twice says the function is not one-to-one, "
             "which is a real property and the subject of lesson 13. It says nothing "
             "about whether the graph is a function."),
            ("Answering \"not a function\" without a witness",
             "Name the input that breaks it. Saying `x = 4` gives both `2` and `−2` is "
             "the answer that survives into lesson 9's domain work and lesson 13's "
             "restrictions; the bare verdict does not."),
        ],
        "standard": ("Finish when you can apply the definition to a rule in any of its "
                     "four representations and name the offending input whenever one "
                     "exists.",
                     "Given equations, tables, sets of pairs and graphs mixed together, "
                     "you should classify each and, for every failure, produce the input "
                     "with two outputs. This is the definition the remaining seven "
                     "lessons build on: notation, domain, transformation, composition and "
                     "inverse all presuppose that an input has one answer."),
        "note": "The definition explains an exception that has come up three times "
                "already. Vertical lines have no slope, cannot be written `y = mx + b`, "
                "and are not functions &mdash; all three because a single `x` is paired "
                "with many `y`. From lesson 8 onward everything in this course is a "
                "function, and that is why the notation `f(x)` is about to be safe to use.",
    },
]
