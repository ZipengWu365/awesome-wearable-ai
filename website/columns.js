/* Read-only presentation of every repository record, grouped by its existing
   editorial theme. No reclassification, invented dates or fabricated metrics. */
(() => {
  'use strict';
  if (['map', 'radar'].includes(new URLSearchParams(location.search).get('view'))) return;
  const data = JSON.parse(document.getElementById('research-data').textContent);
  const radar = data.radar;
  const $ = id => document.getElementById(id);
  const records = new Map(data.records.map(r => [r.id, r]));
  const routeOf = id => data.routes.find(r => r.id === id);
  const signalById = new Map(radar.signals.map(s => [s.id, s]));
  const columnFiles = {prediction:'prediction.html',intervention:'intervention.html',twin:'digital-twins.html',interface:'mixed-reality.html'};
  const pageTheme = document.body.dataset.columnPage;
  const typeNames = {model: 'Model', dataset: 'Dataset', measure: 'Measure', method: 'Method', intervention: 'Intervention', infrastructure: 'Tools & standards'};
  const roleNames = {direct: 'Direct research', support: 'Supporting method or resource', framework: 'Conceptual framework', adjacent: 'Adjacent research'};
  const evidenceNames = {evidence_card: 'Detailed evidence summary available', metadata_verified: 'Bibliographic metadata checked', venue_verified: 'Publication venue checked'};
  const signalEvidence = {preprint: 'Preprint', peer_reviewed: 'Peer-reviewed study', vendor_announcement: 'Vendor announcement'};
  const updateSummaries = {
    'soter-2026': 'Predicts future body-signal values and fills missing readings by modelling relationships between signals, different frequency patterns and the timing of measurements.',
    'wearableqa-2026': 'Tests whether an AI can answer questions about months of personal wearable history: 4,084 questions, 200 people and histories up to 500 days.',
    'meta-dat-1-2026': 'Moves glasses integration from developer preview to a supported toolkit for mobile apps, including camera, voice, head movement and wrist-based input.',
    'meta-display-expansion-2026': 'Announces sales in more markets and voice-driven face-avatar calls. A preorder or announced rollout is not confirmed delivery.',
    't2d-predictive-twin-2026': 'Adds weekly retraining of a personal diabetes model and daily text-message feedback. The small trial measured weight and glucose outcomes.'
  };
  // Reading summaries of existing catalog/source-review entries, not new registry claims.
  const changes = {
    prediction: [
      ['Method · Sep 2026', 'General time-series transfer → physiology-aware forecasting', 'SOTER models relationships between body signals and their timing; it also reconstructs missing readings. Preprint evaluation, not demonstrated clinical benefit.', 'signal-soter-2026'],
      ['Data · Sep 2026', '4,084 questions about long personal histories', 'WearableQA covers 200 people and up to 500 days of wearable history, extending evaluation beyond a single short signal segment.', 'signal-wearableqa-2026'],
      ['Measured gain · Sep 2026', '51.2% → 71.3% question-answering accuracy', 'The same GPT-5.4 gains 20.1 percentage points when given Python tools. Tools and compute change—not the model version. This is not diagnosis accuracy.', 'signal-wearableqa-2026']
    ],
    intervention: [
      ['Methods · research direction', 'One treatment decision → treatment sequences', 'Longitudinal counterfactual models compare actions over time. Their estimates still depend on identification assumptions; a forecast is not a tested treatment effect.', 'method-causal-transformer-2022'],
      ['Trial · 2026 catalog entry', 'Activity tracking → threshold-triggered feedback', 'The Long COVID study tests energy-management messages. It did not outperform control on the primary endpoint: a new feedback feature was not an outcome improvement.', 'intervention-long-covid-pace-me-2026'],
      ['Review · 2026', 'Adaptive timing must account for burden and context', 'The JITAI review synthesizes when and how to intervene, including engagement and social-context challenges. It is a research synthesis, not a new performance benchmark.', 'method-jitai-annual-review-2026']
    ],
    twin: [
      ['Tested function · 2025 baseline', 'Individual simulation → insulin-delivery adjustment', 'A 72-person, six-month trial evaluates glucose–insulin models within a co-adaptation package. The reported benefit applies to this diabetes-specific system.', 'signal-aid-twin-baseline-2025'],
      ['Model updates · Jul 2026 baseline', 'Weekly retraining + daily personal feedback', 'The type 2 diabetes substudy includes 19 participants. Weight differed between groups; glucose stayed stable. Repeated updates do not imply a complete real-time body twin.', 'signal-t2d-predictive-twin-2026'],
      ['New direction · Feb 2026 framework', 'Predict a trajectory → reason about alternative actions', 'Causal digital twins combine causal models and sequential decisions. This is a methodological framework, not a newly validated whole-person twin.', 'method-causal-digital-twins-2026']
    ],
    interface: [
      ['Data · 2024 baseline', 'First-person context + synchronized third-person views', 'Ego-Exo4D supplies paired perspectives of skilled activities for studying movement in context. The dataset is an enabling resource, not a deployed glasses capability.', 'dataset-ego-exo4d'],
      ['Sensing & input · 2026 catalog entry', 'Discrete gestures → continuous optical muscle input', 'Wearable optomyography evaluates continuous decoding and neuroprosthetic control. This is sensing/interface research, not a verified retail product upgrade.', 'model-wearable-optomyography-2026'],
      ['Product tools · Sep 2026', 'Developer preview → supported glasses toolkit', 'Meta DAT 1.0 exposes camera, voice, head movement and wrist input to applications. Rollout is vendor-announced; delivery and regional availability require separate checks.', 'signal-meta-dat-1-2026']
    ]
  };
  const copy = {
    prediction: {
      title: 'Disease prediction: models, signals and health histories',
      takeaway: 'The catalog moves from single-signal measurements toward reusable models and longer personal histories. Recent work adds physiological forecasting, sensor-data generation and question answering—not just another activity classifier.',
      boundary: 'Read this as a synthesis of the collected work, not a measured trend across the whole field. Many resources enable prediction; they are not themselves validated disease predictors.',
      stages: [
        ['Measure individual signals', 'Earlier datasets and measures establish what is sensed and how a health signal is defined.', ['dataset-mitbih-arrhythmia']],
        ['Reuse models across signals', 'BIOT learns across heterogeneous biosignals; SensorFM extends reusable sensor models to many health tasks.', ['model-biot-2023', 'model-sensorfm-2026']],
        ['Model longer histories', 'SOTER adds physiology-aware forecasting; WearableQA tests questions about months of personal wearable data.', ['signal-soter-2026', 'signal-wearableqa-2026']]
      ],
      highlights: ['model-senflow-2026', 'model-sleepfm-clinical-2026', 'model-sensorfm-2026']
    },
    intervention: {
      title: 'Intervention: compare actions and test their effects',
      takeaway: 'The technical shift is from predicting an outcome to estimating what a different action would change, then testing adaptive feedback or control. The repository includes positive, mixed and null trials: new capability does not always mean better outcomes.',
      boundary: 'Counterfactual estimates, simulations and randomized trials provide different evidence. The latest selected source review did not verify a new trial outcome during its review week; the timeline still includes every older and recent catalog entry.',
      stages: [
        ['Define the causal comparison', 'Specify the treatment, comparison group and assumptions before estimating an effect.', ['method-msm-2000', 'method-causal-trees-2016']],
        ['Model actions over time', 'Longitudinal methods compare treatment sequences rather than a single static decision.', ['method-rmsn-2018', 'method-causal-transformer-2022']],
        ['Test feedback in practice', 'Trials test whether tracking, messages or control improve an outcome. The Long COVID trial retained here did not outperform control on its primary endpoint.', ['intervention-long-covid-pace-me-2026', 'method-jitai-annual-review-2026']]
      ],
      highlights: ['method-jitai-annual-review-2026', 'intervention-long-covid-pace-me-2026', 'intervention-wrist-wearables-umbrella-2026']
    },
    twin: {
      title: 'Personal digital twins: update a model of one person',
      takeaway: 'The concrete examples remain disease-specific. Individual glucose–insulin simulations support treatment adjustment; a later type 2 diabetes study adds weekly model updates and daily feedback. Causal-twin frameworks describe what is still needed to compare alternative actions reliably.',
      boundary: 'The repository assigns only two records primarily to this column. Related personalization, simulation and infrastructure records are shown with their original theme labels—not counted as two dozen demonstrated personal twins. A subpopulation simulator is not an individual twin.',
      stages: [
        ['Personalize a prediction', 'Individual adaptation and health interpretation are useful components, but do not by themselves implement a dynamic twin.', ['model-personalized-physio-adaptation-2025', 'model-ph-llm-2025']],
        ['Simulate individual physiology', 'The 2025 automated-insulin-delivery trial tests individual glucose–insulin simulation within a treatment package.', ['intervention-aid-digital-twin-coadaptation-2025']],
        ['Update and compare actions', 'The 2026 predictive-twin study adds repeated feedback; a separate causal framework formalizes alternative-action reasoning.', ['signal-t2d-predictive-twin-2026', 'method-causal-digital-twins-2026']]
      ],
      highlights: ['method-causal-digital-twins-2026', 'intervention-aid-digital-twin-coadaptation-2025', 'watch-jitai-diffusion-twins-2026']
    },
    interface: {
      title: 'Mixed reality: sensing, body input and wearable interfaces',
      takeaway: 'The research ingredients are first-person visual context, body-input models and continuous control. More recent product announcements add programmable glasses interfaces. These are complementary developments, not a completed health-twin system.',
      boundary: 'Hardware and product announcements are separated from research evaluations. An announced feature is not verified delivery, and a displayed avatar is not a physiological digital twin.',
      stages: [
        ['Capture activity in context', 'First- and third-person datasets connect what the wearer sees with movements and the surrounding scene.', ['dataset-ego4d', 'dataset-ego-exo4d']],
        ['Decode body input', 'Cross-user muscle-signal models and optical muscle sensing extend input beyond discrete gestures toward continuous control.', ['model-generic-neuromotor-interface-2025', 'model-wearable-optomyography-2026']],
        ['Connect to applications', 'Glasses developer tools expose camera, speech and movement inputs. Product rollout and regional availability remain separate checks.', ['signal-meta-dat-1-2026', 'signal-meta-display-expansion-2026']]
      ],
      highlights: ['model-wearable-optomyography-2026', 'model-generic-neuromotor-interface-2025', 'dataset-ego-exo4d']
    }
  };
  let theme = 'prediction';
  const el = (tag, cls, text) => { const node = document.createElement(tag); if (cls) node.className = cls; if (text !== undefined) node.textContent = text; return node; };
  const href = (text, url, cls = '') => { const a = el('a', cls, text); a.href = url; return a; };
  const cleanHash = () => { try { return decodeURIComponent(location.hash.slice(1)); } catch { return ''; } };
  function section(parent, title, text) { if (!text) return; parent.append(el('h5', '', title), el('p', '', text)); }
  function primaryLink(parent, url, text) {
    if (!/^https?:\/\//i.test(url || '')) return;
    const a = href(text + ' ↗', url); a.target = '_blank'; a.rel = 'noopener noreferrer'; parent.append(a);
  }
  function sourceLinks(r, parent) {
    if (!r.link_withheld) primaryLink(parent, r.primary_url, r.catalog_status === 'watchlist' ? 'Candidate source' : 'Read original source');
    primaryLink(parent, r.code_url, 'Code'); primaryLink(parent, r.data_url, 'Data');
  }
  function linkToEntry(id, label) {
    const r = records.get(id), s = signalById.get(id.replace(/^signal-/, ''));
    const a = href(label || r?.short_name || r?.title || s?.title || id, '#' + encodeURIComponent(id));
    a.addEventListener('click', e => { e.preventDefault(); jumpTo(id, true); });
    return a;
  }
  function resetFields() {
    for (const id of ['column-query', 'column-year', 'column-type', 'column-status']) $(id).value = '';
    $('column-related').checked = true;
  }
  function syncUrl(push = false, hash = '') {
    const u = new URL(location.href); u.search = '';
    if (!pageTheme) u.searchParams.set('theme', theme);
    for (const [key, id] of [['q', 'column-query'], ['year', 'column-year'], ['type', 'column-type'], ['status', 'column-status']]) {
      if ($(id).value) u.searchParams.set(key, $(id).value);
    }
    if (!$('column-related').checked) u.searchParams.set('related', '0');
    u.hash = hash; history[push ? 'pushState' : 'replaceState'](null, '', u);
  }
  function renderNavigation() {
    $('columns-nav').replaceChildren();
    for (const route of data.routes) {
      const primary = data.records.filter(r => r.primary_route === route.id);
      const a = href('', columnFiles[route.id]); a.style.setProperty('--column', route.color);
      if (theme === route.id) a.setAttribute('aria-current', 'page');
      a.append(el('span', '', 'COLUMN ' + route.number), el('b', '', route.label), el('small', '', `${primary.filter(r => r.catalog_status === 'accepted').length} accepted · ${primary.filter(r => r.catalog_status === 'watchlist').length} watchlist`));
      $('columns-nav').append(a);
    }
  }
  function relevantSignals() {
    const assessment = radar.assessments.find(a => a.route === theme);
    return radar.signals.filter(s => s.route === theme || s.secondary_routes.includes(theme) || assessment?.signal_ids.includes(s.id));
  }
  function renderBrief() {
    const c = copy[theme], node = $('column-brief'); node.replaceChildren();
    node.append(el('p', 'columns-kicker', `${routeOf(theme).number} · ${routeOf(theme).label.toUpperCase()} · EDITORIAL SYNTHESIS`));
    const title = el(pageTheme ? 'h1' : 'h2', '', c.title); title.id = 'column-title'; title.tabIndex = -1;
    node.append(title, el('p', 'column-takeaway', c.takeaway));
    node.append(href('Browse the full timeline ↓', '#column-archive-title', 'column-jump'));
    node.append(el('h3', '', 'What changed — at a glance'));
    const deltas=el('div','column-changes');
    for(const [label,headline,explanation,id] of changes[theme]){
      const card=el('article','column-change');
      card.append(el('span','column-meta',label),el('h4','',headline),el('p','',explanation),linkToEntry(id,'Study, comparison & source →'));
      deltas.append(card);
    }
    node.append(deltas,el('p','column-boundary',c.boundary));
    const background=el('details','column-background');background.append(el('summary','','Background: how the research direction developed'));
    const path = el('ol', 'column-path');
    for (const [heading, text, ids] of c.stages) {
      const li = el('li'); li.append(el('h4', '', heading), el('p', '', text));
      for (const id of ids) li.append(linkToEntry(id));
      path.append(li);
    }
    background.append(path, el('p', 'column-boundary', 'This sequence is a reading guide across the collected work, not a claim that later papers directly descend from earlier ones. Follow the linked records for scope and evidence.'));
    node.append(background);
    node.append(el('h3', '', 'Recent contributions worth reading'));
    const grid = el('div', 'column-highlight-grid');
    for (const id of c.highlights) {
      const r = records.get(id); if (!r) throw new Error('Unknown column highlight: ' + id);
      const card = el('article', 'column-highlight');
      card.append(el('span', 'column-meta', `${r.year} · ${r.catalog_status === 'watchlist' ? 'Watchlist — not accepted' : r.venue || typeNames[r.record_type]}`), el('h4', '', r.short_name || r.title));
      card.append(el('p', '', r.contribution || `${r.subtopic}. Candidate record; the repository does not supply a reviewed result summary.`));
      if (r.id === 'model-senflow-2026') card.append(el('p', '', 'Why read it: the catalog reports faster training and inference than the diffusion comparator; the evaluation covers five downstream datasets, not clinical effectiveness.'));
      if (r.negative_or_null_result) card.append(el('p', '', r.outcome_status));
      card.append(linkToEntry(id, 'Contribution, evidence & source →')); grid.append(card);
    }
    node.append(grid, el('p', 'column-boundary', 'Selected reading suggestions, not the full column. All records—including datasets, standards, older work and watchlist candidates—appear in the timeline below.'));
    const signals = relevantSignals().sort((a, b) => b.event_date.localeCompare(a.event_date));
    const updates = el('details', 'column-updates'); updates.open = true;
    updates.append(el('summary', '', `Dated research & product updates · source review ${radar.reviewed_on}`));
    updates.append(el('p', '', 'These source reviews complement the repository timeline. Older comparison studies are labelled “baseline”; they are not new publications this week.'));
    const links = el('div', 'column-update-links');
    for (const s of signals) links.append(linkToEntry('signal-' + s.id, `${s.event_date} · ${s.title} · ${s.temporal_role === 'baseline' ? 'Earlier baseline' : signalEvidence[s.evidence_level]}`));
    updates.append(links); node.append(updates);
  }
  function belongs(r) { return r.primary_route === theme || ($('column-related').checked && r.secondary_routes.includes(theme)); }
  function allTimelineItems() {
    const rows = data.records.filter(belongs).map(r => ({kind: 'record', id: r.id, year: r.year, title: r.title, record: r}));
    // Reviews linked to catalog IDs enrich those entries; they do not create
    // duplicate papers. Unlinked reviews remain separate, labelled updates.
    const present = new Set(rows.map(r => r.id));
    for (const s of relevantSignals()) {
      if (s.registry_ids.some(id => present.has(id))) continue;
      rows.push({kind: 'update', id: 'signal-' + s.id, year: Number(s.event_date.slice(0, 4)), title: s.title, signal: s});
    }
    return rows;
  }
  function matches(item, ignoreYear = false) {
    const q = $('column-query').value.toLowerCase().trim(), year = ignoreYear ? '' : $('column-year').value, status = $('column-status').value, type = $('column-type').value;
    const r = item.record, s = item.signal;
    const values = r ? [r.title, r.short_name, r.contribution, r.why_it_matters, r.family, r.subtopic, r.tags, r.modalities, r.year, r.venue, r.reason] : [s.title, s.before, s.after, s.keywords, s.evidence, s.types];
    return (!year || item.year === Number(year)) && (!status || (r ? r.catalog_status : 'update') === status) && (!type || (r ? r.record_type : 'update') === type) && (!q || JSON.stringify(values).toLowerCase().includes(q));
  }
  function signalContent(s) {
    const box = el('div', 'column-signal-content');
    box.append(el('p', 'column-meta', `Event ${s.event_date} · Published ${s.publication_date} · Reviewed ${s.verified_on} · ${signalEvidence[s.evidence_level]}`));
    const comparisons = el('div', 'column-comparison');
    for (const [label, text] of [['Before', s.before], ['What changed', s.after]]) { const d = el('div'); section(d, label, text); comparisons.append(d); }
    box.append(comparisons); section(box, 'Reported result / evidence', s.evidence);
    if (s.comparison) { section(box, 'Comparison baseline', s.comparison.baseline); section(box, 'Reported performance', s.comparison.result); section(box, 'Conditions of the comparison', s.comparison.conditions); }
    section(box, 'Practical relevance · editorial interpretation', s.implication);
    section(box, 'Availability', s.availability); section(box, 'What this does not establish', s.limit);
    const links = el('div', 'column-entry-links'); for (const source of s.sources) primaryLink(links, source.url, source.title); box.append(links);
    return box;
  }
  function recordCard(r) {
    const card = el('article', 'column-entry'); card.id = r.id; card.dataset.recordId = r.id;
    const meta = el('div', 'column-meta');
    meta.append(el('span', 'column-badge' + (r.catalog_status === 'watchlist' ? ' column-badge-watch' : ''), r.catalog_status === 'watchlist' ? 'Watchlist — not accepted' : 'Accepted in repository'));
    if (r.record_type) meta.append(el('span', 'column-badge', typeNames[r.record_type] || r.record_type));
    meta.append(el('span', '', `${r.year} · ${r.venue || r.status || 'Catalog record'}`));
    if (r.primary_route !== theme) meta.append(el('span', 'column-badge', 'Related from ' + routeOf(r.primary_route).short_label));
    meta.append(el('span', '', roleNames[r.route_role]));
    const heading = el('h4'); heading.append(linkToEntry(r.id, r.title));
    card.append(meta, heading);
    card.append(el('p', '', r.contribution || `${r.subtopic}. The repository has not supplied a reviewed contribution summary for this candidate.`));
    if (r.record_type === 'dataset') {
      const facts = [['Scale', r.scale], ['Signals', r.modalities?.join(', ')], ['Access', r.access]].filter(([,v]) => v).map(([k,v]) => `${k}: ${v}`).join(' · ');
      if (facts) card.append(el('p', 'column-dataset', facts));
    }
    if (r.outcome_status) card.append(el('p', 'column-outcome', 'Reported outcome: ' + r.outcome_status));
    if (r.link_withheld) card.append(el('p', 'column-source-warning', 'Source-link warning: ' + r.source_issue + ' The flagged original link is withheld; this record remains in the timeline.'));
    const links = el('div', 'column-entry-links'); sourceLinks(r, links); links.append(linkToEntry(r.id, 'Link to this record')); card.append(links);
    const detail = el('details', 'column-record-detail');
    detail.append(el('summary', '', 'Why it matters, results & limitations'));
    section(detail, 'Why this work matters · repository summary', r.why_it_matters);
    section(detail, 'Study design', r.study_design);
    if (!r.outcome_status) detail.append(el('p', 'column-missing', 'No comparable numerical improvement is specified in this catalog entry. Read the original paper for metrics, baselines and evaluation conditions; publication year alone does not show better performance.'));
    section(detail, 'Limitations', r.limitations); section(detail, 'Evidence boundary', r.evidence_boundary);
    section(detail, 'Why this is on the watchlist', r.reason); section(detail, 'Review still needed', r.review_action);
    if (r.review_note) section(detail, 'Source-review note', r.review_note);
    if (r.evidence_depth) section(detail, 'How much was reviewed', `${evidenceNames[r.evidence_depth] || r.evidence_depth}. This describes catalog review depth, not a ranking of study quality or independent replication.`);
    detail.append(el('p', 'column-classification', `${routeOf(r.primary_route).label} · ${r.subtopic}. ${r.classification_reason}`));
    const themes = el('div', 'column-entry-links');
    for (const id of [r.primary_route, ...r.secondary_routes]) themes.append(href(routeOf(id).label, columnFiles[id] + '#' + encodeURIComponent(r.id)));
    detail.append(themes);
    for (const s of radar.signals.filter(s => s.registry_ids.includes(r.id))) {
      const linked = el('details', 'column-linked-review'); linked.id = 'signal-' + s.id;
      linked.append(el('summary', '', `Additional source review: ${s.title}`), signalContent(s)); detail.append(linked);
    }
    const metadata = el('details'); metadata.append(el('summary', '', 'Original metadata & classification'), el('pre', '', JSON.stringify(r, null, 2))); detail.append(metadata);
    card.append(detail); return card;
  }
  function updateCard(s) {
    const card = el('article', 'column-entry'); card.id = 'signal-' + s.id; card.dataset.signalId = s.id;
    const meta = el('div', 'column-meta'); meta.append(el('span', 'column-badge column-badge-update', 'Additional source review'), el('span', '', `${s.event_date} · ${signalEvidence[s.evidence_level]} · ${s.temporal_role === 'baseline' ? 'Earlier baseline' : 'Dated update'}`));
    const heading = el('h4'); heading.append(linkToEntry(card.id, s.title));
    card.append(meta, heading, el('p', '', updateSummaries[s.id] || s.after));
    const result = el('p', 'column-update-result'); result.append(el('strong', '', 'Reported result: '), document.createTextNode(s.evidence)); card.append(result);
    const links = el('div', 'column-entry-links'); for (const source of s.sources) primaryLink(links, source.url, source.title); card.append(links);
    card.append(el('p', 'column-missing', s.registry_ids.length ? 'A related catalog record is available in another column; this review is not another paper.' : 'Not part of the accepted/watchlist record counts. Included from the repository’s separately maintained source review.'));
    const detail = el('details', 'column-record-detail'); detail.append(el('summary', '', 'Before vs after, reported results & sources'), signalContent(s));
    card.append(detail); return card;
  }
  function sortedItems() {
    return allTimelineItems().filter(item => matches(item)).sort((a, b) => b.year - a.year || (a.kind === 'update' && b.kind === 'update' ? b.signal.event_date.localeCompare(a.signal.event_date) : a.kind !== b.kind ? a.kind === 'update' ? -1 : 1 : a.title.localeCompare(b.title)));
  }
  function selectYear(year) {
    $('column-year').value = String(year);
    renderTimeline(); syncUrl(true, 'column-archive-title');
    const active = $('column-years').querySelector('[aria-current="true"]');
    if (active) { active.scrollIntoView({block:'nearest',inline:'center',behavior:'instant'}); active.focus({preventScroll:true}); }
  }
  function yearOverview() {
    const years = $('column-years'), previousScroll = years.scrollLeft, firstRender = !years.children.length;
    const rows = allTimelineItems().filter(item => matches(item, true));
    const values = [...new Set(allTimelineItems().map(item => item.year))].sort((a,b)=>a-b);
    const largest = Math.max(1, ...values.map(y => rows.filter(item => item.year===y && item.record).length));
    years.replaceChildren();
    for (const [index, year] of values.entries()) {
      const items = rows.filter(item => item.year===year);
      const accepted = items.filter(item => item.record?.catalog_status==='accepted').length;
      const watchlist = items.filter(item => item.record?.catalog_status==='watchlist').length;
      const reviews = items.filter(item => item.kind==='update').length;
      const a = href('', '?year='+year+'#column-archive-title', 'column-year-tick');
      a.dataset.year = String(year);a.dataset.accepted=String(accepted);a.dataset.watchlist=String(watchlist); a.setAttribute('aria-current', String($('column-year').value===String(year)));
      a.setAttribute('aria-label', `${year}: ${accepted} accepted, ${watchlist} watchlist, ${reviews} additional reviews. Show this year.`);
      a.append(el('strong','',String(year)),el('span','column-year-count',`${accepted+watchlist} records`));
      const chart = el('span','column-year-bar'); chart.setAttribute('aria-hidden','true');
      const acceptedBar=el('i','year-accepted'),watchBar=el('i','year-watchlist');
      acceptedBar.style.height=(accepted/largest*60)+'px';watchBar.style.height=(watchlist/largest*60)+'px';
      chart.append(watchBar,acceptedBar);a.append(chart);
      a.append(el('small','',`${accepted} accepted · ${watchlist} watchlist`));
      if (reviews) a.append(el('small','',`+ ${reviews} source reviews`));
      const types=[...new Set(items.flatMap(item=>item.record?[typeNames[item.record.record_type]]:[]))];
      a.append(el('span','column-year-types',types.length?types.join(' · '):reviews?'Dated source updates':'No matches for these filters'));
      if(index && year-values[index-1]>1) a.append(el('span','column-year-gap',`${year-values[index-1]} years after ${values[index-1]}`));
      a.onclick=e=>{e.preventDefault();selectYear(year);};years.append(a);
    }
    years.scrollLeft = firstRender ? years.scrollWidth : previousScroll;
    $('column-all-years').setAttribute('aria-pressed',String(!$('column-year').value));
    updateYearControls();
  }
  function updateYearControls() {
    const years=$('column-years');
    $('column-years-back').disabled=years.scrollLeft<=1;
    $('column-years-next').disabled=years.scrollLeft+years.clientWidth>=years.scrollWidth-2;
  }
  function yearInsights(rows) {
    const box=$('column-year-insights'), year=$('column-year').value;
    box.replaceChildren();
    if(!year) {
      box.append(el('p','','All years selected: every matching title is listed below, newest year first. Choose a year above to compare its contributions and source-reviewed updates.'));
      return;
    }
    box.append(el('h3','',`${year} · contributions & updates`));
    // Only existing reviewed comparisons are used; catalog size is never a trend claim.
    const selected = new Set(rows.map(item=>item.id));
    const signals = relevantSignals().filter(s=>s.event_date.startsWith(year) && (selected.has('signal-'+s.id)||s.registry_ids.some(id=>selected.has(id))));
    const grid=el('div','column-year-review-grid');
    for(const s of signals) {
      const card=el('article','column-year-review');
      card.append(el('p','column-meta',`${s.event_date} · ${signalEvidence[s.evidence_level]}`),linkToEntry('signal-'+s.id,s.title));
      const before=el('p');before.append(el('strong','','Before: '),document.createTextNode(s.before));
      const after=el('p');after.append(el('strong','','What changed: '),document.createTextNode(s.after));
      card.append(before,after);
      if(s.comparison){const result=el('p');result.append(el('strong','','Reported comparison: '),document.createTextNode(s.comparison.result+' '+s.comparison.conditions));card.append(result);}
      card.append(el('p','column-year-limit',s.limit));grid.append(card);
    }
    if(signals.length) box.append(grid);
    else box.append(el('p','','No separately reviewed before/after comparison is available for this year under the current filters. The directory below gives each record’s original contribution; a newer publication date does not establish better performance.'));
  }
  function compactEntry(item) {
    const r=item.record,s=item.signal,row=el('details','column-catalog-row');
    row.id=item.id;
    if(r)row.dataset.recordId=r.id;else row.dataset.signalId=s.id;
    const summary=el('summary'),meta=el('span','column-catalog-meta');
    meta.append(el('span','',String(item.year)),el('span','column-badge',r?typeNames[r.record_type]:'Source review'));
    meta.append(el('span',r?.catalog_status==='watchlist'?'column-badge column-badge-watch':'',r?(r.catalog_status==='watchlist'?'Watchlist':'Accepted'):signalEvidence[s.evidence_level]));
    if(r?.primary_route!==theme && r)meta.append(el('span','', 'Related · '+routeOf(r.primary_route).short_label));
    const text=el('span','column-catalog-copy');
    text.append(el('strong','column-catalog-title',item.title),el('span','column-catalog-contribution',r?(r.contribution||r.reason||'Contribution not yet reviewed in the repository.'):(updateSummaries[s.id]||s.after)));
    summary.append(meta,text,el('span','column-catalog-open','Details +'));row.append(summary);
    // Keep all titles searchable in the DOM; build long evidence text only on demand.
    row._hydrate=()=>{
      if(row.dataset.loaded)return;
      row.dataset.loaded='true';
      const card=r?recordCard(r):updateCard(s);card.removeAttribute('id');card.removeAttribute('data-record-id');card.removeAttribute('data-signal-id');
      row.append(card);
    };
    row.addEventListener('toggle',()=>{if(row.open)row._hydrate();});
    return row;
  }
  function renderTimeline() {
    const rows = sortedItems();
    const accepted = rows.filter(i => i.record?.catalog_status === 'accepted').length;
    const watchlist = rows.filter(i => i.record?.catalog_status === 'watchlist').length;
    const updates = rows.filter(i => i.kind === 'update').length;
    const primary = rows.filter(i => i.record?.primary_route === theme).length;
    const total=data.records.filter(belongs).length;
    $('column-result-count').textContent = `${accepted + watchlist} / ${total} repository records match (${accepted} accepted + ${watchlist} watchlist; ${primary} primary + ${accepted + watchlist - primary} cross-theme) · ${updates} additional source reviews. All ${rows.length} matching titles are listed—no pagination.`;
    const list = $('column-timeline'); list.replaceChildren();yearOverview();yearInsights(rows);
    $('column-directory-title').textContent=($('column-year').value||'All years')+' · complete paper & resource directory';
    if (!rows.length) {
      const empty = el('div', 'column-empty'); empty.append(el('p', '', 'No records match these filters. Try another year, clear the search, or include related work.'));
      const reset = el('button', '', 'Show all records in this column'); reset.type = 'button'; reset.onclick = () => { resetFields(); syncUrl(); renderTimeline(); }; empty.append(reset); list.append(empty); return;
    }
    for (const year of [...new Set(rows.map(r => r.year))]) {
      const items = rows.filter(r => r.year === year), group = el('section', 'column-year-group'); group.id = 'year-' + year;
      const label = el('h3', 'column-year-label', String(year)); label.append(el('small', '', `${items.length} entries`)); group.append(label);
      const body = el('div', 'column-year-entries'); for (const item of items) body.append(compactEntry(item)); group.append(body); list.append(group);
    }
  }
  function renderColumn() {
    $('columns-reader').style.setProperty('--column', routeOf(theme).color);
    if(pageTheme) $('columns-coverage').textContent = `${data.route_counts.accepted[theme].total} accepted + ${data.route_counts.watchlist[theme].total} watchlist records in this primary column · Source updates reviewed ${radar.reviewed_on}.`;
    document.title = `${routeOf(theme).label} · Papers & timeline · Awesome Wearable AI`;
    renderNavigation(); renderBrief();
    const value = $('column-year').value; $('column-year').replaceChildren();
    const all = el('option', '', 'All years'); all.value = ''; $('column-year').append(all);
    for (const year of [...new Set(allTimelineItems().map(i => i.year))].sort((a,b) => b-a)) { const option = el('option', '', String(year)); option.value = String(year); $('column-year').append(option); }
    $('column-year').value = value; renderTimeline();
  }
  function jumpTo(id, push = false) {
    let target = $(id);
    if (!target) {
      const r = records.get(id), s = signalById.get(id.replace(/^signal-/, ''));
      if (!r && !s) return false;
      const destination = r && r.primary_route !== theme && !r.secondary_routes.includes(theme) ? r.primary_route : s && !relevantSignals().some(item=>item.id===s.id) ? s.route : null;
      if(destination){location.href=columnFiles[destination]+'#'+encodeURIComponent(id);return true;}
      const findIndex = rows => rows.findIndex(item=>item.id===id || (s && item.record && s.registry_ids.includes(item.record.id)));
      let index=findIndex(sortedItems());
      if(index<0){resetFields();renderColumn();index=findIndex(sortedItems());}
      if(index<0)return false;
      renderTimeline();
      if(s)for(const recordId of s.registry_ids){const owner=$(recordId);if(owner?._hydrate){owner._hydrate();owner.open=true;}}
      target=$(id);
    }
    if (!target) return false;
    target._hydrate?.();
    let parent = target.parentElement;
    while (parent) { if (parent.tagName === 'DETAILS') parent.open = true; parent = parent.parentElement; }
    if (target.tagName === 'DETAILS') target.open = true;
    const detail = target.querySelector('.column-record-detail'); if (detail) detail.open = true;
    if (push) syncUrl(true, id);
    target.tabIndex = -1; target.focus({preventScroll: true}); target.scrollIntoView({block:'start',behavior:'instant'}); return true;
  }
  function restoreLocation() {
    const params = new URLSearchParams(location.search), hash = cleanHash();
    const legacyTheme = hash.match(/^assessment-(prediction|intervention|twin|interface)$/)?.[1];
    const r = records.get(hash), s = signalById.get(hash.replace(/^signal-/, ''));
    theme = [pageTheme, params.get('theme'), legacyTheme, r?.primary_route, s?.route].find(t => routeOf(t)) || 'prediction';
    resetFields(); renderColumn();
    for (const [key,id] of [['q','column-query'],['year','column-year'],['type','column-type'],['status','column-status']]) $(id).value = params.get(key) || '';
    $('column-related').checked = params.get('related') !== '0';
    renderTimeline();
    const selectedTick=$('column-years').querySelector('[aria-current="true"]');
    if(selectedTick) $('column-years').scrollLeft+=selectedTick.getBoundingClientRect().left-$('column-years').getBoundingClientRect().left-($('column-years').clientWidth-selectedTick.clientWidth)/2;
    if (legacyTheme) { syncUrl(false); $('column-title').scrollIntoView({block:'start'}); }
    else if (hash) requestAnimationFrame(() => jumpTo(hash));
  }
  // ID coverage is independent of the selected reading view and cross-links.
  const ids = data.records.map(r => r.id);
  if (new Set(ids).size !== ids.length || ids.length !== data.counts.accepted + data.counts.watchlist || data.records.some(r => !routeOf(r.primary_route))) throw new Error('Incomplete column assignment');
  $('columns-coverage').textContent = `${data.counts.accepted} accepted + ${data.counts.watchlist} watchlist records, each assigned to one primary column. Cross-theme links do not add new records. Catalog: ${data.cutoff} · Selected source updates reviewed: ${radar.reviewed_on}.`;
  $('column-filters').onsubmit = e => e.preventDefault();
  for (const id of ['column-query','column-year','column-type','column-status','column-related']) $(id).addEventListener(id === 'column-query' ? 'input' : 'change', () => { renderTimeline();syncUrl(); });
  $('column-reset').onclick = () => { resetFields(); syncUrl(); renderTimeline(); };
  $('column-all-years').onclick=()=>selectYear('');
  $('column-years-latest').onclick=()=>selectYear(Math.max(...allTimelineItems().map(item=>item.year)));
  for(const [id,direction] of [['column-years-back',-1],['column-years-next',1]]) $(id).onclick=()=>$('column-years').scrollBy({left:direction*Math.max(200,$('column-years').clientWidth*.75),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
  $('column-years').addEventListener('scroll',updateYearControls,{passive:true});
  window.addEventListener('resize',updateYearControls);
  window.addEventListener('popstate', restoreLocation);
  window.addEventListener('hashchange', () => { const hash = cleanHash(); if (hash) jumpTo(hash); });
  restoreLocation();
})();
