#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动优化建议执行器

功能：
1. 读取会话启动检查报告
2. 自动执行低风险、已验证的优化建议
3. 高风险操作需要用户确认
4. 生成执行报告

触发时机：会话启动检查后自动调用

版本：v1.0
日期：2026-03-29
"""

import sys
import io
# 修复 Windows GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

# 配置
OUTPUT_DIR = r"D:\CoPaw\OB-CoPaw\报告"
VERIFIED_OPS_FILE = r"D:\CoPaw\.copaw\workspaces\default\active_skills\self_evolution\verified_operations.json"
BACKUP_DIR = r"D:\CoPaw\.copaw\workspaces\default\backup"


def load_verified_operations():
    """加载已验证的操作记录"""
    if os.path.exists(VERIFIED_OPS_FILE):
        with open(VERIFIED_OPS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'verified': [],
        'pending': [],
        'rejected': []
    }


def save_verified_operations(ops):
    """保存已验证的操作记录"""
    with open(VERIFIED_OPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(ops, f, ensure_ascii=False, indent=2)


def get_risk_level(operation_type):
    """根据操作类型判断风险级别"""
    low_risk = ['add_documentation', 'add_example', 'general', 'cleanup_temp']
    medium_risk = ['modify_description', 'modify_config', 'optimize_file']
    high_risk = ['modify_file', 'delete_file', 'external_send']
    
    if operation_type in low_risk:
        return 'low'
    elif operation_type in medium_risk:
        return 'medium'
    else:
        return 'high'


def execute_optimization(suggestion, verified_ops):
    """执行单个优化建议"""
    op_type = suggestion.get('type', 'general')
    risk_level = get_risk_level(op_type)
    
    print(f"\n{'='*60}")
    print(f"执行优化建议：{suggestion.get('title', '未命名')}")
    print(f"{'='*60}")
    print(f"风险级别：{risk_level.upper()}")
    print(f"操作类型：{op_type}")
    print(f"描述：{suggestion.get('description', '')}")
    
    # 检查是否已验证
    is_verified = suggestion.get('id') in verified_ops.get('verified', [])
    
    if risk_level == 'high' and not is_verified:
        print("⚠️  高风险操作，需要用户确认")
        print("跳过自动执行，等待用户确认")
        verified_ops['pending'].append(suggestion.get('id', 'unknown'))
        return 'pending'
    
    if risk_level == 'medium' and not is_verified:
        print("⚠️  中风险操作，需要用户确认")
        print("跳过自动执行，等待用户确认")
        verified_ops['pending'].append(suggestion.get('id', 'unknown'))
        return 'pending'
    
    # 执行操作
    try:
        action = suggestion.get('action', '')
        
        if action == 'run_script':
            script_path = suggestion.get('script_path', '')
            if os.path.exists(script_path):
                print(f"✅ 执行脚本：{script_path}")
                os.system(f'python "{script_path}"')
                return 'success'
            else:
                print(f"❌ 脚本不存在：{script_path}")
                return 'failed'
        
        elif action == 'backup_file':
            file_path = suggestion.get('file_path', '')
            if os.path.exists(file_path):
                backup_path = Path(BACKUP_DIR) / f"{Path(file_path).name}.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(file_path, backup_path)
                print(f"✅ 已备份：{backup_path}")
                return 'success'
            else:
                print(f"❌ 文件不存在：{file_path}")
                return 'failed'
        
        elif action == 'cleanup_temp':
            temp_dirs = [
                r"D:\CoPaw\.copaw\workspaces\default\tool_result",
                r"D:\CoPaw\.copaw\workspaces\default\temp"
            ]
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                        except Exception as e:
                            print(f"⚠️  清理失败：{file_path} - {e}")
            print("✅ 临时文件清理完成")
            return 'success'
        
        else:
            print(f"⚠️  未知操作类型：{action}")
            return 'skipped'
    
    except Exception as e:
        print(f"❌ 执行失败：{e}")
        return 'failed'


def run_auto_optimization():
    """运行自动优化"""
    print("=" * 60)
    print("🚀 自动优化建议执行器")
    print("=" * 60)
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 加载已验证操作
    verified_ops = load_verified_operations()
    
    # 模拟优化建议（实际应从会话启动检查报告读取）
    suggestions = [
        {
            'id': 'opt_001',
            'title': '清理临时文件',
            'description': '清理 tool_result/ 和 temp/ 目录下的临时文件',
            'type': 'cleanup_temp',
            'action': 'cleanup_temp',
            'risk': 'low'
        },
        {
            'id': 'opt_002',
            'title': '备份 AGENTS.md',
            'description': '在优化前备份 AGENTS.md',
            'type': 'backup_file',
            'action': 'backup_file',
            'file_path': r"D:\CoPaw\.copaw\workspaces\default\AGENTS.md",
            'risk': 'low'
        }
    ]
    
    # 执行优化
    results = {
        'success': 0,
        'pending': 0,
        'failed': 0,
        'skipped': 0
    }
    
    for suggestion in suggestions:
        result = execute_optimization(suggestion, verified_ops)
        results[result] = results.get(result, 0) + 1
    
    # 保存已验证操作
    save_verified_operations(verified_ops)
    
    # 生成报告
    print("\n" + "=" * 60)
    print("📊 执行报告")
    print("=" * 60)
    print(f"✅ 成功：{results['success']}")
    print(f"⏳ 待确认：{results['pending']}")
    print(f"❌ 失败：{results['failed']}")
    print(f"⚠️  跳过：{results['skipped']}")
    
    # 保存报告
    report_path = Path(OUTPUT_DIR) / f"{datetime.now().strftime('%Y-%m-%d')}_自动优化执行报告.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 自动优化执行报告\n\n")
        f.write(f"**时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 执行结果\n\n")
        f.write(f"| 状态 | 数量 |\n")
        f.write(f"|------|------|\n")
        f.write(f"| ✅ 成功 | {results['success']} |\n")
        f.write(f"| ⏳ 待确认 | {results['pending']} |\n")
        f.write(f"| ❌ 失败 | {results['failed']} |\n")
        f.write(f"| ⚠️  跳过 | {results['skipped']} |\n")
    
    print(f"\n📄 报告已保存：{report_path}")
    
    return results


if __name__ == '__main__':
    run_auto_optimization()
