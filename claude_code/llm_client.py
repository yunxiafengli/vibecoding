"""LLM Client for Claude Code Python - Kimi API integration."""

import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from .tools import ToolResult

# Load environment variables
load_dotenv()


class LLMClient:
    """Client for interacting with Kimi LLM API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM client.
        
        Args:
            api_key: Kimi API key (defaults to MOONSHOT_API_KEY env var)
            base_url: API base URL (defaults to MOONSHOT_BASE_URL env var)
            model: Model name (defaults to MOONSHOT_MODEL env var)
        """
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        self.base_url = base_url or os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
        self.model = model or os.getenv("MOONSHOT_MODEL", "kimi-k2-turbo-preview")
        
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY not found. Please set it in .env file or environment variables.")
        
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
    
    def chat_completion(self, messages: List[Dict[str, str]], 
                       tools: Optional[List[Dict[str, Any]]] = None,
                       tool_choice: Optional[str] = "auto",
                       temperature: float = 0.6) -> Any:
        """
        Send chat completion request to LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions for function calling
            tool_choice: How to choose tools ("auto", "none", or specific tool)
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            API response object
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice
        
        return self.client.chat.completions.create(**kwargs)
    
    def execute_with_tools(self, system_prompt: str, user_prompt: str, 
                          available_tools: Dict[str, Any],
                          temperature: float = 0.6,
                          max_iterations: int = 10) -> ToolResult:
        """
        Execute LLM with tool calling capability (supports multi-turn tool calls).
        
        Args:
            system_prompt: System prompt for LLM
            user_prompt: User's request
            available_tools: Dictionary of tool name to tool instance
            temperature: Sampling temperature
            max_iterations: Maximum number of tool call iterations
            
        Returns:
            ToolResult with LLM response or tool execution results
        """
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Prepare tool definitions
            tools = []
            for tool_name, tool in available_tools.items():
                schema = tool.get_schema()
                tool_def = {
                    "type": "function",
                    "function": {
                        "name": schema["name"],
                        "description": schema["description"],
                        "parameters": schema["parameters"]
                    }
                }
                tools.append(tool_def)
            
            total_tool_calls = 0
            all_tool_results = []
            
            # Multi-turn loop: keep calling LLM until it doesn't request tools
            for iteration in range(max_iterations):
                # Call LLM
                response = self.chat_completion(
                    messages=messages,
                    tools=tools if tools else None,
                    tool_choice="auto" if tools else None,
                    temperature=temperature
                )
                
                # Process response
                message = response.choices[0].message
                
                # Check if LLM wants to call a tool
                if message.tool_calls:
                    # Execute tool calls
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = tool_call.function.arguments
                        
                        if tool_name in available_tools:
                            tool = available_tools[tool_name]
                            # Parse arguments (they come as JSON string)
                            import json
                            args = json.loads(tool_args)
                            
                            # Execute tool
                            tool_result = tool.execute(**args)
                            all_tool_results.append(tool_result)
                            total_tool_calls += 1
                            
                            # Add tool call and result to messages for next iteration
                            messages.append({
                                "role": "assistant",
                                "tool_calls": [{
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": tool_name,
                                        "arguments": tool_args
                                    }
                                }]
                            })
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(tool_result.to_dict())
                            })
                else:
                    # LLM didn't call any tools, return the final response
                    return ToolResult(
                        success=True,
                        data={
                            "llm_response": message.content,
                            "tool_results": [r.to_dict() for r in all_tool_results],
                            "tool_calls": total_tool_calls,
                            "iterations": iteration
                        },
                        metadata={
                            "model": self.model,
                            "execution_type": "multi_turn" if total_tool_calls > 0 else "direct_response",
                            "total_tool_calls": total_tool_calls
                        }
                    )
            
            # Max iterations reached
            return ToolResult(
                success=True,
                data={
                    "llm_response": "Maximum iterations reached",
                    "tool_results": [r.to_dict() for r in all_tool_results],
                    "tool_calls": total_tool_calls,
                    "iterations": max_iterations
                },
                metadata={
                    "model": self.model,
                    "execution_type": "multi_turn_max_iter",
                    "total_tool_calls": total_tool_calls
                }
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"LLM execution failed: {str(e)}",
                metadata={"model": self.model}
            )
