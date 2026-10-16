# Plano operacional — produção de imagens com assinatura ChatGPT, sem API paga

**Versão:** 1.0 · **Data:** 16/10/2026 · **Status:** planejamento complementar, não homologação de produção.

## 1. Objetivo e decisão

Estabelecer um fluxo rastreável de criação, revisão, armazenamento e utilização de imagens em projetos no macOS Apple Silicon (MacBook Air M3, 8 GB), empregando **somente recursos oficiais de imagem disponíveis na assinatura ChatGPT** e processamento local. Não exigir credenciais, orçamento, endpoints ou créditos da **OpenAI API de desenvolvedor**.

Este documento complementa [a arquitetura existente](03-arquitetura.md), [a matriz de homologação](04-implementacao-homologacao.md) e a implementação experimental do [PR #1](https://github.com/prof-ramos/image-production/pull/1). Não substitui o contrato técnico, a rubrica de qualidade nem os testes já registrados.

**Duas modalidades de geração:**

1. **Integrada, prioritária:** agente Codex autenticado pelo ChatGPT utiliza a ferramenta integrada por meio de `$imagegen`, quando efetivamente disponível naquela sessão. A skill `image-production` coordena o briefing, a entrega e a revisão; **não** implementa outro gerador nem chama a API. A execução técnica desse caminho foi demonstrada no Mac no PR #1, mas o aceite visual da amostra **falhou** (halo azul), permanecendo `needs_revision`.
2. **Assistida, contingência:** gerar/editar diretamente pelo ChatGPT Images, salvar o resultado pela interface oficial e importá-lo localmente. **Não declarar essa modalidade programática, automática ou já compatível com o manifesto do helper v1.** Exige rastreamento explícito de origem e possível adaptação do contrato antes de integrá-la à mesma rotina.

A ausência da ferramenta integrada ou o atingimento de limites deve resultar em estado **blocked** ou encaminhamento explícito à modalidade assistida, nunca em chamadas pagas de API ocultas.

## 2. Requisitos não negociáveis

- Nenhuma dependência de `OPENAI_API_KEY`, `CODEX_API_KEY`, SDK OpenAI, `/v1/images`, Responses API paga ou recarga de créditos.
- Nenhum fallback automático para serviço pago, provedor alternativo ou modelo local não aprovado.
- Nenhum uso de cookies exportados, HAR, tokens de sessão, endpoints privados do ChatGPT, Playwright/Selenium de extração ou mecanismo para contornar limites.
- Autenticação oficial por conta ChatGPT, observando permissões e controles já existentes; não alterar políticas de segurança e aprovação para desbloquear execução.
- Processamento local determinístico, de baixo consumo, sem Docker/VPS/banco de dados/servidor MCP próprios na versão inicial.
- Preservar originais, referências e prompts efetivamente enviados; jamais sobrescrever arquivo existente sem ação deliberada.
- Não publicar peças, conceder acesso a aplicativos, instalar globalmente ou assumir novos custos como efeito colateral dos testes.
- Ferramentas locais podem usar dependências de código aberto; "sem API" significa aqui **sem consumir a API de geração de imagens faturada separadamente**. As próprias interfaces oficiais e conectores têm comunicação de rede interna, fora do controle deste plano.

## 3. Componentes e responsabilidades

| Elemento | Papel | Decisão |
|---|---|---|
| ChatGPT Images | Geração/edição assistida | Oficial, incluído no acesso do plano aplicável |
| Codex + `$imagegen` | Geração integrada no agente | Preferencial se ferramenta da sessão estiver disponível |
| `image-production` | Compor brief, referências, execução e revisão | Preservar arquitetura do PR #1 |
| Helper Python + Pillow isolado | Arquivos, hashes, formatos, dimensões, alfa, manifesto | Offline; não gera imagens |
| Sistema de arquivos | Originais, variantes, histórico e entregas | Fonte principal de artefatos |
| Google Drive / ChatGPT Work | Integração oficial opcional, posterior | Não assumir capacidade automática de gerar/exportar binários |
| MCP para geração de imagem | Expor `generate_image` a clientes externos | **Fora de escopo:** não há interface oficial por assinatura homologada |

## 4. Organização dos arquivos

Raiz local sugerida, sem exigência de mudança nos projetos atuais:

```text
~/Pictures/ChatGPT-Assets/
  briefings/
  referencias/brandkits/
  importacoes-manuais/
  runs/
    <run-id>/
      inputs/
      work/
      final/
      manifest.json
  aprovadas/
  entregas/
```

As subpastas de cada `run-id` devem seguir o contrato existente do helper. `manifest.json` é a fonte autoritativa de estado, prompts, hashes, arquivos, revisão e erros. Um índice CSV/Markdown de consulta pode ser derivado futuramente; **não manter dois registros independentes e divergentes**. Arquivos em `aprovadas/` e `entregas/` são cópias explícitas, jamais substituições dos originais.

Convenção de nome de entrega: `AAAA-MM-DD_projeto_peca_LxA_vNN.ext`; a indicação `final` somente após aceite visual documentado. Evitar renomear arquivos internos de um run de forma que invalide os hashes.

## 5. Fases de implantação e evidências

| Fase | Execução prevista | Evidência mínima | Condição para avançar |
|---|---|---|---|
| **F0 — Baseline** | Revisar o PR #1, estado dos testes T01–T15 e limitações reais; não presumir merge | SHA/PR, relatório de validação, pendências visuais | Diferenciar código proposto, funcionalidade testada e código em `main` |
| **F1 — Capacidades oficiais** | Confirmar login Codex pela assinatura, presença da ferramenta integrada e recurso ChatGPT Images | Versões observadas e teste real de ferramenta/arquivo, sem segredos nos logs | Não ativar API nem novos créditos |
| **F2 — Ambiente local** | Preparar diretórios com permissões apropriadas e execução isolada do helper | Árvore criada, paths confinados, validação de entrada | Originais intactos e nenhuma infraestrutura residente desnecessária |
| **F3 — Produção integrada** | Brief → `$imagegen` → arquivo retornado → coleta → revisão | Prompt exato, origem, hash, pixels decodificáveis, manifesto | Revisão visual por critério; arquivo técnico válido não implica aprovação |
| **F4 — Contingência assistida** | ChatGPT Images → Salvar → importação local com indicação da origem | Arquivo original, prompt/brief documentado e rastreabilidade | Não falsificar `mode=built-in`; adaptar o contrato antes de usar o helper v1 nesse modo |
| **F5 — Homologação** | Reexecutar matriz existente e cenários institucionais | Resultados observados e evidências, incluindo falhas | Todos os gates técnicos e visuais críticos aprovados |
| **F6 — Integrações opcionais** | Testar compartilhamento oficial no Google Drive/Work, uma operação por vez | Confirmação de capacidades de leitura/escrita e destino real | Nenhuma promessa de exportação autônoma sem teste |

O PR #1 registra **14 testes locais aprovados** e geração integrada real no Codex CLI 0.163.0, mas **não** homologa a revisão visual; o halo persistiu inclusive após edição. [Evidência de homologação parcial](https://github.com/prof-ramos/image-production/blob/feat/image-production-v1/docs/validation/v1-macos.md). Até a revisão do PR, esses recursos não devem ser descritos como já disponíveis em `main`.

## 6. Operação cotidiana

**Fluxo integrado (prioritário):**

1. Receber o objetivo, o público, uso, formato, texto literal, referências, brand kit e restrições.
2. Verificar a ferramenta de imagem **na sessão real**, sem inferir disponibilidade somente por configuração ou versão instalada.
3. Criar run via contrato vigente, guardar inputs/hashes e registrar o prompt de cada variante antes da chamada.
4. Usar `$imagegen` com a ferramenta integrada oficial; usar exclusivamente o caminho de saída realmente retornado.
5. Coletar sem sobrescrever, inspecionar pixels, dimensões, transparência e fazer inspeção visual em tamanho de uso.
6. Registrar notas e evidências por critério; se existir defeito material, marcar `needs_revision`, não `approved`.
7. Somente encaminhar para publicação/entrega após revisão e aprovação adequadas; não publicar automaticamente.

**Fluxo assistido:** solicitar imagem no ChatGPT Images, revisar, usar o comando oficial Salvar e registrar o arquivo na pasta de importações. Enquanto o contrato do helper não incorporar modo manual com proveniência correta, manter esse percurso separado dos runs integrados; processamento não destrutivo de arquivos continua permitido.

**Identidade institucional:** quando o material for da ASOF, utilizar o brand kit fornecido como fonte canônica, conferir nomes e informações, referir-se à **Carreira de Oficial de Chancelaria** (não "categoria"), preferir **Serviço Exterior Brasileiro** e não utilizar a expressão "diplomacia" em peças da associação. Não inventar logotipos, fotografias, dados ou posicionamentos oficiais.

**Formatos de entrega previstos:** 1080×1080, 1080×1350, 1080×1920 e tamanho livre conforme projeto. Preferir proporção correta desde o briefing. Não esticar ou recortar elementos críticos para alcançar dimensões; quando a ferramenta integrada não garantir saída exata, registrar resolução recebida e tratar o redimensionamento como etapa de entrega, sem alterar o original.

## 7. Matriz mínima de aceite complementar

A [matriz T01–T15](04-implementacao-homologacao.md) permanece a referência principal. Acrescentar estes critérios operacionais, sem substituir aqueles:

| ID | Teste | Resultado exigido |
|---|---|---|
| A01 | Geração com assinatura, sem API | Evidência de ferramenta integrada e imagem real, nenhuma chamada/fallback de API de desenvolvedor |
| A02 | Falta de ferramenta, limite ou falha | `blocked`/`failed` com motivo sanitizado; nenhuma geração paga automática |
| A03 | Integridade | PNG/JPEG/WebP decodifica, hash confere, original não sobrescrito |
| A04 | Transparência | Alfa real e inspeção sobre fundos claro/escuro; halos explícitos reprovam |
| A05 | Brand kit e textos literais | Revisor confere marca, texto, hierarquia e fatos no tamanho de publicação |
| A06 | Duas variantes reais | Prompts, arquivos, hashes e revisões independentes |
| A07 | Reentrada e falhas | Run retomável, corrupção/arquivo ausente detectados, sem destruição prévia |
| A08 | Modo assistido | Origem ChatGPT Images declarada; nenhum manifesto afirma falsamente geração CLI |
| A09 | Transferência externa opcional | Só marcar "comprovada" quando arquivo chegar ao destino e integridade for verificada |
| A10 | Isolamento e sigilo | Nenhum cookie, chave, log sensível ou referência privada divulgado no GitHub |

Critérios visuais devem ser inspecionados por humano antes de aprovação institucional; a rubrica pode auxiliar, mas não validar fatos, marcas ou halos somente por metadados. O teste **T14 de MCP** permanece não aplicável à v1 sem MCP gerador: isso não prova compatibilidade MCP externa.

## 8. Limites, riscos e tratamento

- **Não existe contrato oficial confirmado de `generate_image(prompt)` exposto a clientes MCP externos debitando a assinatura.** Não projetar uma camada fictícia para isso.
- **ChatGPT Work / conectores:** gatilhos e ações autorizadas não provam geração e transferência binária autônomas; testar ponta a ponta antes de incorporá-las ao fluxo.
- **Assinatura/cotas:** variarão conforme plano, sessão e regras do produto; não prometer imagens por janela, latência, tamanho exato ou modelo interno específico.
- **Credenciais:** não copiar cookies, sessões ou arquivos HAR; não publicar dados sensíveis e não mudar autenticação existente.
- **Uso de disco:** preservar originais e versões; definir retenção/backup apenas com regra de negócio aprovada.
- **Segurança de caminhos:** recusar path traversal e symlinks fora da área permitida; não prometer proteção contra processos hostis concorrentes não cobertos pelo helper.
- **Custos:** nenhuma API OpenAI paga; caso nova ferramenta oficial peça cobrança adicional, interromper e solicitar autorização antes de configurar.
- **Qualidade:** saída com alfa real ainda pode ter bordas inadequadas; registrar falha visual e evitar publicar automaticamente.

## 9. Entregáveis e definição de concluído

- Documentação clara das duas modalidades (integrada e assistida), sem confundir seus níveis de automação.
- Skill e helper offline revisados, com matriz técnica reproduzível e relatório de limitações.
- Diretórios e manifestos consistentes, cópia não destrutiva, registro de prompts, hashes e revisões.
- Pelo menos um caso institucional completo revisado com brand kit e um caso de transparência com bordas aprovadas.
- Prova negativa operacional de que não houve fallback automático para API paga.
- Instalação global, publicação automática, integração remota e novos custos **fora do aceite inicial**.

**Estado em 16/10/2026:** plano registrado; a implementação experimental e seus testes estão no [PR #1](https://github.com/prof-ramos/image-production/pull/1), ainda não incorporado à `main`. A geração integrada já foi observada, mas a amostra visual permaneceu rejeitada; o presente documento não afirma implantação ou homologação final.
