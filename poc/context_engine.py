#!/usr/bin/env python3
import sys
import json
import os
import hashlib
import time
from pathlib import Path

# --- 配置与路径 ---
WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace/tmp_sandbox/context_engine"))
L1_FILE = WORKSPACE / "l1_memory.json"
L2_FILE = WORKSPACE / "l2_memory.md"
SNAPSHOT_DIR = WORKSPACE / "snapshots"

# 初始化基建
WORKSPACE.mkdir(parents=True, exist_ok=True)
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
if not L1_FILE.exists():
    L1_FILE.write_text("[]")
if not L2_FILE.exists():
    L2_FILE.write_text("# L2 核心法典\n\n")

def log(msg):
    print(f"[Context Engine] {msg}")

def read_l1():
    return json.loads(L1_FILE.read_text())

def write_l1(data):
    L1_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def read_l2():
    return L2_FILE.read_text()

def write_l2(text):
    L2_FILE.write_text(text)

# --- 核心器官 1：L1到L2的降维熔炼 ---
def add_turn(user_msg, system_reply):
    l1 = read_l1()
    l1.append({"U": user_msg, "A": system_reply})
    log(f"记录存入 L1 (当前水线: {len(l1)}/3)")
    
    if len(l1) >= 3:
        log("⚠️ L1 蓄水穿透阈值！唤起廉价算力进行物理降维脱水...")
        # 此处模拟调用了类似 gemini-flash 的总结能力
        mock_summary = f"- [浓缩事实] 用户聊了关于 {l1[0]['U'][:5]}...等3个琐碎问题，核心意图已提纯。\n"
        l2_text = read_l2() + mock_summary
        write_l2(l2_text)
        write_l1([]) # 物理清空 L1
        log("🗑️ 降维完成，L2 法典已更新，L1 垃圾已焚毁。")
    else:
        write_l1(l1)

# --- 核心器官 2：COW 原子快照 ---
def get_snapshot(current_task, session_id):
    timestamp = str(time.time())
    l2_content = read_l2()
    l1_content = read_l1()
    
    # 组装纯净子弹
    snapshot_data = {
        "SystemDirectives": "我是Captain。我没有记忆。我只执行 Snapshot。",
        "AssembledContext": f"【L2长期脱水法则】:\n{l2_content}\n【L1残存短期记忆】:\n{json.dumps(l1_content, ensure_ascii=False)}",
        "CurrentTask": current_task
    }
    
    # 算 Hash，生成不可篡改的死文件
    snapshot_str = json.dumps(snapshot_data, ensure_ascii=False, indent=2)
    hash_str = hashlib.md5((snapshot_str + timestamp + session_id).encode()).hexdigest()[:8]
    snapshot_path = SNAPSHOT_DIR / f"snapshot_{session_id}_{hash_str}.json"
    
    snapshot_path.write_text(snapshot_str)
    log(f"⚡ COW 快照生成！已生成死文件，拒绝任何引用和动态游标。路径: {snapshot_path}")
    return str(snapshot_path)

# --- 核心器官 3：硬熔断 ---
def hard_reset():
    log("💥 侦测到硬熔断指令！引爆现有全部神经记忆！")
    # 模拟向上提取最终结案
    final_archive = "---\n档案结案归档：该主题已物理切断。\n---\n"
    archive_path = WORKSPACE / f"archive_{int(time.time())}.txt"
    archive_path.write_text(final_archive)
    
    L1_FILE.write_text("[]")
    L2_FILE.write_text("# L2 核心法典\n\n")
    # 清理所有快照
    for f in SNAPSHOT_DIR.iterdir():
        f.unlink()
    log(f"🔥 原地销毁完毕。最终灰烬存在 {archive_path}。系统回归年轻。")

# --- CLI 路由 ---
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "add":
        add_turn(sys.argv[2], sys.argv[3])
    elif cmd == "snapshot":
        print(get_snapshot(sys.argv[2], sys.argv[3]))
    elif cmd == "reset":
        hard_reset()
