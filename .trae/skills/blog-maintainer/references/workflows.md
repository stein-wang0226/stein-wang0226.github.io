# 按维护对象执行

以下路径均相对于已确认的维护仓库根目录。先读取当前配置与负责文件，规则变化以代码及用户要求为准；不要把本参考变成第二套可编辑内容登记。

## 新增文章与系列

1. 从 `content/site.json` 选用当前主题与类型；根据用户要求确定题目、摘要、ID、草稿或发布状态。
2. 用现有初始化入口创建草稿，不能覆盖同名 ID/目录：

   ```bash
   make new ID=kv-cache-notes TITLE="KV Cache 笔记" TOPIC=training-inference TYPE=principles
   ```

3. 编辑新建正文，补齐摘要、先修、核心链路、示例、来源和限制；同步登记摘要、标签、关联 ID。用户只要求草稿时保留 `draft`。
4. 要进入本地公开产物时移除 `TEMPLATE:EMPTY` 标记，完善实际内容，再将状态改为 `published`。本地 `published` 不等于已推送或已部署。
5. 命令中的动态参数须安全传递，复杂标题用参数列表或正确 shell 引号，不能执行标题里的命令替换。
6. 新增系列登记一个 `kind=series` 入口；每章登记 `kind=chapter`、父系列 ID、唯一连续正整数 `order`，并保持目录与推荐顺序合理。不要运行历史 `content/series/dlm-survey/generate.py` 覆盖现有章节。

## 更新正文与目录记录

1. 按 ID 或公开 URL 在 `content/catalog.json` 找到唯一源，先审阅其已有修改。
2. 编辑指定段落并保存邻接结构、公式、锚点、引用和交互；事实变化注明证据，纯排版不推断内容更新日期。
3. 摘要、主题或关联有变化时改同一登记记录；`related` 引用现有 ID，禁止重复或自引用。
4. 推荐文章由该记录的 `featured` 控制。搜索由标题、摘要、标签和主要标题生成；要提升检索表达时改权威文字，不写第二份搜索索引。
5. 有意修改基线覆盖的正文后，只记录本次已核对的差异与新 SHA，不重新建立原始迁移快照。需要归档时优先保留源和旧地址，调整状态及入口；涉及移位或删除需单独证明兼容与保留。

## 首页、个人主页、论文与 CV

- 首页分区改 `templates/home.html`，数据装配改 `scripts/views.py`。`render_home` 当前从 `about.md` 的 `## Research Interests` 之前提取简介；改变该分隔或简介范围时同步提取逻辑并查看实际首页。
- 个人事实改 `content/pages/about.md` / `cv.md`；主页简介从个人资料生成，不在首页模板再复制履历。站点品牌与导航取 `content/site.json`，确实硬编码的展示逻辑定位到对应 renderer 后再改。
- 每篇论文的 Markdown 文件名 stem 是 ID。维护其 front matter 的 `title/date/venue/excerpt`，可选 `paperurl/citation`；若有 `permalink`，须匹配 `/publication/<id>/`。没有论文 URL 时不要虚构。
- 精选论文只改 `content/site.json` 的 `publications.featured`。论文列表、详情、个人介绍和 CV 的论文展示由 `scripts/pipeline.py` 生成，不手写相同列表。
- 原有不同论文记录不要仅因标题相近就合并。论文日期不等于笔记更新时间；科研成果与履历按用户材料核对。
- 在线 CV 与 PDF 独立维护。只有用户要求更新 PDF 且材料足够时才生成替换文件；比较教育、经历、论文、联系方式及原版保留范围，并核验新旧下载地址返回同一份预期 PDF。不能把旧 PDF 描述为已同步新版 CV。

## 公共组件与路由

- 导航/页脚/base page/SEO 定位 `scripts/render.py`；首页与目录卡片定位 `scripts/views.py`，样式定位 `assets/site/site.css`。
- 阅读装配定位 `scripts/reading.py` / `assets/site/reading.css`。原文章已有目录则复用；新增目录使用有效 ID，避免重复/冲突；系列位置和 prev/next 从登记顺序生成。
- 调整博客筛选时核对 `q/topic/type/sort`、旧 `category`、相关 `origin` 映射、清除条件、未知值提示、popstate/刷新、附加参数和片段。默认本地列表不把所有章节重复显示为独立集合，关键词搜索可以命中章节。
- `content/redirects.json` 登记固定旧 URL 到有效新 URL，不产生跳转链；查询和片段默认保留。禁用 JavaScript 时保留可见回退链接。PDF 旧地址复制字节，不能用 HTML 替代 PDF。
- 输出目录不能位于仓库内，不能重叠权威源目录。构建与检查失败时保留上一份成功产物，不在旧产物上零散手改。

## 前沿增量维护

1. 读取 `.automation/update-frontier.md` 和当前运行器，不用本 skill 重写其领域核验/轮换规则。
2. 用户只要求某段正文修订时直接维护正文并检查；只有用户要求执行前沿自动更新时才运行 `.automation/run-frontier-update.sh`。
3. 自动运行器要求工作树干净、只允许目标源变化、具备有效 updater 和固定依赖解释器。遇到其他未提交修改时保留并报告，不能自动 stash、提交、reset 或覆盖；用户授权的普通本地编辑仍可继续。
4. 只在核实到实质增量时更新，保留所有插入标记、备份和状态；同步 `last-updated`、changelog 与条目有效日期，目录日期由构建提取。
5. 验证接口确实需要 **仓库根目录与源文件** 两个参数：

   ```bash
   FRONTIER_PYTHON="$HOME/.cache/stein-notes/venv/bin/python" \
     .automation/validate-frontier.sh "$PWD" content/posts/llm-frontier-2026/index.html
   ```

   使用工具 `cwd` 将 `$PWD` 设在实际维护仓库；解释器可替换为已确认具有固定依赖的环境。
6. 运行器默认只准备本地更新。`--publish` 会拉取、提交和推送，只有对应授权存在时才能使用；不要因为运行器提供该开关就默认启用。它还具有当前代码定义的间隔、锁和状态规则，不能绕过。
7. 定时任务创建/修改单独采用可用 schedule skill 和用户授权；普通维护不改定时器或发送消息。
