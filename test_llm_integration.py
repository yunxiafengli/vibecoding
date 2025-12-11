"""
Test LLM integration with Claude Code Python.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_code import ClaudeCode


def test_llm_direct():
    """Test direct LLM call."""
    print("Testing direct LLM call...")
    from claude_code.llm_client import LLMClient
    
    try:
        client = LLMClient()
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is 2+2?"}
            ],
            temperature=0.3
        )
        print(f"✓ LLM Response: {response.choices[0].message.content[:100]}...")
        return True
    except Exception as e:
        print(f"✗ LLM test failed: {str(e)}")
        return False


def test_plan_agent_with_llm():
    """Test PlanAgent with LLM."""
    print("\nTesting PlanAgent with LLM...")
    
    with ClaudeCode() as claude:
        try:
            result = claude.create_task(
                subagent_type="plan-agent",
                description="Test LLM planning",
                prompt="Plan a simple Python function to calculate factorial"
            )
            
            if result.success:
                task_id = result.data["task_id"]
                task_result = claude.wait_for_task(task_id, timeout=30)
                
                if task_result.success and task_result.data["status"] == "completed":
                    plan = task_result.data.get("result", {}).get("data", {}).get("plan", "")
                    print(f"✓ PlanAgent generated plan: {plan[:150]}...")
                    return True
                else:
                    print(f"✗ Task failed: {task_result.data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"✗ Task creation failed: {result.error}")
                return False
        except Exception as e:
            print(f"✗ PlanAgent test failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def test_general_agent_with_llm():
    """Test GeneralPurposeAgent with LLM and tools."""
    print("\nTesting GeneralPurposeAgent with LLM and tools...")
    
    with ClaudeCode() as claude:
        try:
            # Create a task that might use tools
            result = claude.create_task(
                subagent_type="general-purpose",
                description="Analyze project structure",
                prompt="What files are in the current directory? Use the bash tool to check."
            )
            
            if result.success:
                task_id = result.data["task_id"]
                task_result = claude.wait_for_task(task_id, timeout=30)
                
                if task_result.success and task_result.data["status"] == "completed":
                    print(f"✓ GeneralPurposeAgent completed task")
                    print(f"  Result: {task_result.data.get('result', {}).get('data', {})}")
                    return True
                else:
                    print(f"✗ Task failed: {task_result.data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"✗ Task creation failed: {result.error}")
                return False
        except Exception as e:
            print(f"✗ GeneralPurposeAgent test failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Run all LLM integration tests."""
    print("=" * 70)
    print("TESTING LLM INTEGRATION")
    print("=" * 70)
    
    tests = [
        test_llm_direct,
        test_plan_agent_with_llm,
        test_general_agent_with_llm,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ Test {test.__name__} crashed: {str(e)}")
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 70)
    
    if passed == total:
        print("\n✓ All LLM integration tests passed!")
        print("\nThe agents are now using real LLM instead of simulation.")
        return 0
    else:
        print(f"\n✗ {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
