from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = 'baseColor=205EDC&amp;borderRadius=8'
new = 'baseColor=E86819&amp;borderRadius=2'
count = text.count(old)
if count != 2:
    raise SystemExit(f'Expected 2 AlfaCRM URL occurrences, found {count}')
path.write_text(text.replace(old, new), encoding='utf-8')
