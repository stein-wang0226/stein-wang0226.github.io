# 数学符号逐页补充审阅

本轮对应“数学公式、符号要有清晰的概念解释”的追加要求，基于提交
`7559d0f` 审阅 74 份本地唯一源。旧版逐页学习验收记录保持原样，
本轮改前/审阅后 SHA、逐源理由及新增解释见同名 JSON。

## 本轮编辑

- 定义放在相关公式或小节旁，覆盖数学对象、索引、张量形状/单位、
  参数作用及期望、条件分布、转置、范数、指示函数、停止梯度等算子。
- RL 区分裁剪 ε 与除零 ε、轨迹 τ 与 SAPO 门控 τ、即时奖励与未来回报；
  面试手册保留短卡，详细推导仍由主讲维护。
- 架构与优化器明确行/列向量约定、两种转置等价的状态矩阵、
  SVD/polar、Jacobian、动量/二阶原点矩和各成本公式的单位。
- 扩散明确噪声日程、时间方向、连续/离散条件分布、ELBO 符号和
  算子；统计评测明确 offset、contrast、BH 排序、配对标准误和接受域。
- 项目报告补充指标、采样/监督/预算符号；Holon 全部 50 个原生 MathML
  表达式另行核对，修正一处“GQA 同比减少交互计算”的矛盾说明。
- Frontier、SkillsBench 和 Harbor 报告的美元金额改为明确货币单位，
  消除货币文本被当作公式的歧义。
  冻结历史 RL 原稿字节不变。

原有机制图、科研原图、引用、论文数值及实验限制保留。本轮以符号解释
和已发现的局部口径冲突为范围，不将浏览器通过称为论文实验复现。

## 验收

源码审阅与本地验收已完成：52 份源稿编辑，123 段就近符号解释。
逐源审阅/验收 SHA 与三屏覆盖见 `blog-symbol-review-20261115.json`；
浏览器实际结果见 `blog-symbol-validation-20261115.json`。

| 检查 | 本轮实际结果 |
| --- | --- |
| 构建与内容 | `make check OUTPUT=/tmp/my-blogs-symbol-review-build`；107 HTML / 303 公开文件通过 |
| 内容保留 | 项目 venv 执行 `docs/verify-content-migration.py --require-clean --output /tmp/my-blogs-symbol-review-build`；9 项精确 SHA、32 项登记变化、299 原锚点、199 公开路由通过 |
| 组织与引用 | `scripts/organization.py check --output …`；冻结原件与主讲去向通过；`scripts/citations.py check`：1105 source/version 项通过 |
| 集成 | 项目 venv 执行 `scripts/test_pipeline.py`；17/17 通过，331.708 秒 |
| 三屏逐页 | Chrome + Playwright，390/768/1440px；26 实际阅读页 × 三屏 = 78 页检验，74 源 × 三屏 = 222 源检验 |
| 数学与说明 | 每屏 123 段说明可见；无 TeX 错误、裸露 TeX、缺失 display 输出或整页溢出；阻断外部 CDN |
| 原生 MathML | Holon 的 50 个表达式完整保留，其中 8 个为 display；手机长式在独立容器横向滚动，键盘右箭头已验证可访问 |
| 阅读交互 | 48 旧章 × 三屏 = 144 深链通过；74 页无 JS 阅读通过；63 次图表打开/退出通过；学习、面试、项目三种路线通过 |
| 实际截图 | 12 张精确定位截图留在 `/tmp/my-blogs-browser-tests/`；人工查看六张手机及两张桌面截图，RL/AdamW 另定位到公式及说明 |

本地验收 input digest：
`edaab874234d424626aae1a530e7e9bab41081a688cf549ccdd8e349ab32842c`。
验收时 HEAD 为 `7559d0f`、工作区有本轮改动；提交后将通过 Actions 与线上
`build-info.json` 核对同一输入摘要，再记录实际发布状态。
