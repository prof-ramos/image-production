# Hermes: geração de imagens com Codex

## Validação registrada em 22/10/2026 UTC

Sobre `NousResearch/hermes-agent@d923a5eb487a17c0a68801bba9ef0f56c81040a8`,
um cooldown de outro modelo bloqueava a seleção sem modelo usada pelo plugin
de imagens. A correção local passou o modelo de imagens até a seleção do pool,
preservando bloqueios do próprio modelo e o vínculo credencial/endpoint.

O [relatório de validação](../validation/hermes-codex-image-generation-20261022.md)
consolida as fontes da [issue #14](https://github.com/prof-ramos/image-production/issues/14):
291 testes selecionados aprovados, Ruff/code-health aprovados, geração nativa
em nova sessão Hermes e revisões independentes do candidato aprovado.
Esse é um registro da execução na VPS, não uma nova execução na redação da wiki.

Qualidade `medium` e tamanho 1024 × 1024 foram solicitados; o retorno declarou
`low` e o PNG tinha 1254 × 1254. O brief admitia essa diferença. Validação pelo
gateway WhatsApp e incorporação upstream permaneceram pendentes. O relatório
não distribui o patch; revalidar versões e regressões após atualizar o Hermes.

## Preservação reproduzível — 29/10/2026

O [pacote do patch](../patches/hermes-image-model-cooldown/README.md) preserva a correção e seus testes no commit Hermes `0cb5f80a6ef268e8196ac6cfd184cfc32b6d04c8`, sobre a base histórica acima, com hashes e licença. Nesta rodada 274 testes selecionados passaram e os cinco arquivos foram reproduzidos a partir da base limpa. A comparação com a instalação atual distingue arquivos idênticos de funções equivalentes em um módulo que evoluiu. Isso supre a pendência de preservação; não comprova o gateway WhatsApp nem integração upstream.
