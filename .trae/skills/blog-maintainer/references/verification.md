# 检查、预览与发布

## 环境和基本命令

在已确认的仓库根目录使用当前 `Makefile`。当前默认环境为 `~/.cache/stein-notes/venv`，
产物为 `/tmp/my-blogs-site-build`，预览端口为 8000；这些值可通过参数覆盖，不代表环境或服务已存在。
Python 依赖由 `requirements.txt` 固定，不需要为站点运行安装 Node/Ruby。

```bash
# 环境缺失或依赖不符时
make setup

# 每次源文件更新后
make check

# 需要真实预览时
make preview PORT=8766

# 需要单独导出时，目的目录必须为空、与源和产物不重叠
make export DEST=/tmp/site-export-new
```

有效自定义环境可用 `make VENV=/path/to/venv OUTPUT=/tmp/dedicated-site-build check`。
启动预览前检查端口与现有服务；复用指向同一 OUTPUT 的服务，否则选空闲端口并后台启动。
不要杀掉不属于本任务的服务，不从源码根目录启动服务器，不假称一个历史 URL 仍可访问。

`make check` 构建后检查同一产物；已有产物可用 `scripts/check.py --output ...` 检查，
但源文件变化后旧产物应被视为过期，不能跳过重建。输出路径由现有工具验证归属，不覆盖无关目录。

## 按改动范围验收

| 改动 | 最少有意义的验证 |
|---|---|
| 文章内容、标题、摘要或标签 | `make check`；本页渲染、目录/锚点、搜索命中、关联入口；受迁移基线覆盖时加保留检查 |
| 首页、导航、页脚或全站样式 | `make check`；首页/博客/个人页/代表长文章的 390/768/1440px、焦点与导航 |
| 博客筛选或兼容跳转 | `make check`；主题/类型/关键词/排序、查询刷新/分享、无结果/清除、旧参数、新条件优先、片段、无 JavaScript |
| 文章公共阅读组件 | `make check`；代表目录结构、系列 prev/next、MathJax/KaTeX、原交互、SVG 比例、宽表格/代码/长公式、无脚本和加载失败回退 |
| 论文/个人资料/CV/PDF | `make check`；首页精选/论文列表/详情/个人介绍/在线 CV；PDF 涉及改动时比对下载文件与新旧 URL |
| 登记契约、构建、校验、资源导出 | `scripts/test_pipeline.py`；从空产物隔离构建、重复字节一致、源未改写、失败保留上一版本、草稿与旧输出排除、预览/导出一致 |
| 自动更新逻辑 | `.automation/test-frontier-update.py` 的隔离样本，以及带两个参数的真实 `validate-frontier.sh`；不使用真实 push 测试 |

```bash
# 使用固定依赖解释器，命令路径可以替换为有效自定义环境
"$HOME/.cache/stein-notes/venv/bin/python" scripts/test_pipeline.py
python3 .automation/test-frontier-update.py

# 基线覆盖的正文/资源变更并已逐项记录后
python3 docs/verify-content-migration.py --require-clean
```

不为纯文案或无影响的可逆调整编写镜像式测试。检查通过后不重复整套测试，除非后续改动或失败
造成新的未解决问题。只把本次实际执行的检查写入结果；未启动的浏览器、未运行的 GPU 实验、
未访问的外部网站不能记为通过。

## 浏览器证据

- 用实际 UI 操作验证主要链路，源码检查用于定位，不替代点击/输入的结果。
- 测试宽内容在自己的容器滚动，页面整体无横向溢出；查看图表尺寸或截图时区分真正的科研 SVG 与数学排版内部字形。
- 保留原问答展开、目录切换等交互。测试跳转正文、Tab/Enter、可见焦点和有效目标，而不只检查存在按钮。
- 禁用 JavaScript 时应能看到本地文章、章节与正文；公式允许显示 TeX 原文，不能有全屏加载层遮挡。模拟 CDN 失败应使用隔离浏览器上下文，不修改实际网站来源。
- 临时浏览器脚本、截图、隔离 checkout、缓存、日志放在工作区外；需要正式交付的报告和资源放用户指定目录或工作区中，并清楚标明它们不是发布输入。

## 发布与同步

先确认当前已有授权。一般编辑请求不授权提交、推送、切换 Pages、停用旧站、归档或设置定时器；
已明确授权的步骤直接推进，不重复审批。使用 `gh` 进行 GitHub 查询和操作。

1. 获准提交时查看暂存与未暂存差异、未跟踪文件和近期提交风格；只添加相关文件。
   不提交敏感凭据、虚拟环境或产物，不改 Git 配置、不跳过 hooks、不 amend，除非相应动作明确获准。
2. 获准推送时核对当前分支、remote 与差异范围，推送对应分支；禁止用强制推送代替正常处理。
3. 获准切换或部署时读取当前 Pages 设置与工作流；沿用 `.github/workflows/pages.yml` 的
   build → 校验 → 导出 → deploy 依赖，不能绕过失败步骤。
4. 用 `gh run list/view` 或对应 GitHub API 检查实际运行和部署提交，再读取线上
   `build-info.json`，比对 commit 与目标版本。推送成功不能替代部署成功。
5. 访问线上首页、博客搜索、受影响文章/章节、论文、CV/PDF和有关旧地址，核对真实行为。
6. 切换旧 `/wyx0226.github.io/` 前缀时先核对旧项目 Pages；只有停用已授权且新主站已准备好时才执行。
   归档旧仓库需独立授权，保留其历史与许可。

身份链接以当前 `content/site.json` 和 Git remote 为准。当前约定为：

- 个人 GitHub 主页 `https://github.com/stein-wang0226`
- 主维护仓库 `https://github.com/stein-wang0226/stein-wang0226.github.io`
- 主站 `https://stein-wang0226.github.io/`，统一入口 `/blog/`

每次区分本地修改、已提交、已推送、部署成功和线上已核对五个状态，提供证据与未完成范围。
当前仓库文档中的旧验收时间、计数、commit 或“未同步”记录属于历史状态，不能替代新的查询。
