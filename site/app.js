const state = {records: [], watchlist: []};
const $ = (id) => document.getElementById(id);
const unique = (rows, key) => [...new Set(rows.map(x => x[key]).filter(Boolean))].sort();
const fill = (select, values) => values.forEach(value => {
  const option = document.createElement('option'); option.value = value; option.textContent = value; select.appendChild(option);
});
const escapeHtml = (value='') => String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
function render() {
  const q = $('query').value.trim().toLowerCase();
  const type = $('type').value, family = $('family').value, tier = $('tier').value;
  let rows = [...state.records];
  if ($('watchlist').checked) rows = rows.concat(state.watchlist.map(x => ({...x, record_type:'watchlist', family:x.proposed_family || 'unresolved', venue_tier:'watchlist'})));
  rows = rows.filter(row => {
    const haystack = JSON.stringify(row).toLowerCase();
    return (!q || haystack.includes(q)) && (!type || row.record_type === type) && (!family || row.family === family) && (!tier || row.venue_tier === tier);
  });
  $('count').textContent = `${rows.length} matching records${rows.length > 500 ? ' · first 500 shown' : ''}`;
  $('results').innerHTML = rows.slice(0, 500).map(row => `
    <article class="card">
      <div class="meta"><span>${escapeHtml(row.record_type || 'watchlist')}</span><span>${escapeHtml(row.year)}</span><span>${escapeHtml(row.venue_tier || 'watchlist')}</span>${row.evidence_depth ? `<span>${escapeHtml(row.evidence_depth)}</span>` : ''}</div>
      <h2><a href="${escapeHtml(row.primary_url)}" target="_blank" rel="noopener">${escapeHtml(row.title)}</a></h2>
      <p class="venue">${escapeHtml(row.venue || row.status || '')}</p>
      <p>${escapeHtml(row.contribution || row.reason || '')}</p>
      ${row.why_it_matters ? `<p><strong>Why it matters:</strong> ${escapeHtml(row.why_it_matters)}</p>` : ''}
      ${row.limitations ? `<p><strong>Limitations:</strong> ${escapeHtml(row.limitations)}</p>` : ''}
      ${row.evidence_boundary ? `<p><strong>Evidence boundary:</strong> ${escapeHtml(row.evidence_boundary)}</p>` : ''}
      ${row.outcome_status ? `<p><strong>Outcome status:</strong> ${escapeHtml(row.outcome_status)}</p>` : ''}
      <div class="tags">${(row.modalities || []).concat(row.clinical_domains || []).slice(0,10).map(tag => `<span>${escapeHtml(tag)}</span>`).join('')}</div>
    </article>`).join('');
}
fetch('registry.json').then(r => r.json()).then(data => {
  state.records = data.records; state.watchlist = data.watchlist;
  fill($('type'), unique(state.records, 'record_type'));
  fill($('family'), unique(state.records, 'family'));
  fill($('tier'), unique(state.records, 'venue_tier'));
  ['query','type','family','tier','watchlist'].forEach(id => $(id).addEventListener(id === 'query' ? 'input' : 'change', render));
  render();
});
