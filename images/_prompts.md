# Hero image prompts. verbatim, for `gpt-image-1` upgrade

When an OpenAI API key with `api.model.images.request` scope is provisioned, re-render the hero PNGs by feeding these prompts to `openai api images.generate` (model `gpt-image-1`, size `1536x1024`, quality `high`). Keep filenames identical so route references do not break.

## Shared style preamble (prepend to every prompt)

> Flat editorial illustration. Restrained palette: deep navy `#2c5f7f`, soft cyan `#9bc7d8`, warm cream background `#fdf8ef`, single accent of muted gold `#b8860b`. Clean geometric shapes. No text in image. No people's faces (silhouettes OK). No AI-glow, no emoji, no neon, no clutter, no chrome/AI-tropes. Aspect ratio 3:2 landscape. Editorial, calm, executive-grade. Subject placed off-center with generous negative space.

## tier-0-hero.png

> A simple compass/wayfinder symbol over a clean horizon line. Single subject. Communicates "baseline orientation." The compass face is minimalist: cardinal N marker in muted gold, the rest in navy. Soft horizon line in gold. Composition: compass occupies the upper-right third; rest is open cream space.

## tier-1-hero.png

> A clean workbench viewed from above. Three precisely placed tools, evenly spaced: a magnifying glass (verification), a small ruled gauge (evals), a sealed envelope with a gold wax seal (data policy). Wood tones in restrained cream/tan; tools in navy. Top-down view; surface fills lower three-quarters. Communicates "operating discipline."

## tier-2-hero.png

> An abstract relay-baton handoff between two stylized hands across a thin gold vertical line labeled "TRUST BOUNDARY." Left hand in deep navy offering the baton; right hand in soft cyan receiving it. Baton itself is muted gold. The gold boundary line is dashed, vertical, full-height. Negative space above and below. Communicates "delegation with a gate."

## tier-3-hero.png

> A boardroom table viewed from directly above. Oval/elliptical dark walnut table. Seven clean white coffee cup rings arranged at evenly-spaced positions around the perimeter (representing the seven executive lenses). No people. No clutter on the table. Subtle gold ring inset in the table edge. Composition: table centered, ample cream border. Communicates "discipline at the board level."

## academy-overview-hero.png

> A vertical ladder ascending into a soft sunrise. Four widely-spaced rungs visible (four tiers). The ladder is deep navy. The sunrise behind is a soft circular glow in muted gold (`#b8860b` at 18-25% opacity). The lowest rung sits near the bottom edge; the highest rung sits near the top, slightly more prominent. The composition is vertical-emphasis even within the 3:2 landscape canvas; place the ladder slightly left of center. Aspirational, calm, executive.

## aegis-academy-square-logo-mark.png (1024x1024)

> An abstract brand mark combining a shield outline (Aegis = shield in Greek) with a subtle 4-rung ladder motif inside it. Flat, single-color: deep navy `#2c5f7f` on warm cream `#fdf8ef`. Centered, scalable down to favicon size. Below the shield, the word "AEGIS" in a refined serif (Georgia or similar). Suitable for use at small sizes (favicon to social card to print).

## Notes

- The prompts deliberately exclude "ladder" from the Tier 2/3 hero descriptions to keep the ladder motif exclusive to the academy-overview + logo mark. Each tier hero has its own signature object.
- All hero prompts avoid any rendering of human faces. Silhouettes/hands are OK because they read as universal rather than identifying any demographic.
- The style preamble forbids "AI-glow," "neon," and "chrome" deliberately: those are the visual tropes that mark training-era AI image generation. Aegis is editorial, calm, and confidently uncluttered.

## Re-rendering snippet

```bash
export OPENAI_API_KEY=sk-...
cd "/Users/eric_pharr/Projects/Aegis Academy/v1.3/multimedia/images"

# Example for tier-2-hero.png
python3 <<'PY'
import os, base64
from openai import OpenAI
client = OpenAI()
PREAMBLE = "Flat editorial illustration. Restrained palette: deep navy #2c5f7f, soft cyan #9bc7d8, warm cream background #fdf8ef, single accent of muted gold #b8860b. Clean geometric shapes. No text in image. No people's faces (silhouettes OK). No AI-glow, no emoji, no neon, no clutter, no chrome/AI-tropes. Aspect ratio 3:2 landscape. Editorial, calm, executive-grade. Subject placed off-center with generous negative space."
PROMPT = "An abstract relay-baton handoff between two stylized hands across a thin gold vertical line labeled TRUST BOUNDARY. Left hand in deep navy offering the baton; right hand in soft cyan receiving it. Baton itself is muted gold. The gold boundary line is dashed, vertical, full-height. Negative space above and below. Communicates delegation with a gate."
resp = client.images.generate(
    model="gpt-image-1",
    prompt=f"{PREAMBLE}\n\n{PROMPT}",
    size="1536x1024",
    quality="high",
)
img = base64.b64decode(resp.data[0].b64_json)
with open("tier-2-hero.png", "wb") as f:
    f.write(img)
print("OK")
PY
```
