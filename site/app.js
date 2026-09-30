(() => {
  'use strict';

  const body = document.body;
  const initialHash = location.hash;
  if (initialHash) document.documentElement.style.scrollBehavior = 'auto';
  const steps = [...document.querySelectorAll('.step')];
  const progress = document.querySelector('.story-progress span');
  const story = document.querySelector('.scrolly');
  const menuButton = document.querySelector('.menu-button');
  const navigation = document.querySelector('.site-header nav');

  const activateScene = (step) => {
    const scene = step.dataset.scene;
    if (body.dataset.scene === scene) return;
    body.dataset.scene = scene;
    steps.forEach(item => item.classList.toggle('is-active', item === step));
  };

  steps[0].classList.add('is-active');
  const sceneObserver = new IntersectionObserver((entries) => {
    const candidates = entries
      .filter(entry => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
    if (candidates[0]) activateScene(candidates[0].target);
  }, { rootMargin: '-28% 0px -28% 0px', threshold: [0, .15, .35, .65] });
  steps.forEach(step => sceneObserver.observe(step));

  let progressFrame = null;
  const updateProgress = () => {
    progressFrame = null;
    const rect = story.getBoundingClientRect();
    const travelled = Math.max(0, -rect.top);
    const available = Math.max(1, rect.height - innerHeight);
    progress.style.width = `${Math.min(100, travelled / available * 100)}%`;
  };
  addEventListener('scroll', () => {
    if (!progressFrame) progressFrame = requestAnimationFrame(updateProgress);
  }, { passive: true });
  updateProgress();

  menuButton.addEventListener('click', () => {
    const open = navigation.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.textContent = open ? 'Close' : 'Menu';
  });
  navigation.addEventListener('click', () => {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.textContent = 'Menu';
  });

  const TYPE_ORDER = ['model', 'dataset', 'method', 'measure', 'infrastructure', 'intervention'];
  const TYPE_COLORS = {
    model: '#69adf3',
    dataset: '#69cca3',
    method: '#b093ef',
    measure: '#ef95af',
    infrastructure: '#ebc45f',
    intervention: '#ef9278'
  };

  /* A persistent population, inspired by the reference story's use of the same
     people across scenes. Each scene changes their destination—not their identity. */
  const peopleCanvas = document.querySelector('.people-field');
  if (peopleCanvas) {
    const stage = peopleCanvas.closest('.visual-stage');
    const context = peopleCanvas.getContext('2d');
    const peopleLabel = document.querySelector('#people-field-label');
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
    const peopleColors = Object.values(TYPE_COLORS);
    let width = 0;
    let height = 0;
    let animationFrame = 0;
    let frameCount = 0;
    let people = [];

    const seeded = (seed) => {
      const value = Math.sin(seed * 917.13 + 17.7) * 43758.5453;
      return value - Math.floor(value);
    };

    const svgPoint = (x, y) => {
      const scale = Math.min(width / 1200, height / 800);
      return {
        x: (width - 1200 * scale) / 2 + x * scale,
        y: (height - 800 * scale) / 2 + y * scale
      };
    };

    const clusterSvg = (person, centre, spreadX, spreadY) => {
      const angle = seeded(person.id * 3 + 2) * Math.PI * 2;
      const radius = Math.sqrt(seeded(person.id * 7 + 5));
      return svgPoint(
        centre[0] + Math.cos(angle) * spreadX * radius,
        centre[1] + Math.sin(angle) * spreadY * radius
      );
    };

    const ringSvg = (person, centre, innerRadius, outerRadius) => {
      const angle = seeded(person.id * 5 + 3) * Math.PI * 2;
      const radius = innerRadius + seeded(person.id * 7 + 9) * (outerRadius - innerRadius);
      return svgPoint(
        centre[0] + Math.cos(angle) * radius,
        centre[1] + Math.sin(angle) * radius
      );
    };

    const targetFor = (person, scene) => {
      /* Scenes 0–1 deliberately keep this layer hidden. Its starting point is
         the raw-signal origin, so the population enters through the diagram. */
      if (scene <= 1) return clusterSvg(person, [205, 285], 34, 58);
      if (scene === 2) {
        if (person.id < 36) {
          const progress = person.id / 35;
          return svgPoint(205 + progress * 230, 285 + Math.sin(progress * Math.PI * 8) * (9 + progress * 28));
        }
        const latent = [[780,245],[825,270],[865,224],[911,274],[770,328],[818,345],[872,319],[924,342],[789,409],[847,397],[897,418]];
        return clusterSvg(person, latent[(person.id - 36) % latent.length], 18, 20);
      }
      if (scene === 3) {
        const lifecycle = [[120,411],[240,411],[360,411],[480,411],[600,411],[720,411],[840,411],[960,411],[1080,411]];
        return ringSvg(person, lifecycle[person.id % lifecycle.length], 43, 60);
      }
      if (scene === 4) {
        const ecosystem = [[335,233],[605,175],[871,230],[334,558],[598,626],[879,554]];
        return ringSvg(person, ecosystem[person.id % ecosystem.length], 82, 111);
      }
      if (scene === 5) {
        const evidence = [[210,403],[470,403],[730,403],[990,403]];
        return ringSvg(person, evidence[person.id % evidence.length], 88, 116);
      }
      return {
        x: (person.id % 2 ? 1.08 : -.08) * width,
        y: (.12 + seeded(person.id * 13) * .76) * height
      };
    };

    const retargetPeople = () => {
      const scene = Number(body.dataset.scene || 0);
      people.forEach(person => Object.assign(person, { target: targetFor(person, scene) }));
      if (peopleLabel) {
        const sceneLabels = {
          2: 'People move from raw signals into learned representations',
          3: 'Records gather around nine lifecycle stages',
          4: 'Colours regroup the same records by resource type',
          5: 'Records separate around four evidence questions'
        };
        peopleLabel.textContent = sceneLabels[scene] || 'People become structured evidence';
      }
      if (reducedMotion.matches) {
        people.forEach(person => { person.x = person.target.x; person.y = person.target.y; });
        drawPeople();
      }
    };

    const drawPerson = (person) => {
      const size = width < 700 ? 4.1 : 5.2;
      const bob = reducedMotion.matches ? 0 : Math.sin(frameCount * .025 + person.id) * .55;
      context.save();
      context.translate(person.x, person.y + bob);
      context.globalAlpha = .82;
      context.fillStyle = person.color;
      context.beginPath();
      context.arc(0, -size * .92, size * .42, 0, Math.PI * 2);
      context.fill();
      context.strokeStyle = person.color;
      context.lineWidth = Math.max(1.2, size * .29);
      context.lineCap = 'round';
      context.beginPath();
      context.moveTo(0, -size * .35);
      context.lineTo(0, size * .55);
      context.moveTo(0, -.02 * size);
      context.lineTo(-size * .62, size * .28);
      context.moveTo(0, -.02 * size);
      context.lineTo(size * .62, size * .28);
      context.moveTo(0, size * .5);
      context.lineTo(-size * .46, size * 1.08);
      context.moveTo(0, size * .5);
      context.lineTo(size * .46, size * 1.08);
      context.stroke();
      context.restore();
    };

    function drawPeople() {
      context.clearRect(0, 0, width, height);
      people.forEach(drawPerson);
    }

    const animatePeople = () => {
      frameCount += 1;
      const activeScene = Number(body.dataset.scene || 0);
      people.forEach(person => {
        person.vx += (person.target.x - person.x) * .0045;
        person.vy += (person.target.y - person.y) * .0045;
        person.vx *= .9;
        person.vy *= .9;
        person.x += person.vx;
        person.y += person.vy;
      });
      if (activeScene >= 3 && activeScene <= 5 && frameCount % 2 === 0) {
        for (let i = 0; i < people.length; i += 1) {
          const neighbour = people[(i + 7) % people.length];
          const dx = people[i].x - neighbour.x;
          const dy = people[i].y - neighbour.y;
          const distance = Math.hypot(dx, dy) || 1;
          if (distance < 13) {
            const push = (13 - distance) * .018;
            people[i].vx += dx / distance * push;
            people[i].vy += dy / distance * push;
          }
        }
      }
      drawPeople();
      animationFrame = requestAnimationFrame(animatePeople);
    };

    const sizePeopleField = () => {
      const bounds = stage.getBoundingClientRect();
      width = Math.max(1, bounds.width);
      height = Math.max(1, bounds.height);
      const ratio = Math.min(devicePixelRatio || 1, 2);
      peopleCanvas.width = Math.round(width * ratio);
      peopleCanvas.height = Math.round(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      const count = width < 700 ? 54 : 108;
      if (people.length !== count) {
        people = Array.from({ length: count }, (_, id) => ({
          id,
          color: peopleColors[id % peopleColors.length],
          x: seeded(id + 1) * width,
          y: seeded(id + 101) * height,
          vx: 0,
          vy: 0,
          target: { x: 0, y: 0 }
        }));
      }
      retargetPeople();
    };

    new MutationObserver(retargetPeople).observe(body, { attributes: true, attributeFilter: ['data-scene'] });
    new ResizeObserver(sizePeopleField).observe(stage);
    reducedMotion.addEventListener('change', () => {
      cancelAnimationFrame(animationFrame);
      retargetPeople();
      if (!reducedMotion.matches) animationFrame = requestAnimationFrame(animatePeople);
    });
    sizePeopleField();
    if (!reducedMotion.matches) animationFrame = requestAnimationFrame(animatePeople);
  }
  const MODALITY_GROUPS = {
    motion: { label: 'Motion / IMU', terms: ['imu', 'inertial', 'accelerometer', 'gyroscope', 'motion', 'activity', 'gait', 'pose'] },
    cardiac: { label: 'Cardiac / optical', terms: ['ecg', 'ppg', 'heart-rate', 'heart-rate-variability', 'pulse', 'spo2', 'blood-pressure'] },
    neural: { label: 'Neural / muscle', terms: ['eeg', 'meg', 'ecog', 'ieeg', 'emg', 'neural'] },
    sleep: { label: 'Sleep / PSG', terms: ['sleep', 'psg', 'polysomnography', 'actigraphy'] },
    metabolic: { label: 'Metabolic / CGM', terms: ['cgm', 'glucose', 'insulin', 'glucagon', 'meal'] },
    respiratory: { label: 'Respiratory / audio', terms: ['respiration', 'respiratory', 'audio', 'cough', 'voice'] },
    multimodal: { label: 'Multimodal / general', terms: ['multimodal', 'physiological', 'biosignals', 'time-series', 'waveforms', 'wearable-data'] }
  };
  const YEAR_GROUPS = [
    { key: 'before2015', label: 'Before 2015', test: year => year < 2015 },
    { key: '2015-2019', label: '2015–2019', test: year => year >= 2015 && year < 2020 },
    { key: '2020-2022', label: '2020–2022', test: year => year >= 2020 && year < 2023 },
    { key: '2023-2024', label: '2023–2024', test: year => year >= 2023 && year < 2025 },
    { key: '2025+', label: '2025–2026', test: year => year >= 2025 }
  ];
  const LABELS = {
    model: 'Models', dataset: 'Datasets', method: 'Methods', measure: 'Measures',
    infrastructure: 'Infrastructure', intervention: 'Interventions',
    evidence_card: 'Evidence card', metadata_verified: 'Metadata verified', venue_verified: 'Venue verified'
  };
  const state = { records: [], filtered: [], view: 'map', selected: null };
  const els = {
    search: document.querySelector('#search'),
    type: document.querySelector('#type-filter'),
    modality: document.querySelector('#modality-filter'),
    evidence: document.querySelector('#evidence-filter'),
    year: document.querySelector('#year-filter'),
    group: document.querySelector('#group-filter'),
    count: document.querySelector('#result-count'),
    viewport: document.querySelector('#atlas-viewport'),
    map: document.querySelector('#node-map'),
    list: document.querySelector('#record-list'),
    legend: document.querySelector('.legend'),
    shelf: document.querySelector('#detail-shelf'),
    shelfContent: document.querySelector('.shelf-content'),
    backdrop: document.querySelector('.shelf-backdrop')
  };

  const svgNS = 'http://www.w3.org/2000/svg';
  const createSvg = (name, attrs = {}) => {
    const node = document.createElementNS(svgNS, name);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    return node;
  };
  const titleCase = (value = '') => value.replaceAll('_', ' ').replaceAll('-', ' ').replace(/\b\w/g, char => char.toUpperCase());
  const hash = (value) => {
    let result = 2166136261;
    for (let i = 0; i < value.length; i += 1) result = Math.imul(result ^ value.charCodeAt(i), 16777619);
    return result >>> 0;
  };
  const randomFrom = (value, offset = 0) => {
    const number = hash(`${value}-${offset}`);
    return (number % 10000) / 10000;
  };
  const matchesModality = (record, groupKey) => {
    if (groupKey === 'all') return true;
    const terms = MODALITY_GROUPS[groupKey]?.terms || [];
    const values = [...(record.modalities || []), record.family || ''].map(value => String(value).toLowerCase());
    return values.some(value => terms.some(term => value.includes(term)));
  };
  const matchesYear = (record, groupKey) => {
    if (groupKey === 'all') return true;
    const group = YEAR_GROUPS.find(item => item.key === groupKey);
    return group ? group.test(Number(record.year)) : true;
  };

  const appendOption = (select, value, label) => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = label;
    select.append(option);
  };

  const buildLegend = () => {
    TYPE_ORDER.forEach(type => {
      const item = document.createElement('span');
      const dot = document.createElement('i');
      dot.style.setProperty('--color', TYPE_COLORS[type]);
      item.append(dot, document.createTextNode(LABELS[type]));
      els.legend.append(item);
    });
  };

  const groupsFor = (records, grouping) => {
    if (grouping === 'record_type') return TYPE_ORDER.map(key => ({ key, label: LABELS[key] }));
    if (grouping === 'evidence_depth') {
      return ['evidence_card', 'metadata_verified', 'venue_verified'].map(key => ({ key, label: LABELS[key] }));
    }
    const years = records.map(record => Number(record.year)).filter(Boolean);
    const maxYear = Math.max(...years, 2026);
    return [
      { key: 'before2015', label: 'Before 2015' },
      { key: '2015-2019', label: '2015–19' },
      { key: '2020-2022', label: '2020–22' },
      { key: '2023-2024', label: '2023–24' },
      { key: '2025+', label: `2025–${maxYear}` }
    ];
  };

  const groupKey = (record, grouping) => {
    if (grouping !== 'year') return record[grouping] || 'unknown';
    const year = Number(record.year);
    if (year < 2015) return 'before2015';
    if (year < 2020) return '2015-2019';
    if (year < 2023) return '2020-2022';
    if (year < 2025) return '2023-2024';
    return '2025+';
  };

  const mapPosition = (record, index, groups, grouping) => {
    const groupIndex = Math.max(0, groups.findIndex(group => group.key === groupKey(record, grouping)));
    const columns = groups.length <= 3 ? groups.length : 3;
    const rows = Math.ceil(groups.length / columns);
    const col = groupIndex % columns;
    const row = Math.floor(groupIndex / columns);
    const cellWidth = 1100 / columns;
    const cellHeight = 520 / rows;
    const centreX = cellWidth * (col + .5);
    const centreY = 65 + cellHeight * (row + .5);
    const angle = randomFrom(record.id, index) * Math.PI * 2;
    const radiusX = (28 + Math.sqrt(randomFrom(record.id, index + 4)) * Math.min(135, cellWidth * .34));
    const radiusY = (20 + Math.sqrt(randomFrom(record.id, index + 9)) * Math.min(100, cellHeight * .34));
    return { x: centreX + Math.cos(angle) * radiusX, y: centreY + Math.sin(angle) * radiusY };
  };

  const renderMap = () => {
    els.map.replaceChildren();
    const defs = createSvg('defs');
    const filter = createSvg('filter', { id: 'nodeGlow', x: '-100%', y: '-100%', width: '300%', height: '300%' });
    const shadow = createSvg('feDropShadow', { dx: '0', dy: '0', 'stdDeviation': '6', 'flood-color': '#ffffff', 'flood-opacity': '.7' });
    filter.append(shadow); defs.append(filter); els.map.append(defs);

    const groups = groupsFor(state.filtered, els.group.value);
    groups.forEach((group, index) => {
      const columns = groups.length <= 3 ? groups.length : 3;
      const rows = Math.ceil(groups.length / columns);
      const col = index % columns;
      const row = Math.floor(index / columns);
      const label = createSvg('text', {
        class: 'map-label',
        x: 1100 / columns * (col + .5),
        y: 48 + 520 / rows * row
      });
      const count = state.filtered.filter(record => groupKey(record, els.group.value) === group.key).length;
      label.textContent = `${group.label} · ${count}`;
      els.map.append(label);
    });

    state.filtered.forEach((record, index) => {
      const point = mapPosition(record, index, groups, els.group.value);
      const node = createSvg('g', {
        class: 'map-node', tabindex: '0', role: 'button',
        'aria-label': `${record.title}, ${record.year}, ${record.record_type}`,
        transform: `translate(${point.x.toFixed(1)} ${point.y.toFixed(1)})`
      });
      const dot = createSvg('circle', {
        r: record.evidence_depth === 'evidence_card' ? 7 : 5,
        fill: TYPE_COLORS[record.record_type] || '#ffffff',
        opacity: record.evidence_depth === 'venue_verified' ? '.62' : '.92'
      });
      const title = createSvg('title'); title.textContent = record.title;
      node.append(dot, title);
      node.addEventListener('click', () => openShelf(record));
      node.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openShelf(record); }
      });
      els.map.append(node);
    });
  };

  const truncate = (value = '', length = 155) => value.length > length ? `${value.slice(0, length).trim()}…` : value;
  const asList = value => Array.isArray(value) ? value : (value ? [value] : []);
  const renderList = () => {
    els.list.replaceChildren();
    if (!state.filtered.length) {
      const empty = document.createElement('p');
      empty.className = 'empty-state';
      empty.textContent = 'No records match these filters. Try a broader search.';
      els.list.append(empty);
      return;
    }
    state.filtered.forEach(record => {
      const card = document.createElement('article');
      card.className = 'record-card';
      card.tabIndex = 0;
      const meta = document.createElement('p'); meta.className = 'record-meta';
      meta.textContent = `${LABELS[record.record_type] || titleCase(record.record_type)} · ${record.year} · ${titleCase(record.evidence_depth)}`;
      const heading = document.createElement('h3'); heading.textContent = record.title;
      const description = document.createElement('p'); description.textContent = truncate(record.contribution || record.why_it_matters || 'Open this record to inspect its evidence metadata.');
      card.append(meta, heading, description);
      card.addEventListener('click', () => openShelf(record));
      card.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openShelf(record); }
      });
      els.list.append(card);
    });
  };

  const addShelfBlock = (title, text) => {
    if (!text) return;
    const block = document.createElement('section'); block.className = 'shelf-block';
    const heading = document.createElement('h3'); heading.textContent = title;
    const copy = document.createElement('p'); copy.textContent = text;
    block.append(heading, copy); els.shelfContent.append(block);
  };

  const openShelf = (record) => {
    state.selected = record;
    els.shelfContent.replaceChildren();
    const kicker = document.createElement('p'); kicker.className = 'shelf-kicker';
    kicker.textContent = `${LABELS[record.record_type] || record.record_type} · ${record.year} · ${titleCase(record.evidence_depth)}`;
    const heading = document.createElement('h2'); heading.id = 'detail-title'; heading.textContent = record.title;
    const venue = document.createElement('p'); venue.className = 'shelf-venue'; venue.textContent = [record.venue, titleCase(record.family)].filter(Boolean).join(' · ');
    const tags = document.createElement('div'); tags.className = 'shelf-tags';
    [...asList(record.modalities), ...asList(record.body_locations), ...asList(record.populations), ...asList(record.clinical_domains)].slice(0, 12).forEach(tag => {
      const chip = document.createElement('span'); chip.textContent = titleCase(tag); tags.append(chip);
    });
    els.shelfContent.append(kicker, heading, venue, tags);
    addShelfBlock('Contribution', record.contribution);
    addShelfBlock('Why it matters', record.why_it_matters);
    addShelfBlock('Evidence boundary', record.evidence_boundary);
    addShelfBlock('Limitations', record.limitations);
    const indexing = [
      ['Lifecycle', record.lifecycle_stage],
      ['Evidence stage', record.evidence_stage],
      ['Causal status', record.causal_status],
      ['Study design', record.study_design],
      ['Wearable scope', record.wearable_scope],
      ['Venue tier', record.venue_tier]
    ].filter(([, value]) => value).map(([label, value]) => `${label}: ${titleCase(value)}`).join(' · ');
    addShelfBlock('Atlas indexing', indexing);
    const openness = [
      ['Code', record.open_code],
      ['Weights', record.open_weights],
      ['Data', record.open_data]
    ].map(([label, value]) => `${label}: ${value === true ? 'open' : value === false ? 'not open' : 'not recorded'}`).join(' · ');
    addShelfBlock('Openness', openness);
    addShelfBlock('Verification', `${titleCase(record.verification_status)}${record.verified_on ? ` · ${record.verified_on}` : ''}`);
    if (record.primary_url) {
      const link = document.createElement('a'); link.className = 'shelf-link';
      link.href = record.primary_url; link.target = '_blank'; link.rel = 'noreferrer';
      link.append(document.createTextNode('Open primary source'), document.createTextNode('↗'));
      els.shelfContent.append(link);
    }
    els.shelf.classList.add('is-open');
    els.shelf.setAttribute('aria-hidden', 'false');
    els.backdrop.hidden = false;
    document.querySelector('.shelf-close').focus();
  };

  const closeShelf = () => {
    els.shelf.classList.remove('is-open');
    els.shelf.setAttribute('aria-hidden', 'true');
    els.backdrop.hidden = true;
    state.selected = null;
  };

  const applyFilters = () => {
    const query = els.search.value.trim().toLowerCase();
    state.filtered = state.records.filter(record => {
      if (els.type.value !== 'all' && record.record_type !== els.type.value) return false;
      if (!matchesModality(record, els.modality.value)) return false;
      if (els.evidence.value !== 'all' && record.evidence_depth !== els.evidence.value) return false;
      if (!matchesYear(record, els.year.value)) return false;
      if (!query) return true;
      const searchFields = [record.title, record.short_name, record.venue, record.family, record.contribution,
        record.evidence_boundary, record.lifecycle_stage, record.study_design, record.evidence_stage, record.causal_status,
        record.wearable_scope, record.venue_tier, ...asList(record.modalities), ...asList(record.body_locations),
        ...asList(record.populations), ...asList(record.clinical_domains), ...asList(record.tags)];
      return searchFields.filter(Boolean).join(' ').toLowerCase().includes(query);
    });
    els.count.textContent = state.filtered.length;
    renderMap();
    renderList();
  };

  document.querySelectorAll('[data-view]').forEach(button => {
    button.addEventListener('click', () => {
      state.view = button.dataset.view;
      document.querySelectorAll('[data-view]').forEach(item => item.classList.toggle('is-active', item === button));
      els.viewport.classList.toggle('map-view', state.view === 'map');
      els.viewport.classList.toggle('list-view', state.view === 'list');
    });
  });
  [els.search, els.type, els.modality, els.evidence, els.year].forEach(control => control.addEventListener(control === els.search ? 'input' : 'change', applyFilters));
  els.group.addEventListener('change', renderMap);
  document.querySelector('.shelf-close').addEventListener('click', closeShelf);
  els.backdrop.addEventListener('click', closeShelf);
  addEventListener('keydown', event => {
    if (event.key === 'Escape' && state.selected) closeShelf();
    if (event.key === '/' && document.activeElement?.tagName !== 'INPUT') {
      event.preventDefault(); els.search.focus(); document.querySelector('#explore').scrollIntoView();
    }
  });

  buildLegend();
  fetch('registry.json')
    .then(response => {
      if (!response.ok) throw new Error(`Registry request failed: ${response.status}`);
      return response.json();
    })
    .then(data => {
      state.records = data.records || [];
      TYPE_ORDER.forEach(type => appendOption(els.type, type, `${LABELS[type]} (${state.records.filter(record => record.record_type === type).length})`));
      Object.entries(MODALITY_GROUPS).forEach(([key, group]) => {
        const count = state.records.filter(record => matchesModality(record, key)).length;
        appendOption(els.modality, key, `${group.label} (${count})`);
      });
      ['evidence_card', 'metadata_verified', 'venue_verified'].forEach(depth => {
        appendOption(els.evidence, depth, `${LABELS[depth]} (${state.records.filter(record => record.evidence_depth === depth).length})`);
      });
      YEAR_GROUPS.forEach(group => {
        const count = state.records.filter(record => group.test(Number(record.year))).length;
        appendOption(els.year, group.key, `${group.label} (${count})`);
      });
      applyFilters();
    })
    .catch(error => {
      console.error(error);
      els.count.textContent = '—';
      const message = document.createElement('p'); message.className = 'empty-state';
      message.textContent = 'The atlas data could not be loaded. Serve this folder with a local web server and try again.';
      els.list.append(message);
    });

  addEventListener('load', () => {
    if (!initialHash) return;
    const target = document.querySelector(initialHash);
    if (target) window.scrollTo(0, target.offsetTop - 70);
    requestAnimationFrame(() => { document.documentElement.style.scrollBehavior = ''; });
  });
})();
