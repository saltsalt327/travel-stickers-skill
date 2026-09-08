---
name: travel-memory-card-duo
description: "Transform one to five user-supplied travel, street, landscape, lifestyle, portrait, or pet photos into a coordinated four-part travel-memory set: a horizontal watercolor-and-ink card, a matching nine-sticker transparent RGBA sheet, nine individually cropped transparent sticker PNGs with lightweight previews, and an opaque retail packaging preview. Use for photo-to-travel-card, reusable sticker-pack, individual sticker asset, or packaging-mockup requests. Preserve recognition through source-derived anchors; never retain unintended photography, incidental text, signatures, or watermarks."
---

# Travel Memory Card Duo

Turn one to five source photos into four matched bitmap deliverables:

1. A finished 3:2 travel memory card.
2. A 3:2 transparent PNG sticker sheet containing the same nine sticker motifs.
3. Nine individual transparent PNG files cropped from that validated sheet, each with a lightweight preview.
4. A 3:4 opaque retail-style sticker-packaging preview image showing the same nine stickers as a complete product set.

Treat the supplied photos as one source set. Include every supplied image in the relevant image-generation call; if the images exist only in the conversation, pass the smallest `num_last_images_to_include` value that includes all of them (1–5), and if they have local paths, pass all of them as `referenced_image_paths`. When several are provided, choose the strongest photo as the primary composition reference and use the others to supply additional motifs, color cues, or alternate views. Do not make a collage, duplicate a subject, or blend unrelated scenes unless the user explicitly asks for that.

Use the image generation/editing tool for the memory card, transparent sticker sheet, and blank packaging background. Do not simulate or restyle the illustration with filters or code. Export the individual sticker files directly from the validated transparent sheet with `scripts/export_individual_stickers.py`. For the packaging preview, use `scripts/compose_packaging_preview.py` to place the same validated artwork on the generated background with deterministic spacing. These scripts only crop or composite existing raster assets; they do not redraw the illustration. Use local processing for chroma-key removal, alpha validation, individual extraction, and final layout composition.

## Workflow

1. Inspect every supplied photo at full useful detail.
2. Identify the shared or primary scene structure, emotional center, dominant spatial gesture, and one or more compact identification anchors.
3. Select exactly nine distinct, meaningful source-derived sticker motifs across the source set and exactly three concise English keyword phrases.
4. Decide whether one source-visible text item genuinely identifies the place. Default to `NONE`; reject advertising, menus, prices, directions, timestamps, and product labels.
5. Read [references/style-guide.md](references/style-guide.md).
6. Generate the complete memory card first. Treat its nine stickers as the visual master for the second image.
7. Inspect the card. Regenerate once if the medium, layout, sticker count, keywords, or readable text is wrong.
8. Generate a separate sticker sheet from the source set and finished card. Include exactly the same nine motifs, shapes, colors, medium, and narrow warm-white cut borders.
9. Produce transparency with the built-in image-generation transparency workflow: generate the sheet on one uniform removable chroma-key color, then run the installed `remove_chroma_key.py` helper. Choose a key color absent from the stickers; prefer `#ff00ff` for foliage-heavy scenes and `#00ff00` otherwise.
10. Validate the final PNG. It must be RGBA, all four corners must have alpha 0, the nine stickers must remain fully opaque apart from antialiased edges, and no key-color fringe may remain. Retry removal once with a slightly stronger tolerance or `--edge-contract 1` if needed.
11. Run `scripts/export_individual_stickers.py` on the validated transparent sheet. It must create exactly `sticker-01.png` through `sticker-09.png` in row-major order without regenerating, resizing, or modifying the sticker pixels, plus one small transparent WebP preview for each original.
12. Run `scripts/select_packaging_card_color.py` with every source photo and the validated transparent sticker sheet. Use its selected HEX value for the packaging card and the fixed cream text color `#F4E7C8`; save the JSON result with the deliverables so the choice is reproducible.
13. Generate a blank opaque packaging background with the selected full-bleed backing-card color, hang hole, exact title/count text, and empty warm-paper lower area. Inspect the actual lower edge of the backing card, then run `scripts/compose_packaging_preview.py` with that measured pixel coordinate and the validated transparent PNG. Do not redraw, replace, split, merge, or reinterpret the nine stickers.
14. Inspect the individual PNGs and composed packaging preview. Confirm that the generated card still reads as the selected color, the cream text is legible, and the card remains distinct from the sticker artwork. If the background card, title/count text, color relationship, or product presentation is wrong, regenerate only the blank background and compose again. If extraction or the grid is wrong, fix the script inputs or parameters before delivering.

