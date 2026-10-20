# Correções da revisão do PR #4 — 2026-10-20

O PR foi marcado pronto para revisão em 20/10/2026. O Codex revisou `prof-ramos/image-production@e7832a9f39ea34dbb1491df4f0894397d51cd5f2` e publicou três apontamentos confirmados. O CodeRabbit ignorou a revisão porque a base é uma branch diferente da padrão; seu status verde não foi tratado como aprovação.

## Apontamentos e comportamento corrigido

- [P1 — preservar ambos os pareceres](https://github.com/prof-ramos/image-production/pull/4#discussion_r4323687701): novas execuções guardam `technical` e `visual` separadamente, com `candidate_sha256` e identificadores distintos de revisor. Ambos precisam passar para os bytes atuais; o último parecer favorável não substitui o gate do outro papel. Revisões anteriores permanecem no histórico. Execuções legadas continuam legíveis como histórico; uma nova revisão migra conservadoramente para o gate duplo. Identificadores são declarações locais, não atestação de autoria independente.
- [P2 — orçamento entre execuções](https://github.com/prof-ramos/image-production/pull/4#discussion_r4323687713): `prepare` exige uma chave estável por variante e reserva a tentativa antes de gerar. O ledger privado `.lineages/` no root mantém uma tentativa inicial mais duas correções. Uma chave existente exige `--continue-from`; a continuação herda ou seleciona chaves existentes e não permite renomeá-las. Cada asset/run admite um candidato. Cancelamento e falha não reembolsam a reserva. Copiar apenas a pasta do run não preserva o orçamento: conservar o root/ledger. Uma chave deliberadamente diferente não pode ser reconhecida semanticamente pelo helper; o protocolo exige reutilizar a identidade real do asset.
- [P2 — symlinks na fonte](https://github.com/prof-ramos/image-production/pull/4#discussion_r4323687720): o builder rejeita symlinks na raiz, nos ancestrais e no conteúdo da skill antes de escrever no destino. Arquivos, diretórios e links quebrados estão cobertos; uma rejeição preserva o build anterior.

Não houve nova geração ou alteração de evidências históricas do catálogo/piloto. A skill, papéis e README foram alinhados à nova CLI; o [contrato](../../.agents/skills/image-production/references/run-contract.md) explica os campos e a migração. O plugin local passa à versão 0.1.2.

## Verificação

As reproduções dos três apontamentos falharam antes das correções e passaram depois. A revisão independente também reproduziu entradas malformadas que inicialmente causavam traceback; `review=[]`, assets contendo `null` e chaves de tipo inválido passaram a falhar com JSON/exit 2 sem alterar o manifesto. Não há repetição nem relaxamento da homologação visual histórica.

Validação final: `uv run --offline --with-requirements requirements-dev.txt python -m unittest discover -s tests -v` passou com **47 testes** (44 do helper e três do builder). O validador oficial da skill, parse TOML dos quatro papéis/configuração e revisão independente dos casos malformados passaram. O plugin 0.1.2 foi reconstruído e reinstalado pelo CLI oficial; os nove arquivos canônicos instalados conferiram byte a byte. Um app-server novo com cwd `/tmp` descobriu a skill habilitada na versão instalada. O SHA256 do catálogo permaneceu `9d34a7e80c7913bd059998010a1901ceacc0046f8e842c670449c080be5893dd`. O check incremental de whitespace cobre os arquivos alterados; as fontes verbatim anteriores preservam seus bytes e quebras Markdown.

## Segunda revisão do Codex

A revisão solicitada em 20/10/2026 sobre `prof-ramos/image-production@fdeda9ba315d3d88fa2cf1d56b4e70857ccb2eed` publicou um [P2 sobre ancestrais do destino](https://github.com/prof-ramos/image-production/pull/4#discussion_r4324168206). A reprodução demonstrou que `work` ou `work/plugin-dist` como symlink podia redirecionar o build e substituir arquivos externos. O builder verifica lexicalmente o destino e cada ancestral até ROOT antes de percorrer, criar ou remover conteúdo. Dois novos testes cobrem esses ancestrais com links válidos/quebrados e comprovam preservação dos bytes externos.

Validação: `uv run --python 3.12 --with-requirements requirements-dev.txt python -m unittest discover -s tests -v` passou com **49 testes** (44 helper e cinco builder). O runtime padrão mudou e não tinha o cache de dependências; uv utilizou Python 3.12 e instalou as dependências de testes. Nenhuma API ou geração de imagem foi executada. O plugin foi atualizado para 0.1.3; a skill e o catálogo canônicos permaneceram inalterados nesta correção.

## Terceira revisão e preservação transacional do build

A revisão de `prof-ramos/image-production@a16750ddc5e1d7300748616b685783973307b83f` apontou [P2 de fonte ausente ou irregular](https://github.com/prof-ramos/image-production/pull/4#discussion_r4324208273): o build anterior podia ser removido antes da falha de cópia. A validação exige diretório e `SKILL.md` regular, preserva as rejeições de symlinks e recusa destino que seja arquivo. A construção copia a skill e escreve os dois manifests em staging no mesmo parent; somente então troca o pacote, preservando backup recuperável e restaurando-o se a publicação falhar. Assim, erro de cópia parcial ou manifesto não destrói o pacote anterior. A fonte canônica permanece intacta.

Validação final: **57 testes passaram** (44 helper e 13 builder) com `uv run --python 3.12 --with-requirements requirements-dev.txt python -m unittest discover -s tests -v`. As regressões cobrem fonte ausente/arquivo/vazia, destino irregular, symlinks, cópia parcial, manifesto inválido, rollback da troca e publicação completa sem resíduos. O plugin foi atualizado para 0.1.4; os nove arquivos canônicos distribuídos permanecem iguais à fonte. Não houve nova geração, API de imagens ou alteração do catálogo.
