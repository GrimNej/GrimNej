"""The profile README's images, redrawn in the grimnej.com design language.

Same pieces and wording as before; new palette, type, particles and Grim.
"""
import json
import math
import random
from pathlib import Path

import kit as K
import type as T

INPUTS = Path(__file__).parent / "inputs"
ICONS = json.loads((INPUTS / "icons.json").read_text(encoding="utf8"))
GOLD = "#ffb547"
BRAND = {
    "x": "#f0f3fa", "linkedin": "#2b8cf0", "youtube": "#ff3b3b", "instagram": "#ff3d8b", "gmail": "#ff6b3d", "discord": "#7c86ff",
    "html5": "#e34f26", "css": "#3d8bfd", "google": "#4285f4", "openai": "#eceef4", "openjdk": "#f89820",
}
GLOBE = "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-2.9a15.7 15.7 0 0 0-1.4-3.6A8 8 0 0 1 18.9 8zM12 4a13.8 13.8 0 0 1 1.9 4h-3.8A13.8 13.8 0 0 1 12 4zM4.3 14a8.2 8.2 0 0 1 0-4h3.4a16.5 16.5 0 0 0 0 4zm.8 2h2.9a15.7 15.7 0 0 0 1.4 3.6A8 8 0 0 1 5.1 16zM8 8H5.1a8 8 0 0 1 4.3-3.6A15.7 15.7 0 0 0 8 8zm4 12a13.8 13.8 0 0 1-1.9-4h3.8A13.8 13.8 0 0 1 12 20zm2.3-6H9.7a14.7 14.7 0 0 1 0-4h4.6a14.7 14.7 0 0 1 0 4zm.3 5.6a15.7 15.7 0 0 0 1.4-3.6h2.9a8 8 0 0 1-4.3 3.6zm1.7-5.6a16.5 16.5 0 0 0 0-4h3.4a8.2 8.2 0 0 1 0 4z"
SHEEN = (
    '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6fe3ff" stop-opacity="0"/>'
    '<stop offset="0.3" stop-color="#6fe3ff" stop-opacity="0.95"/><stop offset="0.5" stop-color="#ffffff"/>'
    '<stop offset="0.7" stop-color="#ff6b3d" stop-opacity="0.95"/><stop offset="1" stop-color="#ff6b3d" stop-opacity="0"/></linearGradient>'
)
BALL = '<defs><radialGradient id="ball" cx="0.31" cy="0.29" r="0.75"><stop offset="0" stop-color="#2d3348"/><stop offset="0.55" stop-color="#141722"/><stop offset="1" stop-color="#08090d"/></radialGradient></defs>'


def icon_color(slug):
    if slug in BRAND:
        return BRAND[slug]
    hexc = ICONS[slug]["hex"].lstrip("#")
    r, g, b = (int(hexc[i:i + 2], 16) for i in (0, 2, 4))
    # Brands drawn in near-black would vanish on the dark panels.
    return K.INK if 0.2126 * r + 0.7152 * g + 0.0722 * b < 70 else "#" + hexc


def icon(slug, x, y, size, color=None):
    d = GLOBE if slug == "globe" else ICONS[slug]["path"]
    return f'<path d="{d}" transform="translate({x:.1f} {y:.1f}) scale({size / 24:.3f})" fill="{color or icon_color(slug)}"/>'


def bare_svg(w, h, body, css, label):
    """An SVG without the panel frame (buttons, the typing line, the chip board)."""
    glyphs = T.defs()
    T.begin()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">'
        f'<title>{label}</title><style>{K.BASE_CSS}{css}</style><defs>{glyphs}</defs>{body}</svg>'
    )


def hud_tag(text_, x, y, color=K.ICE, border="rgba(111,227,255,0.45)", dot=None, size=14):
    w = T.width(text_, "mono", size) + 18 + (16 if dot else 0)
    out = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" rx="2" fill="rgba(7,8,11,0.82)" stroke="{border}"/>'
    tx = x + 9
    if dot:
        out += f'<circle cx="{x + 14}" cy="{y + 14}" r="3.6" fill="{dot}" style="animation:blink 1.6s steps(2) infinite"/>'
        tx += 16
    return out + K.mono(text_, tx, y + 19, size, color)


