"""Hash-checked safe extraction of the seven public archives."""
from pathlib import Path
import argparse,json,zipfile,hashlib
p=argparse.ArgumentParser();p.add_argument('--uploads',required=True);p.add_argument('--output',required=True);a=p.parse_args();src=Path(a.uploads);out=Path(a.output);out.mkdir(parents=True,exist_ok=True);manifest=json.loads((src/'UPLOAD-CHECK.json').read_text(encoding='utf-8'))
for r in manifest['files']:
 path=src/r['file'];data=path.read_bytes()
 if len(data)!=r['bytes'] or hashlib.sha256(data).hexdigest()!=r['sha256']:raise ValueError('Input archive hash mismatch: '+r['file'])
 with zipfile.ZipFile(path) as z:
  for info in z.infolist():
   dest=(out/info.filename).resolve()
   if not dest.is_relative_to(out.resolve()):raise ValueError('Unsafe zip member')
  z.extractall(out)
print('Seven public packages extracted and hashed; no private answer extracted.')
