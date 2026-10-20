# Validação local de publicação automática — 20/10/2026

A implementação da branch `feat/automatic-plugin-release` foi verificada localmente,
a partir da base `prof-ramos/image-production@bea9f97`, sem publicação real nem
alteração da configuração/cache reais do Codex.

## Evidências

- `uv run --python 3.10 --with-requirements requirements-dev.txt python -m unittest discover -s tests -v`: 82 testes aprovados.
- Mesmo comando com Python 3.13: 82 testes aprovados.
- `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.7 .github/workflows/ci.yml`: aprovado.
- `git diff --check`: aprovado.

Nove testes novos usam repositórios Git descartáveis para conferir exportação do
commit sem alterações locais, fonte empacotada, versão determinística, hashes,
clone limpo da distribuição, no-op, recusa de symlinks/frontmatter inválido,
push rejeitado, `main` avançando durante a preparação e payload remoto danificado.

O teste de integração com Codex CLI 0.163.0 executa o atualizador em `CODEX_HOME`
temporário. Git redireciona a URL canônica somente nesse ambiente de teste para
um bare repo local. A migração do marketplace local para Git e a atualização entre
duas versões passaram, com verificação de todos os bytes instalados. O teste
inicia o atualizador dentro de um checkout com marketplace de desenvolvimento;
as chamadas ao Codex usam diretório neutro e não sofrem esse sombreamento.

Esse teste é omitido quando o executável Codex não está instalado, como pode
acontecer no runner de CI. Os demais testes são offline e não dependem dele.
Nenhuma imagem foi gerada, nenhuma API paga foi chamada e nenhum agente foi
instalado pelo bundle.

## Workflow e limites

As tags oficiais `actions/checkout@v6` e `actions/setup-python@v6` foram resolvidas
em 20/10/2026 e fixadas pelos SHAs completos no workflow. Seus manifests declaram
Node24 e os READMEs exigem Actions Runner >=2.327.1:
[checkout](https://github.com/actions/checkout/tree/d23441a48e516b6c34aea4fa41551a30e30af803),
[setup-python](https://github.com/actions/setup-python/tree/ece7cb06caefa5fff74198d8649806c4678c61a1).
O runner adotado é hospedado pelo GitHub (`ubuntu-latest`).

A autenticação de publicação com `GITHUB_TOKEN`, a execução hospedada do novo job
e a instalação da release remota real dependem de integrar esta implementação
à `main`. Os testes locais não comprovam esses passos. Atualizar arquivos de um
plugin não comprova reload da sessão aberta; a descoberta exige nova sessão.

Procedimento e decisões: [publicação e atualização](../agents/releases.md).


## Ativação remota e instalação real — 20/10/2026

O [PR #5](https://github.com/prof-ramos/image-production/pull/5) foi integrado à
`main` em `prof-ramos/image-production@c40075a8769261a1099c40e9fe686637a0024ca6`.
O [run de push na main](https://github.com/prof-ramos/image-production/actions/runs/39423538379)
concluiu com sucesso os testes/build/preparação em Python 3.10 e 3.13 e o job
`Publish plugin and skill`, usando o `GITHUB_TOKEN` do job. A publicação hospedada
anteriormente pendente neste registro foi comprovada nessa execução.

Um clone separado da branch `plugin-release` e o verificador oficial do repositório
confirmaram:

- Promoção: `10799cb4067755dd2c91859dee97026198bac410`.
- Payload fixado pelo marketplace: `2bafb4a153c9c95c87622c8b5723eb955d0cac77`.
- Origem: `prof-ramos/image-production@c40075a8769261a1099c40e9fe686637a0024ca6`.
- Versão: `0.1.5-main.gc40075a8769261a1099c40e9fe686637a0024ca6`.
- Todos os 23 arquivos do inventário passaram na comparação de hashes, manifests
  e proveniência; o catálogo aponta para o commit de payload acima.

`python3 scripts/update_plugin.py` atualizou a instalação real pelo CLI oficial,
retornando `verified: true`, versão e commit de origem acima. `codex plugin list
--marketplace image-production-local --json`, executado tanto no checkout quanto
em diretório neutro (`/tmp`), confirmou plugin instalado/habilitado, marketplace
Git HTTPS e o mesmo SHA do payload. Esses comandos não indicaram sombreamento
pelo marketplace de desenvolvimento do checkout. O cache permaneceu sob gestão
do Codex, sem edição manual.

CodeRabbit revisou `44ee5dcb9a96cdb802448327581540a9e22f5df7` e apontou somente
[formatação e referência de commit na wiki](https://github.com/prof-ramos/image-production/pull/5#discussion_r4324962017).
A correção documental em `3fa7b4bd860d9267ecb2e3e801567e1c2e81c577` preservou o
código revisado e passou no [novo CI](https://github.com/prof-ramos/image-production/actions/runs/39423439779).
A thread foi resolvida após registrar o commit. Codex GitHub concluiu a revisão de
`44ee5dc` sem achados. A cota CodeRabbit incluída de uma revisão por hora foi
consumida; não houve novo disparo para a correção textual, contratação ou cobrança.

A descoberta dos sete agentes em nova sessão está registrada na
[validação própria](native-seven-agents-20261020.md). A atualização real do plugin
não comprova reload da sessão aberta; iniciar uma nova sessão continua necessário
para conferir a descoberta da skill publicada. Não houve geração de imagens nem
instalação automática do bundle de agentes.
