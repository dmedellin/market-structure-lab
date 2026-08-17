"""Labs for course 6: number theory and cryptography."""

from .common import Lab, cfg_literal

NT_JS = r"""
  /* Everything here is BigInt. Modular exponentiation with 4-digit moduli
     already overflows exact double arithmetic, and a cryptography lab that
     silently rounded would produce ciphertext that does not decrypt -- with no
     sign that arithmetic rather than the method was at fault. */
  function bgcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { var t = a % b; a = b; b = t; } return a; }
  function egcd(a, b) {
    /* Returns [g, x, y] with a*x + b*y = g. The coefficients are what make
       Bezout's identity constructive rather than an existence claim. */
    var old_r = a, r = b, old_s = 1n, s = 0n, old_t = 0n, t = 1n;
    while (r !== 0n) {
      var q = old_r / r;
      var tmp = old_r - q * r; old_r = r; r = tmp;
      tmp = old_s - q * s; old_s = s; s = tmp;
      tmp = old_t - q * t; old_t = t; t = tmp;
    }
    return [old_r, old_s, old_t];
  }
  function modpow(base, exp, mod) {
    var result = 1n; base %= mod;
    if (base < 0n) base += mod;
    while (exp > 0n) {
      if (exp & 1n) result = result * base % mod;
      base = base * base % mod;
      exp >>= 1n;
    }
    return result;
  }
  function modinv(a, m) {
    var e = egcd(((a % m) + m) % m, m);
    if (e[0] !== 1n) return null;
    return ((e[1] % m) + m) % m;
  }
  function isPrimeBig(n) {
    if (n < 2n) return false;
    if (n % 2n === 0n) return n === 2n;
    for (var d = 3n; d * d <= n; d += 2n) if (n % d === 0n) return false;
    return true;
  }
"""


