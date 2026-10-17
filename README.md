# image-production

Skill para coordenar produção de imagens no Codex: briefing, identidade visual, referências, uso de `$imagegen`, organização de arquivos e avaliação.

## Estado

Planejamento e pesquisa concluídos em 16/10/2026. A skill final ainda não está implementada. Os documentos distinguem testes executados e homologação pendente.

## Documentação

- [Inventário de referências e prioridades](docs/planning/01-inventario.md)
- [Relatório de reaproveitamento](docs/planning/02-reaproveitamento.md)
- [Arquitetura proposta](docs/planning/03-arquitetura.md)
- [Implementação e homologação](docs/planning/04-implementacao-homologacao.md)
- [Plano operacional sem API paga](docs/planning/05-plano-operacional-sem-api.md)

## Direção técnica

Usar a ferramenta integrada de imagens por meio da skill `imagegen` disponível. Reservar scripts locais para tarefas determinísticas. Não ativar chamadas API ou novos custos como fallback automático.

Fontes externas mantêm suas próprias licenças. Este repositório inicial contém documentação de planejamento, sem incorporar código de terceiros.
