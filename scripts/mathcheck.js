#!/usr/bin/env node
/*
 * Test the ARITHMETIC the algebra path is built on.
 *
 * WHY THIS EXISTS, and why it is separate from labcheck.js. That harness proves
 * every published lab runs and paints. It cannot prove the numbers are right: a
 * lab that confidently reports the wrong roots passes it, and passes every
 * markup assertion in tests/ too. The footer of every algebra page promises the
 * reader that each figure is computed from the stated definition and that the
 * arithmetic is exact. This file is what makes that promise checkable.
 *
 * The JavaScript under test IS the JavaScript that ships. It is extracted from
 * scripts/mathpath/labs/algebra_core.py, which holds it as raw strings, so
 * there is no second copy to drift -- testing a transcription would prove
 * nothing about the published pages.
 *
 * Usage:  node scripts/mathcheck.js
 */

const fs = require('fs');
const path = require('path');

const SOURCE = path.join(__dirname, 'mathpath', 'labs', 'algebra_core.py');
const src = fs.readFileSync(SOURCE, 'utf8');

/* Each block is  NAME = r"""..."""  in the Python module. */
function block(name) {
  const m = new RegExp(name + ' = r"""([\\s\\S]*?)"""', 'm').exec(src);
  if (!m) { console.error('cannot find ' + name + ' in ' + SOURCE); process.exit(2); }
  return m[1];
}

let fails = 0;
function eq(got, want, label) {
  if (String(got) !== String(want)) { fails += 1; console.log('  FAIL ' + label + ': got ' + got + ', want ' + want); }
}
function near(got, want, tol, label) {
  if (!(Math.abs(got - want) <= tol)) { fails += 1; console.log('  FAIL ' + label + ': got ' + got + ', want ~' + want); }
}

/* A minimal SVG DOM, the same shape scripts/labcheck.js gives a real page. */
function El(name) { this.name = name; this.attrs = {}; this.children = []; this._text = ''; }
El.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
El.prototype.getAttribute = function (k) { return this.attrs[k]; };
El.prototype.appendChild = function (c) { this.children.push(c); return c; };
Object.defineProperty(El.prototype, 'textContent', {
  get: function () { return this._text; },
  set: function (v) { this._text = String(v); if (v === '') this.children = []; }
});
global.document = { createElementNS: function (_ns, n) { return new El(n); } };
function all(el, name, out) {
  out = out || [];
  el.children.forEach(function (c) { if (c.name === name) out.push(c); all(c, name, out); });
  return out;
}

eval(block('RATIONAL_JS') + block('POLY_JS') + block('EXPR_JS') + block('SURD_JS') + block('PLOT_JS'));

// ------------------------------------------------- exact rational arithmetic
console.log('exact rationals');
eq(Rtext(Radd(R(1n, 3n), R(1n, 6n))), '1/2', '1/3 + 1/6');
eq(Rtext(Rmul(R(2n, 3n), R(9n, 4n))), '3/2', '2/3 * 9/4');
eq(Rtext(Rdiv(R(-3n, 4n), R(6n, 8n))), '-1', '-3/4 / 3/4');
eq(Rtext(Rpow(R(2n, 3n), 3)), '8/27', '(2/3)^3');
eq(Rtext(Rpow(R(2n), -3)), '1/8', '2^-3');
eq(Rtext(Rparse('-7/14')), '-1/2', 'parse -7/14 in lowest terms');
eq(Rtext(Rparse('0.375')), '3/8', 'a decimal becomes an exact fraction');
eq(Rtext(Rsqrt(R(4n, 9n))), '2/3', 'sqrt(4/9)');
eq(Rsqrt(R(2n)), 'null', 'sqrt(2) is not rational, and says so');
eq(Rcmp(R(1n, 3n), R(1n, 2n)), -1, 'comparison');
/* Exactness is the whole promise: forty additions of a third stay a third. */
let big = R(1n, 3n);
for (let i = 0; i < 40; i += 1) big = Radd(big, R(1n, 3n));
eq(Rtext(big), '41/3', '41 thirds, exactly');

