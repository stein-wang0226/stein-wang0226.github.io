/* Native details stay readable without scripts; deep links open their ancestors. */
(() => {
  function reveal() {
    let identifier;
    try { identifier = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = identifier && document.getElementById(identifier);
    if (!target) return;
    // A link may name the details element itself, as well as a heading inside.
    let ancestor = target;
    while (ancestor) {
      if (ancestor.tagName === 'DETAILS') ancestor.open = true;
      ancestor = ancestor.parentElement;
    }
    target.tabIndex = -1;
    requestAnimationFrame(() => {
      target.scrollIntoView({block: 'start'});
      target.focus({preventScroll: true});
    });
  }
  window.addEventListener('hashchange', reveal);
  reveal();
  // Dense research plots keep their aspect ratio and offer a larger view.
  const selectors = '.work-mechanism svg' + (document.querySelector('[data-reading-plot-zoom]')
    ? ', .work-original-report figure img, .work-original-report .diagram svg' : '');
  const plots = document.querySelectorAll(selectors);
  if (plots.length) {
    const dialog = document.createElement('dialog');
    dialog.className = 'reading-plot-dialog';
    const close = document.createElement('button');
    close.type = 'button';
    close.textContent = '关闭';
    const title = document.createElement('p');
    title.id = 'reading-plot-title';
    dialog.setAttribute('aria-labelledby', title.id);
    const scroll = document.createElement('div');
    scroll.className = 'reading-plot-scroll';
    const image = document.createElement('img');
    scroll.append(image);
    dialog.append(close, title, scroll);
    document.body.append(dialog);
    close.addEventListener('click', () => dialog.close());
    for (const plot of plots) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'reading-plot-open';
      button.textContent = '放大查看原图';
      button.addEventListener('click', () => {
        const label = plot.alt || plot.getAttribute('aria-label') || '研究机制图';
        title.textContent = label;
        image.src = plot.tagName.toLowerCase() === 'svg'
          ? 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(new XMLSerializer().serializeToString(plot))
          : plot.src;
        image.alt = label;
        dialog.showModal();
        close.focus();
      });
      plot.after(button);
    }
  }
})();
