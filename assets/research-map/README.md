# Wearable AI design handoff

This folder gives the designer the complete research content, sources and editable drafts for the Wearable AI map. The [current English page](../../site/research-map.html) organizes **all 396 accepted records and all 45 watchlist candidates** under four research themes, with a catalog cutoff of 2026-09-02. Every record is embedded and reachable through a theme, year group or search result. The editorial classification was reviewed on 2026-10-04; this is not an October literature refresh.

## Four-theme research logic

The primary research agenda is **wearable disease prediction → intervention and counterfactuals → a personal digital twin**. **Metaverse and mixed reality** form the twin's presentation and interaction entry point, not a fourth clinical stage. The visible calendar tree grows upward; it does not imply that one paper descended from another or that all papers inevitably advance through the stages.

Every record has one primary theme plus optional cross-theme links. Each placement distinguishes direct research, supporting enablers, conceptual frameworks and adjacent work. Resource types remain independent filters. A foundation model or dataset does not itself achieve disease prediction; classifier recourse is not a treatment-effect estimate; a personalized predictor is not automatically an individual dynamic twin; an EMG interface or rendered avatar does not establish an MR personal-twin system.

The overview exposes three clickable keyword lenses per theme. Lenses overlap and do not partition the full catalog. Counts derive from reviewed families, subtopics, tags or curated IDs, not keyword hits in boilerplate limitations. Twin lenses deliberately include explicitly labelled cross-theme enablers; the Smart glasses lens contains adjacent spatial-perception and body-input resources, not six validated glasses systems. Matched labels also appear in record details and the search index.

The current primary counts are 321 prediction records, 95 intervention/counterfactual records, 2 personal-twin records and 23 MR/interface records, including watchlist and supporting resources. These are catalog placements, not counts of validated systems. The twin theme contains a framework and a diabetes-specific physiological-twin trial. MR coverage is primarily enabling and adjacent research, and the complete glasses frontier remains a visible coverage gap. Related records can be revealed through the cross-theme toggle without changing primary counts or silently duplicating the library.

## Complete research content

Use [generated/registry.json](../../generated/registry.json) for the complete accepted registry and watchlist, or [data/records](../../data/records/) for the authoritative YAML. [Taxonomy](../../data/taxonomy.yaml), [repository coverage](../../generated/coverage.md), [families](../../generated/families/index.md) and [explicit relations](../../data/relations.yaml) provide additional structure. The map uses the six native record types: 102 models, 35 measures, 61 methods, 40 interventions, 116 datasets and 42 infrastructure records. The latter includes tools, standards and published reporting guidelines, so it must not be omitted when covering papers. Not every repository record is a paper.

The [map coverage ledger](coverage.json) lists every accepted and watchlist ID with its primary theme, cross-theme links, research role, native type, original year, time group and research family. Builds fail for omitted, duplicate or unassigned IDs. Native families remain in record details and are searchable; resource types are independent filters. Watchlist records retain their publication status and inclusion reason, whether viewed alone or in the complete library.

## Map content and editable assets

| Material | Purpose |
|---|---|
| [coverage.json](coverage.json) | Complete ID-by-ID map assignment and source checksum for all 441 records. |
| [taxonomy.json](taxonomy.json) | Four research themes, research-route semantics, evidence boundaries, topics and native resource types. |
| [route-classification.json](route-classification.json) | Reproducible ID-by-ID theme placement, classification reasons and review notes; never replaces canonical metadata. |
| [four-theme-map-source.html](four-theme-map-source.html) | Current editable English overview, upward year tree, complete library, cross-theme links and evidence details. |
| [technology-radar.json](technology-radar.json) | Dated technical changes, before/after comparisons, evidence limits, sources and four-theme editorial assessments. Separate from registry acceptance. |
| [technology-radar.schema.json](technology-radar.schema.json) | Validated signal contract; methods, data, hardware, performance, products/features and new directions. |
| [preview-intelligence.jpg](preview-intelligence.jpg) | First technology-intelligence workspace screenshot. |
| [preview-four-themes.jpg](preview-four-themes.jpg) | Browser screenshot of the first four-theme overview for design review. |
| [compact-map-source.html](compact-map-source.html) | Preserved earlier native-resource-type interface, retained as a design reference only. |
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

## Technology intelligence updates

The default workspace is a compact intelligence radar; the Research map switch retains the complete upward timeline and all 441 records. Four current-state assessments sit above a dated signal list. Keywords open the original full-library lenses. Search, theme, change-type and time-window filters narrow the signals; every item opens a concise before → change → evidence → limits → implication comparison with primary-source links.

The first review is **2026-10-04**, covering selected signals and evidence baselines. The weekly filter is **2026-09-28–2026-10-04**, not an assertion that all four themes advanced that week. Publication, event and source-check dates remain distinct. A vendor-announced rollout can fall inside a review window without being independently confirmed; that distinction stays visible. An empty selection means no verified updates in this curated selection, not no activity in the entire field.

Maintain the six change types in `technology-radar.json`: methods, data, hardware, performance, products/features and new directions. A performance item must state its baseline, result and comparison conditions. Extra tools or compute must not be reported as a model-weight improvement. Preprints, peer-reviewed frameworks/trials and vendor announcements retain separate evidence labels. Announced, early-access, preordered and delivered features are not interchangeable. Product intelligence does not enter the scientific paper count; new research signals require the normal registry screening process before inclusion.

An assessment is an explicitly labelled editorial interpretation. An emerging pattern must link at least two relevant, differently dated signals, but this structural check is not proof of a scientific trend. Do not manufacture weekly entries for themes with no verified change. Keep older trials available as comparison baselines, not recirculated news. No scheduled monitoring or automatic article generation is configured by this update.

Run `python scripts/validate_technology_radar.py` to check the source contract. The renderer validates it again before publishing, including dates, unique IDs, safe source URLs, four-theme assessment coverage and valid registry references.

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

Run `python scripts/render_research_map.py` with the repository virtual environment activated to rebuild the standalone workspace, four-theme classification and coverage ledger. The classifier uses reviewed family rules and explicit contribution-based ID overrides, never keywords in generic limitations. Unreviewed families fail the build. Run `make audit` to check registry integrity, radar validation, exact map coverage and the reproducible release report. The self-contained workspace is generated identically into `site/research-map.html` and `website/research-map.html`; the latter is published by the existing Pages deployment. The designer's main presentation is retained, with an Intelligence navigation link and a research-section entry to the new workspace.

Repository-created materials use the [repository license](../../LICENSE). Linked papers, images and other third-party resources retain their own rights and access conditions.
