# 安全策略 · Security Policy

## 项目性质 · Project nature

`ink_scroll` 是纯前端、零后端的浏览器装置艺术作品。没有服务器、没有用户账户、没有数据收集。**所有摄像头/麦克风数据只在浏览器本地处理，从不离开你的设备。**

`ink_scroll` is a pure frontend, zero-backend browser art piece. No server, no user accounts, no data collection. **All camera/microphone data is processed locally in the browser and never leaves your device.**

## 第三方依赖 · Third-party dependencies

| 资源 · Resource | 来源 · Source | 用途 · Purpose |
|---|---|---|
| Noto Serif SC | Google Fonts CDN | 字体 · typography |
| MediaPipe Hands | jsDelivr CDN | 手势识别 · hand gesture |

加载 CDN 资源时会向 Google / jsDelivr 发出 HTTP 请求；如果你需要完全离线，请把这些资源下载到本地并改 `<script src>`。

Loading CDN resources triggers HTTP requests to Google / jsDelivr; for fully offline operation, download these to local and rewrite `<script src>`.

## 浏览器权限 · Browser permissions

页面会请求以下浏览器权限（取决于所选模式）：

- **摄像头** `getUserMedia` — 闪光灯模式 + 手势模式
- **全屏** `requestFullscreen` — 按 F 键时
- **未来可能** WebHID（Wiimote 模式）、麦克风（呼吸/音频模式）、DeviceOrientation（手机魔杖）

所有权限提示由浏览器原生展示，可以拒绝。

The page requests the following browser permissions (depending on mode): camera (`getUserMedia`), fullscreen (`requestFullscreen`), and in the future WebHID / microphone / DeviceOrientation. All permission prompts are native to the browser and may be denied.

## 报告漏洞 · Reporting vulnerabilities

如果你发现安全问题（XSS、CDN 投毒、未授权数据外泄等），请**不要**直接开 public issue。请通过以下方式联系：

If you find a security issue (XSS, CDN poisoning, unauthorized data exfiltration, etc.), please **do not** open a public issue. Contact via:

- GitHub: 给 [@Chunyu-Hugh](https://github.com/Chunyu-Hugh) 发私信 · DM the maintainer
- 或在 GitHub repo 的 Security 标签下创建 [private advisory](../../security/advisories/new) · Or file a private advisory

我会在 7 天内响应。

I aim to respond within 7 days.
