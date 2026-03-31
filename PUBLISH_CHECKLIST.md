# Self-Evolution 发布检查清单

## ✅ 已完成

- [x] 项目目录初始化 (`git init`)
- [x] pyproject.toml 配置
- [x] .gitignore
- [x] 核心包结构 (src/self_evolution/)
- [x] CLI 入口
- [x] 文档 (README.md, README_zh.md, CHANGELOG.md, CONTRIBUTING.md)
- [x] LICENSE
- [x] 测试文件
- [x] 本地安装测试 (`pip install -e .` ✅)
- [x] 导入测试 ✅
- [x] CLI 测试 (`self-evolution --version` ✅)
- [x] PyPI Token 获取 ✅
- [x] 记忆系统更新 ✅

## ⏳ 待执行

- [ ] Git 提交
- [ ] 创建 GitHub 远程仓库
- [ ] 推送代码到 GitHub
- [ ] 构建分发包 (`python -m build`)
- [ ] 上传到 PyPI (`twine upload dist/*`)
- [ ] 提交到 CoPaw 官方技能库

## 📋 执行命令

```bash
# 1. Git 提交
cd D:\github\self-evolution
git add .
git commit -m "feat: Initial release v1.0.0"

# 2. 创建 GitHub 仓库（网页或 gh CLI）
# https://github.com/new → 创建 lcq225/self-evolution

# 3. 推送代码
git remote add origin https://github.com/lcq225/self-evolution.git
git branch -M main
git push -u origin main

# 4. 构建分发包
pip install build twine
python -m build

# 5. 上传 PyPI
twine upload dist/*

# 6. 提交 CoPaw 官方
# 创建 PR 到 agentscope-ai/CoPaw
```

## 🔑 PyPI Token

位置：`D:\CoPaw\.copaw.secret\pypi.json`

---

**创建时间**: 2026-03-29 10:50
**状态**: 准备发布
