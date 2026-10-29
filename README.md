# Hoffnang ICPC reference

Open [`index.html`](index.html) in a browser for the searchable reference, theme switch, labeled geometry figures, and print controls. [`Hoffnang_ICPC_Reference.pdf`](Hoffnang_ICPC_Reference.pdf) is the ready-to-print version with the default Hoffnang header. The Markdown source is [`CP_Cheatsheet_Hoffnang.md`](CP_Cheatsheet_Hoffnang.md); `cpp.json` contains VS Code snippets.

The older DOCX is archived at [`legacy/CP_Cheatsheet_Hoffnang_legacy.docx`](legacy/CP_Cheatsheet_Hoffnang_legacy.docx). Use the PDF or browser print for the current version.

The printed PDF has **16 single-sided A4 landscape pages**. The published [2025 ICPC Asia Dhaka Regional rules](https://www.icpc.bubt.edu.bd/rules.php) allowed at most 25 pages and required page numbers plus the team's university and name on every page. Check the rules for the contest you will attend. To change the header, edit the three fields in the web page and use **Print PDF**; the downloadable PDF always has the default header.

## Rebuild and check

```sh
python3 reference/make_figures.py
python3 reference/build_reference.py
python3 reference/sync_fundamentals.py
python3 reference/sync_snippets.py
python3 reference/check_reference.py
google-chrome --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=Hoffnang_ICPC_Reference.pdf "file://$PWD/index.html"
pdfinfo Hoffnang_ICPC_Reference.pdf | rg Pages
```

The tested C++17 implementations live in `reference/algorithms.hpp`. The check script compiles each new snippet by itself, repeats the compile with the existing `#define int long long` template, and runs behavior checks against brute force for the algorithms. It also compiles and checks the older snippets corrected during this update.

The `treeDiameter` editor snippet inserts the reusable BFS helper; the Markdown and web reference show the full input and output example.

The Mo loop follows [Mohammadreza-mz's Mo Algorithm.cpp](https://github.com/Mohammadreza-mz/icpc-cheatsheet/blob/main/Data%20Structure/Mo%20Algorithm.cpp), with the placeholders replaced by callbacks. Hungarian assignment comes from the supplied Shahid Beheshti notebook. Graph, string, number theory, and geometry topics were selected from the supplied BRACU Crows KACT PDF and rewritten as stand-alone, checked C++17 code. The geometry diagrams are local SVG files in `assets/`.
