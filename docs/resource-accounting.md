# Execution accounting

The resource intake was performed once before scientific work. It found a four-core entitlement, a 4-GiB memory limit, no configured swap, and sufficient writable space. Scientific phase execution was sequential with one worker. No stress test, GPU, external compute, remote model/API, live scan, or private data was used.

## Retained instrumented executions

| Execution | Logical checks | Process CPU seconds | Peak RSS KiB | Evidence |
|---|---:|---:|---:|---|
| Abstract intake | 19590 | 0.019609229 | 92464 | results/intake-abstract.json |
| Retained end-to-end intake | 216 query equalities + 6 negative controls | 0.000776562 | 94124 | results/intake-e2e.json |
| Reference campaign | 82644 | 11.582585051 | 115120 | results/reference/runtime-summary.json |
| Final clean reproduction | 82644 | 11.231944165 | 115248 | results/clean/runtime-summary.json |

The two complete executions therefore contribute 165,288 counted logical-obligation evaluations. Including the retained abstract and end-to-end intake gives 185,100. An earlier preliminary scaling pass contributed 564 reported obligations before the encoding-matched comparison repair, for a known subtotal of 185,664. Those superseded timings are not used as scientific performance evidence. Development included additional short pilot attempts and regressions; not every transient attempt has a retained per-attempt counter or CPU record. Accordingly, 185,664 is a **known subtotal**, not a falsely exact cumulative-development count. The retained complete-run CPU values are likewise not a whole-development timing claim.

The final focused regression execution passed 29 tests in 0.019 seconds: 16 interface/contract tests and 13 extremal-construction tests (`results/clean/unit-tests.txt`). These reuse the included input inventory. Tests, timing calls, parsed records, and logical equality assertions are distinct units. Each scaling cut has 2,560 timed query calls; those repetitions are not new cases and are not individually counted as correctness assertions. The full-run logical-obligation counter includes the comparisons actually performed.

## Enforced limits and closure

Each scientific phase sets a 2,500,000,000-byte address-space limit, a 100-second CPU limit, a 120-second wall timeout, and one-core affinity. A whole run refuses more than 85,000 logical checks. Both complete executions have 21 phases and passed within these limits; their combined retained process CPU is 22.814529216 seconds. The input inventory is fixed at 997 entries, with at most 2,000 provenance records per included case. Inputs are generated locally, not downloaded datasets; no scholarly PDF is required or redistributed.

The frozen campaign contains 82,644 distinct programmed obligations, below the 200,000-obligation design ceiling. The clean execution repeats the same obligations for reproducibility rather than enlarging the scientific case set. No additional full scientific campaign is needed unless semantics or implementation changes. A changed theorem, checker, engine, generator, or raw result would require a separately recorded repair and recheck; prose-only packaging changes do not authorize new result claims.

Source downloads and typesetting activity were not fully byte/CPU-metered across all transient browser attempts. The delivered project and exact generated inputs fit the package bounds, but no invented exact total-download or total-development CPU certificate is supplied. This accounting limitation does not alter the exact semantic outcome counts, and it remains an explicit nonclaim.
