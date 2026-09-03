# wearable-signal-processing

Accepted records: **3**

## [actipy](https://github.com/OxWearables/actipy)

- **Year / source:** 2021 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Python toolkit for reading, calibrating, resampling and summarizing raw wearable accelerometry.
- **Why it matters:** Supports transparent preprocessing and cross-device workflows for large accelerometer datasets.
- **Limitations:** Harmonized preprocessing cannot remove all hardware, placement and protocol differences.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [biobankAccelerometerAnalysis](https://github.com/activityMonitoring/biobankAccelerometerAnalysis)

- **Year / source:** 2019 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Reference pipeline developed for large-scale processing of UK Biobank raw accelerometry.
- **Why it matters:** Provides a concrete, inspectable implementation behind influential population accelerometry analyses.
- **Limitations:** The pipeline is tailored to specific acquisition and phenotype conventions and should not be assumed optimal for every cohort.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [GGIR](https://github.com/wadpac/GGIR)

- **Year / source:** 2014 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Open-source R package for processing multi-day raw accelerometer data, including calibration, non-wear handling and sleep/activity summaries.
- **Why it matters:** Widely used in population-scale wrist-accelerometry studies and provides reproducible end-to-end processing.
- **Limitations:** Output validity depends on device metadata, calibration quality, parameter choices and phenotype definitions.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

