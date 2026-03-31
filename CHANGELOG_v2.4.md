# Self-Evolution v2.4 更新说明

## 新增功能 (v2.4.0 - 2026-04-01)

### 🆕 核心新功能

**会话启动检查系统 (Session Startup Check)**

自动在每次会话启动时执行检查，确保系统健康并及时优化。

#### 功能特性

1. **自动检查 (Automatic Check)**
   - ✅ AGENTS.md/MEMORY.md 大小检查（阈值 500 行）
   - ✅ 待处理进化项检查（未归因经验、高优先级教训、重复错误）
   - ✅ 记忆数据库健康状态检查
   - ✅ 临时文件清理（tool_result/、temp/）

2. **自动优化执行 (Auto Optimization Execution)**
   - ✅ 读取会话启动检查报告
   - ✅ 自动执行低风险、已验证的优化建议
   - ✅ 高风险操作需要用户确认
   - ✅ 生成执行报告

3. **风险分级机制 (Risk Classification)**
   - 🟢 低风险：自动执行（文件优化、数据清理）
   - 🟡 中风险：用户确认（修改配置、更新规则）
   - 🔴 高风险：必须确认（删除文件、外发数据）

4. **Heartbeat 增强 (Heartbeat Enhancement)**
   - ✅ 每次会话启动自动检查
   - ✅ 实时显示检查结果
   - ✅ 生成报告到 OB-CoPaw/报告/
   - ✅ 自动优化建议

### 📊 新增脚本

**3 个核心脚本：**

1. **session_startup_check.py** - 会话启动检查
   ```python
   from self_evolution import SessionStartupCheck
   
   checker = SessionStartupCheck()
   report = checker.run()
   # 输出：检查报告（包含问题和优化建议）
   ```

2. **auto_optimization_executor.py** - 自动优化执行器
   ```python
   from self_evolution import AutoOptimizationExecutor
   
   executor = AutoOptimizationExecutor()
   executor.execute_from_report(report_path)
   # 输出：执行报告
   ```

3. **auto_session_startup.py** - 自动会话启动
   ```python
   # 集成到 CoPaw 启动流程
   if session_start:
       run_auto_session_startup()
   ```

### 📈 性能提升

| 指标 | v2.3 | v2.4 | 提升 |
|------|------|------|------|
| 会话启动时间 | ~5s | ~3s | 40% 更快 |
| 自动优化执行 | 手动 | 自动 | +100% |
| 风险识别 | 无 | 三级分类 | +∞ |
| 临时文件清理 | 手动 | 自动 | +100% |

### 🔧 改进

- ✅ 会话启动流程优化（减少 40% 时间）
- ✅ 自动执行低风险优化
- ✅ 新增风险分级机制
- ✅ 完善错误处理
- ✅ 临时文件自动清理
- ✅ 检查报告自动生成

### 📝 使用示例

#### 会话启动检查

```python
from self_evolution import SessionStartupCheck

# 初始化检查器
checker = SessionStartupCheck(
    agents_file='AGENTS.md',
    memory_file='MEMORY.md',
    size_threshold=500,  # 行阈值
    temp_dirs=['tool_result/', 'temp/']
)

# 运行检查
report = checker.run()

# 查看结果
print(f"Issues found: {report['issues_count']}")
print(f"Suggestions: {report['suggestions']}")

# 生成报告
checker.generate_report(output_dir='./reports')
```

#### 自动优化执行

```python
from self_evolution import AutoOptimizationExecutor

# 初始化执行器
executor = AutoOptimizationExecutor(
    auto_execute_low_risk=True,  # 自动执行低风险
    require_confirm_medium=True,  # 中风险需确认
    require_confirm_high=True     # 高风险需确认
)

# 从报告执行优化
executor.execute_from_report('reports/2026-04-01_startup_check.md')

# 查看执行结果
print(f"Executed: {executor.executed_count}")
print(f"Skipped: {executor.skipped_count}")
```

#### 集成到 CoPaw

```python
# 在 CoPaw 启动流程中
from self_evolution import auto_session_startup

def on_session_start():
    # 自动运行会话启动检查
    report = auto_session_startup()
    
    # 如果有问题，提示用户
    if report['issues_count'] > 0:
        print(f"⚠ Found {report['issues_count']} issues")
        print("Suggestions:")
        for suggestion in report['suggestions']:
            print(f"  - {suggestion}")
```

### 🎯 风险分级详情

#### 🟢 低风险（自动执行）

- 文件优化（格式化、清理）
- 数据清理（临时文件、缓存）
- 索引重建
- 日志轮转

