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
