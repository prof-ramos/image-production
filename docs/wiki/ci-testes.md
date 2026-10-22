# CI e testes CLI

## Refatoração local de reservas e revisões — 22/10/2026

Sobre `prof-ramos/image-production@2dc1385767cf49e6cc5be37b4435906aa7913cb7`
mais alterações locais sem commit, dois subagentes concentraram o histórico de
tentativas e a política de revisão no helper existente. A revisão cruzada apontou
uma mudança na precedência de erros de candidato inválido; o coordenador a
corrigiu e acrescentou regressão. Os 92 testes passaram localmente em Python
3.10 e 3.13 no macOS ARM64, e o build local passou. São dez testes adicionais;
nenhuma nova dependência. Fonte: [registro da refatoração](../refactor-log.md#aprofundamento-de-reservas-e-revisão--22102026).

Essa validação cobre o checkout modificado, não CI hospedado nem publicação.
O pacote local foi reconstruído; o cache instalado não foi alterado. Comandos,
formato persistido e política conservadora de tentativas foram preservados.

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

Em 22/10/2026, a reaplicação da refatoração sobre `prof-ramos/image-production@f4862e59bbdf12eff6fd10c0aa57185f49729fbf` gerou `ec142f8dea70889d6edf349a92e2919e0b25575e`. Os 98 testes passaram localmente em Python 3.10 e 3.13, e o build passou. A diferença de seis testes em relação aos 92 anteriores vem da base mais recente; este registro supera a base local anterior para a entrega preparada, sem comprovar CI hospedado ou publicação. Fonte: commit e [registro da refatoração](../refactor-log.md).
