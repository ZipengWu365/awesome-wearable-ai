"""Check built page navigation and asset targets; no external requests or writes."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links=[]
        self.ids=set()
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag in ('a','script','link','img'):
            value=a.get('href') if tag in ('a','link') else a.get('src')
            if value: self.links.append((tag,value))

pages={p.name:Links(p.read_text()) for p in ROOT.glob('*.html')}
research=(ROOT/'research-map.html').read_text()
payload=json.loads(re.search(r'<script id="research-data" type="application/json">(.*?)</script>',research,re.S).group(1))
dynamic_ids={r['id'] for r in payload['records']}|{'signal-'+s['id'] for s in payload['radar']['signals']}|{'column-title'}
errors=[]
for name,page in pages.items():
    for tag,target in page.links:
        url=urlsplit(target)
        if url.scheme or url.netloc or target.startswith('data:'): continue
        path=(ROOT/unquote(url.path)) if url.path else ROOT/name
        if not path.exists(): errors.append(f'{name}: missing target {target}')
        if url.fragment and path.name in pages and unquote(url.fragment) not in pages[path.name].ids|dynamic_ids:
            errors.append(f'{name}: missing anchor {target}')
assert not errors, '\n'.join(errors)
print(f'PASS: local links, anchors and assets across {len(pages)} public HTML pages')
