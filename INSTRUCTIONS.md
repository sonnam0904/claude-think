# INSTRUCTIONS.md: Hướng dẫn Kỹ thuật - Dify Plugin Think Tool

## 📚 Mục lục

1. [Tech Stack](#tech-stack)
2. [Kiến trúc Hệ thống](#kiến-trúc-hệ-thống)
3. [Core Components](#core-components)
4. [Configuration System](#configuration-system)
5. [Error Handling](#error-handling)
6. [Performance & Optimization](#performance--optimization)
7. [Security Considerations](#security-considerations)
8. [Testing](#testing)
9. [Tài liệu Tham khảo](#tài-liệu-tham-khảo)

---

## 🛠️ Tech Stack

### Core Technologies

#### 1. **Python 3.12+**
- **Yêu cầu**: Python version ≥ 3.12
- **Lý do**: Dify plugin SDK yêu cầu Python 3.12 trở lên
- **Kiểm tra version**:
  ```bash
  python --version
  # Hoặc
  python3 --version
  ```

#### 2. **Dify Plugin SDK**
- **Package**: `dify_plugin`
- **Source**: [dify-plugin-sdks](https://github.com/langgenius/dify-plugin-sdks)
- **Cài đặt**: Tự động khi khởi tạo plugin project hoặc:
  ```bash
  pip install dify-plugin
  ```

#### 3. **Dify Plugin CLI (dify-plugin-daemon)**
- **Mục đích**: Tool scaffold để tạo và quản lý Dify plugins
- **Download**: [Dify Plugin CLI Releases](https://github.com/langgenius/dify-plugin-daemon/releases)
- **Cài đặt**:
  ```bash
  # Linux
  chmod +x dify-plugin-linux-amd64
  mv dify-plugin-linux-amd64 dify
  sudo mv dify /usr/local/bin/
  
  # macOS (Brew - Recommended)
  brew tap langgenius/dify
  brew install dify
  
  # Kiểm tra
  dify version
  ```

### Development Tools

#### 4. **Testing Framework**
- **pytest**: Unit testing và integration testing
- **Cài đặt**: `pip install pytest pytest-cov`
- **Cấu hình**: `pytest.ini` hoặc `setup.cfg`

#### 5. **Code Quality**
- **Black**: Code formatting
- **Flake8/Pylint**: Linting
- **mypy**: Type checking (optional)

#### 6. **Version Control**
- **Git**: Source control
- **.gitignore**: Đảm bảo exclude các file nhạy cảm

### Dependencies

#### 7. **Core Libraries**

```python
# requirements.txt
dify-plugin>=1.0.0
pydantic>=2.0.0  # Data validation
python-dotenv>=1.0.0  # Environment variables
```

#### 8. **Optional Libraries**
```python
# Cho logging và observability
structlog>=23.0.0

# Cho async operations (nếu cần)
aiohttp>=3.9.0

# Cho testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0
```

### Environment Requirements

#### 9. **Development Environment**
- **OS**: Linux, macOS, hoặc Windows (với WSL)
- **IDE**: VS Code, PyCharm, hoặc bất kỳ editor nào hỗ trợ Python
- **Python Environment**: 
  - Virtual environment (venv) hoặc conda
  - Recommended: `python -m venv venv`

#### 10. **Configuration Files**
- **.env**: Environment variables cho remote debugging
- **.env.example**: Template cho .env file
- **plugin.yaml**: Plugin metadata và configuration
- **pyproject.toml** hoặc **setup.py**: Package configuration

---

## 🏗️ Kiến trúc Hệ thống

### Tổng quan Kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                    Dify Platform                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Node Agent Workflow                     │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │  │
│  │  │   Tool 1   │→ │ Think Tool │→ │   Tool 2   │ │  │
│  │  └────────────┘  └────────────┘  └────────────┘ │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↕                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Plugin System (Remote/Local)              │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│           Claude Think Plugin (This Project)            │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Plugin Entry Point (main.py)           │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↕                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Tool Provider (think_provider.py)         │  │
│  │  - Credential validation                          │  │
│  │  - Tool registration                              │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↕                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Think Tool (think_tool.py)             │  │
│  │  - Tool invocation logic                          │  │
│  │  - Response formatting                            │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↕                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Context Manager (context_manager.py)         │  │
│  │  - Session management                             │  │
│  │  - Thought accumulation                           │  │
│  │  - Context retrieval                              │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↕                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Prompt Templates (prompt_templates.py)          │  │
│  │  - Domain-specific templates                      │  │
│  │  - Example prompts                                │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

#### 1. **Plugin Registration Flow**
```
Dify Platform
    ↓ (Discovers plugin)
Plugin Entry Point (main.py)
    ↓ (Loads configuration)
Plugin.yaml
    ↓ (Registers provider)
Tool Provider (think_provider.py)
    ↓ (Validates & registers tools)
Think Tool (think_tool.py)
    ↓ (Available to Node Agents)
Node Agent Workflow
```

#### 2. **Tool Invocation Flow**
```
Node Agent calls think tool
    ↓
Dify Plugin System routes to plugin
    ↓
Think Tool receives invocation
    ↓
Context Manager retrieves/stores context
    ↓
Think Tool processes thought
    ↓
Response formatted and returned
    ↓
Context updated with new thought
    ↓
Node Agent receives response
```

#### 3. **Context Management Flow**
```
Session Start
    ↓
Context Manager initialized
    ↓
Think Tool Call #1 → Thought #1 stored
    ↓
Think Tool Call #2 → Thought #2 stored
    ↓ (Context accumulates)
Think Tool Call #N → Thought #N stored
    ↓
Context available for all subsequent calls
    ↓
Session End → Context cleared/archived
```

### File Structure Architecture

```
claude-think-plugin/
├── .env                      # Environment configuration
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── main.py                   # Plugin entry point
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Package configuration
├── plugin.yaml              # Plugin metadata & config
│
├── provider/                 # Tool Provider implementation
│   ├── __init__.py
│   ├── think_provider.yaml  # Provider manifest
│   └── think_provider.py    # Provider class
│
├── tools/                    # Tool implementations
│   ├── __init__.py
│   ├── think.yaml           # Tool manifest
│   └── think_tool.py        # Tool class
│
├── src/                      # Core source code
│   ├── __init__.py
│   ├── context_manager.py   # Context management (thread-safe)
│   ├── prompt_templates.py  # Prompt templates
│   ├── config.py            # Configuration system
│   └── errors.py            # Custom exceptions
│
├── _assets/                  # Static assets
│   └── icon.svg             # Plugin icon
│
└── tests/                    # Test suite
    ├── __init__.py
    ├── test_think_tool.py
    ├── test_context_manager.py
    ├── test_integration.py
    └── test_performance.py
```

### Data Flow Architecture

#### Session Context Data Structure
```python
{
    "session_id": "uuid-string",
    "workflow_id": "workflow-uuid",
    "agent_id": "agent-uuid",
    "thoughts": [
        {
            "timestamp": "2024-01-01T00:00:00Z",
            "thought": "User wants to cancel flight ABC123...",
            "step": 1
        },
        {
            "timestamp": "2024-01-01T00:00:01Z",
            "thought": "Need to verify: user ID, reservation ID...",
            "step": 2
        }
    ],
    "metadata": {
        "created_at": "2024-01-01T00:00:00Z",
        "last_updated": "2024-01-01T00:00:01Z",
        "total_steps": 2
    }
}
```

### Integration Points

#### 1. **Dify Plugin API Integration**
- **Registration**: Plugin tự đăng ký với Dify qua plugin.yaml
- **Discovery**: Dify tự động discover plugin khi start
- **Invocation**: Dify route tool calls đến plugin
- **Response**: Plugin trả về formatted response

#### 2. **Node Agent Integration**
- **Tool Availability**: Think tool xuất hiện trong tool list
- **Tool Selection**: Node Agent tự quyết định khi nào sử dụng
- **Context Awareness**: Node Agent có thể tham chiếu context

#### 3. **Storage Integration** (Optional)
- **Persistent Storage**: Dify cung cấp KV storage nếu cần
- **Session Storage**: Context có thể persist qua sessions
- **Cleanup**: Tự động cleanup old contexts

---

## 🔧 Core Components

### 1. Plugin Entry Point (`main.py`)

#### Mục đích
- Khởi tạo plugin application
- Đăng ký tool provider với Dify
- Xử lý lifecycle events

#### Code Structure
```python
from dify_plugin import create_application
from provider.think_provider import ThinkProvider
from tools.think_tool import ThinkTool

def main():
    # Create plugin application
    app = create_application()
    
    # Register provider
    app.register_provider(
        provider_class=ThinkProvider,
        manifest_path="provider/think_provider.yaml"
    )
    
    # Run application
    app.run()

if __name__ == "__main__":
    main()
```

#### Key Responsibilities
- Application initialization
- Provider registration
- Error handling
- Logging setup

### 2. Tool Provider (`provider/think_provider.py`)

#### Mục đích
- Định nghĩa tool provider
- Validate credentials (nếu có)
- Quản lý provider-level resources

#### Code Structure
```python
from typing import Any, Mapping
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.think_tool import ThinkTool

class ThinkProvider(ToolProvider):
    """
    Provider for Think Tool plugin.
    No credentials required for this tool.
    """
    
    def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
        """
        Validate provider credentials.
        For think tool, no credentials are needed.
        """
        # No validation needed for think tool
        # But can add custom validation if needed
        pass
    
    def get_tool_classes(self):
        """Return list of tool classes provided by this provider."""
        return [ThinkTool]
```

#### Provider Manifest (`provider/think_provider.yaml`)
```yaml
identity:
    author: Your-name
    name: claude_think
    label:
        en_US: Claude Think Tool
        zh_Hans: Claude 思考工具
    description:
        en_US: Multi-step thinking tool for Node Agents based on Claude's think tool research
        zh_Hans: 基于 Claude think tool 研究的多步骤思考工具
    icon: icon.svg
    tags:
        - utilities
        - productivity

tools:
    - tools/think.yaml

extra:
    python:
        source: provider/think_provider.py
```

### 3. Think Tool (`tools/think_tool.py`)

#### Mục đích
- Implement logic cho think tool
- Xử lý tool invocations
- Format responses

#### Code Structure
```python
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from src.context_manager import ContextManager
from src.config import get_config
from src.errors import (
    ThoughtValidationError, 
    ThoughtLengthError, 
    ContextError
)

class ThinkTool(Tool):
    """
    Think tool implementation.
    Allows Node Agents to perform structured multi-step reasoning.
    """
    
    def __init__(self, runtime: Any):
        super().__init__(runtime)
        self.context_manager = ContextManager()
        self.config = get_config()
    
    def _invoke(
        self, 
        tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the think tool with enhanced error handling.
        
        Args:
            tool_parameters: Dictionary containing:
                - thought (str): The thought to think about
        
        Yields:
            ToolInvokeMessage: Formatted response message
        """
        # Extract and validate thought parameter
        thought = tool_parameters.get("thought", "")
        
        if thought is None:
            yield self.create_text_message(
                "Error: 'thought' parameter is required but was not provided"
            )
            return
        
        if not isinstance(thought, str):
            thought = str(thought)
        
        if not thought.strip() and not self.config.allow_empty_thoughts:
            yield self.create_text_message(
                "Error: 'thought' parameter cannot be empty"
            )
            return
        
        # Get session context
        session_id = getattr(self.runtime, "workflow_id", None) or getattr(
            self.runtime, "session_id", "default"
        )
        
        try:
            context = self.context_manager.get_context(session_id)
            
            # Add thought to context (validates length)
            step = self.context_manager.add_thought(
                session_id=session_id,
                thought=thought,
                context=context
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
            
            yield self.create_json_message(response)
            
        except (ThoughtValidationError, ThoughtLengthError) as e:
            yield self.create_text_message(f"Validation error: {str(e)}")
        except ContextError as e:
            yield self.create_text_message(f"Context error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            yield self.create_text_message(
                f"Unexpected error processing thought: {str(e)}"
            )
```

#### Tool Manifest (`tools/think.yaml`)
```yaml
identity:
    name: think
    author: Your-name
    label:
        en_US: Think
        zh_Hans: 思考
    description:
        human:
            en_US: Use this tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.
            zh_Hans: 使用此工具进行思考。它不会获取新信息或更改数据库，只是将思考内容附加到日志中。在需要复杂推理或缓存记忆时使用。
        llm: Use this tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.

parameters:
    - name: thought
      type: string
      required: true
      label:
          en_US: Thought
          zh_Hans: 思考内容
      human_description:
          en_US: A thought to think about
          zh_Hans: 要思考的内容
      llm_description: A thought to think about. Be specific and detailed in your reasoning.
      form: llm

extra:
    python:
        source: tools/think_tool.py
```

### 4. Context Manager (`src/context_manager.py`)

#### Mục đích
- Quản lý session context (thread-safe)
- Lưu trữ và retrieve thoughts
- Tích lũy context qua nhiều tool calls
- Automatic cleanup với background thread

#### Key Features
- **Thread-Safe**: All operations use locks for concurrent access
- **Automatic Cleanup**: Background thread cleans old sessions
- **Configuration-Driven**: Uses config system for limits
- **Memory Efficient**: FIFO eviction when limits reached
- **Statistics Tracking**: Provides usage statistics

#### Code Structure
```python
from typing import Dict, List, Optional
from datetime import datetime
import threading
from src.config import get_config

class ContextManager:
    """
    Manages context accumulation for think tool.
    Stores thoughts per session/workflow.
    Thread-safe implementation with automatic cleanup.
    """
    
    def __init__(self, max_thoughts: Optional[int] = None):
        config = get_config()
        # In-memory storage (thread-safe)
        self._contexts: Dict[str, Dict] = {}
        # Thread lock for thread-safety
        self._lock = threading.RLock()
        # Max thoughts per session (from config)
        self.max_thoughts = max_thoughts or config.max_thoughts
        self.cleanup_interval_hours = config.cleanup_interval_hours
        self.enable_auto_cleanup = config.enable_auto_cleanup
        self.max_thought_length = config.max_thought_length
        
        # Auto cleanup thread (if enabled)
        if self.enable_auto_cleanup:
            self._start_cleanup_thread()
    
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
                        "total_steps": 0
                    }
                }
            return self._contexts[session_id]
    
    def add_thought(
        self, 
        session_id: str, 
        thought: str,
        context: Optional[Dict] = None
    ) -> int:
        """
        Add a thought to the context (thread-safe).
        
        Args:
            session_id: Session identifier
            thought: Thought content
            context: Existing context (optional)
        
        Returns:
            Step number (1-based)
        
        Raises:
            ValueError: If thought is empty (if not allowed) or too long
        """
        # Validate thought
        if not thought.strip() and not config.allow_empty_thoughts:
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
            thought = thought.replace("\x00", "").replace("\r\n", "\n")
        
        with self._lock:
            if context is None:
                context = self.get_context(session_id)
            
            # Check max thoughts limit
            if len(context["thoughts"]) >= self.max_thoughts:
                # Remove oldest thought (FIFO)
                context["thoughts"].pop(0)
            
            # Add new thought
            step = len(context["thoughts"]) + 1
            thought_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "thought": thought,
                "step": step
            }
            
            context["thoughts"].append(thought_entry)
            context["metadata"]["last_updated"] = datetime.utcnow().isoformat()
            context["metadata"]["total_steps"] = step
            
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
            formatted += f"Step {thought_entry['step']} ({thought_entry['timestamp']}):\n"
            formatted += f"{thought_entry['thought']}\n\n"
        
        return formatted
    
    def clear_context(self, session_id: str) -> None:
        """
        Clear context for a session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self._contexts:
            del self._contexts[session_id]
    
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
                except (ValueError, AttributeError):
                    sessions_to_remove.append(session_id)
            
            # Remove old sessions
            for session_id in sessions_to_remove:
                del self._contexts[session_id]
        
        return len(sessions_to_remove)
    
    def get_stats(self) -> Dict:
        """
        Get statistics about context manager.
        
        Returns:
            Dict with statistics (total_sessions, total_thoughts, etc.)
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
    
    def shutdown(self) -> None:
        """Shutdown the context manager and cleanup thread."""
        if self._cleanup_thread:
            self._stop_cleanup.set()
            self._cleanup_thread.join(timeout=5)
```

### 5. Configuration System (`src/config.py`)

#### Mục đích
- Quản lý toàn bộ configuration settings
- Load từ environment variables
- Validate configuration values
- Provide defaults

#### Key Features
- Environment variable-based configuration
- Automatic validation
- Type-safe configuration access
- Global configuration instance
- Singleton pattern implementation

#### Code Structure
```python
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class PluginConfig:
    """Plugin configuration settings."""
    
    # Context Manager settings
    max_thoughts: int = 100
    cleanup_interval_hours: int = 24
    enable_auto_cleanup: bool = True
    
    # Performance settings
    max_thought_length: int = 10000
    
    # Logging settings
    log_level: str = "INFO"
    log_thoughts: bool = False
    
    # Security settings
    allow_empty_thoughts: bool = False
    sanitize_input: bool = True
    
    @classmethod
    def from_env(cls) -> "PluginConfig":
        """Create configuration from environment variables."""
        return cls(
            max_thoughts=int(os.getenv("THINK_MAX_THOUGHTS", "100")),
            # ... other settings
        )
    
    def validate(self) -> None:
        """Validate configuration values."""
        if self.max_thoughts < 1:
            raise ValueError("max_thoughts must be at least 1")
        # ... other validations

# Global configuration instance
_config: Optional[PluginConfig] = None

def get_config() -> PluginConfig:
    """Get global plugin configuration."""
    global _config
    if _config is None:
        _config = PluginConfig.from_env()
        _config.validate()
    return _config
```

#### Usage Example
```python
from src.config import get_config

config = get_config()
max_thoughts = config.max_thoughts
log_level = config.log_level
```

Xem chi tiết trong phần [Configuration System](#configuration-system).

### 6. Error Handling (`src/errors.py`)

#### Mục đích
- Custom exception classes cho plugin
- Type-safe error handling
- Specific error types cho different scenarios
- Clear error messages

#### Exception Hierarchy
```python
# Base exception
class ThinkToolError(Exception):
    """Base exception for Think Tool errors."""
    pass

# Specific exceptions
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
```

#### Usage in Code
```python
from src.errors import ThoughtLengthError, ThoughtValidationError

try:
    context_manager.add_thought(session_id, thought)
except ThoughtLengthError as e:
    # Handle length error
    logger.warning(f"Thought too long: {e}")
except ThoughtValidationError as e:
    # Handle validation error
    logger.error(f"Invalid thought: {e}")
```

Xem chi tiết trong phần [Error Handling](#error-handling).

### 7. Prompt Templates (`src/prompt_templates.py`)

#### Mục đích
- Cung cấp domain-specific prompts
- Examples và best practices
- Template library cho các use cases

#### Code Structure
```python
from typing import Dict

class PromptTemplates:
    """
    Domain-specific prompt templates for think tool usage.
    """
    
    # Base system prompt for think tool usage
    BASE_SYSTEM_PROMPT = """## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness
"""
    
    # Domain-specific templates
    TEMPLATES: Dict[str, str] = {
        "airline": """## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness

Here are some examples of what to iterate over inside the think tool:
<think_tool_example_1>
User wants to cancel flight ABC123
- Need to verify: user ID, reservation ID, reason
- Check cancellation rules:
  * Is it within 24h of booking?
  * If not, check ticket class and insurance
- Verify no segments flown or are in the past
- Plan: collect missing info, verify rules, get confirmation
</think_tool_example_1>

<think_tool_example_2>
User wants to book 3 tickets to NYC with 2 checked bags each
- Need user ID to check:
  * Membership tier for baggage allowance
  * Which payments methods exist in profile
- Baggage calculation:
  * Economy class × 3 passengers
  * If regular member: 1 free bag each → 3 extra bags = $150
  * If silver member: 2 free bags each → 0 extra bags = $0
  * If gold member: 3 free bags each → 0 extra bags = $0
- Payment rules to verify:
  * Max 1 travel certificate, 1 credit card, 3 gift cards
  * All payment methods must be in profile
  * Travel certificate remainder goes to waste
- Plan:
1. Get user ID
2. Verify membership level for bag fees
3. Check which payment methods in profile and if their combination is allowed
4. Calculate total: ticket price + any bag fees
5. Get explicit confirmation for booking
</think_tool_example_2>
""",
        
        "retail": """## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool to:
- Analyze customer request and identify requirements
- Check inventory and availability
- Verify pricing rules and discounts
- Confirm shipping options and policies
- Validate payment methods
""",
        
        "coding": """## Using the think tool

Use this tool when complex reasoning or brainstorming is needed. For example:
- If you explore the repo and discover the source of a bug, call this tool to brainstorm several unique ways of fixing the bug, and assess which change(s) are likely to be simplest and most effective.
- If you receive some test results, call this tool to brainstorm ways to fix the failing tests.
- Before making changes, think through the implications and potential side effects.
"""
    }
    
    @classmethod
    def get_template(cls, domain: str = "default") -> str:
        """
        Get prompt template for a specific domain.
        
        Args:
            domain: Domain name (airline, retail, coding, etc.)
        
        Returns:
            Prompt template string
        """
        return cls.TEMPLATES.get(domain, cls.BASE_SYSTEM_PROMPT)
    
    @classmethod
    def list_domains(cls) -> list[str]:
        """List available domain templates."""
        return list(cls.TEMPLATES.keys())
```

### Component Relationships

```
main.py
    ↓ (loads config)
PluginConfig (config.py)
    ↓ (provides settings)
ContextManager
    ↓ (uses)
ThinkTool
    ↓ (handles errors via)
Custom Exceptions (errors.py)

ThinkProvider
    ↓ (manages)
ThinkTool
    ↓ (uses)
ContextManager (thread-safe)
    ↓ (stores)
Session Context

ThinkTool
    ↓ (references)
PromptTemplates
    ↓ (provides)
Domain-specific prompts

ContextManager
    ↓ (uses)
PluginConfig
    ↓ (configured via)
Environment Variables

Error Handling:
ThinkTool → Custom Exceptions → Error Messages
ContextManager → Validation Errors → Error Messages
```

### Key Design Patterns

#### 1. **Singleton Pattern** (Configuration)
- Global configuration instance
- Single source of truth for settings

#### 2. **Thread-Safe Singleton** (Context Manager)
- Thread-safe shared state
- Re-entrant locks for concurrent access

#### 3. **Factory Pattern** (Tool Creation)
- Dify SDK sử dụng factory pattern để tạo tools
- `Tool.from_credentials()` method

#### 4. **Strategy Pattern** (Prompt Templates)
- Domain-specific prompts có thể switch
- Dễ dàng mở rộng với domain mới

#### 5. **Exception Hierarchy** (Error Handling)
- Base exception class với specific subclasses
- Type-safe error handling

#### 6. **Background Worker Pattern** (Cleanup)
- Daemon thread cho automatic cleanup
- Non-blocking background operations

---

## ⚙️ Configuration System

### Overview

Plugin sử dụng hệ thống configuration linh hoạt dựa trên environment variables, cho phép tùy chỉnh behavior mà không cần thay đổi code.

### Configuration Component (`src/config.py`)

#### Purpose
- Quản lý toàn bộ configuration settings
- Load từ environment variables
- Validate configuration values
- Provide defaults

#### Key Features

**1. Configuration Options**

```python
@dataclass
class PluginConfig:
    # Context Manager settings
    max_thoughts: int = 100
    cleanup_interval_hours: int = 24
    enable_auto_cleanup: bool = True
    
    # Performance settings
    max_thought_length: int = 10000
    
    # Logging settings
    log_level: str = "INFO"
    log_thoughts: bool = False
    
    # Security settings
    allow_empty_thoughts: bool = False
    sanitize_input: bool = True
```

**2. Environment Variables**

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `THINK_MAX_THOUGHTS` | int | 100 | Max thoughts per session |
| `THINK_CLEANUP_HOURS` | int | 24 | Cleanup interval (hours) |
| `THINK_AUTO_CLEANUP` | bool | true | Enable auto cleanup |
| `THINK_MAX_THOUGHT_LENGTH` | int | 10000 | Max characters per thought |
| `THINK_LOG_LEVEL` | string | INFO | Logging level |
| `THINK_LOG_THOUGHTS` | bool | false | Log thought content |
| `THINK_ALLOW_EMPTY_THOUGHTS` | bool | false | Allow empty thoughts |
| `THINK_SANITIZE_INPUT` | bool | true | Sanitize input |

**3. Usage**

```python
from src.config import get_config, PluginConfig

# Get global configuration
config = get_config()
max_thoughts = config.max_thoughts

# Set custom configuration
custom_config = PluginConfig(max_thoughts=200, log_level="DEBUG")
set_config(custom_config)
```

**4. Validation**

Configuration values are automatically validated:
- Range checks (e.g., max_thoughts: 1-1000)
- Type validation
- Fallback to defaults on invalid values

### Configuration Files

Xem thêm chi tiết trong [CONFIGURATION.md](./CONFIGURATION.md).

---

## ⚠️ Error Handling

### Error Handling System (`src/errors.py`)

#### Custom Exception Classes

```python
# Base exception
class ThinkToolError(Exception):
    """Base exception for Think Tool errors."""
    pass

# Specific exceptions
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
```

#### Error Handling in Think Tool

**Enhanced Error Handling Flow:**

```python
try:
    # Add thought to context (validates length)
    step = context_manager.add_thought(session_id, thought, context)
except ThoughtLengthError as e:
    # Handle length error specifically
    yield self.create_text_message(f"Error: {str(e)}")
except ThoughtValidationError as e:
    # Handle validation error
    yield self.create_text_message(f"Validation error: {str(e)}")
except ContextError as e:
    # Handle context operation error
    yield self.create_text_message(f"Context error: {str(e)}")
except Exception as e:
    # Handle unexpected errors
    logger.error(f"Unexpected error: {e}", exc_info=True)
    yield self.create_text_message("An unexpected error occurred")
```

#### Error Types

1. **Validation Errors**
   - Missing required parameters
   - Empty thoughts (if not allowed)
   - Invalid parameter types

2. **Length Errors**
   - Thought exceeds max length
   - Automatic truncation not supported (explicit error)

3. **Context Errors**
   - Session not found (shouldn't happen with auto-creation)
   - Context storage failures
   - Cleanup errors

4. **Configuration Errors**
   - Invalid configuration values
   - Missing required settings

---

## 🚀 Performance & Optimization

### Thread-Safe Operations

#### Context Manager Thread Safety

**Implementation:**
- Uses `threading.RLock()` for re-entrant locks
- All operations wrapped in lock context
- Safe for concurrent access

```python
class ContextManager:
    def __init__(self):
        self._lock = threading.RLock()
        # ...
    
    def get_context(self, session_id: str) -> Dict:
        with self._lock:
            # Thread-safe operation
            ...
    
    def add_thought(self, session_id: str, thought: str) -> int:
        with self._lock:
            # Thread-safe operation
            ...
```

#### Background Cleanup Thread

- Automatic cleanup runs in background
- Configurable cleanup interval
- Safe shutdown mechanism

```python
def _start_cleanup_thread(self) -> None:
    def cleanup_worker():
        while not self._stop_cleanup.wait(interval):
            self.cleanup_old_sessions()
    
    self._cleanup_thread = threading.Thread(
        target=cleanup_worker, daemon=True
    )
    self._cleanup_thread.start()
```

### Performance Optimizations

#### 1. Memory Management
- **FIFO Eviction**: Oldest thoughts removed when limit reached
- **Automatic Cleanup**: Old sessions cleaned automatically
- **Configurable Limits**: Adjust based on use case

#### 2. Efficient Data Structures
- Dictionary-based context storage
- List-based thought storage (ordered, indexed)
- Minimal overhead per operation

#### 3. Context Retrieval
- O(1) context lookup
- Lazy context creation
- Cached context access

### Performance Testing

Xem `tests/test_performance.py` cho comprehensive performance tests:
- Concurrent access tests
- Large thought handling
- Memory efficiency tests
- Cleanup performance

---

## 🔒 Security Considerations

### Security Features

#### 1. Input Validation
- **Length Limits**: Prevent excessive input
- **Type Validation**: Ensure correct data types
- **Sanitization**: Remove dangerous characters

#### 2. Resource Limits
- **Max Thoughts**: Prevent memory exhaustion
- **Max Length**: Limit individual thought size
- **Session Limits**: Automatic cleanup

#### 3. Privacy Controls
- **Optional Logging**: Thought content logging disabled by default
- **Session Isolation**: No cross-session access
- **In-Memory Only**: No persistent storage by default

#### 4. Thread Safety
- **Lock Protection**: All operations thread-safe
- **No Race Conditions**: Proper synchronization
- **Safe Shutdown**: Clean resource cleanup

### Security Configuration

**Production Settings:**
```bash
THINK_MAX_THOUGHTS=100
THINK_MAX_THOUGHT_LENGTH=5000
THINK_LOG_THOUGHTS=false
THINK_SANITIZE_INPUT=true
THINK_CLEANUP_HOURS=12
```

Xem chi tiết trong [SECURITY.md](./SECURITY.md).

---

## 🧪 Testing

### Test Suite Structure

#### 1. Unit Tests (`tests/test_context_manager.py`)
- Context creation and management
- Thought addition and retrieval
- Context formatting
- Cleanup operations

#### 2. Integration Tests (`tests/test_integration.py`)
- Multi-step workflows
- Session isolation
- Context accumulation
- Error handling in workflows

#### 3. Performance Tests (`tests/test_performance.py`)
- Concurrent access performance
- Large thought handling
- Memory efficiency
- Cleanup performance
- Context retrieval speed

#### 4. Tool Tests (`tests/test_think_tool.py`)
- Tool initialization
- Parameter validation
- Error handling
- Response formatting

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov=tools

# Run specific test file
pytest tests/test_performance.py

# Run with verbose output
pytest -v
```

### Test Coverage

- **Unit Tests**: 15+ test cases
- **Integration Tests**: 10+ test cases
- **Performance Tests**: 7+ test cases
- **Total**: 32+ test cases

---

## 📖 Tài liệu Tham khảo

### Official Dify Documentation

#### 1. **Dify Plugin Development**
- **URL**: https://docs.dify.ai/plugin-dev-en
- **Nội dung**: 
  - Plugin development overview
  - Tool plugin development guide
  - General specifications
  - API references

#### 2. **Getting Started with Dify Plugins**
- **URL**: https://docs.dify.ai/plugin-dev-en/0211-getting-started-dify-tool
- **Nội dung**: 
  - Hello World guide
  - Quick start tutorial
  - Basic examples

#### 3. **Dify Plugin Cheatsheet**
- **URL**: https://docs.dify.ai/plugin-dev-en/0131-cheatsheet
- **Nội dung**:
  - Quick reference
  - Common code snippets
  - Troubleshooting guide

#### 4. **Tool Plugin Development**
- **URL**: https://docs.dify.ai/plugin-dev-en/0222-tool-plugin
- **Nội dung**:
  - Detailed tool development guide
  - Google Search example
  - Best practices

#### 5. **General Specifications**
- **URL**: https://docs.dify.ai/plugin-dev-en/0411-general-specifications
- **Nội dung**:
  - Manifest structure
  - Tool specifications
  - API contracts

### Claude Think Tool Research

#### 6. **Claude Think Tool Article**
- **File**: `claude-think-tool.md` (local)
- **Nội dung**:
  - Original research paper
  - Implementation details
  - Performance benchmarks (τ-Bench)
  - Best practices

#### 7. **Key Research Findings**
- **τ-Bench Results**: 54% improvement in complex scenarios
- **SWE-Bench Results**: 1.6% average improvement
- **Use Cases**: When to use vs. when not to use

### Dify SDK References

#### 8. **Dify Plugin SDK GitHub**
- **URL**: https://github.com/langgenius/dify-plugin-sdks
- **Nội dung**:
  - Source code
  - API documentation
  - Examples

#### 9. **Dify Plugin CLI**
- **URL**: https://github.com/langgenius/dify-plugin-daemon
- **Nội dung**:
  - CLI tool source
  - Installation instructions
  - Usage examples

### Benchmark References

#### 10. **τ-Bench (Tau-Bench)**
- **Mục đích**: Benchmark cho customer service scenarios
- **Metrics**: pass^k (consistency metric)
- **Domain**: Airline, Retail

#### 11. **SWE-Bench**
- **Mục đích**: Benchmark cho software engineering tasks
- **Metrics**: Pass rate
- **Context**: Bug fixing, code changes

### Related Concepts

#### 12. **Extended Thinking**
- **Definition**: Claude's built-in extended thinking capability
- **Difference**: Extended thinking vs. Think tool
- **Use Cases**: When to use each

#### 13. **Agent Strategy Plugins**
- **URL**: https://docs.dify.ai/plugin-dev-en/9433-agent-strategy-plugin
- **Nội dung**: Custom Agent thinking strategies

### Best Practices

#### 14. **Plugin Development Best Practices**
- **Code Organization**: Structure và naming conventions
- **Error Handling**: Proper exception handling
- **Logging**: Structured logging practices
- **Testing**: Unit và integration testing

#### 15. **Tool Design Principles**
- **Single Responsibility**: Mỗi tool một nhiệm vụ
- **Idempotency**: Tool calls có thể repeat
- **Error Recovery**: Graceful error handling

### Community Resources

#### 16. **Dify Community**
- **URL**: https://community.dify.ai
- **Nội dung**: 
  - Community forums
  - Q&A
  - Plugin examples

#### 17. **Dify Marketplace**
- **URL**: https://marketplace.dify.ai
- **Nội dung**:
  - Published plugins
  - Examples và patterns
  - Publishing guidelines

### Implementation Examples

#### 18. **Google Search Tool Example**
- **Location**: Dify documentation
- **Nội dung**: Complete implementation example
- **Components**: Provider, Tool, YAML configs

#### 19. **Slack Bot Plugin**
- **URL**: https://docs.dify.ai/plugin-dev-en/0432-develop-a-slack-bot-plugin
- **Nội dung**: Complex plugin example

### Technical References

#### 20. **Python 3.12 Documentation**
- **URL**: https://docs.python.org/3.12/
- **Nội dung**: Python language reference

#### 21. **Pydantic Documentation**
- **URL**: https://docs.pydantic.dev
- **Nội dung**: Data validation library

#### 22. **Pytest Documentation**
- **URL**: https://docs.pytest.org
- **Nội dung**: Testing framework

### Additional Reading

#### 23. **Agentic Tool Use Patterns**
- **Context**: LLM tool use best practices
- **Topics**: Sequential tool calls, error handling, context management

#### 24. **Context Management Strategies**
- **Topics**: Session management, context accumulation, memory management

#### 25. **Prompt Engineering for Tools**
- **Topics**: Writing effective tool descriptions, examples, guidelines

---

## 🔗 Quick Links

### Development
- [Dify Plugin CLI Download](https://github.com/langgenius/dify-plugin-daemon/releases)
- [Dify Plugin SDK Source](https://github.com/langgenius/dify-plugin-sdks)
- [Dify Documentation](https://docs.dify.ai)

### Research
- `claude-think-tool.md` - Claude research paper
- `PROJECT-PLAN.md` - Project planning document
- `AGENTS.md` - Dify plugin cheatsheet

### Project Documentation
- `USER-GUIDE.md` - Complete user guide
- `EXAMPLES.md` - Usage examples
- `API-DOCS.md` - API documentation
- `CONFIGURATION.md` - Configuration guide
- `SECURITY.md` - Security considerations
- `PROGRESS.md` - Project progress summary
- `PHASE1-SUMMARY.md` - Phase 1 completion summary
- `PHASE2-SUMMARY.md` - Phase 2 completion summary
- `PHASE3-SUMMARY.md` - Phase 3 completion summary

### Tools
- [Python 3.12 Download](https://www.python.org/downloads/)
- [VS Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/)

---

## 📋 Quick Reference

### Core Components Summary

| Component | File | Purpose | Key Features |
|-----------|------|---------|--------------|
| **ThinkTool** | `tools/think_tool.py` | Tool implementation | Enhanced error handling, config integration |
| **ContextManager** | `src/context_manager.py` | Context management | Thread-safe, auto cleanup, stats |
| **PluginConfig** | `src/config.py` | Configuration | Environment variables, validation |
| **Error Handling** | `src/errors.py` | Custom exceptions | Type-safe error hierarchy |
| **PromptTemplates** | `src/prompt_templates.py` | Domain prompts | Multiple domain support |
| **ThinkProvider** | `provider/think_provider.py` | Provider class | Tool registration |

### Configuration Quick Reference

| Variable | Default | Range/Possible Values |
|----------|---------|----------------------|
| `THINK_MAX_THOUGHTS` | 100 | 1-1000 |
| `THINK_CLEANUP_HOURS` | 24 | ≥ 1 |
| `THINK_AUTO_CLEANUP` | true | true/false |
| `THINK_MAX_THOUGHT_LENGTH` | 10000 | 100-100000 |
| `THINK_LOG_LEVEL` | INFO | DEBUG/INFO/WARNING/ERROR/CRITICAL |
| `THINK_LOG_THOUGHTS` | false | true/false |
| `THINK_SANITIZE_INPUT` | true | true/false |
| `THINK_ALLOW_EMPTY_THOUGHTS` | false | true/false |

### Test Suite Quick Reference

| Test File | Test Cases | Coverage |
|-----------|-----------|----------|
| `test_context_manager.py` | 15+ | Context operations |
| `test_think_tool.py` | 3+ | Tool functionality |
| `test_integration.py` | 10+ | Integration workflows |
| `test_performance.py` | 7+ | Performance metrics |

### Related Documentation

- [CONFIGURATION.md](./CONFIGURATION.md) - Complete configuration guide
- [SECURITY.md](./SECURITY.md) - Security considerations
- [USER-GUIDE.md](./USER-GUIDE.md) - User guide
- [EXAMPLES.md](./EXAMPLES.md) - Usage examples
- [API-DOCS.md](./API-DOCS.md) - API documentation
- [PROJECT-PLAN.md](./PROJECT-PLAN.md) - Project planning

---

**Document Version**: 2.0  
**Last Updated**: [Current Date]  
**Status**: Complete - Phase 3 Optimized  
**Maintained by**: Development Team

