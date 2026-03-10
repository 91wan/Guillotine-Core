# 🎯 战区 Alpha：「DituLiveSwitcher」重构与修复查杀

## 目标与背景
大刘指令：全面检查并修复 `DituLiveSwitcher` 项目中的 Bug，并将其编译成一个干净、可交付的 macOS `.app` 实体，最终空投进大刘的 `/Users/liuchangxi/Downloads` 文件夹中。

## 战术动作拆解 (委派给 Coder)

### 第一阶段：编译与 Bug 扫描 (Compile & Audit)
1. **诊断工程结构**：进入 `DituLiveSwitcher/`。检查 `Package.swift`，或查看是否存在 `.xcodeproj`。这是一套基于 SPM/终端脚本构建的项目。
2. **执行试编译**：运行底下的 `PageTurnerInterceptor_build.sh` 或 `build.sh`。捕捉任何 Swift 语法报错、架构废弃 API，以及我们 V8 宪法明令禁止的写法（特别留意多线程安全和单例问题）。
3. **修复动作**：手起刀落修改它。如果出现依赖循环或主线程卡顿代码，直接按 V8 极客标准执行局部重写。

### 第二阶段：构建发行实体 (Release Build & Sandbox Delivery)
1. **构建 Release App**：使用 `swift build -c release` 或现有的打包脚本，导出一个完整的 `[AppName].app` 包（而非单纯命令行二进制文件）。如果工程没有完整的 App 打包脚本，手搓一个标准 `mkdir -p` -> `cp` 到 `.app/Contents/MacOS` 及资源配置体系的小脚手架。
2. **物理空投**：编译完成后，执行将最终可用的 `DituLiveSwitcher.app`（或其正确命名的应用包）强行挂载拷贝到 `/Users/liuchangxi/Downloads/` 下。

### 第三阶段：静默提交
完成修改后，针对 `DituLiveSwitcher` 内执行一个以 `fix: ` 开头的提交。返回并报告。
