"""Tool Provider for Claude Think Tool plugin."""

from typing import Any, Mapping
import logging

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.think_tool import ThinkTool

logger = logging.getLogger(__name__)


class ThinkProvider(ToolProvider):
    """
    Provider for Think Tool plugin.
    No credentials required for this tool.
    """

    def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
        """
        Validate provider credentials.
        For think tool, no credentials are needed.

        Args:
            credentials: Credentials mapping (empty for this tool)

        Raises:
            ToolProviderCredentialValidationError: If validation fails
        """
        # No validation needed for think tool
        # But can add custom validation if needed
        logger.debug("Credential validation skipped (no credentials required)")
        pass

    def get_tool_classes(self):
        """
        Return list of tool classes provided by this provider.

        Returns:
            List of tool classes
        """
        return [ThinkTool]

