"""Course 7: systems, matrices and sequences -- three labs over one arithmetic.

Everything on this page is a rational number over BigInt. That is not tidiness
for its own sake: elimination is the first algorithm on this path that FEEDS
its own output back in, and a system whose exact answer is 186/5 becomes
37.199999999999996 after three floating-point row operations. A lab that
printed that would be teaching the reader that elimination is approximate,
which is the opposite of true.

The three labs and the decision behind each:

  system_lab   Every mode solves the SAME system and every mode is a different
               method, so a reader can carry one system across six lessons and
               watch six routes arrive at one answer. The classification --
               one solution, none, infinitely many -- is never inferred from
               the shape of the equations. It comes from comparing the rank of
               the coefficient matrix with the rank of the augmented matrix,
               computed by the same row reduction the reader is being shown,
               which is why the degenerate presets behave correctly instead of
               being special-cased into behaving correctly.

               The reader types whole equations -- "3(x - y)/2 <= 4" -- rather
               than filling six coefficient boxes. EXPR_JS already parses that;
               what this file adds is the step that turns the tree into exact
               coefficients, and REFUSES anything that is not linear rather
               than quietly dropping the term it cannot handle.

  matrix_lab   A matrix lab can very easily become a calculator that asserts.
               Every mode here answers with a second, independent computation
               beside the first: the determinant by cofactor expansion AND by
               row reduction, the inverse by row-reducing [A|I] AND by then
               multiplying A by the result to watch I come back, Cramer's rule
               AND the solution the row reduction found. When two methods that
               share no code agree, the reader has evidence. One number in a
               box is not evidence.

  sequence_lab The nth term and the sum are each computed twice: once by doing
               the thing the definition says -- adding the terms up, one at a
               time -- and once by the closed formula. The lab prints both and
               says whether they matched. This is the only honest way to
               present a formula that the lesson has not yet proved, and it is
               how the geometric mode can show, rather than warn, that the sum
               formula divides by 1 - r and therefore has nothing to say when
               r = 1.

Floating point appears in exactly one place in this file: PLOT_JS turning a
world coordinate into a pixel. Every number the reader is told is exact, and
the two places a decimal is printed at all say that it is a rounding.
"""

from .algebra_core import EXPR_JS, PLOT_JS, POLY_JS, RATIONAL_JS
from .common import Lab, cfg_literal

# ---------------------------------------------------------------- formatting

# Shared by all three labs. Nothing here decides anything -- every verdict on
# the page is made on the exact side and then handed to these to be written.
FORMAT_JS = r"""
  function td(t, cls) { return '<td' + (cls ? ' class="' + cls + '"' : '') + '>' + t + '</td>'; }
  function tdl(t, cls) {
    return '<td style="text-align:left;"' + (cls ? ' class="' + cls + '"' : '') + '>' + t + '</td>';
  }
  function th(t) { return '<th>' + t + '</th>'; }
  function rowhead(t) { return '<th class="rowhead">' + t + '</th>'; }
  function tr(cells, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '>' + cells.join('') + '</tr>'; }
  function table(caption, heads, rows) {
    var head = (heads && heads.length)
      ? '<thead>' + tr(heads.map(function (h) { return th(h); })) + '</thead>' : '';
    return '<div class="table-wrap"><table class="tt"><caption>' + caption + '</caption>'
      + head + '<tbody>' + rows.join('') + '</tbody></table></div>';
  }
  /* The two-column "what was done / what it produced" table. The exemplar's
     trace layout, kept identical so a reader moving between courses is reading
     the same page furniture. */
  function steps(caption, pairs) {
    return table(caption, [], pairs.map(function (p) { return tr([rowhead(p[0]), tdl(p[1])]); }));
  }
  function chip(t, kind) { return '<span class="chip' + (kind ? ' ' + kind : '') + '">' + t + '</span>'; }
  /* " + 3" or " - 7": a bare number as a continuation. Everything on this page
     that writes "something + <number>" goes through it, because "a(n-1) + -7"
     is not a thing a reader writes and not a thing a marker accepts. */
  function plusnum(r) { return (Rsign(r) < 0 ? ' - ' : ' + ') + Rtext(Rabs(r)); }
  function tone(t, kind) { return '<span class="tone-' + kind + '">' + t + '</span>'; }
  function plural(n, one, many) { return n === 1 ? one : many; }
  /* Reader text goes into innerHTML, and on this course the reader types < and
     > all day. Escaped once, at the boundary, rather than trusted: "x + 2y <= 8"
     written raw would lose everything from the < to the next > -- which is the
     end of the cell -- and the page would quietly drop the reader's own words. */
  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* Rparse throws on a zero denominator, and 1/0 is a thing a reader types.
     Every read of reader input goes through this, so a bad fraction becomes a
     sentence in the status banner rather than an exception. */
  function Rread(text) {
    try { return Rparse(String(text).trim()); } catch (err) { return null; }
  }
  /* The one rounding this file performs, and it is never used to decide
     anything -- only to sit beside an exact value that a reader may want to
     place on a number line. Every caller labels it as a rounding. */
  function approx(r, places) {
    var v = Rnum(r);
    if (!isFinite(v)) return 'not a real number';
    return v.toFixed(places === undefined ? 4 : places);
  }
  /* The least common multiple of two rationals: lcm of the numerators over the
     gcd of the denominators. For two integers this is the schoolbook lcm, which
     is what the elimination mode needs; for 1/2 and 1/4 it is 1/2, which is
     what keeps that mode from inventing multipliers with four-digit numerators
     the moment a coefficient stops being whole. */
  function Rlcm(a, b) {
    if (Rzero(a) || Rzero(b)) return R0;
    var an = a.n < 0n ? -a.n : a.n, bn = b.n < 0n ? -b.n : b.n;
    return R(an / bgcd(an, bn) * bn, bgcd(a.d, b.d));
  }
"""


# ------------------------------------------------------------- linear forms

# The step the docstring promises: a parse tree becomes exact coefficients, or
# it becomes a reason it could not.
LINEAR_JS = r"""
  /* A linear form over the unknowns a mode names: the coefficient of each,
     plus the constant. 3x - y/2 + 4 over ['x','y'] is { c: [3, -1/2], k: 4 }.

     Building one from EXPR_JS's tree is where "linear" stops being a word in
     the lesson and becomes a rule that can REFUSE. x*y multiplies two forms
     that both carry an unknown; 1/x divides by one; sqrt(x) is a function of
     one; x^2 raises one to a power. Each returns the reason rather than
     dropping the term, because a lab that silently ignored the xy in
     "xy + x = 4" would solve a different system and say nothing. */
  /* "x and y", "x, y and z" -- a list of unknowns written the way a sentence
     wants it, since these names appear in every refusal this file prints. */
  function varlist(names) {
    if (names.length < 2) return names.join('');
    return names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1];
  }
  function Lnew(nv) { var c = []; for (var i = 0; i < nv; i += 1) c.push(R0); return { c: c, k: R0 }; }
  function Lconst(r, nv) { var f = Lnew(nv); f.k = r; return f; }
  function Lvar(i, nv) { var f = Lnew(nv); f.c[i] = R1; return f; }
  function Lisconst(f) {
    for (var i = 0; i < f.c.length; i += 1) if (!Rzero(f.c[i])) return false;
    return true;
  }
  function Lcomb(a, b, sub) {
    var f = Lnew(a.c.length);
    for (var i = 0; i < a.c.length; i += 1) f.c[i] = sub ? Rsub(a.c[i], b.c[i]) : Radd(a.c[i], b.c[i]);
    f.k = sub ? Rsub(a.k, b.k) : Radd(a.k, b.k);
    return f;
  }
  function Lscale(a, r) {
    var f = Lnew(a.c.length);
    for (var i = 0; i < a.c.length; i += 1) f.c[i] = Rmul(a.c[i], r);
    f.k = Rmul(a.k, r);
    return f;
  }

  /* { f: form } or { bad: the sentence to print. } Never an exception. */
  function Lof(node, names) {
    var nv = names.length;
    if (!node) return { bad: 'there is nothing to read there' };
    switch (node.k) {
      case 'num': {
        var r = Rread(node.v);
        if (r === null) return { bad: '"' + esc(node.v) + '" is not a number I can read exactly' };
        return { f: Lconst(r, nv) };
      }
      case 'var': {
        var i = names.indexOf(node.v);
        if (i < 0) {
          return { bad: 'this system is in ' + varlist(names) + ', and "' + esc(node.v)
            + '" is not one of them' };
        }
        return { f: Lvar(i, nv) };
      }
      case 'neg': {
        var a = Lof(node.a, names);
        return a.bad ? a : { f: Lscale(a.f, R(-1n)) };
      }
      case 'add': case 'sub': {
        var l = Lof(node.a, names); if (l.bad) return l;
        var r2 = Lof(node.b, names); if (r2.bad) return r2;
        return { f: Lcomb(l.f, r2.f, node.k === 'sub') };
      }
      case 'mul': {
        var l2 = Lof(node.a, names); if (l2.bad) return l2;
        var r3 = Lof(node.b, names); if (r3.bad) return r3;
        if (Lisconst(l2.f)) return { f: Lscale(r3.f, l2.f.k) };
        if (Lisconst(r3.f)) return { f: Lscale(l2.f, r3.f.k) };
        return { bad: 'two unknowns are multiplied together, and that is not linear' };
      }
      case 'div': {
        var l3 = Lof(node.a, names); if (l3.bad) return l3;
        var r4 = Lof(node.b, names); if (r4.bad) return r4;
        if (!Lisconst(r4.f)) return { bad: 'an unknown appears in a denominator, and that is not linear' };
        if (Rzero(r4.f.k)) return { bad: 'that divides by zero' };
        return { f: Lscale(l3.f, Rinv(r4.f.k)) };
      }
      case 'pow': {
        var b2 = Lof(node.a, names); if (b2.bad) return b2;
        var e = Lof(node.b, names); if (e.bad) return e;
        if (!Lisconst(e.f)) return { bad: 'an unknown appears in an exponent, and that is not linear' };
        if (!Rint(e.f.k) || e.f.k.n < 0n || e.f.k.n > 12n) {
          return { bad: 'the exponent ' + Rtext(e.f.k) + ' is not a small whole number' };
        }
        var p = Number(e.f.k.n);
        if (p === 1) return { f: b2.f };
        if (Lisconst(b2.f)) return { f: Lconst(Rpow(b2.f.k, p), nv) };
        if (p === 0) return { f: Lconst(R1, nv) };
        return { bad: 'an unknown is raised to the power ' + p + ', and that is not linear' };
      }
      case 'fn': return { bad: node.v + '(...) of an expression is not linear' };
    }
    return { bad: 'I could not read that' };
  }

  /* The relation is pulled out BEFORE tokenising, because EXPR_JS has no
     opinion about < and would reject the character outright. Two-character
     relations are tried first so "<=" is never read as "<" followed by "=". */
  var RELS = [['<=', 'le'], ['>=', 'ge'], ['=<', 'le'], ['=>', 'ge'], ['<', 'lt'], ['>', 'gt'], ['=', 'eq']];
  function relhtml(rel) {
    return rel === 'le' ? '&lt;=' : (rel === 'ge' ? '&gt;=' : (rel === 'lt' ? '&lt;'
      : (rel === 'gt' ? '&gt;' : '=')));
  }
  function relplain(rel) {
    return rel === 'le' ? '<=' : (rel === 'ge' ? '>=' : (rel === 'lt' ? '<' : (rel === 'gt' ? '>' : '=')));
  }
  function relsplit(text) {
    var s = String(text);
    for (var i = 0; i < RELS.length; i += 1) {
      var at = s.indexOf(RELS[i][0]);
      if (at >= 0) {
        return { lhs: s.slice(0, at), rhs: s.slice(at + RELS[i][0].length), rel: RELS[i][1] };
      }
    }
    return null;
  }

  /* One typed line, as  c1 v1 + c2 v2 + ... REL b. Everything is moved to the
     left and the constant to the right, so every later step -- rank, pivot,
     shading, corner -- is reading one shape. */
  function Lequation(text, names) {
    var s = String(text).trim();
    if (!s) return { bad: 'this line is empty' };
    var parts = relsplit(s);
    if (!parts) {
      return { bad: 'there is no =, &lt;=, &gt;=, &lt; or &gt; in "' + esc(s)
        + '", so it is an expression rather than an equation' };
    }
    if (!parts.lhs.trim()) return { bad: 'there is nothing to the left of the ' + relplain(parts.rel) };
    if (!parts.rhs.trim()) return { bad: 'there is nothing to the right of the ' + relplain(parts.rel) };
    var lt, rt;
    try { lt = Eparse(parts.lhs); } catch (err) { return { bad: 'the left side does not parse: ' + esc(err.message) }; }
    try { rt = Eparse(parts.rhs); } catch (err) { return { bad: 'the right side does not parse: ' + esc(err.message) }; }
    var lf = Lof(lt, names); if (lf.bad) return lf;
    var rf = Lof(rt, names); if (rf.bad) return rf;
    var f = Lcomb(lf.f, rf.f, true);
    return { c: f.c, b: Rneg(f.k), rel: parts.rel, src: s };
  }

  /* "3x - (1/2)y". Signs are folded into the term the way a reader writes them,
     and a fraction is bracketed so (3/2)x can never be misread as 3/(2x). */
  function Ltext(coeffs, names) {
    var out = '';
    for (var i = 0; i < coeffs.length; i += 1) {
      var r = coeffs[i];
      if (Rzero(r)) continue;
      var neg = Rsign(r) < 0, mag = Rabs(r);
      out += (out === '') ? (neg ? '-' : '') : (neg ? ' - ' : ' + ');
      out += (Requ(mag, R1) ? '' : Rterm(mag)) + names[i];
    }
    return out === '' ? '0' : out;
  }
  /* "3x", "-x", "(2/3)y". The coefficient is dropped when it is 1 and folded
     into a minus sign when it is -1, because "1x" and "-1x" are things no
     reader writes and no marker accepts. */
  function termtext(coef, name) {
    if (Requ(coef, R1)) return name;
    if (Requ(coef, R(-1n))) return '-' + name;
    return Rterm(coef) + name;
  }
  /* The same term as a continuation: " + 3y", " - 3y", or nothing at all. */
  function plusterm(coef, name) {
    if (Rzero(coef)) return '';
    return (Rsign(coef) < 0 ? ' - ' : ' + ') + termtext(Rabs(coef), name);
  }
  function Rowtext(row, names) {
    return Ltext(row.c, names) + ' ' + relhtml(row.rel) + ' ' + Rtext(row.b);
  }
  function Rowvalue(row, point) {
    var v = R0;
    for (var i = 0; i < row.c.length; i += 1) v = Radd(v, Rmul(row.c[i], point[i]));
    return v;
  }
"""


# ---------------------------------------------------------------- matrices

MATRIX_JS = r"""
  /* A matrix is an array of arrays of rationals. Nothing here rounds, and
     nothing here caches: every routine recomputes from the entries it is given,
     so two routines that agree agreed by arithmetic rather than by sharing a
     variable. */
  function Mcopy(M) { return M.map(function (r) { return r.slice(); }); }
  function Mrows(M) { return M.length; }
  function Mcols(M) { return M.length ? M[0].length : 0; }
  function Msquare(M) { return M.length > 0 && M.length === Mcols(M); }
  function Mshape(M) { return Mrows(M) + ' by ' + Mcols(M); }
  function Mzero(r, c) {
    var out = [];
    for (var i = 0; i < r; i += 1) { var row = []; for (var j = 0; j < c; j += 1) row.push(R0); out.push(row); }
    return out;
  }
  function Mid(n) {
    var out = Mzero(n, n);
    for (var i = 0; i < n; i += 1) out[i][i] = R1;
    return out;
  }
  function Mmap2(A, B, fn) {
    return A.map(function (row, i) { return row.map(function (v, j) { return fn(v, B[i][j]); }); });
  }
  function Madd(A, B) { return Mmap2(A, B, Radd); }
  function Msub(A, B) { return Mmap2(A, B, Rsub); }
  function Mscale(A, r) { return A.map(function (row) { return row.map(function (v) { return Rmul(v, r); }); }); }
  function Mtrans(A) {
    var out = Mzero(Mcols(A), Mrows(A));
    for (var i = 0; i < Mrows(A); i += 1) for (var j = 0; j < Mcols(A); j += 1) out[j][i] = A[i][j];
    return out;
  }
  function Msamesize(A, B) { return Mrows(A) === Mrows(B) && Mcols(A) === Mcols(B); }
  function Mmul(A, B) {
    if (Mcols(A) !== Mrows(B)) return null;
    var out = Mzero(Mrows(A), Mcols(B));
    for (var i = 0; i < Mrows(A); i += 1) {
      for (var j = 0; j < Mcols(B); j += 1) {
        var s = R0;
        for (var k = 0; k < Mcols(A); k += 1) s = Radd(s, Rmul(A[i][k], B[k][j]));
        out[i][j] = s;
      }
    }
    return out;
  }
  /* The row-times-column sum for one entry, written out. This is the entry's
     definition, and printing it is the only way the reader can check that the
     number in the box came from the row and column it claims. */
  function Mdottext(A, B, i, j) {
    var parts = [];
    for (var k = 0; k < Mcols(A); k += 1) {
      parts.push('(' + Rtext(A[i][k]) + ')(' + Rtext(B[k][j]) + ')');
    }
    return parts.join(' + ');
  }
  function Mequ(A, B) {
    if (!Msamesize(A, B)) return false;
    for (var i = 0; i < Mrows(A); i += 1) {
      for (var j = 0; j < Mcols(A); j += 1) if (!Requ(A[i][j], B[i][j])) return false;
    }
    return true;
  }
  function Maug(A, B) {
    return A.map(function (row, i) { return row.concat(B[i]); });
  }
  function Mtake(M, from, count) {
    return M.map(function (row) { return row.slice(from, from + count); });
  }
  function Mminor(M, i, j) {
    var out = [];
    for (var a = 0; a < M.length; a += 1) {
      if (a === i) continue;
      var row = [];
      for (var b = 0; b < M[a].length; b += 1) { if (b === j) continue; row.push(M[a][b]); }
      out.push(row);
    }
    return out;
  }
  /* Cofactor expansion along the first row, recursively. Not the fast way to
     get a determinant, and that is the point: this is the definition the
     lesson gives, and the row-reduction determinant beside it is the check. */
  function Mdet(M) {
    var n = M.length;
    if (!Msquare(M)) return null;
    if (n === 1) return M[0][0];
    if (n === 2) return Rsub(Rmul(M[0][0], M[1][1]), Rmul(M[0][1], M[1][0]));
    var total = R0;
    for (var j = 0; j < n; j += 1) {
      if (Rzero(M[0][j])) continue;
      var term = Rmul(M[0][j], Mdet(Mminor(M, 0, j)));
      total = (j % 2 === 0) ? Radd(total, term) : Rsub(total, term);
    }
    return total;
  }

  /* ---- the three elementary row operations, each on its own ---- */
  function Mswap(M, i, j) {
    var out = Mcopy(M), t = out[i]; out[i] = out[j]; out[j] = t;
    return out;
  }
  function Mscalerow(M, i, s) {
    var out = Mcopy(M);
    out[i] = out[i].map(function (v) { return Rmul(v, s); });
    return out;
  }
  function Maddrow(M, i, j, s) {
    var out = Mcopy(M);
    out[i] = out[i].map(function (v, c) { return Radd(v, Rmul(s, M[j][c])); });
    return out;
  }

  /* Gaussian elimination: forward only, pivots left where they are. No row is
     divided by its pivot, which is what keeps 3x + 2y = 24 from becoming
     x + (2/3)y = 8 in the first line of a trace the reader is meant to follow. */
  function Mgauss(M0, ncols) {
    var M = Mcopy(M0), ops = [], pivots = [], row = 0;
    var stop = ncols === undefined ? Mcols(M) : ncols;
    for (var col = 0; col < stop && row < M.length; col += 1) {
      var p = -1;
      for (var i = row; i < M.length; i += 1) if (!Rzero(M[i][col])) { p = i; break; }
      if (p < 0) continue;
      if (p !== row) {
        M = Mswap(M, row, p);
        ops.push({ op: 'R' + (row + 1) + ' &lt;-&gt; R' + (p + 1),
                   why: 'the pivot position held 0, so a row below it is brought up',
                   after: Mcopy(M) });
      }
      for (var i2 = row + 1; i2 < M.length; i2 += 1) {
        if (Rzero(M[i2][col])) continue;
        var m = Rneg(Rdiv(M[i2][col], M[row][col]));
        M = Maddrow(M, i2, row, m);
        ops.push({ op: 'R' + (i2 + 1) + ' -&gt; R' + (i2 + 1) + ' + ' + Rterm(m) + 'R' + (row + 1),
                   why: 'clears the entry below the pivot in column ' + (col + 1),
                   after: Mcopy(M) });
      }
      pivots.push(col);
      row += 1;
    }
    return { M: M, ops: ops, pivots: pivots, rank: pivots.length };
  }

  /* Gauss-Jordan: every pivot driven to 1 and every other entry in its column
     driven to 0, recording each elementary operation with the matrix it
     produced. `detf` is the factor the operations multiplied the determinant
     by, so det(A) can be recovered from the reduced form without a second
     implementation of anything. */
  function Mrref(M0, opts) {
    opts = opts || {};
    var stop = opts.cols === undefined ? Mcols(M0) : opts.cols;
    var M = Mcopy(M0), ops = [], pivots = [], detf = R1, row = 0;
    for (var col = 0; col < stop && row < M.length; col += 1) {
      var p = -1;
      for (var i = row; i < M.length; i += 1) if (!Rzero(M[i][col])) { p = i; break; }
      if (p < 0) continue;
      if (p !== row) {
        M = Mswap(M, row, p);
        detf = Rneg(detf);
        ops.push({ op: 'R' + (row + 1) + ' &lt;-&gt; R' + (p + 1),
                   why: 'a swap, which multiplies the determinant by -1',
                   after: Mcopy(M) });
      }
      var pv = M[row][col];
      if (!Requ(pv, R1)) {
        var s = Rinv(pv);
        M = Mscalerow(M, row, s);
        detf = Rmul(detf, s);
        ops.push({ op: 'R' + (row + 1) + ' -&gt; ' + Rterm(s) + 'R' + (row + 1),
                   why: 'makes the pivot 1, and multiplies the determinant by ' + Rtext(s),
                   after: Mcopy(M) });
      }
      for (var i2 = 0; i2 < M.length; i2 += 1) {
        if (i2 === row || Rzero(M[i2][col])) continue;
        var m = Rneg(M[i2][col]);
        M = Maddrow(M, i2, row, m);
        ops.push({ op: 'R' + (i2 + 1) + ' -&gt; R' + (i2 + 1) + ' + ' + Rterm(m) + 'R' + (row + 1),
                   why: 'clears column ' + (col + 1) + ', and leaves the determinant alone',
                   after: Mcopy(M) });
      }
      pivots.push(col);
      row += 1;
    }
    return { M: M, ops: ops, pivots: pivots, rank: pivots.length, detf: detf };
  }

  /* "2 1 -1; -3 -1 2" -- rows split on ; or a newline, entries on spaces or
     commas. Every entry goes through Rparse, so 1/2 is an entry and 0.25
     becomes 1/4 rather than a float that will drift three row operations later. */
  function Mparse(text, what) {
    var s = String(text).trim();
    if (!s) return { bad: (what || 'the matrix') + ' box is empty' };
    var lines = s.split(/[;\n]/).map(function (t) { return t.trim(); })
                 .filter(function (t) { return t.length > 0; });
    if (!lines.length) return { bad: (what || 'the matrix') + ' box has no rows in it' };
    var out = [], width = -1;
    for (var i = 0; i < lines.length; i += 1) {
      var cells = lines[i].split(/[\s,]+/).filter(function (t) { return t.length > 0; });
      var vals = [];
      for (var j = 0; j < cells.length; j += 1) {
        var r = Rread(cells[j]);
        if (r === null) {
          return { bad: (what || 'the matrix') + ', row ' + (i + 1) + ', entry ' + (j + 1) + ': "'
            + esc(cells[j]) + '" is not a whole number or a fraction' };
        }
        vals.push(r);
      }
      if (!vals.length) return { bad: (what || 'the matrix') + ', row ' + (i + 1) + ' has no entries' };
      if (width < 0) width = vals.length;
      else if (vals.length !== width) {
        return { bad: (what || 'the matrix') + ' is not rectangular: row 1 has ' + width
          + ' entries and row ' + (i + 1) + ' has ' + vals.length };
      }
      out.push(vals);
    }
    if (out.length > 6 || width > 6) {
      return { bad: 'this lab prints matrices up to 6 by 6, and that one is ' + out.length + ' by ' + width };
    }
    return { M: out };
  }

  /* A matrix as a table. `split` tints every column from that index on, which
     is the augmented bar drawn with the one divider the stylesheet offers. */
  function Mtable(caption, M, opts) {
    opts = opts || {};
    if (!M || !M.length) return table(caption, [], [tr([tdl('(no rows)')])]);
    var rows = M.map(function (r, i) {
      var cells = r.map(function (v, j) {
        var cls = '';
        if (opts.split !== undefined && j >= opts.split) cls = 'on';
        if (opts.mark && opts.mark(i, j)) cls = 'on';
        return td(Rtext(v), cls);
      });
      var head = (opts.rowlabels && opts.rowlabels[i] !== undefined) ? opts.rowlabels[i] : ('R' + (i + 1));
      return tr([rowhead(head)].concat(cells), opts.focus === i ? 'focus' : '');
    });
    return table(caption, opts.heads ? [''].concat(opts.heads) : [], rows);
  }
  /* The trace: every operation with the matrix it produced. */
  function Mtrace(caption, start, ops, opts) {
    var blocks = [Mtable(caption + ' &mdash; the matrix as read', start, opts)];
    if (!ops.length) {
      blocks.push(steps(caption + ' &mdash; the operations', [['nothing to do', 'the matrix is already in that form']]));
      return blocks.join('');
    }
    ops.forEach(function (o, i) {
      blocks.push(Mtable('step ' + (i + 1) + ':  ' + o.op + '   (' + o.why + ')', o.after, opts));
    });
    return blocks.join('');
  }
"""


