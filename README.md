# ASO App Store Screenshots for Codex

Codex skill for turning an iOS app project plus simulator captures into an App Store screenshot set.

## What It Does

- Analyzes the app codebase to identify 3-5 conversion-focused screenshot benefits.
- Reviews simulator screenshots and rates them.
- Pairs each confirmed benefit with the best screenshot.
- Generates deterministic scaffold images for App Store screenshots.
- Supports an optional AI-enhancement phase if an image tool is available.
- Organizes outputs into a resumable `screenshots/` workflow.

## Install

Copy or symlink the skill into `~/.codex/skills`:

```bash
mkdir -p ~/.codex/skills
cp -R /Users/mustafa/Downloads/ssgen/aso-appstore-screenshots ~/.codex/skills/
```

Or:

```bash
mkdir -p ~/.codex/skills
ln -sfn /Users/mustafa/Downloads/ssgen/aso-appstore-screenshots ~/.codex/skills/aso-appstore-screenshots
```

Restart Codex after installing so it reloads available skills.

## Prerequisites

- Python 3
- `Pillow` for the bundled Python scripts
- A readable bold `.ttf` or `.otf` font for screenshot headlines
- Optional image generation or image editing tool for the enhancement phase

Install Pillow:

```bash
python3 -m pip install Pillow
```

If the default system font lookup does not work, set:

```bash
export ASO_HEADLINE_FONT="/path/to/font-file.otf"
```

## Recommended Project Layout

Keep raw simulator images separate from generated assets:

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

## How To Use

Run Codex inside your iOS app project and invoke the skill explicitly:

```text
Use $aso-appstore-screenshots to create App Store screenshots for this iOS app.
```

Common prompts:

- `Use $aso-appstore-screenshots to analyze this app and propose screenshot benefits.`
- `Use $aso-appstore-screenshots to review screenshots in ./simulator-screenshots.`
- `Use $aso-appstore-screenshots to generate scaffold screenshots for the confirmed benefits.`
- `Use $aso-appstore-screenshots to resume from screenshots/aso-state.md.`

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

Use `screenshots/final/` as the upload-ready output folder.

## Bundled Scripts

- `scripts/compose.py` builds deterministic scaffold images.
- `scripts/generate_frame.py` regenerates the phone frame asset.
- `scripts/showcase.py` creates a side-by-side preview image.

## Notes

- Default export size is `1290 x 2796` for the iPhone 6.7-inch App Store slot.
- Raw AI outputs should always be cropped and resized before final review.
- If no image tool is available, the skill can still handle analysis, pairing, and scaffold generation.
