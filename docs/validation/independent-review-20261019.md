# Revisão independente do PR #1 — 19/10/2026

## Resultado e escopo

Revisão do helper, contrato, testes e registros do [PR #1](https://github.com/prof-ramos/image-production/pull/1), partindo de `0d1f0ae26d21fdcc348673376dcc8cacbb36e2e0`, em checkout isolado na nuvem. Foram corrigidas falhas adicionais reproduzidas antes da alteração de produção. A suíte final tem **33 testes aprovados**, incluindo subprocessos reais da CLI. Uma segunda revisão independente repetiu as reproduções e não encontrou bloqueadores no diff corrigido.

Este resultado é técnico. Não é aprovação formal do PR, autorização para merge nem homologação visual. As duas imagens históricas continuam `needs_revision`; não houve nova geração, edição ou inspeção visual nesta rodada.

## Reconciliação das reviews existentes

Foram lidos os comentários da conversa, a submissão de review e a thread inline atualmente disponíveis no GitHub:

- **Codex, P2, erros do argparse sem JSON:** [achado original](https://github.com/prof-ramos/image-production/pull/1#discussion_r4299136341). Já corrigido em [`73f410f`](https://github.com/prof-ramos/image-production/commit/73f410fcba0e43d3f7b9651fb88439488c4a980b). Reconfirmados flags ausentes, escolhas inválidas, comando desconhecido/ausente, argumentos extras e ajuda em texto. A thread ainda estava aberta no início desta rodada; seu estado não representava o código atual.
- **CodeRabbit:** o [comentário disponível](https://github.com/prof-ramos/image-production/pull/1#issuecomment-6224273025) contém resumo, walkthrough e aviso de limite do plano. Não há review inline nem achado acionável do CodeRabbit na lista atual. O status `SUCCESS` desse serviço não comprova revisão integral. Não foi solicitada nova revisão nem alterado o plano.
- **Reviews armazenadas/histórico inválidos e temporário do manifesto inicialmente permissivo:** correções anteriores de [`0d1f0ae`](https://github.com/prof-ramos/image-production/commit/0d1f0ae26d21fdcc348673376dcc8cacbb36e2e0), descritas em [review-fixes-20261019.md](review-fixes-20261019.md), continuam passando. Os 24 testes de entrada foram repetidos antes de adicionar regressões.
- **Issue #2:** o [registro de 16/10](https://github.com/prof-ramos/image-production/issues/2) estava desatualizado quanto ao parser e à contagem de testes. As pendências funcionais/visuais nele descritas continuam válidas.

Não foi descartado um achado de código do CodeRabbit: não havia tal achado publicado para reconciliar. A revisão adicional abaixo foi feita diretamente, sem depender do serviço.

## Achados adicionais corrigidos

| Achado reproduzido | Correção | Evidência de regressão |
|---|---|---|
| `verify` retornava `valid: true, state: approved` depois de retirar uma saída, deixar review pendente, rebaixar uma nota ou alterar a quantidade esperada | Loading rejeita `approved` incompatível com quantidade e reviews válidas/aprovadas | `test_approved_manifest_requires_complete_passing_reviews` |
| Duas cópias do mesmo registro de saída contavam como duas variantes, mesmo apontando para um único arquivo | Caminhos normalizados de saída devem ser únicos; aliases com `.` e barras repetidas também são rejeitados | `test_duplicate_outputs_cannot_count_as_two_variants` |
| Retomada aceitava `variants` 0, negativo ou acima de 20 | Mesmo intervalo e tipo estrito da preparação são exigidos no loading | `test_manifest_variants_range_is_checked_on_resume` |
| `status` regravava manifesto com caminhos vazios, absolutos, contendo traversal ou byte nulo | Validação sintática comum dos caminhos de entrada, saída e prompt antes de qualquer escrita | `test_malformed_snapshot_paths_fail_before_status_write` |
| Home inexistente, JSON excessivamente aninhado e um PNG com chunk inválido escapavam do handler como traceback/exit 1 | Erros esperados nas fronteiras de path, JSON e decoder retornam erro JSON/exit 2; sem imprimir traceback/caminhos do runtime | `test_unexpandable_home_and_deep_json_fail_as_json`, `test_png_decoder_syntax_error_is_a_structured_cli_failure` |
| Snapshot de prompt normalizava CRLF para LF antes de gravar e calcular hash | Valida UTF-8 e conteúdo não vazio, mas preserva os bytes originais | `test_prompt_snapshot_preserves_exact_utf8_bytes` |

As regressões acima foram observadas falhando antes das respectivas correções. O PNG inválido é uma fixture real com estrutura de chunks malformada, não uma exceção simulada por mock. `EOFError` também é tratado na fronteira do decoder como defesa, mas não foi apresentado como bug separado reproduzido.

## Verificações executadas

Ambiente desta rodada: Debian GNU/Linux 13, Linux x86_64 6.18.55, Python 3.12.14, Pillow 12.3.0, PyYAML 6.0.3 e jsonschema 4.26.0, no runtime Python já disponível na nuvem. Nenhuma dependência foi instalada ou atualizada, e nenhuma alteração foi feita no Mac. Não havia `AGENTS.md` no checkout nem nos diretórios ancestrais aplicáveis.

```sh
python -m unittest discover -s tests -v
python /path/to/skill-creator/scripts/quick_validate.py .agents/skills/image-production
python -m py_compile .agents/skills/image-production/scripts/inspect_artifacts.py tests/test_artifacts.py
git diff --check
```

- **33 testes, OK.** Saída integral em [independent-review-tests-20261019.txt](independent-review-tests-20261019.txt).
- **Validador oficial do Skill Creator:** `Skill is valid!`.
- **Compilação Python e whitespace:** passaram.
- **Schema de resultado:** validado com `jsonschema.Draft202012Validator.check_schema`; enum de estados também coberto pela suíte.
- **Amostras históricas:** bytes, SHA-256, dimensões e alfa de `assets/initial.png` e `assets/edit.png` conferem com [evidence.json](evidence.json). Os estados registrados continuam `needs_revision`. Essa checagem não reavaliou aparência.

O teste `test_cli_roundtrip_png_jpeg_webp_and_resume` percorre, por subprocessos reais: `prepare`, `status blocked`, coleta de PNG/JPEG/WebP com sufixos de origem deliberadamente incorretos, reviews parciais até `approved`, re-review com histórico, remoção dos originais, dois `verify` idempotentes e rebaixamento para `needs_revision`. Todas as imagens e afirmações desse teste são sintéticas; não constituem review visual.

A segunda revisão, somente leitura, repetiu o diff, a suíte final e reproduções negativas em processos independentes. Também confirmou que `status failed` continua funcionando quando um artefato desaparece. Não foi adicionado `verify` dentro de `status`: isso impediria registrar justamente a falha que precisa ser comunicada.

## Limites e pendências preservados

- Um escritor por run; nenhuma proteção contra processo hostil trocando diretórios durante a operação.
- Manifesto local não é atestado assinado. Um editor capaz de reescrever evidências e dados coerentemente ainda pode falsificar afirmações. A validação agora impede as inconsistências estruturais e de aprovação reproduzidas.
- Crash entre cópia e manifesto pode deixar candidato ou temporário órfão. Não há exclusão automática nem recuperação transacional nova.
- A seleção/reseleção manual exige intenção explícita; se invalidar a aprovação, o estado deve voltar a `needs_revision` antes da retomada e nova revisão.
- Homologações T05, T07, T08, T09, T10, T04/T06 e T13 continuam pendentes nos termos do issue #2. Integração/empacotamento/descoberta em perfil limpo também não foram homologados nesta rodada.
- Sem nova execução no Mac, geração integrada, API/SDK, instalação global, merge ou deploy.
- O repositório não contém workflow de CI de testes. A verificação publicada é esta execução local em cloud; checks de terceiros devem ser conferidos no SHA publicado e não substituem a evidência acima.
