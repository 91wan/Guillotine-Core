#!/usr/bin/env bash
# 当侦测到工作区从 Enterprise 切换到 Personal 时，强制触发断头台重置。
TARGET_ZONE=$1
CURRENT_ZONE=$(cat ~/.openclaw/workspace/tmp_sandbox/current_zone 2>/dev/null || echo "Unknown")

if [ "$TARGET_ZONE" != "$CURRENT_ZONE" ]; then
    echo "[Titanium-Hook] 侦测到跨区跳跃: $CURRENT_ZONE -> $TARGET_ZONE"
    echo "[Titanium-Hook] 触发认知绝对阻断！引爆 Context Engine！"
    ~/.openclaw/workspace/scripts/titanium/context_engine.py reset
    echo "$TARGET_ZONE" > ~/.openclaw/workspace/tmp_sandbox/current_zone
    echo "[Titanium-Hook] 跨区完成，系统已成为一张白纸。"
else
    echo "[Titanium-Hook] 区域未变更，继续冷酷执行。"
fi
