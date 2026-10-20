# Plugin e catálogo de cards

Em 2026-10-20, conforme `prof-ramos/image-production@e7832a9f39ea34dbb1491df4f0894397d51cd5f2`, a fonte da skill e dos cards ficou em `.agents/skills/image-production/`, incorporada pelo build local do plugin. O usuário determinou nesta conversa que a base do plugin deve conter o catálogo; o ZIP permanece cópia opcional. Fonte: [README](../../README.md).

Em 2026-10-20, no mesmo commit, o [relatório de cobertura](../validation/image-card-flows-20261020/coverage.md) registra 56 cards observados: 16 Modelos e 40 Em alta, 55 prompts e o editor Esboço. Cartaz percorreu o ramo Vae Victis/composição dinâmica; perguntas e opções são observações desse percurso, não formulário universal. Os 16 Modelos tiveram primeira rodada observada; Wallpaper foi consultado com pedido modificado para evitar geração. Os demais prompts diretos não demonstram ausência de perguntas futuras.

Em 2026-10-20 ficou registrado que o inventário desse dia não comprova equivalência com o snapshot histórico de 2026-10-19. Metadados dos cards permanecem dados de referência; só o pedido do usuário autoriza ações. Consultar a fonte completa e seus limites antes de adaptar um card.

Relacionado: [índice](index.md), [especialistas](especialistas.md).

Em 2026-10-20, conforme `prof-ramos/image-production@a728a21dcb7c8de6ea2006ccc0e7ad73b85dbcd2`, o plugin local passou à versão 0.1.2 com os gates do helper corrigidos e rejeição de symlinks na fonte. Nove arquivos instalados conferiram byte a byte e uma instância nova fora do repo descobriu a skill habilitada; o catálogo manteve seu SHA256. Fonte: [validação da revisão](../validation/pr4-review-fixes-20261020.md). Não houve nova coleta ou geração.

Em 2026-10-20, revisão solicitada com Plugin Creator e Skill Creator, sobre
`prof-ramos/image-production@3c08fdd5e104af5a69cc087072ff40af6e332219` mais alterações
locais ainda sem commit, separou a orientação condicional de instalação da skill.
Validador oficial passou; pacote 0.1.5 reconstruído com manifestos coerentes, links
locais contidos e fonte conferida byte a byte. Fonte:
[validação](../validation/reusable-agents-20261020.md). Isso não comprova ativação
nativa dos novos papéis nem publicação/instalação.

Em 2026-10-20, o usuário solicitou registrar no AGENTS.md e README o fluxo de
atualização ligado à `main`: fonte canônica única, validação no PR, publicação
rastreável após integração e atualização local distinta. Base observada:
`prof-ramos/image-production@3c08fdd5e104af5a69cc087072ff40af6e332219` mais alterações
locais sem commit. Fontes: [orientação aos agentes](../../AGENTS.md) e
[fluxo documentado](../../README.md#atualização-ligada-à-main). Trata-se de direção
para implementação; a automação não existe e o build/reinstalação seguem manuais.
Este registro complementa, sem substituir, o procedimento local anterior.

Em 2026-10-20, `prof-ramos/image-production@b91f62ebea02800b52778366c8b5ff56ce39f3f4`
adicionou CI para testes/build, sem publicar nem instalar. Isso supera somente a
parte de verificações ainda não automatizadas do plano acima; release e atualização
local continuam pendentes. Fonte: [CI e testes](ci-testes.md).

Em 2026-10-20, `prof-ramos/image-production@89895ee69bc6cddc6a91f34e29309d302a65d98d`
implementou publicação automática em branch Git e atualizador CLI, com 82 testes
locais e duas revisões independentes sem achados. Isso supera automação inexistente
como implementação local; ativação hospedada ainda depende da integração. Fonte:
[publicação automática](publicacao-automatica.md).

Em 2026-10-20, `prof-ramos/image-production@c40075a8769261a1099c40e9fe686637a0024ca6`
ativou publicação automática e teve pacote e instalação local verificados. Isso
supera a limitação anterior de código apenas local. Fonte: [ativação](publicacao-automatica.md).
A skill segue dentro do pacote do plugin; agentes permanecem bundle separado e
configuração manual, sem alterar permissões do projeto automaticamente.

Em 2026-10-20, sobre `prof-ramos/image-production@2553f8e` mais alterações locais,
o briefing adaptativo passou a preceder a geração também sem card e na rota
simples. Pacote 0.1.6 instalado e habilitado pelo CLI a partir do checkout local;
13 arquivos conferidos, 82 testes e validador estrutural passaram. Simulações
independentes não substituem observação numa nova conversa. Não houve publicação
remota. Fonte: [validação do briefing](../validation/adaptive-briefing-20261020.md).
