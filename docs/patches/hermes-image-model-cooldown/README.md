# Patch reproduzível do resolvedor Codex de imagens

Preservação em 29/10/2026 do patch local descrito na [issue #14](https://github.com/prof-ramos/image-production/issues/14), sobre a base Hermes `d923a5eb487a17c0a68801bba9ef0f56c81040a8`. O commit preservado é `0cb5f80a6ef268e8196ac6cfd184cfc32b6d04c8`; o arquivo `format-patch` contém os cinco arquivos de implementação/teste, com a licença MIT do Hermes em `LICENSE.hermes`.

O patch passa `API_MODEL` do plugin até `pool.select(model=...)`, mantém o par credencial/endpoint e impede que a recusa do modelo no pool seja contornada pelo login singleton. Ele não apaga cooldowns nem contém credenciais reais. Não é um instalador: use somente um clone descartável na base indicada, não a instalação em execução.

## Reprodução

1. Faça checkout da base em um clone independente do Hermes e confirme que não há alterações locais.
2. Confira o SHA-256 do patch contra `manifest.json`.
3. Nesse clone, aplique `git am /caminho/0001-scope-codex-image-credentials.patch`.
4. Compare os cinco arquivos resultantes com os hashes de `manifest.json`.
5. Prepare o ambiente de testes conforme o `AGENTS.md` dessa base e execute o runner canônico:

```sh
scripts/run_tests.sh -j 1 \
  tests/plugins/image_gen/test_codex_image_model_cooldown.py \
  tests/plugins/image_gen/test_openai_codex_provider.py \
  tests/agent/test_auxiliary_client.py \
  tests/agent/test_credential_pool_sole_cooldown.py
```

O SHA do commit reaplicado pode diferir por metadados do committer; os hashes dos arquivos são o critério de reprodução do conteúdo.

## Evidência desta rodada

- Patch aplicado aos arquivos recuperados da base limpa: cinco de cinco hashes reproduzidos.
- Python 3.14.7 / Linux ARM64, runner canônico com ambiente limpo e proteção do Hermes home real preservada.
- Dois arquivos de teste do plugin: **25 testes aprovados**, zero falhas.
- Dois arquivos do resolvedor/pool: **249 testes aprovados**, zero falhas.
- Total desta rodada: **274 testes**. Os 291 testes do relatório de 22/10 são uma execução histórica diferente; não são o total repetido agora.
- `git diff --cached --check`: aprovado antes de preservar o commit.

## Comparação com a instalação e limites

A instalação consultada em 29/10 está em `bf0203a794a07aac3ff764972ab9087baa4e4f4e`, diferente da base histórica. `agent/auxiliary_pool.py` e o plugin de imagens coincidem byte a byte com o patch preservado. `agent/auxiliary_client.py` tem outras mudanças; as árvores sintáticas das funções `_select_pool_entry` e `_resolve_codex_credential_and_base` coincidem. Isso confirma a presença desses trechos em disco, não seu carregamento no gateway.

O PR upstream [NousResearch/hermes-agent#136629](https://github.com/NousResearch/hermes-agent/pull/136629) foi consultado em 29/10: aberto, `merged=false`, head `43481f2a637a6d7263c63a2a13cbb3435900cbb4`. Não foi aplicado nem alterado nesta rodada. O patch aqui é a preservação da correção local histórica, não uma proposta revisada sobre a main atual do Hermes.

A #14 permanece aberta: encaminhamento upstream, validação do processo WhatsApp e limites de dimensão/qualidade continuam separados. Nenhuma configuração, autenticação, instalação ou gateway foi alterado; nenhuma imagem nova ou mensagem foi enviada nesta preservação.
