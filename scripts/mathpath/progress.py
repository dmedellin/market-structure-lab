"""Self-reported completion marks, stored in the browser.

WHY THIS IS NOT A NETWORK FEATURE. Every page under site/ must render with zero
network requests; that invariant is the reason these pages work offline and
carry no third-party anything. A completion tick is a note the reader makes to
themselves -- the footer of every page says the figures are computed locally,
and this is the same promise applied to their own progress. So the mark lives in
localStorage and the page never talks to anyone about it.

Signing in with Microsoft is offered on ONE page (/progress/), which is declared
exempt from self-containment by name. Signing in does not gate a single word of
the material and is not required to tick anything; it only lets the same marks
follow you to another device. A reader who never signs in loses nothing but that.

The marks are not audited and are not evidence. Nothing checks whether the
lesson was read; the reader is telling themselves what they have done.
"""

STORAGE_KEY = "learn-progress"

# Rendered into every lesson, course-home and path page. It is inlined rather
# than shared because a shared file would be a network request.
PROGRESS_JS = r"""
  /* Completion marks. localStorage only: no request leaves the page. */
  (function () {
    var KEY = 'learn-progress';
    function read() {
      try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; }
      catch (e) { return {}; }
    }
    function write(map) {
      try { localStorage.setItem(KEY, JSON.stringify(map)); } catch (e) { /* private mode */ }
    }
    function done(id) { return Object.prototype.hasOwnProperty.call(read(), id); }
    function toggle(id) {
      var map = read();
      if (done(id)) { delete map[id]; } else { map[id] = new Date().toISOString().slice(0, 10); }
      write(map);
      return done(id);
    }
    window.learnProgress = { read: read, done: done, toggle: toggle, key: KEY };
  })();
"""

# The control a LESSON page carries, in the pager region.
LESSON_MARKUP = """
    <div class="progress-bar">
      <button class="progress-toggle" id="progressToggle" type="button" aria-pressed="false">
        <span class="progress-tick" aria-hidden="true">&#10003;</span><span id="progressLabel">Mark this lesson complete</span>
      </button>
      <p class="progress-note">Kept in this browser only, for you. Nothing is sent anywhere and nothing checks it.
        <a href="%s/progress/">Carry it to another device</a>.</p>
    </div>
"""

LESSON_JS = """
  (function () {
    var button = document.getElementById('progressToggle');
    if (!button || !window.learnProgress) return;
    var id = %s;
    var label = document.getElementById('progressLabel');
    function paint() {
      var on = window.learnProgress.done(id);
      button.classList.toggle('is-done', on);
      button.setAttribute('aria-pressed', on ? 'true' : 'false');
      label.textContent = on ? 'Completed' : 'Mark this lesson complete';
    }
    button.addEventListener('click', function () { window.learnProgress.toggle(id); paint(); });
    paint();
  })();
"""

# What a COURSE HOME adds: a count, and a tick against each lesson it lists.
COURSE_JS = """
  (function () {
    if (!window.learnProgress) return;
    var out = document.getElementById('courseProgress');
    var items = [].slice.call(document.querySelectorAll('.syllabus-item[data-lesson]'));
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

# What a PATH PAGE adds: the same count per course on its spine.
PATH_JS = """
  (function () {
    if (!window.learnProgress) return;
    var marks = window.learnProgress.read();
    [].slice.call(document.querySelectorAll('.spine-item[data-course]')).forEach(function (item) {
      var slug = item.getAttribute('data-course');
      var total = parseInt(item.getAttribute('data-lessons'), 10) || 0;
      var n = Object.keys(marks).filter(function (k) { return k.indexOf(slug + '/') === 0; }).length;
      var out = item.querySelector('.spine-progress');
      if (!out || !total) return;
      out.textContent = n ? n + ' of ' + total + ' done' : '';
      item.classList.toggle('is-started', n > 0);
      item.classList.toggle('is-complete', n >= total);
    });
  })();
"""
