# Portabilidade dos especialistas — 20/10/2026

Base auditada: `prof-ramos/image-production@cd1c88ce79c451e7833b2865a00156296cad824c`, branch local `fix/specialist-portability`.

## Alteração e limites

Em 20/10/2026 foram reconstruídas quatro definições de papéis a partir dos requisitos fornecidos pelo usuário: coordinator, producer, technical e visual. Não são arquivos recuperados do workspace cloud. O exemplo `.codex/config.toml` contém somente as quatro tabelas de papéis; nenhuma definição fixa modelo, autenticação, sandbox ou limite de threads. A instalação documentada exige mesclar as tabelas e copiar as definições, preservando configuração e arquivos existentes.

O protocolo atribui escrita exclusiva do manifest ao coordenador, até dois workers e uma geração por vez, revisões independentes do mesmo hash e limite acumulado de duas correções. Nenhuma imagem foi gerada nesta validação.

## Verificação executada

- `uv run --with-requirements requirements-dev.txt python -m unittest discover -s tests -v`: 33 testes, zero falhas.
- `uv run --with PyYAML python <skill-creator>/scripts/quick_validate.py .agents/skills/image-production`: `Skill is valid!`.
- Ensaio em dois diretórios temporários, novo e com configuração existente: cópia da skill e dos quatro TOMLs, parse TOML e resolução de todos os `config_file` passaram. O cenário existente preservou comentário, modelo, sandbox, papel local e `agents.max_threads = 1` byte a byte no prefixo original. Foi um ensaio de merge manual por adição de tabelas sem colisões; não implementa um instalador nem prova merges arbitrários.
- `git diff --check`: sem erros.

## Descoberta nativa: bloqueada neste host

Em 20/10/2026, com `codex-cli 0.163.0`, foi iniciada uma nova sessão `codex exec --ephemeral --sandbox read-only --json` no projeto, restrita a inspecionar as opções nativas de spawn, sem gerar imagens nem criar agentes. A sessão informou `available_image_roles: []`: sua ferramenta expunha `task_name`, `message`, `fork_turns`, `model`, `reasoning_effort`, sem seletor de papéis. Portanto a presença dos arquivos não valida ativação. O fluxo coordenado permanece bloqueado nesse host até uma sessão expor os quatro papéis; o fluxo simples via imagegen continua separado.

`codex debug prompt-input` também não listou os papéis, mas esse comando sozinho não verifica ativação. Não foram alteradas configurações globais nem permissões para forçar descoberta.

Referências de formato consultadas em 20/10/2026: [subagentes](https://developers.openai.com/codex/agent-configuration/subagents) e [configuração](https://developers.openai.com/codex/config-reference). Documentação e versão do host devem ser verificadas novamente ao instalar.

## Material não recuperado

Em 20/10/2026, as três branches remotas listadas não continham `onboarding/pr-1`, biblioteca de 56 prompts nem novos arquivos de piloto. Esses itens não foram inventados ou declarados entregues. As evidências históricas de caneca presentes no repositório continuam `needs_revision`; não houve nova geração nem aprovação visual. Os PRs #1 e #3 e issue #2 não foram alterados, mesclados ou encerrados.
