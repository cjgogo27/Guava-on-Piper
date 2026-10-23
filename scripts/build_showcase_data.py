"""Export only released measurements for the static result page."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((R/p).read_text(encoding='utf8'))
tasks=read('data/evaluation/task_counts.json')
g1=read('data/perception/g1.json');g2=read('data/perception/g2_calibration.json')
out={'task_counts':tasks['tasks'],'g1':{'denominator':48,'counts':{k:v['valid'] for k,v in g1['totals'].items()}},'g2':{'denominator':16,'counts':{k:v['valid'] for k,v in g2['methods'].items()}},'source_scope':'Curated public numerical evidence; no new physics or model requests.'}
(R/'site/evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Wrote site/evidence.json from released source tables')
