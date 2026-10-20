# Publicação automática — implementação de 2026-10-20

Em 2026-10-20 o usuário autorizou implementar publicação automática do plugin e
da skill após integração à main. No commit
`prof-ramos/image-production@89895ee69bc6cddc6a91f34e29309d302a65d98d`, integrado
localmente à main no commit
`prof-ramos/image-production@94cdcd6d836401940d9d658482ad6a7eed1e2e8f`, resultando em
`prof-ramos/image-production@f866b7c26d0e752810e248e70dd6e5976560b098`, foram adicionados
preparo/verificação/publicação Git e atualização da instalação via CLI oficial.
Fonte: [validação local](../validation/automatic-release-20261020.md) e
[regras de distribuição](../agents/releases.md).

A implementação exporta o commit validado (não o checkout sujo), gera versão
`base-main.gSHA`, proveniência e hashes e promove branch `plugin-release` com catálogo
Git fixado no SHA do payload. Dois commits locais evitam autorreferência do SHA;
um push normal publica o estado completo e preserva histórico. Job publicador
só roda após matriz verde em push main e recebe escrita somente nessa etapa.
O atualizador valida versão e bytes antes/depois da instalação; agentes são
bundle separado, sem merge automático da configuração de segurança do projeto.

Em 2026-10-20 passaram 82 testes locais em Python 3.10 e 3.13, actionlint e instalação
Codex isolada com migração local→Git e duas versões. Revisões independentes
Standards e Spec no diff `94cdcd6...f866b7c` não acharam problemas acionáveis.
Publicação hospedada e instalação real ainda não foram comprovadas neste registro.
A janela consulta-main/push é documentada; concorrência e próximo run reconciliam
novo head sem push forçado. Não há nova assinatura ou credencial pessoal.

Este registro supera o estado de automação inexistente como implementação local,
sem confundir código pronto com ativação na main. O [checkpoint geral](execucao-main.md)
registra o progresso remoto; [índice](index.md), [plugin](plugin-e-cards.md) e
[CI](ci-testes.md) trazem contexto relacionado.
