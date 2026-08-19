#!/usr/bin/env python3
"""Give the trading path the completion marks the generated paths already have.

WHY THIS IS A PATCHER AND NOT A RENDERER. The two mathematics paths are
generated from data by build_paths.py, so their lesson pages get the completion
toggle for free. The eight trading courses predate that machinery: their 129
pages are hand-written and there is no generator to re-run. Rewriting them as
data would be a different and much larger change, and would risk the material.
So this edits them in place, and is written to be run again safely.

IDEMPOTENCE IS THE WHOLE DESIGN. A previous in-place patcher in this repo
(register_labs.py) matched only the first line of the statement it was editing
and mangled the file on its second run. Every insertion here is therefore
delimited by an explicit marker and REPLACED rather than appended:

    CSS     /* progress-marks:begin */ ... /* progress-marks:end */
    script  <script data-progress-marks> ... </script>
    markup  identified by id="progressToggle", class="topbar-actions",
            data-lesson= and data-course=

Running it twice must produce a file identical to running it once, and the test
suite checks exactly that.

WHERE THE INVENTORY COMES FROM. The published pages themselves: the path page
lists the courses in order, and each course home lists its lessons in order.
Nothing is re-declared here, so there is no second copy to drift -- a lesson is
in the inventory precisely because a course home links to it.
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mathpath import feedback, progress  # noqa: E402

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PATH_PAGE = "paths/trading/index.html"

CSS_BEGIN = "/* progress-marks:begin */"
CSS_END = "/* progress-marks:end */"
SCRIPT_OPEN = "<script data-progress-marks>"
SCRIPT_CLOSE = "</script>"

SIGNIN_TITLE = ("Optional. Signing in carries your completion ticks to your other "
                "devices; it unlocks nothing, because nothing here is locked.")


# --- the styles these pages do not have ------------------------------------
# Values are copied from mathpath/theme.py so a trading lesson's control is the
# same control a mathematics lesson has, not a lookalike. The custom properties
# used here (--line, --line-strong, --panel, --panel-2, --text, --muted, --cyan,
# --green, --on-accent) are all defined by these pages already, in all three
# palette blocks; that was checked rather than assumed.
CSS = feedback.CSS + """
    .progress-bar {
      display: flex;
      flex-direction: column;
      gap: 7px;
      margin-top: 22px;
      padding: 15px 17px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel-2);
    }
    .progress-toggle {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      align-self: flex-start;
      padding: 10px 16px;
      border: 1px solid var(--line-strong);
      border-radius: 10px;
      background: var(--panel);
      color: var(--text);
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }
    .progress-toggle:hover { border-color: var(--cyan); }
    .progress-toggle .progress-tick {
      display: grid;
      place-items: center;
      width: 20px;
      height: 20px;
      border-radius: 6px;
      border: 1px solid var(--line-strong);
      background: var(--panel-2);
      color: transparent;
      font-size: 0.8rem;
      font-weight: 900;
    }
    .progress-toggle.is-done { border-color: var(--green); color: var(--green); }
    .progress-toggle.is-done .progress-tick {
      border-color: var(--green);
      background: var(--green);
      color: var(--on-accent);
    }
    .progress-note { margin: 0; color: var(--muted); font-size: 0.82rem; }
    .progress-note a { color: var(--cyan); }

    .course-progress {
      margin: 0 0 13px;
      color: var(--muted);
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    /* A finished lesson on a course home, and a finished course on the path
       page. Both are a tick and a border -- never a change of size, because a
       card that grows when marked makes the page jump under the reader. */
    .lesson-card.is-done { border-color: var(--green); }
    .lesson-card.is-done .lesson-ord::after {
      content: " \\2713";
      color: var(--green);
      font-weight: 900;
    }
    .course-card.is-complete { border-color: var(--green); }
    .course-progress-note {
      display: block;
      margin-top: 9px;
      color: var(--green);
      font-size: 0.82rem;
      font-weight: 750;
    }
    .course-progress-note:empty { display: none; }

    .topbar-actions { display: flex; align-items: center; gap: 8px; flex: none; }
    .signin-btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      flex: none;
      padding: 0 12px;
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 11px;
      background: var(--panel-2);
      color: var(--muted);
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 650;
      white-space: nowrap;
    }
    .signin-btn:hover { color: var(--text); border-color: var(--line-strong); }
    .signin-mark { font-size: 0.6rem; line-height: 1; color: var(--line-strong); }
    .signin-btn.is-in .signin-mark { color: var(--green); }
    @media (max-width: 560px) {
      .signin-label { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); clip-path: inset(50%); white-space: nowrap; }
      .signin-btn { padding: 0; width: 38px; justify-content: center; }
    }
