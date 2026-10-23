"""Hash exactly the non-ignored Git release inventory, excluding this manifest."""
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1]
dest=R/'data/provenance/release_manifest.json'
raw=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=R)
names=sorted(set(n.decode('utf8') for n in raw.split(b'\0') if n))
files=[]
for n in names:
    p=R/n
    if p==dest or not p.is_file():continue
    b=p.read_bytes()
    if p.suffix.lower() not in ['.png','.pdf'] and b'\x00' not in b:
        normalized=b'\n'.join(line.rstrip(b' \t') for line in b.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n'
        if normalized!=b:p.write_bytes(normalized);b=normalized
    files.append({'path':n.replace('\\','/'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
dest.write_text(json.dumps({'version':'0.1.0','scope':'Public release files, excluding self; curated exports differ from retained source summary bytes.','files':files},indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'files':len(files),'bytes':sum(x['bytes'] for x in files)}))
