"""Shared pieces for the profile README panels, in the portfolio's design language."""
import math
import random

import type as T

BG = "#07080b"
INK, INK2, INK3 = "#eceef4", "#bcc0cd", "#8f95a7"
EMBER, ICE, SIGNAL, GREEN = "#ff6b3d", "#6fe3ff", "#8b9cff", "#3ee08f"
LINE, LINE2, LINE3 = "rgba(232,235,245,0.09)", "rgba(232,235,245,0.16)", "rgba(232,235,245,0.3)"
SPARK = "M12 2c.6 4.9 3.1 7.4 8 8-4.9.6-7.4 3.1-8 8-.6-4.9-3.1-7.4-8-8 4.9-.6 7.4-3.1 8-8z"

BASE_CSS = """
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes spinr { to { transform: rotate(-360deg); } }
@keyframes blink { 50% { opacity: 0.2; } }
@keyframes fadein { from { opacity: 0; } to { opacity: 1; } }
@keyframes rise { from { transform: translateY(var(--rise, 120px)); } to { transform: translateY(0); } }
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
@keyframes twinkle { 0%, 100% { opacity: var(--o, 0.6); } 50% { opacity: calc(var(--o, 0.6) * 0.25); } }
.fade { animation: fadein 1.4s cubic-bezier(0.16, 1, 0.3, 1) both; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
"""


def svg(w, h, body, css="", title="", radius=18, border=True, bg=True):
    rr = f'<clipPath id="panel"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>'
    edge = f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{radius - 0.75}" fill="none" stroke="{LINE2}" stroke-width="1.5"/>' if border else ""
    glyphs = T.defs()
    T.begin()
    back = f'<rect width="{w}" height="{h}" fill="{BG}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">'
        f"<title>{title}</title><style>{BASE_CSS}{css}</style><defs>{rr}{glyphs}</defs>"
        f'<g clip-path="url(#panel)">{back}{body}</g>{edge}</svg>'
    )


def glow(cx, cy, r, color, opacity, gid):
    return (
        f'<defs><radialGradient id="{gid}"><stop offset="0" stop-color="{color}" stop-opacity="{opacity}"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>'
    )


def grain(w, h, opacity=0.05, gid="grain"):
    return (
        f'<defs><filter id="{gid}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>'
        f'<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0"/></filter></defs>'
        f'<rect width="{w}" height="{h}" filter="url(#{gid})" opacity="{opacity}"/>'
    )


def stars(w, h, n, seed=1, twinkle=0.3):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([0.6, 0.7, 0.8, 1.0, 1.2])
        o = round(rnd.uniform(0.15, 0.6), 2)
        tw = rnd.random() < twinkle
        style = f' style="--o:{o};animation:twinkle {rnd.uniform(2.5, 6):.1f}s ease-in-out {rnd.uniform(0, 4):.1f}s infinite"' if tw else ""
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#dfe6ff" opacity="{o}"{style}/>')
    return "".join(out)


def galaxy(cx, cy, rx, ry, tilt=-14, n=760, seed=7, rings=((0.64, 0.028, 0.42), (0.93, 0.034, 0.44)), speed=1.0):
    """The portfolio's swirl: dense elliptical rings with brighter arcs, a little scatter."""
    rnd = random.Random(seed)
    palette = [(ICE, 0.5), ("#e6ecff", 0.3), (SIGNAL, 0.12), (EMBER, 0.08)]
    layers = {0: [], 1: [], 2: []}
    for i in range(n):
        u = rnd.random()
        acc = 0
        rad = None
        for r0, sd, share in rings:
            acc += share
            if u < acc:
                rad = rnd.gauss(r0, sd)
                break
        if rad is None:
            rad = rnd.uniform(0.35, 1.15)
        ang = rnd.uniform(0, 2 * math.pi)
        arc = 0.5 + 0.5 * math.cos(2 * ang + rad * 3)  # brighter arcs on opposite sides
        if rnd.random() > 0.35 + 0.65 * arc:
            continue
        c = rnd.choices([p[0] for p in palette], [p[1] for p in palette])[0]
        r = rnd.choice([0.6, 0.75, 0.9, 1.05, 1.25, 1.5]) * (1.2 if c == EMBER else 1)
        o = round(min(1, rnd.uniform(0.3, 0.75) + 0.35 * arc), 2)
        layers[i % 3].append((c, round(o * 4) / 4, f'<circle cx="{math.cos(ang) * rad * rx:.0f}" cy="{math.sin(ang) * rad * rx:.0f}" r="{r}"/>'))
    squash = ry / rx
    g = []
    for k_, dots in layers.items():
        dur = [80, 120, 170][k_] / speed
        buckets = {}
        for c, o, el in dots:
            buckets.setdefault((c, o), []).append(el)
        inner = "".join(f'<g fill="{c}" opacity="{o}">{"".join(els)}</g>' for (c, o), els in buckets.items())
        g.append(f'<g style="animation:{"spinr" if k_ == 1 else "spin"} {dur:.0f}s linear infinite;transform-origin:0 0">{inner}</g>')
    return f'<g transform="translate({cx} {cy}) rotate({tilt}) scale(1 {squash:.3f})">{"".join(g)}</g>'


def label(text, x, y, color=INK2, size=18, square=EMBER):
    sq = f'<rect x="{x}" y="{y - size * 0.62}" width="{size * 0.4:.1f}" height="{size * 0.4:.1f}" fill="{square}"/>'
    return sq + f'<g fill="{color}">{T.run(text, "label", size, x + size * 0.95, y)}</g>'


def mono(text, x, y, size=14, color=INK3, anchor="start", tracking=None, style="mono"):
    return f'<g fill="{color}">{T.run(text, style, size, x, y, anchor, tracking)}</g>'


