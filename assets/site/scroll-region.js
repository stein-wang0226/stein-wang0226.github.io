/* Wide tables, code and equations scroll sideways; make only the overflowing ones keyboard reachable. */
(() => {
  const scope = document.querySelector('.reading-content');
  if (!scope) return;
  const english = /^en\b/i.test(document.documentElement.lang || '');
  const label = {
    table: english ? 'Table, scrolls horizontally' : '表格，可横向滚动',
    pre: english ? 'Code, scrolls horizontally' : '代码，可横向滚动',
    equation: english ? 'Equation, scrolls horizontally' : '公式，可横向滚动',
    figure: english ? 'Figure, scrolls horizontally' : '图示，可横向滚动',
  };
  const kind = el => el.tagName === 'PRE' ? 'pre'
    : el.classList.contains('reading-table') ? 'table'
    : el.classList.contains('equation') ? 'equation' : 'figure';
  const candidates = [...scope.querySelectorAll('.reading-table, pre, .equation, figure')];
  const marked = 'data-scroll-focus';
  const sync = () => {
    // Read all widths before writing so the loop does not force a reflow per element.
    const state = candidates.map(el => [el, el.scrollWidth > el.clientWidth + 1]);
    state.forEach(([el, overflows]) => {
      if (overflows) {
        if (el.hasAttribute('tabindex') || el.hasAttribute(marked)) return;
        el.setAttribute(marked, '');
        el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'group');
        el.setAttribute('aria-label', label[kind(el)]);
      } else if (el.hasAttribute(marked)) {
        el.removeAttribute(marked);
        el.removeAttribute('tabindex');
        el.removeAttribute('role');
        el.removeAttribute('aria-label');
      }
    });
  };
  sync();
  addEventListener('load', sync);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync).catch(() => {});
  let frame = 0;
  addEventListener('resize', () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(sync);
  }, {passive: true});
})();
