"""File tool for reading, writing, and searching files."""

import os
from typing import Optional, List, Dict, Any
from .base import BaseTool, ToolResult


class FileTool(BaseTool):
    """Tool for file operations (read, write, search)."""
    
    def __init__(self):
        super().__init__(
            name="file_tool",
            description="Read, write, and search files in the filesystem"
        )
    
    def execute(self, action: str, file_path: str, content: Optional[str] = None, 
                pattern: Optional[str] = None, limit: Optional[int] = None) -> ToolResult:
        """
        Execute file operations.
        
        Args:
            action: Operation to perform (read, write, search, list)
            file_path: Path to the file or directory
            content: Content to write (for write action)
            pattern: Search pattern (for search action)
            limit: Limit for search results or read lines
            
        Returns:
            ToolResult with operation results
        """
        try:
            if action == "read":
                return self._read_file(file_path, limit)
            elif action == "write":
                return self._write_file(file_path, content or "")
            elif action == "search":
                return self._search_in_file(file_path, pattern or "", limit)
            elif action == "list":
                return self._list_directory(file_path)
            else:
                return ToolResult(
                    success=False,
                    error=f"Unknown action: {action}. Supported: read, write, search, list"
                )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"File operation failed: {str(e)}"
            )
    
    def _read_file(self, file_path: str, limit: Optional[int] = None) -> ToolResult:
        """Read a file."""
        if not os.path.exists(file_path):
            return ToolResult(success=False, error=f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            return ToolResult(success=False, error=f"Not a file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if limit:
                    lines = []
                    for i, line in enumerate(f):
                        if i >= limit:
                            break
                        lines.append(line)
                    content = ''.join(lines)
                else:
                    content = f.read()
            
            return ToolResult(
                success=True,
                data={
                    "content": content,
                    "file_path": file_path,
                    "size": len(content)
                },
                metadata={
                    "file_path": file_path,
                    "action": "read"
                }
            )
        except Exception as e:
            return ToolResult(success=False, error=f"Failed to read file: {str(e)}")
    
    def _write_file(self, file_path: str, content: str) -> ToolResult:
        """Write content to a file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return ToolResult(
                success=True,
                data={
                    "file_path": file_path,
                    "size": len(content),
                    "message": f"Successfully wrote to {file_path}"
                },
                metadata={
                    "file_path": file_path,
                    "action": "write"
                }
            )
        except Exception as e:
            return ToolResult(success=False, error=f"Failed to write file: {str(e)}")
    
    def _search_in_file(self, file_path: str, pattern: str, limit: Optional[int] = None) -> ToolResult:
        """Search for pattern in a file."""
        if not os.path.exists(file_path):
            return ToolResult(success=False, error=f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            matches = []
            for i, line in enumerate(lines):
                if pattern in line:
                    matches.append({
                        "line_number": i + 1,
                        "content": line.strip(),
                        "line": i
                    })
                    if limit and len(matches) >= limit:
                        break
            
            return ToolResult(
                success=True,
                data={
                    "matches": matches,
                    "total_matches": len(matches),
                    "pattern": pattern,
                    "file_path": file_path
                },
                metadata={
                    "file_path": file_path,
                    "pattern": pattern,
                    "action": "search"
                }
            )
        except Exception as e:
            return ToolResult(success=False, error=f"Failed to search file: {str(e)}")
    
    def _list_directory(self, dir_path: str) -> ToolResult:
        """List directory contents."""
        if not os.path.exists(dir_path):
            return ToolResult(success=False, error=f"Directory not found: {dir_path}")
        
        if not os.path.isdir(dir_path):
            return ToolResult(success=False, error=f"Not a directory: {dir_path}")
        
        try:
            items = []
            for item in os.listdir(dir_path):
                full_path = os.path.join(dir_path, item)
                items.append({
                    "name": item,
                    "type": "directory" if os.path.isdir(full_path) else "file",
                    "size": os.path.getsize(full_path) if os.path.isfile(full_path) else 0
                })
            
            return ToolResult(
                success=True,
                data={
                    "directory": dir_path,
                    "items": items,
                    "total_items": len(items)
                },
                metadata={
                    "directory": dir_path,
                    "action": "list"
                }
            )
        except Exception as e:
            return ToolResult(success=False, error=f"Failed to list directory: {str(e)}")
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get the parameters schema."""
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "File operation to perform",
                    "enum": ["read", "write", "search", "list"]
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the file or directory"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write (for write action)",
                    "default": None
                },
                "pattern": {
                    "type": "string",
                    "description": "Search pattern (for search action)",
                    "default": None
                },
                "limit": {
                    "type": "integer",
                    "description": "Limit for results or lines",
                    "default": None
                }
            },
            "required": ["action", "file_path"]
        }
