# Publicação e atualização

## Fonte e pacote

A fonte canônica fica em `.agents/skills/image-production/`. O build local mantém
seu comando anterior: `python3 scripts/build_plugin.py`. O marketplace do checkout
continua apontando para `work/plugin-dist/image-production`, destinado ao
desenvolvimento local. A distribuição remota usa a branch `plugin-release`.

O workflow `.github/workflows/ci.yml` valida testes, build e preparação da release
em PRs, pushes na `main` e execução manual. Somente um **push na `main`**, com toda
a matriz aprovada, habilita o job de publicação. A primeira execução hospedada
e a instalação real foram verificadas em 20/10/2026, conforme as
[evidências de ativação](../validation/automatic-release-20261020.md#ativação-remota-e-instalação-real--20102026).

O publicador lê blobs do commit validado, sem incorporar alterações locais. Exige
frontmatter válido da skill, igualdade byte a byte da fonte empacotada e manifests
coerentes. A versão distribuída é `<versão-base>-main.g<SHA completo>`; a base do
manifest de origem continua sendo SemVer estável. A versão única evita colisões no
cache; o catálogo seleciona o SHA exato, sem depender de ordenação de versões.

## Promoção Git

Cada publicação prepara dois commits na branch `plugin-release`:

1. Payload completo em `plugins/image-production/`, bundle separado dos agentes
   em `agent-bundle/` e `release.json` com versão, commit de origem e SHA256 de
   todos esses arquivos.
2. Marketplace `image-production-local` em `.agents/plugins/marketplace.json`,
   cuja entrada `git-subdir` fixa o SHA do primeiro commit.

Um único push normal promove os dois; a `main` não recebe arquivos gerados. O
histórico da branch preserva versões anteriores. Não há force push, PAT ou
publicação de assets que o Codex não saiba instalar. Apenas o job publicador tem
`contents: write`; ele usa o `GITHUB_TOKEN` e um helper `gh` fornecido pelo ambiente
da etapa, sem gravar credenciais na configuração do Git.

O publicador serializa promoções, verifica a `main` remota antes e depois do build
e recusa uma execução ultrapassada. Repetir um commit já publicado é um no-op.
Falha de preparação ou de push mantém a referência publicada anterior. Uma mudança
de `main` imediatamente após a última verificação só pode ser reconciliada pela
execução seguinte; a promoção do catálogo e do payload permanece atômica.

Para diagnóstico local, com as dependências de desenvolvimento instaladas:

```sh
python scripts/release_plugin.py prepare --sha HEAD --output /tmp/image-production-release-check
python scripts/release_plugin.py verify --path /tmp/image-production-release-check
```

O destino deve estar ausente. A preparação usa o commit, portanto alterações sem
commit não entram nesse teste. `publish --sha <SHA>` altera a branch remota e fica
reservado ao fluxo de publicação autorizado. Uma execução manual do workflow
valida, mas não publica; para repetir uma publicação que falhou, reexecute o run
de push da `main`, desde que seu commit continue sendo a ponta da branch.

## Instalação e atualização local

Depois que a branch de distribuição existir:

```sh
python3 scripts/update_plugin.py
```

Esse comando exige Git, Codex CLI compatível e acesso ao repositório. Busca e
verifica a release, adiciona o marketplace Git pela URL HTTPS canônica, executa
`marketplace upgrade` e instala com `plugin add`. Confere versão, inventário e
hashes no caminho retornado pelo Codex; não escreve diretamente no cache. Mantém
o nome `image-production-local`, inclusive ao migrar do marketplace local. Se
uma nova publicação acontecer entre busca e instalação, a divergência de versão
interrompe a verificação: repita o comando quando a publicação terminar.

O CLI gerencia somente a inscrição desse marketplace e a instalação do plugin.
Para voltar ao desenvolvimento local, execute novamente `codex plugin marketplace
add .` na raiz do checkout após o build local e reinstale o plugin. Para inspecionar
ou fixar uma versão anterior, use o SHA do commit de promoção preservado no
histórico, com `codex plugin marketplace add prof-ramos/image-production --ref
<SHA-da-promoção>`. O atualizador volta à branch publicada na próxima execução.

Inicie nova sessão e confirme a descoberta da skill. Atualização dos arquivos não
comprova reload da sessão já aberta.

| Forma de uso | Atualização |
| --- | --- |
| Skill embutida | Acompanha o plugin verificado pelo atualizador |
| Skill do checkout | Acompanha Git; abrir nova sessão para descoberta |
| Cópia avulsa | Sincronização explícita, fora deste atualizador |
| Agentes de projeto | Bundle separado; instalação e reconciliação manual |

O bundle dos agentes inclui os TOMLs, configuração de exemplo e ponteiro para o
commit de origem. Preserve a configuração local e reconcilie somente as seções
necessárias, conforme [portabilidade](../../README.md#portabilidade-e-especialistas).
Ele depende da skill e das referências do projeto de origem; não é um instalador
autônomo. Instalar o plugin não ativa os sete papéis em outros projetos.

Formato e comandos de distribuição: [documentação oficial OpenAI](https://developers.openai.com/plugins/build/plugins).
