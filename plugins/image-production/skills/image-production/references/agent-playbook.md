# Reusable specialist routing

The four production roles remain required. `image_director` and
`image_eval_designer` are optional specialists; load only when their branch applies.
The root coordinator owns dispatch, memory and final reconciliation. Workers return
reports to it and do not recursively spawn workers. Across the whole run, retain
at most two active workers and one image generation, respecting smaller host caps.

| Trigger | Role | Completion evidence |
| --- | --- | --- |
| Complex composition, multiple references, series or selective edit | `image_director` | Brief, reference mapping, draft prompt and requirement-to-check mapping |
| Reserved asset ready for generation | `image_producer` | Actual output path, exact submitted prompt and hash |
| Collected candidate | `image_technical` + `image_visual` | Independent reports for the same candidate hash under the existing rubric |
| Workflow change, regression, quality experiment | `image_eval_designer` | Bounded cases, observed evidence, skipped checks and limitations |

For a straightforward brief, the coordinator performs preparation directly.
For a complex brief, finish direction before reserving an attempt. The coordinator
resolves indispensable product questions, prepares the run, then dispatches the
producer. An evaluation specialist is not a third asset reviewer and cannot
replace either required report or relax its criteria.

Dispatch includes role definition path, brief/source paths, stable asset key,
assigned task, permitted output location, available tools, prior attempts and
expected report. Review dispatch additionally includes candidate path and SHA-256.
Workers can write assigned report files only; coordinator alone mutates run state.
Keep draft prompts distinct from the exact tool-submitted prompt.

Prefer native roles. When native dispatch is unavailable but its TOML exists, read it and pass the full
`developer_instructions` to a generic worker, recording `explicit-load` and the
definition path. Validate each optional role only when selected. Missing optional
roles do not block the four-role workflow: the coordinator performs optional work
directly if its definition is missing. Files and successful generic delegation
do not prove native discovery. Follow the skill's portability rules; the plugin
does not install project `.codex/agents` definitions.

All roles inherit the selected session model. The reasoning model coordinating a
run and the integrated image generator are separate capabilities: do not promise
a particular image backend from a chat model name. Use the live image tool's
supported parameters; API examples are conceptual guidance, not tool arguments.

## Prompt practice

Specify concrete visual relationships and exact text. Identify each reference's
purpose and the details to preserve during an edit. Start with a clear composition
and make targeted changes when a review identifies a defect. Do not append
unrequested style constraints or convert draft alternatives into extra generated
variants. Preserve the original request, output lineage and correction limit.

Sources consulted 2026-10-20:
[OpenAI image prompting](https://developers.openai.com/api/docs/guides/image-prompting)
and [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
These sources inform prompts and role configuration; project contracts govern
this integrated workflow.
