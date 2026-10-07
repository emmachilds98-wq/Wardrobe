#!/usr/bin/env python3
"""A contact sheet of shop photos beside what the page read from them, to judge a photo-reader change on every item
of a kind at once (one item looking right is not proof).

    node tools/qa/dump.js /tmp/look.json                       # every piece's reading, from the page being served
    python3 tools/qa/sheet.py /tmp/look.json trainers out.png  # up to 30 photos of that shape, with swatches
    python3 tools/qa/sheet.py /tmp/look.json trainers out.png 30   # the next 30

Each cell is the photo from docs/data/photos, then swatches: up (c1, the main colour), sole and acc (footwear) and c2.
An empty space means nothing was read."""
import base64
import glob
import io
import json
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def photos():
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "docs", "data", "photos", "*.json"))):
        for k, v in json.load(open(f)).items():
            if k not in out:
                out[k] = v[0] if isinstance(v, list) else v
    return out


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    look, shape, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    keys = sorted(k for k in look if k.endswith("|" + shape))[start:start + 30]
    if not keys:
        sys.exit("no %s pieces in %s" % (shape, sys.argv[1]))
    ph, cw, ch, cols = photos(), 200, 190, 6
    sheet = Image.new("RGB", (cw * cols, ch * ((len(keys) + cols - 1) // cols)), "white")
    d = ImageDraw.Draw(sheet)
    for i, k in enumerate(keys):
        item, x, y = k.split("|")[0], (i % cols) * cw, (i // cols) * ch
        if item in ph and "," in ph[item]:
            im = Image.open(io.BytesIO(base64.b64decode(ph[item].split(",", 1)[1]))).convert("RGB")
            im.thumbnail((cw - 4, 140))
            sheet.paste(im, (x + 2, y + 2))
        L = look[k] or {}
        for j, (label, col) in enumerate((("up", L.get("c1")), ("sole", L.get("sole")), ("acc", L.get("acc")), ("c2", L.get("c2")))):
            if col:
                d.rectangle((x + 2 + j * 49, y + 146, x + 48 + j * 49, y + 172), fill=col, outline="#888")
            d.text((x + 4 + j * 49, y + 174), label, fill="black")
        d.text((x + 4, y + 2), "%d %s" % (start + i, item[:28]), fill="red")
    sheet.save(out)
    print("%d %s pieces -> %s" % (len(keys), shape, out))


if __name__ == "__main__":
    main()
