# Run contract (independent review and stable asset lineages)

Helper: `scripts/inspect_artifacts.py`, Python >=3.10 and Pillow >=10,<13. A successful command prints one JSON object to stdout and exits 0. Invalid input prints one JSON object `{"error": "..."}` to stderr, prints nothing to stdout, and exits 2. That includes argument-parsing failures: missing required flags, invalid choices, unknown subcommands and unrecognized arguments. Those failures do not print argparse usage text. `--help` stays plain text and exits 0. No network access, SDK, image generation, conversion or API fallback. Paths in command arguments are literal paths, never shell fragments. Quote paths; do not interpolate brief text into shell code.

## Prepare

Create a JSON file with this shape (values below are synthetic examples):

```json
{
  "purpose": "Product cutout for an internal sample",
  "audience": "Internal reviewers",
  "intended_use": "Catalog preview",
  "use_case": "product-mockup",
  "variants": 1,
  "text": "",
  "constraints": ["One blue ceramic mug; no logo"],
  "acceptance": ["Mug fully visible", "Transparent background"],
  "transparent": true,
  "brand_kit": null,
  "references": []
}
```

`variants` is a positive integer (max 20 per run); `text` is verbatim. `brand_kit` is null or an absolute existing file path. References are objects with absolute `path` and `role` from reference/edit-target/insert/brand-kit. Existing inputs are copied into `inputs/` and hashed; never modified. A supplied brand kit automatically adds a brand-kit reference. Image references must decode. Omit brand only deliberately. Review always requires brand_reference if a brand kit or reference exists, text_facts if text exists, preservation if an edit-target exists and transparency if requested.

```text
python <script> prepare --root <output-directory> --brief <brief.json> --surface desktop --cli-version 0.163.0 --asset-key catalog-hero
```

`--surface` is desktop or exec. Pass the version actually observed; omit if unknown. Creates a unique UUID run below the chosen root with `inputs/`, `work/`, `final/` and `manifest.json`. Root and existing ancestors must not be symlinks or contain `..`. The root is an explicitly selected output location; the tool does not enforce a machine-wide directory allowlist.

## Reserve an attempt before generation

`prepare` requires one unique `--asset-key` per requested variant. Keys are stable logical identifiers, not paths: an ASCII letter or digit followed by up to 79 ASCII letters/digits/underscores/hyphens. Repeat the flag for multiple variants. Assign each key once and keep it for the same logical asset, even when the prompt, brief or references change. Missing keys produce a JSON error explaining the new contract; there is no automatic fresh identity or counter reset.

A successful `prepare` reserves the initial attempt in the chosen root's `.lineages/<hash-of-key>.json` **before imagegen may be called**. Its JSON result returns `assets`, with `asset_key` and `attempt` (0 for initial, 1 or 2 for corrections), plus `review_policy`. Each key permits an initial attempt and two corrections total across all child runs. Canceled, abandoned or interrupted reservations consume the budget conservatively; no automatic refund occurs. Reserving is bookkeeping, not generation or permission beyond the user's request.

For a correction, use the same root and continue the latest attempt:

```text
python <script> prepare --root <same-output-directory> --brief <correction-brief.json> --surface desktop --continue-from <latest-run-directory>
```

Omit `--asset-key` to inherit all keys; the new brief's `variants` must match their count. To correct only one variant, supply its existing `--asset-key` and set `variants` to 1. Multiple selected existing keys are allowed; their count must equal `variants`. Other variants are not debited. Foreign or renamed keys, a different output root, an older parent run, and a fourth attempt are rejected before generation. A fresh `prepare` with an existing key also fails; use continuation rather than starting another initial attempt. Unchanged output bytes still consume an attempt and require new independent reports in the new run.

The ledger is private and atomically replaced by the coordinator. Preserve the entire output root, including `.lineages`, when moving or resuming executions. Copying a run directory alone does not preserve proof of its budget and causes verification/continuation to fail. One coordinator is the only writer; multi-file crashes may consume a reservation without a completed manifest. Inspect and record such failures instead of deleting ledger entries to regain budget. The helper cannot infer that a deliberately renamed asset key or different root describes the same real asset; this is local bookkeeping, not an attestation against an editor able to rewrite history.

## Collect

Save the submitted prompt in a UTF-8 file, then:

```text
python <script> collect --run <run-directory> --source <returned-image> --prompt <submitted-prompt.txt> --name mug --asset-key catalog-hero
```

Names accept ASCII letters/digits/underscores/hyphens (1–80 chars). Select a key reserved in this run with `--asset-key`; it may be omitted only for a single-variant run. One reservation allows exactly one collected candidate; repeated collection fails without changing the manifest or overwriting files. A correction needs a new `prepare --continue-from` reservation before generation. The source and previous candidates remain intact. Filename collisions use `final/mug.png`, `final/mug-v2.png`, etc. with exclusive creation, including collisions with untracked files from interrupted writes. Extension comes from decoded PNG/JPEG/WebP format, not the input suffix. Only single-frame raster images are supported.

