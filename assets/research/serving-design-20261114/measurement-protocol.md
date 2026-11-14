# LLM服务与长程Agent测量协议（设计）

2026-11-14。未执行模型服务、科学任务、rollout或benchmark。
结果字段保持空值；本文的容量CSV不能替代测量。

## 固定配置

- checkpoint/hash、tokenizer、chat template、adapter、position配置、模型层/状态布局。
- 框架tag/commit、驱动、CUDA、kernel、connector、硬件SKU及真实可用显存。
- TP/DP/EP/PP逻辑与rank放置、网络、KV分片/复制，PD两侧布局和转换。
- 权重/激活/KV的对象、格式、scale、累积dtype及未量化部分。
- 采样参数、随机种子、target/draft版本、验证和拒绝重采样协议。
- 输入/输出token分布、总上下文上限、截断、工具观察预算、请求与研究切分。
- prefix权限域、冷/热cache、保留/驱逐、chunk、预留与准入。

## 到达与计时

分别运行closed-loop固定并发和open-loop固定到达率，记录开始、warm-up和测量窗。
open-loop声明到达分布、排队上限、限流、超时和未完成请求。
不删除OOM、取消和超时；说明纳入分母和统计方式。

每请求记录提交、开始计算、首token、各输出token、结束/取消时刻。
TTFT包含队列；ITL是相邻输出间隔。TPOT仅适用输出token数>1。
平均值与P50/P95/P99同时给出，声明token-level还是request-level。
output throughput使用完整测量窗，prompt/output token分别计数。
goodput声明TTFT、ITL/TPOT和错误的SLO；它与科学正确性分别报告。

## Agent与训练出口

每轨迹记录run/branch/task/study、全部模型调用和重算、工具和CPU执行、
verifier、policy/sample/update版本、logprob协议、lag和准入决定。
输入fixture只读，输出与分支隔离；test答案不能进索引、memory或prompt。
独立verifier的版本、合同、参考/容差和隐藏反馈单独登记。
按研究组汇总成功率与区间，分检索、策略、统计、权限、环境、格式和预算失败。

## 对照顺序

1. 固定低负载检查模板、概率与输出合同一致性。
2. 扫长度/并发，测容量、峰值、抢占、重算与尾延迟。
3. 一次改变prefix、chunk、并行、格式或drafter的一项，保持同质量/SLO目标。
4. 加入工具等待和异质任务；记录CPU、存储、网络队列及有效轨迹/小时。
5. 同推理预算终评，再给同墙钟预算和全部资源成本。

## 成本与结果

计入所有GPU/CPU worker、teacher/reference/critic/reward、存储、网络、
失败、重试、候选、selector及共享资源的分摊方式。
分别报告GPU-hours/成功、CPU-hours/成功。价格未知为null；
成功数为0时成本/成功未定义或无穷，不能填0。

```json
{
  "status": "not_executed",
  "request_count": null,
  "success_count": null,
  "peak_memory_bytes_per_rank": null,
  "ttft_p95_ms": null,
  "itl_p95_ms": null,
  "goodput_requests_per_second": null,
  "output_tokens_per_second": null,
  "gpu_hours": null,
  "cpu_hours": null,
  "cost_per_independent_success": null
}
```
