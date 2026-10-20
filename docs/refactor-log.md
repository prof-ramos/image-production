# Refatoração do helper image-production

Data: 19/10/2026. Branch `feat/image-production-v1`, PR #1. Ambiente da repetição: Ubuntu 24.04, Linux x86_64, Python 3.12.3 e Pillow 12.3.0 num venv isolado (`/tmp/ip-venv`). Não houve geração por API, SDK, MCP ou instalação global. As amostras em `docs/validation/assets/` permanecem `needs_revision`.

O SHA do commit que adiciona este arquivo só existe depois do push. A cópia em `/tmp/refactor-.md` e o artifact recebem esse SHA em seguida. Os quatro commits de código abaixo estão completos.

## Objetivo

Deixar o helper offline com fronteiras internas óbvias, sem trocar o contrato público: subcomandos, JSON de sucesso e de erro, código 0 ou 2, e o formato do manifesto. Mudanças só entram quando tornam o comportamento mais seguro, e nesse caso o contrato, os testes e `SKILL.md` andam juntos.

## Arquitetura antes

Um script único fazia caminho, imagem, brief, manifesto, revisão e CLI. Funcionava e cabia na v1, com três pontos fracos:

- `main` achava o comando com `globals()`. `verify` era um caso especial dentro da CLI.
- A troca atômica do manifesto usava `NamedTemporaryFile` direto no diretório, fora de `inside`.
- A regra do que pode ser `na`, e a decisão `approved` ou `needs_revision`, estavam no meio da gravação.

## Decisões

- Continuar em `scripts/inspect_artifacts.py`. O contrato e o plano já apontam para esse arquivo. Um pacote novo só criaria `sys.path` artificial.
- Quatro fronteiras: confinamento de caminho, forma do manifesto, política pura de revisão, despacho nomeado da CLI.
- `verify` é leitura. A segunda chamada devolve o mesmo JSON e os mesmos bytes.
- `load` não reabre os arquivos originais do brief. A retomada usa os snapshots em `inputs/`.
- Campos extras do manifesto continuam aceitos. A forma que os comandos leem passa a ser exigida antes de qualquer escrita.
- O vocabulário de `state` do manifesto fica igual ao enum de `references/result.schema.json`.

## Passos

### 1. Despacho explícito — `74dc7848618e88fa4956cfd81873c47ad5fd0b76`

`verify` virou função. `COMMANDS` mapeia os cinco subcomandos. Comando ausente na tabela, se a CLI deixasse passar, vira `ValueError` e JSON com saída 2. Na prática o `argparse` continua rejeitando subcomando desconhecido antes disso.

- Suíte: 17 testes, OK.
- CLI ao vivo: OK. Prepare, coleta de PNG com alfa, JPEG e WebP, três reviews até `approved`, novo review com histórico, `verify` duas vezes sem alterar o manifesto, versão `photo-v2.jpg`, run transparente recusando JPEG opaco, `status blocked` retomado, symlink, nome com `..`, arquivo ausente, flags ausentes, escolha inválida e ajuda em texto. Hashes e estado `needs_revision` das amostras conferidos.
- Autorrevisão: JSON, códigos e schema intactos. `verify` não grava. Nenhum caminho novo. Idempotência do `verify` coberta por teste.

### 2. Uma fronteira de caminho — `355aab08bd5e7385d0d462c8a746cf1869ee342b`

`inside` confina raiz e relativo, recusa vazio, absoluto e `..`, e não usa `relative_to` (a exceção dele incluía caminho absoluto). O manifesto temporário passa por `inside` e `write_new`, fica em modo `0600` e some no `finally` se a troca falhar.

- Suíte: 18 testes, OK.
- CLI ao vivo: OK, o mesmo roteiro.
- Autorrevisão: symlinks e traversal continuam recusados. Erros de confinamento não ecoam o diretório do run. Contrato e `SKILL.md` descrevem caminho relativo não vazio, erro curto e o possível `.manifest-*.tmp` órfão. Schema intocado. Há uma janela curta em que o temporário ainda está no umask, antes do `chmod`.

### 3. Política pura de revisão — `7803096985027d0f2371ac2de30660f9c20d1dd7`

`applicable_criteria`, `checked_review` e `approval_state` não leem relógio nem disco. `review` valida antes de mexer no histórico e só então grava `reviewed_at`. Nota `na` em critério obrigatório continua inválida; `na` permitido continua contando como aprovado na decisão final. A contagem de variantes continua obrigatória.

- Suíte: 19 testes, OK.
- CLI ao vivo: OK. O terceiro review fecha `approved`; o review seguinte preserva uma entrada de histórico.
- Autorrevisão: mensagens de erro, estados e schema iguais. Sem mudança de caminho. `review` segue não idempotente de propósito, porque histórico e data mudam. `verify` segue idempotente.

### 4. Manifesto malformado não grava — `13e974ccba7d68549eccc55a79c6ebb1718e5c98`

`validate_manifest` exige estado conhecido, `text`/`variants`/`transparent`, e registros de input/output com os campos que `verify` e `review` leem. Manifesto quebrado falha com `Malformed manifest` antes de `status` ou qualquer outra escrita. Não chama `validate_brief`, para não exigir que o arquivo original ainda exista.

- Suíte: 21 testes, OK.
- CLI ao vivo: OK, inclusive retomada depois de apagar a necessidade do original no fluxo já coberto pela suíte (`test_roundtrip_and_resume_without_source`).
- Autorrevisão: campos extras continuam no objeto. `schema_version` ou `mode` errados continuam `Unsupported manifest`. O enum de estado ficou amarrado ao `result.schema.json` por teste. Contrato e `SKILL.md` descrevem a retomada por snapshot.

## Por que parar

Outro corte seria pacote, adaptadores só para tirar o `Namespace`, ou uma máquina de estados. Nenhum muda uma decisão que o leitor não consiga achar agora. O script permanece o único ponto de entrada, e cada regra de aprovação ou de caminho tem uma função com um teste que não depende do resto.

## Riscos que continuam

- Um processo por run. Não há trava contra dois escritores.
- A checagem de symlink vale no acesso, não contra troca de diretório no meio da chamada.
- Uma queda entre a cópia do candidato e o `save` deixa arquivo órfão em `final/` ou `work/`. Não é apagado automaticamente.
- Uma queda no meio da troca pode deixar `.manifest-*.tmp`. Não é candidato.
- O laço de versão (`mug-v2`, `mug-v3`, …) não tem teto.
- `JSONDecodeError` ainda é `ValueError`; a mensagem do decoder pode citar posição, não o caminho.
- Homologação visual P1 do issue #2 segue aberta. Halo continua `needs_revision`.
- Merge não foi feito.
