# Coordenação reutilizável do projeto

Em 2026-10-20 o usuário solicitou adicionar a skill `chief-of-staff` ao AGENTS.md
ou criar um agente fixo equivalente. Sobre a base
`prof-ramos/image-production@f7f16a151cd6b961b92d684c537afebef640fe7a`, foram feitas
alterações locais ainda sem commit: definição `.codex/agents/chief_of_staff.toml`,
registro em `.codex/config.toml`, ponteiro curto no AGENTS.md e documentação de
[coordenação](../agents/chief-of-staff.md). README e guia diferenciam o papel geral
dos seis papéis de imagem. Fonte: pedido do usuário nesta sessão e esses arquivos.

A adaptação mantém o principal como responsável direto, delegação proporcional,
memória histórica na wiki e OptMem escrito somente pelo root. Mantém modelo,
autenticação e permissões herdados, até dois workers e uma geração por vez.
A instalação não cria meta persistente, agenda ou serviço em segundo plano.
Subagente chamado com esse papel devolve plano/parecer ao principal, sem criar
outra coordenação. Melhorias de ambiente permanecem relacionadas à tarefa.

Verificações em 2026-10-20: sete TOMLs e caminhos registrados conferidos, links
locais conferidos e `git diff --check` passou. Revisão independente sem bloqueios;
simulação por leitura explícita de um pedido de planejamento de regressão de
transparência respeitou a ausência de execução. Não houve ensaio de ativação
nativa do novo tipo, geração, publicação ou agendamento. A descoberta depende
de verificação em sessão nova; arquivos presentes não comprovam execução nativa.

Relacionados: [índice](index.md), [especialistas](especialistas.md),
[memória local](memoria-local.md).

Em 2026-10-20, `prof-ramos/image-production@bea9f975e6d8a2d8813cd7e49432d93472ee3efa` commitou a definição chief_of_staff e o guia antes descritos como locais sem commit. Envio remoto foi bloqueado por escopo OAuth; isso não comprova descoberta nativa. Ver [execução](execucao-main.md).

Em 2026-10-20, em `prof-ramos/image-production@bea9f975e6d8a2d8813cd7e49432d93472ee3efa`,
a descoberta nativa dos sete papéis foi confirmada no Codex CLI 0.163.0: config/read
carregou a camada do projeto e uma sessão nova expôs os sete nomes em agent_type.
Isso supera os registros anteriores de descoberta ainda não verificada para as
definições presentes nesse commit. Não comprova dispatch nem comportamento de
produção de todos eles. Fonte: [relatório](../validation/native-seven-agents-20261020.md).
