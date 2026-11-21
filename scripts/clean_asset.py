#!/usr/bin/env python3
"""Clean an isolated scientific asset: flood-fill remove white/near-white background, soften edges, trim, and optionally reduce excess saturation."""

import argparse
from collections import deque
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


def estimate_bg_color(rgb: np.ndarray) -> np.ndarray:
    h, w, _ = rgb.shape
    patches = np.concatenate(
        [
            rgb[0:6, 0:6].reshape(-1, 3),
            rgb[0:6, max(0, w - 6) : w].reshape(-1, 3),
            rgb[max(0, h - 6) : h, 0:6].reshape(-1, 3),
            rgb[max(0, h - 6) : h, max(0, w - 6) : w].reshape(-1, 3),
        ],
        axis=0,
    )
    return np.median(patches, axis=0)


def flood_remove_bg(rgb: np.ndarray, tol: float) -> np.ndarray:
    """Remove exterior background connected to image borders without punching holes inside the subject."""
    h, w, _ = rgb.shape
    bg_color = estimate_bg_color(rgb)
    dist = np.linalg.norm(rgb.astype(np.float32) - bg_color.astype(np.float32), axis=2)
    is_bg_candidate = dist <= tol

    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    # Seed from all 4 borders
    for x in range(w):
        if is_bg_candidate[0, x]:
            visited[0, x] = True
            q.append((0, x))
        if is_bg_candidate[h - 1, x] and not visited[h - 1, x]:
            visited[h - 1, x] = True
            q.append((h - 1, x))
    for y in range(h):
        if is_bg_candidate[y, 0] and not visited[y, 0]:
            visited[y, 0] = True
            q.append((y, 0))
        if is_bg_candidate[y, w - 1] and not visited[y, w - 1]:
            visited[y, w - 1] = True
            q.append((y, w - 1))

    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and is_bg_candidate[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

    alpha = np.where(visited, 0, 255).astype(np.uint8)

    # Gentle edge feathering to remove harsh 1px white halo
    alpha_img = Image.fromarray(alpha, mode="L")
    blurred = np.array(alpha_img.filter(ImageFilter.GaussianBlur(radius=0.8)), dtype=np.uint8)
    # Only soften pixels near the border of the mask
    border = (blurred > 0) & (blurred < 255)
    alpha[border] = np.minimum(alpha[border], blurred[border])
    return alpha


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clean isolated AI/3D asset for scientific figure compositing."
    )
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output transparent PNG path")
    parser.add_argument(
        "--tol",
        type=float,
        default=28.0,
        help="Color distance tolerance for exterior background removal (default: 28)",
    )
    parser.add_argument(
        "--desaturate",
        type=float,
        default=0.10,
        help="Fraction to reduce color saturation (0.0-0.5, default: 0.10)",
    )
    parser.add_argument(
        "--pad", type=int, default=8, help="Transparent padding around trimmed subject (px)"
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[ERROR] Input not found: {in_path}", file=sys.stderr)
        return 1

    raw_img = Image.open(in_path)
    if raw_img.mode in ("RGBA", "LA") or (raw_img.mode == "P" and "transparency" in raw_img.info):
        rgba = raw_img.convert("RGBA")
        white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        img = Image.alpha_composite(white_bg, rgba).convert("RGB")
    else:
        img = raw_img.convert("RGB")
    if args.desaturate > 0:
        factor = max(0.0, 1.0 - args.desaturate)
        img = ImageEnhance.Color(img).enhance(factor)

    rgb = np.array(img)
    alpha = flood_remove_bg(rgb, tol=args.tol)
    rgba = np.dstack([rgb, alpha])
    out_img = Image.fromarray(rgba, mode="RGBA")

    bbox = out_img.getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        x0 = max(0, x0 - args.pad)
        y0 = max(0, y0 - args.pad)
        x1 = min(out_img.width, x1 + args.pad)
        y1 = min(out_img.height, y1 + args.pad)
        out_img = out_img.crop((x0, y0, x1, y1))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Cleaned asset saved: {out_path} ({out_img.width}x{out_img.height}px)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
