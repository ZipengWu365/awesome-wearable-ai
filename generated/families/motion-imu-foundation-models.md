# motion-imu-foundation-models

Accepted records: **12**

## [High-Performance Self-Supervised Learning by Joint Training of Flow Matching](https://proceedings.mlr.press/v300/ukita26a.html)

- **Year / source:** 2026 · AISTATS · `top_conference`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Introduces a flow-matching sensor foundation model that jointly learns representations and conditional generation on wearable sensor datasets.
- **Why it matters:** Connects efficient generative modeling with reusable wearable representations and reports substantially faster training and inference than the diffusion comparator.
- **Limitations:** Evidence is based on five downstream datasets and does not establish population-scale health transfer or clinical effectiveness.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Beyond Sensor Data: Foundation Models of Behavioral Data from Wearables Improve Health Predictions](https://openreview.net/forum?id=DtVVltU1ak)

- **Year / source:** 2025 · ICML · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Shows that foundation models over derived longitudinal wearable behaviors can improve health prediction beyond raw-sensor-only framing.
- **Why it matters:** Expands reusable learning beyond one narrowly supervised endpoint and provides a reference point for cross-task, cross-dataset or label-efficient wearable modelling.
- **Limitations:** Publication quality and pretraining scale do not establish cross-device, cross-cohort or clinical generalization; calibration, subgroup performance and deployment shift remain task-specific.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [MoPFormer: Motion-Primitive Transformer for Wearable-Sensor Activity Recognition](https://proceedings.neurips.cc/paper_files/paper/2025/hash/37ecb317d11004f77defbca54ef3b928-Abstract-Conference.html)

- **Year / source:** 2025 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Tokenizes IMU streams into discrete motion primitives and pretrains a masked-motion transformer evaluated on six HAR benchmarks and cross-dataset transfer.
- **Why it matters:** Provides an interpretable discrete vocabulary for motion and explicitly evaluates cross-dataset generalization.
- **Limitations:** Evaluation remains concentrated on activity-recognition benchmarks; robustness to long-duration free-living health prediction and unseen devices is not established.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [RelCon: Relative Contrastive Learning for a Motion Foundation Model for Wearable Data](https://openreview.net/forum?id=k2uUeLCrQq)

- **Year / source:** 2025 · ICLR · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Learns relative motion representations for transfer across wearable activity-recognition settings.
- **Why it matters:** Expands reusable learning beyond one narrowly supervised endpoint and provides a reference point for cross-task, cross-dataset or label-efficient wearable modelling.
- **Limitations:** Publication quality and pretraining scale do not establish cross-device, cross-cohort or clinical generalization; calibration, subgroup performance and deployment shift remain task-specific.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Wearable Interactive Full-Body Motion Tracking and Haptic Feedback Network Systems with Deep Learning](https://www.nature.com/articles/s41467-025-63644-3)

- **Year / source:** 2025 · Nature Communications · `sci_journal`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Integrates distributed wearable motion tracking, deep-learning-based interpretation and haptic feedback into an interactive full-body network.
- **Why it matters:** Represents the broader sensor–inference–feedback loop that Wearable AI must cover beyond passive recognition and health-risk prediction.
- **Limitations:** System demonstrations do not establish effectiveness for a clinical indication, and robustness, comfort, calibration and long-term use remain deployment-specific.
- **Evidence boundary:** This record supports a representation, recognition, sensing or control-system claim under the reported evaluation. It does not by itself establish clinical benefit, causal treatment effect, safety, transportability or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [CrossHAR: Generalizing Cross-Dataset Human Activity Recognition via Hierarchical Self-Supervised Pretraining](https://dl.acm.org/doi/10.1145/3659597)

- **Year / source:** 2024 · Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies · `sci_journal`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Develops hierarchical self-supervised pretraining for cross-dataset activity recognition under heterogeneous sensor and label conditions.
- **Why it matters:** Provides a directly relevant benchmark point for evaluating whether wearable representations transfer beyond a single curated dataset.
- **Limitations:** Transfer remains constrained by overlap in activities, devices, placements and population characteristics, and does not imply universal zero-shot recognition.
- **Evidence boundary:** This record supports a representation, recognition, sensing or control-system claim under the reported evaluation. It does not by itself establish clinical benefit, causal treatment effect, safety, transportability or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

## [GOAT: A Generalized Cross-Dataset Activity Recognition Framework with Natural Language Supervision](https://dl.acm.org/doi/10.1145/3699736)

- **Year / source:** 2024 · Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies · `sci_journal`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Uses natural-language supervision to align heterogeneous activity label spaces and improve cross-dataset wearable activity recognition.
- **Why it matters:** Addresses semantic incompatibility across HAR datasets, a major obstacle to reusable sensor models and foundation-model evaluation.
- **Limitations:** Generalization is bounded by the selected datasets, label descriptions, sensor placements and activity ontologies; language supervision does not remove domain shift.
- **Evidence boundary:** This record supports a representation, recognition, sensing or control-system claim under the reported evaluation. It does not by itself establish clinical benefit, causal treatment effect, safety, transportability or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Self-Supervised Learning for Human Activity Recognition Using 700,000 Person-Days of Wearable Data](https://www.nature.com/articles/s41746-024-01062-3)

- **Year / source:** 2024 · npj Digital Medicine · `sci_journal`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Pretrains accelerometer representations using approximately 700,000 person-days and evaluates label-efficient activity recognition.
- **Why it matters:** Expands reusable learning beyond one narrowly supervised endpoint and provides a reference point for cross-task, cross-dataset or label-efficient wearable modelling.
- **Limitations:** Publication quality and pretraining scale do not establish cross-device, cross-cohort or clinical generalization; calibration, subgroup performance and deployment shift remain task-specific.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [SelfPAB: Large-Scale Pre-Training on Accelerometer Data for Human Activity Recognition](https://doi.org/10.1007/s10489-024-05322-3)

- **Year / source:** 2024 · Applied Intelligence · `sci_journal`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Uses large-scale accelerometer pretraining to improve downstream human activity recognition.
- **Why it matters:** Expands reusable learning beyond one narrowly supervised endpoint and provides a reference point for cross-task, cross-dataset or label-efficient wearable modelling.
- **Limitations:** Publication quality and pretraining scale do not establish cross-device, cross-cohort or clinical generalization; calibration, subgroup performance and deployment shift remain task-specific.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [UniMTS: Unified Pre-training for Motion Time Series](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c290d4373c495b2cad0625d6288260f0-Abstract-Conference.html)

- **Year / source:** 2024 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Develops unified pretraining for heterogeneous motion time series and evaluates transfer across motion-sensing tasks and configurations.
- **Why it matters:** Targets sensor-, position- and task-level heterogeneity that limits reusable IMU models.
- **Limitations:** The conference evaluation does not establish generality to all wearable devices, very long free-living recordings or clinical outcomes.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Wearable Accelerometer Foundation Models for Health via Knowledge Distillation](https://machinelearning.apple.com/research/wearable-accelerometer-foundation-models)

- **Year / source:** 2024 · Apple Machine Learning Research · `big_tech_report`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Distils representations from paired accelerometry and photoplethysmography at large participant scale for health and activity tasks.
- **Why it matters:** Expands reusable learning beyond one narrowly supervised endpoint and provides a reference point for cross-task, cross-dataset or label-efficient wearable modelling.
- **Limitations:** Publication quality and pretraining scale do not establish cross-device, cross-cohort or clinical generalization; calibration, subgroup performance and deployment shift remain task-specific.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [ColloSSL: Collaborative Self-Supervised Learning for Human Activity Recognition](https://dl.acm.org/doi/10.1145/3517246)

- **Year / source:** 2022 · Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies · `sci_journal`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Uses synchronized signals from multiple wearable devices as natural supervision for self-supervised activity representation learning.
- **Why it matters:** Shows how cross-device co-occurrence can supply supervision without manual labels and motivates multi-device pretraining strategies.
- **Limitations:** The method assumes access to collaborative or synchronized devices during pretraining and its transfer depends on sensor configuration and task similarity.
- **Evidence boundary:** This record supports a representation, recognition, sensing or control-system claim under the reported evaluation. It does not by itself establish clinical benefit, causal treatment effect, safety, transportability or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

