# Plugin e catálogo de cards

Em 2026-10-20, conforme `prof-ramos/image-production@e7832a9f39ea34dbb1491df4f0894397d51cd5f2`, a fonte da skill e dos cards ficou em `.agents/skills/image-production/`, incorporada pelo build local do plugin. O usuário determinou nesta conversa que a base do plugin deve conter o catálogo; o ZIP permanece cópia opcional. Fonte: [README](../../README.md).

Em 2026-10-20, no mesmo commit, o [relatório de cobertura](../validation/image-card-flows-20261020/coverage.md) registra 56 cards observados: 16 Modelos e 40 Em alta, 55 prompts e o editor Esboço. Cartaz percorreu um ramo com composição dinâmica (Projeto Aurora é o rótulo fictício editorial da cópia pública, não uma entrada observada); perguntas e opções são observações desse percurso, não formulário universal. Os 16 Modelos tiveram primeira rodada observada; Wallpaper foi consultado com pedido modificado para evitar geração. Os demais prompts diretos não demonstram ausência de perguntas futuras.

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

Em 2026-10-20, a conferência de
`prof-ramos/image-production@2dc1385767cf49e6cc5be37b4435906aa7913cb7`, integrado pelo
[PR de briefing](https://github.com/prof-ramos/image-production/pull/12), comprovou
release remota e instalação habilitada da versão 0.1.6 com o mesmo SHA de origem;
13 arquivos instalados conferiram com a fonte. Isso supera apenas a ausência de
publicação e a instalação exclusivamente local do registro anterior. A fonte
consolidada passou pela revisão independente; uma nova conversa continua sem
homologação comportamental. Fonte: [conferência após integração](../validation/adaptive-briefing-20261020.md#conferência-após-a-integração--20102026).

Em 2026-10-20, sobre a mesma fonte
`prof-ramos/image-production@2dc1385767cf49e6cc5be37b4435906aa7913cb7`, uma conversa
nova real no Codex CLI percorreu quatro turnos: capacidade, convite incompleto,
resposta parcial e alteração somente da data. A skill instalada foi lida e o
agente aguardou aprovação da redação sem reservar nem gerar. Isso supera a ausência
de observação comportamental somente para esse percurso no CLI; não comprova a
interface Desktop nem confiabilidade estatística. Casos e evidências estão na
[validação observada](../validation/briefing-live-20261020.md).

Na mesma data, o usuário delegou ao coordenador a decisão sobre o briefing e texto
propostos para um piloto separado. Uma geração integrada produziu PNG opaco 2:3,
1024×1536, com a data original 03/12. Revisões nativas técnica e visual independentes
do mesmo SHA256 passaram, e o helper verificou o run como `approved`. Não houve
correção, envio real pelo WhatsApp ou comparação com identidade oficial sem kit de
marca. A geração nesta sessão é distinta da conversa CLI de teste e de suas
fixtures sintéticas. Fonte: [piloto e seus limites](../validation/briefing-live-20261020.md).

Em 2026-10-22, a revisão de privacidade substituiu identificadores privados por URNs locais e o título particular por um exemplo fictício nos documentos públicos. O nome Projeto Aurora nos registros anteriores agora é substituição editorial; não foi uma nova observação. A mensagem enviada foi omitida. Originais foram preservados fora do Git. Esta revisão da árvore atual não remove versões antigas do histórico. Fonte: [derivação pública](../validation/image-card-flows-20261020/public-derivation.json).

Em 2026-10-22, a revisão de `prof-ramos/image-production@143320651d275b141e5e9ec903519f81d5f2be2d` no PR #16 identificou três ambiguidades de proveniência na correção de privacidade. A rodada seguinte qualificou os valores fictícios e o caminho anonimizado no próprio registro, sincronizou a transcrição e os hashes e preservou as perguntas e opções. Suíte local de 88 testes e revisão independente passaram; não se presume revisão externa do head posterior nem saneamento do histórico. Fonte: [triagem e limites](../validation/pr16-review-20261022.md).

## Carregamento sem duplicação — 26/10/2026

Sobre `prof-ramos/image-production@f71fe5fe544c4fecb673b0b043afc77cec172f1f`
mais o ajuste de configuração desta limpeza, `skill-cleaner` identificou duas
cópias idênticas de `image-production` no inventário do Codex CLI: fonte do projeto
e plugin instalado. O override em [`.codex/config.toml`](../../.codex/config.toml)
desativa o plugin somente neste projeto, preservando a fonte canônica e a
instalação global. Não houve edição nem remoção de arquivos no cache do Codex.

A releitura do inventário CLI confirmou uma única cópia e redução de 39 para 38
skills, com estimativa do analisador de 2.720 para 2.629 tokens. Esses números
pertencem ao inventário CLI consultado, não ao catálogo desta sessão Desktop.
A varredura foi ampliada explicitamente para `~/.agents/skills` e a fonte local,
pois os caminhos padrão do analisador não as abrangiam. Indicações de ausência de
uso não justificaram remoção: skills efetivamente usadas nesta sessão apareciam
com contadores zerados. Coincidências de nomes com conteúdos diferentes foram
preservadas. Os relatórios completos ficaram fora do Git, em diretório privado.
