"""General Purpose Agent for complex research, code searching, and multi-step tasks."""

import os
from typing import Optional, Dict, Any
from .base_agent import BaseAgent
from ..tools import ToolResult, BashTool, FileTool, SearchTool
from ..llm_client import LLMClient


class GeneralPurposeAgent(BaseAgent):
    """General purpose agent for complex tasks."""
    
    def __init__(self, description: str, constraints: Optional[str] = None, output_format: Optional[str] = None):
        super().__init__(description, constraints, output_format)
        self.bash_tool = BashTool()
        self.file_tool = FileTool()
        self.search_tool = SearchTool()
        self.llm_client = LLMClient()
    
    def execute(self, prompt: str) -> ToolResult:
        """Execute the general purpose agent using LLM."""
        try:
            system_prompt = self.get_system_prompt()
            full_prompt = f"""{system_prompt}

User Request:
{prompt}

You have access to the following tools:
- BashTool (run_shell_command): Execute shell commands
- FileTool (file_tool): Read, write, and search files
- SearchTool (search_tool): Search for patterns in files

Please analyze the request and decide whether to use tools. If you need to use tools, call them directly. If you can answer from your knowledge, provide a direct response.
"""
            
            # Prepare available tools
            available_tools = {
                "run_shell_command": self.bash_tool,
                "file_tool": self.file_tool,
                "search_tool": self.search_tool
            }
            
            # Call LLM with tool support
            result = self.llm_client.execute_with_tools(
                system_prompt=full_prompt,
                user_prompt=prompt,
                available_tools=available_tools,
                temperature=0.6
            )
            
            return ToolResult(
                success=result.success,
                data={
                    "agent_type": "general-purpose",
                    "description": self.description,
                    "llm_result": result.data,
                    "prompt": prompt
                },
                metadata={
                    "agent": "GeneralPurposeAgent",
                    "model": self.llm_client.model,
                    **(result.metadata or {})
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"GeneralPurposeAgent execution failed: {str(e)}"
            )
