# biosignal-processing

Accepted records: **7**

## [pyPPG](https://pyppg.readthedocs.io/)

- **Year / source:** 2023 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Open-source Python toolbox for standardized PPG fiducial-point detection and biomarker extraction.
- **Why it matters:** Supports reproducible optical-pulse morphology analysis across studies.
- **Limitations:** Fiducial accuracy and biomarker validity depend on signal quality, site and population.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [TorchECG](https://github.com/DeepPSP/torch_ecg)

- **Year / source:** 2022 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** PyTorch-based toolkit containing ECG datasets, models, preprocessing and evaluation utilities.
- **Why it matters:** Lowers engineering overhead for reproducible ECG deep-learning experiments.
- **Limitations:** Included implementations do not make benchmark splits or clinical claims automatically valid.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [NeuroKit2](https://github.com/neuropsychology/NeuroKit)

- **Year / source:** 2021 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Python toolbox for processing ECG, PPG, EDA, respiration, EMG and related psychophysiological signals.
- **Why it matters:** Offers a unified API for multimodal physiological feature extraction and simulation.
- **Limitations:** Default algorithms and derived features require task-specific validation, especially under motion and free-living noise.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [HeartPy](https://github.com/paulvangentcom/heartrate_analysis_python)

- **Year / source:** 2019 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Python heart-rate analysis toolkit designed for noisy PPG and ECG-like signals.
- **Why it matters:** Useful for transparent baseline processing and quality-aware beat analysis.
- **Limitations:** Performance varies with motion, morphology and sampling conditions and should be externally validated.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [WFDB Python](https://wfdb.io/)

- **Year / source:** 2019 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Official WaveForm DataBase software ecosystem for reading, writing, processing and evaluating physiological waveforms and annotations.
- **Why it matters:** Provides a canonical interface to many PhysioNet waveform resources.
- **Limitations:** File compatibility does not guarantee standardized labels, signal quality or clinically valid evaluation.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [BioSPPy](https://github.com/scientisst/BioSPPy)

- **Year / source:** 2015 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Python toolbox for common ECG, EDA, EEG, EMG, respiration and BVP processing workflows.
- **Why it matters:** Provides reusable baseline signal-processing components across wearable modalities.
- **Limitations:** Algorithms may require adaptation and validation for modern devices, sampling rates and free-living artifacts.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [MNE-Python](https://mne.tools/stable/)

- **Year / source:** 2013 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Open-source ecosystem for EEG, MEG, ECoG and related neurophysiological signal analysis.
- **Why it matters:** Provides mature file I/O, preprocessing, source analysis, visualization and machine-learning interfaces.
- **Limitations:** Correct use requires domain-specific choices about filtering, referencing, artifact rejection and statistical inference.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

