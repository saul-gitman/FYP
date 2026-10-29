#!/usr/bin/env python3
"""Download explicit reference PDF candidates; no credentials or access bypass.

Usage: python download_reference_pdfs.py --ids U25 C08
Omit --ids to try all entries. Run in an environment with permitted network access.
The existing catalog is not automatically changed by this acquisition helper.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import argparse, hashlib, json, os, tempfile

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ids',nargs='*')
    args=parser.parse_args()
    base=Path(__file__).resolve().parent
    manifest=json.loads((base/'PDF_Acquisition_Manifest.json').read_text())
    selected=[x for x in manifest['files'] if args.ids is None or x['id'] in args.ids]
    if args.ids:
        unknown=set(args.ids)-{x['id'] for x in manifest['files']}
        if unknown: parser.error('Unknown ids: '+', '.join(sorted(unknown)))
    output=base/'PDFs';output.mkdir(exist_ok=True)
    results=[]
    for item in selected:
        target=output/item['output']
        if Path(item['output']).name!=item['output'] or not item['url'].startswith('https://'):
            raise ValueError('Manifest must contain flat filenames and HTTPS URLs')
        if target.exists():
            results.append({'id':item['id'],'status':'EXISTS_NOT_OVERWRITTEN','path':str(target)})
            continue
        tmp=None
        try:
            req=Request(item['url'],headers={'User-Agent':'FYP-reference-downloader/1.0'})
            with urlopen(req,timeout=30) as response:
                header=response.read(5)
                if header!=b'%PDF-': raise ValueError('Response is not a PDF')
                fd,tmp=tempfile.mkstemp(dir=output,suffix='.part')
                with os.fdopen(fd,'wb') as f:
                    f.write(header)
                    while True:
                        chunk=response.read(1024*1024)
                        if not chunk: break
                        f.write(chunk)
            os.replace(tmp,target);tmp=None
            results.append({'id':item['id'],'status':'DOWNLOADED','path':str(target),
                            'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
        except (HTTPError,URLError,TimeoutError,OSError,ValueError) as exc:
            results.append({'id':item['id'],'status':'FAILED','error':str(exc)})
        finally:
            if tmp: Path(tmp).unlink(missing_ok=True)
        print(item['id'],results[-1]['status'])
    (base/'acquisition_results.json').write_text(json.dumps(results,indent=2)+'\n')
    return 0 if all(x['status']!='FAILED' for x in results) else 1

if __name__=='__main__': raise SystemExit(main())
