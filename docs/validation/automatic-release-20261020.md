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
