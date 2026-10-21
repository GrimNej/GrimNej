# Profile README source

The images in the profile README are generated here, in the design language of [grimnej.com](https://grimnej.com): the near-black space, particle galaxy, ember accent, Mona Sans at 120 percent width, JetBrains Mono, and Grim. Type is shaped with HarfBuzz and drawn as vector outlines, because GitHub shows README SVGs as images, where web fonts are unreliable.

```bash
python -m pip install uharfbuzz fonttools brotli
python src/gen.py                     # writes every SVG into assets/
python src/gen.py assets banner,typing  # only the listed pieces
```

| Image | What it is |
|---|---|
| `banner.svg` | Build mode tag, GrimNej with the light streak and ember letter, the console card, Grim in the galaxy |
| `pill-*.svg` | The link buttons |
| `typing.svg` | The four lines, typed and deleted in turn |
| `contact-console.svg` | "Have an AI idea? I can tell if it flies." |
| `focus-map.svg` | Current focus, orbiting the AI core |
| `stack-icons.svg` | Languages and infrastructure as balls from the site's pit |
| `ai-tools.svg` | The AI systems board |
| `idea-to-mvp.svg` | How an idea becomes a working product |

Code: `type.py` (shaping and outlines), `kit.py` (galaxy, stars, panels, Grim), `profile.py` (every image), `gen.py` (writes them). Inputs: fonts and brand icons in `inputs/`.
