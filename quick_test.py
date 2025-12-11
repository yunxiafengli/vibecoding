"""
快速测试 Claude Code Python - 复制并修改这个文件来测试不同场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_code import ClaudeCode


def quick_test():
    """快速测试 LLM 集成"""
    print("🚀 开始测试 Claude Code Python\n")
    
    with ClaudeCode() as claude:
        print("1. 测试 PlanAgent（生成计划）...")
        result = claude.create_task(
            subagent_type="plan-agent",
            description="计划待办事项应用",
            prompt="我想开发一个简单的待办事项（Todo）应用，使用 Python 和 SQLite，请帮我制定一个实现计划"
        )
        
        if result.success:
            task_id = result.data["task_id"]
            print(f"   ✓ 任务已创建: {task_id}")
            
            # 等待完成
            print("\n2. 等待 LLM 生成计划...")
            task_result = claude.wait_for_task(task_id, timeout=60)
            
            if task_result.success and task_result.data["status"] == "completed":
                plan = task_result.data["result"]["data"]["plan"]
                print("   ✓ 计划生成完成！\n")
                print("=" * 70)
                print("生成的计划：")
                print("=" * 70)
                print(plan[:800])  # 显示前800字符
                print("\n" + "=" * 70)
                print("✅ 测试成功！LLM 集成正常工作")
                return True
            else:
                print(f"   ✗ 任务失败: {task_result.data.get('error', '未知错误')}")
                return False
        else:
            print(f"   ✗ 创建任务失败: {result.error}")
            return False


if __name__ == "__main__":
    try:
        success = quick_test()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
