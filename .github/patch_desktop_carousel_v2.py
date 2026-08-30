from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

start_marker = "    const desktopCarouselQuery = window.matchMedia('(min-width: 1025px) and (hover: hover) and (pointer: fine)');"
end_marker = "    const lightbox = document.getElementById('lightbox');"
start = text.find(start_marker)
end = text.find(end_marker, start)
if start == -1 or end == -1:
    raise RuntimeError('Carousel JS markers not found')

replacement = r'''    const desktopCarouselQuery = window.matchMedia('(min-width: 1025px) and (hover: hover) and (pointer: fine)');

    function nearestSlideIndex(track, items) {
      if (!items.length) return 0;
      const gap = parseFloat(getComputedStyle(track).gap) || 0;
      const step = items[0].getBoundingClientRect().width + gap;
      return step ? Math.max(0, Math.min(items.length - 1, Math.round(track.scrollLeft / step))) : 0;
    }

    function makeCarouselArrow(direction, label) {
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
      let desktopIndex = 0;
      let raf = 0;

      function renderDesktop() {
        desktopIndex = Math.max(0, Math.min(desktopIndex, slides.length - 1));
        const x = slides[desktopIndex]?.offsetLeft || 0;
        track.style.transform = `translate3d(${-x}px,0,0)`;
        counter.textContent = `${desktopIndex + 1} / ${slides.length}`;
        prev.disabled = desktopIndex === 0;
        next.disabled = desktopIndex === slides.length - 1;
      }

      function renderTouch() {
        track.style.transform = '';
        const index = nearestSlideIndex(track, slides);
        counter.textContent = `${index + 1} / ${slides.length}`;
      }

      function syncMode() {
        if (desktopCarouselQuery.matches) {
          track.scrollLeft = 0;
          renderDesktop();
        } else {
          renderTouch();
        }
      }

      prev.addEventListener('click', () => {
        if (!desktopCarouselQuery.matches) return;
        desktopIndex -= 1;
        renderDesktop();
      });
      next.addEventListener('click', () => {
        if (!desktopCarouselQuery.matches) return;
        desktopIndex += 1;
        renderDesktop();
      });
      track.addEventListener('scroll', () => {
        if (desktopCarouselQuery.matches) return;
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(renderTouch);
      }, { passive: true });
      window.addEventListener('resize', syncMode, { passive: true });
      if (desktopCarouselQuery.addEventListener) desktopCarouselQuery.addEventListener('change', syncMode);
      syncMode();
    });

    document.querySelectorAll('[data-achievement-carousel]').forEach((carousel) => {
      const track = carousel.querySelector('[data-achievement-track]');
      const items = Array.from(track.querySelectorAll('.achievement-item'));
      const controls = carousel.querySelector('.achievement-controls');
      const counter = carousel.querySelector('[data-achievement-counter]');
      const prev = makeCarouselArrow('←', 'Предыдущие дипломы');
      const next = makeCarouselArrow('→', 'Следующие дипломы');
      controls.prepend(prev);
      controls.append(next);
      let desktopPage = 0;
      let raf = 0;

      function touchVisibleCount() {
        if (window.matchMedia('(max-width: 720px)').matches) return 1;
        return 2;
      }

      function desktopPageStarts() {
        const size = 4;
        const maxStart = Math.max(0, items.length - size);
        const starts = [];
        for (let i = 0; i < items.length; i += size) starts.push(Math.min(i, maxStart));
        return [...new Set(starts)];
      }

      function renderDesktop() {
        const starts = desktopPageStarts();
        desktopPage = Math.max(0, Math.min(desktopPage, starts.length - 1));
        const start = starts[desktopPage] || 0;
        const x = items[start]?.offsetLeft || 0;
        track.style.transform = `translate3d(${-x}px,0,0)`;
        counter.textContent = `${desktopPage + 1} / ${starts.length}`;
        prev.disabled = desktopPage === 0;
        next.disabled = desktopPage === starts.length - 1;
      }

      function renderTouch() {
        track.style.transform = '';
        const first = nearestSlideIndex(track, items);
        const end = Math.min(first + touchVisibleCount(), items.length);
        counter.textContent = `${end} / ${items.length}`;
      }

      function syncMode() {
        if (desktopCarouselQuery.matches) {
          track.scrollLeft = 0;
          renderDesktop();
        } else {
          renderTouch();
        }
      }

      prev.addEventListener('click', () => {
        if (!desktopCarouselQuery.matches) return;
        desktopPage -= 1;
        renderDesktop();
      });
      next.addEventListener('click', () => {
        if (!desktopCarouselQuery.matches) return;
        desktopPage += 1;
        renderDesktop();
      });
      track.addEventListener('scroll', () => {
        if (desktopCarouselQuery.matches) return;
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(renderTouch);
      }, { passive: true });
      window.addEventListener('resize', syncMode, { passive: true });
      if (desktopCarouselQuery.addEventListener) desktopCarouselQuery.addEventListener('change', syncMode);
      syncMode();
    });

'''

text = text[:start] + replacement + text[end:]
path.write_text(text, encoding='utf-8')
