# Documentação de domínio

Este repo usa contexto único: `GLOSSARY.md` na raiz e decisões arquiteturais em
`docs/adr/`. Não há layout de monorepo nem glossários por pacote.

## Antes de explorar o domínio

Leia primeiro [o índice da wiki](../wiki/index.md) e as páginas pertinentes,
conforme o AGENTS.md. Se existir, leia também `GLOSSARY.md` na raiz e os ADRs de
`docs/adr/` que afetem o trabalho. Caminhos ausentes não bloqueiam a tarefa:
prossiga sem criar arquivos vazios. A skill `domain-modeling` pode criá-los quando
termos ou decisões forem efetivamente resolvidos.

A wiki preserva fatos, fontes e histórico. Glossário define vocabulário; ADRs
registram decisões e razões. Faça referências entre eles em vez de duplicar a
mesma decisão em vários lugares. O coordenador mantém wiki e OptMem conforme
[as regras de memória](../wiki/memoria-local.md).

## Vocabulário e decisões

Use os termos definidos no glossário ao nomear conceitos em tickets, propostas,
código e testes. Se faltar um conceito necessário, identifique a lacuna durante
o trabalho de domínio. Ao propor algo que contradiga um ADR existente, cite-o,
explique o motivo e registre sua substituição quando a mudança for aprovada.
