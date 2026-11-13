/* A chronological research tree. Branches are repository families, not claims
   that one paper descended from another. All collected entries remain accessible. */
(() => {
  'use strict';
  let dispose = () => {};
  const make=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
  const svgNode=tag=>document.createElementNS('http://www.w3.org/2000/svg',tag);
  const statuses={evidence_card:'Study summary available',metadata_verified:'Publication details checked',venue_verified:'Venue details checked'};
  const types={model:'Model',dataset:'Dataset',measure:'Health measure',method:'Method',intervention:'Intervention',infrastructure:'Hardware, tools & standards'};
  window.renderResearchTree = ({data,theme,label,records,signals,jumpTo}) => {
    dispose();
    const root=document.getElementById('column-tree');root.replaceChildren();
    const tree=data.tree.columns[theme],periods=data.tree.periods;
    let showRelated=true,fullTitles=false,showEarlier=false,selectedBranch='',query='',fontScale=1,frame=0,anchorPeriod='',lastWidth=0;
    const startYear=data.tree.default_start_year,endYear=data.tree.latest_year;
    root.dataset.treeDesign='chronological-branches';
    const heading=make('div','tree-heading');const headingText=make('div');
    const title=make('h2','','Research by topic and year');title.id='tree-title';
    headingText.append(make('p','columns-kicker','RESEARCH TREE · '+label.toUpperCase()),title,make('p','',`All matching work from ${startYear} to ${endYear}, grouped by year. Scroll sideways or choose a year. Click a label for the original title, result and source.`));
    heading.append(headingText);root.append(heading);
    const toolbar=make('div','tree-toolbar');
    const searchLabel=make('label','','Find a work');const search=make('input');search.type='search';search.placeholder='Name, signal or contribution';searchLabel.append(search);
    const branchLabel=make('label','','Filter by topic');const select=make('select');
    const allOption=make('option','','All topics');allOption.value='';select.append(allOption);
    for(const branch of tree.branches.filter(b=>b.id!=='related')){const option=make('option','',branch.label);option.value=branch.id;select.append(option);}branchLabel.append(select);
    const toggle=make('button','','Full paper titles');toggle.type='button';toggle.setAttribute('aria-pressed','false');
    const larger=make('button','','Larger text');larger.type='button';larger.setAttribute('aria-pressed','false');
    const relatedLabel=make('label','tree-related');const related=make('input');related.type='checkbox';related.checked=true;relatedLabel.append(related,document.createTextNode('Include repository cross-linked studies (labelled Related)'));
    const earlierLabel=make('label','tree-related tree-earlier');const earlier=make('input');earlier.type='checkbox';earlierLabel.append(earlier,document.createTextNode(`Include work before ${startYear}`));
    toolbar.append(searchLabel,branchLabel,toggle,larger,relatedLabel,earlierLabel);root.append(toolbar);
    const timeNav=make('nav','tree-time-nav');timeNav.setAttribute('aria-label','Jump to a research-tree period');root.append(timeNav);
    const scrollHelp=make('p','tree-scroll-help','All matching works have labels; none need an expansion button. Scroll sideways within the figure. Year buttons move to a year without hiding the others. The numbers count matching resources in this collection, not all research published that year.');root.append(scrollHelp);
    const navigator=make('div','tree-overview-scroll'),scrollTrack=make('div','tree-scroll-track');
    navigator.tabIndex=0;navigator.setAttribute('aria-label','Scroll the complete research tree horizontally');navigator.append(scrollTrack);root.append(navigator);
    const viewport=make('div','tree-viewport');viewport.tabIndex=0;viewport.setAttribute('aria-label','Complete horizontal research tree. Scroll sideways to move through time.');
    const chart=make('div','tree-chart');const wires=svgNode('svg');wires.classList.add('tree-wires');wires.setAttribute('aria-hidden','true');chart.append(wires);viewport.append(chart);root.append(viewport);
    const palette=make('div','tree-palette');palette.setAttribute('aria-label','Resource-type colour key');
    for(const [kind,name] of Object.entries(types)){const swatch=make('span','tree-palette-item',name);swatch.dataset.resourceType=kind;palette.append(swatch);}root.append(palette);
    const legend=make('details','tree-branch-guide');legend.append(make('summary','','What each branch covers'));root.append(legend);
    const legendItems=make('div','tree-legend');legend.append(legendItems);
    for(const branch of tree.branches.filter(b=>b.id!=='related')){const item=make('div');item.style.setProperty('--branch',branch.color);item.append(make('b','',branch.label),make('p','',branch.summary));legendItems.append(item);}
    const note=make('p','tree-note','Colours show resource types. Original records use their registry year; added papers use the source or manuscript-version year. Groups expand to fit their labels. Lines connect year groups and research roles. Dashed labels await review; double borders mark source updates. Related work keeps its primary classification.');root.append(note);
    const status=make('p','tree-status');status.setAttribute('role','status');status.setAttribute('aria-live','polite');root.append(status);
    const dialog=make('dialog','tree-dialog');dialog.setAttribute('aria-labelledby','tree-dialog-title');document.body.append(dialog);
    const close=make('button','tree-dialog-close','Close');close.type='button';close.onclick=()=>dialog.close();
    const dialogContent=make('div','tree-dialog-content');dialog.append(close,dialogContent);
    dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
    const detailsFor = node => {
      const record=records.get(node.id),signal=signals.get(node.id.replace(/^signal-/,''));
      return {record,signal,title:record?.title||signal?.title,name:record?.short_name||signal?.short_name||signal?.title.split(':')[0]||record?.title,
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
      if(s?.venue){add('Publication',`${s.venue}. ${s.publication_status}.`);add('Source dates',`${/ICML|ICLR|NeurIPS/.test(s.venue)?'First manuscript':'Published'} ${s.publication_date}${s.event_date!==s.publication_date?`; manuscript updated ${s.event_date}`:''}.`);}
      add('What was tested',r?.study_design);add('Reported result',r?.outcome_status||s?.evidence);
      add('Study limits',r?.limitations);add('Research setting',r?.evidence_boundary||s?.limit);
      if(r?.link_withheld)add('Source note',r.source_issue);
      const links=make('div','tree-dialog-links');
      if(r){const reviewed=data.radar.signals.find(s=>s.added_on&&s.registry_ids.includes(r.id));if(!r.link_withheld)primaryLink(links,'Open paper or resource page',reviewed?.sources[0]?.url||r.primary_url);primaryLink(links,'Code',r.code_url);primaryLink(links,'Data',r.data_url);}
      else for(const source of s.sources)primaryLink(links,source.title,source.url);
      if(r)for(const update of data.radar.signals.filter(s=>s.registry_ids.includes(r.id))){
        add('Additional source review',update.title);add('Earlier approach',update.before);add('What changed',update.after);
        add('Reported evidence',update.evidence);add('Research setting',update.limit);
        for(const source of update.sources)primaryLink(links,source.title,source.url);
      }
      const full=make('button','','Read the complete entry');full.type='button';full.onclick=()=>{dialog.close();jumpTo(node.id,true);};links.append(full);dialogContent.append(links);
      if(r?.evidence_depth)dialogContent.append(make('p','tree-source-note',statuses[r.evidence_depth]||r.evidence_depth));
      dialog.showModal();close.focus();
    };
    function leaf(node){
      const {record,signal,name,title,year,text}=detailsFor(node);
      const button=make('button','tree-leaf');button.type='button';button.dataset.treeId=node.id;
      button.dataset.related=String(node.related);button.dataset.treeStatus=record?.catalog_status||'update';button.dataset.resourceType=record?.record_type||signal?.resource_type||'update';
      const compact=compactNameFor(node);
      button.dataset.fullTitle=title;button.dataset.compactLabel=compact;
      button.dataset.year=String(year);
      const label=make('span','tree-leaf-name',fullTitles?title:compact);const kind=record?(record.catalog_status==='watchlist'?'Awaiting review':types[record.record_type]||'Resource'):(signal.evidence_level==='vendor_announcement'?'Product announcement':'Research update');const mark=make('span','tree-leaf-mark',String(year)+(node.related?' · Related':''));
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
      scrollTrack.style.width=width+'px';navigator.scrollLeft=viewport.scrollLeft;
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
      const narrow=viewport.clientWidth<650,limit=(fullTitles?470:350)*fontScale;
      const base=(narrow?Math.max(220,Math.min(330,viewport.clientWidth-40)):390)*fontScale;
      const maximum=Math.max(base,narrow?Math.min(720,viewport.clientWidth*2):viewport.clientWidth-40);
      for(const col of chart.querySelectorAll('.tree-period')){
        let width=base;col.style.width=width+'px';
        for(let pass=0;pass<9;pass++){
          const height=Math.max(0,...[...col.querySelectorAll('.tree-branch-box')].map(box=>box.offsetHeight));
          if(height<=limit||width>=maximum)break;
          width=Math.min(maximum,width*1.32);col.style.width=Math.ceil(width)+'px';
        }
      }
      if(lastWidth&&lastWidth!==viewport.clientWidth){
        const anchor=chart.querySelector(`.tree-period[data-tree-period="${anchorPeriod}"]`);
        if(anchor)viewport.scrollLeft=Math.max(0,anchor.offsetLeft-20);
      }
      lastWidth=viewport.clientWidth;scheduleLines();
    }
    function render(){
      const previousAnchor=anchorPeriod;
      chart.querySelectorAll('.tree-period,.tree-empty').forEach(n=>n.remove());timeNav.replaceChildren();
      const shown=tree.nodes.filter(n=>(showEarlier||detailsFor(n).year>=startYear)&&(showRelated||!n.related)&&
        (!selectedBranch||n.branch===selectedBranch)&&(!query||(()=>{
          const d=detailsFor(n);return `${d.title} ${d.text} ${d.record?.family||''}`.toLowerCase().includes(query);
        })()));
      chart.style.setProperty('--tree-font-scale',fontScale);
      chart.classList.add('is-expanded');
      root.dataset.treeStartYear=showEarlier?'all':String(startYear);
      for(const [index,period] of periods.entries()){
        if(!showEarlier&&period.end<startYear)continue;
        const rows=shown.filter(n=>n.period===index),jump=make('button');
        jump.type='button';jump.dataset.period=String(index);jump.dataset.year=String(period.end);
        jump.append(make('b','',period.label),make('span','',String(rows.length)));
        jump.setAttribute('aria-label',period.label+': '+rows.length+' matching resources. Move to this year.');
        jump.disabled=!rows.length;timeNav.append(jump);
        if(!rows.length)continue;
        const col=make('div','tree-period');col.dataset.treePeriod=String(index);col.dataset.year=String(period.end);
        const fraction=(period.end-startYear)/Math.max(1,endYear-startYear);
        col.dataset.tone=fraction<.25?'early':fraction<.5?'transition':fraction<.8?'recent':'latest';
        const top=make('div','tree-top-bank'),topStack=make('div','tree-top-stack');top.append(topStack);
        const axis=make('div','tree-axis'),bottom=make('div','tree-bottom-stack');col.append(top,axis,bottom);
        for(const lane of ['top','bottom']){
          const group=rows.filter(n=>laneFor(n)===lane);if(!group.length)continue;
          group.sort((a,b)=>detailsFor(a).year-detailsFor(b).year||Number(a.related)-Number(b.related)||
            detailsFor(a).title.localeCompare(detailsFor(b).title));
          const box=make('article','tree-branch-box');
          box.dataset.branch=selectedBranch||'group';box.dataset.lane=lane;box.dataset.group=index+'-'+lane;
          box.append(make('h3','tree-date',period.label));
          box.setAttribute('aria-label',period.label+' · '+tree.lanes[lane]+' · '+group.length+' resources');
          if(group.every(n=>n.related))box.append(make('p','tree-group-note','Related enabling studies'));
          const names=make('div','tree-leaves');
          // No sample limit, hidden remainder, or pagination: every match gets
          // a visible label in its own publication-year group.
          group.forEach(n=>names.append(leaf(n)));box.append(names);
          (lane==='top'?topStack:bottom).append(box);
        }
        chart.append(col);
        jump.onclick=()=>{
          anchorPeriod=String(index);viewport.scrollTo({left:Math.max(0,col.offsetLeft-20),
            behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
          timeNav.querySelectorAll('button').forEach(n=>n.setAttribute('aria-current',String(n===jump)));
        };
      }
      if(!chart.querySelector('.tree-period'))chart.append(make('p','tree-empty',
        `No works match within ${showEarlier?'the complete collection':startYear+'–'+endYear}. Clear the search, change the topic, or include earlier work.`));
      const primary=shown.filter(n=>!n.related&&!n.id.startsWith('signal-')).length,
        relatedCount=shown.filter(n=>n.related).length,updates=shown.filter(n=>!n.related&&n.id.startsWith('signal-')).length;
      status.textContent=`${showEarlier?'All repository years':startYear+'–'+endYear}: ${primary} resources assigned to this column${relatedCount?`; ${relatedCount} related resources from other columns`:''}${updates?`; ${updates} separately labelled updates`:''}. Every matching label is shown by default, with no representative-only selection. The complete archive below also retains earlier work.`;
      anchorPeriod=chart.querySelector(`.tree-period[data-tree-period="${previousAnchor}"]`)?.dataset.treePeriod||
        chart.querySelector('.tree-period')?.dataset.treePeriod||'';
      sizeColumns();
      const anchor=chart.querySelector(`.tree-period[data-tree-period="${anchorPeriod}"]`);
      viewport.scrollLeft=anchor?Math.max(0,anchor.offsetLeft-20):0;viewport.scrollTop=0;
    }
    search.oninput=()=>{query=search.value.toLowerCase().trim();render();};
    select.onchange=()=>{selectedBranch=select.value;render();};
    related.onchange=()=>{showRelated=related.checked;render();};
    earlier.onchange=()=>{showEarlier=earlier.checked;render();};
    toggle.onclick=()=>{
      fullTitles=!fullTitles;toggle.textContent=fullTitles?'Short labels':'Full paper titles';toggle.setAttribute('aria-pressed',String(fullTitles));
      render();
    };
    larger.onclick=()=>{fontScale=fontScale===1?1.18:1;larger.setAttribute('aria-pressed',String(fontScale!==1));larger.textContent=fontScale===1?'Larger text':'Default text size';render();};
    const observer=new ResizeObserver(sizeColumns);observer.observe(viewport);
    const chartObserver=new ResizeObserver(scheduleLines);chartObserver.observe(chart);
    navigator.addEventListener('scroll',()=>{if(Math.abs(viewport.scrollLeft-navigator.scrollLeft)>1)viewport.scrollLeft=navigator.scrollLeft;},{passive:true});
    viewport.addEventListener('scroll',()=>{
      if(Math.abs(navigator.scrollLeft-viewport.scrollLeft)>1)navigator.scrollLeft=viewport.scrollLeft;
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
    document.fonts.ready.then(sizeColumns);
    dispose=()=>{observer.disconnect();chartObserver.disconnect();cancelAnimationFrame(frame);dialog.remove();};render();
  };
})();
