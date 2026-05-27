# 墨卷 · Ink Scroll

**简体中文** · [繁體中文](README.zh-TW.md) · [English](README.en.md)

[![Status](https://img.shields.io/badge/status-alpha-c96442?labelColor=141413)](#-路线图)
[![License: MIT](https://img.shields.io/badge/license-MIT-5e5d59?labelColor=141413)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6b8e6e?labelColor=141413)](CONTRIBUTING.md)
[![Discussions](https://img.shields.io/badge/💬-Discussions-7b8fa8?labelColor=141413)](../../discussions)

> 光照之处，墨色生辉

浏览器端交互水墨画装置。纯 HTML/CSS/JS，零依赖构建，单文件即可运行。

---

用摄像头手电筒或手势控制光圈，揭示隐藏在中国风水墨画下的彩色动画世界。墨线静止，光圈内万物生动。

> 🚧 **项目状态:** Alpha — 骨架已搭好，正在向"标准社区项目"打磨。**欢迎一起来玩**：开 [issue](../../issues/new/choose) 提想法、去 [Discussions](../../discussions) 闲聊、看 [路线图](#-路线图) 找你想做的方向。

## ✨ 特性

| | |
|---|---|
| 🔦 **手电筒模式** | 用手机闪光灯对准摄像头，最亮点即光圈位置 |
| ✋ **手势识别** | MediaPipe 手部追踪，手掌张开控制光圈 |
| 🖱 **鼠标跟随** | 触控板/鼠标滑动画卷，无需摄像头 |
| 🏔 **5 场景** | 山水、竹林、雪景、花鸟、星空 — AI 生成水墨画 |
| 🎬 **场景动画** | 飞鸟、飘雪、花瓣、萤火虫、流星……仅光圈内可见 |
| 🎨 **3 风格** | 墨线（Sobel）、素描、暗调 |
| 📐 **灵敏度** | `[ ]` 键调节摄像头映射范围 |
| 🌐 **三语界面** | 简体 · 繁體 · English，自动检测浏览器语言 |

## 🛠 技术栈

**纯浏览器端，零后端依赖。**

| 层 | 技术 |
|---|---|
| 渲染 | Canvas 2D API |
| 手势 | [MediaPipe Hands](https://ai.google.dev/edge/mediapipe) (CDN) |
| 摄像头 | `getUserMedia` API |
| 边缘检测 | Sobel 算子（手写 JS 实现） |
| 字体 | Noto Serif SC / TC + EB Garamond (Google Fonts) |
| 图片 | Grok (`grok-imagine-image`) 生成 |

旧版 Python + OpenCV 原型见 `archive/`。

## 🚀 快速开始

任何静态文件服务器即可。

```bash
cd web && python3 -m http.server 8888
# 打开：http://localhost:8888
```

摄像头需要 HTTPS（localhost 除外）。推荐 Tailscale：

```bash
tailscale serve --bg 8888
# 然后访问：https://your-machine.tailXXXXx.ts.net
```

## ⌨️ 快捷键

| 键 | 功能 |
|---|---|
| M | 切换模式 |
| ← → | 切换场景 |
| 1 / 2 / 3 | 风格：墨线 / 素描 / 暗调 |
| `[` `]` | 灵敏度 - / + |
| + / - 或滚轮 | 光圈大小 |
| R | 重置平滑 |
| X | 镜像翻转 |
| F | 全屏 |
| Shift + D | 显示 / 隐藏 FPS |
| Q / Esc | 退出 |

## 🏗 架构

```
web/
├── index.html        # 主应用 (~1370 行，零构建，含 i18n 字典)
└── scenes/           # 5 张 AI 生成场景图
    ├── shanshui.png
    ├── bamboo.png
    ├── snow.png
    ├── flowers.png
    └── stars.png
```

### 渲染管线

```
1. 摄像头幽灵图层（15% 透明，画区域内）
2. 墨线遮罩（Sobel 边缘，场景切换时生成一次）
3. 光圈裁剪 → 揭示彩色层（原图 + 程序化动画）
4. 赤陶色光圈环
5. 场景过渡淡入淡出
```

## 📐 设计系统

参见 [DESIGN.md](DESIGN.md)。

品牌色：羊皮纸 `#f5f4ed` · 赤陶 `#c96442` · 墨黑 `#141413`

## 🔮 路线图

**原始构想：IR 手电筒 + Wii Remote** — Johnny Lee 那种装置艺术里的经典做法。Wiimote 内置 IR 摄像头硬件 blob tracking，100Hz、亚像素、对环境光免疫。当前的 webcam 模式只是该愿景的过渡实现。

下面是为这个"光圈揭示"作品调研过的所有可行输入方式。✅ = 纯浏览器 · ⚠️ = 需 native bridge

### 🟢 纯浏览器候选

| 类别 | 方式 | 映射 | 关键 API |
|---|---|---|---|
| 指向 | **IR webcam + IR LED 手电** | 现有亮点检测直接复用 | (no change) |
| | **Wiimote (WebHID)** | IR 摄像头 → XY，加速度 → 半径 | `wiimote-webhid` |
| | Joy-Con (WebHID) | 摇杆 + 陀螺仪 | `joy-con-webhid` (Tomayac) |
| | **Wacom 数位板** | 笔位置 + **笔压 = 半径** | HTML5 Pointer Events |
| | 激光笔 + webcam | HSV 检测红/绿点 | DIY |
| | AR 标记 (ArUco/AprilTag) | 打印纸标记当"灯笼" | `js-aruco2` |
| | 游戏手柄 (Xbox/PS) | 摇杆 + 扳机 | Web Gamepad API |
| | SpaceMouse 6DoF | 6 轴推杆 | `spacemouse-webhid` |
| 身体 | **MediaPipe Pose 全身** | 手腕坐标 + 肩宽 = 半径 | `@mediapipe/tasks-vision` |
| | MediaPipe FaceMesh | 鼻尖 + 张嘴 = 半径 | 同上 |
| | WebGazer 视线追踪 | 看哪揭哪 | `WebGazer.js` |
| 手机 | **手机当魔杖** | 陀螺仪 + WebRTC，二维码配对 | DeviceOrientation API + PeerJS |
| | 手机当触摸板 | 远程触屏 | 同上 + `touchmove` |
| 音频 | 音量 → 半径 | 吹 / 吼 / 拍手 | Web Audio `AnalyserNode` |
| | **呼吸检测** | 吸气放大、呼气收缩 | Web Audio band-pass |
| | 哨音音高 | 音高对应 X 轴 | `pitchy` |
| | 语音命令 | "揭示"、"放大" | Web Speech API (Chromium) |
| 专业 | Web MIDI | nanoKONTROL / Launchpad 推子 | Web MIDI API |
| | OSC over WebSocket | TouchDesigner / Max 推数据 | `osc-js` |
| 生理 | rPPG 心率 | 心跳脉动光圈 | `heartbeat-js` |
| | Muse EEG (BLE) | α 波 → 越静画卷开越大 | `web-muse` |
| 其他 | Pixy2 / OpenMV (Web Serial) | 板载 blob 追踪 | Web Serial API |

### 🟡 需 native bridge

| 方式 | 优势 |
|---|---|
| Kinect v2 / Azure Kinect | 全身骨架 + 深度 (Azure EOL) |
| Intel RealSense / OAK-D | 深度遮罩做手掌剪影 |
| Leap Motion / Ultraleap | 手部骨架精度最高 |
| Tobii 眼动仪 | 真正的高精度视线 |
| FLIR Lepton 热像仪 | 全黑环境也能用 |

### ⭐ 最贴合本项目气质的 5 个方向

每个方向下面都列了需要的技术栈，方便想动手的同学心里有数。"难点"是实现时最容易卡的那一步。

#### ① IR webcam + IR LED 手电

兑现 Johnny Lee 原始愿景的最短路径。**代码零修改**——把环境可见光过滤掉之后，现有的亮点检测立刻变成 IR 追踪。

- **技术栈:** 现有 `getUserMedia` + `spF()` 直接复用
- **硬件:** 一个旧 webcam（拆 IR-cut filter）+ 一片冲洗过的胶片当 IR-pass + 一个 IR LED 手电（亚马逊 ~$10）
- **难点:** 拆机不可逆；要找合适厚度的 IR-pass 滤片
- **状态:** 寻找愿意拆 webcam 的人

#### ② Wacom 笔压 = 半径

水墨画 + 笔压，主题与机制天然闭环。**纯前端，无新依赖**——HTML5 Pointer Events 直接给你笔压值。

- **技术栈:** `pointermove` 事件 + `e.pressure` (0–1)
- **硬件:** 任何 Wacom / XP-Pen / Huion / iPad+Apple Pencil
- **难点:** iPad Safari 的 PointerEvent.pressure 历史上不稳定，需要测试
- **状态:** 准备动手的人来 PR

#### ③ 呼吸 + 全身姿态

吸气放大、呼气收缩；手腕坐标驱动光圈位置。**全沉浸双模态、手不离身、纯浏览器。**

- **技术栈:**
  - 呼吸: Web Audio `AudioContext` + `BiquadFilterNode`（0.1–0.5 Hz 带通）+ `AnalyserNode` RMS 包络
  - 姿态: `@mediapipe/tasks-vision` 的 `PoseLandmarker`（CDN），复用现有 `wkCvs` 摄像头帧
- **硬件:** 笔记本麦克风 + 摄像头（已有）
- **难点:** 画廊噪音环境下呼吸信噪比；MediaPipe Pose 比 Hands 重一些 (~30fps on M1)
- **状态:** 我自己想做的下一个

#### ④ 手机当魔杖（WebRTC + QR 配对）

观众扫码把自己的手机变成魔杖，挥动手机控制光圈。**画廊场景最实用**——观众自带硬件。

- **技术栈:**
  - 大屏: 现有页面 + WebRTC `RTCDataChannel`
  - 手机端: 同源 mobile-friendly 子页面，读 `deviceorientation` (`alpha/beta/gamma`)
  - 配对: PeerJS 公共 broker (省去自建信令) + `qrcode-generator` 生成二维码
- **硬件:** 观众的手机 + 大屏端的电脑
- **难点:** iOS 14+ 要 `DeviceOrientationEvent.requestPermission()`，必须由用户手势触发；首次连接的 ICE 协商时机
- **状态:** 寻找熟悉 WebRTC 的同学一起做

#### ⑤ OSC from TouchDesigner

让策展人/运营在不动代码的情况下，用 TouchDesigner 的 patch 实时调光圈位置、半径、场景切换。**装置艺术圈标准做法。**

- **技术栈:**
  - 浏览器端: WebSocket client + `osc-js` 解码 OSC bundle
  - TD 端: WebSocket DAT 节点，发送 `/spot/x`、`/spot/y`、`/spot/r`、`/scene/next` 等地址
  - 可选: 同一接口也能接 Max/MSP / SuperCollider / Pure Data
- **硬件:** 装 TouchDesigner 的电脑（免费个人版即可）
- **难点:** OSC 是无连接的，丢包要自己处理；建议加平滑
- **状态:** 我会画一个最小 TD patch 当 demo

---

## 🤝 加入

骨架已经写好（一个 ~1370 行的 `web/index.html`、5 张场景、3 种交互模式、3 种语言界面跑起来了），但**真正有意思的部分需要更多人一起玩**——上面那张路线图表里任何一行，只要有人想做，我都可以陪着 review。

### 不写代码也能贡献

| 我能 | 怎么做 |
|---|---|
| 提一个新交互方式 | 开 [New Interaction Modality issue](../../issues/new?template=new_modality.md) |
| 报 bug | 开 [Bug report](../../issues/new?template=bug_report.md) |
| 提小改进 | 开 [Feature request](../../issues/new?template=feature_request.md) |
| 闲聊、问问题、晒成品 | [Discussions](../../discussions) |
| 贡献水墨场景图 | 见 [CONTRIBUTING.md → 场景图](CONTRIBUTING.md#-场景图) |
| 翻译到其他语言 | 开 issue 提议 |

### 写代码贡献

Fork → PR。详细约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。**核心规则只有一条**：保持"单文件、零构建、零框架"。新增 CDN 单文件库 OK，新增 webpack 不 OK。

行为准则：[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
安全问题：[SECURITY.md](SECURITY.md)

不吝赐教。

## 📄 License

MIT — 随便改、随便商用。

有问题联系：[Hugh](https://github.com/Chunyu-Hugh)

详见 [LICENSE](LICENSE)。
