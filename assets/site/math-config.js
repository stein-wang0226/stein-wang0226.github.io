/* MathJax 3.2.2, TeX -> SVG; all components come from this site. */
(() => {
  const root = new URL(document.currentScript.dataset.mathjaxRoot, location.href).href;
  window.SteinMathRoot = root;
  window.MathJax = {
    loader: {paths: {mathjax: root}, load: ['[tex]/boldsymbol', '[tex]/mathtools', '[tex]/braket']},
    tex: {
      inlineMath: [['\\(', '\\)'], ['$', '$']],
      displayMath: [['\\[', '\\]'], ['$$', '$$']],
      processEscapes: true,
      packages: {'[+]': ['boldsymbol', 'mathtools', 'braket'], '[-]': ['autoload']},
      macros: {RR: '\\mathbb{R}', E: '\\mathbb{E}', KL: '\\operatorname{KL}',
        Var: '\\operatorname{Var}', Cov: '\\operatorname{Cov}',
        bm: ['\\boldsymbol{#1}', 1]}
    },
    options: {skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']},
    svg: {fontCache: 'local'},
    startup: {typeset: false}
  };
})();
