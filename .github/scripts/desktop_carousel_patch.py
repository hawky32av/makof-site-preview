from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

text = text.replace(
    "    function enableMouseDrag(track) {\n",
    "    const desktopCarouselQuery = window.matchMedia('(min-width: 1025px) and (hover: hover) and (pointer: fine)');\n\n    function enableMouseDrag(track) {\n      if (desktopCarouselQuery.matches) return;\n",
    1,
)

review_start = text.index("    document.querySelectorAll('[data-review-slider]').forEach((slider) => {")
achievement_start = text.index("    document.querySelectorAll('[data-achievement-carousel]').forEach((carousel) => {", review_start)
lightbox_start = text.index("    const lightbox = document.getElementById('lightbox');", achievement_start)

review_js = r'''    function makeCarouselArrow(direction, label) {
      const button = document.createElement('button');
      button.className = 'carousel-desktop-arrow';
      button.type = 'button';
      button.setAttribute('aria-label', label);
      button.textContent = direction;
      return button;
    }

    document.querySelectorAll('[data-review-slider]').forEach((slider) => {
      const track = slider.querySelector('[data-swipe-track]');
      const slides = Array.from(track.querySelectorAll('.review-slide'));
      const controls = slider.querySelector('.review-controls');
      const counter = slider.querySelector('[data-review-counter]');
      const prev = makeCarouselArrow('←', 'Предыдущий отзыв');
      const next = makeCarouselArrow('→', 'Следующий отзыв');
      controls.prepend(prev);
      controls.append(next);
      let raf = 0;

      function updateCounter(forcedIndex = null) {
        const index = forcedIndex === null ? nearestSlideIndex(track, slides) : forcedIndex;
        counter.textContent = `${index + 1} / ${slides.length}`;
        prev.disabled = index <= 0;
        next.disabled = index >= slides.length - 1;
      }

      function goTo(index) {
        const target = Math.max(0, Math.min(index, slides.length - 1));
        track.scrollTo({ left: slides[target].offsetLeft, behavior: 'smooth' });
        updateCounter(target);
      }

      prev.addEventListener('click', () => goTo(nearestSlideIndex(track, slides) - 1));
      next.addEventListener('click', () => goTo(nearestSlideIndex(track, slides) + 1));
      track.addEventListener('scroll', () => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => updateCounter());
      }, { passive: true });
      window.addEventListener('resize', () => updateCounter(), { passive: true });
      enableMouseDrag(track);
      updateCounter();
    });

'''

achievement_js = r'''    document.querySelectorAll('[data-achievement-carousel]').forEach((carousel) => {
      const track = carousel.querySelector('[data-achievement-track]');
      const items = Array.from(track.querySelectorAll('.achievement-item'));
      const controls = carousel.querySelector('.achievement-controls');
      const counter = carousel.querySelector('[data-achievement-counter]');
      const prev = makeCarouselArrow('←', 'Предыдущие дипломы');
      const next = makeCarouselArrow('→', 'Следующие дипломы');
      controls.prepend(prev);
      controls.append(next);
      let raf = 0;

      function visibleCount() {
        if (window.matchMedia('(max-width: 720px)').matches) return 1;
        if (window.matchMedia('(max-width: 1024px)').matches) return 2;
        return 4;
      }

      function pageStarts() {
        const size = visibleCount();
        const maxStart = Math.max(0, items.length - size);
        const starts = [];
        for (let i = 0; i < items.length; i += size) starts.push(Math.min(i, maxStart));
        return [...new Set(starts)];
      }

      function nearestPageIndex() {
        const starts = pageStarts();
        const first = nearestSlideIndex(track, items);
        let best = 0;
        let bestDistance = Infinity;
        starts.forEach((start, index) => {
          const distance = Math.abs(start - first);
          if (distance < bestDistance) {
            bestDistance = distance;
            best = index;
          }
        });
        return best;
      }

      function updateCounter(forcedPage = null) {
        const starts = pageStarts();
        const page = forcedPage === null ? nearestPageIndex() : Math.max(0, Math.min(forcedPage, starts.length - 1));
        const start = starts[page] || 0;
        const end = Math.min(start + visibleCount(), items.length);
        counter.textContent = `${end} / ${items.length}`;
        prev.disabled = page <= 0;
        next.disabled = page >= starts.length - 1;
      }

      function goToPage(page) {
        const starts = pageStarts();
        const targetPage = Math.max(0, Math.min(page, starts.length - 1));
        const start = starts[targetPage] || 0;
        track.scrollTo({ left: items[start]?.offsetLeft || 0, behavior: 'smooth' });
        updateCounter(targetPage);
      }

      prev.addEventListener('click', () => goToPage(nearestPageIndex() - 1));
      next.addEventListener('click', () => goToPage(nearestPageIndex() + 1));
      track.addEventListener('scroll', () => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => updateCounter());
      }, { passive: true });
      window.addEventListener('resize', () => updateCounter(), { passive: true });
      enableMouseDrag(track);
      updateCounter();
    });

'''

text = text[:review_start] + review_js + achievement_js + text[lightbox_start:]
path.write_text(text, encoding='utf-8')
