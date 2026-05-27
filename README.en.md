# 墨卷 · Ink Scroll

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **English**

[![Status](https://img.shields.io/badge/status-alpha-c96442?labelColor=141413)](#-roadmap)
[![License: MIT](https://img.shields.io/badge/license-MIT-5e5d59?labelColor=141413)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6b8e6e?labelColor=141413)](CONTRIBUTING.en.md)
[![Discussions](https://img.shields.io/badge/💬-Discussions-7b8fa8?labelColor=141413)](../../discussions)

> *Where light falls, ink comes alive*

A browser-based interactive ink-painting installation. Pure HTML/CSS/JS — single file, zero build steps, no backend.

---

Control a spotlight with your webcam flashlight or hand gestures to reveal a living, animated world hidden beneath traditional Chinese ink paintings. The ink lines stay still; inside the spotlight, the world comes alive.

> 🚧 **Project status:** Alpha — the skeleton is in place, polishing toward a "standard community project." **Come play** — open an [issue](../../issues/new/choose), chat in [Discussions](../../discussions), or pick a direction from the [Roadmap](#-roadmap).

## ✨ Features

| | |
|---|---|
| 🔦 **Flashlight** | Point a phone flashlight at the webcam; brightest spot becomes the spotlight |
| ✋ **Hand Gesture** | MediaPipe hand tracking; an open palm drives the spotlight |
| 🖱 **Mouse** | Trackpad / cursor follows naturally, no camera needed |
| 🏔 **5 Scenes** | Mountains, bamboo, snow, blossoms, starry sky — AI-generated |
| 🎬 **Animations** | Birds, snowflakes, petals, fireflies, shooting stars — visible only inside the spotlight |
| 🎨 **3 Styles** | Ink edges (Sobel), sketch, dark |
| 📐 **Sensitivity** | `[ ]` keys adjust the camera-to-canvas mapping |
| 🌐 **3 Languages** | 简 · 繁 · English, auto-detected from your browser |

## 🛠 Tech Stack

**Pure frontend, no backend.**

| Layer | Tech |
|---|---|
| Rendering | Canvas 2D API |
| Gesture | [MediaPipe Hands](https://ai.google.dev/edge/mediapipe) (via CDN) |
| Camera | `getUserMedia` API |
| Edge detection | Sobel operator (hand-rolled in JS) |
| Fonts | Noto Serif SC / TC + EB Garamond (Google Fonts) |
| Imagery | Grok (`grok-imagine-image`) generated |

The original Python + OpenCV prototype is in `archive/`.

## 🚀 Quick Start

Any static file server works.

```bash
cd web && python3 -m http.server 8888
# Open: http://localhost:8888
```

Camera APIs require HTTPS (localhost is exempt). For dev, Tailscale is the fastest path:

```bash
tailscale serve --bg 8888
# Then: https://your-machine.tailXXXXx.ts.net
```

## ⌨️ Shortcuts

| Key | Action |
|---|---|
| M | Switch mode |
| ← → | Switch scene |
| 1 / 2 / 3 | Style: edges / sketch / dark |
| `[` `]` | Sensitivity − / + |
| + / − or wheel | Spotlight radius |
| R | Reset smoothing |
| X | Mirror flip |
| F | Fullscreen |
| Shift + D | Toggle FPS readout |
| Q / Esc | Quit |

## 🏗 Architecture

```
web/
├── index.html        # Main app (~1370 lines, zero build, includes i18n dict)
└── scenes/           # 5 AI-generated scene images
    ├── shanshui.png
    ├── bamboo.png
    ├── snow.png
    ├── flowers.png
    └── stars.png
```

### Render pipeline

```
1. Camera "ghost" layer (15% opacity, clipped to image bounds)
2. Ink mask (Sobel edges, generated once per scene change)
3. Spotlight clip → reveal the color layer (original image + procedural animation)
4. Terracotta spotlight ring
5. Scene crossfade transition
```

## 📐 Design System

See [DESIGN.md](DESIGN.md).

Brand colors: parchment `#f5f4ed` · terracotta `#c96442` · ink black `#141413`

## 🔮 Roadmap

**Original vision: IR flashlight + Wii Remote** — the classic Johnny-Lee-style installation. The Wiimote's onboard IR camera does hardware blob tracking at 100Hz with sub-pixel precision and is immune to ambient light. The current webcam mode is an interim approximation.

Below is the full survey of input modalities considered for this spotlight-reveal piece. ✅ = pure browser · ⚠️ = native bridge required.

### 🟢 Pure-browser candidates

| Category | Modality | Mapping | Key API / Lib |
|---|---|---|---|
| Pointing | **IR webcam + IR LED wand** | Drops into existing brightness-peak code | (no change) |
| | **Wiimote (WebHID)** | IR camera → XY, accel → radius | `wiimote-webhid` |
| | Joy-Con (WebHID) | Stick + IMU | `joy-con-webhid` (Tomayac) |
| | **Wacom tablet** | Pen XY + **pressure = radius** | HTML5 Pointer Events |
| | Laser pointer + webcam | HSV blob detection (red/green) | DIY |
| | AR markers (ArUco/AprilTag) | Printed paper marker as "lantern" | `js-aruco2` |
| | Gamepad (Xbox/PS) | Stick + trigger | Web Gamepad API |
| | SpaceMouse 6DoF | 6-axis puck | `spacemouse-webhid` |
| Body | **MediaPipe Pose** | Wrist + shoulder span = radius | `@mediapipe/tasks-vision` |
| | MediaPipe FaceMesh | Nose + mouth-open = radius | same |
| | WebGazer eye-tracking | Look-to-reveal | `WebGazer.js` |
| Phone | **Phone-as-wand** | Gyro + WebRTC, QR pairing | DeviceOrientation API + PeerJS |
| | Phone as touchpad | Remote touch input | same + `touchmove` |
| Audio | Volume → radius | Blow / shout / clap | Web Audio `AnalyserNode` |
| | **Breath detection** | Inhale grows, exhale shrinks | Web Audio band-pass |
| | Whistle pitch | Pitch → X-axis | `pitchy` |
| | Voice commands | "reveal", "bigger" | Web Speech API (Chromium) |
| Pro | Web MIDI | nanoKONTROL / Launchpad faders | Web MIDI API |
| | OSC over WebSocket | TouchDesigner / Max push | `osc-js` |
| Bio | rPPG heart-rate | Pulse the spotlight with heartbeat | `heartbeat-js` |
| | Muse EEG (BLE) | α-waves → bigger reveal when calm | `web-muse` |
| Misc | Pixy2 / OpenMV (Web Serial) | Onboard blob tracking | Web Serial API |

### 🟡 Native-bridge required

| Modality | Why |
|---|---|
| Kinect v2 / Azure Kinect | Skeletal + depth (Azure EOL) |
| Intel RealSense / OAK-D | Depth-mask hand silhouette |
| Leap Motion / Ultraleap | Highest-fidelity hand tracking |
| Tobii eye tracker | Production-grade gaze |
| FLIR Lepton thermal | Works in pitch dark |

### ⭐ Best matches for this piece

Each direction below lists the tech stack you'd actually need to learn, plus a "tricky" line calling out where the friction usually lives.

#### ① IR webcam + IR LED wand

The shortest path to Johnny-Lee's original vision. **Zero code change** — filter out the visible spectrum and the existing brightness-peak detector becomes an IR tracker.

- **Stack:** existing `getUserMedia` + `spF()`, reused as-is
- **Hardware:** old webcam (remove the IR-cut filter) + a strip of developed photo film as an IR-pass filter + an IR LED flashlight (~$10 on Amazon)
- **Tricky:** the mod is destructive; finding the right IR-pass thickness takes trial-and-error
- **Status:** looking for someone willing to mod a webcam

#### ② Wacom pen pressure → spotlight radius

Ink-painting meets ink-pen — theme and mechanism close the loop. **Pure browser, no new deps** — HTML5 Pointer Events delivers pressure natively.

- **Stack:** `pointermove` event + `e.pressure` (0–1)
- **Hardware:** any Wacom / XP-Pen / Huion / iPad+Apple Pencil
- **Tricky:** PointerEvent.pressure in iPad Safari has historically been flaky — test before relying on it
- **Status:** PRs welcome

#### ③ Breath + full-body pose

Inhale grows, exhale shrinks; wrist drives spotlight position. **Immersive dual-modal, hands-free, pure browser.**

- **Stack:**
  - Breath: Web Audio `AudioContext` + `BiquadFilterNode` (0.1–0.5 Hz band-pass) + `AnalyserNode` RMS envelope
  - Pose: `@mediapipe/tasks-vision` `PoseLandmarker` (CDN), reusing the existing `wkCvs` camera frame
- **Hardware:** laptop microphone + webcam (already there)
- **Tricky:** breath SNR in a noisy gallery; MediaPipe Pose is heavier than Hands (~30fps on M1)
- **Status:** next on my own short list

#### ④ Phone as a wand (WebRTC + QR pair)

Visitor scans a QR code; their phone becomes a wand. **Best for galleries** — every visitor brings their own hardware.

- **Stack:**
  - Big screen: existing page + WebRTC `RTCDataChannel`
  - Phone side: same-origin mobile sub-page reading `deviceorientation` (`alpha/beta/gamma`)
  - Pairing: PeerJS public broker (avoids running your own signaling) + `qrcode-generator` for the QR
- **Hardware:** visitor's phone + the host computer driving the big screen
- **Tricky:** iOS 14+ requires `DeviceOrientationEvent.requestPermission()`, which must be triggered by a user gesture; first-connection ICE timing
- **Status:** looking for a WebRTC-savvy collaborator

#### ⑤ OSC from TouchDesigner

Lets a curator or operator drive position, radius, and scene live from a TouchDesigner patch — without touching code. **Industry-standard installation pattern.**

- **Stack:**
  - Browser: WebSocket client + `osc-js` to decode OSC bundles
  - TD side: WebSocket DAT node, sending `/spot/x`, `/spot/y`, `/spot/r`, `/scene/next` etc.
  - Optional: the same interface accepts Max/MSP / SuperCollider / Pure Data
- **Hardware:** a computer with TouchDesigner installed (free non-commercial license works)
- **Tricky:** OSC is connectionless, you'll handle packet loss yourself; add smoothing
- **Status:** I'll ship a minimal TD patch as a demo

---

## 🤝 Get involved

The skeleton is in place — ~1370-line `web/index.html`, 5 scenes, 3 working modes, 3-language UI — but **the interesting stuff needs more people in the loop**. Any row of the Roadmap above: if someone wants to take it on, I'll review and pair through it.

### You don't need to code to contribute

| I can | How |
|---|---|
| Propose a new interaction modality | Open [New Interaction Modality issue](../../issues/new?template=new_modality.md) |
| Report a bug | Open [Bug report](../../issues/new?template=bug_report.md) |
| Suggest a small improvement | Open [Feature request](../../issues/new?template=feature_request.md) |
| Chat, ask questions, show off your install | [Discussions](../../discussions) |
| Contribute a new ink scene | See [CONTRIBUTING.en.md → Scene images](CONTRIBUTING.en.md#-scene-images) |
| Translate to another language | Open an issue to discuss |

### If you want to code

Fork → PR. See [CONTRIBUTING.en.md](CONTRIBUTING.en.md) for details. **There's one core rule:** preserve "single file, zero build, zero framework." New CDN single-file libs are fine; new bundlers are not.

Code of Conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
Security: [SECURITY.en.md](SECURITY.en.md)

Don't hold back your insights.

## 📄 License

MIT — do whatever you want, commercial use OK.

Questions: [Hugh](https://github.com/Chunyu-Hugh)

See [LICENSE](LICENSE) for details.
