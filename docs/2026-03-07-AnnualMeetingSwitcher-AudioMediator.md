# 🎯 战区 Alpha：「帝都餐饮导播台」—— BGMVisualizerPanel 与 Mediator 接入与压测

## 1. 架构级接入：建立 AudioVUMediator
大刘极客红线要求：
- **拒绝直接访问**：严禁 `View` 模块接触 `AVAudioEngine` / `AVAudioPlayer`。
- **职责分配**：建立 `AudioVUMediator`（核心状态观察与换算器）。
- **流程**：`Mediator` 负责接收引擎分贝，执行归一化（0.0~1.0），然后通过 `@Published` 投喂给没有任何音频依赖的纯渲染组件 `BGMVisualizerPanel`。

## 2. 性能遥测与压测 (The "Torture" Test)
@coder 必须在将组件接入实际预览环境时执行：
- 启动 60FPS 满载界面环境下的高频刷新。
- 确保这根 0.05s (50ms) 频繁刷新的光柱与 Mask **绝不占用主线程超过 15% 的 CPU 资源**。（如占用过高，通过 `.drawingGroup()` 压平图层）。

## 3. “弹匣热插拔”验证 (Hot-Swap Validation)
- 从 `ShadowEnv.json` 热读取 `tick_interval_ms`，`peak_decay_db_per_frame` 与 `peak_hold_seconds`！
- **不准硬编码**：验证修改 JSON 即可改变光柱回落物理特效。如发现偷偷写死了 `0.05` 或衰减速度，立刻启动 V8 宪法追责！

## 交付
完成 `AudioVUMediator.swift` 和 UI 并轨，执行一次合规提交：包含 `Lesson-Learned: SwiftUI 高频渲染下的 Mask 性能优化，通过 drawingGroup 解决 CPU 热点，并通过 ShadowEnv 实现热插拔验证`。
