/* Read-only presentation of every repository record, grouped by its existing
   editorial theme. No reclassification, invented dates or fabricated metrics. */
(() => {
  'use strict';
  if (['map', 'radar'].includes(new URLSearchParams(location.search).get('view'))) return;
  const data = JSON.parse(document.getElementById('research-data').textContent);
  const radar = data.radar;
  const editorial = JSON.parse(document.getElementById('editorial-data').textContent);
  const $ = id => document.getElementById(id);
  const records = new Map(data.records.map(r => [r.id, r]));
  // Plain-language display names only; original classifications stay in data.routes.
  const themeLabels = {prediction:'Predicting health changes',intervention:'Health actions and their effects',twin:'Personal health models',interface:'Wearable devices and mixed reality'};
  const routes = data.routes.map(r=>({...r,label:themeLabels[r.id]||r.label,short_label:themeLabels[r.id]||r.short_label}));
  const routeOf = id => routes.find(r => r.id === id);
  const signalById = new Map(radar.signals.map(s => [s.id, s]));
  const columnFiles = {prediction:'prediction.html',intervention:'intervention.html',twin:'digital-twins.html',interface:'mixed-reality.html'};
  const pageTheme = document.body.dataset.columnPage;
  const typeNames = {model: 'Model', dataset: 'Dataset', measure: 'Measure', method: 'Method', intervention: 'Intervention', infrastructure: 'Tools & standards'};
  const roleNames = {direct: 'Research on this topic', support: 'A method or resource used for this topic', framework: 'A proposed approach', adjacent: 'Research on a related topic'};
  const evidenceNames = {evidence_card: 'A detailed study summary is available', metadata_verified: 'Basic publication details checked', venue_verified: 'Journal or conference details checked'};
  const signalEvidence = {preprint: 'Preprint — not yet peer-reviewed', peer_reviewed: 'Study reviewed by other researchers', vendor_announcement: 'Company announcement'};
  const updateSummaries = {
    'soter-2026': 'Predicts future body-signal values and fills missing readings by modelling relationships between signals, different frequency patterns and the timing of measurements.',
    'wearableqa-2026': 'Tests whether an AI can answer questions about months of personal wearable history: 4,084 questions, 200 people and histories up to 500 days.',
    'meta-dat-1-2026': 'Moves glasses integration from developer preview to a supported toolkit for mobile apps, including camera, voice, head movement and wrist-based input.',
    'meta-display-expansion-2026': 'Announces sales in more markets and voice-driven face-avatar calls. A preorder or announced rollout is not confirmed delivery.',
    't2d-predictive-twin-2026': 'Adds weekly retraining of a personal diabetes model and daily text-message feedback. The small trial measured weight and glucose outcomes.'
  };
  const copy = {
    prediction: {
      title: 'Disease prediction: what wearable data can tell us about health',
      takeaway: 'Researchers are using more types of body signals and longer recordings to study health. Recent AI models can predict future readings, generate example sensor data and answer questions about a person’s recordings. These are different tasks, and each needs its own tests.',
      boundary: 'This summary describes the work collected here, not every study in the field. Many of these tools support health research but have not been shown to predict disease reliably in patients.',
      stages: [
        ['Record body signals', 'Earlier datasets provide recordings, such as heart signals, that researchers can study and compare.', ['dataset-mitbih-arrhythmia']],
        ['Use one model for several tasks', 'BIOT learns from different kinds of body signals. SensorFM is designed to support several health tasks using sensor data.', ['model-biot-2023', 'model-sensorfm-2026']],
        ['Study longer recordings', 'SOTER predicts how body signals change. WearableQA tests whether AI can answer questions about months of wearable data.', ['signal-soter-2026', 'signal-wearableqa-2026']]
      ],
      highlights: ['model-senflow-2026', 'model-sleepfm-clinical-2026', 'model-sensorfm-2026']
    },
    intervention: {
      title: 'Health interventions: which actions actually help?',
      takeaway: 'Predicting what may happen is different from finding out which action helps. This column covers methods for comparing choices and studies that test advice, treatment or device control. Some studies found benefits; others found little or no difference.',
      boundary: 'A computer estimate is not the same as a trial with people. The latest update check found no newly verified trial result for this topic during that week. All collected studies, old and recent, are still listed below.',
      stages: [
        ['Decide what to compare', 'Define the treatment, who receives it and what it is compared with. State the assumptions needed to estimate its effect.', ['method-msm-2000', 'method-causal-trees-2016']],
        ['Compare choices over time', 'These methods study a series of treatment decisions, rather than just one choice.', ['method-rmsn-2018', 'method-causal-transformer-2022']],
        ['Test whether people benefit', 'Trials check whether tracking, messages or treatment improve results. The Long COVID trial did not show a better main result than the comparison group.', ['intervention-long-covid-pace-me-2026', 'method-jitai-annual-review-2026']]
      ],
      highlights: ['method-jitai-annual-review-2026', 'intervention-long-covid-pace-me-2026', 'intervention-wrist-wearables-umbrella-2026']
    },
    twin: {
      title: 'Personal digital twins: computer models that track one person’s health',
      takeaway: 'A personal digital twin is a computer model updated with information about a person. The tested examples here focus on diabetes: they model blood sugar and insulin or give repeated personal feedback. Other papers propose ways to compare treatment choices.',
      boundary: 'Only two collected resources have this as their main topic. Resources from other columns are labelled as related work. They may provide useful parts of a system, but they are not complete, tested models of a person. A model of a group is not a personal twin.',
      stages: [
        ['Adjust predictions for one person', 'Personal predictions and explanations can be useful, but alone they do not make a digital twin that keeps up with changes in a person.', ['model-personalized-physio-adaptation-2025', 'model-ph-llm-2025']],
        ['Model blood sugar and insulin', 'A 2025 trial tested personal computer models as part of an automated insulin treatment system.', ['intervention-aid-digital-twin-coadaptation-2025']],
        ['Update the model and compare choices', 'A 2026 study gives repeated personal feedback. A separate paper proposes how models could estimate the effects of different actions.', ['signal-t2d-predictive-twin-2026', 'method-causal-digital-twins-2026']]
      ],
      highlights: ['method-causal-digital-twins-2026', 'intervention-aid-digital-twin-coadaptation-2025', 'watch-jitai-diffusion-twins-2026']
    },
    interface: {
      title: 'Smart glasses and body signals: new ways to use digital devices',
      takeaway: 'This column covers systems that connect digital information with what people see and do. Researchers study videos from the wearer’s viewpoint and use muscle signals to control devices. New app-building tools also let developers use more inputs from smart glasses.',
      boundary: 'Research tests and company announcements are labelled separately. An announced feature may not yet be available. A digital character on a screen is not a model of how a person’s body works.',
      stages: [
        ['Record what people see and do', 'Videos from the wearer and outside cameras help connect movement with the surrounding scene.', ['dataset-ego4d', 'dataset-ego-exo4d']],
        ['Use muscle signals to control devices', 'Models that work across people and sensors that use light can help track changing movements, not just recognize separate gestures.', ['model-generic-neuromotor-interface-2025', 'model-wearable-optomyography-2026']],
        ['Build apps for smart glasses', 'Developer tools let apps use cameras, speech and movement. Check separately where and when each feature is available.', ['signal-meta-dat-1-2026', 'signal-meta-display-expansion-2026']]
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
    const a = href(text, url); a.target = '_blank'; a.rel = 'noopener noreferrer'; parent.append(a);
  }
  function sourceLinks(r, parent) {
    if (!r.link_withheld) primaryLink(parent, r.primary_url, 'Read the original source');
    primaryLink(parent, r.code_url, 'Code'); primaryLink(parent, r.data_url, 'Data');
  }
  function linkToEntry(id, label) {
    const r = records.get(id), s = signalById.get(id.replace(/^signal-/, ''));
    const featured=Object.values(editorial.columns).flatMap(brief=>brief.stories).find(story=>story.id===id);
    const a = href(label || featured?.name || r?.short_name || r?.title || s?.title.split(':')[0] || id, '#' + encodeURIComponent(id));
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
    for (const route of routes) {
      const primary = data.records.filter(r => r.primary_route === route.id);
      const a = href('', columnFiles[route.id]); a.style.setProperty('--column', route.color);
      if (theme === route.id) a.setAttribute('aria-current', 'page');
      a.append(el('span', '', 'COLUMN ' + route.number), el('b', '', route.label), el('small', '', `${primary.filter(r => r.catalog_status === 'accepted').length} collected resources; ${primary.filter(r => r.catalog_status === 'watchlist').length} awaiting review`));
      $('columns-nav').append(a);
    }
  }
  function relevantSignals() {
    const assessment = radar.assessments.find(a => a.route === theme);
    return radar.signals.filter(s => s.route === theme || s.secondary_routes.includes(theme) || assessment?.signal_ids.includes(s.id));
  }
  function renderBrief() {
    const c = copy[theme], brief = editorial.columns[theme], node = $('column-brief'); node.replaceChildren();
    node.append(el('p', 'columns-kicker', `${routeOf(theme).number} · ${routeOf(theme).label.toUpperCase()} · RESEARCH BRIEF`));
    const title = el(pageTheme ? 'h1' : 'h2', '', brief.headline); title.id = 'column-title'; title.tabIndex = -1;
    node.append(title, el('p', 'column-takeaway', brief.summary));
    const key = el('div','column-brief-key');key.append(el('strong','','What the results show'),el('p','',brief.takeaway));node.append(key);
    node.append(el('p','column-practical',brief.use));
    const evidence = el('div','column-trend-sources');evidence.append(el('span','',brief.status+'. Based on: '));
    for(const id of brief.ids)evidence.append(linkToEntry(id));node.append(evidence);
    const shortcuts=el('nav','column-brief-shortcuts');shortcuts.setAttribute('aria-label','Research brief sections');
    shortcuts.append(href('Browse all papers by year','#column-archive-title','column-jump'),href('Compare six types of change','#column-dimensions'),href('Read the featured studies','#column-featured'));node.append(shortcuts);
    node.append(el('p','column-edition',`Brief edited ${editorial.edited_on} using the repository’s collected work. Each featured study shows its publication date and how its source was checked.`));
    const heading=el('h3','','What changed in methods, data and devices?');heading.id='column-dimensions';node.append(heading);
    const dimensions=el('div','column-dimensions');
    for(const item of brief.dimensions){
      const cell=el('article','column-dimension');cell.dataset.dimension=item.kind;
      cell.append(el('h4','',item.kind),el('p','',item.text));
      const links=el('div','column-dimension-links');for(const id of item.ids)links.append(linkToEntry(id));cell.append(links);dimensions.append(cell);
    }
    node.append(dimensions);
    const featured=el('h3','','Key studies: what they add and how they were tested');featured.id='column-featured';node.append(featured);
    const deltas=el('div','column-changes');
    for(const story of brief.stories){
      const card=el('article','column-change');
      card.dataset.featuredId=story.id;
      card.append(el('span','column-meta',`${story.name} · ${story.date}`),el('h4','',story.headline),el('p','',story.change));
      const result=el('p','column-feature-result');result.append(el('strong','','Result: '),document.createTextNode(story.result));card.append(result);
      const comparison=el('details','column-study-comparison');comparison.append(el('summary','','Compare with earlier work'));
      for(const [label,text] of [['Earlier approach',story.before],['Why it may be useful · our reading',story.benefit],['Conditions and limits',story.condition]]){
        comparison.append(el('h5','',label),el('p','',text));
      }
      comparison.append(el('p','column-source-check',`${story.verification ? 'Review basis' : 'Source checked'} ${story.checked_on}. ${story.verification ? story.verification+'. ' : ''}${story.locator}.`));card.append(comparison);
      const links=el('div','column-study-links');primaryLink(links,story.source,'Read the original source');links.append(linkToEntry(story.id,'Open full entry'));card.append(links);
      deltas.append(card);
    }
    node.append(deltas);
    const background=el('details','column-background');background.append(el('summary','','Background: how the research direction developed'));
    background.append(el('p','',c.takeaway),el('p','column-boundary',c.boundary));
    const path = el('ol', 'column-path');
    for (const [heading, text, ids] of c.stages) {
      const li = el('li'); li.append(el('h4', '', heading), el('p', '', text));
      for (const id of ids) li.append(linkToEntry(id));
      path.append(li);
    }
    background.append(path, el('p', 'column-boundary', 'These examples help explain the topic. They do not mean that each later study was built directly on the earlier one. Open a study to see what it tested.'));
    node.append(background);
    node.append(el('p', 'column-boundary', 'Featured work explains the research direction. The timeline below still lists every resource, including older studies, datasets, tools and items awaiting review.'));
    const signals = relevantSignals().sort((a, b) => b.event_date.localeCompare(a.event_date));
    const updates = el('details', 'column-updates');
    updates.append(el('summary', '', `Research and product news · last checked ${radar.reviewed_on}`));
    updates.append(el('p', '', 'These updates include links to their sources. Earlier studies are included to help explain what changed; they are labelled as earlier work, not this week’s news.'));
    const links = el('div', 'column-update-links');
    for (const s of signals) links.append(linkToEntry('signal-' + s.id, `${s.event_date} · ${s.title} · ${s.temporal_role === 'baseline' ? 'Earlier work for comparison' : signalEvidence[s.evidence_level]}`));
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
    if (s.comparison) { section(box, 'What it was compared with', s.comparison.baseline); section(box, 'Test results', s.comparison.result); section(box, 'How the comparison was tested', s.comparison.conditions); }
    section(box, 'Why it may be useful · our summary', s.implication);
    section(box, 'Availability', s.availability); section(box, 'What this does not establish', s.limit);
    const links = el('div', 'column-entry-links'); for (const source of s.sources) primaryLink(links, source.url, source.title); box.append(links);
    return box;
  }
  function recordCard(r) {
    const card = el('article', 'column-entry'); card.id = r.id; card.dataset.recordId = r.id;
    const meta = el('div', 'column-meta');
    meta.append(el('span', 'column-badge' + (r.catalog_status === 'watchlist' ? ' column-badge-watch' : ''), r.catalog_status === 'watchlist' ? 'Awaiting review' : 'In the collection'));
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
    detail.append(el('summary', '', 'What the study found and what it cannot tell us'));
    section(detail, 'Why this work matters · summary from the collection', r.why_it_matters);
    section(detail, 'How the study was done', r.study_design);
    if (!r.outcome_status) detail.append(el('p', 'column-missing', 'This entry does not give a numerical comparison showing improvement. Read the original paper to see what was measured, what it was compared with and how it was tested. A newer paper does not always mean better results.'));
    section(detail, 'Limits of the study', r.limitations); section(detail, 'What these results can and cannot show', r.evidence_boundary);
    section(detail, 'Why this resource is being considered', r.reason); section(detail, 'What still needs checking', r.review_action);
    if (r.review_note) section(detail, 'Source-review note', r.review_note);
    if (r.evidence_depth) section(detail, 'What we have checked', `${evidenceNames[r.evidence_depth] || r.evidence_depth}. This describes our review of the entry. It does not rate the study or mean that another team has repeated its results.`);
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
    const meta = el('div', 'column-meta'); meta.append(el('span', 'column-badge column-badge-update', 'Extra research or product update'), el('span', '', `${s.event_date} · ${signalEvidence[s.evidence_level]} · ${s.temporal_role === 'baseline' ? 'Earlier work for comparison' : 'Update'}`));
    const heading = el('h4'); heading.append(linkToEntry(card.id, s.title));
    card.append(meta, heading, el('p', '', updateSummaries[s.id] || s.after));
    const result = el('p', 'column-update-result'); result.append(el('strong', '', 'Reported result: '), document.createTextNode(s.evidence)); card.append(result);
    const links = el('div', 'column-entry-links'); for (const source of s.sources) primaryLink(links, source.url, source.title); card.append(links);
    card.append(el('p', 'column-missing', s.registry_ids.length ? 'The related resource is listed in another column. This extra explanation is not counted as another paper.' : 'This update is kept separately from the main collection and the items awaiting review. It is not included in their totals.'));
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
  const stagePeriod = stage => stage.start === stage.end ? String(stage.start) : `${stage.start}–${stage.end}`;
  function stageForYear(year) {
    return editorial.columns[theme].evolution.find(stage => stage.start <= year && stage.end >= year);
  }
  function renderEvolution() {
    const box = $('column-evolution'); box.replaceChildren();
    box.append(el('h3', '', 'How this research has changed over time'));
    box.append(el('p', 'column-evolution-intro', 'Our reading of selected work in this collection. Read left to right: what was added, why it matters, and what still needs testing. These are research branches, not a claim that every newer paper beats the previous one.'));
    const controls=el('div','column-time-controls');
    const track=el('ol','column-evolution-track');track.id='column-evolution-track';track.tabIndex=0;track.setAttribute('aria-label','Research stages, earliest first. Scroll horizontally for later stages.');
    for(const [label,direction] of [['Earlier stages',-1],['Later stages',1]]){
      const button=el('button','',label);button.type='button';button.setAttribute('aria-controls',track.id);
      button.onclick=()=>track.scrollBy({left:direction*Math.max(250,track.clientWidth*.8),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});controls.append(button);
    }
    const stageNav=el('nav','column-stage-nav');stageNav.setAttribute('aria-label','Research stages at a glance');
    box.append(stageNav,controls);
    for(const stage of editorial.columns[theme].evolution){
      const card=el('li','column-evolution-stage');card.dataset.start=stage.start;card.dataset.end=stage.end;
      card.id=`column-stage-${stage.start}`;card.tabIndex=-1;
      const jump=href('',`#${card.id}`);jump.append(el('b','',stagePeriod(stage)),el('span','',stage.headline));
      jump.onclick=e=>{e.preventDefault();card.scrollIntoView({block:'nearest',inline:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});card.focus({preventScroll:true});};stageNav.append(jump);
      card.append(el('span','column-stage-period',stagePeriod(stage)),el('h4','',stage.headline),el('p','',stage.change));
      const meaning=el('p','column-stage-meaning');meaning.append(el('strong','','What this adds: '),document.createTextNode(stage.meaning));card.append(meaning);
      const detail=el('details','column-stage-detail');detail.append(el('summary','','Evidence and limits'),el('p','',stage.limit));
      const links=el('div','column-stage-sources');for(const id of stage.ids)links.append(linkToEntry(id));detail.append(links);card.append(detail);track.append(card);
    }
    box.append(track,el('p','column-time-legend','Selected milestones explain the direction; the full year-by-year directory below keeps every resource. Stage notes stay visible when you filter the directory.'));
  }
  function yearOverview() {
    const years = $('column-years'), previousScroll = years.scrollLeft, firstRender = !years.children.length;
    const rows = allTimelineItems().filter(item => matches(item, true));
    const values = [...new Set(allTimelineItems().map(item => item.year))].sort((a,b)=>a-b);
    years.replaceChildren();
    for (const [index, year] of values.entries()) {
      const items = rows.filter(item => item.year===year);
      const accepted = items.filter(item => item.record?.catalog_status==='accepted').length;
      const watchlist = items.filter(item => item.record?.catalog_status==='watchlist').length;
      const reviews = items.filter(item => item.kind==='update').length;
      const a = href('', '?year='+year+'#column-archive-title', 'column-year-tick');
      a.dataset.year = String(year);a.dataset.accepted=String(accepted);a.dataset.watchlist=String(watchlist); a.setAttribute('aria-current', String($('column-year').value===String(year)));
      a.setAttribute('aria-label', `${year}: ${accepted} collected resources, ${watchlist} awaiting review, ${reviews} extra updates. Show this year.`);
      a.append(el('strong','',String(year)));
      const stage=stageForYear(year);
      const example=items.find(item=>item.record?.catalog_status==='accepted');
      const context=stage ? (stage.start===stage.end ? 'Selected research focus' : `Part of the ${stagePeriod(stage)} stage`) : 'Example from the collection';
      a.append(el('span','column-year-context',context),el('span','column-year-focus',stage?.headline || example?.record.contribution || (reviews?'Research or product source updates':'No reviewed summary for this year')));
      a.append(el('span','column-year-count',`${accepted+watchlist} records matching filters`));
      a.append(el('small','',`${accepted} in the collection; ${watchlist} awaiting review`));
      if (reviews) a.append(el('small','',`${reviews} extra updates`));
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
    box.append(el('h3','',`${year} · what this work adds`));
    const stage=stageForYear(Number(year));
    if(stage){
      const note=el('div','column-selected-stage');
      note.append(el('h4','',stage.headline),el('p','',stage.change));
      const meaning=el('p');meaning.append(el('strong','','Compared with earlier examples: '),document.createTextNode(stage.meaning));note.append(meaning);
      note.append(el('p','column-year-limit',`${stage.start!==stage.end ? `This is a summary of ${stagePeriod(stage)}, not a separate trend established for ${year}. ` : ''}${stage.limit}`));
      const links=el('div','column-stage-sources');for(const id of stage.ids)links.append(linkToEntry(id));note.append(links);
      note.append(el('p','column-year-limit','Context for this research stage; not restricted by the directory filters.'));
      box.append(note);
    }
    const examples=rows.filter(item=>item.record?.catalog_status==='accepted'&&item.record.contribution).slice(0,3);
    if(examples.length){
      box.append(el('h4','','Examples published this year'));
      const examplesList=el('ul','column-year-examples');
      for(const item of examples){const li=el('li');li.append(linkToEntry(item.id),el('p','',item.record.contribution));examplesList.append(li);}
      box.append(examplesList,el('p','column-year-limit','Examples follow the directory order, not a ranking. The complete list below includes all matching work.'));
    }
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
    else if(!stage) box.append(el('p','','The collected entries describe individual contributions, but do not establish a year-to-year trend or a comparable performance gain. No such trend is inferred from the resource count.'));
    if(!rows.length)box.append(el('p','','No entries match your current filters. Clear the filters to see this year’s work.'));
  }
  function compactEntry(item) {
    const r=item.record,s=item.signal,row=el('details','column-catalog-row');
    row.id=item.id;
    if(r)row.dataset.recordId=r.id;else row.dataset.signalId=s.id;
    const summary=el('summary'),meta=el('span','column-catalog-meta');
    meta.append(el('span','',String(item.year)),el('span','column-badge',r?typeNames[r.record_type]:'Source review'));
    meta.append(el('span',r?.catalog_status==='watchlist'?'column-badge column-badge-watch':'',r?(r.catalog_status==='watchlist'?'Awaiting review':'In the collection'):signalEvidence[s.evidence_level]));
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
    $('column-result-count').textContent = `Showing ${accepted + watchlist} of ${total} resources: ${accepted} in the collection and ${watchlist} awaiting review. ${primary} have this as their main topic; ${accepted + watchlist - primary} are related resources from other topics. Also showing ${updates} extra research or product updates. All matching titles appear below.`;
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
    if(pageTheme) $('columns-coverage').textContent = `${data.route_counts.accepted[theme].total} resources in the collection. ${data.route_counts.watchlist[theme].total} more awaiting review. Research brief edited ${editorial.edited_on}; individual source dates appear below.`;
    document.title = `${routeOf(theme).label} · Papers & timeline · Awesome Wearable AI`;
    renderNavigation(); renderBrief(); renderEvolution();
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
  $('columns-coverage').textContent = `${data.counts.accepted} resources in the collection. ${data.counts.watchlist} more awaiting review. Each has one main topic; links from other topics do not count it twice. Collection date: ${data.cutoff}. Updates last checked: ${radar.reviewed_on}.`;
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
