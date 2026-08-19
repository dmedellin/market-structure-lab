# content/ — the data the generated paths are rendered from

Root `AGENTS.md` applies. This adds what is specific to this directory.

`content/discrete_math/` and `content/algebra/` are the SOURCE. The pages under
those course slugs in `site/` are output — **editing a published page there is
reverted by the next build**, so the change appears to work and then vanishes.

Model: **balanced tier** (`gpt-5.6-terra`, or `codex -p build`). Volume work with
real gates behind it — `mathcheck.js` and `labcheck.js` will catch an arithmetic
or lab-mode mistake, which is why this does not need the frontier tier.

## Shape a lesson to what the renderer draws

Three concepts, four method steps, three mistakes, with a little room where a
lesson earns it. `TestLessonDataMatchesTheRenderer` enforces the range. A lesson
supplying two concepts still renders — lopsidedly, on one page out of hundreds.

## The two failures that keep recurring

**A distractor that is also true.** `3/√3` and `√3` are the same number;
`aₙ = 2n−1 for n ≥ 1` and the same rule with an explicit `a₁` describe the same
sequence. Before committing a question, try to argue for each wrong answer. If
you can, rewrite it.

**A lab mode that does not exist.** A lesson naming an unknown mode silently
renders the lab kit's default — the page looks finished and teaches the wrong
thing. `labcheck.js` catches this.

## Adding a lesson

Add the dict, run `python3 scripts/build_paths.py`, then add the URL to the five
declarations named in root `AGENTS.md` §1. The suite tells you which are missing.
