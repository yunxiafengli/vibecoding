# Claude Code Python - CLI 使用指南

## 快速开始

```bash
cd D:\vibecoding
python claude_cli.py
```

## 使用示例

### 示例 1: 创建文件和文件夹

```
> 创建一个名为 my_project 的文件夹，并在里面创建 README.md 文件

🤖 正在理解你的指令并调用工具...

✅ LLM 调用了 2 个工具

[工具调用 1]
状态: 成功
输出:
my_project

[工具调用 2]
结果: Successfully wrote to my_project/README.md

✅ 执行成功！
```

### 示例 2: 搜索代码

```
> 搜索所有包含 "class" 的 Python 文件

🤖 正在理解你的指令并调用工具...

✅ LLM 调用了 1 个工具

[工具调用 1]
状态: 成功
结果: 找到 15 个匹配
  claude_code/main.py:15
  claude_code/tools/base.py:8
  ...

✅ 执行成功！
```

### 示例 3: 使用 Task Tool

```
> 使用 task 工具帮我规划一个用户认证系统

🤖 正在理解你的指令并调用工具...

✅ LLM 调用了 1 个工具

[工具调用 1]
状态: 成功
结果: 任务已创建: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

✅ 执行成功！
```

### 示例 4: 直接命令（快速执行）

```
> bash run dir

✅ 执行成功！

[命令输出]
 Volume in drive D is Data
 ...
```

## 支持的命令

### 自然语言指令

直接输入你想做的事情：

- `创建一个 Python 脚本，打印 Hello World`
- `在当前目录搜索所有 .txt 文件`
- `读取 README.md 文件的内容`
- `创建文件夹 project/{src,tests,docs}`

### 特殊命令

- `help` - 显示帮助信息
- `clear` - 清屏
- `history` - 显示历史命令
- `exit` / `quit` / `q` - 退出程序

### 直接工具调用（快速模式）

格式：`工具名 动作 参数`

- `bash run <命令>` - 执行 shell 命令
  - 示例：`bash run dir`, `bash run echo hello`
  
- `file read <文件路径>` - 读取文件
  - 示例：`file read README.md`
  
- `file write <文件路径> <内容>` - 写入文件
  - 示例：`file write test.txt Hello World`
  
- `search pattern <模式>` - 搜索模式
  - 示例：`search pattern class.*Agent`

## 高级示例

### 创建项目结构

```
> 帮我创建一个完整的 Web 项目，包括 app.py、templates 文件夹和 static 文件夹
```

### 代码分析

```
> 分析当前目录的所有 Python 文件，告诉我项目的主要功能
```

### 使用特定 Agent

```
> 使用 plan-agent 帮我规划一个数据库设计，支持用户、订单、产品管理
```

```
> 使用 explore-agent 分析 claude_code 目录的代码结构
```

## 故障排除

### LLM 没有调用工具

如果 LLM 只是返回文本而没有调用工具：

1. 尝试更明确的指令，例如：
   - 不好的：`写一个 Python 脚本`
   - 好的：`创建一个名为 app.py 的文件，写入一个简单的 Python Web 应用`

2. 或者直接使用快速模式：
   - `file write app.py from flask import Flask...`

### 命令执行失败

检查错误消息：
- `Directory does not exist` - 目录不存在，先创建目录
- `File not found` - 文件不存在，检查路径
- `Command failed` - 命令执行失败，检查命令语法

## 退出程序

输入以下任意命令退出：
- `exit`
- `quit`
- `q`

或者按 `Ctrl+C`

## 提示

1. **明确具体**：越具体的指令，LLM 执行得越准确
2. **分步骤**：复杂任务可以分多个步骤执行
3. **使用快速模式**：对于简单操作，直接工具调用更快
4. **查看历史**：使用 `history` 查看之前的命令

享受使用 Claude Code Python CLI！
