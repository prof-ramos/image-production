# Evidências dos fluxos de cards Images

> Revisão editorial de privacidade — 2026-10-22: cópia pública saneada. URNs substituem conversas privadas; Projeto Aurora é um exemplo fictício e a mensagem particular foi omitida. As alterações não são novas observações de interface. Originais preservados privadamente.

Em 2026-10-20, `cartaz.json` registrou uma observação limitada do card Cartaz em ChatGPT Images. [flow.schema.json](flow.schema.json) define o formato de registro; [cartaz.json](cartaz.json) preserva a captura inicial. O esquema não exige que todas as etapas já tenham sido observadas. A captura inicial foi ampliada durante a investigação; consulte seu conteúdo e limitações para saber quais etapas foram registradas.

A skill REA orienta o método de distinguir observações, inferências e lacunas. A fonte desta captura é a interface nativa observada por CUA (acessibilidade e screenshot), sem estado oculto. Não foram usados ferramentas REA, CDP ou inspeção interna. Este esquema organiza evidências; sua validação não demonstra comportamento da aplicação.

## Separar o que se sabe

- `observed`: somente texto, controles, perguntas, opções, respostas efetivamente enviadas e transições testemunhadas na interface. Preserve a redação literal nas capturas privadas; na cópia pública, marque substituições editoriais e nunca as apresente como texto observado. Registre os artefatos em `evidence` com IDs e referencie-os em `evidence_refs`.
- `inferred`: hipóteses explícitas, cada qual com `claim`, `basis` e `limitations`. Uma hipótese de ramificação não deve entrar em `observed.branches`.
- `user_provided_example_not_yet_observed`: entrada ou exemplo fornecido pelo usuário, sem atribuir sua execução à interface. “Projeto Aurora” e “Dinâmico” na captura inicial pertencem a esta categoria.
- `limitations`: etapas pendentes, cobertura incompleta e outras restrições. Arrays vazios de perguntas ou respostas significam ausência de captura, nunca prova de que o fluxo não pergunta nada.

## Perguntas, opções e condições

Cada pergunta usa um `id` estável e `text`. Nas novas capturas, inclua opções literais com IDs e `evidence_refs`. O esquema também aceita o formato inicial com `input`/`details`, opções com `value` ou apenas `label`, e respostas agrupadas por `q1`, `q2` etc. com `actual_ui_message`; isso preserva a captura existente sem inventar fontes ou IDs retrospectivamente. `allows_free_text` aceita `null` quando não verificado. `answers_submitted` registra apenas respostas realmente enviadas, por `question_id`, `option_ids` e/ou `text`.

Uma ramificação observada tem `id`, `conditions`, `next_question_ids`, `observed_transition` e fontes. Cada condição referencia a pergunta anterior, um operador (`option_selected`, `text_equals`, `text_contains` ou `other`) e seu valor. Para `option_selected`, use o ID da opção. `when` na pergunta registra as condições testemunhadas de sua apresentação; não transforma uma única sequência em regra geral. `other` exige que o valor descreva a condição e que a limitação de interpretação seja registrada. Uma lista de condições descreve a combinação percorrida naquela captura, sem alegar que seja necessária ou suficiente em todos os casos.

Use `branch_coverage` para delimitar a sessão, entradas, idioma e sequência observados, listar `observed_branch_ids` e registrar `unexplored_conditions`. Seu campo `universal` aceita apenas `false`: percorrer alternativas visíveis não prova cobertura universal, nem exclui mudanças por contexto, conta, versão ou respostas livres. O campo pode faltar em capturas anteriores; sua ausência também não demonstra completude.

As referências de evidência precisam ser conferidas manualmente: JSON Schema valida estrutura, mas não garante que IDs apontem para artefatos existentes ou que o texto corresponda à UI. Novas capturas devem adicionar evidência concreta antes de promover exemplos ou hipóteses a observações. Não gerar imagens para preencher lacunas de documentação.

## Normalização do caminho Cartaz

[source-cartaz.md](source-cartaz.md) é uma transcrição legível derivada de `cartaz.json`, preservando perguntas genéricas, proveniência e lacunas, com substituições editoriais indicadas. As seis perguntas iniciais e seis perguntas do seguimento estão em `observed.questions`; as últimas têm `when` vinculado à combinação efetivamente enviada. `observed.branches` liga essa combinação às próximas perguntas, sem afirmar causalidade universal. `user_provided_example` conserva a origem anterior do exemplo; `provenance.user_example_status` registra sua posterior observação limitada. A mensagem particular foi omitida na revisão pública de 22/10; a observação histórica de perda de diacríticos não é uma nova captura. `inferred` preserva hipóteses e confiança; `branch_coverage.unexplored_conditions` preserva os desconhecidos.

## Método de captura por clipboard — 2026-10-20

Nos probes adicionais, o marcador do card foi preparado antes de copiar a resposta no browser. O operador confirmou “Copiado” visível, colou diretamente no documento com URL de arquivo conferida e verificou início, linha distintiva da tabela e cauda antes de salvar. Não usar `app.paste` entre copiar e colar: essa operação restaura o clipboard e pode introduzir a resposta anterior. Capturas duplicadas de outro card ficam rejeitadas; uma recaptura posterior válida mantém a proveniência separada.
