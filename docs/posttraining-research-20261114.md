# 后训练专题：来源、推导与验收

调研截止：2026-11-14。公开入口 `/llm-posttraining/`，六章。
本次研究与正文审阅覆盖该新专题；不将旧文全部科研结论标记为已复现。
本站没有执行 GPU 后训练，三类任务是教学设计，实验矩阵是待执行方案。

## 内容职责

| 章节 | 核心贡献 | 主要来源编号 |
| --- | --- | --- |
| 01 监督与偏好 | mask、两种RFT、恢复、DPO/SimPO/ORPO/KTO、工业训练图 | 12–23、27、49 |
| 02 RL目标 | PPO/GAE/RLOO/GRPO、分母、GSPO/CISPO/SAPO/SAO | 1–11、44、50 |
| 03 OPD | fixed-prefix梯度、full/sample/top-k、多教师、自蒸馏、覆盖与遗忘 | 24–36、60、66 |
| 04 环境与信用 | Harbor隔离、PRM/value、PURE/Cliff、anchor/子任务/GAR | 27、37–44、53–54 |
| 05 系统 | 十类框架、三策略、completion bias、partial KV、固定slime代码 | 25、27、45–65 |
| 06 案例 | code/科学/GUI输入到终评、轨迹契约、单轴消融与成本 | 16、27、30、34、41、53–54 |

编号、原始URL、版本/commit、位置与使用章节见公开
`assets/research/posttraining-20261114/sources.json`，共66项。
该索引从正文参考列表生成。动态文档记录访问日期，不宣称与仓库SHA同步。
不归档整个外部仓库或新大文件；沿用既有V4.1、Ultra、RLDS、ARLArena原件。

## 关键核对与证据边界

1. RFT区分Rejection sampling Fine-Tuning与Reinforcement Fine-Tuning。
   OpenAI使用成功访问的Cookbook案例；API文档重定向页面不作为完整操作核验。
2. ReTerm 2610.18484v1 §3.1只监督教师恢复token；§3.2另有GRPO分支。
   失败上下文与失败动作监督不同，不说所有失败token应统一屏蔽。
3. GRPO全同reward组仅task PG为零，其他KL/OPD/entropy项可非零。
   `1-p^G-(1-p)^G`仅独立二值采样解析，非实测训练数据。
4. GSPO的序列ratio是平均log-ratio的exp，非完整trajectory IS乘积。
   CISPO裁剪IS系数并detach；Soft SAPO的f(r)保留advantage与符号温度。
5. 两种SAPO区分：2511.20347v1软门控；2608.19842v1单rollout共享policy/value。
   SAO 2607.07508v1的strict IS mask不等于PPO的min-clipping。
6. 完整词表reverse-KL局部logits梯度为
   `p_v[(log p_v-log q_v)-D]`；固定sample上的裸log-ratio反传不等价。
   fixed-prefix identity不包含整个状态分布对参数的导数。
7. DeepSeek V4 §5.1.2与V4.1 §5.2.4使用full-vocabulary；
   Ultra §3.3.5的sampled-token偏好是特定Agent实验，off-support解释为作者假说。
8. MiMo 2610.11959v1 §5.6的MOPD2含standard/teacher-prefix/SFT-prefix OPD：
   prefix可来自示范，学生新生成一回合；不称整episode纯on-policy。
   MOPD 2606.30406v1与MOPD2另列，不把两个名字混用。
9. OPSD 2601.18734v2为同模型不同context的特权解法蒸馏；
   SDPO使用环境文本或成功sibling；SDPG另外组合outcome PG、gate/schedule与UKL。
10. Guided-OPD 2606.15912v2学生回合reverse、教师回合forward KL；
    TISD 2609.30878v1干预后重采后缀。科学Avg@128 equal-step/time与代码Avg@4分开。
11. OPDArena 2610.25651v1实际OPD是student-weighted Top-16；
    full-vocab用于部分分布测量。OOD分布变化与遗忘是关联，非因果证明。
12. PRM步骤正确性、MC continuation成功、value、advantage不同。
    PURE最差步骤目标与Cliff首错后信用不能直接迁移到可恢复Agent。
13. Harbor当前overview/verifier文档已访问；separate环境不继承全部工作区，
    artifacts是TOML顶层键；reward.txt/json并存时JSON优先。历史shared任务单独核对。
14. slime SHA `79aa41a884ab0bf65222c94418f6357d3c31192b`：
    `loss.py`715–719行原始短摘录；829–836应用OPD，839之后可normalize。
    `on_policy_distillation.py`与同SHA文档对照；摘录依Apache-2.0标注。
15. verl `staleness_threshold`为backlog比例而非checkpoint lag个数；
    三策略概率、同版本kernel/template/routing误差与完成顺序偏移分别处理。
16. Agent Lightning v1.0 2608.17528v1已重写，保存真实API调用与exact token前缀；
    不将2025 v0.x LightningRL图当作当前实现。
17. 框架固定README支持与特殊branch/recipe边界保留，ROLL部分async仍在实现。
    AReaL新后端、SkyRL两package、NeMo跨tokenizer均不泛化为全组合支持。

## 图与教学资源

| 文件 | 口径 |
| --- | --- |
| group-signal.csv / .svg | G=8独立Bernoulli解析概率，9个p值；图显示1%/50%/99% |
| mimo-compute.csv / .svg | MiMo-V2.6 Pro §4.1 Figure3：43.8/43.5/12.7%；非美元占比 |
| figure-data.json | 轴/来源/公式与数据文件对应 |
| case-contracts.json | 三案例、空轨迹契约，design_only，无虚构reward或cost |
| experiment-matrix.csv | E0–E6单轴对照、固定条件和成本分母，均待执行 |

图以inline SVG呈现并保留viewBox，下载原始SVG与CSV。
flow/目标mask/公式/原始短代码共同讲机制，不引入外部图片或运行依赖。

## 已执行的数学核验

临时脚本 `/tmp/my-blogs-posttraining-artifacts.py`：
四组概率分布×三个logit，有限差分对照reverse-KL解析梯度，误差<1e-8；
三个Soft SAPO温度对照ratio=1的导数为1；
两个GRPO有效组解析值、未cap GAR正优势质量守恒及MiMo比例求和。
共19项通过。这些检查是数学/数据核验，不能称模型训练或论文复现。

构建、浏览器与上线验收另记 `docs/validation.md`。
