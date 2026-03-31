#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话启动检查脚本

功能：
1. 检查 AGENTS.md/MEMORY.md 大小是否超过阈值
2. 检查是否有待处理的进化项
3. 检查记忆数据库健康
4. 生成优化建议（如需要）

触发时机：每次会话启动时自动执行

版本：v1.0
日期：2026-03-29
"""

import sys
import io
# 修复 Windows GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import sqlite3
import os
from pathlib import Path
from datetime import datetime, timedelta

# 配置
DB_PATH = r"D:\CoPaw\.copaw\.agent-memory\memory.db"
AGENTS_MD = r"D:\CoPaw\.copaw\workspaces\default\AGENTS.md"
MEMORY_MD = r"D:\CoPaw\.copaw\workspaces\default\MEMORY.md"
OUTPUT_DIR = r"D:\CoPaw\OB-CoPaw\报告"

# 阈值配置
AGENTS_MD_MAX_LINES = 500
MEMORY_MD_MAX_LINES = 500
PENDING_DAYS_THRESHOLD = 7


def count_lines(file_path):
    """统计文件行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except Exception as e:
        return -1


def check_file_size():
    """检查 AGENTS.md/MEMORY.md 大小"""
    print("=" * 60)
    print("📊 检查文件大小")
    print("=" * 60)
    
    issues = []
    
    # 检查 AGENTS.md
    agents_lines = count_lines(AGENTS_MD)
    status = "✅" if agents_lines <= AGENTS_MD_MAX_LINES else "❌"
    print(f"{status} AGENTS.md: {agents_lines} 行（阈值：{AGENTS_MD_MAX_LINES}）")
    
    if agents_lines > AGENTS_MD_MAX_LINES:
        issues.append({
            'file': 'AGENTS.md',
            'lines': agents_lines,
            'threshold': AGENTS_MD_MAX_LINES,
            'excess': agents_lines - AGENTS_MD_MAX_LINES
        })
    
    # 检查 MEMORY.md
    memory_lines = count_lines(MEMORY_MD)
    status = "✅" if memory_lines <= MEMORY_MD_MAX_LINES else "❌"
    print(f"{status} MEMORY.md: {memory_lines} 行（阈值：{MEMORY_MD_MAX_LINES}）")
    
    if memory_lines > MEMORY_MD_MAX_LINES:
        issues.append({
            'file': 'MEMORY.md',
            'lines': memory_lines,
            'threshold': MEMORY_MD_MAX_LINES,
            'excess': memory_lines - MEMORY_MD_MAX_LINES
        })
    
    return issues


def check_pending_evolution():
    """检查是否有待处理的进化项"""
    print("\n" + "=" * 60)
    print("🧬 检查待处理进化项")
    print("=" * 60)
    
    issues = []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查未归因的经验（超过 7 天）- 使用 outcome 字段
        cursor.execute('''
            SELECT id, action, insight, created_at
            FROM experiences
            WHERE outcome = 'negative'
            AND created_at < datetime('now', '-7 days')
            ORDER BY created_at DESC
        ''')
        unanalyzed = cursor.fetchall()
        
        if unanalyzed:
            print(f"⚠️  发现 {len(unanalyzed)} 条负面经验（超过 7 天）")
            for exp in unanalyzed[:3]:
                print(f"   • {exp[1][:50]}...")
            issues.append({
                'type': 'unanalyzed_experiences',
                'count': len(unanalyzed),
                'items': unanalyzed[:5]
            })
        else:
            print("✅ 无超期负面经验")
        
        # 检查高重要性教训
        cursor.execute('''
            SELECT id, action, insight, importance, created_at
            FROM experiences
            WHERE outcome = 'negative'
            AND importance >= 0.9
            ORDER BY created_at DESC
        ''')
        high_priority = cursor.fetchall()
        
        if high_priority:
            print(f"⚠️  发现 {len(high_priority)} 条高重要性教训")
            for exp in high_priority[:3]:
                print(f"   • [重要性：{exp[3]}] {exp[1][:50]}...")
            issues.append({
                'type': 'high_priority_unconsolidated',
                'count': len(high_priority),
                'items': high_priority[:5]
            })
        else:
            print("✅ 无高重要性教训")
        
        # 检查重复错误
        cursor.execute('''
            SELECT action, COUNT(*) as count
            FROM experiences
            WHERE outcome = 'negative'
            GROUP BY action
            HAVING count >= 3
            ORDER BY count DESC
        ''')
        repeat_errors = cursor.fetchall()
        
        if repeat_errors:
            print(f"⚠️  发现 {len(repeat_errors)} 个重复错误（≥3 次）")
            for err in repeat_errors[:3]:
                print(f"   • {err[0][:50]}... ({err[1]}次)")
            issues.append({
                'type': 'repeat_errors',
                'count': len(repeat_errors),
                'items': repeat_errors[:5]
            })
        else:
            print("✅ 无重复错误")
        
        conn.close()
    
    except Exception as e:
        print(f"❌ 检查失败：{e}")
        import traceback
        traceback.print_exc()
        issues.append({
            'type': 'check_error',
            'error': str(e)
        })
    
    return issues


