# VAE 原理、发展脉络与 VAE 家族系统调研

> 综合整理，覆盖 20+ 核心模型，从 2013 VAE 原始论文到 2025 REPA-E / ACT-ALOHA。
> 重点深入：离散量化路线、VAE 在现代系统中的具体技术角色、CVAE 在机器人策略学习中的应用。

---

## 一、核心原理与 ELBO

VAE（Kingma & Welling, ICLR 2014）将 AE 升级为概率生成模型：编码器输出分布 $q_\phi(z|x) = \mathcal{N}(\mu(x), \sigma^2(x))$，解码器输出条件分布 $p_\theta(x|z)$，先验 $p(z) = \mathcal{N}(0, I)$。

**ELBO**：
$$\mathcal{L}_{\text{ELBO}} = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x) \| p(z))$$

**重参数化**：$z = \mu + \sigma \odot \epsilon, \epsilon \sim \mathcal{N}(0, I)$

**VAE 定位**：训练稳定、概率解释清晰、encoder 天然存在、潜空间连续——现代生成系统中最常用的"前端压缩器 / tokenizer / latent interface"。

---

## 二、三大关键问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| **模糊** | Pixel-wise Gaussian 偏向"平均化" | Perceptual loss, adversarial loss, 离散 latent |
| **Posterior Collapse** | Decoder 太强跳过 latent | KL annealing, free bits, 弱化 decoder, InfoVAE |
| **先验过简** | $\mathcal{N}(0,I)$ 太简单 | VampPrior, flow prior, discrete codebook |

---

## 三、六阶段发展脉络

1. **2013-2015 奠基**：VAE + SGVB
2. **2016-2018 表示与 Disentanglement**：β-VAE, InfoVAE, WAE
3. **2016-2019 条件生成**：CVAE, Graph/Sequence/Multimodal VAE
4. **2017-至今 离散量化**：VQ-VAE → RQ-VAE → FSQ → LFQ
5. **2016-2020 深层高性能**：Ladder VAE → BIVA → NVAE
6. **2021-至今 系统级前端**：KL-VAE, MAGVIT-v2, REPA-E, ACT/ALOHA

---

## 四、连续路线（概要）

| 模型 | 核心改动 | 要点 |
|------|---------|------|
| Vanilla VAE | 连续高斯 + ELBO | 理论基线 |
| β-VAE | 加权 KL (β>1) | Disentanglement |
| CVAE | 条件 $c$ | 条件生成基线，详见 ACT 案例 |
| InfoVAE | MMD 替代 KL | 抗 collapse |
| WAE | 聚合后验匹配 | 更宽松实用 |
| VampPrior | 可学习伪输入先验 | 灵活先验 |
| Flow-VAE | Normalizing flow | 精确后验 |

---

## 五、离散量化路线（重点展开）

### 5.1 VQ-VAE（NeurIPS 2017, DeepMind）

**核心**：编码器输出 $z_e(x)$，最近邻映射到 codebook：$z_q = e_k, k = \arg\min_j \|z_e - e_j\|_2$

**三部分 loss**：
$$\mathcal{L} = \mathcal{L}_{\text{recon}} + \|\text{sg}[z_e] - e\|^2 + \beta\|z_e - \text{sg}[e]\|^2$$

**重要原因**：(1) 避免 posterior collapse；(2) 离散 token 可直接用 Transformer 建模；(3) 码字是学出的"典型模式"，不像高斯均值趋向平均。**直接催生了 DALL-E 和 Parti**。

**缺点**：Codebook collapse / dead codes。

### 5.2 RQ-VAE（ICLR 2022）

残差式多级量化：$z_q \approx q_1 + q_2 + \cdots + q_L$。第 1 级捕获粗略语义，后续各级补细节。组合空间从 $K$ 扩展到 $K^L$。**现代视觉 tokenizer（LlamaGen, Open-MAGVIT2）的核心技术**。

### 5.3 FSQ（ICLR 2024, DeepMind）

**无码本**——每个维度 round 到有限标量集合。一举消除 codebook collapse、dead codes、commitment loss。训练更简单稳定，性能可比 VQ-VAE。

### 5.4 MAGVIT-v2 / LFQ（2023, Google/CMU）

Lookup-Free Quantization：每维 sign 二值化为 $\{-1, +1\}$，查找完全免费。**关键发现："Tokenizer is Key"——tokenizer 质量是视觉生成的关键瓶颈**。Open-MAGVIT2（Tencent, 2024）开源复现。

### 5.5 量化路线对比

| 方法 | 码本 | 组合空间 | 核心优势 |
|------|------|---------|---------|
| VQ-VAE | 显式 $K$ | $K$ | 简单直接 |
| RQ-VAE | $L$ 个 | $K^L$ | 表达力指数级 |
| SQ-VAE | 多个小 | $\prod L_i$ | 搜索成本低 |
| FSQ | **无** | $\prod L_i$ | 无 collapse |
| LFQ | **无** | $2^d$ | 查找免费 |

---

## 六、层级高性能：NVAE（NeurIPS 2020, NVIDIA）