# ------------------------------------------------------------------ banner

def banner():
    W, H = 1200, 360
    size, x0, base_y = 120, 64, 196
    defs, uses, hot = [], [], []
    order = list(range(7))
    random.Random(3).shuffle(order)
    for n, (ch, d, gx, adv) in enumerate(T.glyph_paths("GrimNej", "name", size, x0, base_y)):
        defs.append(f'<path id="ng{n}" d="{d}"/>')
        uses.append(f'<use href="#ng{n}"/>')
        hot.append(f'<use href="#ng{n}" fill="{K.EMBER}" class="hot" style="animation-delay:{order[n] * 2.4 + 2.5:.1f}s"/>')
    name_w = T.width("GrimNej", "name", size)
    name = (
        f'<defs>{"".join(defs)}<clipPath id="nameclip">{"".join(uses)}</clipPath>{SHEEN}'
        f'<linearGradient id="base" x1="{x0}" y1="0" x2="{x0 + name_w:.0f}" y2="30" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset="0.45" stop-color="#d6dcff"/><stop offset="1" stop-color="#8b9cff"/></linearGradient></defs>'
        f'<g clip-path="url(#nameclip)"><rect x="{x0 - 10}" y="{base_y - size}" width="{name_w + 40:.0f}" height="{size * 1.35:.0f}" fill="url(#base)"/>'
        f'<rect class="sheen" x="{x0 - 220}" y="{base_y - size}" width="180" height="{size * 1.35:.0f}" fill="url(#sheen)"/></g>' + "".join(hot)
    )

    # The console card from the old banner, as a glass panel.
    cx, cy, cw, ch = 806, 74, 334, 214
    rows = [("idea:", "stress-tested", K.GREEN), ("agents:", "orchestrated", K.ICE), ("mvp:", "warming engines", K.EMBER), ("bugs:", "under negotiation", K.SIGNAL)]
    console = (
        f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="rgba(10,11,16,0.86)" stroke="{K.LINE2}" stroke-width="1.5"/>'
        f'<path d="M{cx} {cy + 40}H{cx + cw}" stroke="{K.LINE}" stroke-width="1.5"/>'
        + "".join(f'<circle cx="{cx + 20 + i * 14}" cy="{cy + 20}" r="4" fill="{c}" opacity="0.8"/>' for i, c in enumerate([K.EMBER, GOLD, K.GREEN]))
        + K.mono("ai_build_console", cx + 68, cy + 25, 14, K.INK2)
    )
    for i, (k, v, c) in enumerate(rows):
        y = cy + 78 + i * 34
        console += K.mono(k, cx + 22, y, 15, K.INK3) + K.mono(v, cx + 122, y, 15, c)
    vend = cx + 122 + T.width("under negotiation", "mono", 15)
    console += f'<rect class="caret" x="{vend + 6:.0f}" y="{cy + 78 + 3 * 34 - 14}" width="9" height="17" fill="{K.EMBER}"/>'

    body = (
        K.glow(180, 40, 520, K.EMBER, 0.16, "g1")
        + K.glow(1000, 330, 480, K.SIGNAL, 0.18, "g2")
        + K.stars(W, H, 130, seed=3)
        + K.glow(860, 190, 260, "#3a4bb0", 0.34, "g3")
        + f'<g class="field">{K.galaxy(870, 186, 300, 176, tilt=-10, n=1700, seed=11, rings=((0.62, 0.03, 0.46), (0.94, 0.035, 0.44)))}</g>'
        + hud_tag("BUILD MODE: ON", x0, 52, dot=K.GREEN)
        + name
        + K.mono("The AI Guy", x0, 252, 30, K.ICE, style="monob")
        + K.text("AI Solutions Architect · Agentic Engineer · Rapid MVP Builder", "title", 21, x0, 300, K.INK2)
        + console
        + K.grim(672, 168, 0.88, "bg")
        + K.grain(W, H, 0.045)
    )
    css = K.GRIM_CSS + """
.field { animation: fadein 2s ease-out both; }
.sheen { animation: sheen 7s cubic-bezier(0.65, 0, 0.35, 1) 1s infinite; }
@keyframes sheen { 0% { transform: translateX(0); } 40%, 100% { transform: translateX(760px); } }
.hot { opacity: 0; animation: hot 17s ease-in-out infinite; }
@keyframes hot { 0% { opacity: 0; } 1.5%, 7% { opacity: 1; } 9.5%, 100% { opacity: 0; } }
.caret { animation: blink 1.1s steps(2) infinite; }
"""
    return K.svg(W, H, body, css, "GrimNej. The AI Guy. AI Solutions Architect, Agentic Engineer, Rapid MVP Builder. Build mode: on.", radius=20)


