#!/usr/bin/env python3
"""Objective Anti-AI quality gate for scientific figures."""

import argparse
from pathlib import Path
import sys

import numpy as np
from PIL import Image


def rgb_to_hsv_np(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    arr = rgb.astype(np.float32) / 255.0
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin

    sat = np.where(cmax > 1e-6, delta / np.maximum(cmax, 1e-6), 0.0)
    val = cmax
    return delta, sat, val


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run objective Anti-AI visual quality checks on a scientific figure."
    )
    parser.add_argument("--image", required=True, help="Rendered figure PNG/JPG path")
    parser.add_argument(
        "--allow-dark",
        action="store_true",
        help="Allow dark background (e.g. fluorescence microscopy)",
    )
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"[ERROR] Image not found: {img_path}", file=sys.stderr)
        return 1

    raw_img = Image.open(img_path)
    if raw_img.mode in ("RGBA", "LA") or (raw_img.mode == "P" and "transparency" in raw_img.info):
        rgba = raw_img.convert("RGBA")
        white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        img = Image.alpha_composite(white_bg, rgba).convert("RGB")
    else:
        img = raw_img.convert("RGB")
    w, h = img.size
    rgb = np.array(img)
    _, sat, val = rgb_to_hsv_np(rgb)

    failures: list[str] = []
    warnings: list[str] = []

    # 1. Resolution check
    if w < 1600:
        failures.append(f"Resolution too low: {w}x{h}px (minimum width 1600px recommended)")

    # 2. Pure white border check (catches AI gray background / vignette)
    if not args.allow_dark:
        b = min(8, h // 20, w // 20)
        border_pixels = np.concatenate(
            [
                rgb[:b, :, :].reshape(-1, 3),
                rgb[-b:, :, :].reshape(-1, 3),
                rgb[:, :b, :].reshape(-1, 3),
                rgb[:, -b:, :].reshape(-1, 3),
            ],
            axis=0,
        )
        pure_white = np.all(border_pixels >= 250, axis=1)
        white_ratio = float(np.mean(pure_white))
        if white_ratio < 0.90:
            failures.append(
                f"Border pure-white ratio is {white_ratio:.1%} (< 90%). "
                "Detected off-white/gray background or vignette."
            )
        elif white_ratio < 0.97:
            warnings.append(
                f"Border pure-white ratio is {white_ratio:.1%}. Check for clipped elements near margins."
            )

    # 3. Neon / hyper-saturated sci-fi glow check
    neon_mask = (sat > 0.85) & (val > 0.70)
    neon_ratio = float(np.mean(neon_mask))
    if neon_ratio > 0.05:
        failures.append(
            f"Hyper-saturated neon pixels: {neon_ratio:.2%} (> 5%). "
            "Likely contains AI-style neon gradient or glow effects."
        )
    elif neon_ratio > 0.02:
        warnings.append(
            f"Elevated high-saturation pixels: {neon_ratio:.2%}. Consider muting palette."
        )

    # 4. Dark area check
    dark_ratio = float(np.mean(val < 0.20))
    if not args.allow_dark:
        if dark_ratio > 0.25:
            failures.append(
                f"Dark pixel ratio is {dark_ratio:.1%} (> 25%). "
                "Scientific figures should use high-key light backgrounds."
            )
        elif dark_ratio > 0.15:
            warnings.append(f"Dark pixel ratio is {dark_ratio:.1%}. Verify contrast readability.")

    print(f"=== Anti-AI Scientific Figure Audit: {img_path.name} ===")
    print(f"Resolution        : {w}x{h}px")
    if not args.allow_dark:
        print(f"Border Pure-White : {white_ratio:.1%}")
    print(f"Neon Pixel Ratio  : {neon_ratio:.2%}")
    print(f"Dark Pixel Ratio  : {dark_ratio:.1%}")

    for warn in warnings:
        print(f"[WARN] {warn}")
    for fail in failures:
        print(f"[FAIL] {fail}")

    if failures:
        print("RESULT: FAIL — Fix flagged layers before delivery.")
        return 1

    print("RESULT: PASS — Objective Anti-AI gate passed. Proceed to visual inspection.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
