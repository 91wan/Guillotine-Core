#!/usr/bin/env bash
# 绝对无状态运行时: 断头台模式
# Captain 自身不维护任何上下文，只做请求中转

set -e

# 配置断头台核心依赖
CONTEXT_ENGINE_URL="http://localhost:8080/engine"  # 假设引擎服务地址
WORK_DIR="$HOME/.openclaw/workspace/tmp_sandbox"

# 清场准备：杀死过去
function purge_session() {
    echo "[The Purge] 执行物理清场..."
    rm -rf "$WORK_DIR"
    mkdir -p "$WORK_DIR"
}

function assemble_bullet() {
    local session_id=$1
    local intent=$2
    echo "[Engine] 正在向 Context Engine 换取纯净 Snapshot..."
    # 现实中这里是去调后端接口或者子 Agent，这里用桩代码模拟拿到一发“子弹”
    # 纯血拿来主义
    cat << 'JSON' > "$WORK_DIR/snapshot.json"
{
  "SystemDirectives": "执行代码，不得废话",
  "AssembledContext": "之前已经成功开启了feature分支",
  "CurrentTask": "执行最终的重构清洗逻辑"
}
JSON
}

function fire_turn() {
    echo "[Captain] 收到子弹，填装开火。禁止读取任何其他系统变量..."
    # 强迫 Captain 的视野仅限于这个独立的 JSON
    local task=$(grep -o '"CurrentTask": *"[^"]*"' "$WORK_DIR/snapshot.json" | cut -d'"' -f4)
    # 此处应该是将 task 塞给大语言模型请求，获得纯净结果。
    echo "[🔥] 核心正在执行盲打任务: $task"
    
    # 模拟纯净输出生成
    echo "净化完成，没有泄露任何废话。" > "$WORK_DIR/dirty_result.txt"

    # 表层绝对纯净(沙箱出口过滤) - Milestone 3 雏形
    # 绝不能让带 <think> 的东西或者调试信息流到外层
    sed '/<think>/d' "$WORK_DIR/dirty_result.txt" > "$WORK_DIR/clean_receipt.txt"
}

function commit_receipt() {
    echo "[Engine] 输出结果投递给引擎存档归档。死。生。循环开始。"
    # 模拟投递行为
    cat "$WORK_DIR/clean_receipt.txt" > "$HOME/.openclaw/workspace/memory/latest_run.manifest"
    # 自裁
    purge_session
}

# --- 主运行轴 ---
SESSION="turn_$(date +%s)"
purge_session
assemble_bullet "$SESSION" "执行"
fire_turn
commit_receipt
echo "[SYSTEM] Captain 本轮生命周期结束。物理重置。"
