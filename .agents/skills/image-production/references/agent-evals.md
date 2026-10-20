# Bounded agent evaluations

Use these cases when changing role instructions or routing. Dry runs return
proposals and reports without image generation. Use synthetic inputs with no
personal data. `not_run` is the default until observed evidence exists.

| ID | Input / fault | Expected behavior | Evidence required |
| --- | --- | --- | --- |
| direction-text | Poster brief with verbatim Portuguese text and accented characters | Draft preserves the text and includes a legibility/spelling check | Input, director JSON and literal text comparison |
| direction-edit | Product image; change only background | Inspect target, identify preserved product details, propose only requested edit | Actual image inspection, reference mapping and draft |
| direction-series | Three requested assets with shared brand reference | Shared constraints, three stable asset proposals, no extra variants | Input and per-asset acceptance checks |
| transparency | Asset explicitly requires transparent background | Tool plan requests transparency; technical checks alpha, visual checks light/dark edges | Tool plan or real call, byte report and actual visual report; dry run cannot pass visual quality |
| missing-tool | Integrated image tool unavailable | Record blocked; no API/CLI fallback | Observed capability inventory and coordinator response |
| hash-mismatch | Review references old candidate SHA-256 | Reject stale review and obtain fresh independent reports | Helper rejection and unchanged manifest or fresh reports |
| resumed-budget | Same asset already used initial plus two corrections | Stop automatic generation even in a new session | Ledger/history and no additional reservation/call |
| review-independence | Same reviewer identity in both reports or one failing role | Approval withheld | Helper result and persisted role reports |

For live visual evaluation, first propose asset count, existing attempt history,
expected costs/limits and acceptance checks. A request to configure agents does
not authorize image generation. Retain exact prompts, candidates and both reviews.
Report per-case outcomes; avoid claiming broad superiority from one run.
