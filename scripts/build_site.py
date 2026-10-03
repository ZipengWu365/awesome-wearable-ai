#!/usr/bin/env python3
from pathlib import Path
import json
import shutil
from registry import ROOT

def main():
    site=ROOT/'site'
    shutil.copyfile(ROOT/'generated/registry.json',site/'registry.json')
    data=json.loads((site/'registry.json').read_text(encoding='utf-8'))
    html=(site/'template.html').read_text(encoding='utf-8')
    for key,value in {'accepted':data['statistics']['accepted_total'],'watchlist':data['statistics']['watchlist_total'],'twins':data['profiles']['statistics']['digital_twin_profiles']}.items():
        html=html.replace('{{'+key+'}}',str(value))
    (site/'index.html').write_text(html,encoding='utf-8')
    print('Static research portal built')
    return 0
if __name__=='__main__':raise SystemExit(main())
