#!/usr/bin/env python3
"""Compile every displayed algorithm both normally and with the legacy int macro."""
from __future__ import annotations

import subprocess
import tempfile
import re
import atexit
import shutil
from pathlib import Path

from build_reference import ROOT, snippets, printable_code

DEPENDENCIES = {"two_sat": ["scc"]}

def main() -> None:
    code=snippets()
    for name,body in code.items():
        parts=[code[d] for d in DEPENDENCIES.get(name,[])]+[body]
        for legacy_macro in (False,True):
            prelude='#include <bits/stdc++.h>\n'
            if legacy_macro: prelude+='#define int long long\n'
            source=prelude+'namespace cpref {\n'+ '\n'.join(printable_code(p) for p in parts) + '\n}\nsigned main() { return 0; }\n'
            with tempfile.NamedTemporaryFile(mode='w',suffix='.cpp') as f:
                f.write(source);f.flush()
                cmd=['g++','-std=c++17','-Wall','-Wextra','-Werror','-fsyntax-only',f.name]
                result=subprocess.run(cmd,capture_output=True,text=True)
                if result.returncode:
                    raise RuntimeError(f'{name} (legacy macro={legacy_macro}) failed:\n{result.stderr}')
        print('PASS',name)
    test=ROOT/'reference/test_algorithms.cpp'
    test_dir=Path(tempfile.mkdtemp(prefix='cpref-algorithm-tests-'))
    atexit.register(shutil.rmtree, test_dir)
    binary=test_dir/'tests'
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',str(test),'-o',str(binary)],check=True)
    subprocess.run([str(binary)],check=True)

    # Compile and run the older snippets that this audit corrected, straight from Markdown.
    md=(ROOT/'CP_Cheatsheet_Hoffnang.md').read_text()
    cases={
        '3.6': ('assert(numofone(10)==17); assert(numofone(ULLONG_MAX)==((__uint128_t)64<<63));', ''),
        '3.7': ('assert(mod_inverse(3,11)==4); assert(mod_inverse(-3,11)==7);', ''),
        '3.11': ('assert(add(-1,2)==1); assert(sub(1,3)==MOD-2); assert(mul(-2,3)==MOD-6); precompute_nCr(5); assert(nCr_mod(5,2)==10);', ''),
        '7.5': ('Tree t(1); t.update(0,-3000000000LL); assert(t.query(0,1)==-3000000000LL);', '#define int long long\n'),
        '5.2': ('adj={{{1,1000000001LL}},{{2,3}}, {}}; vector<long long>d; vector<int>p; dijkstra(0,d,p); assert(d[2]==1000000004LL && p[2]==1);', ''),
        '5.4': ('vector<tuple<int,int,long long>> e={{0,1,1000000001LL},{1,2,-3}}; auto [neg,d]=bellman_ford(3,e,0); assert(!neg && d[2]==999999998LL); e.push_back({2,1,-1}); assert(bellman_ford(3,e,0).first);', ''),
        '6.2': ('for(int i=1;i<200000;++i){tree_adj[i-1].push_back(i);tree_adj[i].push_back(i-1);} build_lca(0); assert(get_lca(123456,199999)==123456); assert(tree_dist(0,199999)==199999);', ''),
        '7.6': ('LazySegTree t(vector<long long>{0,0,0,0}); t.set(0,4,1000000000LL); assert(t.query(1,2)==1000000000LL); t.add(1,3,-5); assert(t.query(0,4)==1000000000LL && t.query(1,3)==999999995LL); t.set(0,2,LLONG_MIN); assert(t.query(0,1)==LLONG_MIN);', ''),
    }
    for section,(checks,macro) in cases.items():
        match=re.search(r'^### '+re.escape(section)+r'[^\n]*\n.*?```cpp\n(.*?)\n```',md,re.M|re.S)
        assert match,section
        source='#include <bits/stdc++.h>\nusing namespace std;\n'+macro+match.group(1)+'\nsigned main(){'+checks+'}\n'
        with tempfile.NamedTemporaryFile(mode='w',suffix='.cpp') as f:
            f.write(source);f.flush()
            subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror','-Wno-array-bounds',f.name,'-o',str(binary)],check=True)
            subprocess.run([str(binary)],check=True)
        print('PASS audited fundamental',section)

    match=re.search(r'^### 10\.1[^\n]*\n.*?```cpp\n(.*?)\n```',md,re.M|re.S)
    assert match
    with tempfile.NamedTemporaryFile(mode='w',suffix='.cpp') as f:
        f.write(match.group(1));f.flush()
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',f.name,'-o',str(binary)],check=True)
    for input_,expected in [('2 1\n1 2 -1\n','Minimum cost = -1'),('2 0\n','MST does not exist'),('1 0\n','Minimum cost = 0')]:
        got=subprocess.run([str(binary)],input=input_,capture_output=True,text=True,check=True).stdout.strip()
        assert got==expected,(input_,got,expected)
    print('PASS audited fundamental 10.1')

if __name__=='__main__': main()
