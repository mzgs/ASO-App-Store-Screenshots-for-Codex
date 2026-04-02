---
name: aso-appstore-screenshots
description: Create high-converting iOS App Store screenshot sets by analyzing an app codebase, extracting 3-5 conversion-focused benefit headlines, reviewing and pairing simulator screenshots, composing deterministic screenshot scaffolds, and guiding AI enhancement plus App Store resizing. Use when Codex needs to turn an iOS app project and simulator captures into ASO screenshot assets or resume/edit an existing screenshot set.
---

# ASO App Store Screenshots

## Overview

Turn an iOS app project into an App Store-ready screenshot set with a repeatable workflow:

1. Discover the 3-5 core benefits that should drive installs.
2. Review simulator screenshots and pair each confirmed benefit with the best screen.
3. Generate deterministic scaffolds, enhance them with an available image tool, resize them to Apple's exact dimensions, and finalize the approved set.

Use the bundled scripts:

- `scripts/compose.py` builds the deterministic scaffold.
- `scripts/generate_frame.py` regenerates `assets/device_frame.png` if needed.
- `scripts/showcase.py` renders a side-by-side preview image after the set is approved.

Expect two local prerequisites for the Python scripts:

- `Pillow` must be installed in the Python environment used to run the scripts.
- A bold `.ttf` or `.otf` headline font must be readable. `scripts/compose.py` first checks bundled fonts in `.fonts/` or `fonts/`, then common macOS and Linux paths, and also accepts `--font` or `ASO_HEADLINE_FONT`.

## Resume State First

Start every run by checking for `screenshots/aso-state.md` in the user's app project.

- If it exists, summarize what is already confirmed: benefits, screenshot ratings, pairings, brand color, target size, and generated outputs.
- Let the user resume, jump back to a phase, or change a single item without redoing everything else.
- If it does not exist, start at benefit discovery.

Keep the state file short and practical. Update it after each confirmed phase. Include:

- App name and bundle or package identifier if available.
- Confirmed benefits in order.
- Screenshot analysis with file paths and ratings.
- Confirmed benefit-to-screenshot pairings.
- Brand color choice and target App Store size.
- Generated folders, approved variants, and final output paths.

## Discover Benefits

Analyze the codebase before asking questions.

- Inspect UI screens, views, features, onboarding, monetization, models, README files, metadata, and any existing App Store copy.
- Infer what the app does, who it is for, what problem it solves, and why it is different.
- Ask only the follow-up questions the code cannot answer.

Draft 3-5 benefit headlines that are specific and conversion-oriented.

- Lead with a strong action verb: `TRACK`, `SEARCH`, `BUILD`, `SAVE`, `LEARN`, `FIND`, `BOOST`.
- Focus on the user outcome, not the technical implementation.
- Prefer concrete wording over generic phrasing.

Do not proceed until the user explicitly confirms the benefit list and order. Then write the confirmed result into `screenshots/aso-state.md`.

## Review Screenshots And Pair Them

Ask the user for simulator screenshot paths, a directory, or a glob. Open every candidate image with the harness image viewer.

For each screenshot:

- Explain what it shows.
- Rate it `Great`, `Usable`, or `Retake`.
- Call out specific problems such as empty states, placeholder data, cluttered status bars, thin content, or a poor thumbnail read.

If a screenshot needs to be retaken, give exact capture guidance:

- Which screen to open.
- What data state should be visible.
- Which light or dark mode to keep consistent across the set.
- How to clean the status bar.

Then recommend one unique screenshot per confirmed benefit whenever possible. Prefer relevance, clarity at thumbnail size, and visual energy. Pause until the user confirms the pairings, then persist the analysis and pairings in `screenshots/aso-state.md`.

## Generate The Set

Default to `1290 x 2796` for the iPhone 6.7-inch App Store slot unless the user asks for a different Apple slot.

Accepted portrait sizes:

- `1242 x 2688` for iPhone 6.5-inch
- `1290 x 2796` for iPhone 6.7-inch
- `1320 x 2868` for iPhone 6.9-inch

Pick one bold background color automatically from the app's UI, brand palette, and audience. Present the choice briefly and let the user override it. Save the final color in `screenshots/aso-state.md`.

Build deterministic scaffolds first. Assume the installed skill directory is:

```bash
SKILL_DIR="$HOME/.codex/skills/aso-appstore-screenshots"
```

Run `scripts/generate_frame.py` if `assets/device_frame.png` is missing, then compose each scaffold:

```bash
python3 "$SKILL_DIR/scripts/compose.py" \
  --bg "#E31837" \
  --verb "TRACK" \
  --desc "TRADING CARD PRICES" \
  --screenshot path/to/simulator.png \
  --output screenshots/01-track-card-prices/scaffold.png
```

The scaffold is the source of truth for text layout, device placement, and which in-app screen is shown.

## Enhance With An Image Tool

Only perform AI enhancement if the environment actually has an image generation or image editing tool available. Do not pretend the tool exists.

- If no image tool is available, still generate the scaffolds and stop with precise next-step instructions.
- If an image tool is available, generate 3 variants for each scaffold.
- Treat the first approved screenshot as the style template for the rest of the set so rendering, polish, and breakout elements stay consistent.

Keep the enhancement prompt constrained:

- Preserve the exact headline text, hierarchy, and centered placement from the scaffold.
- Preserve the exact device position and on-screen app screenshot from the scaffold.
- Keep the background a solid brand color with no extra text.
- Add depth, polish, and optional breakout elements only when they are clearly supported by the screen content.

When iterating on a later screenshot, use:

1. The current scaffold for layout.
2. The first approved screenshot as the style template.
3. The user's preferred version for that specific screenshot as the creative anchor.

## Crop, Review, And Finalize

Never show raw AI output as the final deliverable. Crop and resize every candidate to Apple's exact dimensions first.

Use one shell command to process all variants for the current benefit:

```bash
TARGET_W=1290 && TARGET_H=2796 && \
for INPUT in screenshots/01-track-card-prices/v1.jpg screenshots/01-track-card-prices/v2.jpg screenshots/01-track-card-prices/v3.jpg; do
  OUTPUT="${INPUT%.jpg}-resized.jpg"
  cp "$INPUT" "$OUTPUT"
  W=$(sips -g pixelWidth "$OUTPUT" | tail -1 | awk '{print $2}')
  H=$(sips -g pixelHeight "$OUTPUT" | tail -1 | awk '{print $2}')
  CROP_W=$(python3 -c "print(round($H * $TARGET_W / $TARGET_H))")
  OFFSET_X=$(python3 -c "print(round(($W - $CROP_W) / 2))")
  sips --cropOffset 0 $OFFSET_X --cropToHeightWidth $H $CROP_W "$OUTPUT" >/dev/null
  sips -z $TARGET_H $TARGET_W "$OUTPUT" >/dev/null
done
```

Review only the resized variants with the user. Once the user picks a winner, copy it into `screenshots/final/NN-benefit-slug.jpg`.

After the whole set is approved, optionally create a showcase image:

```bash
python3 "$SKILL_DIR/scripts/showcase.py" \
  --screenshots screenshots/final/01-track-card-prices.jpg screenshots/final/02-search-any-card.jpg screenshots/final/03-build-your-collection.jpg \
  --output screenshots/showcase.png
```

## Output Layout

Keep outputs in the user's project root:

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

Treat `screenshots/final/` as the upload-ready deliverable folder. Report which Apple display slot the exported files match.
