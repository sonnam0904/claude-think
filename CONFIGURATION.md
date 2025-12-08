# Configuration Guide - Claude Think Tool

## 📋 Overview

The Claude Think Tool plugin supports configuration via environment variables. This guide explains all available configuration options.

## 🔧 Configuration Options

### Context Management

#### `THINK_MAX_THOUGHTS`

- **Type**: Integer
- **Default**: `100`
- **Range**: 1-1000
- **Description**: Maximum number of thoughts per session
- **Example**: `THINK_MAX_THOUGHTS=200`

**Notes**:
- When limit is reached, oldest thoughts are removed (FIFO)
- Higher values use more memory
- Recommended: 50-200 for most use cases

#### `THINK_CLEANUP_HOURS`

- **Type**: Integer
- **Default**: `24`
- **Minimum**: 1
- **Description**: Hours after which old sessions are automatically cleaned up
- **Example**: `THINK_CLEANUP_HOURS=12`

**Notes**:
- Automatic cleanup runs in background thread
- Cleaned sessions cannot be recovered
- Lower values free memory faster but may remove active sessions

#### `THINK_AUTO_CLEANUP`

- **Type**: Boolean
- **Default**: `true`
- **Values**: `true`, `false`, `1`, `0`, `yes`, `no`
- **Description**: Enable automatic cleanup of old sessions
- **Example**: `THINK_AUTO_CLEANUP=true`

**Notes**:
- Disable if you want manual control over cleanup
- Manual cleanup still available via API

### Performance Settings

#### `THINK_MAX_THOUGHT_LENGTH`

- **Type**: Integer
- **Default**: `10000`
- **Range**: 100-100000
- **Description**: Maximum characters allowed per thought
- **Example**: `THINK_MAX_THOUGHT_LENGTH=5000`

**Notes**:
- Larger values allow more detailed thoughts but use more memory
- Recommended: 5000-10000 for most use cases
- Validation error if exceeded

### Logging Settings

#### `THINK_LOG_LEVEL`

- **Type**: String
- **Default**: `INFO`
- **Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Description**: Logging level for the plugin
- **Example**: `THINK_LOG_LEVEL=DEBUG`

**Notes**:
- DEBUG provides detailed information for troubleshooting
- INFO is recommended for production
- WARNING and above for minimal logging

#### `THINK_LOG_THOUGHTS`

- **Type**: Boolean
- **Default**: `false`
- **Values**: `true`, `false`, `1`, `0`, `yes`, `no`
- **Description**: Whether to log thought content (privacy consideration)
- **Example**: `THINK_LOG_THOUGHTS=false`

**Notes**:
- Set to `false` in production to avoid logging sensitive data
- Useful for debugging in development
- Only logs thought length when disabled

### Security Settings

#### `THINK_ALLOW_EMPTY_THOUGHTS`

- **Type**: Boolean
- **Default**: `false`
- **Values**: `true`, `false`, `1`, `0`, `yes`, `no`
- **Description**: Allow empty thoughts (not recommended)
- **Example**: `THINK_ALLOW_EMPTY_THOUGHTS=false`

**Notes**:
- Not recommended for production
- May be useful for testing
- Empty thoughts provide no value

#### `THINK_SANITIZE_INPUT`

- **Type**: Boolean
- **Default**: `true`
- **Values**: `true`, `false`, `1`, `0`, `yes`, `no`
- **Description**: Sanitize input by removing null bytes and control characters
- **Example**: `THINK_SANITIZE_INPUT=true`

**Notes**:
- Recommended to keep enabled
- Prevents potential issues with special characters
- Minimal performance impact

## 📝 Configuration Examples

### Development Configuration

```bash
# .env file for development
THINK_MAX_THOUGHTS=500
THINK_MAX_THOUGHT_LENGTH=10000
THINK_LOG_LEVEL=DEBUG
THINK_LOG_THOUGHTS=true
THINK_CLEANUP_HOURS=24
THINK_AUTO_CLEANUP=true
THINK_SANITIZE_INPUT=true
```

### Production Configuration

```bash
# .env file for production
THINK_MAX_THOUGHTS=100
THINK_MAX_THOUGHT_LENGTH=5000
THINK_LOG_LEVEL=INFO
THINK_LOG_THOUGHTS=false
THINK_CLEANUP_HOURS=12
THINK_AUTO_CLEANUP=true
THINK_SANITIZE_INPUT=true
THINK_ALLOW_EMPTY_THOUGHTS=false
```

### High-Performance Configuration

```bash
# For high-volume scenarios
THINK_MAX_THOUGHTS=50
THINK_MAX_THOUGHT_LENGTH=5000
THINK_CLEANUP_HOURS=6
THINK_AUTO_CLEANUP=true
THINK_LOG_LEVEL=WARNING
THINK_LOG_THOUGHTS=false
```

### Memory-Conscious Configuration

```bash
# Minimal memory usage
THINK_MAX_THOUGHTS=50
THINK_MAX_THOUGHT_LENGTH=2000
THINK_CLEANUP_HOURS=4
THINK_AUTO_CLEANUP=true
```

## 🔍 Configuration Validation

Configuration values are validated at startup. Invalid values will:
1. Log an error
2. Fall back to default values
3. Continue with default configuration

### Common Validation Errors

- `max_thoughts must be at least 1`: Value too small
- `max_thoughts cannot exceed 1000`: Value too large
- `Invalid log_level`: Log level not recognized
- `max_thought_length must be at least 100`: Thought length limit too small

## 🚀 Configuration Loading

Configuration is loaded from environment variables when the plugin starts:

1. **Environment Variables**: Checked first
2. **Default Values**: Used if environment variable not set
3. **Validation**: Values validated on load
4. **Fallback**: Invalid values revert to defaults

## 📊 Configuration Impact

### Memory Usage

- **Thoughts per Session**: More thoughts = more memory
- **Thought Length**: Longer thoughts = more memory per thought
- **Number of Sessions**: More active sessions = more memory

**Memory Estimate**:
- Per thought: ~200-1000 bytes (depending on length)
- Per session: ~20KB-100KB (with 100 thoughts)
- Multiple sessions: Linear scaling

### Performance Impact

- **Cleanup Interval**: More frequent cleanup = slight CPU overhead
- **Auto Cleanup**: Minimal impact (background thread)
- **Input Sanitization**: Negligible impact
- **Logging Level**: DEBUG logging has minor performance impact

## 🛠️ Troubleshooting

### Configuration Not Applied

**Issue**: Changes to environment variables not taking effect

**Solutions**:
- Restart the plugin
- Verify environment variable names (case-sensitive)
- Check `.env` file is in correct location
- Verify variable format (no quotes needed for most values)

### Memory Issues

**Issue**: High memory usage

**Solutions**:
- Reduce `THINK_MAX_THOUGHTS`
- Reduce `THINK_MAX_THOUGHT_LENGTH`
- Decrease `THINK_CLEANUP_HOURS` for more frequent cleanup
- Enable `THINK_AUTO_CLEANUP` if disabled

### Too Many Old Sessions

**Issue**: Old sessions not being cleaned up

**Solutions**:
- Verify `THINK_AUTO_CLEANUP=true`
- Reduce `THINK_CLEANUP_HOURS`
- Manually trigger cleanup via API

## 📚 Related Documentation

- [SECURITY.md](./SECURITY.md) - Security considerations
- [USER-GUIDE.md](./USER-GUIDE.md) - User guide
- [API-DOCS.md](./API-DOCS.md) - API documentation

---

**Last Updated**: [Current Date]

