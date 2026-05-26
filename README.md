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

1. **IR webcam + IR LED 手电** — 兑现原始 Wiimote 愿景的"最低改动版"，代码零修改 · least-effort delivery of the IR-flashlight vision, no code change
2. **Wacom 笔压 = 半径** — 水墨主题 + 笔压自然闭环 · ink-painting meets ink pen
3. **呼吸 = 半径 + MediaPipe Pose 手腕 = 位置** — 全沉浸双模态 · immersive dual-modal, hands-free
4. **手机当魔杖（WebRTC 配对）** — 多观众画廊最实用 · best for multi-visitor gallery
5. **OSC from TouchDesigner** — 装置艺术圈标准做法，策展人可控场 · industry-standard install pattern

## 📄 License

MIT — 随便改、随便商用 · Do whatever you want, commercial use OK.

有问题联系 · Questions: [Hugh](https://github.com/Chunyu-Hugh)

详见 [LICENSE](LICENSE) · See [LICENSE](LICENSE)
