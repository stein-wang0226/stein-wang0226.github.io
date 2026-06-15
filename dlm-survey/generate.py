#!/usr/bin/env python3
"""Split monolithic dlm_research_survey.html into multi-page site."""
import re, os

DIR = "/Users/stein_wang/Desktop/dlm_survey"
SRC = "/Users/stein_wang/Desktop/dlm_research_survey.html"

with open(SRC) as f:
    html = f.read()

# Extract body content between <div class="container"> and </div><!-- container end -->
body_match = re.search(r'(<div class="container">.*?</div>)\s*</div>\s*<!-- container end -->', html, re.DOTALL)
body_html = body_match.group(1) if body_match else ""

# Split by h2 section-title markers
section_pattern = r'(<h2 class="section-title" id="s\d+">)'
parts = re.split(section_pattern, body_html)

# parts[0] = content before first h2 (TOC + overview section header area)
# parts[1] = first h2 tag, parts[2] = content after it, etc.

# Build sections list
sections_meta = [
    ("s01_overview", "01", "扩散语言模型全景概述与四大流派",
     "DLM 四大流派总览：离散扩散、块扩散、连续扩散、预测范式"),
    ("s02_discrete", "02", "离散空间扩散 (Discrete Diffusion)",
     "D3PM · MDLM · LLaDA · Dream · SEDD · DiffuLLaMA · Seed Diffusion"),
    ("s03_block", "03", "块扩散与半自回归 (Block / Semi-AR)",
     "BD3LM · SDAR · DFlash · Nemotron · TiDAR · Fast-dLLM"),
    ("s04_continuous", "04", "连续隐空间扩散 (Continuous DLLM)",
     "Diffusion-LM · COLA · CADD · ELF · LangFlow · TextLDM · Plaid"),
    ("s05_paradigms", "05", "预测范式 (Prediction Paradigms) 大一统",
     "ε-prediction · x₀-prediction · v-prediction · Ratio Estimation · Discrete FM"),
    ("s06_scaling", "06", "DLM Scaling Laws 与 AR 对比",
     "噪声类型依赖 · Masked vs Uniform · 计算效率 · Scaling 总结"),
    ("s07_speculative", "07", "DLM 投机解码：DFlash vs MTP 深度分析",
     "DFlash · S2D2 · SimSD · Trajectory-Level SD · Self-Spec · BlockSpec"),
    ("s08_elbo_rl", "08", "ELBO 问题与 RL 训练 (SPG / GDSD)",
     "ELBO 偏差 · SPG 三明治梯度 · GDSD 自蒸馏 · DUEL · TUBE"),
    ("s09_commercial", "09", "商业落地现状与行业实践",
     "Google · NVIDIA · 字节 · 阿里 · Apple · Mercury · Gemini Diffusion"),
    ("s10_comparison", "10", "综合对比表与未来方向",
     "全景对比表 · RL 训练对比 · 四大未来方向"),
]

# Collect section contents
section_contents = {}
# First part has TOC - we'll extract overview from it
# The overview content is between container start and first h2
overview_content = parts[0]
# Remove the TOC div from overview
overview_content = re.sub(r'<div class="toc">.*?</div>\s*', '', overview_content, flags=re.DOTALL)
# The overview section also starts with an h2 that was embedded
section_contents["s01_overview"] = overview_content.strip()

for i, (fname, num, title, desc) in enumerate(sections_meta):
    idx = 1 + i * 2  # h2 tag index in parts
    if idx < len(parts):
        h2_tag = parts[idx]
        content_after = parts[idx + 1] if idx + 1 < len(parts) else ""
        # For section 1, we already have the content
        if i == 0:
            section_contents[fname] = h2_tag + content_after
        else:
            section_contents[fname] = h2_tag + content_after

