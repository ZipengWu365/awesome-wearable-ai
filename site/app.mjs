import {enrich,parseState,serializeState,select,safeURL,toCSV} from './engine.mjs';
const $=id=>document.getElementById(id);
const pretty=s=>String(s).replaceAll('_',' ').replaceAll('-',' ');
const text=v=>typeof v==='object'?JSON.stringify(v,null,2):String(v??'unknown');
const el=(tag,value,cls)=>{const n=document.createElement(tag);if(value!==undefined)n.textContent=value;if(cls)n.className=cls;return n;};
let rows=[],payload,state=parseState(location.hash),page=1,selected=[],opener;
const size=24;
const controls=['q','type','family','tier','modality','scope','weights','twin','entity','evaluation','raw','labels','participants','rate','sort'];
function link(url,title){const a=el('a',title);const safe=safeURL(url);if(safe){a.href=safe;a.target='_blank';a.rel='noopener noreferrer';}return a;}
function fill(id,values){for(const value of [...new Set(values.flat().filter(Boolean))].sort()){const o=el('option',pretty(value));o.value=value;$(id).append(o);}}
function syncControls(){for(const id of controls)$(id).value=state[id]||'';$('watchlist').checked=state.watchlist==='yes';}
function save(){history.replaceState(null,'',serializeState(state));}
function render(){
 selected=select(rows,state);const pages=Math.max(1,Math.ceil(selected.length/size));page=Math.min(page,pages);
 const accepted=selected.filter(r=>r.pool==='accepted').length;
 $('count').textContent=`${selected.length} matching records · ${accepted} accepted · ${selected.length-accepted} watchlist`;
 $('results').replaceChildren();
 for(const r of selected.slice((page-1)*size,page*size)){
  const a=el('article',undefined,'card');const meta=el('div',undefined,'meta');for(const t of [r.pool,r.record_type,r.year])meta.append(el('span',t));a.append(meta);
  const h=el('h2');h.append(link(r.primary_url,r.title));a.append(h,el('p',r.venue||r.status,'venue'),el('p',r.contribution||r.reason));
  if(r.evidence_boundary)a.append(el('p',r.evidence_boundary,'boundary'));
  if(r.twins.length){const tags=el('div',undefined,'tags');for(const t of [...new Set(r.twins.flatMap(p=>[p.application,p.theme_role]))])tags.append(el('span',pretty(t)));a.append(tags);}
  const button=el('button','Details & sources','details-button');button.addEventListener('click',()=>{opener=button;state.record=r.id;save();details(r);});a.append(button);$('results').append(a);
 }
 if(!selected.length)$('results').append(el('p','No matching records. Try fewer filters. Missing release metadata is not evidence of unavailable data.'));
 $('page').textContent=`Page ${page} of ${pages}`;$('previous').disabled=page===1;$('next').disabled=page===pages;$('csv').disabled=!selected.length;$('json').disabled=!selected.length;
}
function listFields(host,object,skip=[]){const dl=el('dl');for(const [k,v] of Object.entries(object)){if(skip.includes(k))continue;dl.append(el('dt',pretty(k)),el('dd',text(v)));}host.append(dl);}
function details(r){
 const host=$('detail-body');host.replaceChildren();$('detail-title').textContent=r.title;host.append(el('p',`${r.pool} · ${r.venue||r.status||''}`),link(r.primary_url,'Primary source'));
 listFields(host,r,['title','primary_url','resource_profiles','causal_profiles','twins']);
 for(const p of r.twins){host.append(el('h3','Digital twin profile'),el('p',p.claim_boundary,'boundary'));listFields(host,p,['record_id','claim_boundary']);showSources(host,p.source_ids);}
 for(const p of r.causal_profiles){host.append(el('h3','Reasoning and intervention profile'));listFields(host,p,['record_id']);showSources(host,p.source_ids);}
 for(const p of r.resource_profiles){
  const m=p.metadata;const section=el('details');section.append(el('summary',`Imported ${m.local_kind} profile · ${m.release_id||p.local_id}`));section.append(el('p','Version-specific source notes from the local catalogue. The accepted record above supplies current publication status; imported unknowns do not override it.'));
  listFields(section,m,['source_ids','field_sources','publication_status','venue','year']);const table=el('dl');for(const [field,ids] of Object.entries(m.field_sources)){table.append(el('dt',pretty(field)));const dd=el('dd');showSources(dd,ids);table.append(dd);}section.append(el('h4','Field-level sources'),table);host.append(section);
 }
 if(!$('detail').open)$('detail').showModal();
}
function showSources(host,ids){for(const id of ids||[]){const s=payload.profiles.sources.find(x=>x.id===id);if(s){const p=el('p');p.append(link(s.url,s.title),el('small',` · source check ${s.accessed_on} · ${s.note}`));host.append(p);}}}
function close(){state.record='';save();$('detail').close();opener?.focus();}
function download(format){const data=format==='json'?JSON.stringify(selected,null,2):toCSV(selected);const url=URL.createObjectURL(new Blob([data],{type:format==='json'?'application/json':'text/csv;charset=utf-8'}));const a=el('a');a.href=url;a.download=`wearable-ai-results.${format}`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
async function init(){
 try{const response=await fetch('registry.json');if(!response.ok)throw new Error(`HTTP ${response.status}`);payload=await response.json();rows=enrich(payload);
  for(const [id,field] of [['type','record_type'],['family','family'],['tier','venue_tier'],['modality','modalities'],['scope','wearable_scope']])fill(id,rows.map(r=>r[field]));
  fill('twin',rows.flatMap(r=>r.twins.map(p=>p.theme_role)));fill('entity',rows.flatMap(r=>r.twins.map(p=>p.entity)));fill('evaluation',rows.flatMap(r=>r.twins.flatMap(p=>p.evaluation)));
  syncControls();render();if(state.record){const r=rows.find(r=>r.id===state.record&&(r.pool==='accepted'||state.watchlist==='yes'));if(r)details(r);}
 }catch(e){$('count').textContent='Could not load catalogue: '+e.message;}
}
for(const id of [...controls,'watchlist'])$(id).addEventListener(['q','participants','rate'].includes(id)?'input':'change',()=>{state[id]=id==='watchlist'?($('watchlist').checked?'yes':''):$(id).value;state.record='';page=1;save();render();});
$('reset').addEventListener('click',()=>{state=parseState();page=1;syncControls();save();render();});$('twins').addEventListener('click',()=>{state=parseState('#twin=any');page=1;syncControls();save();render();});
$('previous').addEventListener('click',()=>{page--;render();});$('next').addEventListener('click',()=>{page++;render();});$('csv').addEventListener('click',()=>download('csv'));$('json').addEventListener('click',()=>download('json'));
$('share').addEventListener('click',async()=>{save();try{await navigator.clipboard.writeText(location.href);$('message').textContent='Query link copied.';}catch{$('message').textContent='Copy the query link from your address bar.';}});
$('close').addEventListener('click',close);$('detail').addEventListener('cancel',e=>{e.preventDefault();close();});addEventListener('hashchange',()=>{state=parseState(location.hash);page=1;syncControls();render();const r=rows.find(r=>r.id===state.record&&(r.pool==='accepted'||state.watchlist==='yes'));if(r)details(r);else $('detail').close();});
init();
