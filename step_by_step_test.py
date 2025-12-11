"""
分步骤测试：让 LLM 按顺序执行多个操作
"""

import sys
import os
import shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_code import ClaudeCode


def cleanup():
    """清理之前的测试文件"""
    for item in ['ai_articles', 'ai_research', 'test_multi_step']:
        if os.path.exists(item):
            shutil.rmtree(item)


def main():
    print("=" * 70)
    print("分步骤测试：创建文件夹 + 生成文件 + 写入内容")
    print("=" * 70)
    
    # 清理之前的测试
    cleanup()
    
    with ClaudeCode() as claude:
        print("\n步骤 1: 创建文件夹结构...")
        result = claude.create_task(
            subagent_type="general-purpose",
            description="创建两个文件夹",
            prompt="使用 bash_tool 执行: mkdir ai_articles ai_research"
        )
        
        task_id = result.data["task_id"]
        claude.wait_for_task(task_id, timeout=30)
        
        # 验证
        if os.path.exists("ai_articles") and os.path.exists("ai_research"):
            print("✓ 文件夹创建成功")
        else:
            print("✗ 文件夹创建失败")
            return False
        
        print("\n步骤 2: 在 ai_articles 中创建文件并写入内容...")
        result = claude.create_task(
            subagent_type="general-purpose",
            description="创建并写入文章文件",
            prompt="""
            使用 file_tool 执行以下操作：
            action: "write"
            file_path: "ai_articles/llm_overview.txt"
            content: "大模型发展现状：近年来，GPT、Claude、Kimi等大型语言模型快速发展。这些模型在文本生成、代码编写、翻译等任务上表现出色。技术趋势包括多模态融合、推理能力增强和效率优化。应用场景涵盖智能客服、内容创作、编程辅助等。尽管面临计算成本、安全性和伦理挑战，大模型仍在推动AI技术边界，未来有望在更多领域实现突破。"
            """
        )
        
        task_id = result.data["task_id"]
        claude.wait_for_task(task_id, timeout=30)
        
        # 验证
        file_path = "ai_articles/llm_overview.txt"
        if os.path.exists(file_path):
            print("✓ 文件创建成功")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✓ 文件内容（{len(content)} 字符）：")
            print("-" * 70)
            print(content[:300] + "..." if len(content) > 300 else content)
            print("-" * 70)
        else:
            print("✗ 文件创建失败")
            return False
        
        print("\n步骤 3: 让 LLM 自动生成内容并写入...")
        result = claude.create_task(
            subagent_type="general-purpose",
            description="LLM生成文章内容",
            prompt="""
            请写一篇关于人工智能未来发展的简短文章（约150字），
            然后将这篇文章保存到 ai_research/future_of_ai.txt 文件中。
            
            使用 file_tool 的 write 操作来保存文件。
            """
        )
        
        task_id = result.data["task_id"]
        task_result = claude.wait_for_task(task_id, timeout=60)
        
        # 检查 LLM 是否使用了工具
        llm_data = task_result.data['result']['data']['llm_result']
        print(f"\nLLM 工具调用次数: {llm_data.get('tool_calls', 0)}")
        
        if llm_data.get('tool_results'):
            for i, tr in enumerate(llm_data['tool_results'], 1):
                print(f"\n工具调用 {i}:")
                print(f"  成功: {tr['success']}")
                if tr.get('data', {}).get('message'):
                    print(f"  消息: {tr['data']['message']}")
        
        # 验证文件
        research_file = "ai_research/future_of_ai.txt"
        if os.path.exists(research_file):
            print(f"\n✓ {research_file} 创建成功")
            
            with open(research_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✓ 内容长度: {len(content)} 字符")
            print("-" * 70)
            print(content[:200] + "..." if len(content) > 200 else content)
            print("-" * 70)
        else:
            print(f"\n✗ {research_file} 未创建")
            # 这可能是因为 LLM 没有调用工具，而是直接返回了文本
            if 'llm_response' in llm_data:
                print(f"LLM 直接响应: {llm_data['llm_response'][:200]}...")
        
        print("\n" + "=" * 70)
        print("✅ 测试完成！")
        print("=" * 70)
        
        # 清理
        cleanup()
        
        return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
