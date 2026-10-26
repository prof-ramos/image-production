# Briefing adaptativo: conversa nova observada em 20/10/2026

## Escopo e resultado

Uma conversa nova real do Codex CLI 0.163.0 reproduziu a sequência original de
pedido de criativos e convite incompleto da ASOF. O plugin instalado foi descoberto
pelo agente, sem injetar sua fonte no prompt e sem instruir o agente a apenas fazer
perguntas. A conversa foi retomada duas vezes com entradas sintéticas para observar
continuidade e mudança de data. Os quatro turnos terminaram normalmente.

O comportamento de esclarecimento e espera pela aprovação foi observado: não houve
`prepare`, delegação para geração ou chamada de ferramenta de imagem nos quatro
turnos. Isso verifica o comportamento anterior à produção neste percurso; não
comprova o caminho de geração, revisão ou entrega final.

Fonte observada: `prof-ramos/image-production@2dc1385767cf49e6cc5be37b4435906aa7913cb7`.
Plugin instalado/habilitado no inventário CLI:
`0.1.6-main.g2dc1385767cf49e6cc5be37b4435906aa7913cb7`.

## Método e evidências

- CWD temporário neutro fora do repositório, sem AGENTS do projeto.
- `codex exec --skip-git-repo-check --json -o <resposta> '<pedido original>'`;
  os próximos turnos usaram `codex exec resume --skip-git-repo-check --json` com
  o mesmo identificador da conversa, executados um por vez.
- Configuração existente preservada: modelo observado `gpt-6.1-sol`, esforço
  `low`, sandbox `read-only`, aprovação `never`. Não houve override de modelo,
  permissões, autenticação ou plugins; nenhum fallback de API.
- No segundo turno, dois comandos reais leram a `SKILL.md` e a referência
  `communication-brief.md` dentro do cache instalado da versão acima.
- Casos reproduzíveis com entrada, expectativa, resposta observada, status e hashes
  dos JSONL: [cases.json](briefing-live-20261020/cases.json). As respostas portáveis
  normalizam o caminho local da skill como `<installed-plugin>` e identificam essa
  sanitização no caso afetado; a transcrição exata permanece somente em `work/`.
- Transcrições brutas, respostas e metadados locais: `work/briefing-live-20261020/`,
  ignorado pelo Git. Identificador da sessão e caminho do rollout ficam somente
  nesse diretório local; não na wiki nem neste relatório versionável.

## Casos observados

| Caso | Resultado observado | Veredito |
| --- | --- | --- |
| Capacidade para criativos | Respondeu capacidade e pediu assunto, rede social e resultado. Não gerou. | Passou |
| Convite incompleto ASOF | Reutilizou nome, data e local; perguntou canal/público, logo, horário/endereço e estilo; propôs texto para aprovação. Leu a skill instalada e o briefing. | Passou com observação |
| Resposta parcial | Preservou WhatsApp, associados, reserva da data, ausência de logo e horário; escolheu estilo delegado; propôs texto de reserva da data e aguardou aprovação. | Passou com observação |
| Correção somente da data | Atualizou para 04/12, preservou Mundial e restante do texto, explicitou que ainda aguardava aprovação. | Passou |

As entradas de resposta parcial e correção de data são **fixtures sintéticas de
validação**. Elas não representam preferências reais nem aprovação do usuário para
uma arte. Nenhum turno aprovou a redação; nenhuma imagem foi solicitada como
continuação desta conversa de teste.

## Observações de experiência

No turno do convite incompleto, a mensagem intermediária antecipou “convite
festivo”, embora a resposta final perguntasse o estilo. A resposta final não
perguntou separadamente a finalidade/ação, que pode ter sido inferida de “convite”;
a fixture seguinte refinou essa finalidade para reserva de data e o agente a
adotou. O percurso não demonstra um bloqueio funcional por esses pontos, mas eles
merecem observação em pedidos mais ambíguos.

Na resposta parcial, o agente mostrou um caminho interno da skill e citou em inglês
a regra que exige aprovação. Isso acrescentou detalhe técnico à experiência. A
mensagem ainda preservou o gate e a continuidade. As instruções gerais do host
sobre explicar confirmações exigidas por skills também estavam presentes; não se
atribui essa exposição exclusivamente à skill do plugin.

