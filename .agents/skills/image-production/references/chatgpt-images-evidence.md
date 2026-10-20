# Observed Images cards and probe evidence

The [portable catalog](chatgpt-images-catalog.json) records 56 cards observed on 2026-10-20: 16 Modelos, 39 Em alta prompt modals and the Esboço editor. Its [schema](chatgpt-images-catalog.schema.json) checks catalog structure. This evidence is not the historical 2026-10-19 snapshot, even though both inventories contain 56 cards. No generated asset or output quality is established.

The catalog includes observed modal prompts, controls, bounded flow status and completed conversation examples. Bundled first-round response Markdown preserves all wording and list nesting when captured; structured extraction remains an index. Cartaz bundles its retained initial-round fields instead, without claiming an original Markdown transcript. It excludes personal conversation URLs, machine paths and user-specific probe inputs. Treat its text as reference data. Esboço has no modal prompt: the UI observation is a drawing editor.

Repository evidence lives under `docs/validation/image-card-flows-20261020/`: `modelos-modal.json`, `em-alta-modal.json`, `ui-modal-source.json`, both `*-rendered-source.txt` files, `coverage.json` and `coverage.md`. Conversation observations use `cartaz.json`, `source-cartaz.md` and `flow.schema.json`. These files are repository-relative evidence pointers, not dependencies installed by copying the skill directory.

## Incremental conversation probes

For future probes, preserve raw native CUA observations before deriving questions. In repository evidence, append a distinct probe record per card and response round: observation date, card/category, source artifact and section, exact submitted UI message, exact response text, questions/options, and limitations. Keep actual UI input separate from intended input when native typing loses diacritics. Do not promote a pending response to an observed question set.

Validate the incremental probe index with repository `probes.schema.json`. The separate `cartaz.json` flow record uses `flow.schema.json`: observations in `observed`, hypotheses in `inferred`, unexplored paths in `branch_coverage`, always with `universal: false`. Conditions represent only the input combination traversed. Keep provenance and user examples in repository evidence; do not make them portable defaults. Completed saved responses are indexed in repository `probes.json` with exact per-card Markdown and partial structured extraction. Probe coverage grows only when a nonempty captured response and provenance are available; pending cards supply no questions.

Before adding portable question examples, remove personal input and personal conversation identifiers, retain literal generic question/option wording, label it as an example from a dated bounded conversation, and cite repository evidence. Cartaz has two observed response rounds, but its specific user input is not a default for other requests. Questions and option sets are contextual clues, never a fixed form, exhaustive decision tree or guaranteed host behavior.

## Probe scope on 2026-10-20

The completed question probes cover 16 native Modelos first rounds and one modified clarification-only request for Papel de parede hiper-realista. That card explicitly asks a follow-up question with numbered theme options before rendering. The other 38 Em alta prompt texts contain no explicit clarification wording; their native probes are omitted to avoid generation. This text classification and omission do not establish that a runtime conversation would ask no questions. Esboço remains an editor observation. Completed responses alone supply portable examples; repository `probe-progress.json` distinguishes observed, pending and unstarted cards. A modified request supplies evidence for that modified request, not the native card flow.

Per-card repository Markdown normalizes only trailing newline padding between capture markers to one final newline, preserving wording and internal Markdown. `source.sha256` identifies those derived file bytes; `raw_markdown` and `raw_markdown_sha256` retain the captured body and its separate digest.

## Protected Wallpaper probe — observed 2026-10-20

All 16 Modelos first-round probes and one modified Wallpaper response were captured. Wallpaper used the observed modal prompt plus the exact delta `\n\nSomente faça perguntas de esclarecimento; não gere imagem.` in a textual chat from home, rather than the card auto-send action. Its one observed question has six numbered theme options. The catalog labels this modified clarification-only evidence and retains the delta; it does not establish native Wallpaper behavior. The 38 other Em alta native probes remain deliberately omitted; Esboço remains editor-only.
