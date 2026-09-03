# interoperability

Accepted records: **3**

## [HL7 FHIR](https://hl7.org/fhir/)

- **Year / source:** 2014 · HL7 International · `official_standard`
- **Type / stage:** `infrastructure` · `governance` · `official-resource`
- **Contribution:** Defines a widely adopted standard for exchanging electronic health information through modular resources and APIs.
- **Why it matters:** Wearable observations often need to enter clinical systems through interoperable data models.
- **Limitations:** FHIR does not by itself harmonize sensor algorithms, sampling protocols or phenotype validity.
- **Evidence boundary:** This resource defines a standard, governance or reporting framework. Conformance does not by itself demonstrate safety, effectiveness or clinical utility.
- **Verification:** `official_resource_checked` on 2026-09-02

## [Open mHealth](https://www.openmhealth.org/)

- **Year / source:** 2014 · Canonical project documentation · `official_tool`
- **Type / stage:** `infrastructure` · `sensing` · `official-resource`
- **Contribution:** Open schemas and tooling for representing common mobile and wearable health observations.
- **Why it matters:** Provides reusable semantic structures for integrating heterogeneous device data.
- **Limitations:** Schema adoption does not ensure semantic equivalence when source algorithms and sampling differ.
- **Evidence boundary:** Tool inclusion documents available research infrastructure; it does not validate downstream scientific, causal or clinical claims.
- **Verification:** `official_resource_checked` on 2026-09-02

## [OMOP Common Data Model](https://ohdsi.github.io/CommonDataModel/)

- **Year / source:** 2009 · OHDSI · `official_standard`
- **Type / stage:** `infrastructure` · `governance` · `official-resource`
- **Contribution:** Provides a standardized relational model and vocabularies for observational health data.
- **Why it matters:** Supports linking wearable features to longitudinal clinical events and reproducible cohort definitions.
- **Limitations:** Wearable waveform and dense time-series representation often requires extensions or linked stores.
- **Evidence boundary:** This resource defines a standard, governance or reporting framework. Conformance does not by itself demonstrate safety, effectiveness or clinical utility.
- **Verification:** `official_resource_checked` on 2026-09-02

