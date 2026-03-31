#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话启动自动检查集成

功能：
1. 每次会话启动时自动运行检查
2. 发现问题立即汇报
3. 询问是否执行优化
4. 根据用户回答执行

触发时机：每次会话启动时自动执行（无需用户主动调用）

版本：v1.0
日期：2026-03-29
"""

import sys
import io
# 修复 Windows GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import subprocess
import json
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE_DIR = Path(r"D:\CoPaw\.copaw\workspaces\default")
OUTPUT_DIR = Path(r"D:\CoPaw\OB-CoPaw\报告")


def run_startup_check():
    """运行会话启动检查"""
    print("\n" + "=" * 60)
    print("🚀 会话启动自动检查")
    print("=" * 60)
    print(f"时间：{datetime.now().isoformat()}")
    print("=" * 60)
    
    try:
        # 运行检查脚本
        result = subprocess.run(
            [sys.executable, str(WORKSPACE_DIR / "active_skills" / "self_evolution" / "session_startup_check.py")],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # 显示输出
        print(result.stdout)
        if result.stderr:
            print("错误信息:", result.stderr)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print("❌ 检查超时（>60 秒）")
        return False
    except Exception as e:
        print(f"❌ 检查失败：{e}")
        return False


def parse_check_report():
    """解析检查报告"""
    try:
        # 获取最新报告
        reports = sorted(OUTPUT_DIR.glob("*_会话启动检查.md"))
        if not reports:
            return None
        
        latest_report = reports[-1]
        content = latest_report.read_text(encoding='utf-8')
        
        # 简单解析
        issues = []
        suggestions = []
        
        if '❌' in content or '⚠️' in content:
            issues.append("发现问题")
        
        if '💡 生成' in content:
            # 提取建议数量
            for line in content.split('\n'):
                if '💡 生成' in line and '条优化建议' in line:
                    suggestions.append(line.strip())
        
        return {
            'has_issues': len(issues) > 0,
            'issues': issues,
            'suggestions': suggestions,
            'report_path': latest_report
        }
    
    except Exception as e:
        return None


def ask_user_execute():
    """询问用户是否执行优化"""
    print("\n" + "=" * 60)
    print("💡 是否执行优化建议？")
    print("=" * 60)
    print("\n选项：")
    print("  y - 执行所有已验证的低风险优化（推荐）")
    print("  n - 跳过，稍后手动执行")
    print("  v - 查看报告详情")
    print()
    
    # 注意：实际对话中由用户直接回复消息
    # 这里只是展示选项
    return None  # 返回 None 表示等待用户回复


def execute_optimization():
    """执行优化建议"""
    print("\n" + "=" * 60)
    print("🤖 执行优化建议")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(WORKSPACE_DIR / "active_skills" / "self_evolution" / "auto_optimization_executor.py")],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:", result.stderr)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print("❌ 执行超时（>5 分钟）")
        return False
    except Exception as e:
        print(f"❌ 执行失败：{e}")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🧬 老 K 自我进化系统 v2.3")
    print("=" * 60)
    
    # 1. 运行检查
    check_success = run_startup_check()
    
    if not check_success:
        print("\n⚠️  会话启动检查失败，跳过自动优化")
        return 1
    
    # 2. 解析报告
    report = parse_check_report()
    
    if report and report['has_issues']:
        print("\n" + "=" * 60)
        print("📊 检查发现问题")
        print("=" * 60)
        
        for issue in report['issues']:
            print(f"  • {issue}")
        
        for suggestion in report['suggestions']:
            print(f"  💡 {suggestion}")
        
        print("\n" + "=" * 60)
        print("💡 优化建议已生成，等待老 K 在聊天中汇报")
        print("=" * 60)
        print("\n📄 报告已保存，老 K 会读取并在聊天中询问 Mr Lee")
        print("⚠️  不要在命令行等待，退出让老 K 处理")
        
        return 0  # 返回 0 表示检查完成，等待聊天交互
    
    else:
        print("\n" + "=" * 60)
        print("✅ 一切正常，无需优化")
        print("=" * 60)
        return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 异常：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
