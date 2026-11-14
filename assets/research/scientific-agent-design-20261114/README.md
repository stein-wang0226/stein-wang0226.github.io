# 科学 Agent 任务与工业训练研究方案

状态：`research_design`；调研日期：2026-11-14。

这些文件是博客中可下载的合同与研究方案。它们不是已构建的 Harbor package，
不包含 counts、FASTQ、reference、oracle、生成轨迹、经验容差或实验结果。
JSON 中的 `null` 表示未测量或尚未冻结，不能自动替换为 0。

| 文件 | 内容 |
| --- | --- |
| `study-audit.json` | 来源图、数据层、候选输入范围、样本映射证据与发布阻塞项 |
| `instruction-draft.md` | 公开题面草案；未冻结项必须补齐后才能交给参评 Agent |
| `output.schema.json` | 两个 TSV 解析后的行对象与 summary 的 JSON Schema |
| `serialization-contract.md` | 完整字段、单位、缺失、枚举及跨行科学一致性规则 |
| `trajectory.schema.json` | 未来记录的动作、观察、版本、token、artifact 字段 |
| `cluster-plan.json` | 128 / 1024 H100 规划与角色账本；不是 verl 启动配置 |
| `experiment-plan.json` | sci-posttrain A–E、种子、预算、对照和未测量结果 |
| `failure-taxonomy.json` | 客观失败分类与所需证据 |
| `cost-record.schema.json` | 每次任务尝试的资源记录 schema；没有填造成本 |

公共问题和私有评估在未来分别版本化。schema 检查只能验证结构，不能证明
科学结果正确、任务可解、scorer 完备或 benchmark 发布就绪。公开前必须固定
数据与容器 hash、完整元数据、预过滤、允许方法、经验容差和 runtime 预算，
完成多个合理 reference、scorer 负例和隔离盲测。

原始依据：

- GEO GSE52778：<https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778>。
- airway 1.32.0 / BioC3.23：
  <https://bioconductor.org/packages/3.23/data/experiment/html/airway.html>；
  vignette：
  <https://bioconductor.org/packages/3.23/data/experiment/vignettes/airway/inst/doc/airway.html>。
- DESeq2：<https://pmc.ncbi.nlm.nih.gov/articles/PMC4302049/>；
  候选版本 1.52.0：<https://bioconductor.org/packages/3.23/bioc/html/DESeq2.html>。
- edgeR 基础：<https://doi.org/10.1093/bioinformatics/btp616>；
  QL workflow version2：<https://f1000research.com/articles/5-1438/v2>；
  候选版本 4.10.7：<https://bioconductor.org/packages/3.23/bioc/html/edgeR.html>。
- MCore / verl / Qwen 固定 revision 在 `cluster-plan.json` 登记。

本目录的文字、schema 与配置由本站作者整理，遵循本站许可；
上游论文、代码、模型和科学数据各有独立许可，本目录不重新分发它们。
H100 80GB、节点规模、池比例、长度和组大小由本文规划，未声明为厂商配置。