# ------------------------------------------------------------------ link buttons

def pill(label, slug, kind="ghost"):
    h, size = 38, 15
    tw = T.width(label, "label", size)
    w = round(44 + tw + 18)
    bg, fg, stroke = (K.EMBER, "#170702", "none") if kind == "ember" else ("#0b0c11", K.INK, "rgba(232,235,245,0.22)")
    body = f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{(h - 1.5) / 2}" fill="{bg}" stroke="{stroke}" stroke-width="1.5"/>'
    body += icon(slug, 16, h / 2 - 9, 18, fg if kind == "ember" else None)
    body += K.text(label, "label", size, 44, h / 2 + 5.4, fg)
    return bare_svg(w, h, body, "", label)


# ------------------------------------------------------------------ typing line

def typing():
    """The four lines typed out and deleted in turn, character by character (SMIL, one shared clock)."""
    W, H, size = 980, 56, 24
    lines = ["AI agents that actually do the work", "Idea to MVP before the meeting gets cold", "Automation, RAG, cloud, tools, deployments", "If it touches AI, I am probably building it"]
    slot, cycle = 4.0, 4.0 * len(lines)
    type_t, hold_t, del_t = 1.7, 1.4, 0.6  # seconds within each line's slot
    body, defs = "", ""
    for i, line in enumerate(lines):
        w = T.width(line, "mono", size)
        x0 = W / 2 - w / 2
        n = len(line)
        start = i * slot
        times, widths = [0.0], [0.0]
        for c in range(n + 1):  # typing
            times.append(start + type_t * c / n)
            widths.append(w * c / n)
        for c in range(n, -1, -1):  # deleting, after the hold
            times.append(start + type_t + hold_t + del_t * (n - c) / n)
            widths.append(w * c / n)
        # keyTimes must start at 0 and rise; drop duplicate leading stamps.
        kt, vals = [], []
        for t, v in zip(times, widths):
            if kt and t <= kt[-1]:
                vals[-1] = v
                continue
            kt.append(t)
            vals.append(v)
        key_times = ";".join(f"{t / cycle:.4f}" for t in kt)
        width_vals = ";".join(f"{v:.1f}" for v in vals)
        caret_x = ";".join(f"{x0 + v:.1f}" for v in vals)
        shown = ";".join("1" if (start <= t < start + type_t + hold_t + del_t) else "0" for t in kt)
        rest_w = w if i == 0 else 0
        anim = f'dur="{cycle:.0f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{key_times}"'
        defs += f'<clipPath id="c{i}"><rect x="{x0 - 2:.1f}" y="0" width="{rest_w + 4 if i == 0 else 0:.1f}" height="{H}"><animate attributeName="width" values="{width_vals}" {anim}/></rect></clipPath>'
        body += f'<g clip-path="url(#c{i})">{K.mono(line, x0, 37, size, K.ICE)}</g>'
        body += (
            f'<rect class="blinker" x="{x0 + rest_w + 3:.1f}" y="15" width="3" height="28" fill="{K.EMBER}" opacity="{1 if i == 0 else 0}">'
            f'<animate attributeName="x" values="{caret_x}" {anim}/><animate attributeName="opacity" values="{shown}" {anim}/></rect>'
        )
    css = ".blinker { animation: blinkfill 0.9s steps(2) infinite; } @keyframes blinkfill { 50% { fill: transparent; } }"
    strip = f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="12" fill="#0b0c11" stroke="{K.LINE2}" stroke-width="1.5"/>'
    return bare_svg(W, H, f"<defs>{defs}</defs>{strip}{body}", css, ". ".join(lines))


