# Base do plugin — 2026-10-20

O catálogo é parte da skill distribuída pelo plugin, sem depender de ZIP. A fonte única é `.agents/skills/image-production/references/chatgpt-images-catalog.json`. O SKILL consulta o índice e carrega somente o card necessário, incluindo perguntas/opções observadas e seus limites de evidência.

O repositório era uma skill de projeto, sem manifest de plugin. Foram adicionados `.codex-plugin/plugin.json` e `.agents/plugins/marketplace.json`. `python3 scripts/build_plugin.py` cria `work/plugin-dist/image-production/` a partir da fonte, com `skills/`, manifest portátil e overlay Codex. O marketplace local aponta para esse build; portanto, o build deve preceder a instalação. O pacote gerado não contém `.git`, documentos de conversas, pilotos ou outros artefatos de `work/`.

## Verificação

- Codex CLI 0.163.0: `plugin marketplace add` e `plugin add image-production@image-production-local --json` concluíram a instalação local da versão 0.1.1.
- `plugin list --marketplace image-production-local --json` confirmou `installed: true`, `enabled: true` e source local do build mínimo.
- Uma instância nova do app-server oficial recebeu `skills/list` com `cwds: ["/tmp"]` e `forceReload: true`. Retornou `image-production:image-production`, `scope: user`, `enabled: true`, `pluginId: image-production@image-production-local` e caminho instalado `skills/image-production/SKILL.md`. Isso comprova descoberta da skill fora do repositório; não comprova geração.
- Bootstrap numa pasta temporária contendo apenas script, manifest e skill canônica criou 11 arquivos, sem symlinks, `.git`, `docs` ou artefatos locais. Catálogo gerado e fonte são byte a byte iguais, SHA256 `9d34a7e80c7913bd059998010a1901ceacc0046f8e842c670449c080be5893dd`.
- Conteúdo instalado: 56 cards, 55 prompts, primeira rodada dos 16 Modelos e Wallpaper com pedido modificado de esclarecimento sem geração. A classificação dos outros 38 Em alta e do editor Esboço permanece explícita. Nenhuma URL privada de conversa ou caminho pessoal foi incluído no pacote mínimo.

O plugin distribui a skill e suas referências. A configuração dos quatro especialistas permanece no projeto e segue a instalação separada no README; não é apresentada como descoberta automática de papéis pelo plugin. Não houve nova geração, publicação em marketplace remoto ou alteração de autenticação/sandbox. A suíte anterior de 33 testes dos helpers não foi repetida: este ajuste não modifica os helpers.

O ZIP anterior permanece como exportação opcional. Atualizações futuras devem editar a fonte, incrementar a versão do manifest, refazer o build e reinstalar pelo CLI, preservando o cache como saída gerenciada.
