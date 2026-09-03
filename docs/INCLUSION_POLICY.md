# Inclusion policy

## Purpose

Awesome Wearable AI is a curated evidence atlas, not a comprehensive scrape. The core registry is deliberately broader than human-activity recognition, but scientific inclusion is restricted by publication and source quality.

## Core scientific records

A scientific paper may enter `data/records/` only when all of the following are satisfied:

1. The work is materially relevant to wearable, body-sensed, implantable, mobile-health, physiological-signal, adaptive-intervention, or directly enabling time-series research.
2. A stable version of record is available.
3. The venue is listed in `data/venues.yaml` as one of:
   - `top_conference`;
   - `domain_leading_conference`;
   - `sci_journal`.
4. The record states what was evaluated, why it matters, at least one limitation, and the strongest conclusion supported by the design.
5. Predictive performance is not presented as causal effect, policy value, clinical utility, or regulatory validation.

SCI/SCIE status is used as a minimum journal screen, not a guarantee of methodological strength. Top-venue publication is likewise not treated as proof of clinical validity.

## Major-organization technical reports

Official technical reports or research pages from major industrial research organizations may enter the core registry under `big_tech_official_report` when they provide substantive technical detail and are published on the organization's canonical research domain. Corporate announcements, product marketing pages, press releases, reposts, and unsupported performance claims are excluded.

## Infrastructure exceptions

The following do not need a journal or conference venue because they are research infrastructure rather than scientific-effectiveness claims:

- canonical datasets and cohorts;
- official software and acquisition platforms;
- standards from recognized standards bodies;
- regulator or health-technology-assessment guidance.

They use `official_dataset`, `official_tool`, `official_standard`, or `official_guidance`. Their inclusion documents availability and relevance only.

## Excluded from headline counts

- preprint-only papers;
- workshop-only or symposium-only papers;
- student abstracts, posters and extended abstracts;
- venue claims that cannot be matched to a version of record;
- predatory or non-indexed journals;
- duplicated papers or minor variants;
- commercial pages without technical evidence;
- projects whose connection to wearable or body-sensed intelligence is incidental.

Potentially important excluded items are retained in `data/excluded/watchlist.yaml` with a reason and promotion action.

## Scope rings

- `wearable-core`: body-worn sensing, actuation, feedback or computation is central.
- `body-sensed-adjacent`: bedside, ambient or assistive sensing supplies methods directly relevant to wearable intelligence.
- `implantable-closed-loop`: implanted sensing/actuation systems that inform the closed-loop research frontier.
- `mobile-health-enabler`: smartphone or remote-care methods that directly support wearable measurement or intervention.
- `cross-domain-enabler`: general time-series, causal or policy methods included because they solve a clearly specified wearable problem.
- `infrastructure`: tools, standards and governance resources.

## Promotion checklist

A watchlist item can be promoted only after:

- confirming the exact title, year and eligible venue;
- replacing a secondary link with a primary publication or official report;
- checking for duplicate versions;
- assigning a scope ring and evidence stage;
- writing a non-promotional limitation and evidence boundary;
- passing `make build` and `make test`.
