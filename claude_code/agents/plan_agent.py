"""Plan Agent for planning, analysis, and outlining implementation steps."""

from typing import Optional
from .base_agent import BaseAgent
from ..tools import ToolResult
from ..llm_client import LLMClient


class PlanAgent(BaseAgent):
    """Plan agent for planning and analysis tasks."""
    
    def __init__(self, description: str, constraints: Optional[str] = None, output_format: Optional[str] = None):
        super().__init__(description, constraints, output_format)
        self.llm_client = LLMClient()
    
    def execute(self, prompt: str) -> ToolResult:
        """Execute the plan agent using LLM."""
        try:
            system_prompt = self.get_system_prompt()
            full_prompt = f"""{system_prompt}

Planning Request:
{prompt}

Your role is to:
1. Analyze the request thoroughly
2. Break down complex tasks into manageable steps
3. Provide a clear, actionable plan
4. Identify potential challenges and solutions
5. Suggest the best approach and tools to use

Please provide a detailed plan with numbered steps.
"""
            
            # Call LLM for planning
            messages = [
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self.llm_client.chat_completion(
                messages=messages,
                temperature=0.3  # Lower temperature for more focused planning
            )
            
            plan = response.choices[0].message.content
            
            return ToolResult(
                success=True,
                data={
                    "agent_type": "plan-agent",
                    "description": self.description,
                    "plan": plan,
                    "prompt": prompt
                },
                metadata={
                    "agent": "PlanAgent",
                    "model": self.llm_client.model,
                    "output_type": "plan"
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"PlanAgent execution failed: {str(e)}"
            )
