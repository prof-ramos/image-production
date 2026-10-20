# Specialist installation and portability

Read when installing or moving the coordinated workflow to another project.
The plugin packages the skill and references; project agent definitions require
separate configuration.

Copying this skill alone does not install the role definitions in the source repository's `.codex/agents/`. See the repository README and `.codex/config.toml` example. Copy the skill and role files into the target project without overwriting existing directories or files; resolve collisions manually. Manually merge the four `[agents.image_coordinator]`, `[agents.image_producer]`, `[agents.image_technical]`, and `[agents.image_visual]` sections into the host's configuration, each with `config_file = "agents/<name>.toml"` relative to that configuration file. Never automate the merge or replace the configuration. Preserve local model, authentication, sandbox, comments, roles, and a lower existing `agents.max_threads`; never increase the cap for installation. Current agents.max_concurrent_threads_per_session excludes the primary session; max_threads is a legacy alias. The protocol permits at most two workers and obeys any lower host cap. Confirm the reviewed project is trusted by Codex: untrusted projects skip project .codex layers. Do not reduce sandbox or approvals to enable discovery. Start a new session and check native discovery; if unavailable, document explicit-load mode when supported. Do not report native discovery as validated without evidence.

For optional `image_director` and `image_eval_designer`, also copy their role
TOMLs and merge their corresponding sections only when needed. Missing optional
roles do not block production with the four required roles. Follow
[the playbook](agent-playbook.md) for dispatch and explicit-load behavior.
