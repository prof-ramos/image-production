# Implementação e homologação

Data: 16/10/2026. Este roteiro distingue planejamento, observação local e aceite de produção.

## Ordem operacional

| Etapa | Trabalho | Evidência de saída | Critério para avançar |
|---|---|---|---|
| 0 | Fixar fontes por SHA/licença e registrar superfície runtime | Inventário 01 e ambiente observado | Cada componente prioritário tem fonte e classificação |
| 1 | Escrever SKILL.md mínimo com Skill Creator | Skill local em projeto de teste | quick_validate passa e descrição é específica |
| 2 | Ensaiar descoberta explícita e implícita | Log e marcador privado da fixture | Corpo correto lido; descoberta implícita confirmada separadamente |
| 3 | Compor com imagegen disponível | Prompt, chamada integrada e artefato | Nenhum SDK/API ativado silenciosamente |
| 4 | Implementar cópia, manifesto e inspeção | JSON e arquivos versionados | Originais intactos, caminhos confinados, pixels legíveis |
| 5 | Executar matriz visual | Rubrica e imagens aprovadas/reprovadas | Todos os requisitos críticos passam |
| 6 | Testar erros e execução não interativa | Eventos JSONL, resposta schema, erros resumidos | Falha é explícita e nenhum arquivo anterior é perdido |
| 7 | Documentar instalação e restrições reais | Relatório de homologação | App e CLI recebem vereditos próprios |

## Ensaios já executados neste Mac

- `codex --version`: **codex-cli 0.163.0**.
- Ajuda local aceita `--image`, `--json`, `--output-schema`, `-o` e `--ephemeral`.
- Feature `image_generation`: stable/true. É evidência de configuração, não de geração CLI.
- `codex exec --json --output-schema work/schema.json -o work/schema-result.json`: exit 0; resposta final `{"status":"ok"}`; eventos stdout são JSONL. Configuração habitual foi mantida. Alguns MCPs emitiram avisos de autenticação/inicialização. Nenhuma ferramenta MCP foi chamada: isso NÃO homologa uso de MCP junto com schema.
- Fixture em `work/discovery/.agents/skills/image-production-probe/SKILL.md`: CLI localizou e leu o corpo e retornou `IP_DISCOVERY_7C42`, sem o marcador aparecer no prompt. Aviso: catálogo excedeu orçamento; descrições removidas. Descoberta explícita passa; seleção implícita permanece pendente.
- `quick_validate.py`: Python do sistema falhou por falta de PyYAML. Repetição em ambiente isolado `uv run --with pyyaml` passou: `Skill is valid!`. Não mudou Python global.
- Geração integrada **nesta sessão do app**, sem SDK/API: caneca azul isolada, fundo transparente, sem texto/logo. Arquivo `smoke-caneca.png`, PNG RGBA, 1374×1145, 1.114.139 bytes; alfa 0–255, 819.937 pixels totalmente transparentes. Hash e contagens em `smoke-image-result.json`. Inspeção visual: objeto correto; teste técnico não equivale a aprovação de marca, impressão ou bordas em todas as escalas.
- Cópia do arquivo gerado para a pasta de entregáveis concluída; original preservado. Prompt em `smoke-prompt.txt`.

## Matriz ainda necessária para homologar a skill final

| ID | Caso | Verificação | Aprovação |
|---|---|---|---|
| T01 | Descoberta implícita com pedido de produção sem nome da skill | Ler skill certa pelo catálogo | Sem depender de caminho ditado no prompt |
| T02 | Composição real image-production → imagegen | Registrar leitura e chamada integrada | Imagem gerada, manifesto completo, sem API |
| T03 | Geração em codex exec 0.163.0 | Chamada real + arquivo decodificável | Não aceitar só declaração textual do modelo |
| T04 | Editar imagem local | view_image antes; mudar só fundo | Forma/cor/identidade preservadas conforme brief |
| T05 | Gerar com referência local | Papel da referência e caminho/hash | Referência chega à ferramenta e é respeitada |
| T06 | Transparência e cópia final | Alfa + preview em fundo claro/escuro | Sem fundo simulado, sem perda de alfa |
| T07 | Duas variações distintas | Uma chamada por variação | Dois arquivos, prompts e revisões próprios |
| T08 | Marketing | Marca de teste fornecida, título literal | Texto correto, hierarquia e marca aprovados |
| T09 | Produto | Referência de produto, sem inventar detalhes | Geometria, cor, materiais e recorte coerentes |
| T10 | Institucional | Brief factual e texto exato | Sem símbolos/afirmações inventados |
| T11 | Arquivo inexistente/corrompido; saída já ocupada | Erro recuperável, nomes versionados | Nenhuma entrada ou saída antiga sobrescrita |
| T12 | Caminho externo, .. ou symlink | Resolver e validar destino | Gravação indevida recusada |
| T13 | Ferramenta ausente/erro/limite | Estado blocked/failed com causa | Sem fallback API automático |
| T14 | JSON/schema com chamada MCP inofensiva autorizada | Registrar MCP chamado e resposta final | Ambos válidos, erro do MCP não ocultado |
| T15 | Nova sessão/retomada | Reabrir manifesto e referências | Não depender apenas do histórico da conversa |

Os testes pendentes fazem parte da implementação/homologação, não impedem a entrega deste roteiro. Não declarar image-production pronta antes de T01–T15 aplicáveis. Caso MCP seja excluído do escopo inicial, T14 fica explicitamente não aplicável; não usar isso para afirmar compatibilidade MCP testada.

## Evidência por execução

Guardar data, versão, prompt, hashes de entradas, eventos sanitizados, resposta final, arquivo e relatório por critério. Capturar código de saída e validar schema independentemente. Não arquivar stderr bruto de integrações sem sanitização. Limites e tempos: medir duração por execução; não prometer SLA ou resolução exata da ferramenta integrada com base nos parâmetros da API.

## Aceite

Aprovação técnica exige arquivos íntegros, descoberta/composição observadas, originais preservados e erros reproduzíveis. Aprovação visual usa a rubrica da Frente C: nenhum critério crítico pode falhar ou ficar não avaliado; critérios não aplicáveis precisam de justificativa. Aprovação do usuário continua necessária para escolhas de marca ou publicação, quando fizerem parte de um trabalho futuro. Esta entrega não publica nem instala globalmente a skill.
