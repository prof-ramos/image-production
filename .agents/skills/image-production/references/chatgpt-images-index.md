# Images card index — observed 2026-10-20

Use this index to identify the card and category, then read only its entry from [the catalog](chatgpt-images-catalog.json). [Evidence limits](chatgpt-images-evidence.md) and [catalog schema](chatgpt-images-catalog.schema.json) apply. This inventory is the 2026-10-20 observation, not the historical 2026-10-19 snapshot. Status below reflects the catalog at this index update; consult the selected entry for later probe evidence.

Select one entry with the available Python runtime; replace the path with the installed skill location and the name/category with the selected row. This reads local JSON only.

```sh
python - /path/to/image-production/references/chatgpt-images-catalog.json 'Cartaz' 'Modelos' <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as source:
    cards = json.load(source)["cards"]
matches = [card for card in cards
           if card["name"] == sys.argv[2] and card["category"] == sys.argv[3]]
if len(matches) != 1:
    raise SystemExit("Expected exactly one matching card")
print(json.dumps(matches[0], ensure_ascii=False, indent=2))
PY
```

## Modelos

| Card | Observation status |
|---|---|
| Cartaz | bounded question examples captured |
| Design de interiores | bounded question examples captured |
| Logo | bounded question examples captured |
| Ilustração | bounded question examples captured |
| Retrato profissional | bounded question examples captured |
| Ícone | bounded question examples captured |
| Foto de produto | bounded question examples captured |
| Produtos personalizados | bounded question examples captured |
| Infográfico | bounded question examples captured |
| Panfleto | bounded question examples captured |
| Capa de livro | bounded question examples captured |
| Mockup de aplicativo | bounded question examples captured |
| Embalagem | bounded question examples captured |
| Anúncio | bounded question examples captured |
| Miniatura | bounded question examples captured |
| Mockup de site | bounded question examples captured |

## Em alta

| Card | Observation status |
|---|---|
| Vista aérea | native probe omitted to avoid generation |
| Lata colecionável | native probe omitted to avoid generation |
| De volta aos anos 80 | native probe omitted to avoid generation |
| Caricatura | native probe omitted to avoid generation |
| Esboço | editor; no prompt |
| Figurinhas | native probe omitted to avoid generation |
| Oktoberfest retrô | native probe omitted to avoid generation |
| Cabine de fotos | native probe omitted to avoid generation |
| Câmera digital dos anos 2000 | native probe omitted to avoid generation |
| Anime | native probe omitted to avoid generation |
| Retrato dos anos 70 | native probe omitted to avoid generation |
| Pintura impressionista | native probe omitted to avoid generation |
| Coleção de pins | native probe omitted to avoid generation |
| Embaixo d’água | native probe omitted to avoid generation |
| Avatar 3D | native probe omitted to avoid generation |
| Pintura acrílica | native probe omitted to avoid generation |
| Miniatura de feltro | native probe omitted to avoid generation |
| Carta de tarô | native probe omitted to avoid generation |
| Estátua | native probe omitted to avoid generation |
| Mundo de massinha | native probe omitted to avoid generation |
| Kit de modelismo | native probe omitted to avoid generation |
| Arcade de 16 bits | native probe omitted to avoid generation |
| Estilo manuscrito | native probe omitted to avoid generation |
| Guia de maquiagem | native probe omitted to avoid generation |
| Rabisco | native probe omitted to avoid generation |
| Seu boneco de cabeça grande | native probe omitted to avoid generation |
| Versão mini | native probe omitted to avoid generation |
| Corte transversal | native probe omitted to avoid generation |
| Melhore fotos | native probe omitted to avoid generation |
| Desejo de viajar | native probe omitted to avoid generation |
| Flash noturno | native probe omitted to avoid generation |
| Pôster blueprint | native probe omitted to avoid generation |
| Colorimetria | native probe omitted to avoid generation |
| Quadrinho | native probe omitted to avoid generation |
| Quadrinho estilo anime | native probe omitted to avoid generation |
| Jornal de fantasia | native probe omitted to avoid generation |
| Tira de filme | native probe omitted to avoid generation |
| Papel de parede hiper-realista | modified clarification-only response observed; native flow unprobed |
| Cor do cabelo | native probe omitted to avoid generation |
| Leitura de mão | native probe omitted to avoid generation |