# Generate each sub-page
def make_head(title, fname):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 扩散语言模型前沿调研</title>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$','$'],['\\\\(','\\\\)']],
    displayMath: [['$$','$$'],['\\\\[','\\\\]']],
    ignoreHtmlClass: 'diagram|code-block'
  }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }},
  startup: {{
    pageReady: () => {{
      return MathJax.startup.defaultPageReady().then(() => {{
        document.documentElement.classList.add('mathjax-loaded');
      }});
    }}
  }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<script>
  window.addEventListener('error', function(e) {{
    if (e.target && e.target.src && e.target.src.includes('mathjax')) {{
      var s = document.createElement('script');
      s.src = 'https://unpkg.com/mathjax@3/es5/tex-svg.js';
      s.async = true;
      document.head.appendChild(s);
    }}
  }}, true);
</script>
<link rel="stylesheet" href="shared.css">
<script>
window.addEventListener('load', function() {{
  var check = setInterval(function() {{
    if (window.MathJax && MathJax.startup && MathJax.startup.promise) {{
      clearInterval(check);
      MathJax.startup.promise.then(function() {{
        document.documentElement.classList.add('mathjax-loaded');
      }});
    }}
  }}, 200);
  setTimeout(function() {{ clearInterval(check); document.documentElement.classList.add('mathjax-loaded'); }}, 15000);
}});
</script>
</head>
<body>
<div id="math-loading"><div class="spinner"></div>正在加载数学公式渲染...</div>
"""

def make_nav(active_idx):
    links = []
    for i, (fname, num, title, desc) in enumerate(sections_meta):
        cls = ' class="active"' if i == active_idx else ''
        links.append(f'<a href="{fname}.html"{cls}>{num}</a>')
    nav_items = ' <span class="sep">|</span> '.join(links)
    return f"""<nav class="nav-bar">
  <a href="index.html" style="font-weight:700;color:var(--accent);">首页</a>
  <span class="sep">|</span>
  {nav_items}
</nav>"""

def make_page_nav(active_idx):
    prev_link = ""
    next_link = ""
    if active_idx > 0:
        pf, pn = sections_meta[active_idx - 1][0], sections_meta[active_idx - 1][2]
        prev_link = f'<a href="{pf}.html">&larr; {pn}</a>'
    else:
        prev_link = '<a href="index.html">&larr; 首页</a>'
    if active_idx < len(sections_meta) - 1:
        nf, nn = sections_meta[active_idx + 1][0], sections_meta[active_idx + 1][2]
        next_link = f'<a href="{nf}.html">{nn} &rarr;</a>'
    else:
        next_link = '<a href="index.html">返回首页</a>'
    return f'<div class="page-nav">{prev_link}{next_link}</div>'

def make_footer():
    return """
<div style="margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--border); text-align: center; color: var(--text2); font-size: 0.85em;">
  <p>本文档基于讨论笔记 + 50+ 篇论文深度调研整理 · 2026.06</p>
  <p>涵盖：D3PM · MDLM · LLaDA · Dream · SEDD · DiffuLLaMA · COLA · CADD · ELF · LangFlow · TextLDM · Plaid · DFlash · BD3LM · SDAR · Fast-dLLM · Nemotron · S2D2 · SimSD · Trajectory-Level SD · Mercury 2 · SPG · GDSD · FS-DFM</p>
</div>
</div><!-- container end -->
</body>
</html>
"""

# Write sub-pages
for i, (fname, num, title, desc) in enumerate(sections_meta):
    content = section_contents.get(fname, "")
    page = make_head(title, fname)
    page += make_nav(i)
    page += f'\n<div class="container">\n'
    page += content
    page += make_page_nav(i)
    page += make_footer()
    path = os.path.join(DIR, f"{fname}.html")
    with open(path, 'w') as f:
        f.write(page)
    print(f"  Created {fname}.html ({len(page)} bytes)")

# Create index page
index_html = make_head("扩散语言模型前沿调研", "index")
index_html += make_nav(-1)
index_html += """
<div class="hero">
  <h1>扩散语言模型前沿调研</h1>
  <div class="subtitle">离散 / 连续 / 块扩散三大路线全景 · 预测范式大一统 · DFlash vs MTP · Scaling Laws · ELBO 与 RL 训练</div>
  <div class="meta">2026.06 · 基于讨论笔记 + 50+ 篇论文深度调研 · 覆盖 D3PM → MDLM → LLaDA → Dream → ELF → COLA → CADD 全链路</div>
</div>

<div class="container">

<div class="toc">
  <h2>目录 · 共 10 章</h2>
  <p style="color:var(--text2);font-size:0.9em;margin-bottom:16px;">点击各章节卡片进入详细页面。每章独立成页，方便阅读与检索。</p>
</div>

<div class="index-grid">
"""

card_descs = [
    ("扩散语言模型 (DLM) 是近两年快速崛起的研究方向。本章从宏观视角梳理四大流派：离散空间扩散、块扩散/半自回归、连续隐空间扩散、预测范式选择，为后续各章提供全局地图。",
     "四大流派 · 核心讨论观点 · DLM vs AR 定位"),
    ("离散扩散坚持文本的离散本质，通过转移矩阵定义加噪/去噪。从 D3PM 的三种转移矩阵设计，到 MDLM 的连续时间简化，到 LLaDA 的 8B 规模验证，再到 Dream 的 AR 初始化 + 自适应噪声，完整呈现离散扩散的技术演进。SEDD 提出第四预测范式，DiffuLLaMA 证明 AR→DLM 适配路线。",
     "D3PM (NeurIPS'21) · MDLM (NeurIPS'24) · LLaDA 8B (ICLR'25) · Dream 7B · SEDD · DiffuLLaMA · Seed Diffusion"),
    ("块扩散的核心思想：宏观自回归保证长文本可控性，微观块内并行去噪提供速度优势。BD3LM 建立了 AR↔Diffusion 的插值框架 (ICLR'25 Oral)，SDAR 将预训练 AR 模型轻量转换为块扩散。DFlash 用块扩散做投机解码实现 6x 加速，Nemotron 统一三模态，Fast-dLLM 实现 27.6x 吞吐量提升。",
     "BD3LM (ICLR'25 Oral) · SDAR · DFlash 6x · Nemotron 三模态 · TiDAR · Fast-dLLM 27.6x · DiffuSpec"),
    ("如何桥接离散文本与连续空间？三条路线并行：Embedding 空间扩散 (Diffusion-LM → ELF → LangFlow)、VAE 隐空间扩散 (COLA → TextLDM → Plaid)、连续增强离散扩散 (Apple CADD 7B)。何恺明团队的 MAR→Back to Basics→ELF 路线尤其值得关注。",
     "Diffusion-LM (NeurIPS'22) · COLA 2.3B · CADD 7B · ELF · LangFlow · TextLDM · Plaid · CCDD"),
    ("模型在预测什么？这决定了梯度稳定性和生成质量。ε-prediction (噪声)、x₀-prediction (干净数据)、v-prediction (速度)、Ratio Estimation (SEDD)、Discrete Flow Matching (FS-DFM 128x 加速)。同时对比 Flow Matching 与 Diffusion 的本质差异。",
     "ε / x₀ / v / Ratio / Discrete FM · Flow Matching vs Diffusion · Back to Basics"),
    ("首个覆盖 25M→10B 参数的离散扩散 scaling 研究 (NeurIPS'25) 揭示：噪声类型决定 scaling 行为。ICML'26 的颠覆性结论：'Masked diffusion isn't the future paradigm'——应评估速度-质量 Pareto 前沿，而非仅看困惑度。DLM 过拟合在投机场景下反而是优势。",
     "NeurIPS'25 Scaling · ICML'26 Sahoo · 噪声类型依赖 · 过拟合优势 · high-entropy 回避"),
    ("DFlash 用块扩散做投机解码实现 6x 加速，但 DFlash 不一定比 MTP 好。2025-2026 年迎来 dLLM 推理加速爆发期：S2D2 (4.7x)、SimSD (7.46x)、Trajectory-Level SD (7-14x) 等。从'token 投机'到'轨迹投机'的范式跃迁。AR vs DLM draft model 的发散性深度分析。",
     "DFlash vs MTP · S2D2 · SimSD · Trajectory-Level SD · Self-Spec · BlockSpec · APD · 发散性分析"),
    ("离散扩散模型的似然不可精确计算——ELBO 是有偏的下界估计，严重影响 RL 训练。SPG (Meta) 用上下界构造'三明治'策略梯度；GDSD 通过自蒸馏完全绕过 ELBO。DUEL 和 TUBE 分别从精确似然和上界两个方向逼近真实值。",
     "ELBO 偏差诊断 · SPG 三明治梯度 · GDSD 自蒸馏 · DUEL · TUBE"),
    ("Google Gemini Diffusion (1479 tok/s)、NVIDIA Nemotron-Diffusion (3-4x)、字节 Seed Diffusion (2146 tok/s)、阿里 LLaDA 系列 (8B→100B MoE)、Apple CADD 7B、Inception Mercury 2 (1196 tok/s)。Gemini Diffusion 的'失败'评估与 Mercury 2 的首个商用突破。",
     "Google · NVIDIA · 字节 · 阿里 · Apple · Inception Labs · Gemini · Mercury 2"),
    ("18 种核心方法的全景对比表（含预测范式标注）、DLM RL 训练方法对比。四大未来方向判断：扩散投机解码成为主流加速范式、连续 Flow Matching 取代传统扩散、RL 训练是核心瓶颈、Scaling 仍未有定论。",
     "全景对比表 · RL 训练对比 · 四大未来方向 · 核心结论"),
]

for i, (fname, num, title, desc) in enumerate(sections_meta):
    papers = card_descs[i][1]
    long_desc = card_descs[i][0]
    index_html += f"""
  <a class="index-card" href="{fname}.html">
    <span class="ic-num">第 {num} 章</span>
    <div class="ic-title">{title}</div>
    <div class="ic-desc">{long_desc}</div>
    <div class="ic-papers">{papers}</div>
  </a>
"""

index_html += """
</div>

<div class="insight" style="margin-top: 32px;">
  <div class="insight-title">讨论核心结论</div>
  <p>当前 dLLM 领域处于"加速验证已成立，质量追赶进行中"的阶段。最具落地价值的方向是扩散投机解码（DFlash 路线），最具学术突破潜力的是连续 Flow Matching + RL 训练（ELF + SPG/GDSD 路线）。纯扩散 LM 的 scaling 需要更多实验验证——Gemini 的"失败"和 Seed 的成功都表明，scaling law 在 dLLM 上的表现比 AR 更复杂。</p>
</div>
"""
index_html += make_footer()

with open(os.path.join(DIR, "index.html"), 'w') as f:
    f.write(index_html)
print(f"  Created index.html ({len(index_html)} bytes)")
print(f"\nDone! {len(sections_meta) + 1} files generated in {DIR}")
