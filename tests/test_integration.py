"""Integration tests for Claude Think Tool plugin."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from collections.abc import Generator

from tools.think_tool import ThinkTool
from src.context_manager import ContextManager


class TestThinkToolIntegration:
    """Integration tests for ThinkTool with ContextManager."""

    def test_think_tool_with_context_manager(self):
        """Test that ThinkTool properly uses ContextManager."""
        runtime = Mock()
        runtime.workflow_id = "test-workflow-1"
        tool = ThinkTool(runtime)

        # First thought
        params1 = {"thought": "First thought: Analyze user request"}
        result1 = list(tool._invoke(params1))
        assert len(result1) == 1
        assert "success" in result1[0].content.lower() or "step" in result1[0].content.lower()

        # Second thought
        params2 = {"thought": "Second thought: Check policies"}
        result2 = list(tool._invoke(params2))
        assert len(result2) == 1

        # Verify context accumulation
        context = tool.context_manager.get_context("test-workflow-1")
        assert len(context["thoughts"]) == 2
        assert context["thoughts"][0]["thought"] == "First thought: Analyze user request"
        assert context["thoughts"][1]["thought"] == "Second thought: Check policies"

    def test_multiple_sessions_isolation(self):
        """Test that different sessions maintain separate contexts."""
        runtime1 = Mock()
        runtime1.workflow_id = "workflow-1"
        tool1 = ThinkTool(runtime1)

        runtime2 = Mock()
        runtime2.workflow_id = "workflow-2"
        tool2 = ThinkTool(runtime2)

        # Add thoughts to different sessions
        tool1._invoke({"thought": "Thought in workflow 1"})
        tool2._invoke({"thought": "Thought in workflow 2"})

        # Verify isolation
        context1 = tool1.context_manager.get_context("workflow-1")
        context2 = tool2.context_manager.get_context("workflow-2")

        assert len(context1["thoughts"]) == 1
        assert len(context2["thoughts"]) == 1
        assert context1["thoughts"][0]["thought"] == "Thought in workflow 1"
        assert context2["thoughts"][0]["thought"] == "Thought in workflow 2"

    def test_error_handling_in_integration(self):
        """Test error handling in integrated scenario."""
        runtime = Mock()
        runtime.workflow_id = "test-workflow-error"
        tool = ThinkTool(runtime)

        # Missing parameter
        result = list(tool._invoke({}))
        assert len(result) == 1
        assert "error" in result[0].content.lower() or "required" in result[0].content.lower()

        # Empty thought
        result = list(tool._invoke({"thought": ""}))
        assert len(result) == 1
        assert "error" in result[0].content.lower() or "required" in result[0].content.lower()

        # Valid thought should still work
        result = list(tool._invoke({"thought": "Valid thought"}))
        assert len(result) == 1

    def test_step_numbering(self):
        """Test that steps are numbered correctly across multiple calls."""
        runtime = Mock()
        runtime.workflow_id = "test-workflow-steps"
        tool = ThinkTool(runtime)

        for i in range(1, 6):
            params = {"thought": f"Thought {i}"}
            result = list(tool._invoke(params))
            assert len(result) == 1

        context = tool.context_manager.get_context("test-workflow-steps")
        assert len(context["thoughts"]) == 5
        assert context["metadata"]["total_steps"] == 5

        # Verify step numbers
        for i, thought_entry in enumerate(context["thoughts"], 1):
            assert thought_entry["step"] == i
            assert thought_entry["thought"] == f"Thought {i}"

    def test_context_formatted_output(self):
        """Test formatted context output."""
        runtime = Mock()
        runtime.workflow_id = "test-workflow-format"
        tool = ThinkTool(runtime)

        # Add multiple thoughts
        for thought in ["Thought A", "Thought B", "Thought C"]:
            list(tool._invoke({"thought": thought}))

        # Get formatted context
        formatted = tool.context_manager.get_formatted_context("test-workflow-format")

        assert "Previous thoughts" in formatted
        assert "Thought A" in formatted
        assert "Thought B" in formatted
        assert "Thought C" in formatted
        assert "Step 1" in formatted
        assert "Step 2" in formatted
        assert "Step 3" in formatted


class TestMultiStepWorkflow:
    """Test multi-step workflow scenarios."""

    def test_policy_check_workflow(self):
        """Simulate a policy-check workflow."""
        runtime = Mock()
        runtime.workflow_id = "policy-workflow"
        tool = ThinkTool(runtime)

        # Step 1: Initial analysis
        list(tool._invoke({"thought": "User wants to cancel. Need to verify: user ID, reservation ID"}))
        
        # Step 2: After getting info
        list(tool._invoke({"thought": "Got reservation. Booking was 48h ago. Check cancellation policy."}))
        
        # Step 3: Policy check
        list(tool._invoke({"thought": "Policy check: Outside 24h window, but user has insurance. Can cancel."}))
        
        # Step 4: Final validation
        list(tool._invoke({"thought": "All checks passed. Ready to process cancellation."}))

        context = tool.context_manager.get_context("policy-workflow")
        assert len(context["thoughts"]) == 4
        assert context["metadata"]["total_steps"] == 4

    def test_decision_making_workflow(self):
        """Simulate a decision-making workflow."""
        runtime = Mock()
        runtime.workflow_id = "decision-workflow"
        tool = ThinkTool(runtime)

        # Step 1: List options
        list(tool._invoke({"thought": "Options: A (fast, expensive), B (slow, cheap), C (medium, medium)"}))
        
        # Step 2: Evaluate
        list(tool._invoke({"thought": "User needs speed. Eliminate B. Between A and C, A is faster but more expensive."}))
        
        # Step 3: Decision
        list(tool._invoke({"thought": "Decision: Choose A because speed is priority and cost is acceptable."}))

        context = tool.context_manager.get_context("decision-workflow")
        assert len(context["thoughts"]) == 3
