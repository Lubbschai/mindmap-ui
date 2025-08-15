#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例 - AI思维导图生成器

这个文件展示了如何使用思维导图生成器的不同模式
"""

def show_usage_examples():
    """显示使用示例"""
    examples = [
        {
            "mode": "GUI模式",
            "command": "python mindmap_generator.py",
            "description": "启动完整的图形界面，需要OpenAI API密钥"
        },
        {
            "mode": "演示模式", 
            "command": "python demo.py",
            "description": "启动演示版本，无需API密钥，可测试界面功能"
        }
    ]
    
    print("AI思维导图生成器 - 使用示例")
    print("=" * 50)
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['mode']}")
        print(f"   命令: {example['command']}")
        print(f"   说明: {example['description']}")
    
    print(f"\n配置要求:")
    print("   - Python 3.7+")
    print("   - 安装依赖: pip install -r requirements.txt")
    print("   - GUI模式需要OpenAI API密钥")
    
    print(f"\n生成的文件格式:")
    print("   - 文件扩展名: .mmd")
    print("   - 格式: Mermaid mindmap语法")
    print("   - 可在GitHub、Mermaid Live Editor等平台渲染")

if __name__ == "__main__":
    show_usage_examples()