#!/usr/bin/env python3
"""Keep VS Code snippets aligned with corrected Markdown and extended reference."""
from __future__ import annotations

import json
import re

from build_reference import ROOT, SECTIONS, printable_code, snippets

MD=(ROOT/'CP_Cheatsheet_Hoffnang.md').read_text()
PATH=ROOT/'cpp.json'
TEXT=PATH.read_text()

def markdown_cpp(section: str) -> str:
    pattern=r'^### '+re.escape(section)+r'[^\n]*\n.*?```cpp\n(.*?)\n```'
    m=re.search(pattern,MD,re.M|re.S)
    assert m,section
    return m.group(1)

def body_lines(code: str) -> str:
    return '\n'.join('      '+json.dumps(line,ensure_ascii=False)+',' for line in code.splitlines()).rstrip(',')

def replace_body(title: str, code: str) -> None:
    global TEXT
    pattern=r'("'+re.escape(title)+r'":\s*\{.*?"body":\s*\[\n)(.*?)(\n    \],\n    "description")'
    m=re.search(pattern,TEXT,re.S)
    assert m,title
    TEXT=TEXT[:m.start(2)]+body_lines(code)+TEXT[m.end(2):]

replace_body('Count Total Set Bits 0..N',markdown_cpp('3.6'))
replace_body('Extended GCD & Modular Inverse',markdown_cpp('3.7'))
replace_body('Complete Modulo Sheet & O(1) nCr',markdown_cpp('3.11'))
replace_body('Sieve of Eratosthenes',markdown_cpp('3.3'))
replace_body('Binary Exponentiation with Modulo',markdown_cpp('3.4 Binary Exponentiation'))
replace_body('Knuth-Morris-Pratt (KMP) Algorithm',markdown_cpp('8.1'))
replace_body('Fenwick Tree (BIT: Sum & Range Average)',markdown_cpp('7.2'))
replace_body("Kruskal's MST",markdown_cpp('10.1'))
replace_body('KACTL Segment Tree (Associative f, [b, e))',markdown_cpp('7.5'))
replace_body('Math Series & Algebra Cheatsheet',markdown_cpp('10.7'))
for title, section in [
    ('Dijkstra Algorithm', '5.1'),
    ('Bellman-Ford Algorithm', '5.4'),
    ('Lowest Common Ancestor (Binary Lifting)', '6.2'),
    ('Lazy Segment Tree (Range Add, Set & Max)', '7.6'),
    ('Two Pointers & Sliding Window', '9.2'),
    ('Binary Search on Answer', '9.3'),
]:
    replace_body(title, markdown_cpp(section))

if '"Dijkstra Algorithm (Set-Based)"' not in TEXT:
    entry={
        'prefix':['dijkstraSet'],
        'body':markdown_cpp('5.2').splitlines(),
        'description':'Set-based Dijkstra with nonnegative weights and 64-bit distances.',
    }
    block='  "Dijkstra Algorithm (Set-Based)": '+json.dumps(entry,ensure_ascii=False,indent=2).replace('\n','\n  ')
    i=TEXT.rfind('\n}')
    assert i!=-1
    TEXT=TEXT[:i].rstrip()+',\n\n'+block+TEXT[i:]
else:
    replace_body('Dijkstra Algorithm (Set-Based)',markdown_cpp('5.2'))

code=snippets()
new=[]
for _,_,entries in SECTIONS:
    for key,title,desc,source in entries:
        label='Extended: '+title
        body='namespace cpref {\n'+printable_code(code[key])+'\n} // namespace cpref'
        if '"'+label+'"' in TEXT:
            replace_body(label,body)
            continue
        entry={"prefix":["cp_"+key],"body":body.splitlines(),"description":desc+' Source: '+source+'.'}
        # Serialize one object without rewriting the existing snippet file.
        block='  '+json.dumps(label,ensure_ascii=False)+': '+json.dumps(entry,ensure_ascii=False,indent=2).replace('\n','\n  ')
        new.append(block)
if new:
    i=TEXT.rfind('\n}')
    assert i!=-1
    TEXT=TEXT[:i].rstrip()+',\n\n'+',\n\n'.join(new)+TEXT[i:]

json.loads(TEXT) # reject malformed snippets before writing
PATH.write_text(TEXT)
