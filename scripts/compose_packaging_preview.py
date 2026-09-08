#!/usr/bin/env python3
"""Compose a generated packaging plate and a validated nine-sticker PNG on a fixed grid."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter


def connected_components(alpha: Image.Image, threshold: int = 8, minimum: int = 500):
    """Return exactly nine substantial alpha regions in row-major order."""
    width, height = alpha.size
    pixels = alpha.load()
    visited = bytearray(width * height)
    regions = []

    for y in range(height):
        for x in range(width):
            index = y * width + x
            if visited[index] or pixels[x, y] <= threshold:
                continue
            visited[index] = 1
            queue = deque([(x, y)])
            min_x = max_x = x
            min_y = max_y = y
            count = 0
            while queue:
                current_x, current_y = queue.popleft()
                count += 1
                min_x = min(min_x, current_x)
                max_x = max(max_x, current_x)
                min_y = min(min_y, current_y)
                max_y = max(max_y, current_y)
                for delta_y in (-1, 0, 1):
                    for delta_x in (-1, 0, 1):
                        if not delta_x and not delta_y:
                            continue
                        next_x = current_x + delta_x
                        next_y = current_y + delta_y
                        if next_x < 0 or next_y < 0 or next_x >= width or next_y >= height:
                            continue
                        next_index = next_y * width + next_x
                        if visited[next_index] or pixels[next_x, next_y] <= threshold:
                            continue
                        visited[next_index] = 1
                        queue.append((next_x, next_y))
            if count >= minimum:
                regions.append((min_x, min_y, max_x + 1, max_y + 1, count))

    if len(regions) != 9:
        raise ValueError(f"expected 9 sticker regions, found {len(regions)}")
    by_top = sorted(regions, key=lambda region: region[1])
    gaps = sorted(
        range(len(by_top) - 1),
        key=lambda index: by_top[index + 1][1] - by_top[index][1],
        reverse=True,
    )[:2]
    split_points = sorted(index + 1 for index in gaps)
    rows = [by_top[: split_points[0]], by_top[split_points[0] : split_points[1]], by_top[split_points[1] :]]
    if any(len(row) != 3 for row in rows):
        raise ValueError("expected a 3x3 sticker source layout")
    ordered = []
    for row in rows:
        ordered.extend(sorted(row, key=lambda region: region[0]))
    return ordered


def extract_sticker_crops(stickers: Image.Image, padding: int = 2) -> list[Image.Image]:
    """Crop the nine stickers without resizing or altering their RGBA pixels."""
    if stickers.mode != "RGBA":
        raise ValueError(f"sticker source must be RGBA, got {stickers.mode}")
    if padding < 1:
        raise ValueError("padding must be at least 1 pixel")

    crops = []
    for min_x, min_y, max_x, max_y, _ in connected_components(stickers.getchannel("A")):
        crop = stickers.crop((min_x, min_y, max_x, max_y))
        padded = Image.new("RGBA", (crop.width + 2 * padding, crop.height + 2 * padding), (0, 0, 0, 0))
        padded.alpha_composite(crop, (padding, padding))
        crops.append(padded)
    return crops


def fit(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    scale = min(max_width / image.width, max_height / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def add_sticker(canvas: Image.Image, sticker: Image.Image, x: int, y: int) -> None:
    alpha = sticker.getchannel("A")
    shadow_alpha = alpha.filter(ImageFilter.GaussianBlur(5)).point(lambda value: round(value * 0.18))
    shadow = Image.new("RGBA", sticker.size, (73, 65, 51, 0))
    shadow.putalpha(shadow_alpha)
    canvas.alpha_composite(shadow, (x, y + 3))
    canvas.alpha_composite(sticker, (x, y))


def compose(background_path: Path, stickers_path: Path, output_path: Path, card_bottom: int) -> None:
    background = Image.open(background_path).convert("RGBA")
    stickers = Image.open(stickers_path).convert("RGBA")
    width, height = background.size
    crops = extract_sticker_crops(stickers, padding=2)

    side_margin = round(width * 0.05)
    desired_column_gap = round(width * 0.025)
    top_bottom_margin = round(height * 0.025)
    desired_row_gap = round(height * 0.018)
    available_width = width - 2 * side_margin - 2 * desired_column_gap
    available_height = height - card_bottom - 2 * top_bottom_margin - 2 * desired_row_gap
    cell_width = available_width // 3
    cell_height = available_height // 3
    max_width = max(1, round(cell_width * 0.97))
    max_height = max(1, round(cell_height * 0.97))
    fitted = [fit(crop, max_width, max_height) for crop in crops]

    column_widths = [max(fitted[row * 3 + column].width for row in range(3)) for column in range(3)]
    row_heights = [max(fitted[row * 3 + column].height for column in range(3)) for row in range(3)]
    column_gap = (width - 2 * side_margin - sum(column_widths)) // 2
    row_gap = (height - card_bottom - 2 * top_bottom_margin - sum(row_heights)) // 2
    if column_gap <= 0 or row_gap <= 0:
        raise ValueError("sticker scale is too large for the requested margins")

    column_lefts = []
    cursor = side_margin
    for column_width in column_widths:
        column_lefts.append(cursor)
        cursor += column_width + column_gap

    grid_top = card_bottom + top_bottom_margin
    row_tops = []
    cursor = grid_top
    for row_height in row_heights:
        row_tops.append(cursor)
        cursor += row_height + row_gap

    for index, sticker in enumerate(fitted):
        row, column = divmod(index, 3)
        x = column_lefts[column] + (column_widths[column] - sticker.width) // 2
        y = row_tops[row] + (row_heights[row] - sticker.height) // 2
        add_sticker(background, sticker, x, y)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    background.convert("RGB").save(output_path, "PNG")
    print(
        f"Wrote {output_path} | {width}x{height} | "
        f"side={side_margin}px column_gap={column_gap}px "
        f"top_bottom={top_bottom_margin}px row_gap={row_gap}px"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", type=Path, required=True)
    parser.add_argument("--stickers", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--card-bottom", type=int, required=True, help="Visible lower edge of backing card in pixels")
    args = parser.parse_args()
    compose(args.background, args.stickers, args.out, args.card_bottom)


if __name__ == "__main__":
    main()
