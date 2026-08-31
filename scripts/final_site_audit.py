from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re

ROOT = Path('.')
PAGES = [Path('index.html'), Path('privacy.html'), Path('consent.html'), Path('offer.html'), Path('404.html')]
REF_ATTRS = {'href', 'src', 'data-lightbox-src', 'data-image', 'data-learning-image'}

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []
        self.images = []
        self.h1 = 0
        self.titles = 0
        self.descriptions = 0
        self.canonicals = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.append(d['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'title':
            self.titles += 1
        if tag == 'meta' and d.get('name') == 'description':
            self.descriptions += 1
        if tag == 'link' and d.get('rel') == 'canonical':
            self.canonicals.append(d.get('href'))
        if tag == 'img':
            self.images.append(d)
        for attr in REF_ATTRS:
            if attr in d:
                self.refs.append((tag, attr, d[attr]))

errors = []
warnings = []

for page in PAGES:
    text = page.read_text(encoding='utf-8')
    p = AuditParser()
    p.feed(text)
    if p.h1 != 1:
        errors.append(f'{page}: expected 1 H1, found {p.h1}')
    if p.titles != 1:
        errors.append(f'{page}: expected 1 title, found {p.titles}')
    if page != Path('404.html') and p.descriptions != 1:
        errors.append(f'{page}: expected 1 meta description, found {p.descriptions}')
    if len(p.ids) != len(set(p.ids)):
        dupes = sorted({x for x in p.ids if p.ids.count(x) > 1})
        errors.append(f'{page}: duplicate IDs: {dupes}')
    ids = set(p.ids)
    for tag, attr, ref in p.refs:
        if not ref:
            continue
        if ref.startswith('#'):
            if page == Path('index.html') and ref[1:] not in ids:
                errors.append(f'{page}: missing fragment target {ref}')
            continue
        if ref.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:')):
            continue
        split = urlsplit(ref)
        local = unquote(split.path)
        if not local:
            continue
        candidate = page.parent / local
        if not candidate.exists():
            errors.append(f'{page}: missing local reference {ref}')
    for img in p.images:
        if 'alt' not in img:
            errors.append(f'{page}: img missing alt: {img.get("src", "?")}')

index = Path('index.html').read_text(encoding='utf-8')
if 'https://makof.ru/assets/og/og-preview-v2.jpg' not in index:
    errors.append('index.html: active OG image URL missing')
if not Path('assets/og/og-preview-v2.jpg').exists():
    errors.append('active OG image file missing')
if Path('assets/og/og-preview.jpg').exists():
    warnings.append('obsolete assets/og/og-preview.jpg still exists')
if index.count('<h1') != 1:
    errors.append('index.html: raw H1 count is not 1')

blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', index, re.S)
if not blocks:
    errors.append('index.html: no JSON-LD')
for i, block in enumerate(blocks, 1):
    try:
        json.loads(block)
    except Exception as e:
        errors.append(f'index.html: JSON-LD block {i} invalid: {e}')

robots = Path('robots.txt').read_text(encoding='utf-8')
if 'Sitemap: https://makof.ru/sitemap.xml' not in robots:
    errors.append('robots.txt: sitemap declaration missing')

sitemap = Path('sitemap.xml').read_text(encoding='utf-8')
locs = re.findall(r'<loc>(.*?)</loc>', sitemap)
if locs != ['https://makof.ru/']:
    errors.append(f'sitemap.xml: unexpected locs {locs}')

for legal in ('privacy.html', 'consent.html', 'offer.html', '404.html'):
    text = Path(legal).read_text(encoding='utf-8')
    if 'noindex,follow' not in text:
        errors.append(f'{legal}: noindex,follow missing')

print(f'Checked {len(PAGES)} HTML pages')
print(f'Errors: {len(errors)}')
for x in errors:
    print('ERROR:', x)
print(f'Warnings: {len(warnings)}')
for x in warnings:
    print('WARNING:', x)
if errors:
    raise SystemExit(1)
print('FINAL SITE AUDIT PASSED')