def text(text_, style, size, x, y, color=INK, anchor="start", extra=""):
    return f'<g fill="{color}"{extra}>{T.run(text_, style, size, x, y, anchor)}</g>'


def para(text_, style, size, x, y, max_w, lh, color=INK2, anchor="start"):
    lines = T.wrap(text_, style, size, max_w)
    return f'<g fill="{color}">' + "".join(T.run(l, style, size, x, y + i * lh, anchor) for i, l in enumerate(lines)) + "</g>", len(lines)


def spark(x, y, size, color=EMBER, spin=0):
    s = size / 24
    anim = f' style="animation:spin {spin}s linear infinite;transform-origin:{x}px {y}px"' if spin else ""
    return f'<g{anim}><path d="{SPARK}" transform="translate({x - size / 2:.1f} {y - size / 2 - 2 * s:.1f}) scale({s:.3f})" fill="{color}"/></g>'


def arrow_ur(x, y, size, color=INK):
    s = size / 24
    return f'<path d="M7 17 17 7M9 7h8v8" transform="translate({x:.1f} {y - size:.1f}) scale({s:.3f})" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'


def grim(x, y, scale=1.0, gid="g", happy=False):
    """Grim, the site mascot, with its float, blink and phone ping."""
    eyes = (
        '<g filter="url(#{g}-glow)"><path d="M43.5 57 Q49 48.5 54.5 57" fill="none" stroke="#dcfbff" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M65.5 57 Q71 48.5 76.5 57" fill="none" stroke="#dcfbff" stroke-width="3" stroke-linecap="round"/></g>'
        if happy
        else '<g filter="url(#{g}-glow)" style="animation:grimblink 5s infinite;transform-origin:60px 54px"><ellipse cx="49" cy="54" rx="4.6" ry="6.4" fill="#dcfbff"/><ellipse cx="71" cy="54" rx="4.6" ry="6.4" fill="#dcfbff"/></g>'
    ).replace("{g}", gid)
    return f"""<g transform="translate({x} {y}) scale({scale})">
<defs><linearGradient id="{gid}-cloak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b3250"/><stop offset="0.55" stop-color="#161a28"/><stop offset="1" stop-color="#0d1019"/></linearGradient>
<radialGradient id="{gid}-screen" cx="0.5" cy="0.4" r="0.7"><stop offset="0" stop-color="#d6f8ff"/><stop offset="1" stop-color="#4fc3ec"/></radialGradient>
<radialGradient id="{gid}-light" cx="0.5" cy="1" r="0.9"><stop offset="0" stop-color="#6fe3ff" stop-opacity="0.45"/><stop offset="1" stop-color="#6fe3ff" stop-opacity="0"/></radialGradient>
<filter id="{gid}-glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<ellipse cx="60" cy="127" rx="24" ry="4" fill="rgba(0,0,0,0.5)"/>
<g style="animation:bob 3.2s ease-in-out infinite">
<path d="M66 4 C84 7 101 25 102 58 L102 104 Q96 115 88.5 106 Q81 96 74.5 106 Q67 116 60 106 Q53 96 45.5 106 Q39 116 31.5 106 Q24 96 18 104 L18 60 C18 31 38 6 66 4 Z" fill="url(#{gid}-cloak)" stroke="rgba(139,156,255,0.4)" stroke-width="1.5"/>
<path d="M66 4 C84 7 101 25 102 58" fill="none" stroke="rgba(200,212,255,0.55)" stroke-width="2" stroke-linecap="round"/>
<ellipse cx="60" cy="55" rx="28" ry="24" fill="#04050a"/><ellipse cx="60" cy="72" rx="26" ry="11" fill="url(#{gid}-light)"/>
{eyes}
<ellipse cx="41" cy="66" rx="4" ry="2.2" fill="{EMBER}" opacity="0.38"/><ellipse cx="79" cy="66" rx="4" ry="2.2" fill="{EMBER}" opacity="0.38"/>
<rect x="47" y="77" width="26" height="33" rx="5" fill="#0a0c13" stroke="#3b4363" stroke-width="1.5"/><rect x="50" y="80" width="20" height="25" rx="2.5" fill="url(#{gid}-screen)"/>
<path d="M53 86h11M53 91h14M53 96h9M53 101h12" stroke="rgba(10,40,60,0.55)" stroke-width="2" stroke-linecap="round"/>
<circle cx="67.5" cy="82.5" r="2.4" fill="{EMBER}" style="animation:blink 2s steps(2) infinite"/>
<ellipse cx="46" cy="96" rx="5.2" ry="4.4" fill="#283049"/><ellipse cx="74" cy="96" rx="5.2" ry="4.4" fill="#283049"/>
</g></g>"""


GRIM_CSS = "@keyframes grimblink { 0%, 92%, 100% { transform: scaleY(1); } 95% { transform: scaleY(0.1); } }"


def bubble(x, y, lines, w=None, size=16, tail="right", cls=""):
    """Grim's speech bubble: light card, dark text, a little tail."""
    lw = max(T.width(l, "bodyb", size) for l in lines)
    w = w or lw + 36
    h = 22 + len(lines) * size * 1.35
    tx = x + w - 30 if tail == "right" else x + 26
    body = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h:.0f}" rx="14" fill="{INK}"/><path d="M{tx} {y + h - 1:.0f} l10 12 l4 -12z" fill="{INK}"/>'
    for i, l in enumerate(lines):
        body += f'<g fill="#0b0d12">{T.run(l, "bodyb", size, x + 18, y + 14 + size + i * size * 1.35)}</g>'
    return f'<g class="{cls}">{body}</g>'
