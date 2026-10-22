# Hermes: credenciais por modelo e geração nativa

## Fontes e alcance

Registro da investigação e da validação realizadas na VPS, conforme a
[issue #14](https://github.com/prof-ramos/image-production/issues/14), o
[diagnóstico local](https://github.com/prof-ramos/image-production/issues/14#issuecomment-6329610766)
e a [validação após correção](https://github.com/prof-ramos/image-production/issues/14#issuecomment-6329944040).
O diagnóstico foi registrado em 22/10/2026 UTC, ainda 21/10 em São Paulo.
Este documento consolida essas evidências; sua redação não representa nova
execução dos testes, geração ou inspeção independente dos artefatos da VPS.

Base do projeto: `prof-ramos/image-production@2dc1385767cf49e6cc5be37b4435906aa7913cb7`.
Base do Hermes: `NousResearch/hermes-agent@d923a5eb487a17c0a68801bba9ef0f56c81040a8`,
v0.22.2 (2026.9.24), stable, instalado por Git em Linux ARM64.
Runtime informado: Python 3.14.7, Pillow 12.3.0 e OpenAI SDK 2.24.0.
O hash do Hermes identifica a base anterior ao patch local, não uma revisão
upstream que já contenha a correção. As fontes não fornecem um commit ou hash
do patch; este relatório não é um pacote reproduzível de instalação da correção.

## Bloqueio e mecanismo observado

O login Codex era reconhecido, mas `OpenAICodexImageGenProvider.is_available()`
retornava falso. O resolvedor de runtime encontrava um token no pool; o
resolvedor auxiliar usado pelo plugin de imagens não o resolvia.

O snapshot local continha um cooldown de `gpt-5.3-codex` até
`2027-10-21T04:30:05.598599+00:00`, sem cooldown geral ativo nem bloqueio de
`gpt-image-2`. A aplicação da função pura instalada ao snapshot em memória
demonstrou bloqueio sem modelo e elegibilidade para o modelo de imagens.
O diagnóstico não chamou `pool.select()` sobre credenciais reais e confirmou
que o armazenamento de autenticação permaneceu inalterado. Token não expirado
é uma constatação local, não prova de autorização junto ao servidor.

Na base instalada, o fallback de `resolve_codex_runtime_credentials` filtrava
o cooldown geral por `last_error_reset_at`. Já o caminho
`_read_codex_credential` → `_resolve_codex_credential_and_base` →
`_select_pool_entry` usava `pool.select()` sem modelo. A regra conservadora de
`model_cooldown_until(entry, None)` considera qualquer cooldown ativo de modelo.
Assim, o bloqueio de um modelo de conversa ocultava a credencial de imagens.

A ausência inicial de `image_gen.provider` explícito era uma pendência do
teste funcional; não explicava a indisponibilidade na consulta direta ao plugin.

## Correção local e regressões

Segundo a validação publicada, o plugin passou a transmitir seu `API_MODEL`
até `pool.select(model=...)`, preservando a resolução conjunta de credencial
e endpoint. A recusa do pool para o modelo solicitado passou a impedir o
contorno pelo fallback singleton legado. Chamadas antigas sem modelo mantiveram
o comportamento anterior; a alteração cobriu o caminho de imagens, sem afirmar
correção de todos os clientes auxiliares de texto.

Dois leitores de chave/endpoint foram movidos para `agent/auxiliary_pool.py`,
sem mudança de comportamento, para respeitar o limite de code-health.
O código instalado foi comparado byte a byte com o código validado.

Foi observado ciclo vermelho/verde para cooldown de outro modelo e para
o bypass indevido pelo singleton quando o próprio modelo estava bloqueado.
Em clone independente, com o runner canônico e a proteção do Hermes home real
preservada, o resultado registrado foi:

```text
291 tests passed, 0 failed
scripts/check --staged --base HEAD --only ruff,health
2 checks, ok
code health: 0 blocking, 0 advisory
```

A cobertura selecionada verificou permissão para modelo não bloqueado, recusa
para o modelo bloqueado, ausência de bypass pelo singleton e preservação de
tokens, refresh tokens, cooldowns, endpoint e vínculo credencial/modelo/host.
Não foi declarada execução de toda a suíte do Hermes. O clone independente
evitou referências a metadados Git da instalação protegida presentes na
tentativa inicial com worktree; as proteções dos testes foram mantidas.

## Geração e aprovação do candidato

Com `image_gen.provider: openai-codex` explícito, uma nova sessão Hermes,
usando `gpt-6.1-sol` na conversa, executou uma chamada nativa a `image_generate`.
Foi usada a autenticação Codex existente, sem fallback externo por API key,
SDK ou HTTP, nova autenticação ou reset de cooldown.

| Campo | Solicitado | Retornado/verificado |
| --- | --- | --- |
| Provedor | `openai-codex` | `openai-codex` |
| Qualidade | `medium` | `low` |
| Dimensões | 1024 × 1024 | 1254 × 1254 pixels decodificados |
| Formato | — | PNG |
| Tamanho | — | 1.483.192 bytes |

Seletor enviado: `gpt-image-2-medium`.

SHA256 do candidato `origami-fox.png`:
`6fae227b4aef33db32cad4969b2ca96e269aac465793d81467152136673553cb`.

O brief pedia uma raposa laranja de origami, inteira, sobre fundo creme, sem
texto ou logos. Não exigia dimensões ou tier exatos. A aprovação desse candidato
não comprova entrega de qualidade `medium` nem de 1024 × 1024: ambos divergiram
da solicitação. Requisitos exatos devem ser conferidos no retorno e no arquivo,
sem assumir que o seletor garante o resultado.

Dois workers distintos revisaram técnica e visualmente o mesmo SHA256, com
relatórios separados. O helper passou de `needs_revision`, após somente um
parecer, para `approved`, após ambos, e retornou
`{"valid":true,"state":"approved","outputs":1}` na verificação.
Prompt enviado, snapshots, linhagem, candidato e pareceres foram preservados
localmente na VPS. Não foram incorporados a este relatório nem reinspecionados
durante sua redação. A comparação em memória antes/depois da sessão confirmou
preservação de tokens, refresh tokens, cooldowns e endpoints.

## Estado da integração e manutenção

| Etapa | Evidência registrada |
| --- | --- |
| Instalação da adaptação | Validada localmente; testes offline não comprovam geração |
| Disponibilidade do provedor | Bloqueio investigado e correção local aplicada |
| Geração nativa | PNG real retornado em nova sessão Hermes |
| Revisão do candidato | Técnica e visual independentes aprovadas para o mesmo hash |
| WhatsApp | Gateway não reiniciado; geração pelo processo em execução não validada |
| Upstream | Sem envio de patch, PR ou merge nesta tarefa |

Na conferência registrada na issue, o
[relato Hermes #125695](https://github.com/NousResearch/hermes-agent/issues/125695)
e o [PR #136629](https://github.com/NousResearch/hermes-agent/pull/136629)
estavam abertos. O diff consultado do PR não transmitia `API_MODEL` no código
de produção do plugin de imagens. Esses estados são históricos e precisam
ser revalidados antes de decidir sobre atualização ou incorporação.

A #14 permaneceu aberta para acompanhamento da incorporação/manutenção.
Após atualizar o Hermes, conferir se a versão contém a correção do caminho de
imagens e repetir regressões pertinentes antes de assumir que o patch local
continua aplicado. Atualização pode substituir arquivos alterados localmente.
Validar o gateway WhatsApp separadamente, dentro da autorização de operação.
Não limpar cooldowns ou copiar tokens como procedimento de diagnóstico.

Este registro não atribui o defeito à skill `image-production`, não distribui
o patch do Hermes e não afirma homologação geral de qualidade, de todos os
modelos ou de todos os canais.
