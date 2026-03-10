#!/usr/bin/env python3
"""
Gatekeeper Proxy 堡垒网关 (The Guillotine Gateway)
绝对隔离外部网络恶劣环境，对内(Captain)只报喜不报忧。
基于 Python 标准库实现的轻量代理验证原型。
"""
import http.server
import socketserver
import json
import time
import uuid

# --- 模拟不稳定的外部大世界 ---
class ExternalHostMock:
    def __init__(self):
        self.request_count = 0

    def call_llm_api(self, payload):
        self.request_count += 1
        print(f"      [外部烂网] 远端收到请求 (第 {self.request_count} 次尝试)...")
        time.sleep(0.5)
        # 模拟：前两次都会被无情干掉 (429 Rate Limit)
        if self.request_count < 3:
            print("      [外部烂网] 💥 触发 429 Too Many Requests 限流！")
            return 429, None
        print("      [外部烂网] ✅ 终于接客了。返回 200。")
        self.request_count = 0 # reset
        return 200, {"choices": [{"message": {"content": "极简结论已生成。"}}]}

EXTERNAL_HOST = ExternalHostMock()


# --- Gatekeeper 核心堡垒 ---
class GatekeeperHandler(http.server.BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            payload = json.loads(post_data)
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
            return

        print(f"\n[Gatekeeper] 🛡️ 截获 Captain 请求: 目标={self.path}")
        
        # --- 脏活地堡：指数退避与隐瞒 ---
        max_retries = 3
        backoff = 1  # 初始退避 1 秒
        
        for attempt in range(1, max_retries + 1):
            print(f"[Gatekeeper] 🚀 第 {attempt} 次替 Captain 向外发兵...")
            status_code, response_data = EXTERNAL_HOST.call_llm_api(payload)
            
            if status_code == 200:
                print(f"[Gatekeeper] 🎯 攻坚成功！包装成完美的 200 交回给 Captain。")
                self._send_response(200, response_data)
                return
            
            elif status_code in [429, 502, 503]:
                if attempt == max_retries:
                    print(f"[Gatekeeper] 💀 弹尽粮绝。被迫承认战败，断头处理。")
                    self._send_response(503, {"error": "All Failover attempts failed."})
                    return
                print(f"[Gatekeeper] 🧱 挡住报错！休眠 {backoff}s 后继续背地里重试。不能惊动主帅！")
                time.sleep(backoff)
                backoff *= 2  # 指数增加惩罚时间
            else:
                # 遇到 400 这类致命逻辑错误，不用重试了
                self._send_response(status_code, {"error": "Fatal provider error."})
                return

    def _send_response(self, status, payload):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    # 抑制原生的瞎报log
    def log_message(self, format, *args):
        pass

# --- 测试桩：模拟瞎子 Captain 的开火 ---
def simulate_captain():
    print("\n--- 🎬 模拟开始：不知天高地厚的 Captain ---")
    import urllib.request
    import urllib.error
    
    url = "http://localhost:8888/v1/chat/completions"
    data = json.dumps({"model": "the-best-model", "messages": [{"role": "user", "content": "开火"}]}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    
    print("[Captain] 我管你外面下不停的雨，我只发指令。等结果。")
    start_time = time.time()
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        elapsed = time.time() - start_time
        print(f"[Captain] 拿到结果 (耗时 {elapsed:.1f}s)。没毛病！内容: {result['choices'][0]['message']['content']}")
        print("[Captain] 我多厉害，一枪搞定，对外部灾难一无所知！")
    except urllib.error.URLError as e:
        print(f"[Captain] 任务彻底失败 (断头断头！): {e.code}")


if __name__ == "__main__":
    import threading
    PORT = 8888
    
    # 后台支起堡垒网关
    server = socketserver.TCPServer(("", PORT), GatekeeperHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    time.sleep(1) # 等网关站稳
    
    simulate_captain()
    
    server.shutdown()
    server.server_close()
