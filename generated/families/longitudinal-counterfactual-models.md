# longitudinal-counterfactual-models

Accepted records: **11**

## [From Prediction to Intervention: Causal Digital Twins for Personalized Clinical Decision Support](https://link.springer.com/article/10.1186/s12967-026-07895-8)

- **Year / source:** 2026 · Journal of Translational Medicine · `sci_journal`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Formalizes a causal-digital-twin framework combining structural causal models, potential outcomes and reinforcement learning for individualized counterfactual reasoning and sequential decisions.
- **Why it matters:** Directly addresses the gap between trajectory prediction and intervention reasoning that arises when wearable or CGM digital twins are used to recommend actions.
- **Limitations:** The article proposes a methodological framework rather than reporting prospective validation of a deployed personalized treatment policy; identifiability, calibration, safety and transportability remain application-specific.
- **Evidence boundary:** This record supports a causal design framework. It does not show that a fitted digital twin can recover valid individual treatment effects or improve clinical outcomes without design-specific empirical validation.
- **Verification:** `primary_source_checked` on 2026-09-02

## [Longitudinal Targeted Minimum Loss-Based Estimation with Temporal-Difference Heterogeneous Transformer](https://proceedings.mlr.press/v235/shirakawa24a.html)

- **Year / source:** 2024 · ICML · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Combines a heterogeneous temporal transformer with longitudinal targeted learning to estimate dynamic-policy counterfactual means with confidence intervals.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [A Multi-Task Gaussian Process Model for Inferring Time-Varying Treatment Effects in Panel Data](https://proceedings.mlr.press/v206/chen23d.html)

- **Year / source:** 2023 · AISTATS · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Uses structured Gaussian processes to infer dynamic counterfactual trajectories and uncertainty in treated and control panels.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Causal Transformer for Estimating Counterfactual Outcomes](https://proceedings.mlr.press/v162/melnychuk22a.html)

- **Year / source:** 2022 · ICML · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Uses separate transformer streams and adversarial balancing to estimate counterfactual outcomes under time-varying treatments.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Continuous-Time Modeling of Counterfactual Outcomes Using Neural Controlled Differential Equations](https://proceedings.mlr.press/v162/seedat22b.html)

- **Year / source:** 2022 · ICML · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Models irregularly sampled treatment and covariate histories in continuous time with treatment-effect neural controlled differential equations.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Predicting the Impact of Treatments over Time with Uncertainty-Aware Neural Differential Equations](https://proceedings.mlr.press/v151/de-brouwer22a.html)

- **Year / source:** 2022 · AISTATS · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Combines neural differential equations with uncertainty estimation to flag poorly supported longitudinal counterfactual predictions.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [SyncTwin: Treatment Effect Estimation with Longitudinal Outcomes](https://proceedings.neurips.cc/paper/2021/hash/19485224d128528da1602ca47383f078-Abstract.html)

- **Year / source:** 2021 · NeurIPS · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Constructs interpretable synthetic twins from pre-treatment longitudinal trajectories to estimate post-treatment counterfactual outcomes.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Estimating Counterfactual Treatment Outcomes over Time Through Adversarially Balanced Representations](https://openreview.net/forum?id=BJg866NFvB)

- **Year / source:** 2020 · ICLR · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Introduces Counterfactual Recurrent Networks with treatment-invariant temporal representations for multi-step treatment-response estimation.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Estimating the Effects of Continuous-Valued Interventions Using Generative Adversarial Networks](https://proceedings.neurips.cc/paper/2020/hash/11b9842e0a271ff252c1903e7132cd68-Abstract.html)

- **Year / source:** 2020 · NeurIPS · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Introduces SCIGAN for individualized dose-response estimation under continuous interventions.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Time Series Deconfounder: Estimating Treatment Effects over Time in the Presence of Hidden Confounders](https://proceedings.mlr.press/v119/bica20a.html)

- **Year / source:** 2020 · ICML · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Uses multi-treatment temporal factor modelling to construct substitute confounders before longitudinal treatment-effect estimation.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

## [Forecasting Treatment Responses Over Time Using Recurrent Marginal Structural Networks](https://proceedings.neurips.cc/paper/2018/hash/56e6a93212e4482d99c84a639d254b67-Abstract.html)

- **Year / source:** 2018 · NeurIPS · `top_conference`
- **Type / stage:** `method` · `causal-inference` · `methodological`
- **Contribution:** Builds recurrent marginal structural networks for forecasting responses to planned treatment sequences under time-dependent confounding.
- **Why it matters:** Targets time-varying treatments and outcomes, which is closer to continuous wearable monitoring and adaptive health decisions than static treatment-effect estimation.
- **Limitations:** Most evaluations use simulated or semi-synthetic counterfactuals; hidden confounding, treatment-policy shift, irregular sampling and weak overlap can invalidate estimates.
- **Evidence boundary:** Counterfactual forecasts are conditional on identification and model assumptions and should not be presented as verified patient trajectories or clinical utility.
- **Verification:** `review_reference_checked` on 2026-09-02