// ------------------------------------------------------ polynomials over Q
console.log('polynomials over Q');
function P() { return Array.prototype.slice.call(arguments).map(v => (typeof v === 'object' ? v : R(BigInt(v)))); }
eq(Ptext(P(-6, 1, 1)), 'x^2 + x - 6', 'standard form');
eq(Ptext(P(0, 0, 3)), '3x^2', 'a monomial');
eq(Ptext(P(1, -1)), '-x + 1', 'a leading -1 is written as a sign');
eq(Ptext([R(3n, 4n), R(1n)]), 'x + (3/4)', 'a fractional coefficient is bracketed');
eq(Ptext([]), '0', 'the zero polynomial');
eq(Pdeg([]), -1, 'the zero polynomial has degree -1');
eq(Ptext(Pmul(P(-2, 1), P(3, 1))), 'x^2 + x - 6', '(x-2)(x+3) expands');
eq(Rtext(Peval(P(-6, 1, 1), R(2n))), '0', 'p(2) = 0');
eq(Ptext(Pderiv(P(-6, 1, 1))), '2x + 1', 'derivative');
const dm = Pdivmod(P(-6, 1, 1), P(-2, 1));
eq(Ptext(dm.q) + ' r ' + Ptext(dm.r), 'x + 3 r 0', 'exact division');
const dm2 = Pdivmod(P(1, 0, 0, 1), P(-1, 1));
eq(Ptext(dm2.q) + ' r ' + Ptext(dm2.r), 'x^2 + x + 1 r 2', 'x^3+1 divided by x-1');
eq(Ptext(Pgcd(P(-6, 1, 1), P(-4, 0, 1))), 'x - 2', 'polynomial gcd');

// ---------------------------------------- the rational root theorem, applied
console.log('rational roots and factoring');
eq(Prationalroots(P(-6, 1, 1)).map(Rtext).join(','), '-3,2', 'roots of x^2+x-6');
eq(Prationalroots(P(-3, 5, 2)).map(Rtext).join(','), '-3,1/2', 'roots of 2x^2+5x-3');
eq(Prationalroots(P(1, 0, 1)).length, 0, 'x^2+1 has no rational root');
/* Factors come out in ascending order of their root: deterministic and stated. */
eq(Pfactortextfull(P(-6, 1, 1)), '(x + 3)(x - 2)', 'factor x^2+x-6');
eq(Pfactortextfull(P(-3, 5, 2)), '(x + 3)(2x - 1)', 'factor 2x^2+5x-3');
eq(Pfactortextfull(P(4, -4, 1)), '(x - 2)^2', 'a perfect square keeps its multiplicity');
eq(Pfactortextfull(P(1, 0, 1)), 'x^2 + 1', 'an irreducible polynomial is written as itself');
eq(Pfactortextfull(P(-4, 0, 1)), '(x + 2)(x - 2)', 'difference of squares');
eq(Pfactortextfull(P(0, -9, 0, 1)), 'x(x + 3)(x - 3)', 'x^3-9x');
eq(Pfactortextfull(P(6, -5, 1)), '(x - 2)(x - 3)', 'x^2-5x+6');
/* 4x^3-8x-12 = 4(x^3-2x-3), and +-1, +-3 are the only candidates: none works. */
eq(Pfactortextfull(P(-12, -8, 0, 4)), '4(x^3 - 2x - 3)', 'the content comes out, the cubic stays');
eq(Pfactor(P(-12, -8, 0, 4)).complete, false, 'a cubic leftover is not claimed complete');
eq(Pfactor(P(1, 0, 1)).complete, true, 'a quadratic leftover is complete');

