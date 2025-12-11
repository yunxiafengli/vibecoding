"""
Demo: 创建文件并写入内容 - 展示 LLM 的内容生成和文件操作能力

这个 demo 演示了：
1. 创建文件夹结构
2. 生成关于大模型发展的文章内容
3. 写入文件
4. 读取并验证文件内容
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_code import ClaudeCode


def demo_create_files_and_content():
    """演示创建文件结构并生成内容"""
    print("=" * 70)
    print("DEMO: 创建文件夹并生成大模型发展现状文章")
    print("=" * 70)
    
    with ClaudeCode() as claude:
        print("\n1. 创建复杂任务：生成内容并管理文件...")
        
        # 创建一个复杂的任务，要求 LLM 完成多个步骤
        result = claude.create_task(
            subagent_type="general-purpose",
            description="创建文件夹结构并生成文章",
            prompt="""
            请帮我完成以下任务：
            
            1. 在当前目录创建两个文件夹：
               - ai_articles（用于存放文章）
               - ai_research（用于存放研究资料）
            
            2. 在 ai_articles 文件夹中创建一个名为 "llm_development_overview.txt" 的文件
            
            3. 在该文件中写入一篇约200字的文章，主题是目前大模型的发展现状，包括：
               - 当前主流大模型（如GPT、Claude、Kimi等）的发展情况
               - 大模型的技术趋势和应用场景
               - 面临的挑战和未来发展方向
            
            4. 使用bash工具确认文件夹和文件已成功创建
            
            5. 读取刚刚创建的文件内容，验证内容是否正确写入
            
            请使用适当的工具（bash、file）来完成这些任务。
            """,
            constraints="确保文章内容专业、准确，约200字左右"
        )
        
        if result.success:
            task_id = result.data["task_id"]
            print(f"   ✓ 任务已创建: {task_id}")
            print(f"   状态: {result.data['status']}")
            
            print("\n2. 等待 LLM 执行任务（可能需要30-60秒）...")
            print("   LLM 正在：")
            print("   - 分析任务要求")
            print("   - 决定使用哪些工具")
            print("   - 生成文章内容")
            print("   - 执行文件操作")
            
            # 等待任务完成，设置较长的超时时间
            task_result = claude.wait_for_task(task_id, timeout=120)
            
            if task_result.success and task_result.data["status"] == "completed":
                print("\n   ✓ 任务执行完成！")
                
                # 显示 LLM 的执行结果
                llm_result = task_result.data["result"]["data"]["llm_result"]
                
                print("\n3. LLM 执行总结：")
                print("-" * 70)
                
                if llm_result.get("tool_calls", 0) > 0:
                    print(f"   使用了 {llm_result['tool_calls']} 个工具调用")
                    
                    # 显示每个工具调用的结果
                    for i, tool_result in enumerate(llm_result.get("tool_results", []), 1):
                        if tool_result["success"]:
                            print(f"   ✓ 工具调用 {i} 成功")
                            if "stdout" in tool_result.get("data", {}):
                                output = tool_result["data"]["stdout"]
                                if output and output != "(empty)":
                                    print(f"     输出: {output[:100]}...")
                        else:
                            print(f"   ✗ 工具调用 {i} 失败: {tool_result.get('error', '')}")
                else:
                    print(f"   LLM 直接响应: {llm_result.get('llm_response', '无')[:100]}...")
                
                print("-" * 70)
                
                # 验证文件是否创建成功
                print("\n4. 验证文件创建结果：")
                
                # 检查 ai_articles 文件夹是否存在
                if os.path.exists("ai_articles"):
                    print("   ✓ ai_articles 文件夹已创建")
                    
                    # 检查文件是否存在
                    article_file = os.path.join("ai_articles", "llm_development_overview.txt")
                    if os.path.exists(article_file):
                        print("   ✓ 文章文件已创建")
                        
                        # 读取文件内容
                        with open(article_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        print(f"   ✓ 文件大小: {len(content)} 字符")
                        
                        # 显示文件内容预览
                        print("\n" + "=" * 70)
                        print("生成的文章内容（预览）：")
                        print("=" * 70)
                        print(content[:500])  # 显示前500字符
                        if len(content) > 500:
                            print("...")
                        print("=" * 70)
                        
                        # 验证内容质量
                        print("\n5. 内容质量检查：")
                        checks = [
                            ("字数", len(content) >= 150, f"{len(content)} 字"),
                            ("提及大模型", "大模型" in content or "LLM" in content or "GPT" in content, "是"),
                            ("提及发展趋势", "发展" in content or "趋势" in content or "未来" in content, "是"),
                            ("提及应用场景", "应用" in content or "场景" in content, "是"),
                        ]
                        
                        for check_name, passed, detail in checks:
                            status = "✓" if passed else "✗"
                            print(f"   {status} {check_name}: {detail}")
                        
                        print("\n" + "=" * 70)
                        print("✅ DEMO 成功完成！")
                        print("=" * 70)
                        print("\n总结：")
                        print("  ✓ 成功创建文件夹结构")
                        print("  ✓ 生成了专业的文章内容")
                        print("  ✓ 正确使用工具完成任务")
                        print("  ✓ LLM 展现了复杂任务处理能力")
                        
                        return True
                    else:
                        print("   ✗ 文章文件未找到")
                        return False
                else:
                    print("   ✗ ai_articles 文件夹未创建")
                    return False
            else:
                print(f"\n   ✗ 任务执行失败: {task_result.data.get('error', '未知错误')}")
                return False
        else:
            print(f"✗ 任务创建失败: {result.error}")
            return False


def cleanup():
    """清理测试文件"""
    print("\n" + "=" * 70)
    print("清理测试文件...")
    print("=" * 70)
    
    import shutil
    
    # 删除创建的文件夹
    for folder in ["ai_articles", "ai_research"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ 删除文件夹: {folder}")
    
    print("✓ 清理完成")


if __name__ == "__main__":
    try:
        success = demo_create_files_and_content()
        
        # 自动清理（非交互模式）
        print("\n自动清理测试文件...")
        cleanup()
        
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Demo 出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
