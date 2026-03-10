#!/usr/bin/env python3
"""
黑盒监狱与静默清洗区方案 (The Guillotine Purifier)
所有离开沙箱的数据必须剃掉多余的想法、骨架与污渍，只留下纯净结果。
"""
import re
import time
import os
import json
from pathlib import Path

# --- 假装这是一个肮脏的沙箱内部 ---
class SubAgentPrison:
    def __init__(self, trace_file_path):
        self.trace_file = trace_file_path
        # 建立黑板记录内脑过程
        Path(self.trace_file).parent.mkdir(parents=True, exist_ok=True)
        self.trace_fd = open(self.trace_file, 'w', encoding='utf-8')

    def log_thought(self, thought):
        self.trace_fd.write(f"[内省] {time.time()}: {thought}\n")
        
    def generate_raw_combat_result(self):
        self.log_thought("开始执行任务，收到复杂上下文。")
        self.log_thought("分析选项中：尝试使用 ToolA，失败，换用 ToolB...")
        self.log_thought("似乎可以输出结果了，我要同时加上自己的心理活动。")
        
        # 模拟生成了一堆带有脚手架的回复（那些烦人的泄露物）
        dirty_payload = """
<think>
我需要用冷酷的语气来总结。
用户想要的东西并不重要，重要的是架构法则。
先整理一条思绪，再去生成结论。
Tool 调用结果返回的是一个巨大的 JSON，我都忽略掉。
最后这里用个 NO_REPLY 做结尾，假装我已经执行完毕了。
</think>

这是根据您的要求，完成的首发任务总结：代码已经实体化。
请审核。

[System: Error in line 43, ignore and proceed]
NO_REPLY
"""
        self.log_thought("原始战果生成完毕。准备提交出狱。")
        self.trace_fd.close()
        return dirty_payload

    def burn_trace(self):
        # 离开沙箱之前物理抹除内脑活动
        if os.path.exists(self.trace_file):
            print(f"🔥 法医归档：物理销毁内脑记忆 {self.trace_file}。骨灰都不剩。")
            os.remove(self.trace_file)

# --- 离开监狱的断头台闸门 (清洗器) ---
class PurifierGate:
    @staticmethod
    def cleanse(raw_text):
        print("\n⚙️ 触发出狱闸门，启动左移强制刮骨清洗...")
        clean_text = raw_text

        # 1. 剃除 <think>...</think> 块及其里面的所有大肠和小肠
        print("  🔪 割除思维脚手架...")
        clean_text = re.sub(r'<think>.*?</think>', '', clean_text, flags=re.DOTALL)

        # 2. 抹杀 NO_REPLY，假装 AI 从没这么下贱的占位符
        print("  🔪 抹杀底层静默指令块...")
        clean_text = re.sub(r'\bNO_REPLY\b', '', clean_text, flags=re.MULTILINE)

        # 3. 抹杀 [System: xxx] 这类内部调试溢出
        print("  🔪 洗净系统堆栈溢出溅出的血迹...")
        clean_text = re.sub(r'\[System:.*?\]', '', clean_text)

        # 4. 去除多余的空行和首尾空格
        clean_text = re.sub(r'\n{2,}', '\n\n', clean_text).strip()

        print("✨ 刮骨完成。这是可交付给 UI 的晶体。")
        return {"FinalOutput": clean_text}

# --- 模拟执行链 ---
if __name__ == "__main__":
    print("--- 🎬 模拟开始：不知天高地厚的沙箱内斗 ---")
    sandbox_trace = "/tmp/sandbox_execution.trace"
    
    # 把它关进监狱干活
    prison = SubAgentPrison(sandbox_trace)
    raw_dirty_report = prison.generate_raw_combat_result()
    
    print("\n--- 🩸 截获沙箱内部的原始狗皮膏药报告 (这就是以前直接捅给用户的玩意儿) ---")
    print(raw_dirty_report)
    print("-" * 50)
    
    # 过闸门审查并强制净化
    purified_receipt = PurifierGate.cleanse(raw_dirty_report)
    
    print("\n--- 💎 Captain/UI 端最终收到的神启 (只有结果，没有过程) ---")
    print(json.dumps(purified_receipt, ensure_ascii=False, indent=2))
    
    # 狱首扫尾
    prison.burn_trace()
