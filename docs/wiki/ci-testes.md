# CI e testes CLI

Em 2026-10-20 o usuário aprovou implementar CI, ampliar testes dos scripts e
reduzir o AGENTS.md. Em
`prof-ramos/image-production@b91f62ebea02800b52778366c8b5ff56ce39f3f4` foram adicionados
workflow de testes/build para PRs e main e oito testes CLI isolados. O AGENTS.md
passou a apontar para uma referência de release. A lógica dos scripts de produção
não mudou. Fonte: [validação](../validation/ci-review-cli-20261020.md).

Os 73 testes e o build passaram em Python 3.10 e 3.13; actionlint passou. Revisões
Standards e Spec independentes não encontraram problemas. Ainda sem execução
hospedada, push, publicação ou instalação. Este registro supera a observação da
retrospectiva de inexistência de workflow, mas não comprova ativação no GitHub.

Em 2026-10-20, o [run 39421270501](https://github.com/prof-ramos/image-production/actions/runs/39421270501)
executou testes/build no GitHub para `prof-ramos/image-production@bea9f975e6d8a2d8813cd7e49432d93472ee3efa`,
com sucesso em Python 3.10 e 3.13. Isso supera a limitação anterior de verificação
apenas local para esse workflow/head. Ver [execução](execucao-main.md).

Em 2026-10-20 o [run 39423538379](https://github.com/prof-ramos/image-production/actions/runs/39423538379)
executou a automação de `prof-ramos/image-production@c40075a8769261a1099c40e9fe686637a0024ca6`
e publicou após a matriz verde. Em PRs, o job publicador foi corretamente omitido;
o [run do head final](https://github.com/prof-ramos/image-production/actions/runs/39423439779)
comprovou os testes/preparo sem publicação. Isso supera a descrição histórica do
CI limitado somente a testes/build para a implementação nova. Fontes adicionais:
[relatório](../validation/automatic-release-20261020.md).