"""

# --- the scripts -----------------------------------------------------------
# Byte-for-byte the same behaviour as mathpath/progress.py: the same storage
# key, the same date format, the same shape of stored value. A tick made on a
# trading lesson and a tick made on an algebra lesson have to be the same kind
# of thing, because /progress/ counts them together.
COURSE_JS = """
  (function () {
    if (!window.learnProgress) return;
    var out = document.getElementById('courseProgress');
    var items = [].slice.call(document.querySelectorAll('[data-lesson]'));
    if (!items.length) return;
    function paint() {
      var n = 0;
      items.forEach(function (item) {
        var on = window.learnProgress.done(item.getAttribute('data-lesson'));
        item.classList.toggle('is-done', on);
        if (on) n += 1;
      });
      if (out) {
        out.textContent = n === 0
          ? 'None of the ' + items.length + ' lessons marked complete'
          : n + ' of ' + items.length + ' lessons marked complete';
      }
    }
    paint();
    window.addEventListener('storage', paint);
  })();
"""

PATH_JS = """
  (function () {
    if (!window.learnProgress) return;
    var marks = window.learnProgress.read();
    [].slice.call(document.querySelectorAll('[data-course]')).forEach(function (item) {
      var slug = item.getAttribute('data-course');
      var total = parseInt(item.getAttribute('data-lessons'), 10) || 0;
      var n = Object.keys(marks).filter(function (k) { return k.indexOf(slug + '/') === 0; }).length;
      var out = item.querySelector('.course-progress-note');
      if (!out || !total) return;
      out.textContent = n ? n + ' of ' + total + ' lessons marked complete' : '';
      item.classList.toggle('is-complete', n >= total);
    });
  })();
"""

SIGNIN_JS = """
  (function () {
    var a = document.getElementById('signinLink');
    if (!a) return;
    var s = null;
    try { s = JSON.parse(sessionStorage.getItem('learn-auth') || 'null'); }
    catch (e) { return; }
    if (!s || !s.access_token) return;
    var label = document.getElementById('signinLabel');
    var name = null;
    try {
      if (s.id_token) {
        var c = JSON.parse(atob(s.id_token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
        name = c.name || c.preferred_username || null;
      }
    } catch (e) { name = null; }
    if (label) label.textContent = name ? String(name).split(' ')[0] : 'Signed in';
    a.setAttribute('title', (name ? 'Signed in as ' + name : 'Signed in')
      + '. Your completion ticks can follow you to another device.');
    a.classList.add('is-in');
  })();
"""


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def up_to_root(relative):
    """The relative prefix that reaches site/ from a page's own directory."""
    depth = len(pathlib.PurePosixPath(relative).parent.parts)
    return "../" * depth


# --- inventory, read out of the published pages ----------------------------
def strip_tags(fragment):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment)).strip()


def trading_inventory():
    text = (SITE / PATH_PAGE).read_text(encoding="utf-8")
    courses = []
    for card in re.finditer(r'<article class="course-card"[^>]*>(.*?)</article>', text, re.S):
        link = re.search(r'<h3><a href="\.\./\.\./([a-z0-9-]+)/">(.*?)</a></h3>', card.group(1), re.S)
        if not link:
            continue
        slug = link.group(1)
        courses.append({
            "slug": slug,
            "title": strip_tags(link.group(2)),
            "lessons": course_lessons(slug),
        })
    return courses


