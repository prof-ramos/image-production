# CI, cobertura CLI e instruções — 2026-10-20

Implementação: `prof-ramos/image-production@b91f62ebea02800b52778366c8b5ff56ce39f3f4`.
Base de comparação: `prof-ramos/image-production@ea02540cd413f8bf1e7ecc52ef56c9deffcb0975`.
O usuário aprovou os três itens via ask-matt/implement: CI, testes CLI e AGENTS
mais curto. O commit da base preserva separadamente o trabalho anterior da sessão.

## Resultado

- `.github/workflows/ci.yml`: suíte offline e build em PRs, pushes na main e
  execução manual, Ubuntu/Python 3.10 e 3.13. Permissão somente de leitura;
  checkout sem credenciais persistidas. Não publica, instala ou envia comentários.
- `tests/test_review_cli.py` e fixture `tests/fixtures/gh_stub.py`: oito testes
  executam os scripts públicos como subprocessos e isolam o executável gh.
  Cobrem páginas adicionais em três superfícies, deduplicação, falha no meio da
  coleta, mudança de head, falha de envio sem retry, envio e dry-run simulados.
- `AGENTS.md`: detalhes de release movidos para `docs/agents/releases.md`,
  preservando ponteiros e controles de coordenação, memória e revisão.

## Evidência executada

- Python 3.10: 73 testes passaram em 5,638 s.
- Python 3.13: 73 testes passaram em 7,485 s.
- Build local passou nos dois runtimes.
- `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.7 .github/workflows/ci.yml`
  terminou com código zero.
- Links locais dos documentos alterados resolvidos; `git diff --check` passou.
- Três mutações em cópias temporárias removeram paginação, tratamento de erro no
  envio e guarda de mudança de head; o teste correspondente falhou em cada uma.
  Isso verifica sensibilidade a regressões, sem mudar o código de produção.
- Revisão independente Standards: zero apontamentos documentados ou heurísticos
  relevantes. Revisão independente Spec: zero apontamentos. Ambas compararam
  os seis arquivos do commit de implementação contra a base acima.

## Limites

Execução hospedada no GitHub Actions não realizada. Commits locais, sem push,
proteção de branch, publicação, geração de imagem ou comentários reais no PR.
A fixture simula o contrato do CLI gh; não comprova comportamento remoto do
GitHub/CodeRabbit nem completude de revisões do serviço.

Referências consultadas para o workflow:
[Python no GitHub Actions](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
e [sintaxe de workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
Os refs v4 de actions/checkout e v5 de actions/setup-python foram resolvidos pelo
CLI na API oficial e fixados por SHA no arquivo.
