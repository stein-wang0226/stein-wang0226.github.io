"""Assemble explicitly marked teaching fragments; preserve original HTML text."""
from collections import defaultdict
import html
from html.parser import HTMLParser
import json
import re
from urllib.parse import unquote, urljoin, urlsplit

from render import rel, route_path

START = "<!-- READING:FRAGMENT:START -->"
END = "<!-- READING:FRAGMENT:END -->"

# Short, editorially selected links keep derivation and review in one directory.
FOCUS = {
    "transformer-decoder-flow": [("training-forward", "逐步训练前向"), ("numerical-forward", "完整数值算例"), ("decode-forward", "Prefill → decode"), ("code", "完整 PyTorch")],
    "architecture-transformer": [("reading-section-3", "因果 mask"), ("reading-section-5", "标签移位与梯度"), ("reading-section-7", "实现检查")],
    "architecture-attention": [("course-heading-1", "点积缩放推导"), ("reading-section-4", "RoPE 相对位移"), ("reading-section-7", "缓存与自测")],
    "architecture-moe": [("reading-section-2", "FFN 参数账本"), ("reading-section-4", "负载与容量"), ("reading-section-8", "常见失败")],
    "architecture-residual": [("reading-section-2", "Norm 梯度路径"), ("reading-section-3", "RMSNorm 算例"), ("reading-section-6", "故障对照")],
    "architecture-hybrid": [("reading-section-2", "外积状态"), ("reading-section-3", "衰减与定向更新"), ("reading-section-7", "信息损失检查")],
    "architecture-comparison": [("reading-section-2", "六条比较轴"), ("reading-section-7", "共同协议")],
    "llm-training-pretraining": [("reading-section-3", "条件预测"), ("scaling-derivation", "Scaling Law 推导"), ("scaling-ladder", "实验阶梯"), ("mup-transfer", "μP 超参数迁移"), ("wsd-schedule", "WSD 调度")],
    "llm-training-midtraining": [("data", "CSV 任务与目标"), ("reading-section-6", "配比与回放"), ("results", "受控结果")],
    "llm-training-sft-rft": [("course-heading-2", "角色 mask 与梯度"), ("course-heading-3", "轨迹准入"), ("course-heading-4", "拒绝采样偏移")],
    "llm-training-rl-evaluation": [("course-heading-2", "CSV 验收算例"), ("course-heading-4", "训练与交付指标"), ("course-heading-6", "故障定位")],
    "training-methods-systems": [("adamw-derivation", "AdamW 逐步推导"), ("muon-mechanism", "Muon 更新几何"), ("training-frameworks", "框架与训练架构"), ("roofline", "性能瓶颈"), ("state-sharding", "ZeRO 显存账本")],
    "posttraining-supervision": [("reading-section-2", "目标与 mask"), ("dpo-derivation", "DPO 推导"), ("reading-section-9", "RL 与 OPD 准入")],
    "posttraining-algorithms": [("baseline-proof", "PG 与 baseline"), ("ppo-piecewise", "PPO 分段目标"), ("course-heading-4", "论文数值配方"), ("course-heading-6", "训练诊断"), ("interview-cards", "GRPO 面试追问")],
    "posttraining-opd": [("reading-section-2", "局部 KL 梯度"), ("reading-section-3", "采样信号"), ("course-heading-2", "OPD 监控")],
    "posttraining-rewards": [("reading-section-6", "重复奖励漏洞"), ("reading-section-8", "多步信用"), ("course-heading-4", "机制追问")],
    "posttraining-frameworks": [("course-heading-1", "配置映射"), ("reading-section-5", "三种偏移"), ("reading-section-10", "完整算力成本")],
    "posttraining-cases": [("reading-section-2", "代码修复轨迹"), ("reading-section-4", "科学分析合同"), ("reading-section-9", "诊断与成本")],
    "agent-rag": [("course-heading-1", "BM25 推导"), ("course-heading-3", "RRF 算例"), ("reading-section-6", "分层评测")],
    "agent-planning": [("course-heading-1", "BoN 存在与选择"), ("course-heading-2", "UCT 算例"), ("reading-section-6", "预算与停止")],
    "agent-trust": [("reading-section-3", "隔离机制"), ("reading-section-5", "攻击分母"), ("reading-section-6", "理解检查")],
    "agent-task-synthesis": [("reading-section-4", "公开与隐藏合同"), ("reading-section-6", "数值容差"), ("reading-section-13", "最小对照")],
    "scientific-task-family": [("course-heading-2", "配对 design"), ("course-heading-3", "Contrast 推导"), ("course-heading-4", "BH 算例")],
    "cluster-training-evaluation": [("course-heading-2", "配对差分"), ("course-heading-3", "依赖与 bootstrap"), ("reading-section-7", "失败分类")],
    "agent-benchmark-map": [("course-heading-2", "pass@k 组合推导"), ("course-heading-3", "质量与成本分母"), ("reading-section-21", "留出设计")],
    "serving-runtime": [("reading-section-3", "分页状态"), ("reading-section-4", "Prefix 复用"), ("reading-section-7", "调度自测")],
    "serving-parallel": [("reading-section-4", "量化误差"), ("course-heading-1", "投机精确性"), ("course-heading-2", "接受长度与速度")],
    "serving-capacity": [("reading-section-3", "70B 容量算例"), ("reading-section-4", "延迟分母"), ("reading-section-6", "单位成功成本")],
    "research-agent-data": [("reading-section-2", "四条合成路线"), ("course-heading-2", "环境迁移"), ("reading-section-6", "榜单审计")],
    "research-agentic-rl": [("reading-section-6", "信用分配路线"), ("reading-section-7", "有效学习机会"), ("reading-section-8", "异步偏差")],
    "research-architecture-landscape": [("reading-section-4", "GDN 到 KDA"), ("reading-section-5", "实际层计划"), ("reading-section-16", "比较协议")],
    "research-base-architecture": [("reading-section-3", "CED 张量来源"), ("reading-section-9", "890 B/token 推导"), ("reading-section-10", "Replay 边界")],
    "research-architecture-training": [("reading-section-3", "AttnRes 深度注意力"), ("reading-section-4", "mHC 凸组合"), ("recurrent-depth", "递归深度")],
    "research-inference-diffusion": [("reading-section-2", "三类 drafter"), ("reading-section-4", "选择偏差反例"), ("course-heading-1", "并发退化")],
    "research-agent-frontiers": [("reading-section-3", "科学能力三层"), ("reading-section-5", "时间切分"), ("reading-section-6", "并行资源账本")],
    "dlm-overview": [("generation", "四 token 算例"), ("lineage", "路线与机制")],
    "dlm-paradigms": [("vp-conversion", "VP 坐标换算"), ("loss-weight", "时间权重"), ("discrete-score", "离散比率")],
    "dlm-discrete": [("bayes", "反向贝叶斯"), ("weighted-mlm", "KL 到 CE"), ("llada", "LLaDA 数值配方")],
    "dlm-block": [("factorization", "块因子化"), ("attention-mask", "训练可见性"), ("cache", "缓存充分条件")],
    "dlm-continuous": [("flow", "路径方向"), ("rounding", "MSE 与 CE 反例"), ("evaluation", "三层误差")],
    "dlm-elbo-rl": [("elbo-gap", "三种误差"), ("spg", "SPG 符号例"), ("diagnosis", "训练诊断")],
    "dlm-scaling": [("compute-optimal", "最优幂律"), ("crossover", "数据复用边界")],
    "dlm-speculative": [("acceptance", "尾和期望"), ("cycle-cost", "真实周期成本")],
    "dlm-comparison": [("comparison", "机制比较"), ("protocol", "共同合同"), ("interview", "复述与追问")],
    "dlm-loop-transformer": [("gradient", "共享参数梯度"), ("halting", "停止与质量")],
    "dlm-ddpm": [("decomposition", "ELBO 裂项"), ("posterior", "高斯配方"), ("noise-loss", "噪声损失")],
    "dlm-flow-sde": [("variance-proof", "条件到边际证明"), ("probability-flow", "SDE 与 ODE"), ("vp-sde", "逆向 VP")],
    "dlm-vae": [("reparameterization", "重参数化梯度"), ("gaussian-kl", "高斯 KL 算例"), ("vq", "VQ 梯度职责")],
    "dlm-commercial": [("evidence", "产品证据"), ("latency", "Burst 延迟算例")],
}