def course_lessons(slug):
    text = (SITE / slug / "index.html").read_text(encoding="utf-8")
    lessons = []
    for card in re.finditer(r'<article class="lesson-card"[^>]*>(.*?)</article>', text, re.S):
        link = re.search(r'<a class="lesson-link" href="\./([a-z0-9-]+)/">(.*?)</a>',
                         card.group(1), re.S)
        if not link:
            continue
        label = re.sub(r'<span class="lesson-ord">.*?</span>', "", link.group(2), flags=re.S)
        lessons.append({"slug": link.group(1), "title": strip_tags(label)})
    return lessons


# --- the four edits, each replacing its own marked region ------------------
def ensure_css(text):
    block = "%s%s    %s" % (CSS_BEGIN, CSS, CSS_END)
    # An existing block is REMOVED and re-inserted, never edited where it sits.
    # Editing in place cannot fix a block that is in the wrong place, and the
    # first version of this patcher put it in one -- so a rerun would have kept
    # the whole feature inside <noscript> forever. Removal restores the file to
    # its unpatched text, which is what keeps this idempotent.
    text = re.sub(r"[ \t]*" + re.escape(CSS_BEGIN) + r".*?" + re.escape(CSS_END) + r"\n?",
                  lambda _m: "", text, flags=re.S)
    # The FIRST style block -- the page's own stylesheet. NOT the last: every
    # one of these pages ends with a <noscript><style> that hides the theme
    # toggle, and rules put there apply only when scripting is OFF. The first
    # version of this patcher used rfind and buried the whole feature in that
    # block, so the toggle and the feedback panel rendered unstyled for every
    # reader who had JavaScript on -- which is everyone who can use them.
    marker = text.find("</style>")
    if marker == -1:
        raise SystemExit("no <style> block to extend")
    # Insert as WHOLE LINES before the closing tag's own line, so the </style>
    # line keeps the indentation it came with. Inserting at the tag itself made
    # the block's column depend on that indentation, while removal above eats
    # it -- so the first rerun moved the block by two spaces and only then
    # settled. Idempotent from the first run is the requirement, not eventually.
    line_start = text.rfind("\n", 0, marker) + 1
    return text[:line_start] + "    " + block + "\n" + text[line_start:]


def ensure_script(text, body):
    block = SCRIPT_OPEN + body + "  " + SCRIPT_CLOSE + "\n"
    if SCRIPT_OPEN in text:
        return re.sub(re.escape(SCRIPT_OPEN) + r".*?" + re.escape(SCRIPT_CLOSE),
                      lambda _m: block.rstrip("\n"), text, count=1, flags=re.S)
    marker = text.rfind("</body>")
    if marker == -1:
        raise SystemExit("no </body> to precede")
    return text[:marker] + "  " + block + text[marker:]


def ensure_masthead(text, relative):
    """The sign-in control, beside the theme toggle, inside one grouped child.

    The masthead is justify-content: space-between, so a bare extra child is
    spread into open space rather than sitting next to the toggle.
    """
    href = up_to_root(relative) + "progress/"
    link = ('<a class="signin-btn" id="signinLink" href="%s" title="%s">'
            '<span class="signin-mark" aria-hidden="true">&#9679;</span>'
            '<span class="signin-label" id="signinLabel">Sign in</span></a>'
            % (esc(href), esc(SIGNIN_TITLE)))
    toggle = re.search(r'<button class="icon-btn" id="themeToggle".*?</button>', text, re.S)
    if toggle is None:
        raise SystemExit("no theme toggle in the masthead")
    if 'class="topbar-actions"' in text:
        # Already grouped: only refresh the link, so a moved page gets the right depth.
        return re.sub(r'<a class="signin-btn" id="signinLink".*?</a>',
                      lambda _m: link, text, count=1, flags=re.S)
    group = '<div class="topbar-actions">%s%s</div>' % (link, toggle.group(0))
    return text[:toggle.start()] + group + text[toggle.end():]


