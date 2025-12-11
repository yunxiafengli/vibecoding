"""
Demo: 并行任务处理演示

这个demo展示如何使用Task Tool创建多个并行任务，同时执行不同的工作。
"""

import sys
import os
import time

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_code import ClaudeCode


def demo_parallel_research():
    """演示：并行执行多个研究任务"""
    print("=" * 70)
    print("并行任务演示：同时执行多个研究任务")
    print("=" * 70)
    
    with ClaudeCode() as claude:
        print("\n1. 创建3个并行研究任务...")
        print("   任务1: 研究Python异步编程最佳实践")
        print("   任务2: 分析当前AI Agent技术趋势")
        print("   任务3: 探索代码重构方法论")
        
        # 创建3个并行任务
        tasks = []
        
        # 任务1: 研究Python异步编程
        task1 = claude.create_task(
            subagent_type="general-purpose",
            description="研究Python异步编程",
            prompt="""
            请研究并总结Python异步编程的最佳实践，包括：
            - async/await的基本概念和使用方法
            - 常见的异步编程模式和陷阱
            - asyncio库的核心组件
            - 实际应用场景和代码示例
            请提供约300字的详细总结。
            """
        )
        if task1.success:
            tasks.append(("Python异步编程研究", task1.data["task_id"]))
            print(f"   ✓ 任务1已创建: {task1.data['task_id'][:8]}...")
        
        # 任务2: 分析AI Agent技术
        task2 = claude.create_task(
            subagent_type="general-purpose",
            description="分析AI Agent技术",
            prompt="""
            请分析当前AI Agent技术的发展趋势，包括：
            - 主要的技术框架和工具
            - 应用场景和成功案例
            - 面临的挑战和解决方案
            - 未来发展方向
            请提供约300字的详细分析。
            """
        )
        if task2.success:
            tasks.append(("AI Agent技术分析", task2.data["task_id"]))
            print(f"   ✓ 任务2已创建: {task2.data['task_id'][:8]}...")
        
        # 任务3: 探索代码重构方法
        task3 = claude.create_task(
            subagent_type="general-purpose",
            description="探索代码重构方法",
            prompt="""
            请探索代码重构的最佳实践和方法论，包括：
            - 重构的基本原则和时机
            - 常见的重构模式和技巧
            - 如何确保重构的安全性
            - 重构工具和自动化方法
            请提供约300字的详细指南。
            """
        )
        if task3.success:
            tasks.append(("代码重构方法论", task3.data["task_id"]))
            print(f"   ✓ 任务3已创建: {task3.data['task_id'][:8]}...")
        
        print(f"\n2. 所有任务正在并行执行...")
        print(f"   共启动了 {len(tasks)} 个任务，它们将在后台同时运行")
        
        # 等待所有任务完成
        print("\n3. 等待所有任务完成（约30-60秒）...")
        all_results = claude.wait_for_all_tasks(timeout=90)
        
        print("\n" + "=" * 70)
        print("任务执行结果：")
        print("=" * 70)
        
        success_count = 0
        for i, (task_name, task_id) in enumerate(tasks, 1):
            # 查找对应的任务结果
            task_result = next((r for r in all_results if r["task_id"] == task_id), None)
            
            if task_result:
                
                status = task_result["status"]
                status_icon = "✓" if status == "completed" else "✗"
                
                print(f"\n任务 {i}: {task_name}")
                print(f"   状态: {status_icon} {status}")
                
                if status == "completed":
                    success_count += 1
                    # 显示LLM生成的内容
                    llm_result = task_result["result"]["data"]["llm_result"]
                    if "llm_response" in llm_result:
                        content = llm_result["llm_response"]
                        print(f"   内容预览: {content[:150]}...")
                    elif "tool_calls" in llm_result:
                        print(f"   工具调用: {llm_result['tool_calls']} 次")
                elif status == "failed":
                    print(f"   错误: {task_result.get('error', '未知错误')}")
        
        print("\n" + "=" * 70)
        print(f"总结: {success_count}/{len(tasks)} 个任务成功完成")
        print("=" * 70)
        
        return success_count == len(tasks)


