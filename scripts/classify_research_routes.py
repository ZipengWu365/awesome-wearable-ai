#!/usr/bin/env python3
"""Build an evidence-aware editorial route layer without changing the registry.

The four routes describe the user's research questions, not resource types or a
claim that every paper has achieved the final capability. Family rules cover
reusable enablers; reviewed ID overrides handle mixed families and edge cases.
Only titles, stated contributions, and curated overrides drive assignments.
Boilerplate limitations, a model's name, and the word "personalized" alone do not.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "generated" / "registry.json"
OUTPUT_PATH = ROOT / "assets" / "research-map" / "route-classification.json"
ROUTES = ("prediction", "intervention", "twin", "interface")
ROLES = ("direct", "support", "framework", "adjacent")
REVIEW_DATE = "2026-10-04"


def rule(primary: str, role: str, subtopic: str, reason: str,
         secondary: tuple = (), note: str = "", needs_review: bool = False) -> dict:
    return {
        "primary_route": primary,
        "secondary_routes": list(secondary),
        "route_role": role,
        "subtopic": subtopic,
        "classification_reason": reason,
        "review_note": note,
        "needs_review": needs_review,
    }


FAMILY_RULES = {}


def families(names: str, primary: str, role: str, subtopic: str, reason: str,
             secondary: tuple = (), note: str = "") -> None:
    for name in names.split():
        if name in FAMILY_RULES:
            raise ValueError(f"Duplicate family rule: {name}")
        FAMILY_RULES[name] = rule(primary, role, subtopic, reason, secondary, note)


families(
    "ecg-cardiac-foundation-models ppg-optical-foundation-models cgm-metabolic-foundation-models",
    "prediction", "support", "Cardiac & metabolic models",
    "Signal pretraining and reusable representations support health estimation; a foundation model is not itself an individualized simulator or a proven intervention.",
)
families(
    "eeg-neural-foundation-models sleep-psg-foundation-models respiratory-acoustic-foundation-models",
    "prediction", "support", "Brain, sleep & respiratory models",
    "Representation learning supports physiological state analysis; transfer benchmarks do not alone establish prospective disease prediction or a personal twin.",
)
families(
    "motion-imu-foundation-models",
    "prediction", "support", "Activity & behavior models",
    "Wearable motion representations and activity recognition are upstream sensing capabilities, not causal treatment evidence or an implemented personal twin.",
)
families(
    "multimodal-physiological-models",
    "prediction", "support", "Multimodal physiological models",
    "Multisignal representation learning supports health-state estimation; fusion or personalization alone does not establish a dynamic personal twin.",
)
families(
    "sensor-language-agents",
    "prediction", "support", "Sensor-language & health reasoning",
    "Grounding language in sensor observations supports interpretation of personal data; text alignment and fluent health reports are not validated intervention reasoning or personal twins.",
)
families(
    "general-time-series-enablers",
    "prediction", "support", "General forecasting enablers",
    "General time-series modelling is a transferable methodological resource; its inclusion does not demonstrate wearable disease prediction without a task-specific evaluation.",
)
families(
    "har-benchmarks free-living-human-sensing affect-stress-datasets population-scale-cohorts "
    "ppg-cardiac-datasets eeg-sleep-datasets metabolic-cgm-datasets multimodal-clinical-waveforms",
    "prediction", "support", "Datasets & longitudinal cohorts",
    "A dataset or cohort provides sensing and evaluation infrastructure; its availability is not evidence that a predictive, causal, or twin capability has been achieved.",
)
families(
    "activity-and-population-risk-measures aging-and-circadian-measures cardiac-risk-and-aging-measures "
    "frailty-and-mobility-measures neurological-and-motor-measures mental-health-and-stress-measures "
    "metabolic-and-glucose-measures pregnancy-and-reproductive-measures infection-and-recovery-measures "
    "sleep-and-circadian-measures",
    "prediction", "support", "Disease risk & digital biomarkers",
    "Digital measures, longitudinal descriptions, or observational associations support the prediction route; an association is not a treatment effect or a calibrated individual future simulator.",
)
families(
    "cardiac-rhythm-measures",
    "prediction", "support", "Disease screening & monitoring",
    "Rhythm detection and monitoring identify existing disease-related states; they are upstream evidence for the prediction route, not future disease forecasts or intervention-effect estimates.",
)
families(
    "digital-measure-frameworks",
    "prediction", "framework", "Biomarker evaluation frameworks",
    "A perspective or review organizes measurement and validation; it does not implement or validate a new patient-level predictive system.",
)
families(
    "missingness-calibration-and-sensor-bias privacy-fairness-and-transportability",
    "prediction", "support", "Signal quality & trustworthy models",
    "Calibration, missing-data handling, privacy, and bias analysis support reliable wearable measurements and models; these methods do not themselves achieve a clinical endpoint.",
)
families(
    "biosignal-processing biosignal-io wearable-signal-processing sleep-analysis time-series-tooling "
    "time-series-feature-engineering data-platforms benchmarking-and-evaluation wearable-hardware-and-edge",
    "prediction", "support", "Tools, platforms & evaluation",
    "Acquisition, processing, software, or benchmark infrastructure supports sensing and modelling; a tool or platform is not itself a predictive, causal, or digital-twin result.",
)
families(
    "commercial-platform-apis mobile-health-platforms interoperability",
    "prediction", "support", "Personal-data infrastructure",
    "Data collection, integration, or application infrastructure enables longitudinal personal systems; it is not evidence of a disease predictor or an implemented twin.",
    ("intervention", "twin"),
)
families(
    "regulatory-guidance reporting-guidelines ethics-and-governance digital-measure-evaluation",
    "prediction", "support", "Validation, safety & governance",
    "Reporting, validation, safety, and governance resources constrain claims across the research pathway; they are not studies demonstrating a new wearable capability.",
    ("intervention", "twin"),
)
families(
    "causal-identification-foundations causal-discovery-and-invariance",
    "intervention", "support", "Causal identification",
    "Causal methodology supports reasoning about actions under explicit identification assumptions; generic methodological evidence does not establish the effect of a particular wearable intervention.",
    ("twin",),
)
families(
    "longitudinal-counterfactual-models",
    "intervention", "support", "Longitudinal counterfactuals",
    "Treatment-response estimation over time supports intervention reasoning; a conditional counterfactual model is not automatically a continuously updated individual digital twin.",
    ("twin",),
)
families(
    "counterfactual-explanations-and-recourse",
    "intervention", "support", "Predictive recourse",
    "Classifier recourse describes changes that alter a model prediction; such predictive counterfactuals must not be presented as verified causal treatment effects.",
)
families(
    "adaptive-treatment-and-policy-learning off-policy-evaluation",
    "intervention", "support", "Policy learning & evaluation",
    "Policy learning or off-policy evaluation supports sequential decisions under study-specific assumptions; a generic algorithm is not a prospectively validated wearable intervention.",
)
families(
    "micro-randomized-trial-methods",
    "intervention", "support", "Adaptive trials & JITAI",
    "Micro-randomized designs and estimators support evaluation of time-varying intervention effects; a design paper alone does not establish an effective deployed intervention.",
)
families(
    "jitai-behavioral-interventions ai-coaching-and-adaptive-messaging remote-monitoring-and-clinical-escalation "
    "digital-screening-and-clinical-escalation workplace-behavior-feedback wearable-feedback-randomized-trials",
    "intervention", "direct", "Adaptive health interventions",
    "The stated contribution evaluates an intervention or feedback pathway rather than only predicting a state; findings are limited to the tested intervention package and study population.",
)
families(
    "automated-insulin-delivery closed-loop-sleep-interventions",
    "intervention", "direct", "Closed-loop physiological control",
    "Sensing-linked physiological control or stimulation is the main contribution; closed-loop operation alone does not imply an individual digital twin or unrestricted counterfactual validity.",
)
families(
    "responsive-neurostimulation adaptive-neurorehabilitation closed-loop-and-home-neuromodulation",
    "intervention", "adjacent", "Neurostimulation & rehabilitation",
    "Neural stimulation or rehabilitation studies inform sensing-linked intervention, but implanted or body-sensed clinical systems are adjacent to consumer wearable AI and need separate scope labels.",
)
families(
    "digital-rehabilitation-and-pain adaptive-rehabilitation-and-exercise wearable-robotics-and-assistance",
    "intervention", "direct", "Rehabilitation & assistance",
    "The main contribution evaluates a therapeutic, rehabilitation, or assistive intervention; a personalized controller does not by itself establish a digital twin.",
)
families(
    "wearable-feedback-evidence-synthesis",
    "intervention", "support", "Intervention evidence synthesis",
    "Reviews synthesize intervention outcomes and limitations; they are evidence resources, not new implemented algorithms or primary intervention trials.",
)
families(
    "egocentric-multimodal-datasets",
    "interface", "support", "First-person & spatial intelligence",
    "First-person and multimodal activity data enable scene-aware interfaces; the dataset itself does not implement mixed reality, a metaverse entry, or a personal twin.",
    note="Adjacent enabling data: do not label the dataset as a demonstrated smart-glasses or twin system.",
)
families(
    "emg-neuromotor-datasets",
    "interface", "support", "Neuromotor & neural interfaces",
    "Muscle-signal gesture, pose, or typing data support body-based input interfaces; they are not demonstrations of a mixed-reality personal twin.",
    note="Adjacent interface-enabling data; task-specific MR integration is not established by this resource.",
)
families(
    "emg-neuromotor-models",
    "interface", "adjacent", "Neuromotor & neural interfaces",
    "The contribution concerns wearable intention decoding or human-computer input; it is relevant interface technology, not proof of a mixed-reality or metaverse twin system.",
)
families(
    "assistive-wearable-systems",
    "interface", "adjacent", "Assistive perception & interaction",
    "Multimodal wearable perception and feedback support interaction with the real world; assistive feasibility is not evidence of a metaverse or personal-twin implementation.",
    ("intervention",),
)
families(
    "frontier-frameworks",
    "prediction", "framework", "Full-stack wearable frameworks",
    "A full-stack wearable review or framework connects sensing, AI, and personalized interaction; it does not demonstrate a deployed personal twin.",
    ("intervention", "twin", "interface"),
)


OVERRIDES = {
    # Only explicit twin frameworks and individual dynamic simulation occupy
    # the primary twin route. Other personal-data methods remain enablers.
    "method-causal-digital-twins-2026": rule(
        "twin", "framework", "Causal twin frameworks",
        "Proposes a causal digital-twin framework combining structural causal models, potential outcomes, and sequential decisions; it does not report prospective validation of a deployed personal twin.",
        ("intervention",),
        "Conceptual and methodological framework, not an implemented or clinically validated whole-person twin.",
    ),
    "intervention-aid-digital-twin-coadaptation-2025": rule(
        "twin", "direct", "Individual physiological simulation",
        "Studies individual physiological digital-twin-supported human-machine adaptation for automated insulin delivery; the empirical scope is a diabetes intervention, not a general personal or metaverse twin.",
        ("intervention",),
        "Narrow physiological twin demonstrated within the trial context. Do not generalize to unrestricted individual treatment effects. The source registry's implantable scope label needs checking for this CGM/pump study.",
        True,
    ),
    "watch-jitai-diffusion-twins-2026": rule(
        "intervention", "adjacent", "Subpopulation intervention simulation",
        "The title describes a subpopulation diffusion simulator for HeartSteps deployment; population simulation may support intervention research but is not an individual continuously updated twin.",
        ("twin",),
        "Subpopulation, not individual, twin; watchlist metadata alone does not establish implementation quality or clinical benefit.",
        True,
    ),
    "method-synctwin-2021": rule(
        "intervention", "support", "Longitudinal counterfactuals",
        "Constructs synthetic comparison units to estimate longitudinal treatment effects; the name SyncTwin does not mean a persistent person-specific physiological digital twin.",
        ("twin",),
        "Synthetic-control twin is a methodological enabler, not an implemented personal twin.",
    ),
    "model-personalized-physio-adaptation-2025": rule(
        "prediction", "support", "Individual adaptation",
        "Studies parameter-efficient adaptation of physiological representations to individuals; this is a personalization component, not a dynamically updated simulator of the person.",
        ("twin",),
    ),
    "model-personal-health-insights-agent-2026": rule(
        "prediction", "support", "Personal health interpretation",
        "Evaluates an agent workflow for analysing longitudinal wearable summaries; personal-data reasoning is a potential twin interface or analytical component, not an implemented individual digital twin.",
        ("twin",),
    ),
    "model-ph-llm-2025": rule(
        "prediction", "support", "Personal health interpretation",
        "Studies language-model adaptation and evaluation for reasoning over personal wearable data; personalized health language does not establish causal intervention effects or a dynamic personal twin.",
        ("twin",),
        "Source identity requires review: the registry retains a preprint-style title and journal URL that may not identify the corresponding final sleep-and-fitness-coaching paper. No canonical metadata is changed here.",
        True,
    ),
    "watch-physiollm-2024": rule(
        "prediction", "support", "Personal health interpretation",
        "The title concerns personalized insights from wearables and language models; an insight assistant is an enabler, not an individual dynamic digital twin.",
        ("twin",),
    ),
    "watch-conversational-health-agents-2024": rule(
        "prediction", "support", "Personal health interpretation",
        "The title describes personalized conversational health agents; conversational personalization is not sufficient evidence of causal simulation or a digital twin.",
        ("twin",),
    ),
    # Prediction and monitoring are kept distinct from causal effects.
    "model-sleepfm-clinical-2026": rule(
        "prediction", "direct", "Disease prediction",
        "The stated task is disease prediction from multimodal sleep signals; predictive evaluation does not demonstrate intervention effects or an individualized simulator.",
    ),
    "model-insulin-resistance-wearables-2026": rule(
        "prediction", "direct", "Disease risk estimation",
        "Predicts insulin resistance using wearable measurements and blood biomarkers; the target is a health-state estimate, not the causal effect of changing behavior or treatment.",
    ),
    "model-health-llm-2024": rule(
        "prediction", "direct", "Health prediction from sensor summaries",
        "Evaluates health prediction from structured wearable summaries using language models; it does not establish causal intervention reasoning or an individual twin.",
    ),
    "measure-mood-episode-prediction-2024": rule(
        "prediction", "direct", "Disease episode prediction",
        "Predicts next-day mood episodes using personalized sleep and circadian features; personalization of a predictor is not a personal digital twin.",
    ),
    "measure-prediabetes-glycemic-control-2021": rule(
        "prediction", "direct", "Future glycemic-control prediction",
        "Tests whether wearable activity patterns predict changes in HbA1c; prediction of change does not identify the effect of an activity intervention.",
    ),
    "measure-cosinorage-2024": rule(
        "prediction", "direct", "Aging & outcome risk estimation",
        "Evaluates a wearable circadian aging measure against mortality and incident disease outcomes across cohorts; outcome associations do not identify the effect of altering the circadian measure.",
    ),
    "measure-brain-health-review-2026": rule(
        "prediction", "framework", "Brain-health biomarker synthesis",
        "Synthesizes passive wearable measures for brain health; a review is not a new validated predictor or implemented personal twin.",
    ),
    "measure-covid-presymptomatic-2020": rule(
        "prediction", "direct", "Early disease warning",
        "Uses deviations from an individual's wearable baseline to detect changes around infection; early warning and baseline personalization do not establish a dynamic twin or causal treatment effect.",
    ),
    # Explicit interface contributions in otherwise health-oriented families.
    "model-sing-wearables-2025": rule(
        "interface", "adjacent", "Spatial speech interaction",
        "Combines direction-of-arrival sensing, speech embeddings, and a language model for spatially aware wearable interaction; no personal-twin or metaverse implementation is established.",
    ),
    "model-full-body-haptic-network-2025": rule(
        "interface", "adjacent", "Body tracking & haptics",
        "Integrates body motion tracking and haptic feedback into an interactive wearable network; body representation and feedback are not a validated physiological or whole-person twin.",
    ),
    "model-neuript-2025": rule(
        "interface", "support", "Neuromotor & neural interfaces",
        "Develops transferable neural-interface representations; it is adjacent input-decoding infrastructure, not a demonstrated mixed-reality entry or personal twin.",
        ("prediction",),
    ),
    "model-labram-2024": rule(
        "interface", "support", "Neuromotor & neural interfaces",
        "Pretrains generic EEG representations for BCI transfer; neural-interface enabling evidence does not demonstrate an MR interaction system or personal twin.",
        ("prediction",),
    ),
    "model-belt2-2024": rule(
        "interface", "adjacent", "Neural-language decoding",
        "Aligns EEG and language representations for brain decoding; this is adjacent neural communication research rather than a deployed wearable MR or metaverse twin interface.",
        ("prediction",),
    ),
    "model-eeg-to-text-2022": rule(
        "interface", "adjacent", "Neural-language decoding",
        "The stated task decodes EEG into text; neural-language decoding is adjacent interaction research, not a personal-twin implementation.",
        (),
        "Known source-link issue in the existing map: retain the record but do not treat the listed source as verified evidence until corrected.",
        True,
    ),
    "model-eeg-language-alignment-2023": rule(
        "prediction", "support", "Neural-language representations",
        "Studies representational alignment between EEG and language; this does not by itself implement a usable neural-input interface or personal twin.",
        ("interface",),
    ),
    "model-neurolm-2025": rule(
        "prediction", "support", "Neural-language representations",
        "Connects EEG representations with language across decoding tasks; generic multi-task alignment is a shared enabler, not itself a validated MR interface or personal twin.",
        ("interface",),
    ),
    "model-eeg-eye-llm-2024": rule(
        "prediction", "support", "Neural-state estimation",
        "Classifies word-level neural states during reading using EEG, eye tracking, and language representations; eye tracking alone does not make this a mixed-reality input system.",
        ("interface",),
    ),
    "model-holollm-2025": rule(
        "interface", "adjacent", "Multisensory scene understanding",
        "Aligns LiDAR, infrared, radar, and Wi-Fi sensing with language for human-sensing reasoning; environmental sensing is adjacent spatial intelligence, not a verified smart-glasses personal twin.",
        ("prediction",),
    ),
    "model-sensor2text-2024": rule(
        "prediction", "support", "Sensor-language & health reasoning",
        "Maps wearable activity observations to language for interactive tracking; descriptive language interaction does not demonstrate a metaverse entry or dynamic personal twin.",
        ("interface",),
    ),
    "model-hybrid-emg-eeg-rehab-2025": rule(
        "intervention", "adjacent", "Intention-aware rehabilitation control",
        "Uses EMG and EEG intention detection to adapt an elbow rehabilitation controller under fatigue; this is an adjacent rehabilitation-control system, not an MR or personal-twin implementation.",
        ("interface",),
    ),
    "dataset-eeg-motor-imagery": rule(
        "interface", "support", "Neuromotor & neural interfaces",
        "Motor execution and imagery EEG support neural-input decoding; benchmark data do not demonstrate a usable MR entry or personal twin.",
        ("prediction",),
    ),
    "dataset-bci-competition-iv-2a": rule(
        "interface", "support", "Neuromotor & neural interfaces",
        "A motor-imagery BCI dataset supports input-decoding research, not a demonstrated mixed-reality or personal-twin system.",
        ("prediction",),
    ),
    "dataset-moabb": rule(
        "interface", "support", "Neuromotor & neural interfaces",
        "BCI benchmarking data and aggregation support neural-interface comparison; infrastructure is not evidence of a metaverse or personal-twin capability.",
        ("prediction",),
    ),
    "infra-moabb": rule(
        "interface", "support", "Neuromotor & neural interfaces",
        "BCI benchmarking software supports neural-input evaluation; it is not itself a demonstrated wearable MR interface or personal twin.",
        ("prediction",),
    ),
    "watch-cet-mae-2024": rule(
        "interface", "adjacent", "Neural-language decoding",
        "The title concerns EEG-to-text representation transfer; this is adjacent neural communication research, not a demonstrated MR or metaverse twin system.",
    ),
    "watch-zero-shot-trajectory-llm-2024": rule(
        "prediction", "support", "Trajectory interpretation",
        "The title concerns trajectory tracing using language models; location inference is not enough to establish an MR interaction system or personal twin.",
        ("interface",),
    ),
    # VR trial evidence belongs to intervention first, not an MR-entry claim.
    "intervention-reverie-vr-sports-2025": rule(
        "intervention", "direct", "VR-assisted health intervention",
        "Evaluates adaptive VR exercise in a randomized trial; VR is the intervention medium, not evidence of an MR-glasses personal-twin entry.",
        ("interface",),
    ),
    "intervention-vr-chronic-pain-2025": rule(
        "intervention", "direct", "VR-assisted health intervention",
        "Evaluates a telehealth VR pain intervention using a crossover design; intervention outcomes do not establish a metaverse or personal-twin interface.",
        ("interface",),
    ),
    "intervention-brain-spine-interface-2023": rule(
        "intervention", "adjacent", "Neural rehabilitation control",
        "Links cortical decoding to spinal stimulation for walking assistance; an implanted clinical neural interface is adjacent to wearable AI and does not demonstrate an MR or personal-twin entry.",
        ("interface",),
        "Do not infer randomization or population-level benefit from generic intervention boilerplate.",
    ),
    "intervention-closed-loop-depression-2021": rule(
        "intervention", "adjacent", "Individual closed-loop neurostimulation",
        "Demonstrates biomarker-triggered intracranial stimulation in one participant; individualized closed-loop control is not a personal digital twin or a population-level randomized result.",
        note="Single-participant implanted clinical system; preserve its study-specific evidence boundary.",
    ),
    "method-heartsteps-mrt-2019": rule(
        "intervention", "direct", "Adaptive trials & JITAI",
        "Tests the effects of contextually tailored activity suggestions in a micro-randomized optimization trial; it evaluates an intervention, rather than only proposing a trial design.",
    ),
    "method-jitai-annual-review-2026": rule(
        "intervention", "framework", "Adaptive-intervention synthesis",
        "Reviews the state and next steps of just-in-time adaptive interventions; the review is not itself a newly validated intervention policy.",
    ),
    "method-causal-counterfactual-prediction-2020": rule(
        "intervention", "framework", "Causal actionability framework",
        "Organizes the causal and counterfactual requirements for actionable healthcare; it is a methodological framework rather than proof of a particular wearable intervention's effect.",
        ("twin",),
    ),
    "method-v-learning-2015": rule(
        "intervention", "support", "Policy learning & evaluation",
        "Dynamic treatment-policy learning is a methodological enabler; source identity must be resolved before citing this particular registry entry as evidence.",
        note="Known source-link issue in the existing map; no canonical record is removed or rewritten by this classification.",
        needs_review=True,
    ),
    "infra-consort-ai-2020": rule(
        "intervention", "support", "Trial reporting & validation",
        "Reporting guidance for AI intervention trials constrains evaluation claims; it is not an implemented intervention or new treatment-effect result.",
        ("prediction", "twin"),
    ),
    "infra-spirit-ai-2020": rule(
        "intervention", "support", "Trial reporting & validation",
        "Protocol-reporting guidance supports AI intervention study design; a guideline does not demonstrate predictive, causal, or twin capability.",
        ("prediction", "twin"),
    ),
    "watch-human-symbiotic-health-intelligence-2025": rule(
        "prediction", "framework", "Full-stack wearable frameworks",
        "The watchlist title and review tags describe full-stack integration from materials to personalized interaction; this is a broad framework, not a validated personal digital twin.",
        ("intervention", "twin", "interface"),
        "Review/framework adjacency must not be counted as an implemented twin or MR-glasses system.",
    ),
}


def classify_record(record: dict) -> dict:
    """Return one assignment; raise on unsupported inputs instead of hiding gaps."""
    record_id = record.get("id")
    family = record.get("family") or record.get("proposed_family")
    if not isinstance(record_id, str) or not record_id:
        raise ValueError("A route assignment requires a nonempty record ID")
    if not isinstance(family, str) or not family:
        raise ValueError(f"Missing classification family for {record_id}")
    if record_id in OVERRIDES:
        assignment = copy.deepcopy(OVERRIDES[record_id])
        basis = "Registry title and stated contribution; curated ID-level editorial override"
    elif family in FAMILY_RULES:
        assignment = copy.deepcopy(FAMILY_RULES[family])
        basis = f"Registry title, stated contribution, and reviewed family rule: {family}"
    else:
        raise ValueError(f"Unreviewed research family {family!r} for {record_id}")
    is_watchlist = "proposed_family" in record and "record_type" not in record
    notes = [assignment["review_note"]] if assignment["review_note"] else []
    if is_watchlist:
        assignment["needs_review"] = True
        notes.append(
            "Provisional watchlist assignment based on title and proposed family. "
            "Publication status and article-level contribution require review; no promotion to the accepted corpus is implied."
        )
        basis = basis.replace("stated contribution", "proposed family")
    elif record.get("wearable_scope") in {"cross-domain-enabler", "body-sensed-adjacent", "mobile-health-enabler"}:
        notes.append(f"Source scope: {record['wearable_scope']}; relevance does not establish a consumer-wearable implementation.")
    assignment["review_note"] = " ".join(notes)
    assignment["classification_basis"] = basis
    assignment["id"] = record_id
    assignment["catalog_status"] = "watchlist" if is_watchlist else "accepted"
    if assignment["primary_route"] not in ROUTES or assignment["route_role"] not in ROLES:
        raise ValueError(f"Invalid route or role for {record_id}")
    secondary = assignment["secondary_routes"]
    if (len(secondary) != len(set(secondary)) or assignment["primary_route"] in secondary
            or any(route not in ROUTES for route in secondary)):
        raise ValueError(f"Invalid secondary routes for {record_id}")
    return assignment


def build_classification(registry: dict) -> dict:
    """Map every accepted and watchlist ID exactly once without mutating it."""
    originals = list(registry["records"]) + list(registry["watchlist"])
    ids = [record["id"] for record in originals]
    if len(ids) != len(set(ids)):
        raise ValueError("Registry IDs must be unique across accepted and watchlist records")
    assignments = [classify_record(record) for record in originals]
    for source_key, status in (("records", "accepted"), ("watchlist", "watchlist")):
        actual_ids = {row["id"] for row in assignments if row["catalog_status"] == status}
        if actual_ids != {row["id"] for row in registry[source_key]}:
            raise ValueError(f"Source records have inconsistent {status} status fields")
    assignments.sort(key=lambda row: row["id"])
    counts = {}
    for route in ROUTES:
        rows = [row for row in assignments if row["primary_route"] == route]
        counts[route] = {
            "total": len(rows),
            "accepted": sum(row["catalog_status"] == "accepted" for row in rows),
            "watchlist": sum(row["catalog_status"] == "watchlist" for row in rows),
            "by_role": {role: sum(row["route_role"] == role for row in rows) for role in ROLES},
            "secondary_mentions": sum(route in row["secondary_routes"] for row in assignments),
        }
    fingerprint = hashlib.sha256(
        json.dumps(registry, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "classification_version": "1.0.0",
        "editorial_review_date": REVIEW_DATE,
        "source_registry_version": registry["version"],
        "source_registry_cutoff": registry["generated_on"],
        "source_registry_sha256": fingerprint,
        "scope": "All existing accepted and watchlist records; not a claim of complete field coverage or an October literature update.",
        "method": "Reviewed family rules with explicit contribution-based ID overrides; no keyword inference from boilerplate limitations; no canonical registry edits.",
        "role_definitions": {
            "direct": "Directly studies the route question in its stated scope; not a blanket claim of maturity, causal validity, or clinical benefit.",
            "support": "Foundational methods, data, tools, measurements, or components; does not itself achieve the route's final capability.",
            "framework": "Conceptual framework, perspective, or synthesis; distinguished from an implemented and validated system.",
            "adjacent": "Related setting or enabling technology outside the target capability; for example an EMG interface is not automatically an MR personal-twin system.",
        },
        "counts": counts,
        "total_records": len(assignments),
        "needs_review_ids": [row["id"] for row in assignments if row["needs_review"]],
        "records": assignments,
    }


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    document = build_classification(registry)
    OUTPUT_PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Mapped {document['total_records']} records to {OUTPUT_PATH.relative_to(ROOT)}")
    for route, count in document["counts"].items():
        print(f"{route}: {count['accepted']} accepted + {count['watchlist']} watchlist; roles {count['by_role']}")
    print(f"Needs review ({len(document['needs_review_ids'])}): " + ", ".join(document["needs_review_ids"]))


if __name__ == "__main__":
    main()
