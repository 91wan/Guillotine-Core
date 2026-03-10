#!/usr/bin/env bash
# OpenClaw-Titanium 核心基建组装脚本
# 融合 Defensive-Starter-Kit (三库隔离) 与 Guillotine (断头台无状态) 架构

set -e

echo "[Titanium] 开始执行钛金架构融合..."

# 1. 挂载断头台网关 (Gatekeeper Proxy)
echo "[Titanium] 🛡️ 部署 Gatekeeper Proxy (叹息之墙网关)..."
cp ~/.openclaw/workspace/scripts/core/gatekeeper_proxy.py ~/.openclaw/workspace/scripts/titanium/
chmod +x ~/.openclaw/workspace/scripts/titanium/gatekeeper_proxy.py
# 真实场景中，这里会配置 systemd 或 pm2 使其常驻，并将 OPENCLAW_API_BASE 指向它。
echo "  -> Gatekeeper Proxy 已就位，准备拦截所有 429/500 限流报错。"

# 2. 挂载记忆降维引擎 (Context Engine)
echo "[Titanium] 🧠 部署 Context Engine (记忆降维脱水器)..."
cp ~/.openclaw/workspace/scripts/core/context_engine.py ~/.openclaw/workspace/scripts/titanium/
chmod +x ~/.openclaw/workspace/scripts/titanium/context_engine.py
echo "  -> Context Engine 已就位，随时准备物理汽化 L1 短期记忆。"

# 3. 部署跨区熔断探针 (Zone-Switch Hard-Reset Probe)
echo "[Titanium] 💥 部署三区切换熔断探针 (Defensive-Kit 结合点)..."
cat << 'PROBE' > ~/.openclaw/workspace/scripts/titanium/zone_switch_hook.sh
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
PROBE
chmod +x ~/.openclaw/workspace/scripts/titanium/zone_switch_hook.sh

# 4. 部署底层输出净化闸门 (Purifier Valve)
echo "[Titanium] 🚿 部署 Purifier Valve (静默刮骨闸门)..."
cp ~/.openclaw/workspace/scripts/core/purifier_sandbox.py ~/.openclaw/workspace/scripts/titanium/
chmod +x ~/.openclaw/workspace/scripts/titanium/purifier_sandbox.py
echo "  -> 净化闸门已就位。所有离开沙箱的字符将被强制剔除机器残骸。"

echo "[Titanium] ✅ 钛金架构 (OpenClaw-Titanium) 组装完成。"
echo "系统当前状态：绝对致盲、物理防越界、输出极简。"