Each collection stores the candidate's `asset_key`, independent prompt snapshot/hash, metadata and empty role-review map. Exact UTF-8 prompt bytes, including line endings, are preserved. Collection consumes the run/key reservation once; identical bytes do not bypass this rule. A crash between ledger consumption and manifest replacement can leave an untracked candidate or a consumed reservation; do not automatically refund or recollect. Candidates are not automatically approved. Each run covers only its reserved variants, and approval applies only to those candidates. Parent runs and their review records remain historical; a child's approval does not approve other, unselected variants.

Transparency requires real nonempty alpha and visible pixels; all-transparent files fail. Dimensions and bytes are reported, not resized. File integrity is rechecked before review and on `verify`.

## Review

Provide exactly these seven keys under `criteria`: objective, text_facts, composition, brand_reference, visual_integrity, preservation, transparency. Each value is `{"score": 2, "evidence": "Observed evidence"}`; score is 0/1/2 or `"na"` with a reason. Require reviewer name and no empty evidence.

```text
python <script> review --run <run-directory> --asset mug.png --review <review.json>
python <script> verify --run <run-directory>
python <script> status --run <run-directory> --state blocked --reason "Integrated tool unavailable in this session"
```

Submit two separate JSON reports, one per independent reviewer:

```json
{"reviewer":"technical-worker-id","role":"technical","candidate_sha256":"<current metadata SHA256>","criteria":{}}
```

Replace the empty `criteria` example with all seven entries described above. The second report uses `role: "visual"` and a distinct reviewer identifier. Both roles must inspect and provide evidence for all applicable criteria; technical metadata alone cannot establish visual fidelity. A missing role, a combined role, the wrong candidate hash, or the same reviewer for both roles cannot approve the candidate. Reports stay separately persisted under `outputs[].reviews.technical` and `.visual`, each bound to the candidate's current SHA256. Replacing one role's report preserves the other role, records the previous latest report in `review_history`, and recomputes approval from both current reports. `outputs[].review` is the latest received report for backward-compatible display; it is not the approval authority.

Scores are reviewer assertions, not algorithmically established truth or proof that distinct labels represent distinct humans/processes. Core objective/composition/visual_integrity cannot be na. Other criteria are critical when applicable. Both current reports must score every applicable criterion 2, and every reserved variant must have its candidate and complete pair, before the run is approved. `status` only accepts blocked/failed; it cannot force approval. Re-collect/review resumes processing.

Manifest includes schema_version, run_id, UTC timestamps, surface, observed CLI version, mode=built-in, brief, input snapshots, outputs with prompt/metadata/review/reviews/asset_key, state and error. New manifests also record `review_policy=independent-dual-role-v1`, `attempt_policy=stable-asset-lineage-v1` and `assets` reservations. Loading checks that state, the brief fields later commands read (`text`, `variants`, `transparent`), and each input/output record have the expected shape. The variants range remains 1–20 on resume. Snapshot paths must be nonempty relative paths without parent traversal or null bytes; normalized output paths must be unique. Stored non-null reviews and every review-history entry must satisfy the same reviewer, seven-criterion, evidence and applicability requirements as a new review. History may be absent, but must be an array when present; null entries are invalid. An `approved` state must agree with the number of unique output records and the applicable review policy. Reserved runs require the independent dual-role policy and cannot downgrade to legacy approval. Each reserved key may appear only once in outputs. Verification also checks the root ledger and reservation/candidate hash association. Invalid stored data fail with the standard JSON error before any write, including `status`. Extra fields are preserved. Loading does not require the original reference files to still exist; snapshots in `inputs/` are the resume source. `verify`, `collect` and `review` confirm snapshot hashes, prompt hashes, and current output metadata before proceeding. `status` validates the manifest but deliberately does not require intact artifacts, so it can record a missing/corrupt-file failure. The manifest is local bookkeeping, not a signed attestation against an editor able to rewrite both data and evidence. Do not use this manifest as `codex exec --output-schema`; use the compact [result schema](result.schema.json) for a final session report. Events from `--json` remain JSONL. The manifest `state` vocabulary is the same enum as that result schema.

## Historical manifests

Manifests created before these policies remain readable and verifiable under `legacy-single-review-historical`; `verify` explicitly labels that policy in its result instead of presenting it as dual review. Historical approval is not retroactively converted into independent approval. The first new `review` requires a valid role/hash report, preserves old reports in history, clears current reviews for every candidate and migrates the entire run to the dual-role gate. It remains unapproved until each candidate receives its new independent pair.

Legacy manifests have no stable asset reservation ledger. `collect` and automatic continuation from them are blocked with a migration/audit explanation; the helper cannot reconstruct unknown historical correction attempts or silently reset their budget. Audit the existing history before establishing any new lineage, and preserve the legacy artifacts. Re-reviewing an existing legacy candidate does not authorize regeneration.

Local path confinement assumes a trusted local filesystem and one writer; it rejects symlinks at access time but is not an OS sandbox against a hostile process racing directory replacement. Relative paths stored in the manifest must be non-empty and stay inside the run. Confinement failures report a short error and do not include absolute paths. Atomic manifest replacement preserves the previous version if serialization fails and leaves the manifest owner-readable only. A crash between writing candidate bytes and manifest update can leave an untracked candidate; inspect before resuming, never auto-delete it. A crash during replacement can also leave a `.manifest-*.tmp` file; ignore it and do not treat it as a candidate.
