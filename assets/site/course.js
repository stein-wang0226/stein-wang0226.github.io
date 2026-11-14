/* One native mobile directory; deep links also reveal optional extensions. */
(() => {
  const toc = document.querySelector('.course-toc');
  if (!toc) return;
  const mobile = matchMedia('(max-width: 900px)');
  const adapt = () => { toc.open = !mobile.matches; };
  adapt();
  mobile.addEventListener('change', adapt);
  toc.addEventListener('click', event => {
    if (event.target.closest('a') && mobile.matches) toc.open = false;
  });
})();
