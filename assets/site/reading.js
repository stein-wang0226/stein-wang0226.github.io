/* Native details stay readable without scripts; deep links open their ancestors. */
(() => {
  function reveal() {
    let identifier;
    try { identifier = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = identifier && document.getElementById(identifier);
    if (!target) return;
    let ancestor = target.parentElement;
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
})();
