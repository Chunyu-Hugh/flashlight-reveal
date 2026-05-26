# 墨卷 · Ink Scroll

> 光照之处，墨色生辉 · Where light falls, ink comes alive

浏览器端交互水墨画装置。纯 HTML/CSS/JS，零依赖构建，单文件即可运行。

A browser-based interactive ink painting installation. Pure HTML/CSS/JS — single file, zero build steps, no backend.

---

用摄像头手电筒或手势控制光圈，揭示隐藏在中国风水墨画下的彩色动画世界。墨线静止，光圈内万物生动。

Control a spotlight with your webcam flashlight or hand gestures to reveal a living, animated world hidden beneath traditional Chinese ink paintings.

## ✨ 特性 · Features

| | |
|---|---|
| 🔦 **手电筒模式** | 用手机闪光灯对准摄像头，最亮点即光圈位置 |
| ✋ **手势识别** | MediaPipe 手部追踪，手掌张开控制光圈 |
| 🖱 **鼠标跟随** | 触控板/鼠标滑动画卷，无需摄像头 |
| 🏔 **5 场景** | 山水、竹林、雪景、花鸟、星空 — AI 生成水墨画 |
| 🎬 **场景动画** | 飞鸟、飘雪、花瓣、萤火虫、流星……仅光圈内可见 |
| 🎨 **3 风格** | 墨线（Sobel）、素描、暗调 |
| 📐 **灵敏度** | `[ ]` 键调节摄像头映射范围 |

| | |
|---|---|
| 🔦 **Flashlight** | Point phone flashlight at webcam; brightest spot = spotlight |
| ✋ **Hand Gesture** | MediaPipe hand tracking; open palm controls spotlight |
| 🖱 **Mouse** | Trackpad/cursor follows naturally, no camera needed |
| 🏔 **5 Scenes** | Mountains, bamboo, snow, blossoms, starry sky — AI-generated |
| 🎬 **Animations** | Birds, snowflakes, petals, fireflies, shooting stars — inside spotlight only |
| 🎨 **3 Styles** | Ink edges (Sobel), sketch, dark |
| 📐 **Sensitivity** | `[ ]` keys to adjust camera-to-canvas mapping |

## 🛠 技术栈 · Tech Stack

**纯浏览器端，零后端依赖。Pure frontend, no backend.**

| 层 | 技术 |
|---|---|
| 渲染 · Rendering | Canvas 2D API |
| 手势 · Gesture | [MediaPipe Hands](https://ai.google.dev/edge/mediapipe) (CDN) |
| 摄像头 · Camera | `getUserMedia` API |
| 边缘检测 · Edge Detection | Sobel 算子（手写 JS 实现） |
| 图片 · Images | Grok (`grok-imagine-image`) 生成 |

旧版 Python + OpenCV 原型见 `archive/`。

The original Python + OpenCV prototype is in `archive/`.

## 🚀 快速开始 · Quick Start

任何静态文件服务器即可。Any static file server works.

```bash
cd web && python3 -m http.server 8888
# 打开 · Open: http://localhost:8888
```

摄像头需要 HTTPS（localhost 除外）。推荐 Tailscale：Camera requires HTTPS. Use Tailscale:

```bash
tailscale serve --bg 8888
# 然后访问 · Then: https://your-machine.tailXXXXx.ts.net
```

## ⌨️ 快捷键 · Shortcuts

| 键 | 功能 | Action |
|---|---|---|
| M | 切换模式 | Switch mode |
| ← → | 切换场景 | Switch scene |
| 1 / 2 / 3 | 风格：墨线 / 素描 / 暗调 | Style |
| `[` `]` | 灵敏度 - / + | Sensitivity |
| + / - | 光圈大小 | Spot radius |
| X | 镜像翻转 | Mirror |
| F | 全屏 | Fullscreen |
| Q / Esc | 退出 | Quit |

## 🏗 架构 · Architecture

```
web/
├── index.html        # 主应用 (~650 行，零构建)
└── scenes/           # 5 张 AI 生成场景图
    ├── shanshui.png
    ├── bamboo.png
    ├── snow.png
    ├── flowers.png
    └── stars.png
```

### 渲染管线 · Render Pipeline

```
1. 摄像头幽灵图层（15% 透明，画区域内）  Camera ghost overlay
2. 墨线遮罩（Sobel 边缘，场景切换时生成一次）  Ink edge mask
3. 光圈裁剪 → 揭示彩色层（原图 + 程序化动画）  Spotlight clip → color reveal
4. 赤陶色光圈环  Terracotta ring
5. 场景过渡淡入淡出  Crossfade transition
```

## 📐 设计系统 · Design System

参见 [DESIGN.md](DESIGN.md) · See [DESIGN.md](DESIGN.md)

品牌色 · Brand colors：羊皮纸 `#f5f4ed` · 赤陶 `#c96442` · 墨黑 `#141413`

## 📄 License

MIT — 随便改、随便商用 · Do whatever you want, commercial use OK.

有问题联系 · Questions: [Hugh](https://github.com/hugh-chunyu)

详见 [LICENSE](LICENSE) · See [LICENSE](LICENSE)
