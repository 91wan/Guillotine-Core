# 🎯 战区 Alpha：「真空沙盒 (Vacuum Sandbox)」压测协议

**架构师最高性能指令**：
1. **纯净目标**：为 `BGMVisualizerPanel.swift` 建立绝对独立的 SwiftUI Preview 沙盒。
2. **零依赖存活 (Zero Dependency)**：该 View 仅由 `(leftLevel: Float, rightLevel: Float)` 驱动，严禁引入任何业务层逻辑或真实音频组件。
3. **极限高频模拟器 (The 50ms Mock Engine)**：在文件底部包含一个 `MockVUEngine`，使用 `Timer.publish(every: 0.05, on: .main, in: .common).autoconnect()` 生成极其狂暴的伪数据（模拟真实音频动态范围）。
4. **性能验证**：必须确保绿、黄、红（-60到0 dBFS）三段渐变、动态遮罩，在 50ms 级别频率下 60FPS 顺滑刷新无撕裂性能问题。
5. **提交要求**：这是独立测试组件，完成组件代码并测试验证后，以此为内容创建独立的 `BGMVisualizerSandbox.swift` 以备架构师性能宣判，并执行标准 `feat(switcher):` 提交。