# --------------------------------------------------- exact evaluation, in n

EXACT_JS = r"""
  /* EXPR_JS evaluates a tree to a double, which is right for drawing and wrong
     for a sequence: the closed form 3*2^(n-1) at n = 40 is an integer with
     twelve digits, and a double would hand back the nearest one it could
     store. This evaluates the same tree in exact rationals instead, and
     returns the reason rather than a number wherever it cannot. */
  function Xeval(node, env) {
    if (!node) return { bad: 'there is nothing to evaluate' };
    switch (node.k) {
      case 'num': {
        var r = Rread(node.v);
        return r === null ? { bad: '"' + esc(node.v) + '" is not an exact number' } : { v: r };
      }
      case 'var': {
        if (env && Object.prototype.hasOwnProperty.call(env, node.v)) return { v: env[node.v] };
        return { bad: 'the letter "' + node.v + '" has no value here' };
      }
      case 'neg': { var a = Xeval(node.a, env); return a.bad ? a : { v: Rneg(a.v) }; }
      case 'add': case 'sub': case 'mul': case 'div': {
        var l = Xeval(node.a, env); if (l.bad) return l;
        var r2 = Xeval(node.b, env); if (r2.bad) return r2;
        if (node.k === 'add') return { v: Radd(l.v, r2.v) };
        if (node.k === 'sub') return { v: Rsub(l.v, r2.v) };
        if (node.k === 'mul') return { v: Rmul(l.v, r2.v) };
        if (Rzero(r2.v)) return { bad: 'that divides by zero' };
        return { v: Rdiv(l.v, r2.v) };
      }
      case 'pow': {
        var b = Xeval(node.a, env); if (b.bad) return b;
        var e = Xeval(node.b, env); if (e.bad) return e;
        if (!Rint(e.v)) return { bad: 'the exponent ' + Rtext(e.v) + ' is not a whole number, so the value is not rational' };
        if (e.v.n > 400n || e.v.n < -400n) return { bad: 'the exponent ' + Rtext(e.v) + ' is larger than this lab will print' };
        if (Rzero(b.v) && e.v.n < 0n) return { bad: '0 raised to a negative power divides by zero' };
        return { v: Rpow(b.v, Number(e.v.n)) };
      }
      case 'fn': return { bad: node.v + '(...) has no exact rational value in general' };
    }
    return { bad: 'I could not read that' };
  }
  function Xparse(text) {
    var s = String(text).trim();
    if (!s) return { bad: 'that box is empty' };
    try { return { node: Eparse(s) }; } catch (err) { return { bad: 'that does not parse: ' + esc(err.message) }; }
  }
"""


# ------------------------------------------ inequalities, decided not sampled

FEAS_JS = r"""
  /* A constraint is  a x + b y <= c , strictly when `strict`. Every >= is
     stored negated so there is exactly one direction to reason about, and an
     = becomes the two of them.

     Whether the region is empty, whether it runs off to infinity, and whether
     an objective grows without bound on it are the same question asked three
     times -- is this set of inequalities satisfiable -- so one routine answers
     all three. It is Fourier-Motzkin elimination on exact rationals. Testing a
     grid of sample points would answer "I did not find one", which is a
     different sentence from "there is none", and on the preset whose region is
     the single point (1, 1) the grid answers wrongly. */
  function Cnew(a, b, c, strict, src) { return { a: a, b: b, c: c, strict: !!strict, src: src || '' }; }
  function Cfromrow(row) {
    var a = row.c[0], b = row.c[1], c = row.b;
    if (row.rel === 'le') return [Cnew(a, b, c, false, row.src)];
    if (row.rel === 'lt') return [Cnew(a, b, c, true, row.src)];
    if (row.rel === 'ge') return [Cnew(Rneg(a), Rneg(b), Rneg(c), false, row.src)];
    if (row.rel === 'gt') return [Cnew(Rneg(a), Rneg(b), Rneg(c), true, row.src)];
    return [Cnew(a, b, c, false, row.src), Cnew(Rneg(a), Rneg(b), Rneg(c), false, row.src)];
  }
  function Cholds(k, x, y) {
    var cmp = Rcmp(Radd(Rmul(k.a, x), Rmul(k.b, y)), k.c);
    return k.strict ? cmp < 0 : cmp <= 0;
  }
  function Ctext(k, names) {
    return Ltext([k.a, k.b], names) + ' ' + (k.strict ? '&lt;' : '&lt;=') + ' ' + Rtext(k.c);
  }

  /* Eliminate y by pairing every upper bound with every lower bound, then read
     the surviving one-variable constraints off against each other. */
  function FMfeasible(cons) {
    var pos = [], neg = [], onex = [];
    cons.forEach(function (k) {
      if (Rsign(k.b) > 0) pos.push(k);
      else if (Rsign(k.b) < 0) neg.push(k);
      else onex.push(k);
    });
    pos.forEach(function (u) {
      neg.forEach(function (l) {
        /* (-l.b) * u  +  (u.b) * l  -- both multipliers positive, so both
           inequalities keep their direction, and the y terms cancel. */
        var s1 = Rneg(l.b), s2 = u.b;
        onex.push(Cnew(Radd(Rmul(s1, u.a), Rmul(s2, l.a)), R0,
                       Radd(Rmul(s1, u.c), Rmul(s2, l.c)), u.strict || l.strict, ''));
      });
    });
    var lo = null, loStrict = false, hi = null, hiStrict = false;
    for (var i = 0; i < onex.length; i += 1) {
      var k = onex[i], s = Rsign(k.a);
      if (s === 0) {
        var sc = Rsign(k.c);
        if (sc < 0 || (sc === 0 && k.strict)) {
          return { feasible: false, why: 'the constraints combine to 0 ' + (k.strict ? '&lt;' : '&lt;=')
            + ' ' + Rtext(k.c) + ', which no point can satisfy' };
        }
        continue;
      }
      var bound = Rdiv(k.c, k.a);
      if (s > 0) {
        if (hi === null || Rcmp(bound, hi) < 0) { hi = bound; hiStrict = k.strict; }
        else if (Requ(bound, hi) && k.strict) hiStrict = true;
      } else {
        if (lo === null || Rcmp(bound, lo) > 0) { lo = bound; loStrict = k.strict; }
        else if (Requ(bound, lo) && k.strict) loStrict = true;
      }
    }
    if (lo !== null && hi !== null) {
      var c2 = Rcmp(lo, hi);
      if (c2 > 0) {
        return { feasible: false, why: 'after eliminating y, x would have to be at least ' + Rtext(lo)
          + ' and at most ' + Rtext(hi) };
      }
      if (c2 === 0 && (loStrict || hiStrict)) {
        return { feasible: false, why: 'after eliminating y, x is squeezed onto ' + Rtext(lo)
          + ' and then excluded from it by a strict inequality' };
      }
    }
    return { feasible: true, lo: lo, hi: hi, loStrict: loStrict, hiStrict: hiStrict };
  }

  /* The directions the region goes on forever in: drop every constant, and the
     inequalities become a cone. "Is the region unbounded" is then "is there a
     non-zero direction in that cone", and "does cx + dy grow forever" is "is
     there one on which cx + dy is positive" -- both handed straight back to
     FMfeasible, which is why neither is a guess. */
  function Crec(cons) { return cons.map(function (k) { return Cnew(k.a, k.b, R0, false, ''); }); }
  function Cgrows(cons, ox, oy) {
    if (Rzero(ox) && Rzero(oy)) return false;
    return FMfeasible(Crec(cons).concat([Cnew(Rneg(ox), Rneg(oy), R(-1n), false, '')])).feasible;
  }
  function Cunbounded(cons) {
    var dirs = [[R1, R0], [R(-1n), R0], [R0, R1], [R0, R(-1n)]];
    for (var i = 0; i < dirs.length; i += 1) {
      if (Cgrows(cons, dirs[i][0], dirs[i][1])) return true;
    }
    return false;
  }

  /* Every point where two boundary lines meet, kept when it satisfies every
     constraint. `inRegion` is false for a point that sits on a boundary the
     reader wrote strictly -- it is a corner of the picture that is not a member
     of the set, which is the whole difference between < and <=. */
  function Ccorners(cons) {
    var out = [];
    for (var i = 0; i < cons.length; i += 1) {
      for (var j = i + 1; j < cons.length; j += 1) {
        var A = cons[i], B = cons[j];
        var det = Rsub(Rmul(A.a, B.b), Rmul(A.b, B.a));
        if (Rzero(det)) continue;
        var x = Rdiv(Rsub(Rmul(A.c, B.b), Rmul(A.b, B.c)), det);
        var y = Rdiv(Rsub(Rmul(A.a, B.c), Rmul(A.c, B.a)), det);
        var ok = true, inRegion = true;
        for (var t = 0; t < cons.length; t += 1) {
          var v = Radd(Rmul(cons[t].a, x), Rmul(cons[t].b, y));
          var cmp = Rcmp(v, cons[t].c);
          if (cmp > 0) { ok = false; break; }
          if (cons[t].strict && cmp === 0) inRegion = false;
        }
        if (!ok) continue;
        var seen = false;
        for (var q = 0; q < out.length; q += 1) {
          if (Requ(out[q].x, x) && Requ(out[q].y, y)) { out[q].from.push([i, j]); seen = true; break; }
        }
        if (!seen) out.push({ x: x, y: y, inRegion: inRegion, from: [[i, j]] });
      }
    }
    out.sort(function (p, q) { var c = Rcmp(p.x, q.x); return c !== 0 ? c : Rcmp(p.y, q.y); });
    return out;
  }
"""


# ------------------------------------------------------------ page helpers

