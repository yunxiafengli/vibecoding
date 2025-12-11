"""Explore Agent for exploring, understanding and analyzing codebases."""

import os
from typing import Optional, List, Dict, Any
from .base_agent import BaseAgent
from ..tools import ToolResult, BashTool, FileTool, SearchTool
from ..llm_client import LLMClient


class ExploreAgent(BaseAgent):
    """Explore agent for codebase exploration and analysis."""
    
    def __init__(self, description: str, constraints: Optional[str] = None, output_format: Optional[str] = None):
        super().__init__(description, constraints, output_format)
        self.bash_tool = BashTool()
        self.file_tool = FileTool()
        self.search_tool = SearchTool()
        self.llm_client = LLMClient()
    
    def execute(self, prompt: str) -> ToolResult:
        """Execute the explore agent using LLM."""
        try:
            system_prompt = self.get_system_prompt()
            full_prompt = f"""{system_prompt}

Exploration Request:
{prompt}

Your role is to:
1. Explore and understand the codebase structure
2. Analyze code patterns, architecture, and conventions
3. Identify key components and their relationships
4. Document findings and insights
5. Provide recommendations for improvements

Use appropriate tools to explore files, search for patterns, and analyze the codebase.
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
                temperature=0.5  # Lower temperature for more focused analysis
            )
            
            return ToolResult(
                success=result.success,
                data={
                    "agent_type": "explore-agent",
                    "description": self.description,
                    "llm_result": result.data,
                    "prompt": prompt
                },
                metadata={
                    "agent": "ExploreAgent",
                    "model": self.llm_client.model,
                    "exploration_type": "codebase_analysis",
                    **(result.metadata or {})
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"ExploreAgent execution failed: {str(e)}"
            )
