#!/usr/bin/env python3
"""Render a mock of the in-game controls with the plugin's own textures.

Follows the plugin's rules: a sprite for square action buttons, an empty nine-patch
button + the button's name for everything else, "_active" variants when pressed.
    python3 tools/preview.py classic preview-classic.png
    python3 tools/preview.py new preview-new.png
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plugin", "textures")
SCALE = 3  # device pixels per point (iPhone @3x)
NINE = json.load(open(os.path.join(TEX, "nine.json")))


def tex(name):
    path = os.path.join(TEX, name + ".png")
    return Image.open(path).convert("RGBA") if os.path.exists(path) else None


def nine_slice(name, w, h, n):
    img = tex(name)
    c = NINE[name]
    l, t, r, b = c["l"], c["t"], c["r"], c["b"]
    xs = [0, l, img.width - r, img.width]
    ys = [0, t, img.height - b, img.height]
    dx = [0, l * n, w - r * n, w]
    dy = [0, t * n, h - b * n, h]
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for j in range(3):
        for i in range(3):
            piece = img.crop((xs[i], ys[j], xs[i + 1], ys[j + 1]))
            tw, th = dx[i + 1] - dx[i], dy[j + 1] - dy[j]
            if tw > 0 and th > 0:
                out.alpha_composite(piece.resize((tw, th), Image.NEAREST), (dx[i], dy[j]))
    return out


def button(canvas, style, x, y, w, h, item=None, label="", active=False, empty=None):
    W, H = int(w * SCALE), int(h * SCALE)
    ratio = w / h
    sprite = None
    if item and 0.75 <= ratio <= 1.33:
        sprite = tex(f"{style}/{item}{'_active' if active else ''}") or tex(f"{style}/{item}")
    if sprite:
        skin = sprite.resize((W, H), Image.NEAREST)
    else:
        empty = empty or ("empty_2" if style == "new" else "empty_1")
        name = f"empty/{empty}{'_active' if active else ''}"
        base = tex(f"empty/{empty}")
        n = max(1, round(min(W, H) / base.width))
        skin = nine_slice(name, W, H, n)
        d = ImageDraw.Draw(skin)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(min(W, H) * 0.30))
        except OSError:
            font = ImageFont.load_default()
        bb = d.textbbox((0, 0), label, font=font)
        tx, ty = (W - (bb[2] - bb[0])) // 2 - bb[0], (H - (bb[3] - bb[1])) // 2 - bb[1]
        s = max(1, int(min(W, H) / 18))
        d.text((tx + s, ty + s), label, font=font, fill=(63, 63, 63, 255))
        d.text((tx, ty), label, font=font, fill=(255, 255, 255, 255))
    canvas.alpha_composite(skin, (int(x * SCALE), int(y * SCALE)))


def joystick(canvas, style, x, y, size):
    S = int(size * SCALE)
    canvas.alpha_composite(tex(f"{style}/joystick_pad").resize((S, S), Image.NEAREST), (int(x * SCALE), int(y * SCALE)))
    t = S // 4
    canvas.alpha_composite(tex(f"{style}/joystick_stick").resize((t, t), Image.NEAREST),
                           (int(x * SCALE) + (S - t) // 2, int(y * SCALE) + (S - t) // 2))


def main(style, out):
    W, H = 844, 390
    bg = Image.new("RGBA", (W * SCALE, H * SCALE), (70, 120, 60, 255))
    ImageDraw.Draw(bg).rectangle([0, 0, W * SCALE, int(H * SCALE * 0.45)], fill=(120, 170, 230, 255))
    m, b = 8, 52
    st = style
    # top row: the default layout's wide buttons -> empty button + name
    button(bg, st, m, m, 64, 36, item="debug_screen", label="Debug")
    button(bg, st, m + 72, m, 64, 36, item="chat", label="Chat")
    button(bg, st, m + 144, m, 76, 36, label="Keyboard")
    button(bg, st, W - 72, m, 64, 36, label="Mouse")
    button(bg, st, W // 2 - 20, m, 40, 40, item="pause")
    # D-pad
    x0, y0 = 20, H - 3 * b - 3 * m
    button(bg, st, x0 + b + m, y0, b, b, item="up")
    button(bg, st, x0, y0 + b + m, b, b, item="left")
    button(bg, st, x0 + 2 * (b + m), y0 + b + m, b, b, item="right", active=True)
    button(bg, st, x0 + b + m, y0 + 2 * (b + m), b, b, item="down")
    # right side
    button(bg, st, W - 2 * b - 3 * m - 20, H - 2 * b - 3 * m, b, b, item="sneak")
    button(bg, st, W - b - m - 20, H - b - m - 70, b + 8, b + 8, item="jump")
    button(bg, st, W - 2 * b - 3 * m - 20, H - 3 * b - 4 * m, b, b, item="attack")
    button(bg, st, W - b - 2 * m - 20, H - 3 * b - 4 * m - 8, b, b, item="use")
    button(bg, st, W // 2 + 80, H - b - m + 4, b, b, item="inventory")
    button(bg, st, W // 2 - 20, H - b - m + 12, 84, 40, label="Opti-Zoom")
    button(bg, st, W // 2 + 80, H - b - m - 36, 48, 48, item="player_list")
    button(bg, st, W // 2 - 20, H - b - m - 36, 84, 40, label="Tab", active=True)
    joystick(bg, st, 215, H - 140, 110)
    bg.convert("RGB").save(out)
    print("saved", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "classic", sys.argv[2] if len(sys.argv) > 2 else "preview.png")
