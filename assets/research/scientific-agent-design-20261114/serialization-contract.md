# RNA-seq 输出合同

版本 `science-rnaseq-proposal-v1`，状态：研究设计。`output.schema.json` 定义单行
解析对象和 summary；以下定义 TSV、跨行和科学一致性，均是未来公共合同。

TSV 是 UTF-8、tab 分隔、首行字段名、LF 换行；字段顺序如下。不得重复 ID、
遗漏输入行或添加未知 sample / gene。sample 按输入列顺序，gene 按输入行顺序。
`NA` 表示缺失；实测零写 `0`。布尔值写 `true/false`。拒绝 NaN、Infinity、
空数字和用缺失代替有值字段。JSON 使用 `null` 表示缺失。

## sample_qc.tsv

| 字段 | 类型 / 单位 | 规则 |
| --- | --- | --- |
| sample_id | string | 与 counts 列和 samples 主键完全相同 |
| donor_id | string | 完全来自公开样本映射 |
| condition | enum | `Dex / untreated`，完全来自公开样本映射 |
| library_assigned_counts | integer / assigned counts | 输入此列所有 gene counts 的和；不等于原始测序 read 总数 |
| detected_genes | integer / genes | 输入此列 count > 0 的 gene 数 |
| normalization_factor | number / relative effective library size | 正数；几何均值归一至 1。DESeq2 size factor或edgeR effective library size需按此共同单位转换；它们不要求逐值相同 |

每个输入 sample 恰一行。库大小和检测数从完整输入 gene 宇宙计算，不随预过滤
改变。输入零库会阻塞建模，不能人为指定一个正的 factor；此候选合同发布前须
确认固定输入没有零库。QC 异常类别不作为未公开阈值隐藏评分。

## gene_stats.tsv

| 字段 | 类型 / 单位 | 规则 |
| --- | --- | --- |
| gene_id | string | 输入 gene 主键；不得以 symbol 替换或合并不同 ID |
| log2_fc | number / log2 ratio 或 NA | Dex / untreated，未收缩估计 |
| lfc_se | nonnegative number / log2 ratio 或 NA | 同一 LFC 的标准误；允许方法不提供时 NA |
| pvalue | number [0,1] 或 NA | 公开方法的原假设检验 p 值 |
| padj | number [0,1] 或 NA | 公开可检验集合上的 BH 调整值 |
| status | enum | `tested / filtered / all_zero / not_estimable` |
| direction | enum | `increase / decrease / zero / not_estimable` |
| significant | boolean | finite padj <= 0.05 才为 true |

每个输入 gene 恰一行。`all_zero` 优先：输入各样本均0，四个数值字段为NA。
公开预过滤排除的非全零gene为`filtered`，数值字段为NA；具体过滤规则尚待冻结。
剩余gene若无法完成公开检验为`not_estimable`，本合同主字段全部NA；否则
`tested`且log2_fc / pvalue / padj必须有限。其lfc_se可NA。

对tested行：LFC > 0为increase，< 0为decrease，= 0为zero；
其它status的direction为not_estimable，significant为false。方向不是显著性。
`filtered`和`not_estimable`原因由未来公开方法协议唯一规定，不能任意选择状态
躲过评分。DESeq2 independent filtering、Cook's outlier / 缺失和edgeR预过滤
必须在reference构建后形成明确协议；不能对方法间p值硬设统一容差。

BH集合为公开协议确定的tested行；字段padj与该集合复算一致。使用shrunken LFC、
logFC不同底数、TPM / FPKM或其它gene宇宙必须另建合同版本，不混进本字段。

## summary.json

全部字段见schema，不接受未知字段。`fixture_sha256`是冻结
`input-manifest.json`原始字节的SHA-256；manifest中另登记每个输入的hash。
`artifact_sha256`分别对应两个TSV的原始字节。

`counts`含samples、genes_input、genes_tested、genes_filtered、genes_all_zero、
genes_not_estimable、genes_significant。四种status数量和必须等于genes_input；
显著数等于TSV中significant=true数量，不能超过genes_tested。

`method / method_version`是公开允许方法的复算协议标识；`design`固定
`~ donor + condition`，`contrast`固定`Dex / untreated`。方法元数据用于复算，
不要求或评分解释文采。

## 发布前尚未冻结

真实fixture / transformation hash、允许方法精确版本、预过滤 / outlier政策、
经验数值容差、scorer单位权重、wrapper / container摘要和runtime限额。
本合同提供完整字段形状，但尚不能作为已校准的科学评分器。