“Evento fictício” ficou fora das propostas de texto em todos os turnos, conforme
seu papel de contexto do exercício.

## Limites

Esta evidência é uma conversa nova no **CLI**, não observação da interface do Codex
Desktop. Foram quatro turnos em uma única conversa/modelo; não mede confiabilidade
estatística. O teste não aprovou texto, não exerceu disponibilidade da ferramenta
integrada de imagem, não produziu arquivo e não avaliou identidade visual, formato
ou qualidade de uma arte. O sandbox observado era somente leitura; ausência de
geração neste percurso não demonstra que uma chamada de imagem teria funcionado.

Os casos JSON são registros reproduzíveis de regressão com resultados observados,
não testes automáticos de comportamento nem alegação de ciclo red-green.
Mensagens de autenticação de conectores não relacionados apareceram no stderr; a
conversa e as leituras do plugin terminaram normalmente, sem alteração de acesso.

## Piloto de produção separado — 20/10/2026

Após os testes acima, o usuário real recebeu a proposta completa de uma imagem
vertical 2:3 para WhatsApp, destinada aos associados, com finalidade de reservar a
data, sem logo, horário, endereço ou RSVP. A proposta incluía exatamente:

> Reserve a data / Confraternização de fim de ano da ASOF / 03/12 • Mundial

O usuário respondeu “Voce é o coordenador, voce decide”. O coordenador adotou essa
proposta sob a delegação explícita. As fixtures sintéticas da conversa CLI não
foram usadas como autorização; a data do piloto permaneceu 03/12.

A produção ocorreu separadamente na sessão Desktop em andamento, pelo caminho
integrado `built-in`, com definição de coordenador carregada e papéis nativos
`image_producer`, `image_technical` e `image_visual` delegados. Houve uma geração,
tentativa 0, sem correções nem mutações simultâneas do manifesto. O coordenador
registrou os dois pareceres independentes para o mesmo SHA256.

Artefatos locais, relativos à raiz do repositório:

- Arte: [asof-save-date.png](../../work/approved-pilot-20261020/2320ec8b-0007-4dc4-a50e-b75ef1b5282c/final/asof-save-date.png).
- Estado, metadados e pareceres: [manifest.json](../../work/approved-pilot-20261020/2320ec8b-0007-4dc4-a50e-b75ef1b5282c/manifest.json).
- Prompt submetido: [submitted-prompt.txt](../../work/approved-pilot-20261020/2320ec8b-0007-4dc4-a50e-b75ef1b5282c/work/submitted-prompt.txt).
- Pareceres: [técnico](../../work/approved-pilot-20261020/2320ec8b-0007-4dc4-a50e-b75ef1b5282c/work/technical-review.json) e [visual](../../work/approved-pilot-20261020/2320ec8b-0007-4dc4-a50e-b75ef1b5282c/work/visual-review.json).
- Resumo portátil: [production-result.json](briefing-live-20261020/production-result.json).

O candidato é PNG opaco de 1024×1536, exatamente 2:3, com SHA256
`d6a7ca0b992c3d31fe9a78af9f970ec233a222dd388a19289c53cd9ab2e9f5b5`.
O helper `verify`, executado novamente sobre esse run, retornou
`{"valid": true, "state": "approved", "outputs": 1}`. O hash dos bytes da arte
conferiu com o manifesto; o prompt submetido conferiu byte a byte com a cópia
retida pelo helper.

Os dois revisores inspecionaram o candidato e prévias de 360×540. Ambos registraram
leitura dos textos, data, local e acentos; hierarquia, contraste e ausência de
informações inventadas. Todos os critérios aplicáveis receberam 2 nos dois
pareceres. `brand_reference` foi `na` por ausência de kit/referências; preservação
e avaliação de recorte transparente também não se aplicavam. Verde e dourado
foram escolhas criativas delegadas, sem alegação de identidade oficial da ASOF.

O envio real pelo WhatsApp, sua compressão e a apresentação na interface não foram
testados. Os artefatos em `work/` são locais e ignorados pelo Git; os links dependem
desse diretório preservado. A conversa CLI acima continuou sem aprovar nem gerar;
este piloto acrescenta evidência de produção separada e não altera esse limite.
