# Guia do desenvolvedor

Este projeto reúne uma skill de produção de imagens para Codex, sua distribuição
como plugin, especialistas de projeto e utilitários Python. O helper de artefatos
é offline; a geração depende da ferramenta integrada de imagens disponível na
sessão do Codex.

A publicação automática roda no workflow após os testes da `main`. A execução
hospedada e a instalação real foram verificadas em 20/10/2026; consulte as
[evidências de ativação](validation/automatic-release-20261020.md#ativação-remota-e-instalação-real--20102026).

## 1. Configuração

### Requisitos e checkout

- Git e Python 3.10 ou superior. O CI está configurado para Python 3.10 e 3.13.
- Codex com a skill `imagegen` e ferramenta integrada para produzir imagens.
  Isso não é necessário para executar os testes offline ou construir o pacote.
- CLI GitHub `gh`, somente para operações de issues, PRs e CodeRabbit.
- `uv` é uma alternativa opcional para ambientes Python isolados.

Os comandos deste guia usam shell POSIX, como macOS ou Linux. Se ainda não houver
checkout:

```sh
git clone https://github.com/prof-ramos/image-production.git
cd image-production
```

Use a branch que contém a implementação desejada. Mudanças que ainda estiverem
somente em um checkout local não estarão disponíveis em um novo clone remoto.
Antes de editar, confira `git status --short`, leia o [AGENTS.md](../AGENTS.md) e
consulte o [índice da wiki](wiki/index.md).

### Ambiente Python

Na raiz do checkout, crie um ambiente isolado:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

As dependências são Pillow, PyYAML e jsonschema, nas faixas definidas em
[requirements-dev.txt](../requirements-dev.txt). `.venv/` é ignorado pelo Git.
Para sair do ambiente, use `deactivate`. Como alternativa sem ativação de venv:

```sh
uv run --with-requirements requirements-dev.txt python -m unittest discover -s tests -v
```

A suíte não precisa de chave OpenAI, autenticação GitHub ou geração paga. O modo
integrado de produção também não usa uma chave API configurada por este repo.

### Plugin e especialistas

Depois de conferir o checkout e a disponibilidade do CLI Codex:

```sh
python3 scripts/build_plugin.py
codex plugin marketplace add .
codex plugin add image-production@image-production-local
```

O pacote é gerado em `work/plugin-dist/image-production`. Abra uma nova sessão
para conferir a descoberta da skill. Para usar apenas a skill do checkout, inicie
uma sessão neste projeto e solicite `$image-production`.

Os sete papéis em `.codex/agents/` são configuração de projeto; instalar o plugin
não os instala automaticamente em outros projetos. Siga as
[instruções de instalação dos especialistas](../.agents/skills/image-production/references/specialist-installation.md)
para copiar definições e mesclar a configuração sem substituir regras locais.
Há seis papéis de imagem: quatro obrigatórios na produção coordenada e dois
opcionais. O papel geral `chief_of_staff` orienta trabalhos longos e com várias
etapas, conforme [coordenação do projeto](agents/chief-of-staff.md). A presença
dos arquivos não comprova ativação nativa; confira os papéis em uma sessão nova.

### GitHub e memória local

Para trabalhar com GitHub, verifique a autenticação antes de operações remotas:

```sh
gh auth status
gh repo view prof-ramos/image-production --json nameWithOwner,visibility,url
```

Se necessário, use `gh auth login --hostname github.com` e conclua o fluxo de
autenticação. Não grave tokens no repositório. O App CodeRabbit e o acesso do
serviço ao repo são configurações separadas do login no `gh`.

A wiki é versionada. O índice auxiliar OptMem em `.local/` não acompanha clone
ou plugin; sua instalação é opcional para executar testes, mas o coordenador deve
seguir o [procedimento de memória local](wiki/memoria-local.md) para seu fluxo.
Somente o coordenador escreve notas reais.

## 2. Estrutura do projeto

| Caminho | Responsabilidade |
| --- | --- |
| `.agents/skills/image-production/SKILL.md` | Entrada canônica da skill |
| `.agents/skills/image-production/scripts/inspect_artifacts.py` | CLI offline de reservas, coleta, revisão e integridade |
| `.agents/skills/image-production/references/` | Contrato, schemas, rubrica, catálogo e instruções condicionais |
| `.codex/agents/` e `.codex/config.toml` | Papéis e configuração dos especialistas |
| `.codex-plugin/plugin.json` | Manifest de origem e versão do plugin |
| `.agents/plugins/marketplace.json` | Marketplace local, apontando para o pacote gerado |
| `scripts/build_plugin.py` | Build da distribuição a partir da fonte canônica |
| `scripts/request_coderabbit.py` | Solicitação de revisão via comentário no PR |
| `scripts/export_coderabbit.py` | Coleta de feedback via GitHub CLI, somente leitura |
| `.coderabbit.yaml` | Configuração das revisões CodeRabbit |
| `tests/` e `tests/fixtures/` | Testes e simulação isolada do CLI GitHub |
| `.github/workflows/ci.yml` | Testes, preparação e publicação condicionada à `main` |
| `scripts/release_plugin.py` | Preparação, verificação e promoção Git da release |
| `scripts/update_plugin.py` | Atualização pelo Codex e conferência da instalação |
| `docs/agents/` | Regras de tickets, domínio e distribuição |
| `docs/reviews/` | Protocolo de revisão e triagem |
| `docs/wiki/` | Memória histórica com fontes e commits |
| `docs/validation/` | Evidências sanitizadas de verificações executadas |
| `docs/planning/` | Planejamento histórico; não prova implementação atual |
| `work/` | Pacotes e execuções locais; ignorado pelo Git |
| `.local/` | Estado local do OptMem; ignorado pelo Git |

## 3. Fluxo de desenvolvimento

### Alterar e verificar

1. Confirme a branch, as mudanças existentes e o escopo do pedido. Preserve trabalho
   anterior. Para começar uma tarefa nova a partir de uma base já conferida,
   `git switch -c nome-da-tarefa` cria uma branch local.
2. Edite a fonte canônica. Para mudar o comportamento da produção, compare a
   [skill](../.agents/skills/image-production/SKILL.md), o
   [contrato](../.agents/skills/image-production/references/run-contract.md), os
   schemas e os testes. Para papéis, consulte o
   [playbook](../.agents/skills/image-production/references/agent-playbook.md).
3. Reproduza defeitos com um teste pertinente. Teste comportamentos observáveis;
   use o stub de `gh` para cenários remotos, mantendo testes offline.
4. Execute os testes afetados durante o trabalho; ao concluir, rode a suíte completa,
   o build e `git diff --check`.
5. Confira o diff e os arquivos selecionados antes de fazer commit. Registre
   aprendizados duráveis na wiki com data, fonte e `repo@commit`.

Apenas o coordenador altera o manifesto de uma execução de imagem. Uma geração
por vez, revisões técnica e visual independentes para o mesmo SHA-256 e o limite
cumulativo de correções permanecem parte do contrato. Os testes de código não
autorizam novas gerações nem a regeneração da caneca histórica.

### Abrir e revisar um PR

Prepare a descrição em arquivo UTF-8 e use o CLI:

```sh
git push -u origin HEAD
gh pr create --repo prof-ramos/image-production --title "Título da mudança" --body-file /caminho/descricao.md
```

Após criar o PR com sucesso, solicite revisão da branch atual:

```sh
python3 scripts/request_coderabbit.py --dry-run
python3 scripts/request_coderabbit.py
```

`--dry-run` consulta o GitHub e mostra o comentário sem enviar. A chamada seguinte
envia um comentário como a conta autenticada. Também é possível informar o número
do PR. O script impede duplicatas do mesmo head/conta, recusa drafts/PRs fechados,
espera uma hora entre pedidos no mesmo PR e limita a inicial mais dois pedidos
seguintes. Essas regras não representam a cota global da conta CodeRabbit.

Para acompanhar o CI e coletar o feedback de um PR, substitua `4` pelo número real:

```sh
gh pr checks 4 --repo prof-ramos/image-production
python3 scripts/export_coderabbit.py 4 > /tmp/image-production-pr4-coderabbit.json
```

Confira o código de saída da coleta antes de usar o arquivo. O redirecionamento
pode deixá-lo vazio em falhas. Siga o [protocolo CodeRabbit](reviews/coderabbit.md)
para confirmar achados, corrigir, testar e revisar o novo commit. `requested`
significa comentário enviado, não revisão concluída. Merge é uma ação separada.

### Atualizar a distribuição

Ao preparar uma nova versão instalável, atualize a versão no manifest de origem,
refaça o build e reinstale pelo fluxo do Codex. Preserve a identidade do plugin;
confira versão e conteúdo do pacote. Edite a fonte, não o cache instalado.

O CI prepara e valida a release em PRs; após um push aprovado na `main`, o job
publicador promove o marketplace Git na branch `plugin-release`. A instalação
local é separada: `python3 scripts/update_plugin.py` usa o CLI do Codex e verifica
versão e hashes. Cópias avulsas da skill e configuração de agentes exigem
atualização explícita. Consulte [publicação e atualização](agents/releases.md)
para ativação, recuperação e limites.

## 4. Abordagem de teste

Com a venv ativada, rode os mesmos comandos centrais do CI:

```sh
python -m unittest discover -s tests -v
python scripts/build_plugin.py
git diff --check
```

Para executar apenas os testes CLI durante uma alteração:

```sh
python -m unittest discover -s tests -p 'test_review_cli.py' -v
```

| Área | O que verifica |
| --- | --- |
| `test_artifacts.py` | Arquivos raster sintéticos, manifesto, integridade, reservas, retomadas e gates de revisão |
| `test_plugin_builder.py` | Conteúdo e substituição do pacote, falhas de build e rejeição de symlinks |
| `test_review_export.py` | Seleção e classificação do feedback exportado |
| `test_review_request.py` | Decisão de solicitação, duplicatas e limites |
| `test_review_cli.py` | Scripts completos com `gh` simulado: páginas adicionais, falhas de envio e mudança de head |
| `test_release.py` | Snapshots Git, proveniência, promoção, falhas e atualização pelo Codex isolado quando instalado |

O CI está configurado para PRs, pushes na `main` e execução manual, com Python
3.10 e 3.13 em Ubuntu. O [relatório de validação](validation/ci-review-cli-20261020.md)
registra 73 testes locais aprovados em cada uma dessas versões; esse número é uma
evidência histórica, não uma contagem fixa a preservar. A
[validação de publicação automática](validation/automatic-release-20261020.md)
registra 82 testes e a atualização nativa do plugin em ambiente isolado.

Validação de estrutura da skill com `quick_validate.py` é complementar e depende
da instalação local do Skill Creator; o script não é distribuído neste repo.
`actionlint` pode validar alterações no workflow. Ambos são verificações adicionais,
não etapas atualmente executadas pelo workflow de CI.

Testes sintéticos não comprovam qualidade visual, fidelidade de marca, texto
correto na imagem ou descoberta nativa dos agentes. Para homologação real, siga a
[rubrica](../.agents/skills/image-production/references/quality-rubric.md), preserve
candidatos/prompts e registre as revisões independentes no contrato de produção.

## 5. Solução de problemas

Para a adaptação Hermes, consulte a
[validação do provedor Codex](validation/hermes-codex-image-generation-20261022.md).
Ela registra o caso em que o login é reconhecido, mas um cooldown de outro
modelo bloqueia o gerador. Inclui correção local, geração real e limites da
validação; não fornece um patch instalável nem comprova operação no WhatsApp.

| Sintoma | Verificação e ação |
| --- | --- |
| `ModuleNotFoundError` para PIL, yaml ou jsonschema | Ative `.venv`, confira `python --version` e reinstale `requirements-dev.txt` nesse ambiente, ou use o comando com `uv` |
| `gh` ausente ou HTTP 401 | Confira `gh --version` e `gh auth status`; restaure a autenticação CLI antes de repetir. Não migre silenciosamente para UI |
| Plugin não encontrado | Execute o build, confirme `work/plugin-dist/image-production`, confira o marketplace com `codex plugin marketplace list` e instale novamente |
| Plugin mostra comportamento antigo | Confira a fonte e a versão do manifest, refaça o build/reinstalação e abra nova sessão; não edite o cache |
| Especialista não aparece | Confira `.codex/config.toml`, os arquivos apontados e a confiança do projeto revisado. Reinicie a sessão; use carga explícita somente como documentado, sem reduzir sandbox ou aprovações |
| Ferramenta de imagem indisponível | Registre o bloqueio da produção e confirme as capacidades da sessão. O helper offline não substitui o gerador e não ativa fallback API |
| Build rejeita symlink ou arquivo inesperado | Confira o caminho indicado e os arquivos de origem/destino. Preserve o pacote anterior; não contorne a validação nem apague dados sem verificar sua origem |
| Helper informa manifesto ou hash inválido | Preserve os arquivos e execute `verify` conforme o contrato. Compare candidato, prompt e snapshots; obtenha novos pareceres se o candidato mudar |
| Limite de correções ou reserva consumida | Leia o ledger e o histórico. Tentativas canceladas também contam; não reinicie a identidade do asset para liberar orçamento |
| CodeRabbit não responde | Confira App, acesso ao repo, plano/cota e comentário enviado. Não faça disparos repetidos; envio não prova aceitação pelo bot |
| Script recusa outro pedido de review | Confira duplicata, estado do PR, intervalo e limite de rodadas. Não apague comentários para contornar a contagem |
| Envio de comentário falhou ou ficou incerto | Leia os comentários do PR antes de tentar novamente; pode ter havido entrega mesmo sem resposta de sucesso |
| Coleta exportada está vazia | Confira o código de saída. Falhas de acesso ou mudança de head descartam o relatório; arquivo vazio não significa aprovação |
| Publicação ausente ou falhou | Confira o job publicador do push na `main`, o SHA ainda na ponta e a permissão `contents: write`; reexecute o run correto após resolver a causa |
| Atualização diverge da versão esperada | Aguarde o término da publicação e repita `python3 scripts/update_plugin.py`; mantenha o cache sob gestão do Codex |
| Checks do CI ausentes | Confira se o workflow chegou à branch remota e se o evento foi disparado; use `gh pr checks`/`gh run list`. Arquivo local não prova execução hospedada |
| OptMem ausente | Consulte a wiki e configure pelo procedimento documentado; o estado local não faz parte do plugin |

Para inspecionar o helper sem alterar uma execução:

```sh
python .agents/skills/image-production/scripts/inspect_artifacts.py --help
python .agents/skills/image-production/scripts/inspect_artifacts.py verify --help
```

Antes de compartilhar um diagnóstico, remova credenciais e dados sensíveis.
Registre comando, versão, commit, resultado observado e limitações. Artefatos
brutos ficam fora do Git; evidências sanitizadas podem entrar em `docs/validation/`.
