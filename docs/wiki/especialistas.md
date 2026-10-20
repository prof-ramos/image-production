# Especialistas e evidência de execução

Em 2026-10-20, conforme `prof-ramos/image-production@e7832a9f39ea34dbb1491df4f0894397d51cd5f2`, o [README](../../README.md) definiu quatro papéis: coordenador, produtor, verificador técnico e revisor visual. O coordenador escreve o manifesto; revisores independentes identificam o mesmo SHA-256; o fluxo admite até dois workers e uma geração por vez, respeitando limites menores do host. O limite acumulado de duas correções inclui retomadas e histórico anterior.

Em 2026-10-20 o [relatório de portabilidade](../validation/specialist-portability-20261020.md), nesse commit, registrou o diagnóstico de confiança do projeto e a verificação nativa de um `image_technical` por canário; as quatro definições foram observadas na configuração efetiva. Esse registro superou a hipótese inicial, preservada no relatório, de ativação ainda não verificada. Não extrapolar esse ensaio para versões futuras do host nem para todos os comportamentos dos quatro papéis.

Em 2026-10-20 ficou preservada a separação entre testes técnicos, qualidade visual e carregamento nativo. Os 33 testes históricos não homologam visualmente imagens. A caneca histórica continuou `needs_revision`; esta coordenação não autoriza nova geração nem relaxamento de preservação. Fonte: relatório de portabilidade e README acima.

Relacionado: [índice](index.md), [base de cards](plugin-e-cards.md), [memória](memoria-local.md).
