# Examples - Claude Think Tool Usage

This document provides comprehensive examples of how to use the Claude Think Tool in various scenarios.

## 📚 Table of Contents

1. [Quick Start Examples](#quick-start-examples)
2. [Domain-Specific Examples](#domain-specific-examples)
3. [Workflow Examples](#workflow-examples)
4. [System Prompt Examples](#system-prompt-examples)

---

## 🚀 Quick Start Examples

### Example 1: Simple Reasoning

**Use Case:** Agent needs to reason about a user request before acting

```python
# Agent receives: "Can I return this item I bought last week?"

think(thought="User wants to return an item. I need to check: 
1. What item they bought
2. When they bought it (they said 'last week')
3. Return policy (usually 14-30 days)
4. Item condition
5. Return method

Let me start by retrieving their purchase history.")
```

**Result:** Agent has structured its approach before taking action.

### Example 2: Multi-Step Analysis

**Use Case:** Breaking down a complex task

```python
# Step 1: Initial analysis
think(thought="User wants to book a trip. Breaking down requirements:
- Destination: Not specified yet, need to ask
- Dates: Not specified yet, need to ask  
- Number of travelers: Not specified yet, need to ask
- Budget: Not specified yet, need to ask

First step: Ask user for these details.")

# Step 2: After getting information
think(thought="Got user requirements:
- Destination: Paris
- Dates: Next month, flexible
- Travelers: 2 adults
- Budget: $3000

Now I can search for flights and hotels within budget.")

# Step 3: After search results
think(thought="Found options:
- Flight: $1200 for 2 (within budget)
- Hotel: $150/night × 7 nights = $1050 (within budget)
- Total: $2250, leaving $750 for activities

All within budget. Ready to present options to user.")
```

---

## 🏢 Domain-Specific Examples

### Airline Customer Service

#### Example: Flight Cancellation

**Complete Workflow:**

```python
# User: "I need to cancel my flight ABC123"

# Step 1: Initial analysis
think(thought="User wants to cancel flight ABC123. 
I need to:
1. Verify user identity
2. Retrieve reservation details
3. Check cancellation policy
4. Verify no segments already flown
5. Process cancellation if allowed")

# Step 2: After retrieving reservation
think(thought="Retrieved reservation:
- User ID: verified ✓
- Reservation ID: ABC123 ✓
- Booking date: 48 hours ago
- Flight date: Next week
- Ticket class: Economy Basic
- Status: Confirmed

Cancellation policy check:
- Booking was 48h ago (outside 24h free cancellation window)
- Economy Basic is non-refundable
- BUT: User has travel insurance

Next: Check insurance coverage for cancellation")

# Step 3: After checking insurance
think(thought="Insurance check complete:
- Policy covers cancellation for any reason
- Claim can be filed after cancellation
- No refund from airline, but insurance will cover

Decision: Can proceed with cancellation. 
Will inform user about:
- Cancellation is possible
- No airline refund (non-refundable ticket)
- Insurance will cover via claim
- Need to confirm before proceeding")

# Step 4: Before processing
think(thought="Final validation:
✓ User identity verified
✓ Reservation found
✓ Cancellation rules checked
✓ Insurance verified
✓ User informed and confirmed

Ready to process cancellation.")
```

#### Example: Complex Booking

**Complete Workflow:**

```python
# User: "I want to book 3 tickets to NYC with 2 checked bags each"

# Step 1: Analyze requirements
think(thought="User booking request:
- Destination: NYC
- Tickets: 3
- Checked bags: 2 per passenger = 6 total bags

What I need:
1. User ID (to check membership tier for baggage allowance)
2. Payment methods in user profile
3. Ticket prices
4. Baggage fees calculation
5. Available payment methods and limits")

# Step 2: After getting user profile
think(thought="User profile retrieved:
- User ID: verified ✓
- Membership tier: Silver
- Silver tier baggage: 2 free checked bags per passenger

Baggage calculation:
- 3 passengers × 2 bags each = 6 bags total
- Silver tier: 3 passengers × 2 free bags = 6 free bags
- Extra bags needed: 0
- Baggage fees: $0

Payment methods in profile:
- Credit card: Visa ending in 1234 ✓
- Travel certificate: $500 available ✓

Payment rules:
- Max 1 travel certificate
- Can combine with credit card
- All payment methods must be in profile (both present ✓)")

# Step 3: After getting flight prices
think(thought="Flight prices retrieved:
- Economy tickets: $300 each
- Total for 3 tickets: $900
- Baggage fees: $0 (all covered by membership)
- Total cost: $900

Payment plan:
- Use travel certificate: $500
- Remaining: $400
- Use credit card for remaining: $400
- Total: $900 ✓

All checks passed. Ready to create booking.")

# Step 4: Before booking
think(thought="Final booking validation:
✓ 3 tickets available at $300 each
✓ Total cost: $900
✓ Baggage: 6 bags, all free with Silver membership
✓ Payment: $500 certificate + $400 credit card
✓ Both payment methods in profile
✓ All policies complied with

Ready to create booking and get confirmation.")
```

### Retail E-commerce

#### Example: Order Processing

```python
# Step 1: Receive order
think(thought="New order received:
- Customer ID: verified
- Items: 5 items in cart
- Shipping address: provided
- Payment: Credit card

Validation checklist:
1. All items in stock? (need to check)
2. Shipping address valid? (need to verify)
3. Payment method valid? (need to process)
4. Order total correct? (need to calculate)")

# Step 2: After inventory check
think(thought="Inventory check:
- Item 1: In stock ✓
- Item 2: In stock ✓
- Item 3: Low stock (2 left) - OK for order of 1 ✓
- Item 4: Out of stock ✗
- Item 5: In stock ✓

Issue found: Item 4 is out of stock.
Action needed: Remove item 4, notify customer, recalculate total")

# Step 3: After recalculation
think(thought="Order updated:
- Removed out-of-stock item
- New total: $450 (was $550)
- Customer notified about removal

Next steps:
1. Process payment for $450
2. Create order
3. Generate shipping label
4. Send confirmation email")
```

### Software Development / Coding

#### Example: Bug Fixing

```python
# Step 1: Analyze bug report
think(thought="Bug report analysis:
- Issue: User login failing for specific accounts
- Error: 'Invalid credentials' even with correct password
- Affected: ~10% of users with email domains ending in .edu

Hypothesis: 
- Might be email validation issue
- Could be case sensitivity problem
- Possible database query issue with special characters

Next: Search codebase for login logic")

# Step 2: After code review
think(thought="Found login code in auth.py:
- Uses email.toLowerCase() - should handle .edu correctly
- Database query uses LIKE with wildcard
- Issue: LIKE '%@domain.com' might not match '@domain.edu'

Root cause identified:
- Query pattern doesn't account for .edu TLD properly
- Need to fix database query or email matching logic

Fix options:
1. Fix query to handle all TLDs properly
2. Use exact email match instead of LIKE
3. Normalize email before query

Best option: Option 2 - exact match is more secure and faster")

# Step 3: Before implementing fix
think(thought="Fix plan:
- Change query from LIKE pattern to exact email match
- Add email normalization before query
- Update tests to cover .edu domain case
- Test with affected user accounts

Impact assessment:
- Low risk: Simple query change
- Backward compatible: Yes
- Performance: Better (exact match is faster)

Ready to implement.")
```

---

## 🔄 Workflow Examples

### Example: Customer Service Agent

**System Prompt:**
```markdown
You are a customer service agent. Before taking any action:
1. Use the think tool to analyze the request
2. Check all relevant policies
3. Verify you have all required information
4. Plan your response
5. Execute the plan
```

**Workflow:**
```
User Request
    ↓
think("Analyze request and identify requirements")
    ↓
think("Check applicable policies and rules")
    ↓
Tool: Get user information
    ↓
think("Verify information is complete and valid")
    ↓
think("Plan response based on policies and information")
    ↓
Tool: Execute action (if needed)
    ↓
think("Validate action was correct")
    ↓
Response to User
```

### Example: Data Analysis Workflow

**Workflow:**
```
think("Plan data analysis: 
1. Fetch data from source A
2. Fetch data from source B  
3. Validate data completeness
4. Merge datasets
5. Calculate metrics
6. Generate report")
    ↓
Tool: Fetch data A
    ↓
think("Data A retrieved. Checking completeness...")
    ↓
Tool: Fetch data B
    ↓
think("Data B retrieved. Both datasets complete. 
Ready to merge...")
    ↓
Tool: Merge and process
    ↓
think("Data merged successfully. Calculating metrics...")
    ↓
Tool: Generate report
    ↓
think("Report generated. All steps completed successfully.")
```

---

## 📋 System Prompt Examples

### Generic Customer Service

```markdown
## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness
```

### Airline Domain

See `src/prompt_templates.py` for the full airline domain prompt with examples.

### Retail Domain

```markdown
## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool to:
- Analyze customer request and identify requirements
- Check inventory and availability
- Verify pricing rules and discounts
- Confirm shipping options and policies
- Validate payment methods
```

### Coding/Development Domain

```markdown
## Using the think tool

Use this tool when complex reasoning or brainstorming is needed. For example:
- If you explore the repo and discover the source of a bug, call this tool to brainstorm several unique ways of fixing the bug, and assess which change(s) are likely to be simplest and most effective.
- If you receive some test results, call this tool to brainstorm ways to fix the failing tests.
- Before making changes, think through the implications and potential side effects.
```

---

## 💡 Tips for Writing Good Thoughts

### ✅ Good Thought Examples

**Structured and Clear:**
```
think(thought="Step 1: Analyze request - User wants refund
Step 2: Check policies - Refunds allowed within 30 days
Step 3: Verify purchase date - Purchased 15 days ago (within 30 days ✓)
Step 4: Check item condition - User says unused (meets requirement ✓)
Conclusion: Refund is eligible, proceed with processing")
```

**Detailed Reasoning:**
```
think(thought="Evaluating shipping options:
- Option 1: Standard (5-7 days, $5) - cheapest but slow
- Option 2: Express (2-3 days, $15) - moderate cost and speed
- Option 3: Overnight (1 day, $30) - fastest but expensive

User needs item by Friday (3 days away). 
Standard won't arrive in time. Express will arrive in time.
Overnight is unnecessary cost.

Decision: Recommend Express shipping.")
```

### ❌ Poor Thought Examples

**Too Vague:**
```
think(thought="figure it out")
```

**No Structure:**
```
think(thought="user wants something need to check stuff maybe do something")
```

**Missing Context:**
```
think(thought="yes")
```

---

## 🔗 See Also

- [USER-GUIDE.md](./USER-GUIDE.md) - Complete user guide
- [PROJECT-PLAN.md](./PROJECT-PLAN.md) - Research and planning
- `src/prompt_templates.py` - Domain-specific prompt templates

---

**Last Updated:** [Current Date]