def parent_of(entry, by_id):
    parent = by_id.get(entry.get("series"))
    return parent if parent and parent.get("reading_mode") == "longform" else None


def chapters_of(parent, entries):
    return sorted((e for e in entries if e.get("series") == parent["id"]
                   and e["status"] == "published"), key=lambda e: e["order"])


def short_title(entry):
    return html.escape(re.sub(r"^\d+\s*·\s*", "", entry["title"]))


def fragment(root, entry):
    text = (root / entry["source"]).read_text(encoding="utf-8")
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError(f"course: {entry['id']} requires one explicitly marked fragment")
    result = text.split(START, 1)[1].split(END, 1)[0]
    result = teaching_diagrams(root, result)
    if re.search(r"<(?:html|head|body|script)\b", result, re.I):
        raise ValueError(f"course: {entry['id']} fragment contains a document shell or script")
    return result


def teaching_diagrams(root, text):
    """Reuse six archived teaching SVGs with explicit, current annotations."""
    marker = r"<!-- READING:RL-DIAGRAM:(\d) -->"
    if not re.search(marker, text):
        return text
    path = root / "assets/archive/blog-before-learning-rework-20261115/posts/rl-interview-guide/index.html.txt"
    diagrams = re.findall(r"<svg\b.*?</svg>", path.read_text(encoding="utf-8"), re.S)
    if len(diagrams) != 6:
        raise ValueError("course: expected six intact RL teaching diagrams")
    notes = {
        1: "价值分解：这里的平均按当前策略的动作分布计算；优势为正表示优于该状态的策略平均。",
        2: "本图取 γ=1。一般折扣目标还需外层 γᵗ；删掉过去奖励不改期望，但不保证每个任务上方差都下降。",
        3: "一步 Actor-Critic 示例取 γ=1，真实 terminal 的下一状态 value 为0。δ是含 bootstrap 误差的优势估计。",
        4: "图示只描述固定优势时的 clipped 策略项；其他样本、共享参数和 KL 项仍可能改变该动作概率。",
        5: "更新 epochs 由具体配方决定，mini-batch 数不等于 epochs。重新采样与有限复用需共同控制策略偏移。",
        6: "反馈来源与优化算法是两条分类轴。显式奖励模型并非所有偏好优化流程的必需组件。",
    }
    replacements = {
        1: [("所有动作的平均水平", "按策略加权的平均水平"), ("→ 好动作", "→ 优于策略平均"),
            ("→ 坏动作", "→ 低于策略平均")],
        2: [("⚠ ∇P 无法直接算", "用对数导数改写采样估计"),
            ("→ 方差更小", "→ 去除无关的过去奖励")],
        3: [("两个网络在循环中互相促进：Critic 评分更准 → Actor 策略更好 → 数据质量更高",
             "Actor 更新策略；Critic 拟合回报，两条目标分别检查收敛与误差")],
        5: [("K = 3~10，同一批数据反复用 ← PPO 的效率优势（对比 REINFORCE 用一次就扔）",
             "K 按配方设定；保存 old log-prob，监控偏移、KL 与 clip fraction"),
            ("新策略的数据分布已变化，旧数据不再有效 → 必须重新采集",
             "有限复用后重新采样；长期回放需要另外的目标与偏移处理")],
        6: [("reward 从人类偏好学习（需 RM）", "人类偏好：训练 RM 或直接偏好优化"),
            ("reward 来自可验证规则（不需 RM）", "可验证结果：规则或独立 verifier"),
            ("当前主流", "可验证任务"),
            ("三者的差异在于 reward 来源", "三者主要区分反馈来源")],
    }
    def replace(match):
        number = int(match[1])
        if number not in notes:
            raise ValueError("course: unknown RL diagram")
        svg = diagrams[number - 1]
        for before, after in replacements.get(number, []):
            svg = svg.replace(before, after)
        # Figure-local names avoid collisions in the assembled topic.
        ids = re.findall(r'\bid=["\']([^"\']+)', svg)
        for identifier in sorted(ids, key=len, reverse=True):
            svg = re.sub(r'(?<=id=")' + re.escape(identifier) + r'(?=")',
                         f"rl-diagram-{number}-{identifier}", svg)
            svg = svg.replace(f"#{identifier})", f"#rl-diagram-{number}-{identifier})")
        return (f'<figure class="teaching-diagram" data-rl-diagram="{number}">{svg}'
                f'<figcaption>{notes[number]}</figcaption></figure>')
    return re.sub(marker, replace, text)


