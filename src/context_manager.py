"""Context Manager for accumulating thoughts across tool calls."""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import threading
import time

from src.config import get_config

logger = logging.getLogger(__name__)


class ContextManager:
    """
    Manages context accumulation for think tool.
    Stores thoughts per session/workflow.
    Thread-safe implementation with automatic cleanup.
    """

    def __init__(self, max_thoughts: Optional[int] = None):
        """
        Initialize ContextManager.

        Args:
            max_thoughts: Maximum number of thoughts per session (uses config if None)
        """
        config = get_config()
        # In-memory storage (can be replaced with persistent storage)
        self._contexts: Dict[str, Dict] = {}
        # Thread lock for thread-safety
        self._lock = threading.RLock()
        # Max thoughts per session (configurable)
        self.max_thoughts = max_thoughts if max_thoughts is not None else config.max_thoughts
        self.cleanup_interval_hours = config.cleanup_interval_hours
        self.enable_auto_cleanup = config.enable_auto_cleanup
        self.max_thought_length = config.max_thought_length
        
        # Auto cleanup thread (if enabled)
        self._cleanup_thread: Optional[threading.Thread] = None
        self._stop_cleanup = threading.Event()
        
        if self.enable_auto_cleanup:
            self._start_cleanup_thread()
        
        logger.info(
            f"ContextManager initialized: max_thoughts={self.max_thoughts}, "
            f"cleanup_interval={self.cleanup_interval_hours}h, "
            f"auto_cleanup={self.enable_auto_cleanup}"
        )
    
    def _start_cleanup_thread(self) -> None:
        """Start background cleanup thread."""
        def cleanup_worker():
            while not self._stop_cleanup.wait(self.cleanup_interval_hours * 3600):
                try:
                    cleaned = self.cleanup_old_sessions(self.cleanup_interval_hours)
                    if cleaned > 0:
                        logger.info(f"Auto-cleanup: Removed {cleaned} old session(s)")
                except Exception as e:
                    logger.error(f"Error in auto-cleanup: {e}", exc_info=True)
        
        self._cleanup_thread = threading.Thread(
            target=cleanup_worker, daemon=True, name="ContextManager-Cleanup"
        )
        self._cleanup_thread.start()
        logger.debug("Auto-cleanup thread started")
    
    def shutdown(self) -> None:
        """Shutdown the context manager and cleanup thread."""
        if self._cleanup_thread:
            self._stop_cleanup.set()
            self._cleanup_thread.join(timeout=5)
            logger.info("ContextManager shutdown complete")

    def get_context(self, session_id: str) -> Dict:
        """
        Get or create context for a session (thread-safe).

        Args:
            session_id: Unique session identifier

        Returns:
            Dict containing session context
        """
        with self._lock:
            if session_id not in self._contexts:
                self._contexts[session_id] = {
                    "session_id": session_id,
                    "thoughts": [],
                    "metadata": {
                        "created_at": datetime.utcnow().isoformat(),
                        "last_updated": datetime.utcnow().isoformat(),
                        "total_steps": 0,
                    },
                }
                logger.debug(f"Created new context for session: {session_id}")
            return self._contexts[session_id]

    def add_thought(
        self, session_id: str, thought: str, context: Optional[Dict] = None
    ) -> int:
        """
        Add a thought to the context (thread-safe).

        Args:
            session_id: Session identifier
            thought: Thought content
            context: Existing context (optional, will be retrieved if None)

        Returns:
            Step number (1-based)

        Raises:
            ValueError: If thought exceeds max length or is empty (if not allowed)
        """
        # Validate thought
        if not thought:
            config = get_config()
            if not config.allow_empty_thoughts:
                raise ValueError("Thought cannot be empty")
        
        # Check thought length
        if len(thought) > self.max_thought_length:
            raise ValueError(
                f"Thought length ({len(thought)}) exceeds maximum "
                f"({self.max_thought_length} characters)"
            )
        
        # Sanitize input if enabled
        config = get_config()
        if config.sanitize_input:
            # Basic sanitization: remove null bytes and control characters
            thought = thought.replace("\x00", "").replace("\r\n", "\n")
        
        with self._lock:
            if context is None:
                context = self.get_context(session_id)

            # Check max thoughts limit
            if len(context["thoughts"]) >= self.max_thoughts:
                # Remove oldest thought (FIFO)
                removed = context["thoughts"].pop(0)
                logger.warning(
                    f"Max thoughts reached for session {session_id}, "
                    f"removed oldest thought (step {removed['step']})"
                )

            # Add new thought
            step = len(context["thoughts"]) + 1
            now = datetime.utcnow()
            thought_entry = {
                "timestamp": now.isoformat(),
                "thought": thought,
                "step": step,
            }

            context["thoughts"].append(thought_entry)
            context["metadata"]["last_updated"] = now.isoformat()
            context["metadata"]["total_steps"] = step

            # Log thought if configured (be careful with sensitive data)
            if config.log_thoughts:
                logger.debug(
                    f"Added thought to session {session_id}: step {step}, "
                    f"thought length={len(thought)}"
                )
            else:
                logger.debug(
                    f"Added thought to session {session_id}: step {step}, "
                    f"thought length={len(thought)} (content not logged)"
                )
            return step

    def get_all_thoughts(self, session_id: str) -> List[Dict]:
        """
        Get all thoughts for a session.

        Args:
            session_id: Session identifier

        Returns:
            List of thought entries
        """
        context = self.get_context(session_id)
        return context.get("thoughts", [])

    def get_formatted_context(self, session_id: str) -> str:
        """
        Get formatted context string for Node Agent.

        Args:
            session_id: Session identifier

        Returns:
            Formatted string of all thoughts
        """
        thoughts = self.get_all_thoughts(session_id)
        if not thoughts:
            return "No thoughts yet in this session."

        formatted = "Previous thoughts in this session:\n\n"
        for thought_entry in thoughts:
            formatted += (
                f"Step {thought_entry['step']} "
                f"({thought_entry['timestamp']}):\n"
            )
            formatted += f"{thought_entry['thought']}\n\n"

        return formatted

    def clear_context(self, session_id: str) -> None:
        """
        Clear context for a session (thread-safe).

        Args:
            session_id: Session identifier
        """
        with self._lock:
            if session_id in self._contexts:
                del self._contexts[session_id]
                logger.info(f"Cleared context for session: {session_id}")
    
    def get_stats(self) -> Dict:
        """
        Get statistics about context manager.

        Returns:
            Dict with statistics
        """
        with self._lock:
            total_sessions = len(self._contexts)
            total_thoughts = sum(
                len(ctx.get("thoughts", [])) for ctx in self._contexts.values()
            )
            return {
                "total_sessions": total_sessions,
                "total_thoughts": total_thoughts,
                "max_thoughts": self.max_thoughts,
                "cleanup_interval_hours": self.cleanup_interval_hours,
                "auto_cleanup_enabled": self.enable_auto_cleanup,
            }

    def cleanup_old_sessions(self, max_age_hours: Optional[int] = None) -> int:
        """
        Clean up old sessions (thread-safe).

        Args:
            max_age_hours: Maximum age in hours (uses config default if None)

        Returns:
            Number of sessions cleaned up
        """
        if max_age_hours is None:
            max_age_hours = self.cleanup_interval_hours
        
        current_time = datetime.utcnow()
        sessions_to_remove = []

        with self._lock:
            for session_id, context in self._contexts.items():
                last_updated_str = context["metadata"].get("last_updated")
                if not last_updated_str:
                    continue

                try:
                    last_updated = datetime.fromisoformat(
                        last_updated_str.replace("Z", "+00:00")
                    )
                    age_hours = (current_time - last_updated).total_seconds() / 3600

                    if age_hours > max_age_hours:
                        sessions_to_remove.append(session_id)
                except (ValueError, AttributeError) as e:
                    logger.warning(
                        f"Error parsing timestamp for session {session_id}: {e}"
                    )
                    # Remove sessions with invalid timestamps
                    sessions_to_remove.append(session_id)

            # Remove old sessions
            for session_id in sessions_to_remove:
                del self._contexts[session_id]
                logger.info(f"Cleaned up old session: {session_id}")

        return len(sessions_to_remove)

    def get_context_summary(self, session_id: str) -> Dict:
        """
        Get summary of context for a session.

        Args:
            session_id: Session identifier

        Returns:
            Dict with context summary
        """
        context = self.get_context(session_id)
        return {
            "session_id": session_id,
            "total_steps": context["metadata"]["total_steps"],
            "created_at": context["metadata"]["created_at"],
            "last_updated": context["metadata"]["last_updated"],
        }

