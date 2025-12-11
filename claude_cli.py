#!/usr/bin/env python3
"""
Claude Code Python - 智能 CLI 界面

一个交互式命令行工具，让用户用自然语言与 LLM 交互，
自动调用工具（bash, file, search, task）完成任务。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_code import ClaudeCode
from claude_code.llm_client import LLMClient


class ClaudeCLI:
    """交互式 CLI 界面"""
    
    def __init__(self):
        self.claude = ClaudeCode()
        self.llm = LLMClient()
        self.history = []
        
    def print_banner(self):
        """显示欢迎横幅"""
        print("\n" + "=" * 70)
        print(" Claude Code Python - 智能命令行助手")
        print("=" * 70)
        print("\n💡 提示：输入自然语言指令，我会自动调用工具帮你完成")
        print("📋 可用工具：bash(命令执行) | file(文件操作) | search(搜索) | task(任务管理)")
        print("❌ 输入 'exit' 或 'quit' 退出")
        print("🆘 输入 'help' 查看帮助")
        print("=" * 70 + "\n")
    
    def print_help(self):
        """显示帮助信息"""
        print("\n" + "=" * 70)
        print(" 使用帮助")
        print("=" * 70)
        print("""
使用示例：

1. 文件操作：
   > 创建一个名为 test.py 的文件，写入 print('hello')
   > 读取 README.md 文件的前10行
   > 在当前目录搜索所有 .py 文件

2. 命令执行：
   > 列出当前目录的文件
   > 创建文件夹 my_project
   > 查看当前路径

3. 代码搜索：
   > 搜索所有包含 "class" 的 Python 文件
   > 查找包含 "TODO" 的文件

4. 复杂任务：
   > 创建一个 Web 项目结构，包括 app.py 和 templates 文件夹
   > 分析当前项目的代码结构

5. 使用 Task Tool：
   > 使用 task 工具帮我规划一个用户认证系统
   > 用 explore-agent 分析这个代码库
   > 用 plan-agent 设计数据库结构

特殊命令：
   help    - 显示此帮助信息
   clear   - 清屏
   history - 显示历史命令
   exit    - 退出程序
        """)
        print("=" * 70 + "\n")
    
    def execute_direct_command(self, command):
        """直接执行简单命令（不调用 LLM）"""
        parts = command.split()
        if len(parts) < 2:
            return False
        
        tool = parts[0]
        action = parts[1]
        
        try:
            if tool == "bash" and action == "run":
                cmd = " ".join(parts[2:])
                result = self.claude.execute_bash(cmd, f"Execute: {cmd}")
                self.print_result(result)
                return True
            elif tool == "file" and action == "read":
                file_path = parts[2]
                result = self.claude.read_file(file_path)
                self.print_result(result)
                return True
            elif tool == "file" and action == "write":
                file_path = parts[2]
                content = " ".join(parts[3:])
                result = self.claude.write_file(file_path, content)
                self.print_result(result)
                return True
            elif tool == "search" and action == "pattern":
                pattern = parts[2]
                result = self.claude.search_files(pattern)
                self.print_result(result)
                return True
        except:
            pass
        
        return False
    
    def print_result(self, result):
        """打印执行结果"""
        if result.success:
            print("\n✅ 执行成功！")
            if result.data:
                if isinstance(result.data, dict):
                    if 'stdout' in result.data:
                        print("\n[命令输出]")
                        print(result.data['stdout'][:500])
                    elif 'content' in result.data:
                        print("\n[文件内容]")
                        print(result.data['content'][:500])
                    elif 'results' in result.data:
                        print(f"\n[搜索结果 - 找到 {result.data['total_matches']} 个匹配]")
                        for match in result.data['results'][:5]:
                            print(f"  {match['file']}:{match['line_number']}")
                    else:
                        print(f"\n[结果] {result.data}")
                else:
                    print(f"\n[结果] {result.data}")
        else:
            print("\n❌ 执行失败")
            print(f"错误: {result.error}")
    
    def process_natural_language(self, user_input):
        """处理自然语言输入，调用 LLM"""
        print(f"\n🤖 正在理解你的指令并调用工具...")
        
        # 构建系统提示
        system_prompt = """