# ------------------------------------------------------------------ contact console

def console():
    W, H = 1100, 260
    body = (
        K.glow(160, 30, 420, K.EMBER, 0.14, "c1") + K.glow(980, 250, 420, K.SIGNAL, 0.16, "c2") + K.stars(W, H, 90, seed=21)
        + f'<g class="field">{K.galaxy(930, 130, 260, 92, tilt=-6, n=900, seed=5, rings=((0.7, 0.04, 0.5), (0.98, 0.035, 0.4)))}</g>'
        + f'<rect x="38" y="38" width="1024" height="184" rx="14" fill="rgba(10,11,16,0.86)" stroke="{K.LINE2}" stroke-width="1.5"/>'
        + K.mono("$", 72, 84, 19, K.EMBER, style="monob") + K.mono("idea_to_mvp --speed=ridiculous --excuses=0", 94, 84, 19, K.ICE)
        + K.text("Have an AI idea? I can tell if it flies.", "head", 34, 72, 136, K.INK)
        + K.text("Then I build the runway", "head", 34, 72, 180, K.INK)
    )
    dot_x = 72 + T.width("Then I build the runway", "head", 34) + 4
    cur_x = 160 + T.width("grim98413@gmail.com", "mono", 17) + 6
    body += (
        f'<rect x="{dot_x:.0f}" y="172" width="8" height="8" fill="{K.EMBER}"/>'
        + K.mono("contact:", 72, 208, 17, K.INK3) + K.mono("grim98413@gmail.com", 160, 208, 17, K.INK2)
        + f'<rect class="caret" x="{cur_x:.0f}" y="194" width="9" height="17" fill="{K.EMBER}"/>'
        + K.grim(906, 70, 0.95, "cg")
        + K.grain(W, H, 0.04)
    )
    css = K.GRIM_CSS + ".field { animation: fadein 2s ease-out both; } .caret { animation: blink 1.1s steps(2) infinite; }"
    return K.svg(W, H, body, css, "Have an AI idea? I can tell if it flies. Then I build the runway. Contact: grim98413@gmail.com", radius=20)


# ------------------------------------------------------------------ focus map

def node(x, y, w, title, sub, accent, delay):
    return (
        f'<g class="node" style="animation-delay:{delay}s">'
        f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="10" fill="#0b0c11" stroke="{K.LINE2}" stroke-width="1.5"/>'
        f'<rect x="{x + 18}" y="{y + 18}" width="8" height="8" fill="{accent}"/>'
        + K.text(title, "head", 20, x + 36, y + 30, K.INK)
        + K.mono(sub, x + 18, y + 54, 13, K.INK3)
        + "</g>"
    )


