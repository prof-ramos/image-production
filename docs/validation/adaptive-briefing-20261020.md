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
