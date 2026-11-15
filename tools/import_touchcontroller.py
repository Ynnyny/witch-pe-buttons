#!/usr/bin/env python3
"""Import button textures from a TouchController checkout (LGPL-3.0-or-later).

    git clone --depth 1 https://github.com/fifth-light/TouchController.git
    python3 tools/import_touchcontroller.py ./TouchController

What it does (no pixel is altered):
  * copies the sprites used by the plugin into plugin/textures/<style>/<item>[_active].png
  * converts Android 9-patch buttons (empty/*.9.png) into plain PNGs and records where
    they stretch in plugin/textures/nine.json  ({"empty/empty_1": {"l":..,"t":..,"r":..,"b":..}})
"""
import json
import os
import subprocess
import sys

from PIL import Image

if len(sys.argv) < 2:
    sys.exit(__doc__)
SRC = os.path.abspath(sys.argv[1])
TEX = os.path.join(SRC, "touchcontroller", "resources", "texture")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plugin", "textures")

# plugin item name -> (directory, file stem) inside control/<style>/
ITEMS = {
    "up": ("dpad", "up"), "down": ("dpad", "down"), "left": ("dpad", "left"), "right": ("dpad", "right"),
    "jump": ("jump", "jump"), "sneak": ("sneak", "sneak"), "sprint": ("sprint", "sprint"),
    "inventory": ("inventory", "inventory"), "chat": ("chat", "chat"), "pause": ("pause", "pause"),
    "debug_screen": ("debug_screen", "debug_screen"), "player_list": ("player_list", "player_list"),
    "perspective": ("perspective", "perspective"), "shield": ("shield", "shield"),
    "screenshot": ("screenshot", "screenshot"), "hide_hud": ("hide_hud", "hide_hud"),
    "pickaxe": ("pickaxe", "pickaxe"), "attack": ("attack", "attack"), "use": ("use", "use"),
    "joystick_pad": ("joystick", "pad"), "joystick_stick": ("joystick", "stick"),
}


def copy_png(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    Image.open(src).convert("RGBA").save(dst)


count = 0
for style in ("classic", "new"):
    for item, (folder, stem) in ITEMS.items():
        for suffix in ("", "_active"):
            src = os.path.join(TEX, "control", style, folder, stem + suffix + ".png")
            if os.path.exists(src):
                copy_png(src, os.path.join(OUT, style, item + suffix + ".png"))
                count += 1
print("sprites copied:", count)


def runs(flags):
    """Contiguous True runs -> [(start, end_exclusive)]"""
    result, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            result.append((start, i))
            start = None
    return result


nine = {}
empty_dir = os.path.join(TEX, "empty")
for name in sorted(os.listdir(empty_dir)):
    if not name.endswith(".9.png"):
        continue
    im = Image.open(os.path.join(empty_dir, name)).convert("RGBA")
    w, h = im.size
    px = im.load()
    mark = lambda x, y: px[x, y][3] > 0 and px[x, y][:3] == (0, 0, 0)
    top = runs([mark(x, 0) for x in range(1, w - 1)])      # horizontal stretch (interior coords)
    left = runs([mark(0, y) for y in range(1, h - 1)])     # vertical stretch
    W, H = w - 2, h - 2
    (x0, x1), (y0, y1) = top[0], left[0]
    stem = name[:-6]
    interior = im.crop((1, 1, w - 1, h - 1))
    dst = os.path.join(OUT, "empty", stem + ".png")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    interior.save(dst)
    nine["empty/" + stem] = {"l": x0, "t": y0, "r": W - x1, "b": H - y1}
    print(f"{stem}: {W}x{H} stretch x={top} y={left} -> caps {nine['empty/' + stem]}")

with open(os.path.join(OUT, "nine.json"), "w") as f:
    json.dump(nine, f, indent=1, sort_keys=True)

commit = subprocess.run(["git", "-C", SRC, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("TouchController commit:", commit)
