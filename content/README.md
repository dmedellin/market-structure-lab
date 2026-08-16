# Course source manifests

Authoritative titles and descriptions for each course, as shipped with the
original lesson packages. The course home pages and every lesson's meta
description are derived from these.

They live here because the packages arrived in `~/.hermes/tmp/`, which is not
durable — a cleanup there would otherwise destroy the only record of the
intended copy. These are provenance, not build inputs; nothing reads them at
runtime.

  market-structure.manifest.json       Course 1, labs 02-07 (lab 01 predates the manifest)
  trade-setup-execution.manifest.json  Course 2, all 15 lessons
  options-trading.manifest.json        Course 3, all 16 lessons
  technical-indicators.manifest.json   Course 4, all 16 lessons

The file name matches the course's URL slug. Course 1's manifest was named
market-structure-lab.manifest.json while the course was published under that
prefix; the course now lives at /market-structure/ and the manifest follows it.
