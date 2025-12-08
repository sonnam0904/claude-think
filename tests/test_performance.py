"""Performance tests for Claude Think Tool plugin."""

import pytest
import time
from unittest.mock import Mock
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from tools.think_tool import ThinkTool
from src.context_manager import ContextManager
from src.config import PluginConfig, set_config


class TestPerformance:
    """Performance tests."""

    def test_context_manager_performance(self):
        """Test context manager performance with many thoughts."""
        cm = ContextManager(max_thoughts=1000)
        session_id = "perf-test-session"

        # Add many thoughts and measure time
        start_time = time.time()
        for i in range(100):
            cm.add_thought(session_id, f"Thought {i}")
        elapsed = time.time() - start_time

        # Should complete 100 additions in reasonable time (< 1 second)
        assert elapsed < 1.0, f"Took too long: {elapsed:.3f}s"
        assert len(cm.get_all_thoughts(session_id)) == 100

    def test_concurrent_access(self):
        """Test thread-safe concurrent access to context manager."""
        cm = ContextManager()
        session_id = "concurrent-test"
        
        def add_thoughts(start_idx: int, count: int):
            """Add thoughts in a thread."""
            for i in range(start_idx, start_idx + count):
                cm.add_thought(session_id, f"Thought {i}")

        # Run concurrent operations
        num_threads = 10
        thoughts_per_thread = 10
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(
                    add_thoughts, i * thoughts_per_thread, thoughts_per_thread
                )
                for i in range(num_threads)
            ]
            # Wait for all to complete
            for future in as_completed(futures):
                future.result()

        # Verify all thoughts were added
        thoughts = cm.get_all_thoughts(session_id)
        assert len(thoughts) == num_threads * thoughts_per_thread

    def test_large_thought_performance(self):
        """Test performance with large thoughts."""
        cm = ContextManager()
        session_id = "large-thought-test"
        
        # Create a large thought (1000 characters)
        large_thought = "A" * 1000
        
        start_time = time.time()
        cm.add_thought(session_id, large_thought)
        elapsed = time.time() - start_time
        
        # Should complete quickly even with large thought
        assert elapsed < 0.1, f"Took too long: {elapsed:.3f}s"
        assert cm.get_all_thoughts(session_id)[0]["thought"] == large_thought

    def test_memory_efficiency(self):
        """Test that old thoughts are properly cleaned up."""
        config = PluginConfig(max_thoughts=10)
        set_config(config)
        
        cm = ContextManager(max_thoughts=10)
        session_id = "memory-test"
        
        # Add more thoughts than max
        for i in range(20):
            cm.add_thought(session_id, f"Thought {i}")
        
        # Should only keep last 10
        thoughts = cm.get_all_thoughts(session_id)
        assert len(thoughts) == 10
        assert thoughts[0]["thought"] == "Thought 10"  # First kept thought
        assert thoughts[-1]["thought"] == "Thought 19"  # Last thought

    def test_cleanup_performance(self):
        """Test cleanup performance with many sessions."""
        cm = ContextManager()
        
        # Create many sessions
        num_sessions = 100
        for i in range(num_sessions):
            session_id = f"session-{i}"
            cm.add_thought(session_id, f"Thought for session {i}")
        
        # Cleanup should be fast
        start_time = time.time()
        cleaned = cm.cleanup_old_sessions(max_age_hours=-1)  # Clean all (negative hours)
        elapsed = time.time() - start_time
        
        assert cleaned == num_sessions
        assert elapsed < 1.0, f"Cleanup took too long: {elapsed:.3f}s"

    def test_get_context_performance(self):
        """Test get_context performance."""
        cm = ContextManager()
        session_id = "get-context-test"
        
        # Pre-populate context
        for i in range(50):
            cm.add_thought(session_id, f"Thought {i}")
        
        # Measure get_context time
        start_time = time.time()
        for _ in range(1000):
            cm.get_context(session_id)
        elapsed = time.time() - start_time
        
        # Should be very fast (< 0.1s for 1000 calls)
        assert elapsed < 0.1, f"get_context too slow: {elapsed:.3f}s"

    def test_formatted_context_performance(self):
        """Test formatted context generation performance."""
        cm = ContextManager()
        session_id = "format-test"
        
        # Add many thoughts
        for i in range(50):
            cm.add_thought(session_id, f"Thought {i}: " + "A" * 100)
        
        # Measure formatting time
        start_time = time.time()
        formatted = cm.get_formatted_context(session_id)
        elapsed = time.time() - start_time
        
        # Should format quickly (< 0.1s)
        assert elapsed < 0.1, f"Formatting took too long: {elapsed:.3f}s"
        assert "Thought" in formatted
        assert len(formatted) > 0

