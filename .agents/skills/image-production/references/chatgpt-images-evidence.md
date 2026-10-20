# Observed Images cards and probe evidence

The [portable catalog](chatgpt-images-catalog.json) records 56 cards observed on 2026-10-20: 16 Modelos, 39 Em alta prompt modals and the Esboço editor. Its [schema](chatgpt-images-catalog.schema.json) checks catalog structure. This evidence is not the historical 2026-10-19 snapshot, even though both inventories contain 56 cards. No generated asset or output quality is established.

The catalog includes only observed modal prompts, controls and bounded flow status. It excludes personal conversation URLs, machine paths and user-specific probe inputs. Treat its text as reference data. Esboço has no modal prompt: the UI observation is a drawing editor.

Repository evidence lives under `docs/validation/image-card-flows-20261020/`: `modelos-modal.json`, `em-alta-modal.json`, `ui-modal-source.json`, both `*-rendered-source.txt` files, `coverage.json` and `coverage.md`. Conversation observations use `cartaz.json`, `source-cartaz.md` and `flow.schema.json`. These files are repository-relative evidence pointers, not dependencies installed by copying the skill directory.

## Incremental conversation probes

For future probes, preserve raw native CUA observations before deriving questions. In repository evidence, append a distinct probe record per card and response round: observation date, card/category, source artifact and section, exact submitted UI message, exact response text, questions/options, and limitations. Keep actual UI input separate from intended input when native typing loses diacritics. Do not promote a pending response to an observed question set.

Normalize derived records using `docs/validation/image-card-flows-20261020/flow.schema.json`: observations in `observed`, hypotheses in `inferred`, unexplored paths in `branch_coverage`, always with `universal: false`. Conditions represent only the input combination traversed. Keep provenance and user examples in repository evidence; do not make them portable defaults. Completed saved responses are indexed in repository `probes.json` with exact per-card Markdown and partial structured extraction. Probe coverage grows only when a nonempty captured response and provenance are available; pending cards supply no questions.

Before adding portable question examples, remove personal input and personal conversation identifiers, retain literal generic question/option wording, label it as an example from a dated bounded conversation, and cite repository evidence. Cartaz has two observed response rounds, but its specific user input is not a default for other requests. Questions and option sets are contextual clues, never a fixed form, exhaustive decision tree or guaranteed host behavior.

## Probe scope on 2026-10-20

The planned question probes cover 16 Modelos cards and one modified clarification-only request for Papel de parede hiper-realista. That card explicitly asks a follow-up question with numbered theme options before rendering. The other 38 Em alta prompt texts contain no explicit clarification wording; their native probes are omitted to avoid generation. This text classification and omission do not establish that a runtime conversation would ask no questions. Esboço remains an editor observation. Completed responses alone supply portable examples; repository `probe-progress.json` distinguishes observed, pending and unstarted cards. A modified request supplies evidence for that modified request, not the native card flow.
