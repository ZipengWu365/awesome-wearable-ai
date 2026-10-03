#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter

from registry import ROOT, derive_relations, group_by, load_records, load_watchlist

FAMILY_LABELS = {
    "motion-imu-foundation-models": "Motion / IMU models and representations",
    "ppg-optical-foundation-models": "PPG and optical physiology",
    "ecg-cardiac-foundation-models": "ECG and cardiac sensing",
    "eeg-neural-foundation-models": "EEG, MEG and neural foundation models",
    "emg-neuromotor-models": "EMG and neuromotor interfaces",
    "sleep-psg-foundation-models": "Sleep and polysomnography",
    "cgm-metabolic-foundation-models": "CGM and metabolic sensing",
    "respiratory-acoustic-foundation-models": "Respiratory and acoustic sensing",
    "multimodal-physiological-models": "Multimodal physiological models",
    "sensor-language-agents": "Sensor-language models and agents",
    "general-time-series-enablers": "General time-series enablers",
}

TYPE_LABELS = {
    "model": "Models and representation systems",
    "dataset": "Datasets, cohorts and benchmarks",
    "method": "Causal, counterfactual and adaptive-policy methods",
    "measure": "Digital measures and computational phenotypes",
    "intervention": "Adaptive interventions and closed-loop systems",
    "infrastructure": "Tools, platforms, standards and guidance",
}


def md_link(title: str, url: str) -> str:
    return f"[{title}]({url})"


def record_table(rows: list[dict], limit: int = 12) -> str:
    rows = sorted(rows, key=lambda row: (-int(row["year"]), row["title"].lower()))[:limit]
    lines = [
        "| Resource | Year | Venue/source | Family | Evidence boundary |",
        "|---|---:|---|---|---|",
    ]
    for row in rows:
        boundary = row["evidence_boundary"].replace("|", "/")
        lines.append(
            f"| {md_link(row['title'], row['primary_url'])} | {row['year']} | "
            f"{row['venue']} | `{row['family']}` | {boundary} |"
        )
    return "\n".join(lines)


