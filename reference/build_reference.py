#!/usr/bin/env python3
"""Regenerate the static web and Markdown reference from tested C++ snippets."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = (ROOT / "reference/algorithms.hpp").read_text()

SECTIONS = [
    ("11", "Graph algorithms", [
        ("scc", "Strongly connected components", "O(V+E); IDs are source-first. Use for condensation DAGs.", "KACT graph pp. 12–13"),
        ("two_sat", "2-SAT", "O(V+E). Add each clause (x=value OR y=value); depends on SCC.", "KACT graph p. 13"),
        ("bridges", "Bridges in an undirected multigraph", "O(V+E). Give every edge a unique ID; recursive DFS has a stack-depth limit.", "KACT graph p. 12"),
        ("dinic", "Dinic maximum flow", "Directed capacities, 0-indexed vertices; add both directions explicitly if needed.", "KACT graph p. 10"),
        ("hopcroft_karp", "Hopcroft–Karp matching", "O(E√V). Left and right vertices are numbered separately from zero.", "KACT graph p. 11"),
        ("euler_walk", "Undirected Euler walk", "O(V+E). Supports parallel edges and loops; returns no path if degree/connectivity conditions fail.", "KACT graph p. 13"),
    ]),
    ("12", "Offline queries and assignment", [
        ("mo", "Mo's algorithm", "Offline inclusive [l,r] queries. Supply inverse add/remove callbacks and a current-answer callback.", "Notebook p. 2; linked GitHub Mo skeleton"),
        ("hungarian", "Hungarian minimum-cost assignment", "O(n²m), n≤m; negative costs work. Returns total cost and a 0-indexed column for every row.", "Notebook pp. 14–15"),
    ]),
    ("13", "String algorithms", [
        ("z_function", "Z function", "O(N). z[i] is the longest prefix matching the substring beginning at i; z[0]=0.", "KACT strings p. 22"),
        ("manacher", "Manacher palindrome radii", "O(N). Separate odd and even radii; formulas for actual lengths are in the code.", "KACT strings p. 22"),
        ("aho", "Aho–Corasick multiple-pattern matching", "Lowercase a–z patterns; count overlaps and duplicates. Build after all insertions.", "KACT strings p. 23, generalized"),
        ("suffix_array", "Suffix array and LCP", "O(N log²N). Uses sorting for clarity; use a radix version only after benchmarking.", "KACT strings p. 22, simplified"),
        ("rolling_hash", "Static double rolling hash", "O(N) build and O(1) substring hash. Uses half-open [l,r) ranges; collisions remain possible.", "KACT strings p. 23, range convention standardized"),
    ]),
    ("14", "Number theory", [
        ("crt", "Extended GCD and general CRT", "Handles non-coprime moduli; returns no solution on incompatibility or 64-bit lcm overflow.", "KACT number theory p. 9, checked variant"),
        ("phi_sieve", "Linear Euler totient sieve", "O(N) precomputation; phi[1]=1. Useful for coprime counting.", "KACT number theory p. 9"),
        ("miller_rabin", "64-bit Miller–Rabin", "Deterministic uint64 primality with __int128 modular multiplication; GNU C++17.", "KACT number theory p. 9, checked variant"),
    ]),
    ("15", "Geometry algorithms", [
        ("geometry_int", "Exact integer geometry", "__int128 orientation; segment intersection, convex hull, twice signed area, point in polygon.", "KACT geometry pp. 15–17, unified"),
        ("geometry_circle", "Circle–line intersection", "Infinite line AB; returns 0, 1, or 2 points. Rejects degenerate lines.", "KACT geometry p. 16"),
    ]),
]

FORMULAS = [
    ("2D shapes", [
        ("Triangle", "sides a,b,c; base b, height h", "A=bh/2=√(s(s−a)(s−b)(s−c)), s=(a+b+c)/2; P=a+b+c; r=A/s; R=abc/(4A)."),
        ("Right triangle", "legs a,b; hypotenuse c", "c²=a²+b²; A=ab/2; R=c/2; r=(a+b−c)/2."),
        ("Equilateral triangle", "side a", "A=√3·a²/4; P=3a; h=√3·a/2; r=√3·a/6; R=√3·a/3."),
        ("Square", "side a", "A=a²; P=4a; diagonal d=a√2; inradius a/2; circumradius a/√2."),
        ("Rectangle", "sides a,b", "A=ab; P=2(a+b); diagonal d=√(a²+b²)."),
        ("Parallelogram", "adjacent sides a,b; height h to a; angle θ", "A=ah=ab sinθ; P=2(a+b)."),
        ("Rhombus", "side a; height h; diagonals d₁,d₂", "A=d₁d₂/2=ah; P=4a; diagonals bisect at right angles."),
        ("Trapezoid", "parallel bases a,b; height h", "A=(a+b)h/2; midline=(a+b)/2; P=sum of four sides."),
        ("Regular n-gon", "n sides of length a; apothem t", "P=na; t=a/(2tan(π/n)); A=Pt/2=na²/(4tan(π/n)); circumradius R=a/(2sin(π/n))."),
        ("Circle", "radius r, diameter d=2r", "A=πr²; circumference C=2πr; chord length at central angle θ: 2r sin(θ/2)."),
        ("Sector", "radius r; angle θ in radians", "A=r²θ/2; arc length=rθ; perimeter=2r+rθ."),
        ("Annulus", "outer radius R; inner radius r", "A=π(R²−r²); total boundary length=2π(R+r)."),
        ("Ellipse", "semiaxes a≥b", "A=πab; focal distance c=√(a²−b²); perimeter ≈ π[3(a+b)−√((3a+b)(a+3b))]."),
        ("Semicircle", "radius r", "A=πr²/2; perimeter including diameter=πr+2r."),
    ]),
    ("3D solids", [
        ("Cube", "edge a", "V=a³; surface S=6a²; space diagonal=a√3."),
        ("Cuboid", "edges a,b,c", "V=abc; S=2(ab+bc+ca); space diagonal=√(a²+b²+c²)."),
        ("Right prism", "base area B; base perimeter P; height h", "V=Bh; S=2B+Ph."),
        ("Cylinder", "radius r; height h", "V=πr²h; curved area=2πrh; total S=2πr(r+h)."),
        ("Cone", "radius r; height h; slant s=√(r²+h²)", "V=πr²h/3; curved area=πrs; total S=πr(r+s)."),
        ("Sphere", "radius r", "V=4πr³/3; S=4πr²."),
        ("Hemisphere", "radius r", "V=2πr³/3; curved area=2πr²; total S=3πr²."),
        ("Right pyramid", "base area B; perimeter P; height h; common face slant s", "V=Bh/3; S=B+Ps/2 when every lateral face shares slant height s."),
        ("Cone frustum", "radii R≥r; height h; slant s=√(h²+(R−r)²)", "V=πh(R²+Rr+r²)/3; S=π(R²+r²)+π(R+r)s."),
        ("Regular tetrahedron", "edge a", "V=a³/(6√2); S=√3·a²; height=a√(2/3)."),
        ("Torus", "major radius R from center to tube center; tube radius r<R", "V=2π²Rr²; S=4π²Rr."),
    ]),
    ("Coordinate and contest geometry", [
        ("Two points", "P(x₁,y₁), Q(x₂,y₂)", "distance=√((x₂−x₁)²+(y₂−y₁)²); midpoint=((x₁+x₂)/2,(y₁+y₂)/2)."),
        ("Dot and cross", "vectors u,v; angle θ", "u·v=|u||v|cosθ; cross(u,v)=uₓvᵧ−uᵧvₓ=|u||v|sinθ; sign of cross gives orientation."),
        ("Point to line", "point P; line through A,B", "distance=|cross(B−A,P−A)|/|B−A|; projection=A+(B−A)·dot(P−A,B−A)/|B−A|²."),
        ("Polygon", "vertices in boundary order", "signed 2A=Σ cross(Pᵢ,Pᵢ₊₁); perimeter=Σ|Pᵢ₊₁−Pᵢ|; centroid=Σ(Pᵢ+Pᵢ₊₁)cross(Pᵢ,Pᵢ₊₁)/(3·signed 2A)."),
        ("Lattice polygon", "integer vertices; B boundary lattice points", "Pick: A=I+B/2−1; B=Σ gcd(|Δx|,|Δy|) over edges."),
        ("Triangle laws", "opposite sides a,b,c and angles A,B,C", "a²=b²+c²−2bc cos A; a/sin A=b/sin B=c/sin C=2R."),
        ("Rotation", "point (x,y), angle θ counterclockwise", "(x′,y′)=(x cosθ−y sinθ, x sinθ+y cosθ)."),
        ("Circle equations", "center (h,k), radius r", "(x−h)²+(y−k)²=r²; tangent at point T is perpendicular to radius OT."),
    ]),
]

OTHER_FORMULAS = [
    ("Number theory and counting", [
        ("Prime factors", "n=∏pᵢ^eᵢ", "divisor count τ(n)=∏(eᵢ+1); divisor sum σ(n)=∏(pᵢ^(eᵢ+1)−1)/(pᵢ−1); φ(n)=n∏(1−1/pᵢ)."),
        ("Factorials", "prime p", "Exponent of p in n!: Σₖ≥1⌊n/pᵏ⌋. Trailing zeros in base b: min over pᵉ|b of ⌊vₚ(n!)/e⌋."),
        ("Binomial", "0≤k≤n", "C(n,k)=n!/(k!(n−k)!)=C(n−1,k−1)+C(n−1,k); if p is prime, factorial/inverse method needs n<p."),
        ("Stars and bars", "n identical items; k groups", "Allow empty groups: C(n+k−1,k−1). Require positive groups: C(n−1,k−1), n≥k."),
        ("Inclusion–exclusion", "finite sets A₁…Aₙ", "|∪Aᵢ|=Σ|Aᵢ|−Σ|Aᵢ∩Aⱼ|+Σ|Aᵢ∩Aⱼ∩Aₖ|−⋯."),
        ("Catalan", "n≥0", "Cat(n)=C(2n,n)/(n+1); Cat(0)=1; Cat(n+1)=Σᵢ₌₀ⁿ Cat(i)Cat(n−i)."),
        ("Repeated permutations", "n items, counts c₁…cₖ", "Number of distinct permutations=n!/(c₁!⋯cₖ!). Derangements: Dₙ=(n−1)(Dₙ₋₁+Dₙ₋₂)."),
        ("Burnside", "finite symmetry group G acting on X", "Orbits=(1/|G|)Σ_{g∈G}|Fix(g)|. Rotational necklaces: (1/n)Σ_{d|n}φ(d)·colors^(n/d)."),
        ("Lucas", "prime modulus p; base-p digits nᵢ,kᵢ", "C(n,k) mod p = ∏ᵢ C(nᵢ,kᵢ) mod p."),
        ("GCD and CRT", "positive moduli m,n", "ax+by=c solvable iff gcd(a,b)|c. x≡a (mod m), x≡b (mod n) compatible iff gcd(m,n)|(b−a)."),
        ("Signed division", "b>0; mathematical floor/ceil", "C++ integer / truncates toward zero. Normalize remainder to [0,b); floor(a/b)=(a−r)/b, ceil(a/b)=floor(a/b)+(r≠0)."),
    ]),
    ("Probability, graphs and games", [
        ("Probability", "events A,B; P(B)>0", "P(A|B)=P(A∩B)/P(B); P(A∪B)=P(A)+P(B)−P(A∩B); independent ⇒ P(A∩B)=P(A)P(B)."),
        ("Expectation", "random variables X,Y", "E[X]=Σx·P(X=x); E[X+Y]=E[X]+E[Y] even without independence; E[1_A]=P(A)."),
        ("Variance", "random variable X", "Var(X)=E[X²]−E[X]²; independent X,Y ⇒ Var(X+Y)=Var(X)+Var(Y)."),
        ("Binomial distribution", "X~Bin(n,p)", "P(X=k)=C(n,k)pᵏ(1−p)^(n−k); E[X]=np; Var(X)=np(1−p)."),
        ("Euler trails", "connected undirected graph after ignoring isolated vertices", "Euler circuit iff every degree is even; Euler path iff exactly 0 or 2 vertices have odd degree."),
        ("Planar graphs", "connected planar embedding", "V−E+F=2. Simple planar V≥3 ⇒ E≤3V−6; simple bipartite planar V≥3 ⇒ E≤2V−4."),
        ("Bipartite matching", "bipartite graph", "König: maximum matching size = minimum vertex-cover size. DAG minimum path cover = V−maximum matching in split graph."),
        ("Grundy", "finite impartial game with normal play", "g(v)=mex{g(u): v→u}; disjoint games combine by XOR; losing position iff combined Grundy=0."),
    ]),
]

def snippets() -> dict[str, str]:
    result = {}
    for name, body in re.findall(r"// \[snippet:([a-z_]+):start\]\n(.*?)// \[snippet:\1:end\]", HEADER, re.S):
        result[name] = body.rstrip()
    expected = [entry[0] for _, _, entries in SECTIONS for entry in entries]
    assert set(expected) == set(result), (set(expected)-set(result), set(result)-set(expected))
    return result

def printable_code(body: str) -> str:
    # The older base template defines `int` as a macro. Keep these tested index types intact.
    return '#ifdef int\n#pragma push_macro("int")\n#undef int\n#define CPREF_POP_INT\n#endif\n' + body + '\n#ifdef CPREF_POP_INT\n#pragma pop_macro("int")\n#undef CPREF_POP_INT\n#endif'

def replace_generated(path: Path, start: str, end: str, body: str, anchor: str) -> None:
    text = path.read_text()
    block = start + "\n" + body.rstrip() + "\n" + end
    if start in text:
        text = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, text, flags=re.S)
    else:
        assert anchor in text, (path, anchor)
        text = text.replace(anchor, block + "\n" + anchor)
    path.write_text(text)

def html_content(code: dict[str, str]) -> str:
    parts = []
    for section, heading, entries in SECTIONS:
        parts.append(f'<div class="chapter-title" id="ch-{section}">{section}. {html.escape(heading)}</div>')
        for key,title,desc,source in entries:
            parts.append(f'''<article class="item" data-search="{html.escape(key + ' ' + title + ' ' + heading, quote=True)}">
  <div class="item-head"><span class="item-title">{html.escape(title)}</span><span class="item-meta">{html.escape(source)}</span></div>
  <p class="item-desc">{html.escape(desc)}</p>
  <pre><code>{html.escape(printable_code(code[key]))}</code></pre>
</article>''')
    parts.append('<div class="chapter-title" id="ch-16">16. Illustrated geometry formulas</div>')
    parts.append('<p class="formula-intro item">Symbols in each figure match the formula table. All angles are in radians unless degrees are stated.</p>')
    for heading,rows in FORMULAS:
        slug={"2D shapes":"2d","3D solids":"3d","Coordinate and contest geometry":"coordinates"}[heading]
        parts.append(f'<div class="item formula-group{" illustrated" if slug != "coordinates" else ""}"><h3>{html.escape(heading)}</h3>')
        if slug != "coordinates":
            parts.append(f'<img class="shape-figure" src="assets/geometry-{slug}.svg" alt="Labeled diagrams of common {html.escape(heading.lower())}">')
        parts.append('<div class="formula-scroll"><table class="comp-table formula-table"><thead><tr><th>Shape / rule</th><th>Meaning</th><th>Formulas</th></tr></thead><tbody>')
        for title,vars_,formula in rows:
            parts.append('<tr><th scope="row">'+html.escape(title)+'</th><td>'+html.escape(vars_)+'</td><td>'+html.escape(formula)+'</td></tr>')
        parts.append('</tbody></table></div></div>')
    parts.append('<div class="chapter-title" id="ch-17">17. Math and contest formulas</div>')
    for heading,rows in OTHER_FORMULAS:
        parts.append(f'<div class="item formula-group"><h3>{html.escape(heading)}</h3><div class="formula-scroll"><table class="comp-table formula-table"><thead><tr><th>Topic</th><th>Conditions</th><th>Formula</th></tr></thead><tbody>')
        for title,vars_,formula in rows:
            parts.append('<tr><th scope="row">'+html.escape(title)+'</th><td>'+html.escape(vars_)+'</td><td>'+html.escape(formula)+'</td></tr>')
        parts.append('</tbody></table></div></div>')
    return "\n".join(parts)

def markdown_content(code: dict[str, str]) -> str:
    out = ["\n---\n", "# Extended contest reference", "", "All code below is C++17 and 0-indexed. The tested source is `reference/algorithms.hpp`; each block belongs inside `namespace cpref` or can have `cpref::` removed. Dependencies are stated above the blocks.", ""]
    for section,heading,entries in SECTIONS:
        out += [f"## Section {section}: {heading}", ""]
        for key,title,desc,source in entries:
            out += [f"### {section}.{entries.index((key,title,desc,source))+1} {title}", f"- **When/contract:** {desc}", f"- **Source:** {source}", "```cpp", printable_code(code[key]), "```", ""]
    out += ["## Section 16: Illustrated geometry formulas", "", "All angles are in radians unless degrees are stated.", ""]
    for heading,rows in FORMULAS:
        slug={"2D shapes":"2d","3D solids":"3d","Coordinate and contest geometry":"coordinates"}[heading]
        out += [f"### {heading}", ""]
        if slug != "coordinates": out += [f"![Labeled {heading.lower()}](assets/geometry-{slug}.svg)", ""]
        out += ["| Shape / rule | Meaning | Formulas |", "|---|---|---|"]
        for title,vars_,formula in rows: out.append(f"| {title} | {vars_} | {formula} |")
        out.append("")
    out += ["## Section 17: Math and contest formulas", ""]
    for heading,rows in OTHER_FORMULAS:
        out += [f"### {heading}", "", "| Topic | Conditions | Formula |", "|---|---|---|"]
        for title,vars_,formula in rows: out.append(f"| {title} | {vars_} | {formula} |")
        out.append("")
    out += ["### Source and use notes", "", "- Basic Mo loop adapted from [Mohammadreza-mz's Mo Algorithm.cpp](https://github.com/Mohammadreza-mz/icpc-cheatsheet/blob/main/Data%20Structure/Mo%20Algorithm.cpp) and the supplied Shahid Beheshti notebook; its original add/remove/get placeholders are implemented as callbacks here.", "- Graph, string, number theory, and geometry topics were selected from the supplied BRACU Crows KACT PDF, then rewritten as self-contained, tested C++17 snippets.", "- The Hungarian assignment was adapted from the supplied Shahid Beheshti notebook and returns a row-to-column map.", ""]
    return "\n".join(out)

def main() -> None:
    code = snippets()
    replace_generated(ROOT / "index.html", '<!-- EXTENDED_REFERENCE_START -->', '<!-- EXTENDED_REFERENCE_END -->', html_content(code), '  </div> <!-- End columns -->')
    md = ROOT / "CP_Cheatsheet_Hoffnang.md"
    start,end='<!-- EXTENDED_REFERENCE_START -->','<!-- EXTENDED_REFERENCE_END -->'
    text = md.read_text()
    block=start+'\n'+markdown_content(code).rstrip()+'\n'+end+'\n'
    if start in text:
        text=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n?',lambda _:block,text,flags=re.S)
    else: text=text.rstrip()+'\n\n'+block
    md.write_text(text)

if __name__ == '__main__': main()
