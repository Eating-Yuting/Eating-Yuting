"""
Schotter Heart — after Georg Nees, 1968.

Same falling-apart squares, but only drawn where a heart shape should be.
Writes heart.svg next to this file. sketch.py and sketch.svg stay untouched.

Run it:
    python3 heart.py
"""

import math
import random

# ---------------------------------------------------------------------------
# The knobs. These are yours. Change them, run again, look, commit.
# ---------------------------------------------------------------------------

COLS = 21            # squares across
ROWS = 19            # squares down
SEED = 520           # 520 = 我爱你。Same seed = same image, every time, forever.
CHAOS = 0.9          # how fast the heart falls apart. 0 = perfect heart.
SQUARE = 22          # size of one square, in svg units
MARGIN = 50          # breathing room around the grid
STROKE = "#ff6b9d"   # line colour (sakura pink)
BACKGROUND = "#fff0f5"  # background (blush)
STROKE_WIDTH = 1.3

OUTPUT = "heart.svg"

# ---------------------------------------------------------------------------
# The heart curve. Returns True if a grid cell lives inside the heart.
# ---------------------------------------------------------------------------


def inside_heart(px, py):
    """px/py are the cell's position, as fractions from 0 to 1."""
    # Convert to the coordinate space the heart formula expects (-1.3 ~ 1.3).
    x = (px - 0.5) * 2.6
    y = (0.5 - py) * 2.6   # flip, because svg y grows downwards
    # Classic heart equation: (x^2 + y^2 - 1)^3 - x^2 * y^3 <= 0
    return (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0


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
        # Disorder grows with depth — the top of the heart stays calm.
        damage = CHAOS * (row / ROWS) ** 2

        for col in range(COLS):
            # Skip this cell unless it is inside the heart.
            px = (col + 0.5) / COLS
            py = (row + 0.5) / ROWS
            if not inside_heart(px, py):
                continue

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
    print(f"wrote {OUTPUT} — a pink heart, {COLS}x{ROWS} cells, seed {SEED}, chaos {CHAOS}")
    print("open it in a browser, then change a number and run me again")
