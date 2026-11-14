# Profile 轻度美化与开源方案

调研日期：2026-11-14。当前按用户反馈保持轻度美化：
原生正文为主，浅色短题头、墨色姓名和一条青绿色细线。
后续更新默认沿用这一强度，不自动增加大型横幅或研究项目配图。

## 开源方案选择

| 方案 | 已核对的用途与限制 | 本次处理 |
| --- | --- | --- |
| [ryme.md](https://github.com/ryanpolasky/ryme.md) | MIT；Profile 横幅模板与 SVG / GIF 导出；静态资源可自行托管 | 采用 Sleek Hero 的姓名适配与强调线思路，改写为轻量静态题头 |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | MIT；README SVG 横幅、形状与文字；在线地址依赖图片服务 | 已调研；当前轻量题头由本地脚本生成 |
| [Readme Typing SVG](https://github.com/DenverCoder1/readme-typing-svg) | MIT；打字动效，可自行托管 | 本次保持静态标题 |
| [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats) | README 明确声明不再维护；公共实例仅提供尽力服务 | 未采用旧公共端点 |
| [GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended) | MIT；持续维护的统计卡片方案，可输出主题图片 | 研究成果继续用正文表达，未接入统计卡片 |

采用的模板固定到 `aede040201f5ed5168eb74c5e1fe319895b724ed`，
源文件为 `src/lib/templates/sleek-header.ts`。保留
[MIT 许可](LICENSE-ryme.md)；实际改写在
[render_visuals.py](tools/render_visuals.py)。未安装浏览器主题扩展，也未修改 GitHub 的网页外壳。

## 图片与管理位置

- `assets/header.jpg`：1280 × 180 的浅色姓名题头，只有文字与细线。
- 复用 `assets/hero-source.jpg` 左侧无主体的空白区域，以极低透明度混入浅色底面。
  蛋白雕塑、电脑和图节点不进入当前题头；无需重新调用图片生成服务。
- 生成原件的提示词和完整来源地址保存在 `assets/hero.provenance.json`；
  题头是装饰排版，不能作为实验结果或真实产品截图。
- 原大横幅和四张项目配图保留来源与历史文件，当前 README 不再展示。
- `assets/manifest.json` 的 `assets` 只登记当前题头的尺寸、字节数、SHA-256 和模板出处；
  `archived_assets` 标明旧版图片。
- Profile 发布仓库根目录放 `README.md` 与同样的 `assets/`；主站本目录是维护源稿。
  README 使用相对地址，发布时一起提交图片，避免第三方实时服务失效。

正文不把论文状态或实验指标烘焙进题头。题头有有意义的替代文本；
HTML 只指定宽度，保持原始比例。内容更新通常只需要改正文，不重新生成整套图片。

## 维护命令

图片工具仅需要 Pillow。可在独立环境中安装：

```bash
python3 -m venv /tmp/profile-imaging
/tmp/profile-imaging/bin/pip install 'Pillow>=11,<13'
/tmp/profile-imaging/bin/python docs/github-profile/tools/render_visuals.py --header
/tmp/profile-imaging/bin/python docs/github-profile/tools/render_visuals.py --manifest
```

`--header` 用保留的底图重新排版；`--manifest` 更新尺寸和哈希。
`--fetch <hero|task-synthesis|agentic-rl|gui-agents|science-models>` 明确发起图片生成，
遇到同名已有图片会停止。若要更新配图，先备份旧图，明确选定需要修改的一张。
不要在普通构建 / GitHub Actions 中调用图片生成接口。
该接口有时返回“生成中”提示 JPEG，工具会识别并阻止它进入新资源。
本次通过 `GenerateImage` 后端生成真实图片后，使用
`--adopt <name> --image <生成原件路径>` 归档；完整提示词和尺寸不变，
来源 JSON 同时记录实际调用方式，不能把提示图视为生成完成。

```bash
python scripts/profile.py check
python scripts/profile.py preview --gh /path/to/gh --output /tmp/profile-preview.html
python scripts/profile.py status --gh /path/to/gh
```

预览使用 GitHub Markdown API 的实际标签过滤，图片内嵌到本地 HTML；
样式只模拟 GitHub。发布后还需实测个人主页中图片加载、图片比例与链接。

2026-11-14 初版验收（历史）：展示图片共 282,838 字节；本地 390 / 650 / 1024px 亮色与
1024px 暗色预览通过。Profile 提交 `514379c` 已上线，真实 GitHub 页面在
390 / 1440px 下五张图片均正常加载并保持比例，研究区域无横向滚动，
图片链接、论文状态与折叠操作正常。README 与远端逐字节一致；
展示图片按 Git blob 哈希逐项核对一致。没有运行新的训练或科研实验。

当前轻度样式本地验收：题头 15,071 字节，展示清单只有这一张图片。
`make governance` / `make profile-check` 通过；390 / 650 / 1024px 亮色与
1024px 暗色预览的比例、宽度和折叠操作通过。页面继续保留四项研究工作与论文信息。
当前 Profile 提交 `aa85585` 已上线；390 / 1440px 的实际页面确认只有题头，
图片加载、比例、链接及折叠操作通过。远端 README 与题头资源均已核对一致。