def check_memory_health():
    """检查记忆数据库健康"""
    print("\n" + "=" * 60)
    print("🧠 检查记忆数据库健康")
    print("=" * 60)
    
    try:
        # 简单检查数据库是否可访问
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if 'experiences' in tables and 'facts' in tables:
            print("✅ 记忆数据库表结构正常")
            
            # 检查记录数
            cursor.execute("SELECT COUNT(*) FROM experiences")
            exp_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM facts")
            fact_count = cursor.fetchone()[0]
            
            print(f"   记录数：{exp_count} 经验 + {fact_count} 事实")
            print("✅ 记忆数据库健康")
            conn.close()
            return []
        else:
            print("⚠️  记忆数据库表结构异常")
            conn.close()
            return [{
                'type': 'memory_health',
                'status': 'warning',
                'message': '缺少核心表'
            }]
    
    except Exception as e:
        print(f"⚠️  无法检查记忆数据库：{e}")
        return [{
            'type': 'memory_check_error',
            'error': str(e)
        }]


def check_tool_result_cleanup():
    """检查临时文件是否需要清理"""
    print("\n" + "=" * 60)
    print("🧹 检查临时文件清理")
    print("=" * 60)
    
    issues = []
    
    # 检查 tool_result 目录
    tool_result_dir = Path(r"D:\CoPaw\.copaw\workspaces\default\tool_result")
    if tool_result_dir.exists():
        files = list(tool_result_dir.glob("*"))
        if len(files) > 10:
            print(f"⚠️  tool_result/ 目录有 {len(files)} 个文件，建议清理")
            issues.append({
                'type': 'tool_result_cleanup',
                'count': len(files),
                'path': str(tool_result_dir)
            })
        else:
            print("✅ tool_result/ 目录整洁")
    
    # 检查 temp 目录
    temp_dir = Path(r"D:\CoPaw\.copaw\temp")
    if temp_dir.exists():
        files = list(temp_dir.glob("*"))
        if len(files) > 0:
            print(f"⚠️  .copaw/temp/ 目录有 {len(files)} 个临时文件，建议清理")
            issues.append({
                'type': 'temp_cleanup',
                'count': len(files),
                'path': str(temp_dir)
            })
        else:
            print("✅ .copaw/temp/ 目录已清理")
    
    return issues


def generate_optimization_suggestions(file_issues, evolution_issues):
    """生成优化建议"""
    print("\n" + "=" * 60)
    print("💡 生成优化建议")
    print("=" * 60)
    
    suggestions = []
    
    # 文件过大建议
    for issue in file_issues:
        if issue['file'] == 'AGENTS.md':
            suggestions.append({
                'type': 'optimize_agents_md',
                'priority': 'high',
                'title': 'AGENTS.md 过大，建议优化',
                'description': f"当前 {issue['lines']} 行，超过阈值 {issue['threshold']} 行",
                'action': '运行 scripts/optimize_agents_md.py',
                'risk': 'low',
                'verified': True  # 已验证过的操作
            })
        elif issue['file'] == 'MEMORY.md':
            suggestions.append({
                'type': 'optimize_memory_md',
                'priority': 'high',
                'title': 'MEMORY.md 过大，建议优化',
                'description': f"当前 {issue['lines']} 行，超过阈值 {issue['threshold']} 行",
                'action': '运行 scripts/optimize_memory_v2.py',
                'risk': 'low',
                'verified': True
            })
    
    # 进化项处理建议
    for issue in evolution_issues:
        if issue['type'] == 'unanalyzed_experiences':
            suggestions.append({
                'type': 'analyze_experiences',
                'priority': 'medium',
                'title': f"{issue['count']} 条负面经验待归因",
                'description': '使用 AI 辅助归因分析',
                'action': '运行 active_skills/self_evolution/ai_attributor.py',
                'risk': 'low',
                'verified': False
            })
        elif issue['type'] == 'high_priority_unconsolidated':
            suggestions.append({
                'type': 'consolidate_lessons',
                'priority': 'high',
                'title': f"{issue['count']} 条高重要性教训待固化",
                'description': '固化到 AGENTS.md/MEMORY.md 或创建技能',
                'action': '运行 active_skills/self_evolution/auto_consolidator.py',
                'risk': 'medium',
                'verified': False
            })
        elif issue['type'] == 'repeat_errors':
            suggestions.append({
                'type': 'fix_repeat_errors',
                'priority': 'high',
                'title': f"{issue['count']} 个重复错误需要解决",
                'description': '分析根因并制定改进措施',
                'action': '运行 active_skills/self_evolution/pattern_detector.py',
                'risk': 'medium',
                'verified': False
            })
    
    if not suggestions:
        print("✅ 无需优化建议")
    else:
        for i, sug in enumerate(suggestions, 1):
            priority_icon = "🔴" if sug['priority'] == 'high' else "🟡"
            print(f"{priority_icon} 建议{i}: {sug['title']}")
            print(f"   描述：{sug['description']}")
            print(f"   操作：{sug['action']}")
            print()
    
    return suggestions


