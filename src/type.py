"""Text to SVG outlines: HarfBuzz shaping on the real variable fonts, glyphs as paths.

GitHub serves README SVGs inside <img>, where web fonts are unreliable, so every
word is drawn as vector outlines instead of <text>.
"""
import io
from functools import lru_cache
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

FONTS = Path(__file__).parent / "inputs" / "fonts"


@lru_cache(None)
def _face(name):
    files = {"sans": ["mona-sans-latin.woff2", "mona-sans-latin-ext.woff2"], "mono": ["jetbrains-mono-latin.woff2"]}[name]
    faces = []
    for f in files:
        t = TTFont(FONTS / f)
        t.flavor = None
        b = io.BytesIO()
        t.save(b)
        faces.append((hb.Face(b.getvalue()), t["head"].unitsPerEm, t.getBestCmap()))
    return faces


class _Pen(BasePen):
    def __init__(self, sx, sy, ox, oy):
        super().__init__(None)
        self.d = []
        self.sx, self.sy, self.ox, self.oy = sx, sy, ox, oy

    def _p(self, p):
        return f"{self.ox + p[0] * self.sx:.1f} {self.oy - p[1] * self.sy:.1f}"

    def _moveTo(self, p):
        self.d.append("M" + self._p(p))

    def _lineTo(self, p):
        self.d.append("L" + self._p(p))

    def _curveToOne(self, a, b, c):
        self.d.append("C" + " ".join(self._p(q) for q in (a, b, c)))

    def _qCurveToOne(self, a, b):
        self.d.append("Q" + self._p(a) + " " + self._p(b))

    def _closePath(self):
        self.d.append("Z")


STYLES = {
    # name: (font, wght, wdth, tracking em)
    "name": ("sans", 840, 120, -0.048),
    "mega": ("sans", 870, 125, -0.05),
    "h2": ("sans", 830, 120, -0.045),
    "row": ("sans", 840, 122, -0.05),
    "title": ("sans", 720, 112, -0.02),
    "head": ("sans", 780, 115, -0.03),
    "body": ("sans", 430, 100, 0.0),
    "bodyb": ("sans", 640, 104, 0.0),
    "label": ("sans", 650, 108, 0.0),
    "orb": ("sans", 760, 112, -0.01),
    "band": ("sans", 860, 122, -0.035),
    "step": ("sans", 820, 118, -0.04),
    "contact": ("sans", 860, 122, -0.055),
    "mono": ("mono", 500, None, 0.0),
    "monob": ("mono", 650, None, 0.04),
}


def _font(style, face_idx=0):
    name, wght, wdth, _ = STYLES[style]
    face, upem, _ = _face(name)[face_idx]
    f = hb.Font(face)
    v = {"wght": wght}
    if wdth:
        v["wdth"] = wdth
    f.set_variations(v)
    return f, upem


def _runs(text, style):
    """Split text into runs by which font file covers each character."""
    faces = _face(STYLES[style][0])
    runs, cur, idx = [], "", None
    for ch in text:
        i = next((k for k, (_, _, cmap) in enumerate(faces) if ord(ch) in cmap), 0)
        if idx is None or i == idx:
            cur += ch
        else:
            runs.append((cur, idx))
            cur = ch
        idx = i
    if cur:
        runs.append((cur, idx or 0))
    return runs


def shape(text, style, size, tracking=None):
    """Return [(font, gid, x_offset_px, y_offset_px)] and the total advance in px."""
    track = STYLES[style][3] if tracking is None else tracking
    out, x = [], 0.0
    for run, idx in _runs(text, style):
        f, upem = _font(style, idx)
        buf = hb.Buffer()
        buf.add_str(run)
        buf.guess_segment_properties()
        hb.shape(f, buf, {"kern": True, "liga": True})
        k = size / upem
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((f, info.codepoint, x + pos.x_offset * k, -pos.y_offset * k, k))
            x += pos.x_advance * k + track * size
    return out, x - track * size


def width(text, style, size, tracking=None):
    return shape(text, style, size, tracking)[1]


def path(text, style, size, x=0, y=0, anchor="start", tracking=None):
    """SVG path data for text whose baseline starts at (x, y)."""
    glyphs, w = shape(text, style, size, tracking)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    d = []
    for f, gid, gx, gy, k in glyphs:
        pen = _Pen(k, k, x + gx, y + gy)
        f.draw_glyph_with_pen(gid, pen)
        d.extend(pen.d)
    return "".join(d)


def glyph_paths(text, style, size, x=0, y=0, tracking=None):
    """One path per glyph (for per-letter effects): [(char, d, x_left, advance)]."""
    glyphs, _ = shape(text, style, size, tracking)
    res = []
    chars = list(text)
    for i, (f, gid, gx, gy, k) in enumerate(glyphs):
        pen = _Pen(k, k, x + gx, y + gy)
        f.draw_glyph_with_pen(gid, pen)
        nxt = glyphs[i + 1][2] if i + 1 < len(glyphs) else None
        res.append((chars[i] if i < len(chars) else "", "".join(pen.d), x + gx, (nxt - gx) if nxt is not None else None))
    return res


def wrap(text, style, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if cur and width(t, style, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- glyph reuse
# Each document defines every glyph it needs once (at 100 px), and text runs are
# lists of <use> placements. Cuts file size by an order of magnitude.

_DEFS = {}


def begin():
    _DEFS.clear()


def defs():
    return "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in _DEFS.values())


def _glyph_id(style, idx, gid):
    key = (style, idx, gid)
    if key not in _DEFS:
        f, upem = _font(style, idx)
        k = 100 / upem
        pen = _Pen(k, k, 0, 0)
        f.draw_glyph_with_pen(gid, pen)
        _DEFS[key] = (f"g{len(_DEFS)}", "".join(pen.d))
    return _DEFS[key][0] if _DEFS[key][1] else None


def run(text, style, size, x=0, y=0, anchor="start", tracking=None):
    """<use> placements for text whose baseline starts at (x, y)."""
    track = STYLES[style][3] if tracking is None else tracking
    total = width(text, style, size, tracking)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total
    out, cx = [], x
    s = size / 100
    for part, idx in _runs(text, style):
        f, upem = _font(style, idx)
        buf = hb.Buffer()
        buf.add_str(part)
        buf.guess_segment_properties()
        hb.shape(f, buf, {"kern": True, "liga": True})
        k = size / upem
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            gid = _glyph_id(style, idx, info.codepoint)
            if gid:
                out.append(f'<use href="#{gid}" transform="translate({cx + pos.x_offset * k:.1f} {y - pos.y_offset * k:.1f}) scale({s:.3f})"/>')
            cx += pos.x_advance * k + track * size
    return "".join(out)
