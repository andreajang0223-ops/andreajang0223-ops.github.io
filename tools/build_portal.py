#!/usr/bin/env python3
"""Build the series home page (andreajang0223-ops.github.io) from the university + high school pages.

Usage: python3 build_portal.py <university index.html> <high school index.html> <out index.html>
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).parent
uni_html, hs_html = (Path(p).read_text(encoding='utf-8') for p in sys.argv[1:3])
out = Path(sys.argv[3])

def const(html, name):
    line = next(l for l in html.split('\n') if l.startswith('const ' + name + ' = '))
    body = line[line.index('=') + 1:].strip().rstrip(';')
    return json.loads(body)

TW = const(uni_html, 'TW_MAP')
P, CBY = TW['proj'], {c['name']: c for c in TW['counties']}
def project(lat, lon, county):
    x, y = (lon - P['lon0']) * P['c'] * P['k'], (P['lat0'] - lat) * P['k']
    c = CBY.get(county)
    if c and c.get('inset'):
        i = c['inset']; x, y = x * i['s'] + i['ox'], y * i['s'] + i['oy']
    return round(x, 1), round(y, 1)

uni = const(uni_html, 'SCHOOL_LIST')
hs = const(hs_html, 'SCHOOL_LIST')
dots = [[*project(s['lat'], s['lon'], s['county']), 0] for s in uni if s.get('lat') is not None and s.get('status') == 'active']
dots += [[*project(s['lat'], s['lon'], s['county']), 1] for s in hs if s.get('lat') is not None]

counties = ''.join(f'<path class="county" d="{c["d"]}"><title>{c["name"]}</title></path>' for c in TW['counties'])
insets = ''.join(f'<rect class="inset-box" x="{c["inset"]["box"][0]}" y="{c["inset"]["box"][1]}" width="{c["inset"]["box"][2] - c["inset"]["box"][0]}" height="{c["inset"]["box"][3] - c["inset"]["box"][1]}" rx="8"/>'
                 for c in TW['counties'] if c.get('inset'))

HS_GLYPH = ('<path class="b" d="M5 12.6H19V20.6H14.1V17.3a2.1 2.1 0 0 0-4.2 0V20.6H5Z"/><path class="a" d="M12 7.3 20.7 12.6H3.3Z"/>'
            '<path class="s" d="M12 7.3V2.3"/><path class="a" d="M12.4 2.3h4.7l-1.2 1.45 1.2 1.45h-4.7Z"/>')
JH_GLYPH = ('<path class="b" d="M3.5 6.2c2.9-.6 5.6-.1 8.5 1.6V19.4c-2.9-1.7-5.6-2.2-8.5-1.6Z"/>'
            '<path class="a" d="M20.5 6.2c-2.9-.6-5.6-.1-8.5 1.6V19.4c2.9-1.7 5.6-2.2 8.5-1.6Z"/>')
ES_GLYPH = ('<path class="a" d="M14.8 4.4 19.6 9.2 9.4 19.4 4.6 14.6Z"/><path class="b" d="M4.6 14.6 9.4 19.4 3.6 20.4Z"/>'
            '<path class="s" d="M12.9 6.3 17.7 11.1" stroke="#0B7A6E"/>')
vb = TW['viewBox']
html = (HERE / 'template.html').read_text(encoding='utf-8')
for k, v in {
    '@@HS_GLYPH@@': HS_GLYPH, '@@JH_GLYPH@@': JH_GLYPH, '@@ES_GLYPH@@': ES_GLYPH.replace(' stroke="#0B7A6E"', ''),
    '@@UNI_URL@@': 'https://andreajang0223-ops.github.io/taiwan-campus-3d/',
    '@@HS_URL@@': 'https://andreajang0223-ops.github.io/taiwan-highschool-3d/',
    '@@UNI_N@@': str(len(uni)), '@@HS_N@@': str(len(hs)),
    '@@VIEWBOX@@': ' '.join(map(str, vb)), '@@COUNTIES@@': counties, '@@INSETS@@': insets,
    '@@DOTS@@': json.dumps(dots, separators=(',', ':')),
}.items():
    assert k in html, k
    html = html.replace(k, v)
out.write_text(html, encoding='utf-8')
print('wrote', out, f'{len(html.encode()) / 1024:.0f} KB', len(dots), 'dots')
