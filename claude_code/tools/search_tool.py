"""Search tool for searching patterns across files."""

import os
import re
from typing import Optional, List, Dict, Any
from .base import BaseTool, ToolResult


class SearchTool(BaseTool):
    """Tool for searching patterns across multiple files."""
    
    def __init__(self):
        super().__init__(
            name="search_tool",
            description="Search for patterns across files and directories"
        )
    
    def execute(self, pattern: str, path: str = ".", include: Optional[str] = None, 
                max_results: int = 100) -> ToolResult:
        """
        Search for pattern in files.
        
        Args:
            pattern: Regular expression pattern to search for
            path: Directory or file path to search in
            include: Glob pattern to filter files (e.g., '*.py', '*.js')
            max_results: Maximum number of results to return
            
        Returns:
            ToolResult with search results
        """
        try:
            results = []
            
            if os.path.isfile(path):
                # Search in a single file
                file_results = self._search_in_file(path, pattern)
                if file_results:
                    results.extend(file_results)
            elif os.path.isdir(path):
                # Search recursively in directory
                results = self._search_in_directory(path, pattern, include, max_results)
            else:
                return ToolResult(success=False, error=f"Path not found: {path}")
            
            # Limit results
            if len(results) > max_results:
                results = results[:max_results]
                truncated = True
            else:
                truncated = False
            
            return ToolResult(
                success=True,
                data={
                    "pattern": pattern,
                    "path": path,
                    "results": results,
                    "total_matches": len(results),
                    "truncated": truncated
                },
                metadata={
                    "pattern": pattern,
                    "search_path": path,
                    "total_files_searched": len(set(r["file"] for r in results))
                }
            )
            
        except re.error as e:
            return ToolResult(success=False, error=f"Invalid regex pattern: {str(e)}")
        except Exception as e:
            return ToolResult(success=False, error=f"Search failed: {str(e)}")
    
    def _search_in_file(self, file_path: str, pattern: str) -> List[Dict[str, Any]]:
        """Search for pattern in a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            results = []
            regex = re.compile(pattern)
            
            for i, line in enumerate(lines):
                if regex.search(line):
                    results.append({
                        "file": file_path,
                        "line_number": i + 1,
                        "line_content": line.strip(),
                        "match": regex.search(line).group() if regex.search(line) else None
                    })
            
            return results
        except Exception:
            return []  # Skip files that can't be read
    
    def _search_in_directory(self, dir_path: str, pattern: str, 
                           include: Optional[str], max_results: int) -> List[Dict[str, Any]]:
        """Search recursively in a directory."""
        results = []
        
        # File extensions to search
        search_extensions = None
        if include:
            # Parse glob pattern (simple version)
            if include.startswith("*."):
                ext = include[1:]  # Remove '*'
                search_extensions = [ext]
        else:
            # Default: search common text files
            search_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', 
                               '.md', '.txt', '.json', '.xml', '.yaml', '.yml', '.html', '.css', '.scss']
        
        for root, dirs, files in os.walk(dir_path):
            # Skip common directories to ignore
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', 'venv', '.venv']]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check file extension
                if search_extensions:
                    if not any(file.endswith(ext) for ext in search_extensions):
                        continue
                
                file_results = self._search_in_file(file_path, pattern)
                results.extend(file_results)
                
                # Check if we've reached max results
                if len(results) >= max_results:
                    return results
        
        return results
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get the parameters schema."""
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regular expression pattern to search for"
                },
                "path": {
                    "type": "string",
                    "description": "Directory or file path to search in",
                    "default": "."
                },
                "include": {
                    "type": "string",
                    "description": "Glob pattern to filter files (e.g., '*.py', '*.js')",
                    "default": None
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 100
                }
            },
            "required": ["pattern"]
        }
