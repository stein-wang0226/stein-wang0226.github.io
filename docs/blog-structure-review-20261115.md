# 知识结构与覆盖核查 · 2026-11-15

本轮基于 `7392b5c51784230aef0d8809bebabef02219cb15`。带查询参数读取线上
`build-info.json` 确认该版本且 `dirty=false`；不以缓存中的旧响应判断发布状态。
本文件记录早期结构补充时的范围与验收；后续分类整合、正文补充及最终验收见
`blog-curriculum-review-20261115.md` 和 `blog-curriculum-validation-20261115.json`。

## 结论与调整

原有七段连续学习路径适合顺序阅读，但训练阶段、技术专题和研究增量混在查找路径中。
“优化器存在”不代表它容易找到，“前沿架构表存在”也不代表训练、推理、数据已由该表覆盖。
现在增加四类常显目录，复用 `content/site.json` 的 `learning_paths` 记录、既有文章与锚点；
保留七段顺序学习路径、原 URL、公式、代码、科研图与来源。

| 分类 | 核查结论 | 主讲位置 / 本轮变化 |
| --- | --- | --- |
| 经典模型架构 | 已有张量、Attention/RoPE、FFN/MoE、残差、混合状态六节 | `content/series/llm-architecture/`；目录直接进入连续长章 |
| 前沿开源架构 | 已有九家族版本与配置、机制和证据；本轮没有重新核验全部型号 | `s06_architecture_landscape.html`；补经典到前沿的学习链路与四类目录回链 |
| 训练阶段 | 已有 pretrain、midtrain/CPT、SFT/RFT、RL、OPD 与交接 | `content/series/llm-training-lifecycle/` 与 `llm-posttraining/`；按问题直达 |
| 优化器 | 已有 SGD→AdamW 推导、矩估计与偏差修正、数值例、Muon等算法与成本对照 | `s05_training_methods_systems.html#adamw-derivation`；提升为训练目录显式入口 |
| Scaling Law / ladder | 原先主要为6NT算力和Chinchilla结论，缺完整最优分配与实验组织 | `s01_pretraining.html#scaling-law`；补可分离损失、约束求导、凸性、IsoFLOP、调度偏差、留出规模与实验阶梯图 |
| 训练架构与框架 | 已有并行、状态分片、batch、集群规划及后训练框架表；职责界限不够醒目 | `s05_training_methods_systems.html#training-stack`；新增数据目标/更新/执行/编排四层图与入口 |
| 推理 | 已有 prefill/decode、分页KV、前缀复用、vLLM调度、量化、投机、容量与成本 | `content/series/llm-serving/`；增加五个常显目录入口 |
| 数据 | 内容分布在训练阶段和Agent任务章节 | 四类目录按pretrain、midtrain、监督轨迹、可执行任务、独立评测连接主讲 |

## 新增内容依据与边界

- Kaplan 2020：<https://arxiv.org/abs/2001.08361v1>。
- Chinchilla 2022：<https://arxiv.org/html/2203.15556v1>，§2–3、Table 1；本轮读取原文。
- Megatron Core：<https://docs.nvidia.com/megatron-core/developer-guide/latest/index.html>；
  本轮读取，Core与Megatron-LM参考训练应用的职责分开表述。
- 最优分配公式为经验损失模型假设下的推导，不是独立实验。
- Scaling ladder 表为工程组织建议；没有本地训练点、拟合曲线或外推误差实测。
- 仍未给出 μP/μTransfer 的完整参数化推导，亦未系统拟合 MoE、数据受限/重复、
  RL 与 test-time compute 的统一规律；不称为所有 Scaling 方向的完整综述。
- 框架职责说明不代表完成所有版本、后端、精度、优化器组合的运行测试。
- 保留现有前沿型号表的版本边界；本轮仅核查结构与可达性，不宣称重新完成所有最新规格的事实审计。

## 当次验收

- `make check OUTPUT=/tmp/my-blogs-structure-20261115`：107 HTML 页面、303 公开文件通过。
- `docs/verify-content-migration.py --require-clean --output /tmp/my-blogs-structure-20261115`：
  通过；三份正文按本轮独立记录更新精确 SHA 与原因，未修改不可变基线。
- `scripts/learning_review.py check`：通过；新增结构审阅作为补充，不覆盖此前符号与逐页记录。
- 本轮浏览器脚本 `/tmp/my-blogs-browser-tests/structure-check.js`：
  四个相关视图 × 三种宽度，共12次检查；20个目录链接全部实际点击并确认目标可见；
  禁用外部请求检查本地公式渲染；无JavaScript目录与Scaling跳转通过。
- 截图核看：桌面四类目录与390px Scaling正文，图文、公式和原有视觉风格正常。
- 数学复核：对正系数下的解析最优点，检验预算恒等式、导数为零以及相邻规模损失更高；
  仅为代数验证，不产生实验数据或训练收益结论。
- 发布入口复核：线上训练长章包含 `training-methods-systems--adamw-derivation`，
  研究地图包含 `research-architecture-landscape`；新目录与新增Scaling正文尚未发布。
- 临时浏览器证据：`/tmp/my-blogs-browser-tests/structure-report.json`。
- 此阶段之后的集成检查与修复记录统一见上述课程复查文档。

预览：<http://127.0.0.1:8773/blog/#knowledge-map>。
