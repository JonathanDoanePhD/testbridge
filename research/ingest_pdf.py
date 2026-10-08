"""Local-only PDF ingestion. Never automatically publish publisher text.
Usage: python research/ingest_pdf.py local.pdf --url https://publisher/document.pdf --output private-corpus.json
Requires pypdf. Review table extraction / OCR and permissions before use.
"""
import argparse,json,hashlib,pathlib
from pypdf import PdfReader
p=argparse.ArgumentParser();p.add_argument('pdf');p.add_argument('--url',required=True);p.add_argument('--output',required=True);a=p.parse_args();path=pathlib.Path(a.pdf);raw=path.read_bytes();reader=PdfReader(path);chunks=[]
for i,page in enumerate(reader.pages):
 text=page.extract_text() or ''
 # Page-local word windows retain page references; tables require manual verification.
 words=text.split()
 for start in range(0,len(words),240):chunks.append(dict(id=f'p{i+1}-{start}',page=i+1,url=a.url,title=f'{path.name} page {i+1}',text=' '.join(words[start:start+300]),tags='',kind='extracted publisher text'))
pathlib.Path(a.output).write_text(json.dumps(dict(sha256=hashlib.sha256(raw).hexdigest(),source_url=a.url,chunks=chunks,warning='Private extraction; review copyright, tables, and OCR before sharing.'),indent=2));print(len(chunks),'page-linked chunks written locally')
