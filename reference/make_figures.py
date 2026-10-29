#!/usr/bin/env python3
"""Generate local, print-friendly SVG geometry diagrams (no external assets)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

TWO_D = [
  ("Triangle", '<path d="M25 105 L162 105 L112 22 Z"/><path class="measure" d="M112 22 V105"/><text x="74" y="123">b</text><text x="116" y="70">h</text><text x="23" y="63">a</text><text x="145" y="65">c</text>'),
  ("Right triangle", '<path d="M30 105 H158 L30 24 Z"/><path class="measure" d="M30 94 h11 v11"/><text x="90" y="123">a</text><text x="15" y="65">b</text><text x="105" y="62">c</text>'),
  ("Equilateral triangle", '<path d="M96 20 L30 110 H162 Z"/><path class="measure" d="M96 20 V110"/><text x="93" y="127">a</text><text x="100" y="72">h</text>'),
  ("Square", '<rect x="48" y="24" width="90" height="90"/><path class="measure" d="M48 114 L138 24"/><text x="86" y="130">a</text><text x="94" y="66">d</text>'),
  ("Rectangle", '<rect x="22" y="40" width="142" height="68"/><path class="measure" d="M22 108 L164 40"/><text x="90" y="125">a</text><text x="9" y="77">b</text><text x="94" y="66">d</text>'),
  ("Parallelogram", '<path d="M24 105 H146 L171 37 H49 Z"/><path class="measure" d="M49 37 V105"/><text x="85" y="123">a</text><text x="51" y="77">h</text><text x="155" y="80">b</text>'),
  ("Rhombus", '<path d="M94 20 L164 72 L94 124 L24 72 Z"/><path class="measure" d="M94 20 V124 M24 72 H164"/><text x="99" y="68">d₁</text><text x="54" y="68">d₂</text><text x="127" y="39">a</text>'),
  ("Trapezoid", '<path d="M25 110 H170 L139 35 H59 Z"/><path class="measure" d="M59 35 V110"/><text x="95" y="30">a</text><text x="89" y="126">b</text><text x="62" y="78">h</text>'),
  ("Regular n-gon", '<path d="M93 20 L155 49 L140 113 L47 113 L31 49 Z"/><path class="measure" d="M93 72 V113 M93 72 L155 49"/><text x="98" y="99">t</text><text x="98" y="127">a</text><text x="124" y="77">R</text>'),
  ("Circle", '<circle cx="94" cy="74" r="51"/><path class="measure" d="M94 74 H145"/><circle class="center" cx="94" cy="74" r="2"/><text x="115" y="67">r</text>'),
  ("Sector", '<path d="M92 105 L92 28 A77 77 0 0 1 161 69 Z"/><path class="measure" d="M92 105 Q113 83 116 84"/><text x="98" y="59">r</text><text x="121" y="90">θ</text>'),
  ("Annulus", '<circle cx="95" cy="73" r="53"/><circle cx="95" cy="73" r="25"/><path class="measure" d="M95 73 H148 M95 77 H120"/><text x="124" y="67">R</text><text x="101" y="91">r</text>'),
  ("Ellipse", '<ellipse cx="96" cy="73" rx="72" ry="42"/><path class="measure" d="M24 73 H168 M96 31 V115"/><text x="126" y="67">a</text><text x="101" y="52">b</text>'),
  ("Semicircle", '<path d="M35 105 A61 61 0 0 1 157 105 Z"/><path class="measure" d="M96 105 H157"/><text x="121" y="98">r</text>'),
]

THREE_D = [
  ("Cube", '<path d="M35 52 L110 52 L110 116 L35 116 Z M35 52 L62 25 H137 L110 52 M110 52 L137 25 V90 L110 116"/><path class="measure" d="M35 116 L62 90 L137 90"/><text x="67" y="130">a</text>'),
  ("Cuboid", '<path d="M22 56 H132 V112 H22 Z M22 56 L56 27 H165 L132 56 M132 56 L165 27 V84 L132 112"/><path class="measure" d="M22 112 L56 84 H165"/><text x="72" y="129">a</text><text x="166" y="63">b</text><text x="9" y="91">c</text>'),
  ("Prism", '<path d="M35 103 L94 35 L155 103 Z M35 103 V65 L94 9 L155 65 V103 M94 35 V9 M35 65 L94 9 L155 65"/><text x="15" y="82">h</text><text x="100" y="123">B</text>'),
  ("Cylinder", '<ellipse cx="96" cy="36" rx="61" ry="19"/><path d="M35 36 V109 M157 36 V109 M35 109 A61 19 0 0 0 157 109"/><path class="measure" d="M96 36 H157 M169 36 V109"/><text x="122" y="30">r</text><text x="172" y="78">h</text>'),
  ("Cone", '<path d="M96 15 L34 108 A62 18 0 0 0 158 108 Z"/><path class="measure" d="M96 15 V108 H158"/><text x="99" y="69">h</text><text x="126" y="100">r</text><text x="48" y="63">s</text>'),
  ("Sphere", '<circle cx="96" cy="75" r="53"/><ellipse class="measure" cx="96" cy="75" rx="53" ry="16"/><path class="measure" d="M96 75 L137 42"/><text x="118" y="55">r</text>'),
  ("Pyramid", '<path d="M96 15 L31 108 L151 108 Z M96 15 L169 83 L151 108 M31 108 L80 83 L169 83"/><path class="measure" d="M96 15 V91"/><text x="100" y="65">h</text><text x="88" y="124">B</text>'),
  ("Frustum", '<ellipse cx="96" cy="36" rx="34" ry="11"/><path d="M62 36 L31 106 A65 18 0 0 0 161 106 L130 36"/><path class="measure" d="M96 36 H130 M96 106 H161 M169 36 V106"/><text x="112" y="28">r</text><text x="127" y="99">R</text><text x="171" y="75">h</text>'),
  ("Hemisphere", '<path d="M35 76 A61 61 0 0 1 157 76 A61 20 0 0 1 35 76 Z"/><ellipse class="measure" cx="96" cy="76" rx="61" ry="20"/><path class="measure" d="M96 76 H157"/><text x="121" y="70">r</text>'),
  ("Tetrahedron", '<path d="M96 20 L31 107 L157 107 Z M96 20 L95 75 L31 107 M95 75 L157 107"/><path class="measure" d="M96 20 V91"/><text x="101" y="61">h</text><text x="88" y="123">a</text>'),
  ("Torus", '<ellipse cx="96" cy="73" rx="75" ry="48"/><ellipse cx="96" cy="73" rx="30" ry="15"/><path class="measure" d="M96 73 H146 M146 73 H171"/><text x="120" y="68">R</text><text x="151" y="68">r</text>'),
]

def render(title: str, items: list[tuple[str,str]], cols: int) -> str:
    w,h=210,165
    rows=(len(items)+cols-1)//cols
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols*w}" height="{rows*h}" viewBox="0 0 {cols*w} {rows*h}" role="img" aria-label="{title}">',
         '<style>svg{background:#fff;font-family:Arial,sans-serif}.panel{fill:#fff;stroke:#cbd5e1;stroke-width:1}.shape{fill:#e0f2fe;stroke:#0f172a;stroke-width:2.2;stroke-linejoin:round}.shape .measure{fill:none;stroke:#e11d48;stroke-width:1.5;stroke-dasharray:4 3}.shape .center{fill:#e11d48;stroke:none}.shape text{fill:#9f1239;font-size:13px;font-weight:bold;stroke:none}.title{fill:#0f172a;font-size:13px;font-weight:bold}</style>']
    for i,(name,svg) in enumerate(items):
        x=(i%cols)*w;y=(i//cols)*h
        out += [f'<g transform="translate({x},{y})"><rect class="panel" x="3" y="3" width="204" height="159" rx="8"/><text class="title" x="12" y="20">{name}</text><g class="shape" transform="translate(6,20)">{svg}</g></g>']
    out.append('</svg>')
    return '\n'.join(out)+'\n'

(ASSETS/'geometry-2d.svg').write_text(render('Common plane shapes',TWO_D,4))
(ASSETS/'geometry-3d.svg').write_text(render('Common three-dimensional solids',THREE_D,3))
