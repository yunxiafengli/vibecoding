"""Task Tool for creating and managing subagents."""

import asyncio
import uuid
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor, Future
from .base import BaseTool, ToolResult


class TaskResult:
    """Result from a task execution."""
    
    def __init__(self, task_id: str, agent_type: str, status: str, result: Optional[ToolResult] = None, error: Optional[str] = None):
        self.task_id = task_id
        self.agent_type = agent_type
        self.status = status  # pending, running, completed, failed
        self.result = result
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "agent_type": self.agent_type,
            "status": self.status,
            "result": self.result.to_dict() if self.result else None,
            "error": self.error
        }


class TaskManager:
    """Manages running tasks and subagents."""
    
    def __init__(self):
        self.tasks: Dict[str, TaskResult] = {}
        self.agents: Dict[str, Any] = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
        self._futures: Dict[str, Future] = {}
    
    def create_task(self, agent_type: str, description: str, prompt: str, 
                   constraints: Optional[str] = None, 
                   output_format: Optional[str] = None) -> str:
        """Create a new task with a subagent."""
        # Delayed import to avoid circular dependencies
        from ..agents import GeneralPurposeAgent, PlanAgent, ExploreAgent
        
        task_id = str(uuid.uuid4())
        
        # Create appropriate agent
        if agent_type == "general-purpose":
            agent = GeneralPurposeAgent(description, constraints, output_format)
        elif agent_type == "plan-agent":
            agent = PlanAgent(description, constraints, output_format)
        elif agent_type == "explore-agent":
            agent = ExploreAgent(description, constraints, output_format)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        # Store task and agent
        self.tasks[task_id] = TaskResult(task_id, agent_type, "pending")
        self.agents[task_id] = agent
        
        # Submit task for execution
        future = self.executor.submit(self._run_agent, task_id, agent, prompt)
        self._futures[task_id] = future
        
        return task_id
    
    def _run_agent(self, task_id: str, agent, prompt: str) -> None:
        """Run an agent in a separate thread."""
        try:
            # Update status to running
            self.tasks[task_id].status = "running"
            
            # Execute agent
            result = agent.execute(prompt)
            
            # Update task result
            self.tasks[task_id].status = "completed"
            self.tasks[task_id].result = result
            
        except Exception as e:
            # Update task with error
            self.tasks[task_id].status = "failed"
            self.tasks[task_id].error = str(e)
    
    def get_task_status(self, task_id: str) -> Optional[TaskResult]:
        """Get the status of a task."""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[TaskResult]:
        """Get all tasks."""
        return list(self.tasks.values())
    
    def wait_for_task(self, task_id: str, timeout: Optional[float] = None) -> Optional[TaskResult]:
        """Wait for a task to complete."""
        future = self._futures.get(task_id)
        if future:
            try:
                future.result(timeout=timeout)
            except Exception as e:
                self.tasks[task_id].status = "failed"
                self.tasks[task_id].error = str(e)
        
        return self.tasks.get(task_id)
    
    def wait_for_all_tasks(self, timeout: Optional[float] = None) -> List[TaskResult]:
        """Wait for all tasks to complete."""
        # Wait for all futures
        for future in self._futures.values():
            try:
                future.result(timeout=timeout)
            except Exception:
                pass
        
        return self.get_all_tasks()
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self.executor.shutdown(wait=True)


class TaskTool(BaseTool):
    """Task Tool for creating and managing subagents."""
    
    def __init__(self):
        super().__init__(
            name="task",
            description="Launch a new agent to handle complex, multi-step tasks autonomously"
        )
        self.task_manager = TaskManager()
    
    def execute(self, subagent_type: str, description: str, prompt: str,
                constraints: Optional[str] = None,
                output_format: Optional[str] = None) -> ToolResult:
        """
        Create and launch a subagent task.
        
        Args:
            subagent_type: Type of agent to launch (general-purpose, plan-agent, explore-agent)
            description: Short description of the task
            prompt: The detailed task prompt for the agent
            constraints: Optional constraints or limitations
            output_format: Optional output format template
            
        Returns:
            ToolResult with task information
        """
        try:
            # Validate subagent type
            valid_types = ["general-purpose", "plan-agent", "explore-agent"]
            if subagent_type not in valid_types:
                return ToolResult(
                    success=False,
                    error=f"Invalid subagent_type. Must be one of: {', '.join(valid_types)}"
                )
            
            # Create task
            task_id = self.task_manager.create_task(
                agent_type=subagent_type,
                description=description,
                prompt=prompt,
                constraints=constraints,
                output_format=output_format
            )
            
            # Get initial task status
            task = self.task_manager.get_task_status(task_id)
            
            return ToolResult(
                success=True,
                data={
                    "task_id": task_id,
                    "status": task.status,
                    "agent_type": subagent_type,
                    "description": description
                },
                metadata={
                    "task_id": task_id,
                    "created_at": "now"
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to create task: {str(e)}"
            )
    
    def get_task_status(self, task_id: str) -> Optional[TaskResult]:
        """Get the status of a specific task."""
        return self.task_manager.get_task_status(task_id)
    
    def get_all_tasks(self) -> List[TaskResult]:
        """Get all tasks."""
        return self.task_manager.get_all_tasks()
    
    def wait_for_task(self, task_id: str, timeout: Optional[float] = None) -> Optional[TaskResult]:
        """Wait for a task to complete."""
        return self.task_manager.wait_for_task(task_id, timeout)
    
    def wait_for_all_tasks(self, timeout: Optional[float] = None) -> List[TaskResult]:
        """Wait for all tasks to complete."""
        return self.task_manager.wait_for_all_tasks(timeout)
    
    def cleanup(self) -> None:
        """Clean up task manager resources."""
        self.task_manager.cleanup()
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get the parameters schema for the task tool."""
        return {
            "type": "object",
            "properties": {
                "subagent_type": {
                    "type": "string",
                    "description": "The type of specialized agent to launch (general-purpose, plan-agent, explore-agent)",
                    "enum": ["general-purpose", "plan-agent", "explore-agent"]
                },
                "description": {
                    "type": "string",
                    "description": "A short (3-5 word) description of the task"
                },
                "prompt": {
                    "type": "string",
                    "description": "The detailed task description for the agent to perform"
                },
                "constraints": {
                    "type": "string",
                    "description": "Optional constraints or limitations for task execution",
                    "default": None
                },
                "output_format": {
                    "type": "string",
                    "description": "Optional output format template for the task result",
                    "default": None
                }
            },
            "required": ["subagent_type", "description", "prompt"]
        }
