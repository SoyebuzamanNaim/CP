#!/usr/bin/env python3
"""Check static page links, generated code, JavaScript syntax and printable PDF."""
from __future__ import annotations

import html
import json
import re
import subprocess
import tempfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from build_reference import ROOT, SECTIONS, printable_code, snippets

class Tags(HTMLParser):
    def __init__(self) -> None:
        super().__init__();self.ids=[];self.anchors=[];self.local=[]
    def handle_starttag(self,tag,attrs):
        props=dict(attrs)
        if 'id' in props:self.ids.append(props['id'])
        if tag=='a' and props.get('href','').startswith('#'):self.anchors.append(props['href'][1:])
        for key in ('href','src'):
            value=props.get(key,'')
            if value and not value.startswith(('http:','https:','#','mailto:','data:')):
                self.local.append(value)

def main() -> None:
    page=(ROOT/'index.html').read_text()
    tags=Tags();tags.feed(page)
    dup=[name for name,n in Counter(tags.ids).items() if n>1]
    assert not dup,dup
    missing=set(tags.anchors)-set(tags.ids)
    assert not missing,missing
    assert all(f'ch-{i}' in tags.ids for i in range(1,18))
    for path in tags.local:
        assert (ROOT/path).exists(),path
    for asset in (ROOT/'assets').glob('*.svg'):ElementTree.parse(asset)

    generated=page.split('<!-- EXTENDED_REFERENCE_START -->',1)[1].split('<!-- EXTENDED_REFERENCE_END -->',1)[0]
    code=snippets()
    for key,body in code.items():
        pattern=r'<article class="item" data-search="'+re.escape(key)+r'[^\"]*".*?<pre><code>(.*?)</code></pre>'
        m=re.search(pattern,generated,re.S)
        assert m,key
        assert html.unescape(m.group(1))==printable_code(body),key
    json_snippets=json.loads((ROOT/'cpp.json').read_text())
    md=(ROOT/'CP_Cheatsheet_Hoffnang.md').read_text()
    corrected={
        '5.2': ('dijkstra set dijkstraset', 'Dijkstra Algorithm'),
        '5.4': ('bellman ford bellman_ford negative cycle', 'Bellman-Ford Algorithm'),
        '6.2': ('lca lowest common ancestor binary lifting tree distance kth ancestor', 'Lowest Common Ancestor (Binary Lifting)'),
        '7.6': ('lazy segment tree range add set update range max kactl', 'Lazy Segment Tree (Range Add, Set & Max)'),
        '9.2': ('two pointers sliding window opposite direction merge sorted subsegments', 'Two Pointers & Sliding Window'),
        '9.3': ('binary search on answer predicate monotonic check mid bsearch float', 'Binary Search on Answer'),
    }
    for section,(search,title) in corrected.items():
        block=re.search(r'^### '+re.escape(section)+r'[^\n]*\n.*?```cpp\n(.*?)\n```',md,re.M|re.S)
        item=re.search(r'<div class="item" data-search="'+re.escape(search)+r'">.*?<pre><code>(.*?)</code></pre>',page,re.S)
        assert block and item and html.unescape(item.group(1))==block.group(1),section
        assert json_snippets[title]['body']==block.group(1).splitlines(),title
    for _,_,entries in SECTIONS:
        for key,title,_,_ in entries:
            expected=('namespace cpref {\n'+printable_code(code[key])+'\n} // namespace cpref').splitlines()
            assert json_snippets['Extended: '+title]['body']==expected,key
    assert generated.count('<article class="item"')==sum(len(x[2]) for x in SECTIONS)

    scripts=re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',page,re.S)
    assert len(scripts)==1
    with tempfile.NamedTemporaryFile(mode='w',suffix='.js') as f:
        f.write(scripts[0]);f.flush()
        subprocess.run(['node','--check',f.name],check=True)

    pdf=ROOT/'Hoffnang_ICPC_Reference.pdf'
    info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True).stdout
    count=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))
    assert 1<=count<=25,count
    pages=subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True,text=True,check=True).stdout.split('\f')
    pages=[p for p in pages if p.strip()]
    assert len(pages)==count,(len(pages),count)
    for i,p in enumerate(pages,1):
        assert 'Team Hoffnang' in p and f'Page {i}' in p,(i,p[:200])
        assert len(p.strip())>200,(i,'nearly blank')
    assert 'Illustrated geometry formulas' in page and 'Math and contest formulas' in page
    print(f'PASS site structure, generated snippets, JS, SVG, and {count}-page PDF')

if __name__=='__main__':main()
