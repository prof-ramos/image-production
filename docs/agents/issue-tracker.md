# Issue tracker: GitHub

Issues e especificações deste repo ficam em GitHub Issues de
`prof-ramos/image-production`. Use o CLI `gh`, com `--repo prof-ramos/image-production`
explícito nas operações para evitar atuar em outro repositório.

## Operações

- Criar: `gh issue create --repo prof-ramos/image-production --title "Título" --body-file /caminho/issue.md`.
- Ler: `gh issue view <numero> --repo prof-ramos/image-production --json number,title,body,labels,comments`.
- Listar: `gh issue list --repo prof-ramos/image-production --state open --json number,title,labels`, filtrando por label quando necessário.
- Comentar: `gh issue comment <numero> --repo prof-ramos/image-production --body-file /caminho/comentario.md`.
- Aplicar/remover rótulos: `gh issue edit <numero> --repo prof-ramos/image-production --add-label "rotulo"` ou `--remove-label "rotulo"`.
- Fechar: `gh issue close <numero> --repo prof-ramos/image-production` após registrar o resultado e as evidências.

Para textos multilinha, escreva um arquivo UTF-8 e use `--body-file`. Consulte o
`--help` do CLI instalado antes de usar operações adicionais ou dependentes de
versão. Se a autenticação falhar, reporte o bloqueio e priorize restaurar o acesso
CLI; não migre silenciosamente para a interface.

## Contratos para as skills

Quando uma skill pedir publicar no issue tracker, crie uma issue GitHub dentro
do escopo autorizado. Quando pedir buscar um ticket, leia a issue e seus
comentários. Esta configuração não autoriza criar tickets ou enviar mensagens
sem uma tarefa que peça essas ações.

**PRs as a request surface: no.**

PRs são o mecanismo de revisão e integração; não entram automaticamente na fila
de solicitações da triagem. O disparo CodeRabbit continua seguindo
[seu protocolo](../reviews/coderabbit.md).

## Hierarquia de trabalho

Quando uma tarefa exigir mapa e subtarefas, use issues relacionadas. Prefira
sub-issues e dependências nativas quando o CLI e o repositório as suportarem.
Caso contrário, registre `Part of #<pai>` no filho, uma lista de filhos no pai e
`Blocked by: #<numero>` para dependências. Não crie hierarquias ou rótulos
adicionais antes de uma tarefa concreta precisar deles.
