# Context Engine 边界协议 (The Guillotine Boundary)

## 0. 绝对法则 (The Absolute Law)
1. **中枢无状态**：Captain 进程内存中禁止出现 `history`、`messages_array`、`conversation` 等任何表示上下文堆叠的变量。
2. **拿来主义**：Captain 总是向 Context Engine 请求“当前应该知道什么”，而不是自己去翻笔记。
3. **阅后即焚**：跑完一次推理，当前上下文结构物理销毁。

## 1. 核心数据结构 (Data Structures)

### 1.1 唯一身份标识
```json
// Captain 唯一持有的随身信物
{
  "SessionID": "string (UUID)",
  "Intent": "string (原始用户指令或系统触发事件)"
}
```

### 1.2 引擎投喂切片 (Prompt Snapshot)
```json
// Context Engine 交给 Captain 的子弹，Captain 只管打出去
{
  "SystemDirectives": "string (极简的系统法典和能力限制)",
  "AssembledContext": "string (已经被引擎后台剥离、压缩、降维成纯文本的背景信息)",
  "CurrentTask": "string (当前需要立刻响应的指令)"
}
```

### 1.3 落地结算单 (Turn Receipt)
```json
// Captain 完事后把残骸扔回给引擎，然后自己去死
{
  "SessionID": "string",
  "ExecutedActions": ["string", "string"], // 动用了哪些武器
  "FinalOutput": "string (极简纯粹的结果，绝无 <think> 和调试信息)",
  "IsTerminal": boolean // 是否需要结束本剧集
}
```

## 2. API 边界契约 (The RPC/IPC Boundary)

系统间通过本地 IPC 或强隔离机制调用，绝不传引用，只传值。

*   **`rpc_call ContextEngine.AssembleSnapshot(SessionID, Intent) -> PromptSnapshot`**
    *   **职责**：Context Engine 在幕后（可能通过调用低阶模型去总结、检索向量库）拼装出这一刻的唯一真理。阻塞等待。
    *   **约束**：Captain 拿到这个 Snapshot 后直接生成大模型请求，不得擅自追加任何长文本。

*   **`rpc_call ContextEngine.CommitTurn(TurnReceipt) -> void`**
    *   **职责**：把这一轮的输出交接给引擎存盘。
    *   **约束**：发完这个请求，Captain 本地变量强制触发垃圾回收（GC / Flush）。

