#!/usr/bin/env python3
"""Copy corrected fundamental code from Markdown into the web reference."""
from __future__ import annotations

import html
import re

from build_reference import ROOT

md = (ROOT / 'CP_Cheatsheet_Hoffnang.md').read_text()
path = ROOT / 'index.html'
page = path.read_text()

items = {
    '3.3': 'sieve gprime prime generation eratosthenes',
    '3.4 Binary Exponentiation': 'binary exponentiation binexpomod modular power',
    '3.11': 'modulo arithmetic sheet mod inverse fermat ncr combinations factorials add sub mul power divi 1e9+7 998244353',
    '5.1': 'dijkstra shortest path priority queue dijkstra',
    '5.2': 'dijkstra set dijkstraset',
    '5.4': 'bellman ford bellman_ford negative cycle',
    '6.1': 'tree diameter bfs treediameter',
    '6.2': 'lca lowest common ancestor binary lifting tree distance kth ancestor',
    '7.2': 'fenwick tree bit binary indexed tree average range query sum',
    '7.6': 'lazy segment tree range add set update range max kactl',
    '8.1': 'kmp knuth morris pratt string matching',
    '9.2': 'two pointers sliding window opposite direction merge sorted subsegments',
    '9.3': 'binary search on answer predicate monotonic check mid bsearch float',
}
for section, search in items.items():
    found = re.search(r'^### ' + re.escape(section) + r'[^\n]*\n.*?```cpp\n(.*?)\n```', md, re.M | re.S)
    assert found, section
    pattern = r'(<div class="item" data-search="' + re.escape(search) + r'">.*?<pre><code>)(.*?)(</code></pre>)'
    page, count = re.subn(pattern, lambda m: m.group(1) + html.escape(found.group(1)) + m.group(3), page, count=1, flags=re.S)
    assert count == 1, section

path.write_text(page)
