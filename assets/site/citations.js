(() => {
  const form = document.querySelector('#reference-form');
  if (!form) return;
  const rows = [...document.querySelectorAll('.reference-list>li')];
  function update(write = true) {
    const q = form.elements.q.value.trim().toLowerCase();
    const kind = form.elements.kind.value;
    const version = form.elements.version.value.trim().toLowerCase();
    let count = 0;
    for (const row of rows) {
      row.hidden = !(row.dataset.search.includes(q) && (!kind || row.dataset.kind === kind)
        && row.dataset.version.toLowerCase().includes(version));
      if (!row.hidden) count++;
    }
    document.querySelector('#reference-count').textContent = count ? `${count} 项来源` : '没有匹配来源，可清除条件后继续查阅。';
    if (write) {
      const params = new URLSearchParams();
      for (const [key, value] of Object.entries({q, kind, version})) if (value) params.set(key, value);
      history.replaceState(null, '', location.pathname + (params.size ? '?' + params : '') + location.hash);
    }
  }
  function restore() {
    const params = new URLSearchParams(location.search);
    for (const key of ['q', 'kind', 'version']) form.elements[key].value = params.get(key) || '';
    update(false);
  }
  form.addEventListener('input', () => update());
  form.addEventListener('change', () => update());
  form.addEventListener('submit', e => {e.preventDefault(); update();});
  form.addEventListener('reset', () => requestAnimationFrame(() => update()));
  window.addEventListener('popstate', restore);
  restore();
})();
