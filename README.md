# Awesome Wearable AI website

An editorial, scroll-driven introduction to the [Awesome Wearable AI](https://github.com/ZipengWu365/awesome-wearable-ai) evidence atlas.

Published with GitHub Pages at <https://zipengwu365.github.io/awesome-wearable-ai/> from the isolated `gh-pages` branch. The research source and its history remain on `main`.

## Preview locally

The site is dependency-free. Serve the directory over HTTP so the browser can load `registry.json`:

```bash
python3 -m http.server 4173
```

Then open <http://localhost:4173>.

## Files

- `index.html` — narrative structure, visual-stage SVG, atlas interface
- `styles.css` — visual system, scene transitions, responsive and reduced-motion rules
- `app.js` — scroll state, search/filter/group interactions, record detail shelf
- `registry.json` — 396 accepted records synced from Awesome Wearable AI v0.3.0
- `assets/images/` — generated desktop/mobile hero, impact and community illustrations

The interface deliberately separates lifecycle stages from record taxonomy and keeps each record's evidence boundary visible. Counts are coverage indicators, not claims of clinical efficacy or exhaustive retrieval.
