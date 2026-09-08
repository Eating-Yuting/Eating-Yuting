"""
Schotter Ice — after Georg Nees, 1968.

The original falling grid, frozen into a slab of ice: pale blue field,
deep blue lines, and a gentler collapse so the cracks stay crisp.
Writes ice.svg. sketch.py and heart.py are untouched.

Run it:
    python3 ice.py
"""

import math
import random

# ---------------------------------------------------------------------------
# The knobs.
# ---------------------------------------------------------------------------

COLS = 14            # squares across
ROWS = 8            # squares down
SEED = 273           # 273 K = 0 °C — freezing point 🧊
CHAOS = 0.6          # gentler than the original, like cracks, not rubble
SQUARE = 40          # size of one square, in svg units
MARGIN = 60          # breathing room around the grid
STROKE = "#5aa9e6"   # deep ice blue
BACKGROUND = "#eef6ff"  # pale frozen field
STROKE_WIDTH = 0.7

OUTPUT = "ice.svg"

# ---------------------------------------------------------------------------
# The drawing.
# ---------------------------------------------------------------------------


def square(x, y, size, angle_deg, dx, dy):
    """One square, rotated about its own centre and nudged off its grid slot."""
    cx, cy = x + size / 2, y + size / 2
    return (
        f'  <rect x="{x:.2f}" y="{y:.2f}" width="{size}" height="{size}" '
        f'transform="translate({dx:.2f} {dy:.2f}) '
        f'rotate({angle_deg:.2f} {cx:.2f} {cy:.2f})" />'
    )


def draw():
    rng = random.Random(SEED)
    parts = []

    for row in range(ROWS):
        # Disorder grows with depth — but ice stays mostly in place.
        damage = CHAOS * (row / ROWS) ** 2

        for col in range(COLS):
            x = MARGIN + col * SQUARE
            y = MARGIN + row * SQUARE
            angle = rng.uniform(-1, 1) * damage * 45
            dx = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            dy = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            parts.append(square(x, y, SQUARE, angle, dx, dy))

    width = COLS * SQUARE + MARGIN * 2
    height = ROWS * SQUARE + MARGIN * 2

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">',
            f'  <rect width="100%" height="100%" fill="{BACKGROUND}" />',
            f'  <g fill="none" stroke="{STROKE}" stroke-width="{STROKE_WIDTH}">',
            *parts,
            "  </g>",
            "</svg>",
        ]
    )


if __name__ == "__main__":
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(draw())
    print(f"wrote {OUTPUT} — {COLS}x{ROWS} ice squares, seed {SEED}, chaos {CHAOS}")
    print("open it in a browser, then change a number and run me again")
