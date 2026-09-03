#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import shutil

from registry import ROOT

SITE = ROOT / "site"
GENERATED = ROOT / "generated"


def main() -> int:
    SITE.mkdir(exist_ok=True)
    shutil.copyfile(GENERATED / "registry.json", SITE / "registry.json")
    stats = json.loads((GENERATED / "statistics.json").read_text(encoding="utf-8"))
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Awesome Wearable AI Evidence Atlas</title>
  <meta name="description" content="Search {stats['accepted_total']} quality-screened wearable AI records and {stats['watchlist_total']} watchlist candidates.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <p class="eyebrow">Awesome Wearable AI · v0.3.0</p>
    <h1>Wearable AI Evidence Atlas</h1>
    <p>Models, datasets, digital measures, causal methods, adaptive interventions, closed-loop systems, and deployment infrastructure.</p>
    <div class="stats"><span>{stats['accepted_total']} accepted</span><span>{stats['watchlist_total']} watchlist</span><span>{stats['relation_total']} relations</span></div>
  </header>
  <main>
    <section class="controls" aria-label="Search and filters">
      <input id="query" type="search" placeholder="Search title, contribution, modality, domain, venue…" aria-label="Search records">
      <select id="type"><option value="">All record types</option></select>
      <select id="family"><option value="">All families</option></select>
      <select id="tier"><option value="">All evidence sources</option></select>
      <label><input id="watchlist" type="checkbox"> Include watchlist</label>
    </section>
    <p id="count" class="count"></p>
    <section id="results" class="grid" aria-live="polite"></section>
  </main>
  <footer>Counts are coverage indicators. Inclusion does not establish clinical utility, causal effect, or regulatory approval.</footer>
  <script src="app.js"></script>
</body>
</html>'''
    (SITE / "index.html").write_text(html, encoding="utf-8")
    print("Static search site built")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
