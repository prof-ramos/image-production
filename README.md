# image-production

Skill para produzir imagens raster no Codex com brief, referências de marca, `$imagegen`, entrega local e revisão documentada. **v1 em homologação**. O catálogo integra a base do plugin; ZIP é somente uma cópia opcional.

## Instalar o plugin local

A fonte única da skill e do catálogo fica em [`.agents/skills/image-production`](.agents/skills/image-production/SKILL.md). O build cria um pacote mínimo local com manifests e `skills/`, sem `.git`, artefatos de `work/` ou conversas de validação. Execute na raiz do checkout:

```sh
python3 scripts/build_plugin.py
codex plugin marketplace add .
codex plugin add image-production@image-production-local
```

Inicie uma nova sessão com `[@Image Production](plugin://image-production@image-production-local)`. A skill do plugin consulta o [índice](.agents/skills/image-production/references/chatgpt-images-index.md), carrega o card solicitado no [catálogo](.agents/skills/image-production/references/chatgpt-images-catalog.json) e usa suas perguntas/opções observadas para esclarecer apenas o que falta no briefing. Não exige extrair ou anexar ZIP.

São 56 cards observados em 20/10/2026: 55 prompts e Esboço como editor. Inclui primeira rodada dos 16 Modelos e Wallpaper com pedido modificado para evitar geração; os exemplos não são um formulário fixo nem cobertura de todas as ramificações. Consulte os [limites de evidência](.agents/skills/image-production/references/chatgpt-images-evidence.md).

Para atualizar, refaça o build e reinstale após incrementar a versão no manifest de origem. Edite a fonte no repositório; o cache instalado é gerenciado pelo Codex. O plugin distribui a skill e suas referências. Os papéis de especialistas continuam exigindo a configuração de projeto descrita abaixo; instalar o plugin não ativa esses papéis automaticamente.

[Verificação de instalação e descoberta do plugin](docs/validation/plugin-base-20261020.md).

## Usar no repositório

A skill está em [`.agents/skills/image-production`](.agents/skills/image-production/SKILL.md), descoberta pelo Codex ao iniciar uma sessão neste projeto. Peça `$image-production` com finalidade, referências, variações e destino. A sessão precisa ter a skill `imagegen` e a ferramenta integrada disponíveis. A skill não instala nem implementa o gerador.

O utilitário local exige Python 3.10+ e Pillow >=10,<13. Use o runtime disponível ou `uv run --with 'pillow>=10,<13' python .agents/skills/image-production/scripts/inspect_artifacts.py --help`. A geração integrada não requer chave API. Não há fallback automático, SDK OpenAI ou chamadas de rede no utilitário.

## Portabilidade e especialistas

Copiar somente a pasta `image-production` para `.agents/skills/` de outro projeto instala a skill, mas não instala os especialistas. Para o fluxo coordenado:

1. Copie a pasta da skill sem substituir uma skill existente.
2. Copie os arquivos de [`.codex/agents/`](.codex/agents/) para `.codex/agents/` no destino. Crie o diretório apenas se ausente; preserve os arquivos existentes e resolva colisões manualmente, sem sobrescrever o diretório ou seus arquivos.
3. Use [`.codex/config.toml`](.codex/config.toml) como exemplo para mesclar manualmente as quatro seções `[agents.image_coordinator]`, `[agents.image_producer]`, `[agents.image_technical]` e `[agents.image_visual]` na configuração adotada pelo host. Cada `config_file` aponta para `agents/<nome>.toml`, relativo ao arquivo de configuração (por exemplo, `agents/image_coordinator.toml`). Não substitua a configuração inteira nem automatize o merge. Preserve `model`, autenticação, sandbox, comentários e papéis locais; reconcilie uma seção existente antes de alterá-la.
4. Preserve um `agents.max_threads` local menor; não aumente o limite para instalar estes papéis. A chave atual `agents.max_concurrent_threads_per_session` exclui a sessão principal; `max_threads` é um alias legado. O protocolo admite até dois workers e deve respeitar qualquer limite menor do host. Esse limite não autoriza gerações simultâneas.
5. Confirme a confiança do projeto no Codex: projetos não confiáveis ignoram a configuração `.codex/`. A confiança deve abranger somente o projeto revisado, preservando sandbox e aprovações. Inicie nova sessão e confirme que o host descobriu os quatro papéis e consegue usá-los. Os arquivos de exemplo, por si só, não comprovam descoberta; a validação do Codex CLI 0.163.0 em 20/10/2026 está no relatório abaixo.

