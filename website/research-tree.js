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
    root.dataset.treeDesign='chronological-branches';
    const heading=make('div','tree-heading');const headingText=make('div');
    const title=make('h2','','Research by topic and year');title.id='tree-title';
    headingText.append(make('p','columns-kicker','RESEARCH TREE · '+label.toUpperCase()),title,make('p','','Read left to right through the collection. The upper and lower branches separate research roles. Click a label for the original title, contribution and source.'));
    heading.append(headingText);root.append(heading);
    const toolbar=make('div','tree-toolbar');
    const searchLabel=make('label','','Find a work');const search=make('input');search.type='search';search.placeholder='Name, signal or contribution';searchLabel.append(search);
    const branchLabel=make('label','','Filter by topic');const select=make('select');
    const allOption=make('option','','All topics');allOption.value='';select.append(allOption);
    for(const branch of tree.branches.filter(b=>b.id!=='related')){const option=make('option','',branch.label);option.value=branch.id;select.append(option);}branchLabel.append(select);
    const toggle=make('button','','Expand all works');toggle.type='button';toggle.setAttribute('aria-pressed','false');
    const larger=make('button','','Larger text');larger.type='button';larger.setAttribute('aria-pressed','false');
    const relatedLabel=make('label','tree-related');const related=make('input');related.type='checkbox';relatedLabel.append(related,document.createTextNode('Include related work from other columns'));
    toolbar.append(searchLabel,branchLabel,toggle,larger,relatedLabel);root.append(toolbar);
    const timeNav=make('nav','tree-time-nav');timeNav.setAttribute('aria-label','Jump to a research-tree period');root.append(timeNav);
    const viewport=make('div','tree-viewport');viewport.tabIndex=0;viewport.setAttribute('aria-label','Horizontal research tree. Scroll sideways to move through time.');
    const chart=make('div','tree-chart');const wires=svgNode('svg');wires.classList.add('tree-wires');wires.setAttribute('aria-hidden','true');chart.append(wires);viewport.append(chart);root.append(viewport);
    const palette=make('div','tree-palette');palette.setAttribute('aria-label','Resource-type colour key');
    for(const [kind,name] of Object.entries(types)){const swatch=make('span','tree-palette-item',name);swatch.dataset.resourceType=kind;palette.append(swatch);}root.append(palette);
    const legend=make('details','tree-branch-guide');legend.append(make('summary','','What each branch covers'));root.append(legend);
    const legendItems=make('div','tree-legend');legend.append(legendItems);
    for(const branch of tree.branches.filter(b=>b.id!=='related')){const item=make('div');item.style.setProperty('--branch',branch.color);item.append(make('b','',branch.label),make('p','',branch.summary));legendItems.append(item);}
    const note=make('p','tree-note','Colours identify resource types, not quality or performance. Dates follow the years in the repository; period widths are not to scale. Lines group work by time and research role, not citation ancestry. Dashed labels await review; double borders mark extra updates. Expand a group to read all names.');root.append(note);
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
    const compactNameFor=node=>{const {name}=detailsFor(node);return data.tree.display_labels[node.id]||name.match(/^([A-Za-z][A-Za-z0-9+._-]{1,24}):/)?.[1]||name;};
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
      button.dataset.related=String(node.related);button.dataset.treeStatus=record?.catalog_status||'update';button.dataset.resourceType=record?.record_type||'update';
      const compact=compactNameFor(node);
      button.dataset.fullTitle=title;button.dataset.compactLabel=compact;
      button.dataset.year=String(year);
      const label=make('span','tree-leaf-name',allOpen?title:compact);const kind=record?(record.catalog_status==='watchlist'?'Awaiting review':types[record.record_type]||'Resource'):(signal.evidence_level==='vendor_announcement'?'Product announcement':'Research update');const mark=make('span','tree-leaf-mark',String(year));
      button.append(label,mark);button.title=`${year} · ${title}\n${text}`;
      button.setAttribute('aria-label',`${name}, ${year}. ${node.related?'Related work. ':''}${kind}. Open summary.`);button.onclick=()=>openNode(node);return button;
    }

    const upperLabel=make('span','tree-lane-label tree-lane-top',tree.lanes.top);
    const lowerLabel=make('span','tree-lane-label tree-lane-bottom',tree.lanes.bottom);
    chart.append(upperLabel,lowerLabel);
    function laneFor(node){
      const r=detailsFor(node).record;
      if(node.related)return 'bottom';
      if(theme==='twin')return node.branch==='framework'?'bottom':'top';
      if(theme==='intervention')return ['causal','timing'].includes(node.branch)?'top':'bottom';
      if(theme==='prediction')return ['physiology','reasoning'].includes(node.branch)||(node.branch==='activity'&&['model','dataset'].includes(r?.record_type))?'top':'bottom';
      return r&&['dataset','measure','infrastructure'].includes(r.record_type)?'bottom':'top';
    }
    function scheduleLines(){cancelAnimationFrame(frame);frame=requestAnimationFrame(drawLines);}
    function drawLines(){
      const columns=[...chart.querySelectorAll('.tree-period')];
      if(!columns.length){wires.replaceChildren();upperLabel.hidden=true;lowerLabel.hidden=true;return;}
      upperLabel.hidden=false;lowerLabel.hidden=false;
      const topHeight=Math.max(180,...columns.map(c=>c.querySelector('.tree-top-stack').offsetHeight));
      chart.style.setProperty('--tree-top-height',topHeight+'px');
      const width=chart.offsetWidth,height=chart.offsetHeight,base=chart.getBoundingClientRect();
      wires.setAttribute('width',width);wires.setAttribute('height',height);wires.setAttribute('viewBox',`0 0 ${width} ${height}`);
      wires.replaceChildren();
      const defs=svgNode('defs'),gradient=svgNode('linearGradient');
      gradient.id='tree-time-wash';gradient.setAttribute('x1','0%');gradient.setAttribute('x2','100%');
      for(const [offset,color] of [['0%','#a7c8d6'],['55%','#c8d3b7'],['100%','#ddd29a']]){
        const stop=svgNode('stop');stop.setAttribute('offset',offset);stop.setAttribute('stop-color',color);gradient.append(stop);
      }defs.append(gradient);wires.append(defs);
      const axis=columns[0].querySelector('.tree-axis').getBoundingClientRect();
      const y=axis.top-base.top+axis.height/2;
      const trunk=svgNode('path');trunk.setAttribute('d',`M 8 ${y} C ${width*.3} ${y-5}, ${width*.65} ${y+4}, ${width-10} ${y}`);
      trunk.setAttribute('class','tree-trunk');trunk.style.stroke='url(#tree-time-wash)';wires.append(trunk);
      const labelX=viewport.scrollLeft+viewport.clientWidth/2;
      upperLabel.style.left=labelX+'px';upperLabel.style.top=(y-64)+'px';
      lowerLabel.style.left=labelX+'px';lowerLabel.style.top=(y+28)+'px';
      for(const col of columns){
        const c=col.getBoundingClientRect(),hub=c.left-base.left+c.width*.45;
        for(const box of col.querySelectorAll('.tree-branch-box')){
          const r=box.getBoundingClientRect(),top=box.dataset.lane==='top',sign=top?-1:1;
          const edge=(top?r.bottom:r.top)-base.top,x=r.left-base.left+r.width*.53;
          const branch=svgNode('path');branch.dataset.branch=box.dataset.branch;branch.dataset.group=box.dataset.group;
          branch.setAttribute('d',`M ${hub-52} ${y} C ${hub+10} ${y+sign*9}, ${x-25} ${edge-sign*18}, ${x} ${edge}`);
          branch.setAttribute('class','tree-branch-line');branch.style.stroke=top?'#aac7d4':'#cfc9a8';wires.append(branch);
          // Small forks echo the grouped topics. They do not count papers or
          // assert technical descent; every work is a real clickable label.
          for(let fork=0;fork<3;fork++){
            const startX=hub-22+fork*15,startY=y+sign*(10+fork*10),twig=svgNode('path');
            twig.setAttribute('d',`M ${startX} ${startY} Q ${startX+20} ${startY+sign*5} ${startX+28+fork*5} ${startY+sign*(20+fork*2)}`);
            twig.setAttribute('class','tree-twig');twig.style.stroke=top?'#b6cfdb':'#dbd5ad';wires.append(twig);
          }
        }
      }
    }
    function sizeColumns(){
      const periodsShown=chart.querySelectorAll('.tree-period').length||4;
      const slots=viewport.clientWidth<650?1:Math.min(4,periodsShown);
      const width=Math.max(185,Math.min(slots===1?330:440,(viewport.clientWidth-40-(slots-1)*18)/slots))*fontScale;
      chart.style.setProperty('--tree-column-width',width+'px');
      if(lastWidth&&lastWidth!==viewport.clientWidth){
        const anchor=chart.querySelector(`.tree-period[data-tree-period="${anchorPeriod}"]`);
        if(anchor)viewport.scrollLeft=Math.max(0,anchor.offsetLeft-20);
      }
      lastWidth=viewport.clientWidth;scheduleLines();
    }
    function render(){
      chart.querySelectorAll('.tree-period,.tree-empty').forEach(n=>n.remove());timeNav.replaceChildren();
      const shown=tree.nodes.filter(n=>(showRelated||!n.related)&&(!selectedBranch||n.branch===selectedBranch)&&(!query||(()=>{
        const d=detailsFor(n);return `${d.title} ${d.text} ${d.record?.family||''}`.toLowerCase().includes(query);
      })()));
      chart.style.setProperty('--tree-font-scale',fontScale);
      chart.classList.toggle('is-expanded',allOpen);
      for(const [index,period] of periods.entries()){
        const rows=shown.filter(n=>n.period===index);if(!rows.length)continue;
        const col=make('div','tree-period');col.dataset.treePeriod=String(index);
        const top=make('div','tree-top-bank'),topStack=make('div','tree-top-stack');top.append(topStack);
        const axis=make('div','tree-axis'),bottom=make('div','tree-bottom-stack');col.append(top,axis,bottom);
        for(const lane of ['top','bottom']){
          const group=rows.filter(n=>laneFor(n)===lane);if(!group.length)continue;
          group.sort((a,b)=>Number(b.featured)-Number(a.featured)||Number(a.related)-Number(b.related)||
            Number(detailsFor(a).record?.catalog_status==='watchlist')-Number(detailsFor(b).record?.catalog_status==='watchlist')||
            compactNameFor(a).length-compactNameFor(b).length||detailsFor(a).year-detailsFor(b).year||detailsFor(a).name.localeCompare(detailsFor(b).name));
          if(allOpen)group.sort((a,b)=>detailsFor(a).year-detailsFor(b).year||detailsFor(a).name.localeCompare(detailsFor(b).name));
          const box=make('article','tree-branch-box');box.dataset.branch=selectedBranch||'group';box.dataset.lane=lane;box.dataset.group=index+'-'+lane;
          const date=make('h3','tree-date',period.label);box.append(date);
          box.setAttribute('aria-label',period.label+' · '+tree.lanes[lane]);
          // The compact view is a readable index. Every other entry is kept in
          // this same group and is revealed by the explicit expansion controls.
          const names=make('div','tree-leaves'),preview=6;
          group.slice(0,preview).sort((a,b)=>detailsFor(a).year-detailsFor(b).year||detailsFor(a).name.localeCompare(detailsFor(b).name)).forEach(n=>names.append(leaf(n)));box.append(names);
          if(group.length>preview){
            const rest=make('details','tree-more');rest.open=allOpen;
            rest.append(make('summary','',`Show ${group.length-preview} more works`));
            const more=make('div','tree-leaves');group.slice(preview).sort((a,b)=>detailsFor(a).year-detailsFor(b).year||detailsFor(a).name.localeCompare(detailsFor(b).name)).forEach(n=>more.append(leaf(n)));rest.append(more);
            rest.addEventListener('toggle',()=>{box.classList.toggle('is-open',rest.open);for(const button of box.querySelectorAll('.tree-leaf'))button.querySelector('.tree-leaf-name').textContent=rest.open||allOpen?button.dataset.fullTitle:button.dataset.compactLabel;scheduleLines();});box.append(rest);
          }
          (lane==='top'?topStack:bottom).append(box);
        }
        chart.append(col);
        const jump=make('button','',period.label);jump.type='button';jump.onclick=()=>{
          anchorPeriod=String(index);viewport.scrollTo({left:Math.max(0,col.offsetLeft-20),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
        };timeNav.append(jump);
      }
      if(!chart.querySelector('.tree-period'))chart.append(make('p','tree-empty','No works match. Clear the search or choose another topic.'));
      const primary=shown.filter(n=>!n.related&&!n.id.startsWith('signal-')).length,relatedCount=shown.filter(n=>n.related).length,updates=shown.filter(n=>n.id.startsWith('signal-')).length;
      status.textContent=`${primary} resources in this column${relatedCount?`; ${relatedCount} related resources`:''}${updates?`; ${updates} separately labelled updates`:''}. All matching works are included. Compact labels open full titles; expand a group or choose “Expand all works” for the complete tree.`;
      anchorPeriod=chart.querySelector('.tree-period')?.dataset.treePeriod||'';
      viewport.scrollLeft=0;viewport.scrollTop=0;sizeColumns();
    }
    search.oninput=()=>{query=search.value.toLowerCase().trim();render();};
    select.onchange=()=>{selectedBranch=select.value;render();};
    related.onchange=()=>{showRelated=related.checked;render();};
    toggle.onclick=()=>{
      allOpen=!allOpen;toggle.textContent=allOpen?'Compact overview':'Expand all works';toggle.setAttribute('aria-pressed',String(allOpen));
      render();
    };
    larger.onclick=()=>{fontScale=fontScale===1?1.18:1;larger.setAttribute('aria-pressed',String(fontScale!==1));larger.textContent=fontScale===1?'Larger text':'Default text size';render();};
    const observer=new ResizeObserver(sizeColumns);observer.observe(viewport);
    viewport.addEventListener('scroll',()=>{
      if(lastWidth===viewport.clientWidth){
        const columns=[...chart.querySelectorAll('.tree-period')];
        columns.sort((a,b)=>Math.abs(a.offsetLeft-20-viewport.scrollLeft)-Math.abs(b.offsetLeft-20-viewport.scrollLeft));
        if(columns[0])anchorPeriod=columns[0].dataset.treePeriod;
      }scheduleLines();
    },{passive:true});
    const highlight=event=>{
      const box=event.target.closest('.tree-branch-box');chart.querySelectorAll('.tree-branch-line').forEach(p=>p.classList.toggle('is-active',!!box&&p.dataset.group===box.dataset.group));
    };
    chart.addEventListener('pointerover',highlight);chart.addEventListener('focusin',highlight);
    chart.addEventListener('pointerleave',()=>chart.querySelectorAll('.is-active').forEach(n=>n.classList.remove('is-active')));
    document.fonts.ready.then(scheduleLines);
    dispose=()=>{observer.disconnect();cancelAnimationFrame(frame);dialog.remove();};render();
  };
})();
