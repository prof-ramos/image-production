# Run contract (v1)

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
python <script> prepare --root <output-directory> --brief <brief.json> --surface desktop --cli-version 0.163.0
```

`--surface` is desktop or exec. Pass the version actually observed; omit if unknown. Creates a unique UUID run below the chosen root with `inputs/`, `work/`, `final/` and `manifest.json`. Root and existing ancestors must not be symlinks or contain `..`. The root is an explicitly selected output location; the tool does not enforce a machine-wide directory allowlist.

## Collect

Save the submitted prompt in a UTF-8 file, then:

```text
python <script> collect --run <run-directory> --source <returned-image> --prompt <submitted-prompt.txt> --name mug
```

Names accept ASCII letters/digits/underscores/hyphens (1–80 chars). Extension comes from decoded PNG/JPEG/WebP format, not the input suffix. Only single-frame raster images are supported. `final/mug.png`, `final/mug-v2.png`, etc. are created exclusively; original source and previous files remain intact. Outputs are candidates, not automatically approved. Each collect stores an independent prompt snapshot and hash. New candidates invalidate run approval. Remove/reselect candidates manually only with explicit intent; v1 expects one collected final candidate per requested variant. Extra corrective candidates may be retained as separate runs when the desired variant count is already reached.

Transparency requires real nonempty alpha and visible pixels; all-transparent files fail. Dimensions and bytes are reported, not resized. File integrity is rechecked before review and on `verify`.

## Review

Provide exactly these seven keys under `criteria`: objective, text_facts, composition, brand_reference, visual_integrity, preservation, transparency. Each value is `{"score": 2, "evidence": "Observed evidence"}`; score is 0/1/2 or `"na"` with a reason. Require reviewer name and no empty evidence.

```text
python <script> review --run <run-directory> --asset mug.png --review <review.json>
python <script> verify --run <run-directory>
python <script> status --run <run-directory> --state blocked --reason "Integrated tool unavailable in this session"
```

Review JSON: `{"reviewer":"Codex visual inspection","criteria":{...}}`. Scores are reviewer assertions, not algorithmically established truth. Core objective/composition/visual_integrity cannot be na. Other criteria are critical when applicable. All applicable scores must be 2 to approve; variants count must match. `status` only accepts blocked/failed; it cannot force approval. Re-collect/review resumes processing.

Manifest includes schema_version, run_id, UTC timestamps, surface, observed CLI version, mode=built-in, brief, input snapshots, outputs with prompt/metadata/review, state and error. Loading checks that state, the brief fields later commands read (`text`, `variants`, `transparent`), and each input/output record have the expected shape. Extra fields are preserved. Loading does not require the original reference files to still exist; snapshots in `inputs/` are the resume source. `verify` confirms snapshot hashes, prompt hashes, and current output metadata; malformed/missing/tampered files fail before any write. Do not use this manifest as `codex exec --output-schema`; use the compact [result schema](result.schema.json) for a final session report. Events from `--json` remain JSONL. The manifest `state` vocabulary is the same enum as that result schema.

Local path confinement assumes a trusted local filesystem and one writer; it rejects symlinks at access time but is not an OS sandbox against a hostile process racing directory replacement. Relative paths stored in the manifest must be non-empty and stay inside the run. Confinement failures report a short error and do not include absolute paths. Atomic manifest replacement preserves the previous version if serialization fails and leaves the manifest owner-readable only. A crash between writing candidate bytes and manifest update can leave an untracked candidate; inspect before resuming, never auto-delete it. A crash during replacement can also leave a `.manifest-*.tmp` file; ignore it and do not treat it as a candidate.