def ensure_lesson_toggle(text, lesson_id, relative):
    markup = (
        '\n    <div class="progress-bar">\n'
        '      <button class="progress-toggle" id="progressToggle" type="button" aria-pressed="false">\n'
        '        <span class="progress-tick" aria-hidden="true">&#10003;</span>'
        '<span id="progressLabel">Mark this lesson complete</span>\n'
        '      </button>\n'
        '      <p class="progress-note">Kept in this browser only, for you. Nothing is sent anywhere '
        'and nothing checks it.\n'
        '        <a href="%sprogress/">Carry it to another device</a>.</p>\n'
        '    </div>\n' % up_to_root(relative)
    )
    if 'id="progressToggle"' in text:
        return re.sub(r'\n    <div class="progress-bar">.*?\n    </div>\n',
                      lambda _m: markup, text, count=1, flags=re.S)
    anchor = text.find('<nav class="lesson-nav"')
    if anchor == -1:
        raise SystemExit("no lesson pager to precede")
    line_start = text.rfind("\n", 0, anchor) + 1
    return text[:line_start] + markup.lstrip("\n") + "\n" + text[line_start:]


def ensure_feedback_panel(text, lesson_id, lesson_title, course_title):
    """The recommendations panel, at the foot of the lesson.

    Placed after the pager and before the footer, which is where the generated
    lessons put it: past the material and the completion mark, so it reads as
    "now that you have been through this", not as a form to fill in first.
    """
    markup = feedback.MARKUP % {
        "id": esc(lesson_id),
        "lesson": esc(lesson_title),
        "course": esc(course_title),
    }
    if 'id="lessonFeedback"' in text:
        return re.sub(r'\n    <section class="lesson-feedback".*?\n    </section>\n',
                      lambda _m: markup, text, count=1, flags=re.S)
    # Anchored on the pager, not on the footer: the seven market-structure
    # lessons close with a bare <footer> and the rest with <footer class="footer">,
    # so the footer is not a reliable landmark. Every lesson page has the pager --
    # the completion toggle above is placed by finding it.
    nav = text.find('<nav class="lesson-nav"')
    if nav == -1:
        raise SystemExit("no lesson pager to follow")
    close = text.find("</nav>", nav)
    if close == -1:
        raise SystemExit("unterminated lesson pager")
    close += len("</nav>")
    return text[:close] + "\n" + markup + text[close:]


def ensure_course_hooks(text, course_slug, lessons):
    """data-lesson on each lesson card, and one line saying how many are done."""
    by_slug = {l["slug"]: l for l in lessons}
    seen = []

    def stamp(match):
        head, body = match.group(1), match.group(2)
        link = re.search(r'<a class="lesson-link" href="\./([a-z0-9-]+)/">', body)
        if not link or link.group(1) not in by_slug:
            return match.group(0)
        slug = link.group(1)
        seen.append(slug)
        head = re.sub(r'\s+data-lesson="[^"]*"', "", head)
        return '<article class="lesson-card"%s data-lesson="%s/%s">%s</article>' % (
            head, course_slug, slug, body)

    text = re.sub(r'<article class="lesson-card"([^>]*)>(.*?)</article>', stamp, text, flags=re.S)
    if len(seen) != len(lessons):
        raise SystemExit("%s: stamped %d of %d lesson cards" % (course_slug, len(seen), len(lessons)))

    line = '<p class="course-progress" id="courseProgress">None of the %d lessons marked complete</p>\n\n          ' % len(lessons)
    if 'id="courseProgress"' in text:
        return re.sub(r'<p class="course-progress" id="courseProgress">.*?</p>',
                      lambda _m: line.strip(), text, count=1, flags=re.S)
    anchor = text.find('<ol class="course-track"')
    if anchor == -1:
        raise SystemExit("%s: no course track to precede" % course_slug)
    return text[:anchor] + line + text[anchor:]


