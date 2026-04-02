# ASO App Store Screenshots

Codex skill for turning an iOS app project plus simulator captures into an App Store screenshot set.

## What It Does

- Analyzes an app codebase and proposes 3-5 conversion-focused screenshot benefits.
- Reviews simulator screenshots and rates them as `Great`, `Usable`, or `Retake`.
- Pairs each confirmed benefit with the best available screen.
- Generates deterministic screenshot scaffolds with consistent text and device placement.
- Supports an optional AI-enhancement phase when an image tool is available.
- Saves progress in `screenshots/aso-state.md` so work can resume cleanly.

## Repository Contents

```text
.
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── assets/device_frame.png
├── fonts/
└── scripts/
    ├── compose.py
    ├── generate_frame.py
    └── showcase.py
```

## Install

Clone this repository directly into Codex as the `aso-appstore-screenshots` skill:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/mzgs/ASO-App-Store-Screenshots-for-Codex.git \
  ~/.codex/skills/aso-appstore-screenshots
```



Restart Codex after installing so the new skill is loaded.

## Prerequisites

- Python 3
- `Pillow`
- Simulator screenshots from the iOS app you want to market
- Optional image generation or image editing tooling for the enhancement phase

Install Pillow:

```bash
python3 -m pip install Pillow
```

`scripts/compose.py` requires a readable bold `.ttf` or `.otf` font for the headline. The scripts now prefer bundled fonts from `.fonts/` or `fonts/` inside the skill directory, with the repo defaulting to bundled Arial and DejaVu variants before falling back to common macOS and Linux system font paths.

If you want to force a specific font, set:

```bash
export ASO_HEADLINE_FONT="/absolute/path/to/ASO-App-Store-Screenshots-for-Codex/fonts/Arial Bold.ttf"
```

## How To Use In Codex

Run Codex inside your iOS app project and invoke the skill explicitly:

```text
Use $aso-appstore-screenshots to create App Store screenshots for this iOS app.
```

Common prompts:

- `Use $aso-appstore-screenshots to analyze this app and propose screenshot benefits.`
- `Use $aso-appstore-screenshots to review screenshots in ./simulator-screenshots.`
- `Use $aso-appstore-screenshots to generate scaffold screenshots for the confirmed benefits.`
- `Use $aso-appstore-screenshots to resume from screenshots/aso-state.md.`

## Recommended Project Layout

Keep raw captures separate from generated assets:

```text
your-app/
  simulator-screenshots/
    home.png
    search.png
    detail.png
  screenshots/
```

- Put raw simulator captures in `simulator-screenshots/`.
- Let the skill create and manage `screenshots/`.

## Workflow

1. Benefit discovery from the app codebase.
2. Screenshot review and rating.
3. Benefit-to-screenshot pairing.
4. Brand color selection.
5. Scaffold generation.
6. Optional AI enhancement.
7. Crop, resize, and final export.

Progress is saved in:

```text
screenshots/aso-state.md
```

## Script Usage

Set the skill directory once:

```bash
SKILL_DIR="$HOME/.codex/skills/aso-appstore-screenshots"
```

Generate or refresh the reusable device frame:

```bash
python3 "$SKILL_DIR/scripts/generate_frame.py"
```

Generate a deterministic screenshot scaffold:

```bash
python3 "$SKILL_DIR/scripts/compose.py" \
  --bg "#E31837" \
  --verb "TRACK" \
  --desc "TRADING CARD PRICES" \
  --screenshot simulator-screenshots/home.png \
  --output screenshots/01-track-card-prices/scaffold.png
```

Generate a showcase image from approved finals:

```bash
python3 "$SKILL_DIR/scripts/showcase.py" \
  --screenshots \
    screenshots/final/01-track-card-prices.jpg \
    screenshots/final/02-search-any-card.jpg \
    screenshots/final/03-build-your-collection.jpg \
  --output screenshots/showcase.png
```

You can also add a footer link to the showcase:

```bash
python3 "$SKILL_DIR/scripts/showcase.py" \
  --screenshots screenshots/final/01-track-card-prices.jpg screenshots/final/02-search-any-card.jpg \
  --output screenshots/showcase.png \
  --github "https://github.com/your-org/your-app"
```

## Export Sizes

Default output size:

- `1290 x 2796` for the iPhone 6.7-inch App Store slot

Supported portrait targets:

- `1242 x 2688` for iPhone 6.5-inch
- `1290 x 2796` for iPhone 6.7-inch
- `1320 x 2868` for iPhone 6.9-inch

## Output Layout

```text
screenshots/
  aso-state.md
  01-track-card-prices/
    scaffold.png
    v1.jpg
    v1-resized.jpg
    v2.jpg
    v2-resized.jpg
    v3.jpg
    v3-resized.jpg
  02-search-any-card/
  final/
    01-track-card-prices.jpg
    02-search-any-card.jpg
  showcase.png
```

Treat `screenshots/final/` as the upload-ready output folder.

## Notes

- Raw AI outputs should always be cropped and resized before final review.
- If no image tool is available, the skill still handles analysis, pairing, and scaffold generation.
- `scripts/compose.py` is the source of truth for headline layout, device placement, and screenshot positioning.
