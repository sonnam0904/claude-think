"""Tests for ContextManager."""

import pytest
from datetime import datetime, timedelta
from src.context_manager import ContextManager


class TestContextManager:
    """Test suite for ContextManager."""

    def test_init(self):
        """Test ContextManager initialization."""
        cm = ContextManager(max_thoughts=50)
        assert cm.max_thoughts == 50
        assert len(cm._contexts) == 0

    def test_get_context_new_session(self):
        """Test getting context for a new session."""
        cm = ContextManager()
        session_id = "test-session-1"
        context = cm.get_context(session_id)

        assert context["session_id"] == session_id
        assert context["thoughts"] == []
        assert context["metadata"]["total_steps"] == 0
        assert "created_at" in context["metadata"]

    def test_add_thought(self):
        """Test adding a thought to context."""
        cm = ContextManager()
        session_id = "test-session-2"
        thought = "This is a test thought"

        step = cm.add_thought(session_id, thought)

        assert step == 1
        context = cm.get_context(session_id)
        assert len(context["thoughts"]) == 1
        assert context["thoughts"][0]["thought"] == thought
        assert context["thoughts"][0]["step"] == 1

    def test_add_multiple_thoughts(self):
        """Test adding multiple thoughts."""
        cm = ContextManager()
        session_id = "test-session-3"

        thoughts = ["Thought 1", "Thought 2", "Thought 3"]
        for i, thought in enumerate(thoughts, 1):
            step = cm.add_thought(session_id, thought)
            assert step == i

        context = cm.get_context(session_id)
        assert len(context["thoughts"]) == 3
        assert context["metadata"]["total_steps"] == 3

    def test_max_thoughts_limit(self):
        """Test max thoughts limit enforcement."""
        cm = ContextManager(max_thoughts=3)
        session_id = "test-session-4"

        # Add 5 thoughts, but max is 3
        for i in range(5):
            cm.add_thought(session_id, f"Thought {i+1}")

        context = cm.get_context(session_id)
        assert len(context["thoughts"]) == 3  # Should only keep last 3
        assert context["thoughts"][0]["thought"] == "Thought 3"  # Oldest kept
        assert context["thoughts"][-1]["thought"] == "Thought 5"  # Newest

    def test_get_all_thoughts(self):
        """Test retrieving all thoughts."""
        cm = ContextManager()
        session_id = "test-session-5"

        thoughts = ["Thought A", "Thought B"]
        for thought in thoughts:
            cm.add_thought(session_id, thought)

        all_thoughts = cm.get_all_thoughts(session_id)
        assert len(all_thoughts) == 2
        assert all_thoughts[0]["thought"] == "Thought A"
        assert all_thoughts[1]["thought"] == "Thought B"

    def test_get_formatted_context(self):
        """Test formatted context string."""
        cm = ContextManager()
        session_id = "test-session-6"

        cm.add_thought(session_id, "First thought")
        formatted = cm.get_formatted_context(session_id)

        assert "Previous thoughts" in formatted
        assert "First thought" in formatted
        assert "Step 1" in formatted

    def test_get_formatted_context_empty(self):
        """Test formatted context for empty session."""
        cm = ContextManager()
        session_id = "test-session-7"

        formatted = cm.get_formatted_context(session_id)
        assert "No thoughts yet" in formatted

    def test_clear_context(self):
        """Test clearing context."""
        cm = ContextManager()
        session_id = "test-session-8"

        cm.add_thought(session_id, "Some thought")
        assert len(cm._contexts) == 1

        cm.clear_context(session_id)
        assert session_id not in cm._contexts

    def test_get_context_summary(self):
        """Test getting context summary."""
        cm = ContextManager()
        session_id = "test-session-9"

        cm.add_thought(session_id, "Thought 1")
        cm.add_thought(session_id, "Thought 2")

        summary = cm.get_context_summary(session_id)
        assert summary["session_id"] == session_id
        assert summary["total_steps"] == 2
        assert "created_at" in summary
        assert "last_updated" in summary

