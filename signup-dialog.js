(() => {
  const source = document.querySelector('#signup-form');
  const dialog = document.querySelector('#signup-dialog');
  if (!source || !dialog || typeof dialog.showModal !== 'function') return;

  // Both placements use the existing CRM form, including validation and submission.
  // Resolve its stylesheet on this deployment (GitHub Pages or the production domain).
  const frame = source.querySelector('iframe');
  const formUrl = new URL(frame.src);
  formUrl.searchParams.set('css', new URL('alfa-form.css?v=neutral1', document.baseURI).href);
  frame.src = formUrl.href;
  source.querySelector('.alfacrm-fallback a').href = formUrl.href;
  let opener;
  let initialized = false;
  let previousOverflow;

  document.querySelectorAll('a[href="#signup-form"]').forEach((button) => {
    button.setAttribute('aria-haspopup', 'dialog');
    button.setAttribute('aria-controls', dialog.id);
    button.addEventListener('click', (event) => {
      event.preventDefault();
      opener = button;
      if (!initialized) {
        const copy = source.cloneNode(true);
        copy.removeAttribute('id');
        copy.querySelector('iframe').loading = 'eager';
        dialog.querySelector('#signup-dialog-content').append(copy);
        initialized = true;
      }
      previousOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      dialog.showModal();
    });
  });
  dialog.querySelector('.signup-dialog-close').addEventListener('click', () => dialog.close());
  // Native dialog supplies focus containment, Escape and an inert background.
  let pointerStartedOutside = false;
  const outside = (event) => {
    const box = dialog.getBoundingClientRect();
    return event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
  };
  dialog.addEventListener('pointerdown', (event) => { pointerStartedOutside = outside(event); });
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog && pointerStartedOutside && outside(event)) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.style.overflow = previousOverflow;
    opener?.focus({ preventScroll: true });
  });
})();
