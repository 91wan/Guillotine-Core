# 🎯 战区 Alpha：「帝都餐饮导播台」—— 视觉与并发的无菌重构

## 第一步：净化 (已完成)
隔离清道夫已清空一切残留垃圾，工作区目前处于绝对纯净。

## 第二步：开发 - 绝对 UI 物理隔离 (委派至 Coder)
**目标文件**： `Sources/AnnualMeetingSwitcher/Sources/AnnualMeetingSwitcher/Views/BGMVisualizerPanel.swift` (需新建或重写)。

**架构师最高指令**：
1. **专注单一职责**：在全绿的无菌室里，完成没有任何业务耦合、纯粹由状态 `@Binding` 或观察对象传入 `leftLevel: Float, rightLevel: Float` 驱动的 `BGMVisualizerPanel.swift`。
2. **性能隔离审查**：实现一个内置的 `MockVisualizerController`（假数据发生器），用 `Timer.publish(every: 0.05, on: .main, in: .common)` 的强开主线程锁生成 0.0-1.0 随机或正弦波假数据，**专门测试 UI 层的渲染开销与 50 毫秒高频刷新率**。
3. **视觉设计极致要求**：利用 SwiftUI 构建属于广电极客的“绿-黄-红”跨度渐变的双通道 VU（音量电平）表。必须如丝般顺滑。
4. **V7 宪法红线**：严禁触发或触碰 AVFoundation 与真实后台服务！严格分离渲染层。完成代码后，触发一次纯粹针对 UI 的标准的 `feat(switcher):` commit。