## Deliverable 1: complete memory card

- Use one 3:2 horizontal canvas on warm off-white uncoated paper with a continuous 4–5% outer margin.
- Build the left 66–68% as one large near-square unframed illustration above a shallow exposed-paper keyword footer. Do not add an outline, keyline, mat, inner card, rounded frame, or shadow around the illustration.
- Center exactly three short scene-derived English keyword phrases once beneath the illustration, separated by centered dots: `[keyword 1] · [keyword 2] · [keyword 3]`.
- Place exactly nine separate die-cut stickers in the right 30–32%. Use the full composition height, three loose staggered rows of three (or an equally clear compact asymmetric arrangement), an uneven size hierarchy, relaxed spacing, narrow irregular warm-white hand-cut borders (about 3–6 px at 1536 px output width), and subtle flat paper shadows. Keep every sticker separated and fully visible.
- Preserve the identification anchor through silhouette, proportion, placement, relationship, and signature colors in the same medium as the whole card.
- Add no title, caption, date, writing area, postal marks, address lines, subtitle, watermark, or signature.

## Deliverable 2: transparent sticker PNG

- Use a separate 3:2 horizontal canvas.
- Include exactly the same nine stickers from the finished card; do not redesign, replace, split, merge, or add motifs.
- Arrange the stickers in three relaxed rows of three with generous transparent space. Keep every sticker fully visible, separated, and uncropped.
- Preserve a very narrow irregular warm-white die-cut border around every sticker: visually about 3–6 px on a 1536 px-wide output or 0.75–1.25% of the motif width. It must remain visible around antialiased edges but read as a fine cut edge, not a padded halo. Do not create a broad white border or soft white glow.
- Remove the card paper, shadows, footer, keywords, title, labels, and all readable text.
- Do not add an overall sheet, panel, frame, texture, floor plane, reflection, or cast/contact shadow.
- Deliver a real PNG with an Alpha channel. A checkerboard, black, or white preview background is not part of the file.

For chroma-key generation, explicitly require a perfectly uniform flat background with no lighting variation, texture, gradients, shadows, reflections, or key color inside the sticker art. Use the installed helper:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
  --input <chroma-source.png> \
  --out <transparent-stickers.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 60 \
  --despill
```

If the helper needs Pillow, load the Codex workspace dependency runtime and use its Python executable. If soft-matte removal leaves a fringe, retry once with `--edge-contract 1`; if hard-key removal is cleaner for opaque paper stickers, use a sampled key color and a moderate tolerance. Never claim transparency before checking the Alpha channel.

## Deliverable 3: nine individual transparent sticker PNGs

- Use `scripts/export_individual_stickers.py` to crop the validated transparent sheet directly. Do not ask the image model to regenerate the stickers.
- Save exactly nine files named `sticker-01.png` through `sticker-09.png`, ordered from left to right and top to bottom according to the three-row source sheet.
- Preserve each sticker's original pixels, full irregular warm-white cut border, Alpha channel, and source resolution. Do not resize, repaint, sharpen, recolor, or add shadows.
- Crop tightly enough for convenient reuse while retaining transparent padding on every side. Each output must be an RGBA PNG with all four corner alpha values equal to 0 and exactly one complete, uncropped sticker.
- Do not include any part of another sticker, paper background, label, keyword, shadow, or chroma-key fringe.
- Also create `previews/sticker-01-preview.webp` through `previews/sticker-09-preview.webp`. Use a 160×160 transparent canvas, center a proportionally scaled copy of the corresponding PNG with breathing room, and keep the WebP lightweight. These files are browsing previews only; never substitute them for the full PNG assets.

Use the bundled helper after the transparent sheet passes validation:

```bash
python3 scripts/export_individual_stickers.py \
  --input <transparent-stickers.png> \
  --out-dir <individual-stickers-directory>
