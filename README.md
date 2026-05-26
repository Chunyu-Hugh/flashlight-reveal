# 墨卷 · Ink Scroll

[![Status](https://img.shields.io/badge/status-alpha-c96442?labelColor=141413)](#-路线图--roadmap)
[![License: MIT](https://img.shields.io/badge/license-MIT-5e5d59?labelColor=141413)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6b8e6e?labelColor=141413)](CONTRIBUTING.md)
[![Discussions](https://img.shields.io/badge/💬-Discussions-7b8fa8?labelColor=141413)](../../discussions)

> 光照之处，墨色生辉 · Where light falls, ink comes alive

浏览器端交互水墨画装置。纯 HTML/CSS/JS，零依赖构建，单文件即可运行。

A browser-based interactive ink painting installation. Pure HTML/CSS/JS — single file, zero build steps, no backend.

---

用摄像头手电筒或手势控制光圈，揭示隐藏在中国风水墨画下的彩色动画世界。墨线静止，光圈内万物生动。

Control a spotlight with your webcam flashlight or hand gestures to reveal a living, animated world hidden beneath traditional Chinese ink paintings.

> 🚧 **项目状态 · Status:** Alpha — 骨架已搭好，正在向"标准社区项目"打磨。**欢迎一起来玩**：开 [issue](../../issues/new/choose) 提想法、去 [Discussions](../../discussions) 闲聊、看 [Roadmap](#-路线图--roadmap) 找你想做的方向。
>
> Skeleton's in place, polishing toward a "standard community project." **Come play** — open an [issue](../../issues/new/choose), chat in [Discussions](../../discussions), pick a direction from the [Roadmap](#-路线图--roadmap).

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
| + / - 或滚轮 | 光圈大小 | Spot radius (or wheel) |
| R | 重置平滑 | Reset smoothing |
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

## 🔮 路线图 · Roadmap

**原始构想：IR 手电筒 + Wii Remote** — Johnny Lee 那种装置艺术里的经典做法。Wiimote 内置 IR 摄像头硬件 blob tracking，100Hz、亚像素、对环境光免疫。当前的 webcam 模式只是该愿景的过渡实现。

**Original vision:** Johnny-Lee-style — IR flashlight tracked by a Wii Remote's onboard IR camera. Hardware blob tracking at 100Hz, sub-pixel, ambient-light-immune. The current webcam mode is an interim approximation.

下面是为这个"光圈揭示"作品调研过的所有可行输入方式。✅ = 纯浏览器 · ⚠️ = 需 native bridge

Below is the full survey of interaction modalities considered for this spotlight-reveal piece. ✅ = pure browser · ⚠️ = native bridge required

### 🟢 纯浏览器候选 · Pure-browser candidates

| 类别 · Category | 方式 · Modality | 映射 · Mapping | 关键 API · API/Lib |
|---|---|---|---|
| 指向 · Pointing | **IR webcam + IR LED 手电** | 现有亮点检测直接复用 · drops into existing brightness-peak code | (no change) |
| | **Wiimote (WebHID)** | IR 摄像头 → XY，加速度 → 半径 | `wiimote-webhid` |
| | Joy-Con (WebHID) | 摇杆+陀螺仪 · stick + IMU | `joy-con-webhid` (Tomayac) |
| | **Wacom 数位板** | 笔位置 + **笔压 = 半径** · pen XY + pressure | HTML5 Pointer Events |
| | 激光笔 + webcam | HSV 检测红/绿点 · color-blob | DIY |
| | AR 标记 (ArUco/AprilTag) | 打印纸标记当"灯笼" · printed marker as lantern | `js-aruco2` |
| | 游戏手柄 (Xbox/PS) | 摇杆+扳机 · stick + trigger | Web Gamepad API |
| | SpaceMouse 6DoF | 6 轴推杆 · 6-axis puck | `spacemouse-webhid` |
| 身体 · Body | **MediaPipe Pose 全身** | 手腕坐标 + 肩宽 = 半径 · wrist + shoulder span | `@mediapipe/tasks-vision` |
| | MediaPipe FaceMesh | 鼻尖 + 张嘴 = 半径 · nose + mouth-open | 同上 |
| | WebGazer 视线追踪 | 看哪揭哪 · look to reveal | `WebGazer.js` |
| 手机 · Phone | **手机当魔杖** | 陀螺仪+WebRTC，二维码配对 · gyro + WebRTC, QR pair | DeviceOrientation API + PeerJS |
| | 手机当触摸板 | 远程触屏 · remote touch | 同上 + `touchmove` |
| 音频 · Audio | 音量 → 半径 | 吹/吼/拍手 · blow/shout/clap | Web Audio `AnalyserNode` |
| | **呼吸检测** | 吸气放大、呼气收缩 · inhale/exhale | Web Audio band-pass |
| | 哨音音高 | 音高对应 X 轴 · pitch → X | `pitchy` |
| | 语音命令 | "揭示"、"放大"·  voice commands | Web Speech API (Chromium) |
| 专业 · Pro | Web MIDI | nanoKONTROL / Launchpad 推子 · faders | Web MIDI API |
| | OSC over WebSocket | TouchDesigner/Max 推数据 · TD/Max push | `osc-js` |
| 生理 · Bio | rPPG 心率 | 心跳脉动光圈 · pulse with heartbeat | `heartbeat-js` |
| | Muse EEG (BLE) | α 波 → 越静画卷开越大 · alpha → reveal | `web-muse` |
| 其他 · Misc | Pixy2 / OpenMV (Web Serial) | 板载 blob 追踪 · onboard blob track | Web Serial API |

### 🟡 需 native bridge · Native-bridge required

| 方式 · Modality | 优势 · Why |
|---|---|
| Kinect v2 / Azure Kinect | 全身骨架 + 深度 · skeletal + depth (Azure EOL) |
| Intel RealSense / OAK-D | 深度遮罩做手掌剪影 · depth mask hand silhouette |
| Leap Motion / Ultraleap | 手部骨架精度最高 · highest-fidelity hand tracking |
| Tobii 眼动仪 | 真正的高精度视线 · production-grade gaze |
| FLIR Lepton 热像仪 | 全黑环境也能用 · works in pitch dark |

### ⭐ 最贴合本项目气质的 5 个方向 · Best matches for this piece

每个方向下面都列了需要的技术栈，方便想动手的同学心里有数。"难点"是实现时最容易卡的那一步。

For each direction below, the tech stack lists what you'd actually need to learn, and "tricky" calls out where the friction usually lives.

#### ① IR webcam + IR LED 手电 · IR-modified webcam + IR LED wand

兑现 Johnny Lee 原始愿景的最短路径。**代码零修改**——把环境可见光过滤掉之后，现有的亮点检测立刻变成 IR 追踪。
The shortest path to Johnny-Lee's original vision. **Zero code change** — filter out visible light and the existing brightness-peak detector becomes an IR tracker.

- **技术栈 · Stack:** 现有 `getUserMedia` + `spF()` 直接复用 · existing pipeline, no new code
- **硬件 · Hardware:** 一个旧 webcam（拆 IR-cut filter）+ 一片冲洗过的胶片当 IR-pass + 一个 IR LED 手电（亚马逊 ~$10）
- **难点 · Tricky:** 拆机不可逆；要找合适厚度的 IR-pass 滤片
- **状态 · Status:** 寻找愿意拆 webcam 的人 · Looking for someone willing to mod a webcam

#### ② Wacom 笔压 = 半径 · Wacom pen pressure → spotlight radius

水墨画 + 笔压，主题与机制天然闭环。**纯前端，无新依赖**——HTML5 Pointer Events 直接给你笔压值。
Ink-painting meets ink-pen — theme and mechanism close the loop. **Pure browser, no new deps** — HTML5 Pointer Events delivers pressure natively.

- **技术栈 · Stack:** `pointermove` 事件 + `e.pressure` (0–1)
- **硬件 · Hardware:** 任何 Wacom / XP-Pen / Huion / iPad+Apple Pencil
- **难点 · Tricky:** iPad Safari 的 PointerEvent.pressure 历史上不稳定，需要测试
- **状态 · Status:** 准备动手的人来 PR · PRs welcome

#### ③ 呼吸 + 全身姿态 · Breath + full-body pose

吸气放大、呼气收缩；手腕坐标驱动光圈位置。**全沉浸双模态、手不离身、纯浏览器。**
Inhale grows, exhale shrinks; wrist drives position. **Immersive dual-modal, hands-free, pure browser.**

- **技术栈 · Stack:**
  - 呼吸 · Breath: Web Audio `AudioContext` + `BiquadFilterNode`（0.1–0.5 Hz 带通）+ `AnalyserNode` RMS 包络
  - 姿态 · Pose: `@mediapipe/tasks-vision` 的 `PoseLandmarker`（CDN），复用现有 `wkCvs` 摄像头帧
- **硬件 · Hardware:** 笔记本麦克风 + 摄像头（已有）
- **难点 · Tricky:** 画廊噪音环境下呼吸信噪比；MediaPipe Pose 比 Hands 重一些 (~30fps on M1)
- **状态 · Status:** 我自己想做的下一个 · On my own short list

#### ④ 手机当魔杖 · Phone as a wand (WebRTC + QR pair)

观众扫码把自己的手机变成魔杖，挥动手机控制光圈。**画廊场景最实用**——观众自带硬件。
Visitor scans a QR code; their phone becomes a wand. **Best for galleries** — everyone brings their own hardware.

- **技术栈 · Stack:**
  - 大屏 · Big screen: 现有页面 + WebRTC `RTCDataChannel`
  - 手机端 · Phone: 同源 mobile-friendly 子页面，读 `deviceorientation` (`alpha/beta/gamma`)
  - 配对 · Pairing: PeerJS 公共 broker (省去自建信令) + `qrcode-generator` 生成二维码
- **硬件 · Hardware:** 观众的手机 + 大屏端的电脑
- **难点 · Tricky:** iOS 14+ 要 `DeviceOrientationEvent.requestPermission()`，必须由用户手势触发；首次连接的 ICE 协商时机
- **状态 · Status:** 寻找熟悉 WebRTC 的同学一起做 · Looking for a WebRTC-savvy collaborator

#### ⑤ OSC from TouchDesigner · OSC 控场

让策展人/运营在不动代码的情况下，用 TouchDesigner 的 patch 实时调光圈位置、半径、场景切换。**装置艺术圈标准做法。**
Lets a curator drive position/radius/scene live from a TouchDesigner patch — without touching code. **Industry-standard installation pattern.**

- **技术栈 · Stack:**
  - 浏览器端 · Browser: WebSocket client + `osc-js` 解码 OSC bundle
  - TD 端 · TD side: WebSocket DAT 节点，发送 `/spot/x`、`/spot/y`、`/spot/r`、`/scene/next` 等地址
  - 可选 · Optional: 同一接口也能接 Max/MSP / SuperCollider / Pure Data
- **硬件 · Hardware:** 装 TouchDesigner 的电脑（免费个人版即可）
- **难点 · Tricky:** OSC 是无连接的，丢包要自己处理；建议加平滑
- **状态 · Status:** 我会画一个最小 TD patch 当 demo · Will ship a minimal demo patch

---

## 🤝 加入 · Get involved

骨架已经写好（一个 660 行的 `web/index.html`、5 张场景、3 种交互模式跑起来了），但**真正有意思的部分需要更多人一起玩**——上面那张 Roadmap 表里任何一行，只要有人想做，我都可以陪着 review。

The skeleton's in place — 660-line `web/index.html`, 5 scenes, 3 working modes — but **the interesting stuff needs more people in the loop**. Any row of the Roadmap above: if someone wants to take it on, I'll review and pair through it.

### 不写代码也能贡献 · You don't need to code

| 我能 · I can | 怎么做 · How |
|---|---|
| 提一个新交互方式 | 开 [New Interaction Modality issue](../../issues/new?template=new_modality.md) |
| 报 bug | 开 [Bug report](../../issues/new?template=bug_report.md) |
| 提小改进 | 开 [Feature request](../../issues/new?template=feature_request.md) |
| 闲聊、问问题、晒成品 | [Discussions](../../discussions) |
| 贡献水墨场景图 | 见 [CONTRIBUTING.md → 场景图](CONTRIBUTING.md#-场景图--scene-images) |
| 翻译到其他语言 | 开 issue 提议 |

### 写代码贡献 · If you want to code

Fork → PR。详细约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。**核心规则只有一条**：保持"单文件、零构建、零框架"。新增 CDN 单文件库 OK，新增 webpack 不 OK。

Fork → PR. See [CONTRIBUTING.md](CONTRIBUTING.md) for details. **One core rule:** preserve "single file, zero build, zero framework." New CDN single-file libs are fine; new bundlers are not.

行为准则 · Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
安全问题 · Security: [SECURITY.md](SECURITY.md)

不吝赐教 · Don't hold back your insights.

## 📄 License

MIT — 随便改、随便商用 · Do whatever you want, commercial use OK.

有问题联系 · Questions: [Hugh](https://github.com/Chunyu-Hugh)

详见 [LICENSE](LICENSE) · See [LICENSE](LICENSE)
