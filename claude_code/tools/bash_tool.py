"""Bash tool for executing shell commands."""

import subprocess
import os
import platform
from typing import Optional, Dict, Any
from .base import BaseTool, ToolResult


class BashTool(BaseTool):
    """Tool for executing bash/shell commands."""
    
    def __init__(self):
        super().__init__(
            name="run_shell_command",
            description="Execute shell commands with safety checks and output capture"
        )
    
    def execute(self, command: str, description: str, dir_path: Optional[str] = None) -> ToolResult:
        """
        Execute a shell command.
        
        Args:
            command: The command to execute
            description: Brief description of the command's purpose
            dir_path: Optional directory to run the command in
            
        Returns:
            ToolResult with command output and metadata
        """
        try:
            print(f"Executing: {description}")
            print(f"Command: {command}")
            
            # Determine shell based on OS
            is_windows = platform.system() == "Windows"
            
            # Set working directory
            cwd = dir_path if dir_path else os.getcwd()
            if not os.path.isdir(cwd):
                return ToolResult(
                    success=False,
                    error=f"Directory does not exist: {cwd}"
                )
            
            # Execute command
            if is_windows:
                # On Windows, handle mkdir specially (remove -p flag which doesn't exist on Windows)
                if command.startswith('mkdir '):
                    # Remove -p flag
                    dirs_command = command.replace('mkdir -p ', '').replace('mkdir ', '').strip()
                    # Convert space-separated directories to comma-separated for PowerShell
                    # PowerShell mkdir supports: mkdir dir1,dir2,dir3
                    dirs_command = dirs_command.replace(' ', ',')
                    # Use PowerShell's native mkdir which supports multiple directories
                    command = f'powershell -Command "mkdir {dirs_command}"'
                
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                # On Unix-like systems
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            # Get output
            stdout, stderr = process.communicate()
            exit_code = process.returncode
            
            # Prepare result data
            data = {
                "stdout": stdout or "(empty)",
                "stderr": stderr or "(empty)",
                "exit_code": exit_code,
                "command": command,
                "directory": cwd
            }
            
            success = exit_code == 0
            error = stderr if not success else None
            
            return ToolResult(
                success=success,
                data=data,
                error=error,
                metadata={
                    "exit_code": exit_code,
                    "executed_in": cwd,
                    "command": command
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to execute command: {str(e)}"
            )
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get the parameters schema for the bash tool."""
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute"
                },
                "description": {
                    "type": "string", 
                    "description": "Brief description of the command's purpose"
                },
                "dir_path": {
                    "type": "string",
                    "description": "Optional directory path to run the command in",
                    "default": None
                }
            },
            "required": ["command", "description"]
        }
