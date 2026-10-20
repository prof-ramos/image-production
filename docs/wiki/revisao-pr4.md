# Revisão do PR #4

Em 2026-10-20 o usuário aprovou nesta conversa o objetivo: colocar o [PR #4 de prof-ramos/image-production](https://github.com/prof-ramos/image-production/pull/4) em revisão e tratar apontamentos. Não autorizou merge nesta etapa.

Em 2026-10-20 o coordenador destacou que um check concluído e verde pode apenas indicar que um bot ignorou um rascunho; não comprova revisão nem aprovação. Antes de corrigir um apontamento, conferir o comentário original, o commit revisado e sua reprodução no código. Registrar separadamente correções, validação e apontamentos sem ação justificadamente.

Este registro documenta o objetivo e o processo; o estado mutável do PR e seus comentários devem ser consultados no GitHub antes de cada decisão. Referência local de código observada na criação da página: `prof-ramos/image-production@e7832a9f39ea34dbb1491df4f0894397d51cd5f2`.

Relacionado: [índice](index.md), [memória](memoria-local.md), [especialistas](especialistas.md).

## Revisão e correções observadas

Em 2026-10-20 o PR foi marcado pronto; o Codex revisou `prof-ramos/image-production@e7832a9f39ea34dbb1491df4f0894397d51cd5f2` e apontou um P1 de pareceres independentes e dois P2 de orçamento entre runs e symlinks na fonte. Os três foram reproduzidos e corrigidos em `prof-ramos/image-production@a728a21dcb7c8de6ea2006ccc0e7ad73b85dbcd2`, com 47 testes e revisão independente. Fonte: [relatório com links dos comentários](../validation/pr4-review-fixes-20261020.md). Esse registro supera o retrato de PR sem revisão, sem afirmar aprovação externa do commit corrigido, resolução de threads ou merge.

Em 2026-10-20 o Git HTTPS/gh retornou credencial armazenada inválida, enquanto o conector GitHub oficial permaneceu funcional. A publicação do commit acima usou blobs/árvore/commit e atualização com SHA esperado. Árvore e commit local/remoto conferiram sem alterar credenciais ou descartar trabalho. Revalidar as conexões antes de operações futuras; este registro não substitui o estado da autenticação.

## Segunda revisão solicitada

Em 2026-10-20 o usuário solicitou explicitamente nova revisão e tratamento dos apontamentos. A [solicitação única](https://github.com/prof-ramos/image-production/pull/4#issuecomment-6289241456) levou o Codex a revisar `prof-ramos/image-production@fdeda9ba315d3d88fa2cf1d56b4e70857ccb2eed`. Surgiu um [P2 sobre symlinks nos ancestrais do destino do builder](https://github.com/prof-ramos/image-production/pull/4#discussion_r4324168206), distinto da validação anterior da fonte. O [relatório de correções](../validation/pr4-review-fixes-20261020.md) registra a reprodução e sua validação. A revisão de um commit anterior não constitui aprovação automática de uma atualização.

Em 2026-10-20 uma nova solicitação após a correção anterior levou à revisão de `prof-ramos/image-production@a16750ddc5e1d7300748616b685783973307b83f`. O Codex apontou [P2 de fonte ausente/irregular removendo o build anterior](https://github.com/prof-ramos/image-production/pull/4#discussion_r4324208273). O relatório de validação citado acima documenta a reprodução e a proteção do pacote anterior durante falhas de construção; preservar fontes e validar o pacote antes de substituí-lo integra a decisão técnica desta etapa.
