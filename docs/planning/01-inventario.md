# Inventário de referências — image-production

Consulta consolidada: 16/10/2026. Base de trabalho: o plano v1.3 transcrito pelo usuário. O link compartilhado retornou título, sem corpo recuperável; não foi usado como evidência de conteúdo adicional.

## Prioridade e produção de evidência

| Prioridade | Alvo | Evidência que a frente deve produzir | Teste associado |
|---|---|---|---|
| P0 | B02 imagegen instalado + B04 codex rust-v0.163.0 | Contrato integrado, diferenças API, exposição runtime | T02–T06 |
| P0 | B03 Skill Creator | Estrutura e validação; descrição de seleção | T01–T02 |
| P0 | B01 Hatch Pet | Entradas/saídas entre geração e transformação; preservar licenças | T02, T07, T11–T12 |
| P0 | A01 skills e A02 noninteractive | Mecanismo de descoberta; eventos vs resposta final | T01, T03, T14 |
| P0 | C01 Image Evals | Rubrica adaptada e gates críticos | T08–T10 |
| P1 | C02 Transparent Assets + C03/C04 Academy | Briefs de teste, papéis das referências, revisão de bordas | T04–T10 |
| P2 | B05 imagegencam e B06 demo | Fluxos/UX; provar dependência de API | Não importar chamadas; teste conceitual dos briefs |
| P3 | B07 universal, B08 CLIP, B09 GABRIEL, B10 evals | Limites de portabilidade/custo e motivo de exclusão inicial | Só testar se necessidade futura surgir |

Classes são atribuídas ao componente, não ao repositório inteiro: **direto** = mecanismo/instrução utilizável no ambiente alvo; **adaptação** = exige mudança explícita; **conceitual** = inspira desenho, sem incorporar execução; **dependente de API** = código usa API e credenciais próprias; **incompatível** = contrato/ambiente não atende ao uso pretendido, sem afirmar que o projeto é defeituoso.

IDs de documentação: A01 Build skills; A02 Non-interactive mode; A03 Image generation. IDs de publicações: C01–C05 correspondem à lista numerada da Frente C. Código: B01–B10. Documentação sem data editorial é marcada corrente, consultada na data acima; não inferir data de publicação a partir do crawler.

Código oficial versionado responde ao contrato da versão; documentação corrente responde ao uso atual; observação local responde à sessão concreta. Nenhum deles sozinho comprova os demais. Issues são pistas de falha, sem valor normativo.

## Escopo não aprofundado

`simple-evals`, `frontier-evals`, `monitorability-evals`, `model_spec_evals` e `gpt-5-coding-examples` ficam como alvos de expansão **não verificados nesta rodada**, sem classificação de reúso aprovada. A suficiência para o núcleo inicial vem das fontes P0; não alegamos varredura exaustiva da organização. Issues #14343 e #40248 citadas no plano não foram usadas como prova de comportamento. Expansão só será útil se houver lacuna concreta de avaliação ou execução.


# Frente A — documentação oficial e superfície CLI

Consulta: 2026-10-16. Escopo: pesquisa para image-production no Codex Mac 0.163.0; sem geração, configuração ou instalação de skills.

## Fontes e resultados

