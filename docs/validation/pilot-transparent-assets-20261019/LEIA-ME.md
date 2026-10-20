# Reprodução de 12 ativos transparentes, sem API

10/12 aprovados; 14 chamadas à ferramenta integrada.

Abra comparacao.html para comparar os PNGs originais dos exemplos e os novos resultados sobre vários fundos.

| Ativo | Estado | Tentativa selecionada |
|---|---|---|
| Perfume âmbar | needs_revision | 2 |
| Óleo botânico | needs_revision | 2 |
| Difusor | approved | 1 |
| Vela | approved | 1 |
| Receita trimestral | approved | 1 |
| Mix regional | approved | 1 |
| Ícone de aplicativo | approved | 1 |
| Adesivo de morango | approved | 1 |
| Ramo botânico | approved | 1 |
| Estampa | approved | 1 |
| Camiseta marfim | approved | 1 |
| Moletom verde | approved | 1 |

Os prompts originais e utilizados estão em prompts/. Os pareceres independentes, inclusive de tentativas rejeitadas, estão em pareceres/. As imagens anteriores não selecionadas estão em tentativas/. Os PNGs em imagens/ preservam os bytes devolvidos pela ferramenta.

A comparação é de assunto, materiais, transparência e requisitos do briefing; não representa identidade de pixels nem equivalência entre modelos. Model, quality e size da API não foram passados à ferramenta integrada. Os gráficos usam apenas os dados fictícios do exemplo.

Nenhuma página foi publicada e nenhuma API de geração foi chamada.

## Pendências de enquadramento

Os 12 ativos tiveram integridade técnica confirmada. Dez passaram em todos os critérios visuais aplicáveis. Perfume e óleo passaram em materiais, detalhes essenciais e transparência visível, mas permanecem `needs_revision` no enquadramento.

O prompt de refinamento pediu margem mínima de 10%. Na inspeção visual do perfume, as margens aproximadas foram 8,81% acima, 7,42% à direita e 9,32% abaixo. No óleo, a margem superior foi aproximadamente 9,05%; a inferior passou, com 11,85%. Pixels de alfa muito baixo também podem ocupar regiões mais externas; o parecer técnico registra a caixa de todo alfa maior que zero separadamente. Não se afirma que o alvo numérico de 10% foi cumprido.

Cada frasco teve duas tentativas totais. As versões anteriores estão preservadas e não houve preenchimento de margem, recorte, limpeza de fundo ou alteração determinística do PNG entregue. As composições e páginas de comparação são apenas evidências de inspeção.

Os gráficos foram conferidos visualmente contra os dados fictícios: Q1 $42M, Q2 $51M, Q3 $63M e Q4 $78M; North America 46%, Europe 29%, APAC 25%, centro 100%. Rótulos, valores e proporções visuais passaram.

As referências são os PNGs originais disponibilizados no material, não uma nova execução da API. O texto fornecido informa que essas imagens vieram da versão original com GPT Image 2; não são uma medição de GPT Image 2.5. A ferramenta integrada não expõe a seleção de modelo, quality ou size; não se afirma igualdade de backend ou identidade de pixels.
