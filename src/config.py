"""Configuration management for Claude Think Tool plugin."""

import os
from typing import Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class PluginConfig:
    """Plugin configuration settings."""

    # Context Manager settings
    max_thoughts: int = 100
    cleanup_interval_hours: int = 24
    enable_auto_cleanup: bool = True

    # Performance settings
    enable_context_compression: bool = False
    max_thought_length: int = 10000  # Max characters per thought

    # Logging settings
    log_level: str = "INFO"
    log_thoughts: bool = False  # Whether to log thought content (privacy)

    # Security settings
    allow_empty_thoughts: bool = False
    sanitize_input: bool = True

    @classmethod
    def from_env(cls) -> "PluginConfig":
        """
        Create configuration from environment variables.

        Environment variables:
        - THINK_MAX_THOUGHTS: Maximum thoughts per session (default: 100)
        - THINK_CLEANUP_HOURS: Cleanup interval in hours (default: 24)
        - THINK_AUTO_CLEANUP: Enable auto cleanup (default: true)
        - THINK_LOG_LEVEL: Log level (default: INFO)
        - THINK_LOG_THOUGHTS: Log thought content (default: false)
        - THINK_MAX_THOUGHT_LENGTH: Max characters per thought (default: 10000)

        Returns:
            PluginConfig instance
        """
        return cls(
            max_thoughts=int(
                os.getenv("THINK_MAX_THOUGHTS", str(cls.max_thoughts))
            ),
            cleanup_interval_hours=int(
                os.getenv("THINK_CLEANUP_HOURS", str(cls.cleanup_interval_hours))
            ),
            enable_auto_cleanup=os.getenv(
                "THINK_AUTO_CLEANUP", "true"
            ).lower() in ("true", "1", "yes"),
            max_thought_length=int(
                os.getenv("THINK_MAX_THOUGHT_LENGTH", str(cls.max_thought_length))
            ),
            log_level=os.getenv("THINK_LOG_LEVEL", cls.log_level).upper(),
            log_thoughts=os.getenv("THINK_LOG_THOUGHTS", "false").lower()
            in ("true", "1", "yes"),
            allow_empty_thoughts=os.getenv(
                "THINK_ALLOW_EMPTY_THOUGHTS", "false"
            ).lower() in ("true", "1", "yes"),
            sanitize_input=os.getenv("THINK_SANITIZE_INPUT", "true").lower()
            in ("true", "1", "yes"),
        )

    def validate(self) -> None:
        """
        Validate configuration values.

        Raises:
            ValueError: If configuration values are invalid
        """
        if self.max_thoughts < 1:
            raise ValueError("max_thoughts must be at least 1")
        if self.max_thoughts > 1000:
            raise ValueError("max_thoughts cannot exceed 1000")
        if self.cleanup_interval_hours < 1:
            raise ValueError("cleanup_interval_hours must be at least 1")
        if self.max_thought_length < 100:
            raise ValueError("max_thought_length must be at least 100")
        if self.max_thought_length > 100000:
            raise ValueError("max_thought_length cannot exceed 100000")
        if self.log_level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            raise ValueError(f"Invalid log_level: {self.log_level}")


# Global configuration instance
_config: Optional[PluginConfig] = None


def get_config() -> PluginConfig:
    """
    Get global plugin configuration.

    Returns:
        PluginConfig instance
    """
    global _config
    if _config is None:
        _config = PluginConfig.from_env()
        try:
            _config.validate()
        except ValueError as e:
            logger.error(f"Invalid configuration: {e}")
            # Use default config if validation fails
            _config = PluginConfig()
    return _config


def set_config(config: PluginConfig) -> None:
    """
    Set global plugin configuration.

    Args:
        config: PluginConfig instance
    """
    global _config
    config.validate()
    _config = config
    logger.info("Plugin configuration updated")