def baseline(root, identifier):
    path = root / "docs/organization-audit-20261114.json"
    if not path.is_file():
        return {}
    return next((p for p in json.loads(path.read_text())["pages"]
                 if p["id"] == identifier), {})


class Fragment(HTMLParser):
    """Edit only attribute/heading spans, without serializing scientific DOM."""
    def __init__(self, text, entry, root):
        super().__init__(convert_charrefs=False)
        self.text, self.entry = text, entry
        self.offsets = [0]
        for match in re.finditer("\n", text):
            self.offsets.append(match.end())
        self.ids, self.tags, self.headings, self.stack = set(), [], [], []
        self.old = baseline(root, entry["id"])
        self.legacy = defaultdict(list)
        for item in self.old.get("generated_headings", []):
            self.legacy[item["label"]].append(item["anchor"])
        self.feed(text)
        number = 0
        for item in self.headings:
            if item["id"]:
                continue
            label = re.sub(r"<[^>]+>", "", text[item["inner"]:item["end"]]).strip()
            prior = self.legacy[label]
            identifier = prior.pop(0) if prior else None
            if not identifier:
                number += 1
                identifier = f"course-heading-{number}"
                while identifier in self.ids:
                    number += 1
                    identifier = f"course-heading-{number}"
            item["id"] = identifier
            self.ids.add(identifier)
        # Includes previously generated reading directory anchors.
        self.aliases = sorted(set(self.old.get("public_anchors", [])) - self.ids)
        self.all_ids = self.ids | set(self.aliases)

    def source_offset(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                raise ValueError(f"course: {self.entry['id']} duplicate #{attrs['id']}")
            self.ids.add(attrs["id"])
        start = self.source_offset()
        item = {"tag": tag, "start": start, "raw": self.get_starttag_text(),
                "attrs": attrs, "id": attrs.get("id")}
        self.tags.append(item)
        if tag in {"h2", "h3", "h4", "h5"}:
            item["inner"] = start + len(item["raw"])
            self.stack.append(item)

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1]["tag"] == tag:
            item = self.stack.pop()
            item["end"] = self.source_offset()
            self.headings.append(item)


