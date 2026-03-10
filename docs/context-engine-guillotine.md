# Context Engine 物理剥离计划 (The Guillotine Context Extraction)

## 🎯 总目标
实施“断头台架构”的第一刀：斩断 Captain (核心路由) 的记忆神经。将所有的上下文堆叠、合并、截断逻辑从主循环中连根拔除，交给一个完全独立的、物理隔离的 Context Engine 负责。Captain 每次启动 Task，拿到的都是唯一且清洗过的“当前切片 (Prompt Snapshot)”。

## 🔪 阶段架构拆解

### Milestone 1: 定义 Context Engine 独立协议边境 
**目标**：建立 Captain 与未来独立 Context Engine 之间的纯粹数据契约，彻底阻断状态渗透。
*   **职责重申**：
    *   **Captain**：只通过入参获取 `Instruction`，通过出参拿到 `Clean_Result`，中间不再持有、也不再读写任何类似于 `conversation_history` 或是 `memory_stack` 的对象。
    *   **Context Engine**：作为底层服务挂载，对外暴露极简的 API（例如：`GetCleanSnapshot(SessionID) -> String` 和 `FlushResult(SessionID, Result)`）。
*   **输出交付**：一份名为 `Context_Boundary_Protocol.md` 的接口与数据结构定义文件。

### Milestone 2: 现存主循环大清洗 (The Purge)
**目标**：把现存系统中所有与记忆相关的脏代码全部扫地出门，准备硬对接。
*   **动作核心**：
    *   搜寻并铲除 Captain 调度主轴上的一切历史包袱状态（包含但不限于数组 `push/pop` 历史对话的操作）。
    *   废弃并在核心层面禁用所有依赖于在单一实例内存里保留长期记忆的中间件。
*   **验收标准**：核心主轴变得完全无法记忆上下文（即所谓的“致盲期”阵痛）。

### Milestone 3: 独立 Context Engine 服务实体化 (The Standalone Core)
**目标**：真正把第一阶段定义的协议实体化，构建这台独立的记忆处理器。
*   **机制核心**：
    *   构建无声的后台进程或独立组件，专门处理数据的合并与压缩。
    *   所有的压缩策略（例如超长文本脱水、关键事件提取）都在这个黑盒内以子沙盒、或者降级模型的形式静默运行，绝不惊动 Captain。
*   **验收标准**：通过本地测试，Captain 能依靠“拿来主义”获取切片并执行完单次任务，没有任何越权感知。

## ⚠️ 开发约束
严格隔离。由于这将导致核心发生大出血般的结构震荡，必须要起一个专用的 Feature 分支（建议命名为 `feature/guillotine-context-engine`），只有当 Milestone 3 测试完全通过后，才允许向主轴合并。