def _esc(text):
    """HTML-escape a label that goes into markup this file writes."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _options(labels):
    """Preset options carry an INDEX, never the preset text.

    An inequality contains < and >, and those characters inside an attribute
    value break every regular expression that reads this page -- the test
    harness's included. The presets live in a JS literal instead, and the option
    only says which one of them to load.
    """
    return "".join('<option value="%d">%s</option>' % (i, _esc(label))
                   for i, label in enumerate(labels))


def _kpi(idbase):
    return (
        '        <div class="kpi-grid">\n'
        '          <div class="kpi"><span id="%sK1Lab">&mdash;</span><strong id="%sK1">&mdash;</strong></div>\n'
        '          <div class="kpi"><span id="%sK2Lab">&mdash;</span><strong id="%sK2">&mdash;</strong></div>\n'
        '          <div class="kpi"><span id="%sK3Lab">&mdash;</span><strong id="%sK3">&mdash;</strong></div>\n'
        "        </div>\n" % ((idbase,) * 6)
    )


# ==========================================================================
# Lab 1: systems of linear equations and inequalities.
# ==========================================================================

# Presets carry the equations as text, because the reader's input IS text and a
# preset that skipped the parser would be exercising a path the reader never
# takes. Each list ends with the case that breaks: parallel lines, a repeated
# equation, a rank that drops, an empty feasible region, an objective with
# nowhere to stop.
SYS_PRESETS = {
    "graph": [
        {"label": "one solution: the lines cross exactly once",
         "eq": ["2x + 3y = 12", "x - y = 1"]},
        {"label": "no solution: the same slope, a different intercept",
         "eq": ["2x + 3y = 12", "4x + 6y = 7"]},
        {"label": "infinitely many: the second line IS the first",
         "eq": ["2x + 3y = 12", "4x + 6y = 24"]},
        {"label": "the crossing point is not a lattice point",
         "eq": ["3x + 2y = 4", "5x - 7y = 1"]},
        {"label": "a vertical line and a horizontal one",
         "eq": ["x = 3", "y = -2"]},
        {"label": "both lines through the origin",
         "eq": ["y = 2x", "y = -x/3"]},
    ],
    "substitution": [
        {"label": "one equation already gives y",
         "eq": ["y = 2x - 1", "3x + 2y = 12"], "pick": "0,1"},
        {"label": "the coefficient is not 1, so a fraction appears at once",
         "eq": ["3x + 2y = 7", "5x - y = 3"], "pick": "0,0"},
        {"label": "the substitution ends at 0 = 5, which is false",
         "eq": ["x + y = 4", "2x + 2y = 13"], "pick": "0,1"},
        {"label": "the substitution ends at 0 = 0, which is true for every x",
         "eq": ["x + y = 4", "3x + 3y = 12"], "pick": "0,1"},
        {"label": "fractions in the equations, exact all the way down",
         "eq": ["x/2 + y/3 = 1", "x - y = 1"], "pick": "1,0"},
        {"label": "the unknown you chose is missing from that equation",
         "eq": ["2x = 6", "x + y = 5"], "pick": "0,1"},
    ],
    "elimination": [
        {"label": "multiply one equation only",
         "eq": ["x + 2y = 7", "3x - y = 7"], "pick": "0"},
        {"label": "multiply both: the lcm of 2 and 3",
         "eq": ["2x + 3y = 5", "3x - 2y = 14"], "pick": "0"},
        {"label": "both unknowns vanish and 0 = 9 is left",
         "eq": ["2x - y = 4", "6x - 3y = 3"], "pick": "0"},
        {"label": "both unknowns vanish and 0 = 0 is left",
         "eq": ["2x - y = 4", "6x - 3y = 12"], "pick": "0"},
        {"label": "fractional coefficients, and an answer over 17",
         "eq": ["x/2 + y/3 = 4", "x/3 - y/4 = 1"], "pick": "0"},
        {"label": "one equation has no y to eliminate",
         "eq": ["3x = 9", "2x + 5y = 13"], "pick": "1"},
    ],
    "three": [
        {"label": "one solution: (1, 2, 3)",
         "eq": ["x + y + z = 6", "2x - y + z = 3", "x + 2y - z = 2"]},
        {"label": "inconsistent: the last row reduces to 0 = 1",
         "eq": ["x + y + z = 2", "2x + 3y + z = 5", "3x + 4y + 2z = 8"]},
        {"label": "dependent: rank 2, so a whole line of solutions",
         "eq": ["x + y + z = 2", "2x + 3y + z = 5", "3x + 4y + 2z = 7"]},
        {"label": "the first pivot is 0, so a swap comes first",
         "eq": ["y + z = 3", "x + 2y - z = 1", "2x - y + z = 4"]},
        {"label": "fractions typed in, whole numbers out",
         "eq": ["x/2 + y/3 - z/4 = 1", "x - y + z = 0", "2x + y - z = 3"]},
        {"label": "rank 1: three copies of one plane, two free unknowns",
         "eq": ["x + 2y - z = 1", "2x + 4y - 2z = 2", "3x + 6y - 3z = 3"]},
    ],
    "inequalities": [
        {"label": "a bounded quadrilateral in the first quadrant",
         "eq": ["x >= 0", "y >= 0", "x + 2y <= 8", "3x + y <= 9"]},
        {"label": "unbounded: the region runs off to the north-east",
         "eq": ["x + y >= 4", "2x + y >= 5", "x >= 0", "y >= 0"]},
        {"label": "empty: no point satisfies all four",
         "eq": ["x + y <= 1", "x + y >= 4", "x >= 0", "y >= 0"]},
        {"label": "strict: the corners are drawn and then excluded",
         "eq": ["x + y < 4", "y > x", "x > 0", ""]},
        {"label": "the region is the single point (1, 1)",
         "eq": ["x + y <= 2", "x + y >= 2", "x - y <= 0", "x - y >= 0"]},
        {"label": "fractional boundaries",
         "eq": ["x/2 + y/3 <= 2", "y >= x/4", "x >= 0", "y >= 0"]},
    ],
    "linprog": [
        {"label": "maximise 3x + 2y on a bounded region",
         "eq": ["x >= 0", "y >= 0", "x + 2y <= 8", "3x + y <= 9"],
         "obj": "3x + 2y", "sense": "max"},
        {"label": "minimise 3x + 4y where the region is open above",
         "eq": ["x + y >= 4", "2x + y >= 5", "x >= 0", "y >= 0"],
         "obj": "3x + 4y", "sense": "min"},
        {"label": "the optimum is a whole EDGE, and two corners tie",
         "eq": ["x >= 0", "y >= 0", "x + y <= 5", "x + 2y <= 8"],
         "obj": "2x + 2y", "sense": "max"},
        {"label": "unbounded: the objective has nowhere to stop",
         "eq": ["x >= 0", "y >= 0", "y <= x + 2", ""],
         "obj": "x + y", "sense": "max"},
        {"label": "infeasible: there is no corner to evaluate",
         "eq": ["x + y <= 1", "x + y >= 4", "x >= 0", "y >= 0"],
         "obj": "x + y", "sense": "max"},
        {"label": "the optimal corner is (20/19, 45/19)",
         "eq": ["x >= 0", "y >= 0", "3x + 5y <= 15", "5x + 2y <= 10"],
         "obj": "4x + 3y", "sense": "max"},
    ],
}

SYS_TITLES = {
    "graph": ("Two lines, and where they meet",
              "One solution, none, or infinitely many -- decided by rank, drawn by sampling"),
    "substitution": ("Solving by substitution",
                     "Isolate one unknown, put it in the other equation, and check the answer"),
    "elimination": ("Solving by elimination",
                    "Multipliers from the lcm, and the unknown that cancels"),
    "three": ("Three equations, three unknowns",
              "Gaussian elimination on the augmented matrix, then back substitution"),
    "inequalities": ("Systems of inequalities",
                     "The feasible region, its corners, and whether it is empty"),
    "linprog": ("Linear programming",
                "The objective at every corner, and the corner that wins"),
}

SYS_VARS = {"three": ["x", "y", "z"]}
SYS_LINES = {"graph": 2, "substitution": 2, "elimination": 2,
             "three": 3, "inequalities": 4, "linprog": 4}
SYS_PLOT = ("graph", "inequalities", "linprog")
SYS_PICK = ("substitution", "elimination")

SYS_LEGENDS = {
    "graph": '<span class="tone-cyan"><i class="legend-swatch"></i>equation 1</span>'
             '<span class="tone-purple"><i class="legend-swatch"></i>equation 2</span>'
             '<span class="tone-green"><i class="legend-swatch"></i>the solution</span>',
    # The two region modes draw a boundary the reader may have written strictly,
    # and a dashed line is the only way a picture can say "this edge is not part
    # of the set" -- so their legends name that distinction explicitly.
    "inequalities": '<span class="tone-cyan"><i class="legend-swatch"></i>the feasible region</span>'
                    '<span class="tone-purple"><i class="legend-swatch"></i>an included boundary</span>'
                    '<span class="tone-muted"><i class="legend-swatch"></i>a strict boundary</span>'
                    '<span class="tone-amber"><i class="legend-swatch"></i>corners</span>',
    "linprog": '<span class="tone-cyan"><i class="legend-swatch"></i>the feasible region</span>'
               '<span class="tone-purple"><i class="legend-swatch"></i>a boundary</span>'
               '<span class="tone-amber"><i class="legend-swatch"></i>corners</span>'
               '<span class="tone-green"><i class="legend-swatch"></i>the winning corner</span>',
}
SYS_LEGEND_DEFAULT = ('<span class="tone-cyan"><i class="legend-swatch"></i>exact fractions throughout</span>'
                      '<span class="tone-amber"><i class="legend-swatch"></i>every step shown</span>')


SYS_SCRIPT = r"""
  var MODE = '__MODE__';
  var VARS = __VARS__;
  var NLINES = __NLINES__;
  var HASPLOT = __HASPLOT__, HASPICK = __HASPICK__, HASOBJ = __HASOBJ__;
  var NV = VARS.length;

  var preset = document.getElementById('syPreset');
  var eqIn = [];
  for (var q = 1; q <= NLINES; q += 1) eqIn.push(document.getElementById('syEq' + q));
  var objIn = HASOBJ ? document.getElementById('syObj') : null;
  var senseIn = HASOBJ ? document.getElementById('sySense') : null;
  var pickIn = HASPICK ? document.getElementById('syPick') : null;
  var svg = HASPLOT ? document.getElementById('syPlot') : null;
  var work = document.getElementById('syWork');
  var status = document.getElementById('syStatus');
  var titleOut = document.getElementById('syTitle'), subOut = document.getElementById('sySub');
  var k1 = document.getElementById('syK1'), k2 = document.getElementById('syK2'), k3 = document.getElementById('syK3');
  var k1L = document.getElementById('syK1Lab'), k2L = document.getElementById('syK2Lab'), k3L = document.getElementById('syK3Lab');

  function setkpi(a, av, b, bv, c, cv) {
    k1L.textContent = a; k1.textContent = av;
    k2L.textContent = b; k2.textContent = bv;
    k3L.textContent = c; k3.textContent = cv;
  }
  function pointtext(p) {
    return '(' + p.map(function (v) { return Rtext(v); }).join(', ') + ')';
  }

  /* ---- reading what is in the boxes ---- */
  function readLines() {
    var rows = [], bad = [], empty = [], seen = [];
    for (var i = 0; i < eqIn.length; i += 1) {
      var text = String(eqIn[i].value || '');
      seen.push(text);
      if (!text.trim()) { empty.push(i + 1); continue; }
      var r = Lequation(text, VARS);
      if (r.bad) { bad.push({ line: i + 1, why: r.bad, src: text }); continue; }
      r.line = i + 1;
      rows.push(r);
    }
    return { rows: rows, bad: bad, empty: empty, seen: seen };
  }
  /* Always painted, whatever else went wrong, so a reader who typed nonsense
     can see which box holds it. */
  function asreadtable(read) {
    var body = [];
    for (var i = 0; i < read.seen.length; i += 1) {
      var text = read.seen[i], why = null, row = null;
      for (var b = 0; b < read.bad.length; b += 1) if (read.bad[b].line === i + 1) why = read.bad[b].why;
      for (var r = 0; r < read.rows.length; r += 1) if (read.rows[r].line === i + 1) row = read.rows[r];
      var right = why ? tone(why, 'red') : (row ? Rowtext(row, VARS) : tone('empty &mdash; skipped', 'muted'));
      body.push(tr([rowhead('box ' + (i + 1)), tdl(esc(text.trim()) || '(nothing typed)'), tdl(right)]));
    }
    return table('What is in each box, and what it became',
                 ['', 'as typed', 'moved to the standard form'], body);
  }
  function fail(html, read) {
    if (svg) svg.textContent = '';
    work.innerHTML = read ? asreadtable(read) : '';
    status.innerHTML = html;
    setkpi('status', 'stuck', 'reason', 'see below', 'fix', 'the box named above');
  }

  /* ---- the classification, from rank and from nothing else ---- */
  function solveSystem(rows, nv) {
    var Ab = rows.map(function (r) { return r.c.concat([r.b]); });
    var red = Mrref(Ab, { cols: nv });
    var rankA = red.rank;
    var rankAb = Mrref(Ab).rank;
    var badrow = -1;
    for (var i = 0; i < red.M.length; i += 1) {
      var allzero = true;
      for (var j = 0; j < nv; j += 1) if (!Rzero(red.M[i][j])) { allzero = false; break; }
      if (allzero && !Rzero(red.M[i][nv])) { badrow = i; break; }
    }
    if (badrow >= 0) return { kind: 'none', red: red, rankA: rankA, rankAb: rankAb, badrow: badrow, Ab: Ab };
    if (rankA < nv) {
      var free = [];
      for (var c = 0; c < nv; c += 1) if (red.pivots.indexOf(c) < 0) free.push(c);
      return { kind: 'many', red: red, rankA: rankA, rankAb: rankAb, free: free, Ab: Ab };
    }
    var x = [];
    for (var v = 0; v < nv; v += 1) x.push(red.M[red.pivots.indexOf(v)][nv]);
    return { kind: 'one', red: red, rankA: rankA, rankAb: rankAb, x: x, Ab: Ab };
  }
  /* The answer put back into the equations AS TYPED. Every mode ends here,
     because a method that produced a number and never checked it has not
     finished, and because this is the one table that would catch a bug in
     everything above it. */
  function checktable(rows, point) {
    return table('Substituted back into the equations as they were typed',
      ['as typed', 'left side', 'right side', 'holds?'],
      rows.map(function (row) {
        var lhs = Rowvalue(row, point), cmp = Rcmp(lhs, row.b);
        var ok = row.rel === 'eq' ? cmp === 0
          : (row.rel === 'le' ? cmp <= 0 : (row.rel === 'lt' ? cmp < 0
          : (row.rel === 'ge' ? cmp >= 0 : cmp > 0)));
        return tr([tdl(esc(row.src)), td(Rtext(lhs)), td(Rtext(row.b)),
                   td(ok ? chip('yes', 'ok') : chip('no', 'no'))]);
      }));
  }
  function rankblock(sol, nv) {
    return table('Rank decides the number of solutions, and nothing else does',
      ['quantity', 'value', 'what it says'], [
        tr([rowhead('rank of A'), td(String(sol.rankA)),
            tdl('the number of independent directions in the left-hand sides')]),
        tr([rowhead('rank of [A | b]'), td(String(sol.rankAb)),
            tdl('the same count once the constants are carried along')]),
        tr([rowhead('unknowns'), td(String(nv)), tdl(VARS.join(', '))]),
        tr([rowhead('verdict'), tdl(sol.kind === 'none'
              ? 'rank [A | b] is bigger than rank A, so the constants ask for something the left sides cannot deliver: NO solution'
              : (sol.kind === 'many'
                 ? 'the ranks agree at ' + sol.rankA + ', below the ' + nv + ' unknowns, so '
                   + (nv - sol.rankA) + ' of them ' + plural(nv - sol.rankA, 'is', 'are')
                   + ' free: INFINITELY many solutions'
                 : 'the ranks agree and equal the number of unknowns: exactly ONE solution'))]),
      ]);
  }
  /* The general solution, written with the free unknowns named. */
  function familytext(sol, nv) {
    var pivots = sol.red.pivots, out = [];
    for (var c = 0; c < nv; c += 1) {
      if (pivots.indexOf(c) < 0) { out.push(VARS[c] + ' is free'); continue; }
      var r = pivots.indexOf(c), parts = [], konst = sol.red.M[r][nv];
      for (var j = 0; j < nv; j += 1) {
        if (j === c || Rzero(sol.red.M[r][j])) continue;
        var m = Rneg(sol.red.M[r][j]);
        parts.push((Rsign(m) < 0 ? ' - ' : ' + ') + (Requ(Rabs(m), R1) ? '' : Rterm(Rabs(m))) + VARS[j]);
      }
      out.push(VARS[c] + ' = ' + Rtext(konst) + parts.join(''));
    }
    return out.join(',   ');
  }

  /* ---- windows for the picture ---- */
  function windowFor(xs, ys) {
    var fx = xs.filter(isFinite), fy = ys.filter(isFinite);
    var cx = 0, cy = 0, d = 0, i;
    if (fx.length) { cx = 0; for (i = 0; i < fx.length; i += 1) cx += fx[i]; cx /= fx.length; }
    if (fy.length) { cy = 0; for (i = 0; i < fy.length; i += 1) cy += fy[i]; cy /= fy.length; }
    for (i = 0; i < fx.length; i += 1) d = Math.max(d, Math.abs(fx[i] - cx));
    for (i = 0; i < fy.length; i += 1) d = Math.max(d, Math.abs(fy[i] - cy) / 0.62);
    var span = Math.max(9, d * 2.8);
    return { xmin: cx - span / 2, xmax: cx + span / 2,
             ymin: cy - span * 0.62 / 2, ymax: cy + span * 0.62 / 2 };
  }
  function lineinfo(row) {
    var a = row.c[0], b = row.c[1];
    if (Rzero(a) && Rzero(b)) {
      return { kind: 'flat', text: 'no ' + VARS[0] + ' and no ' + VARS[1] + ' are left: this reads 0 = '
        + Rtext(row.b) + ', ' + (Rzero(row.b) ? 'true everywhere, so it draws nothing'
        : 'false everywhere, so nothing satisfies it') };
    }
    if (Rzero(b)) {
      var at = Rdiv(row.b, a);
      return { kind: 'vertical', at: at, text: VARS[0] + ' = ' + Rtext(at) + ' &mdash; vertical, so it has no slope' };
    }
    var m = Rdiv(Rneg(a), b), c0 = Rdiv(row.b, b);
    return { kind: 'slope', m: m, c0: c0,
             text: VARS[1] + ' = ' + Ptext([c0, m], VARS[0]) };
  }
  function drawline(plot, info, cls, win) {
    if (info.kind === 'vertical') {
      plot.segment(Rnum(info.at), win.ymin, Rnum(info.at), win.ymax, cls);
    } else if (info.kind === 'slope') {
      var m = Rnum(info.m), c0 = Rnum(info.c0);
      plot.curve(function (x) { return m * x + c0; }, cls);
    }
  }

  /* ================================================== mode: graph ======== */
  function paintGraph(rows) {
    var sol = solveSystem(rows, 2);
    var infos = rows.map(lineinfo);
    var blocks = [];
    blocks.push(table('The two lines, as read', ['as typed', 'standard form', 'the form the picture uses'],
      rows.map(function (row, i) {
        return tr([tdl(esc(row.src)), tdl(Rowtext(row, VARS)), tdl(infos[i].text)]);
      })));
    blocks.push(Mtable('The augmented matrix [A | b] &mdash; constants tinted', sol.Ab,
      { split: 2, heads: VARS.concat(['=']) }));
    /* Gauss-Jordan is run on the COEFFICIENT columns only, and the constants
       are carried rather than pivoted on. That is what leaves an inconsistent
       system reading 0 = -17 instead of collapsing to the row 0 0 | 1, and it
       is why this table is not the reduced row echelon form of the augmented
       matrix -- the matrix lab, which reduces every column, will give a
       different (and equally correct) answer for the same numbers. The caption
       says which of the two it is so the reader is never left to guess. */
    blocks.push(Mtable('...and the same matrix with the ' + VARS[0] + ' and ' + VARS[1]
      + ' columns fully reduced, the constants carried along', sol.red.M,
      { split: 2, heads: VARS.concat(['=']) }));
    blocks.push(rankblock(sol, 2));
    if (sol.kind === 'one') blocks.push(checktable(rows, sol.x));
    work.innerHTML = blocks.join('');

    var xs = [], ys = [];
    if (sol.kind === 'one') { xs.push(Rnum(sol.x[0])); ys.push(Rnum(sol.x[1])); }
    infos.forEach(function (info) {
      if (info.kind === 'vertical') xs.push(Rnum(info.at));
      else if (info.kind === 'slope') {
        ys.push(Rnum(info.c0));
        if (!Rzero(info.m)) xs.push(Rnum(Rdiv(Rneg(info.c0), info.m)));
      }
    });
    var win = windowFor(xs, ys);
    var plot = Plot(svg, win);
    plot.frame();
    drawline(plot, infos[0], 'plot-curve', win);
    drawline(plot, infos[1], 'plot-curve alt', win);
    if (sol.kind === 'one') {
      plot.point(Rnum(sol.x[0]), Rnum(sol.x[1]), 'plot-point root', pointtext(sol.x));
    }
    plot.describe('Two lines drawn by evaluating each of them at 480 points, '
      + (sol.kind === 'one' ? 'with their single crossing point marked at ' + pointtext(sol.x)
         : (sol.kind === 'none' ? 'parallel and never meeting' : 'lying exactly on top of each other')) + '.');

    setkpi('rank A', String(sol.rankA), 'rank [A|b]', String(sol.rankAb), 'solutions',
      sol.kind === 'one' ? '1' : (sol.kind === 'none' ? '0' : 'infinitely many'));

    if (sol.kind === 'one') {
      status.innerHTML = '<strong>The lines cross once, at ' + pointtext(sol.x) + '.</strong> '
        + 'The two ranks are both 2 and there are 2 unknowns, which is the whole reason there is '
        + 'exactly one crossing point. The check table above put that pair back into the '
        + 'equations as you typed them, fractions and all &mdash; the picture agrees with it '
        + 'because the marked point and the two curves came out of the same numbers.';
    } else if (sol.kind === 'none') {
      status.innerHTML = '<strong>The lines are parallel and distinct, so there is no solution.</strong> '
        + 'Row reduction turned row ' + (sol.badrow + 1) + ' into 0 = '
        + Rtext(sol.red.M[sol.badrow][2]) + ', which no pair of numbers can satisfy. Notice that '
        + 'rank A is ' + sol.rankA + ' but rank [A | b] is ' + sol.rankAb + ': the constants are '
        + 'asking for something the left-hand sides cannot produce. Both lines are still drawn '
        + 'above, and they never meet inside the window or outside it.';
    } else {
      /* rank A can be 1 (one line, one free unknown) or 0 (both equations
         reduced to 0 = 0, so every point of the plane is a solution). The
         count of free unknowns comes from the rank, never from the shape of
         what was typed, so this sentence cannot drift away from the verdict
         table above it. */
      var freeN = 2 - sol.rankA;
      status.innerHTML = '<strong>' + (sol.rankA === 0
          ? 'Both equations reduced to 0 = 0, so every point of the plane is a solution.'
          : 'The two equations describe the same line, so every point on it is a solution.')
        + '</strong> The ranks agree at ' + sol.rankA + ', ' + freeN + ' short of the 2 unknowns, so '
        + freeN + ' of them ' + plural(freeN, 'is', 'are') + ' free: ' + familytext(sol, 2) + '. '
        + (sol.rankA === 0
           ? 'Nothing is drawn above because neither equation constrains a point: a line needs at '
             + 'least one non-zero coefficient. '
           : 'Only one line is visible above because the second is drawn exactly on top of the '
             + 'first. ')
        + '"Infinitely many" is not the same as "any pair you like" &mdash; the pairs still have to '
        + 'satisfy what is left of the system.';
    }
  }

  /* ============================================ mode: substitution ======= */
  function paintSubst(rows) {
    var choice = String((pickIn && pickIn.value) || '0,1').split(',');
    var li = Math.max(0, Math.min(1, parseInt(choice[0], 10) || 0));
    var vi = Math.max(0, Math.min(1, parseInt(choice[1], 10) || 0));
    var wi = 1 - vi;
    var eq = rows[li], other = rows[1 - li];
    var sol = solveSystem(rows, 2);
    var lines = [];
    lines.push(['the two equations, as typed and as arranged',
      'equation 1:  ' + esc(rows[0].src) + '  &rarr;  ' + Rowtext(rows[0], VARS)
        + '<br>equation 2:  ' + esc(rows[1].src) + '  &rarr;  ' + Rowtext(rows[1], VARS)]);

    var cv = eq.c[vi], cw = eq.c[wi];
    if (Rzero(cv)) {
      work.innerHTML = steps('Substitution, step by step', lines.concat([[
        'isolate ' + VARS[vi] + ' in equation ' + (li + 1),
        'that equation is ' + Rowtext(eq, VARS) + ', and the coefficient of ' + VARS[vi]
          + ' in it is 0. There is no ' + VARS[vi] + ' there to isolate, so this choice cannot start. '
          + 'Pick a different unknown or a different equation in the control beside the boxes.']]))
        + rankblock(sol, 2);
      setkpi('isolating', VARS[vi] + ' in eq ' + (li + 1), 'coefficient', '0', 'status', 'cannot start');
      status.innerHTML = '<strong>Equation ' + (li + 1) + ' has no ' + VARS[vi] + ' in it.</strong> '
        + 'Substitution needs an equation you can rearrange into "' + VARS[vi] + ' = something", and '
        + Rowtext(eq, VARS) + ' is not one. That is not a dead end for the system, only for this '
        + 'starting move: the other three choices in the control are all still open, and the rank '
        + 'table below already knows how many solutions there are.';
      return;
    }
    /* v = konst + slope * w, exactly. */
    var konst = Rdiv(eq.b, cv), slope = Rneg(Rdiv(cw, cv));
    var isoText = VARS[vi] + ' = ' + Ptext([konst, slope], VARS[wi]);
    lines.push(['isolate ' + VARS[vi] + ' in equation ' + (li + 1),
      Rowtext(eq, VARS) + '  &rarr;  ' + termtext(cv, VARS[vi]) + ' = '
        + Ptext([eq.b, Rneg(cw)], VARS[wi]) + '  &rarr;  ' + isoText]);
    lines.push(['put that into equation ' + (2 - li),
      termtext(other.c[vi], '(' + Ptext([konst, slope], VARS[wi]) + ')')
        + plusterm(other.c[wi], VARS[wi]) + ' = ' + Rtext(other.b)]);
    var A = Radd(other.c[wi], Rmul(other.c[vi], slope));
    var B = Rsub(other.b, Rmul(other.c[vi], konst));
    lines.push(['collect the ' + VARS[wi] + ' terms',
      (Rzero(A) ? '0' + VARS[wi] : termtext(A, VARS[wi])) + ' = ' + Rtext(B)]);

    var point = null;
    if (!Rzero(A)) {
      var w = Rdiv(B, A);
      lines.push(['solve for ' + VARS[wi],
        VARS[wi] + ' = ' + Rterm(B) + ' / ' + Rterm(A) + ' = ' + Rtext(w)]);
      var v = Radd(konst, Rmul(slope, w));
      lines.push(['back-substitute into ' + isoText,
        'at ' + VARS[wi] + ' = ' + Rtext(w) + ',  ' + VARS[vi] + ' = ' + Rtext(konst)
          + plusterm(slope, '(' + Rtext(w) + ')') + ' = ' + Rtext(v)]);
      point = [];
      point[vi] = v; point[wi] = w;
      lines.push(['the solution', pointtext(point)]);
    } else if (Rzero(B)) {
      lines.push(['what is left', '0 = 0, which is true whatever ' + VARS[wi] + ' is']);
    } else {
      lines.push(['what is left', '0 = ' + Rtext(B) + ', which is false whatever ' + VARS[wi] + ' is']);
    }

    var blocks = [steps('Substitution, step by step', lines), rankblock(sol, 2)];
    if (point) blocks.push(checktable(rows, point));
    work.innerHTML = blocks.join('');

    setkpi('isolated', VARS[vi] + ' from eq ' + (li + 1),
      VARS[wi], point ? Rtext(point[wi]) : '--',
      VARS[vi], point ? Rtext(point[vi]) : '--');

    if (point) {
      var agrees = sol.kind === 'one' && Requ(point[0], sol.x[0]) && Requ(point[1], sol.x[1]);
      status.innerHTML = '<strong>' + pointtext(point) + '.</strong> Substitution and row reduction '
        + 'were run separately on the same two equations, and they '
        + (agrees ? 'agree' : 'DISAGREE, which is a bug and not a lesson') + '. That is the only '
        + 'evidence worth having: the trace above never looked at the rank table, and the rank '
        + 'table never looked at the trace. Every value in the trace is an exact fraction, so the '
        + 'answer is ' + pointtext(point) + ' rather than a decimal that is nearly it.';
    } else if (Rzero(A) && Rzero(B)) {
      status.innerHTML = '<strong>The unknown vanished and 0 = 0 was left.</strong> That is not a '
        + 'failure of the method and it does not mean "no solution" &mdash; it means the second '
        + 'equation said nothing the first had not already said. Every point on the line '
        + Rowtext(rows[0], VARS) + ' solves the system, so the answer is a whole line: '
        + familytext(sol, 2) + '.';
    } else {
      status.innerHTML = '<strong>The unknown vanished and 0 = ' + Rtext(B) + ' was left.</strong> '
        + 'A number cannot equal a different number, so no pair (' + VARS[0] + ', ' + VARS[1]
        + ') satisfies both equations. The two lines are parallel. Notice what substitution did NOT '
        + 'do here: it did not produce a wrong answer, it produced a false statement, and the false '
        + 'statement is the answer.';
    }
  }

  /* ============================================== mode: elimination ====== */
  function paintElim(rows) {
    var vi = Math.max(0, Math.min(1, parseInt(String((pickIn && pickIn.value) || '0'), 10) || 0));
    var wi = 1 - vi;
    var sol = solveSystem(rows, 2);
    var c1 = rows[0].c[vi], c2 = rows[1].c[vi];
    var lines = [];
    lines.push(['the two equations, as typed and as arranged',
      'equation 1:  ' + esc(rows[0].src) + '  &rarr;  ' + Rowtext(rows[0], VARS)
        + '<br>equation 2:  ' + esc(rows[1].src) + '  &rarr;  ' + Rowtext(rows[1], VARS)]);
    lines.push(['coefficients of ' + VARS[vi],
      'equation 1 has ' + Rtext(c1) + ', equation 2 has ' + Rtext(c2)]);

    var red = null;
    if (Rzero(c1) && Rzero(c2)) {
      lines.push(['nothing to eliminate',
        'neither equation contains ' + VARS[vi] + ', so it is already gone and the system is really '
          + 'about ' + VARS[wi] + ' alone']);
      red = { c: rows[0].c.slice(), b: rows[0].b };
    } else if (Rzero(c1)) {
      lines.push(['already eliminated',
        'equation 1 has no ' + VARS[vi] + ', so no multiplying is needed: use it as it stands']);
      red = { c: rows[0].c.slice(), b: rows[0].b };
    } else if (Rzero(c2)) {
      lines.push(['already eliminated',
        'equation 2 has no ' + VARS[vi] + ', so no multiplying is needed: use it as it stands']);
      red = { c: rows[1].c.slice(), b: rows[1].b };
    } else {
      var l = Rlcm(c1, c2), m1 = Rdiv(l, c1), m2 = Rdiv(l, c2);
      lines.push(['the least common multiple of ' + Rtext(c1) + ' and ' + Rtext(c2),
        Rtext(l) + ', so equation 1 is multiplied by ' + Rtext(m1) + ' and equation 2 by ' + Rtext(m2)
          + '. Both then carry ' + termtext(l, VARS[vi]) + ', and subtracting removes it.']);
      var e1 = { c: rows[0].c.map(function (r) { return Rmul(r, m1); }), b: Rmul(rows[0].b, m1), rel: 'eq' };
      var e2 = { c: rows[1].c.map(function (r) { return Rmul(r, m2); }), b: Rmul(rows[1].b, m2), rel: 'eq' };
      lines.push(['multiply equation 1 by ' + Rtext(m1), Rowtext(e1, VARS)]);
      lines.push(['multiply equation 2 by ' + Rtext(m2), Rowtext(e2, VARS)]);
      red = { c: [Rsub(e1.c[0], e2.c[0]), Rsub(e1.c[1], e2.c[1])], b: Rsub(e1.b, e2.b) };
      lines.push(['subtract the second from the first',
        Ltext(red.c, VARS) + ' = ' + Rtext(red.b)]);
    }

    var A = red.c[wi], B = red.b, point = null;
    if (!Rzero(A)) {
      var w = Rdiv(B, A);
      lines.push(['solve for ' + VARS[wi], termtext(A, VARS[wi]) + ' = ' + Rtext(B)
        + ',  so ' + VARS[wi] + ' = ' + Rterm(B) + ' / ' + Rterm(A) + ' = ' + Rtext(w)]);
      var srcRow = !Rzero(rows[0].c[vi]) ? rows[0] : (!Rzero(rows[1].c[vi]) ? rows[1] : null);
      if (srcRow) {
        var v = Rdiv(Rsub(srcRow.b, Rmul(srcRow.c[wi], w)), srcRow.c[vi]);
        lines.push(['back-substitute into ' + Rowtext(srcRow, VARS),
          termtext(srcRow.c[vi], VARS[vi]) + plusterm(srcRow.c[wi], '(' + Rtext(w) + ')') + ' = '
            + Rtext(srcRow.b) + ',  so ' + VARS[vi] + ' = ' + Rtext(v)]);
        point = []; point[vi] = v; point[wi] = w;
        lines.push(['the solution', pointtext(point)]);
      } else {
        lines.push(['and ' + VARS[vi] + '?',
          'no equation contains ' + VARS[vi] + ', so it is free: any value works']);
      }
    } else if (Rzero(B)) {
      lines.push(['what is left', '0 = 0, true for every point on the line']);
    } else {
      lines.push(['what is left', '0 = ' + Rtext(B) + ', false for every point']);
    }

    var blocks = [steps('Elimination, step by step', lines), rankblock(sol, 2)];
    if (point) blocks.push(checktable(rows, point));
    work.innerHTML = blocks.join('');
    setkpi('eliminating', VARS[vi], VARS[wi], point ? Rtext(point[wi]) : '--',
           VARS[vi], point ? Rtext(point[vi]) : '--');

    if (point) {
      var agrees = sol.kind === 'one' && Requ(point[0], sol.x[0]) && Requ(point[1], sol.x[1]);
      status.innerHTML = '<strong>' + pointtext(point) + '.</strong> The multipliers came from the '
        + 'least common multiple of the two coefficients, which is why they are the smallest whole '
        + 'numbers that do the job rather than just any pair that works. Elimination and row '
        + 'reduction ran separately here and '
        + (agrees ? 'landed on the same pair' : 'DISAGREED, which is a bug and not a lesson') + '. '
        + 'Try eliminating the other unknown first: the trace changes completely and the answer does not.';
    } else if (Rzero(A) && Rzero(B)) {
      status.innerHTML = '<strong>Both unknowns cancelled and 0 = 0 was left.</strong> One equation '
        + 'is a multiple of the other, so the second added no information. The solutions are every '
        + 'point on ' + Rowtext(rows[0], VARS) + ': ' + familytext(sol, 2) + '. Rank sees the same '
        + 'thing from the other side &mdash; rank A is ' + sol.rankA + ' for two unknowns.';
    } else {
      status.innerHTML = '<strong>Both unknowns cancelled and 0 = ' + Rtext(B) + ' was left.</strong> '
        + 'That statement is false, so nothing satisfies both equations. This is the case worth '
        + 'sitting with: elimination did not break, it produced a contradiction, and a contradiction '
        + 'is a complete answer. The lines are parallel and distinct.';
    }
  }

  /* =================================================== mode: three ======= */
  function paintThree(rows) {
    var sol = solveSystem(rows, 3);
    var Ab = sol.Ab;
    var ech = Mgauss(Ab, 3);
    var heads = VARS.concat(['=']);
    var blocks = [];
    blocks.push(table('The system, as read', ['as typed', 'standard form'],
      rows.map(function (row) { return tr([tdl(esc(row.src)), tdl(Rowtext(row, VARS))]); })));
    blocks.push(Mtrace('Forward elimination on [A | b]', Ab, ech.ops, { split: 3, heads: heads }));

    var lines = [], point = null, contradiction = -1;
    for (var i = 0; i < ech.M.length; i += 1) {
      var allzero = true;
      for (var j = 0; j < 3; j += 1) if (!Rzero(ech.M[i][j])) { allzero = false; break; }
      if (allzero && !Rzero(ech.M[i][3])) { contradiction = i; break; }
    }
    if (contradiction >= 0) {
      lines.push(['row ' + (contradiction + 1) + ' of the echelon form',
        '0' + VARS[0] + ' + 0' + VARS[1] + ' + 0' + VARS[2] + ' = ' + Rtext(ech.M[contradiction][3])
          + ', which is false. Back substitution has nothing to substitute into.']);
    } else if (ech.pivots.length < 3) {
      lines.push(['not enough pivots',
        'the echelon form has ' + ech.pivots.length + ' pivot ' + plural(ech.pivots.length, 'column', 'columns')
          + ' for 3 unknowns, so back substitution runs out before it reaches every unknown. '
          + 'The reduced form below names the free ones.']);
    } else {
      var x = [];
      for (var r = ech.pivots.length - 1; r >= 0; r -= 1) {
        var col = ech.pivots[r], sum = ech.M[r][3], parts = [Rtext(ech.M[r][3])];
        for (var c = col + 1; c < 3; c += 1) {
          if (Rzero(ech.M[r][c])) continue;
          sum = Rsub(sum, Rmul(ech.M[r][c], x[c]));
          parts.push('(' + Rtext(ech.M[r][c]) + ')(' + Rtext(x[c]) + ')');
        }
        x[col] = Rdiv(sum, ech.M[r][col]);
        lines.push(['row ' + (r + 1) + ' gives ' + VARS[col],
          Ltext(ech.M[r].slice(0, 3), VARS) + ' = ' + Rtext(ech.M[r][3]) + ',  so ' + VARS[col]
            + ' = (' + parts.join(' - ') + ') / ' + Rterm(ech.M[r][col]) + ' = ' + Rtext(x[col])]);
      }
      point = x;
      lines.push(['the solution', pointtext(x)]);
    }
    blocks.push(steps('Back substitution, from the bottom row upward', lines));
    /* Coefficient columns only; see the note in paintGraph. The row count of
       this table is therefore NOT the rank of [A | b] -- two rows reading
       0 = 1 and 0 = 2 are one independent constraint between them, which is
       why the rank beside it is computed by a full reduction and not by
       counting the non-zero rows printed here. */
    blocks.push(Mtable('Gauss-Jordan takes it further: the ' + VARS.join(', ')
      + ' columns fully reduced, the constants carried along', sol.red.M,
      { split: 3, heads: heads }));
    blocks.push(rankblock(sol, 3));
    if (point) blocks.push(checktable(rows, point));
    work.innerHTML = blocks.join('');

    setkpi('rank A', String(sol.rankA), 'rank [A|b]', String(sol.rankAb),
           'solutions', sol.kind === 'one' ? '1' : (sol.kind === 'none' ? '0' : 'infinitely many'));

    if (point) {
      var agrees = sol.kind === 'one' && Requ(point[0], sol.x[0]) && Requ(point[1], sol.x[1])
        && Requ(point[2], sol.x[2]);
      status.innerHTML = '<strong>' + VARS[0] + ' = ' + Rtext(point[0]) + ', ' + VARS[1] + ' = '
        + Rtext(point[1]) + ', ' + VARS[2] + ' = ' + Rtext(point[2]) + '.</strong> Forward '
        + 'elimination plus back substitution and Gauss-Jordan are two different routes through the '
        + 'same matrix, and they ' + (agrees ? 'arrived together' : 'DISAGREED, which is a bug') + '. '
        + 'Every entry in the trace is an exact fraction; three floating-point row operations on this '
        + 'system would already have put rounding error into the third decimal place, and the check '
        + 'table would then show left and right sides that nearly match instead of matching.';
    } else if (sol.kind === 'none') {
      status.innerHTML = '<strong>No solution.</strong> Elimination drove one row to 0 = '
        + Rtext(ech.M[contradiction >= 0 ? contradiction : 0][3]) + '. Geometrically the three planes '
        + 'have no common point &mdash; they can still meet in pairs, which is why this case is easy '
        + 'to miss by drawing. Rank A is ' + sol.rankA + ' and rank [A | b] is ' + sol.rankAb + ', and '
        + 'that gap is the whole diagnosis.';
    } else {
      status.innerHTML = '<strong>Infinitely many solutions: ' + (3 - sol.rankA) + ' free '
        + plural(3 - sol.rankA, 'unknown', 'unknowns') + '.</strong> The ranks agree at ' + sol.rankA
        + ', below the 3 unknowns, so '
        + (sol.rankA === 2 ? 'the planes meet in a line rather than a point'
           : (sol.rankA === 1 ? 'all three equations describe one plane, and every point of it is a '
                                + 'solution'
                              : 'no equation constrains a point at all and every point of space is '
                                + 'a solution'))
        + '. Read the family off the '
        + 'reduced form: ' + familytext(sol, 3) + '. Choosing a value for each free unknown gives one '
        + 'actual solution, and the check table would pass on every one of them.';
    }
  }

  /* ---- shared by the two region modes ---- */
  function buildregion(rows) {
    var cons = [];
    rows.forEach(function (row) { Cfromrow(row).forEach(function (k) { cons.push(k); }); });
    var feas = FMfeasible(cons);
    var corners = feas.feasible ? Ccorners(cons) : [];
    return { cons: cons, feas: feas, corners: corners,
             unbounded: feas.feasible ? Cunbounded(cons) : false };
  }
  function drawregion(region, rows, extra) {
    var xs = [], ys = [];
    region.corners.forEach(function (p) { xs.push(Rnum(p.x)); ys.push(Rnum(p.y)); });
    if (!xs.length) { xs = [0]; ys = [0]; }
    var win = windowFor(xs, ys);
    var plot = Plot(svg, win);
    plot.frame();
    /* The shading is the one place a picture is sampled rather than decided:
       the grid is in pixels and so are its sample points. Every verdict printed
       below the picture -- empty, bounded, this corner wins -- is exact, and the
       strict boundaries are drawn dashed because no shading resolution could
       ever show that a boundary line is missing from its own region. */
    var nums = region.cons.map(function (k) { return [Rnum(k.a), Rnum(k.b), Rnum(k.c)]; });
    if (region.feas.feasible) {
      plot.shade(function (x, y) {
        for (var i = 0; i < nums.length; i += 1) {
          if (nums[i][0] * x + nums[i][1] * y > nums[i][2] + 1e-9) return false;
        }
        return true;
      });
    }
    region.cons.forEach(function (k) {
      drawline(plot, lineinfo({ c: [k.a, k.b], b: k.c }), k.strict ? 'plot-curve parent' : 'plot-curve alt', win);
    });
    region.corners.forEach(function (p) {
      if (!p.inRegion) plot.hole(Rnum(p.x), Rnum(p.y));
      else plot.point(Rnum(p.x), Rnum(p.y), 'plot-point', pointtext([p.x, p.y]));
    });
    if (extra) extra(plot, win);
    plot.describe('The feasible region of ' + rows.length + ' inequalities, shaded by testing every '
      + 'sample point against all of them, with ' + region.corners.length + ' corner '
      + plural(region.corners.length, 'point', 'points') + ' marked.');
    return { plot: plot, win: win };
  }
  /* Numbered over the CONSTRAINT list rather than the boxes, because an
     equality typed into one box becomes two constraints and the corner table
     names them individually. A reader who sees "C3 with C4" can find C3 here. */
  function constable(region) {
    return table('Each constraint, and what it says about the origin',
      ['', 'as typed', 'rewritten as  ... &lt;= number', 'boundary line', 'is (0, 0) in it?'],
      region.cons.map(function (k, i) {
        var ok = Cholds(k, R0, R0);
        return tr([rowhead('C' + (i + 1)), tdl(esc(k.src)), tdl(Ctext(k, VARS)),
                   tdl(lineinfo({ c: [k.a, k.b], b: k.c }).text),
                   td(ok ? chip('yes', 'ok') : chip('no', 'no'))]);
      }));
  }
  function cornertable(region, caption, valueOf, best) {
    var heads = ['corner', 'boundaries meeting there', 'in the region?'];
    if (valueOf) heads.push('objective');
    return table(caption, heads, region.corners.map(function (p, i) {
      var cells = [tdl(pointtext([p.x, p.y])),
                   tdl(p.from.map(function (pair) { return 'C' + (pair[0] + 1) + ' with C' + (pair[1] + 1); }).join(', ')),
                   td(p.inRegion ? chip('yes', 'ok') : chip('on a strict edge', 'no'))];
      if (valueOf) cells.push(td(Rtext(valueOf(p)) + (best && best.indexOf(i) >= 0 ? ' ' + chip('best', 'ok') : '')));
      return tr(cells, best && best.indexOf(i) >= 0 ? 'focus' : '');
    }));
  }

  /* ============================================ mode: inequalities ======= */
  function paintIneq(rows) {
    var region = buildregion(rows);
    var blocks = [constable(region)];
    blocks.push(table('Is the region empty? Decided by eliminating y, not by looking',
      ['question', 'answer'], [
        tr([rowhead('any point at all?'), tdl(region.feas.feasible
          ? 'yes &mdash; Fourier-Motzkin eliminated y and left a range of x that is not empty'
          : 'no &mdash; ' + region.feas.why)]),
        tr([rowhead('range of x'), tdl(!region.feas.feasible ? 'there is none'
          : ((region.feas.lo === null ? 'unbounded below' : (region.feas.loStrict ? 'x &gt; ' : 'x &gt;= ') + Rtext(region.feas.lo))
            + '   and   '
            + (region.feas.hi === null ? 'unbounded above' : (region.feas.hiStrict ? 'x &lt; ' : 'x &lt;= ') + Rtext(region.feas.hi))))]),
        tr([rowhead('bounded?'), tdl(!region.feas.feasible ? 'the question does not arise'
          : (region.unbounded
             ? 'no &mdash; there is a direction you can travel forever without leaving the region'
             : 'yes &mdash; every direction eventually leaves the region'))]),
      ]));
    blocks.push(cornertable(region, 'Where the boundary lines meet, and which of those points the region actually contains'));
    work.innerHTML = blocks.join('');
    drawregion(region, rows);

    var inside = region.corners.filter(function (p) { return p.inRegion; }).length;
    /* Two different counts, and a strict inequality separates them: the table
       lists every point where two boundaries cross, and only some of those are
       points the region contains. Printing one number would make the KPI
       disagree with the sentence below it, so it prints both when they differ. */
    setkpi('constraints', String(region.cons.length),
           'corners', inside === region.corners.length ? String(inside)
             : inside + ' of ' + region.corners.length,
           'region', !region.feas.feasible ? 'empty' : (region.unbounded ? 'unbounded' : 'bounded'));

    if (!region.feas.feasible) {
      status.innerHTML = '<strong>The region is empty: no point satisfies all of them.</strong> '
        + region.feas.why.charAt(0).toUpperCase() + region.feas.why.slice(1) + '. That verdict is a '
        + 'proof rather than a search &mdash; eliminating y between the inequalities produced a '
        + 'statement about x alone that cannot hold, so no y could have rescued any x. A shading '
        + 'grid could only ever have reported that it found nothing, which is a weaker claim.';
    } else if (region.unbounded) {
      status.innerHTML = '<strong>The region is not empty, and it is unbounded.</strong> There are '
        + region.corners.length + ' corner ' + plural(region.corners.length, 'point', 'points')
        + ' where boundary lines cross, ' + inside + ' of them actually in the region, but the '
        + 'shading runs off the edge of the window and keeps going. Unbounded regions are perfectly '
        + 'ordinary; what they cost you is the guarantee that a maximum exists, which is exactly the '
        + 'issue the linear programming mode runs into.';
    } else {
      status.innerHTML = '<strong>A bounded region with ' + inside + ' corner '
        + plural(inside, 'point', 'points') + ' in it.</strong> '
        + (inside < region.corners.length
           ? 'The table above lists ' + region.corners.length + ', because that is how many places '
             + 'two boundary lines cross; ' + (region.corners.length - inside) + ' of them sit on a '
             + 'strictly written boundary and so are drawn but not owned. '
           : '')
        + 'A dashed boundary is one the reader '
        + 'wrote strictly, and a hollow circle is a corner the picture draws and the region does not '
        + 'contain &mdash; at pixel resolution nothing else could show you that. Every corner above '
        + 'is an exact pair of fractions, found by solving the two boundary equations that meet '
        + 'there and then testing the result against every constraint.';
    }
  }

  /* ================================================= mode: linprog ======= */
  function readObjective() {
    var text = String(objIn.value || '').trim();
    if (!text) return { bad: 'the objective box is empty, so there is nothing to optimise' };
    if (relsplit(text)) {
      return { bad: 'the objective is an expression such as 3x + 2y, not an equation &mdash; take out the relation sign' };
    }
    var node;
    try { node = Eparse(text); } catch (err) { return { bad: 'the objective does not parse: ' + err.message }; }
    var f = Lof(node, VARS);
    if (f.bad) return { bad: 'in the objective, ' + f.bad };
    return { f: f.f, text: text };
  }
  function paintLp(rows) {
    var obj = readObjective();
    var region = buildregion(rows);
    var sense = String((senseIn && senseIn.value) || 'max');
    if (obj.bad) {
      work.innerHTML = constable(region)
        + steps('The objective', [['what went wrong', obj.bad]]);
      setkpi('objective', 'unreadable',
             'corners in region',
             String(region.corners.filter(function (p) { return p.inRegion; }).length),
             'optimum', '--');
      status.innerHTML = '<strong>' + obj.bad.charAt(0).toUpperCase() + obj.bad.slice(1) + '.</strong> '
        + 'The constraints above were read without trouble, so the region is still there; it is only '
        + 'the thing being ' + (sense === 'max' ? 'maximised' : 'minimised') + ' that is missing. '
        + 'Type something linear in ' + varlist(VARS)
        + ', such as <code>3x + 2y</code>.';
      return;
    }
    function valueOf(p) {
      return Radd(Radd(Rmul(obj.f.c[0], p.x), Rmul(obj.f.c[1], p.y)), obj.f.k);
    }
    var usable = [];
    region.corners.forEach(function (p, i) { if (p.inRegion) usable.push(i); });
    var best = [], bestVal = null;
    usable.forEach(function (i) {
      var v = valueOf(region.corners[i]);
      if (bestVal === null) { bestVal = v; best = [i]; return; }
      var cmp = Rcmp(v, bestVal);
      if ((sense === 'max' && cmp > 0) || (sense === 'min' && cmp < 0)) { bestVal = v; best = [i]; }
      else if (cmp === 0) best.push(i);
    });
    var runaway = region.feas.feasible && (sense === 'max'
      ? Cgrows(region.cons, obj.f.c[0], obj.f.c[1])
      : Cgrows(region.cons, Rneg(obj.f.c[0]), Rneg(obj.f.c[1])));

    var blocks = [constable(region)];
    blocks.push(steps('The objective, as read', [
      ['as typed', esc(obj.text)],
      ['as coefficients', Ltext(obj.f.c, VARS) + (Rzero(obj.f.k) ? '' : ' + ' + Rtext(obj.f.k))],
      ['direction', sense === 'max' ? 'maximise' : 'minimise'],
      ['does it run away?', !region.feas.feasible ? 'there is no region to run away on'
        : (runaway ? 'YES &mdash; there is a direction inside the region along which it '
            + (sense === 'max' ? 'increases' : 'decreases') + ' forever, '
            + 'so no corner can be the answer'
          : 'no &mdash; every direction the region allows either lowers it or leaves it alone, so an '
            + 'optimum exists and a corner attains it')],
    ]));
    /* When the objective runs away there is no winner, and marking the largest
       corner "best" would be the exact mistake the preset exists to catch. */
    var crown = runaway ? [] : best;
    blocks.push(cornertable(region, 'The objective evaluated at every corner', valueOf, crown));
    work.innerHTML = blocks.join('');

    drawregion(region, rows, function (plot, win) {
      crown.forEach(function (i) {
        var p = region.corners[i];
        plot.point(Rnum(p.x), Rnum(p.y), 'plot-point root', Rtext(valueOf(p)));
      });
      /* The level line of the objective through the winning corner: every point
         on it scores the same, which is why a tie is a tie along an edge. */
      if (crown.length) {
        var v = bestVal;
        drawline(plot, lineinfo({ c: [obj.f.c[0], obj.f.c[1]], b: Rsub(v, obj.f.k) }), 'plot-aux', win);
      }
    });

    setkpi('direction', sense === 'max' ? 'maximise' : 'minimise',
           'corners in region', String(usable.length),
           'optimum', (!region.feas.feasible || runaway || bestVal === null) ? '--' : Rtext(bestVal));

    if (!region.feas.feasible) {
      status.innerHTML = '<strong>Infeasible: there is no region, so there is nothing to optimise.</strong> '
        + region.feas.why.charAt(0).toUpperCase() + region.feas.why.slice(1) + '. A linear programme '
        + 'with no feasible point has no answer at all &mdash; not a bad answer, no answer &mdash; and '
        + 'reporting "0 at the origin" here would be worse than reporting nothing.';
    } else if (runaway) {
      status.innerHTML = '<strong>Unbounded: the objective has nowhere to stop.</strong> The region '
        + 'runs off to infinity in a direction along which ' + esc(obj.text) + ' keeps '
        + (sense === 'max' ? 'increasing' : 'decreasing') + ', so however good a corner looks there '
        + 'is a feasible point better than it. The corner values above are all real numbers and the '
        + (sense === 'max' ? 'largest' : 'smallest') + ' of them is still not the answer &mdash; '
        + 'which is why no corner is marked best above. Evaluating the corners is the right method '
        + 'only once something guarantees an optimum exists, and on an unbounded region nothing does.';
    } else if (!best.length) {
      status.innerHTML = '<strong>The region is not empty, but no corner of it lies inside it.</strong> '
        + 'Either the boundary lines never meet, or every meeting point is excluded by a strict '
        + 'inequality. The corner method has nothing to evaluate; the optimum is approached along an '
        + 'edge without ever being reached, which is what a strict inequality costs you.';
    } else if (best.length > 1) {
      /* Two tied corners are the ends of one optimal edge. More than two means
         the objective is constant on the whole region (a zero linear part), and
         calling that "an edge" would be a picture the reader cannot find. */
      var tied = best.map(function (i) { return pointtext([region.corners[i].x, region.corners[i].y]); });
      status.innerHTML = '<strong>A tie: ' + best.length + ' corners score ' + Rtext(bestVal)
        + '.</strong> ' + (best.length === 2
          ? tied.join(' and ') + ' are joined by an edge, and the dashed line through them is the '
            + 'set of points scoring ' + Rtext(bestVal) + ' &mdash; it lies exactly along that edge '
            + 'because the objective is parallel to it. Every point on that edge is optimal, so '
            + '"the corner that wins" is the wrong shape of question here.'
          : tied.join(', ') + ' all score the same because the objective has no ' + varlist(VARS)
            + ' in it left to vary &mdash; it is the constant ' + Rtext(bestVal) + ' at every point '
            + 'of the region, corner or not. Every feasible point is optimal, which is a degenerate '
            + 'linear programme rather than a hard one.');
    } else {
      var p = region.corners[best[0]];
      status.innerHTML = '<strong>' + (sense === 'max' ? 'Maximum' : 'Minimum') + ' ' + Rtext(bestVal)
        + ', at the corner ' + pointtext([p.x, p.y]) + '.</strong> The objective was evaluated at '
        + 'every corner in the table above and this one won; the dashed line through it is the set of '
        + 'points scoring ' + Rtext(bestVal) + ', and the whole region sits on one side of it, which '
        + 'is the picture of why no feasible point does better. Rounded, that optimum is '
        + approx(bestVal, 4) + ' &mdash; a rounding, printed once, of the exact value ' + Rtext(bestVal) + '.';
    }
  }

  /* ---------------------------------------------------------- the driver */
  function redraw() {
    var read = readLines();
    subOut.textContent = 'unknowns: ' + VARS.join(', ');
    titleOut.textContent = read.rows.length
      ? read.rows.map(function (r) { return r.src; }).join('     ')
      : 'nothing to solve yet';

    if (read.bad.length) {
      var wants = (MODE === 'inequalities' || MODE === 'linprog')
        ? 'an inequality sign. <code>x + 2y &lt;= 8</code>, <code>y &gt; x</code> and '
          + '<code>x/2 - y &gt;= 1</code> are all fine'
        : 'an equals sign. <code>2x + 3y = 12</code>, <code>y = 2x - 1</code> and '
          + '<code>x/2 + y/3 = 1</code> are all fine';
      fail('<strong>Box ' + read.bad[0].line + ' cannot be read: ' + read.bad[0].why + '.</strong> '
        + 'Every line has to be linear in ' + varlist(VARS) + ' and has to contain ' + wants
        + '; brackets and implicit multiplication are understood. Nothing below is drawn '
        + 'from a half-read system, because a system with one line missing is a different system.', read);
      return;
    }
    if (MODE === 'inequalities' || MODE === 'linprog') {
      if (!read.rows.length) {
        fail('<strong>There are no constraints to work with.</strong> Every box is empty, and an '
          + 'empty list of inequalities describes the whole plane &mdash; which has no corners, no '
          + 'boundary and nothing to optimise over. Type at least one, such as '
          + '<code>x + 2y &lt;= 8</code>, or pick a worked example.', read);
        return;
      }
      if (MODE === 'inequalities') paintIneq(read.rows); else paintLp(read.rows);
      return;
    }
    if (read.empty.length) {
      fail('<strong>Box ' + read.empty[0] + ' is empty.</strong> This mode needs all ' + NLINES
        + ' equations: with one of them missing the system is a different system, usually with '
        + 'infinitely many solutions instead of one, and printing that as though it were the answer '
        + 'to what you typed would be a lie about the arithmetic rather than about the typing.', read);
      return;
    }
    var notEq = null;
    read.rows.forEach(function (row) { if (row.rel !== 'eq' && notEq === null) notEq = row; });
    if (notEq) {
      fail('<strong>Box ' + notEq.line + ' is an inequality, and this mode solves equations.</strong> '
        + '"' + esc(notEq.src) + '" describes a half-plane rather than a line, and neither substitution '
        + 'nor elimination nor rank has anything to say about it. The inequalities and linear '
        + 'programming modes of this lab are the ones built for it.', read);
      return;
    }
    if (MODE === 'graph') paintGraph(read.rows);
    else if (MODE === 'substitution') paintSubst(read.rows);
    else if (MODE === 'elimination') paintElim(read.rows);
    else paintThree(read.rows);
  }

  function applyPreset() {
    var p = PRESETS[Math.max(0, Math.min(PRESETS.length - 1, parseInt(preset.value, 10) || 0))];
    if (!p) return;
    for (var i = 0; i < eqIn.length; i += 1) eqIn[i].value = (p.eq && p.eq[i]) || '';
    if (objIn) objIn.value = p.obj || '';
    if (senseIn && p.sense) senseIn.value = p.sense;
    if (pickIn && p.pick) pickIn.value = p.pick;
  }
  preset.addEventListener('change', function () { applyPreset(); redraw(); });
  eqIn.forEach(function (el) { el.addEventListener('input', redraw); });
  if (objIn) objIn.addEventListener('input', redraw);
  if (senseIn) senseIn.addEventListener('change', redraw);
  if (pickIn) pickIn.addEventListener('change', redraw);
  applyPreset();
  redraw();
  window.redrawLab = redraw;
