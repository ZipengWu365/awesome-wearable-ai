# Sensor and foundation-model landscape

## Classification principle

The model registry distinguishes the signal domain, deployment scope and role in the wearable pipeline. A general time-series model is not labelled a wearable foundation model merely because it can ingest a numeric sequence.

## Families

### Motion and IMU

Reusable representations for accelerometers, gyroscopes and multi-position motion streams. Important questions include cross-device transfer, sampling-rate robustness, body placement, free-living validity and semantic alignment across activity taxonomies.

### ECG and cardiac sensing

Includes waveform foundation models, ECG-language alignment and multimodal cardiac models. Clinical diagnostic performance requires external validation and cannot be inferred from representation quality alone.

### PPG and optical physiology

Covers raw optical waveforms, field-versus-clinical pretraining, signal quality, pulse morphology and transfer to cardiovascular or physiological tasks. Motion, skin tone, contact pressure and device optics are first-order concerns.

### EEG, MEG and neural interfaces

Includes scalp and intracranial signals, topology-agnostic models, language alignment and neural-interface transfer. Channel geometry, montage heterogeneity, subject leakage and clinical task definition require explicit handling.

### EMG and neuromotor interfaces

Includes surface EMG, optical muscle sensing and multimodal neural–muscular control systems for interaction, prostheses and rehabilitation. Evaluation should separate discrete classification, continuous control, fatigue robustness, cross-user calibration and clinical function.

### Sleep and polysomnography

Includes multimodal PSG, wearable sleep signals and sleep-disease representations. Consumer sleep summaries are not equivalent to raw PSG and should be separated.

### CGM and metabolic sensing

Models continuous glucose trajectories and their relation to meals, insulin, activity and metabolic phenotypes. Forecast accuracy alone is insufficient for insulin-dosing decisions.

### Respiratory and acoustic sensing

Covers cough, breath, stethoscope, speech and ambient health acoustics. Recording conditions and device acoustics can dominate transfer.

### Multimodal physiological models

Models multiple biosignals, missing modalities and cross-modal transfer. The central challenge is whether shared representations retain clinically relevant modality-specific information.

### Sensor-language models and agents

Align sensor streams or derived summaries with language for retrieval, recognition, explanation or interaction. Agent outputs require grounding, uncertainty and prospective safety evaluation.

### General time-series enablers

Included only when their design directly addresses a wearable-relevant bottleneck such as irregular sampling, efficient adaptation, long context, missing data or low-resource deployment. They are not counted as wearable-native models.

## Recommended comparison axes

- pretraining scale in subjects, hours, time points and datasets;
- raw waveform versus derived summaries;
- sensor modalities and body placement;
- participant-level and cross-cohort splitting;
- frozen, linear-probe, fine-tuned, zero-shot and few-shot settings;
- cross-device, cross-position and cross-sampling-rate transfer;
- missing-modality robustness;
- calibration and uncertainty;
- subgroup performance;
- code, weights, training data and licensing;
- energy, latency and on-device feasibility;
- clinical association, analytical validation and clinical validation.