def focus_map():
    W, H = 1100, 340
    cx, cy = 550, 190
    body = (
        K.glow(cx, cy, 340, "#3a4bb0", 0.3, "f1") + K.glow(120, 40, 360, K.EMBER, 0.12, "f2") + K.stars(W, H, 100, seed=33)
        + f'<g class="field">{K.galaxy(cx, cy, 360, 118, tilt=-3, n=1500, seed=17, rings=((0.78, 0.04, 0.55), (1.0, 0.03, 0.35)))}</g>'
        + K.text("Currently focused on anything that makes AI useful", "head", 23, cx, 46, K.INK, "middle")
        # The AI core: a brushed-silver disc with black type.
        + '<defs><radialGradient id="silver" cx="0.36" cy="0.3" r="0.8"><stop offset="0" stop-color="#ffffff"/>'
        '<stop offset="0.45" stop-color="#e3e6ee"/><stop offset="0.8" stop-color="#b9bfcc"/><stop offset="1" stop-color="#8f96a6"/></radialGradient>'
        '<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#7c8394"/></linearGradient></defs>'
        + f'<circle cx="{cx}" cy="{cy}" r="74" fill="rgba(232,235,245,0.10)" class="pulse" style="transform-origin:{cx}px {cy}px"/>'
        + f'<circle cx="{cx}" cy="{cy}" r="60" fill="url(#silver)" stroke="url(#rim)" stroke-width="1.5"/>'
        + K.text("AI", "orb", 30, cx, cy - 2, "#07080b", "middle")
        + K.mono("non-stop", cx, cy + 21, 12.5, "#2a2d38", "middle", style="monob")
        + K.mono("adapting", cx, cy + 37, 12.5, "#2a2d38", "middle", style="monob")
        + node(110, 78, 230, "AI agents", "tools, memory, loops", K.ICE, 0)
        + node(760, 78, 230, "Agentic AI", "orchestrated systems", K.SIGNAL, 0.6)
        + node(84, 216, 250, "Automation", "workflows with less drama", K.GREEN, 1.2)
        + node(430, 260, 240, "Rapid MVPs", "prototype before overthinking", K.EMBER, 1.8)
        + node(770, 216, 240, "Cloud deploy", "Docker, APIs, infra", GOLD, 2.4)
        + K.grain(W, H, 0.04)
    )
    css = """
.field { animation: fadein 2s ease-out both; }
.node { animation: breathe 4.8s ease-in-out infinite; }
@keyframes breathe { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
.pulse { animation: pulse 3.2s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { transform: scale(0.92); opacity: 0.9; } 50% { transform: scale(1.14); opacity: 0; } }
"""
    return K.svg(W, H, body, css, "Currently focused on anything that makes AI useful: AI agents, Agentic AI, Automation, Rapid MVPs, Cloud deploy. AI, non-stop adapting.", radius=20)


# ------------------------------------------------------------------ skills, as balls from the pit

SKILLS = [
    ("Python", "python"), ("TypeScript", "typescript"), ("JavaScript", "javascript"), ("Rust", "rust"), ("Java", "openjdk"), ("Lua", "lua"),
    ("PHP", "php"), ("HTML", "html5"), ("CSS", "css"), ("React", "react"), ("Next.js", "nextdotjs"), ("Node.js", "nodedotjs"),
    ("FastAPI", "fastapi"), ("Flask", "flask"), ("Docker", "docker"), ("Kubernetes", "kubernetes"), ("Linux", "linux"), ("Git", "git"),
    ("GitHub Actions", "githubactions"), ("PostgreSQL", "postgresql"), ("Redis", "redis"), ("Supabase", "supabase"), ("MongoDB", "mongodb"),
    ("AWS", None), ("Google Cloud", "googlecloud"), ("Azure", None), ("PyTorch", "pytorch"), ("TensorFlow", "tensorflow"), ("OpenCV", "opencv"),
]


def _settle(balls, W, H, iters=2600, seed=2):
    rnd = random.Random(seed)
    for b in balls:
        b["x"], b["y"] = rnd.uniform(b["r"], W - b["r"]), rnd.uniform(-H * 2, H - b["r"])
    for _ in range(iters):
        for b in balls:
            b["y"] += 2.0
        for _ in range(3):
            for i, a in enumerate(balls):
                for b in balls[i + 1:]:
                    dx, dy = b["x"] - a["x"], b["y"] - a["y"]
                    d = math.hypot(dx, dy) or 0.01
                    m = a["r"] + b["r"] + 1.5
                    if d < m:
                        p = (m - d) / 2
                        a["x"] -= dx / d * p; a["y"] -= dy / d * p
                        b["x"] += dx / d * p; b["y"] += dy / d * p
            for b in balls:
                b["x"] = min(max(b["x"], b["r"] + 1), W - b["r"] - 1)
                b["y"] = min(b["y"], H - b["r"] - 1)


