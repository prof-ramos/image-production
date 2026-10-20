# Descoberta nativa dos sete agentes — 20/10/2026

Em 2026-10-20, com `codex-cli 0.163.0`, foi confirmada a descoberta nativa
das sete definições do projeto na base
`prof-ramos/image-production@bea9f975e6d8a2d8813cd7e49432d93472ee3efa`.
A verificação usou a configuração existente e uma sessão nova, efêmera e
restrita a leitura. Não alterou confiança, modelo, autenticação ou permissões.

## Evidência observada

O protocolo local `codex app-server --stdio`, por `initialize` seguido de
`config/read` com `cwd` do repositório e `includeLayers: true`, retornou as sete
definições efetivas. A camada `.codex` do projeto apresentou
`disabledReason: null`.

Uma sessão independente de `codex exec` identificou `agent_type` como seletor
nativo da ferramenta de criação de subagentes. Seu schema enumerou estes nomes:

- `chief_of_staff`
- `image_coordinator`
- `image_director`
- `image_eval_designer`
- `image_producer`
- `image_technical`
- `image_visual`

Os sete nomes coincidiram entre configuração efetiva e schema exposto. O schema
também apresentou os papéis genéricos `default`, `explorer` e `worker`.

## Reprodução da inspeção de schema

Execute na raiz do checkout, preservando a configuração existente:

```sh
codex exec --ephemeral --sandbox read-only --json \
  'Diagnóstico read-only de descoberta nativa. Não leia arquivos, não execute shell, não use ferramentas, não crie agentes, não gere imagens e não altere nada. Olhe somente o schema de ferramenta de criação de subagentes disponível na sua sessão nova. Informe JSON com campo native_role_selector (nome do parâmetro que seleciona papel ou null) e available_roles (valores literais de papéis nativos enumerados no schema). Não deduza papéis do AGENTS.md nem de arquivos.'
```

O ensaio original acrescentou `-o` para salvar a resposta final no diretório
temporário abaixo. A sessão diagnóstica respondeu sem chamar ferramentas.

## Artefatos locais e limites

Evidências sanitizadas temporárias do ensaio, sem credenciais ou configuração
privada, ficaram em `/tmp/image-production-native-seven-20261020/`:

| Arquivo | SHA-256 |
| --- | --- |
| `effective-config-sanitized.json` | `a0a5fb5695549eadf8812fcee04f2910208dc0b5afecbfed2ad61a2e3bf5bc46` |
| `schema-last.json` | `6670a5fc24fe8929715e118e0b2eb5b842f5d8aa1e5a7dc48b4777f27bb18f70` |
| `schema-events.jsonl` | `d0ca5be622d0fca22aafb2a9634cc17cd872a79df8d80c85265f2047aee2f419` |

`report.json` no mesmo diretório resume comando, versão, commit e resultados.
Arquivos em `/tmp` são evidências locais transitórias e não acompanham o clone.

Esta verificação comprova configuração efetiva e descoberta no schema nativo
da sessão nova. Não ensaiou dispatch dos sete papéis, execução de suas
instruções, geração de imagens ou qualidade visual. Nenhum subagente foi criado
pelo diagnóstico. A inspeção não utilizou carga explícita dos TOMLs como
substituto de descoberta nativa. O resultado é específico à versão e à base
indicadas; não homologou hosts futuros.

O [relatório anterior de portabilidade](specialist-portability-20261020.md)
preserva o canário histórico de execução de `image_technical`; esse resultado
histórico não foi ampliado para execução dos sete agentes neste ensaio.