def public_target(entry, anchor, by_id):
    # Bookmarks into a former assembled topic keep their chapter namespace.
    for child in by_id.values():
        if child.get("relocated_from") == entry["id"] and (
                anchor == child["id"] or anchor.startswith(child["id"] + "--")):
            suffix = anchor[len(child["id"]):].removeprefix("--")
            return public_target(child, suffix, by_id)
    parent = parent_of(entry, by_id)
    if parent:
        return parent["url"], entry["id"] + ("--" + anchor if anchor else "")
    return entry["url"], anchor


def relocated_directory(ctx, entry, text):
    """Render old chapter bookmarks from catalog history, without duplicate prose."""
    marker = "<!-- READING:RELOCATED -->"
    if marker not in text:
        return text
    children = [e for e in ctx.entries if e.get("relocated_from") == entry["id"]]
    mapping, rows, aliases = {}, [], []
    for child in children:
        doc = Fragment(fragment(ctx.root, child), child, ctx.root)
        parent = parent_of(child, ctx.by_id)
        route, anchor = public_target(child, "", ctx.by_id)
        href = ctx.rel(entry["url"], route) + "#" + anchor
        mapping[child["id"]] = href
        rows.append(f'<li id="{child["id"]}"><a href="{href}">'
                    f'{html.escape(parent["title"])} → {short_title(child)}</a></li>')
        for old in sorted(doc.all_ids):
            key = child["id"] + "--" + old
            mapping[key] = href + "--" + old
            aliases.append(f'<span class="reading-anchor" id="{html.escape(key, quote=True)}"></span>')
    directory = ('<section id="relocated-topics"><h2>原章节现在在哪里</h2>'
                 '<p>各节正文已在对应主题连续展开。旧书签会直接定位；也可使用以下链接。</p>'
                 '<ul>' + "".join(rows) + '</ul>' + "".join(aliases) + '</section>')
    script = ('<script>(()=>{const routes=' + json.dumps(mapping, ensure_ascii=False) +
              ';const move=()=>{let key="";try{key=decodeURIComponent(location.hash.slice(1))}catch{}'
              'if(!routes[key])return;const target=new URL(routes[key],location.href);'
              'target.search=location.search;location.replace(target.href)};'
              'addEventListener("hashchange",move);move()})();</script>')
    return text.replace(marker, directory).replace("</body>", script + "</body>")


