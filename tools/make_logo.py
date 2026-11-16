"""Build the OpenSprint wordmark from Inter's real outlines.

"Open" sits on the top baseline, "Sprint" is stepped down, and the right leg
of the "n" is extended down to Sprint's baseline (the bottom of the S).
Usage: python make_logo.py <inter.woff2> <out_dir> [weight] [drop_ratio]
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

src, out = sys.argv[1], sys.argv[2]
weight = float(sys.argv[3]) if len(sys.argv) > 3 else 800
drop_ratio = float(sys.argv[4]) if len(sys.argv) > 4 else 0.82

font = TTFont(src)
font = instancer.instantiateVariableFont(font, {"wght": weight})
gs = font.getGlyphSet()
cmap = font.getBestCmap()
hmtx = font["hmtx"]
upm = font["head"].unitsPerEm
cap = font["OS/2"].sCapHeight
track = -0.035 * upm            # tight letter-spacing, like the site headings


def bounds(ch):
    bp = BoundsPen(gs); gs[cmap[ord(ch)]].draw(bp); return bp.bounds


def draw(pen_out, ch, x, y):
    # font units are y-up; SVG is y-down, so flip around the baseline y
    tp = TransformPen(pen_out, (1, 0, 0, -1, x, y))
    gs[cmap[ord(ch)]].draw(tp)
    return hmtx[cmap[ord(ch)]][0] + track


drop = round(cap * drop_ratio)
pen = SVGPathPen(gs)
x = 0.0
base_top = cap + 40              # top baseline, leaving room above the caps
for ch in "Ope":
    x += draw(pen, ch, x, base_top)

# the "n": find its right stem from the outline so the extension lines up exactly
nx0, ny0, nx1, ny1 = bounds("n")
lx0, _, lx1, _ = bounds("l")     # an "l" is a single stem: use its width
stem = lx1 - lx0
n_x = x
x += draw(pen, "n", n_x, base_top)
right = n_x + nx1
left = right - stem
# extend the leg: from a little above the n's baseline down to Sprint's baseline
leg_top = base_top - 20
leg_bottom = base_top + drop
pen.moveTo((left, leg_top)); pen.lineTo((right, leg_top)); pen.lineTo((right, leg_bottom)); pen.lineTo((left, leg_bottom)); pen.closePath()

# "Sprint" starts just after the leg, a small gap like normal letter spacing
sx0 = bounds("S")[0]
x = right + 0.08 * upm - sx0
for ch in "Sprint":
    x += draw(pen, ch, x, base_top + drop)

path = pen.getCommands()

# tight viewBox from the actual outline extents
from fontTools.pens.recordingPen import RecordingPen
# compute bounds by re-drawing through a BoundsPen with the same transforms
bp = BoundsPen(gs)
def draw_b(ch, x, y):
    tp = TransformPen(bp, (1, 0, 0, -1, x, y)); gs[cmap[ord(ch)]].draw(tp); return hmtx[cmap[ord(ch)]][0] + track
x = 0.0
for ch in "Ope": x += draw_b(ch, x, base_top)
draw_b("n", n_x, base_top)
bp.moveTo((left, leg_top)); bp.lineTo((right, leg_bottom)); bp.closePath()
x = right + 0.08 * upm - sx0
for ch in "Sprint": x += draw_b(ch, x, base_top + drop)
bx0, by0, bx1, by1 = bp.bounds
pad = 4
vb = f"{bx0 - pad:.0f} {by0 - pad:.0f} {bx1 - bx0 + 2 * pad:.0f} {by1 - by0 + 2 * pad:.0f}"
w, h = bx1 - bx0 + 2 * pad, by1 - by0 + 2 * pad


def svg(fill, title=True):
    t = "<title>OpenSprint</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="OpenSprint">{t}'
            f'<path fill="{fill}" d="{path}"/></svg>\n')


import os
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "logo.svg"), "w", encoding="utf-8", newline="\n").write(svg("#0a0a0a"))
open(os.path.join(out, "logo-white.svg"), "w", encoding="utf-8", newline="\n").write(svg("#ffffff"))

# Favicon: just the junction, the extended "n" with the "S" stepped down beside it
fpen = SVGPathPen(gs)
fb = BoundsPen(gs)
for p in (fpen, fb):
    draw_n = TransformPen(p, (1, 0, 0, -1, 0, base_top)); gs[cmap[ord("n")]].draw(draw_n)
    p.moveTo((nx1 - stem, leg_top)); p.lineTo((nx1, leg_top)); p.lineTo((nx1, leg_bottom)); p.lineTo((nx1 - stem, leg_bottom)); p.closePath()
    ds = TransformPen(p, (1, 0, 0, -1, nx1 + 0.08 * upm - sx0, base_top + drop)); gs[cmap[ord("S")]].draw(ds)
fx0, fy0, fx1, fy1 = fb.bounds
side = max(fx1 - fx0, fy1 - fy0) * 1.36
cx, cy = (fx0 + fx1) / 2, (fy0 + fy1) / 2
fvb = f"{cx - side / 2:.0f} {cy - side / 2:.0f} {side:.0f} {side:.0f}"
open(os.path.join(out, "favicon.svg"), "w", encoding="utf-8", newline="\n").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fvb}">'
    f'<rect x="{cx - side / 2:.0f}" y="{cy - side / 2:.0f}" width="{side:.0f}" height="{side:.0f}" rx="{side * .22:.0f}" fill="#1b1e23"/>'
    f'<path fill="#ffffff" d="{fpen.getCommands()}"/></svg>\n')

print(f"aspect {w / h:.3f}  size {w:.0f}x{h:.0f}  bytes {len(path)}")
