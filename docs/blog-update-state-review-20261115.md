# 更新目标与状态恢复算例复查

本轮基于 `ecfc19824cd3b76ef725b56a8b99fb9670bf453c` 刷新74份权威源的
目录与算例清单，重点检查并修改5份主讲。本记录的审阅与数值证据限定于这5份，
没有重新逐条核验全站前沿发布、论文性能或历史项目统计。

| 主讲 | 完整计算链 | 独立复算 |
| --- | --- | --- |
| [DPO](https://stein-wang0226.github.io/llm-posttraining/#posttraining-supervision--dpo-full-example) | 回答token条件概率 → 似然求和 → reference差值 → sigmoid/loss → logit梯度 → SGD | loss 0.589309 → 0.587872；共享首位置的两概率仍相加为1；有限差分核对三参数梯度 |
| [GAE](https://stein-wang0226.github.io/llm-posttraining/#posttraining-algorithms--gae-full-example) | reward/value → TD → 反向优势 → lambda-return目标 → actor/critic loss | 终局优势[0.4,0.4]、critic loss 0.08；暂停误标终止使首步优势0.3 → −0.1 |
| [异步交接](https://stein-wang0226.github.io/llm-posttraining/#posttraining-frameworks--async-full-example) | 分段版本/行为概率 → old/current重算 → ratio → 裁剪顺序与聚合 | 乘积1.44、几何平均1.20；错换分母变1.309091，裁剪顺序改变第二项 |
| [状态分支](https://stein-wang0226.github.io/llm-architecture/#architecture-hybrid--state-branch-example) | 前缀 → 起点快照 → 两独立分支 → 重放/截窗/换参数 | A/B输出8.5/0.5，错误共享使B变2.25；换参数重放7.125，复用旧态7.25 |
| [DDPM](https://stein-wang0226.github.io/dlm-survey/#dlm-ddpm--ddpm-full-example) | 加噪 → 噪声loss/梯度 → 解析与预测均值 → 随机反向样本 → 最后一步 | simple loss 0.04，等方差KL 1/90；采样末态1.045586，不等于真实输入1 |

数值使用明确简化条件：DPO是三参数二分类模型，GAE按两个决策平均且无额外正则，
异步表是概率代数而非框架完整recipe，SSM是标量递推，DDPM是不可用作正式配方的
两步日程。它们均不代表LLM训练、GPU kernel或在线服务benchmark。

新增核心计算默认展开，DPO的一步参数更新与异步裁剪顺序折叠为延伸阅读；
继续保留Transformer完整forward、原稿、旧URL、旧锚点、引用编号与两份不可变保留基线。
目录摘要与实质更新日期同步到唯一catalog，DDPM的审阅状态对应本轮推导、数值与页面证据。

逐源改前/改后SHA、具体理由、基线SHA与数值结果见
[审阅数据](blog-update-state-review-20261115.json)。
当前版本的实际构建、浏览器与保留检查结果见
[验收数据](blog-update-state-validation-20261115.json)；线上状态以Actions和
`build-info.json`实际提交为准。

实际验收：`make check`通过（107个HTML页面、303个公开文件），1119项来源/版本记录
检查通过，17项隔离集成测试通过，当前产物的原稿、旧锚点与迁移保留检查通过。
三个主题在390/768/1440px下共9次完整展开阅读检查通过；五个新算例共15次定位检查、
6次实际跨节点击和5条无脚本旧章入口通过，知识目录的21个入口在三屏存在且无全页溢出。
截图复查发现DDPM表的手机步骤列过窄，局部调整表宽后重新完成该算例的三屏检查，
没有将调整前的表格结果当作最终版的证明。数值、格式、兼容性与科研事实复现分别计量。
