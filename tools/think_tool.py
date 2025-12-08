"""Think tool implementation for structured multi-step reasoning."""

from collections.abc import Generator
from typing import Any
import logging

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from src.context_manager import ContextManager
from src.config import get_config
from src.errors import ThoughtValidationError, ThoughtLengthError, ContextError

logger = logging.getLogger(__name__)


class ThinkTool(Tool):
    """
    Think tool implementation.
    Allows Node Agents to perform structured multi-step reasoning.
    """

    def __init__(self, runtime: Any, session: Any):
        """
        Initialize ThinkTool.

        Args:
            runtime: Tool runtime context from Dify
            session: Session context from Dify
        """
        super().__init__(runtime, session)
        self.context_manager = ContextManager()
        logger.info("ThinkTool initialized")

    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the think tool.

        Args:
            tool_parameters: Dictionary containing:
                - thought (str): The thought to think about

        Yields:
            ToolInvokeMessage: Formatted response message
        """
        config = get_config()
        
        # Extract thought from parameters
        thought = tool_parameters.get("thought", "")
        
        # Validate thought parameter exists
        if thought is None:
            error_msg = "Error: 'thought' parameter is required but was not provided"
            logger.error(error_msg)
            yield self.create_text_message(error_msg)
            return
        
        # Convert to string if needed
        if not isinstance(thought, str):
            thought = str(thought)
        
        # Validate thought content
        if not thought.strip() and not config.allow_empty_thoughts:
            error_msg = "Error: 'thought' parameter cannot be empty"
            logger.error(error_msg)
            yield self.create_text_message(error_msg)
            return
        
        # Get session context
        # Try to get session_id from various sources
        session_id = None
        
        # First, try to get from runtime attributes (workflow_id or session_id)
        session_id = getattr(self.runtime, "workflow_id", None) or getattr(
            self.runtime, "session_id", None
        )
        
        # If not found, use "default" as fallback
        if not session_id:
            session_id = "default"

        logger.debug(f"Processing thought for session: {session_id}, length={len(thought)}")

        try:
            # Get context
            context = self.context_manager.get_context(session_id)

            # Add thought to context (this will validate length)
            step = self.context_manager.add_thought(
                session_id=session_id, thought=thought, context=context
            )

            # Format response
            response = {
                "status": "success",
                "step": step,
                "thought": thought,
                "context_size": len(context.get("thoughts", [])),
                "session_id": session_id,
                "max_thoughts": self.context_manager.max_thoughts,
            }

            logger.info(
                f"Thought added successfully: session={session_id}, "
                f"step={step}, context_size={response['context_size']}, "
                f"thought_length={len(thought)}"
            )
            yield self.create_json_message(response)

        except (ThoughtValidationError, ThoughtLengthError) as e:
            # Specific validation errors
            error_msg = f"Validation error: {str(e)}"
            logger.warning(f"{error_msg}, session_id={session_id}")
            yield self.create_text_message(error_msg)
        except ContextError as e:
            # Context operation errors
            error_msg = f"Context error: {str(e)}"
            logger.error(f"{error_msg}, session_id={session_id}", exc_info=True)
            yield self.create_text_message(error_msg)
        except Exception as e:
            # Unexpected errors
            error_msg = f"Unexpected error processing thought: {str(e)}"
            logger.error(f"{error_msg}, session_id={session_id}", exc_info=True)
            yield self.create_text_message(error_msg)

