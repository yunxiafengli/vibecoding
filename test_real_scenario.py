"""
真实场景测试：创建文件夹和文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_code import ClaudeCode

print("=" * 70)
print("测试：创建文件夹并生成文章内容")
print("=" * 70)

with ClaudeCode() as claude:
    print("\n创建任务...")
    result = claude.create_task(
        subagent_type="general-purpose",
        description="创建文件夹并写入文章",
        prompt="""
        请完成以下任务：
        
        1. 创建两个文件夹：ai_articles 和 ai_research
        2. 在 ai_articles 文件夹中创建一篇关于大模型发展现状的文章，文件名为 llm_overview.txt
        3. 文章内容应包括：GPT、Claude、Kimi等模型的介绍、技术趋势、应用场景、挑战和未来方向（约200-300字）
        4. 验证文件是否成功创建
        5. 读取并显示文件内容的前100字
        
        请自主决定使用哪些工具来完成这些任务，并确保每一步都成功执行。
        """
    )
    
    if result.success:
        task_id = result.data["task_id"]
        print(f"任务ID: {task_id}")
        
        print("\n等待任务完成（最多60秒）...")
        task_result = claude.wait_for_task(task_id, timeout=60)
        
        if task_result.success:
            print("\n✓ 任务完成！")
            data = task_result.data
            print(f"状态: {data['status']}")
            print(f"Agent: {data['agent_type']}")
            
            # 检查 llm_result
            llm_result = data['result']['data']['llm_result']
            print(f"\n工具调用次数: {llm_result.get('tool_calls', 0)}")
            
            if llm_result.get('tool_results'):
                for i, tr in enumerate(llm_result['tool_results'], 1):
                    print(f"\n工具调用 {i}:")
                    print(f"  成功: {tr['success']}")
                    if tr.get('data', {}).get('stdout'):
                        print(f"  输出: {tr['data']['stdout'][:100]}")
        else:
            print(f"\n✗ 任务失败: {task_result.data}")
    else:
        print(f"\n✗ 创建任务失败: {result.error}")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
