# Awesome Wearable AI v0.3.0 release audit

**Decision: PASS**

## Inventory

- Accepted records: **396**
- Watchlist records: **45**
- Derived and explicit relations: **2169**
- Negative, null or materially mixed intervention records: **14**
- Exact duplicate accepted titles: **0**
- Reused primary URLs: **2** (permitted for parent/subset resources; listed below)

### Accepted records by type

- dataset: 116
- infrastructure: 42
- intervention: 40
- measure: 35
- method: 61
- model: 102

### Model families

- cgm-metabolic-foundation-models: 2
- ecg-cardiac-foundation-models: 15
- eeg-neural-foundation-models: 14
- emg-neuromotor-models: 3
- general-time-series-enablers: 22
- motion-imu-foundation-models: 12
- multimodal-physiological-models: 10
- ppg-optical-foundation-models: 3
- respiratory-acoustic-foundation-models: 2
- sensor-language-agents: 15
- sleep-psg-foundation-models: 4

### Venue/source tiers

- big_tech_report: 6
- domain_leading_conference: 8
- official_dataset: 116
- official_guidance: 5
- official_standard: 2
- official_tool: 30
- sci_journal: 143
- top_conference: 86

### Verification levels

- official_resource_checked: 153
- primary_source_checked: 167
- review_reference_checked: 76

### Evidence-depth levels

- evidence_card: 95
- metadata_verified: 225
- venue_verified: 76

### Reused primary URLs

- `https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml`: dataset-tuh-eeg, dataset-tusz
- `https://physionet.org/content/challenge-2020/1.0.2`: dataset-georgia-ecg, dataset-cinc2020-ecg

## Automated checks

### PASS — registry validation

```text
OK: 396 accepted records, 45 watchlist records, 169 venue-policy entries validated
```

### PASS — unit tests

```text
test_evidence_records_are_not_link_only (test_registry.RegistryTests) ... ok
test_headline_scale (test_registry.RegistryTests) ... ok
test_intervention_outcome_transparency (test_registry.RegistryTests) ... ok
test_registry_export (test_registry.RegistryTests) ... ok
test_relations (test_registry.RegistryTests) ... ok
test_unique_ids_and_titles (test_registry.RegistryTests) ... ok

----------------------------------------------------------------------
Ran 6 tests

OK
```

### PASS — internal links

```text
Internal Markdown links OK
```

## Scientific limitations

- The atlas is a quality-screened scoping registry, not a PRISMA systematic review and not an exhaustive census.
- Venue/source screening removes many weak or unresolved items but does not substitute for study-level risk-of-bias assessment.
- `venue_verified` records are bibliography-grade index entries; their full methods and results have not been independently appraised in this release.
- `metadata_verified` records have checked core metadata but may still lack effect-size, subgroup, calibration or transportability extraction.
- Dataset, standard and tool entries enter through canonical-resource criteria rather than publication prestige.
- Protocols are labelled as protocols and do not count as effectiveness evidence.
- Predictive counterfactual explanations are separated from causal treatment effects and policy-value evidence.
- A model's inclusion does not imply that its weights, training data or commercial use rights are open.
- Coverage is frozen at 2026-09-02; subsequent venue decisions and publications require a new release.