def rewrite_link(value, entry, output_url, by_id, site_url=""):
    url = urlsplit(urljoin("https://notes.local" + entry["url"], value))
    if url.scheme not in {"http", "https"}:
        return value
    if url.netloc not in {"notes.local", urlsplit(site_url).netloc}:
        return value
    target = next((e for e in by_id.values() if e["origin"] == "local"
                   and route_path(e["url"]) == route_path(url.path)), None)
    path, anchor = (public_target(target, unquote(url.fragment), by_id) if target
                    else (url.path, unquote(url.fragment)))
    return rel(output_url, path + ("?" + url.query if url.query else "") +
               ("#" + anchor if anchor else ""))


def render_fragment(root, entry, output_url, by_id, site_url=""):
    doc = Fragment(fragment(root, entry), entry, root)
    prefix = entry["id"] + "--"
    edits = []
    for item in doc.tags:
        raw = item["raw"]
        def attribute(match):
            key, quote, value = match[1], match[2], html.unescape(match[3])
            if key == "id":
                value = prefix + value
            elif key in {"href", "xlink:href"} and value.startswith("#") and value[1:] in doc.all_ids:
                value = "#" + prefix + value[1:]
            elif key in {"href", "src", "poster", "data"}:
                value = rewrite_link(value, entry, output_url, by_id, site_url)
            elif key in {"for", "aria-labelledby", "aria-describedby", "aria-controls", "headers"}:
                value = " ".join(prefix + v if v in doc.all_ids else v for v in value.split())
            value = re.sub(r"url\(#([^)]+)\)",
                           lambda m: "url(#" + prefix + m[1] + ")" if m[1] in doc.all_ids else m[0],
                           value)
            return f'{key}={quote}{html.escape(value, quote=True)}{quote}'
        raw = re.sub(r'([\w:-]+)=(["\'])(.*?)\2', attribute, raw, flags=re.S)
        if item in doc.headings:
            level = int(item["tag"][1])
            raw = re.sub(r"^<h[2-5]", f"<h{level + 1}", raw)
            if not item["attrs"].get("id"):
                raw = raw[:-1] + f' id="{prefix}{html.escape(item["id"], quote=True)}">'
            edits.append((item["end"], item["end"] + len(item["tag"]) + 3, f"</h{level + 1}>"))
        edits.append((item["start"], item["start"] + len(item["raw"]), raw))
    body = doc.text
    for start, end, value in sorted(edits, reverse=True):
        body = body[:start] + value + body[end:]
    aliases = "".join(f'<span class="reading-anchor" id="{prefix}{html.escape(i, quote=True)}"></span>'
                      for i in doc.aliases)
    title = short_title(entry)
    content = aliases + body
    if entry.get("chapter_group") in {"prerequisite", "extension", "reference"}:
        content = '<details class="course-extension"><summary>展开本节推导与参考</summary>' + content + "</details>"
    return (f'<section class="course-chapter" id="{entry["id"]}" tabindex="-1">'
            f'<h2>{entry["order"]}. {title}</h2>{content}</section>')


