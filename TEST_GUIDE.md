# Claude Code Python - 测试指南

## 快速开始

### 1. 运行完整测试套件

```bash
# 测试所有功能（包括 LLM 集成）
python test_llm_integration.py

# 测试基础功能（不调用 LLM）
python test_all_features.py

# 运行演示
python demos/task_tool_demo.py
```

### 2. 交互式测试

创建一个测试脚本 `test_my_scenario.py`：

```python
from claude_code import ClaudeCode

# 测试 PlanAgent
with ClaudeCode() as claude:
    # 创建规划任务
    result = claude.create_task(
        subagent_type="plan-agent",
        description="Plan a web scraper",
        prompt="I need to build a web scraper to extract product prices from an e-commerce site"
    )
    
    # 等待完成
    task_id = result.data["task_id"]
    task_result = claude.wait_for_task(task_id)
    
    # 打印结果
    print("=" * 70)
    print("Generated Plan:")
    print("=" * 70)
    print(task_result.data["result"]["data"]["plan"])
```

## 测试场景示例

### 场景 1: 使用 PlanAgent 制定计划

```python
from claude_code import ClaudeCode

with ClaudeCode() as claude:
    result = claude.create_task(
        subagent_type="plan-agent",
        description="Plan database design",
        prompt="""
        Design a database schema for a social media app.
        It should support users, posts, comments, and likes.
        Use PostgreSQL.
        """
    )
    
    task_id = result.data["task_id"]
    task_result = claude.wait_for_task(task_id)
    
    if task_result.success:
        print("✓ Plan generated successfully!")
        print(task_result.data["result"]["data"]["plan"])
```

### 场景 2: 使用 ExploreAgent 分析代码库

```python
from claude_code import ClaudeCode

with ClaudeCode() as claude:
    result = claude.create_task(
        subagent_type="explore-agent",
        description="Analyze project structure",
        prompt="Analyze the claude_code directory and describe the architecture"
    )
    
    task_id = result.data["task_id"]
    task_result = claude.wait_for_task(task_id, timeout=60)
    
    if task_result.success:
        print("✓ Analysis complete!")
        print(task_result.data["result"]["data"]["llm_result"]["llm_response"])
```

### 场景 3: 使用 GeneralPurposeAgent 执行复杂任务

```python
from claude_code import ClaudeCode

with ClaudeCode() as claude:
    result = claude.create_task(
        subagent_type="general-purpose",
        description="Find Python files",
        prompt="Search for all Python files in the current directory and list them"
    )
    
    task_id = result.data["task_id"]
    task_result = claude.wait_for_task(task_id, timeout=60)
    
    if task_result.success:
        print("✓ Task completed!")
        llm_result = task_result.data["result"]["data"]["llm_result"]
        
        if llm_result.get("tool_results"):
            print(f"Used {llm_result['tool_calls']} tool calls")
            for tool_result in llm_result["tool_results"]:
                print(f"Tool output: {tool_result['data']['stdout']}")
        else:
            print(f"LLM response: {llm_result['llm_response']}")
```

### 场景 4: 并行执行多个任务

```python
from claude_code import ClaudeCode

with ClaudeCode() as claude:
    # 创建多个并行任务
    tasks = []
    
    # 任务1: 规划 API
    task1 = claude.create_task(
        subagent_type="plan-agent",
        description="Plan REST API",
        prompt="Plan a REST API for user management"
    )
    tasks.append(task1.data["task_id"])
    
    # 任务2: 分析代码库
    task2 = claude.create_task(
        subagent_type="explore-agent",
        description="Analyze codebase",
        prompt="Analyze the tools directory structure"
    )
    tasks.append(task2.data["task_id"])
    
    # 任务3: 研究技术
    task3 = claude.create_task(
        subagent_type="general-purpose",
        description="Research authentication",
        prompt="Compare JWT and session-based authentication"
    )
    tasks.append(task3.data["task_id"])
    
    print(f"Created {len(tasks)} parallel tasks")
    
    # 等待所有任务完成
    all_results = claude.wait_for_all_tasks(timeout=90)
    
    print("\n" + "=" * 70)
    print("ALL TASKS COMPLETED")
    print("=" * 70)
    
    for i, task in enumerate(all_results, 1):
        print(f"\nTask {i} ({task['agent_type']}):")
        print(f"Status: {task['status']}")
        if task['status'] == 'completed':
            result_data = task['result']['data']
            if 'plan' in result_data:
                print(f"Plan: {result_data['plan'][:100]}...")
            elif 'llm_result' in result_data:
                llm_result = result_data['llm_result']
                if 'llm_response' in llm_result:
                    print(f"Response: {llm_result['llm_response'][:100]}...")
                if 'tool_calls' in llm_result and llm_result['tool_calls'] > 0:
                    print(f"Used {llm_result['tool_calls']} tools")
```

