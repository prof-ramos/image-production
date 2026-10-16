# Relatório de reaproveitamento

Data: 16/10/2026. Referências e SHAs no inventário 01; arquitetura no documento 03.

## O que já existe e será usado

| Componente | Origem | Uso na image-production | Limite |
|---|---|---|---|
| Geração, edição e transparência integradas | B02 imagegen + B04 codex | Aplicar a skill instalada e a ferramenta exposta | Não reimplementar; não fixar parâmetros API no contrato integrado |
| Estrutura SKILL.md e divulgação progressiva | B03 Skill Creator, A01 | Nome/descrição, corpo conciso, referências carregadas quando úteis | Metadados UI opcionais; não são registro de ferramenta |
| Preparação → geração → inspeção → montagem | B01 Hatch Pet | Adaptar separação probabilística/determinística e validação | Não copiar atlas, nomes de estados, chroma key ou subagentes como obrigação universal |
| Prompt estruturado e invariantes | B02, C03 Academy | Objetivo, sujeito, referência com papel, texto literal, restrições | Prompt não garante cor, texto ou tamanho exato |
| Eventos e manifesto final | A02 e CLI local | JSONL para execução, schema para resposta final | Validar arquivos independentemente do relato do modelo |
| Rubrica com bloqueios essenciais | C01 Image Evals | Adaptar correção, marca, composição e preservação | Escala 0/1/2 é nossa proposta, não padrão oficial OpenAI |

## O que precisa ser desenvolvido

| Componente novo | Fonte de inspiração | Por que não copiar diretamente | Evidência exigida |
|---|---|---|---|
| Intake breve de brand kit/brief | B02 + C03/C04 | Imagegen é geral; marketing não cobre todos usos | Brief normalizado sem invenções |
| Registro de referências, prompts e variantes | B01 + A02 | Contrato pet é especializado | Manifesto rastreável por run/artefato |
| Cópia segura e nomes versionados | B01 + política imagegen instalada | Pastas de pets não são saída de produção | Sem sobrescrita; hash preservado |
| Inspeção de formato/alfa/dimensões | Utilitários B01 | Inspeção de atlas não atende imagem genérica | Fixtures opaca, transparente e corrompida |
| Revisão visual com gates | C01/C02 | Framework/grader API adicionaria dependência | Evidência por critério e comparação com referência |
| Tratamento de indisponibilidade | B02/B04 | Ferramentas variam por sessão/provider | Erro explícito e ausência de fallback silencioso |

## Exclusões deliberadas da primeira versão

- B05 imagegencam: usa GPT Image por API e hardware específico; aproveitar só tratamento conceitual de referência e revisão.
- B06 Photobooth demo: API/web, streaming e aplicação Next; não incorporar frontend/servidor para uma skill local.
- B07 codex-universal: imagem Docker Linux não é ambiente nativo Mac nem dependência necessária da skill.
- B08 CLIP: similaridade texto-imagem não comprova correção de texto, marca ou ausência de defeitos; dependência/pesos desnecessários agora.
- B09 GABRIEL e B10 evals: rubricas e rastreabilidade são úteis; os frameworks/API não são necessários ao primeiro fluxo.
- Grader automático complexo, OCR como aprovador único, instalação global e publicação: fora desta etapa de roteiro.

## Licenciamento e versões

Licenças confirmadas e SHAs estão em B01–B10. Ao incorporar código, manter avisos e cumprir Apache-2.0/MIT conforme o arquivo e sua licença específica; não presumir licença de datasets ou marcas. Referenciar conceitos não requer copiar grandes volumes de código/documentação. Revalidar origem e contrato na implementação, pois catálogo remoto, skill instalada, CLI e desktop podem evoluir separadamente.

## Conclusão técnica

O núcleo necessário já existe: geração integrada, formato de skill e padrões de organização. O desenvolvimento deve se concentrar no contexto específico de produção e na evidência de entrega. A integração não requer um novo gerador, um novo MCP nem uma dependência API obrigatória. A homologação completa ainda depende de executar a matriz 04 sobre a futura skill implementada.

Fontes principais: [imagegen](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/imagegen/SKILL.md), [Hatch Pet](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/hatch-pet/SKILL.md), [Skill Creator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md), [Image Evals](https://developers.openai.com/cookbook/examples/multimodal/image_evals).
