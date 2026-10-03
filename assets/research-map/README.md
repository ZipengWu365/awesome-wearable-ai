# Wearable AI design handoff

This folder gives the designer the complete research content, sources and editable drafts for the Wearable AI map. The [current English page](../../site/research-map.html) maps **all 396 accepted records and all 45 watchlist candidates** from the repository, with a data cutoff of 2026-09-02. Every record is embedded in the page and reachable through a branch, year group or search result; this is no longer a 16-example overview.

## Complete research content

Use [generated/registry.json](../../generated/registry.json) for the complete accepted registry and watchlist, or [data/records](../../data/records/) for the authoritative YAML. [Taxonomy](../../data/taxonomy.yaml), [repository coverage](../../generated/coverage.md), [families](../../generated/families/index.md) and [explicit relations](../../data/relations.yaml) provide additional structure. The map uses the six native record types: 102 models, 35 measures, 61 methods, 40 interventions, 116 datasets and 42 infrastructure records. The latter includes tools, standards and published reporting guidelines, so it must not be omitted when covering papers. Not every repository record is a paper.

The [map coverage ledger](coverage.json) lists every accepted and watchlist ID with its branch, original year, time group and research family. Builds fail for omitted, duplicate or unassigned IDs. All 73 accepted research families remain available as filters. Watchlist records stay separate and retain their publication status and inclusion reason.

## Map content and editable assets

| Material | Purpose |
|---|---|
| [coverage.json](coverage.json) | Complete ID-by-ID map assignment and source checksum for all 441 records. |
| [taxonomy.json](taxonomy.json) | Native record-type branches, an independent watchlist branch and the full-coverage requirement. |
| [compact-map-source.html](compact-map-source.html) | Editable source for the self-contained English map, including expandable year counts, full lists, search and evidence details. |
| [milestones.json](milestones.json) | Earlier 32 source-checked examples, captions, original IDs, date notes and evidence boundaries. Supplemental material only; no longer the map's data source. |
| [Research map SVG](drafts/wearable-ai-research-map.svg) and [PNG](drafts/wearable-ai-research-map.png) | Earlier classification layout draft. |
| [Evolution tree SVG](drafts/wearable-ai-evolution-tree.svg) and [PNG](drafts/wearable-ai-evolution-tree.png) | Earlier 29-node timeline layout draft. |
| [XMind](drafts/wearable-ai-research-map.xmind) | Editable classification, selected timeline and a full source-index sheet. The full index preserves existing metadata; it was not comprehensively re-audited. |

The poster and XMind layouts are earlier reference drafts, not approved final designs or full-coverage substitutes. The current page uses the complete registry. Do not carry the posters' fixed dimensions or bilingual labels into the final English interface.

## Design requirements

- English only, with concise, natural labels and a clear type hierarchy.
- Show the main map within one desktop viewport; do not shrink a large poster until its labels become unreadable.
- Use a shared upward year axis so contemporary work can be compared across branches. The registry spans 1980–2026. Earlier years are explicitly grouped as 1980–2009 and 2010–2014; 2015 onward is shown annually. This is a grouped calendar axis, not a linear time scale. Exact original years remain visible for every record.
- Use a coherent palette tied to research roles. Reveal fuller descriptions and source links on selection instead of placing paragraphs beside every node.
- Cover every repository paper and resource within the interface, not merely through a download link. Use expandable year counts and complete lists rather than selecting a few highlights. Never cap results or silently omit unfamiliar families. Filtering changes the visible subset, not the included data.
- Branches describe research categories. Do not imply model inheritance, clinical benefit or a causal progression without supporting evidence.

## Source caveats

The earlier selected works received renewed primary-source checks, but the complete registry did not. `milestones.json` records two known title or link mismatches: `model-eeg-to-text-2022` and `method-v-learning-2015`. These records remain in the full map with visible warnings and their incorrect source hyperlinks withheld. Their links are also withheld in the XMind source-index sheet. The original registry was not silently corrected. Complete coverage is not a claim of complete source re-verification.

Registry years can refer to first-publication or issue years. Notes retain identified differences, including LSM, PaPaGei and the JITAI review. Prediction or measurement validation is not evidence of treatment benefit. IDEA and myBPmyLife retain their negative or mixed findings. Some records concern clinical or implantable-adjacent sensing rather than consumer wearables.

## Visual references

These links are design references, not evidence that all of them use the same chart structure. Third-party PDFs and images have not been copied into this repository.

- [Awesome VLA](https://github.com/yueen-ma/awesome-vla): taxonomy and named research milestones.
- [Awesome VLA and WAM](https://github.com/DravenALG/awesome-vla-wam): concise topic navigation and research entries.
- [Time series papers](https://github.com/TSCenter/awesome-time-series-papers): task and year organization.
- [World models survey](https://arxiv.org/pdf/2606.00133): Figure 1 combines classification, milestones and applications; Figure 3 separates capability comparison.
- [Robot world model survey](https://ntumars.github.io/wm-robot-survey/): compact role-based timeline and architecture explanations.

## Rebuild and preview

Run `python scripts/render_research_map.py` from the repository root to rebuild `site/research-map.html` and its coverage ledger from the template and full exported registry. Run `make test` to check registry integrity and exact map coverage. The page is self-contained and can be opened locally. The existing published editorial site in [website](../../website/) and its deployment workflow are unchanged by this handoff.

Repository-created materials use the [repository license](../../LICENSE). Linked papers, images and other third-party resources retain their own rights and access conditions.
