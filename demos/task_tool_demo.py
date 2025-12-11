"""
Demo: Task Tool Usage - Parallel Multi-Agent Tasks

This demo shows how to use the Task Tool to create and manage subagents
that can execute tasks in parallel.
"""

import sys
import os
import time

# Add parent directory to path to import claude_code
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_code import ClaudeCode


def demo_single_task():
    """Demo: Create a single task with a subagent."""
    print("=" * 70)
    print("DEMO 1: Single Task Execution")
    print("=" * 70)
    
    with ClaudeCode() as claude:
        # Create a task with a plan-agent to analyze requirements
        print("\n1. Creating a planning task...")
        result = claude.create_task(
            subagent_type="plan-agent",
            description="Plan API endpoint implementation",
            prompt="""
            I need to implement a REST API endpoint for user authentication.
            The endpoint should handle login, registration, and token refresh.
            Please provide a detailed implementation plan.
            """,
            constraints="Use Python with FastAPI, include proper error handling and security measures"
        )
        
        if result.success:
            task_id = result.data["task_id"]
            print(f"   ✓ Task created: {task_id}")
            print(f"   Status: {result.data['status']}")
            
            # Wait for task completion
            print("\n2. Waiting for task completion...")
            task_result = claude.wait_for_task(task_id, timeout=30)
            
            if task_result and task_result.success:
                task_data = task_result.data
                print(f"   ✓ Task completed!")
                print(f"   Agent Type: {task_data['agent_type']}")
                print(f"   Status: {task_data['status']}")
                if task_data.get('result', {}).get('data', {}).get('plan'):
                    print(f"\n   Generated Plan:")
                    print(f"   {task_data['result']['data']['plan'][:200]}...")
        else:
            print(f"   ✗ Failed: {result.error}")


def demo_parallel_tasks():
    """Demo: Create multiple tasks that run in parallel."""
    print("\n" + "=" * 70)
    print("DEMO 2: Parallel Task Execution")
    print("=" * 70)
    
    with ClaudeCode() as claude:
        print("\n1. Creating multiple parallel tasks...")
        
        # Task 1: Explore codebase
        task1 = claude.create_task(
            subagent_type="explore-agent",
            description="Explore project structure",
            prompt="Analyze the current project structure and identify key components, patterns, and architecture."
        )
        
        # Task 2: Plan a feature
        task2 = claude.create_task(
            subagent_type="plan-agent",
            description="Plan database integration",
            prompt="Plan the integration of a PostgreSQL database with proper ORM setup and migration strategy."
        )
        
        # Task 3: Research implementation
        task3 = claude.create_task(
            subagent_type="general-purpose",
            description="Research authentication methods",
            prompt="Research and compare JWT vs session-based authentication for a web API, including security considerations."
        )
        
        task_ids = []
        if task1.success:
            task_ids.append(task1.data["task_id"])
            print(f"   ✓ Task 1 (Explore): {task1.data['task_id']}")
        if task2.success:
            task_ids.append(task2.data["task_id"])
            print(f"   ✓ Task 2 (Plan): {task2.data['task_id']}")
        if task3.success:
            task_ids.append(task3.data["task_id"])
            print(f"   ✓ Task 3 (Research): {task3.data['task_id']}")
        
        print(f"\n2. All tasks are running in parallel...")
        print(f"   (Tasks executing concurrently in background threads)")
        
        # Wait for all tasks to complete
        print("\n3. Waiting for all tasks to complete...")
        all_tasks = claude.wait_for_all_tasks(timeout=60)
        
        print(f"\n4. Task Results:")
        for i, task in enumerate(all_tasks, 1):
            print(f"\n   Task {i} ({task['agent_type']}):")
            print(f"   - ID: {task['task_id']}")
            print(f"   - Status: {task['status']}")
            if task['status'] == 'completed':
                print(f"   - Result: Success")
            elif task['status'] == 'failed':
                print(f"   - Error: {task.get('error', 'Unknown error')}")


def demo_general_purpose_agent():
    """Demo: Using the general-purpose agent for complex tasks."""
    print("\n" + "=" * 70)
    print("DEMO 3: General-Purpose Agent (Complex Multi-Step Task)")
    print("=" * 70)
    
    with ClaudeCode() as claude:
        print("\n1. Creating a complex multi-step task...")
        
        # Create a task that would involve multiple steps
        result = claude.create_task(
            subagent_type="general-purpose",
            description="Analyze and refactor auth module",
            prompt="""
            I need to analyze the current authentication module and refactor it for better security.
            Please:
            1. First explore the current auth-related files
            2. Identify security vulnerabilities
            3. Suggest improvements
            4. Create a refactoring plan
            """,
            constraints="Focus on security best practices and maintain backward compatibility"
        )
        
        if result.success:
            task_id = result.data["task_id"]
            print(f"   ✓ Task created: {task_id}")
            
            # Wait for completion
            print("\n2. Executing multi-step task...")
            task_result = claude.wait_for_task(task_id, timeout=30)
            
            if task_result and task_result.success:
                task_data = task_result.data
                print(f"   ✓ Task completed!")
                print(f"   Agent: {task_data['agent_type']}")
                print(f"   Result: {task_data['result']['data']['result'][:150]}...")


def demo_bash_integration():
    """Demo: Using bash tool alongside Task Tool."""
    print("\n" + "=" * 70)
    print("DEMO 4: Bash Tool Integration with Task Tool")
    print("=" * 70)
    
    with ClaudeCode() as claude:
        print("\n1. Executing bash command to check project structure...")
        
        # Use bash tool to explore the project
        result = claude.execute_bash(
            command="ls -la",
            description="List files in current directory"
        )
        
        if result.success:
            print(f"   ✓ Command executed successfully")
            print(f"   Files found: {len(result.data.get('stdout', '').split())} items")
        
        # Create a task based on the findings
        print("\n2. Creating task based on filesystem analysis...")
        task_result = claude.create_task(
            subagent_type="explore-agent",
            description="Analyze project structure",
            prompt="Based on the file listing, analyze the project structure and identify the main components and their purposes."
        )
        
        if task_result.success:
            task_id = task_result.data["task_id"]
            claude.wait_for_task(task_id, timeout=20)
            print(f"   ✓ Analysis task completed")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("CLAUDE CODE PYTHON - TASK TOOL DEMO")
    print("Parallel Multi-Agent Task Execution")
    print("=" * 70)
    
    try:
        # Run all demos
        demo_single_task()
        demo_parallel_tasks()
        demo_general_purpose_agent()
        demo_bash_integration()
        
        print("\n" + "=" * 70)
        print("ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nKey Features Demonstrated:")
        print("  ✓ Task Tool with subagent support")
        print("  ✓ Three agent types: general-purpose, plan-agent, explore-agent")
        print("  ✓ Parallel task execution")
        print("  ✓ Bash tool integration")
        print("  ✓ Task status monitoring and synchronization")
        
    except Exception as e:
        print(f"\n✗ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
