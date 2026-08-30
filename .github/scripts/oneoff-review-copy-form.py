from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old = '<p>Отзывы оставил скриншотами — без пересказа и сокращений.</p>'
new = '<p>Несколько сообщений от учеников и родителей после занятий и экзамена.</p>'
if old not in text:
    raise SystemExit('Review intro text not found')
text = text.replace(old, new, 1)

old_iframe = 'width="100%" height="100%" frameborder="0" scrolling="no"'
new_iframe = 'width="100%" height="500" frameborder="0" scrolling="no"'
if old_iframe not in text:
    raise SystemExit('Iframe sizing attributes not found')
text = text.replace(old_iframe, new_iframe, 1)

path.write_text(text, encoding='utf-8')
