#!/usr/bin/env python3
"""
Showcase Image Generator
Creates a preview image showing up to 3 final App Store screenshots
side-by-side on a white background with an optional GitHub link at the bottom.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ── Layout ──────────────────────────────────────────────────────────
PADDING = 60
GAP = 40
BOTTOM_BAR_H = 100
FONT_SIZE_MAX = 48
FONT_SIZE_MIN = 16
TEXT_COLOUR = "#000000"
BG_COLOUR = (255, 255, 255)
SKILL_DIR = Path(__file__).resolve().parents[1]
FONT_DIR_CANDIDATES = [SKILL_DIR / ".fonts", SKILL_DIR / "fonts"]
PREFERRED_BUNDLED_FONTS = [
    "Arial.ttf",
    "DejaVuSans.ttf",
    "Arial Bold.ttf",
    "dejavu-sans-bold.ttf",
]


def bundled_font_candidates():
    candidates = []
    for font_dir in FONT_DIR_CANDIDATES:
        if not font_dir.exists():
            continue
        for name in PREFERRED_BUNDLED_FONTS:
            path = font_dir / name
            if path.exists():
                candidates.append(path)
        for path in sorted(font_dir.glob("*")):
            if path.suffix.lower() in {".ttf", ".otf"} and path not in candidates:
                candidates.append(path)
    return [str(path) for path in candidates]


DEFAULT_FONT_CANDIDATES = [
    *bundled_font_candidates(),
    "/Library/Fonts/SF-Pro-Display-Regular.otf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def resolve_font(font_path=None):
    candidates = [font_path] if font_path else []
    candidates.extend(DEFAULT_FONT_CANDIDATES)
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def fit_text_font(text, max_w, size_max, size_min, font_path):
    """Return the largest font size where text fits within max_w."""
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for size in range(size_max, size_min - 1, -2):
        if font_path:
            font = ImageFont.truetype(font_path, size)
        else:
            font = ImageFont.load_default()
            return font
        bbox = dummy.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            return font
    if font_path:
        return ImageFont.truetype(font_path, size_min)
    return ImageFont.load_default()


def create_showcase(screenshots, output_path, github_url=None, font_path=None):
    images = [Image.open(p).convert("RGBA") for p in screenshots]

    target_h = 800
    scaled = []
    for img in images:
        ratio = target_h / img.height
        scaled.append(img.resize((int(img.width * ratio), target_h), Image.LANCZOS))

    total_w = sum(s.width for s in scaled) + GAP * (len(scaled) - 1) + PADDING * 2
    total_h = target_h + PADDING * 2 + (BOTTOM_BAR_H if github_url else 0)

    canvas = Image.new("RGB", (total_w, total_h), BG_COLOUR)

    x = PADDING
    for s in scaled:
        canvas.paste(s, (x, PADDING), s if s.mode == "RGBA" else None)
        x += s.width + GAP

    if github_url:
        draw = ImageDraw.Draw(canvas)
        max_text_w = total_w - PADDING * 2
        font = fit_text_font(github_url, max_text_w, FONT_SIZE_MAX, FONT_SIZE_MIN, font_path)

        text_y = PADDING + target_h + (BOTTOM_BAR_H // 2)
        draw.text(
            (total_w // 2, text_y),
            github_url,
            fill=TEXT_COLOUR,
            font=font,
            anchor="mm",
        )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, "PNG")
    print(f"✓ {output_path} ({total_w}×{total_h})")


def main():
    p = argparse.ArgumentParser(description="Generate showcase image")
    p.add_argument(
        "--screenshots",
        nargs="+",
        required=True,
        help="Paths to final screenshot PNGs (up to 3)",
    )
    p.add_argument("--output", required=True, help="Output file path")
    p.add_argument("--github", default=None, help="GitHub URL to display at bottom")
    p.add_argument("--font", help="Optional .ttf/.otf font for the footer text")
    args = p.parse_args()

    create_showcase(args.screenshots, args.output, args.github, resolve_font(args.font))


if __name__ == "__main__":
    main()