// ------------------------------------------------------- expression parsing
console.log('the expression parser');
const ev = (s, x) => Eeval(Eparse(s), { x: x });
const pol = (s) => { const p = Epolyof(s); return p === null ? 'null' : Ptext(p); };
eq(ev('2x', 3), 6, 'implicit multiplication: 2x');
eq(ev('3(x+1)', 4), 15, '3(x+1)');
eq(ev('(x+1)(x-2)', 5), 18, '(x+1)(x-2)');
eq(ev('4x^2', 3), 36, '4x^2');
eq(ev('2sqrt(x)', 9), 6, '2sqrt(x)');
eq(Eeval(Eparse('xy'), { x: 3, y: 4 }), 12, 'xy is a product of two variables');
/* The two places a reader is marked wrong. */
eq(ev('-x^2', 3), -9, '-x^2 means -(x^2)');
eq(ev('(-x)^2', 3), 9, '(-x)^2');
eq(ev('2^3^2', 0), 512, '^ is right-associative');
eq(ev('8/2/2', 0), 2, '/ is left-associative');
eq(ev('2*3^2', 0), 18, 'power before times');
eq(isNaN(ev('sqrt(x)', -1)), true, 'outside the domain gives NaN, not an exception');
/* Errors are named rather than swallowed. */
const msg = (s) => { try { Eparse(s); return ''; } catch (e) { return e.message; } };
eq(msg('2x +'), 'the expression ends early', 'a trailing operator');
eq(msg('sqrtt(x)'), 'unknown function "sqrtt"', 'a typo in a function name');
eq(msg('x $ 2'), 'unexpected character "$"', 'a stray character');
eq(msg('(x+1'), 'expected ")"', 'an unclosed bracket');
/* Typed input reaches the EXACT machinery, not a float approximation of it. */
eq(pol('(x+1)(x-2)'), 'x^2 - x - 2', 'a typed product expands exactly');
eq(pol('(x/3) + 1/2'), '(1/3)x + (1/2)', 'rational coefficients stay exact');
eq(pol('(2x-1)^3'), '8x^3 - 12x^2 + 6x - 1', 'a typed cube expands');
eq(pol('sqrt(x)'), 'null', 'sqrt(x) is not a polynomial');
eq(pol('1/x'), 'null', 'division by x is not a polynomial');
eq(pol('0.1x + 0.2x'), '(3/10)x', '0.1 + 0.2 is 3/10, not 0.30000000000000004');

// ----------------------------------------------- surds and quadratic roots
console.log('exact surds and quadratic roots');
const Q = (v) => R(BigInt(v));
eq(surdtext(Rsurd(Q(9))), '3', 'sqrt(9)');
eq(surdtext(Rsurd(Q(8))), '2sqrt(2)', 'sqrt(8)');
eq(surdtext(Rsurd(R(1n, 2n))), '(1/2)sqrt(2)', 'sqrt(1/2)');
eq(surdtext(Rsurd(Q(72))), '6sqrt(2)', 'sqrt(72)');
let r = quadroots(Q(1), Q(-5), Q(6));
eq(r.kind + ' ' + r.roots.map(Rtext).join(','), 'rational 2,3', 'x^2-5x+6');
r = quadroots(Q(1), Q(-2), Q(-4));
eq(r.kind + ' ' + pmtext(r.p, r.s), 'irrational 1 +- sqrt(5)', 'x^2-2x-4 keeps its surd');
r = quadroots(Q(1), Q(-4), Q(4));
eq(r.kind + ' ' + Rtext(r.roots[0]), 'double 2', 'a repeated root');
r = quadroots(Q(1), Q(0), Q(1));
eq(r.kind + ' ' + pmtext(r.p, r.s, true), 'complex +-i', 'x^2+1');
r = quadroots(Q(1), Q(-2), Q(5));
eq(r.kind + ' ' + pmtext(r.p, r.s, true), 'complex 1 +- 2i', 'x^2-2x+5');
eq(quadroots(Q(2), Q(5), Q(-3)).roots.map(Rtext).join(','), '-3,1/2', '2x^2+5x-3');
r = quadroots(Q(3), Q(-6), Q(2));
eq(pmtext(r.p, r.s), '1 +- (1/3)sqrt(3)', '3x^2-6x+2');
/* The irrational pair really are roots: substitute them back. */
{
  const a = 3, b = -6, c = 2;
  const pv = Rnum(r.p), sv = Rnum(r.s.q) * Math.sqrt(Number(r.s.k));
  eq(Math.abs(a * (pv + sv) * (pv + sv) + b * (pv + sv) + c) < 1e-12, true, 'the + root checks out');
  eq(Math.abs(a * (pv - sv) * (pv - sv) + b * (pv - sv) + c) < 1e-12, true, 'the - root checks out');
}

