# 配对 RNA-seq 差异表达：公开问题草案

状态：研究设计，尚未发布为参评任务。下文“待冻结”项必须在发布前补齐；
不能把这些未知条件作为私有 scorer 隐藏规则。

从提供的四供体配对 gene count 数据中估计 Dex 相对 untreated 的表达变化，
输出可复算的样本计数概要、每个输入基因的统计结果和一致性摘要。
结论只限于本数据的细胞、处理和时间；不要求符合论文中的基因名单或叙事，
也不能由这些数据推断临床疗效或蛋白功能。

公共输入：

- `counts.tsv`：gene × sample 的非负整数 assigned fragment counts；首列
  `gene_id`，其余列与 `samples.tsv.sample_id` 完整一一对应。
- `samples.tsv`：`sample_id, donor_id, condition`。condition 只有 `Dex` 和
  `untreated`；每供体各一份，两者是配对样本，SRA run 不是额外供体。
- `input-manifest.json`：固定输入 hash、版本、计数 / 注释语义、gene 宇宙、
  配对与单位，以及允许的方法 / 预过滤政策。实际文件和 hash 待构建冻结。
- `output.schema.json` 和 `serialization-contract.md`：完整机器输出和跨行规则。

统计方向固定为 Dex / untreated，设计控制 donor；主字段 `log2_fc` 是未收缩
估计。对比检验和允许方法列表待 reference 校准后冻结，不能由评分器临时更改。
BH 调整的集合按公开预过滤和可检验基因规则确定；FDR 阈值设为 0.05。
不同可接受方法的分项复算协议、容差和缺失规则须公开说明后方可评测。

交付 `sample_qc.tsv`、`gene_stats.tsv`、`summary.json`，并提供一个读取公共输入、
重新产生这些文件的可执行分析脚本。字段、单位、排序、零与缺失严格遵循
公开合同。不要额外提交研究解释作为评分项；方法名 / 版本用于数值复算路由。

容器摘要、离线工具依赖、CPU / 内存 / wall-time 限额、安装与网络政策待冻结。
计划使用无互联网的 Agent 环境和隔离的私有 grader；当前没有可运行环境或
私有 reference，不能把本草案称为可立即执行的 Harbor 任务。
