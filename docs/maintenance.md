# 内容维护

## 最短流程

1. 在 `content/catalog.json` 找到文章 ID 和正文 `source`；直接编辑该正文。
2. 内容范围有变化时更新同一记录的标题、摘要、主题与标签；相关文章填写 ID。已知内容更新时间才填写 `updated`。
3. 执行 `make check`，再用 `make preview` 检查真实发布产物。
4. 需要发布时审阅 `git diff`，按已获授权范围提交、推送；等待 Actions 部署成功。
5. 核对线上 `build-info.json` 的提交，以及首页、博客筛选、代表文章、论文、PDF 和兼容链接。

线上是否包含本次更新，以部署成功的 Actions 运行和 `build-info.json` 的提交标识为准；
本地工作区构建可能带本地修改标志，不能代替线上核对。

## 新文章

```bash
make new ID=my-topic TITLE="文章标题" TOPIC=llm-foundations TYPE=principles
```

主题 ID：`llm-foundations`、`multimodal`、`rl-post-training`、`agent`、`training-inference`、`diffusion`。
内容类型见 `content/site.json`。命令创建 Markdown 和草稿登记记录，同名 ID 或目录会停止，不能覆盖。
补齐摘要、先修知识、核心链路、示例、来源及限制，移除 `TEMPLATE:EMPTY` 标记，并更新登记摘要。
发布前改为 `published`；空模板不会通过发布检查。复杂公式或已有交互仍可维护完整 HTML。

新增系列须登记一个 `kind=series` 的入口；每章登记 `kind=chapter`、父系列 ID 和正整数 `order`。
`source` 与 `url` 分别指向源文件和公开地址，不通过文件名猜测顺序。
删除或改名后更新 `redirects.json`，重新构建会清理旧产物；不要删除仍需保留的历史内容。

## 预览与校验

```bash
make setup
make check
make preview PORT=8766
```

`build.py --output /tmp/my-blogs-site-build` 渲染并校验新产物，成功后才替换原产物。
`check.py --output ...` 检查已有产物；`export.py --output ... --dest ...` 复制同一份清单。
源文件变化后重新构建，再刷新预览。不要从源码目录运行 HTTP 服务，也不要把公开产物复制回仓库。

## 内容日期与事实

未知日期保持 `null`。构建时间、Git 时间和“整理完成日”不等于内容实质更新时间。
前沿条目的 `last-updated`、最新 changelog 和条目日期应一致；目录自动从正文提取。
性能数字注明硬件、版本、配置与测量来源；厂商自报、预印本与推测应区别标注。
检查记录中的待核实项持续保留，补齐后再调整整理状态；格式统一不代表科学结论已全面验证。

## 个人资料及 PDF

个人履历只根据作者提供的信息更新。论文 Markdown 是论文列表唯一来源；SemDLM 与 SemDLM+ 是不同记录。
在线 CV 与 PDF 分别维护。编辑 `content/pages/cv.md` 后单独导出 PDF，比较教育、经历、论文与联系方式，
确认后再替换 `assets/Curriculum_Vitae.pdf`；构建会生成内容一致的旧下载地址副本。
现有 PDF 完整保留，不假定与在线 CV 同版本。

## 前沿自动更新

唯一自动编辑源为 `content/posts/llm-frontier-2026/index.html`。协议见 `.automation/update-frontier.md`。
运行器保留全部插入标记，并在编辑前生成时间戳备份；状态和日志位于被 Git 忽略的 `.automation/` 子目录。
默认 `.automation/run-frontier-update.sh` 仅准备本地更新，要求工作树干净，并限制更新后只有该源文件未暂存变化。
其他改动、暂存项、无效日期或标记缺失都会阻塞，不擅自覆盖。

`.automation/validate-frontier.sh` 使用同一构建 / 校验入口并核对目录日期；
先 `make setup`，或设置 `FRONTIER_PYTHON` 指向安装了锁定依赖的解释器。
运行器的 `--publish` 会提交和推送，必须有对应发布授权；本次没有运行。
推送成功仍不等于部署完成，最后核对 Actions 与线上版本。

## 历史导入工具

`content/series/dlm-survey/generate.py` 仅用于指定原始单页的新目录导入；不用于覆盖现有 14 章。
`docs/content-migration-manifest.json` 是整理前不可重建的迁移基线。
当前整理的有意内容差异单独记录；不要重新生成原始基线掩盖变化。
