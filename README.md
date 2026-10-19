# image-production

Skill para produzir imagens raster no Codex com brief, referências de marca, `$imagegen`, entrega local e revisão documentada. **v1 em homologação**, sem instalação global automática.

## Usar no repositório

A skill está em [`.agents/skills/image-production`](.agents/skills/image-production/SKILL.md), descoberta pelo Codex ao iniciar uma sessão neste projeto. Peça `$image-production` com finalidade, referências, variações e destino. A sessão precisa ter a skill `imagegen` e a ferramenta integrada disponíveis. A skill não instala nem implementa o gerador.

O utilitário local exige Python 3.10+ e Pillow >=10,<13. Use o runtime disponível ou `uv run --with 'pillow>=10,<13' python .agents/skills/image-production/scripts/inspect_artifacts.py --help`. A geração integrada não requer chave API. Não há fallback automático, SDK OpenAI ou chamadas de rede no utilitário.

Para usar em outro projeto, copie somente a pasta `image-production` para `.agents/skills/` desse projeto, sem substituir uma skill existente. Inicie nova sessão e confirme a descoberta. Instalação global fica fora desta versão.

## Fluxo

1. Normalizar brief e identificar papéis das referências/brand kit.
2. Criar execução com snapshots e hashes das entradas.
3. Aplicar `imagegen`, salvar prompt realmente enviado e inspecionar resultado.
4. Copiar candidatos sem sobrescrever e verificar formato, dimensões e alfa.
5. Registrar revisão visual e limitações por critério.

O helper é offline e não gera imagens. Aprovação registra a revisão informada; não é um julgamento visual automático. Veja o [contrato operacional](.agents/skills/image-production/references/run-contract.md) e a [rubrica](.agents/skills/image-production/references/quality-rubric.md).

## Desenvolvimento e verificação

```sh
uv run --with-requirements requirements-dev.txt python -m unittest discover -s tests -v
```

A suíte usa fixtures sintéticas locais, sem API, credenciais ou geração paga. O validador oficial `quick_validate.py` do Skill Creator pode ser executado contra `.agents/skills/image-production` num runtime com PyYAML. Ele valida estrutura, não comportamento.

[Resultados e limitações no Mac](docs/validation/v1-macos.md). A repetição da suíte em 19/10/2026 foi em Linux/cloud e está em [v1-linux-cloud.md](docs/validation/v1-linux-cloud.md); ela não substitui o registro do Mac. O corte interno do helper está em [refactor-log.md](docs/refactor-log.md). Artefatos de execução reais ficam em `work/` ignorado; o relatório versionado contém apenas evidências sanitizadas. Não trate testes de arquivos como homologação visual de marketing/produto/institucional.

A [revisão independente de 19/10/2026](docs/validation/independent-review-20261019.md) reconcilia os comentários do PR, documenta as correções adicionais e registra 33 testes, incluindo CLI ponta a ponta para PNG/JPEG/WebP. As homologações visuais pendentes continuam separadas desses resultados técnicos.

## Planejamento e fontes

- [Inventário de referências](docs/planning/01-inventario.md)
- [Reaproveitamento](docs/planning/02-reaproveitamento.md)
- [Arquitetura](docs/planning/03-arquitetura.md)
- [Plano de homologação](docs/planning/04-implementacao-homologacao.md)

O planejamento é um retrato de 16/10/2026; o relatório de validação registra o estado da implementação. Não foi transplantado código dos repositórios pesquisados. Fontes externas mantêm suas licenças; esta entrega não concede direitos sobre marcas ou imagens de referência.
