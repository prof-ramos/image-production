# Briefing adaptativo — 20/10/2026

## Escopo e fonte

Pedido: completar o briefing antes de gerar peças de comunicação, perguntando
somente o que ainda não foi informado. Base: `prof-ramos/image-production@2553f8ef5a36015b881ae96084e7a1a2cfdcd22b`
mais alterações locais sem commit. Versão local: 0.1.6.

A skill e `references/communication-brief.md` agora cobrem canal/placement,
uso/envio, público/finalidade, logo e materiais, dados/ação, estilo e redação.
As rotas de card e imagem simples passam pela mesma checagem. O contexto de
exercício fictício não vira texto visível automaticamente. Brief completo ou edição
pontual reaproveita respostas anteriores. Instruções concorrentes encontradas no
checkout foram preservadas e consolidadas em uma única referência de briefing.

## Verificações executadas

- Avaliação anterior: leitura e simulação identificaram a rota simples como
  permissão ambígua para pular esclarecimentos; a geração precoce também ocorreu
  na conversa que motivou o pedido.
- Revisão independente posterior, por leitura e simulação: cinco casos — convite
  incompleto, briefing completo, mudança só da data, escolhas criativas delegadas,
  Instagram com CTA WhatsApp. Identificou duplicação de referências, consolidada
  em `communication-brief.md`. Não houve geração de imagens nesta avaliação.
- `uv run --with-requirements requirements-dev.txt python -m unittest discover -s tests -v`:
  82 testes passaram. Duas asserções inicialmente falharam por versão 0.1.5 fixa;
  as expectativas agora derivam a versão-base do manifesto da fixture.
- Build local e `quick_validate.py` do Skill Creator com o runtime uv: válidos.
  O Python global não tinha PyYAML; nenhuma dependência global foi instalada.
- `git diff --check`: sem erros.
- Instalação pelo Codex CLI, sem editar seu cache: versão 0.1.6, instalada e habilitada.
  Os 13 arquivos da skill instalada conferiram byte a byte com a fonte.

## Distribuição e limites

O cadastro `image-production-local` foi trocado pelo CLI do marketplace Git para
o checkout local, pois a versão anterior do CLI recusou sobrescrever uma fonte
com outra. O plugin passa a usar `work/plugin-dist/image-production` local.
Não houve push, merge nem publicação remota desta alteração. Para voltar à
release remota, o fluxo existente é `python3 scripts/update_plugin.py`.

Instalar arquivos não comprova reload de uma conversa aberta. Abra uma nova
conversa para carregar a skill atualizada. As simulações verificam interpretação
das instruções; não são homologação do comportamento de uma nova conversa nem
avaliação visual de imagens. O gate é conversacional, não uma validação automática
de prontidão de negócio pelo helper.

## Conferência após a integração — 20/10/2026

O [PR de briefing](https://github.com/prof-ramos/image-production/pull/12) foi
integrado em `prof-ramos/image-production@2dc1385767cf49e6cc5be37b4435906aa7913cb7`.
Isso supera o checkpoint anterior de ausência de publicação remota e instalação
somente pelo checkout. A release e a instalação habilitada pelo marketplace Git
apontam à versão `0.1.6-main.g2dc1385767cf49e6cc5be37b4435906aa7913cb7`;
inventário e SHA256 dos 13 arquivos instalados conferiram com a fonte. Não foi
necessária nova instalação nesta conferência.

O [CI do merge](https://github.com/prof-ramos/image-production/actions/runs/39442317079)
passou. A revisão independente da fonte consolidada não identificou bloqueadores
de UX. O [achado do Codex](https://github.com/prof-ramos/image-production/pull/12#discussion_r4326318035)
sobre o atalho no README foi corrigido em `c9dc161`; o resumo do bot ainda se refere
ao head anterior `53eafe8`. O CodeRabbit retornou alteração de base/head e não há
evidência suficiente de revisão substantiva concluída. Não se declara aprovação
de nenhum bot no novo head. A conferência não gerou imagens nem observou uma nova
conversa; preserva-se esse limite da validação comportamental.

Uma etapa posterior de 20/10/2026 observou quatro turnos numa conversa CLI nova e
produziu um piloto separado nesta sessão com duas revisões independentes. Ver
[resultados observados e limites](briefing-live-20261020.md). Essa evidência supera
a ausência de observação apenas nos percursos efetivamente descritos; não deve ser
interpretada como teste da interface Desktop ou de envio pelo WhatsApp.
