# Configuração de skills de engenharia

Em 2026-10-20 o usuário invocou `setup-matt-pocock-skills`, autorizou sim para
as configurações e escolheu AGENTS em vez de Claude. Base observada:
`prof-ramos/image-production@3c08fdd5e104af5a69cc087072ff40af6e332219` mais alterações
locais ainda sem commit. Fontes: pedido do usuário nesta sessão, skill local em
`~/.agents/skills/setup-matt-pocock-skills/SKILL.md` e arquivos abaixo.

Configurados [GitHub Issues](../agents/issue-tracker.md),
[cinco rótulos de triagem](../agents/triage-labels.md) e
[domínio em contexto único](../agents/domain.md). `AGENTS.md` recebeu um único bloco
`Agent skills`. Nenhum CLAUDE.md, glossário vazio ou ADR fictício foi criado.
Preservada a wiki como memória histórica e o papel exclusivo do coordenador.

O CLI criou `needs-triage`, `needs-info`, `ready-for-agent` e `ready-for-human` no
GitHub, preservando `wontfix` existente. Leitura posterior confirmou os cinco.
Links locais e unicidade do bloco foram conferidos; `git diff --check` passou.
Não houve criação de issues, alteração de visibilidade, permissão, publicação ou
merge. Configuração oferece suporte às skills `triage`, `to-tickets`, `to-spec`
e `domain-modeling`; não comprova execução ponta a ponta de cada uma delas.

Em 2026-10-20 foi criado o [guia do desenvolvedor](../guia-do-desenvolvedor.md),
a pedido do usuário, com configuração, estrutura, desenvolvimento, testes e
solução de problemas. Base observada:
`prof-ramos/image-production@f7f16a151cd6b961b92d684c537afebef640fe7a`; documentação
acrescentada localmente sobre essa base. README e índice da wiki apontam para o
guia. Links locais, cinco seções solicitadas e comandos de ajuda do helper, dos
scripts CodeRabbit e do marketplace foram conferidos; `git diff --check` passou.
Mudança somente documental, sem repetir a suíte ou executar ações remotas.
