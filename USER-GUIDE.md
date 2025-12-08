# User Guide - Claude Think Tool Plugin

## 📖 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [When to Use the Think Tool](#when-to-use-the-think-tool)
5. [Best Practices](#best-practices)
6. [Example Scenarios](#example-scenarios)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The Claude Think Tool enables Dify Node Agents to perform structured multi-step reasoning by creating a dedicated "thinking space" during complex tool use scenarios. This tool helps agents:

- Analyze tool outputs carefully
- Make better decisions in policy-heavy environments
- Handle sequential decision-making where mistakes are costly
- Accumulate context across multiple reasoning steps

**Key Benefits:**
- ✅ 54% improvement in complex scenarios (based on τ-Bench research)
- ✅ Better policy compliance
- ✅ More consistent decision-making
- ✅ Richer context for complex workflows

---

## 📦 Installation

### Prerequisites

- Dify instance (Cloud or Self-hosted)
- Node Agent configured in your workflow

### Installation Steps

1. **Install the Plugin**:
   - Go to Plugin Management in your Dify workspace
   - Install "Claude Think Tool" plugin
   - No credentials required - ready to use immediately

2. **Enable in Workflow**:
   - The think tool will automatically appear in your Node Agent's available tools
   - No additional configuration needed

3. **Verify Installation**:
   - Check that "think" tool appears in your Node Agent's tool list
   - Test with a simple workflow

---

## 🚀 Basic Usage

### Simple Example

When a Node Agent needs to reason about something, it can call the think tool:

```
think(thought="Let me analyze the user's request. They want to cancel a flight reservation. I need to verify: user ID, reservation ID, and cancellation reason.")
```

### Multi-Step Thinking

The think tool accumulates thoughts across multiple calls in the same workflow session:

**Step 1:**
```
think(thought="User wants to cancel flight ABC123. Need to verify: user ID, reservation ID, reason.")
```

**Step 2:**
```
think(thought="Check cancellation rules: Is it within 24h of booking? If not, check ticket class and insurance.")
```

**Step 3:**
```
think(thought="Verify no segments flown or are in the past. Plan: collect missing info, verify rules, get confirmation.")
```

All thoughts are stored in context and can be referenced by the agent.

---

## 💡 When to Use the Think Tool

### ✅ Ideal Use Cases

1. **Policy-Heavy Environments**
   - Customer service with complex rules
   - Compliance checking
   - Multi-step validation processes

2. **Sequential Tool Chains**
   - When each tool call depends on previous results
   - Need to analyze intermediate results
   - Decision points between tool calls

3. **Complex Decision Making**
   - Multiple options to evaluate
   - Need to consider trade-offs
   - Costly mistakes if wrong decision

### ❌ Not Recommended For

1. **Simple, Single Tool Calls**
   - Direct API calls with no reasoning needed
   - Parallel tool calls
   - Straightforward data retrieval

2. **Non-Sequential Operations**
   - Independent tool calls
   - Tasks with minimal constraints

---

## 🎓 Best Practices

### 1. Use Clear, Structured Thoughts

**Good:**
```
think(thought="Step 1: Analyze user request. User wants to book 3 tickets. Step 2: Identify requirements - need user ID, destination, dates, number of bags. Step 3: Check membership tier for baggage allowance.")
```

**Not Good:**
```
think(thought="figure out what user wants")
```

### 2. Break Down Complex Tasks

Instead of one long thought, use multiple focused thoughts:

```
think(thought="Analyze booking request: 3 tickets to NYC with 2 checked bags each")
think(thought="Check membership tier - will determine baggage fees")
think(thought="Verify payment methods in user profile")
think(thought="Calculate total: ticket price + any bag fees")
```

### 3. Reference Previous Context

When making a decision, reference what you thought about earlier:

```
think(thought="Based on my previous analysis, the user is a silver member with 2 free bags. This means 3 passengers × 2 bags = 6 bags total, but 3 × 2 free = 6 free. So no extra bag fees apply.")
```

### 4. Use for Validation

Always validate before taking action:

```
think(thought="Before executing cancellation: Verify all rules checked ✓, All required info collected ✓, User confirmed ✓, Ready to proceed.")
```

### 5. Document Your Reasoning Process

Make your thoughts detailed enough to understand later:

```
think(thought="Cancellation rule analysis: Booking was 48 hours ago (outside 24h window). Ticket class is Economy Basic (non-refundable). However, user has travel insurance that covers cancellation. Conclusion: Cancellation is allowed with insurance claim.")
```

---

## 📝 Example Scenarios

### Scenario 1: Airline Customer Service

**User Request:** "I want to cancel my flight ABC123"

**Agent Workflow:**

1. **Initial Analysis:**
   ```
   think(thought="User wants to cancel flight ABC123. Need to verify: user ID, reservation ID, reason for cancellation.")
   ```

2. **Retrieve Information:**
   - Tool: Get user reservation details

3. **Policy Check:**
   ```
   think(thought="Retrieved reservation. Booking was 48 hours ago (outside 24h window). Ticket is Economy Basic. Need to check: cancellation rules for this ticket class, travel insurance status, refund eligibility.")
   ```

4. **Decision:**
   ```
   think(thought="Analysis complete: Ticket is non-refundable but user has insurance. Can cancel with insurance claim. Plan: Inform user of cancellation policy, process cancellation, initiate insurance claim.")
   ```

5. **Action:**
   - Tool: Process cancellation
   - Response to user

### Scenario 2: Multi-Step Data Processing

**Task:** Analyze customer data and generate report

**Agent Workflow:**

1. **Planning:**
   ```
   think(thought="Plan for data analysis: Step 1) Fetch customer data, Step 2) Validate data completeness, Step 3) Calculate metrics, Step 4) Format report")
   ```

2. **After Fetching Data:**
   ```
   think(thought="Data retrieved. Checking completeness: Customer ID ✓, Purchase history ✓, Missing: Last contact date. Need to fetch additional data.")
   ```

3. **After Processing:**
   ```
   think(thought="All data collected. Calculated metrics: Total purchases: $5000, Average order: $250, Last purchase: 30 days ago. Ready to format report.")
   ```

4. **Before Final Output:**
   ```
   think(thought="Report structure: Summary section with key metrics, Detailed breakdown by category, Recommendations based on purchase patterns. All sections ready.")
   ```

### Scenario 3: Complex Decision Making

**Task:** Choose best payment option from multiple methods

**Agent Workflow:**

1. **List Options:**
   ```
   think(thought="Available payment methods: Credit card (fees: 3%), PayPal (fees: 2.5%), Bank transfer (fees: 0% but 3-day delay). Order amount: $1000.")
   ```

2. **Evaluate Each:**
   ```
   think(thought="Credit card: Fast (instant), fees $30, secure. PayPal: Fast (instant), fees $25, secure, user prefers. Bank transfer: Slow (3 days), no fees, secure. User needs order quickly.")
   ```

3. **Decision:**
   ```
   think(thought="Decision: User needs order quickly (eliminates bank transfer). Between credit card and PayPal, PayPal is cheaper ($25 vs $30) and user prefers it. Choose PayPal.")
   ```

---

## 🔧 System Prompt Configuration

### Recommended System Prompt

Add this to your Node Agent's system prompt for optimal think tool usage:

```markdown
## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness
```

### Domain-Specific Prompts

See `src/prompt_templates.py` for domain-specific prompts (airline, retail, coding).

---

## 🐛 Troubleshooting

### Tool Not Appearing

**Problem:** Think tool doesn't show in Node Agent tool list

**Solutions:**
- Verify plugin is installed in workspace
- Check that Node Agent has access to tools
- Restart the plugin if running locally
- Check plugin logs for errors

### Thoughts Not Accumulating

**Problem:** Context seems to reset between tool calls

**Solutions:**
- Ensure all tool calls are in the same workflow session
- Check that session_id is consistent (should be automatic)
- Verify context manager is working (check logs)

### Too Many Thoughts

**Problem:** Context becomes too large, affecting performance

**Solutions:**
- Context manager automatically limits to 100 thoughts per session
- Older thoughts are removed (FIFO)
- Consider breaking into multiple workflows if needed

### Tool Call Errors

**Problem:** Think tool returns error

**Solutions:**
- Check that "thought" parameter is provided
- Verify thought is not empty string
- Check plugin logs for detailed error messages

---

## 📊 Tips for Maximum Effectiveness

1. **Start with Planning:** Use think tool early to plan your approach

2. **Validate Frequently:** Use think tool to validate before each major action

3. **Document Decisions:** Use think tool to document why you made a decision

4. **Reference Previous Thoughts:** Reference what you thought earlier in the same session

5. **Be Specific:** More detailed thoughts lead to better reasoning

---

## 🔗 Additional Resources

- [PROJECT-PLAN.md](./PROJECT-PLAN.md) - Project planning and research
- [INSTRUCTIONS.md](./INSTRUCTIONS.md) - Technical documentation
- [claude-think-tool.md](./claude-think-tool.md) - Original Claude research

---

**Last Updated:** [Current Date]  
**Plugin Version:** 0.1.0

