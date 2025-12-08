"""Domain-specific prompt templates for think tool usage."""

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
""",
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