Se o host não expuser papéis nativos mas admitir subagentes genéricos, use o modo de carga explícita: leia cada TOML e forneça integralmente suas `developer_instructions` ao worker correspondente, registrando papel e caminho. Isso não comprova ativação nativa. O fluxo coordenado fica bloqueado quando faltar uma definição ou a capacidade necessária de delegação. Para uma imagem simples e independente, use `$imagegen` diretamente. A instalação do plugin disponibiliza a skill; a configuração dos especialistas permanece separada.

O coordenador é o único escritor do manifest e aguarda os relatórios separados de `image_technical` e `image_visual`, ambos relativos ao mesmo SHA256 do candidato. Use até dois workers simultâneos e apenas uma geração por vez. O limite de duas correções por asset acumula todo o histórico, inclusive retomadas. A caneca histórica não deve ser gerada novamente.

[Validação de portabilidade e limitação de descoberta em 20/10/2026](docs/validation/specialist-portability-20261020.md).

## Fluxo

1. Normalizar brief e identificar papéis das referências/brand kit.
2. Antes de gerar, criar execução com `prepare --asset-key <chave-estável>` por variante; preservar o root/ledger. Para corrigir, usar `--continue-from <último-run>` e selecionar as chaves existentes, sem renomeá-las. A reserva consome uma tentativa mesmo se cancelada.
3. Aplicar `imagegen`, salvar prompt realmente enviado e inspecionar resultado.
4. Copiar candidatos sem sobrescrever e verificar formato, dimensões e alfa.
5. Registrar separadamente reviews `technical` e `visual`, com `candidate_sha256` e revisores distintos. Ambos precisam passar para o mesmo hash; um parecer favorável não apaga a reprovação do outro.

O helper é offline e não gera imagens. Aprovação registra a revisão informada; não é um julgamento visual automático. Veja o [contrato operacional](.agents/skills/image-production/references/run-contract.md) e a [rubrica](.agents/skills/image-production/references/quality-rubric.md).

[Correções dos três apontamentos do PR #4 e validação](docs/validation/pr4-review-fixes-20261020.md).

## Desenvolvimento e verificação

```sh
uv run --with-requirements requirements-dev.txt python -m unittest discover -s tests -v
```

A suíte usa fixtures sintéticas locais, sem API, credenciais ou geração paga. O validador oficial `quick_validate.py` do Skill Creator pode ser executado contra `.agents/skills/image-production` num runtime com PyYAML. Ele valida estrutura, não comportamento.

[Resultados e limitações no Mac](docs/validation/v1-macos.md). A repetição da suíte em 19/10/2026 foi em Linux/cloud e está em [v1-linux-cloud.md](docs/validation/v1-linux-cloud.md); ela não substitui o registro do Mac. O corte interno do helper está em [refactor-log.md](docs/refactor-log.md). Artefatos de execução reais ficam em `work/` ignorado; o relatório versionado contém apenas evidências sanitizadas. Não trate testes de arquivos como homologação visual de marketing/produto/institucional.

A [revisão independente de 19/10/2026](docs/validation/independent-review-20261019.md) reconcilia os comentários do PR, documenta as correções adicionais e registra 33 testes, incluindo CLI ponta a ponta para PNG/JPEG/WebP. As homologações visuais pendentes continuam separadas desses resultados técnicos.

[Piloto recuperado: 12 ativos transparentes, prompts e pareceres históricos](docs/validation/pilot-transparent-assets-20261019/README.md).

[Catálogo observado de 56 cards e fluxos de esclarecimento](docs/validation/image-card-flows-20261020/README.md): 55 prompts completos e o editor Esboço, coletados em 20/10/2026; exemplos conversacionais têm cobertura delimitada. A cópia portátil está nas referências da skill.

## Planejamento e fontes

- [Inventário de referências](docs/planning/01-inventario.md)
- [Reaproveitamento](docs/planning/02-reaproveitamento.md)
- [Arquitetura](docs/planning/03-arquitetura.md)
- [Plano de homologação](docs/planning/04-implementacao-homologacao.md)

O planejamento é um retrato de 16/10/2026; o relatório de validação registra o estado da implementação. Não foi transplantado código dos repositórios pesquisados. Fontes externas mantêm suas licenças; esta entrega não concede direitos sobre marcas ou imagens de referência.
