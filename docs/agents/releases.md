# Publicação e atualização

A fonte canônica da skill e de seus recursos é `.agents/skills/image-production/`.
O plugin deve incorporar essa fonte pelo build; edite o repositório e preserve o
cache instalado sob gestão do Codex. Mantenha coerentes a versão e a apresentação
dos manifests portátil e de compatibilidade.

O fluxo de publicação pretendido é: validar no PR, construir a partir do commit
integrado à `main` e publicar uma versão rastreável do plugin contendo a mesma
skill. Cada versão distribuída deve identificar o commit e os hashes dos arquivos.
Falhas de testes, validação ou divergência entre fonte e pacote devem impedir a
publicação. Consulte o [README](../../README.md#atualização-ligada-à-main) para o escopo.

A publicação ainda não está automatizada. O CI em `.github/workflows/ci.yml`
executa testes e build em PRs e pushes na `main`, mas não publica nem instala. O marketplace atual aponta para
`work/plugin-dist/image-production`, ignorado pelo Git; merge na `main` não
publica nem atualiza instalações. Até a automação existir, preserve o procedimento
manual documentado e relate separadamente build, publicação e instalação.

Ao implementar a automação, use distribuição Git rastreável e trate separadamente
a atualização local: skill embutida acompanha o plugin; skill no checkout acompanha
a atualização do repositório; cópias avulsas precisam de sincronização explícita.
Inclua os especialistas no planejamento, preservando a configuração local e sua
instalação separada enquanto não houver suporte implementado e verificado.
Não declare atualização automática, instalação ou descoberta nativa sem evidência.

