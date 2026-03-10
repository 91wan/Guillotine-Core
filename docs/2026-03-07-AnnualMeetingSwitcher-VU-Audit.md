# 🎯 战区 Alpha：「帝都餐饮导播台」—— BGMVisualizerPanel 极限审判

## 1. 静态代码复核 (Static Review - V8 绝缘性检查)
本阶段已由大刘与 Captain 代为执行并强力纠偏。
当前 `BGMVisualizerPanel.swift` 已严格遵守 V8.1「全局状态物理隔离」与 V8.3「弹匣式热更新」协议。
- ❌ 无 `static var shared`
- ❌ 无 `AVFoundation` 依赖
- ✅ 纯响应式渲染组件，完全由 `leftLevelFraction`、`rightLevelFraction` 等参数注入驱动。

## 2. 视觉与性能遥测要求 (Visual & Metric Review - 50ms 极限测试)
委派给 @coder 的核心最终任务：在这个已物理隔离完毕的 `BGMVisualizerPanel` 基础上，**将其并入导播台主工作区 (AnnualMeetingSwitcher) 对应的视图容器中，并挂载一个在主工程内部测试用的 Mock 引擎容器**。
- **物理惯性与呼吸感**：验证由 `ShadowEnv.json` 提供常量的 `peakHoldSeconds` 与 `decayPerFrame` 带来的引力滑落感。
- **60FPS 满帧承诺**：必须在主线程 50ms (0.05s) 刷新率下极致润滑，严禁生硬掉帧 (Jitter) 或过度渲染问题。若发生 CPU 超载，需使用 `drawingGroup()` 或 Metal 等机制优化！
- **广电级渐变**：红、黄、绿三层颜色过渡必须完全符合专业电平表标准。

## 3. 合并申请与进化反哺 (Merge Proposal)
通过压力审判后：
1. 请 @coder 将这段性能优化与整合经验提炼。
2. 触发主战区标准 `feat(switcher):` 提交。
3. 必须在 Commit 消息末尾加入思考锚点：`Lesson-Learned: SwiftUI 高频渲染下的 Mask 性能优化，...` 以供架构史官在周末提纯防线！
