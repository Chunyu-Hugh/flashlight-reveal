#!/bin/bash
# Flashlight Reveal v2 — 启动脚本
# 用法:
#   ./run.sh                    默认demo图，绘画模式
#   ./run.sh mypic.jpg          用自己的图
#   ./run.sh mypic.jpg -m flashlight  手电筒临时模式
#   ./run.sh mypic.jpg --calibrate    首次使用建议校准

cd "$(dirname "$0")"

# 激活虚拟环境
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
elif [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi

# 默认全屏 + mirror-x（摄像头对着屏幕时通常需要镜像）
exec python3 reveal.py "$@" -f --mirror-x