"""


def system_lab(cfg):
    """Systems of linear equations, six ways, over one exact arithmetic.

    The teaching decision: the classification -- one solution, none, infinitely
    many -- is computed from the rank of A against the rank of [A | b] by the
    same row reduction the reader is being shown, and every mode prints it
    beside its own trace. So substitution's "0 = 5" and elimination's "both
    unknowns cancelled" and the graph's parallel lines are not three
    special-cased messages; they are three views of one arithmetic fact, and
    the reader can watch them agree on a system they chose.

    The other decision is that the reader types equations rather than filling
    coefficient boxes. That means the lab must be able to REFUSE -- "xy + x = 4"
    is not linear -- and it means the fractions in "x/2 + y/3 = 1" arrive as
    fractions and stay that way to the answer.
    """
    mode = cfg.get("mode", "graph")
    if mode not in SYS_PRESETS:
        mode = "graph"
    presets = cfg.get("presets") or SYS_PRESETS[mode]
    title, subtitle = SYS_TITLES[mode]
    varnames = SYS_VARS.get(mode, ["x", "y"])
    nlines = SYS_LINES[mode]
    has_plot = mode in SYS_PLOT
    has_pick = mode in SYS_PICK
    has_obj = mode == "linprog"

    labels = [p.get("label", "example %d" % (i + 1)) for i, p in enumerate(presets)]

    boxlabel = "Constraint" if mode in ("inequalities", "linprog") else "Equation"
    eq_fields = "".join(
        '        <div class="field" id="syField%d">\n'
        '          <label for="syEq%d">%s %d</label>\n'
        '          <input id="syEq%d" type="text" value="" inputmode="text" autocomplete="off">\n'
        "        </div>\n" % (i, i, boxlabel, i, i)
        for i in range(1, nlines + 1)
    )

    pick_field = ""
    if mode == "substitution":
        opts = "".join(
            '<option value="%d,%d">solve equation %d for %s</option>' % (line, v, line + 1, varnames[v])
            for line in range(2) for v in range(2)
        )
        pick_field = (
            '        <div class="field" id="syFieldPick">\n'
            '          <label for="syPick">Which unknown to isolate</label>\n'
            '          <select id="syPick">' + opts + "</select>\n"
            "        </div>\n"
        )
    elif mode == "elimination":
        opts = "".join(
            '<option value="%d">eliminate %s first</option>' % (v, varnames[v]) for v in range(2)
        )
        pick_field = (
            '        <div class="field" id="syFieldPick">\n'
            '          <label for="syPick">Which unknown to eliminate</label>\n'
            '          <select id="syPick">' + opts + "</select>\n"
            "        </div>\n"
        )

    obj_field = ""
    if has_obj:
        obj_field = (
            '        <div class="field" id="syFieldObj">\n'
            '          <label for="syObj">Objective to optimise</label>\n'
            '          <input id="syObj" type="text" value="" inputmode="text" autocomplete="off">\n'
            "        </div>\n"
            '        <div class="field" id="syFieldSense">\n'
            '          <label for="sySense">Direction</label>\n'
            '          <select id="sySense"><option value="max">maximise</option>'
            '<option value="min">minimise</option></select>\n'
            "        </div>\n"
        )

    stage = ('      <div class="lab-stage" id="syStage"><svg id="syPlot"></svg></div>\n'
             if has_plot else "")
    legend = SYS_LEGENDS.get(mode, SYS_LEGEND_DEFAULT)

    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong id="syTitle">System</strong><span id="sySub"></span></div>\n'
        '        <div class="inline-legend">' + legend + "</div>\n"
        "      </div>\n"
        + stage
        + '      <div id="syWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="syStatus" style="margin-top:12px;"></div>'
    )

    hint = {
        "inequalities": "Type inequalities in x and y: <code>x + 2y &lt;= 8</code>, "
                        "<code>y &gt; x</code>, <code>x/2 - y &gt;= 1</code>. Leave a box empty to "
                        "drop that constraint. Every corner below is an exact pair of fractions.",
        "linprog": "The four boxes are the constraints and the fifth is what you are optimising. "
                   "Every corner of the region is found exactly and the objective is evaluated at "
                   "each of them, so the winner is read off a table rather than guessed from the picture.",
    }.get(
        mode,
        "Type equations the way you would write them: <code>2x + 3y = 12</code>, "
        "<code>y = 2x - 1</code>, <code>x/2 + y/3 = 1</code>. Brackets and implicit "
        "multiplication are understood, and every coefficient becomes an exact fraction.",
    )

    controls = (
        '        <div class="field" id="syFieldPreset">\n'
        '          <label for="syPreset">Worked example</label>\n'
        '          <select id="syPreset">' + _options(labels) + "</select>\n"
        "        </div>\n"
        + eq_fields + obj_field + pick_field
        + _kpi("sy")
        + '        <p class="small-copy" id="syHint" style="margin:0;">' + hint + "</p>"
    )

    script = (
        RATIONAL_JS + POLY_JS + EXPR_JS + PLOT_JS + FORMAT_JS + LINEAR_JS + MATRIX_JS + FEAS_JS
        + cfg_literal("PRESETS", presets)
        + SYS_SCRIPT
        .replace("__MODE__", mode)
        .replace("__VARS__", "['" + "', '".join(varnames) + "']")
        .replace("__NLINES__", str(nlines))
        .replace("__HASPLOT__", "true" if has_plot else "false")
        .replace("__HASPICK__", "true" if has_pick else "false")
        .replace("__HASOBJ__", "true" if has_obj else "false")
    )

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a worked example, or type your own system"),
        panel_intro=cfg.get(
            "panel_intro",
            "Everything below is recomputed from what is in these boxes. The number of solutions "
            "comes from comparing two ranks, never from the shape of the equations, which is why "
            "the parallel and the repeated presets behave correctly rather than being handled.",
        ),
        script=script,
    )


# ==========================================================================
# Lab 2: matrices.
# ==========================================================================

# A matrix is typed as rows separated by semicolons. Every list below ends with
# a singular matrix, because "no inverse" and "determinant 0" and "a zero row
# appeared" are three descriptions of one event and a reader should meet them
# together rather than as three separate warnings.
MAT_PRESETS = {
    "rows": [
        {"label": "a 3 by 3 with determinant -1", "a": "2 1 -1; -3 -1 2; -2 1 2",
         "i": "1", "j": "2", "k": "3"},
        {"label": "swapping two rows flips the sign", "a": "1 2; 3 4",
         "i": "1", "j": "2", "k": "2"},
        {"label": "scaling by 0 throws information away for good", "a": "1 2 3; 4 5 6; 7 8 10",
         "i": "2", "j": "3", "k": "0"},
        {"label": "a fractional multiplier", "a": "2 4; 1 3", "i": "1", "j": "2", "k": "1/2"},
        {"label": "singular, and no row operation can rescue it", "a": "1 2 3; 2 4 6; 1 0 1",
         "i": "1", "j": "2", "k": "-2"},
        {"label": "rectangular: row operations never needed squareness", "a": "1 2 3 4; 5 6 7 8",
         "i": "1", "j": "2", "k": "-5"},
    ],
    "rref": [
        {"label": "an augmented 3 by 4: one solution", "a": "1 1 1 6; 2 -1 1 3; 1 2 -1 2"},
        {"label": "rank 2: a whole row reduces to zeros", "a": "1 2 3; 2 4 6; 1 1 1"},
        {"label": "inconsistent: the last row becomes 0 0 0 | 1", "a": "1 1 1 2; 2 3 1 5; 3 4 2 8"},
        {"label": "the first pivot is 0, so the first move is a swap", "a": "0 1 2; 1 3 4; 2 1 0"},
        {"label": "already reduced: no operations at all", "a": "1 0 0; 0 1 0; 0 0 1"},
        {"label": "fractions in, fractions out", "a": "1/2 1/3; 1/4 1/5"},
    ],
    "arith": [
        {"label": "AB and BA are both defined and different", "a": "1 2; 3 4", "b": "0 1; 1 0", "op": "mul"},
        {"label": "adding needs the same shape, and these do not have it",
         "a": "1 2; 3 4", "b": "1 2 3; 4 5 6", "op": "add"},
        {"label": "a 2 by 3 times a 3 by 2", "a": "1 2 3; 4 5 6", "b": "7 8; 9 10; 11 12", "op": "mul"},
        {"label": "multiplying by the identity changes nothing", "a": "2 -1; 3 5", "b": "1 0; 0 1", "op": "mul"},
        {"label": "two matrices that are not zero whose product is",
         "a": "1 1; 1 1", "b": "1 -1; -1 1", "op": "mul"},
        {"label": "scaling by 1/2", "a": "2 4; 6 8", "b": "1 0; 0 1", "op": "scale", "k": "1/2"},
    ],
    "det": [
        {"label": "a 3 by 3, and Cramer solves it", "a": "2 1 -1; -3 -1 2; -2 1 2", "vec": "8 -11 -3"},
        {"label": "a 2 by 2", "a": "3 8; 4 6", "vec": "1 2"},
        {"label": "singular: det is 0 and Cramer cannot divide", "a": "1 2 3; 2 4 6; 1 0 1", "vec": "1 2 3"},
        {"label": "triangular: the determinant is the diagonal product", "a": "2 5 7; 0 3 1; 0 0 4", "vec": "1 1 1"},
        {"label": "fractional entries, determinant 1/60", "a": "1/2 1/3; 1/4 1/5", "vec": "1 1"},
        {"label": "a 4 by 4, where the expansion recurses twice",
         "a": "1 0 2 -1; 3 0 0 5; 2 1 4 -3; 1 0 5 0", "vec": "1 2 3 4"},
    ],
    "inverse": [
        {"label": "a 2 by 2 whose inverse is whole", "a": "2 1; 1 1"},
        {"label": "a 3 by 3", "a": "2 1 -1; -3 -1 2; -2 1 2"},
        {"label": "singular: a zero row appears and stops everything", "a": "1 2; 2 4"},
        {"label": "whole entries, fractional inverse", "a": "1 2; 3 4"},
        {"label": "diagonal: each entry inverts on its own", "a": "2 0 0; 0 -3 0; 0 0 1/2"},
        {"label": "singular 3 by 3: the rows are not independent", "a": "1 2 3; 4 5 6; 7 8 9"},
    ],
}

MAT_TITLES = {
    "rows": ("The three elementary row operations",
             "Swap, scale, add a multiple -- each applied on its own, with its effect on the determinant"),
    "rref": ("Gauss-Jordan, every operation printed",
             "The reduced row echelon form, and the rank two independent algorithms agree on"),
    "arith": ("Matrix arithmetic",
              "Sum, difference, scalar multiple and product, with every entry derived"),
    "det": ("The determinant, two ways, and Cramer's rule",
            "Cofactor expansion beside row reduction, and the solution beside the one rref found"),
    "inverse": ("The inverse by row reduction",
                "Reduce [A | I], then multiply A by what came out and watch I come back"),
}

MAT_OPS = [("add", "A + B"), ("sub", "A - B"), ("mul", "A x B"), ("mulr", "B x A"), ("scale", "k A")]
MAT_HASB = ("arith",)
MAT_HASVEC = ("det",)
MAT_HASROWSEL = ("rows",)
MAT_HASK = ("rows", "arith")


MAT_SCRIPT = r"""
  var MODE = '__MODE__';
  var HASB = __HASB__, HASVEC = __HASVEC__, HASROWSEL = __HASROWSEL__, HASK = __HASK__;

  var preset = document.getElementById('maPreset');
  var inA = document.getElementById('maA');
  var inB = HASB ? document.getElementById('maB') : null;
  var inVec = HASVEC ? document.getElementById('maVec') : null;
  var inK = HASK ? document.getElementById('maScalar') : null;
  var opIn = HASB ? document.getElementById('maOp') : null;
  var rowI = HASROWSEL ? document.getElementById('maRowI') : null;
  var rowJ = HASROWSEL ? document.getElementById('maRowJ') : null;
  var work = document.getElementById('maWork');
  var status = document.getElementById('maStatus');
  var titleOut = document.getElementById('maTitle'), subOut = document.getElementById('maSub');
  var k1 = document.getElementById('maK1'), k2 = document.getElementById('maK2'), k3 = document.getElementById('maK3');
  var k1L = document.getElementById('maK1Lab'), k2L = document.getElementById('maK2Lab'), k3L = document.getElementById('maK3Lab');

  function setkpi(a, av, b, bv, c, cv) {
    k1L.textContent = a; k1.textContent = av;
    k2L.textContent = b; k2.textContent = bv;
    k3L.textContent = c; k3.textContent = cv;
  }
  function colheads(n) {
    var out = [];
    for (var i = 0; i < n; i += 1) out.push('c' + (i + 1));
    return out;
  }
  function inlinematrix(M) {
    return M.map(function (r) {
      return '[' + r.map(function (v) { return Rtext(v); }).join('  ') + ']';
    }).join(' ');
  }
  function fail(html, extra) {
    work.innerHTML = extra || '';
    status.innerHTML = html;
    setkpi('status', 'stuck', 'reason', 'see below', 'fix', 'the box named above');
  }

  /* ================================================== mode: rows ========= */
  function paintRows(A) {
    var n = A.length, square = Msquare(A);
    var i = Math.max(0, Math.min(n - 1, parseInt(String(rowI.value), 10) - 1 || 0));
    var j = Math.max(0, Math.min(n - 1, parseInt(String(rowJ.value), 10) - 1 || 0));
    var kv = Rread(inK.value);
    var clamped = (parseInt(String(rowI.value), 10) > n) || (parseInt(String(rowJ.value), 10) > n);
    if (kv === null) {
      fail('<strong>The multiplier "' + esc(inK.value) + '" is not a number I can use.</strong> '
        + 'Row operations multiply by an exact rational, so type a whole number or a fraction such '
        + 'as <code>-2</code> or <code>1/2</code>. A decimal works too and is converted to a '
        + 'fraction: 0.25 becomes 1/4, and stays 1/4 however many operations follow.',
        Mtable('The matrix, which was read without trouble', A, { heads: colheads(Mcols(A)) }));
      return;
    }
    var heads = colheads(Mcols(A));
    var detA = square ? Mdet(A) : null;
    var blocks = [Mtable('A, as typed', A, { heads: heads })];

    /* Each of the three, applied to A ITSELF rather than to the running result,
       so the reader can see what one operation does without unpicking two. */
    var swapped = Mswap(A, i, j);
    var scaled = Mscalerow(A, i, kv);
    var added = Maddrow(A, i, j, kv);
    blocks.push(Mtable('1.  swap: R' + (i + 1) + ' &lt;-&gt; R' + (j + 1), swapped,
      { heads: heads, focus: i }));
    blocks.push(Mtable('2.  scale: R' + (i + 1) + ' &rarr; ' + Rterm(kv) + 'R' + (i + 1), scaled,
      { heads: heads, focus: i }));
    blocks.push(Mtable('3.  add a multiple: R' + (i + 1) + ' &rarr; R' + (i + 1) + ' + '
      + Rterm(kv) + 'R' + (j + 1), added, { heads: heads, focus: i }));

    /* The determinant recomputed from scratch after each one -- never adjusted
       by the rule the table is about to state, or the table would be checking
       itself against itself. */
    if (square) {
      var rows = [
        tr([rowhead('A'), td(Rtext(detA)), td('&mdash;'),
            tdl('the determinant of the matrix as typed')]),
        tr([rowhead('after the swap'), td(Rtext(Mdet(swapped))),
            td(i === j ? '1' : '-1'),
            tdl(i === j ? 'swapping a row with itself does nothing at all'
                        : 'a swap always multiplies the determinant by -1')]),
        tr([rowhead('after the scaling'), td(Rtext(Mdet(scaled))), td(Rtext(kv)),
            tdl(Rzero(kv) ? 'scaling by 0 makes the determinant 0, and there is no operation that '
                            + 'undoes it: the row is gone'
                          : 'scaling one row by k multiplies the determinant by k')]),
        tr([rowhead('after the addition'), td(Rtext(Mdet(added))), td(i === j ? Rtext(Radd(R1, kv)) : '1'),
            tdl(i === j ? 'adding a multiple of a row to ITSELF is really a scaling by 1 + k, so the '
                          + 'determinant does change'
                        : 'adding a multiple of ANOTHER row leaves the determinant untouched, which '
                          + 'is why elimination can use it freely')]),
      ];
      blocks.push(table('What each one did to the determinant, recomputed from the entries each time',
        ['', 'determinant', 'factor', 'the rule'], rows));
    } else {
      blocks.push(steps('The determinant', [['not defined here',
        'A is ' + Mshape(A) + ', and only a square matrix has a determinant. The row operations '
          + 'above are still perfectly legal &mdash; they never needed squareness.']]));
    }

    /* And the three composed, which is what elimination actually does. */
    var run = Mswap(A, i, j);
    var seq = [{ op: 'R' + (i + 1) + ' &lt;-&gt; R' + (j + 1),
                 why: i === j ? 'a swap of a row with itself, which changes nothing'
                              : 'the swap, applied to A as typed',
                 after: Mcopy(run) }];
    run = Mscalerow(run, i, kv);
    seq.push({ op: 'R' + (i + 1) + ' &rarr; ' + Rterm(kv) + 'R' + (i + 1),
               why: 'the scaling, applied to what the swap left',
               after: Mcopy(run) });
    run = Maddrow(run, i, j, kv);
    seq.push({ op: 'R' + (i + 1) + ' &rarr; R' + (i + 1) + ' + ' + Rterm(kv) + 'R' + (j + 1),
               why: 'the addition, applied to what the scaling left',
               after: Mcopy(run) });
    blocks.push(Mtrace('All three in order, each acting on the result of the last', A, seq, { heads: heads }));
    work.innerHTML = blocks.join('');

    setkpi('shape', Mshape(A), 'det A', square ? Rtext(detA) : 'not square',
           'multiplier', Rtext(kv));

    var msg = '<strong>Three operations, three effects on the determinant.</strong> ';
    if (square) {
      /* Two of the three rules only hold when i and j are DIFFERENT rows, and
         the table above already computes what actually happened. This sentence
         has to be read off the same condition, or the page would state a rule
         while showing it being broken one line higher. */
      msg += (i === j
        ? 'Not the three you were promised, though: rows i and j are the same row here, so the '
          + '"swap" swapped R' + (i + 1) + ' with itself and left the determinant exactly as it was, '
          + 'and the third operation added a multiple of a row to ITSELF, which is a scaling by '
          + '1 + k and multiplied the determinant by ' + Rtext(Radd(R1, kv)) + '. Only the middle '
          + 'one behaved as advertised, multiplying by ' + Rtext(kv) + '. '
        : 'The swap flips the sign, the scaling multiplies by ' + Rtext(kv) + ', and adding a '
          + 'multiple of a different row changes nothing. Those three facts are what make elimination '
          + 'safe: it is built almost entirely out of the third one. ')
        + 'Every determinant in the table was '
        + 'computed from the entries of that matrix by cofactor expansion, not by applying the rule '
        + 'the row states &mdash; so the table is evidence for the rule rather than a restatement of it.';
      if (Rzero(kv)) {
        msg += ' You have the multiplier at 0, which is the one scaling that is not reversible: the '
          + 'determinant collapses to 0 and no later operation brings it back.';
      }
    } else {
      msg += 'A is ' + Mshape(A) + ', so there is no determinant to watch, but the operations '
        + 'themselves are unchanged &mdash; row reduction works on any shape, and that is exactly why '
        + 'it can solve a system with more equations than unknowns.';
    }
    if (clamped) {
      msg += ' The row numbers were clamped to the ' + n + ' rows this matrix actually has.';
    }
    if (i === j) {
      msg += ' That is the reason the rule about adding a multiple always says "of another row": '
        + 'pick two different rows in the control above and all three rules come back.';
    }
    status.innerHTML = msg;
  }

  /* ================================================== mode: rref ========= */
  function paintRref(A) {
    var heads = colheads(Mcols(A));
    var red = Mrref(A);
    var ech = Mgauss(A);
    /* Two algorithms, one number. Mgauss never normalises a pivot and never
       clears upward; Mrref does both. If they disagreed about the rank, one of
       them would be wrong, and the reader would be able to see it here. */
    var nonzero = 0;
    ech.M.forEach(function (r) {
      var z = true;
      r.forEach(function (v) { if (!Rzero(v)) z = false; });
      if (!z) nonzero += 1;
    });
    var free = [];
    for (var c = 0; c < Mcols(A); c += 1) if (red.pivots.indexOf(c) < 0) free.push('c' + (c + 1));
    var twice = Mrref(red.M);

    var blocks = [Mtrace('Gauss-Jordan on A', A, red.ops, { heads: heads })];
    blocks.push(table('What the reduced form says',
      ['quantity', 'value', 'meaning'], [
        tr([rowhead('operations used'), td(String(red.ops.length)),
            tdl('every one of them is printed above, in order')]),
        tr([rowhead('pivot columns'), tdl(red.pivots.length
              ? red.pivots.map(function (c) { return 'c' + (c + 1); }).join(', ') : 'none'),
            tdl('the columns that carry a leading 1 in the reduced form')]),
        tr([rowhead('free columns'), tdl(free.length ? free.join(', ') : 'none'),
            tdl('columns with no pivot; read as a system, these are the free unknowns')]),
        tr([rowhead('rank, by Gauss-Jordan'), td(String(red.rank)),
            tdl('the number of pivots the reduction found')]),
        tr([rowhead('rank, by forward elimination'), td(String(nonzero)),
            tdl('the number of non-zero rows a different algorithm left behind')]),
        tr([rowhead('do they agree?'), tdl(red.rank === nonzero
              ? chip('yes', 'ok') + ' two algorithms that share no code returned ' + red.rank
              : chip('no', 'no') + ' one of them is wrong, and that is a bug rather than a lesson')]),
        tr([rowhead('reducing twice'), tdl(Mequ(twice.M, red.M)
              ? chip('no change', 'ok') + ' the reduced form is already reduced, as it must be'
              : chip('changed', 'no') + ' which would mean the first reduction had not finished')]),
      ]));
    blocks.push(Mtable('For comparison: forward elimination alone, which stops halfway', ech.M,
      { heads: heads }));
    work.innerHTML = blocks.join('');

    setkpi('shape', Mshape(A), 'rank', String(red.rank), 'operations', String(red.ops.length));
    status.innerHTML = '<strong>Rank ' + red.rank + ', reached in ' + red.ops.length + ' row '
      + plural(red.ops.length, 'operation', 'operations') + '.</strong> '
      + (red.ops.length === 0
         ? 'This matrix was already in reduced row echelon form, so the trace above is empty. That is '
           + 'a real answer and not a missing one. '
         : 'Each step above shows the operation and the matrix it produced, so the trace can be '
           + 'checked by hand a line at a time. ')
      + 'The reduced form is unique &mdash; a different order of operations gets there by a different '
      + 'route and lands on the same matrix &mdash; which is what makes rank a property of A rather '
      + 'than a property of how you reduced it. Every entry is an exact fraction, which is what lets '
      + 'the two rank counts above be compared at all: in floating point a pivot of 1/2 becomes an '
      + 'entry that is nearly zero three steps later, and "nearly zero" is not a rank.';
  }

  /* ================================================== mode: arith ======== */
  function paintArith(A, B) {
    var op = String((opIn && opIn.value) || 'mul');
    var kv = Rread(inK.value);
    var heads = colheads(Mcols(A));
    var blocks = [Mtable('A  (' + Mshape(A) + ')', A, { heads: heads }),
                  Mtable('B  (' + Mshape(B) + ')', B, { heads: colheads(Mcols(B)) })];
    var result = null, why = '', label = '';

    if (op === 'add' || op === 'sub') {
      label = op === 'add' ? 'A + B' : 'A - B';
      if (!Msamesize(A, B)) {
        why = 'A is ' + Mshape(A) + ' and B is ' + Mshape(B) + '. Adding matrices adds them entry '
          + 'by entry, and there is no entry of B sitting where some entries of A are, so the sum '
          + 'is not defined. This is not a rule to memorise &mdash; there is simply nothing to add.';
      } else {
        result = op === 'add' ? Madd(A, B) : Msub(A, B);
      }
    } else if (op === 'scale') {
      label = 'k A';
      if (kv === null) {
        why = '"' + esc(inK.value) + '" is not a number I can multiply by. Try 2, -1 or 1/2.';
      } else {
        result = Mscale(A, kv);
      }
    } else {
      var L = op === 'mul' ? A : B, Rm = op === 'mul' ? B : A;
      label = op === 'mul' ? 'A x B' : 'B x A';
      if (Mcols(L) !== Mrows(Rm)) {
        why = 'the left matrix is ' + Mshape(L) + ' and the right one is ' + Mshape(Rm)
          + '. Each entry of a product is a row of the left times a column of the right, so the rows '
          + 'of the left must be exactly as long as the columns of the right are tall: '
          + Mcols(L) + ' against ' + Mrows(Rm) + '.';
      } else {
        result = Mmul(L, Rm);
        var derive = [];
        for (var i = 0; i < Mrows(L); i += 1) {
          for (var j = 0; j < Mcols(Rm); j += 1) {
            derive.push(tr([rowhead('entry (' + (i + 1) + ', ' + (j + 1) + ')'),
                            tdl('row ' + (i + 1) + ' of the left, times column ' + (j + 1) + ' of the right'),
                            tdl(Mdottext(L, Rm, i, j) + ' = ' + Rtext(result[i][j]))]));
          }
        }
        blocks.push(table('Every entry of ' + label + ', from the row and column it came from',
          ['', 'which row, which column', 'the sum'], derive));
      }
    }

    if (result) blocks.push(Mtable(label, result, { heads: colheads(Mcols(result)) }));
    else blocks.push(steps(label, [['not defined', why]]));

    /* The comparison the lesson is really about, computed whether or not the
       operation the reader picked was a product. */
    var AB = Mmul(A, B), BA = Mmul(B, A);
    var cmp;
    if (!AB && !BA) cmp = 'neither product is defined for these two shapes';
    else if (!AB) cmp = 'A x B is not defined, though B x A is &mdash; order matters before the '
      + 'arithmetic even starts';
    else if (!BA) cmp = 'B x A is not defined, though A x B is &mdash; order matters before the '
      + 'arithmetic even starts';
    else if (!Msamesize(AB, BA)) cmp = 'both are defined but they are not even the same shape: A x B '
      + 'is ' + Mshape(AB) + ' and B x A is ' + Mshape(BA);
    else cmp = Mequ(AB, BA)
      ? chip('equal here', 'ok') + ' A x B = B x A for this particular pair, which is a coincidence '
        + 'about these two matrices and not a rule'
      : chip('different', 'no') + ' A x B = ' + inlinematrix(AB) + ' and B x A = ' + inlinematrix(BA);
    blocks.push(steps('Does order matter?', [['A x B against B x A', cmp]]));
    work.innerHTML = blocks.join('');

    setkpi('A', Mshape(A), 'B', Mshape(B),
           label, result ? Mshape(result) : 'not defined');

    /* "AB = 0 does not mean one of them is 0" is worth an example, and the
       example is on the page whenever the reader has typed one. Read off the
       product actually computed rather than cross-referenced to a preset by
       position, which stops being true the moment the preset list changes. */
    var isproduct = op === 'mul' || op === 'mulr';
    var zeronote = '';
    if (isproduct && result && Mequ(result, Mzero(Mrows(result), Mcols(result)))
        && !Mequ(A, Mzero(Mrows(A), Mcols(A))) && !Mequ(B, Mzero(Mrows(B), Mcols(B)))) {
      zeronote = ' And look at what came out: ' + label + ' is the zero matrix while neither A nor '
        + 'B is zero. With numbers that cannot happen; with matrices it happens whenever the columns '
        + 'of the right one point along directions the left one flattens.';
    }

    if (!result) {
      status.innerHTML = '<strong>' + label + ' is not defined.</strong> ' + why.charAt(0).toUpperCase()
        + why.slice(1) + ' Everything else on the page is still computed, because the shapes that do '
        + 'work are the interesting part of this lesson.';
    } else if (AB && BA && Msamesize(AB, BA) && !Mequ(AB, BA)) {
      status.innerHTML = '<strong>' + label + ' = ' + inlinematrix(result) + '.</strong> '
        + 'A x B and B x A are both defined here and they are different matrices. Multiplication of '
        + 'numbers does not behave like this, and almost every mistake with matrices comes from '
        + 'assuming it does &mdash; there is no cancelling and no reordering.' + zeronote;
    } else {
      var note;
      if (AB && BA && Msamesize(AB, BA)) {
        note = 'A x B and B x A happen to be equal for this particular pair, which is a fact about '
          + 'these two matrices and not a rule &mdash; change one entry and it stops being true.';
      } else if (AB && BA) {
        note = 'A x B and B x A are both defined here and are not even the same shape, so whether '
          + 'order matters is settled before any arithmetic happens.';
      } else if (AB || BA) {
        note = 'Only one of the two products is defined at all: with these shapes, writing them the '
          + 'other way round does not give a different answer, it gives no expression.';
      } else {
        note = 'Neither product is defined for these two shapes.';
      }
      status.innerHTML = '<strong>' + label + ' = ' + inlinematrix(result) + '.</strong> '
        + (isproduct
           ? 'Every entry above was derived from the row and the column it came from, so the result '
             + 'can be checked one entry at a time rather than trusted whole. '
           : (op === 'scale'
              ? 'Every entry above is one entry of A multiplied by k, in exact fractions, so the '
                + 'result can be checked one entry at a time rather than trusted whole. '
              : 'Every entry above is one entry of A paired with the entry of B sitting in the same '
                + 'place, in exact fractions, so the result can be checked one entry at a time '
                + 'rather than trusted whole. '))
        + note + zeronote;
    }
  }

  /* ==================================================== mode: det ======== */
  function cofactorblock(A) {
    var n = A.length;
    if (n === 1) return steps('The determinant of a 1 by 1 matrix', [['it is the entry itself', Rtext(A[0][0])]]);
    if (n === 2) {
      return steps('The determinant of a 2 by 2 matrix', [['ad - bc',
        '(' + Rtext(A[0][0]) + ')(' + Rtext(A[1][1]) + ') - (' + Rtext(A[0][1]) + ')(' + Rtext(A[1][0])
          + ') = ' + Rtext(Mdet(A))]]);
    }
    var body = [], total = R0;
    for (var j = 0; j < n; j += 1) {
      var minor = Mminor(A, 0, j), md = Mdet(minor);
      var term = Rmul(j % 2 === 0 ? R1 : R(-1n), Rmul(A[0][j], md));
      total = Radd(total, term);
      body.push(tr([rowhead('column ' + (j + 1)), td(j % 2 === 0 ? '+' : '-'), td(Rtext(A[0][j])),
                    tdl(inlinematrix(minor)), td(Rtext(md)), td(Rtext(term))]));
    }
    body.push(tr([rowhead('total'), td(''), td(''), tdl('the terms added up'), td(''), td(Rtext(total))], 'focus'));
    return table('Cofactor expansion along row 1, with every minor shown',
      ['', 'sign', 'entry', 'the minor', 'its determinant', 'the term'], body);
  }
  function paintDet(A, bvec) {
    var n = A.length, heads = colheads(n);
    var detCof = Mdet(A);
    var red = Mrref(A);
    /* The second determinant: row reduction tracked the factor it multiplied
       the determinant by, and the reduced form of a non-singular matrix is I,
       whose determinant is 1. So det(A) = 1 / factor -- computed without ever
       expanding a cofactor. */
    var detRow = red.rank === n ? Rinv(red.detf) : R0;

    var blocks = [Mtable('A', A, { heads: heads }), cofactorblock(A)];
    blocks.push(steps('The same determinant by row reduction, which shares no code with the above', [
      ['the reduced form', red.rank === n ? 'the identity, so its determinant is 1'
        : 'rank ' + red.rank + ' out of ' + n + ', so a row of zeros appeared and the reduced form '
          + 'has determinant 0'],
      ['the factor the operations introduced', Rtext(red.detf)
        + ' &mdash; swaps contributed -1 each, and each pivot divided by contributed its reciprocal'],
      ['so det A is', red.rank === n ? '1 / ' + Rterm(red.detf) + ' = ' + Rtext(detRow) : '0'],
      ['do the two agree?', Requ(detCof, detRow)
        ? chip('yes', 'ok') + ' both routes give ' + Rtext(detCof)
        : chip('no', 'no') + ' cofactor says ' + Rtext(detCof) + ' and row reduction says '
          + Rtext(detRow) + ', which is a bug'],
    ]));

    var singular = Rzero(detCof);
    if (!bvec) {
      blocks.push(steps("Cramer's rule", [['no constants given',
        'type ' + n + ' numbers in the constants box &mdash; for example <code>'
          + heads.map(function () { return '1'; }).join(' ') + '</code> &mdash; and each unknown is '
          + 'computed as a ratio of two determinants.']]));
    } else if (bvec.length !== n) {
      blocks.push(steps("Cramer's rule", [['the wrong number of constants',
        'A has ' + n + ' rows and the constants box holds ' + bvec.length + ' '
          + plural(bvec.length, 'number', 'numbers') + '. There has to be one constant per equation.']]));
    } else if (singular) {
      blocks.push(steps("Cramer's rule", [['nothing to divide by',
        'every unknown in Cramer\'s rule is a determinant divided by det A, and det A is 0 here. '
          + 'That is not the method failing &mdash; a singular system has either no solution or '
          + 'infinitely many, and no single ratio could name either of those.']]));
    } else {
      var body = [], xs = [];
      for (var c = 0; c < n; c += 1) {
        var Ac = Mcopy(A);
        for (var r = 0; r < n; r += 1) Ac[r][c] = bvec[r];
        var dc = Mdet(Ac), xv = Rdiv(dc, detCof);
        xs.push(xv);
        body.push(tr([rowhead('x' + (c + 1)), tdl(inlinematrix(Ac)), td(Rtext(dc)),
                      tdl(Rtext(dc) + ' / ' + Rterm(detCof) + ' = ' + Rtext(xv))]));
      }
      blocks.push(table("Cramer's rule: replace one column with the constants, then divide",
        ['', 'A with that column replaced', 'its determinant', 'the unknown'], body));
      var aug = A.map(function (row, i) { return row.concat([bvec[i]]); });
      var solved = Mrref(aug, { cols: n });
      var rrefX = [];
      for (var v = 0; v < n; v += 1) rrefX.push(solved.M[solved.pivots.indexOf(v)][n]);
      var same = true;
      for (var q = 0; q < n; q += 1) if (!Requ(xs[q], rrefX[q])) same = false;
      blocks.push(Mtable('And the same system row-reduced, which used none of the determinants above',
        solved.M, { split: n, heads: heads.concat(['=']) }));
      blocks.push(steps('The two answers', [
        ["Cramer's rule", xs.map(function (v) { return Rtext(v); }).join(',   ')],
        ['row reduction', rrefX.map(function (v) { return Rtext(v); }).join(',   ')],
        ['agree?', same ? chip('yes', 'ok') + ' two methods, one answer'
                        : chip('no', 'no') + ' which is a bug and not a lesson'],
      ]));
    }
    work.innerHTML = blocks.join('');
    setkpi('shape', Mshape(A), 'det A', Rtext(detCof),
           'invertible', singular ? 'no' : 'yes');

    if (singular) {
      status.innerHTML = '<strong>det A = 0: this matrix is singular.</strong> Cofactor expansion '
        + 'and row reduction both say so, and they were computed separately. A zero determinant means '
        + 'the rows are not independent &mdash; row reduction found rank ' + red.rank + ' out of ' + n
        + ' &mdash; so A squashes space flat and cannot be undone. Cramer\'s rule divides by det A, '
        + 'which is why it has nothing to say here, and why "no unique solution" is the honest '
        + 'answer rather than a number.';
    } else {
      status.innerHTML = '<strong>det A = ' + Rtext(detCof) + ', by two routes that share no code.</strong> '
        + (n > 2 ? 'Cofactor expansion walked the ' + n + ' minors of row 1, recursively, and row '
           : (n === 2 ? 'Cofactor expansion took ad - bc, and row '
                      : 'The expansion had a single entry to read and no minors to recurse into, '
                        + 'and row '))
        + 'reduction never expanded anything &mdash; it multiplied together the factors its '
        + 'own operations introduced. Agreement between them is the evidence; either one alone would '
        + 'just be a number in a box. Everything is exact, so a determinant of ' + Rtext(detCof)
        + ' is that value and not a float that rounds to it.';
    }
  }

  /* ================================================= mode: inverse ====== */
  function paintInverse(A) {
    var n = A.length, heads = colheads(n);
    var I = Mid(n);
    var aug = Maug(A, I);
    var red = Mrref(aug, { cols: n });
    var left = Mtake(red.M, 0, n), right = Mtake(red.M, n, n);
    var augHeads = heads.concat(heads.map(function (h) { return 'i' + h.slice(1); }));

    var blocks = [Mtable('A', A, { heads: heads })];
    blocks.push(Mtrace('Row reducing [A | I] &mdash; the identity half is tinted', aug, red.ops,
      { split: n, heads: augHeads }));

    if (!Mequ(left, I)) {
      var zero = -1;
      for (var i = 0; i < n; i += 1) {
        var z = true;
        for (var j = 0; j < n; j += 1) if (!Rzero(left[i][j])) { z = false; break; }
        if (z) { zero = i; break; }
      }
      blocks.push(steps('There is no inverse', [
        ['the left half did not become I', 'reduction reached rank ' + red.rank + ' out of ' + n
          + ', so the left half of the reduced matrix is not the identity and never can be'],
        ['the row that gives it away', zero >= 0
          ? 'row ' + (zero + 1) + ' of the left half is entirely zeros. Whatever sits beside it in '
            + 'the right half, no matrix multiplied by A could produce a 1 there.'
          : 'the pivots ran out before every column had one'],
        ['det A, computed independently', Rtext(Mdet(A))
          + ' &mdash; cofactor expansion agrees that this matrix is singular'],
      ]));
      work.innerHTML = blocks.join('');
      setkpi('shape', Mshape(A), 'rank', String(red.rank), 'inverse', 'does not exist');
      status.innerHTML = '<strong>A is singular: it has no inverse.</strong> The row reduction did '
        + 'not fail or crash &mdash; it finished, and what it finished with was a left half that is '
        + 'not the identity, with rank ' + red.rank + ' where ' + n + ' was needed. The determinant, '
        + 'computed by cofactor expansion without looking at any of this, is ' + Rtext(Mdet(A))
        + '. Two independent routes to the same verdict. A matrix like this collapses at least one '
        + 'direction to nothing, and no matrix can un-collapse it.';
      return;
    }

    var inv = right;
    var prod1 = Mmul(A, inv), prod2 = Mmul(inv, A);
    blocks.push(Mtable('The right half is A inverse', inv, { heads: heads }));
    blocks.push(Mtable('A x A inverse, multiplied out entry by entry', prod1, { heads: heads }));
    blocks.push(Mtable('A inverse x A, which had no reason to be the same', prod2, { heads: heads }));
    blocks.push(steps('Is it really the inverse?', [
      ['A x A inverse = I ?', Mequ(prod1, I) ? chip('yes', 'ok') + ' the identity came back'
                                             : chip('no', 'no') + ' which is a bug'],
      ['A inverse x A = I ?', Mequ(prod2, I) ? chip('yes', 'ok') + ' and from the other side too'
                                             : chip('no', 'no') + ' which is a bug'],
      ['det A x det A inverse', Rtext(Mdet(A)) + ' x ' + Rtext(Mdet(inv)) + ' = '
        + Rtext(Rmul(Mdet(A), Mdet(inv))) + ', which must be 1 and is'],
    ]));
    work.innerHTML = blocks.join('');
    setkpi('shape', Mshape(A), 'det A', Rtext(Mdet(A)), 'A x A inv', Mequ(prod1, I) ? 'I' : 'not I');
    status.innerHTML = '<strong>A inverse = ' + inlinematrix(inv) + '.</strong> The row reduction '
      + 'produced it, and then it was MULTIPLIED back against A &mdash; both ways round &mdash; and '
      + 'the identity came out. That multiplication is the proof; without it the page would be '
      + 'asking you to take the reduction on trust. Notice how often the inverse has fractions in it '
      + 'when A does not: the entries of an inverse are cofactors over the determinant, and there is '
      + 'no reason for that division to come out whole. In floating point those fractions would be '
      + 'the first thing to drift, and A times A inverse would come back as an identity with 0.9999 '
      + 'on the diagonal.';
  }

  /* ---------------------------------------------------------- the driver */
  function redraw() {
    var pa = Mparse(inA.value, 'A');
    subOut.textContent = MODE === 'arith' ? 'two matrices, exact entries' : 'exact rational entries';
    if (pa.bad) {
      titleOut.textContent = 'A cannot be read';
      fail('<strong>' + pa.bad.charAt(0).toUpperCase() + pa.bad.slice(1) + '.</strong> '
        + 'Type a matrix as rows separated by semicolons and entries separated by spaces: '
        + '<code>2 1 -1; -3 -1 2; -2 1 2</code> is a 3 by 3. Entries may be whole numbers or '
        + 'fractions such as <code>-1/2</code>, and every one of them is kept exactly.');
      return;
    }
    var A = pa.M;
    titleOut.textContent = 'A is ' + Mshape(A);

    if (MODE === 'rows') { paintRows(A); return; }
    if (MODE === 'rref') { paintRref(A); return; }
    if (MODE === 'arith') {
      var pb = Mparse(inB.value, 'B');
      if (pb.bad) {
        titleOut.textContent = 'B cannot be read';
        fail('<strong>' + pb.bad.charAt(0).toUpperCase() + pb.bad.slice(1) + '.</strong> '
          + 'A was read without trouble; it is the second box that is the problem. Rows go in '
          + 'separated by semicolons, entries by spaces: <code>0 1; 1 0</code>.',
          Mtable('A, which was read without trouble', A, { heads: colheads(Mcols(A)) }));
        return;
      }
      paintArith(A, pb.M);
      return;
    }
    if (!Msquare(A)) {
      fail('<strong>A is ' + Mshape(A) + ', and this mode needs a square matrix.</strong> '
        + (MODE === 'det'
           ? 'A determinant is defined only when the matrix has as many rows as columns &mdash; the '
             + 'cofactor expansion below would have nothing to recurse into otherwise. '
           : 'Only a square matrix can have an inverse: A inverse has to work from both sides, and '
             + 'for a non-square A the two products would not even have the same shape. ')
        + 'Add or remove a column so that the shape is n by n.',
        Mtable('A, as typed', A, { heads: colheads(Mcols(A)) }));
      return;
    }
    if (MODE === 'det') {
      var bvec = null;
      var pv = Mparse(inVec.value, 'the constants');
      if (!pv.bad) {
        /* One row of numbers, or one column -- a reader writes both. */
        bvec = pv.M.length === 1 ? pv.M[0] : pv.M.map(function (r) { return r[0]; });
      }
      paintDet(A, bvec);
      if (pv.bad && String(inVec.value).trim()) {
        status.innerHTML = '<strong>The constants box: ' + pv.bad + '.</strong> The determinant '
          + 'above is unaffected &mdash; it never needed the constants. Cramer\'s rule does: type '
          + 'one number per equation, such as <code>8 -11 -3</code>.';
      }
      return;
    }
    paintInverse(A);
  }

  function applyPreset() {
    var p = PRESETS[Math.max(0, Math.min(PRESETS.length - 1, parseInt(preset.value, 10) || 0))];
    if (!p) return;
    inA.value = p.a || '';
    if (inB) inB.value = p.b || '';
    if (inVec) inVec.value = p.vec || '';
    if (inK) inK.value = p.k || '2';
    if (opIn && p.op) opIn.value = p.op;
    if (rowI) rowI.value = p.i || '1';
    if (rowJ) rowJ.value = p.j || '2';
  }
  preset.addEventListener('change', function () { applyPreset(); redraw(); });
  inA.addEventListener('input', redraw);
  if (inB) inB.addEventListener('input', redraw);
  if (inVec) inVec.addEventListener('input', redraw);
  if (inK) inK.addEventListener('input', redraw);
  if (opIn) opIn.addEventListener('change', redraw);
  if (rowI) rowI.addEventListener('change', redraw);
  if (rowJ) rowJ.addEventListener('change', redraw);
  applyPreset();
  redraw();
  window.redrawLab = redraw;
