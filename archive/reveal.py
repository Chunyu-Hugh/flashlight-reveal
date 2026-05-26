#!/usr/bin/env python3
"""
Flashlight Reveal v2 — 摄像头版壁画手电筒

改进：
  - 透视校准：4点标定，精确映射摄像头→屏幕
  - 绘画模式：照过的地方颜色永久保留
  - 双模式：手电筒（临时）/ 画笔（永久）
  - 多线程：摄像头采集独立线程，渲染不卡
  - 发光羽化效果
  - 校准数据可保存/加载
"""

import cv2
import numpy as np
import argparse
import sys
import json
import threading
import time
from pathlib import Path
from collections import deque


# ═══════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════

def create_demo_image(width=1920, height=1080):
    """生成彩色 demo 图"""
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # 天空渐变
    for i in range(height):
        img[i, :] = [int(40 + 80 * i / height),
                     int(100 + 80 * i / height),
                     int(180 + 40 * i / height)]

    # 太阳
    cv2.circle(img, (width // 2, height // 4), 120, (80, 200, 255), -1)
    cv2.circle(img, (width // 2, height // 4), 120, (100, 220, 255), 3)

    # 山
    pts = np.array([[0, height], [width//4, height//2], [width//2, height//3],
                    [3*width//4, height//2+50], [width, height//2-50], [width, height]], np.int32)
    cv2.fillPoly(img, [pts], (60, 120, 60))

    # 前景山
    pts2 = np.array([[0, height], [width//3, height*2//3], [width//2, height//2+50],
                     [2*width//3, height*2//3+30], [width, height*2//3], [width, height]], np.int32)
    cv2.fillPoly(img, [pts2], (30, 80, 30))

    # 树
    for bx in [width//5, width//2, 4*width//5]:
        # 树干
        cv2.rectangle(img, (bx-15, height-250), (bx+15, height-100), (80, 50, 20), -1)
        # 树冠
        for layer in range(3):
            r = 100 - layer * 20
            cy = height - 260 - layer * 30
            cv2.circle(img, (bx, cy), r, (20, 100+layer*20, 20), -1)

    # 地面
    cv2.rectangle(img, (0, height-100), (width, height), (100, 140, 60), -1)

    # 花
    np.random.seed(42)
    for _ in range(150):
        x = np.random.randint(50, width-50)
        y = np.random.randint(height-90, height-30)
        r = np.random.randint(3, 12)
        color = tuple(np.random.randint(50, 255, 3).tolist())
        cv2.circle(img, (x, y), r, color, -1)

    # 文字
    cv2.putText(img, "Flashlight Reveal", (width//2-300, 80),
                cv2.FONT_HERSHEY_DUPLEX, 2.5, (255, 255, 255), 3)

    return img


def create_hidden_layer(color_img, style="edges"):
    """从彩色图生成隐藏层"""
    gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

    if style == "edges":
        edges = cv2.Canny(gray, 35, 100)
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif style == "sketch":
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (31, 31), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        sketch = (sketch * 0.6).astype(np.uint8)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    else:  # "dark"
        return (cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) * 0.12).astype(np.uint8)


# ═══════════════════════════════════════════════════════
#  校准系统
# ═══════════════════════════════════════════════════════

class Calibration:
    """4点透视校准：将摄像头坐标映射到屏幕坐标"""

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.cam_points = []   # 摄像头画面中的4个角点
        self.screen_points = []  # 对应屏幕上的4个角点
        self.M = None  # 透视变换矩阵

    def set_default(self):
        """默认校准：假设摄像头正好覆盖屏幕"""
        margin = 0.05
        self.cam_points = [
            (margin, margin),
            (1 - margin, margin),
            (1 - margin, 1 - margin),
            (margin, 1 - margin),
        ]
        self.screen_points = [
            (0, 0),
            (self.screen_w, 0),
            (self.screen_w, self.screen_h),
            (0, self.screen_h),
        ]
        self._compute_matrix()

    def add_point_pair(self, cam_x_frac, cam_y_frac, screen_x, screen_y):
        """添加一对校准点（摄像头用归一化坐标 0~1）"""
        self.cam_points.append((cam_x_frac, cam_y_frac))
        self.screen_points.append((screen_x, screen_y))

    def _compute_matrix(self):
        if len(self.cam_points) >= 4:
            src = np.float32([(p[0] * 640, p[1] * 480) for p in self.cam_points[:4]])
            dst = np.float32(self.screen_points[:4])
            self.M = cv2.getPerspectiveTransform(src, dst)

    def transform(self, cam_x_frac, cam_y_frac):
        """将归一化摄像头坐标映射到屏幕坐标"""
        if self.M is None:
            # 回退到简单比例映射
            return (int(cam_x_frac * self.screen_w),
                    int(cam_y_frac * self.screen_h))
        pt = np.float32([[cam_x_frac * 640, cam_y_frac * 480]])
        pt = cv2.perspectiveTransform(pt.reshape(-1, 1, 2), self.M)
        return (int(np.clip(pt[0][0][0], 0, self.screen_w)),
                int(np.clip(pt[0][0][1], 0, self.screen_h)))

    def save(self, path):
        data = {
            "screen_w": self.screen_w,
            "screen_h": self.screen_h,
            "cam_points": self.cam_points,
            "screen_points": self.screen_points,
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"校准数据已保存: {path}")

    @classmethod
    def load(cls, path, screen_w, screen_h):
        with open(path) as f:
            data = json.load(f)
        calib = cls(data["screen_w"], data["screen_h"])
        calib.cam_points = data["cam_points"]
        calib.screen_points = data["screen_points"]
        calib._compute_matrix()
        # 如果屏幕尺寸变了，更新但保持映射关系
        calib.screen_w = screen_w
        calib.screen_h = screen_h
        return calib


# ═══════════════════════════════════════════════════════
#  摄像头线程
# ═══════════════════════════════════════════════════════

class CameraThread:
    """独立线程采集摄像头，降低延迟"""

    def __init__(self, camera_id=0, width=640, height=480, fps=30):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.width = width
        self.height = height
        self.frame = None
        self.gray_frame = None
        self.running = False
        self.lock = threading.Lock()
        self._thread = None
        self.fps_counter = deque(maxlen=30)

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        t0 = time.time()
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
                    self.gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.fps_counter.append(time.time() - t0)
                t0 = time.time()

    def get_frames(self):
        with self.lock:
            if self.frame is None:
                return None, None
            return self.frame.copy(), self.gray_frame.copy()

    def get_fps(self):
        if not self.fps_counter:
            return 0
        return 1.0 / (sum(self.fps_counter) / len(self.fps_counter))

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=1)
        self.cap.release()


# ═══════════════════════════════════════════════════════
#  光点检测
# ═══════════════════════════════════════════════════════

class SpotDetector:
    """检测摄像头画面中的手电筒光点"""

    def __init__(self, method="centroid", threshold_percentile=97):
        self.method = method
        self.threshold_percentile = threshold_percentile
        self.last_spot = None
        self.confidence = 0.0

    def detect(self, gray_frame):
        """返回 (归一化坐标, 置信度)，未检测到返回 (None, 0.0)"""
        h, w = gray_frame.shape

        if self.method == "max":
            blurred = cv2.GaussianBlur(gray_frame, (15, 15), 0)
            _, max_val, _, max_loc = cv2.minMaxLoc(blurred)
            if max_val > 200:  # 亮度阈值
                fx, fy = max_loc[0] / w, max_loc[1] / h
                conf = min(max_val / 255.0, 1.0)
                self.last_spot = (fx, fy)
                self.confidence = conf
                return (fx, fy), conf

        elif self.method == "centroid":
            # 取最亮的 N% 像素，计算质心
            blurred = cv2.GaussianBlur(gray_frame, (21, 21), 0)
            thresh_val = np.percentile(blurred, self.threshold_percentile)
            if thresh_val < 150:
                self.confidence *= 0.9  # 衰减置信度
                return None, max(self.confidence, 0.0)

            _, bright = cv2.threshold(blurred, thresh_val, 255, cv2.THRESH_BINARY)

            # 形态学操作去噪
            kernel = np.ones((5, 5), np.uint8)
            bright = cv2.morphologyEx(bright, cv2.MORPH_OPEN, kernel)
            bright = cv2.morphologyEx(bright, cv2.MORPH_CLOSE, kernel)

            # 找轮廓，取最大的
            contours, _ = cv2.findContours(bright, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                self.confidence *= 0.9
                return None, max(self.confidence, 0.0)

            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            if area < 20:  # 太小，忽略
                self.confidence *= 0.9
                return None, max(self.confidence, 0.0)

            M = cv2.moments(largest)
            if M["m00"] > 0:
                cx = M["m10"] / M["m00"]
                cy = M["m01"] / M["m00"]
                fx, fy = cx / w, cy / h
                conf = min(area / 5000, 1.0)  # 面积越大，置信度越高
                self.last_spot = (fx, fy)
                self.confidence = conf
                return (fx, fy), conf

        self.confidence *= 0.9
        return None, max(self.confidence, 0.0)


# ═══════════════════════════════════════════════════════
#  渲染器
# ═══════════════════════════════════════════════════════

class RevealRenderer:
    """管理显色状态和画面合成"""

    def __init__(self, target_img, hidden_img, mode="paint"):
        self.target = target_img.astype(np.float32)
        self.hidden = hidden_img.astype(np.float32)
        self.h, self.w = target_img.shape[:2]
        self.mode = mode  # "paint" 永久 | "flashlight" 临时

        # 永久显色的累积遮罩（绘画模式用）
        self.paint_mask = np.zeros((self.h, self.w), dtype=np.float32)

    def compute_frame(self, screen_pos, radius, trail=None):
        """
        合成一帧画面
        screen_pos: (x, y) 屏幕坐标
        radius: 光圈半径
        trail: 尾迹位置列表 [(x, y), ...]
        """
        # 当前帧的临时遮罩
        frame_mask = np.zeros((self.h, self.w), dtype=np.float32)

        # 主光圈
        if screen_pos is not None:
            sx, sy = screen_pos
            cv2.circle(frame_mask, (sx, sy), radius, 1.0, -1)

        # 尾迹
        if trail:
            for i, (tx, ty) in enumerate(reversed(trail[:8])):
                alpha = 0.5 * (1 - i / 8)
                r = max(int(radius * 0.6 * (1 - i / 8)), 8)
                cv2.circle(frame_mask, (tx, ty), r, alpha, -1)

        # 羽化
        blur_size = min(max(radius * 2 + 1, 31), 201)
        frame_mask = cv2.GaussianBlur(frame_mask, (blur_size, blur_size), radius / 3)

        if self.mode == "paint":
            # 绘画模式：累积遮罩
            self.paint_mask = np.maximum(self.paint_mask, frame_mask)
            # 再加一层羽化让边缘更自然
            paint_blur = cv2.GaussianBlur(self.paint_mask, (51, 51), 15)
            effective_mask = paint_blur
        else:
            # 手电筒模式：只用当前帧的遮罩
            effective_mask = frame_mask

        # 合成
        mask_3ch = np.stack([effective_mask, effective_mask, effective_mask], axis=2)
        result = self.hidden * (1.0 - mask_3ch) + self.target * mask_3ch
        result = np.clip(result, 0, 255).astype(np.uint8)

        return result

    def get_paint_progress(self):
        """返回绘画进度（已显色区域的百分比）"""
        return float(np.sum(self.paint_mask > 0.1) / (self.w * self.h))

    def reset_paint(self):
        self.paint_mask.fill(0)


# ═══════════════════════════════════════════════════════
#  主程序
# ═══════════════════════════════════════════════════════

def run_calibration(camera, screen_w, screen_h):
    """交互式校准流程"""
    calib = Calibration(screen_w, screen_h)
    calib_points_needed = 4
    current_point = 0
    instructions = [
        "把光点对准屏幕 左上角，按 SPACE",
        "把光点对准屏幕 右上角，按 SPACE",
        "把光点对准屏幕 右下角，按 SPACE",
        "把光点对准屏幕 左下角，按 SPACE",
    ]

    detector = SpotDetector(method="centroid")
    cam_w, cam_h = 640, 480
    calib_win = "Calibration"
    cv2.namedWindow(calib_win, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(calib_win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # 屏幕角点（归一化）
    screen_corners = [(0, 0), (1, 0), (1, 1), (0, 1)]
    screen_px = [(0, 0), (screen_w, 0), (screen_w, screen_h), (0, screen_h)]

    print("\n=== 校准模式 ===")
    print("请用手电筒依次照射屏幕的四个角\n")

    while True:
        ret, raw = camera.cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
        spot, conf = detector.detect(gray)

        # 画面：显示摄像头画面 + 标记
        display = raw.copy()
        if spot:
            px, py = int(spot[0] * cam_w), int(spot[1] * cam_h)
            cv2.circle(display, (px, py), 15, (0, 255, 255), 2)
            cv2.circle(display, (px, py), 5, (0, 255, 255), -1)

        # 文字说明
        cv2.putText(display, f"Point {current_point + 1}/4", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(display, instructions[current_point], (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(display, "DETECTED!" if conf > 0.5 else "searching...", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0) if conf > 0.5 else (100, 100, 100), 2)

        # 当前角点在屏幕上的位置标记
        scx, scy = screen_px[current_point]
        cv2.circle(display, (int(scx * cam_w / screen_w), int(scy * cam_h / screen_h)),
                   8, (0, 0, 255), -1)

        cv2.imshow(calib_win, display)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC 跳过校准
            calib.set_default()
            break
        elif key == ord(' '):
            if spot and conf > 0.5:
                calib.add_point_pair(spot[0], spot[1],
                                     screen_px[current_point][0],
                                     screen_px[current_point][1])
                print(f"  ✓ 第 {current_point+1} 点: cam=({spot[0]:.3f},{spot[1]:.3f}) -> screen={screen_px[current_point]}")
                current_point += 1
                if current_point >= calib_points_needed:
                    calib._compute_matrix()
                    print("校准完成！")
                    break
            else:
                print("  未检测到光点，请确保手电筒亮着并照在角落上")

    cv2.destroyWindow(calib_win)
    return calib


def main():
    parser = argparse.ArgumentParser(
        description="Flashlight Reveal v2 — 壁画手电筒（摄像头版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 reveal.py                        # 默认demo图，绘画模式
  python3 reveal.py mural.jpg              # 用自己的图
  python3 reveal.py mural.jpg -m flashlight # 手电筒模式（离开就暗）
  python3 reveal.py mural.jpg --calibrate  # 手动校准
  python3 reveal.py mural.jpg -c calib.json # 加载校准文件
        """
    )
    parser.add_argument("image", nargs="?", help="图片路径（不指定则生成demo图）")
    parser.add_argument("-c", "--camera", type=int, default=0, help="摄像头索引")
    parser.add_argument("--cam-width", type=int, default=640)
    parser.add_argument("--cam-height", type=int, default=480)
    parser.add_argument("-s", "--style", choices=["edges", "sketch", "dark"],
                        default="edges", help="隐藏层风格")
    parser.add_argument("-r", "--radius", type=int, default=140, help="光圈半径")
    parser.add_argument("-m", "--mode", choices=["paint", "flashlight"],
                        default="paint", help="paint=永久显色, flashlight=临时")
    parser.add_argument("--detect", choices=["max", "centroid"],
                        default="centroid", help="检测方法")
    parser.add_argument("--calibrate", action="store_true", help="启动校准流程")
    parser.add_argument("--calib-file", type=str, default="calibration.json",
                        help="校准文件路径")
    parser.add_argument("--threshold", type=int, default=97,
                        help="centroid检测的亮度百分位阈值 (默认97)")
    parser.add_argument("-f", "--fullscreen", action="store_true")
    parser.add_argument("--mirror-x", action="store_true", help="水平镜像摄像头")
    parser.add_argument("--mirror-y", action="store_true", help="垂直镜像摄像头")
    parser.add_argument("--no-trail", action="store_true", help="关闭尾迹")
    args = parser.parse_args()

    # 加载或生成图像
    if args.image:
        target = cv2.imread(args.image)
        if target is None:
            print(f"错误：无法加载 {args.image}")
            sys.exit(1)
    else:
        target = create_demo_image(1920, 1080)

    h, w = target.shape[:2]
    print(f"图像: {w}x{h} | 模式: {args.mode} | 隐藏层: {args.style}")

    # 隐藏层
    hidden = create_hidden_layer(target, args.style)

    # 渲染器
    renderer = RevealRenderer(target, hidden, args.mode)

    # 摄像头线程
    cam = CameraThread(args.camera, args.cam_width, args.cam_height)
    if not cam.cap.isOpened():
        print(f"错误：无法打开摄像头 {args.camera}")
        sys.exit(1)
    cam.start()
    time.sleep(0.5)  # 等第一帧

    # 校准
    calib_path = Path(args.calib_file)
    if args.calibrate:
        calibration = run_calibration(cam, w, h)
        calibration.save(calib_path)
    elif calib_path.exists():
        print(f"加载校准文件: {calib_path}")
        calibration = Calibration.load(str(calib_path), w, h)
    else:
        print("使用默认校准（假设摄像头正对全屏）")
        calibration = Calibration(w, h)
        calibration.set_default()

    # 光点检测器
    detector = SpotDetector(method=args.detect, threshold_percentile=args.threshold)

    # 窗口
    win_name = "Flashlight Reveal v2"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    if args.fullscreen:
        cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # 状态
    radius = args.radius
    trail_enabled = not args.no_trail
    trail_positions = []
    smooth_x, smooth_y = w // 2, h // 2
    smooth_alpha = 0.3
    show_ui = True
    mouse_x, mouse_y = w // 2, h // 2
    mouse_down = False

    def on_mouse(event, x, y, flags, param):
        nonlocal mouse_x, mouse_y, mouse_down
        mouse_x, mouse_y = x, y
        mouse_down = (flags & cv2.EVENT_FLAG_LBUTTON) != 0

    cv2.setMouseCallback(win_name, on_mouse)

    print("\n=== 控制键 ===")
    print("  Q/ESC    退出          F      全屏")
    print("  +/-      光圈大小       R      重置画面")
    print("  T        尾迹开关       S      保存截图")
    print("  1/2/3    隐藏层风格     M      切换模式")
    print("  H        隐藏/显示UI    C      重新校准")
    print("  鼠标拖拽 模拟手电筒（调试用）")
    print("==============\n")

    no_spot_frames = 0
    last_progress_report = 0

    while True:
        # 获取摄像头帧
        color_frame, gray_frame = cam.get_frames()

        screen_pos = None

        if color_frame is not None and gray_frame is not None:
            # 镜像
            if args.mirror_x:
                color_frame = cv2.flip(color_frame, 1)
                gray_frame = cv2.flip(gray_frame, 1)
            if args.mirror_y:
                color_frame = cv2.flip(color_frame, 0)
                gray_frame = cv2.flip(gray_frame, 0)

            # 检测光点
            spot, conf = detector.detect(gray_frame)

            if spot and conf > 0.3:
                no_spot_frames = 0
                screen_pos = calibration.transform(spot[0], spot[1])
            else:
                no_spot_frames += 1

        # 鼠标作为后备（调试或没检测到光点时）
        if screen_pos is None or (mouse_down and no_spot_frames > 30):
            screen_pos = (mouse_x, mouse_y)

        # 平滑
        if screen_pos:
            smooth_x = int(smooth_alpha * screen_pos[0] + (1 - smooth_alpha) * smooth_x)
            smooth_y = int(smooth_alpha * screen_pos[1] + (1 - smooth_alpha) * smooth_y)
            smooth_pos = (smooth_x, smooth_y)
        else:
            smooth_pos = None

        # 尾迹
        if trail_enabled and smooth_pos:
            trail_positions.append(smooth_pos)
            if len(trail_positions) > 10:
                trail_positions.pop(0)
        elif not trail_enabled:
            trail_positions = []

        # 渲染
        result = renderer.compute_frame(smooth_pos, radius, trail_positions)

        # UI 叠加
        if show_ui:
            # 摄像头小窗
            if color_frame is not None:
                preview_h = 180
                preview_w = int(preview_h * color_frame.shape[1] / color_frame.shape[0])
                preview = cv2.resize(color_frame, (preview_w, preview_h))
                if spot:
                    px = int(spot[0] * preview_w)
                    py = int(spot[1] * preview_h)
                    cv2.circle(preview, (px, py), 8, (0, 255, 255), 2)
                    cv2.circle(preview, (px, py), 3, (0, 255, 255), -1)
                result[10:10 + preview_h, w - preview_w - 10:w - 10] = preview
                cv2.rectangle(result,
                              (w - preview_w - 10, 10),
                              (w - 10, 10 + preview_h), (80, 80, 80), 2)

            # 状态文字
            lines = [
                f"Mode: {args.mode} | Radius: {radius} | Style: {args.style}",
                f"FPS: {cam.get_fps():.0f} | Trail: {'ON' if trail_enabled else 'OFF'}",
            ]
            if args.mode == "paint":
                progress = renderer.get_paint_progress()
                lines.append(f"Revealed: {progress * 100:.1f}%")
                if progress > 0 and time.time() - last_progress_report > 5:
                    print(f"  显色进度: {progress * 100:.1f}%")
                    last_progress_report = time.time()

            y = h - 70
            for line in lines:
                cv2.putText(result, line, (20, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (160, 160, 160), 1)
                y += 22

        cv2.imshow(win_name, result)

        # 键盘
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        elif key == ord('f'):
            prop = cv2.getWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN,
                                  cv2.WINDOW_NORMAL if prop == cv2.WINDOW_FULLSCREEN
                                  else cv2.WINDOW_FULLSCREEN)
        elif key == ord('+') or key == ord('='):
            radius = min(radius + 15, max(w, h) // 3)
        elif key == ord('-') or key == ord('_'):
            radius = max(radius - 15, 20)
        elif key == ord('r'):
            renderer.reset_paint()
            trail_positions.clear()
            print("画面已重置")
        elif key == ord('t'):
            trail_enabled = not trail_enabled
            trail_positions.clear()
        elif key == ord('m'):
            args.mode = "flashlight" if args.mode == "paint" else "paint"
            renderer.mode = args.mode
            renderer.reset_paint()
            print(f"切换模式: {args.mode}")
        elif key == ord('s'):
            out_dir = Path(__file__).parent / "screenshots"
            out_dir.mkdir(exist_ok=True)
            ts = int(time.time())
            out_path = out_dir / f"reveal_{args.mode}_{ts}.png"
            cv2.imwrite(str(out_path), result)
            print(f"截图: {out_path}")
        elif key == ord('h'):
            show_ui = not show_ui
        elif key == ord('c'):
            print("重新校准...")
            cv2.destroyWindow(win_name)
            calibration = run_calibration(cam, w, h)
            calibration.save(calib_path)
            renderer.reset_paint()
            cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(win_name, on_mouse)
            if args.fullscreen:
                cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN,
                                      cv2.WINDOW_FULLSCREEN)
        elif key in (ord('1'), ord('2'), ord('3')):
            styles = ["edges", "sketch", "dark"]
            args.style = styles[key - ord('1')]
            hidden = create_hidden_layer(target, args.style)
            renderer.hidden = hidden.astype(np.float32)
            print(f"风格: {args.style}")

    # 清理
    cam.stop()
    cv2.destroyAllWindows()

    # 保存校准（如果有改动）
    if not calib_path.exists():
        calibration.save(calib_path)

    print("再见！")


if __name__ == "__main__":
    main()
