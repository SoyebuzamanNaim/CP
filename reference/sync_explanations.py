#!/usr/bin/env python3
"""Place the hand-written guides above legacy code blocks in the HTML page."""
from __future__ import annotations

import html
import re
from pathlib import Path

from code_guides import GUIDES

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    path = ROOT / "index.html"
    page = path.read_text()
    start = page.index('<div class="chapter-title" id="ch-1">')
    end = page.index('<!-- EXTENDED_REFERENCE_START -->')
    legacy = page[start:end]
    titles = re.findall(r'<span class="item-title">(.*?)</span>', legacy)
    assert len(titles) == len(set(titles))
    for encoded_title in titles:
        title = html.unescape(encoded_title)
        assert title in GUIDES, title
        title_end = legacy.index(f'<span class="item-title">{encoded_title}</span>') + len(f'<span class="item-title">{encoded_title}</span>')
        code_start = legacy.index('<pre><code>', title_end)
        assert '<span class="item-title">' not in legacy[title_end:code_start], title
        before = legacy[title_end:code_start]
        guide = '      <div class="item-desc">' + html.escape(GUIDES[title], quote=False) + '</div>\n'
        if re.search(r'\s*<div class="item-desc">.*?</div>\s*$', before, re.S):
            before = re.sub(r'\s*<div class="item-desc">.*?</div>\s*$', '\n' + guide, before, flags=re.S)
        else:
            before = before + guide
        legacy = legacy[:title_end] + before + legacy[code_start:]
    page = page[:start] + legacy + page[end:]
    path.write_text(page)
    assert page.count('<pre><code>') == page.count('class="item-desc"')


if __name__ == '__main__':
    main()