"""


def matrix_lab(cfg):
    """Matrices of exact rationals, where every answer arrives twice.

    The teaching decision: a matrix lab is one small step away from being a
    calculator that asserts, so no mode here reports a single number. The
    determinant comes from cofactor expansion AND from the factor row reduction
    accumulated; the inverse comes from reducing [A | I] AND is then multiplied
    back against A from both sides; Cramer's rule sits beside the solution row
    reduction found; the rank is reported by two different reductions. The two
    computations in each pair share no code, so when they agree the reader has
    evidence rather than a claim -- and a singular matrix makes all of them say
    the same thing at once, which is the point of putting them together.
    """
    mode = cfg.get("mode", "rref")
    if mode not in MAT_PRESETS:
        mode = "rref"
    presets = cfg.get("presets") or MAT_PRESETS[mode]
    title, subtitle = MAT_TITLES[mode]
    has_b = mode in MAT_HASB
    has_vec = mode in MAT_HASVEC
    has_rowsel = mode in MAT_HASROWSEL
    has_k = mode in MAT_HASK
    labels = [p.get("label", "example %d" % (i + 1)) for i, p in enumerate(presets)]

    rownums = "".join('<option value="%d">row %d</option>' % (i, i) for i in range(1, 7))
    extra = ""
    if has_b:
        extra += (
            '        <div class="field" id="maFieldB">\n'
            '          <label for="maB">Matrix B</label>\n'
            '          <input id="maB" type="text" value="" inputmode="text" autocomplete="off">\n'
            "        </div>\n"
            '        <div class="field" id="maFieldOp">\n'
            '          <label for="maOp">Operation</label>\n'
            '          <select id="maOp">'
            + "".join('<option value="%s">%s</option>' % (v, _esc(t)) for v, t in MAT_OPS)
            + "</select>\n        </div>\n"
        )
    if has_rowsel:
        extra += (
            '        <div class="field" id="maFieldI">\n'
            '          <label for="maRowI">Row i</label>\n'
            '          <select id="maRowI">' + rownums + "</select>\n        </div>\n"
            '        <div class="field" id="maFieldJ">\n'
            '          <label for="maRowJ">Row j</label>\n'
            '          <select id="maRowJ">' + rownums + "</select>\n        </div>\n"
        )
    if has_k:
        extra += (
            '        <div class="field" id="maFieldK">\n'
            '          <label for="maScalar">Multiplier k</label>\n'
            '          <input id="maScalar" type="text" value="" inputmode="text" autocomplete="off">\n'
            "        </div>\n"
        )
    if has_vec:
        extra += (
            '        <div class="field" id="maFieldVec">\n'
            '          <label for="maVec">Constants, one per equation</label>\n'
            '          <input id="maVec" type="text" value="" inputmode="text" autocomplete="off">\n'
            "        </div>\n"
        )

    legend = {
        "rows": '<span class="tone-cyan"><i class="legend-swatch"></i>the row acted on</span>'
                '<span class="tone-amber"><i class="legend-swatch"></i>the determinant, recomputed</span>',
        "rref": '<span class="tone-cyan"><i class="legend-swatch"></i>every operation, in order</span>'
                '<span class="tone-amber"><i class="legend-swatch"></i>rank, by two algorithms</span>',
        "arith": '<span class="tone-cyan"><i class="legend-swatch"></i>every entry derived</span>'
                 '<span class="tone-amber"><i class="legend-swatch"></i>AB against BA</span>',
        "det": '<span class="tone-cyan"><i class="legend-swatch"></i>cofactor expansion</span>'
               '<span class="tone-purple"><i class="legend-swatch"></i>row reduction</span>'
               '<span class="tone-green"><i class="legend-swatch"></i>Cramer against rref</span>',
        "inverse": '<span class="tone-cyan"><i class="legend-swatch"></i>[A | I] reduced</span>'
                   '<span class="tone-green"><i class="legend-swatch"></i>A times the result</span>',
    }[mode]

    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong id="maTitle">Matrix</strong><span id="maSub"></span></div>\n'
        '        <div class="inline-legend">' + legend + "</div>\n"
        "      </div>\n"
        '      <div id="maWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="maStatus" style="margin-top:12px;"></div>'
    )

    controls = (
        '        <div class="field" id="maFieldPreset">\n'
        '          <label for="maPreset">Worked example</label>\n'
        '          <select id="maPreset">' + _options(labels) + "</select>\n"
        "        </div>\n"
        '        <div class="field" id="maFieldA">\n'
        '          <label for="maA">Matrix A</label>\n'
        '          <input id="maA" type="text" value="" inputmode="text" autocomplete="off">\n'
        "        </div>\n"
        + extra
        + _kpi("ma")
        + '        <p class="small-copy" id="maHint" style="margin:0;">Rows are separated by '
          "<code>;</code> and entries by spaces, so <code>2 1 -1; -3 -1 2; -2 1 2</code> is a 3 by 3. "
          "Fractions such as <code>-1/2</code> are entries like any other, and stay exact through "
          "every operation below.</p>"
    )

    script = (
        RATIONAL_JS + POLY_JS + EXPR_JS + FORMAT_JS + LINEAR_JS + MATRIX_JS
        + cfg_literal("PRESETS", presets)
        + MAT_SCRIPT
        .replace("__MODE__", mode)
        .replace("__HASB__", "true" if has_b else "false")
        .replace("__HASVEC__", "true" if has_vec else "false")
        .replace("__HASROWSEL__", "true" if has_rowsel else "false")
        .replace("__HASK__", "true" if has_k else "false")
    )

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a worked example, or type your own matrix"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every answer below is computed twice, by routes that share no code, and the page says "
            "whether they agreed. One number in a box is not evidence; two methods meeting is.",
        ),
        script=script,
    )


# ==========================================================================
# Lab 3: sequences and series.
# ==========================================================================

# Every list ends with the case where the formula has nothing to say: a closed
# form that is nearly right, a ratio of exactly 1, a ratio of -1, and an
# expression that is not a binomial at all.
SEQ_PRESETS = {
    "define": [
        {"label": "arithmetic: add 3 each time", "a1": "5", "rec": "p + 3", "closed": "5 + 3(n - 1)", "n": "8"},
        {"label": "geometric: double each time", "a1": "3", "rec": "2p", "closed": "3*2^(n - 1)", "n": "8"},
        {"label": "the square numbers, built by adding the odd numbers", "a1": "1",
         "rec": "p + 2n - 1", "closed": "n^2", "n": "8"},
        {"label": "the triangular numbers", "a1": "1", "rec": "p + n", "closed": "n(n + 1)/2", "n": "8"},
        {"label": "halve and add 1: the closed form has a power in it", "a1": "1",
         "rec": "p/2 + 1", "closed": "2 - 2^(1 - n)", "n": "8"},
        {"label": "a closed form that is nearly right, and parts company at n = 1", "a1": "5",
         "rec": "p + 3", "closed": "3n", "n": "8"},
    ],
    "arithmetic": [
        {"label": "a1 = 3, d = 5", "a1": "3", "d": "5", "n": "10"},
        {"label": "a decreasing sequence, d = -4", "a1": "20", "d": "-4", "n": "10"},
        {"label": "d = 0: every term is the same, and the formulas still hold", "a1": "7", "d": "0", "n": "10"},
        {"label": "a fractional difference, d = 3/2", "a1": "1/2", "d": "3/2", "n": "10"},
        {"label": "the counting numbers, whose sum is the triangular numbers", "a1": "1", "d": "1", "n": "12"},
        {"label": "a1 and d both negative", "a1": "-2", "d": "-7", "n": "10"},
    ],
    "geometric": [
        {"label": "r = 1/2: the infinite sum converges", "a1": "1", "r": "1/2", "n": "10"},
        {"label": "r = 2: the terms run away", "a1": "1", "r": "2", "n": "10"},
        {"label": "r = -1/2: alternating, and still convergent", "a1": "1", "r": "-1/2", "n": "10"},
        {"label": "r = 1: the sum formula divides by 1 - r, which is 0", "a1": "4", "r": "1", "n": "10"},
        {"label": "r = -1: the partial sums oscillate and never settle", "a1": "3", "r": "-1", "n": "10"},
        {"label": "r = 2/3 with a fractional first term", "a1": "9/4", "r": "2/3", "n": "10"},
    ],
    "binomial": [
        {"label": "(x + 1)^5", "bin": "x + 1", "pow": "5"},
        {"label": "(2x - 3)^4", "bin": "2x - 3", "pow": "4"},
        {"label": "(x - 1/2)^3", "bin": "x - 1/2", "pow": "3"},
        {"label": "(3x + 2)^0: the empty product", "bin": "3x + 2", "pow": "0"},
        {"label": "(x^2 - 2)^6: the two terms need not be x and a number", "bin": "x^2 - 2", "pow": "6"},
        {"label": "x^2 + x + 1 has three terms, so the binomial theorem does not apply",
         "bin": "x^2 + x + 1", "pow": "4"},
    ],
}

SEQ_TITLES = {
    "define": ("Two definitions of one sequence",
               "A recursive rule and a closed form, generating the list side by side"),
    "arithmetic": ("Arithmetic sequences and their sums",
                   "The nth term and the sum, each computed twice and compared"),
    "geometric": ("Geometric sequences and their sums",
                  "Partial sums against the formula, and what happens when |r| is not below 1"),
    "binomial": ("The binomial theorem",
                 "Pascal's triangle against the C(n, k) formula, against multiplying it out"),
}

SEQ_COUNTS = ("4", "6", "8", "10", "12", "16", "20")
SEQ_POWERS = ("0", "1", "2", "3", "4", "5", "6", "8", "10", "12")


SEQ_SCRIPT = r"""
  var MODE = '__MODE__';
  var HASPLOT = __HASPLOT__;

  var preset = document.getElementById('sqPreset');
  var inA1 = (MODE === 'binomial') ? null : document.getElementById('sqA1');
  var inRec = (MODE === 'define') ? document.getElementById('sqRec') : null;
  var inClosed = (MODE === 'define') ? document.getElementById('sqClosed') : null;
  var inD = (MODE === 'arithmetic') ? document.getElementById('sqD') : null;
  var inR = (MODE === 'geometric') ? document.getElementById('sqR') : null;
  var inBin = (MODE === 'binomial') ? document.getElementById('sqBin') : null;
  var selN = (MODE === 'binomial') ? null : document.getElementById('sqN');
  var selPow = (MODE === 'binomial') ? document.getElementById('sqPow') : null;
  var svg = HASPLOT ? document.getElementById('sqPlot') : null;
  var work = document.getElementById('sqWork');
  var status = document.getElementById('sqStatus');
  var titleOut = document.getElementById('sqTitle'), subOut = document.getElementById('sqSub');
  var k1 = document.getElementById('sqK1'), k2 = document.getElementById('sqK2'), k3 = document.getElementById('sqK3');
  var k1L = document.getElementById('sqK1Lab'), k2L = document.getElementById('sqK2Lab'), k3L = document.getElementById('sqK3Lab');

  function setkpi(a, av, b, bv, c, cv) {
    k1L.textContent = a; k1.textContent = av;
    k2L.textContent = b; k2.textContent = bv;
    k3L.textContent = c; k3.textContent = cv;
  }
  function termcount() {
    var v = parseInt(String(selN ? selN.value : '10'), 10);
    return (!v || v < 1) ? 10 : Math.min(24, v);
  }
  function fail(html, extra) {
    if (svg) svg.textContent = '';
    work.innerHTML = extra || '';
    status.innerHTML = html;
    setkpi('status', 'stuck', 'reason', 'see below', 'fix', 'the box named above');
  }
  function agreechip(same) {
    return same ? chip('agree', 'ok') : chip('DISAGREE', 'no');
  }

  /* ================================================= mode: define ======== */
  function paintDefine() {
    var a1 = Rread(inA1.value);
    if (a1 === null) {
      fail('<strong>The first term "' + esc(inA1.value) + '" is not a number I can use.</strong> '
        + 'A sequence has to start somewhere exact: type a whole number or a fraction such as '
        + '<code>5</code> or <code>-1/2</code>. Everything after it is generated from that value, '
        + 'so a first term I cannot read leaves nothing to generate.');
      return;
    }
    var pr = Xparse(inRec.value), pc = Xparse(inClosed.value);
    if (pr.bad || pc.bad) {
      fail('<strong>' + (pr.bad ? 'The recursive rule: ' + pr.bad : 'The closed form: ' + pc.bad)
        + '.</strong> The recursive rule may use <code>p</code> for the previous term and '
        + '<code>n</code> for the position, as in <code>p + 3</code> or <code>p/2 + 1</code>. The '
        + 'closed form may use <code>n</code> only, as in <code>n^2</code> or '
        + '<code>3*2^(n - 1)</code>. Both are evaluated in exact fractions, never in decimals.');
      return;
    }
    var N = termcount(), rec = [null], clo = [null], firstBad = null, unroll = [];
    for (var i = 1; i <= N; i += 1) {
      var env = { n: R(BigInt(i)) };
      if (i === 1) {
        rec.push(a1);
        unroll.push(['a1', 'given as ' + Rtext(a1)]);
      } else {
        env.p = rec[i - 1];
        var got = Xeval(pr.node, env);
        if (got.bad) { firstBad = 'the recursive rule at n = ' + i + ': ' + got.bad; break; }
        rec.push(got.v);
        if (i <= 4) {
          unroll.push(['a' + i, 'the rule with p = a' + (i - 1) + ' = ' + Rtext(rec[i - 1])
            + ' and n = ' + i + ',  giving ' + Rtext(got.v)]);
        }
      }
      var cv = Xeval(pc.node, { n: R(BigInt(i)) });
      if (cv.bad) { firstBad = 'the closed form at n = ' + i + ': ' + cv.bad; break; }
      clo.push(cv.v);
    }
    if (firstBad) {
      fail('<strong>Stuck at ' + firstBad + '.</strong> The terms computed before that point are '
        + 'still correct; it is this one that has no exact value. A rule such as '
        + '<code>1/(n - 3)</code> hits exactly this at n = 3.');
      return;
    }
    var mismatch = -1;
    for (var q = 1; q <= N && q < rec.length && q < clo.length; q += 1) {
      if (!Requ(rec[q], clo[q])) { mismatch = q; break; }
    }
    var body = [];
    for (var t = 1; t < rec.length && t < clo.length; t += 1) {
      var same = Requ(rec[t], clo[t]);
      body.push(tr([rowhead('n = ' + t), td(Rtext(rec[t])), td(Rtext(clo[t])),
                    td(same ? chip('same', 'ok') : chip('different', 'no'), same ? 't' : 'f')],
                   mismatch === t ? 'focus' : ''));
    }
    work.innerHTML = steps('The recursion unrolled, one term at a time', unroll)
      + table('The two definitions, evaluated independently',
              ['', 'from the recursive rule', 'from the closed form', ''], body);

    setkpi('terms', String(N), 'first difference', mismatch < 0 ? 'none' : 'n = ' + mismatch,
           'verdict', mismatch < 0 ? 'the same sequence' : 'different sequences');

    if (mismatch < 0) {
      status.innerHTML = '<strong>The two definitions agree on all ' + N + ' terms.</strong> '
        + 'That is evidence, not proof &mdash; agreement on twenty terms is not agreement on every '
        + 'term, and the difference between those two statements is what induction exists to close. '
        + 'What it does rule out is the commonest kind of error: a closed form that is off by one, '
        + 'or right for the first few terms and wrong afterwards. Change the count to 20 and watch '
        + 'the evidence get stronger without ever becoming a proof.';
    } else {
      status.innerHTML = '<strong>They part company at n = ' + mismatch + ': the recursion gives '
        + Rtext(rec[mismatch]) + ' and the closed form gives ' + Rtext(clo[mismatch]) + '.</strong> '
        + 'These are two different sequences, however alike they look. This is exactly what a lab '
        + 'that printed only one of them would hide from you &mdash; a closed form is a claim about '
        + 'a recursion, and a claim can be false. Notice that they were computed separately: the '
        + 'closed form never saw the previous term, and the recursion never saw n except where you '
        + 'wrote it.';
    }
  }

  /* ============================================= mode: arithmetic ======== */
  function paintArith() {
    var a1 = Rread(inA1.value), d = Rread(inD.value);
    if (a1 === null || d === null) {
      fail('<strong>' + (a1 === null ? 'The first term' : 'The common difference') + ' "'
        + esc(a1 === null ? inA1.value : inD.value) + '" is not a number I can use.</strong> '
        + 'Both boxes take a whole number or a fraction &mdash; <code>3</code>, <code>-4</code>, '
        + '<code>3/2</code>. A difference of 3/2 is the case worth trying: in decimals the tenth '
        + 'term picks up a rounding error that the sum then multiplies by ten.');
      return;
    }
    var N = termcount(), terms = [null], sums = [null], run = R0;
    for (var i = 1; i <= N; i += 1) {
      terms.push(i === 1 ? a1 : Radd(terms[i - 1], d));
      run = Radd(run, terms[i]);
      sums.push(run);
    }
    var body = [];
    for (var t = 1; t <= N; t += 1) {
      /* Both columns computed here, from different definitions: the left by
         adding d to the term before it, the right by the closed formula. */
      var byFormula = Radd(a1, Rmul(R(BigInt(t - 1)), d));
      var sumPair = Rdiv(Rmul(R(BigInt(t)), Radd(a1, terms[t])), R(2n));
      var sumOther = Rdiv(Rmul(R(BigInt(t)), Radd(Rmul(R(2n), a1), Rmul(R(BigInt(t - 1)), d))), R(2n));
      var ok = Requ(byFormula, terms[t]) && Requ(sumPair, sums[t]) && Requ(sumOther, sums[t]);
      body.push(tr([rowhead('n = ' + t), td(Rtext(terms[t])), td(Rtext(byFormula)),
                    td(Rtext(sums[t])), td(Rtext(sumPair)), td(Rtext(sumOther)),
                    td(ok ? chip('all four', 'ok') : chip('MISMATCH', 'no'))]));
    }
    var an = Radd(a1, Rmul(R(BigInt(N - 1)), d));
    var sumA = sums[N];
    var sumB = Rdiv(Rmul(R(BigInt(N)), Radd(a1, an)), R(2n));
    var sumC = Rdiv(Rmul(R(BigInt(N)), Radd(Rmul(R(2n), a1), Rmul(R(BigInt(N - 1)), d))), R(2n));

    work.innerHTML =
      steps('The sequence, as defined', [
        ['first term a1', Rtext(a1)],
        ['common difference d', Rtext(d) + ' &mdash; added to get from each term to the next'],
        ['the rule', 'a(n) = a(n-1)' + plusnum(d) + ',  and the claim is that a(n) = a1 + (n-1)d'],
      ])
      + table('Every term and every partial sum, computed both ways',
        ['', 'term, by adding d', 'term, by a1 + (n-1)d', 'sum, by adding them up',
         'sum, by n(a1 + an)/2', 'sum, by n(2a1 + (n-1)d)/2', 'agree?'], body)
      + steps('At n = ' + N, [
        ['the nth term by stepping', Rtext(terms[N]) + ' &mdash; ' + (N - 1)
          + ' additions of ' + Rtext(d) + ', done one at a time'],
        ['the nth term by formula', Rtext(a1) + ' + ' + (N - 1) + '(' + Rtext(d) + ') = ' + Rtext(an)],
        ['these agree?', agreechip(Requ(terms[N], an))],
        ['the sum by adding the terms up', Rtext(sumA)],
        ['the sum by n(a1 + an)/2', N + '(' + Rtext(a1) + plusnum(an) + ')/2 = ' + Rtext(sumB)],
        ['the sum by n(2a1 + (n-1)d)/2', Rtext(sumC)],
        ['all three agree?', agreechip(Requ(sumA, sumB) && Requ(sumA, sumC))],
      ]);

    setkpi('a(' + N + ')', Rtext(an), 'sum to ' + N, Rtext(sumA),
           'checks', Requ(terms[N], an) && Requ(sumA, sumB) && Requ(sumA, sumC) ? 'all passed' : 'FAILED');

    status.innerHTML = '<strong>a(' + N + ') = ' + Rtext(an) + ' and the sum of the first ' + N
      + ' terms is ' + Rtext(sumA) + '.</strong> Each of those was computed twice: once by doing '
      + 'what the definition says &mdash; adding d again and again, adding the terms up one at a '
      + 'time &mdash; and once by the closed formula. The page prints both and says whether they '
      + 'matched, which is the only honest way to show you a formula the lesson has not proved. '
      + (Rzero(d)
         ? 'You have d = 0, so every term is ' + Rtext(a1) + ' and the sum formula reduces to n times '
           + 'a1. The formulas do not need a special case for it, and that is worth noticing.'
         : 'The pairing formula n(a1 + an)/2 is Gauss\'s trick: pair the first term with the last, '
           + 'the second with the second-last, and every pair adds to the same thing.');
  }

  /* ============================================== mode: geometric ======== */
  function paintGeom() {
    var a1 = Rread(inA1.value), r = Rread(inR.value);
    if (a1 === null || r === null) {
      fail('<strong>' + (a1 === null ? 'The first term' : 'The common ratio') + ' "'
        + esc(a1 === null ? inA1.value : inR.value) + '" is not a number I can use.</strong> '
        + 'Both boxes take a whole number or a fraction. The ratio is the interesting one: try '
        + '<code>1/2</code>, then <code>2</code>, then <code>1</code>, and watch the infinite sum '
        + 'go from a number to nothing to a division by zero.');
      return;
    }
    var N = termcount(), terms = [null], sums = [null], run = R0;
    for (var i = 1; i <= N; i += 1) {
      terms.push(i === 1 ? a1 : Rmul(terms[i - 1], r));
      run = Radd(run, terms[i]);
      sums.push(run);
    }
    var one = Requ(r, R1);
    var absLess = Rcmp(Rabs(r), R1) < 0;
    /* |r| < 1 is sufficient for the series to converge, not necessary: if the
       first term is 0 then every term is 0 and every partial sum is 0, whatever
       r does. Without this the page would print a table of zeros and then tell
       the reader those partial sums run away without bound. */
    var trivial = Rzero(a1) && !absLess;
    var body = [];
    for (var t = 1; t <= N; t += 1) {
      var byFormula = Rmul(a1, Rpow(r, t - 1));
      var sumFormula = one
        ? Rmul(R(BigInt(t)), a1)
        : Rdiv(Rmul(a1, Rsub(R1, Rpow(r, t))), Rsub(R1, r));
      var ok = Requ(byFormula, terms[t]) && Requ(sumFormula, sums[t]);
      body.push(tr([rowhead('n = ' + t), td(Rtext(terms[t])), td(Rtext(byFormula)),
                    td(Rtext(sums[t])), td(Rtext(sumFormula)),
                    td(ok ? chip('agree', 'ok') : chip('MISMATCH', 'no'))]));
    }
    var an = Rmul(a1, Rpow(r, N - 1));
    var sumA = sums[N];
    var sumB = one ? Rmul(R(BigInt(N)), a1) : Rdiv(Rmul(a1, Rsub(R1, Rpow(r, N))), Rsub(R1, r));
    var limit = absLess ? Rdiv(a1, Rsub(R1, r)) : (trivial ? R0 : null);

    var infinite, tail;
    if (trivial) {
      infinite = 'every term is 0, so every partial sum is 0 and the infinite sum is 0. |r| = '
        + Rtext(Rabs(r)) + ' is not below 1, and that condition exists to make r^n shrink &mdash; '
        + 'but a1 r^(n-1) is already 0 whatever r^(n-1) does, so there is nothing left for it to '
        + 'do. This is the one geometric sequence that converges for every ratio.';
      tail = 'Every term is 0 whatever r does, so the partial sums are 0, 0, 0, ... and they settle '
        + 'immediately rather than running away. |r| &lt; 1 is a sufficient condition for '
        + 'convergence and not a necessary one, and a1 = 0 is the case that shows the difference.';
    } else if (absLess) {
      infinite = 'r^n shrinks towards 0 as n grows, so a1(1 - r^n)/(1 - r) closes in on a1/(1 - r) = '
        + Rtext(limit) + '. Rounded, that limit is ' + approx(limit, 6) + ' &mdash; a rounding of the '
        + 'exact value, printed so you can place it on the graph.';
    } else if (one) {
      infinite = 'the sum formula divides by 1 - r, and 1 - r is 0. There is nothing to fix here: '
        + 'every term is ' + Rtext(a1) + ', the partial sums are ' + Rtext(a1) + ', ' + Rtext(Rmul(R(2n), a1))
        + ', ' + Rtext(Rmul(R(3n), a1)) + ', ... and they do not approach anything. The formula does '
        + 'not merely fail to apply &mdash; the quantity it names does not exist.';
    } else if (Requ(r, R(-1n))) {
      infinite = 'the partial sums are ' + Rtext(a1) + ', 0, ' + Rtext(a1) + ', 0, ... for ever. They '
        + 'do not grow and they do not settle, so there is no infinite sum. |r| = 1 exactly, and 1 is '
        + 'not less than 1.';
      tail = 'The partial sums alternate between ' + Rtext(a1) + ' and 0 for ever: they do not run '
        + 'away, and they still do not approach anything. "Diverges" covers both behaviours, which '
        + 'is why the condition is |r| below 1 rather than "the terms get smaller".';
    } else {
      infinite = '|r| = ' + Rtext(Rabs(r)) + ', which is at least 1, so r^n does not shrink and the '
        + 'partial sums run away without bound. The formula a1/(1 - r) would still hand back a '
        + 'number here, ' + Rtext(Rdiv(a1, Rsub(R1, r))) + ', and that number is meaningless: it is '
        + 'what you get by using a formula outside the condition it was derived under.';
      tail = 'r^n grows instead of shrinking, so the partial sums run away without bound. Notice '
        + 'that a1/(1 - r) still evaluates &mdash; to ' + Rtext(Rdiv(a1, Rsub(R1, r))) + ' &mdash; '
        + 'and that the number it produces means nothing at all: it comes from a derivation that '
        + 'assumed r^n was heading for 0.';
    }

    work.innerHTML =
      steps('The sequence, as defined', [
        ['first term a1', Rtext(a1)],
        ['common ratio r', Rtext(r) + ' &mdash; multiplied by, to get from each term to the next'],
        ['the rule', 'a(n) = ' + Rtext(r) + ' a(n-1),  and the claim is that a(n) = a1 r^(n-1)'],
      ])
      + table('Every term and every partial sum, computed both ways',
        ['', 'term, by multiplying', 'term, by a1 r^(n-1)', 'sum, by adding them up',
         one ? 'sum, by n a1' : 'sum, by a1(1 - r^n)/(1 - r)', 'agree?'], body)
      + steps('At n = ' + N + ', and beyond', [
        ['the nth term by stepping', Rtext(terms[N])],
        ['the nth term by formula', Rtext(a1) + ' x ' + Rterm(r) + '^' + (N - 1) + ' = ' + Rtext(an)],
        ['these agree?', agreechip(Requ(terms[N], an))],
        ['the sum by adding the terms up', Rtext(sumA)],
        ['the sum by the formula', Rtext(sumB) + (one ? '  (the r = 1 case, where the usual formula '
          + 'divides by zero and n a1 takes its place)' : '')],
        ['these agree?', agreechip(Requ(sumA, sumB))],
        ['and the infinite sum?', infinite],
      ]);

    /* Partial sums against n, with the limit drawn where there is one. */
    var ys = [];
    for (var s = 1; s <= N; s += 1) ys.push(Rnum(sums[s]));
    if (limit !== null) ys.push(Rnum(limit));
    var lo = Math.min.apply(null, ys), hi = Math.max.apply(null, ys);
    if (!isFinite(lo) || !isFinite(hi) || lo === hi) { lo = lo - 1; hi = hi + 1; }
    var pad = Math.max(0.5, (hi - lo) * 0.16);
    var plot = Plot(svg, { xmin: 0, xmax: N + 1, ymin: lo - pad, ymax: hi + pad });
    plot.frame();
    if (limit !== null) plot.hline(Rnum(limit), 'plot-asym', 'a1/(1 - r) = ' + Rtext(limit));
    for (var g = 1; g < N; g += 1) {
      plot.segment(g, Rnum(sums[g]), g + 1, Rnum(sums[g + 1]), 'plot-aux');
    }
    for (var h = 1; h <= N; h += 1) plot.point(h, Rnum(sums[h]), 'plot-point');
    plot.describe('The first ' + N + ' partial sums plotted against n'
      + (limit === null ? ', with no limit to draw because |r| is at least 1'
                        : ', with the limit ' + Rtext(limit) + ' drawn as a horizontal line') + '.');

    setkpi('a(' + N + ')', Rtext(an), 'sum to ' + N, Rtext(sumA),
           'infinite sum', limit === null ? 'does not exist' : Rtext(limit));

    if (trivial) {
      status.innerHTML = '<strong>a1 = 0, so every term is 0 and the infinite sum is 0.</strong> '
        + tail;
    } else if (absLess) {
      status.innerHTML = '<strong>|r| = ' + Rtext(Rabs(r)) + ' is below 1, so the infinite sum is '
        + Rtext(limit) + '.</strong> The graph shows the partial sums walking towards that line and '
        + 'never crossing it. Every partial sum above was computed twice, once by adding the terms '
        + 'up and once by the formula, and they agree exactly &mdash; which matters here more than '
        + 'anywhere else on this page, because a1(1 - r^n)/(1 - r) with r = ' + Rtext(r) + ' and n = '
        + N + ' is a fraction over ' + String(Rpow(r, N).d) + ', and a decimal would have run out of '
        + 'room to tell the last few partial sums apart.';
    } else if (one) {
      status.innerHTML = '<strong>r = 1: the sum formula divides by zero, so it says nothing here.</strong> '
        + 'The sequence is ' + Rtext(a1) + ', ' + Rtext(a1) + ', ' + Rtext(a1) + ', ... and the sum of '
        + N + ' of them is ' + Rtext(sumA) + ' &mdash; which the table computed by adding the terms '
        + 'up, and again by n a1, the formula that takes over when the usual one has a zero in its '
        + 'denominator. The partial sums climb a straight line on the graph and never level off. '
        + 'This is not a gap in the theory: a1(1 - r^n)/(1 - r) was derived by dividing by 1 - r, '
        + 'and that step was never available when r is 1.';
    } else {
      status.innerHTML = '<strong>|r| = ' + Rtext(Rabs(r)) + ', which is not below 1, so there is no '
        + 'infinite sum.</strong> ' + tail
        + ' The finite sums in the table are all perfectly real numbers and every one of them was '
        + 'checked against the formula; it is only the limit that does not exist. That distinction '
        + '&mdash; a formula for every finite n, no limit as n grows &mdash; is the whole content of '
        + 'the condition |r| &lt; 1.';
    }
  }

  /* =============================================== mode: binomial ======== */
  function pascalrows(n) {
    var rows = [[1n]];
    for (var i = 1; i <= n; i += 1) {
      var prev = rows[i - 1], row = [1n];
      for (var j = 1; j < i; j += 1) row.push(prev[j - 1] + prev[j]);
      row.push(1n);
      rows.push(row);
    }
    return rows;
  }
  function bfact(k) { var out = 1n; for (var i = 2n; i <= k; i += 1n) out *= i; return out; }
  function bchoose(n, k) {
    return bfact(BigInt(n)) / (bfact(BigInt(k)) * bfact(BigInt(n - k)));
  }
  function paintBinom() {
    var n = Math.max(0, Math.min(12, parseInt(String(selPow.value), 10) || 0));
    var text = String(inBin.value || '').trim();
    var poly = text ? Epolyof(text, 'x') : null;
    var rows = pascalrows(n);

    /* Pascal's triangle is built from additions and knows nothing about the
       reader's expression, so it is drawn whatever else went wrong. */
    var triangle = table("Pascal's triangle, each entry the sum of the two above it",
      [], rows.map(function (row, i) {
        return tr([rowhead('row ' + i)].concat(row.map(function (v) { return td(String(v)); })),
                  i === n ? 'focus' : '');
      }));
    var formula = table('The same row from the formula C(n, k) = n! / (k! (n-k)!)',
      ['k', 'n! / (k! (n-k)!)', 'from the triangle', 'agree?'],
      rows[n].map(function (v, k) {
        var c = bchoose(n, k);
        return tr([rowhead('k = ' + k),
                   td(String(bfact(n)) + ' / (' + String(bfact(k)) + ' x ' + String(bfact(n - k)) + ') = ' + String(c)),
                   td(String(v)), td(c === v ? chip('yes', 'ok') : chip('no', 'no'))]);
      }));

    if (poly === null) {
      fail('<strong>"' + esc(text) + '" is not a polynomial in x that I can read.</strong> '
        + 'Type two terms, such as <code>x + 1</code>, <code>2x - 3</code> or <code>x^2 - 2</code>. '
        + "Pascal's triangle below does not depend on it and is drawn anyway &mdash; the triangle is "
        + 'about the numbers C(n, k), not about any particular binomial.', triangle + formula);
      return;
    }
    var nonzero = [];
    for (var i = 0; i < poly.length; i += 1) if (!Rzero(poly[i])) nonzero.push(i);
    var expanded = Ppow(poly, n);

    if (nonzero.length !== 2) {
      var why = nonzero.length < 2
        ? 'it has ' + nonzero.length + ' non-zero ' + plural(nonzero.length, 'term', 'terms')
          + ', and a binomial has exactly two'
        : 'it has ' + nonzero.length + ' non-zero terms, and the binomial theorem is about exactly two';
      work.innerHTML = triangle + formula
        + steps('Why the theorem does not apply here', [
          ['what you typed', esc(text) + '  =  ' + Ptext(poly)],
          ['the problem', why],
          ['what multiplying out actually gives', '(' + Ptext(poly) + ')^' + n + ' = ' + Ptext(expanded)],
          ['how many terms that has', String(expanded.filter(function (c) { return !Rzero(c); }).length)
            + ', where the binomial theorem would have predicted ' + (n + 1)],
        ]);
      setkpi('exponent', String(n), 'terms typed', String(nonzero.length), 'theorem', 'does not apply');
      status.innerHTML = '<strong>' + esc(text) + ' is not a binomial, so the theorem has nothing to '
        + 'say about it.</strong> ' + why.charAt(0).toUpperCase() + why.slice(1) + '. Multiplying it '
        + 'out is still perfectly possible and the answer is above &mdash; what is missing is the '
        + 'shortcut. That is worth seeing: the binomial theorem is not a general fact about powers '
        + 'of polynomials, it is a fact about powers of exactly two terms, and the row of C(n, k) '
        + 'above is the right length for the wrong expression.';
      return;
    }

    var dHi = nonzero[1], dLo = nonzero[0];
    var cHi = poly[dHi], cLo = poly[dLo];
    var total = [], body = [];
    for (var k = 0; k <= n; k += 1) {
      var coefN = R(bchoose(n, k));
      var coef = Rmul(coefN, Rmul(Rpow(cHi, n - k), Rpow(cLo, k)));
      var deg = dHi * (n - k) + dLo * k;
      var tp = [];
      for (var z = 0; z < deg; z += 1) tp.push(R0);
      tp.push(coef);
      total = Padd(total, tp);
      body.push(tr([rowhead('k = ' + k), td(String(bchoose(n, k))),
                    tdl('(' + Ptext(polyof(cHi, dHi)) + ')^' + (n - k) + ' (' + Ptext(polyof(cLo, dLo)) + ')^' + k),
                    tdl(Ptext(tp))]));
    }
    var same = Pzero(Psub(total, expanded));

    work.innerHTML = triangle + formula
      + table('Each term: C(n, k) times the first term to the power n-k, times the second to the power k',
        ['', 'C(' + n + ', k)', 'the two powers', 'the term'], body)
      + steps('Three routes to the same expansion', [
        ['assembled from the coefficients above', Ptext(total)],
        ['by multiplying (' + Ptext(poly) + ') by itself ' + n + ' '
          + plural(n, 'time', 'times'), Ptext(expanded)],
        ['do they agree?', same ? chip('yes', 'ok') + ' every coefficient matches'
          : chip('no', 'no') + ' which is a bug and not a lesson'],
        ['the coefficients on their own', rows[n].join(', ')
          + ' &mdash; row ' + n + " of Pascal's triangle, which is where they came from"],
      ]);

    setkpi('exponent', String(n), 'terms in the answer', String(n + 1),
           'checks', same ? 'all passed' : 'FAILED');
    status.innerHTML = '<strong>(' + Ptext(poly) + ')^' + n + ' = ' + Ptext(expanded) + '.</strong> '
      + 'Three independent computations produced that: Pascal\'s triangle built by adding pairs of '
      + 'numbers, the factorial formula C(n, k) = n!/(k!(n-k)!), and simply multiplying the '
      + 'binomial by itself ' + n + ' ' + plural(n, 'time', 'times') + '. They agree, and they had '
      + 'no way of knowing about each other. '
      + (n === 0
         ? 'You have the exponent at 0, where every one of them says 1: the empty product, one term, '
           + 'row 0 of the triangle. That is not a special case bolted on, it is what the formulas say.'
         : 'The factorials get large quickly &mdash; ' + String(bfact(n)) + ' at n = ' + n
           + ' &mdash; which is why they are computed in BigInt: at n = 21 an ordinary number can no '
           + 'longer hold n! exactly, and the coefficients would start coming out wrong while still '
           + 'looking plausible.');
  }
  /* One monomial as a polynomial, for printing a single term of the binomial. */
  function polyof(coef, deg) {
    var out = [];
    for (var i = 0; i < deg; i += 1) out.push(R0);
    out.push(coef);
    return out;
  }

  /* ---------------------------------------------------------- the driver */
  function redraw() {
    if (MODE === 'define') {
      titleOut.textContent = 'a1 = ' + String(inA1.value) + ',  a(n) = ' + String(inRec.value);
      subOut.textContent = 'against the closed form ' + String(inClosed.value);
      paintDefine();
    } else if (MODE === 'arithmetic') {
      titleOut.textContent = 'a1 = ' + String(inA1.value) + ',  d = ' + String(inD.value);
      subOut.textContent = 'the first ' + termcount() + ' terms, and their sum';
      paintArith();
    } else if (MODE === 'geometric') {
      titleOut.textContent = 'a1 = ' + String(inA1.value) + ',  r = ' + String(inR.value);
      subOut.textContent = 'the first ' + termcount() + ' terms, their sum, and the limit';
      paintGeom();
    } else {
      titleOut.textContent = '(' + String(inBin.value) + ')^' + String(selPow.value);
      subOut.textContent = "expanded by Pascal's triangle and by C(n, k)";
      paintBinom();
    }
  }

  function applyPreset() {
    var p = PRESETS[Math.max(0, Math.min(PRESETS.length - 1, parseInt(preset.value, 10) || 0))];
    if (!p) return;
    if (inA1) inA1.value = p.a1 || '1';
    if (inRec) inRec.value = p.rec || '';
    if (inClosed) inClosed.value = p.closed || '';
    if (inD) inD.value = p.d || '1';
    if (inR) inR.value = p.r || '1/2';
    if (inBin) inBin.value = p.bin || 'x + 1';
    if (selN && p.n) selN.value = p.n;
    if (selPow && p.pow) selPow.value = p.pow;
  }
  preset.addEventListener('change', function () { applyPreset(); redraw(); });
  [inA1, inRec, inClosed, inD, inR, inBin].forEach(function (el) {
    if (el) el.addEventListener('input', redraw);
  });
  if (selN) selN.addEventListener('change', redraw);
  if (selPow) selPow.addEventListener('change', redraw);
  applyPreset();
  redraw();
  window.redrawLab = redraw;