def number_lab(cfg):
    """One lab, six modes, each showing the ALGORITHM rather than its output.

    A gcd that appears is a fact to memorize; a gcd with its division steps
    laid out is a method the reader can run on paper afterwards. Every mode
    here prints its trace.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="ntTitle">Number theory workbench</strong><span id="ntSub"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>the step that decides</span></div>
      </div>
      <div class="lab-stage"><div class="table-wrap" id="ntOut"></div></div>
      <div class="status-banner" id="ntStatus" style="margin-top:12px;"></div>"""
    controls = """        <div class="field">
          <label for="ntMode">Mode</label>
          <select id="ntMode">
            <option value="div">Division algorithm: a = qb + r</option>
            <option value="euclid">Euclidean algorithm: gcd(a, b)</option>
            <option value="bezout">Extended Euclid: ax + by = gcd</option>
            <option value="modtable">Modular arithmetic tables</option>
            <option value="modexp">Modular exponentiation by squaring</option>
            <option value="congr">Solve ax &equiv; b (mod m)</option>
            <option value="crt">Chinese remainder theorem</option>
            <option value="fermat">Fermat and Euler</option>
            <option value="sieve">Sieve of Eratosthenes</option>
            <option value="factor">Prime factorisation</option>
          </select>
        </div>
        <div class="field" id="ntAWrap">
          <label for="ntA">a</label>
          <input id="ntA" type="number" value="1071" />
        </div>
        <div class="field" id="ntBWrap">
          <label for="ntB">b</label>
          <input id="ntB" type="number" value="462" />
        </div>
        <div class="field" id="ntMWrap">
          <label for="ntM">m (modulus)</label>
          <input id="ntM" type="number" value="26" />
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span id="ntK1Label">gcd</span><strong id="ntK1">&mdash;</strong></div>
          <div class="kpi"><span id="ntK2Label">steps</span><strong id="ntK2">&mdash;</strong></div>
        </div>"""

    script = NT_JS + r"""
  var modeSel = document.getElementById('ntMode');
  var aIn = document.getElementById('ntA'), bIn = document.getElementById('ntB'), mIn = document.getElementById('ntM');
  var out = document.getElementById('ntOut'), status = document.getElementById('ntStatus');
  var title = document.getElementById('ntTitle'), sub = document.getElementById('ntSub');
  var k1 = document.getElementById('ntK1'), k2 = document.getElementById('ntK2');
  var k1L = document.getElementById('ntK1Label'), k2L = document.getElementById('ntK2Label');

  function table(head, rows) {
    return '<table class="tt"><thead><tr>' + head.map(function (h) { return '<th>' + h + '</th>'; }).join('')
      + '</tr></thead><tbody>' + rows.join('') + '</tbody></table>';
  }
  function row(cells, focus) {
    return '<tr' + (focus ? ' class="focus"' : '') + '>' + cells.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>';
  }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  function show(fields) {
    ['A', 'B', 'M'].forEach(function (f) {
      document.getElementById('nt' + f + 'Wrap').hidden = fields.indexOf(f) === -1;
    });
  }

  var MODES = {
    div: function (a, b) {
      show(['A', 'B']);
      title.textContent = 'Division algorithm';
      sub.textContent = 'a = qb + r with 0 ≤ r < |b|';
      if (b === 0n) { out.innerHTML = ''; status.textContent = 'b must not be 0 — division by zero has no quotient.'; return; }
      var q = a / b, r = a - q * b;
      if (r < 0n) { q -= (b > 0n ? 1n : -1n); r = a - q * b; }
      out.innerHTML = table(['a', 'b', 'q', 'r', 'check a = qb + r'],
        [row([a, b, q, r, q + '·' + b + ' + ' + r + ' = ' + (q * b + r)], true)]);
      k1L.textContent = 'remainder'; k1.textContent = r;
      k2L.textContent = 'quotient'; k2.textContent = q;
      status.innerHTML = 'The theorem says this q and r are <strong>unique</strong>: exactly one pair satisfies '
        + 'a = qb + r with 0 ≤ r &lt; |b|. Note the remainder is never negative here even when a is — '
        + 'which is why −7 mod 3 is 2, not −1.';
    },
    euclid: function (a, b) {
      show(['A', 'B']);
      title.textContent = 'Euclidean algorithm';
      sub.textContent = 'replace (a, b) by (b, a mod b) until b = 0';
      var rows = [], x = a < 0n ? -a : a, y = b < 0n ? -b : b, steps = 0;
      while (y !== 0n) {
        var q = x / y, r = x % y;
        rows.push(row([x, y, q, r], r === 0n));
        x = y; y = r; steps += 1;
        if (steps > 200) break;
      }
      out.innerHTML = table(['a', 'b', 'q = ⌊a/b⌋', 'r = a mod b'], rows);
      k1L.textContent = 'gcd'; k1.textContent = x;
      k2L.textContent = 'divisions'; k2.textContent = steps;
      status.innerHTML = 'gcd(' + a + ', ' + b + ') = <strong>' + x + '</strong> in ' + steps + ' divisions. '
        + 'Each line is justified by one fact: gcd(a, b) = gcd(b, a mod b), because any common divisor of a and b '
        + 'divides a − qb. Listing divisors of ' + a + ' instead would take vastly longer.';
    },
    bezout: function (a, b) {
      show(['A', 'B']);
      title.textContent = 'Extended Euclidean algorithm';
      sub.textContent = 'ax + by = gcd(a, b)';
      var e = egcd(a, b);
      var rows = [row([a, b, e[1], e[2], e[0], a + '·(' + e[1] + ') + ' + b + '·(' + e[2] + ') = ' + (a * e[1] + b * e[2])], true)];
      out.innerHTML = table(['a', 'b', 'x', 'y', 'gcd', 'check'], rows);
      k1L.textContent = 'gcd'; k1.textContent = e[0];
      k2L.textContent = 'x, y'; k2.textContent = e[1] + ', ' + e[2];
      status.innerHTML = 'Bézout: the gcd is not merely a common divisor, it is the smallest positive '
        + 'integer expressible as ' + a + 'x + ' + b + 'y. The coefficients above are computed by running '
        + 'the Euclidean algorithm backwards, which is also where modular inverses come from.';
    },
    modtable: function (a, b, m) {
      show(['M']);
      title.textContent = 'Arithmetic modulo ' + m;
      sub.textContent = 'addition and multiplication tables';
      if (m < 2n || m > 16n) { out.innerHTML = ''; status.textContent = 'Choose a modulus between 2 and 16 so the tables fit.'; return; }
      var n = Number(m);
      function build(op, symbol) {
        var head = [symbol];
        for (var i = 0; i < n; i += 1) head.push(i);
        var rows = [];
        for (var r = 0; r < n; r += 1) {
          var cells = ['<strong>' + r + '</strong>'];
          for (var c = 0; c < n; c += 1) cells.push(op(r, c));
          rows.push(row(cells, false));
        }
        return table(head, rows);
      }
      out.innerHTML = '<div style="margin-bottom:14px;">' + build(function (x, y) { return (x + y) % n; }, '+')
        + '</div>' + build(function (x, y) { return (x * y) % n; }, '×');
      var units = [];
      for (var u = 1; u < n; u += 1) if (bgcd(BigInt(u), m) === 1n) units.push(u);
      k1L.textContent = 'units'; k1.textContent = units.length;
      k2L.textContent = 'prime?'; k2.textContent = isPrimeBig(m) ? 'yes' : 'no';
      status.innerHTML = 'The ' + units.length + ' elements with a multiplicative inverse are '
        + units.join(', ') + ' — exactly those coprime to ' + m + '. '
        + (isPrimeBig(m)
            ? 'Because ' + m + ' is prime, every nonzero element is invertible, so this is a field.'
            : 'Because ' + m + ' is composite, some nonzero products are 0 (zero divisors), and those elements have no inverse.');
    },
    modexp: function (a, b, m) {
      show(['A', 'B', 'M']);
      title.textContent = 'Modular exponentiation';
      sub.textContent = 'a^b mod m by repeated squaring';
      if (m < 2n) { out.innerHTML = ''; status.textContent = 'The modulus must be at least 2.'; return; }
      if (b < 0n) { out.innerHTML = ''; status.textContent = 'Use a non-negative exponent.'; return; }
      var rows = [], base = ((a % m) + m) % m, exp = b, result = 1n, bit = 0;
      while (exp > 0n) {
        var use = (exp & 1n) === 1n;
        if (use) result = result * base % m;
        rows.push(row([bit, use ? '1' : '0', base, use ? result : '—'], use));
        base = base * base % m;
        exp >>= 1n;
        bit += 1;
        if (bit > 64) break;
      }
      out.innerHTML = table(['bit of b', 'value', 'a^(2^bit) mod m', 'running result'], rows);
      k1L.textContent = 'a^b mod m'; k1.textContent = modpow(a, b, m);
      k2L.textContent = 'multiplications'; k2.textContent = rows.length * 2;
      status.innerHTML = '<strong>' + a + '^' + b + ' mod ' + m + ' = ' + modpow(a, b, m) + '</strong>, found in about '
        + (rows.length * 2) + ' multiplications rather than ' + b + '. Reducing mod m at every step is what keeps the '
        + 'numbers small; computing ' + a + '^' + b + ' first would be an integer with thousands of digits.';
    },
    congr: function (a, b, m) {
      show(['A', 'B', 'M']);
      title.textContent = 'Linear congruence';
      sub.textContent = 'ax ≡ b (mod m)';
      if (m < 2n) { out.innerHTML = ''; status.textContent = 'The modulus must be at least 2.'; return; }
      var g = bgcd(((a % m) + m) % m, m);
      var solutions = [];
      if (b % g === 0n) {
        var m2 = m / g, a2 = (a / g) % m2, b2 = (b / g) % m2;
        var inv = modinv(a2, m2);
        if (inv !== null) {
          var x0 = ((b2 * inv) % m2 + m2) % m2;
          for (var i = 0n; i < g; i += 1n) solutions.push((x0 + i * m2) % m);
        }
      }
      var rows = solutions.length
        ? solutions.map(function (x) { return row([x, ((a * x) % m + m) % m, ((b % m) + m) % m, '✓'], true); })
        : [row(['none', '—', ((b % m) + m) % m, 'no solution'], true)];
      out.innerHTML = table(['x', 'ax mod m', 'b mod m', ''], rows);
      k1L.textContent = 'gcd(a, m)'; k1.textContent = g;
      k2L.textContent = 'solutions'; k2.textContent = solutions.length;
      status.innerHTML = solutions.length
        ? 'gcd(a, m) = ' + g + ' divides b, so there are exactly <strong>' + g + '</strong> solutions modulo ' + m
          + ', spaced ' + (m / g) + ' apart. The count is the gcd — not one, and not m.'
        : 'gcd(a, m) = ' + g + ' does <strong>not</strong> divide ' + b + ', so there is <strong>no solution at all</strong>. '
          + 'That is the whole solvability criterion, and it is checkable before any work is done.';
    },
    crt: function (a, b, m) {
      show(['A', 'B', 'M']);
      title.textContent = 'Chinese remainder theorem';
      sub.textContent = 'x ≡ a (mod m), x ≡ b (mod m+1) — two coprime moduli';
      var m1 = m, m2 = m + 1n;
      if (m1 < 2n) { out.innerHTML = ''; status.textContent = 'The modulus must be at least 2.'; return; }
      var r1 = ((a % m1) + m1) % m1, r2 = ((b % m2) + m2) % m2;
      var M = m1 * m2;
      var inv1 = modinv(m2 % m1, m1), inv2 = modinv(m1 % m2, m2);
      var x = ((r1 * m2 % M) * inv1 + (r2 * m1 % M) * inv2) % M;
      var rows = [
        row(['x ≡ ' + r1 + ' (mod ' + m1 + ')', m2, inv1, r1 * m2 * inv1 % M], false),
        row(['x ≡ ' + r2 + ' (mod ' + m2 + ')', m1, inv2, r2 * m1 * inv2 % M], false),
        row(['<strong>x</strong>', '', '', '<strong>' + x + ' (mod ' + M + ')</strong>'], true)
      ];
      out.innerHTML = table(['congruence', 'other modulus', 'its inverse', 'contribution'], rows);
      k1L.textContent = 'x'; k1.textContent = x;
      k2L.textContent = 'modulus'; k2.textContent = M;
      status.innerHTML = 'Consecutive integers are always coprime, so ' + m1 + ' and ' + m2 + ' are, and the theorem '
        + 'applies: <strong>x = ' + x + '</strong>, unique modulo ' + M + '. Check it: ' + x + ' mod ' + m1 + ' = '
        + (x % m1) + ' and ' + x + ' mod ' + m2 + ' = ' + (x % m2) + '.';
    },
    fermat: function (a, b, m) {
      show(['A', 'M']);
      title.textContent = "Fermat's little theorem and Euler's theorem";
      sub.textContent = 'a^(p−1) ≡ 1 (mod p) when p is prime and p ∤ a';
      if (m < 2n) { out.innerHTML = ''; status.textContent = 'The modulus must be at least 2.'; return; }
      var prime = isPrimeBig(m);
      var phi = 0n;
      for (var i = 1n; i < m; i += 1n) if (bgcd(i, m) === 1n) phi += 1n;
      var base = ((a % m) + m) % m;
      var coprime = bgcd(base, m) === 1n;
      var rows = [];
      for (var e = 1n; e <= (m < 14n ? m : 14n); e += 1n) {
        var v = modpow(base, e, m);
        rows.push(row([e, v, v === 1n ? '← 1' : ''], v === 1n));
      }
      out.innerHTML = table(['e', a + '^e mod ' + m, ''], rows);
      k1L.textContent = 'φ(m)'; k1.textContent = phi;
      k2L.textContent = 'a^φ(m) mod m'; k2.textContent = coprime ? modpow(base, phi, m) : 'undefined';
      status.innerHTML = coprime
        ? 'φ(' + m + ') = ' + phi + ' and ' + a + '^' + phi + ' ≡ ' + modpow(base, phi, m) + ' (mod ' + m + '). '
          + (prime
              ? 'Since ' + m + ' is prime, φ(m) = m − 1 and this is Fermat\'s little theorem — the special case.'
              : 'Since ' + m + ' is composite, Fermat does not apply but Euler still does; φ(m) counts the units, not m − 1.')
        : '<strong>gcd(' + a + ', ' + m + ') ≠ 1</strong>, so neither theorem applies: both require a coprime to the modulus, '
          + 'and no power of ' + a + ' can ever be 1 mod ' + m + '.';
    },
    sieve: function (a, b, m) {
      show(['A']);
      title.textContent = 'Sieve of Eratosthenes';
      sub.textContent = 'cross out the multiples of each prime in turn';
      var N = clamp(Number(a), 10, 200);
      var composite = new Array(N + 1).fill(false), killedBy = new Array(N + 1).fill(0);
      for (var p = 2; p * p <= N; p += 1) {
        if (composite[p]) continue;
        for (var q = p * p; q <= N; q += p) if (!composite[q]) { composite[q] = true; killedBy[q] = p; }
      }
      var cells = '';
      var primes = 0;
      for (var i = 2; i <= N; i += 1) {
        if (!composite[i]) primes += 1;
        cells += '<span class="chip' + (composite[i] ? '' : ' ok') + '" title="'
          + (composite[i] ? 'first crossed out as a multiple of ' + killedBy[i] : 'prime') + '">' + i + '</span>';
      }
      out.innerHTML = '<div>' + cells + '</div>';
      k1L.textContent = 'primes ≤ N'; k1.textContent = primes;
      k2L.textContent = 'N'; k2.textContent = N;
      status.innerHTML = 'There are <strong>' + primes + '</strong> primes up to ' + N + '. Sieving stops at √N = '
        + Math.floor(Math.sqrt(N)) + ': any composite has a factor no larger than its square root, so anything still '
        + 'standing after that is prime. Hover a crossed-out number to see which prime removed it.';
    },
    factor: function (a) {
      show(['A']);
      title.textContent = 'Prime factorisation';
      sub.textContent = 'the unique decomposition guaranteed by the fundamental theorem';
      var n = a < 0n ? -a : a;
      if (n < 2n) { out.innerHTML = ''; status.textContent = 'Factorisation is defined for integers greater than 1.'; return; }
      var rows = [], parts = [], left = n, steps = 0;
      for (var d = 2n; d * d <= left; d += 1n) {
        var e = 0n;
        while (left % d === 0n) { left /= d; e += 1n; steps += 1; }
        if (e > 0n) { rows.push(row([d, e, left], false)); parts.push(d + (e > 1n ? '^' + e : '')); }
      }
      if (left > 1n) { rows.push(row([left, 1n, 1n], true)); parts.push(left.toString()); }
      out.innerHTML = table(['prime', 'exponent', 'remaining'], rows);
      k1L.textContent = 'factors'; k1.textContent = parts.length;
      k2L.textContent = 'divisors'; k2.textContent = (function () {
        var count = 1n, m2 = n;
        for (var d2 = 2n; d2 * d2 <= m2; d2 += 1n) {
          var e2 = 0n;
          while (m2 % d2 === 0n) { m2 /= d2; e2 += 1n; }
          if (e2 > 0n) count *= (e2 + 1n);
        }
        if (m2 > 1n) count *= 2n;
        return count.toString();
      })();
      status.innerHTML = '<strong>' + n + ' = ' + (parts.join(' · ') || n) + '</strong>. '
        + 'The fundamental theorem of arithmetic says this decomposition exists and is unique up to order — '
        + 'which is exactly what makes the exponent counting above give the number of divisors.';
    }
  };

  function redraw() {
    var a, b, m;
    try {
      a = BigInt(aIn.value || '0'); b = BigInt(bIn.value || '0'); m = BigInt(mIn.value || '2');
    } catch (e) {
      status.textContent = 'Enter whole numbers.';
      return;
    }
    MODES[modeSel.value](a, b, m);
  }

  [aIn, bIn, mIn].forEach(function (el) { el.addEventListener('input', redraw); });
  modeSel.addEventListener('change', function () {
    var d = DEFAULTS[modeSel.value];
    if (d) { aIn.value = d[0]; bIn.value = d[1]; mIn.value = d[2]; }
    redraw();
  });

  var DEFAULTS = {
    div: [1071, 462, 26], euclid: [1071, 462, 26], bezout: [1071, 462, 26],
    modtable: [3, 5, 12], modexp: [7, 128, 13], congr: [6, 9, 15],
    crt: [2, 3, 5], fermat: [3, 0, 7], sieve: [100, 0, 26], factor: [360, 0, 26]
  };

  modeSel.value = """ + '"%s"' % cfg.get("mode", "euclid") + r""";
  (function () {
    var d = DEFAULTS[modeSel.value];
    if (d) { aIn.value = d[0]; bIn.value = d[1]; mIn.value = d[2]; }
  })();
  """ + (cfg.get("overrides_js") or "") + r"""
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Number theory workbench",
        subtitle="Algorithms with their traces",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose an algorithm"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every mode prints the steps, not only the answer, so the method is "
            "something you can carry to paper.",
        ),
        script=script,
    )


def rsa_lab(cfg):
    """RSA end to end on numbers small enough to check by hand.

    The keys are GENERATED from the primes you choose, the message is actually
    encrypted and decrypted, and the lab shows that d is recoverable by
    factoring n -- which is the honest way to teach why the real thing uses
    primes with hundreds of digits rather than two-digit ones.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>RSA with small primes</strong><span>Key generation, encryption, decryption, and the attack</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>public</span><span class="tone-red"><i class="legend-swatch"></i>private</span></div>
      </div>
      <div class="lab-stage"><div class="table-wrap" id="rsaOut"></div></div>
      <div class="status-banner" id="rsaStatus" style="margin-top:12px;"></div>"""
    controls = """        <div class="field">
          <label for="rsaP">p (prime)</label>
          <input id="rsaP" type="number" value="61" />
        </div>
        <div class="field">
          <label for="rsaQ">q (prime)</label>
          <input id="rsaQ" type="number" value="53" />
        </div>
        <div class="field">
          <label for="rsaE">e (public exponent, coprime to &phi;(n))</label>
          <input id="rsaE" type="number" value="17" />
        </div>
        <div class="field">
          <label for="rsaM">m (message, 0 &le; m &lt; n)</label>
          <input id="rsaM" type="number" value="65" />
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>n = pq</span><strong id="rsaN">&mdash;</strong></div>
          <div class="kpi"><span>&phi;(n)</span><strong id="rsaPhi">&mdash;</strong></div>
          <div class="kpi"><span>d</span><strong id="rsaD">&mdash;</strong></div>
        </div>"""

    script = NT_JS + r"""
  var pIn = document.getElementById('rsaP'), qIn = document.getElementById('rsaQ');
  var eIn = document.getElementById('rsaE'), mIn = document.getElementById('rsaM');
  var out = document.getElementById('rsaOut'), status = document.getElementById('rsaStatus');

  function redraw() {
    var p, q, e, m;
    try {
      p = BigInt(pIn.value || '0'); q = BigInt(qIn.value || '0');
      e = BigInt(eIn.value || '0'); m = BigInt(mIn.value || '0');
    } catch (err) { status.textContent = 'Enter whole numbers.'; return; }

    if (!isPrimeBig(p) || !isPrimeBig(q)) {
      out.innerHTML = '';
      status.innerHTML = '<strong>p and q must both be prime.</strong> '
        + (isPrimeBig(p) ? q + ' is not.' : p + ' is not.')
        + ' RSA rests on φ(n) = (p−1)(q−1), and that formula is only correct for two distinct primes.';
      return;
    }
    if (p === q) {
      out.innerHTML = '';
      status.innerHTML = '<strong>p and q must be different.</strong> With p = q, φ(n) = p(p−1), not (p−1)², '
        + 'and n = p² is trivially factorable by taking a square root.';
      return;
    }
    var n = p * q, phi = (p - 1n) * (q - 1n);
    if (bgcd(e, phi) !== 1n) {
      out.innerHTML = '';
      status.innerHTML = '<strong>e = ' + e + ' is not coprime to φ(n) = ' + phi + '</strong> (their gcd is '
        + bgcd(e, phi) + '), so e has no inverse mod φ(n) and no decryption exponent exists. '
        + 'Try 17, or any prime that does not divide ' + phi + '.';
      return;
    }
    var d = modinv(e, phi);
    if (m < 0n || m >= n) {
      out.innerHTML = '';
      status.innerHTML = '<strong>The message must satisfy 0 ≤ m &lt; n = ' + n + '.</strong> '
        + 'Anything larger is indistinguishable from m mod n after encryption — which is why real messages '
        + 'are split into blocks smaller than the modulus.';
      return;
    }

    var c = modpow(m, e, n), back = modpow(c, d, n);

    /* The attack, run for real: factor n by trial division, recompute phi,
       recompute d. On these primes it takes microseconds, and that is the
       point being made. */
    var t0 = (typeof performance !== 'undefined' && performance.now) ? performance.now() : 0;
    var f = 0n;
    for (var t = 2n; t * t <= n; t += 1n) if (n % t === 0n) { f = t; break; }
    var t1 = (typeof performance !== 'undefined' && performance.now) ? performance.now() : 0;
    var recovered = f ? modinv(e, (f - 1n) * (n / f - 1n)) : null;

    var rows = [
      ['p, q', p + ', ' + q, 'private — the only secret that matters'],
      ['n = pq', n.toString(), 'public'],
      ['φ(n) = (p−1)(q−1)', phi.toString(), 'private (computable from p and q)'],
      ['e', e.toString(), 'public, coprime to φ(n)'],
      ['d = e⁻¹ mod φ(n)', d.toString(), 'private; check: ed mod φ(n) = ' + (e * d % phi)],
      ['message m', m.toString(), ''],
      ['ciphertext c = mᵉ mod n', c.toString(), 'what an eavesdropper sees'],
      ['decrypted cᵈ mod n', back.toString(), back === m ? 'matches m' : 'DOES NOT match m']
    ];
    out.innerHTML = '<table class="tt"><thead><tr><th>quantity</th><th>value</th><th>role</th></tr></thead><tbody>'
      + rows.map(function (r, i) {
          return '<tr' + (i === 7 ? ' class="focus"' : '') + '><td>' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td></tr>';
        }).join('') + '</tbody></table>';

    document.getElementById('rsaN').textContent = n;
    document.getElementById('rsaPhi').textContent = phi;
    document.getElementById('rsaD').textContent = d;

    status.innerHTML = (back === m
      ? 'Decryption returned the original message, and it did so because of Euler\'s theorem: '
        + 'ed ≡ 1 (mod φ(n)) makes m^(ed) ≡ m (mod n). '
      : '<span class="tone-red">Decryption did not return m.</span> ')
      + '<br /><strong>Now the attack.</strong> This lab factored n = ' + n + ' by trial division in '
      + (f ? Math.max(0.001, (t1 - t0)).toFixed(3) + ' ms, finding p = ' + f + ', and recomputed d = ' + recovered
          + ' — the private key, from public information alone.' : 'no time at all.')
      + ' Nothing about the method resists that; only the SIZE of the primes does. Production keys use primes of '
      + 'about 1024 bits each, where the same trial division would outlast the universe.';
  }

  [pIn, qIn, eIn, mIn].forEach(function (el) { el.addEventListener('input', redraw); });
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="RSA, generated and broken",
        subtitle="Small enough to check by hand",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose the primes"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every value below is computed from the four inputs. The last paragraph "
            "recovers the private key by factoring, because that is the honest way "
            "to show what the security actually rests on.",
        ),
        script=script,
    )