def stack_icons():
    W, H = 1100, 230
    balls = [dict(name=n, slug=s, r=34 if i < 4 else 30) for i, (n, s) in enumerate(SKILLS)]
    _settle(balls, 1036, 186)
    rnd = random.Random(9)
    order = sorted(range(len(balls)), key=lambda i: -balls[i]["y"])
    out = []
    for rank, i in enumerate(order):
        b = balls[i]
        x, y, r = 32 + b["x"], 22 + b["y"], b["r"]
        col = icon_color(b["slug"]) if b["slug"] else K.EMBER
        rgb = ",".join(str(int(col[k:k + 2], 16)) for k in (1, 3, 5))
        g = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="url(#ball)" stroke="rgba({rgb},0.5)" stroke-width="1.4"/>'
        rot = rnd.uniform(-22, 22)
        if b["slug"]:
            sz = r * 0.98
            g += f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.0f})">{icon(b["slug"], -sz / 2, -sz / 2, sz, col)}</g>'
        else:
            fs = r * 0.5
            g += f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.0f})" fill="{K.INK}">{T.run(b["name"], "head", fs, 0, fs * 0.36, "middle")}</g>'
        out.append(f'<g class="ball" style="--d:{-(180 + b["y"] + rnd.uniform(0, 120)):.0f}px;animation-delay:{0.2 + rank * 0.05:.2f}s">{g}</g>')
    body = BALL + K.glow(550, 260, 460, K.EMBER, 0.13, "gs") + K.stars(W, H, 60, seed=31) + "".join(out) + K.grain(W, H, 0.04)
    css = """
.ball { animation: drop 1.1s cubic-bezier(0.34, 1.3, 0.64, 1) both; }
@keyframes drop { from { transform: translateY(var(--d)); } to { transform: translateY(0); } }
"""
    return K.svg(W, H, body, css, "Skills: " + ", ".join(n for n, _ in SKILLS), radius=20)


# ------------------------------------------------------------------ AI tools board

AI_TOOLS = [
    ("OpenAI", "openai"), ("OpenAI Agents SDK", "openai"), ("Anthropic", "anthropic"), ("Gemini", "googlegemini"), ("Google ADK", "google"),
    ("LangChain", "langchain"), ("LangGraph", "langgraph"), ("LlamaIndex", None), ("CrewAI", "crewai"), ("AutoGen", None), ("Pydantic AI", "pydantic"),
    ("DSPy", None), ("Mastra", None), ("Semantic Kernel", None), ("MCP", "modelcontextprotocol"), ("RAG", None), ("Vector DBs", None),
    ("Pinecone", None), ("Qdrant", "qdrant"), ("Chroma", None), ("Vercel AI SDK", "vercel"), ("Hugging Face", "huggingface"), ("Ollama", "ollama"),
]


def ai_tools():
    """The AI badges as one chip board; the chips take turns glowing ember."""
    W = 1100
    size, h, gap, pad = 15, 40, 10, 16
    chips = [(name, slug, pad + 28 + T.width(name, "label", size) + pad) for name, slug in AI_TOOLS]
    rows, cur, cw = [], [], 0
    for c in chips:
        if cur and cw + gap + c[2] > W:
            rows.append(cur)
            cur, cw = [], 0
        cur.append(c)
        cw += (gap if cw else 0) + c[2]
    rows.append(cur)
    order = list(range(len(chips)))
    random.Random(8).shuffle(order)
    body, k = "", 0
    for ri, row in enumerate(rows):
        x = (W - sum(c[2] for c in row) - gap * (len(row) - 1)) / 2
        y = 4 + ri * (h + gap)
        for name, slug, w in row:
            body += f'<rect class="cb" style="animation-delay:{order[k] * 1.3:.1f}s" x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="9" fill="#0b0c11" stroke="rgba(232,235,245,0.18)" stroke-width="1.5"/>'
            body += icon(slug, x + pad, y + h / 2 - 9, 18) if slug else f'<rect x="{x + pad + 5}" y="{y + h / 2 - 4}" width="8" height="8" fill="{K.EMBER}"/>'
            body += K.text(name, "label", size, x + pad + 28, y + h / 2 + 5.4, K.INK)
            x += w + gap
            k += 1
    H = int(8 + len(rows) * (h + gap))
    css = """
.cb { animation: hotchip 30s ease-in-out infinite; }
@keyframes hotchip { 0%, 100% { stroke: rgba(232,235,245,0.18); } 1.5%, 3.5% { stroke: #ff6b3d; } 5% { stroke: rgba(232,235,245,0.18); } }
"""
    return bare_svg(W, H, body, css, "AI systems: " + ", ".join(n for n, _ in AI_TOOLS))


