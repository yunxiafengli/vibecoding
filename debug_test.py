"""
Debug test for LLM tool calling
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_code import ClaudeCode

print("=" * 70)
print("调试测试：简单任务")
print("=" * 70)

with ClaudeCode() as claude:
    print("\n测试 1: 创建单个文件夹...")
    result = claude.create_task(
        subagent_type="general-purpose",
        description="创建测试文件夹",
        prompt="使用 bash_tool 创建一个名为 test_folder 的文件夹，然后告诉我是否成功"
    )
    
    task_id = result.data["task_id"]
    print(f"任务ID: {task_id}")
    
    task_result = claude.wait_for_task(task_id, timeout=30)
    
    print(f"\n任务状态: {task_result.data['status']}")
    print(f"工具调用次数: {task_result.data['result']['data']['llm_result'].get('tool_calls', 0)}")
    
    # 检查文件夹是否创建
    if os.path.exists("test_folder"):
        print("✓ test_folder 创建成功")
    else:
        print("✗ test_folder 未创建")
    
    print("\n" + "=" * 70)
    print("测试 2: 创建文件并写入内容...")
    print("=" * 70)
    
    result = claude.create_task(
        subagent_type="general-purpose",
        description="创建并写入文件",
        prompt="使用 file_tool 创建一个名为 debug_test.txt 的文件，并写入内容 'Hello from LLM'"
    )
    
    task_id = result.data["task_id"]
    print(f"任务ID: {task_id}")
    
    task_result = claude.wait_for_task(task_id, timeout=30)
    
    print(f"\n任务状态: {task_result.data['status']}")
    llm_result = task_result.data['result']['data']['llm_result']
    print(f"工具调用次数: {llm_result.get('tool_calls', 0)}")
    
    if llm_result.get('tool_results'):
        for i, tr in enumerate(llm_result['tool_results'], 1):
            print(f"\n工具调用 {i}:")
            print(f"  成功: {tr['success']}")
            print(f"  数据: {tr.get('data', {})}")
    
    # 检查文件是否创建
    if os.path.exists("debug_test.txt"):
        print("✓ debug_test.txt 创建成功")
        with open("debug_test.txt", 'r') as f:
            print(f"  内容: {f.read()}")
    else:
        print("✗ debug_test.txt 未创建")

print("\n" + "=" * 70)
print("调试完成")
print("=" * 70)
