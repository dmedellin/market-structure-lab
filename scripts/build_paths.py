#!/usr/bin/env python3
"""Render every generated path into site/.

    python3 scripts/build_paths.py            # write the pages
    python3 scripts/build_paths.py --check    # fail if any page would change

--check is what CI runs. The content is the source and the pages are derived, so
a page edited by hand is a page that will be silently reverted the next time
anyone builds; failing loudly is the only honest alternative.

A new generated path is one import and one entry in GENERATED_PATHS below. It is
deliberately not a discovery scan of content/: the set of published paths is a
decision, and it should be readable in one place rather than inferred from which
directories happen to exist.
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "content"))
sys.dont_write_bytecode = True

from algebra import PATH as ALGEBRA_PATH  # noqa: E402
from discrete_math import PATH as DISCRETE_MATH_PATH  # noqa: E402
from mathpath import render  # noqa: E402

GENERATED_PATHS = (DISCRETE_MATH_PATH, ALGEBRA_PATH)

SITE = REPO_ROOT / "site"
# The list of pages this build produces, consumed by scripts/labcheck.js.
MANIFEST = REPO_ROOT / "scripts" / "generated-pages.txt"


def path_pages(path):
    """[(relative path under site/, markup)] for one path."""
    out = [("paths/%s/index.html" % path["slug"], render.path_page(path))]
    courses = path["courses"]
    for index, course in enumerate(courses):
        out.append((
            "%s/index.html" % course["slug"],
            render.course_home(course=course, index=index, courses=courses, path=path),
        ))
        lessons = course["lessons"]
        for position, lesson in enumerate(lessons):
            out.append((
                "%s/%s/index.html" % (course["slug"], lesson["slug"]),
                render.lesson_page(
                    path=path,
                    course=course,
                    lesson=lesson,
                    index=position,
                    prev_lesson=lessons[position - 1] if position else None,
                    next_lesson=lessons[position + 1] if position + 1 < len(lessons) else None,
                ),
            ))
    return out


def pages():
    """[(relative path under site/, markup)] for every generated path."""
    out = []
    for path in GENERATED_PATHS:
        out.extend(path_pages(path))
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="do not write; exit non-zero if any page differs")
    args = parser.parse_args(argv)

    built = pages()

    # The manifest scripts/labcheck.js consumes. It is derived from the same
    # page list, so the harness can never drift from what was built -- and it is
    # what lets --generated mean "the pages this harness was written for" rather
    # than "every page in the repository". The trading path's widgets use DOM
    # features the harness deliberately does not implement, and reporting them
    # as failures would be reporting a limitation of the harness as a defect in
    # those pages.
    manifest = MANIFEST
    manifest_body = "\n".join("site/" + relative for relative, _m in built) + "\n"

    changed, written, manifest_written = [], 0, 0
    current_manifest = manifest.read_text(encoding="utf-8") if manifest.is_file() else None
    if current_manifest != manifest_body:
        changed.append(str(manifest.relative_to(REPO_ROOT)))
        if not args.check:
            manifest.write_text(manifest_body, encoding="utf-8")
            manifest_written = 1
    for relative, markup in built:
        target = SITE / relative
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current == markup:
            continue
        changed.append(relative)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(markup, encoding="utf-8")
            written += 1

    for path in GENERATED_PATHS:
        total_lessons = sum(len(c["lessons"]) for c in path["courses"])
        print("%s: %d courses, %d lessons"
              % (path["title"], len(path["courses"]), total_lessons))
    print("%d generated pages in total" % len(built))
    if args.check:
        if changed:
            print("OUT OF DATE (%d page(s)); run scripts/build_paths.py:" % len(changed))
            for relative in changed[:20]:
                print("  %s" % relative)
            if len(changed) > 20:
                print("  ... and %d more" % (len(changed) - 20))
            return 1
        print("every published page matches the content in content/")
        return 0
    # The manifest is counted apart from the pages: folding it in made this line
    # report "-1 already current" on a full rebuild.
    print("wrote %d page(s), %d already current%s"
          % (written, len(built) - written,
             "; manifest updated" if manifest_written else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
