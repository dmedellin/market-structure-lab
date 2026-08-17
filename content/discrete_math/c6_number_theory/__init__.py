"""Course 6 — Number Theory and Cryptography."""

from . import part_a, part_b

COURSE = {
    "slug": "number-theory-and-cryptography",
    "title": "Number Theory and Cryptography",
    "level": "Intermediate",
    "summary": (
        "The arithmetic of remainders, from the division algorithm to RSA: primes and "
        "unique factorisation, gcd and the Euclidean algorithm, Bézout's identity, "
        "modular arithmetic and exponentiation, linear congruences, the Chinese "
        "remainder theorem, Fermat and Euler, and public-key encryption."
    ),
    "blurb": (
        "Everything follows from one theorem about division with remainder. Primes, "
        "gcds, congruences and modular inverses build up to RSA &mdash; which is "
        "generated, used and then broken here on primes small enough to check by hand."
    ),
    "key": [
        "a = qb + r,  0 ≤ r < b            unique q and r",
        "gcd(a,b) = ax + by                Bézout",
        "a^{p−1} ≡ 1 (mod p)               Fermat, for prime p ∤ a",
        "ed ≡ 1 (mod φ(n))  ⟹  m^{ed} ≡ m  (mod n)     RSA",
    ],
    "assumes_short": "Courses 1–3",
    "assumes_long": "proof technique and induction",
    "outcomes_intro": (
        "By the end you can compute in modular arithmetic confidently and explain "
        "exactly what RSA's security rests on."
    ),
    "outcomes": [
        ("Run the algorithms by hand",
         "Division, Euclid, extended Euclid, fast exponentiation. Each with its trace, "
         "so the method transfers to paper."),
        ("Solve congruences",
         "Decide solvability, count the solutions, and find them &mdash; including "
         "simultaneous systems by the Chinese remainder theorem."),
        ("Use Fermat and Euler",
         "Reduce enormous exponents to small ones, and know exactly which hypotheses "
         "each theorem needs."),
        ("Explain RSA honestly",
         "Generate a key, encrypt and decrypt, and then recover the private key by "
         "factoring &mdash; which is what shows what the security actually depends on."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 6 are divisibility and gcd, 7 to 11 are modular arithmetic, and "
        "12 to 14 apply all of it."
    ),
    "how_to": [
        "Use the workbench lab in every lesson. Each mode prints the algorithm's trace "
        "rather than only its answer, and the point is to be able to reproduce the "
        "trace on paper afterwards.",
        "Do the RSA lesson with the primes it starts with, then change them. Watching "
        "the key change and the ciphertext change with it is what makes the mechanism "
        "concrete.",
        "Take the factoring demonstration in lesson 14 seriously. The lab breaks the "
        "key it just generated, and understanding why that is easy here and hard in "
        "practice is the whole security argument.",
    ],
    "not_covered": [
        "Analytic number theory: the prime number theorem is quoted in lesson 3 and not "
        "proved, and the Riemann hypothesis is mentioned only as context.",
        "Elliptic curves, discrete logarithms and Diffie&ndash;Hellman. RSA is the one "
        "public-key system developed here.",
        "Cryptographic engineering: padding schemes, key management, side channels and "
        "protocol design. Lesson 14 is the mathematics of RSA, and textbook RSA is not "
        "a system anyone should deploy.",
    ],
    "footer_lead": (
        "All arithmetic on this course is exact big-integer arithmetic, because modular "
        "exponentiation with four-digit moduli already exceeds what floating point can "
        "represent. The RSA lab generates a real key, uses it, and then recovers the "
        "private key by factoring &mdash; on primes chosen small enough that it takes "
        "microseconds."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
