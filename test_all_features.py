"""
Comprehensive test of all Claude Code Python features.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_code import ClaudeCode


def test_bash_tool():
    """Test bash tool functionality."""
    print("Testing Bash Tool...")
    with ClaudeCode() as claude:
        # Test simple command
        result = claude.execute_bash("echo Hello World", "Test echo command")
        assert result.success, f"Bash tool failed: {result.error}"
        assert "Hello World" in result.data["stdout"], "Echo command output incorrect"
        print("  ✓ Bash tool works correctly")


def test_file_tool():
    """Test file tool functionality."""
    print("Testing File Tool...")
    with ClaudeCode() as claude:
        # Test read
        result = claude.read_file("README.md", limit=5)
        assert result.success, f"File read failed: {result.error}"
        assert "Claude Code Python" in result.data["content"], "File content incorrect"
        
        # Test write
        test_content = "Test content"
        result = claude.write_file("test_file.txt", test_content)
        assert result.success, f"File write failed: {result.error}"
        
        # Verify write
        result = claude.read_file("test_file.txt")
        assert result.success, f"File read after write failed: {result.error}"
        assert result.data["content"] == test_content, "File content mismatch after write"
        
        # Cleanup
        os.remove("test_file.txt")
        print("  ✓ File tool works correctly")


def test_search_tool():
    """Test search tool functionality."""
    print("Testing Search Tool...")
    with ClaudeCode() as claude:
        # Search for class definitions
        result = claude.search_files("class.*Tool", include="*.py")
        assert result.success, f"Search failed: {result.error}"
        assert result.data["total_matches"] > 0, "No matches found"
        print(f"  ✓ Search tool found {result.data['total_matches']} matches")


def test_task_tool():
    """Test task tool with subagents."""
    print("Testing Task Tool...")
    with ClaudeCode() as claude:
        # Test plan agent
        result = claude.create_task(
            subagent_type="plan-agent",
            description="Test planning",
            prompt="Plan a simple function implementation"
        )
        assert result.success, f"Task creation failed: {result.error}"
        task_id = result.data["task_id"]
        
        # Wait for completion
        task_result = claude.wait_for_task(task_id, timeout=30)
        assert task_result.success, f"Task execution failed"
        assert task_result.data["status"] == "completed", "Task not completed"
        print("  ✓ Plan agent works correctly")
        
        # Test explore agent
        result = claude.create_task(
            subagent_type="explore-agent",
            description="Test exploration",
            prompt="Explore the tools directory structure"
        )
        assert result.success, f"Explore task creation failed: {result.error}"
        task_id = result.data["task_id"]
        
        task_result = claude.wait_for_task(task_id, timeout=30)
        assert task_result.success, f"Explore task execution failed"
        assert task_result.data["status"] == "completed", "Explore task not completed"
        print("  ✓ Explore agent works correctly")
        
        # Test general-purpose agent
        result = claude.create_task(
            subagent_type="general-purpose",
            description="Test general task",
            prompt="Analyze the project structure"
        )
        assert result.success, f"General task creation failed: {result.error}"
        task_id = result.data["task_id"]
        
        task_result = claude.wait_for_task(task_id, timeout=30)
        assert task_result.success, f"General task execution failed"
        assert task_result.data["status"] == "completed", "General task not completed"
        print("  ✓ General-purpose agent works correctly")


def test_parallel_tasks():
    """Test parallel task execution."""
    print("Testing Parallel Task Execution...")
    with ClaudeCode() as claude:
        # Create multiple tasks
        tasks = []
        for i in range(3):
            result = claude.create_task(
                subagent_type="plan-agent",
                description=f"Parallel task {i+1}",
                prompt=f"Plan implementation of feature {i+1}"
            )
            assert result.success, f"Task {i+1} creation failed"
            tasks.append(result.data["task_id"])
        
        # Wait for all tasks
        all_tasks = claude.wait_for_all_tasks(timeout=60)
        assert len(all_tasks) == 3, f"Expected 3 tasks, got {len(all_tasks)}"
        
        for task in all_tasks:
            assert task["status"] == "completed", f"Task {task['task_id']} not completed"
        
        print(f"  ✓ All {len(tasks)} tasks executed in parallel successfully")


def main():
    """Run all tests."""
    print("=" * 60)
    print("CLAUDE CODE PYTHON - COMPREHENSIVE TEST")
    print("=" * 60)
    
    try:
        test_bash_tool()
        test_file_tool()
        test_search_tool()
        test_task_tool()
        test_parallel_tasks()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nFeatures verified:")
        print("  ✓ Bash tool for command execution")
        print("  ✓ File tool for read/write operations")
        print("  ✓ Search tool for pattern matching")
        print("  ✓ Task tool with subagent support")
        print("  ✓ Three agent types (general-purpose, plan, explore)")
        print("  ✓ Parallel task execution")
        print("  ✓ Task status monitoring")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