"""


def sequence_lab(cfg):
    """Sequences, where the formula is checked rather than announced.

    The teaching decision: every quantity a formula names is also computed the
    long way -- the nth term by stepping through the recursion, the sum by
    adding the terms up one at a time, the binomial coefficients by adding
    pairs in Pascal's triangle -- and the page prints both and says whether
    they matched. A lesson that has not yet proved a1 + (n-1)d cannot honestly
    assert it, and this is the difference between showing a reader the formula
    works and telling them it does.

    It is also what lets `geometric` demonstrate rather than warn: the sum
    formula divides by 1 - r, so at r = 1 there is nothing to print, and the
    column that added the terms up carries on quite happily beside the gap.
    """
    mode = cfg.get("mode", "arithmetic")
    if mode not in SEQ_PRESETS:
        mode = "arithmetic"
    presets = cfg.get("presets") or SEQ_PRESETS[mode]
    title, subtitle = SEQ_TITLES[mode]
    has_plot = mode == "geometric"
    labels = [p.get("label", "example %d" % (i + 1)) for i, p in enumerate(presets)]

    def field(fid, label):
        return ('        <div class="field" id="%sField">\n'
                '          <label for="%s">%s</label>\n'
                '          <input id="%s" type="text" value="" inputmode="text" autocomplete="off">\n'
                "        </div>\n" % (fid, fid, label, fid))

    fields = ""
    if mode == "define":
        fields = (field("sqA1", "First term a1")
                  + field("sqRec", "Recursive rule for a(n), using p for the previous term")
                  + field("sqClosed", "Closed form for a(n), using n"))
    elif mode == "arithmetic":
        fields = field("sqA1", "First term a1") + field("sqD", "Common difference d")
    elif mode == "geometric":
        fields = field("sqA1", "First term a1") + field("sqR", "Common ratio r")
    else:
        fields = field("sqBin", "The binomial, in x")

    if mode == "binomial":
        fields += (
            '        <div class="field" id="sqPowField">\n'
            '          <label for="sqPow">Exponent n</label>\n'
            '          <select id="sqPow">'
            + "".join('<option value="%s">n = %s</option>' % (v, v) for v in SEQ_POWERS)
            + "</select>\n        </div>\n"
        )
    else:
        fields += (
            '        <div class="field" id="sqNField">\n'
            '          <label for="sqN">How many terms</label>\n'
            '          <select id="sqN">'
            + "".join('<option value="%s"%s>%s terms</option>'
                      % (v, ' selected' if v == "10" else "", v) for v in SEQ_COUNTS)
            + "</select>\n        </div>\n"
        )

    legend = {
        "define": '<span class="tone-cyan"><i class="legend-swatch"></i>the recursion</span>'
                  '<span class="tone-purple"><i class="legend-swatch"></i>the closed form</span>'
                  '<span class="tone-red"><i class="legend-swatch"></i>where they differ</span>',
        "arithmetic": '<span class="tone-cyan"><i class="legend-swatch"></i>done the long way</span>'
                      '<span class="tone-purple"><i class="legend-swatch"></i>done by formula</span>',
        "geometric": '<span class="tone-cyan"><i class="legend-swatch"></i>the partial sums</span>'
                     '<span class="tone-red"><i class="legend-swatch"></i>the limit, where there is one</span>',
        "binomial": "<span class=\"tone-cyan\"><i class=\"legend-swatch\"></i>Pascal's triangle</span>"
                    '<span class="tone-purple"><i class="legend-swatch"></i>the C(n, k) formula</span>'
                    '<span class="tone-green"><i class="legend-swatch"></i>multiplied out</span>',
    }[mode]

    stage = ('      <div class="lab-stage" id="sqStage"><svg id="sqPlot"></svg></div>\n'
             if has_plot else "")
    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong id="sqTitle">Sequence</strong><span id="sqSub"></span></div>\n'
        '        <div class="inline-legend">' + legend + "</div>\n"
        "      </div>\n"
        + stage
        + '      <div id="sqWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="sqStatus" style="margin-top:12px;"></div>'
    )

    hint = {
        "define": "The recursive rule may use <code>p</code> for the previous term and <code>n</code> "
                  "for the position: <code>p + 3</code>, <code>p/2 + 1</code>, <code>p + 2n - 1</code>. "
                  "The closed form uses <code>n</code> alone: <code>n^2</code>, "
                  "<code>3*2^(n - 1)</code>. Both are evaluated in exact fractions.",
        "binomial": "Type a binomial in <code>x</code>: <code>x + 1</code>, <code>2x - 3</code>, "
                    "<code>x^2 - 2</code>. Every coefficient below is exact, and the factorials are "
                    "computed in BigInt so that n = 12 is as reliable as n = 3.",
    }.get(
        mode,
        "Both boxes take whole numbers or fractions such as <code>3/2</code>. Every term, every "
        "partial sum and every formula below is an exact fraction, computed from what is in these "
        "two boxes.",
    )

    controls = (
        '        <div class="field" id="sqFieldPreset">\n'
        '          <label for="sqPreset">Worked example</label>\n'
        '          <select id="sqPreset">' + _options(labels) + "</select>\n"
        "        </div>\n"
        + fields
        + _kpi("sq")
        + '        <p class="small-copy" id="sqHint" style="margin:0;">' + hint + "</p>"
    )

    script = (
        RATIONAL_JS + POLY_JS + EXPR_JS + PLOT_JS + FORMAT_JS + LINEAR_JS + EXACT_JS
        + cfg_literal("PRESETS", presets)
        + SEQ_SCRIPT
        .replace("__MODE__", mode)
        .replace("__HASPLOT__", "true" if has_plot else "false")
    )

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a worked example, or define your own sequence"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every formula on this page is checked against the thing it is a formula for. The terms "
            "are added up one at a time beside the closed form for their sum, and the page says "
            "whether the two agreed rather than assuming they did.",
        ),
        script=script,
    )
