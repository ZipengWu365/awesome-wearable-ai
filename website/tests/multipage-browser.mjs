// Run with a local static server and Firefox WebDriver BiDi on port 9222.
import assert from 'node:assert/strict';
import {mkdirSync,writeFileSync} from 'node:fs';
const base=process.env.ATLAS_TEST_URL||'http://127.0.0.1:8765';
const socket=new WebSocket(process.env.ATLAS_BIDI_URL||'ws://127.0.0.1:9222/session');
const output='/tmp/awa-multipage-audit';mkdirSync(output,{recursive:true});
let seq=0;const pending=new Map(),errors=[];
const done=new Promise((resolve,reject)=>{socket.addEventListener('close',resolve);socket.addEventListener('error',reject);});
const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});
socket.addEventListener('message',event=>{const m=JSON.parse(event.data);if(m.method==='log.entryAdded'&&m.params.level==='error'&&m.params.type==='javascript')errors.push(m.params.text);const p=pending.get(m.id);if(!p)return;pending.delete(m.id);m.type==='error'?p.reject(new Error(JSON.stringify(m))):p.resolve(m.result);});
socket.addEventListener('open',async()=>{try{
  await send('session.new',{capabilities:{}});await send('session.subscribe',{events:['log.entryAdded']});
  const {contexts}=await send('browsingContext.getTree');const context=contexts.find(c=>c.url.includes('8765'))?.context||contexts[0].context;
  const evaluate=async expression=>{const r=await send('script.evaluate',{expression,target:{context},awaitPromise:true});if(r.type==='exception')throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  const json=async expr=>JSON.parse(await evaluate('JSON.stringify('+expr+')'));
  const pause=ms=>new Promise(r=>setTimeout(r,ms));
  const navigate=async path=>{try{await send('browsingContext.navigate',{context,url:base+'/'+path,wait:'complete'});}catch(error){if(!path.startsWith('index.html#')||!String(error).includes('NS_BINDING_ABORTED'))throw error;}await pause(180);};
  const screenshot=async name=>{const r=await send('browsingContext.captureScreenshot',{context,origin:'viewport'});writeFileSync(output+'/'+name+'.png',Buffer.from(r.data,'base64'));};
  const files=['index.html','columns.html','guide.html','story.html','models.html','history.html','evidence.html','library.html','compare.html','prediction.html','intervention.html','digital-twins.html','mixed-reality.html'];
  for(const file of files){
    await navigate(file);await pause(200);
    const nav=await json(`[...document.querySelectorAll('.site-header nav a')].map(a=>a.getAttribute('href'))`);
    assert(nav.length>=5,file+' navigation missing');assert(nav.every(a=>!a.startsWith('#')),file+' main navigation must change pages');
    assert.equal(await evaluate(`document.querySelectorAll('.site-header nav a[aria-current="page"]').length`),1,file+' active nav');
    if(file==='index.html')assert.equal(await evaluate(`!!document.querySelector('.scrolly,#intelligence,#explore')`),false,'Home must not embed the long site');
    for(const width of [1440,768,390,320]){
      await send('browsingContext.setViewport',{context,viewport:{width,height:960},devicePixelRatio:1});await pause(120);
      const bounds=await json(`({width:innerWidth,scroll:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})`);
      assert(bounds.scroll<=width+1,file+' overflow '+JSON.stringify(bounds));
      if(width===390){await evaluate(`document.querySelector('.menu-button').click();true`);assert.equal(await evaluate(`document.querySelector('.menu-button').getAttribute('aria-expanded')`),'true',file+' menu open; errors: '+JSON.stringify(errors));await evaluate(`document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));true`);assert.equal(await evaluate(`document.querySelector('.menu-button').getAttribute('aria-expanded')`),'false',file+' menu close');}
      if(['index.html','columns.html','prediction.html'].includes(file)&&[1440,390].includes(width)){await evaluate('window.scrollTo(0,0);true');await screenshot(file.replace('.html','')+'-'+width);}
    }
    console.log('PASS page',file,'4 viewport sizes; real navigation; mobile menu');
  }
  const allIds=new Set(),themeFiles={prediction:'prediction.html',intervention:'intervention.html',twin:'digital-twins.html',interface:'mixed-reality.html'};
  for(const [theme,file] of Object.entries(themeFiles)){
    await navigate(file);
    const primaryTree=await json(`[...document.querySelectorAll('.tree-leaf')].filter(n=>n.dataset.related==='false'&&!n.dataset.treeId.startsWith('signal-')).map(n=>n.dataset.treeId).sort()`);
    const primaryRegistry=await json(`JSON.parse(document.getElementById('research-data').textContent).records.filter(r=>r.primary_route==='${theme}').map(r=>r.id).sort()`);
    assert.deepEqual(primaryTree,primaryRegistry,'Tree preserves every primary entry in '+theme);
    await evaluate(`document.querySelector('.tree-toolbar button').click();true`);await pause(150);
    assert.equal(await evaluate(`[...document.querySelectorAll('.tree-leaf')].every(n=>n.getClientRects().length>0)`),true,'Show every leaf reveals all names');
    await evaluate(`document.querySelector('.tree-leaf').click();true`);
    assert.equal(await evaluate(`document.querySelector('.tree-dialog').open`),true,'Leaf opens an immediate article summary');
    assert.equal(await evaluate(`document.querySelector('.tree-dialog h2').textContent.length>0`),true,'Popup names the actual work');
    assert.equal(await evaluate(`[...document.querySelectorAll('.tree-dialog a')].every(a=>!a.href.includes('/pdf/')&&!/\.pdf([?#]|$)/i.test(a.href))`),true,'Article links use landing pages');
    await evaluate(`document.querySelector('.tree-dialog-close').click();document.querySelector('.tree-toolbar button').click();true`);
    await evaluate(`document.querySelector('.tree-related input').click();true`);await pause(120);
    assert.equal(await evaluate(`[...document.querySelectorAll('.tree-leaf')].filter(n=>n.dataset.related==='true').length===JSON.parse(document.querySelector('#research-data').textContent).records.filter(r=>r.primary_route!=='${theme}'&&r.secondary_routes.includes('${theme}')).length`),true,'Related tree entries follow repository cross-links');
    await evaluate(`document.querySelector('.tree-related input').click();true`);
    const branch=await evaluate(`document.querySelector('.tree-toolbar select option:nth-child(2)').value`);
    await evaluate(`document.querySelector('.tree-toolbar select').value=${JSON.stringify(branch)};document.querySelector('.tree-toolbar select').dispatchEvent(new Event('change'));true`);
    assert.equal(await evaluate(`[...document.querySelectorAll('.tree-branch-box')].every(n=>n.dataset.branch===${JSON.stringify(branch)})`),true,'Branch filter matches the tree');
    await evaluate(`document.querySelector('.tree-toolbar select').value='';document.querySelector('.tree-toolbar select').dispatchEvent(new Event('change'));true`);
    for(const width of [1440,390]){await send('browsingContext.setViewport',{context,viewport:{width,height:960},devicePixelRatio:1});await evaluate(`document.querySelector('#column-tree').scrollIntoView({block:'start',behavior:'instant'});true`);await pause(150);await screenshot(theme+'-tree-'+width);assert.equal(await evaluate(`document.documentElement.scrollWidth<=innerWidth+1`),true,'Tree remains within the page');}
    assert.equal(await evaluate(`(()=>{const boxes=[...document.querySelectorAll('.tree-branch-box')];return boxes.every(box=>[...box.querySelectorAll('.tree-leaf')].filter(n=>n.getClientRects().length).every(n=>{const a=n.getBoundingClientRect(),b=box.getBoundingClientRect();return a.left>=b.left&&a.right<=b.right+1;}));})()`),true,'Leaf text stays inside its branch box');
    assert.equal(await evaluate(`document.querySelectorAll('.column-change').length`),3,'Three concrete change summaries per theme');
    assert.equal(await evaluate(`document.querySelector('#column-dimensions').textContent`),'2 · What is new, and what has been tested?','Separate questions from the overall direction');
    assert.equal(await evaluate(`[...document.querySelectorAll('.column-dimension')].every(n=>n.querySelector('h4').textContent.endsWith('?')&&n.querySelector('.column-dimension-answer').textContent&&n.querySelector('.column-dimension-basis').textContent)`),true,'Questions have direct answers and explicit evidence scope');
    assert.equal(await evaluate(`document.querySelectorAll('.column-brief-key').length`),0,'Do not present a single example as the overall trend');
    assert.equal(await evaluate(`document.querySelectorAll('.column-dimension').length`),6,'All six reader questions addressed');
    assert.equal(await evaluate(`document.querySelectorAll('.column-study-comparison').length`),3,'Every featured work has comparison and limits');
    assert.equal(await evaluate(`document.querySelectorAll('.column-trend-sources a').length>=2`),true,'Trend supported by several works');
    assert.equal(await evaluate(`[...document.querySelectorAll('.column-study-links a:first-child')].every(a=>a.href.startsWith('https://'))`),true,'Direct primary-source links');
    assert.equal(await evaluate(`[...document.querySelectorAll('.column-change h4,.column-change p')].every(n=>!/[→↗↓↑]/.test(n.textContent))`),true,'Explain comparisons with words, not arrows');
    assert.equal(await evaluate(`document.querySelector('#columns-coverage')===null`),true,'No resource-count line above the column');
    assert.equal(await evaluate(`document.querySelector('#column-title').textContent===document.querySelector('#columns-nav [aria-current="page"] b').textContent`),true,'Column title describes its scope, not one example');
    assert.equal(await evaluate(`document.querySelector('.column-background').open`),false,'Background must not obscure current changes');
    assert.equal(await evaluate(`document.querySelectorAll('.column-evolution-stage').length>=2`),true,'Research history explains several stages');
    assert.equal(await evaluate(`[...document.querySelectorAll('.column-evolution-stage')].every(n=>n.querySelector('.column-stage-meaning').textContent.length>50&&n.querySelector('.column-stage-sources a'))`),true,'Every stage explains its contribution and links evidence');
    assert.equal(await evaluate(`document.querySelectorAll('.column-year-bar').length`),0,'Do not present resource volume as the research trend');
    assert.equal(await evaluate(`(()=>{const d=JSON.parse(document.querySelector('#research-data').textContent),ids=new Set([...d.records.map(r=>r.id),...d.radar.signals.map(s=>'signal-'+s.id)]);return [...document.querySelectorAll('.column-change a,.column-dimension a,.column-trend-sources a')].filter(a=>a.hash).every(a=>ids.has(decodeURIComponent(a.hash.slice(1))));})()`),true,'Brief links to genuine records');
    const expected=await json(`JSON.parse(document.getElementById('research-data').textContent).records.filter(r=>r.primary_route==='${theme}').map(r=>r.id).sort()`);
    await evaluate(`document.querySelector('#column-related').click();true`);
    const collected=await json(`[...document.querySelectorAll('[data-record-id]')].map(n=>n.dataset.recordId)`);
    assert.deepEqual(collected.sort(),expected,theme+' exact complete directory coverage');for(const id of collected){assert(!allIds.has(id),'Duplicate primary ID');allIds.add(id);}
    assert.equal(await evaluate(`document.querySelectorAll('.column-pagination').length`),0,'No hidden pages');
    const years=await json(`[...document.querySelectorAll('.column-year-tick')].map(n=>Number(n.dataset.year))`);
    assert.deepEqual(years,[...years].sort((a,b)=>a-b),'Horizontal years must be chronological');
    assert.equal(await evaluate(`[...document.querySelectorAll('.column-year-tick')].reduce((sum,n)=>sum+Number(n.dataset.accepted)+Number(n.dataset.watchlist),0)`),expected.length,'Bars count all primary records exactly');
    for(const y of years){
      await evaluate(`document.querySelector('.column-year-tick[data-year="${y}"]').click();true`);
      assert.equal(await evaluate(`document.querySelector('#column-year-insights').textContent.includes('what this work adds')`),true,'Year selection explains contributions');
      assert.equal(await evaluate(`(()=>{const expected=JSON.parse(document.querySelector('#research-data').textContent).records.filter(r=>r.primary_route==='${theme}'&&r.year===${y}).map(r=>r.id).sort();const actual=[...document.querySelectorAll('[data-record-id]')].map(n=>n.dataset.recordId).sort();return JSON.stringify(actual)===JSON.stringify(expected)})()`),true,'Exact IDs for '+theme+' '+y);
    }
    const year=years.at(-1);
    await evaluate(`document.querySelector('.column-year-tick[data-year="${year}"]').click();true`);
    const expectedYear=await json(`JSON.parse(document.getElementById('research-data').textContent).records.filter(r=>r.primary_route==='${theme}'&&r.year===${year}).map(r=>r.id).sort()`);
    assert.deepEqual(await json(`[...document.querySelectorAll('[data-record-id]')].map(n=>n.dataset.recordId).sort()`),expectedYear,'Every selected-year title visible');
    assert.equal(await evaluate(`document.querySelector('.column-year-tick[data-year="${year}"]').getAttribute('aria-current')`),'true');
    await evaluate(`document.querySelector('#column-all-years').click();true`);
    assert.equal(await evaluate(`document.querySelectorAll('[data-record-id]').length`),expected.length);
    await evaluate(`document.querySelector('#column-reset').click();document.querySelector('#column-query').value='no-match-xyz-123';document.querySelector('#column-query').dispatchEvent(new Event('input'));true`);
    assert.equal(await evaluate(`!!document.querySelector('.column-empty')`),true);await evaluate(`document.querySelector('.column-empty button').click();true`);assert.equal(await evaluate(`document.querySelectorAll('.column-pagination').length`),0);
    for(const width of [1440,390]){await send('browsingContext.setViewport',{context,viewport:{width,height:960},devicePixelRatio:1});await evaluate(`document.querySelector('#column-evolution').scrollIntoView({block:'start',behavior:'instant'});true`);await pause(150);await screenshot(theme+'-evolution-'+width);assert.equal(await evaluate(`document.documentElement.scrollWidth<=innerWidth+1`),true);await evaluate(`document.querySelector('.column-time-overview').scrollIntoView({block:'start',behavior:'instant'});true`);await pause(150);await screenshot(theme+'-timeline-'+width);assert.equal(await evaluate(`document.documentElement.scrollWidth<=innerWidth+1`),true);}
    const featuredIds=await json(`[...document.querySelectorAll('[data-featured-id]')].map(n=>n.dataset.featuredId)`);
    for(const id of featuredIds){await navigate(file+'#'+encodeURIComponent(id));await pause(80);assert.equal(await evaluate(`document.getElementById(${JSON.stringify(id)})?.open`),true,'Featured entry opens: '+id);}
    await navigate(file);await send('browsingContext.setViewport',{context,viewport:{width:1440,height:960},devicePixelRatio:1});
    await evaluate(`document.querySelector('#column-dimensions').scrollIntoView({block:'start',behavior:'instant'});true`);await pause(120);await screenshot(theme+'-brief-comparisons');
    console.log('PASS complete horizontal timeline',theme,expected.length,'primary records; every year and title accessible');
  }
  assert.equal(allIds.size,441);
  await navigate('prediction.html#dataset-mitbih-arrhythmia');await pause(200);assert.equal(await evaluate(`document.querySelector('#dataset-mitbih-arrhythmia .column-record-detail').open`),true,'Deep link opens a later-page record');
  await navigate('digital-twins.html#signal-aid-twin-baseline-2025');assert.equal(await evaluate(`document.getElementById('signal-aid-twin-baseline-2025').open`),true,'Linked review opens');
  await navigate('prediction.html?year=2024&page=2#column-archive-title');assert.equal(await evaluate(`document.querySelector('#column-year').value`),'2024','Old pagination links retain year');
  await evaluate(`document.querySelector('.column-year-tick[data-year="2025"]').click();history.back();true`);await pause(180);assert.equal(await evaluate(`document.querySelector('#column-year').value`),'2024','Back restores year');
  await navigate('prediction.html');await evaluate(`document.querySelector('#columns-nav a[href="digital-twins.html"]').click();true`);await pause(250);assert.equal(await evaluate(`location.pathname.endsWith('/digital-twins.html')`),true,'Theme changes actual page');
  await navigate('index.html#explore');await pause(250);assert.equal(await evaluate(`location.pathname.endsWith('/library.html')`),true,'Old homepage link redirects');
  await navigate('models.html');await pause(200);await evaluate(`document.querySelector('.family-node[data-family]').click();true`);await pause(350);assert.equal(await evaluate(`location.pathname.endsWith('/library.html')&&new URLSearchParams(location.search).get('type')==='model'`),true,'Family opens library filter');
  for(const panel of ['lifecycle','families','datasets','evidence','watchlist','downloads']){await navigate('compare.html?panel='+panel);assert.deepEqual(await json(`[...document.querySelectorAll('[data-comparison-panel]')].filter(n=>!n.hidden).map(n=>n.dataset.comparisonPanel)`),[panel]);}
  await navigate('library.html');await pause(300);assert.equal(await evaluate(`document.querySelector('#result-count').textContent`),'396');await evaluate(`document.querySelector('[data-view="list"]').click();document.querySelector('.record-card').click();true`);assert.equal(await evaluate(`document.querySelector('#detail-shelf').classList.contains('is-open')`),true);
  await navigate('story.html');assert.equal(await evaluate(`document.querySelectorAll('.step').length`),6);
  for(let n=0;n<6;n++){await evaluate(`document.querySelectorAll('.step')[${n}].scrollIntoView({block:'center',behavior:'instant'});true`);await pause(180);assert.equal(await evaluate(`document.querySelectorAll('.step.is-active').length`),1);}
  await navigate('research-map.html?view=map');assert.equal(await evaluate(`document.querySelector('.atlas').hidden`),false);
  assert.deepEqual(errors,[]);console.log('PASS 441 IDs; navigation; filters; horizontal years; complete directory; legacy links; graph links; 6 scenes; no page JS errors');
  await send('session.end');socket.close();
}catch(error){console.error(error);process.exitCode=1;try{await send('session.end');}catch{}socket.close();}});
await done;
