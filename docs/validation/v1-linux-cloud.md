# v1 — repetição em Linux/cloud (19/10/2026)

Esta rodada **não** foi executada no Mac. O registro original continua em [v1-macos.md](v1-macos.md) e não foi reescrito. Nenhuma imagem foi gerada ou reavaliada aqui. As amostras `docs/validation/assets/initial.png` e `docs/validation/assets/edit.png` seguem com veredito visual `needs_revision` por halo, como em [evidence.json](evidence.json).

## Ambiente

- Ubuntu 24.04.5 LTS, Linux 6.12.94+ x86_64 (agente em nuvem).
- Python 3.12.3, Pillow 12.3.0, PyYAML 6.0.3, no venv isolado `/tmp/ip-venv`.
- `uv` não estava instalado. O venv foi criado com `python3 -m venv` e `pip install -r requirements-dev.txt`. O Python global do sistema não foi alterado.
- Sem `OPENAI_API_KEY`, Image API, SDK, MCP próprio, navegador ou instalação global da skill.

## O que esta rodada verificou

O review do Codex na PR #1 tinha um achado P2 aberto: `argparse` escrevia o usage em texto e saía antes do handler JSON. Flags obrigatórias ausentes, escolha inválida e subcomando desconhecido agora saem com `{"error": "..."}` em stderr, stdout vazio e código 2. `--help` continua texto e código 0. O contrato em `references/run-contract.md` descreve esse formato.

Exemplos reais desta máquina:

```text
collect --run /tmp/example
→ exit 2
→ {"error": "the following arguments are required: --source, --prompt, --name"}

nope
→ exit 2
→ {"error": "argument command: invalid choice: 'nope' (choose from 'prepare', 'collect', 'review', 'verify', 'status')"}

prepare ... --surface nope
→ exit 2
→ {"error": "argument --surface: invalid choice: 'nope' (choose from 'desktop', 'exec')"}
```

## Suíte

```sh
/tmp/ip-venv/bin/python -m unittest discover -s tests -v
```

Resultado: **16 testes, OK**, em 0.513s. A saída integral, com o log antigo do Mac preservado acima, está em [unit-tests.txt](unit-tests.txt). Os dois testes novos cobrem falhas de parsing (flags ausentes, escolha inválida, subcomando desconhecido, comando ausente, argumento não reconhecido) e a ajuda em texto.

## Validador de skill

`quick_validate.py` do Skill Creator, árvore fixada no inventário (`openai/skills` `49f948faa9258a0c61caceaf225e179651397431`), executado no mesmo venv:

```sh
/tmp/ip-venv/bin/python quick_validate.py .agents/skills/image-production
```

Resultado: `Skill is valid!` (exit 0). O validador confere o frontmatter; não exercita geração nem a rubrica visual.

## Fora desta rodada

Não houve nova sessão Codex, `imagegen`, edição de arquivo local nem inspeção visual. O issue #2 continua com a homologação P1 e a integração P2 em aberto:

- T05 geração nova só com referência, T07 duas variantes AI independentes, T08 marketing, T09 produto real, T10 institucional.
- T04/T06 nova estratégia de recorte sem halo; as amostras atuais permanecem `needs_revision`.
- T13 falha real recuperável da ferramenta, sem fallback de API.
- Invocação por outro agente, descoberta em perfil limpo, empacotamento, pasta `~/Pictures/ChatGPT-Assets/` e decisão de implantação.

Limites já descritos no relatório do Mac continuam valendo: um escritor por run, sem sandbox contra troca concorrente de diretório e sem recuperação transacional se o processo cair entre a cópia do candidato e o manifesto. Merge não foi feito nesta rodada.
