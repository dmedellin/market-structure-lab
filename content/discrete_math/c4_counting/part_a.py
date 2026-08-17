"""Course 4, lessons 01-07 — the basic rules and the binomial coefficients."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "sum-and-product-rules",
        "title": "The Sum and Product Rules",
        "module": "Basic counting",
        "one_line": "Add for alternatives, multiply for stages.",
        "summary": (
            "Two rules underlie all of counting. The sum rule handles disjoint "
            "alternatives; the product rule handles independent successive choices. "
            "Almost every error in this course is applying one where the other belongs."
        ),
        "key": [
            "SUM      disjoint alternatives:      |A ∪ B| = |A| + |B|   when A ∩ B = ∅",
            "PRODUCT  successive choices:         |A × B| = |A| · |B|",
            "\"or\"  usually means add.    \"and then\"  usually means multiply.",
            "The sum rule REQUIRES disjointness. Check it.",
        ],
        "key_label": "Two rules, one distinction",
        "concepts_intro": (
            "The arithmetic is trivial. Deciding which rule applies is the entire "
            "content of the lesson."
        ),
        "concepts": [
            ("The sum rule needs disjointness",
             "`|A ∪ B| = |A| + |B|` only when nothing is in both. Overlap means "
             "double-counting, and lesson 9 is the general repair."),
            ("The product rule needs independence of counts",
             "The number of second choices must not depend on which first choice was "
             "made. The number itself may vary if it varies uniformly &mdash; but then "
             "say so."),
            ("Most problems combine both",
             "Split into disjoint cases (sum), count each by stages (product), and add. "
             "That template solves most of this course."),
        ],
        "read_title": "The two rules",
        "read_intro": "Statements, the conditions they need, and how they combine.",
        "body": [
            ("thm", ("Sum rule",
                     "If a task can be done in one of `n₁` ways or in one of `n₂` ways, "
                     "and the two sets of ways are <strong>disjoint</strong>, then there "
                     "are `n₁ + n₂` ways to do it. For `k` pairwise disjoint sets, "
                     "`|A₁ ∪ ⋯ ∪ A_k| = |A₁| + ⋯ + |A_k|`.")),
            ("thm", ("Product rule",
                     "If a task consists of two successive choices, with `n₁` ways to make "
                     "the first and, for each of those, `n₂` ways to make the second, then "
                     "there are `n₁n₂` ways in total. For `k` stages the count is the "
                     "product of the stage counts.")),
            ("p", "The product rule is where `|A × B| = |A| · |B|` came from in course 2, "
                  "and where truth tables get their `2ⁿ` rows: `n` successive independent "
                  "binary choices."),
            ("example", ("Both rules in one problem",
                         "How many strings of length 3 over `{a,…,z}` start with a vowel or "
                         "end with `z`? Vowel first: `5 · 26 · 26 = 3380`. Ending `z`: "
                         "`26 · 26 · 1 = 676`. These overlap &mdash; strings starting with "
                         "a vowel AND ending in `z`, of which there are `5 · 26 · 1 = 130`. "
                         "So the answer is `3380 + 676 − 130 = 3926`, not `4056`.")),
            ("p", "That subtraction is lesson 9 arriving early. The sum rule as stated does "
                  "not apply, because the two sets are not disjoint; using it anyway "
                  "over-counts by exactly the size of the overlap."),
            ("h3", "When the second count depends on the first"),
            ("p", "The product rule is often stated as needing \"independent\" choices, "
                  "which is imprecise. What it needs is that the <em>number</em> of second "
                  "choices is the same whichever first choice was made. Choosing an ordered "
                  "pair of distinct letters has 26 first choices and 25 second ones "
                  "&mdash; the second count is 25 regardless of the first &mdash; so the "
                  "product rule applies and gives 650."),
            ("p", "When the count genuinely varies, split into cases and use the sum rule "
                  "on the cases. That is the standard repair and it is what makes the two "
                  "rules a complete toolkit rather than two heuristics."),
            ("h3", "Complementary counting"),
            ("thm", ("Counting the complement",
                     "`|A| = |U| − |Ā|`. When the objects satisfying a condition are hard "
                     "to count and those failing it are easy, count the failures.")),
            ("example", ("At least one",
                         "How many 4-digit PINs contain at least one 7? Directly this needs "
                         "cases for one, two, three or four sevens. By complement: all PINs "
                         "number `10⁴ = 10000`, and those with no 7 number `9⁴ = 6561`, so "
                         "the answer is `3439`. \"At least one\" is almost always a signal "
                         "to count the complement.")),
        ],
        "lab": ("counting", {
            "n": 5, "r": 3, "rule": "pr",
            "panel_title": "The product rule, enumerated",
            "panel_intro": "The `nʳ` row is the product rule applied `r` times. The list "
                           "below shows every selection, so the formula can be checked "
                           "rather than trusted.",
        }),
        "steps_title": "Choosing a rule",
        "steps_intro": "Ask two questions before writing any arithmetic.",
        "steps": [
            ("Are these alternatives or stages?",
             "\"Either… or…\" suggests the sum rule; \"first… then…\" suggests the "
             "product rule. Most problems have both, nested."),
            ("If alternatives: are they disjoint?",
             "If an object could be counted in two cases, the sum rule over-counts. Fix "
             "the cases or use lesson 9."),
            ("If stages: does the second count vary?",
             "It must be the same number for every first choice. If not, split into cases "
             "where it is constant."),
            ("Consider the complement",
             "\"At least one\", \"not all\" and \"at least two\" usually count more easily "
             "as total minus failures."),
        ],
        "worked": {
            "title": "Passwords",
            "intro": ["Length 6 to 8, from 26 letters and 10 digits, containing at least one digit."],
            "lines": [
                "Alphabet size 36.  Split by LENGTH — disjoint, so add.",
                "",
                "length 6:   36⁶ − 26⁶ =  2 176 782 336 −    308 915 776 =  1 867 866 560",
                "length 7:   36⁷ − 26⁷ = 78 364 164 096 −  8 031 810 176 = 70 332 353 920",
                "length 8:   36⁸ − 26⁸ = 2 821 109 907 456 − 208 827 064 576",
                "                                                       = 2 612 282 842 880",
                "",
                "total = 1 867 866 560 + 70 332 353 920 + 2 612 282 842 880",
                "      = 2 684 483 063 360",
            ],
            "after": [
                "Two rules, each used once. The sum rule handled the three lengths, which "
                "are disjoint because a password has exactly one length; complementary "
                "counting handled \"at least one digit\" within each length. Counting the "
                "digit-containing passwords directly would need eight overlapping cases."
            ],
        },
        "quiz_title": "Sum and product",
        "quiz": [
            {"q": "A menu has 4 starters and 5 mains. How many two-course meals?",
             "a": ["9", "20", "10", "45"],
             "c": 1,
             "why": "Two successive choices, so the product rule: `4 · 5 = 20`. Adding "
                    "would answer \"how many single dishes are available\"."},
            {"q": "The sum rule requires:",
             "a": ["the sets to be the same size",
                   "the sets to be disjoint",
                   "the sets to be finite and ordered",
                   "nothing"],
             "c": 1,
             "why": "Overlap is counted twice. When the sets are not disjoint the "
                    "inclusion&ndash;exclusion principle of lesson 9 is the correct rule."},
            {"q": "How many 3-digit strings over `{0,…,9}` contain at least one 5?",
             "a": ["100", "271", "300", "243"],
             "c": 1,
             "why": "`10³ − 9³ = 1000 − 729 = 271`. Counting directly needs cases for one, "
                    "two and three fives, and they must not overlap."},
        ],
        "mistakes": [
            ("Adding when the cases overlap",
             "The over-count equals the size of the intersection. Either redefine the "
             "cases to be disjoint or subtract the overlap explicitly."),
            ("Multiplying when the second count varies",
             "If the number of second choices depends on the first, split into cases where "
             "it does not, then add."),
            ("Counting \"at least one\" directly",
             "It almost always produces overlapping cases. Total minus none is one "
             "subtraction and cannot double-count."),
        ],
        "standard": ("Finish when you state the rule and its condition before computing.",
                     "Count the 4-digit PINs with at least two identical digits. Do it by "
                     "complement, and say in one sentence why the direct count would be "
                     "harder. That sentence is the skill."),
        "note": "Both rules are theorems about sets: the sum rule is additivity of "
                "cardinality over disjoint unions, and the product rule is "
                "`|A × B| = |A| · |B|` from course 2 lesson 5. Counting is set theory with "
                "the sets kept small enough to measure.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "counting-with-restrictions",
        "title": "Counting with Restrictions",
        "module": "Basic counting",
        "one_line": "Cases, complements, and the order in which constraints are applied.",
        "summary": (
            "Restrictions make counting harder in a specific way: they break the product "
            "rule's uniformity. Three techniques repair it &mdash; apply the constraint "
            "first, split into cases, or count the complement."
        ),
        "key": [
            "Place the CONSTRAINED positions first.",
            "Split into cases where the counts are uniform, then add.",
            "\"at least one\" → count the complement",
            "Check: do the cases overlap? do they cover everything?",
        ],
        "key_label": "Three repairs",
        "concepts_intro": (
            "A restriction is a place where the product rule stops applying directly. "
            "Each technique restores it."
        ),
        "concepts": [
            ("Handle the constrained choice first",
             "If the first digit cannot be 0, choose it first (9 ways) and then the rest "
             "freely. Choosing left to right regardless is what creates the difficulty."),
            ("Split into cases when the count varies",
             "Cases must be disjoint and exhaustive &mdash; the same discipline as a proof "
             "by cases in course 1 lesson 14."),
            ("Complement when the restriction says \"at least\"",
             "The complement of \"at least one\" is \"none\", which is a single "
             "unrestricted count."),
        ],
        "read_title": "Working with restrictions",
        "read_intro": "The three techniques, each on an example where it is clearly the right one.",
        "body": [
            ("h3", "Constrain first"),
            ("example", ("Leading digit",
                         "How many 4-digit numbers are there? The first digit cannot be 0, "
                         "so choose it first: 9 ways, then `10 · 10 · 10` for the rest, "
                         "giving 9000. Working left to right without noticing the "
                         "restriction gives `10⁴` and counts `0123` as a four-digit number.")),
            ("example", ("Two constraints at once",
                         "Four-digit numbers, first digit nonzero and last digit even. "
                         "Constrain both ends first: 9 choices for the first, 5 for the "
                         "last, then `10 · 10` in the middle &mdash; `9 · 10 · 10 · 5 = "
                         "4500`. Order of consideration is free; order of positions is not.")),
            ("h3", "Split into cases"),
            ("example", ("A constraint that interacts",
                         "Four-digit numbers with first digit nonzero and all digits "
                         "distinct. Constrain first: 9 choices for the leading digit. The "
                         "second digit may be anything except the first, including 0, so "
                         "9 choices; then 8; then 7. Total `9 · 9 · 8 · 7 = 4536`. Note "
                         "the second count is 9 and not 8 &mdash; 0 becomes available "
                         "exactly because it was excluded from the first position.")),
            ("p", "Where two restrictions genuinely interact, cases are unavoidable. "
                  "Count the strings of length 4 over `{a, b, c}` with at least two `a`s: "
                  "split by the number of `a`s &mdash; exactly two, exactly three, exactly "
                  "four &mdash; count each, and add. The cases are disjoint because a "
                  "string has one definite number of `a`s."),
            ("h3", "Complement"),
            ("example", ("At least one repeat",
                         "How many 5-digit PINs have at least one repeated digit? All PINs: "
                         "`10⁵ = 100000`. All-distinct PINs: `10 · 9 · 8 · 7 · 6 = 30240`. "
                         "Answer `69760`. The direct count would need cases for one pair, "
                         "two pairs, a triple, and so on &mdash; overlapping and easy to "
                         "get wrong.")),
            ("p", "The general signal: if the condition is \"at least\" something, or "
                  "\"not all\", or \"some\", the complement is usually a single clean count. "
                  "If it is \"exactly\", cases are usually right."),
            ("h3", "Checking the answer"),
            ("ul", [
                "<strong>Do the cases overlap?</strong> If an object satisfies two, it was "
                "counted twice.",
                "<strong>Do the cases cover everything?</strong> A missing case is an "
                "undercount that never announces itself.",
                "<strong>Does a small instance check out?</strong> Shrink `n` until you can "
                "enumerate by hand and compare with the formula. The lab does this to 400 "
                "objects.",
            ]),
        ],
        "lab": ("counting", {
            "n": 4, "r": 3, "rule": "p",
            "panel_title": "Distinct selections, listed",
            "panel_intro": "The `P(n, r)` row counts ordered selections without repetition "
                           "&mdash; the \"all digits distinct\" pattern. The enumeration "
                           "below is what a restriction count should be checked against.",
        }),
        "steps_title": "Handling a restriction",
        "steps_intro": "Identify what the restriction breaks, then choose the repair.",
        "steps": [
            ("Locate the constrained positions",
             "Deal with them first so the remaining choices are uniform. This alone "
             "handles most restrictions."),
            ("If the counts still vary, split into cases",
             "Choose the case variable so that within each case the product rule applies "
             "cleanly."),
            ("If the condition is \"at least\", complement",
             "Total minus the objects failing the condition. One subtraction, no overlap."),
            ("Verify on a small instance",
             "Shrink the parameters until enumeration is possible and compare. A formula "
             "that disagrees with a list is wrong."),
        ],
        "worked": {
            "title": "Committees with a constraint",
            "intro": ["From 6 women and 5 men, choose a committee of 4 with at least one of each."],
            "lines": [
                "Total committees of 4 from 11 people:      C(11,4) = 330",
                "",
                "COMPLEMENT: the committees that FAIL the condition are the",
                "all-women and all-men ones.",
                "",
                "   all women:   C(6,4) = 15",
                "   all men:     C(5,4) =  5",
                "   these are disjoint (a committee of 4 cannot be both)",
                "",
                "   330 − 15 − 5 = 310",
                "",
                "CHECK BY CASES: 1W3M + 2W2M + 3W1M",
                "   C(6,1)C(5,3) + C(6,2)C(5,2) + C(6,3)C(5,1)",
                " = 6·10 + 15·10 + 20·5  =  60 + 150 + 100  =  310         agree",
            ],
            "after": [
                "Two independent routes to 310. That agreement is the real check: a single "
                "method producing a plausible number is not evidence that the classification "
                "was right, and the case method is where a missing case would show up."
            ],
        },
        "quiz_title": "Restrictions",
        "quiz": [
            {"q": "How many 4-digit numbers have all digits distinct?",
             "a": ["5040", "4536", "10000", "9000"],
             "c": 1,
             "why": "First digit nonzero: 9 choices. Second: 9 (anything but the first, "
                    "and 0 is now allowed). Then 8, then 7. `9 · 9 · 8 · 7 = 4536`."},
            {"q": "\"At least one\" conditions are usually counted by:",
             "a": ["listing cases", "the complement", "the product rule", "induction"],
             "c": 1,
             "why": "The complement is \"none\", which is a single unrestricted count. "
                    "Direct cases overlap and multiply quickly."},
            {"q": "Two counting cases overlap. The result is:",
             "a": ["an undercount", "an over-count", "correct", "undefined"],
             "c": 1,
             "why": "Objects in both cases are counted twice, so the total is too large. "
                    "A missing case would undercount."},
        ],
        "mistakes": [
            ("Ignoring the leading-digit restriction",
             "`10⁴` counts `0123` as a four-digit number. Constrained positions get chosen "
             "first for exactly this reason."),
            ("Forgetting that excluding a value from one position frees it for another",
             "After choosing a nonzero first digit, the second digit has 9 options, not 8: "
             "0 has become available."),
            ("Cases that overlap or leave a gap",
             "Both errors are silent. Check the cases sum to the unrestricted total when "
             "the restriction is removed."),
        ],
        "standard": ("Finish when you check a restricted count two ways.",
                     "Count the 5-letter strings over `{a,…,e}` containing at least one "
                     "`a`, by complement and by cases on the number of `a`s. If the two "
                     "agree you have both the arithmetic and the classification right."),
        "note": "The instinct to count what you want directly is usually the expensive "
                "one. Complementary counting, and later inclusion and exclusion, both "
                "amount to counting something easier and correcting &mdash; which is the "
                "dominant strategy in this course.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "permutations",
        "title": "Permutations",
        "module": "Arrangements",
        "one_line": "Ordered selections without repetition.",
        "summary": (
            "`P(n, r) = n!/(n−r)!` counts the ways to arrange `r` of `n` distinct objects "
            "in order. Factorials grow explosively, and that growth is a fact about the "
            "problem rather than about the notation."
        ),
        "key": [
            "P(n, r) = n(n−1)⋯(n−r+1) = n!/(n−r)!",
            "P(n, n) = n!                  all n objects arranged",
            "0! = 1                        the empty arrangement",
            "circular arrangements of n:   (n−1)!",
        ],
        "key_label": "Ordered, no repetition",
        "concepts_intro": (
            "The product rule with a shrinking pool of choices. Everything else is "
            "notation."
        ),
        "concepts": [
            ("Each choice removes one option",
             "`n` ways for the first position, `n−1` for the second, and so on for `r` "
             "positions. That product is `P(n, r)`."),
            ("`0! = 1` is a convention that works",
             "It makes `P(n, n) = n!/0! = n!` come out right and keeps every formula in "
             "this course free of special cases."),
            ("Factorial growth is genuinely enormous",
             "`52!` is about `8 × 10⁶⁷`. Every shuffle of a deck that has ever been "
             "performed was almost certainly unique."),
        ],
        "read_title": "Arrangements",
        "read_intro": "The formula, its derivation, and two variants worth knowing.",
        "body": [
            ("def", ("Permutation",
                     "A <strong>permutation</strong> of a set is an ordered arrangement of "
                     "its elements. An <strong>`r`-permutation</strong> is an ordered "
                     "arrangement of `r` of them.")),
            ("thm", ("Counting `r`-permutations",
                     "For `0 ≤ r ≤ n`, `P(n, r) = n(n−1)(n−2)⋯(n−r+1) = n!/(n−r)!`.")),
            ("proof", [
                "Fill the `r` positions in order. The first has `n` candidates. Whatever "
                "was chosen, the second has `n−1` remaining, the third `n−2`, and the "
                "`r`th has `n−r+1`. The number of options at each stage does not depend on "
                "which particular objects were chosen earlier, so the product rule applies.",
            ]),
            ("p", "Note the count of factors: `r` of them, running from `n` down to "
                  "`n−r+1`. Writing `n` down to `n−r` is the standard off-by-one, and it "
                  "gives `P(n, r+1)`."),
            ("example", ("Podium finishes",
                         "Ten runners, how many ways to fill gold, silver and bronze? "
                         "`P(10,3) = 10 · 9 · 8 = 720`. Order matters here &mdash; the same "
                         "three runners in a different order is a different outcome &mdash; "
                         "which is exactly what makes it a permutation rather than a "
                         "combination.")),
            ("h3", "Circular arrangements"),
            ("thm", ("Arrangements around a circle",
                     "`n` distinct objects can be arranged in a circle in `(n−1)!` ways, "
                     "when rotations are considered identical.")),
            ("proof", [
                "There are `n!` linear arrangements. Each circular arrangement corresponds "
                "to exactly `n` of them, one for each choice of which object is written "
                "first. So the circular count is `n!/n = (n−1)!`.",
                "Equivalently: fix one object's position to break the rotational symmetry, "
                "and arrange the remaining `n−1` freely.",
            ]),
            ("p", "The division-by-symmetry argument is the pattern to remember: when "
                  "several arrangements are considered the same, count them all and divide "
                  "by the size of the equivalence class. That is course 2's equivalence "
                  "relation doing combinatorial work, and lesson 7 uses it again."),
            ("h3", "The size of factorials"),
            ("math", [
                "  5! =                        120",
                " 10! =                  3 628 800",
                " 20! =  2 432 902 008 176 640 000",
                " 52! ≈ 8.07 × 10⁶⁷",
            ]),
            ("p", "`52!` exceeds the number of atoms in the Milky Way. Any algorithm that "
                  "examines all permutations of a modest input is not slow &mdash; it is "
                  "impossible, and course 8 lesson 11 gives that observation a name."),
        ],
        "lab": ("counting", {
            "n": 5, "r": 3, "rule": "p",
            "panel_title": "Permutations, listed",
            "panel_intro": "The P row is highlighted. Raise `n` past 20 and the "
                           "enumeration stops while the count stays exact &mdash; it is "
                           "computed in big integers, not floating point.",
        }),
        "steps_title": "Counting arrangements",
        "steps_intro": "Confirm order matters before reaching for the formula.",
        "steps": [
            ("Check that order matters",
             "If rearranging the same objects gives a different outcome, it is a "
             "permutation. If not, lesson 4 has the right formula."),
            ("Check that repetition is forbidden",
             "Objects are drawn without replacement. If they may repeat, lesson 7 applies "
             "and the answer is `nʳ`."),
            ("Count the factors",
             "`P(n, r)` has exactly `r` factors, ending at `n−r+1`. Miscounting them is "
             "the standard error."),
            ("Divide out any symmetry",
             "Circular seating divides by `n`; a necklace that may be flipped divides by "
             "`2n`. Name the symmetry before dividing."),
        ],
        "worked": {
            "title": "Seating with a constraint",
            "intro": ["Eight people at a round table; two of them must sit together."],
            "lines": [
                "Unrestricted circular arrangements:  (8−1)! = 5040",
                "",
                "Treat the pair as a single block:",
                "   7 items around a circle:   (7−1)! = 720",
                "   the pair can be in 2 internal orders:  × 2",
                "   ⟹  1440 arrangements with the two together",
                "",
                "With the two apart:  5040 − 1440 = 3600",
                "",
                "Check: 1440 / 5040 = 2/7, and indeed with 7 other seats adjacent",
                "to a fixed person, 2 of them are next to that person.",
            ],
            "after": [
                "The block trick &mdash; glue constrained objects together, count, then "
                "multiply by their internal arrangements &mdash; is the standard device for "
                "\"must be adjacent\" constraints. The final ratio check is cheap and "
                "catches an error in the block count immediately."
            ],
        },
        "quiz_title": "Permutations",
        "quiz": [
            {"q": "`P(7, 3)` equals:",
             "a": ["21", "35", "210", "5040"],
             "c": 2,
             "why": "`7 · 6 · 5 = 210`. Three factors, starting at 7. `C(7,3) = 35` is the "
                    "unordered count."},
            {"q": "Why is `0! = 1`?",
             "a": ["By convention, and it makes `P(n,n) = n!` come out right",
                   "Because 0 has one factor", "It is undefined", "Because `1! = 1`"],
             "c": 0,
             "why": "It is the empty product, and it removes special cases from every "
                    "formula in this course &mdash; `C(n,0) = 1` depends on it too."},
            {"q": "Five people around a round table can be seated in:",
             "a": ["`5! = 120` ways", "`4! = 24` ways", "`5⁵` ways", "`P(5,5)/5!` ways"],
             "c": 1,
             "why": "Rotations are the same arrangement, so divide `5!` by 5, giving "
                    "`4! = 24`. Equivalently, fix one person and arrange the other four."},
        ],
        "mistakes": [
            ("Using `P` when order does not matter",
             "A committee of three is not an ordered triple. `P(n,r)` counts each "
             "committee `r!` times, which is exactly the relationship lesson 4 exploits."),
            ("Miscounting the factors",
             "`P(n, r)` runs from `n` down to `n − r + 1`, which is `r` factors. Ending at "
             "`n − r` gives one too many."),
            ("Forgetting to divide out a symmetry",
             "Circular arrangements, necklaces and identical items all require dividing by "
             "the size of the symmetry class. Naming the symmetry first prevents dividing "
             "by the wrong number."),
        ],
        "standard": ("Finish when you can justify the divisor in a symmetry argument.",
                     "Count the ways to seat 6 people around a round table with two "
                     "specific people not adjacent. Do it by complement, and state exactly "
                     "why the circular count is `5!` rather than `6!`."),
        "note": "A permutation is also a bijection from a set to itself, which is course 2 "
                "lesson 12's remark. There are `n!` of them, and under composition they "
                "form the symmetric group &mdash; the object most of finite group theory "
                "is about.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "combinations",
        "title": "Combinations",
        "module": "Arrangements",
        "one_line": "Unordered selections without repetition.",
        "summary": (
            "`C(n, r) = n!/(r!(n−r)!)` counts subsets of size `r`. It is `P(n, r)` "
            "divided by `r!`, because each subset was counted once for every order of "
            "its elements."
        ),
        "key": [
            "C(n, r) = P(n, r)/r! = n!/(r!(n−r)!)",
            "C(n, r) = C(n, n−r)          symmetry: choosing r is leaving n−r",
            "C(n, 0) = C(n, n) = 1",
            "Σ_r C(n, r) = 2ⁿ             all subsets",
        ],
        "key_label": "Unordered, no repetition",
        "concepts_intro": (
            "One formula, derived from permutations by dividing out the orderings that "
            "do not matter."
        ),
        "concepts": [
            ("Divide by `r!` to forget the order",
             "Each `r`-subset arises from exactly `r!` ordered selections, so "
             "`C(n,r) = P(n,r)/r!`."),
            ("Symmetry is obvious once seen",
             "Choosing which `r` to include is the same as choosing which `n−r` to leave "
             "out, so `C(n,r) = C(n,n−r)`."),
            ("The subsets sum to `2ⁿ`",
             "Every subset has exactly one size, so summing `C(n,r)` over all `r` counts "
             "every subset once &mdash; and course 2 lesson 2 already knew the total."),
        ],
        "read_title": "Choosing without order",
        "read_intro": "The derivation, the identities, and the standard applications.",
        "body": [
            ("def", ("Combination",
                     "An <strong>`r`-combination</strong> of a set is a subset of size "
                     "`r`. The number of them is written `C(n, r)` or `binom(n, r)` and "
                     "read \"`n` choose `r`\".")),
            ("thm", ("Counting combinations",
                     "`C(n, r) = P(n, r)/r! = n!/(r!(n−r)!)` for `0 ≤ r ≤ n`.")),
            ("proof", [
                "Count ordered selections of `r` distinct objects in two ways. Directly "
                "there are `P(n, r)` of them.",
                "Alternatively, choose which `r` objects to use (`C(n, r)` ways) and then "
                "arrange them (`r!` ways), giving `C(n, r) · r!`.",
                "The two counts are of the same set, so `P(n, r) = C(n, r) · r!`, and "
                "dividing gives the formula.",
            ]),
            ("p", "That proof is a <em>double count</em>: one set counted two ways, and the "
                  "two expressions therefore equal. Lesson 13 makes the technique explicit; "
                  "it appears here because it is the cleanest derivation of the formula."),
            ("thm", ("Symmetry",
                     "`C(n, r) = C(n, n−r)`.")),
            ("proof", [
                "The map sending a subset to its complement is a bijection between the "
                "`r`-subsets and the `(n−r)`-subsets: it is injective because a set is "
                "determined by its complement, and surjective because every "
                "`(n−r)`-subset is the complement of its own complement.",
            ]),
            ("p", "The bijective proof is better than the algebraic one, which merely "
                  "observes that the formula is symmetric in `r` and `n−r`. A bijection "
                  "says <em>why</em>: the two collections are the same objects, described "
                  "from opposite sides."),
            ("thm", ("Sum over all sizes",
                     "`Σ_{r=0}^{n} C(n, r) = 2ⁿ`.")),
            ("proof", [
                "Count the subsets of an `n`-set two ways. By size: `C(n, r)` of each size "
                "`r`, and every subset has exactly one size, so the total is the sum. "
                "Directly: each element is independently in or out, giving `2ⁿ`.",
            ]),
            ("example", ("Poker hands",
                         "A 5-card hand from 52 is `C(52,5) = 2 598 960`, since the order "
                         "cards arrive in does not matter. Hands containing all four aces: "
                         "choose the four aces (1 way) and one more card from 48, giving 48. "
                         "So the probability is `48/2598960 ≈ 0.0000185` &mdash; course 5 "
                         "makes that division legitimate.")),
            ("example", ("Lattice paths",
                         "Paths from `(0,0)` to `(m,n)` using unit steps right and up: each "
                         "path is a sequence of `m + n` steps of which `m` are right, so "
                         "there are `C(m+n, m)` of them. Choosing which steps are right "
                         "determines the path completely.")),
        ],
        "lab": ("counting", {
            "n": 6, "r": 3, "rule": "c",
            "panel_title": "Combinations, listed",
            "panel_intro": "Compare the C row with the P row above it: the ratio is "
                           "exactly `r!`, which is the derivation of the formula made "
                           "visible.",
        }),
        "steps_title": "Recognising a combination",
        "steps_intro": "Order and repetition, in that order.",
        "steps": [
            ("Ask whether order matters",
             "Committees, hands and subsets: no. Podiums, passwords and sequences: yes. "
             "This one question separates lessons 3 and 4."),
            ("Ask whether repetition is allowed",
             "If objects may be chosen more than once, lesson 8 applies instead."),
            ("Use symmetry to simplify",
             "`C(20,18) = C(20,2) = 190`. Computing the smaller side is faster and less "
             "error-prone."),
            ("Check with a small case",
             "`C(4,2) = 6` should match the six pairs you can list. The lab does this "
             "automatically up to 400 selections."),
        ],
        "worked": {
            "title": "Committees with structure",
            "intro": ["From 8 mathematicians and 6 physicists, choose 5 with at least 3 mathematicians."],
            "lines": [
                "Cases by the number of mathematicians — disjoint and exhaustive:",
                "",
                "   3 maths, 2 physicists:  C(8,3)·C(6,2) =  56 · 15 =  840",
                "   4 maths, 1 physicist:   C(8,4)·C(6,1) =  70 ·  6 =  420",
                "   5 maths, 0 physicists:  C(8,5)·C(6,0) =  56 ·  1 =   56",
                "",
                "   total = 840 + 420 + 56 = 1316",
                "",
                "Sanity check:  total committees of 5 from 14 is C(14,5) = 2002,",
                "and 1316 < 2002.   ✓",
            ],
            "after": [
                "Within each case the product rule applies because the two choices are "
                "independent: which mathematicians are chosen does not change how many "
                "ways the physicists can be. The sum rule then combines the cases, which "
                "are disjoint because a committee has one definite composition."
            ],
        },
        "quiz_title": "Combinations",
        "quiz": [
            {"q": "`C(10, 3)` equals:",
             "a": ["30", "120", "720", "1000"],
             "c": 1,
             "why": "`10·9·8 / 3! = 720/6 = 120`. The 720 is `P(10,3)`, which counts each "
                    "subset six times."},
            {"q": "Why is `C(n, r) = C(n, n−r)`?",
             "a": ["The formula is symmetric",
                   "Choosing which `r` to include is choosing which `n−r` to exclude — a bijection",
                   "Both equal `2ⁿ`",
                   "It is only true for even `n`"],
             "c": 1,
             "why": "The complement map is a bijection between the two collections. The "
                    "algebraic symmetry is a consequence, not the reason."},
            {"q": "How many 5-card hands can be dealt from 52 cards?",
             "a": ["`P(52,5)`", "`C(52,5) = 2 598 960`", "`52⁵`", "`5! · C(52,5)`"],
             "c": 1,
             "why": "A hand is a set of cards; the order they were dealt in is not part of "
                    "the hand. `P(52,5)` counts each hand `5! = 120` times."},
        ],
        "mistakes": [
            ("Using `C` where order matters",
             "A three-digit code is not a three-element subset. Ask what makes two "
             "outcomes different before choosing a formula."),
            ("Adding when the choices are simultaneous",
             "\"3 mathematicians AND 2 physicists\" is a product within a case. The sum "
             "rule combines the cases, not the parts of one case."),
            ("Computing the large side of a symmetric coefficient",
             "`C(30,28)` is `C(30,2) = 435`, which is two multiplications rather than "
             "twenty-eight."),
        ],
        "standard": ("Finish when you can state, for any counting problem, whether order "
                     "and repetition matter.",
                     "Take five problems from anywhere in this lesson and classify each "
                     "before computing. The classification is the part that transfers; the "
                     "arithmetic is not."),
        "note": "`C(n, r)` is also written `binom(n, r)` and called a binomial coefficient, "
                "because lesson 6 shows it is the coefficient of `x^r y^{n−r}` in "
                "`(x + y)ⁿ`. The two facts &mdash; counting subsets and expanding a power "
                "&mdash; are the same fact.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "binomial-coefficients",
        "title": "Binomial Coefficients and Pascal's Triangle",
        "module": "Binomial coefficients",
        "one_line": "The numbers `C(n, r)`, arranged so their identities become visible.",
        "summary": (
            "Pascal's rule builds each entry from the two above it, and the resulting "
            "triangle displays symmetry, the row sums, the hockey stick and several "
            "other identities &mdash; each with a counting proof."
        ),
        "key": [
            "Pascal's rule   C(n,k) = C(n−1,k−1) + C(n−1,k)",
            "symmetry        C(n,k) = C(n,n−k)",
            "row sum         Σ_k C(n,k) = 2ⁿ",
            "hockey stick    Σ_{i=k}^{n} C(i,k) = C(n+1,k+1)",
        ],
        "key_label": "Four identities, all provable by counting",
        "concepts_intro": (
            "Every identity in this lesson has a counting proof that is shorter and more "
            "illuminating than the algebra."
        ),
        "concepts": [
            ("Pascal's rule is a case split",
             "Count the `k`-subsets of an `n`-set by whether they contain a fixed element. "
             "Those that do, and those that do not, are exactly the two terms."),
            ("Row sums are the power set",
             "Summing across a row counts every subset once, which course 2 already showed "
             "is `2ⁿ`."),
            ("The triangle is a computation, not a picture",
             "Pascal's rule gives every entry from the previous row using only addition, "
             "which is how the values are produced without factorials."),
        ],
        "read_title": "The triangle and its identities",
        "read_intro": "Pascal's rule first, then the identities it generates.",
        "body": [
            ("thm", ("Pascal's rule",
                     "For `1 ≤ k ≤ n−1`, `C(n,k) = C(n−1,k−1) + C(n−1,k)`.")),
            ("proof", [
                "Fix an element `x` of an `n`-set and count the `k`-subsets by whether they "
                "contain `x`.",
                "Those containing `x` are determined by the other `k−1` elements, chosen "
                "from the remaining `n−1`: `C(n−1, k−1)` of them.",
                "Those not containing `x` are `k`-subsets of the other `n−1` elements: "
                "`C(n−1, k)` of them.",
                "The two classes are disjoint and cover everything, so the sum rule gives "
                "the identity.",
            ]),
            ("p", "That is a two-line proof of a fact whose algebraic verification requires "
                  "combining fractions with factorials. The pattern &mdash; split on "
                  "whether a fixed element is included &mdash; recurs throughout the course."),
            ("math", [
                "n=0                     1",
                "n=1                   1   1",
                "n=2                 1   2   1",
                "n=3               1   3   3   1",
                "n=4             1   4   6   4   1",
                "n=5           1   5  10  10   5   1",
                "n=6         1   6  15  20  15   6   1",
            ]),
            ("thm", ("Row sum",
                     "`Σ_{k=0}^{n} C(n,k) = 2ⁿ`: every row of the triangle sums to a power "
                     "of two.")),
            ("thm", ("Alternating row sum",
                     "For `n ≥ 1`, `Σ_{k=0}^{n} (−1)^k C(n,k) = 0`: a set with at least one "
                     "element has exactly as many even-sized subsets as odd-sized ones.")),
            ("proof", [
                "Fix an element `x`. Pairing each subset containing `x` with the same "
                "subset minus `x` matches every subset with one of the opposite parity, "
                "and this pairing is a bijection. So the two counts are equal.",
                "For `n = 0` the identity fails: the empty set has one subset, of even "
                "size, and there is no `x` to pair with.",
            ]),
            ("thm", ("Hockey stick",
                     "`Σ_{i=k}^{n} C(i,k) = C(n+1, k+1)`.")),
            ("proof", [
                "Count the `(k+1)`-subsets of `{1, …, n+1}` by their largest element. If "
                "the largest is `i+1`, the remaining `k` elements come from `{1, …, i}`, "
                "giving `C(i, k)` such subsets. Summing over `i` from `k` to `n` counts "
                "every `(k+1)`-subset exactly once.",
            ]),
            ("p", "Classifying by the largest element is the other reusable device in this "
                  "lesson. It turns a sum into a single count and is the standard way to "
                  "prove identities whose left side is a sum."),
            ("thm", ("Vandermonde's identity",
                     "`C(m+n, r) = Σ_{k=0}^{r} C(m, k) C(n, r−k)`.")),
            ("proof", [
                "Split `m + n` objects into a group of `m` and a group of `n`. An "
                "`r`-subset takes `k` from the first group and `r−k` from the second, for "
                "some `k`. Summing over `k` counts every `r`-subset exactly once.",
            ]),
        ],
        "lab": ("pascal", {
            "identity": "rule", "n": 6, "k": 2,
            "panel_title": "Highlight and check",
            "panel_intro": "The lab highlights the terms of the selected identity and adds "
                           "them up, comparing the total against what the identity claims. "
                           "The picture and the arithmetic are shown together.",
        }),
        "steps_title": "Proving a binomial identity by counting",
        "steps_intro": "Find a set both sides count.",
        "steps": [
            ("Decide what the right-hand side counts",
             "`C(n+1, k+1)` counts `(k+1)`-subsets of an `(n+1)`-set. Naming the objects "
             "is the first move."),
            ("Find a classification giving the left-hand side",
             "By whether a fixed element is in; by the largest element; by how many come "
             "from each of two groups."),
            ("Check the classes are disjoint and exhaustive",
             "Every object in exactly one class. This is where a counting proof goes wrong "
             "if it goes wrong."),
            ("State the conclusion",
             "One set, two counts, therefore two equal expressions. That sentence is the "
             "proof's ending."),
        ],
        "worked": {
            "title": "Prove `Σ_k k·C(n,k) = n·2ⁿ⁻¹`",
            "intro": ["Count committees with a designated chair, two ways."],
            "lines": [
                "Objects: pairs (committee, chair) where the chair is a committee member,",
                "         from a pool of n people.  Committees may be any size ≥ 1.",
                "",
                "COUNT 1 — choose the committee first:",
                "   a committee of size k can be chosen C(n,k) ways,",
                "   and its chair k ways.   Total  Σ_k k·C(n,k).",
                "",
                "COUNT 2 — choose the chair first:",
                "   n ways to pick the chair, then each of the other n−1 people",
                "   independently in or out:  2ⁿ⁻¹.   Total  n·2ⁿ⁻¹.",
                "",
                "Same set, two counts  ⟹  Σ_k k·C(n,k) = n·2ⁿ⁻¹.        ∎",
            ],
            "after": [
                "The algebraic proof of this identity requires differentiating the binomial "
                "theorem. The counting proof is four lines and explains the answer: the "
                "factor `n` is the chair and the `2ⁿ⁻¹` is everyone else's independent "
                "decision."
            ],
        },
        "quiz_title": "Binomial coefficients",
        "quiz": [
            {"q": "Pascal's rule is proved by:",
             "a": ["algebra with factorials",
                   "splitting the `k`-subsets by whether they contain a fixed element",
                   "induction on `k`",
                   "the binomial theorem"],
             "c": 1,
             "why": "That case split gives the two terms directly. The algebraic "
                    "verification works but explains nothing."},
            {"q": "Row 6 of Pascal's triangle sums to:",
             "a": ["36", "64", "12", "720"],
             "c": 1,
             "why": "`2⁶ = 64`. The row counts the subsets of a six-element set, grouped "
                    "by size."},
            {"q": "The alternating sum `Σ_k (−1)^k C(n,k)` is 0 for `n ≥ 1` because:",
             "a": ["the row is symmetric",
                   "the even-sized and odd-sized subsets are matched by a bijection",
                   "`C(n,k)` is always even",
                   "the row sums to `2ⁿ`"],
             "c": 1,
             "why": "Adding or removing a fixed element pairs each subset with one of "
                    "opposite parity. Symmetry alone would not give it &mdash; odd rows are "
                    "symmetric too and their alternating sum is 0 for the same bijective "
                    "reason."},
        ],
        "mistakes": [
            ("Proving identities algebraically by default",
             "The counting proof is usually shorter and always more informative. Algebra "
             "confirms; counting explains."),
            ("Applying Pascal's rule at the edges",
             "`C(n,0)` and `C(n,n)` have only one parent, and the rule as stated needs "
             "`1 ≤ k ≤ n−1`. The edge entries are 1 by definition."),
            ("Forgetting the `n = 0` exception in the alternating sum",
             "The bijection needs an element to add or remove. With none, the sum is 1."),
        ],
        "standard": ("Finish when you can prove an identity by counting one set twice.",
                     "Prove `C(n,k)·C(k,j) = C(n,j)·C(n−j,k−j)` by counting the ways to "
                     "choose a `k`-subset and then a `j`-subset of it. Both sides count "
                     "the same pairs, in different orders."),
        "note": "Pascal's triangle mod 2 reproduces the Sierpiński triangle, because "
                "`C(n,k)` is odd exactly when the binary digits of `k` are a subset of "
                "those of `n` &mdash; Kummer's theorem. Course 6's modular arithmetic is "
                "what makes that statement precise.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "the-binomial-theorem",
        "title": "The Binomial Theorem",
        "module": "Binomial coefficients",
        "one_line": "Why the same numbers count subsets and expand powers.",
        "summary": (
            "`(x + y)ⁿ = Σ C(n,k) x^{n−k} y^k`. The coefficient counts the ways to choose "
            "`k` factors to contribute `y`, which is why the binomial coefficients appear "
            "&mdash; and the substitutions `x = y = 1` recover the row sums."
        ),
        "key": [
            "(x + y)ⁿ = Σ_{k=0}^{n} C(n,k) x^{n−k} y^k",
            "x = y = 1   ⟹   Σ C(n,k) = 2ⁿ",
            "x = 1, y = −1  ⟹  Σ (−1)^k C(n,k) = 0",
            "The coefficient counts CHOICES of which factors supply y.",
        ],
        "key_label": "One theorem, several corollaries",
        "concepts_intro": (
            "The theorem is a counting statement wearing algebraic notation, and its "
            "corollaries come from substituting numbers."
        ),
        "concepts": [
            ("Expanding is choosing",
             "Multiplying out `(x+y)ⁿ` means picking `x` or `y` from each factor. The "
             "coefficient of `x^{n−k}y^k` counts the ways to pick `y` from exactly `k` of "
             "them."),
            ("Substitution generates identities",
             "Setting `x` and `y` to specific values turns the theorem into a numerical "
             "identity. Two substitutions give the row sum and the alternating sum for free."),
            ("The multinomial theorem generalises it",
             "With more than two terms the coefficients count arrangements of a multiset, "
             "which is lesson 7's subject."),
        ],
        "read_title": "The theorem and what follows",
        "read_intro": "Statement, the counting proof, and four corollaries.",
        "body": [
            ("thm", ("Binomial theorem",
                     "For any `x, y` and any `n ≥ 0`, "
                     "`(x + y)ⁿ = Σ_{k=0}^{n} C(n,k) x^{n−k} y^k`.")),
            ("proof", [
                "`(x+y)ⁿ` is the product of `n` identical factors `(x+y)`. Expanding without "
                "collecting terms produces one term for each way of choosing `x` or `y` "
                "from each factor &mdash; `2ⁿ` terms in all.",
                "A term equals `x^{n−k}y^k` exactly when `y` was chosen from `k` of the "
                "factors, and the number of ways to choose those `k` factors is `C(n,k)`.",
                "Collecting equal terms therefore gives coefficient `C(n,k)` on "
                "`x^{n−k}y^k`.",
            ]),
            ("p", "This explains the name: the binomial coefficients are the coefficients "
                  "in a binomial expansion, and they count subsets because expanding is "
                  "choosing. The two facts are not analogous &mdash; they are the same fact."),
            ("p", "An induction proof using Pascal's rule is also available and is a good "
                  "exercise for course 3's technique. It verifies the theorem; the counting "
                  "argument explains it."),
            ("h3", "Corollaries by substitution"),
            ("math", [
                "x = 1, y = 1     Σ_k C(n,k)          = 2ⁿ",
                "x = 1, y = −1    Σ_k (−1)^k C(n,k)   = 0        for n ≥ 1",
                "x = 1, y = 2     Σ_k 2^k C(n,k)      = 3ⁿ",
                "x = 1, y = t     Σ_k t^k C(n,k)      = (1 + t)ⁿ",
            ]),
            ("p", "The last line is the generating function of the binomial coefficients, "
                  "and lesson 12 makes that phrase mean something. For now it is the "
                  "observation that a single algebraic identity encodes a whole row of the "
                  "triangle."),
            ("example", ("Extracting one coefficient",
                         "What is the coefficient of `x⁵y³` in `(2x − 3y)⁸`? The general "
                         "term is `C(8,k)(2x)^{8−k}(−3y)^k`. Take `k = 3`: "
                         "`C(8,3)·2⁵·(−3)³ = 56 · 32 · (−27) = −48384`.")),
            ("p", "Two places to be careful: the constants inside the parentheses are "
                  "raised to the powers too, and a negative sign must be carried through "
                  "the odd power. Both are dropped often enough to be worth naming."),
            ("thm", ("Multinomial theorem",
                     "`(x₁ + ⋯ + x_m)ⁿ = Σ (n! / (k₁! ⋯ k_m!)) x₁^{k₁} ⋯ x_m^{k_m}`, summed "
                     "over all non-negative `kᵢ` with `k₁ + ⋯ + k_m = n`. The coefficient "
                     "counts the ways to assign the `n` factors to the `m` terms, which is "
                     "lesson 7's arrangement count.")),
        ],
        "lab": ("pascal", {
            "identity": "row", "n": 5, "k": 2,
            "panel_title": "Row sums and the expansion",
            "panel_intro": "The expansion of `(x + y)ⁿ` is printed below the controls, with "
                           "coefficients taken from the triangle. Selecting the row-sum "
                           "identity highlights exactly the terms that add to `2ⁿ`.",
        }),
        "steps_title": "Using the theorem",
        "steps_intro": "Write the general term first.",
        "steps": [
            ("Write the general term",
             "`C(n,k) a^{n−k} b^k` where `a` and `b` are the two whole expressions being "
             "added, constants and signs included."),
            ("Solve for `k` from the power you want",
             "Match the exponent of one variable and read off `k`. Matching both is a "
             "useful check that the term exists."),
            ("Evaluate the constants carefully",
             "`(2x)⁵` contributes `2⁵`, and `(−3y)³` contributes `(−3)³ = −27`. Signs on "
             "odd powers are the standard slip."),
            ("Substitute to get identities",
             "Setting `x` and `y` to 1, −1 or small integers turns the theorem into "
             "numerical facts about a row of the triangle."),
        ],
        "worked": {
            "title": "Expand and extract",
            "intro": ["Two uses of the same general term."],
            "lines": [
                "(x + y)⁴ = C(4,0)x⁴ + C(4,1)x³y + C(4,2)x²y² + C(4,3)xy³ + C(4,4)y⁴",
                "         =      x⁴ +      4x³y +      6x²y² +      4xy³ +      y⁴",
                "",
                "coefficients 1, 4, 6, 4, 1  —  row 4 of Pascal's triangle",
                "",
                "Coefficient of x²y⁶ in (x + 2y)⁸:",
                "   general term  C(8,k) x^{8−k} (2y)^k",
                "   want y⁶  ⟹  k = 6,  and then x^{8−6} = x²        ✓",
                "   C(8,6)·2⁶ = 28 · 64 = 1792",
            ],
            "after": [
                "The check that `x^{8−k}` gives the exponent you wanted is worth the second "
                "it takes. If the two exponents do not both match, the term you are looking "
                "for does not appear in the expansion at all."
            ],
        },
        "quiz_title": "The binomial theorem",
        "quiz": [
            {"q": "The coefficient of `x³y²` in `(x + y)⁵` is:",
             "a": ["5", "10", "20", "15"],
             "c": 1,
             "why": "`C(5,2) = 10` &mdash; the number of ways to choose which two of the "
                    "five factors supply the `y`."},
            {"q": "Substituting `x = y = 1` gives:",
             "a": ["`Σ C(n,k) = 2ⁿ`", "`Σ (−1)^k C(n,k) = 0`",
                   "`C(n,0) = 1`", "nothing useful"],
             "c": 0,
             "why": "Both sides become numbers: the left is `2ⁿ` and the right is the sum "
                    "of the row. The row-sum identity falls out."},
            {"q": "In `(3x − y)⁷`, the coefficient of `x⁴y³` is:",
             "a": ["`C(7,3)·3⁴`", "`−C(7,3)·3⁴`", "`C(7,4)·3³`", "`−C(7,4)`"],
             "c": 1,
             "why": "`C(7,3)(3x)⁴(−y)³ = C(7,3)·81·(−1)·x⁴y³`. The odd power of `−y` "
                    "carries the minus sign."},
        ],
        "mistakes": [
            ("Forgetting the constants inside the parentheses",
             "`(2x)⁵` is `32x⁵`. The coefficient of the term is `C(n,k)` times whatever "
             "the constants contribute."),
            ("Losing a sign on an odd power",
             "`(−y)³ = −y³`. Half of all extraction errors are this one."),
            ("Confusing the index with the exponent",
             "In `C(n,k)x^{n−k}y^k`, `k` is the exponent of the SECOND term. Reading it as "
             "the first gives the mirror-image coefficient, which is right only when the "
             "row is symmetric at that point."),
        ],
        "standard": ("Finish when you can extract a coefficient with constants and signs "
                     "present.",
                     "Find the coefficient of `x⁴y⁵` in `(2x − 3y)⁹`, and check the sign "
                     "and both constants. Then set `x = y = 1` in the same expansion and "
                     "confirm the result equals `(2 − 3)⁹ = −1`."),
        "note": "Newton extended the theorem to non-integer exponents, where the sum "
                "becomes an infinite series and the coefficients use the generalised "
                "binomial coefficient. That is where lesson 12's generating functions "
                "acquire their power, and it is outside this course.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "permutations-with-repetition",
        "title": "Permutations with Repetition",
        "module": "Repetition",
        "one_line": "Arrangements when objects may repeat, or are indistinguishable.",
        "summary": (
            "Two different situations share this name. Choosing `r` items from `n` with "
            "repetition allowed and order mattering gives `nʳ`. Arranging a multiset "
            "divides by the factorials of the repetition counts."
        ),
        "key": [
            "ordered, repetition allowed:      nʳ",
            "arrangements of a multiset:       n! / (n₁! n₂! ⋯ n_k!)",
            "MISSISSIPPI:  11! / (1!·4!·4!·2!) = 34 650",
            "The divisor is the symmetry you are quotienting out.",
        ],
        "key_label": "Two counts, one name",
        "concepts_intro": (
            "Repetition appears in two guises, and they need different formulas. "
            "Distinguishing them is the lesson."
        ),
        "concepts": [
            ("Drawing with replacement gives `nʳ`",
             "Each of the `r` positions is filled independently from all `n` options. This "
             "is the product rule with no shrinkage."),
            ("Identical objects divide out",
             "Arranging `n` objects of which some are indistinguishable gives `n!` divided "
             "by the factorial of each repetition count."),
            ("The divisor is a symmetry group size",
             "Swapping two identical letters produces the same word, so each distinct word "
             "was counted once for every such swap &mdash; exactly the circular-arrangement "
             "argument of lesson 3."),
        ],
        "read_title": "Repetition in arrangements",
        "read_intro": "Both counts, derived, and the connection to binomial coefficients.",
        "body": [
            ("thm", ("Ordered selections with repetition",
                     "The number of sequences of length `r` from an `n`-element set, with "
                     "repetition allowed, is `nʳ`.")),
            ("proof", [
                "Each position is filled independently, with all `n` options available "
                "every time. The product rule gives `n · n ⋯ n = nʳ`.",
            ]),
            ("p", "This is the count of functions from an `r`-set to an `n`-set, and of "
                  "strings of length `r` over an alphabet of size `n`. `{0,1}ⁿ` has `2ⁿ` "
                  "elements for exactly this reason."),
            ("thm", ("Arrangements of a multiset",
                     "If `n` objects consist of `k` distinct types with `n₁, …, n_k` copies "
                     "(`n₁ + ⋯ + n_k = n`), the number of distinguishable arrangements is "
                     "`n! / (n₁! n₂! ⋯ n_k!)`.")),
            ("proof", [
                "Label the identical copies temporarily so all `n` objects are distinct; "
                "there are `n!` arrangements. Each distinguishable arrangement arises from "
                "exactly `n₁! n₂! ⋯ n_k!` of them, one for each way of permuting the "
                "labels within each type. Dividing gives the count.",
            ]),
            ("example", ("MISSISSIPPI",
                         "Eleven letters: one M, four I, four S, two P. The number of "
                         "distinguishable arrangements is "
                         "`11!/(1!·4!·4!·2!) = 39 916 800 / 1152 = 34 650`, rather than "
                         "`11! = 39 916 800`.")),
            ("h3", "The connection to binomial coefficients"),
            ("p", "`C(n, r)` is a special case: arranging `r` copies of \"in\" and `n − r` "
                  "copies of \"out\" gives `n!/(r!(n−r)!)`, which is exactly `C(n,r)`. "
                  "Choosing a subset and arranging a two-type multiset are the same problem."),
            ("thm", ("Multinomial coefficient",
                     "`n! / (n₁! ⋯ n_k!)` is written `binom(n; n₁, …, n_k)` and counts both "
                     "the arrangements of the multiset and the ways to distribute `n` "
                     "distinct objects into `k` labelled boxes with prescribed sizes. It is "
                     "the coefficient in the multinomial theorem of lesson 6.")),
            ("example", ("Distributing into boxes",
                         "Deal 52 cards to four players, 13 each: "
                         "`52!/(13!)⁴ ≈ 5.36 × 10²⁸`. The formula is the same because "
                         "assigning each card a player is arranging a multiset of 13 copies "
                         "of each of four labels.")),
            ("h3", "Lattice paths again"),
            ("p", "A path from `(0,0)` to `(m,n)` using unit right and up steps is an "
                  "arrangement of `m` R's and `n` U's, so there are `(m+n)!/(m! n!) = "
                  "C(m+n, m)` of them &mdash; the same answer lesson 4 gave, now visible as "
                  "a multiset arrangement."),
        ],
        "lab": ("counting", {
            "n": 4, "r": 3, "rule": "pr",
            "panel_title": "Repetition allowed",
            "panel_intro": "The `nʳ` row is ordered selection with repetition. Compare it "
                           "with the `P` row directly below: the gap is exactly the "
                           "selections that reuse an object.",
        }),
        "steps_title": "Counting with repetition",
        "steps_intro": "Decide which of the two situations you are in.",
        "steps": [
            ("Are you drawing with replacement, or arranging a fixed multiset?",
             "Drawing gives `nʳ`; arranging gives the factorial quotient. They are "
             "different questions with different answers."),
            ("For drawing, apply the product rule",
             "`n` options at every one of the `r` positions, with no shrinkage."),
            ("For arranging, count the repetitions of each type",
             "The divisor is the product of the factorials of those counts. Missing a "
             "repeated letter inflates the answer."),
            ("Check the exponents sum to `n`",
             "`n₁ + ⋯ + n_k` must equal the total number of objects. If it does not, a "
             "type has been miscounted."),
        ],
        "worked": {
            "title": "Arrangements with a constraint",
            "intro": ["How many arrangements of BANANA have no two A's adjacent?"],
            "lines": [
                "BANANA: 6 letters — 3 A, 2 N, 1 B.",
                "",
                "Total arrangements:  6!/(3!·2!·1!) = 720/12 = 60",
                "",
                "For no two A's adjacent, place the non-A letters first:",
                "   arrange B, N, N:   3!/2! = 3 ways      e.g.  B N N",
                "   this creates 4 gaps:  _ B _ N _ N _",
                "   choose 3 of the 4 gaps for the A's:  C(4,3) = 4",
                "",
                "   3 × 4 = 12 arrangements with no two A's adjacent",
                "",
                "So 60 − 12 = 48 arrangements DO have two A's adjacent.",
            ],
            "after": [
                "The gap method is the standard device for \"no two adjacent\" constraints: "
                "arrange the unconstrained objects, then insert the constrained ones into "
                "the gaps between them. It works because choosing distinct gaps guarantees "
                "no two of the inserted objects touch."
            ],
        },
        "quiz_title": "Repetition",
        "quiz": [
            {"q": "How many strings of length 4 can be made from `{a, b, c}`?",
             "a": ["12", "24", "81", "64"],
             "c": 2,
             "why": "`3⁴ = 81`. Repetition is allowed and order matters, so each of four "
                    "positions has three independent options."},
            {"q": "How many distinguishable arrangements does BOOKKEEPER have? (B,O,O,K,K,E,E,P,E,R)",
             "a": ["`10!`", "`10!/(2!·2!·3!)`", "`10!/(2!·3!)`", "`10!/4!`"],
             "c": 1,
             "why": "Two O, two K, three E, and the rest single. Divide by the factorial "
                    "of each repetition count."},
            {"q": "Why does arranging a multiset divide by factorials?",
             "a": ["To keep the answer an integer",
                   "Each distinguishable arrangement was counted once per permutation of the identical copies",
                   "Because the objects are ordered",
                   "It is a convention"],
             "c": 1,
             "why": "Labelling the copies makes all `n!` arrangements distinct; removing "
                    "the labels collapses each group of `n₁!⋯n_k!` into one."},
        ],
        "mistakes": [
            ("Confusing the two situations",
             "\"Repetition allowed\" when drawing gives `nʳ`; \"repeated objects\" when "
             "arranging gives a quotient. They are different problems."),
            ("Missing a repeated letter",
             "Every repetition contributes a factorial to the divisor. Count the "
             "occurrences of each letter explicitly before dividing."),
            ("Applying the gap method without checking the gap count",
             "Arranging `m` objects creates `m + 1` gaps, including the ends. Using `m − 1` "
             "counts only the internal gaps and undercounts."),
        ],
        "standard": ("Finish when you can handle an adjacency constraint by gaps.",
                     "Count the arrangements of MISSISSIPPI with no two S's adjacent. "
                     "Arrange the other seven letters, count the gaps, and choose four of "
                     "them. Both halves &mdash; the multiset arrangement and the gap choice "
                     "&mdash; are this lesson."),
        "note": "The multinomial coefficient counts three things at once: arrangements of "
                "a multiset, distributions of distinct objects into labelled boxes of "
                "given sizes, and coefficients in the multinomial expansion. Recognising "
                "a problem as any one of them gives you the other two.",
    },
]
