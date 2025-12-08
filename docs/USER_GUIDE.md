# User Guide - Claude Think Tool for Dify

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using the Think Tool](#using-the-think-tool)
4. [Best Practices](#best-practices)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)

---

## Introduction

The Claude Think Tool is a Dify plugin that enables Node Agents to perform structured multi-step reasoning. Based on Claude's research showing 54% improvement in complex scenarios, this tool helps agents:

- **Analyze complex situations** with structured thinking
- **Accumulate context** across multiple reasoning steps
- **Follow policies** more consistently
- **Make better decisions** through systematic reasoning

### Key Features

- ✅ **Multi-Step Thinking**: Perform structured reasoning across multiple steps
- ✅ **Context Accumulation**: Automatically accumulates thoughts in session context
- ✅ **Zero Configuration**: No credentials required
- ✅ **Domain-Specific**: Pre-built templates for different use cases

---

## Getting Started

### Installation

1. **Install the plugin** in your Dify workspace
2. **Enable the plugin** for your Node Agents
3. **Start using** the think tool in your workflows

The think tool will automatically appear in your Node Agent's available tools list.

### Basic Usage

The think tool accepts one parameter:

- **`thought`** (required): The thought or reasoning step you want to record

Example:
```
think(thought="Analyze the user request and list required information")
```

---

## Using the Think Tool

### When to Use

Use the think tool when you need to:

1. **Process Tool Results**: After receiving results from other tools, think about what they mean
2. **Follow Policies**: Break down policy requirements and verify compliance
3. **Plan Multi-Step Actions**: Structure your approach before executing complex tasks
4. **Make Decisions**: Systematically evaluate options before choosing
5. **Validate Information**: Check if you have all required information

### When NOT to Use

Avoid using the think tool for:

- ❌ Simple, single-step operations
- ❌ Non-sequential tool calls
- ❌ Tasks with no constraints or policies
- ❌ Straightforward instruction following

### Basic Pattern

```
1. Receive user request or tool result
2. Call think() to analyze and plan
3. Execute actions (tool calls)
4. Call think() again to validate results
5. Respond to user
```

---

## Best Practices

### 1. Structure Your Thinking

Organize your thoughts clearly:

```
think(thought="
- User wants to cancel flight ABC123
- Need to verify: user ID, reservation ID
- Check cancellation rules:
  * Within 24h of booking?
  * Ticket class and insurance?
- Plan: collect info, verify rules
")
```

### 2. Use Multiple Steps

Break complex reasoning into multiple steps:

```
Step 1: think("Analyze request and identify requirements")
Step 2: think("List policies that apply")
Step 3: think("Check if all info is collected")
Step 4: think("Verify compliance with policies")
Step 5: think("Plan the action")
```

### 3. Reference Previous Thoughts

The tool automatically accumulates context. Each new thought builds on previous ones:

```
think("User wants to book 3 tickets")
# ... some tool calls ...
think("Based on previous analysis, check membership tier for baggage")
```

### 4. Use Domain-Specific Patterns

#### For Customer Service:

```
think("
User request: [request]
- Policies that apply: [list]
- Required information: [list]
- Compliance check: [verification]
- Action plan: [steps]
")
```

#### For Multi-Step Tool Chains:

```
think("Plan the sequence: Tool A → Tool B → Tool C")
# Execute Tool A
think("Analyze Tool A result, adjust plan if needed")
# Execute Tool B
think("Synthesize Tool A and B results")
# Execute Tool C
```

#### For Decision Making:

```
think("List factors: cost, time, quality")
think("Evaluate Option A: pros/cons")
think("Evaluate Option B: pros/cons")
think("Compare and select best option")
```

---

## Examples

### Example 1: Policy-Heavy Customer Service

**Scenario**: User wants to cancel a flight

```
1. think("
   User wants to cancel flight ABC123
   - Need to verify: user ID, reservation ID, reason
   - Check cancellation rules:
     * Is it within 24h of booking?
     * If not, check ticket class and insurance
   - Verify no segments flown
   - Plan: collect missing info, verify rules
   ")

2. [Tool call: Get user reservation info]

3. think("
   Reservation retrieved:
   - Booking date: [date] (check 24h rule)
   - Ticket class: [class] (check refund policy)
   - Segments: [list] (verify not flown)
   - Compliance: [status]
   ")

4. [Tool call: Process cancellation if compliant]

5. think("Cancellation processed, verify success and notify user")
```

### Example 2: Multi-Step Data Processing

**Scenario**: Process customer order with validation

```
1. think("Plan: Validate order → Check inventory → Calculate shipping → Process payment")

2. [Tool call: Validate order]

3. think("Order validated. Next: Check inventory for items")

4. [Tool call: Check inventory]

5. think("Inventory checked. Items available. Calculate shipping costs")

6. [Tool call: Calculate shipping]

7. think("All checks passed. Ready to process payment")

8. [Tool call: Process payment]
```

### Example 3: Complex Decision Making

**Scenario**: Choose best shipping option

```
1. think("Factors to consider: cost, speed, reliability")

2. think("
   Option A - Standard Shipping:
   - Cost: $10
   - Speed: 5-7 days
   - Reliability: 95%
   ")

3. think("
   Option B - Express Shipping:
   - Cost: $25
   - Speed: 2-3 days
   - Reliability: 98%
   ")

4. think("
   Comparison:
   - If cost-sensitive: Option A
   - If time-sensitive: Option B
   - User preference: [check]
   ")

5. [Tool call: Select and apply option]
```

---

## Advanced Usage

### Context Accumulation

The think tool automatically accumulates thoughts in the session. All thoughts in a workflow session are stored together:

- Each thought is numbered sequentially (Step 1, Step 2, ...)
- Thoughts are timestamped
- Previous thoughts are available for reference
- Context is session-specific (isolated per workflow)

### Session Management

- Each workflow execution has its own session
- Context persists throughout the workflow execution
- Context is cleared when workflow completes
- Maximum 100 thoughts per session (configurable)

---

## Troubleshooting

### Tool Not Available

**Problem**: Think tool doesn't appear in tool list

**Solution**:
- Verify plugin is installed and enabled
- Check plugin permissions in Dify
- Restart the Node Agent if needed

### Context Not Accumulating

**Problem**: Thoughts are not being stored together

**Solution**:
- Ensure you're using the same workflow session
- Check that workflow_id is consistent
- Verify no errors in tool execution logs

### Too Many Thoughts

**Problem**: Reaching thought limit (100 thoughts)

**Solution**:
- The tool automatically removes oldest thoughts (FIFO)
- Consider summarizing previous thoughts
- Break workflows into smaller chunks if needed

### Thoughts Not Useful

**Problem**: Agent not using think tool effectively

**Solution**:
- Add system prompt with examples (see Best Practices)
- Provide domain-specific guidance
- Show examples of effective thinking patterns

---

## Tips for Better Results

### 1. Add System Prompts

Include guidance in your Node Agent's system prompt:

```
## Using the think tool

Before taking any action, use the think tool to:
- List rules that apply
- Check required information
- Verify compliance
- Plan your approach
```

### 2. Provide Examples

Show the agent examples of good thinking:

```
<example>
think("
User wants to cancel booking
- Verify: user ID, booking ID
- Check: cancellation policy, timing
- Plan: collect info → verify → execute
")
</example>
```

### 3. Domain-Specific Guidance

Tailor your prompts to your domain:
- **Customer Service**: Focus on policies and compliance
- **Data Processing**: Focus on validation and transformation
- **Decision Making**: Focus on evaluation and comparison

---

## Frequently Asked Questions

### Q: Does the think tool make external API calls?

**A**: No. The think tool only logs thoughts internally. It doesn't make any external calls or change any data.

### Q: How long is context stored?

**A**: Context is stored for the duration of the workflow execution. It's cleared when the workflow completes.

### Q: Can I access previous thoughts?

**A**: Yes! Previous thoughts are automatically available in the session context. The agent can reference them in subsequent tool calls.

### Q: Is there a limit on thought length?

**A**: There's no hard limit, but keep thoughts concise and focused. Very long thoughts may impact performance.

### Q: Can I use think tool multiple times?

**A**: Absolutely! That's the main purpose - to enable multi-step structured thinking.

---

## Additional Resources

- [PROJECT-PLAN.md](../PROJECT-PLAN.md) - Project overview
- [INSTRUCTIONS.md](../INSTRUCTIONS.md) - Technical documentation
- [claude-think-tool.md](../claude-think-tool.md) - Original research

---

**Version**: 0.1.0  
**Last Updated**: [Current Date]

