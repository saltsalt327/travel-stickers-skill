#!/usr/bin/env python3
"""Export a validated nine-sticker RGBA sheet as nine individual PNG files."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from PIL import Image

from compose_packaging_preview import extract_sticker_crops


def make_preview(sticker: Image.Image, size: int) -> Image.Image:
    """Center a sticker on a small square transparent preview canvas."""
    if size < 64:
        raise ValueError("preview size must be at least 64 pixels")
    content_size = size - max(12, round(size * 0.1))
    thumbnail = sticker.copy()
    thumbnail.thumbnail((content_size, content_size), Image.Resampling.LANCZOS)
    preview = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - thumbnail.width) // 2
    y = (size - thumbnail.height) // 2
    preview.alpha_composite(thumbnail, (x, y))
    return preview


def export_individual_stickers(
    input_path: Path,
    output_dir: Path,
    padding: int = 12,
    preview_dir: Optional[Path] = None,
    preview_size: int = 160,
    preview_quality: int = 72,
) -> list[Path]:
    if not 1 <= preview_quality <= 100:
        raise ValueError("preview quality must be between 1 and 100")
    if preview_dir is None:
        preview_dir = output_dir / "previews"

    with Image.open(input_path) as source:
        if source.format != "PNG":
            raise ValueError(f"sticker source must be a PNG, got {source.format or 'unknown'}")
        if source.mode != "RGBA":
            raise ValueError(f"sticker source must be RGBA, got {source.mode}")

        alpha = source.getchannel("A")
        corners = (
            alpha.getpixel((0, 0)),
            alpha.getpixel((source.width - 1, 0)),
            alpha.getpixel((0, source.height - 1)),
            alpha.getpixel((source.width - 1, source.height - 1)),
        )
        if corners != (0, 0, 0, 0):
            raise ValueError(f"all source corners must be transparent, got {corners}")

        stickers = extract_sticker_crops(source, padding=padding)
        output_dir.mkdir(parents=True, exist_ok=True)
        preview_dir.mkdir(parents=True, exist_ok=True)
        output_paths = []
        for index, sticker in enumerate(stickers, start=1):
            alpha = sticker.getchannel("A")
            edge_values = (
                list(alpha.crop((0, 0, sticker.width, 1)).getdata())
                + list(alpha.crop((0, sticker.height - 1, sticker.width, sticker.height)).getdata())
                + list(alpha.crop((0, 0, 1, sticker.height)).getdata())
                + list(alpha.crop((sticker.width - 1, 0, sticker.width, sticker.height)).getdata())
            )
            if any(edge_values):
                raise ValueError(f"sticker-{index:02d} does not have transparent padding on every side")
            output_path = output_dir / f"sticker-{index:02d}.png"
            sticker.save(output_path, "PNG")
            output_paths.append(output_path)

            preview = make_preview(sticker, preview_size)
            preview_path = preview_dir / f"sticker-{index:02d}-preview.webp"
            preview.save(preview_path, "WEBP", quality=preview_quality, method=6)

    print(
        f"Wrote {len(output_paths)} individual RGBA stickers to {output_dir} "
        f"and {len(output_paths)} lightweight previews to {preview_dir}"
    )
    return output_paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Validated nine-sticker RGBA PNG")
    parser.add_argument("--out-dir", type=Path, required=True, help="Directory for sticker-01.png through sticker-09.png")
    parser.add_argument("--padding", type=int, default=12, help="Transparent pixels retained around each sticker")
    parser.add_argument("--preview-dir", type=Path, help="Preview directory; defaults to <out-dir>/previews")
    parser.add_argument("--preview-size", type=int, default=160, help="Square preview size in pixels")
    parser.add_argument("--preview-quality", type=int, default=72, help="Lossy WebP quality from 1 to 100")
    args = parser.parse_args()
    export_individual_stickers(
        args.input,
        args.out_dir,
        args.padding,
        args.preview_dir,
        args.preview_size,
        args.preview_quality,
    )


if __name__ == "__main__":
    main()
