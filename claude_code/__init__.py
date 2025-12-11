"""Claude Code Python - A Python implementation of Claude Code with Task Tool and subagents."""

__version__ = "0.1.0"
__author__ = "Claude Code Python Team"

from .main import ClaudeCode
from .tools.task_tool import TaskTool
from .tools.bash_tool import BashTool
from .llm_client import LLMClient

__all__ = ["ClaudeCode", "TaskTool", "BashTool", "LLMClient"]