// ------------------------------------------------------------- the grapher
console.log('the grapher');
{
  const svg = new El('svg');
  const p = Plot(svg, { xmin: -5, xmax: 5, ymin: -10, ymax: 10 });
  near(p.sx(-5), 44, 0.01, 'left edge');
  near(p.sx(5), 644, 0.01, 'right edge');
  near(p.sx(0), 344, 0.01, 'x = 0 is centred');
  near(p.sy(10), 16, 0.01, 'top edge');
  near(p.sy(-10), 386, 0.01, 'bottom edge');
  eq(p.sy(5) < p.sy(-5), true, 'positive y is higher on screen');
  p.frame();
  eq(svg.getAttribute('viewBox'), '0 0 660 420', 'viewBox');
  const axes = all(svg, 'line').filter(l => l.attrs.class === 'plot-axis');
  eq(axes.length, 2, 'two axes');
  near(parseFloat(axes[0].attrs.y1), 201, 0.01, 'the x-axis sits at y = 0');
  near(parseFloat(axes[1].attrs.x1), 344, 0.01, 'the y-axis sits at x = 0');
}
{
  /* A window with zero out of view still gets a labelled frame. */
  const svg = new El('svg');
  Plot(svg, { xmin: 10, xmax: 20, ymin: 100, ymax: 200 }).frame();
  const axes = all(svg, 'line').filter(l => l.attrs.class === 'plot-axis');
  near(parseFloat(axes[0].attrs.y1), 386, 0.01, 'the x-axis pins to the near edge');
  near(parseFloat(axes[1].attrs.x1), 44, 0.01, 'the y-axis pins to the near edge');
}
function runs(fn) {
  const svg = new El('svg');
  Plot(svg, { xmin: -5, xmax: 5, ymin: -10, ymax: 10 }).frame().curve(fn);
  return all(svg, 'polyline');
}
eq(runs(x => x * x - 4).length, 1, 'a parabola is one unbroken run');
/* Joining across a pole draws a vertical line that is not part of the graph,
   which is exactly why readers believe 1/x is connected.
   The curve breaks for TWO different reasons and both need testing. A pole the
   sampler lands on exactly returns Infinity and breaks on the non-finite check;
   a pole it steps over returns two large finite values of opposite sign and can
   only be caught by the jump check. Sampling runs from -5 to 5 in 480 steps, so
   x = 0 IS a sample and x = 0.3 is not -- and a test using only 1/x passes with
   the jump check deleted, which is how this gap was found. */
eq(runs(x => 1 / x).length, 2, '1/x: a pole landed on exactly');
eq(runs(x => 1 / (x - 0.3)).length, 2, '1/(x-0.3): a pole stepped over');
eq(runs(x => 1 / (x * x - 0.09)).length, 3, 'two stepped-over poles give three runs');
{
  const rs = runs(x => Math.sqrt(x));
  eq(rs.length, 1, 'sqrt(x) is one run');
  eq(parseFloat(rs[0].attrs.points.split(' ')[0].split(',')[0]) >= 343.9, true,
     'sqrt(x) starts at x = 0 and not before');
}
{
  const svg = new El('svg');
  const pl = Plot(svg, { xmin: -5, xmax: 5, ymin: -10, ymax: 10 }).frame();
  pl.point(2, -4, 'plot-point root', '2');
  const c = all(svg, 'circle').filter(e => e.attrs.class === 'plot-point root');
  near(parseFloat(c[0].attrs.cx), 464, 0.01, 'a marked point lands where the number says');
  near(parseFloat(c[0].attrs.cy), 275, 0.01, 'and at the right height');
  pl.vline(3, 'plot-asym', 'x = 3');
  near(parseFloat(all(svg, 'line').filter(e => e.attrs.class === 'plot-asym')[0].attrs.x1), 524, 0.01,
       'an asymptote lands where the number says');
  const before = all(svg, 'circle').length;
  pl.point(NaN, 3); pl.point(1, Infinity);
  eq(all(svg, 'circle').length, before, 'a non-finite point is skipped, not drawn at NaN');
}
{
  const svg = new El('svg');
  NumberLine(svg, -10, 10).interval(-3, 5, true, false);
  const ends = all(svg, 'circle');
  eq(ends.length, 2, 'an interval has two endpoints');
  eq(ends[0].attrs.class, 'plot-end closed', 'a closed end is filled');
  eq(ends[1].attrs.class, 'plot-end open', 'an open end is hollow');
  near(parseFloat(ends[0].attrs.cx), 30 + (7 / 20) * 600, 0.01, 'the closed end is placed correctly');
}

if (fails) {
  console.log('\n' + fails + ' assertion(s) FAILED');
  process.exit(1);
}
console.log('\nevery arithmetic assertion passes');