def anchors(root, entry, entries):
    found = set(re.findall(r'\bid=["\']([^"\']+)', (root / entry["source"]).read_text()))
    if entry.get("reading_mode") == "longform":
        found.update(baseline(root, entry["id"]).get("public_anchors", []))
        for child in chapters_of(entry, entries):
            doc = Fragment(fragment(root, child), child, root)
            found.add(child["id"])
            found.update(child["id"] + "--" + i for i in doc.all_ids)
        found.add("course-toc")
    return found


def assemble(ctx, entry, text):
    if text.count("<!-- READING:COURSE -->") != 1:
        raise ValueError(f"course: {entry['id']} requires one course assembly marker")
    children = chapters_of(entry, ctx.entries)
    contents = "".join(render_fragment(ctx.root, e, entry["url"], ctx.by_id, ctx.site["url"])
                       for e in children)
    def chapter_links(child):
        doc = Fragment(fragment(ctx.root, child), child, ctx.root)
        focus = FOCUS.get(child["id"], [])
        if not focus:
            raise ValueError(f"course: {child['id']} requires curated directory links")
        for anchor, _ in focus:
            if anchor not in {h["id"] for h in doc.headings}:
                raise ValueError(f"course: {child['id']} missing focus heading #{anchor}")
        links = "".join(f'<li><a href="#{child["id"]}--{html.escape(anchor, quote=True)}">'
                        f'{html.escape(label)}</a></li>' for anchor, label in focus)
        return (f'<li data-chapter="{child["id"]}"><a href="#{child["id"]}">'
                f'{short_title(child)}</a><ul class="course-focus">{links}</ul></li>')
    directory = ('<details class="course-toc" id="course-toc" open>'
                 '<summary>本页目录</summary><nav aria-label="页内课程目录"><ol>' +
                 "".join(chapter_links(e) for e in children) + "</ol></nav></details>")
    text = text.replace("<!-- READING:COURSE -->",
                        '<div class="course-layout">' + directory +
                        '<div class="course-body">' + contents + '</div></div>')
    for path in ("course.css",):
        text = text.replace("</head>", f'<link rel="stylesheet" href="{ctx.asset(entry["url"], "/assets/site/" + path)}"></head>', 1)
    text = text.replace("</head>", f'<script defer src="{ctx.asset(entry["url"], "/assets/site/course.js")}"></script></head>', 1)
    return text


