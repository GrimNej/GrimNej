"""Generate the profile README's images into assets/.

    python src/gen.py [out-dir] [name,name...]
"""
import sys
import time
from pathlib import Path

import profile as P

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "assets"
only = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None
OUT.mkdir(parents=True, exist_ok=True)
jobs = {
    "banner": P.banner,
    "typing": P.typing,
    "contact-console": P.console,
    "focus-map": P.focus_map,
    "stack-icons": P.stack_icons,
    "ai-tools": P.ai_tools,
    "idea-to-mvp": P.idea_to_mvp,
    "pill-portfolio": lambda: P.pill("portfolio", "globe", "ember"),
    "pill-email": lambda: P.pill("grim98413@gmail.com", "gmail"),
    "pill-linkedin": lambda: P.pill("GrimNej", "linkedin"),
    "pill-instagram": lambda: P.pill("@grimnej", "instagram"),
    "pill-x": lambda: P.pill("@grimnej_", "x"),
    "pill-youtube": lambda: P.pill("@grimnej", "youtube"),
}
for name, fn in jobs.items():
    if only and name not in only:
        continue
    t = time.time()
    svg = fn()
    (OUT / f"{name}.svg").write_text(svg, encoding="utf8")
    print(f"{name:16} {len(svg.encode()) / 1024:5.0f} KB  {time.time() - t:4.1f}s", flush=True)
