# .github/ — CI, Pages and Release

Root `AGENTS.md` applies.

Model: **frontier tier** (`codex -p deep`). A workflow change is not verifiable
by the local suite, and a broken one blocks every subsequent change.

**Some invariants exist ONLY here.** The local suite will not catch them —
"exactly one `<title>` per document" is one, and an SVG `<title>` violates it.
That failure was found by pushing, which is the expensive way. Run the workflow's
own steps locally first:

    python3 -c "
    import yaml, subprocess
    d = yaml.safe_load(open('.github/workflows/ci.yml'))
    for s in [x for x in d['jobs']['site']['steps'] if 'run' in x and x.get('name')]:
        r = subprocess.run(['bash','-c',s['run']], capture_output=True, text=True, env={'WEB_ROOT':'site'})
        print(('OK   ' if r.returncode==0 else 'FAIL ') + s['name'])"

Shell blocks inside YAML are the other recurring failure: a `for page in` broken
across lines destroys the continuation. Check with `bash -n` before pushing.

`ci.yml` runs on pull request and on the merged commit; `release.yml` calls it so
a protected-main build cannot publish unless the same commit passed the same
checks. Do not weaken that arrangement to make a check easier.
