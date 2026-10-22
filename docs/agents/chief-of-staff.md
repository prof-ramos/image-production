# Coordenação do projeto

`chief_of_staff` adapta a skill `chief-of-staff` para trabalhos longos ou com
várias etapas neste repositório. O agente principal exerce o papel diretamente:
mantém o objetivo, acompanha entregas e integra o trabalho dos especialistas.
A definição reutilizável está em
[chief_of_staff.toml](../../.codex/agents/chief_of_staff.toml).

## Execução e continuidade

- Mantenha um plano curto com resultados esperados, responsáveis, dependências,
  evidências e bloqueios. Atualize-o quando uma descoberta mudar a próxima ação.
- Antes de delegar alterações, registre HEAD, referência remota após `fetch` e
  alterações locais. Reconcilie divergências com a memória e use um worktree
  isolado quando necessário para preservar trabalho anterior.
- Delegue execução e revisão em tarefas delimitadas, com propriedade de arquivos
  e ponteiros para requisitos, código e decisões. Avise que outros agentes podem
  editar o checkout; preserve seu trabalho. Use até dois workers simultâneos,
  respeitando limites menores do host. Workers devolvem resultados ao principal,
  sem criar descendentes.
- Para tarefas que alterem o mesmo arquivo, atribua um único escritor ou aplique
  as mudanças sequencialmente. Outros workers podem analisar, revisar e propor
  patches em paralelo.
- Resolva decisões técnicas triviais diretamente; concentre a delegação em
  tarefas concretas que se beneficiem de contexto próprio ou revisão independente.
- O principal integra resultados, verifica artefatos e mantém diálogo com o
  usuário. Um `chief_of_staff` chamado como subagente entrega apenas plano ou
  parecer ao principal; isso evita coordenadores concorrentes.
- Antes de executar, considere melhorias do ambiente que reduzam falhas na tarefa
  autorizada. Prefira verificações determinísticas para erros mecânicos e regras
  de revisão para decisões de julgamento. Mudanças proporcionais relacionadas
  cabem na tarefa; melhorias independentes ficam como propostas separadas.
- Encerre com o que foi entregue, evidências efetivamente verificadas e limites
  ou decisões pendentes. Preserve requisitos e autorizações já concedidos.

## Memória e agendas

Consulte o [índice histórico](../wiki/index.md) antes de decisões. Somente o
coordenador principal executa OptMem e escreve a wiki, conforme
[memória local](../wiki/memoria-local.md). Subagentes leem a wiki e retornam
descobertas com fontes. Acrescente fatos datados, com `repo@commit` para código,
preservando o histórico e marcando registros superados. Atualize páginas afetadas
e índice; mantenha credenciais e transcrições fora da memória.

Quando uma recorrência ajudar o objetivo e o host oferecer agendas, sugira uma
frequência e um resultado observável, como revisão de links e contradições da
wiki. A instalação do papel não cria metas persistentes, serviços ou agendas.
Criar uma agenda depende de solicitação ou autorização correspondente do usuário.

## Ativação e portabilidade

A seção `[agents.chief_of_staff]` em
[config.toml](../../.codex/config.toml) aponta para a definição. Para outro projeto,
copie apenas esse TOML e mescle a seção na configuração existente, preservando
modelos, autenticação, sandbox, aprovações e limites. O papel depende destes
documentos do projeto; ao transportá-lo, adapte os ponteiros ao destino.

Em uma nova sessão, verifique se o host expõe o papel nativo. A presença dos
arquivos não demonstra sua ativação nem execução contínua. Se houver apenas
subagentes genéricos, leia o TOML do papel atribuído e forneça integralmente suas
`developer_instructions`, registrando a carga explícita. Sem delegação, informe
a limitação e execute diretamente o que for possível dentro do escopo; não
registre trabalho de subagentes que não ocorreu.

## Relação com produção de imagem

Este é um papel geral de projeto, separado dos seis papéis de imagem. Não
substitui o contrato de `image_coordinator`: apenas ele escreve o manifesto,
com revisões técnica e visual independentes para o mesmo candidato. O principal
pode assumir a coordenação da execução de imagem lendo integralmente a definição
do coordenador e o contrato. Preserve o limite de dois workers, uma geração por
vez e o orçamento acumulado de correções. Para produzir imagens, leia a
[skill canônica](../../.agents/skills/image-production/SKILL.md) e o
[playbook](../../.agents/skills/image-production/references/agent-playbook.md).
