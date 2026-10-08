/* A chronological research tree. Branches are repository families, not claims
   that one paper descended from another. All collected entries remain accessible. */
(() => {
  'use strict';
  let dispose = () => {};
  const make=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
  const svgNode=tag=>document.createElementNS('http://www.w3.org/2000/svg',tag);
  const statuses={evidence_card:'Study summary available',metadata_verified:'Publication details checked',venue_verified:'Venue details checked'};
  const types={model:'Model',dataset:'Dataset',measure:'Health measure',method:'Method',intervention:'Intervention',infrastructure:'Tool or standard'};
  window.renderResearchTree = ({data,theme,label,records,signals,jumpTo}) => {
    dispose();
    const root=document.getElementById('column-tree');root.replaceChildren();
    const tree=data.tree.columns[theme],periods=data.tree.periods;
    let showRelated=false,allOpen=false,selectedBranch='',query='',fontScale=1,frame=0,anchorPeriod='',lastWidth=0;
    const heading=make('div','tree-heading');const headingText=make('div');
    const title=make('h2','','Research by topic and year');title.id='tree-title';
    headingText.append(make('p','columns-kicker','RESEARCH TREE · '+label.toUpperCase()),title,make('p','','Recent periods are shown first. Choose an earlier period to trace the history. Each branch groups a research topic; click a work to read its summary and source.'));
    heading.append(headingText);root.append(heading);
    const toolbar=make('div','tree-toolbar');
    const searchLabel=make('label','','Find a work');const search=make('input');search.type='search';search.placeholder='Name, signal or contribution';searchLabel.append(search);
    const branchLabel=make('label','','Research branch');const select=make('select');
    const allOption=make('option','','All branches');allOption.value='';select.append(allOption);
    for(const branch of tree.branches.filter(b=>b.id!=='related')){const option=make('option','',branch.label);option.value=branch.id;select.append(option);}branchLabel.append(select);
    const toggle=make('button','','Show all entries');toggle.type='button';toggle.setAttribute('aria-pressed','false');
    const larger=make('button','','Larger text');larger.type='button';larger.setAttribute('aria-pressed','false');
    const relatedLabel=make('label','tree-related');const related=make('input');related.type='checkbox';relatedLabel.append(related,document.createTextNode('Include related work from other columns'));
    toolbar.append(searchLabel,branchLabel,toggle,larger,relatedLabel);root.append(toolbar);
    const timeNav=make('nav','tree-time-nav');timeNav.setAttribute('aria-label','Jump to a research-tree period');root.append(timeNav);
    const viewport=make('div','tree-viewport');viewport.tabIndex=0;viewport.setAttribute('aria-label','Horizontal research tree. Scroll sideways to move through time.');
    const chart=make('div','tree-chart');const wires=svgNode('svg');wires.classList.add('tree-wires');wires.setAttribute('aria-hidden','true');chart.append(wires);viewport.append(chart);root.append(viewport);
    const legend=make('details','tree-branch-guide');legend.append(make('summary','','What each branch covers'));root.append(legend);
    const legendItems=make('div','tree-legend');legend.append(legendItems);
    for(const branch of tree.branches.filter(b=>b.id!=='related')){const item=make('div');item.style.setProperty('--branch',branch.color);item.append(make('b','',branch.label),make('p','',branch.summary));legendItems.append(item);}
    const note=make('p','tree-note','The overview shows selected names and keeps the other topics compact. Expand any branch to read every name. Solid borders mark collected resources; dashed borders mark work awaiting review; double borders mark separate research or product updates. Lines connect topics to periods, not papers to their predecessors. Periods have equal width.');root.append(note);
    const status=make('p','tree-status');status.setAttribute('role','status');status.setAttribute('aria-live','polite');root.append(status);
    const dialog=make('dialog','tree-dialog');dialog.setAttribute('aria-labelledby','tree-dialog-title');document.body.append(dialog);
    const close=make('button','tree-dialog-close','Close');close.type='button';close.onclick=()=>dialog.close();
    const dialogContent=make('div','tree-dialog-content');dialog.append(close,dialogContent);
    dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
    const detailsFor = node => {
      const record=records.get(node.id),signal=signals.get(node.id.replace(/^signal-/,''));
      return {record,signal,title:record?.title||signal?.title,name:record?.short_name||signal?.title.split(':')[0]||record?.title,
        year:record?.year||Number(signal.event_date.slice(0,4)),text:record?.contribution||record?.reason||signal?.after||''};
    };
    const primaryLink=(container,text,url)=>{if(!/^https?:\/\//i.test(url||''))return;const a=make('a','',text);a.href=url;a.target='_blank';a.rel='noopener noreferrer';container.append(a);};
    const openNode=node=>{
      const {record:r,signal:s,title,year,text}=detailsFor(node);dialogContent.replaceChildren();
      dialogContent.append(make('p','tree-node-kind',`${year} · ${r?(r.catalog_status==='watchlist'?'Awaiting review':types[r.record_type]||'Resource'):(s.evidence_level==='vendor_announcement'?'Company announcement':'Additional research update')}${node.related?' · Related work from another column':''}`));
      const h=make('h2','',title);h.id='tree-dialog-title';dialogContent.append(h,make('p','tree-node-contribution',text));
      const add=(label,value)=>{if(value){dialogContent.append(make('h3','',label),make('p','',value));}};
      add('Why this work matters',r?.why_it_matters);
      add('What was tested',r?.study_design);add('Reported result',r?.outcome_status||s?.evidence);
      add('Study limits',r?.limitations);add('How to read this result',r?.evidence_boundary||s?.limit);
      if(r?.link_withheld)add('Source note',r.source_issue);
      const links=make('div','tree-dialog-links');
      if(r){if(!r.link_withheld)primaryLink(links,'Open paper or resource page',r.primary_url);primaryLink(links,'Code',r.code_url);primaryLink(links,'Data',r.data_url);}
      else for(const source of s.sources)primaryLink(links,source.title,source.url);
      if(r)for(const update of data.radar.signals.filter(s=>s.registry_ids.includes(r.id))){
        add('Additional source review',update.title);add('Earlier approach',update.before);add('What changed',update.after);
        add('Reported evidence',update.evidence);add('What this does not establish',update.limit);
        for(const source of update.sources)primaryLink(links,source.title,source.url);
      }
      const full=make('button','','Read the complete entry');full.type='button';full.onclick=()=>{dialog.close();jumpTo(node.id,true);};links.append(full);dialogContent.append(links);
      if(r?.evidence_depth)dialogContent.append(make('p','tree-source-note',statuses[r.evidence_depth]||r.evidence_depth));
      dialog.showModal();close.focus();
    };
    function leaf(node){
      const {record,signal,name,title,year,text}=detailsFor(node);
      const button=make('button','tree-leaf');button.type='button';button.dataset.treeId=node.id;
      button.dataset.related=String(node.related);button.dataset.treeStatus=record?.catalog_status||'update';
      const label=make('span','tree-leaf-name',name);const kind=record?(record.catalog_status==='watchlist'?'Awaiting review':types[record.record_type]||'Resource'):(signal.evidence_level==='vendor_announcement'?'Product announcement':'Research update');const mark=make('span','tree-leaf-mark',String(year));
      button.append(label,mark);button.title=`${year} · ${title}\n${text}`;
      button.setAttribute('aria-label',`${name}, ${year}. ${node.related?'Related work. ':''}${kind}. Open summary.`);button.onclick=()=>openNode(node);return button;
    }
    function scheduleLines(){cancelAnimationFrame(frame);frame=requestAnimationFrame(drawLines);}
    function drawLines(){
      const columns=[...chart.querySelectorAll('.tree-period')];if(!columns.length){wires.replaceChildren();return;}
      if(lastWidth&&lastWidth!==viewport.clientWidth){const anchor=columns.find(c=>c.dataset.treePeriod===anchorPeriod);if(anchor)viewport.scrollLeft=anchor.offsetLeft-30;}
      lastWidth=viewport.clientWidth;
      const visible=columns.filter(c=>Math.min(c.offsetLeft+c.offsetWidth,viewport.scrollLeft+viewport.clientWidth)-Math.max(c.offsetLeft,viewport.scrollLeft)>Math.min(c.offsetWidth,viewport.clientWidth)*.25);
      const topHeight=Math.max(80,...(visible.length?visible:columns).map(c=>c.querySelector('.tree-top-stack').getBoundingClientRect().height));
      chart.style.setProperty('--tree-top-height',topHeight+'px');
      const width=chart.offsetWidth,height=chart.offsetHeight,base=chart.getBoundingClientRect();
      wires.setAttribute('width',width);wires.setAttribute('height',height);wires.setAttribute('viewBox',`0 0 ${width} ${height}`);wires.replaceChildren();
      const point=n=>{const r=n.getBoundingClientRect();return{x:r.left-base.left+r.width/2,y:r.top-base.top+r.height/2};};
      const hubs=columns.map(c=>point(c.querySelector('.tree-hub')));
      const trunk=svgNode('path');trunk.setAttribute('d',`M 18 ${hubs[0].y} L ${width-18} ${hubs[0].y}`);trunk.setAttribute('class','tree-trunk');wires.append(trunk);
      for(const [index,col] of columns.entries()){
        const hub=hubs[index];
        for(const box of col.querySelectorAll('.tree-branch-box')){
          const r=box.getBoundingClientRect(),top=box.closest('.tree-top-stack'),x=r.left-base.left+r.width*.32,y=(top?r.bottom:r.top)-base.top;
          const path=svgNode('path');path.dataset.branch=box.dataset.branch;path.style.stroke=box.style.getPropertyValue('--branch');
          path.setAttribute('d',`M ${hub.x} ${hub.y} C ${hub.x+18} ${(hub.y+y)/2}, ${x-20} ${(hub.y+y)/2}, ${x} ${y}`);path.setAttribute('class','tree-branch-line');wires.append(path);
        }
      }
    }
    function render(){
      chart.querySelectorAll('.tree-period,.tree-empty').forEach(c=>c.remove());timeNav.replaceChildren();
      const shown=tree.nodes.filter(n=>(showRelated||!n.related)&&(!selectedBranch||n.branch===selectedBranch)&&(!query||(()=>{const d=detailsFor(n);return`${d.title} ${d.text} ${d.record?.family||''}`.toLowerCase().includes(query);})()));
      chart.style.setProperty('--tree-font-scale',fontScale);chart.style.setProperty('--tree-column-width',(370*fontScale)+'px');
      let visiblePeriods=0;
      for(const [index,period] of periods.entries()){
        const rows=shown.filter(n=>n.period===index);if(!rows.length)continue;
        visiblePeriods++;
        const col=make('div','tree-period');col.dataset.treePeriod=String(index);
        const date=make('h3','tree-date',period.label);col.append(date);
        const top=make('div','tree-top-bank'),topStack=make('div','tree-top-stack');top.append(topStack);
        const axis=make('div','tree-axis');axis.append(make('span','tree-hub'));
        const bottom=make('div','tree-bottom-stack');col.append(top,axis,bottom);
        for(const [branchIndex,branch] of tree.branches.entries()){
          const group=rows.filter(n=>n.branch===branch.id);if(!group.length)continue;
          group.sort((a,b)=>Number(b.featured)-Number(a.featured)||Number(detailsFor(a).record?.catalog_status==='watchlist')-Number(detailsFor(b).record?.catalog_status==='watchlist')||detailsFor(a).name.length-detailsFor(b).name.length||detailsFor(a).name.localeCompare(detailsFor(b).name));
          const box=make('article','tree-branch-box');box.dataset.branch=branch.id;box.style.setProperty('--branch',branch.color);
          box.title=branch.summary;box.setAttribute('aria-description',branch.summary);
          box.append(make('h4','',branch.label));
          // Keep the overview legible without truncating paper names. Verbose
          // titles use one preview; two short names can share a compact branch.
          const prominent=branchIndex<2||group.some(n=>n.id.startsWith('signal-'))||selectedBranch||query;
          const preview=!prominent?0:group.length>1&&detailsFor(group[0]).name.length+detailsFor(group[1]).name.length<=90?2:1;
          const leaves=make('div','tree-leaves');group.slice(0,preview).forEach(n=>leaves.append(leaf(n)));box.append(leaves);
          if(group.length>preview){
            const rest=make('details','tree-more');rest.open=allOpen;
            rest.append(make('summary','',preview?`Show ${group.length-preview} more entries`:`Show all ${group.length} entries`));
            const more=make('div','tree-leaves');group.slice(preview).forEach(n=>more.append(leaf(n)));rest.append(more);rest.addEventListener('toggle',scheduleLines);box.append(rest);
          }
          (branchIndex%2===0?topStack:bottom).append(box);
        }
        chart.append(col);
        const jump=make('button','',period.label);jump.type='button';jump.onclick=()=>{anchorPeriod=col.dataset.treePeriod;viewport.scrollTo({left:Math.max(0,col.offsetLeft-30),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});};timeNav.append(jump);
      }
      if(!visiblePeriods){chart.append(make('p','tree-empty','No entries match. Clear the search or choose another branch.'));}
      else chart.querySelectorAll('.tree-empty').forEach(n=>n.remove());
      const primary=shown.filter(n=>!n.related&&!n.id.startsWith('signal-')).length,relatedCount=shown.filter(n=>n.related).length,updates=shown.filter(n=>n.id.startsWith('signal-')).length;
      status.textContent=`${primary} resources in this column${relatedCount?`; ${relatedCount} related resources`:''}${updates?`; ${updates} separately labelled updates`:''}. Every matching name is available; expand a branch or choose “Show all entries”.`;
      const recent=chart.querySelector('.tree-period[data-tree-period="3"]')||chart.querySelector('.tree-period[data-tree-period="4"]');
      anchorPeriod=(recent||chart.querySelector('.tree-period'))?.dataset.treePeriod||'';lastWidth=viewport.clientWidth;
      viewport.scrollLeft=recent?recent.offsetLeft-30:0;viewport.scrollTop=0;scheduleLines();
    }
    search.oninput=()=>{query=search.value.toLowerCase().trim();render();};select.onchange=()=>{selectedBranch=select.value;render();};related.onchange=()=>{showRelated=related.checked;render();};
    toggle.onclick=()=>{allOpen=!allOpen;toggle.textContent=allOpen?'Show short overview':'Show all entries';toggle.setAttribute('aria-pressed',String(allOpen));chart.querySelectorAll('.tree-more').forEach(n=>n.open=allOpen);scheduleLines();};
    larger.onclick=()=>{fontScale=fontScale===1?1.2:1;larger.setAttribute('aria-pressed',String(fontScale!==1));larger.textContent=fontScale===1?'Larger text':'Default text size';render();};
    const observer=new ResizeObserver(scheduleLines);observer.observe(viewport);
    viewport.addEventListener('scroll',()=>{if(lastWidth===viewport.clientWidth){const columns=[...chart.querySelectorAll('.tree-period')];columns.sort((a,b)=>Math.abs(a.offsetLeft-30-viewport.scrollLeft)-Math.abs(b.offsetLeft-30-viewport.scrollLeft));if(columns[0])anchorPeriod=columns[0].dataset.treePeriod;}scheduleLines();},{passive:true});
    const highlight=event=>{const box=event.target.closest('.tree-branch-box');chart.dataset.activeBranch=box?.dataset.branch||'';chart.querySelectorAll('.tree-branch-line').forEach(p=>p.classList.toggle('is-active',p.dataset.branch===box?.dataset.branch));};
    chart.addEventListener('pointerover',highlight);chart.addEventListener('focusin',highlight);chart.addEventListener('pointerleave',()=>{chart.dataset.activeBranch='';chart.querySelectorAll('.is-active').forEach(n=>n.classList.remove('is-active'));});
    dispose=()=>{observer.disconnect();cancelAnimationFrame(frame);dialog.remove();};render();
  };
})();