- [Build skills](https://learn.chatgpt.com/docs/build-skills), aberto primeiro por https://developers.openai.com/codex/skills (redirecionamento oficial). Página corrente, sem data editorial apresentada. Skill é diretório com SKILL.md; name/description são obrigatórios. scripts/, references/, assets/ e agents/openai.yaml são opcionais. Descoberta começa pelos metadados; instruções completas carregam ao selecionar. Invocação explícita e correspondência implícita por descrição são suportadas. Locais documentados incluem .agents/skills do repositório, ~/.agents/skills, /etc/codex/skills e sistema. openai.yaml pode declarar dependências MCP e política de invocação. Inferência: compor skills significa instruir o agente a ler/aplicar outros fluxos; não estabelece uma API síncrona para chamar uma skill como função, obter retorno tipado ou garantir ferramenta disponível. Referências entre skills devem explicitar caminhos/descoberta e os artefatos intermediários.
- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), aberto primeiro por https://developers.openai.com/codex/noninteractive. Página corrente, sem data editorial apresentada. `codex exec --json` emite eventos JSONL; isso difere de um único objeto final. `--output-schema FILE` define JSON Schema para resposta final; `-o FILE` grava a última mensagem. A interface serve para coordenar tarefas e relatórios, mas um JSON válido não comprova que uma imagem foi gerada nem valida seus pixels. Exigir validação posterior de existência, tamanho, tipo de arquivo e referências a artefatos. Não interpretar cada evento JSONL como o manifesto final.
- [Image generation](https://learn.chatgpt.com/docs/image-generation), aberta e conteúdo consultado. Página corrente, sem data editorial apresentada. Documenta geração/edição no compositor e invocação explícita `$imagegen`; referências podem orientar a imagem. Também distingue geração programática pela API. A documentação atual atribui geração embutida a gpt-image-2 e aos limites gerais de uso; isso é informação corrente, não prova histórica/versionada do aplicativo 0.163.0. A interface não documenta endpoint público para um script local invocar a ferramenta embutida do app.

## Classificação de aplicabilidade

| Elemento | Classe | Decisão fundamentada |
|---|---|---|
| SKILL.md com instruções e referências | Direto | Mecanismo oficial adequado para organizar briefing, revisão e entrega. |
| scripts locais de inspeção de arquivos | Direto | Pasta opcional suportada; verificar dependências antes de executar. |
| Uma skill orientar o uso de outra skill | Adaptação | Composição por instruções e contexto, com entradas/saídas explícitas; evitar suposta função `call_skill`. |
| Fluxo de produção com estados e manifesto | Conceitual | Design de workflow útil; persistência, validação e retomada precisam ser implementadas. |
| `codex exec --json --output-schema` | Direto na CLI | Flags presentes em 0.163.0 local; não demonstra ferramenta de imagem acessível em execução não interativa. |
| Script usar Responses/Image API | API | Caminho programático separado; credencial e custo API; não executar nesta pesquisa. |
| Afirmar que arquivo YAML registra nova ferramenta nativa de imagem | Incompatível/não fundamentado | Metadados/dependências não criam uma implementação nem endpoint da ferramenta. |
| Garantir geração embutida pelo simples uso de `exec` | Incompatível/não fundamentado | Docs e help provam formato de execução/saída, não disponibilidade runtime da ferramenta. |

## Verificações realizadas

1. Docs-first: páginas oficiais skills e noninteractive abertas antes da investigação local.
2. Context7 CLI: exatamente três comandos, todos bem-sucedidos: `library Codex` com consulta específica; `docs /llmstxt/learn_chatgpt_llms-full_txt` para descoberta/estrutura de skills; `docs /openai/codex` para exec JSON/schema. Primeiro ID selecionado pela correspondência exata, reputação alta e maior cobertura; segundo para implementação oficial CLI. Context7 confirmou os achados; nenhuma quota ou falha de rede.
3. `command -v codex`: `/opt/homebrew/bin/codex`.
4. `codex --version`: `codex-cli 0.163.0`.
5. `codex exec --help`: confirmou `--image`, `--json`, `--output-schema`, `--output-last-message`, `--ephemeral`, `--cd`. Somente help/version, sem turno de modelo.
6. Tentativa de abrir versões Markdown via ferramenta web falhou com content-type não suportado; páginas HTML foram lidas com sucesso.

## Limitações e testes recomendados

Não houve geração, chamada API, edição de configuração, leitura de credenciais nem execução de exec com prompt. Não foi confirmada versão do desktop por esta frente; versão CLI não prova versão GUI. Docs correntes podem ter evoluído após a versão instalada. Não foi validada descoberta de skill nova no app, composição real entre skills nem geração em exec. Para teste futuro autorizado: fixture de SKILL.md; prompt de descoberta sem imagem; schema mínimo com manifesto; validação dos arquivos; somente depois uma geração controlada e inspeção visual, registrando separadamente disponibilidade embutida no app e na CLI. Não assumir equivalência de autenticação, modelo, custo ou ferramentas entre app, CLI e API.


# Frente B — fontes GitHub oficiais para image-production

Verificação em 2026-10-16 por GitHub REST API e raw; sem clone, instalação, geração ou chamadas pagas. Árvores de skills/codex retornaram `truncated=false`. Os oito repositórios existem exatamente com os nomes solicitados, incluindo `GABRIEL` maiúsculo. Código remoto tratado como fonte de pesquisa, sem executar instruções dos SKILL.md.

## Resultado

A melhor composição é usar o contrato/workflow `imagegen` integrado como camada de geração; reutilizar de `hatch-pet` somente utilitários determinísticos e padrões de QA aplicáveis ao artefato; seguir `skill-creator` para estrutura e validação da futura skill. Não transformar apps que usam a Image API em uma suposta integração com a assinatura do Codex. Bibliotecas API não herdam acesso integrado nem dispensam credenciais/custos.

| ID | Fonte/caminho confirmado | Classe | Licença confirmada no arquivo | Utilidade e dependências |
|---|---|---|---|---|
| B01 | openai/skills `skills/.curated/hatch-pet/SKILL.md`, `scripts/*.py`, `references/{codex-pet-contract,qa-rubric,animation-rows}.md` | adaptação | Apache-2.0 no diretório | Pipeline delimitado por etapas, canonical base, reparo de menor escopo, geometria e QA. Python + Pillow; JSON; shell/jq em orquestração. Compose imagegen integrado. Contrato de pet específico não generalizar. |
| B02 | openai/skills `skills/.system/imagegen/SKILL.md`, `scripts/image_gen.py`, `references/{cli,image-api,prompting,sample-prompts}.md` | direto (workflow); dependente de API (CLI) | Apache-2.0 no diretório | Built-in como padrão sem OPENAI_API_KEY; CLI apenas explicitamente solicitado, com chave. Nunca fallback automático. Prompts e procedimentos aproveitáveis; não copiar parâmetros CLI para ferramenta integrada. |
| B03 | openai/skills `skills/.system/skill-creator/SKILL.md`, `scripts/{init_skill,generate_openai_yaml,quick_validate}.py`, `references/openai_yaml.md` | direto | Apache-2.0 no diretório | Estrutura concisa, descrição de gatilhos, progressive disclosure, recursos por responsabilidade e validação. Scripts Python; validador/yaml precisam PyYAML. Não prova qualidade funcional ou visual. |
| B04 | openai/codex `codex-rs/ext/image-generation/{imagegen_description.md,src/tool.rs,src/backend.rs,src/extension.rs}` e `codex-rs/skills/src/assets/samples/imagegen/` | conceitual; direto para contrato | Apache-2.0 no repo; amostra imagegen tem licença própria | Implementação real da ferramenta integrada. Código Rust não é necessário para produzir imagens nem deve ser transplantado para skill. Configuração/provider/auth determinam exposição. |
| B05 | openai/imagegencam `software/src/imagegencam/openai_client.py`, `software/pyproject.toml`, README.md | dependente de API; adaptação conceitual | Apache-2.0 | Exemplo real de edição com referência e planejamento de prompt. Python >=3.11, openai>=1.109.0, qrcode>=8.2, Pillow>=10; hardware Raspberry Pi/Picamera2/Display HAT, serviços Linux para produto completo. OPENAI_API_KEY exigida. Mac é estação de montagem, não prova execução nativa integral. |
| B06 | openai/openai-imagegen-demo `services/imagegen-api.ts`, README.md, package.json | dependente de API | MIT | App fotocabine web: Next ^15.5.25, React 19.1, TS, Tailwind 4. Serviço frontend usa rota server/streaming; README exige OPENAI_API_KEY e Image API /images/edits. Útil para UX/streaming/referências, excessivo para skill local. |
| B07 | openai/codex-universal README.md, Dockerfile, LICENSES/LICENSE e SBOM | incompatível como runtime Mac nativo; conceitual | MIT do projeto; componentes têm licenças diversas | Ambiente Docker Ubuntu, linux/amd64 e arm64; README diz que apenas amd64 é usado pelos mantenedores e arm64 não inclui Swift. Não entrega ferramenta integrada image_gen nem ambiente idêntico ao app. Não introduzir Docker por padrão. |
| B08 | openai/CLIP README.md, requirements.txt, LICENSE | conceitual/adaptação opcional | MIT | Embeddings e similaridade texto-imagem; não gera imagens nem substitui QA visual. PyTorch, torchvision, ftfy, regex, tqdm, pesos/model download. README oferece CPU, exemplos CUDA; MPS/Apple Silicon não validado aqui. |
| B09 | openai/GABRIEL README.md, pyproject.toml, LICENSE | dependente de API; conceitual | Apache-2.0 | Medição/classificação de corpus via GPT API; não é gerador raster. Python >=3.10, openai>=1.109.1, pandas/numpy/scipy/pydantic etc. Custo e complexidade desnecessários para pipeline inicial. |
| B10 | openai/evals README.md, pyproject.toml, LICENSE.md | conceitual; dependente de API | MIT exceto datasets, cada qual com licença | Padrões de avaliação e registry; README pede chave API, Python >=3.9, Git LFS para datasets. Reutilizar ideia de casos/falhas/rubrica, não instalar framework para validar meia dúzia de artefatos. |

## Contratos importantes e risco de versão 0.163.0

- `hatch-pet` atual usa atlas de 1536×1872, 8×9 células de 192×208; contagens de frames por linha: 6,8,8,4,5,8,6,6,6. PNG/WebP com transparência e células não usadas vazias. Pet local em `$CODEX_HOME/pets/<pet-name>/pet.json` e `spritesheet.webp`. É um contrato do app documentado na skill, não encontrado/confirmado no app desktop fechado.
- `hatch-pet` é especializado e longo (mais de 500 linhas): geração base + até nove strips, subagentes, espelhamento condicional apenas de running-left, inspeção de frames, composição e QA em GIF/contact sheet. Usa chroma key escolhido com referência às cores; validar alpha/resíduos é determinístico, identidade/movimento continuam precisando visão humana/modelo.
- Instruções remotas de limpeza removem intermediários após QA: adaptar para política explícita de retenção, nunca executar cegamente em pastas existentes. Código licenciado não implica licença de marcas/referências/artefatos gerados.
- Tag real de CLI é `rust-v0.163.0`, não `v0.163.0` (404). Annotated-tag SHA `129b8ec7ee6f4511557a4856279f529025c25af4`, commit `83086188ae0614bd882818ff1aa23f3194962012`. Não confundir versão CLI com release do desktop.
- No commit 0.163.0 a extensão image-generation e a amostra imagegen existem. `ImagegenArgs` aceita apenas `prompt`, `transparent_background`, `referenced_image_paths` (até 5 caminhos absolutos), `num_last_images_to_include` (1–5), com rejeição de campos desconhecidos. Sem argumentos `model`, `quality`, `size` ou output path no contrato integrado.
- A extensão 0.163.0 só expõe ferramenta quando provider é OpenAI ou requer auth OpenAI/actor authorization. Presença do código não prova habilitação, plano, limites ou funcionamento da sessão desktop. Precisa de teste end-to-end autorizado em fase posterior.
- A amostra imagegen no tag permite fallback pedido/confirmado; skills/main atual o restringe a solicitação explícita. Fixar versão de origem e respeitar a skill instalada como autoridade operacional evita drift.
- Nesta sessão o tool `image_gen.imagegen` está exposto com o contrato acima. Isso confirma capacidade anunciada, não uma geração bem-sucedida (não foi solicitada nem executada).

## Verificação Mac realizada

Mac local identificado como macOS 27.0.1 / arm64. AST parse dos scripts baixados `prepare_pet_run.py`, `validate_atlas.py` e `openai_client.py` passou (verificação sintática, sem execução de geração). `python3` padrão não tem `PIL` nem `yaml`: o pipeline não roda nesse interpretador sem runtime/dependências adicionais. Nenhuma dependência instalada. Não foram testados renderização de atlas, API, hardware, modelo CLIP, build Next ou Docker; compatibilidade dessas partes permanece não demonstrada. Recomendação: quando implementar, preferir runtime fornecido pelo app e smoke tests determinísticos com fixture própria; não alterar Python global.

## SHAs e fontes imutáveis

- **skills**: `49f948faa9258a0c61caceaf225e179651397431` — [árvore fixada](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431).
- **codex**: `96eb400d1231f0199e96f640c740096087cf3e9b` — [árvore fixada](https://github.com/openai/codex/tree/96eb400d1231f0199e96f640c740096087cf3e9b).
- **imagegencam**: `3475b97a2b631d7735d97f34d58dea47deb17942` — [árvore fixada](https://github.com/openai/imagegencam/tree/3475b97a2b631d7735d97f34d58dea47deb17942).
- **openai-imagegen-demo**: `0831e720b129c2cce2e33f01270328f384cfa61a` — [árvore fixada](https://github.com/openai/openai-imagegen-demo/tree/0831e720b129c2cce2e33f01270328f384cfa61a).
- **codex-universal**: `47f4f0eb5337083e2f610db0d15558932cb4901d` — [árvore fixada](https://github.com/openai/codex-universal/tree/47f4f0eb5337083e2f610db0d15558932cb4901d).
- **CLIP**: `d05afc436d78f1c48dc0dbf8e5980a9d471f35f6` — [árvore fixada](https://github.com/openai/CLIP/tree/d05afc436d78f1c48dc0dbf8e5980a9d471f35f6).
- **GABRIEL**: `9caced978453d4ae857118eed01ed6abe9e72723` — [árvore fixada](https://github.com/openai/GABRIEL/tree/9caced978453d4ae857118eed01ed6abe9e72723).
- **evals**: `8eac7a7de5215c907fbddc30efdaf316913eccdd` — [árvore fixada](https://github.com/openai/evals/tree/8eac7a7de5215c907fbddc30efdaf316913eccdd).

Fontes prioritárias fixadas:
- [B01: skills/.curated/hatch-pet/SKILL.md](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/hatch-pet/SKILL.md)
- [B01 contrato: skills/.curated/hatch-pet/references/codex-pet-contract.md](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/hatch-pet/references/codex-pet-contract.md)
- [B02: skills/.system/imagegen/SKILL.md](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/imagegen/SKILL.md)
- [B03: skills/.system/skill-creator/SKILL.md](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md)
- [B04: codex-rs/ext/image-generation/src/tool.rs](https://github.com/openai/codex/blob/96eb400d1231f0199e96f640c740096087cf3e9b/codex-rs/ext/image-generation/src/tool.rs)
- [B05: software/src/imagegencam/openai_client.py](https://github.com/openai/imagegencam/blob/3475b97a2b631d7735d97f34d58dea47deb17942/software/src/imagegencam/openai_client.py)
- [B06: README.md](https://github.com/openai/openai-imagegen-demo/blob/0831e720b129c2cce2e33f01270328f384cfa61a/README.md)
- [B07 licença: LICENSES/LICENSE](https://github.com/openai/codex-universal/blob/47f4f0eb5337083e2f610db0d15558932cb4901d/LICENSES/LICENSE)
- [B08: README.md](https://github.com/openai/CLIP/blob/d05afc436d78f1c48dc0dbf8e5980a9d471f35f6/README.md)
- [B09: pyproject.toml](https://github.com/openai/GABRIEL/blob/9caced978453d4ae857118eed01ed6abe9e72723/pyproject.toml)
- [B10 licença: LICENSE.md](https://github.com/openai/evals/blob/8eac7a7de5215c907fbddc30efdaf316913eccdd/LICENSE.md)
- [Contrato integrado no tag 0.163.0](https://github.com/openai/codex/blob/83086188ae0614bd882818ff1aa23f3194962012/codex-rs/ext/image-generation/src/tool.rs)
- [Disponibilidade por provider no tag 0.163.0](https://github.com/openai/codex/blob/83086188ae0614bd882818ff1aa23f3194962012/codex-rs/ext/image-generation/src/extension.rs)


# Frente C — avaliação e direção de imagens

Consulta: 16/10/2026. Pesquisa documental; nenhuma geração, avaliação por API ou inspeção de imagens produzidas foi executada.

## Fontes abertas e verificadas

1. [Image Evals for Image Generation and Editing Use Cases](https://developers.openai.com/cookbook/examples/multimodal/image_evals), Emre Okcular e Kathy Lau, OpenAI, 29/01/2026. Cookbook oficial. Recomenda avaliar por fluxo: correção de instruções/texto, qualidade, marca e preservação em edições. Restrições essenciais são gates, separados das notas de estética. Usa escalas 0–5 e exemplos de juízes multimodais; requer calibração humana. O harness exemplifica chamadas API, armazenamento de casos, saídas e notas, e não constitui ferramenta integrada do Codex. A seção de marketing contém aparente reaproveitamento de critérios de UI em feedback humano; adaptar ao objetivo real em vez de copiar literalmente. Para marca, recomenda referências canônicas do sistema de design. A proposta abaixo usa escala própria 0/1/2, não atribuível à OpenAI.
2. [Generate Transparent Image Assets for Campaigns and Presentations](https://developers.openai.com/cookbook/examples/multimodal/transparent-image-assets-for-campaigns-and-presentations), Tiger He, OpenAI, 20/08/2026. Cookbook oficial com exemplos de catálogo, slides, templates e vestuário. Defende ativos transparentes reutilizáveis e feedback sobre bordas, adequação à marca e utilidade. Instruções que descrevem cenário/fundo podem contrariar o pedido de transparência; o exemplo usa API com modelo habilitado para transparência. Isso não prova que parâmetros da API existam no image_gen integrado.
3. [Creating images with ChatGPT](https://openai.com/academy/image-generation/), OpenAI Academy, 10/04/2026. Descrever finalidade, sujeito, ação, ambiente, estilo e restrições concretas; atribuir papéis às referências e relações espaciais; editar um aspecto por vez. Texto literal curto, posição e tipografia explícitas ajudam. Para conteúdo denso, admite acabamento em ferramenta de design. Orientação de ChatGPT, útil conceitualmente, não contrato da API ou do Codex.
4. [ChatGPT for marketing](https://academy.openai.com/en/public/clubs/work-users-ynjqu/resources/use-cases-marketing), 14/07/2025, atualização 27/08/2026. Exemplos oficiais de brief com objetivo, público, oferta, tom, entregáveis e indicadores; apropriado para intake de marketing. Não apresenta benchmark de conversão nem garantia de desempenho comercial de imagem.
5. [Introducing 4o Image Generation](https://openai.com/index/introducing-4o-image-generation/), 25/03/2025. Fonte histórica oficial com limitações de recorte, informação densa e precisão de edição. A própria página remete à experiência atual; não usar seus números, disponibilidade ou capacidades como especificação vigente. Não é paper de benchmark atual.

## Contrato local versus documentação API

A skill integrada deve usar somente argumentos expostos pela ferramenta image_gen disponível. Parâmetros como model, size, quality, input_fidelity, output_format, background e n encontrados nos exemplos API não podem ser inventados no contrato integrado. No ambiente atual, transparent_background é um argumento integrado explícito; referências são incluídas pelos mecanismos documentados na ferramenta. O prompt descreve intenção visual, sem garantir dimensões ou fidelidade pixel a pixel.

Separar: pesquisa atual de documentação; avaliação de skill/instruções; avaliação das imagens geradas. Passar em uma dessas etapas não implica passar nas outras.

## Rubrica operacional proposta (própria)

Escala por critério: 0 = falha material; 1 = parcial, dúvida ou ajuste necessário; 2 = atende com evidência. Usar N/A quando ausente do brief. Registrar evidência e ajuste, sem atribuir nota a uma imagem que não foi inspecionada.

| Critério | 0 | 1 | 2 |
|---|---|---|---|
| Objetivo/público/formato | Não comunica a finalidade | Comunica com ruído | Leitura clara no contexto previsto |
| Texto/fatos | Erro, invenção, omissão | Legibilidade ou fidelidade incerta | Conteúdo conferido e legível no tamanho de uso |
| Composição | Corte/posição inviabilizam uso | Precisa ajustar margens ou hierarquia | Ordem de leitura, respiro e recorte adequados |
| Marca/referência | Identidade ou produto descaracterizado | Desvio perceptível | Compatível com fonte canônica fornecida |
| Integridade visual | Anatomia/objetos/artefatos comprometem uso | Defeitos localizados | Sem defeitos relevantes detectados |
| Edição/preservação | Altera conteúdo protegido | Drift ou comparação inconclusiva | Pedido atendido e invariantes conferidos |
| Transparência, se pedida | Fundo opaco ou quadriculado pintado | Alpha existe mas bordas falham | Alpha real e bordas úteis nos fundos de destino |

Gates próprios: texto/fatos essenciais, produto/identidade, alteração proibida e transparência exigida devem ter 2 antes de entrega final. Uma nota estética alta não compensa falha factual. Nota 1 exige revisão ou limitação declarada; 0 exige correção. Não resumir tudo em média que esconda bloqueios.

## O que verificar e como

Determinístico local: arquivo decodifica, tipo real, largura/altura e proporção, presença de canal alpha e pixels efetivamente transparentes, caminho e versões, consistência de metadados entregues. Alpha sozinho não prova recorte bom. Hash demonstra identidade de arquivos, não qualidade. Comparação pixel a pixel é forte apenas onde invariância exata é realmente exigida e o fluxo a suporta.

Inspeção visual atual: conteúdo, ortografia ampliada e no tamanho de uso, hierarquia, enquadramento, marca, anatomia, preservação contra original, bordas sobre fundos claro/escuro e contexto da peça. OCR é apoio falível, não árbitro único. Hex do prompt não demonstra fidelidade cromática; transparência não é aparência de xadrez; mockup de UI não comprova funcionalidade ou acessibilidade.

Grader API futuro, opcional: julgar saídas e referências com rubricagem estruturada e razões; comparar contra amostra rotulada por humanos, medir falsos positivos/negativos e repetir calibração após alterações. Registrar modelo/versão/data e tratar como sinal, não verdade. Exige implementação, acesso e custos; não ativar nem chamar API para apenas instalar ou melhorar uma skill.

## Casos de teste propostos (a executar depois)

| ID | Fluxo | Entrada e exigência central | Falha que precisa detectar |
|---|---|---|---|
| M1 | Marketing | Cartaz com frase PT-BR curta, acentos e CTA literal | Texto errado/extrínseco e leitura confusa |
| M2 | Marketing | Variações de mesma campanha para canais distintos | Corte de conteúdo e deriva da marca |
| M3 | Marketing | Oferta com data e preço fornecidos | Inventar termos, preço ou validade |
| P1 | Produto | Foto real de embalagem, mudar somente ambiente | Alterar rótulo, forma, cor ou quantidade |
| P2 | Produto | Objeto isolado transparente para fundo claro e escuro | Fundo pintado, halo, borda truncada |
| P3 | Produto | Compor sujeito da referência 1 com contexto da 2 | Misturar papéis e proporções |
| I1 | Institucional | Peça sóbria com marca canônica e texto aprovado | Marca reinventada, tom inadequado, fatos fictícios |
| I2 | Institucional | Diagrama de relações com dados fornecidos | Setas/rótulos/relações inexatos apesar da boa aparência |
| E1 | Edição | Uma troca localizada com invariantes enumerados | Alteração fora da área e drift cumulativo |
| U1 | Produto/UI | Mockup com ação principal e áreas obrigatórias | Tela plausível visualmente mas escopo/ação incorretos |

Antes de executar, definir para cada caso referências reais autorizadas, texto exato, invariantes, formato e condições de aceite. Casos sintéticos devem ser identificados como demonstração, sem publicar fatos fictícios como reais.

## Triagem de comunidade

Busca encontrou relatos de transparência e receitas de prompting em fórum/Reddit. Não incorporados como norma: confundem modelos, versões, ferramentas e pós-processamento; alguns recomendam supostas instruções internas do image_gen sem fundamento verificável. Servem somente como pistas de regressões a testar. Nenhuma recomendação acima depende desses relatos.


## Nota de consolidação

Os relatos de cada frente acima descrevem apenas o trabalho do respectivo agente. Os testes de geração/CLI feitos pelo coordenador depois estão no documento 04. A disponibilidade integrada no app foi demonstrada por geração bem-sucedida; a geração em exec continua pendente.