def demo_file_operations():
    """演示：并行文件操作任务"""
    print("\n" + "=" * 70)
    print("并行文件操作演示：创建多个文件")
    print("=" * 70)
    
    with ClaudeCode() as claude:
        print("\n1. 创建3个并行文件操作任务...")
        
        # 创建临时文件夹
        os.makedirs("demo_output", exist_ok=True)
        
        # 创建3个并行任务，每个任务创建不同的文件
        tasks = []
        
        # 任务1: 创建Python最佳实践文档
        task1 = claude.create_task(
            subagent_type="general-purpose",
            description="创建Python最佳实践文档",
            prompt="""
            请创建一份Python编程最佳实践的文档，保存到文件 demo_output/python_best_practices.md
            内容包括：
            - 代码风格和规范（PEP 8）
            - 常用设计模式
            - 性能优化技巧
            - 测试和调试建议
            请使用file_tool工具创建文件并写入内容。
            """
        )
        if task1.success:
            tasks.append(("Python最佳实践", task1.data["task_id"]))
        
        # 任务2: 创建API设计指南
        task2 = claude.create_task(
            subagent_type="general-purpose",
            description="创建API设计指南",
            prompt="""
            请创建一份RESTful API设计指南，保存到文件 demo_output/api_design_guide.md
            内容包括：
            - RESTful原则
            - 资源命名规范
            - HTTP方法使用
            - 状态码选择
            - 错误处理
            请使用file_tool工具创建文件并写入内容。
            """
        )
        if task2.success:
            tasks.append(("API设计指南", task2.data["task_id"]))
        
        # 任务3: 创建数据库设计规范
        task3 = claude.create_task(
            subagent_type="general-purpose",
            description="创建数据库设计规范",
            prompt="""
            请创建一份数据库设计规范文档，保存到文件 demo_output/database_design.md
            内容包括：
            - 命名规范
            - 数据类型选择
            - 索引设计原则
            - 关系设计
            - 性能考虑
            请使用file_tool工具创建文件并写入内容。
            """
        )
        if task3.success:
            tasks.append(("数据库设计规范", task3.data["task_id"]))
        
        print(f"   已创建 {len(tasks)} 个文件生成任务")
        
        # 等待所有任务完成
        print("\n2. 等待任务完成...")
        all_results = claude.wait_for_all_tasks(timeout=120)
        
        # 验证文件创建
        print("\n3. 验证文件创建结果：")
        success_count = 0
        
        expected_files = [
            "demo_output/python_best_practices.md",
            "demo_output/api_design_guide.md",
            "demo_output/database_design.md"
        ]
        
        for file_path in expected_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"   ✓ {os.path.basename(file_path)} ({len(content)} 字符)")
                success_count += 1
            else:
                print(f"   ✗ {os.path.basename(file_path)} 未找到")
        
        print(f"\n   成功创建 {success_count}/{len(expected_files)} 个文件")
        return success_count == len(expected_files)


def cleanup():
    """清理测试文件"""
    print("\n" + "=" * 70)
    print("清理测试文件...")
    print("=" * 70)
    
    import shutil
    
    # 删除demo_output文件夹
    if os.path.exists("demo_output"):
        shutil.rmtree("demo_output")
        print("✓ 删除 demo_output 文件夹")
    
    print("✓ 清理完成")


def main():
    """运行所有demo"""
    print("\n" + "=" * 70)
    print("CLAUDE CODE PYTHON - 并行任务处理演示")
    print("Task Tool 并行多Agent任务执行")
    print("=" * 70)
    
    success1 = success2 = False
    
    try:
        # 演示1: 并行研究任务
        success1 = demo_parallel_research()
        
        # 演示2: 并行文件操作
        success2 = demo_file_operations()
        
        print("\n" + "=" * 70)
        print("✅ 所有演示完成！")
        print("=" * 70)
        print("\n演示的功能：")
        print("  ✓ Task Tool 创建并行任务")
        print("  ✓ Subagent 自主执行任务")
        print("  ✓ 多任务并发执行")
        print("  ✓ 任务状态监控和同步")
        print("  ✓ 工具调用和结果验证")
        
    except Exception as e:
        print(f"\n❌ 演示出错: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理
        cleanup()
    
    return success1 and success2


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
