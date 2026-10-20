# Agentes reutilizáveis — 2026-10-20

Base observada: `prof-ramos/image-production@3c08fdd5e104af5a69cc087072ff40af6e332219`.
As alterações deste relatório são locais sobre essa base, ainda sem commit.

Foram acrescentados `image_director` e `image_eval_designer`, opcionais, aos quatro
papéis existentes. O coordenador encaminha tarefas conforme o playbook; workers
não criam descendentes. Preservados o escritor único, dois workers no máximo,
geração sequencial, revisão independente por SHA-256 e limite acumulado de correções.
Plugin local incrementado para 0.1.5; não reinstalado nem publicado.

## Verificações executadas

- `uv run --with-requirements requirements-dev.txt python -m unittest discover -s tests -v`: 57 testes passaram, 3,184 segundos.
- Parse dos seis TOMLs por `tomllib`: todos os caminhos registrados existem e cada definição contém `developer_instructions` não vazias, sem sobrescritas de modelo ou permissões.
- `python3 scripts/build_plugin.py`: pacote reconstruído em `work/plugin-dist/image-production`.
- `git diff --check`: sem problemas de whitespace.
- Revisão independente por subagente: leitura integral dos dois novos TOMLs, diff e referências; sem bloqueio. Corrigida ambiguidade de fallback quando falta o próprio arquivo opcional.

## Limites

Testes existentes verificam o helper e o build, não a qualidade de imagens nem o
cumprimento integral das instruções por modelos. Novos papéis avaliados por leitura
e simulação de carga explícita; descoberta/execução nativa não comprovada nesta
sessão. Nenhuma chamada de geração, API, instalação global ou mudança de permissões.
Papéis continuam separados da instalação do plugin; README explica sua cópia e
mescla manual em outros projetos. Os cenários do avaliador são um protocolo,
não resultados de benchmark visual.

## Revisão com Plugin Creator e Skill Creator — 2026-10-20

Sobre a mesma base e alterações locais, a revisão moveu apenas as instruções
de instalação/portabilidade do corpo da skill para
`references/specialist-installation.md`, com ponteiro condicionado à instalação.
Preservados controles operacionais, política de descoberta e catálogo.

- `quick_validate.py` oficial executado via runtime isolado com PyYAML: `Skill is valid!`.
- Build 0.1.5 reconstruído após a edição.
- Manifestos portátil e de compatibilidade conferidos quanto a identidade, versão,
  apresentação, schema e limite de 30 caracteres do subtítulo.
- Todos os links Markdown locais do pacote resolvidos dentro do pacote; arquivos
  distribuídos conferidos byte a byte contra a fonte canônica.
- `git diff --check` passou. Sem mudança de código executável nesta revisão; os
  57 testes anteriores não foram repetidos. Não houve reinstalação, publicação
  ou nova validação de descoberta nativa.
