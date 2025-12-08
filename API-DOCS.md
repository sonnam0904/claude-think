# API Documentation - Claude Think Tool

## 📚 Table of Contents

1. [Tool Specification](#tool-specification)
2. [Input/Output Formats](#inputoutput-formats)
3. [Context Manager API](#context-manager-api)
4. [Error Codes](#error-codes)
5. [Response Formats](#response-formats)

---

## 🔧 Tool Specification

### Tool Name

`think`

### Tool Description

Use this tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.

### Tool Manifest

Located at: `tools/think.yaml`

```yaml
identity:
    name: think
    author: Claude Think Tool Team
    label:
        en_US: Think
        zh_Hans: 思考

parameters:
    - name: thought
      type: string
      required: true
      llm_description: A thought to think about. Be specific and detailed in your reasoning.
```

---

## 📥 Input/Output Formats

### Input Parameters

#### `thought` (required)

- **Type**: `string`
- **Required**: Yes
- **Description**: The thought to think about. Be specific and detailed in your reasoning.
- **Example**: 
  ```json
  {
    "thought": "User wants to cancel flight ABC123. Need to verify: user ID, reservation ID, reason."
  }
  ```

### Output Format

#### Success Response

```json
{
  "status": "success",
  "step": 1,
  "thought": "User wants to cancel flight ABC123. Need to verify: user ID, reservation ID, reason.",
  "context_size": 1,
  "session_id": "workflow-uuid"
}
```

#### Error Response

```json
{
  "status": "error",
  "message": "Error: 'thought' parameter is required"
}
```

---

## 🗄️ Context Manager API

### Overview

The ContextManager manages session-based context accumulation for thoughts.

### Methods

#### `get_context(session_id: str) -> Dict`

Get or create context for a session.

**Parameters:**
- `session_id` (str): Unique session identifier (typically workflow_id)

**Returns:**
- `Dict`: Session context containing:
  - `session_id`: Session identifier
  - `thoughts`: List of thought entries
  - `metadata`: Metadata including created_at, last_updated, total_steps

**Example:**
```python
context = context_manager.get_context("workflow-123")
# Returns:
# {
#   "session_id": "workflow-123",
#   "thoughts": [...],
#   "metadata": {
#     "created_at": "2024-01-01T00:00:00Z",
#     "last_updated": "2024-01-01T00:00:01Z",
#     "total_steps": 2
#   }
# }
```

#### `add_thought(session_id: str, thought: str, context: Optional[Dict] = None) -> int`

Add a thought to the context.

**Parameters:**
- `session_id` (str): Session identifier
- `thought` (str): Thought content
- `context` (Optional[Dict]): Existing context (optional)

**Returns:**
- `int`: Step number (1-based)

**Example:**
```python
step = context_manager.add_thought(
    session_id="workflow-123",
    thought="Analyze user request"
)
# Returns: 1
```

#### `get_all_thoughts(session_id: str) -> List[Dict]`

Get all thoughts for a session.

**Parameters:**
- `session_id` (str): Session identifier

**Returns:**
- `List[Dict]`: List of thought entries, each containing:
  - `timestamp`: ISO timestamp
  - `thought`: Thought content
  - `step`: Step number

**Example:**
```python
thoughts = context_manager.get_all_thoughts("workflow-123")
# Returns:
# [
#   {
#     "timestamp": "2024-01-01T00:00:00Z",
#     "thought": "First thought",
#     "step": 1
#   },
#   {
#     "timestamp": "2024-01-01T00:00:01Z",
#     "thought": "Second thought",
#     "step": 2
#   }
# ]
```

#### `get_formatted_context(session_id: str) -> str`

Get formatted context string for Node Agent.

**Parameters:**
- `session_id` (str): Session identifier

**Returns:**
- `str`: Formatted string of all thoughts

**Example:**
```python
formatted = context_manager.get_formatted_context("workflow-123")
# Returns:
# "Previous thoughts in this session:
#
# Step 1 (2024-01-01T00:00:00Z):
# First thought
#
# Step 2 (2024-01-01T00:00:01Z):
# Second thought
# "
```

#### `clear_context(session_id: str) -> None`

Clear context for a session.

**Parameters:**
- `session_id` (str): Session identifier

**Example:**
```python
context_manager.clear_context("workflow-123")
```

#### `get_context_summary(session_id: str) -> Dict`

Get summary of context for a session.

**Parameters:**
- `session_id` (str): Session identifier

**Returns:**
- `Dict`: Context summary containing:
  - `session_id`: Session identifier
  - `total_steps`: Number of thoughts
  - `created_at`: Creation timestamp
  - `last_updated`: Last update timestamp

**Example:**
```python
summary = context_manager.get_context_summary("workflow-123")
# Returns:
# {
#   "session_id": "workflow-123",
#   "total_steps": 5,
#   "created_at": "2024-01-01T00:00:00Z",
#   "last_updated": "2024-01-01T00:05:00Z"
# }
```

---

## ⚠️ Error Codes

### Missing Parameter

**Error**: `'thought' parameter is required`

**Cause**: The `thought` parameter was not provided in the tool call.

**Solution**: Ensure the `thought` parameter is included in the tool call.

**Example:**
```json
{
  "thought": "Your thought here"
}
```

### Empty Thought

**Error**: `'thought' parameter is required`

**Cause**: The `thought` parameter was provided but is an empty string.

**Solution**: Provide a non-empty thought string.

### Context Processing Error

**Error**: `Error processing thought: {error_message}`

**Cause**: An internal error occurred while processing the thought.

**Solution**: Check plugin logs for detailed error information.

---

## 📤 Response Formats

### JSON Message Format

When using `create_json_message()`, the response is formatted as:

```json
{
  "status": "success",
  "step": 1,
  "thought": "...",
  "context_size": 1,
  "session_id": "..."
}
```

### Text Message Format

When using `create_text_message()`, the response is a plain text string:

```
Error: 'thought' parameter is required
```

---

## 🔐 Session Management

### Session ID

The session ID is automatically derived from:
1. `runtime.workflow_id` (preferred)
2. `runtime.session_id` (fallback)
3. `"default"` (if neither available)

### Context Limits

- **Max Thoughts per Session**: 100 (configurable)
- **Behavior**: When limit is reached, oldest thoughts are removed (FIFO)
- **Retention**: Context persists for the duration of the workflow session

---

## 📝 Usage Examples

### Basic Usage

```python
# Tool call
think(thought="Analyze user request and identify requirements")

# Response
{
  "status": "success",
  "step": 1,
  "thought": "Analyze user request and identify requirements",
  "context_size": 1,
  "session_id": "workflow-abc123"
}
```

### Multi-Step Usage

```python
# Step 1
think(thought="First thought")
# Response: { "status": "success", "step": 1, ... }

# Step 2
think(thought="Second thought")
# Response: { "status": "success", "step": 2, "context_size": 2, ... }

# Step 3
think(thought="Third thought")
# Response: { "status": "success", "step": 3, "context_size": 3, ... }
```

---

## 🔗 Related Documentation

- [USER-GUIDE.md](./USER-GUIDE.md) - User guide with examples
- [EXAMPLES.md](./EXAMPLES.md) - Comprehensive examples
- [INSTRUCTIONS.md](./INSTRUCTIONS.md) - Technical implementation details

---

**Last Updated:** [Current Date]  
**API Version:** 1.0.0

