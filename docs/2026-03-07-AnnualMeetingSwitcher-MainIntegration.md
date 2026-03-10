# 🎯 战区 Alpha：「帝都餐饮导播台」—— 终极点火与全链路合围

## 1. 物理挂载 (The Attachment)
- **审查点**：在主控面板（现有 `ContentView.swift` 等价的主界面）中注入 Mediator。
- **极客红线**：严禁任何全局对象的获取！必须在入口处使用 `@StateObject private var vuMediator` 将其生命周期与主窗口死死绑定。一旦界面销毁，Mediator 立即执行物理断电。

## 2. 信号并轨 (Signal Sync)
- **审查点**：并轨纯净版 `BGMVisualizerPanel` 渲染组件。
- **极客红线**：调用必须保持极致简洁。接收 Mediator “洗白”好的 fraction 数据，并且外部或内部必须强制挂载 `.drawingGroup()` 进行 Metal 级硬件加速渲染（彻底把 CPU 占用压至个位数）。

## 交付
请特遣队 `@coder` 在你的沙盒/业务空间内，完成主面板（`ContentView.swift` 或同级别容器）对 `AudioVUMediator` 与 `BGMVisualizerPanel` 的“绝缘与并轨”。修改完毕后，执行最终的主线 `feat(switcher):` 提交。
