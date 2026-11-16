/* MathJax makes every formula a tab stop so its context menu is keyboard-reachable.
   Lesson pages carry hundreds of inline symbols, so keep only display formulas focusable. */
(() => {
  const scope = document.querySelector('.reading-content') || document.querySelector('main');
  if (!scope) return;
  const quiet = node => {
    if (node.nodeType !== 1) return;
    const containers = node.matches('mjx-container') ? [node] : node.querySelectorAll('mjx-container');
    containers.forEach(container => {
      if (container.getAttribute('display') !== 'true' && container.getAttribute('tabindex') === '0') {
        container.setAttribute('tabindex', '-1');
      }
    });
  };
  quiet(scope);
  new MutationObserver(records => records.forEach(record => {
    if (record.type === 'attributes') {
      quiet(record.target);
      return;
    }
    record.addedNodes.forEach(quiet);
  })).observe(scope, {childList: true, subtree: true, attributes: true, attributeFilter: ['tabindex']});
})();
