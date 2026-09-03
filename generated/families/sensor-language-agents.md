# sensor-language-agents

Accepted records: **15**

## [Transforming Wearable Data into Personal Health Insights Using Large Language Model Agents](https://www.nature.com/articles/s41467-025-67922-y)

- **Year / source:** 2026 · Nature Communications · `sci_journal`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Evaluates an LLM-agent workflow that converts longitudinal wearable summaries and activity events into personal health analyses.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [HoloLLM: Multisensory Foundation Model for Language-Grounded Human Sensing and Reasoning](https://proceedings.neurips.cc/paper_files/paper/2025/hash/6a5020522b551fb076dcf613ac5e7bed-Abstract-Conference.html)

- **Year / source:** 2025 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Aligns LiDAR, infrared, mmWave radar and Wi-Fi sensing with language for human-sensing recognition and reasoning benchmarks.
- **Why it matters:** Expands wearable AI toward privacy-preserving ambient and multisensory human understanding and language-grounded reasoning.
- **Limitations:** The sensing setup is primarily ambient rather than body-worn, and benchmark gains do not establish health validity or real-world clinical benefit.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [IMUZero: Zero-Shot Human Activity Recognition by Language-Based Cross-Modality Fusion](https://doi.org/10.1145/3770669)

- **Year / source:** 2025 · Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies · `sci_journal`
- **Type / stage:** `model` · `prediction` · `external-validation`
- **Contribution:** Uses language-based cross-modal alignment to recognize activity classes without task-specific examples for every target label.
- **Why it matters:** Extends wearable recognition beyond closed label sets and links IMU signals to semantic descriptions.
- **Limitations:** Zero-shot activity recognition depends on label semantics and benchmark construction; it is not evidence of zero-shot disease diagnosis or causal reasoning.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Large Language Model-guided Semantic Alignment for Human Activity Recognition](https://doi.org/10.1145/3770652)

- **Year / source:** 2025 · Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies · `sci_journal`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Uses LLM-derived semantic structure to align sensor representations and activity concepts across datasets.
- **Why it matters:** Shows how language supervision can support heterogeneous label spaces and cross-dataset wearable recognition.
- **Limitations:** Semantic alignment performance does not demonstrate clinically valid interpretation, intervention selection or unrestricted open-world reasoning.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [LLM4HAR: Generalizable On-device Human Activity Recognition with Pretrained LLMs](https://doi.org/10.1145/3711896.3737226)

- **Year / source:** 2025 · KDD · `top_conference`
- **Type / stage:** `model` · `prediction` · `external-validation`
- **Contribution:** Adapts pretrained language-model components for generalizable and resource-aware on-device activity recognition.
- **Why it matters:** Connects cross-dataset HAR with edge deployment constraints rather than assuming cloud-scale inference.
- **Limitations:** On-device feasibility and HAR accuracy do not establish battery performance across hardware, clinical reliability or safety-critical deployment.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [One Model to Fit Them All: Universal IMU-based Human Activity Recognition with LLM-assisted Cross-dataset Representation](https://doi.org/10.1145/3749509)

- **Year / source:** 2025 · Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies · `sci_journal`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Constructs an LLM-assisted representation intended to support a single IMU activity-recognition model across heterogeneous datasets.
- **Why it matters:** Directly addresses incompatible activity taxonomies and acquisition settings across wearable HAR datasets.
- **Limitations:** Universality is bounded by the included datasets, sensor channels and label ontology; disease and intervention generalization were not evaluated.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [SensorLM: Learning the Language of Wearable Sensors](https://proceedings.neurips.cc/paper_files/paper/2025/hash/42cd98f0e7520d4a63c34891ac1c972f-Abstract-Conference.html)

- **Year / source:** 2025 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Aligns wearable sensor sequences with language to support semantically grounded reasoning and transfer over human sensing data.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [SING: Spatial Context in Large Language Model for Next-Gen Wearables](https://proceedings.mlr.press/v267/mishra25a.html)

- **Year / source:** 2025 · ICML · `top_conference`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Fuses microstructure-assisted direction-of-arrival sensing and speech embeddings with an LLM for spatially aware wearable speech interaction.
- **Why it matters:** Demonstrates a concrete path from physical wearable sensing to on-device language interfaces for accessibility and augmented-reality use cases.
- **Limitations:** The training data include synthetic spatial speech and the evaluated tasks are interaction-oriented rather than health-outcome or clinical-deployment studies.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Towards a Personal Health Large Language Model](https://www.nature.com/articles/s41591-025-03615-9)

- **Year / source:** 2025 · Nature Medicine · `sci_journal`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Studies LLM adaptation and evaluation for personalized reasoning over longitudinal wearable health data and expert-authored tasks.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Health-LLM: Large Language Models for Health Prediction via Wearable Sensor Data](https://arxiv.org/abs/2401.06866)

- **Year / source:** 2024 · CHIL · `domain_leading_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Evaluates language-model prompting and adaptation for health prediction from structured wearable sensor summaries.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Integrating Large Language Models, EEG, and Eye Tracking for Word-Level Neural State Classification in Reading Comprehension](https://doi.org/10.1109/TNSRE.2024.3443620)

- **Year / source:** 2024 · IEEE Transactions on Neural Systems and Rehabilitation Engineering · `sci_journal`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Integrates EEG, eye tracking and language-model representations for word-level neural-state classification.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Sensor2Text: Enabling Natural Language Interactions for Daily Activity Tracking Using Wearable Sensors](https://doi.org/10.1145/3699747)

- **Year / source:** 2024 · Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies · `sci_journal`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Translates wearable sensor observations into language-oriented representations for interactive daily-activity tracking.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Can Brain Signals Reveal Inner Alignment with Human Languages?](https://aclanthology.org/2023.findings-emnlp.120/)

- **Year / source:** 2023 · Findings of EMNLP · `domain_leading_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Studies alignment between EEG-derived representations and human-language models.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [IMUGPT 2.0: Language-Based Cross-Modality Transfer for Sensor-Based Human Activity Recognition](https://doi.org/10.1145/3678545)

- **Year / source:** 2023 · ISWC · `domain_leading_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Uses language and cross-modality generation to expand IMU activity-recognition training data.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Open Vocabulary Electroencephalography-to-Text Decoding and Zero-Shot Sentiment Classification](https://ojs.aaai.org/index.php/AAAI/article/view/20272)

- **Year / source:** 2022 · AAAI · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Decodes open-vocabulary text from EEG and studies zero-shot sentiment classification.
- **Why it matters:** Connects sensor-derived evidence with natural-language reasoning, reporting, retrieval or interaction, a key interface layer for longitudinal wearable systems.
- **Limitations:** Language outputs can be fluent while clinically wrong; grounding, calibration, privacy, hallucination control and prospective utility require independent evaluation.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

