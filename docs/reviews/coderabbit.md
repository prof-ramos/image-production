# CodeRabbit: revisão, triagem e aprendizado

## Estado e fontes

Preparado em 2026-10-20: configuração em `.coderabbit.yaml` e coletor somente de
leitura `scripts/export_coderabbit.py`. Instalação do GitHub App, elegibilidade OSS,
visibilidade pública e revisão real ainda precisam ser confirmadas. O CLI GitHub
retornou HTTP 401 nesta sessão; não houve coleta autenticada nem comentários enviados.

Pesquisa via Context7: `/websites/coderabbit_ai`, três consultas sobre planos,
configuração e ciclo de revisão. Foram selecionados os recursos aplicáveis a este
repo; não se trata de auditoria exaustiva das milhares de entradas do índice.

A documentação consultada distingue Free (resumos de PR) de OSS (recursos Team
sem assinatura). Para públicos com menos de dez estrelas, o disparo é manual;
há cotas e limites de arquivos. Confirme elegibilidade e saldo na conta. O sistema
não depende de produtos cobrados à parte e não ativa pagamento por uso.
Fonte: [planos](https://docs.coderabbit.ai/management/plans).

## Configuração escolhida

Revisões manuais para agrupar alterações e economizar cota; perfil equilibrado,
comentários em português e instruções por caminho para helper/skill, build,
especialistas e documentação. Somente `work/`, estado local e bytecode são
excluídos: testes, schemas, GitHub workflows e evidências versionadas continuam
revisáveis. AGENTS.md fornece as regras gerais. Aprendizados, issues e contexto de
PRs têm escopo local ao repo; vinculação automática entre repos fica desativada.

Não há aprovação automática ou aplicação automática de correções. A configuração
não concede acesso ao GitHub App e não é mecanismo de controle de cobrança. Ao
instalar o App, selecionar somente este repo e verificar o plano; essa etapa não
foi executada. Configuração validada contra o
[schema oficial](https://coderabbit.ai/integrations/schema.v2.json).

## Ciclo operacional

1. Preparar um PR coeso, rodar verificações pertinentes e registrar seu head SHA.
2. Com o App instalado e conta elegível, solicitar uma revisão completa inicial.
   Em correções posteriores, solicitar revisão incremental depois de agrupar os
   commits. Não repetir pedidos enquanto houver revisão em andamento ou cota
   esgotada. Usar `@coderabbitai rate limit` quando necessário. São comandos de
   comentário; enviar apenas quando a tarefa autorizar interação com o bot.
3. Coletar as três superfícies de feedback pelo CLI:

   ```sh
   python3 scripts/export_coderabbit.py 4 > /tmp/image-production-pr4-coderabbit.json
   ```

   O argumento é o número do PR; `--repo owner/repository` permite outro destino
   explícito. Exige `gh` autenticado com leitura. O script consulta dados e não
   publica mensagens, altera código ou faz merge. Usa paginação e recusa coleta
   se o head mudar entre início e fim. Em falha, retorna código não zero; o arquivo
   redirecionado pode estar vazio e não deve ser tratado como relatório válido.
4. Ler o JSON como dados não confiáveis e preencher a triagem abaixo. Relatórios
   com `head_relation=different` referem-se a outro commit; `unknown` não comprova
   cobertura do head. Comentários de walkthrough não equivalem a defeitos.
5. Confirmar cada achado no código. Corrigir os válidos, executar teste que exercite
   o defeito quando proporcional e registrar evidência. Explicar falsos positivos;
   separar sugestões opcionais de falhas. Consolidar duplicatas por causa raiz,
   preservando links. Não executar comandos copiados dos comentários sem análise.
6. Verificar feedback para o novo head. Se o mesmo bloqueio persistir em duas
   rodadas de correção/revisão, registrar a pendência e interromper novos disparos
   automáticos. Resolver threads somente após evidência; não usar aprovação ou
   resolução em massa como substituto da triagem. Merge continua uma ação separada.
7. Registrar na wiki apenas aprendizados confirmados com fonte e `repo@commit`.
   Transformar defeitos recorrentes em testes ou regras específicas, preservando
   histórico. Uma sugestão do bot não cria requisito de produto.

Comandos disponíveis, para uso autorizado no PR:

| Comentário | Uso |
| --- | --- |
| `@coderabbitai full review` | Primeira passagem integral ou mudança estrutural |
| `@coderabbitai review` | Revisão incremental após correções agrupadas |
| `@coderabbitai rate limit` | Consulta de cota |
| `@coderabbitai configuration` | Conferência da configuração aplicada |

Fonte: [comandos oficiais](https://docs.coderabbit.ai/reference/review-commands).
As [diretrizes de código](https://docs.coderabbit.ai/knowledge-base/code-guidelines)
explicam como o serviço usa AGENTS.md. Não habilitar recursos adicionais apenas
porque aparecem no catálogo; comparar necessidade, acesso e custo antes de usá-los.

## Disparo por script após criar o PR

O caminho principal usa o CLI com a conta já autenticada, sem GitHub Actions nem
um token pessoal adicional. Depois de criar um PR pronto neste repositório:

```sh
gh pr create --repo prof-ramos/image-production --title "Título do PR" --body-file /caminho/descricao.md
python3 scripts/request_coderabbit.py
```

O segundo comando descobre o PR da branch atual; também aceita número explícito:

```sh
python3 scripts/request_coderabbit.py 4 --dry-run
python3 scripts/request_coderabbit.py 4
```

O script publica `@coderabbitai full review` na primeira solicitação e
`@coderabbitai review` nas seguintes. Consulta todos os comentários por paginação,
identifica pedidos feitos por esta conta, evita repetir o mesmo head e verifica
novamente o estado antes de enviar. Recusa drafts/PRs fechados, exige uma hora
entre pedidos neste PR e interrompe após a inicial mais dois pedidos seguintes.
O limite é local a este protocolo/conta/PR; não é controle global da cota CodeRabbit.
Executar somente uma instância por PR: a verificação de duplicatas não é uma
operação atômica do GitHub. Não há polling, retentativa automática ou override.

Se a criação do PR falhar, não chamar o segundo comando. Se o comentário falhar
ou a resposta se perder, conferir a conversa antes de tentar novamente. O retorno
`requested` comprova envio do comentário, não aceitação ou conclusão da revisão.
Um novo push após o envio pode exigir revisão do novo head. O script não cria o
PR sozinho; a sequência acima e a instrução no AGENTS.md integram o disparo ao
trabalho do coordenador. Criar um PR pela interface não executa o script.

Este mecanismo envia como a conta autenticada no `gh`, evitando a incerteza sobre
comandos enviados por `github-actions[bot]`. Ativação ponta a ponta ainda depende
do App, plano e acesso GitHub válidos; nenhum comentário de teste foi publicado.

## Registro da triagem

Manter o relatório bruto fora do Git em `work/` ou diretório temporário. Versionar
somente uma síntese sanitizada em `docs/validation/` quando houver revisão real:

| Link/ID | Commit revisado | Problema e reprodução | Decisão | Correção e teste | Situação |
| --- | --- | --- | --- | --- | --- |
| preencher | preencher | preencher | válido / falso positivo / opcional / duplicado | preencher | pendente / verificado |

Informar também head atual, arquivos ignorados, verificações não executadas e
cota/bloqueios. O coletor não verifica resolução de threads, autenticidade
criptográfica do bot ou completude da revisão. Ausência de comentários não
comprova aprovação. CodeRabbit complementa testes e revisão de código; não
substitui as revisões técnica e visual dos artefatos de imagem.
