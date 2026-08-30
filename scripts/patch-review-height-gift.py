from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_gift = '<p class="trial-gift"><strong>После пробного — в подарок</strong><span>Мой учебник «Основы программирования для ЕГЭ: Python 3 с нуля» и конспект-шпаргалка по ЕГЭ-2026.</span></p>'
new_gift = '<div class="trial-gift"><strong>После пробного — в подарок</strong><ul class="trial-gift-list"><li>Мой учебник «Основы программирования для ЕГЭ: Python 3 с нуля»</li><li>Конспект-шпаргалка по ЕГЭ-2026</li></ul></div>'
if old_gift not in text:
    raise RuntimeError('Trial gift markup not found')
text = text.replace(old_gift, new_gift, 1)

review_start = text.index("    document.querySelectorAll('[data-review-slider]').forEach((slider) => {")
review_end = text.index("    document.querySelectorAll('[data-achievement-carousel]').forEach((carousel) => {", review_start)
review = text[review_start:review_end]

old_raf = '''      let desktopIndex = 0;\n      let raf = 0;\n\n      function renderDesktop() {'''
new_raf = '''      let desktopIndex = 0;\n      let raf = 0;\n\n      slides.forEach((slide) => {\n        const image = slide.querySelector('img');\n        if (image && !image.complete) {\n          image.addEventListener('load', () => {\n            if (desktopCarouselQuery.matches) renderDesktop();\n          }, { once: true });\n        }\n      });\n\n      function renderDesktop() {'''
if old_raf not in review:
    raise RuntimeError('Review init marker not found')
review = review.replace(old_raf, new_raf, 1)

old_render = '''      function renderDesktop() {\n        desktopIndex = Math.max(0, Math.min(desktopIndex, slides.length - 1));\n        const x = slides[desktopIndex]?.offsetLeft || 0;\n        track.style.transform = `translate3d(${-x}px,0,0)`;\n        counter.textContent = `${desktopIndex + 1} / ${slides.length}`;\n        prev.disabled = desktopIndex === 0;\n        next.disabled = desktopIndex === slides.length - 1;\n      }\n\n      function renderTouch() {\n        track.style.transform = '';\n        const index = nearestSlideIndex(track, slides);\n        counter.textContent = `${index + 1} / ${slides.length}`;\n      }'''
new_render = '''      function renderDesktop() {\n        desktopIndex = Math.max(0, Math.min(desktopIndex, slides.length - 1));\n        const activeSlide = slides[desktopIndex];\n        const x = activeSlide?.offsetLeft || 0;\n        track.style.transform = `translate3d(${-x}px,0,0)`;\n        requestAnimationFrame(() => {\n          const targetHeight = activeSlide?.getBoundingClientRect().height || 0;\n          if (targetHeight > 0) track.style.height = `${Math.ceil(targetHeight)}px`;\n        });\n        counter.textContent = `${desktopIndex + 1} / ${slides.length}`;\n        prev.disabled = desktopIndex === 0;\n        next.disabled = desktopIndex === slides.length - 1;\n      }\n\n      function renderTouch() {\n        track.style.transform = '';\n        track.style.height = '';\n        const index = nearestSlideIndex(track, slides);\n        counter.textContent = `${index + 1} / ${slides.length}`;\n      }'''
if old_render not in review:
    raise RuntimeError('Review render block not found')
review = review.replace(old_render, new_render, 1)

text = text[:review_start] + review + text[review_end:]
path.write_text(text, encoding='utf-8')