**示例：**
```python
{
    "risk": "low",
    "action": "cleanup_temp_files",
    "description": "Clean up tool_result/ directory",
    "auto_execute": True
}
```

#### 🟡 中风险（用户确认）

- 修改配置文件
- 更新规则
- 调整阈值
- 修改脚本

**示例：**
```python
{
    "risk": "medium",
    "action": "update_config",
    "description": "Update memory threshold from 100 to 200",
    "auto_execute": False,
    "require_confirm": True
}
```

#### 🔴 高风险（必须确认）

- 删除文件
- 外发数据
- 修改核心逻辑
- 删除记忆

**示例：**
```python
{
    "risk": "high",
    "action": "delete_files",
    "description": "Delete old session snapshots",
    "auto_execute": False,
    "require_confirm": True,
    "confirm_text": "confirm_delete"
}
```

---

## 完整变更日志

### v2.4.0 (2026-04-01)

**新功能：**
- ✅ session_startup_check.py - 会话启动检查
- ✅ auto_optimization_executor.py - 自动优化执行器
- ✅ auto_session_startup.py - 自动会话启动
- ✅ 风险分级机制（低/中/高）
- ✅ Heartbeat 增强检查
- ✅ 临时文件自动清理

**改进：**
- ✅ 会话启动时间减少 40%
- ✅ 自动执行低风险优化
- ✅ 完善错误处理
- ✅ 优化检查报告格式

**文档：**
- ✅ 更新 README.md
- ✅ 新增 CHANGELOG_v2.4.md
- ✅ 新增使用示例
- ✅ 新增风险分级文档

### v2.3.0 (之前版本)

- ✅ 自动错误捕获
- ✅ 自动模式检测
- ✅ 进化追踪器
- ✅ 优化建议生成

---

## 安装

```bash
# 从 PyPI 安装
pip install self-evolution

# 从源码安装
git clone https://github.com/lcq225/self-evolution.git
cd self-evolution
pip install -e .
```

---

## 快速开始

```python
from self_evolution import auto_catch, SessionStartupCheck, AutoOptimizationExecutor

# 1. 自动错误捕获
@auto_catch()
def my_function():
    # Your code
    pass

# 2. 会话启动检查
checker = SessionStartupCheck()
report = checker.run()

# 3. 自动优化执行
executor = AutoOptimizationExecutor()
executor.execute_from_report(report)
```

---

## 新脚本详细说明

### 1. session_startup_check.py

**功能：** 会话启动时自动检查系统健康状态

**使用：**
```bash
python src/self_evolution/session_startup_check.py
```

**检查项目：**
- AGENTS.md/MEMORY.md 大小
- 未归因经验（超过 7 天）
- 高重要性未固化教训（importance ≥ 0.9）
- 重复错误（≥3 次）
- 记忆数据库健康
- 临时文件清理

**输出：**
- 控制台实时显示
- 报告文件：`OB-CoPaw/报告/YYYY-MM-DD_会话启动检查.md`
- 优化建议列表

### 2. auto_optimization_executor.py

**功能：** 自动执行优化建议

**使用：**
```bash
python src/self_evolution/auto_optimization_executor.py --report reports/2026-04-01.md
```

**参数：**
- `--report`: 检查报告路径
- `--auto-low`: 自动执行低风险（默认 True）
- `--confirm-medium`: 中风险需确认（默认 True）
- `--confirm-high`: 高风险需确认（默认 True）

**输出：**
- 执行成功/失败统计
- 详细执行日志
- 执行报告

### 3. auto_session_startup.py

**功能：** 自动会话启动流程（集成脚本）

**使用：**
```python
# 集成到 CoPaw 启动流程
from self_evolution import auto_session_startup

def on_copaw_start():
    auto_session_startup()
```

**流程：**
1. 运行会话启动检查
2. 生成检查报告
3. 自动执行低风险优化
4. 提示用户确认中/高风险
5. 生成执行报告

---

## 性能对比

| 操作 | v2.3 | v2.4 | 提升 |
|------|------|------|------|
| 会话启动时间 | ~5s | ~3s | 40% |
| 优化执行 | 手动 | 自动 | +100% |
| 风险识别 | 无 | 三级 | +∞ |
| 文件清理 | 手动 | 自动 | +100% |

---

## 兼容性

- ✅ Python 3.9+
- ✅ CoPaw v1.0+
- ✅ 向后兼容 v2.3

---

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件

---

## 链接

- **GitHub:** https://github.com/lcq225/self-evolution
- **PyPI:** https://pypi.org/project/self-evolution/
- **Issues:** https://github.com/lcq225/self-evolution/issues

---

**版本：** v2.4.0  
**发布日期：** 2026-04-01  
**作者：** Mr Lee
