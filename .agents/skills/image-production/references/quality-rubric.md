# Visual review rubric

Project rubric, adapted conceptually from [OpenAI Image Evals](https://developers.openai.com/cookbook/examples/multimodal/image_evals). Not an official OpenAI scoring standard. Inspect the output; metadata does not prove semantic correctness.

| Key | Evidence to record |
|---|---|
| objective | Intended subject, audience and use are communicated; required elements present |
| text_facts | Exact copy, spelling/accents and supplied facts legible at use size; no invented terms |
| composition | Hierarchy, margins, crop and reading order fit destination |
| brand_reference | Compare canonical brand/product references; colors, shape, materials and identity preserved |
| visual_integrity | No material anatomy, geometry, texture or graphical defects |
| preservation | Compare edit target; requested change made and listed invariants retained |
| transparency | Real alpha plus useful edges on light/dark destination backgrounds; no painted checkerboard/halos |

0 = material failure, 1 = partial/uncertain, 2 = meets requirement with observed evidence; na = not applicable with reason. Never average away critical defects. Metadata checks cover decoding, format, dimensions, file size, hash and alpha; visual scores require inspection. No OCR, CLIP or paid model grader is required or called. Future graders must be calibrated against human labels and cannot silently replace this review.

For cutouts, explicitly inspect any broad glow, color haze or semi-transparent background outside the silhouette and inside holes/handles. The presence of transparent pixels somewhere in the canvas does not satisfy a clean-cutout requirement. If uncertain, score 1 and request correction rather than approve. A second reviewer may overturn an earlier approval; preserve the earlier review as evidence.