```

## Deliverable 4: sticker packaging preview

- Generate the blank background only after the transparent nine-sticker PNG has passed Alpha validation, then compose the final image with `scripts/compose_packaging_preview.py`.
- Use the validated transparent PNG as the immutable visual master. Preserve exactly the same nine sticker motifs, watercolor-and-ink artwork, narrow warm-white cut borders, and source-derived colors. Do not use the packaging preview as the source for any earlier deliverable.
- Use a 3:4 portrait composition with a near top-down, product-photography presentation. Set a warm cream matte paper background with subtle natural grain and soft diffused daylight.
- Select the backing-card color from the source photos instead of using a fixed blue-gray. Run `scripts/select_packaging_card_color.py` after the transparent sheet is validated. The helper derives dark, restrained variants from the photo palette, requires at least a 4.5:1 contrast ratio against cream `#F4E7C8`, and downranks hues or Lab colors already dominant in the visible sticker artwork. Use the selected HEX value exactly in the generation prompt; do not default to blue merely because it worked for a prior set. If no candidate passes, use the highest-scoring source-derived candidate after darkening or desaturating it until both thresholds pass rather than inventing an unrelated brand color.
- Place the selected-color paper backing card flush against the top edge and span the full image width edge-to-edge. Target a shorter card occupying about 15–17% of the canvas height; if the generated background exceeds 18%, regenerate the background before composing. Leave no cream margin above it and no side gutters around it; let the canvas crop its top corners if needed. Keep slight rounded lower corners, subtle thickness and shadow, a centered retail hang hole, and centered `#F4E7C8` typography. Use an uppercase serif location/theme title; if the place is confidently known use `[PLACE] DAYS`, otherwise use `TRAVEL DAYS`. Add only the exact quantity label `9 PIECES` beneath it in small uppercase sans-serif type.
- Arrange all nine stickers below the backing card with `scripts/compose_packaging_preview.py`, not by asking the image model to guess the final spacing. The script must use the outermost visible die-cut border as each sticker's boundary and place one sticker in each position of a strict 3×3 product grid. Use identical left and right outer margins, identical column gutters, identical row gutters, and equal top/bottom visible-boundary margins. Target side margins at about 5% of canvas width, column gutters at about 2.5% of canvas width, and both the card-to-first-row and last-row-to-bottom margins at about 2.5% of canvas height. Increase sticker occupancy within each cell to make the nine pieces visibly larger while preserving aspect ratio and the fine 3–6 px border.
- Preserve the narrow sticker borders. Add only subtle external contact/drop shadows to make the stickers read as physical paper goods; never add shadows inside the transparent PNG.
- This preview is intentionally opaque and may contain the backing card, paper background, dynamic title, and `9 PIECES` label. It must not contain a checkerboard, source photo, unrelated props, platform UI, watermark, or extra motifs.

Run the color selector with all source photos and the validated sheet before generating the blank packaging background:

```bash
python3 scripts/select_packaging_card_color.py \
  --photos <source-photo-1> [<source-photo-2> ...] \
  --stickers <transparent-stickers.png> \
  --out <packaging-card-color.json>
```

## Shared art direction

- Rebuild the scene from 5–8 source-derived watercolor color families on a warm ivory paper ground; keep the overall image bright, airy, and lightly sun-washed.
- Establish the first read with 3–6 clear masses and a strong perspective path, then let selective details describe the place without filling every area equally.
- Use digital watercolor that preserves traditional watercolor behavior: transparent layered washes, wet-on-wet sky and atmosphere, wet-on-dry architectural accents, pigment pooling, soft blooms, subtle granulation, dry-brush texture, and reserved paper-white highlights.
- Draw with thin, loose, irregular gray-brown or olive ink contours. Let some edges stay crisp for architecture and focal objects while others feather, break, or dissolve into the wash.
- Build foliage from layered irregular leaf clusters, visible branch and trunk gestures, and varied green dabs; simplify leaves into expressive shapes rather than botanical studies. Keep buildings readable through perspective, façades, windows, balconies, roofs, and a few decisive lines.
- Reduce people, cars, and other small subjects to compact, readable silhouettes or color accents with no detailed faces or anatomy. Keep distant forms paler and softer to create atmospheric depth.
- Use transparent cool blue-gray or green-gray shadow washes with no hard digital gradients. Keep near-black sparse and reserve the strongest contrast for the focal architecture and foreground details.
- Keep the mood observational, calm, bright, humane, lived-in, and lightly nostalgic, like a hand-painted city travel journal or editorial urban sketch.
- Avoid photorealism, photographic patches, opaque gouache, cut-paper, risograph, screen-print fills, thick black outlines, marker strokes, glossy 3D, dramatic lighting, botanical leaf studies, detailed anatomy, polished vectors, anime, clip art, and unrelated objects.

