# Especialistas e evidência de execução

Em 2026-10-20, conforme `prof-ramos/image-production@e7832a9f39ea34dbb1491df4f0894397d51cd5f2`, o [README](../../README.md) definiu quatro papéis: coordenador, produtor, verificador técnico e revisor visual. O coordenador escreve o manifesto; revisores independentes identificam o mesmo SHA-256; o fluxo admite até dois workers e uma geração por vez, respeitando limites menores do host. O limite acumulado de duas correções inclui retomadas e histórico anterior.

Em 2026-10-20 o [relatório de portabilidade](../validation/specialist-portability-20261020.md), nesse commit, registrou o diagnóstico de confiança do projeto e a verificação nativa de um `image_technical` por canário; as quatro definições foram observadas na configuração efetiva. Esse registro superou a hipótese inicial, preservada no relatório, de ativação ainda não verificada. Não extrapolar esse ensaio para versões futuras do host nem para todos os comportamentos dos quatro papéis.

Em 2026-10-20 ficou preservada a separação entre testes técnicos, qualidade visual e carregamento nativo. Os 33 testes históricos não homologam visualmente imagens. A caneca histórica continuou `needs_revision`; esta coordenação não autoriza nova geração nem relaxamento de preservação. Fonte: relatório de portabilidade e README acima.

Relacionado: [índice](index.md), [base de cards](plugin-e-cards.md), [memória](memoria-local.md).

## Ampliação de 2026-10-20

Em 2026-10-20, a pedido do usuário para criar agentes reutilizáveis de geração
GPT, foram acrescentados localmente dois papéis opcionais: `image_director` e
`image_eval_designer`. Base de código observada:
`prof-ramos/image-production@3c08fdd5e104af5a69cc087072ff40af6e332219`; as mudanças
ainda não têm commit. Este registro supera a contagem de quatro definições como
inventário completo, preservando quatro papéis obrigatórios para produção.
Fontes: [playbook](../../.agents/skills/image-production/references/agent-playbook.md)
e [validação](../validation/reusable-agents-20261020.md).
Os 57 testes e o build passaram; não comprovam descoberta nativa dos dois papéis
novos nem qualidade visual. Plugin local 0.1.5 reconstruído, sem reinstalação.

## Gate persistido após revisão

Em 2026-10-20, conforme `prof-ramos/image-production@a728a21dcb7c8de6ea2006ccc0e7ad73b85dbcd2`, o helper passou a persistir os dois pareceres por papel e SHA256, exigir revisores distintos e reservar tentativas por chave estável no ledger do root antes de gerar. Isso supera a implementação anterior que avaliava apenas o último parecer e não persistia o limite entre runs. A inicial mais duas correções inclui reservas canceladas; nova chave deliberada não é identidade semântica comprovada. Legado permanece histórico e nova revisão migra conservadoramente. Fonte: [correções do PR](../validation/pr4-review-fixes-20261020.md).