def decorate_course(ctx, entry, text):
    """One introduction, one directory, and navigation between whole topics."""
    path = entry["url"]
    text = assemble(ctx, entry, text)
    match = re.search(r"(<body\b[^>]*>)(.*)(</body>)", text, re.S | re.I)
    if not match:
        raise ValueError(f"course: {entry['id']} missing complete body")
    body = match[2]
    present = set(re.findall(r'\bid=["\']([^"\']+)', body))
    aliases = "".join(f'<span class="reading-anchor" id="{html.escape(i, quote=True)}"></span>'
                      for i in baseline(ctx.root, entry["id"]).get("public_anchors", [])
                      if i not in present and i != "site-main")
    intro = (f'<header class="reading-intro" id="site-main" tabindex="-1">'
             f'<p><a href="{ctx.rel(path, "/blog/")}#learning-paths">完整学习主线</a></p>'
             f'<h1>{html.escape(entry["title"])}</h1><p>{html.escape(entry["summary"])}</p></header>')
    main_route = ctx.site.get("learning_paths", [{}])[0].get("stages", [])
    ids = [n["entry"] for n in main_route]
    navigation = []
    if entry["id"] in ids:
        position = ids.index(entry["id"])
        for index, relationship, arrow in ((position - 1, "prev", "上一主题："),
                                            (position + 1, "next", "下一主题：")):
            if 0 <= index < len(ids):
                row = ctx.by_id[ids[index]]
                navigation.append(f'<a rel="{relationship}" href="{ctx.rel(path, row["url"])}">'
                                  f'{arrow}{html.escape(row["title"])}</a>')
    body = re.sub(r"(<table\b.*?</table>)", r'<div class="reading-table">\1</div>', body, flags=re.S | re.I)
    text = (text[:match.start(2)] + ctx.navigation(path) + intro +
            '<div class="reading-content reading-course">' + aliases + body + '</div>' +
            '<nav class="reading-series" aria-label="学习主题导航">' + "".join(navigation) +
            '</nav>' + ctx.footer(path) + text[match.end(2):])
    tags = "".join(f'<link rel="stylesheet" href="{ctx.asset(path, "/assets/site/" + name)}">'
                   for name in ("site.css", "reading.css"))
    tags += f'<script defer src="{ctx.asset(path, "/assets/site/reading.js")}"></script>'
    tags += f'<script defer src="{ctx.asset(path, "/assets/site/scroll-region.js")}"></script>'
    tags += f'<link rel="canonical" href="{ctx.canonical(path)}">'
    return text.replace("</head>", tags + "</head>", 1)


def compatibility(ctx, entry):
    parent = parent_of(entry, ctx.by_id)
    if not parent:
        raise ValueError(f"course: {entry['id']} is not an assembled chapter")
    doc = Fragment(fragment(ctx.root, entry), entry, ctx.root)
    destination = ctx.rel(entry["url"], parent["url"])
    mapping = {i: entry["id"] + "--" + i for i in doc.all_ids}
    links = '<ul>' + "".join(
        f'<li id="{html.escape(i, quote=True)}"><a href="{destination}#{html.escape(mapping[i], quote=True)}">'
        f'{html.escape(i)}</a></li>' for i in sorted(mapping) if i != "site-main") + "</ul>"
    body = (f'<h1>{html.escape(entry["title"])}</h1><p>本节已合入连续阅读的主题页。</p>'
            f'<p><a href="{destination}#{entry["id"]}">阅读本节完整正文</a></p>'
            '<noscript><p>可使用下面的旧锚点直接进入对应正文位置。</p></noscript><details>'
            '<summary>旧目录位置</summary>' + links + '</details>')
    ctx.page(entry["url"], entry["title"], body)
    path = ctx.output / route_path(entry["url"])
    text = path.read_text()
    text = re.sub(r'<link rel="canonical"[^>]*>',
                  f'<link rel="canonical" href="{ctx.canonical(parent["url"])}#{entry["id"]}">'
                  '<meta name="robots" content="noindex">', text)
    text = text.replace("</body>", '<script>const target=new URL(' +
                        json.dumps(destination) + ',location.href);const anchors=' +
                        json.dumps(dict(sorted(mapping.items())), ensure_ascii=False) + ';target.search=location.search;'
                        'let old="";try{old=decodeURIComponent(location.hash.slice(1))}catch{}'
                        'target.hash=anchors[old]||' + json.dumps(entry["id"]) + ';'
                        'location.replace(target.href);</script></body>')
    path.write_text(text, encoding="utf-8")