def main() -> int:
    records = load_records()
    watchlist = load_watchlist()
    relations = derive_relations(records)
    counts = Counter(record["record_type"] for record in records)
    family_counts = Counter(record["family"] for record in records)
    verification = Counter(record["verification_status"] for record in records)
    evidence_depth = Counter(record["evidence_depth"] for record in records)
    by_type = group_by(records, "record_type")
    negative_interventions = sum(
        bool(record.get("negative_or_null_result"))
        for record in by_type.get("intervention", [])
    )
    foundation_tagged = sum(
        "foundation-model" in record.get("tags", [])
        for record in by_type.get("model", [])
    )

    lines = [
        '<div align="center">',
        "",
        "# Awesome Wearable AI",
        "",
        "**An evidence-aware, machine-readable atlas of wearable and body-sensed intelligence—from sensing and representation learning to causal reasoning, adaptive interventions and closed-loop health systems.**",
        "",
        "**Website:** [https://zipengwu365.github.io/awesome-wearable-ai/](https://zipengwu365.github.io/awesome-wearable-ai/)",
        "",
        "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        "[![Registry CI](https://github.com/ZipengWu365/awesome-wearable-ai/actions/workflows/validate.yml/badge.svg)](https://github.com/ZipengWu365/awesome-wearable-ai/actions/workflows/validate.yml)",
        f"[![Accepted](https://img.shields.io/badge/accepted-{len(records)}-1f6feb)](generated/statistics.json)",
        f"[![Models](https://img.shields.io/badge/models-{counts.get('model', 0)}-8250df)](data/records/models.yaml)",
        f"[![Watchlist](https://img.shields.io/badge/watchlist-{len(watchlist)}-b7791f)](data/excluded/watchlist.yaml)",
        "[![Version](https://img.shields.io/badge/version-v0.3.0-4c1)](CHANGELOG.md)",
        "",
        "**Models · Datasets · Digital Measures · Causal Methods · JITAIs · Closed-loop Systems · Standards**",
        "",
        "</div>",
        "",
        "Research map: [full-repository interactive timeline](site/research-map.html) · [designer handoff and editable assets](assets/research-map/README.md). Every accepted record and watchlist candidate is included, with an [ID-by-ID coverage ledger](assets/research-map/coverage.json), expandable year groups and complete search results.",
        "",
        "> **Scope and evidence rule.** Scientific entries must appear in the explicit venue whitelist: SCI/SCIE journals, explicitly whitelisted top journals, top conferences, or domain-leading archival conferences. Official technical reports from major research organizations are allowed. Canonical datasets, standards and research tools use separate official-resource criteria. Pure preprints, workshop-only papers, unresolved publication claims and borderline venues remain in a visible watchlist and are excluded from headline counts.",
        "",
        "## What changed in v0.3.0",
        "",
        f"The earlier package contained only a small seed registry. This release rebuilds the project around **{len(records)} accepted records**, **{len(watchlist)} screened watchlist candidates**, and **{len(relations)} machine-derived or explicit relations**. Counts are generated from the YAML source files during every build; they are not manually typed marketing figures.",
        "",
        "## Registry at a glance",
        "",
        "| Record type | Accepted records |",
        "|---|---:|",
    ]
    for key in TYPE_LABELS:
        lines.append(f"| {TYPE_LABELS[key]} | {counts.get(key, 0)} |")

    lines.extend([
        "",
        f"> The **{counts.get('model', 0)} model records are not claimed to be {counts.get('model', 0)} foundation models**. They include {foundation_tagged} records explicitly tagged as foundation-model work, plus leading self-supervised representations, sensor-language systems, cross-dataset models and wearable control interfaces. This distinction prevents count inflation through terminology drift.",
        "",
        "### Curation depth",
        "",
        "| Evidence depth | Records | Interpretation |",
        "|---|---:|---|",
        f"| `evidence_card` | {evidence_depth.get('evidence_card', 0)} | Contribution, limitation and claim boundary were curated from a primary or canonical source. |",
        f"| `metadata_verified` | {evidence_depth.get('metadata_verified', 0)} | Core metadata and scope were checked; full methodological appraisal remains pending. |",
        f"| `venue_verified` | {evidence_depth.get('venue_verified', 0)} | Bibliographic and venue eligibility were screened; treat as an index record, not a completed evidence appraisal. |",
        "",
        "### Source-verification status",
        "",
        "| Verification status | Records |",
        "|---|---:|",
    ])
    for key, value in sorted(verification.items()):
        lines.append(f"| `{key}` | {value} |")

    lines.extend([
        "",
        "## Navigate by research question",
        "",
        "- **Which sensor model should I start from?** Read the [model landscape](docs/MODEL_LANDSCAPE.md) and browse [model-family pages](generated/families/index.md).",
        "- **Which dataset can support external validation or population modelling?** Use the [dataset registry](data/records/datasets.yaml), [coverage report](generated/coverage.md), or searchable site.",
        "- **What can a wearable-derived association legitimately support?** Consult the [Evidence Guide](docs/EVIDENCE_GUIDE.md); association, prediction, causal effect, policy value and clinical utility are separate claim layers.",
        "- **How should counterfactual or personalized intervention questions be formulated?** Use the [counterfactual and intervention map](docs/COUNTERFACTUAL_AND_INTERVENTION_MAP.md).",
        "- **How was this literature located and screened?** See the reproducible [search strategy](docs/SEARCH_STRATEGY.md), [inclusion policy](docs/INCLUSION_POLICY.md) and transparent [watchlist](data/excluded/watchlist.yaml).",
        "",
        "## Wearable AI lifecycle",
        "",
        "```text",
        "Sensing and acquisition",
        "        ↓",
        "Signal quality, calibration and cross-device harmonisation",
        "        ↓",
        "Representation learning and foundation models",
        "        ↓",
        "Digital measures and computational phenotypes",
        "        ↓",
        "Prediction, monitoring and prognosis",
        "        ↓",
        "Causal identification and counterfactual reasoning",
        "        ↓",
        "Policy learning and adaptive intervention design",
        "        ↓",
        "Closed-loop delivery, clinical utility, safety and governance",
        "```",
        "",
        "## Sensor and model landscape",
        "",
        "A single `sensor model` category hides major differences in signal physics, annotation, time scale, supervision and clinical use. The registry currently separates eleven model families:",
        "",
        "| Family | Count |",
        "|---|---:|",
    ])
    for family, label in FAMILY_LABELS.items():
        lines.append(f"| {label} | {family_counts.get(family, 0)} |")

    lines.extend([
        "",
        record_table(by_type.get("model", []), 18),
        "",
        "The README shows only recent representative records. The complete source of truth is [models.yaml](data/records/models.yaml), and every accepted family receives a generated page under [generated/families](generated/families/index.md).",
        "",
        "## Adaptive intervention and closed-loop evidence",
        "",
        f"The intervention registry contains **{counts.get('intervention', 0)} accepted records**, including **{negative_interventions} records explicitly marked as negative, null or materially mixed**. Protocols, proximal-effect analyses, randomized clinical outcomes and deployed closed-loop systems are kept distinct. A protocol is not effectiveness evidence; a model counterfactual is not a causal treatment effect.",
        "",
        record_table(by_type.get("intervention", []), 18),
        "",
        "## Counterfactual reasoning: four non-equivalent meanings",
        "",
        "| Layer | Question | Evidence required |",
        "|---|---|---|",
        "| Predictive counterfactual | What input change flips a model output? | Model-behaviour validation; no treatment-effect claim. |",
        "| Causal counterfactual | What would happen under a different action? | Identification assumptions, randomization, or defensible causal design. |",
        "| Policy counterfactual | What would a different sequential policy achieve? | Online trial or reliable off-policy evaluation with overlap and uncertainty checks. |",
        "| Generative / digital-twin counterfactual | Can an individual trajectory be simulated under intervention? | Calibration, interventional validity, external validation and prospective utility evidence. |",
        "",
        "## Machine-readable structure",
        "",
        "```text",
        "data/records/          # accepted source-of-truth records",
        "data/excluded/         # transparent watchlist and exclusion reasons",
        "data/venues.yaml       # venue and source eligibility policy",
        "data/concepts.yaml     # controlled vocabularies",
        "data/relations.yaml    # explicit cross-record links",
        "schema/                # JSON Schemas",
        "generated/             # JSON, CSV, statistics, family pages and coverage",
        "site/                  # dependency-free searchable atlas",
        "scripts/               # validation, export, rendering, audit and site generation",
        "```",
        "",
        "Build locally:",
        "",
        "```bash",
        "python -m pip install -r requirements.txt",
        "make build",
        "make test",
        "make audit",
        "```",
        "",
        "## Coverage boundary",
        "",
        "This release is intentionally broad but does **not** claim PRISMA-level exhaustive retrieval. It prioritizes source quality and transparent curation depth. Known gaps, unresolved venues and candidate preprints are documented in [COVERAGE_LIMITS.md](docs/COVERAGE_LIMITS.md) and [watchlist.yaml](data/excluded/watchlist.yaml). Venue prestige is an inclusion filter, not evidence of clinical validity.",
        "",
        "## Contributing",
        "",
        "Use the issue templates or submit a PR. Every scientific proposal must provide a version-of-record URL, venue, year, inclusion basis, concise contribution, limitation and evidence boundary. Watchlist promotion requires resolving the recorded exclusion reason. See [CONTRIBUTING.md](CONTRIBUTING.md).",
        "",
        "## Citation and license",
        "",
        "Please cite the original papers, datasets and standards directly. Repository citation metadata are in [CITATION.cff](CITATION.cff). Repository code and text use [LICENSE](LICENSE); linked resources retain their own licenses and access conditions.",
    ])
    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("README rendered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
