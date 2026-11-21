#!/usr/bin/env python3
"""Render an HTML/SVG scientific figure to high-DPI PNG (and optional vector PDF) via Headless Chrome."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
]


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if path and os.path.exists(path):
            return path
    raise FileNotFoundError(
        "No Chrome/Chromium binary found. Install Google Chrome or set CHROME_BIN."
    )


def render_png(
    chrome: str,
    html_path: Path,
    output_path: Path,
    width: int,
    height: int,
    scale: float,
    budget_ms: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    file_url = html_path.resolve().as_uri()
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--default-background-color=ffffffff",
        f"--window-size={width},{height}",
        f"--force-device-scale-factor={scale}",
        f"--virtual-time-budget={budget_ms}",
        f"--screenshot={output_path.resolve()}",
        file_url,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not output_path.exists():
        raise RuntimeError(
            f"Chrome PNG render failed (code {res.returncode}):\n{res.stderr}"
        )

    # Ensure exact target pixel dimensions (trim/pad pure white if Chrome viewport adds extra rows)
    target_w = int(round(width * scale))
    target_h = int(round(height * scale))
    with Image.open(output_path) as img:
        img = img.convert("RGB")
        if img.size != (target_w, target_h):
            canvas = Image.new("RGB", (target_w, target_h), (255, 255, 255))
            crop = img.crop((0, 0, min(img.width, target_w), min(img.height, target_h)))
            canvas.paste(crop, (0, 0))
            canvas.save(output_path, format="PNG", optimize=True)


def render_pdf(chrome: str, html_path: Path, pdf_path: Path, budget_ms: int) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    file_url = html_path.resolve().as_uri()
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--virtual-time-budget={budget_ms}",
        f"--print-to-pdf={pdf_path.resolve()}",
        file_url,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(
            f"Chrome PDF render failed (code {res.returncode}):\n{res.stderr}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render HTML/SVG scientific figure to high-DPI PNG / PDF."
    )
    parser.add_argument("--html", required=True, help="Input HTML file path")
    parser.add_argument("--output", required=True, help="Output PNG file path")
    parser.add_argument("--pdf", default="", help="Optional output vector PDF path")
    parser.add_argument("--width", type=int, default=1600, help="CSS viewport width (px)")
    parser.add_argument("--height", type=int, default=960, help="CSS viewport height (px)")
    parser.add_argument("--scale", type=float, default=2.0, help="Device scale factor (DPR)")
    parser.add_argument(
        "--budget-ms", type=int, default=2500, help="Chrome virtual time budget (ms)"
    )
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        print(f"[ERROR] HTML file not found: {html_path}", file=sys.stderr)
        return 1

    chrome = os.environ.get("CHROME_BIN") or find_chrome()
    out_png = Path(args.output)
    render_png(chrome, html_path, out_png, args.width, args.height, args.scale, args.budget_ms)
    with Image.open(out_png) as img:
        print(f"[OK] Rendered PNG: {out_png} ({img.width}x{img.height}px)")

    if args.pdf:
        out_pdf = Path(args.pdf)
        render_pdf(chrome, html_path, out_pdf, args.budget_ms)
        print(f"[OK] Rendered PDF: {out_pdf}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