## Motif and keyword rules

- Choose nine visible motifs with useful variety across the source set: a main-subject fragment, a grouped or paired variation when present, an environmental form, a structural fragment, a functional object, a small atmospheric or scale cue, and three additional distinct secondary forms or details. Distribute motifs across the supplied photos when meaningful, but never force irrelevant or duplicate stickers just to fill the count.
- Treat a group visible as one sticker when selected as a grouped motif.
- Keep all nine motifs coarse, source-derived, and stylistically identical on the card and transparent sheet. Use the validated sheet unchanged for the individual exports and packaging preview.
- Remove lettering when a sticker repeats a landmark sign.
- Write three precise English keyword phrases grounded in the scene, light, object, or spatial feeling. Prefer `Crater Smoke`, `Blue Summit`, or `Quiet Ridge` over generic words such as `Travel` or `Beautiful`.

## Quality checks

### Complete card

- The scene is identifiable at a glance but reads first as large shapes and quiet space.
- The left illustration dominates and is completely unframed.
- The right column contains exactly nine separated stickers with a clear size hierarchy and a loose three-row rhythm.
- Exactly three English keyword phrases appear once beneath the left image.
- No unintended readable text, watermark, signature, or photographic patch remains.

### Transparent PNG

- The file format is PNG and the image mode is RGBA.
- All four corner alpha values are 0.
- Exactly nine sticker objects remain; none is cropped, touching, or duplicated.
- The sticker designs match those on the card and retain narrow warm-white cut borders.
- No paper sheet, colored background, key-color halo, shadow, label, or extra fragment remains.

### Individual sticker PNGs

- Exactly nine files exist, named `sticker-01.png` through `sticker-09.png` in row-major order.
- Every file is RGBA with transparent corners and contains exactly one complete sticker.
- Each sticker is a direct, unscaled crop of the validated sheet and retains its full narrow warm-white cut border.
- No neighboring sticker, background, shadow, label, or chroma-key fringe appears in any file.
- Exactly nine 160×160 transparent WebP previews exist in the `previews` subdirectory, match their corresponding stickers, and remain substantially smaller than the originals.

### Sticker packaging preview

- The preview is an opaque 3:4 portrait product-style image composed after the transparent PNG validation succeeds, using a generated blank background and the bundled deterministic compositor. The backing card is short enough to leave more vertical area for visibly larger stickers.
- It shows exactly nine recognizable stickers from the validated PNG, with no redesign, duplication, cropping, or extra motif.
- The source-derived backing-card color matches the selection JSON: sample a representative card region away from text, hole, edges, and shadow; its Lab distance from the selected HEX should be no more than 8 after allowing for paper texture and lighting. It reaches at least 4.5:1 contrast against cream `#F4E7C8`, and its Lab distance from every dominant visible sticker color is at least 18. The card touches the top edge, spans the full image width with no top blank strip or side gutters, and occupies only about 15–17% of the canvas height. Its centered hang hole, dynamic title, and exact `9 PIECES` label are present and legible; no other text is needed.
- The nine stickers occupy a strict 3×3 grid with visibly larger sticker coverage: matching left/right outer margins, matching column gaps, matching row gaps, and matching top/bottom visible-boundary margins. The compositor must make the top margin from the backing card's lower edge to the highest sticker cut border equal to the bottom margin from the lowest sticker cut border to the canvas bottom, with no oversized blank band below the grid. The warm cream paper background, subtle grain, soft diffused lighting, and restrained external sticker shadows create a physical stationery product presentation.
- No checkerboard, source photo, unrelated props, platform UI, watermark, or transparent-background claim appears in this preview.

## Delivery

Show the three primary images and provide separate file links for the card, transparent nine-sticker sheet, packaging preview, packaging color-selection JSON, all nine individual PNGs, and their preview directory. Label the groups clearly as `完整旅行记忆卡`, `透明底九枚贴纸 PNG`, `九张单枚透明贴纸 PNG`, `轻量预览图`, and `贴纸商品包装展示图`. Briefly name the identification anchor(s), the nine sticker motifs, the three English keyword phrases, the selected card HEX and contrast ratio, and every saved path. Clearly identify WebP files as previews rather than full-resolution assets. State that a dark or checkerboard preview behind a transparent asset represents transparency only after Alpha validation succeeds; do not describe the opaque packaging preview as transparent.