VAE 生成质量的里程碑。深卷积 + 30+ 层 latent + spectral normalization + balanced KL。首次证明纯 VAE 在 CelebA-HQ 1024×1024 上 FID 6.56 可匹敌 GAN。**证明模糊问题不是原理性的，而是之前模型不够深。**

---

## 七、VAE 在现代生成系统中的角色（重点展开）

### 7.1 Latent Diffusion 前端（KL-VAE / SD-VAE）

KL-f8 VAE：$512 \times 512 \times 3 \to 64 \times 64 \times 4$（压缩比 8×）。**KL 权重仅 $10^{-6}$**（优先保重建质量，"规整性"交给 diffusion）。训练用 LPIPS 感知损失 + PatchGAN 对抗损失。SD3-VAE 扩展到 16 通道。

### 7.2 AR 视觉 Tokenizer（DALL-E → Parti → LlamaGen）

DALL-E（dVAE, 32×32 tokens）→ Parti（ViT-VQGAN）→ LlamaGen（RQ-VAE + LLaMA AR）。核心发现：tokenizer 质量直接决定下游 AR 模型上限。

### 7.3 视频生成（Sora / MAGVIT-v2）

Sora：video VQ-VAE 将视频压缩为 spacetime patches。MAGVIT-v2：LFQ + 时空下采样。视频 VAE 核心挑战：时空一致性 + 极高压缩比。

### 7.4 多模态视觉 Tokenizer

Chameleon (Meta)：自研 VQ tokenizer，图像文本统一 token。SEED-Voken (Tencent)：基于 Open-MAGVIT2。趋势：visual token 需保留语义信息（不仅是像素重建）。

### 7.5 CVAE 在 ACT/ALOHA 中的关键角色

**问题**：行为克隆中同一观测对应多种合理动作，直接 MSE 导致 mode averaging。

**ACT 的 CVAE 方案**：
- Encoder：Transformer (4层)，输入观测+动作序列，输出 latent $z$ ($d_z=32$) 的 $\mu, \sigma^2$
- Decoder：Transformer (7层, 512 dim)，输入观测+$z$+$k$ 个 query，输出动作 chunk
- Loss：$\mathcal{L} = \|a_{\text{pred}} - a_{\text{gt}}\|_1 + \beta D_{\text{KL}}(q(z|o,a) \| \mathcal{N}(0,I))$，$\beta \in [10, 100]$
- 推理：$z=0$（先验均值），策略确定性

**核心机制**：CVAE 将不同 demonstration 的"动作风格"编码到 latent $z$ 中，decoder 学到"给定风格 $z$，输出对应动作"，而非对所有风格取平均。

**Temporal Ensembling**：指数衰减加权融合相邻 chunk，消除边界抖动。

### 7.6 REPA-E（ICCV 2025）

首次 VAE + DiT 端到端联合训练。核心发现：直接用 diffusion loss 端到端训练不稳定，但通过 representation alignment（REPA）可以稳定训练。打破"先训练 VAE 再冻结"的范式。

### 7.7 系统角色总结

| 系统 | VAE 类型 | 角色 | 关键设计 |
|------|---------|------|---------|
| SD 1/2 | KL-f8 | 图像→连续 latent | KL=10⁻⁶, LPIPS+GAN |
| SD3/FLUX | KL-f8 (16ch) | 图像→连续 latent | 16 通道 |
| DALL-E/Parti | dVAE/ViT-VQGAN | 图像→离散 token | VQ+AR |
| LlamaGen | RQ-VAE | 图像→多级 token | RQ+LLaMA |
| Sora | Video VQ-VAE | 视频→spacetime patches | 时空压缩 |
| MAGVIT-v2 | LFQ | 视频→离散 token | 查找免费 |
| ACT/ALOHA | CVAE | 观测+动作→latent→动作 chunk | 解决多模态 |
| Chameleon | VQ tokenizer | 视觉+文本统一 token | Early fusion |

---

## 八、核心论文索引

| 模型 | 年份/会议 | 核心贡献 | 影响 |
|------|----------|---------|------|
| VAE | ICLR 2014 | 概率生成 + 重参数化 | 奠基 |
| β-VAE | ICLR 2017 | 加权 KL | Disentanglement |
| CVAE | NeurIPS 2015 | 条件 VAE | 条件生成基线 |
| VQ-VAE | NeurIPS 2017 | 向量量化码本 | DALL-E/Parti 基础 |
| RQ-VAE | ICLR 2022 | 残差多级量化 | 现代 tokenizer 核心 |
| KL-VAE/LDM | CVPR 2022 | Latent Diffusion 前端 | Stable Diffusion |
| NVAE | NeurIPS 2020 | 深层级卷积 VAE | VAE 质量上限 |
| MAGVIT-v2/LFQ | 2023 | Lookup-Free 视频 tokenizer | "Tokenizer is Key" |
| FSQ | ICLR 2024 | 无码本量化 | 消除 collapse |
| ACT/ALOHA | RSS 2023 | CVAE 动作 chunking | 机器人策略学习 |
| REPA-E | ICCV 2025 | VAE+DiT 端到端 | 打破两阶段范式 |