你是一个智能命令行助手，能够调用工具来帮助用户完成任务。

可用的工具：
1. bash_tool (run_shell_command) - 执行 shell 命令
   - 用于：创建文件夹、列出文件、执行命令等
   
2. file_tool - 文件操作
   - action: "read" - 读取文件
   - action: "write" - 写入文件
   - action: "search" - 在文件中搜索
   - action: "list" - 列出目录
   
3. search_tool - 在多个文件中搜索模式
   - 用于：搜索代码、查找文本等
   
4. task_tool - 创建和管理子任务
   - subagent_type: "plan-agent" - 制定计划
   - subagent_type: "explore-agent" - 探索代码库
   - subagent_type: "general-purpose" - 复杂任务

重要原则：
- 根据用户请求选择合适的工具
- 如果需要多个步骤，按顺序执行
- 执行后返回结果给用户
- 如果任务复杂，使用 task_tool 创建子任务

当前工作目录: {}
""".format(os.getcwd())
        
        try:
            # 使用 LLM 处理请求
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            # 准备可用工具
            available_tools = {
                "run_shell_command": self.claude.tools["bash"],
                "file_tool": self.claude.tools["file"],
                "search_tool": self.claude.tools["search"]
            }
            
            # 调用 LLM
            response = self.llm.execute_with_tools(
                system_prompt=system_prompt,
                user_prompt=user_input,
                available_tools=available_tools,
                temperature=0.3
            )
            
            if response.success:
                data = response.data
                
                if data.get('tool_calls', 0) > 0:
                    print(f"\n✅ LLM 调用了 {data['tool_calls']} 个工具")
                    
                    # 显示工具调用结果
                    for i, tool_result in enumerate(data.get('tool_results', []), 1):
                        print(f"\n[工具调用 {i}]")
                        if tool_result.get('success'):
                            print("状态: 成功")
                            if 'stdout' in tool_result.get('data', {}):
                                output = tool_result['data']['stdout']
                                if output and output != '(empty)':
                                    print(f"输出:\n{output[:300]}")
                            elif 'message' in tool_result.get('data', {}):
                                print(f"结果: {tool_result['data']['message']}")
                        else:
                            print("状态: 失败")
                            print(f"错误: {tool_result.get('error', '未知错误')}")
                
                # 显示 LLM 的直接响应
                if 'llm_response' in data:
                    print(f"\n[LLM 响应]\n{data['llm_response']}")
            else:
                print(f"\n❌ LLM 处理失败: {response.error}")
        
        except Exception as e:
            print(f"\n❌ 处理出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def add_to_history(self, command):
        """添加到历史记录"""
        self.history.append(command)
        if len(self.history) > 50:  # 限制历史记录数量
            self.history.pop(0)
    
    def show_history(self):
        """显示历史命令"""
        if not self.history:
            print("\n暂无历史命令")
            return
        
        print("\n" + "=" * 70)
        print(" 历史命令")
        print("=" * 70)
        for i, cmd in enumerate(self.history, 1):
            print(f"{i:3d}. {cmd}")
        print("=" * 70 + "\n")
    
    def run(self):
        """主循环"""
        self.print_banner()
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                # 添加到历史记录
                self.add_to_history(user_input)
                
                # 处理特殊命令
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 再见！")
                    break
                elif user_input.lower() == 'help':
                    self.print_help()
                    continue
                elif user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_banner()
                    continue
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                # 尝试直接命令（如：bash run dir）
                if self.execute_direct_command(user_input):
                    continue
                
                # 处理自然语言
                self.process_natural_language(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # 清理资源
        self.claude.cleanup()


def main():
    """主函数"""
    try:
        cli = ClaudeCLI()
        cli.run()
    except Exception as e:
        print(f"启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
