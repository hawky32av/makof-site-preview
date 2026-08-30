from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = '%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css'
new = 'https%3A%2F%2Fhawky32av.github.io%2Fmakof-site-preview%2Falfa-form.css'
if old not in s:
    raise SystemExit('Default AlfaCRM CSS URL not found')
s = s.replace(old, new)
p.write_text(s, encoding='utf-8')
