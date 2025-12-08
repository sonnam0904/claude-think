"""Custom exceptions for Claude Think Tool plugin."""


class ThinkToolError(Exception):
    """Base exception for Think Tool errors."""
    pass


class ThoughtValidationError(ThinkToolError):
    """Raised when thought validation fails."""
    pass


class ThoughtLengthError(ThinkToolError):
    """Raised when thought exceeds maximum length."""
    pass


class ContextError(ThinkToolError):
    """Raised when context operations fail."""
    pass


class ConfigurationError(ThinkToolError):
    """Raised when configuration is invalid."""
    pass

