(function () {
  "use strict";
  var root = document.querySelector(".harbor-report");
  if (!root) return;
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue("--accent").trim();
  var accent2 = style.getPropertyValue("--accent2").trim();
  var ink = style.getPropertyValue("--ink").trim();
  var muted = style.getPropertyValue("--muted").trim();
  var rule = style.getPropertyValue("--rule").trim();
  var bg2 = style.getPropertyValue("--bg2").trim();
  var el = document.getElementById("regrade-chart");
  if (el && window.echarts) {
    var chart = echarts.init(el, null, { renderer: "svg" });
    chart.setOption({
      animation: false,
      color: [accent, accent2, muted],
      backgroundColor: bg2,
      tooltip: { trigger: "axis", appendToBody: true, axisPointer: { type: "shadow" },
        formatter: function (items) { return items[0].name + "：" + items[0].value + " trials"; } },
      grid: { top: 15, right: 46, bottom: 32, left: 120 },
      xAxis: { type: "value", name: "trials", min: 0, max: 100,
        axisLabel: { color: muted }, nameTextStyle: { color: muted },
        splitLine: { lineStyle: { color: rule } }, axisLine: { lineStyle: { color: rule } } },
      yAxis: { type: "category", inverse: true,
        data: ["误拒修正", "误收修正", "保留原分"],
        axisLabel: { color: ink }, axisLine: { show: false }, axisTick: { show: false } },
      series: [{ type: "bar", barWidth: 38, label: { show: true, position: "right", color: ink },
        data: [{ value: 89, itemStyle: { color: accent } },
          { value: 45, itemStyle: { color: accent2 } },
          { value: 28, itemStyle: { color: muted } }] }]
    });
    window.addEventListener("resize", function () { chart.resize(); });
  }
  if (window.mermaid) mermaid.initialize({ startOnLoad: false, theme: "neutral", securityLevel: "strict" });
  var input = document.getElementById("source-search");
  var count = document.getElementById("source-count");
  var reset = document.getElementById("source-reset");
  var sources = Array.from(document.querySelectorAll("#sources ol li"));
  function filter() {
    var query = input.value.trim().toLocaleLowerCase();
    var visible = 0;
    sources.forEach(function (item) {
      var show = item.textContent.toLocaleLowerCase().includes(query);
      item.hidden = !show;
      if (show) visible += 1;
    });
    count.textContent = visible + " / " + sources.length + " 项来源";
  }
  if (input && count && reset) {
    input.addEventListener("input", filter);
    reset.addEventListener("click", function () { input.value = ""; filter(); input.focus(); });
    window.addEventListener("hashchange", function () {
      if (/^#cite-\d+$/.test(location.hash)) { input.value = ""; filter(); }
    });
    filter();
  }
})();
