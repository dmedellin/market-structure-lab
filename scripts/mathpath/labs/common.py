"""Shared pieces every lab uses.

A lab is a function cfg -> Lab. It returns the markup for the lab section and
the JavaScript that drives it. Two rules hold for all of them, and the footer
of every page on this path states the first one as a promise to the reader:

  1. NOTHING IS PRECOMPUTED. Every number a lab shows is computed in the
     browser from the definition the lesson just gave. A lab that shipped the
     answer as a literal would be a page asserting a result rather than
     demonstrating one, and the reader could not tell the difference.
  2. EXACT ARITHMETIC WHERE EXACTNESS IS THE POINT. Counting, modular
     arithmetic and probability over finite sample spaces are done in integers
     (BigInt where a factorial can overflow, integer numerator/denominator for
     probabilities). Floating point appears only where a lesson is explicitly
     about approximation, and says so.
"""

import json


class Lab:
    def __init__(self, *, title, subtitle, markup, script, legend=(), controls="",
                 panel_title="", panel_intro="", note=""):
        self.title = title
        self.subtitle = subtitle
        self.markup = markup
        self.script = script
        self.legend = legend
        self.controls = controls
        self.panel_title = panel_title
        self.panel_intro = panel_intro
        self.note = note


def cfg_literal(name, value):
    """Embed a config object as a JS literal.

    json.dumps output is valid JS, and </script> can never appear inside it
    because the payloads are lesson data (numbers, short strings, formulas),
    never markup -- the escape below makes that structural rather than lucky.
    """
    return "  var %s = %s;\n" % (name, json.dumps(value).replace("</", "<\\/"))


# Rendered once per page that carries a quiz. The questions are lesson data;
# this is only the machinery that shows them, scores them, and explains each
# answer after it is chosen.
QUIZ_MARKUP = """      <article class="card practice">
        <div class="practice-head"><h3>{title}</h3><span class="score" id="quizScore">Score 0 / 0</span></div>
        <p id="quizPrompt" class="small-copy" style="margin:0;"></p>
        <div class="choice-grid" id="quizChoices"></div>
        <div class="feedback" id="quizFeedback" aria-live="polite">Choose the answer you can justify.</div>
        <button class="btn small" id="quizNext" type="button" style="margin-top:2px;">Next question</button>
      </article>"""

QUIZ_SCRIPT = """
    /* Practice. The questions are lesson data; this only presents and scores
       them. Every wrong answer gets the reason it is wrong, not just a cross:
       an unexplained "incorrect" teaches the reader to guess again. */
    (function () {
      var prompt = document.getElementById('quizPrompt');
      if (!prompt) return;
      var choices = document.getElementById('quizChoices');
      var feedback = document.getElementById('quizFeedback');
      var scoreOut = document.getElementById('quizScore');
      var nextBtn = document.getElementById('quizNext');
      var index = 0, asked = 0, right = 0, answered = false;

      function paintScore() { scoreOut.textContent = 'Score ' + right + ' / ' + asked; }

      function render() {
        var q = QUIZ[index % QUIZ.length];
        answered = false;
        prompt.innerHTML = q.q;
        choices.textContent = '';
        feedback.innerHTML = 'Choose the answer you can justify.';
        q.a.forEach(function (text, i) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'choice';
          b.innerHTML = text;
          b.addEventListener('click', function () { pick(q, i, b); });
          choices.appendChild(b);
        });
      }

      function pick(q, i, button) {
        if (answered) return;
        answered = true;
        asked += 1;
        var correct = i === q.c;
        if (correct) right += 1;
        button.classList.add(correct ? 'right' : 'wrong');
        if (!correct) {
          choices.children[q.c].classList.add('right');
        }
        feedback.innerHTML = (correct ? '<strong>Correct.</strong> ' : '<strong>Not quite.</strong> ') + q.why;
        paintScore();
      }

      nextBtn.addEventListener('click', function () { index += 1; render(); });
      paintScore();
      render();
    })();
"""
