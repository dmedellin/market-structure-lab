"""Course 1, lessons 01-07 — propositional logic."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "propositions-and-truth-values",
        "title": "Propositions and Truth Values",
        "module": "Propositional logic",
        "one_line": "What counts as a proposition, and what does not.",
        "summary": (
            "A proposition is a declarative sentence with exactly one truth value. "
            "Establish which sentences qualify, why questions and open sentences do "
            "not, and why this restriction is what makes everything later possible."
        ),
        "key": [
            "p :  \"17 is prime\"             proposition, true",
            "q :  \"x + 1 = 5\"               NOT a proposition (open sentence)",
            "r :  \"Close the door.\"         NOT a proposition (not declarative)",
            "s :  \"This sentence is false\"  NOT a proposition (no consistent value)",
        ],
        "key_label": "Four sentences, one proposition",
        "concepts_intro": (
            "Everything in this course is built on sentences that have a truth value. "
            "The first job is to say precisely which sentences those are."
        ),
        "concepts": [
            ("A proposition has exactly one truth value",
             "It is either true or false &mdash; not both, not neither, and not "
             "\"it depends\". The value may be unknown to us; what matters is that "
             "the sentence has one."),
            ("Open sentences are not propositions yet",
             "`x &gt; 3` has no truth value until `x` is given one. It becomes a "
             "proposition when the variable is bound, which is what quantifiers do "
             "in lesson 8."),
            ("Truth is not the same as provability",
             "\"Every even number greater than 2 is a sum of two primes\" is a "
             "proposition. Nobody knows its value; it still has one."),
        ],
        "read_title": "What a proposition is",
        "read_intro": "Four rules, and the sentences each one excludes.",
        "body": [
            ("def", ("Proposition",
                     "A <strong>proposition</strong> is a declarative sentence that is "
                     "either true or false, but not both. Its <strong>truth value</strong> "
                     "is `T` or `F`.")),
            ("p", "Three kinds of sentence fail this definition, and each fails for its "
                  "own reason."),
            ("ul", [
                "<strong>Not declarative.</strong> \"What time is it?\" and \"Close the "
                "door.\" assert nothing, so there is nothing to be true or false.",
                "<strong>Open.</strong> \"`x + 1 = 5`\" is true for `x = 4` and false "
                "otherwise. It has a truth value only once `x` is fixed. Such a sentence "
                "is a <em>predicate</em>, and lesson 8 gives it the treatment it deserves.",
                "<strong>Self-referentially paradoxical.</strong> \"This sentence is "
                "false\" cannot be true (it would then be false) and cannot be false (it "
                "would then be true). No truth value can be assigned consistently.",
            ]),
            ("p", "The third exclusion is not a technicality. It is the reason logic is "
                  "built on a restricted class of sentences rather than on English: the "
                  "moment sentences may talk about their own truth, the two-valued system "
                  "breaks."),
            ("thm", ("Bivalence",
                     "Every proposition has exactly one of the two truth values `T`, `F`. "
                     "This is an assumption of classical logic, not a theorem within it, "
                     "and it is what licenses `p ∨ ¬p` &mdash; the law of the excluded "
                     "middle &mdash; used throughout this path.")),
            ("p", "Unknown is not a third value. \"There are infinitely many twin primes\" "
                  "is a proposition whose value nobody currently knows; the sentence is "
                  "true or it is false, and our ignorance is a fact about us."),
            ("example", ("Sorting sentences",
                         "\"`2 + 2 = 5`\" &mdash; proposition, false. "
                         "\"`n` is even\" &mdash; open, not a proposition. "
                         "\"Every integer greater than 1 has a prime factor\" &mdash; "
                         "proposition, true. \"Let `x = 3`\" &mdash; an instruction, not a "
                         "proposition.")),
            ("p", "Notation: propositions get lower-case letters `p`, `q`, `r`, `s`. "
                  "Those letters are <em>propositional variables</em> &mdash; placeholders "
                  "for whole sentences, not for numbers."),
        ],
        "lab": ("truth_table", {
            "formulas": ["p", "~p", "p & q", "p | q", "p -> q", "p <-> q", "p ^ q"],
            "compare_with": "p | q",
            "panel_title": "One variable at a time",
            "panel_intro": "Start with `p` alone: two rows, because one proposition has "
                           "two possible truth values and nothing else.",
        }),
        "steps_title": "Deciding whether a sentence is a proposition",
        "steps_intro": "Four questions, in this order. The first \"no\" settles it.",
        "steps": [
            ("Is it declarative?",
             "Questions, commands and exclamations assert nothing. If the sentence "
             "cannot sensibly be preceded by \"It is true that…\", stop here."),
            ("Are all its variables fixed?",
             "If the sentence contains a free variable, it is an open sentence. Bind "
             "it or substitute a value and it becomes a proposition."),
            ("Does it refer to its own truth?",
             "Self-reference is where the two-valued assumption breaks. A sentence that "
             "asserts something about its own truth value is excluded."),
            ("Is it vague rather than merely unknown?",
             "\"This film is good\" has no definite value; \"there are infinitely many "
             "twin primes\" has one we do not know. Only the first fails."),
        ],
        "worked": {
            "title": "Classifying six sentences",
            "intro": ["Work down the list and give the reason, not just the verdict."],
            "lines": [
                "1.  \"7 is a prime number.\"               proposition, T",
                "2.  \"Is 7 prime?\"                        no  — interrogative",
                "3.  \"x is a prime number.\"               no  — open in x",
                "4.  \"7 is prime and 8 is prime.\"         proposition, F",
                "5.  \"There is a largest prime.\"          proposition, F  (Euclid)",
                "6.  \"P = NP.\"                            proposition, value unknown",
            ],
            "after": [
                "Line 6 is the one worth dwelling on. It is a perfectly good "
                "proposition: a precise mathematical claim that is true or false. That "
                "no one has determined which does not put it in a third category."
            ],
        },
        "quiz_title": "Proposition or not",
        "quiz": [
            {"q": "Which of these is a proposition?",
             "a": ["`x` is greater than 5", "Please compute the sum.",
                   "Every prime greater than 2 is odd", "How many primes are there?"],
             "c": 2,
             "why": "It is declarative and has a definite truth value (true). The first "
                    "is open in `x`, the second is a command, and the fourth is a question."},
            {"q": "\"There are infinitely many twin primes.\" What is this sentence?",
             "a": ["Not a proposition, because nobody knows whether it is true",
                   "A proposition whose truth value is currently unknown",
                   "A proposition with truth value \"unknown\"",
                   "An open sentence"],
             "c": 1,
             "why": "Bivalence says every proposition has one of exactly two values. "
                    "Unknown is a state of our knowledge, not a third truth value."},
            {"q": "Why is \"This sentence is false\" excluded?",
             "a": ["It is not declarative",
                   "It contains a free variable",
                   "No truth value can be assigned to it consistently",
                   "It is too vague"],
             "c": 2,
             "why": "Assuming it true makes it false and assuming it false makes it true. "
                    "The exclusion of self-reference is what keeps the two-valued system "
                    "coherent."},
        ],
        "mistakes": [
            ("Treating \"unknown\" as a truth value",
             "A conjecture is a proposition. Its value exists whether or not anyone has "
             "found it, and no rule in this course needs to know which it is."),
            ("Calling an open sentence false because it is sometimes false",
             "`x &gt; 3` is not false; it has no value at all until `x` is fixed. "
             "Confusing \"not always true\" with \"false\" is the same error that makes "
             "quantifier negation hard in lesson 10."),
            ("Assuming vagueness and ignorance are the same problem",
             "\"Tall\" has no sharp boundary, so \"he is tall\" is not a proposition. "
             "\"P = NP\" has a sharp meaning we cannot currently evaluate, so it is."),
        ],
        "standard": ("Finish when you can say why a sentence fails, not just that it does.",
                     "Given ten sentences you should be able to sort them and name the "
                     "specific reason for each exclusion: not declarative, open, "
                     "self-referential, or vague. \"It's not a proposition\" without the "
                     "reason is the answer that does not transfer to lesson 8."),
        "note": "The truth table lab appears here with a single variable on purpose. "
                "Two rows for one proposition, four for two, `2ⁿ` for `n` &mdash; the "
                "doubling is worth noticing now, because lesson 3 depends on it and "
                "course 4 counts it.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "logical-connectives",
        "title": "Logical Connectives",
        "module": "Propositional logic",
        "one_line": "Negation, conjunction, disjunction, exclusive or.",
        "summary": (
            "Four connectives, each defined by exactly what it does to truth values. "
            "The one that causes trouble is `∨`, which is inclusive &mdash; and the "
            "one English does not have a clean word for is `⊕`."
        ),
        "key": [
            "¬p       true exactly when p is false",
            "p ∧ q    true exactly when both are true",
            "p ∨ q    true when at least one is true   (INCLUSIVE)",
            "p ⊕ q    true when exactly one is true    (exclusive)",
        ],
        "key_label": "Four connectives, four definitions",
        "concepts_intro": (
            "A connective is defined by its truth table and by nothing else. Any "
            "intuition about the English word is a convenience, not the definition."
        ),
        "concepts": [
            ("Or is inclusive",
             "`p ∨ q` is true when both are true. English \"or\" is often exclusive "
             "(\"soup or salad\"), and reading `∨` that way is the single most common "
             "error in this course."),
            ("Connectives are functions on truth values",
             "`∧` takes two truth values and returns one. It does not know or care what "
             "the propositions are about, which is why `p ∧ q` and `q ∧ p` are the same."),
            ("Precedence exists to save parentheses",
             "`¬` binds tightest, then `∧`, then `∨`. So `¬p ∧ q` means `(¬p) ∧ q`. "
             "When in doubt, write the parentheses."),
        ],
        "read_title": "The four basic connectives",
        "read_intro": "Each defined by a truth table, then read back into English.",
        "body": [
            ("def", ("Negation",
                     "`¬p` (\"not `p`\") is true when `p` is false and false when `p` is "
                     "true. It is the only unary connective in this course.")),
            ("def", ("Conjunction",
                     "`p ∧ q` (\"`p` and `q`\") is true exactly when both `p` and `q` are "
                     "true &mdash; one row of the four.")),
            ("def", ("Disjunction",
                     "`p ∨ q` (\"`p` or `q`\") is true exactly when at least one of "
                     "`p`, `q` is true &mdash; three rows of the four. This is the "
                     "<strong>inclusive</strong> or.")),
            ("def", ("Exclusive or",
                     "`p ⊕ q` is true exactly when exactly one of `p`, `q` is true. "
                     "It is false when both are true, which is where it parts company "
                     "with `∨`.")),
            ("p", "The two disjunctions differ in exactly one row of four, and that row "
                  "is where natural language is ambiguous. \"You may have coffee or tea\" "
                  "usually means `⊕`; \"an error occurs if the file is missing or "
                  "unreadable\" means `∨`. Mathematics settles the ambiguity by decree: "
                  "`∨` is always inclusive."),
            ("math", [
                "p   q  |  ¬p   p∧q   p∨q   p⊕q",
                "----------------------------------",
                "T   T  |   F     T     T     F     ← the row that separates ∨ from ⊕",
                "T   F  |   F     F     T     T",
                "F   T  |   T     F     T     T",
                "F   F  |   T     F     F     F",
            ]),
            ("p", "Two English constructions to watch. \"Neither `p` nor `q`\" is "
                  "`¬p ∧ ¬q`, which lesson 5 shows equals `¬(p ∨ q)`. \"`p` unless `q`\" "
                  "is `¬q → p`, which is lesson 4's business and is <em>not</em> `p ⊕ q`."),
            ("thm", ("Precedence",
                     "In order from tightest to loosest: `¬`, then `∧`, then `∨` and `⊕`, "
                     "then `→`, then `↔`. So `¬p ∨ q ∧ r` means `(¬p) ∨ (q ∧ r)`. This is "
                     "convention rather than mathematics, and parentheses always win.")),
        ],
        "lab": ("truth_table", {
            "formulas": ["p | q", "p ^ q", "p & q", "~p & ~q", "~(p | q)", "~p | ~q",
                         "~(p & q)", "(p | q) & ~(p & q)"],
            "compare_with": "p ^ q",
            "mode": "two",
            "panel_title": "Separate the two disjunctions",
            "panel_intro": "Compare `p | q` with `p ^ q` and read the row where they "
                           "differ. Then check that `(p | q) & ~(p & q)` is `⊕` written "
                           "out of the other three connectives.",
        }),
        "steps_title": "Translating English into connectives",
        "steps_intro": "The verb tells you the shape; the small words tell you which.",
        "steps": [
            ("Find the atomic propositions",
             "Split the sentence into the smallest parts that are themselves true or "
             "false, and name them `p`, `q`, `r`."),
            ("Identify the connective words",
             "\"and\", \"but\", \"yet\" and \"however\" are all `∧`. \"or\" is `∨` unless "
             "the sentence forces exclusivity. \"neither…nor\" is a negated disjunction."),
            ("Decide whether the or is exclusive",
             "Ask what happens when both hold. If the sentence is still true, it is `∨`; "
             "if it becomes false, it is `⊕`."),
            ("Parenthesise, then check a row",
             "Write the formula with explicit parentheses and test it on the case you "
             "understand best. One wrong row means a wrong translation."),
        ],
        "worked": {
            "title": "Translating four sentences",
            "intro": ["Let `p` = \"it is raining\" and `q` = \"the ground is wet\"."],
            "lines": [
                "\"It is raining and the ground is wet.\"           p ∧ q",
                "\"It is raining but the ground is not wet.\"       p ∧ ¬q",
                "\"Neither is it raining nor is the ground wet.\"   ¬p ∧ ¬q",
                "\"Either it is raining or the ground is wet,",
                "  but not both.\"                                 p ⊕ q",
            ],
            "after": [
                "\"But\" is `∧`. It carries a contrast in English that logic simply "
                "discards, because the truth value of \"`p` but `q`\" is the truth value "
                "of \"`p` and `q`\" in every case. Losing that shade of meaning is a "
                "deliberate trade: what remains is checkable."
            ],
        },
        "quiz_title": "Connectives",
        "quiz": [
            {"q": "`p` and `q` are both true. What is `p ∨ q`?",
             "a": ["False, because \"or\" means one or the other",
                   "True, because `∨` is inclusive",
                   "Undefined", "It depends on the propositions"],
             "c": 1,
             "why": "`p ∨ q` is false in exactly one case: when both are false. Both "
                    "true is the row where `∨` and `⊕` differ."},
            {"q": "Which formula means \"neither `p` nor `q`\"?",
             "a": ["`¬p ∨ ¬q`", "`¬(p ∧ q)`", "`¬p ∧ ¬q`", "`p ⊕ q`"],
             "c": 2,
             "why": "\"Neither\" asserts both are false, so it is `¬p ∧ ¬q`. That is "
                    "equal to `¬(p ∨ q)` by De Morgan, but not to either of the first two."},
            {"q": "Without extra parentheses, `¬p ∧ q` means:",
             "a": ["`¬(p ∧ q)`", "`(¬p) ∧ q`", "ambiguous", "`¬(p) ∧ ¬(q)`"],
             "c": 1,
             "why": "`¬` binds tighter than `∧`, so it applies to `p` alone. These two "
                    "readings differ: at `p = F, q = F` the first is true and the second "
                    "is false."},
        ],
        "mistakes": [
            ("Reading `∨` as exclusive",
             "It costs you one row in every truth table containing a disjunction, and it "
             "makes De Morgan's laws look wrong in lesson 5."),
            ("Dropping parentheses around a negation",
             "`¬p ∧ q` and `¬(p ∧ q)` disagree in two of four rows. When a negation "
             "governs more than a single letter, write the brackets."),
            ("Translating \"but\" as something other than `∧`",
             "\"But\", \"although\" and \"however\" all signal contrast, which is a fact "
             "about emphasis. The truth conditions are exactly those of \"and\"."),
        ],
        "standard": ("Finish when you can produce any of the four truth tables from memory "
                     "and defend the `∨` row.",
                     "The test is not reciting the tables: it is being handed \"either "
                     "`p` or `q`\" in a sentence and deciding correctly whether both "
                     "holding keeps it true."),
        "note": "`⊕` is the parity connective: `p ⊕ q ⊕ r` is true when an odd number of "
                "them are true. That is why it appears in checksums and error-detecting "
                "codes, and why course 6 meets it again as addition modulo 2.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "truth-tables",
        "title": "Truth Tables",
        "module": "Propositional logic",
        "one_line": "The complete method for evaluating any compound statement.",
        "summary": (
            "A truth table lists every assignment of truth values to the variables and "
            "evaluates the formula at each. It is finite, mechanical and complete "
            "&mdash; and it is the only tool in this course that can never be wrong."
        ),
        "key": [
            "n variables  ⟹  2ⁿ rows      1 var: 2   2 vars: 4   3 vars: 8",
            "Build inner subexpressions first, then combine them.",
            "The table is COMPLETE: it checks every possible case.",
        ],
        "key_label": "The method, in three lines",
        "concepts_intro": (
            "Truth tables are the ground truth of propositional logic. Every later "
            "shortcut is justified by the fact that a table would agree."
        ),
        "concepts": [
            ("The number of rows is `2ⁿ`",
             "Each variable doubles the cases. Three variables give 8 rows, five give 32. "
             "This growth is why lesson 5's equivalence laws are worth having."),
            ("Columns go inside out",
             "Evaluate the innermost subexpressions first and build outward, exactly as "
             "you would evaluate an arithmetic expression."),
            ("A table settles the question completely",
             "If two formulas agree in every row they are equivalent, full stop. There "
             "is nothing further to check, because the rows are all the cases there are."),
        ],
        "read_title": "Building a truth table",
        "read_intro": "Rows first, then columns, then read the answer off the last one.",
        "body": [
            ("p", "A truth table for a formula with variables `p₁ … pₙ` has one row per "
                  "assignment of truth values to those variables. Since each variable "
                  "takes two values independently, there are `2ⁿ` rows &mdash; a fact "
                  "that is really the product rule of counting, which course 4 makes "
                  "explicit."),
            ("p", "The conventional row order lists `T` before `F` and varies the "
                  "rightmost variable fastest, so with two variables the rows read "
                  "`TT`, `TF`, `FT`, `FF`. Any order works; a consistent one lets two "
                  "tables be compared line by line."),
            ("def", ("Truth table",
                     "A table with one row per assignment of truth values to the "
                     "variables of a formula, and one column per subexpression, ending "
                     "with the value of the whole formula in that assignment.")),
            ("p", "The intermediate columns are not decoration. They are where a mistake "
                  "is caught: if the final column looks wrong, the subexpression columns "
                  "tell you exactly which step produced it."),
            ("example", ("Building `¬(p ∧ q)` step by step",
                         "First a column for `p ∧ q` (true in one row of four), then "
                         "negate it (true in three). Compare with the column for "
                         "`¬p ∨ ¬q`: same four values. That agreement is De Morgan's law, "
                         "and the table is its proof.")),
            ("thm", ("Truth tables are complete for propositional logic",
                     "Any question about a formula built from `¬ ∧ ∨ → ↔ ⊕` &mdash; is it "
                     "always true, is it ever true, is it equivalent to this other one "
                     "&mdash; is answered by its truth table. There is no propositional "
                     "question a table leaves open.")),
            ("p", "The catch is size, not correctness. Ten variables give 1024 rows and "
                  "twenty give over a million; deciding whether a large formula is "
                  "satisfiable is the canonical hard problem of computer science, and "
                  "course 8 returns to it by name."),
        ],
        "lab": ("truth_table", {
            "formulas": ["~(p & q)", "~p | ~q", "p -> q", "~p | q", "p & (q | r)",
                         "(p & q) | (p & r)", "(p | q) & r", "p | (q & r)"],
            "compare_with": "~p | ~q",
            "panel_title": "Build any table",
            "panel_intro": "Every subexpression gets its own column, evaluated inside "
                           "out. Type your own formula to see a table nobody prepared "
                           "in advance.",
        }),
        "steps_title": "Constructing a table by hand",
        "steps_intro": "Five minutes of setup saves the errors that come from improvising.",
        "steps": [
            ("Count the variables and write `2ⁿ` rows",
             "Three variables means eight rows. Getting this wrong at the start "
             "guarantees a wrong answer at the end."),
            ("Fill the variable columns systematically",
             "Rightmost alternates every row, next every two rows, next every four. "
             "The pattern makes a missing row visible."),
            ("Add one column per subexpression",
             "Innermost first. Each new column should depend only on columns already "
             "written."),
            ("Read the last column",
             "All `T` is a tautology, all `F` a contradiction, a mixture is contingent "
             "&mdash; the vocabulary of lesson 6."),
        ],
        "worked": {
            "title": "`p → (q ∨ r)`, in full",
            "intro": ["Three variables, so eight rows, and two subexpression columns."],
            "lines": [
                "p  q  r  |  q∨r  |  p → (q∨r)",
                "-------------------------------",
                "T  T  T  |   T   |     T",
                "T  T  F  |   T   |     T",
                "T  F  T  |   T   |     T",
                "T  F  F  |   F   |     F   ← the only false row",
                "F  T  T  |   T   |     T",
                "F  T  F  |   T   |     T",
                "F  F  T  |   T   |     T",
                "F  F  F  |   F   |     T   ← false hypothesis, true conditional",
            ],
            "after": [
                "Two rows deserve attention. Row 4 is the only way to make a conditional "
                "false: true hypothesis, false conclusion. Row 8 is the one that surprises "
                "people &mdash; `p` is false, so the conditional is true regardless of "
                "what `q ∨ r` does. Lesson 4 explains why that convention is the right one."
            ],
        },
        "quiz_title": "Reading and building tables",
        "quiz": [
            {"q": "How many rows does a truth table for a formula in four variables have?",
             "a": ["4", "8", "16", "It depends on the connectives"],
             "c": 2,
             "why": "`2⁴ = 16`. The number of rows depends only on the variable count; "
                    "the connectives determine the columns, not the rows."},
            {"q": "Two formulas have identical final columns. What follows?",
             "a": ["They are logically equivalent",
                   "They are both tautologies",
                   "They contain the same connectives",
                   "Nothing without checking more cases"],
             "c": 0,
             "why": "Agreement in every row is the definition of logical equivalence. "
                    "There are no further cases: the table already lists them all."},
            {"q": "Why are truth tables impractical for large formulas?",
             "a": ["They can give wrong answers",
                   "The number of rows grows exponentially in the variable count",
                   "Some connectives cannot be tabulated",
                   "They only work for two variables"],
             "c": 1,
             "why": "A table is always correct; it is `2ⁿ` rows. At `n = 30` that is over "
                    "a billion, which is why equivalence laws and, later, SAT solvers exist."},
        ],
        "mistakes": [
            ("Writing fewer than `2ⁿ` rows",
             "A missing row is a case you have not checked, and it is exactly the case "
             "that a counterexample tends to live in."),
            ("Evaluating outside in",
             "`¬(p ∧ q)` is not `¬p ∧ ¬q`. Building the inner column first makes that "
             "impossible to get wrong; jumping to the outer connective does not."),
            ("Reusing a row order inconsistently between two tables",
             "If you are comparing two formulas, the rows must be in the same order or "
             "the comparison is meaningless. The lab pins the order for this reason."),
        ],
        "standard": ("Finish when you can build a three-variable table without hesitating "
                     "over the row pattern.",
                     "Take `(p → q) ∧ (q → r)` and produce all eight rows with the two "
                     "conditionals as separate columns. If the row pattern is automatic, "
                     "the rest of this course is bookkeeping."),
        "note": "The lab's subexpression columns are generated from the parsed formula, "
                "so they appear in evaluation order rather than in an order someone chose. "
                "That is also why an ill-formed formula is rejected rather than guessed at.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "conditional-statements",
        "title": "The Conditional and Its Relatives",
        "module": "Propositional logic",
        "one_line": "If-then, converse, inverse, contrapositive, and vacuous truth.",
        "summary": (
            "`p → q` is false in exactly one case. Establish which, why a false "
            "hypothesis makes the whole conditional true, and how the converse, "
            "inverse and contrapositive relate &mdash; only one of the three is "
            "equivalent to the original."
        ),
        "key": [
            "p → q            false ONLY when p is T and q is F",
            "q → p            the CONVERSE          — not equivalent",
            "¬p → ¬q          the INVERSE           — not equivalent",
            "¬q → ¬p          the CONTRAPOSITIVE    — EQUIVALENT",
        ],
        "key_label": "One conditional, three relatives",
        "concepts_intro": (
            "The conditional is the connective every theorem is stated with, and the "
            "one whose truth table looks wrong until you see why it must be that way."
        ),
        "concepts": [
            ("One false row, three true ones",
             "`p → q` fails only when the hypothesis holds and the conclusion does not. "
             "Every other combination leaves the promise unbroken."),
            ("A false hypothesis makes it true",
             "This is <em>vacuous truth</em>. \"Every unicorn in this room is purple\" is "
             "true, because there is no unicorn here to be a counterexample."),
            ("Only the contrapositive is equivalent",
             "`p → q` and `¬q → ¬p` agree in all four rows. The converse and the inverse "
             "do not, and confusing either with the original is the most consequential "
             "error in this lesson."),
        ],
        "read_title": "If, then",
        "read_intro": "The definition, the reason for it, and the three statements it is confused with.",
        "body": [
            ("def", ("Conditional",
                     "`p → q` (\"if `p` then `q`\") is false when `p` is true and `q` is "
                     "false, and true in every other case. `p` is the "
                     "<strong>hypothesis</strong> (or antecedent) and `q` the "
                     "<strong>conclusion</strong> (consequent).")),
            ("p", "Think of a conditional as a promise: \"if you pass the exam, I will "
                  "buy you dinner.\" The promise is broken in exactly one situation "
                  "&mdash; you pass and no dinner appears. If you fail, the promise says "
                  "nothing about what happens and is not broken whichever way things go. "
                  "That is why both rows with a false hypothesis count as true."),
            ("def", ("Vacuous truth",
                     "A conditional whose hypothesis is false is <strong>vacuously "
                     "true</strong>. \"Every element of the empty set is prime\" is true, "
                     "and so is \"every element of the empty set is composite\".")),
            ("p", "Vacuous truth is not a loophole to be tolerated; it is what makes "
                  "general statements behave. \"Every prime greater than 100 that is even "
                  "is a perfect square\" has to be true, or a statement about a set could "
                  "fail merely because the set is empty."),
            ("def", ("Converse, inverse, contrapositive",
                     "Given `p → q`: the <strong>converse</strong> is `q → p`, the "
                     "<strong>inverse</strong> is `¬p → ¬q`, and the "
                     "<strong>contrapositive</strong> is `¬q → ¬p`.")),
            ("thm", ("Contraposition",
                     "`p → q ≡ ¬q → ¬p`. The converse and inverse are equivalent to each "
                     "other, and neither is equivalent to the original.")),
            ("proof", [
                "`p → q` is false only when `p` is T and `q` is F. `¬q → ¬p` is false "
                "only when `¬q` is T and `¬p` is F &mdash; that is, when `q` is F and `p` "
                "is T. Those are the same single row, so the two formulas are false in "
                "the same case and true in the other three.",
            ]),
            ("example", ("Why the converse is a different claim",
                         "\"If `n` is divisible by 4 then `n` is even\" is true. Its "
                         "converse, \"if `n` is even then `n` is divisible by 4\", is "
                         "false &mdash; take `n = 6`. Its contrapositive, \"if `n` is odd "
                         "then `n` is not divisible by 4\", is true, as it must be.")),
            ("def", ("Biconditional",
                     "`p ↔ q` (\"`p` if and only if `q`\") is true exactly when `p` and "
                     "`q` have the same truth value. It is equivalent to "
                     "`(p → q) ∧ (q → p)` &mdash; the statement and its converse together.")),
            ("p", "In a theorem, \"if and only if\" is an instruction: two proofs are "
                  "owed, one in each direction. Proving only one is the most common way "
                  "an otherwise correct answer is incomplete."),
        ],
        "lab": ("truth_table", {
            "formulas": ["p -> q", "q -> p", "~p -> ~q", "~q -> ~p", "~p | q",
                         "p <-> q", "(p -> q) & (q -> p)", "~(p & ~q)"],
            "compare_with": "~q -> ~p",
            "mode": "two",
            "panel_title": "Compare the four relatives",
            "panel_intro": "Set A to `p -> q` and step B through the converse, the "
                           "inverse and the contrapositive. Two of them are separated "
                           "from A by a row; one is not.",
        }),
        "steps_title": "Working with a conditional",
        "steps_intro": "Identify the parts before doing anything else.",
        "steps": [
            ("Find the hypothesis and the conclusion",
             "English hides them: \"`q` whenever `p`\", \"`p` only if `q`\" and \"`p` is "
             "sufficient for `q`\" all mean `p → q`. \"`p` if `q`\" means `q → p`."),
            ("Ask what would falsify it",
             "A conditional is refuted by one case with a true hypothesis and a false "
             "conclusion. If you cannot describe that case, you have not understood "
             "the claim."),
            ("Form the contrapositive when the hypothesis is awkward",
             "\"If `n²` is even then `n` is even\" is hard to attack directly; its "
             "contrapositive \"if `n` is odd then `n²` is odd\" falls out in one line. "
             "Lesson 13 makes this a method."),
            ("Never assume the converse",
             "Proving `p → q` gives you nothing about `q → p`. If you need both, say so "
             "and prove both."),
        ],
        "worked": {
            "title": "Four forms of one statement",
            "intro": ["Let `p` = \"`n` is divisible by 6\" and `q` = \"`n` is divisible by 3\"."],
            "lines": [
                "original         p → q     if 6 | n then 3 | n         TRUE",
                "converse         q → p     if 3 | n then 6 | n         FALSE  (n = 9)",
                "inverse         ¬p → ¬q    if 6 ∤ n then 3 ∤ n         FALSE  (n = 9)",
                "contrapositive  ¬q → ¬p    if 3 ∤ n then 6 ∤ n         TRUE",
            ],
            "after": [
                "The single value `n = 9` refutes both the converse and the inverse, "
                "which is not a coincidence: they are equivalent to each other, so any "
                "counterexample to one is a counterexample to the other."
            ],
        },
        "quiz_title": "Conditionals",
        "quiz": [
            {"q": "`p` is false and `q` is false. What is `p → q`?",
             "a": ["False", "True", "Undefined", "The same as `q → p`"],
             "c": 1,
             "why": "A conditional is false only when the hypothesis is true and the "
                    "conclusion false. Here the hypothesis is false, so the conditional "
                    "is vacuously true."},
            {"q": "Which statement is equivalent to \"if it rains, the match is cancelled\"?",
             "a": ["If the match is cancelled, it rained",
                   "If it does not rain, the match is not cancelled",
                   "If the match is not cancelled, it did not rain",
                   "It rains and the match is cancelled"],
             "c": 2,
             "why": "That is the contrapositive, `¬q → ¬p`, the only one of the three "
                    "relatives equivalent to the original. The first is the converse and "
                    "the second the inverse."},
            {"q": "\"`p` only if `q`\" translates to:",
             "a": ["`q → p`", "`p → q`", "`p ↔ q`", "`¬p ∨ ¬q`"],
             "c": 1,
             "why": "\"Only if\" marks the CONCLUSION, not the hypothesis: `p` holding "
                    "requires `q`. Compare \"`p` if `q`\", which is `q → p` &mdash; the "
                    "two English phrases point opposite ways."},
        ],
        "mistakes": [
            ("Affirming the converse",
             "From `p → q` and `q`, nothing follows about `p`. This is the error behind "
             "most bad reasoning from evidence, and lesson 11 names it as a fallacy."),
            ("Finding vacuous truth absurd and rejecting it",
             "It is a consequence of wanting `p → q` to be false only when the promise "
             "is broken. Any other convention makes universally quantified statements "
             "over empty sets behave badly."),
            ("Proving one direction of a biconditional",
             "`p ↔ q` is two conditionals. An \"if and only if\" answer with one argument "
             "in it is half an answer, however good that half is."),
        ],
        "standard": ("Finish when you can write all three relatives of a conditional and "
                     "say which is equivalent, without a table.",
                     "Given \"if a function is differentiable then it is continuous\", "
                     "produce the converse, inverse and contrapositive, and identify "
                     "which are true. The habit of forming the contrapositive is what "
                     "lesson 13 turns into a proof technique."),
        "note": "`p → q ≡ ¬p ∨ q` is worth memorising: it converts every conditional into "
                "a disjunction and is how conditionals are eliminated when a formula is "
                "put into the normal forms of lesson 7.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "logical-equivalence",
        "title": "Logical Equivalence",
        "module": "Propositional logic",
        "one_line": "When two formulas say the same thing, and the laws that rewrite one into the other.",
        "summary": (
            "Two formulas are equivalent when no assignment separates them. Prove it "
            "with a table or with a chain of named laws &mdash; De Morgan, "
            "distribution, absorption &mdash; and refute it with a single row."
        ),
        "key": [
            "p ≡ q    means    p ↔ q is a tautology",
            "¬(p ∧ q) ≡ ¬p ∨ ¬q               De Morgan",
            "¬(p ∨ q) ≡ ¬p ∧ ¬q               De Morgan",
            "p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)  distribution",
        ],
        "key_label": "Equivalence and three laws",
        "concepts_intro": (
            "Equivalence is the relation that lets a complicated formula be replaced by "
            "a simple one without changing what it claims."
        ),
        "concepts": [
            ("Equivalence means agreement in every row",
             "Not similar structure, not the same variables &mdash; the same truth value "
             "under every assignment. `p → q` and `¬p ∨ q` look nothing alike and are "
             "equivalent."),
            ("One row refutes it",
             "To disprove an equivalence you exhibit one assignment where the two differ. "
             "That is a complete disproof and needs no further argument."),
            ("The laws are shortcuts, not new facts",
             "Every law in this lesson could be verified by a truth table. Their value "
             "is that they let you transform a 32-row formula without writing 32 rows."),
        ],
        "read_title": "Equivalence and the laws",
        "read_intro": "The definition first, then the toolkit that follows from it.",
        "body": [
            ("def", ("Logical equivalence",
                     "Formulas `A` and `B` are <strong>logically equivalent</strong>, "
                     "written `A ≡ B`, when they have the same truth value under every "
                     "assignment &mdash; equivalently, when `A ↔ B` is a tautology.")),
            ("p", "Note that `≡` is not a connective. `A ≡ B` is a statement <em>about</em> "
                  "two formulas, made in ordinary mathematical language; `A ↔ B` is itself "
                  "a formula. The two are related exactly as stated in the definition."),
            ("h3", "The laws worth knowing by name"),
            ("math", [
                "identity        p ∧ T ≡ p              p ∨ F ≡ p",
                "domination      p ∨ T ≡ T              p ∧ F ≡ F",
                "idempotent      p ∧ p ≡ p              p ∨ p ≡ p",
                "double negation ¬¬p ≡ p",
                "commutative     p ∧ q ≡ q ∧ p          p ∨ q ≡ q ∨ p",
                "associative     (p ∧ q) ∧ r ≡ p ∧ (q ∧ r)",
                "distributive    p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)",
                "                p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)",
                "De Morgan       ¬(p ∧ q) ≡ ¬p ∨ ¬q     ¬(p ∨ q) ≡ ¬p ∧ ¬q",
                "absorption      p ∨ (p ∧ q) ≡ p        p ∧ (p ∨ q) ≡ p",
                "negation        p ∨ ¬p ≡ T             p ∧ ¬p ≡ F",
                "conditional     p → q ≡ ¬p ∨ q         ¬(p → q) ≡ p ∧ ¬q",
                "biconditional   p ↔ q ≡ (p → q) ∧ (q → p)",
            ]),
            ("p", "Two of these repay extra attention. <strong>De Morgan</strong> is how a "
                  "negation is pushed inward past a connective, and the connective flips "
                  "as it passes: `∧` becomes `∨` and back. <strong>Distribution</strong> "
                  "works in both directions here, unlike in arithmetic where "
                  "`a + (b × c)` is not `(a + b) × (a + c)`."),
            ("p", "The second distributive law is the one people doubt. Check it: at "
                  "`p = T` both sides are `T`; at `p = F` the left is `q ∧ r` and the "
                  "right is `q ∧ r`. It holds."),
            ("thm", ("Substitution",
                     "If `A ≡ B`, then replacing an occurrence of `A` inside a larger "
                     "formula by `B` produces an equivalent formula. This is what makes "
                     "chains of rewriting valid.")),
            ("example", ("Simplifying by chain",
                         "`¬(p → q) ≡ ¬(¬p ∨ q) ≡ ¬¬p ∧ ¬q ≡ p ∧ ¬q`. Three steps: "
                         "conditional law, De Morgan, double negation. The result says "
                         "what it should &mdash; a conditional fails exactly when the "
                         "hypothesis holds and the conclusion does not.")),
        ],
        "lab": ("truth_table", {
            "formulas": ["~(p & q)", "~p | ~q", "~(p | q)", "~p & ~q",
                         "p & (q | r)", "(p & q) | (p & r)", "p | (q & r)",
                         "(p | q) & (p | r)", "p | (p & q)", "p"],
            "compare_with": "~p | ~q",
            "mode": "two",
            "panel_title": "Prove or refute an equivalence",
            "panel_intro": "In compare mode the lab highlights any row that separates the "
                           "two formulas. No highlighted row means equivalent; one is a "
                           "complete disproof.",
        }),
        "steps_title": "Proving an equivalence",
        "steps_intro": "Two routes. Choose by the number of variables.",
        "steps": [
            ("Few variables? Build the table",
             "Up to three variables a table is eight rows and takes a minute. It cannot "
             "be wrong and needs no cleverness."),
            ("Many variables? Chain the laws",
             "Start from the more complicated side and rewrite toward the simpler one, "
             "naming the law used at each step."),
            ("Eliminate conditionals first",
             "Rewrite every `→` as `¬p ∨ q` and every `↔` as a conjunction of two "
             "conditionals. The remaining laws all speak `∧`, `∨`, `¬`."),
            ("To refute, hunt for one row",
             "Try to make one side true and the other false. Setting a variable to make "
             "the two sides disagree is usually easier than checking all rows."),
        ],
        "worked": {
            "title": "Show `(p → q) ∧ (p → r) ≡ p → (q ∧ r)`",
            "intro": ["Three variables, so a table would be eight rows. The chain is shorter."],
            "lines": [
                "(p → q) ∧ (p → r)",
                "  ≡ (¬p ∨ q) ∧ (¬p ∨ r)      conditional law, twice",
                "  ≡ ¬p ∨ (q ∧ r)             distribution (backwards)",
                "  ≡ p → (q ∧ r)              conditional law",
            ],
            "after": [
                "Read the result back into English: promising `q` and promising `r`, both "
                "on the same condition, is promising `q ∧ r` on that condition. The chain "
                "proves it; the sentence is why it should have been expected."
            ],
        },
        "quiz_title": "Equivalences",
        "quiz": [
            {"q": "`¬(p ∨ q)` is equivalent to:",
             "a": ["`¬p ∨ ¬q`", "`¬p ∧ ¬q`", "`p ∧ q`", "`¬p → q`"],
             "c": 1,
             "why": "De Morgan: the negation passes inward and the connective flips. "
                    "\"Not (`p` or `q`)\" is \"neither `p` nor `q`\"."},
            {"q": "You want to disprove `A ≡ B`. What is enough?",
             "a": ["Show they have different connectives",
                   "Show they differ in at least half the rows",
                   "Exhibit one assignment where their values differ",
                   "Show `A` is a tautology and `B` is not"],
             "c": 2,
             "why": "Equivalence requires agreement in every row, so one disagreeing row "
                    "refutes it completely. Nothing more is needed or helps."},
            {"q": "`¬(p → q)` simplifies to:",
             "a": ["`¬p → ¬q`", "`p ∧ ¬q`", "`¬p ∨ q`", "`q → p`"],
             "c": 1,
             "why": "A conditional fails exactly when its hypothesis holds and its "
                    "conclusion does not. By the laws: `¬(¬p ∨ q) ≡ p ∧ ¬q`."},
        ],
        "mistakes": [
            ("Negating both sides of a connective without flipping it",
             "`¬(p ∧ q)` is not `¬p ∧ ¬q`. The two differ in two of four rows, and De "
             "Morgan exists precisely to record the flip."),
            ("Treating `≡` as a connective inside a formula",
             "`p ≡ q` is a claim about two formulas; `p ↔ q` is a formula. Writing "
             "`(p ≡ q) ∧ r` is a category error."),
            ("Checking a few rows and concluding equivalence",
             "Agreement on the rows you looked at is not agreement on all of them. This "
             "is the same gap course 3 spends a whole course closing."),
        ],
        "standard": ("Finish when you can simplify a four-connective formula by named "
                     "laws and justify each step.",
                     "Take `¬(p ∨ (¬p ∧ q))` and reduce it to `¬p ∧ ¬q`, naming De Morgan, "
                     "distribution and negation as you use them. A step you cannot name "
                     "is a step you have guessed."),
        "note": "Every law above has a dual, obtained by swapping `∧` with `∨` and `T` "
                "with `F`. That symmetry is not a coincidence; lesson 7 makes it a "
                "structural fact about Boolean algebra.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "tautologies-and-satisfiability",
        "title": "Tautology, Contradiction, Satisfiability",
        "module": "Propositional logic",
        "one_line": "Always true, never true, and sometimes true.",
        "summary": (
            "Classify a formula by its final column: all true, all false, or mixed. "
            "Then meet satisfiability &mdash; the question of whether any assignment "
            "works &mdash; and why it is the problem computer science measures "
            "hardness against."
        ),
        "key": [
            "tautology      true under EVERY assignment          p ∨ ¬p",
            "contradiction  true under NO assignment             p ∧ ¬p",
            "contingent     true under some, false under others  p ∧ q",
            "satisfiable    true under at least one assignment",
        ],
        "key_label": "Three classes, one question",
        "concepts_intro": (
            "One column, three verdicts &mdash; and a fourth question that turns out to "
            "be the hard one."
        ),
        "concepts": [
            ("A tautology carries no information",
             "`p ∨ ¬p` is true whatever `p` says, so learning it tells you nothing about "
             "the world. That is exactly why tautologies are useful as reasoning steps."),
            ("Contradiction and negation are linked",
             "`A` is a contradiction exactly when `¬A` is a tautology. Every question "
             "about one is a question about the other."),
            ("Satisfiable is weaker than valid",
             "Satisfiable asks whether SOME row is true; tautology asks whether EVERY row "
             "is. Most useful formulas are satisfiable and not tautologies."),
        ],
        "read_title": "Classifying formulas",
        "read_intro": "The three classes, then the question that made this lesson famous.",
        "body": [
            ("def", ("Tautology, contradiction, contingency",
                     "A formula is a <strong>tautology</strong> if it is true under every "
                     "assignment, a <strong>contradiction</strong> if it is true under "
                     "none, and <strong>contingent</strong> otherwise.")),
            ("def", ("Satisfiability",
                     "A formula is <strong>satisfiable</strong> if at least one assignment "
                     "makes it true. Tautologies and contingent formulas are satisfiable; "
                     "contradictions are not.")),
            ("p", "The relationships are worth stating as a single sentence: `A` is a "
                  "tautology exactly when `¬A` is unsatisfiable, and `A` is satisfiable "
                  "exactly when `¬A` is not a tautology. Every one of these questions "
                  "reduces to any other, which is why an algorithm for one is an "
                  "algorithm for all."),
            ("thm", ("Equivalence as a tautology",
                     "`A ≡ B` if and only if `A ↔ B` is a tautology. Lesson 5's whole "
                     "subject is therefore a special case of this lesson's.")),
            ("p", "Deciding satisfiability by truth table takes `2ⁿ` rows. For a formula "
                  "with 100 variables &mdash; small by the standards of real applications "
                  "&mdash; that is more rows than there are atoms in the observable "
                  "universe, and no faster general method is known."),
            ("thm", ("SAT is NP-complete (Cook, 1971)",
                     "The problem of deciding whether a propositional formula is "
                     "satisfiable was the first problem shown NP-complete. Course 8 "
                     "defines the term; what matters here is that this lesson's innocent "
                     "question is the reference point against which computational "
                     "hardness is measured.")),
            ("p", "The practical situation is stranger than the theory suggests. Modern "
                  "SAT solvers routinely handle formulas with millions of variables, "
                  "because real instances have structure that the worst case does not. "
                  "Hardness in the worst case and difficulty in practice are different "
                  "claims."),
            ("example", ("Classifying three formulas",
                         "`(p → q) ∨ (q → p)` is a tautology &mdash; check all four rows. "
                         "`(p ↔ q) ∧ (p ⊕ q)` is a contradiction, since the two conjuncts "
                         "are negations of each other. `p → (q ∧ r)` is contingent.")),
        ],
        "lab": ("truth_table", {
            "formulas": ["p | ~p", "p & ~p", "(p -> q) | (q -> p)", "(p -> q) & (p & ~q)",
                         "((p -> q) & p) -> q", "((p -> q) & q) -> p",
                         "(p & q) -> p", "p -> (p | q)", "(p <-> q) & (p ^ q)"],
            "panel_title": "Classify a formula",
            "panel_intro": "The verdict is computed by counting the true rows: all of "
                           "them, none of them, or some. Try `((p -> q) & q) -> p` "
                           "&mdash; it looks like a valid inference and is not one.",
        }),
        "steps_title": "Classifying a formula",
        "steps_intro": "Look for a shortcut before writing `2ⁿ` rows.",
        "steps": [
            ("Try to make it false",
             "To test for a tautology, assume the whole formula is false and work "
             "backwards. If that forces a contradiction, it is a tautology."),
            ("Try to make it true",
             "To test satisfiability, look for one assignment. Finding it ends the "
             "question; a table is only needed when you fail."),
            ("Use the structure",
             "A disjunction is satisfiable if either side is; a conjunction is a "
             "contradiction if either side is. Half the work is often unnecessary."),
            ("Fall back on the table",
             "When the shortcuts do not settle it, `2ⁿ` rows always will. Correctness "
             "beats elegance when the answer matters."),
        ],
        "worked": {
            "title": "Is `((p → q) ∧ ¬q) → ¬p` a tautology?",
            "intro": ["Assume it is false and see whether that is possible."],
            "lines": [
                "Suppose the whole conditional is FALSE.",
                "  then  (p → q) ∧ ¬q   is T     and   ¬p   is F",
                "  ¬p = F               ⟹   p = T",
                "  (p → q) ∧ ¬q = T     ⟹   p → q = T  and  ¬q = T",
                "  ¬q = T               ⟹   q = F",
                "  p = T, q = F         ⟹   p → q = F      CONTRADICTION",
                "No assignment makes it false, so it is a TAUTOLOGY.",
            ],
            "after": [
                "This tautology has a name: <em>modus tollens</em>, the inference rule of "
                "lesson 11. Every valid rule of inference is a tautology in exactly this "
                "shape &mdash; premises conjoined, implying the conclusion."
            ],
        },
        "quiz_title": "Classification",
        "quiz": [
            {"q": "`A` is a contradiction. What is `¬A`?",
             "a": ["A contradiction", "Contingent", "A tautology",
                   "Satisfiable but not a tautology"],
             "c": 2,
             "why": "`A` is false in every row, so `¬A` is true in every row. The two "
                    "questions are the same question."},
            {"q": "Which is true of every contingent formula?",
             "a": ["It is satisfiable and not a tautology",
                   "It is a tautology", "It is unsatisfiable",
                   "Its negation is a contradiction"],
             "c": 0,
             "why": "Contingent means at least one true row and at least one false row: "
                    "satisfiable, but not valid."},
            {"q": "Why is deciding satisfiability hard in general?",
             "a": ["Some formulas have no truth table",
                   "The number of assignments grows as `2ⁿ`, and no generally faster method is known",
                   "Truth tables give wrong answers for large formulas",
                   "Satisfiability is undecidable"],
             "c": 1,
             "why": "It is perfectly decidable &mdash; just exponentially so by the "
                    "obvious method. Undecidability is a different phenomenon, and course "
                    "8 lesson 12 meets it."},
        ],
        "mistakes": [
            ("Confusing satisfiable with true",
             "A satisfiable formula is one that <em>could</em> be true. Whether it is "
             "true depends on the assignment, which the formula alone does not fix."),
            ("Assuming a tautology says something",
             "Tautologies are exactly the formulas that carry no information about the "
             "world. Their usefulness lies in being safe to assert, not in being informative."),
            ("Reading NP-complete as \"impossible\"",
             "It is a statement about worst-case scaling. SAT solvers handle industrial "
             "instances with millions of variables every day."),
        ],
        "standard": ("Finish when you can settle a tautology claim by assuming it false.",
                     "Take `(p ∨ q) → (p ∧ q)` and decide its class without a full table, "
                     "by trying to construct a falsifying assignment. You should find one "
                     "in two lines &mdash; and be able to say which row it is."),
        "note": "The lab reports the count of satisfying rows, not only the verdict. That "
                "count is the number of models of the formula, and counting models is a "
                "strictly harder problem than deciding whether one exists.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "normal-forms-and-boolean-algebra",
        "title": "Normal Forms and Boolean Algebra",
        "module": "Propositional logic",
        "one_line": "Every formula rewritten into one of two standard shapes.",
        "summary": (
            "Disjunctive and conjunctive normal form give every formula a canonical "
            "shape, readable straight off its truth table. The same algebra runs "
            "digital circuits, which is why `∧`, `∨` and `¬` are AND, OR and NOT gates."
        ),
        "key": [
            "DNF   (p ∧ ¬q) ∨ (¬p ∧ q)      an OR of ANDs  — read off the TRUE rows",
            "CNF   (p ∨ q) ∧ (¬p ∨ ¬q)      an AND of ORs  — read off the FALSE rows",
            "Every formula has both. {∧, ∨, ¬} is functionally complete.",
        ],
        "key_label": "Two shapes, one formula",
        "concepts_intro": (
            "A normal form is a standard shape. Its value is that any formula can be put "
            "into it, so two formulas can be compared structurally."
        ),
        "concepts": [
            ("DNF is read off the true rows",
             "For each row where the formula is true, write the conjunction that "
             "describes that row; join them with `∨`. The result is equivalent by "
             "construction."),
            ("CNF is read off the false rows",
             "For each false row, write a disjunction ruling that row out; join them "
             "with `∧`. This is the form SAT solvers consume."),
            ("Three connectives suffice",
             "`{∧, ∨, ¬}` can express every truth function. So can `{∧, ¬}` alone, and "
             "remarkably so can NAND by itself."),
        ],
        "read_title": "Canonical forms",
        "read_intro": "How to produce each from a truth table, and why it always works.",
        "body": [
            ("def", ("Literal, clause, term",
                     "A <strong>literal</strong> is a variable or its negation (`p`, `¬q`). "
                     "A <strong>clause</strong> is a disjunction of literals; a "
                     "<strong>term</strong> is a conjunction of literals.")),
            ("def", ("Disjunctive normal form",
                     "A formula is in <strong>DNF</strong> when it is a disjunction of "
                     "terms &mdash; an OR of ANDs of literals.")),
            ("def", ("Conjunctive normal form",
                     "A formula is in <strong>CNF</strong> when it is a conjunction of "
                     "clauses &mdash; an AND of ORs of literals.")),
            ("thm", ("Every formula has a DNF and a CNF",
                     "Given any truth table, an equivalent DNF and an equivalent CNF can "
                     "be written down directly from it.")),
            ("proof", [
                "For DNF: take each row where the formula is true, and write the "
                "conjunction of literals that is true in exactly that row &mdash; `p` if "
                "`p` is `T` there, `¬p` if it is `F`. Each such term is true in one row "
                "and false in every other. Their disjunction is therefore true in exactly "
                "the rows where the original is true.",
                "For CNF, do the same with the false rows and take the complementary "
                "clause for each: the clause is false in exactly that row and true "
                "everywhere else, so the conjunction is false in exactly the rows where "
                "the original is false.",
                "If the formula has no true rows it is a contradiction and its DNF is "
                "empty, conventionally `F`; if it has no false rows its CNF is `T`.",
            ]),
            ("example", ("Reading DNF off a table",
                         "Suppose a formula in `p`, `q` is true exactly in rows `TF` and "
                         "`FT`. Its DNF is `(p ∧ ¬q) ∨ (¬p ∧ q)`, which is exactly "
                         "`p ⊕ q` &mdash; and this is how any truth function whatever "
                         "gets a formula.")),
            ("h3", "Functional completeness"),
            ("def", ("Functionally complete",
                     "A set of connectives is <strong>functionally complete</strong> if "
                     "every truth function can be expressed using only those connectives.")),
            ("p", "`{∧, ∨, ¬}` is functionally complete, by the theorem above. `{∧, ¬}` is "
                  "too, because De Morgan gives `p ∨ q ≡ ¬(¬p ∧ ¬q)`; symmetrically so is "
                  "`{∨, ¬}`. What is striking is that a single connective can suffice: "
                  "NAND, written `p ↑ q ≡ ¬(p ∧ q)`, expresses negation as `p ↑ p` and "
                  "conjunction as `(p ↑ q) ↑ (p ↑ q)`."),
            ("h3", "The same algebra, in hardware"),
            ("p", "Replace `T` with 1, `F` with 0, `∧` with AND, `∨` with OR and `¬` with "
                  "NOT, and every law of lesson 5 becomes a fact about digital circuits. "
                  "A formula in DNF is a two-level circuit: a layer of AND gates feeding "
                  "one OR gate. That correspondence is why NAND being functionally "
                  "complete matters commercially &mdash; a chip can be built from one "
                  "kind of gate."),
            ("p", "The two-level DNF circuit is fast and often enormous. Minimising it "
                  "&mdash; finding the smallest equivalent formula &mdash; is its own "
                  "hard problem, and is what Karnaugh maps and the Quine&ndash;McCluskey "
                  "algorithm address."),
        ],
        "lab": ("truth_table", {
            "formulas": ["p ^ q", "(p & ~q) | (~p & q)", "(p | q) & (~p | ~q)",
                         "p -> q", "~p | q", "(p | ~p) & (~p | q)",
                         "p <-> q", "(p & q) | (~p & ~q)"],
            "compare_with": "(p & ~q) | (~p & q)",
            "mode": "two",
            "panel_title": "A formula and its normal form",
            "panel_intro": "Each pair here is a formula beside its DNF or CNF. They are "
                           "equivalent by construction, so no row should separate them "
                           "&mdash; verify that rather than take it on trust.",
        }),
        "steps_title": "Producing a normal form",
        "steps_intro": "From a formula, either go through the table or push negations inward.",
        "steps": [
            ("Build the truth table",
             "The table route always works and needs no cleverness. Its cost is `2ⁿ` "
             "rows, and its output may be far from minimal."),
            ("For DNF, take the true rows",
             "One term per true row, each literal positive where the variable is `T` and "
             "negated where it is `F`. Join with `∨`."),
            ("For CNF, take the false rows",
             "One clause per false row, each literal negated relative to the row. Join "
             "with `∧`. Getting this polarity backwards is the standard slip."),
            ("Or transform algebraically",
             "Eliminate `→` and `↔`, push negations in with De Morgan until they sit on "
             "variables, then distribute. This can be much shorter, and can also blow up."),
        ],
        "worked": {
            "title": "CNF of `p → (q ∧ r)`",
            "intro": ["The algebraic route, since the table would be eight rows."],
            "lines": [
                "p → (q ∧ r)",
                "  ≡ ¬p ∨ (q ∧ r)          conditional law",
                "  ≡ (¬p ∨ q) ∧ (¬p ∨ r)   distribution",
                "",
                "Two clauses, each a disjunction of literals — this is CNF.",
                "Check one row: p = T, q = T, r = F",
                "  original     T → (T ∧ F) = T → F = F",
                "  CNF          (F ∨ T) ∧ (F ∨ F) = T ∧ F = F      agree",
            ],
            "after": [
                "Spot-checking a single row does not prove the equivalence &mdash; the "
                "chain of named laws does that. The check is there to catch a slip in the "
                "chain, which is a different job and worth doing every time."
            ],
        },
        "quiz_title": "Normal forms",
        "quiz": [
            {"q": "A formula is true in exactly two of its four rows. How many terms does its canonical DNF have?",
             "a": ["One", "Two", "Four", "It depends on the connectives"],
             "c": 1,
             "why": "The canonical DNF has one term per TRUE row. Two true rows give two "
                    "terms joined by `∨`."},
            {"q": "Which set of connectives is NOT functionally complete?",
             "a": ["`{∧, ¬}`", "`{∨, ¬}`", "`{∧, ∨}`", "`{NAND}`"],
             "c": 2,
             "why": "Without negation you cannot express `¬p`: any formula built from `∧` "
                    "and `∨` alone is true when all variables are true, so it cannot be "
                    "false there."},
            {"q": "CNF is the input format for SAT solvers because:",
             "a": ["It is always shorter than DNF",
                   "Satisfiability of a CNF is trivial",
                   "Every clause must be satisfied, which gives a uniform constraint structure",
                   "DNF cannot represent all formulas"],
             "c": 2,
             "why": "A CNF is satisfied only when every clause has a true literal, which "
                    "is a clean constraint the solver propagates. Note satisfiability of "
                    "a DNF <em>is</em> trivial &mdash; check one term &mdash; but "
                    "converting to DNF can blow up exponentially."},
        ],
        "mistakes": [
            ("Getting the polarity backwards in CNF",
             "For a false row, a variable that is `T` in that row contributes the "
             "NEGATIVE literal. Reversing this produces a formula false in all the wrong "
             "places."),
            ("Assuming the canonical form is minimal",
             "The canonical DNF of a formula true in seven of eight rows has seven terms; "
             "an equivalent one-term formula may exist. Canonical and small are different "
             "goals."),
            ("Believing conversion is always cheap",
             "Converting CNF to DNF can multiply the size exponentially. That the two "
             "forms always exist says nothing about the cost of getting between them."),
        ],
        "standard": ("Finish when you can write both normal forms of a three-variable "
                     "formula from its table.",
                     "Take `(p ⊕ q) ∧ r`, build the table, and produce the canonical DNF "
                     "and CNF. Check the term count against the number of true and false "
                     "rows &mdash; they must match exactly."),
        "note": "Course 8's discussion of NP-completeness uses CNF-SAT specifically. The "
                "restriction to CNF costs nothing there, because any formula can be "
                "converted to an equisatisfiable CNF in linear time by naming its "
                "subformulas &mdash; the Tseytin transformation.",
    },
]
