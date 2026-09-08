# Visual style guide

## Core language

Record a place through selective memory rather than descriptive realism. Combine an airy city-travel illustration with traditional watercolor behavior: transparent layered washes, loose architectural ink contours, dry-brush foliage, warm paper, restrained accents, and quiet negative space.

## Shape and material

- Make the scene read first as 3–6 clear masses with a strong perspective path. Keep the dominant sky, paper, or atmospheric field broad and calm.
- Build scenery with readable architectural perspective, layered transparent planes, pale distant forms, and selective structural lines for façades, windows, balconies, roofs, streets, and trees.
- Use transparent watercolor washes with wet-on-wet atmosphere, wet-on-dry details, pigment pooling, soft blooms, subtle granulation, dry-brush bark and foliage, and reserved paper-white highlights. Apply a fine, natural watercolor-paper tooth consistently across image and stickers.
- Use thin, loose, irregular gray-brown or olive ink contours. Mix crisp focal edges with broken, feathered, and dissolving edges; keep line weight varied and never mechanically uniform.
- Do not create photorealistic patches, thick black outlines, marker bands, flat opaque fills, smooth digital gradients, repeated decorative linework, pebble dots, or overworked botanical detail.

## Color and typography

- Derive 5–8 color families from the source. Favor warm ivory, sage and olive greens, pale sky blue, cool blue-gray, warm stone, ochre, terracotta, muted red, and occasional teal accents. Keep the overall palette light and moderately restrained, with selective saturated color notes.
- Use transparent cool blue-gray or green-gray shadow washes rather than flat digital shadows or gradients. Keep black sparse and soften distant colors for atmospheric depth.
- Set exactly three short English keyword phrases once in a small, quiet footer beneath the left image, separated by centered dots. Use muted ink and let the exposed paper carry them without a box or label.

## Card composition

- Keep a continuous warm-paper border around the entire card.
- Leave the left image completely unframed and visually dominant. Reserve only a shallow exposed-paper strip beneath it for the keyword footer.
- Treat the nine right-column stickers as memory fragments, not a catalog: use uneven scale, three loose staggered rows, relaxed spacing, narrow warm-white cut edges, and subtle flat shadows. Render the sticker art in the same airy watercolor-and-ink medium as the card.

## Transparent sticker composition

- Treat the finished card stickers as the immutable visual master.
- Keep exactly nine stickers, their narrow warm-white cut edges, relative size hierarchy, source-derived palette, and watercolor-and-ink medium.
- Arrange the stickers in three loose rows of three with enough empty transparent space for easy reuse.
- Use no shadows, overall paper, captions, labels, footer, or decorative fragments.

## Individual sticker exports

- Treat the validated transparent nine-sticker sheet as the only source. Crop each sticker directly; never regenerate or reinterpret it.
- Export `sticker-01.png` through `sticker-09.png` in left-to-right, top-to-bottom order.
- Preserve the original RGBA pixels, full narrow warm-white cut border, and transparent padding on every side. Do not resize, repaint, sharpen, recolor, or add shadows.
- Each file must contain exactly one complete sticker and no neighboring sticker, paper, label, or chroma-key fringe.
- Create a matching 160×160 transparent WebP browsing preview for each full PNG. Center the scaled sticker with breathing room, preserve its aspect ratio and warm-white border, and keep previews clearly separated from the original assets.

## Sticker packaging preview composition

- Treat this as the fourth, presentation-only deliverable generated after the transparent PNG has been validated. It is an opaque retail product mockup, not a replacement for the transparent asset.
- Use the validated transparent PNG as the immutable visual master. Preserve exactly nine sticker motifs, their watercolor-and-ink artwork, narrow warm-white cut borders, and source-derived palette; scale them up within the fixed grid without changing their identities.
- Use a 3:4 portrait, near top-down layout on a warm cream matte paper background with subtle natural grain and soft diffused daylight. Keep the presentation clean, quiet, and suitable for a stationery product listing.
- Derive the backing-card color from the supplied photo palette for each set; never make blue-gray the universal default. Choose a dark, restrained variant of a meaningful source color, require at least 4.5:1 contrast against cream `#F4E7C8`, and keep clear perceptual separation from the dominant visible sticker colors. Prefer a supporting or underused source hue over the hue that already occupies the largest sticker areas.
- Place the selected-color paper backing card flush to the top edge and full-bleed across the entire image width. Target roughly 15–17% of the image height for the card; if the generated plate is taller than 18%, regenerate it. Do not leave a top margin, cream strip, or left/right gutter around the card; let the canvas crop the top corners if needed. Keep slightly softened lower corners, subtle thickness and shadow, a centered retail hang hole, and centered `#F4E7C8` typography. Use a large uppercase serif title: `[PLACE] DAYS` only when the place is confidently known, otherwise `TRAVEL DAYS`. Place the exact `9 PIECES` quantity label beneath in small uppercase sans-serif type.
- Arrange the nine stickers below the backing card with the bundled deterministic compositor, based on the stickers' visible outer cut borders rather than approximate optical placement. Divide the usable lower area into a strict 3×3 grid, use identical left and right outer margins, identical column gutters, identical row gutters, and equal top and bottom visible-boundary margins. Target about 5% of canvas width for each side margin, about 2.5% for each column gutter, and about 2.5% of canvas height for both the gap below the card and the bottom margin. Increase each sticker's occupancy within its cell so the pieces read larger while retaining the fine 3–6 px cut border. Center one complete sticker in each cell, preserve its original aspect ratio, and use the same occupancy rule in every cell. Keep all nine face-up, separated, and fully visible; do not stagger, scatter, overlap, or vary the grid spacing.
- Add only subtle external contact/drop shadows to the stickers and backing card to suggest physical paper goods. Do not alter the sticker artwork or widen the narrow borders.
- Keep the preview background opaque. Do not place the source photo, checkerboard, unrelated props, platform UI, watermarks, or extra text in the composition. The reference-specific title `JEJU DAYS` is not a fixed template value.

## Avoid

- Photographic patches, painterly photo filters, lens blur, film grain, or realistic texture.
- Visible marker strokes, uncontrolled muddy washes, harsh digital gradients, glossy 3D, or smooth vector precision.
- Detailed faces, anatomy, fabric folds, botanically exact leaves, branches, vehicle mechanics, geology, or decorative filler.
- Do not add titles, captions, dates, postal marks, watermarks, signatures, or source text to the complete card or transparent PNG. The packaging preview may contain only the dynamic title and exact `9 PIECES` label specified above.
- Broad sticker borders, fake transparency, checkerboards baked into the bitmap, residual chroma color, or an opaque background in the sticker PNG.
