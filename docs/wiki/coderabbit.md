# Integração CodeRabbit

Em 2026-10-20 o usuário solicitou pesquisar CodeRabbit via Context7 e montar um
sistema aplicável ao repo. Base observada:
`prof-ramos/image-production@3c08fdd5e104af5a69cc087072ff40af6e332219` mais alterações
locais sem commit. Biblioteca consultada `/websites/coderabbit_ai`; três consultas
cobriram planos, configuração e revisão. Fontes e decisões estão no
[protocolo](../reviews/coderabbit.md).

Acrescentados configuração de revisão manual, instruções por caminho e coletor
CLI somente de leitura de comentários/pareceres, com classificação por head SHA.
Nenhuma instalação do App, disparo real ou plano pago foi ativado. `gh` retornou
HTTP 401; a visibilidade pública continua sem confirmação nesta execução.
Aprendizados do bot só entram na memória após validação no código. Esta é uma
integração de revisão de software; não homologação visual nem automação de release.

Verificações executadas no mesmo dia: 60 testes passaram (3,395 s), incluindo
três novos casos do coletor: filtro de autor/superfícies, commit antigo e ausência
de feedback sem inferência de aprovação. YAML validado contra schema oficial
baixado no dia. CLI `--help` conferida; coleta real falhou de forma controlada
por acesso GitHub indisponível, sem emitir relatório completo. Paginação e mudança
de head estão implementadas, mas não tiveram ensaio autenticado.

Em 2026-10-20 o usuário pediu automatizar o disparo e propôs um script logo após
criar o PR. Acrescentado `scripts/request_coderabbit.py`, usando a conta `gh`, com
consulta paginada, deduplicação por head/conta, rechecagem do estado, intervalo
de uma hora e limite inicial mais dois pedidos. O AGENTS.md integra a chamada ao
fluxo do coordenador. Isso complementa o disparo manual descrito antes; não há
GitHub Actions, novos tokens nem comentário publicado nesta validação. Base de
código permanece `prof-ramos/image-production@3c08fdd` mais alterações locais.
Fonte: [protocolo](../reviews/coderabbit.md#disparo-por-script-após-criar-o-pr).

Validação posterior no mesmo dia: 65 testes passaram (4,055 s), incluindo cinco
casos novos de seleção full/incremental, deduplicação, estado do PR, limites e
intervalo. `request_coderabbit.py 4 --dry-run` consultou GitHub com sucesso e
preparou solicitação para head `3c08fdd5e104af5a69cc087072ff40af6e332219`, sem
enviar. Isso supera o bloqueio de autenticação observado antes quanto a essa
consulta; não comprova envio, aceitação do bot ou revisão concluída.

Em 2026-10-20 coleta real no PR #4 observou Review skipped/Plan Free, sem prova de revisão linha a linha. Isso complementa o dry-run anterior: autenticação de leitura funciona, mas push de workflow foi recusado por escopo OAuth. Fontes e limites no [checkpoint](execucao-main.md).

Em 2026-10-20, no head `prof-ramos/image-production@bea9f975e6d8a2d8813cd7e49432d93472ee3efa`
já publicado e PR #4 retarget para main, o pedido full pelo script foi entregue.
O bot recusou por 153 arquivos excederem 100; logo não revisou o head. Isso supera
somente o retrato anterior de ausência de solicitação real no head novo, sem
transformar o skip em aprovação. Fontes: [pedido](https://github.com/prof-ramos/image-production/pull/4#issuecomment-6290668201)
e [resposta](https://github.com/prof-ramos/image-production/pull/4#issuecomment-6290669977).

Em 2026-10-20 o CodeRabbit realizou revisão real no PR #5, head
`prof-ramos/image-production@44ee5dcb9a96cdb802448327581540a9e22f5df7`, selecionando
19 arquivos. Encontrou um ajuste Minor de espaçamento/referência de commit na wiki;
foi corrigido em `prof-ramos/image-production@3fa7b4bd860d9267ecb2e3e801567e1c2e81c577`
e a [thread](https://github.com/prof-ramos/image-production/pull/5#discussion_r4324962017)
foi resolvida com evidência. Nenhum achado de código foi relatado. A revisão externa
continua ligada ao head original; a atualização posterior foi textual e passou
em CI. Não se alegou nova revisão nem aprovação formal do bot no head posterior.
A cota incluída foi consumida; não houve novo disparo ou cobrança para a correção.
Isso supera ausência de review comprovada para esse PR, sem alterar o histórico
de recusa do PR #4 por 153 arquivos. Fonte: PR/thread e [ativação](publicacao-automatica.md).
