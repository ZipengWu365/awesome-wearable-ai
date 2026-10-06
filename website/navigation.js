(() => {
  'use strict';
  const page = location.pathname.split('/').pop() || 'index.html';
  const groups = {'prediction.html':'columns.html','intervention.html':'columns.html','digital-twins.html':'columns.html','mixed-reality.html':'columns.html','research-map.html':'columns.html','story.html':'guide.html','models.html':'guide.html','history.html':'guide.html','compare.html':'library.html'};
  document.querySelectorAll('.site-header nav a').forEach(a => {
    if (a.getAttribute('href') === (groups[page] || page)) a.setAttribute('aria-current','page');
  });
  const button = document.querySelector('.menu-button'), nav = document.querySelector('.site-header nav');
  function close() { nav?.classList.remove('is-open'); button?.setAttribute('aria-expanded','false'); if (button) button.textContent='Menu'; }
  button?.addEventListener('click', () => { const open=nav.classList.toggle('is-open'); button.setAttribute('aria-expanded',String(open)); button.textContent=open?'Close':'Menu'; });
  nav?.addEventListener('click', e => { if (e.target.closest('a')) close(); });
  if(page==='compare.html'){
    const selected=new URLSearchParams(location.search).get('panel')||'lifecycle';
    const panels=[...document.querySelectorAll('[data-comparison-panel]')];
    const active=panels.some(p=>p.dataset.comparisonPanel===selected)?selected:'lifecycle';
    panels.forEach(p=>p.hidden=p.dataset.comparisonPanel!==active);
    document.querySelectorAll('.resource-tabs a').forEach(a=>{if(new URL(a.href).searchParams.get('panel')===active)a.setAttribute('aria-current','page');});
  }
  document.addEventListener('keydown', e => { if (e.key==='Escape' && nav?.classList.contains('is-open')) {close();button.focus();} });
  // Previously shared section links now resolve to the owning public page.
  if (page==='index.html' && location.hash && window.ATLAS_ANCHOR_PAGES) {
    let key;try{key=decodeURIComponent(location.hash.slice(1));}catch{return;}
    const target=window.ATLAS_ANCHOR_PAGES[key];
    if (target && target!=='index.html') location.replace(target + (key.startsWith('trend-') || ['intelligence','comparison-lab','community'].includes(key) ? '' : location.hash));
  }
})();
