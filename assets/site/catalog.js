/* Progressive enhancement: the server-rendered catalog stays readable on failure. */
(async () => {
  const form = document.querySelector('#catalog-form');
  if (!form) return;
  try {
    const response = await fetch('catalog.json');
    if (!response.ok) throw new Error('catalog');
    const data = await response.json();
    const fields = Object.fromEntries(['q', 'topic', 'type', 'sort'].map(k => [k, form.elements[k]]));
    const notice = document.querySelector('#catalog-notice');
    const container = document.querySelector('#catalog-results');
    const chips = document.querySelector('#topic-chips');
    const clear = document.querySelector('#clear-filters');
    const icon = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    function restore() {
      const params = new URLSearchParams(location.search);
      const legacy = params.get('category');
      notice.textContent = '';
      if (legacy) {
        const mapping = data.compatibility.legacy_values?.[legacy];
        if (mapping) {
          for (const [k, v] of Object.entries(mapping)) {
            const existing = params.get(k);
            const valid = k === 'origin' ? existing === 'external' :
              fields[k] && Array.from(fields[k].options || []).some(o => o.value === existing && existing);
            if (!valid) params.set(k, v);
          }
        } else {
          for (const k of ['q', 'topic', 'type', 'origin']) params.delete(k);
          notice.textContent = '原分类无法识别，已恢复完整目录。';
        }
        params.delete('category');
      }
      for (const [k, field] of Object.entries(fields)) {
        const value = params.get(k) || (k === 'sort' ? 'updated-desc' : '');
        field.value = value;
        if (k !== 'q' && field.value !== value) {
          field.value = k === 'sort' ? 'updated-desc' : '';
          notice.textContent = '部分筛选值无法识别，已恢复有效条件。';
        }
      }
      if (params.get('origin') === 'external') {
        notice.textContent = '独立子站列在本地文章下方。';
        document.querySelector('#external').scrollIntoView();
      }
      update(false);
    }
    function update(write = true) {
      const state = Object.fromEntries(Object.entries(fields).map(([k, f]) => [k, f.value]));
      if (write) {
        const params = new URLSearchParams(location.search);
        params.delete('category');
        for (const [k, v] of Object.entries(state)) {
          params.delete(k);
          if (v && !(k === 'sort' && v === 'updated-desc')) params.set(k, v);
        }
        history.replaceState(null, '', location.pathname + (params.size ? '?' + params : '') + location.hash);
      }
      const query = state.q.trim().toLocaleLowerCase();
      const filtered = !!(query || state.topic || state.type || state.sort !== 'updated-desc');
      for (const chip of chips.querySelectorAll('button')) {
        chip.setAttribute('aria-pressed', String(chip.dataset.topic === state.topic));
      }
      clear.hidden = !filtered;
      const rows = data.entries.filter(e => e.origin === 'local' && e.status === 'published'
        && (query || e.kind !== 'chapter')
        && (!state.topic || e.topic === state.topic)
        && (!state.type || e.type === state.type)
        && (!query || e.search.includes(query)));
      rows.sort((a, b) => state.sort !== 'title' && (a.updated || b.updated) && a.updated !== b.updated
        ? (b.updated || '').localeCompare(a.updated || '')
        : (a.title < b.title ? -1 : a.title > b.title ? 1 : a.id.localeCompare(b.id)));
      container.innerHTML = rows.map(e => {
        if (!filtered && e.id === data.featured_id) {
          return document.querySelector('#catalog-feature').innerHTML;
        }
        const topic = data.topics.find(t => t.id === e.topic).label;
        const type = data.types.find(t => t.id === e.type).label;
        const children = data.entries.filter(c => c.series === e.id && c.status === 'published').sort((a,b) => a.order-b.order);
        return `<article class="note-card${e.kind === 'series' ? ' series-card' : ''}" data-entry="${esc(e.id)}"><div class="tag"><span>${esc(topic)}</span><span class="note-type">${esc(type)}${e.kind === 'chapter' ? ' · 系列章节' : ''}</span></div>
          <h2><a href="${esc(e.url)}">${esc(e.title)}</a></h2><p>${esc(e.summary)}</p>
          <div class="card-bottom"><span class="note-date">${esc(e.updated || '更新时间待确认')}</span>
          <a class="card-open" href="${esc(e.url)}" aria-label="阅读${esc(e.title)}">${e.kind === 'series' ? '浏览系列' : '阅读笔记'}${icon}</a></div>
          ${children.length ? `<details><summary>查看系列章节</summary><ol>${children.map(c=>`<li><a href="${esc(c.url)}">${esc(c.title)}</a></li>`).join('')}</ol></details>` : ''}</article>`;
      }).join('');
      document.querySelector('#result-count').textContent = `${rows.length} 项匹配内容`;
      document.querySelector('#no-results').hidden = !!rows.length;
    }
    form.addEventListener('submit', event => { event.preventDefault(); update(); });
    form.addEventListener('input', () => update());
    form.addEventListener('change', () => update());
    clear.addEventListener('click', () => {
      for (const [k, f] of Object.entries(fields)) f.value = k === 'sort' ? 'updated-desc' : '';
      notice.textContent = ''; update(); fields.q.focus();
    });
    chips.addEventListener('click', event => {
      const chip = event.target.closest('button[data-topic]');
      if (!chip) return;
      fields.topic.value = chip.dataset.topic;
      update();
    });
    window.addEventListener('popstate', restore);
    restore();
    document.querySelector('#topic-fallback').hidden = true;
    chips.hidden = false;
  } catch {
    document.querySelector('#catalog-notice').textContent = '筛选暂不可用，以下目录和章节链接仍可浏览。';
  }
})();
