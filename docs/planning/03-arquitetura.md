# Arquitetura proposta — image-production

Data: 16/10/2026. Especificação operacional; a skill final ainda não foi instalada ou implementada.

## Decisões

`image-production` coordena produção; `$imagegen` mantém a responsabilidade pela geração/edição. Composição significa o agente ler e aplicar as duas skills; não existe aqui uma função inventada `call_skill`. Scripts locais não chamam uma ferramenta interna do app por HTTP nem substituem geração por desenho programático.

Escopo inicial: briefing, contexto de marca, referências, geração integrada, inspeção, cópia não destrutiva, manifesto e validações determinísticas. Sem SDK OpenAI, servidor MCP próprio, CLIP ou grader API obrigatório. API permanece extensão separada, explícita, sujeita a credencial e custo; indisponibilidade integrada não autoriza mudança automática para API.

## Entradas

Brief: objetivo, público, uso, slug da taxonomia de imagegen, número de variações, texto literal, restrições e critérios de aprovação. Brand kit: arquivo fornecido, paleta, tipografia e regras existentes; não inventar identidade. Cada imagem recebe papel: referência, alvo de edição ou inserção. Diretório de saída é resolvido antes da cópia; nomes são locais, sem derivar comandos shell do brief.

## Fluxo

1. Verificar skill e ferramenta disponíveis na sessão real. Não inferir disponibilidade por instalação, feature flag ou sucesso de JSON.
2. Ler brief/brand kit e identificar requisitos essenciais ausentes. Só pedir decisão de produto quando indispensável.
3. Carregar imagens locais com `view_image` antes de editar. Usar o mecanismo de referências exposto pela ferramenta da sessão; não presumir assinatura fixa entre app e CLI.
4. Preparar prompt curto: finalidade, cenário, sujeito, composição, cores, texto exato e invariantes. Não usar parâmetros exclusivos da API como supostos argumentos da ferramenta integrada.
5. Aplicar `$imagegen`, uma chamada por ativo/variante distinta. Guardar o prompt realmente enviado.
6. Inspecionar visualmente e validar arquivos. Uma iteração dirigida por defeito concreto; após duas tentativas corretivas, registrar pendência e entregar candidato para decisão, evitando repetição ilimitada.
7. Copiar arquivo retornado de sua localização real para a saída. Não presumir /tmp nem argumento de destino integrado. Preservar original e criar nome versionado se já existir.
8. Gravar manifesto e relatório visual; só marcar aprovado quando os requisitos críticos passarem.

## Estrutura mínima a implementar

```text
image-production/
  SKILL.md
  references/quality-rubric.md
  scripts/inspect_artifacts.py
```

Frontmatter obrigatório: `name: image-production` e descrição discriminante. `agents/openai.yaml` é opcional, metadado de UI/política; não registra ferramenta nativa. Acrescentar outros arquivos apenas se uso real justificar. Instalação inicial de homologação em `.agents/skills/image-production` de um projeto isolado; instalação global só após aprovação dos testes. Não editar imagegen oficial.

## Contratos e persistência

Cada execução terá `run_id`, data, versão CLI observada, superfície (`desktop` ou `exec`), modo (`built-in` ou `api-explicit`), brief, referências com hash, prompt final, outputs, validações, revisão visual e estado. Diretórios `inputs`, `work` e `final` separados logicamente; referências de entrada não são sobrescritas.

Estados propostos: `prepared`, `generated`, `needs_revision`, `approved`, `blocked`, `failed`. Schema de resposta final deve ter propriedades obrigatórias explícitas e `additionalProperties: false`; manifesto de negócio é separado dos eventos JSONL do CLI. Registrar erro resumido sem credenciais, URLs de acesso ou dump de configuração.

Cada output registra caminho relativo ao run, SHA-256, formato, dimensões, bytes, canal alfa e resultado por requisito. Validar o conteúdo real, não apenas extensão. Resolver caminhos e rejeitar fuga da saída por `..` ou symlinks antes de gravar; copiar exclusivamente com criação nova, sem sobrescrita implícita.

## Limites da avaliação

Presença de elementos, texto correto, identidade e hierarquia não são comprovados por dimensões ou Pillow. Regras de arquivo são automáticas; conformidade visual exige inspeção com rubrica. OCR e graders multimodais são opcionais futuros e precisam de calibração; não garantem aprovação factual. Transparência: exigir canal alfa e pixels transparentes; depois inspecionar bordas e halos. Exportação não pode descartar alfa inadvertidamente.

## Compatibilidade

Documentação corrente orienta o desenho, mas não substitui ensaio na CLI 0.163.0. Não presumir ambiente Docker codex-universal no Mac. Dependências locais: Python e Pillow para inspeção, PyYAML para quick_validate; usar ambiente isolado. Catálogo local saturado prejudica descoberta implícita, mesmo com leitura explícita funcionando. Nenhuma configuração de segurança deve ser relaxada para fazer testes passarem.

## Rubrica de aceite proposta



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

