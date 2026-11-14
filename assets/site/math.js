/* Visible body first; collapsed extensions are typeset when opened. */
(() => {
  const scope = document.querySelector('.reading-content') || document.querySelector('main');
  if (!scope || !/\\[([]|\$\$?/.test(scope.textContent)) return;
  let queue = Promise.resolve();
  const notice = document.createElement('p');
  notice.className = 'reading-math-status';
  notice.setAttribute('role', 'status');
  const render = elements => {
    queue = queue.then(() => MathJax.typesetPromise(elements)).catch(error => {
      notice.replaceChildren(document.createTextNode('部分公式暂未排版，TeX 原文仍可阅读。'));
      const retry = document.createElement('button');
      retry.textContent = '重试公式排版';
      retry.addEventListener('click', () => render(elements), {once: true});
      notice.append(' ', retry);
      if (!notice.isConnected) scope.prepend(notice);
      console.error('Formula typesetting:', error);
    });
    return queue;
  };
  function visibleRoots(node) {
    if (node.tagName === 'DETAILS' && !node.open) return [];
    if (!node.querySelector('details:not([open])')) return [node];
    return Array.from(node.children).flatMap(visibleRoots);
  }
  const loader = document.createElement('script');
  loader.src = new URL('tex-svg.js', window.SteinMathRoot).href;
  loader.onload = () => MathJax.startup.promise.then(() => {
    window.SteinTypeset = node => render(visibleRoots(node));
    render(visibleRoots(scope));
    scope.addEventListener('toggle', event => {
      if (event.target.tagName === 'DETAILS' && event.target.open) {
        render(visibleRoots(event.target));
      }
    }, true);
  }).catch(showFailure);
  function showFailure() {
    notice.textContent = '公式组件加载失败，TeX 原文仍可阅读。';
    const retry = document.createElement('button');
    retry.textContent = '重新加载公式';
    retry.addEventListener('click', () => location.reload());
    notice.append(' ', retry);
    scope.prepend(notice);
  }
  loader.onerror = showFailure;
  document.head.append(loader);
})();
