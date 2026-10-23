"""Generate an isolated collision candidate using caller-owned MJCF/CAD.

No mesh is distributed. No actuator/inertial/contact tuning or original-file
overwrite is permitted. This transformation is not proof of collision fidelity.
"""
from pathlib import Path
import argparse,xml.etree.ElementTree as ET,json,hashlib

def transform(source,output,mapping):
    source=Path(source).resolve();output=Path(output).resolve()
    if source==output or output.exists():raise ValueError('Use a new output path; never overwrite source/candidate')
    tree=ET.parse(source);root=tree.getroot();mesh_names={x.get('name') for x in root.iter('mesh')};changes=[]
    for geom_name,mesh_name in mapping.items():
        hits=[g for g in root.iter('geom') if g.get('name')==geom_name]
        if len(hits)!=1 or mesh_name not in mesh_names:raise ValueError('Unique geom and existing caller-owned mesh required')
        g=hits[0]
        if g.get('type')!='box':raise ValueError('Expected historical box proxy')
        before=dict(g.attrib);g.set('type','mesh');g.set('mesh',mesh_name)
        for key in ['size','pos','quat','euler','axisangle','xyaxes','zaxis']:g.attrib.pop(key,None)
        changes.append({'name':geom_name,'before':before,'after':dict(g.attrib)})
    output.parent.mkdir(parents=True,exist_ok=True);tree.write(output,encoding='utf-8',xml_declaration=True)
    return {'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'changes':changes,'warning':'CAD convex hull can fill cavities. Requires contact audit and per-task regression before use.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('--mapping',required=True,help='JSON geom-name to existing-mesh-name mapping');a=p.parse_args()
    print(json.dumps(transform(a.source,a.output,json.loads(a.mapping)),indent=2))
