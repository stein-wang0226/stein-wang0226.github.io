/* Wide tables, code and formulas scroll; make only the scrolling ones keyboard reachable. */
(() => {
  const scope = document.querySelector('.reading-content') || document.querySelector('main');
  if (!scope) return;
  // MathJax's visually hidden MathML runs a few pixels wider than the visible
  // formula; cap it so only real glyph clipping counts as a scroll region.
  const style = document.createElement('style');
  style.textContent = '.reading-content mjx-assistive-mml{max-width:100%}';
  document.head.append(style);
  const english = /^en\b/i.test(document.documentElement.lang || '');
  const nouns = {
    table: english ? 'Table' : '表格',
    pre: english ? 'Code' : '代码',
    equation: english ? 'Equation' : '公式',
    figure: english ? 'Figure' : '图示',
  };
  const axis = (x, y) => english
    ? (x && y ? 'scrolls horizontally and vertically'
      : x ? 'scrolls horizontally' : 'scrolls vertically')
    : (x && y ? '可横向和纵向滚动' : x ? '可横向滚动' : '可上下滚动');
  const kinds = '.reading-table, pre, .equation, figure, table';
  const formulas = 'mjx-container:not([display="true"])';
  const kind = el => el.tagName === 'MJX-CONTAINER' ? 'equation'
    : el.tagName === 'PRE' ? 'pre'
    : el.tagName === 'TABLE' ? 'table'
    : el.classList.contains('reading-table') ? 'table'
    : el.classList.contains('equation') ? 'equation' : 'figure';
  const marked = 'data-scroll-focus';
  const scrolls = (el, x, y) => {
    const computed = getComputedStyle(el);
    return [(x && /^(auto|scroll)$/.test(computed.overflowX)),
      (y && /^(auto|scroll)$/.test(computed.overflowY))];
  };
  const sync = () => {
    const elements = [...scope.querySelectorAll(kinds), ...scope.querySelectorAll(formulas)];
    // Read all widths before writing so the loop does not force a reflow per element.
    // Any positive overflow counts: a table can miss its container by a subpixel and
    // still scroll, and axe's scrollable-region-focusable reports that same region.
    const state = elements.map(el => [el,
      el.scrollWidth > el.clientWidth, el.scrollHeight > el.clientHeight]);
    state.forEach(([el, x, y]) => {
      const [scrollX, scrollY] = (x || y) ? scrolls(el, x, y) : [false, false];
      if (scrollX || scrollY) {
        if (el.hasAttribute(marked)) {
          const label = nouns[kind(el)] + (english ? ', ' : '，') + axis(scrollX, scrollY);
          if (el.getAttribute('aria-label') !== label) el.setAttribute('aria-label', label);
          return;
        }
        // MathJax always sets tabindex, so only data-scroll-focus proves we own it.
        if (el.tagName !== 'MJX-CONTAINER' && el.hasAttribute('tabindex')) return;
        el.setAttribute(marked, '');
        el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'group');
        el.setAttribute('aria-label', nouns[kind(el)] + (english ? ', ' : '，') + axis(scrollX, scrollY));
      } else if (el.hasAttribute(marked)) {
        el.removeAttribute(marked);
        el.removeAttribute('role');
        el.removeAttribute('aria-label');
        if (el.tagName === 'MJX-CONTAINER') el.setAttribute('tabindex', '-1');
        else el.removeAttribute('tabindex');
      }
    });
  };
  sync();
  addEventListener('load', sync);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync).catch(() => {});
  let frame = 0;
  const schedule = () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(sync);
  };
  addEventListener('resize', schedule, {passive: true});
  // MathJax typesets after load and details reveal hidden blocks, so rescan then.
  new MutationObserver(schedule).observe(scope, {childList: true, subtree: true});
  scope.addEventListener('toggle', schedule, true);
})();
