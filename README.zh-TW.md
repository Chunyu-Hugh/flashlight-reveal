# 墨卷 · Ink Scroll

[简体中文](README.md) · **繁體中文** · [English](README.en.md)

[![Status](https://img.shields.io/badge/status-alpha-c96442?labelColor=141413)](#-路線圖)
[![License: MIT](https://img.shields.io/badge/license-MIT-5e5d59?labelColor=141413)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6b8e6e?labelColor=141413)](CONTRIBUTING.zh-TW.md)
[![Discussions](https://img.shields.io/badge/💬-Discussions-7b8fa8?labelColor=141413)](../../discussions)

> 光照之處，墨色生輝

瀏覽器端互動水墨畫裝置。純 HTML/CSS/JS，零依賴建構，單檔案即可執行。

---

用攝像頭手電筒或手勢控制光圈，揭示隱藏在中國風水墨畫下的彩色動畫世界。墨線靜止，光圈內萬物生動。

> 🚧 **專案狀態:** Alpha — 骨架已搭好，正在向「標準社群專案」打磨。**歡迎一起來玩**：開 [issue](../../issues/new/choose) 提想法、去 [Discussions](../../discussions) 閒聊、看 [路線圖](#-路線圖) 找你想做的方向。

## ✨ 特性

| | |
|---|---|
| 🔦 **手電筒模式** | 用手機閃光燈對準攝像頭，最亮點即光圈位置 |
| ✋ **手勢辨識** | MediaPipe 手部追蹤，手掌張開控制光圈 |
| 🖱 **滑鼠跟隨** | 觸控板/滑鼠滑動畫卷，無需攝像頭 |
| 🏔 **5 場景** | 山水、竹林、雪景、花鳥、星空 — AI 生成水墨畫 |
| 🎬 **場景動畫** | 飛鳥、飄雪、花瓣、螢火蟲、流星……僅光圈內可見 |
| 🎨 **3 風格** | 墨線（Sobel）、素描、暗調 |
| 📐 **靈敏度** | `[ ]` 鍵調節攝像頭映射範圍 |
| 🌐 **三語介面** | 簡體 · 繁體 · English，自動偵測瀏覽器語言 |

## 🛠 技術堆疊

**純瀏覽器端，零後端依賴。**

| 層 | 技術 |
|---|---|
| 渲染 | Canvas 2D API |
| 手勢 | [MediaPipe Hands](https://ai.google.dev/edge/mediapipe) (CDN) |
| 攝像頭 | `getUserMedia` API |
| 邊緣偵測 | Sobel 運算元（手寫 JS 實作） |
| 字型 | Noto Serif SC / TC + EB Garamond (Google Fonts) |
| 圖片 | Grok (`grok-imagine-image`) 生成 |

舊版 Python + OpenCV 原型見 `archive/`。

## 🚀 快速開始

任何靜態檔案伺服器即可。

```bash
cd web && python3 -m http.server 8888
# 打開：http://localhost:8888
```

攝像頭需要 HTTPS（localhost 除外）。推薦 Tailscale：

```bash
tailscale serve --bg 8888
# 然後存取：https://your-machine.tailXXXXx.ts.net
```

## ⌨️ 快捷鍵

| 鍵 | 功能 |
|---|---|
| M | 切換模式 |
| ← → | 切換場景 |
| 1 / 2 / 3 | 風格：墨線 / 素描 / 暗調 |
| `[` `]` | 靈敏度 - / + |
| + / - 或滾輪 | 光圈大小 |
| R | 重設平滑 |
| X | 鏡像翻轉 |
| F | 全螢幕 |
| Shift + D | 顯示 / 隱藏 FPS |
| Q / Esc | 退出 |

## 🏗 架構

```
web/
├── index.html        # 主應用 (~1370 行，零建構，含 i18n 字典)
└── scenes/           # 5 張 AI 生成場景圖
    ├── shanshui.png
    ├── bamboo.png
    ├── snow.png
    ├── flowers.png
    └── stars.png
```

### 渲染管線

```
1. 攝像頭幽靈圖層（15% 透明，畫區域內）
2. 墨線遮罩（Sobel 邊緣，場景切換時生成一次）
3. 光圈裁切 → 揭示彩色層（原圖 + 程序化動畫）
4. 赤陶色光圈環
5. 場景過渡淡入淡出
```

## 📐 設計系統

參見 [DESIGN.md](DESIGN.md)。

品牌色：羊皮紙 `#f5f4ed` · 赤陶 `#c96442` · 墨黑 `#141413`

## 🔮 路線圖

**原始構想：IR 手電筒 + Wii Remote** — Johnny Lee 那種裝置藝術裡的經典做法。Wiimote 內建 IR 攝像頭硬體 blob tracking，100Hz、亞像素、對環境光免疫。當前的 webcam 模式只是該願景的過渡實作。

下面是為這個「光圈揭示」作品調研過的所有可行輸入方式。✅ = 純瀏覽器 · ⚠️ = 需 native bridge

### 🟢 純瀏覽器候選

| 類別 | 方式 | 映射 | 關鍵 API |
|---|---|---|---|
| 指向 | **IR webcam + IR LED 手電** | 現有亮點偵測直接複用 | (no change) |
| | **Wiimote (WebHID)** | IR 攝像頭 → XY，加速度 → 半徑 | `wiimote-webhid` |
| | Joy-Con (WebHID) | 搖桿 + 陀螺儀 | `joy-con-webhid` (Tomayac) |
| | **Wacom 數位板** | 筆位置 + **筆壓 = 半徑** | HTML5 Pointer Events |
| | 雷射筆 + webcam | HSV 偵測紅/綠點 | DIY |
| | AR 標記 (ArUco/AprilTag) | 列印紙標記當「燈籠」 | `js-aruco2` |
| | 遊戲手把 (Xbox/PS) | 搖桿 + 扳機 | Web Gamepad API |
| | SpaceMouse 6DoF | 6 軸推桿 | `spacemouse-webhid` |
| 身體 | **MediaPipe Pose 全身** | 手腕座標 + 肩寬 = 半徑 | `@mediapipe/tasks-vision` |
| | MediaPipe FaceMesh | 鼻尖 + 張嘴 = 半徑 | 同上 |
| | WebGazer 視線追蹤 | 看哪揭哪 | `WebGazer.js` |
| 手機 | **手機當魔杖** | 陀螺儀 + WebRTC，QR Code 配對 | DeviceOrientation API + PeerJS |
| | 手機當觸控板 | 遠端觸控 | 同上 + `touchmove` |
| 音訊 | 音量 → 半徑 | 吹 / 吼 / 拍手 | Web Audio `AnalyserNode` |
| | **呼吸偵測** | 吸氣放大、呼氣收縮 | Web Audio band-pass |
| | 哨音音高 | 音高對應 X 軸 | `pitchy` |
| | 語音指令 | 「揭示」、「放大」 | Web Speech API (Chromium) |
| 專業 | Web MIDI | nanoKONTROL / Launchpad 推桿 | Web MIDI API |
| | OSC over WebSocket | TouchDesigner / Max 推資料 | `osc-js` |
| 生理 | rPPG 心率 | 心跳脈動光圈 | `heartbeat-js` |
| | Muse EEG (BLE) | α 波 → 越靜畫卷開越大 | `web-muse` |
| 其他 | Pixy2 / OpenMV (Web Serial) | 板載 blob 追蹤 | Web Serial API |

### 🟡 需 native bridge

| 方式 | 優勢 |
|---|---|
| Kinect v2 / Azure Kinect | 全身骨架 + 深度 (Azure EOL) |
| Intel RealSense / OAK-D | 深度遮罩做手掌剪影 |
| Leap Motion / Ultraleap | 手部骨架精度最高 |
| Tobii 眼動儀 | 真正的高精度視線 |
| FLIR Lepton 熱像儀 | 全黑環境也能用 |

### ⭐ 最貼合本專案氣質的 5 個方向

每個方向下面都列了需要的技術堆疊，方便想動手的同學心裡有數。「難點」是實作時最容易卡的那一步。

#### ① IR webcam + IR LED 手電

兌現 Johnny Lee 原始願景的最短路徑。**程式碼零修改**——把環境可見光過濾掉之後，現有的亮點偵測立刻變成 IR 追蹤。

- **技術堆疊:** 現有 `getUserMedia` + `spF()` 直接複用
- **硬體:** 一個舊 webcam（拆 IR-cut filter）+ 一片沖洗過的底片當 IR-pass + 一個 IR LED 手電（亞馬遜 ~$10）
- **難點:** 拆機不可逆；要找合適厚度的 IR-pass 濾片
- **狀態:** 尋找願意拆 webcam 的人

#### ② Wacom 筆壓 = 半徑

水墨畫 + 筆壓，主題與機制天然閉環。**純前端，無新依賴**——HTML5 Pointer Events 直接給你筆壓值。

- **技術堆疊:** `pointermove` 事件 + `e.pressure` (0–1)
- **硬體:** 任何 Wacom / XP-Pen / Huion / iPad+Apple Pencil
- **難點:** iPad Safari 的 PointerEvent.pressure 歷史上不穩定，需要測試
- **狀態:** 準備動手的人來 PR

#### ③ 呼吸 + 全身姿態

吸氣放大、呼氣收縮；手腕座標驅動光圈位置。**全沉浸雙模態、手不離身、純瀏覽器。**

- **技術堆疊:**
  - 呼吸: Web Audio `AudioContext` + `BiquadFilterNode`（0.1–0.5 Hz 帶通）+ `AnalyserNode` RMS 包絡
  - 姿態: `@mediapipe/tasks-vision` 的 `PoseLandmarker`（CDN），複用現有 `wkCvs` 攝像頭畫面
- **硬體:** 筆電麥克風 + 攝像頭（已有）
- **難點:** 畫廊噪音環境下呼吸訊噪比；MediaPipe Pose 比 Hands 重一些 (~30fps on M1)
- **狀態:** 我自己想做的下一個

#### ④ 手機當魔杖（WebRTC + QR 配對）

觀眾掃碼把自己的手機變成魔杖，揮動手機控制光圈。**畫廊場景最實用**——觀眾自備硬體。

- **技術堆疊:**
  - 大螢幕: 現有頁面 + WebRTC `RTCDataChannel`
  - 手機端: 同源 mobile-friendly 子頁面，讀 `deviceorientation` (`alpha/beta/gamma`)
  - 配對: PeerJS 公共 broker (省去自建信令) + `qrcode-generator` 生成 QR Code
- **硬體:** 觀眾的手機 + 大螢幕端的電腦
- **難點:** iOS 14+ 要 `DeviceOrientationEvent.requestPermission()`，必須由使用者手勢觸發；首次連線的 ICE 協商時機
- **狀態:** 尋找熟悉 WebRTC 的同學一起做

#### ⑤ OSC from TouchDesigner

讓策展人/營運在不動程式碼的情況下，用 TouchDesigner 的 patch 即時調光圈位置、半徑、場景切換。**裝置藝術圈標準做法。**

- **技術堆疊:**
  - 瀏覽器端: WebSocket client + `osc-js` 解碼 OSC bundle
  - TD 端: WebSocket DAT 節點，發送 `/spot/x`、`/spot/y`、`/spot/r`、`/scene/next` 等位址
  - 可選: 同一介面也能接 Max/MSP / SuperCollider / Pure Data
- **硬體:** 裝 TouchDesigner 的電腦（免費個人版即可）
- **難點:** OSC 是無連線的，丟封包要自己處理；建議加平滑
- **狀態:** 我會畫一個最小 TD patch 當 demo

---

## 🤝 加入

骨架已經寫好（一個 ~1370 行的 `web/index.html`、5 張場景、3 種互動模式、3 種語言介面跑起來了），但**真正有意思的部分需要更多人一起玩**——上面那張路線圖表裡任何一行，只要有人想做，我都可以陪著 review。

### 不寫程式碼也能貢獻

| 我能 | 怎麼做 |
|---|---|
| 提一個新互動方式 | 開 [New Interaction Modality issue](../../issues/new?template=new_modality.md) |
| 報 bug | 開 [Bug report](../../issues/new?template=bug_report.md) |
| 提小改進 | 開 [Feature request](../../issues/new?template=feature_request.md) |
| 閒聊、問問題、曬成品 | [Discussions](../../discussions) |
| 貢獻水墨場景圖 | 見 [CONTRIBUTING.zh-TW.md → 場景圖](CONTRIBUTING.zh-TW.md#-場景圖) |
| 翻譯到其他語言 | 開 issue 提議 |

### 寫程式碼貢獻

Fork → PR。詳細約定見 [CONTRIBUTING.zh-TW.md](CONTRIBUTING.zh-TW.md)。**核心規則只有一條**：保持「單檔案、零建構、零框架」。新增 CDN 單檔案函式庫 OK，新增 webpack 不 OK。

行為準則：[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
安全問題：[SECURITY.zh-TW.md](SECURITY.zh-TW.md)

不吝賜教。

## 📄 License

MIT — 隨便改、隨便商用。

有問題聯絡：[Hugh](https://github.com/Chunyu-Hugh)

詳見 [LICENSE](LICENSE)。
