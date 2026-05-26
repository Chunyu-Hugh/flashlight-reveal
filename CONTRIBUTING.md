# 贡献指南 · Contributing

欢迎！墨卷是一个**艺术装置 + 开放实验场**——单文件 HTML、零依赖、欢迎一切让"光圈揭示水墨"这个核心变得更有趣的想法。

Welcome. `flashlight-reveal` is an **art installation + open experiment** — a single-file HTML app with zero dependencies. All ideas that make the "spotlight reveals ink" core more compelling are welcome.

---

## 🌱 怎么参与 · Ways to contribute

不需要写代码也能贡献。No coding required to contribute.

| 我能做什么 · I can | 怎么做 · How |
|---|---|
| 提一个新的交互方式 | 开 [New Interaction Modality issue](../../issues/new?template=new_modality.md) |
| 报告 bug | 开 [Bug report](../../issues/new?template=bug_report.md) |
| 提功能想法 | 开 [Feature request](../../issues/new?template=feature_request.md) |
| 闲聊、问问题、晒成品 | 去 [Discussions](../../discussions) |
| 改代码 | Fork → 改 → PR（见下） |
| 改 README/文档 | 直接 PR |
| 贡献场景图 (`web/scenes/`) | 见"场景图"章节 |
| 翻译到其它语言 | 开 issue 提议，我们一起看怎么组织 |

---

## 🛠 本地开发 · Local development

零依赖，零构建。Zero deps, zero build.

```bash
git clone git@github.com:Chunyu-Hugh/flashlight-reveal.git
cd flashlight-reveal/web
python3 -m http.server 8888
# 打开 · open http://localhost:8888
```

摄像头功能需要 HTTPS（localhost 例外）。开发用 Tailscale `tailscale serve --bg 8888` 最快。

Camera APIs require HTTPS (localhost exempt). For dev, Tailscale `tailscale serve --bg 8888` is the fastest.

---

## 📝 代码风格 · Code style

整个项目就一个 `web/index.html`（~660 行）。**保持这个约束**——单文件、零依赖是产品的一部分，不是技术债。

The whole project lives in one `web/index.html` (~660 lines). **Keep it that way** — single-file, zero-deps is part of the product, not tech debt.

具体约定 · Specifics:

- **不引入构建工具**（webpack/vite/parcel 全部 no）· No build tools
- **不引入框架**（React/Vue/Svelte 全部 no）· No frameworks
- **可以引入 CDN 单文件库**（如 MediaPipe），但要明确写为何需要 · CDN single-file libs OK if justified
- **风格延续现有代码**：超紧凑、单字母变量在内部 OK、注释少而精 · Match existing style: terse, short names internally, comments rare and meaningful
- **新交互方式**：在 `M` 对象（mode dispatch table）里加一个新 entry，遵循 `{icon, name, init, spot, cln, ex, needCam, req}` 接口
- **新场景图**：512×512+ PNG，水墨风格，放到 `web/scenes/`，在 `sceneFiles` 数组注册

---

## 🎨 场景图 · Scene images

新场景图欢迎！要求：

- 中国风水墨/书画风格（与现有 `shanshui/bamboo/snow/flowers/stars` 一致）
- 512×512 像素以上，PNG 格式，文件大小 < 1MB
- 单色或低饱和度——边缘检测 (Sobel) 对高对比单色效果最好
- 你拥有版权 或 来源是 CC0/CC-BY，在 PR 里注明来源

Scene image PRs welcome with: Chinese ink-painting style matching existing scenes; ≥512×512 PNG, <1MB; monochrome or low-saturation (Sobel edge detection works best on high-contrast monochrome); you own copyright or source is CC0/CC-BY (cite it in the PR).

---

## 🔀 PR 流程 · PR workflow

1. Fork & 创建分支：`git checkout -b modality/wacom-pressure`
2. 改动尽量小、可解释。一个 PR 一件事。
3. 在浏览器里实测——单元测试在这个项目里不存在
4. PR 描述里**贴一张 GIF/截图**展示效果
5. 我（@Chunyu-Hugh）会尽快 review

Fork & branch → small focused change → test in browser → **attach a GIF/screenshot** in PR → maintainer review.

---

## 💬 行为准则 · Code of Conduct

参见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。简而言之：**对作品认真，对人友善**。

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). TL;DR: **be rigorous about the work, kind to people**.

---

## 🙏 致谢 · Acknowledgments

每个被合并的贡献者会被加到 README 致谢区。第一次贡献者特别欢迎——告诉我哪里阻塞你了，我帮你过坎。

Every merged contributor is credited in the README. First-time contributors especially welcome — tell me where you got stuck and I'll help you through.

不吝赐教 · Don't hold back your insights.