### 场景 5: 使用 Bash 工具

```python
from claude_code import ClaudeCode

with ClaudeCode() as claude:
    # 直接执行 bash 命令
    result = claude.execute_bash("dir", "List files")
    
    if result.success:
        print("✓ Command executed:")
        print(result.data["stdout"])
    else:
        print(f"✗ Command failed: {result.error}")
```

### 场景 6: 使用搜索工具

```python
from claude_code import ClaudeCode

with ClaudeCode() as claude:
    # 搜索代码模式
    result = claude.search_files(
        pattern="class.*Agent",
        include="*.py"
    )
    
    if result.success:
        print(f"✓ Found {result.data['total_matches']} matches")
        for match in result.data['results'][:3]:  # 显示前3个
            print(f"  {match['file']}:{match['line_number']} - {match['line_content'][:50]}")
```

## 测试命令速查

```bash
# 安装依赖
pip install -r requirements.txt

# 基础功能测试
python test_all_features.py

# LLM 集成测试
python test_llm_integration.py

# 完整演示
python demos/task_tool_demo.py

# 交互式测试
python -c "
from claude_code import ClaudeCode
with ClaudeCode() as claude:
    result = claude.create_task('plan-agent', 'Test', 'Hello')
    print(result.data)
"
```

## 预期输出示例

### PlanAgent 输出
```
# Plan for: Plan database design

## Analysis
Based on the request, this task requires designing a PostgreSQL database...

## Proposed Steps

1. **Requirements Analysis**
   - Identify entities: users, posts, comments, likes
   - Determine relationships between entities
   ...
```

### GeneralPurposeAgent 输出（使用工具）
```
✓ Task completed!
LLM decided to use bash tool
Tool output:
 Volume in drive D is Data
 Directory of D:\vibecoding

2025/12/11  10:30    <DIR>          .
2025/12/11  10:30    <DIR>          ..
... files listed ...
```

### ExploreAgent 输出
```
✓ Analysis complete!
The codebase follows a clean architecture with separation of concerns...

Key findings:
- Tools are modular and extensible
- Agents have clear responsibilities
- Good use of design patterns
```

## 故障排除

### API 密钥问题
```bash
# 检查 .env 文件是否存在
cat .env

# 如果没有，从示例复制
cp .env.example .env

# 编辑并添加你的 API 密钥
# MOONSHOT_API_KEY=your_key_here
```

### 网络问题
```python
# 测试直接 API 调用
from claude_code.llm_client import LLMClient

client = LLMClient()
response = client.chat_completion([
    {"role": "user", "content": "Hello"}
])
print(response.choices[0].message.content)
```

### 超时问题
```python
# 增加超时时间
task_result = claude.wait_for_task(task_id, timeout=120)  # 120秒
```

## 下一步

1. **尝试不同的任务**：修改示例中的 prompt，测试各种场景
2. **添加新工具**：继承 `BaseTool` 类，扩展功能
3. **添加新 Agent**：继承 `BaseAgent` 类，创建专用 agent
4. **集成到项目**：在你的项目中使用 `ClaudeCode` 类

祝你测试愉快！
