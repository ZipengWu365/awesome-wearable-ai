# general-time-series-enablers

Accepted records: **22**

## [TimesFM-3: A Zero-Shot Foundation Model for Multivariate Forecasting](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/)

- **Year / source:** 2026 · Google Research · `big_tech_report`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Introduces a 330M-parameter multivariate zero-shot forecasting model pretrained on more than one trillion real and synthetic time points.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [ChatTime: A Unified Multimodal Time Series Foundation Model Bridging Numerical and Textual Data](https://arxiv.org/abs/2412.11376)

- **Year / source:** 2025 · AAAI · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Links numerical time series with textual context in a general foundation-model framework.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

## [MIRA: Medical Time Series Foundation Model for Real-World Health Data](https://proceedings.neurips.cc/paper_files/paper/2025/hash/8e12ba543adc673da5b89c9311fcf72c-Abstract-Conference.html)

- **Year / source:** 2025 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Develops a continuous-time medical time-series foundation model pretrained on a heterogeneous corpus reported to contain more than 454 billion time points.
- **Why it matters:** Its treatment of irregular intervals, heterogeneous sampling and missingness is relevant to longitudinal wearable-health streams even though the paper is not wearable-specific.
- **Limitations:** The primary focus is medical forecasting rather than raw wearable sensing; transfer to free-living consumer devices requires direct evaluation.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [SEMPO: Lightweight Foundation Models for Time Series Forecasting](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ecfb69ce6be017deb5a926c2718f6bc1-Abstract-Conference.html)

- **Year / source:** 2025 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `external-validation`
- **Contribution:** Develops a lightweight spectral and prompt-mixture foundation model for zero- and few-shot time-series forecasting.
- **Why it matters:** Its focus on model and data efficiency is relevant to wearable and edge settings where foundation-model cost is a limiting factor.
- **Limitations:** The reported benchmarks are general forecasting datasets; wearable physiological validity must be demonstrated separately.
- **Evidence boundary:** This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Time-MoE: Billion-Scale Time Series Foundation Models with Mixture of Experts](https://openreview.net/forum?id=e1wDDFmlVu)

- **Year / source:** 2025 · ICLR · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Scales time-series pretraining with a mixture-of-experts architecture and large token corpora.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [TimePFN: Effective Multivariate Time Series Forecasting with Synthetic Data](https://arxiv.org/abs/2502.16294)

- **Year / source:** 2025 · AAAI · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Uses prior-data-fitted-network training on synthetic processes for zero-shot multivariate forecasting.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Timer-XL: Long-Context Transformers for Unified Time Series Forecasting](https://openreview.net/forum?id=KMCJXjlDDr)

- **Year / source:** 2025 · ICLR · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Extends autoregressive time-series modelling to long-context and multivariate forecasting settings.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [A Decoder-Only Foundation Model for Time-Series Forecasting](https://proceedings.mlr.press/v235/das24m.html)

- **Year / source:** 2024 · ICML · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Introduces decoder-only large-scale pretraining for zero-shot time-series forecasting.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Chronos: Learning the Language of Time Series](https://openreview.net/forum?id=gerNCVqqtR)

- **Year / source:** 2024 · Transactions on Machine Learning Research · `sci_journal`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Tokenizes numerical time series and trains language-model-style probabilistic forecasters.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [General Time Transformer: An Encoder-Decoder Foundation Model for Most Time Series Analysis Tasks](https://doi.org/10.1145/3627673.3679931)

- **Year / source:** 2024 · CIKM · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Builds an encoder-decoder foundation model intended to span several time-series analysis tasks.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [MOMENT: A Family of Open Time-Series Foundation Models](https://proceedings.mlr.press/v235/goswami24a.html)

- **Year / source:** 2024 · ICML · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Provides open pretrained time-series models and a multi-task evaluation framework relevant to sensor transfer.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [TEST: Text Prototype Aligned Embedding to Activate LLM Ability for Time Series](https://openreview.net/forum?id=Tuh4nZVb0g)

- **Year / source:** 2024 · ICLR · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Aligns time-series embeddings with textual prototypes to reuse frozen language-model representations.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Time-FFM: Towards LM-Empowered Federated Foundation Model for Time Series Forecasting](https://arxiv.org/abs/2405.14252)

- **Year / source:** 2024 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Studies federated foundation-model learning for time-series forecasting across distributed data holders.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Time-LLM: Time Series Forecasting by Reprogramming Large Language Models](https://openreview.net/forum?id=Unb5CVPtae)

- **Year / source:** 2024 · ICLR · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Reprograms frozen large language models for time-series forecasting through prototype and prompt alignment.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Timer: Generative Pre-Trained Transformers Are Large Time Series Models](https://proceedings.mlr.press/v235/liu24cb.html)

- **Year / source:** 2024 · ICML · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Applies generative autoregressive pretraining to unified time-series modelling.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Tiny Time Mixers: Fast Pre-Trained Models for Enhanced Zero/Few-Shot Forecasting of Multivariate Time Series](https://arxiv.org/abs/2401.03955)

- **Year / source:** 2024 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Provides compact pretrained forecasting models that are practical for constrained and edge-adjacent deployment.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Unified Training of Universal Time Series Forecasting Transformers](https://proceedings.mlr.press/v235/woo24a.html)

- **Year / source:** 2024 · ICML · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Pretrains a universal forecasting transformer over diverse time-series domains.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [UniTS: Building a Unified Time Series Model](https://arxiv.org/abs/2403.00131)

- **Year / source:** 2024 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Unifies forecasting, classification, imputation and anomaly detection in one time-series model.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `review_reference_checked` on 2026-09-02

## [A Time Series Is Worth 64 Words: Long-Term Forecasting with Transformers](https://openreview.net/forum?id=Jbdc0vTOcol)

- **Year / source:** 2023 · ICLR · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Introduces channel-independent patch tokenization that became a common backbone for time-series and sensor modelling.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [One Fits All: Power General Time Series Analysis by Pretrained Language Model](https://proceedings.neurips.cc/paper_files/paper/2023/hash/86c17de05579cde52025f9984e6e2ebb-Abstract-Conference.html)

- **Year / source:** 2023 · NeurIPS · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Adapts pretrained language models to multiple time-series tasks through a shared representation interface.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [TS2Vec: Towards Universal Representation of Time Series](https://ojs.aaai.org/index.php/AAAI/article/view/20881)

- **Year / source:** 2022 · AAAI · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Learns hierarchical contrastive time-series representations that are widely used as a transferable baseline for sensor data.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Unsupervised Representation Learning for Time Series with Temporal Neighborhood Coding](https://openreview.net/forum?id=8qDwejCuCN)

- **Year / source:** 2021 · ICLR · `top_conference`
- **Type / stage:** `model` · `representation` · `methodological`
- **Contribution:** Defines temporal neighborhoods for unsupervised representation learning and is frequently applicable to wearable time series.
- **Why it matters:** Provides a general time-series backbone or adaptation strategy that can be evaluated on wearable and physiological data without assuming modality-specific pretraining.
- **Limitations:** The model was not developed specifically for wearable physiology; inclusion records transfer potential and benchmark relevance, not demonstrated wearable superiority.
- **Evidence boundary:** This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness.
- **Verification:** `primary_source_checked` on 2026-09-02

