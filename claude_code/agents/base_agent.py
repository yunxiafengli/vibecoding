"""Base agent class for Claude Code Python."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..tools import ToolResult


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, description: str, constraints: Optional[str] = None, output_format: Optional[str] = None):
        self.description = description
        self.constraints = constraints
        self.output_format = output_format
    
    @abstractmethod
    def execute(self, prompt: str) -> ToolResult:
        """Execute the agent with the given prompt."""
        pass
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        base_prompt = f"""You are a {self.__class__.__name__} agent.
        
Task: {self.description}
"""
        
        if self.constraints:
            base_prompt += f"""
Constraints:
{self.constraints}
"""
        
        if self.output_format:
            base_prompt += f"""
Output Format:
{self.output_format}
"""
        
        return base_prompt
