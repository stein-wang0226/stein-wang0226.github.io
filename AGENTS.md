# 项目工作约定

这是 Yuxiang Wang 的学术主页和 Stein’s Notes 的唯一维护仓库。
先读 `README.md`，涉及结构、批量内容或公共设计时再读相应协议。
用户在当前任务中的要求优先于本文件；已有授权沿用，不重复询问。

## 入口与职责

- 项目管理与规模化整理：`.trae/skills/blog-project-manager/SKILL.md`。
- 日常正文、首页、CV、论文与组件修改：`.trae/skills/blog-maintainer/SKILL.md`。
- 管理协议：`docs/project-management.md`。
- 正文、HTML、资源与引用协议：`docs/content-contract.md`。
- 视觉与交互协议：`docs/design-system.md`。
- GitHub README 与账号资料：`docs/github-profile/DEPLOYMENT.md`。

## 只编辑权威源

| 对象 | 来源 |
| --- | --- |
| 主题、导航、页面、资源、精选论文 ID | `content/site.json` |
| 文章和系列登记 | `content/catalog.json` |
| 正文 | 登记中的 `source` |
| 个人事实 | `content/pages/about.md`、`content/pages/cv.md` |
| 论文事实 | `content/publications/*.md` |
| GitHub Profile 展示稿 | `docs/github-profile/README.md` |
| 全站展示与阅读装配 | `templates/`、`scripts/`、`assets/site/` |
| 历史公开地址 | `content/redirects.json` |

构建产物、预览、临时脚本、缓存和 checkout 放仓库外。不要回写生成 HTML、
创建第二份可编辑目录或向旧站写入新正文。
维护协议不是第二份数据登记，具体数量和关系以当前 JSON 为准。

## 内容与设计

- 保留有效 URL、锚点、公式、代码、图表、原件、许可和自动插入标记。
- 复用 Stein’s Notes 的暖白、墨色、青绿色和现有本地字体。
  新公共组件遵循 `docs/design-system.md`；原科学 HTML 不因美化被整篇重写。
- 图表保留宽高比；数学排版内部 SVG 不应用科研图表缩放规则。
- 事实、版本、性能数字、履历和论文状态有来源；推导与实测分别标注。
- Profile 展示原创方法、交付和研究成果。普通 fork、练习仓库和空壳仓库
  不因存在就成为精选工作，也不以工作量数字替代结果。
- 迁移基线不可重建；有意修改只更新已核对文件的差异记录。

## 执行和验收

先检查 Git 状态并保留他人改动。常规修改直接实施，缺少关键事实时继续独立部分。

```bash
make governance
make check
# Profile 修改另外核对 GitHub 渲染和远端状态
make profile-check
make profile-status GH=/path/to/gh
```

按影响范围补实际浏览器验证，不把链接检查称为事实核验。
`review_status=reviewed` 表示本次明确范围经过审阅，不表示所有科研结论均已复现。
只记录实际执行的验收；历史计数和发布记录不是本次证据。

提交和推送遵循用户明确授权，分别核对差异、Actions 和线上版本。
不要自动提交其他任务的文件，不改 Git 配置，不跳过 hooks，不强制推送。
Profile README、账号字段、置顶项目、主站部署是四个不同的同步对象。
