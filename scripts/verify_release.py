"""Offline checksum and publication-leak checks. Does not print potential secrets."""
from pathlib import Path
import hashlib,json,re,sys
R=Path(__file__).resolve().parents[1]
manifest=R/'data/provenance/release_manifest.json'
errors=[]
if manifest.exists():
    for x in json.loads(manifest.read_text(encoding='utf8'))['files']:
        p=R/x['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:errors.append({'file':x['path'],'issue':'hash_mismatch'})
else:errors.append({'file':str(manifest.relative_to(R)),'issue':'manifest_missing'})
patterns={'api_key':re.compile(rb'\bsk-[A-Za-z0-9_-]{16,}'),'private_key':re.compile(rb'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----'),'private_host':re.compile(rb'(?<!\d)(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})(?!\d)')}
for p in R.rglob('*'):
    if not p.is_file() or any(x in p.parts for x in ['.git','__pycache__']):continue
    if p.stat().st_size>20*2**20:errors.append({'file':str(p.relative_to(R)),'issue':'unexpected_large_file'})
    if p.suffix.lower() in ['.py','.md','.json','.jsonl','.toml','.yaml','.yml','.tex','.bib','.csv','.txt','']:
        b=p.read_bytes()
        for name,pat in patterns.items():
            if pat.search(b):errors.append({'file':str(p.relative_to(R)),'issue':name})
print(json.dumps({'passed':not errors,'errors':errors},indent=2))
sys.exit(bool(errors))
