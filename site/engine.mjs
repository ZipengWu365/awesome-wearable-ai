// Pure query/export functions. Missing appraisal never means negative evidence.
export const fields = ['q','type','family','tier','modality','scope','weights','twin','entity','evaluation','raw','labels','participants','rate','watchlist','sort','record'];
export function parseState(hash='') {
 const p=new URLSearchParams(hash.replace(/^#/,''));
 return Object.fromEntries(fields.map(k=>[k,p.get(k)||'']));
}
export function serializeState(s) {return '#'+new URLSearchParams(fields.filter(k=>s[k]).map(k=>[k,s[k]])).toString();}
export function enrich(payload) {
 const groups=Object.fromEntries(['digital_twin','causal','resources'].map(k=>[k,new Map()]));
 for(const [kind,index] of Object.entries(groups))for(const p of payload.profiles?.[kind]||[]){if(!index.has(p.record_id))index.set(p.record_id,[]);index.get(p.record_id).push(p);}
 return [...payload.records.map(r=>({...r,pool:'accepted'})),...payload.watchlist.map(r=>({...r,pool:'watchlist',record_type:'watchlist',family:r.proposed_family,venue_tier:'watchlist'}))].map(r=>({...r,twins:groups.digital_twin.get(r.id)||[],causal_profiles:groups.causal.get(r.id)||[],resource_profiles:groups.resources.get(r.id)||[]}));
}
const has=(values,value)=>!value||(Array.isArray(values)?values:[values]).includes(value);
const numeric=(value,min)=>!min||(typeof value==='number'&&value>=Number(min));
export function matches(row,s) {
 if(row.pool==='watchlist'&&s.watchlist!=='yes')return false;
 if(s.q&&!JSON.stringify(row).normalize('NFKC').toLowerCase().includes(s.q.normalize('NFKC').toLowerCase()))return false;
 for(const [key,field] of [['type','record_type'],['family','family'],['tier','venue_tier'],['modality','modalities'],['scope','wearable_scope']])if(!has(row[field],s[key]))return false;
 if(s.weights&&String(row.open_weights??'unknown')!==s.weights)return false;
 if(s.twin||s.entity||s.evaluation)if(!row.twins.some(p=>(!s.twin||s.twin==='any'||p.theme_role===s.twin)&&has(p.entity,s.entity)&&has(p.evaluation,s.evaluation)))return false;
 // Every release constraint must hold on ONE profile; never mix different products.
 if(s.raw||s.labels||s.participants||s.rate)if(!row.resource_profiles.some(({metadata:m})=>m.local_kind==='datasets'&&(!s.raw||String(m.raw_data_available)===s.raw)&&(!s.labels||String(m.labels_available)===s.labels)&&numeric(m.n_participants,s.participants)&&(!s.rate||(typeof m.sampling_frequency_hz==='object'&&Object.entries(m.sampling_frequency_hz).some(([sensor,hz])=>(!s.modality||sensor===s.modality)&&numeric(hz,s.rate))))))return false;
 return true;
}
export function select(rows,s) {return rows.filter(r=>matches(r,s)).sort((a,b)=>s.sort==='year'?Number(b.year)-Number(a.year)||a.title.localeCompare(b.title):a.title.localeCompare(b.title));}
export function safeURL(value) {try{const u=new URL(value);return /^https?:$/.test(u.protocol)&&!u.username&&!u.password?u.href:null;}catch{return null;}}
export function csvValue(value) {let s=typeof value==='object'?JSON.stringify(value):String(value??'');if(/^[\s]*[=+\-@]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';}
export function toCSV(rows) {const keys=[...new Set(rows.flatMap(Object.keys))];return [keys.map(csvValue).join(','),...rows.map(r=>keys.map(k=>csvValue(r[k])).join(','))].join('\r\n')+'\r\n';}