def save_report(file_issues, evolution_issues, suggestions):
    """保存检查报告"""
    try:
        OUTPUT_DIR_path = Path(OUTPUT_DIR)
        OUTPUT_DIR_path.mkdir(parents=True, exist_ok=True)
        
        today = datetime.now().strftime("%Y-%m-%d")
        report_path = OUTPUT_DIR_path / f"{today}_会话启动检查.md"
        
        content = f"""# 📊 会话启动检查报告

**生成时间：** {datetime.now().isoformat()}

## 📊 文件大小检查

"""
        
        for issue in file_issues:
            content += f"- ❌ {issue['file']}: {issue['lines']} 行（阈值：{issue['threshold']}）\n"
        
        if not file_issues:
            content += "- ✅ 所有文件大小正常\n"
        
        content += "\n## 🧬 进化项检查\n\n"
        for issue in evolution_issues:
            if issue['type'] == 'unanalyzed_experiences':
                content += f"- ⚠️  {issue['count']} 条未归因的负面经验\n"
            elif issue['type'] == 'high_priority_unconsolidated':
                content += f"- ⚠️  {issue['count']} 条高重要性未固化的教训\n"
            elif issue['type'] == 'repeat_errors':
                content += f"- ⚠️  {issue['count']} 个重复错误\n"
        
        if not evolution_issues:
            content += "- ✅ 无待处理进化项\n"
        
        content += "\n## 💡 优化建议\n\n"
        for i, sug in enumerate(suggestions, 1):
            content += f"{i}. **{sug['title']}**\n"
            content += f"   - 操作：{sug['action']}\n"
            content += f"   - 风险：{'低' if sug['risk'] == 'low' else '中'}\n"
            content += f"   - 已验证：{'是' if sug.get('verified') else '否'}\n\n"
        
        if not suggestions:
            content += "无需优化建议\n"
        
        report_path.write_text(content, encoding='utf-8')
        print(f"\n📄 报告已保存：{report_path}")
    
    except Exception as e:
        print(f"\n⚠️  保存报告失败：{e}")


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 会话启动检查")
    print("=" * 60)
    print(f"时间：{datetime.now().isoformat()}")
    print("=" * 60)
    
    # 1. 检查文件大小
    file_issues = check_file_size()
    
    # 2. 检查待处理进化项
    evolution_issues = check_pending_evolution()
    
    # 3. 检查记忆数据库健康
    memory_issues = check_memory_health()
    evolution_issues.extend(memory_issues)
    
    # 4. 检查临时文件清理
    cleanup_issues = check_tool_result_cleanup()
    evolution_issues.extend(cleanup_issues)
    
    # 5. 生成优化建议
    suggestions = generate_optimization_suggestions(file_issues, evolution_issues)
    
    # 6. 保存报告
    save_report(file_issues, evolution_issues, suggestions)
    
    # 7. 总结
    print("\n" + "=" * 60)
    print("✅ 检查完成")
    print("=" * 60)
    
    total_issues = len(file_issues) + len(evolution_issues)
    if total_issues == 0:
        print("🎉 一切正常，无需优化")
    else:
        print(f"⚠️  发现 {total_issues} 个问题")
        print(f"💡 生成 {len(suggestions)} 条优化建议")
        print("\n📋 建议执行顺序:")
        for i, sug in enumerate(suggestions, 1):
            priority = "优先" if sug['priority'] == 'high' else "稍后"
            print(f"   {i}. [{priority}] {sug['title']}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
