# Travel Memory Card Duo

一个用于 Codex 的旅行记忆卡技能。输入 1–5 张照片后，它会按顺序输出四类彼此匹配的素材：

1. **完整旅行记忆卡**：3:2 横版卡片，包含主插画、三个英文关键词和九枚贴纸。
2. **独立透明贴纸 PNG**：额外输出一张单独的 `.png` 文件，只保留与完整卡片相同的九枚贴纸。
3. **九张单枚透明贴纸 PNG 和轻量预览图**：从验证通过的九枚总图自动裁切出 `sticker-01.png` 到 `sticker-09.png`，保留完整暖白切边和透明背景，并为每张生成一张 160×160 透明 WebP 预览图。
4. **贴纸商品包装展示图**：在透明 PNG 验证完成后，再生成一张 3:4 竖版的实体贴纸包装预览图。

## 透明 PNG 版本的含义

透明贴纸图不是从完整卡片中截取出来的预览，也不是把贴纸放在白底或棋盘格底上。它是一个独立交付文件：

- 文件格式为 **PNG**；
- 图像带有真实 **Alpha 透明通道（RGBA）**；
- 整张纸张背景被移除；
- 九枚贴纸保留窄一些的暖白色手剪边缘；
- 不含标题、关键词、标签、阴影或其他装饰；
- 可直接用于二次排版、社交媒体、数字手账或贴纸打印准备。

包装展示图是独立的商品陈列预览，不是透明 PNG 的替代品。它会先根据照片主色与贴纸可见色彩自动选择较深、较克制的包装卡颜色，要求与奶油色文字 `#F4E7C8` 至少达到 4.5:1 对比度，并避开已经主导贴纸主体的大面积颜色。随后生成较矮的满幅贴顶包装卡、挂孔、动态地点标题、`9 PIECES` 数量标识和暖米白纸张背景，再用固定排版脚本放置九枚贴纸；包装卡下方的九枚贴纸按严格三列×三行网格排列，以贴纸实际可见的最外层切边为测量基准，左右外边距、列间距、行间距，以及包装卡下缘到第一排贴纸与最后一排贴纸到底边的上下留白统一，同时提高九枚贴纸在网格中的占用面积。贴纸切边进一步缩窄为约 3–6 px。包装背景和阴影只存在于展示图中，不会进入透明 PNG。

九张单枚贴纸不会再次调用图像模型，而是直接从验证通过的透明总图按从左到右、从上到下的顺序裁切。每张保持 RGBA、原始像素和完整暖白切边，并在四周保留透明安全边距。配套 WebP 预览图使用统一 160×160 透明画布，仅用于快速浏览、网页列表或聊天预览，正式排版仍应使用原始 PNG。

## Four coordinated deliverables

Given one to five source photos, this Codex skill produces:

1. A finished 3:2 collectible travel memory card.
2. A separate transparent-background `.png` sticker image containing the same nine sticker motifs.
3. Nine individual transparent PNG files named `sticker-01.png` through `sticker-09.png`, plus nine lightweight 160×160 transparent WebP previews.
4. A 3:4 opaque retail-style sticker-packaging preview generated only after the transparent PNG passes validation.

The sticker PNG is a real RGBA file with an Alpha channel, not a flattened image with a white, black, or checkerboard background.

## Usage

```text
使用 $travel-memory-card-duo 把我上传的 1–5 张照片做成完整旅行记忆卡、同款九枚窄白边透明底 PNG 贴纸总图、九张单枚透明 PNG，并在透明 PNG 验证通过后生成贴纸商品包装展示图。
```

## Files

- `SKILL.md` — workflow and output requirements
- `agents/openai.yaml` — Codex UI metadata
- `references/style-guide.md` — shared visual language for every deliverable
- `scripts/export_individual_stickers.py` — exports nine individual RGBA PNGs and matching lightweight WebP previews
- `scripts/select_packaging_card_color.py` — selects a source-derived backing-card color with contrast and sticker-separation checks
- `scripts/compose_packaging_preview.py` — deterministic 3×3 packaging-grid compositor

## Installation

Copy this repository folder into your Codex skills directory, then invoke it as `$travel-memory-card-duo`.

## 案例

<img width="1536" height="1024" alt="Travel memory card example" src="https://github.com/user-attachments/assets/6bf06b40-9115-4619-b4bc-9cb2250031ee" />
<img width="1536" height="1024" alt="Transparent sticker PNG example" src="https://github.com/user-attachments/assets/2cab6521-dde5-4af7-9fec-2d5609585354" />

## License and usage restrictions

Copyright © 2026 carolinaaafy. All rights reserved.

Personal, non-commercial use is permitted. Re-uploading, mirroring, repackaging, copying for redistribution, selling, paid-service use, client projects, and other commercial exploitation are prohibited.

Source photographs, likenesses, landmarks, trademarks, and other third-party content are not licensed by this repository.

See [LICENSE.md](LICENSE.md) for the complete terms. This repository is source-available, not open source.
