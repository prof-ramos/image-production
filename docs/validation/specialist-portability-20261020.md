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

## Primeira tentativa de ativação nativa — superada pela verificação abaixo

Em 20/10/2026, com `codex-cli 0.163.0`, foi iniciada uma nova sessão `codex exec --ephemeral --sandbox read-only --json` no projeto, restrita a inspecionar as opções nativas de spawn, sem gerar imagens nem criar agentes. A sessão informou `available_image_roles: []`: sua ferramenta expunha `task_name`, `message`, `fork_turns`, `model`, `reasoning_effort`, sem seletor de papéis. Esse resultado descreve a interface genérica exposta à sessão, não demonstra que os TOMLs sejam inválidos nem verifica o mecanismo interno de descoberta do host. A ativação nativa permanece não verificada. Quando subagentes genéricos estiverem disponíveis, o modo de carga explícita das quatro definições permanece suportado; deve ser identificado como tal. Bloqueio do fluxo coordenado aplica-se à ausência de definições ou delegação necessária.

`codex debug prompt-input` também não listou os papéis, mas esse comando sozinho não verifica ativação. Não foram alteradas configurações globais nem permissões para forçar descoberta.

Referências de formato consultadas em 20/10/2026: [subagentes](https://developers.openai.com/codex/agent-configuration/subagents) e [configuração](https://developers.openai.com/codex/config-reference). Documentação e versão do host devem ser verificadas novamente ao instalar.

## Material não recuperado

Em 20/10/2026, as três branches remotas listadas não continham `onboarding/pr-1`, biblioteca de 56 prompts nem novos arquivos de piloto. Esses itens não foram inventados ou declarados entregues. As evidências históricas de caneca presentes no repositório continuam `needs_revision`; não houve nova geração nem aprovação visual. Os PRs #1 e #3 e issue #2 não foram alterados, mesclados ou encerrados.

## Diagnóstico e resolução de confiança — 20/10/2026

A hipótese inicial de indisponibilidade nativa foi superada: o `config/read` do app-server instalado retornou a camada do projeto desabilitada, com a razão explícita de que faltava confiança para carregar `.codex/config.toml`. As quatro tabelas eram reconhecidas, mas ignoradas. Nenhuma migração para o formato standalone da documentação mais nova foi necessária: o mecanismo `config_file` funciona no CLI 0.163.0 instalado.

1. `codex app-server --stdio`, via protocolo oficial `initialize` e `config/read` com `cwd` do projeto e `includeLayers: true`, confirmou `agents: null` e `disabledReason` exigindo confiança do projeto.
2. Um `CODEX_HOME` temporário, com configuração de confiança exclusivamente para a cópia do projeto, carregou as quatro definições. Autenticação existente foi referenciada por symlink temporário, sem copiar ou publicar credenciais.
3. Teste runtime `codex exec --ephemeral --sandbox read-only --json`: um canário aleatório foi adicionado somente às instruções do `image_technical` em cópia temporária. A sessão principal recebeu apenas o pedido de usar esse papel nativo; não recebeu o token nem instruções manuais do papel. A resposta retornou o canário exato, exit 0. Isso verifica que o papel carregou suas instruções no runtime; não é apenas uma afirmação de descoberta baseada em arquivos.
4. Foi acrescentada uma única entrada de confiança em `~/.codex/config.toml` para `/Users/gabrielramos/Developer/image-production`, preservando todo o conteúdo anterior como prefixo e sem alterar autenticação, modelo, sandbox ou aprovações. O TOML foi reparseado.
5. Nova consulta `config/read` com a configuração real confirmou `image_coordinator`, `image_producer`, `image_technical`, `image_visual` e `disabledReason: null` para a camada do projeto.

O teste de execução usou somente `image_technical`; as quatro definições foram verificadas na configuração efetiva. Nenhuma geração, edição de imagem ou nova correção da caneca foi realizada. O modo de carga explícita continua disponível quando um host admitir agentes genéricos mas não papéis nativos.

Nova tentativa oficial de recuperar material cloud: `codex cloud list --json --limit 20` retornou `tasks=[]`, sem cursor. O UUID da conversa não é um ID de tarefa cloud aceito (`cloud status` retornou 404). Comentários dos PRs #1/#3 e issue #2 não forneciam IDs `task_e_` ou referências ao material ausente; GitHub Actions não tinha artifacts. Busca apenas por nomes relacionados em Downloads não encontrou o catálogo. Não há fonte recuperada que permita declarar entregue a biblioteca de 56 prompts ou os pilotos cloud.
