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
