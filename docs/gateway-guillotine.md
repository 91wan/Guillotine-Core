# 大动脉替换方案：Gatekeeper Proxy 堡垒网关 (The Guillotine Gateway)

## 🎯 核心痛点与目的
在原始的 OpenClaw v2026.3.8 中，大量的 `rate_limit` (429 限流)、`overload` (服务器过载) 以及 Socket 抖动，全部穿透进应用层或沙箱内部。为了处理这些垃圾状态，应用层写了成百上千行的“退避、重试、延时”补丁。这种将网络状态耦合进业务逻辑的做法是剧毒的。

本方案的目标是：**建立一个名为 Gatekeeper（守门人）的绝对强权网关。把针对第三方大模型（如 OpenAI、Anthropic）的网络层挣扎，100% 挡在沙箱之外。** 

## 🔪 架构定义与手术路径

### 1. The Zero-Tolerance API (沙箱出口视角的零容忍)
*   **硬约束**：队长 (Captain) 和黑盒沙箱发出的所有外部请求 (HTTP/RPC)，只准面对内部的 `Gatekeeper/Proxy` 地址。
*   **协议**：沙箱不配置设置任何 `Timeout` 或者 `Retry` 参数。沙箱眼中的响应只有两种：
    *   `200 OK` + `Content` (数据返回)
    *   `503 Service Unavailable` 或 Socket 断裂 (此路彻底不通，任务当场宣告断头)

### 2. 脏活收容所 (Gatekeeper 缓冲熔断池)
所有的挣扎必须下沉到网关进程。Gatekeeper 不是简单的透传（Pass-through），而是具备极强生存意志的盾牌。
*   **截流阻击 (429/Overload 降维)**：如果远端返回 `429` 或是 `500` 级别错误，Gatekeeper 绝不会立刻把这个错误捅给 Captain。它会在**网关侧**内部阻塞该请求，执行诸如指数退避（Exponential Backoff）等重试操作（例如上限重试 3 次，耗时 30 秒）。
*   **无缝备胎投递 (Failover 强行切换)**：如果在一次主链路请求彻底死亡后，Gatekeeper 将偷偷篡改 API Token 和 URL 结构，用“备用渠道（比如从 GPT 换到等价的 Claude，或从主节点换到备用节点）”悄悄重打该请求。
*   **对内说假话**：不管 Gatekeeper 内部有多么惊心动魄地重试和切流，只要它最终能拿回数据，它就必须以毫无波澜的姿态，返回一个干净的 HTTP 200 给 Captain。让 Captain 以为它的每一次开火都是百发百中。

### 3. 工程实施落点 (Milestones)

*   **Milestone 1**: 编写脱离原框架的独立 `Gatekeeper Proxy` 桩代码（优先使用轻量的异步转发引擎拦截，比如重写请求头，代理外部的 OpenAI 流量结构）。
*   **Milestone 2**: 实装“背着沙箱偷擦屁股”的内部重试列队机制（模拟 429 和 502 错误并实现无缝隐瞒捕捉）。
*   **Milestone 3**: 强行把沙箱里的原始网络发起端（例如 `fetch` 或者 Client）篡改为默认打向这个本地强权代理端口。

---
*“让炮兵觉得靶子永远在那里，哪怕我们背地里已经去给他换了三把枪。”*
