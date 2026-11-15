# 完整计算算例与阅读衔接复查

本轮基于 `a8f5bcedc72da8b3ed735afe07a7076000321348`，对74份权威源进行目录、
学习顺序与关键算例/公式/边界段落抽查，重点细读五个计算主讲和归位后的阅读提示，
实际修改9份正文。逐源记录、改前/改后SHA、抽查位置与数值复算保存在
[JSON记录](blog-worked-example-review-20261115.json)。
本记录不表示重新核验全部前沿发布、论文性能或历史项目统计。

## 五条补齐的计算链路

| 主讲 | 本轮补充 | 复算结果与边界 |
| --- | --- | --- |
| [Attention](https://stein-wang0226.github.io/llm-architecture/#architecture-attention--online-softmax-example) | Q/K/V → 整行softmax → 两块最大值、指数和、加权和 → 输出 | 输出均为3；不同分块及共同logit平移一致，浮点逐bit一致另论 |
| [MoE](https://stein-wang0226.github.io/llm-architecture/#architecture-moe--moe-full-example) | 四token → router矩阵 → top-2与重新归一 → 派发/回收 → 容量与通信 | 负载[3,4,1]；丢弃路径改变D输出；示例双向表示payload为24 B |
| [Packing](https://stein-wang0226.github.io/llm-training-lifecycle/#llm-training-pretraining--packing-full-example) | 文档边界 → 4×4可见矩阵 → 目标mask → shift标签 → loss分母 | 有效目标2个，loss约1.039721；attention隔离与目标屏蔽分别负责 |
| [量化](https://stein-wang0226.github.io/llm-serving/#serving-parallel--quantized-dot-example) | 权重 → 整数编码/饱和 → 恢复 → 点积 → 输出误差与scale存储 | 4.67→4.00；含FP32 scale的微型组为6 B，不能由位宽推整体加速 |
| [Flow Matching](https://stein-wang0226.github.io/dlm-survey/#dlm-flow-sde--flow-full-example) | 高斯端点 → 条件监督 → 后验平均 → 边际速度/梯度 → Euler与解析轨迹 | 单配对监督4、边际速度2；Euler 0.2与解析0.180196有有限步误差 |

以上数字是明确假设下的教学计算。MoE专家简化为线性函数，量化未实现GPTQ/AWQ校准，
Flow未训练网络；新增图展示状态交接，不是性能图。数值核查包括稳定online softmax、
实际router乘法与专家计算、整数裁剪、按文档成员关系推导mask、条件高斯矩及RK4对照。

## 阅读结构修正

- 残差章与比较章采用当前主题和章序，不再提示“研究地图第07章”或“前五章”。
- 家族表的Muon链接直接进入训练主讲；收束分别指向前面的残差机制和后续DeepSeek缓存专例。
- 训练章的Muon摘要改为本章链接，量化章直达架构precision节。
- README与维护说明修正原研究地图的角色：来源参考与兼容源，正文按catalog归位。
- 原Transformer完整forward、历史原稿、旧URL/锚点与两份不可变保留基线继续保留。

## 实际验收

`make check`通过：107个HTML页面、303个公开文件。引用检查通过：1119个来源/版本记录。
迁移保留检查通过；17项隔离集成测试通过。

真实Chrome检查25个阅读页面在390/768/1440px下的呈现，覆盖222次源片段检查、
147次旧章片段跳转、74份无脚本入口、63次科研图放大/关闭及三条阅读目标。
首轮发现量化点积公式在390px过宽；将等式按计算步骤拆行后，重新检查四个受影响主题
共12次，公式、全页宽度与锚点均通过。五个新算例15次三屏定位与
家族→Muon三次真实点击通过；知识目录21个入口在三屏下存在且无全页溢出。
这是格式、阅读和兼容验收，不是科研结果复现。

本地构建带本地修改标记，验收源SHA与产物输入指纹见
[最终验收数据](blog-worked-example-validation-20261115.json)。
发布状态以GitHub Actions和线上 `build-info.json` 的实际提交及正文核对为准。