def ensure_path_hooks(text, courses):
    """data-course/data-lessons on each course card, and a line for its count."""
    counts = {c["slug"]: len(c["lessons"]) for c in courses}
    seen = []

    def stamp(match):
        head, body = match.group(1), match.group(2)
        link = re.search(r'<h3><a href="\.\./\.\./([a-z0-9-]+)/">', body)
        if not link or link.group(1) not in counts:
            return match.group(0)
        slug = link.group(1)
        seen.append(slug)
        head = re.sub(r'\s+data-(course|lessons)="[^"]*"', "", head)
        if 'class="course-progress-note"' not in body:
            body = body.rstrip() + '\n              <span class="course-progress-note"></span>\n            '
        return '<article class="course-card"%s data-course="%s" data-lessons="%d">%s</article>' % (
            head, slug, counts[slug], body)

    text = re.sub(r'<article class="course-card"([^>]*)>(.*?)</article>', stamp, text, flags=re.S)
    if len(seen) != len(courses):
        raise SystemExit("path page: stamped %d of %d course cards" % (len(seen), len(courses)))
    return text


def main():
    courses = trading_inventory()
    if not courses:
        raise SystemExit("no trading courses found; refusing to patch nothing")
    changed = 0
    touched = 0

    def save(relative, text, before):
        nonlocal changed, touched
        touched += 1
        target = SITE / relative
        if text != before:
            target.write_text(text, encoding="utf-8")
            changed += 1

    # Lessons: the toggle, the masthead control, the styles and the scripts.
    for course in courses:
        for lesson in course["lessons"]:
            relative = "%s/%s/index.html" % (course["slug"], lesson["slug"])
            before = (SITE / relative).read_text(encoding="utf-8")
            lesson_id = '"%s/%s"' % (course["slug"], lesson["slug"])
            text = ensure_css(before)
            text = ensure_masthead(text, relative)
            text = ensure_lesson_toggle(text, lesson_id, relative)
            text = ensure_feedback_panel(text, "%s/%s" % (course["slug"], lesson["slug"]),
                                         lesson["title"], course["title"])
            text = ensure_script(text, progress.PROGRESS_JS + (progress.LESSON_JS % lesson_id)
                                 + feedback.STORE_JS + feedback.LESSON_JS + SIGNIN_JS)
            save(relative, text, before)

        # Course home: a tick against each lesson it lists, and a count.
        relative = "%s/index.html" % course["slug"]
        before = (SITE / relative).read_text(encoding="utf-8")
        text = ensure_css(before)
        text = ensure_masthead(text, relative)
        text = ensure_course_hooks(text, course["slug"], course["lessons"])
        text = ensure_script(text, progress.PROGRESS_JS + COURSE_JS + SIGNIN_JS)
        save(relative, text, before)

    # The path page: the same count, per course, on its spine.
    before = (SITE / PATH_PAGE).read_text(encoding="utf-8")
    text = ensure_css(before)
    text = ensure_masthead(text, PATH_PAGE)
    text = ensure_path_hooks(text, courses)
    text = ensure_script(text, progress.PROGRESS_JS + PATH_JS + SIGNIN_JS)
    save(PATH_PAGE, text, before)

    # The capstone pages are not lessons -- they belong to no course's list and
    # so are not tickable and not in any denominator. They still get the way in
    # to /progress/, because every other page a reader can land on has one.
    for relative in ("paths/trading/iren-analysis-2026-08-16/index.html",
                     "paths/trading/iren-analysis-2026-08-16/slides/index.html"):
        if not (SITE / relative).exists():
            continue
        before = (SITE / relative).read_text(encoding="utf-8")
        text = ensure_css(before)
        text = ensure_masthead(text, relative)
        text = ensure_script(text, SIGNIN_JS)
        save(relative, text, before)

    lessons = sum(len(c["lessons"]) for c in courses)
    print("Trading path: %d courses, %d lessons now tickable." % (len(courses), lessons))
    print("%d page(s) visited, %d rewritten." % (touched, changed))


if __name__ == "__main__":
    main()