# ------------------------------------------------------------------ idea to MVP

def idea_to_mvp():
    W, H = 1100, 300
    flow = "M110 150C260 84 360 216 510 150S760 84 990 150"
    stages = [
        ("Idea", "what if...", "famous last words", K.ICE),
        ("Map", "system shape", "no fog allowed", K.SIGNAL),
        ("Test Risk", "hardest part first", "panic, but typed", K.EMBER),
        ("Build", "MVP + deploy", "it lives", K.GREEN),
        ("Handoff", "docs + next moves", "future-proof-ish", GOLD),
    ]
    body = (
        K.glow(140, 30, 420, K.EMBER, 0.13, "i1") + K.glow(980, 290, 420, K.SIGNAL, 0.16, "i2") + K.stars(W, H, 90, seed=41)
        + f'<g class="field">{K.galaxy(550, 160, 500, 70, tilt=-2, n=900, seed=23, rings=((0.85, 0.05, 0.6), (1.0, 0.03, 0.3)))}</g>'
        + '<defs><linearGradient id="flow" x1="110" y1="0" x2="990" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#6fe3ff"/>'
        '<stop offset="0.5" stop-color="#8b9cff"/><stop offset="1" stop-color="#ff6b3d"/></linearGradient>'
        '<filter id="spk" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
        + K.text("How I move from idea to working product", "head", 25, 550, 48, K.INK, "middle")
        + f'<path class="dash" d="{flow}" fill="none" stroke="url(#flow)" stroke-width="3" stroke-linecap="round" opacity="0.85"/>'
    )
    for i, (t, a, b, c) in enumerate(stages):
        x = 54 + i * 208
        body += (
            f'<g class="card" style="animation-delay:{i * 0.4:.1f}s"><rect x="{x}" y="92" width="160" height="116" rx="12" fill="#0b0c11" stroke="{K.LINE2}" stroke-width="1.5"/>'
            f'<rect x="{x + 20}" y="92" width="40" height="3" fill="{c}"/>'
            + K.text(t, "head", 20, x + 80, 134, K.INK, "middle")
            + K.mono(a, x + 80, 164, 13, K.INK3, "middle")
            + K.mono(b, x + 80, 186, 13, c, "middle")
            + "</g>"
        )
    body += (
        f'<circle r="6" fill="#ffffff" filter="url(#spk)"><animateMotion dur="5.5s" repeatCount="indefinite" path="{flow}"/>'
        '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="5.5s" repeatCount="indefinite"/></circle>'
        + K.mono("Architecture first. Execution fast. No shrine to one stack.", 550, 262, 16, K.INK2, "middle")
        + K.grain(W, H, 0.04)
    )
    css = """
.field { animation: fadein 2s ease-out both; }
.dash { stroke-dasharray: 14 14; animation: dash 5s linear infinite; }
@keyframes dash { to { stroke-dashoffset: -112; } }
.card { animation: lift 4.8s ease-in-out infinite; }
@keyframes lift { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
"""
    return K.svg(W, H, body, css, "How I move from idea to working product: Idea, Map, Test Risk, Build, Handoff. Architecture first. Execution fast. No shrine to one stack.", radius=20)
