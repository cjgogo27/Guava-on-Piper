"""Static references, released-data equality and video checksums (no browser)."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'site'
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=set();self.anchors=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ['src','poster','href']:
            if k in a:self.refs.append(a[k])
p=Parser();p.feed((S/'index.html').read_text(encoding='utf8'));errors=[]
for ref in p.refs:
    if ref=='#' or ref.startswith(('https://','http://','mailto:')):continue
    if ref.startswith('#'):
        if ref[1:] not in p.ids:errors.append('missing anchor:'+ref)
    elif not (S/ref).is_file():errors.append('missing local asset:'+ref)
for v in json.loads((S/'assets/video_manifest.json').read_text())['clips']:
    b=(S/'assets'/f"{v['id']}.mp4").read_bytes()
    if hashlib.sha256(b).hexdigest()!=v['published_video_sha256']:errors.append('video hash mismatch:'+v['id'])
    assert v['full_source_timeline_retained'] and v['speed_multiplier']==4
e=json.loads((S/'evidence.json').read_text());ev=json.loads((R/'data/evaluation/task_counts.json').read_text());assert e['task_counts']==ev['tasks']
for k,file in [('g1','g1.json'),('g2','g2_calibration.json')]:
    raw=json.loads((R/'data/perception'/file).read_text());counts={m:x['valid'] for m,x in raw['totals' if k=='g1' else 'methods'].items()};assert e[k]['counts']==counts
assert len(e['task_counts'])==15
print(json.dumps({'passed':not errors,'local_refs_checked':len(p.refs),'errors':errors,'scope':'Static/data/asset verification; not browser video playback'}));assert not errors
