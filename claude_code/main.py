"""Main Claude Code Python implementation."""

from typing import Dict, Any, Optional, List
from .tools import TaskTool, BashTool, FileTool, SearchTool, ToolResult


class ClaudeCode:
    """Main Claude Code class that orchestrates tools and agents."""
    
    def __init__(self):
        self.tools = {
            "task": TaskTool(),
            "bash": BashTool(),
            "file": FileTool(),
            "search": SearchTool()
        }
        self.task_tool = self.tools["task"]
    
    def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """Execute a tool by name."""
        if tool_name not in self.tools:
            return ToolResult(
                success=False,
                error=f"Unknown tool: {tool_name}. Available: {list(self.tools.keys())}"
            )
        
        tool = self.tools[tool_name]
        return tool.execute(**kwargs)
    
    def create_task(self, subagent_type: str, description: str, prompt: str,
                   constraints: Optional[str] = None,
                   output_format: Optional[str] = None) -> ToolResult:
        """Create a new task with a subagent."""
        return self.task_tool.execute(
            subagent_type=subagent_type,
            description=description,
            prompt=prompt,
            constraints=constraints,
            output_format=output_format
        )
    
    def get_task_status(self, task_id: str) -> Optional[ToolResult]:
        """Get the status of a task."""
        task = self.task_tool.get_task_status(task_id)
        if task:
            return ToolResult(
                success=True,
                data=task.to_dict()
            )
        return None
    
    def wait_for_task(self, task_id: str, timeout: Optional[float] = None) -> ToolResult:
        """Wait for a task to complete."""
        task = self.task_tool.wait_for_task(task_id, timeout)
        if task:
            return ToolResult(
                success=True,
                data=task.to_dict()
            )
        return ToolResult(success=False, error=f"Task not found: {task_id}")
    
    def wait_for_all_tasks(self, timeout: Optional[float] = None) -> List[Dict[str, Any]]:
        """Wait for all tasks to complete."""
        tasks = self.task_tool.wait_for_all_tasks(timeout)
        return [task.to_dict() for task in tasks]
    
    def execute_bash(self, command: str, description: str, dir_path: Optional[str] = None) -> ToolResult:
        """Execute a bash command."""
        return self.tools["bash"].execute(
            command=command,
            description=description,
            dir_path=dir_path
        )
    
    def read_file(self, file_path: str, limit: Optional[int] = None) -> ToolResult:
        """Read a file."""
        return self.tools["file"].execute(
            action="read",
            file_path=file_path,
            limit=limit
        )
    
    def write_file(self, file_path: str, content: str) -> ToolResult:
        """Write content to a file."""
        return self.tools["file"].execute(
            action="write",
            file_path=file_path,
            content=content
        )
    
    def search_files(self, pattern: str, path: str = ".", 
                    include: Optional[str] = None, max_results: int = 100) -> ToolResult:
        """Search for pattern in files."""
        return self.tools["search"].execute(
            pattern=pattern,
            path=path,
            include=include,
            max_results=max_results
        )
    
    def cleanup(self):
        """Clean up resources."""
        self.task_tool.cleanup()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
