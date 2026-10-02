# Wearable AI design handoff

This folder gives the designer the research content, sources and editable drafts for the Wearable AI map. The [current English page](../../site/research-map.html) is a **16-milestone overview, not a visualization of the entire repository**. The repository contains 396 accepted records and 45 watchlist candidates, with a data cutoff of 2026-09-02.

## Complete research content

Use [generated/registry.json](../../generated/registry.json) for the complete accepted registry and watchlist, or [data/records](../../data/records/) for the authoritative YAML. The [search interface](../../site/index.html) exposes all records. [Taxonomy](../../data/taxonomy.yaml), [coverage](../../generated/coverage.md), [model families](../../generated/families/index.md) and [explicit relations](../../data/relations.yaml) provide additional structure. The selected map does not enumerate datasets, standards or tools; it places them in a supporting layer.

## Map content and editable assets

| Material | Purpose |
|---|---|
| [milestones.json](milestones.json) | 32 source-checked candidate works, short captions, original record IDs, source URLs, date notes and evidence boundaries. Includes the 29-item poster selection; this is separate from the 16-item web selection. |
| [taxonomy.json](taxonomy.json) | Four proposed research roles, eight routes, exact web selections and a pointer to the complete registry. This is an editorial display taxonomy, not a replacement for the registry taxonomy. |
| [compact-map-source.html](compact-map-source.html) | Editable source for the self-contained English overview. |
| [Research map SVG](drafts/wearable-ai-research-map.svg) and [PNG](drafts/wearable-ai-research-map.png) | Earlier classification layout draft. |
| [Evolution tree SVG](drafts/wearable-ai-evolution-tree.svg) and [PNG](drafts/wearable-ai-evolution-tree.png) | Earlier 29-node timeline layout draft. |
| [XMind](drafts/wearable-ai-research-map.xmind) | Editable classification, selected timeline and a full source-index sheet. The full index preserves existing metadata; it was not comprehensively re-audited. |

The poster and XMind layouts are reference drafts, not approved final designs. They were superseded by the compact page because their density, size and styling did not meet the desired single-screen presentation. Do not carry their fixed dimensions or bilingual labels into the final English interface.

## Design requirements

- English only, with concise, natural labels and a clear type hierarchy.
- Show the main map within one desktop viewport; do not shrink a large poster until its labels become unreadable.
- Use a shared upward year axis so contemporary work can be compared across branches. Keep dates attached to the correct works.
- Use a coherent palette tied to research roles. Reveal fuller descriptions and source links on selection instead of placing paragraphs beside every node.
- Preserve access to the complete registry. A small overview must be visibly identified as a selection, not the whole literature.
- Branches describe research categories. Do not imply model inheritance, clinical benefit or a causal progression without supporting evidence.

## Source caveats

The selected works received renewed primary-source checks, but the complete registry did not. `milestones.json` records two known title or link mismatches: `model-eeg-to-text-2022` and `method-v-learning-2015`. They are excluded from map milestones and their hyperlinks are withheld in the XMind source-index sheet. The original registry was not silently corrected.

Registry years can refer to first-publication or issue years. Notes retain identified differences, including LSM, PaPaGei and the JITAI review. Prediction or measurement validation is not evidence of treatment benefit. IDEA and myBPmyLife retain their negative or mixed findings. Some records concern clinical or implantable-adjacent sensing rather than consumer wearables.

## Visual references

These links are design references, not evidence that all of them use the same chart structure. Third-party PDFs and images have not been copied into this repository.

- [Awesome VLA](https://github.com/yueen-ma/awesome-vla): taxonomy and named research milestones.
- [Awesome VLA and WAM](https://github.com/DravenALG/awesome-vla-wam): concise topic navigation and research entries.
- [Time series papers](https://github.com/TSCenter/awesome-time-series-papers): task and year organization.
- [World models survey](https://arxiv.org/pdf/2606.00133): Figure 1 combines classification, milestones and applications; Figure 3 separates capability comparison.
- [Robot world model survey](https://ntumars.github.io/wm-robot-survey/): compact role-based timeline and architecture explanations.

## Rebuild and preview

Run `python scripts/render_research_map.py` from the repository root to rebuild `site/research-map.html` from the source template and selected metadata. The page is self-contained and can be opened locally. The existing published editorial site in [website](../../website/) and its deployment workflow are unchanged by this handoff.

Repository-created materials use the [repository license](../../LICENSE). Linked papers, images and other third-party resources retain their own rights and access conditions.
