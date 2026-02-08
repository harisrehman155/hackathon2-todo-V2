# Anthropic Claude Prompt Engineering Best Practices

Official best practices for prompt engineering with Claude, particularly Claude 4.x and later models.

**Sources:**
- [Claude 4.x Best Practices - Claude Docs](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- [Prompt Engineering for Business Performance](https://www.anthropic.com/news/prompt-engineering-for-business-performance)

---

## Core Principles

### 1. Clear, Explicit Instructions

**Key Change in Claude 4.x:**
Claude 4.x models have been trained for more precise instruction following than previous generations.

**What This Means:**
- Claude 4.x responds well to **clear, explicit instructions**
- Being **specific** about desired output enhances results
- Customers who desire "above and beyond" behavior from previous Claude models might need to **more explicitly request** these behaviors with newer models

**Guidelines:**
- State what you want directly—don't assume Claude will infer
- Use clear, unambiguous language
- Specify exactly what behavior you expect

**Example:**
```
❌ Vague:
"Help the user with their code."

✅ Explicit:
"Review the user's code for bugs, security vulnerabilities, and performance
issues. Provide specific suggestions with code examples showing how to fix
each issue."
```

### 2. Provide Context and Motivation

**Principle:**
Providing context or motivation behind your instructions—such as explaining to Claude **why** such behavior is important—can help Claude 4.x models better understand requirements.

**Why This Works:**
- Helps Claude understand underlying goals
- Enables better decision-making in ambiguous situations
- Improves alignment with user intent

**Guidelines:**
- Explain WHY something matters, not just WHAT to do
- Provide background information
- State the goal or purpose

**Example:**
```
✅ With Context:
"When analyzing code, always explain the reasoning behind your suggestions.
This is important because developers need to understand WHY a change is
necessary, not just WHAT to change. This helps them learn and avoid similar
issues in the future."

vs.

❌ Without Context:
"When analyzing code, explain your suggestions."
```

### 3. Careful Example Selection

**Principle:**
Claude 4.x models pay **close attention to details** and examples as part of their precise instruction-following capabilities.

**Guidelines:**
- Ensure your examples **align with the behaviors you want to encourage**
- **Minimize behaviors you want to avoid** in examples
- Use diverse, canonical examples rather than exhaustive edge cases
- Quality over quantity—each example consumes tokens

**Example:**
```
✅ Good Examples:
Show 2-3 diverse examples that demonstrate the pattern you want, with clear
alignment to desired behavior.

❌ Bad Examples:
- Too many examples (token waste)
- Examples showing undesired patterns
- Examples that contradict instructions
```

### 4. Thinking Capabilities

**Feature:**
Claude 4.x models offer **thinking capabilities** that can be especially helpful for:
- Tasks involving reflection after tool use
- Complex multi-step reasoning

**How to Use:**
You can guide Claude's initial or interleaved thinking for better results.

**Example:**
```xml
<thinking>
Before responding, consider:
1. What is the user trying to achieve?
2. What information do I need to gather?
3. What approach would be most effective?
</thinking>
```

**When to Enable Thinking:**
- Complex reasoning tasks
- Multi-step workflows
- Tool use with reflection
- Decision-making with trade-offs

---

## Structural Elements

### XML Tags

**Feature:**
Claude can use XML tags if requested and processes them effectively.

**Benefits:**
- Clear section boundaries
- Structured information organization
- Explicit parsing of different prompt components

**Common Tags:**
```xml
<identity>
Agent identity and purpose
</identity>

<instructions>
Core operational instructions
</instructions>

<context>
Background information and reasoning
</context>

<examples>
Demonstration examples
</examples>

<tools>
Tool descriptions and usage guidance
</tools>

<constraints>
Boundaries and limitations
</constraints>

<output_format>
Expected response structure
</output_format>

<thinking>
Reasoning and analysis space
</thinking>
```

### Prompt Structure Template

```xml
<identity>
You are [name/role], created by [creator]. Your purpose is [goal].
You have expertise in [domain] and excel at [capabilities].
</identity>

<context>
[Why this agent exists, what problem it solves, background information]
</context>

<instructions>
Your workflow:
1. [Step 1 with clear action]
2. [Step 2 with clear action]
3. [Step 3 with clear action]

When [condition], do [action] because [reason].
</instructions>

<tools>
Available tools:
- tool_name(param): [Self-contained description with clear use case]
- tool_name(param): [When to use this tool]
</tools>

<constraints>
You must:
- [Required behavior 1]
- [Required behavior 2]

You must not:
- [Prohibited behavior 1]
- [Prohibited behavior 2]
</constraints>

<output_format>
Respond using this structure:
[Description of expected format, with example if needed]
</output_format>
```

---

## Best Practices Summary

### Do This ✅

1. **Be Explicit**
   - State requirements clearly and directly
   - Don't rely on inference
   - Specify exact desired behaviors

2. **Provide Context**
   - Explain why instructions matter
   - Give background information
   - State goals and motivations

3. **Use Structure**
   - Organize with XML tags or clear sections
   - Group related information
   - Maintain logical flow

4. **Choose Examples Carefully**
   - Align with desired behaviors
   - Use diverse, canonical examples
   - Minimize undesired patterns

5. **Leverage Thinking**
   - Enable for complex reasoning
   - Guide reflection after tool use
   - Structure multi-step analysis

6. **Be Specific About Output**
   - Define exact format expectations
   - Provide output examples
   - Specify structure requirements

### Avoid This ❌

1. **Vague Instructions**
   - "Be helpful" → Too general
   - "Do your best" → Not actionable
   - Assuming Claude will infer intent

2. **Missing Context**
   - Instructions without reasoning
   - No explanation of why
   - Lack of background information

3. **Poor Examples**
   - Too many examples (token waste)
   - Examples showing undesired behavior
   - Contradictory examples

4. **Unstructured Prompts**
   - Wall of text without organization
   - Mixed concerns in single section
   - No clear delimiters

5. **Assuming "Above and Beyond"**
   - Claude 4.x is more precise
   - Explicitly request extra effort if desired
   - Don't expect inference of unstated goals

---

## Prompt Chaining

**Technique:**
Sometimes Claude performs better on complex tasks if you break the task down into **multiple prompts** corresponding to each step.

**When to Use:**
- Complex multi-step workflows
- Tasks requiring distinct phases
- When intermediate outputs need validation

**Example:**
```
Prompt 1: "Analyze this code and identify all security vulnerabilities."
[Get response]

Prompt 2: "For each vulnerability identified, provide a specific code fix."
[Get response]

Prompt 3: "Now review the proposed fixes and identify any potential issues."
```

**Benefits:**
- Clearer focus per step
- Better intermediate validation
- Easier debugging of issues

---

## Context Window Management

**Capabilities:**
- Claude 3.5 Sonnet: 200K token context window
- Claude 3 Opus: 200K token context window

**Best Practices:**
- Use context wisely—more context ≠ better performance
- Apply context engineering principles (see `context-engineering.md`)
- Implement just-in-time retrieval for large information sets
- Use prompt caching for repeated content

**See Also:**
- `context-engineering.md` for detailed context optimization strategies

---

## Tool Use

**Best Practices for Tool Definitions:**

1. **Self-Contained Descriptions**
   - Each tool should be independently understandable
   - Include purpose, parameters, and return value
   - Specify when to use the tool

2. **Avoid Overlap**
   - Each tool should have a distinct purpose
   - Minimize overlapping functionality
   - Clear boundaries between tools

3. **Descriptive Parameters**
   - Use clear parameter names
   - Include type information
   - Document constraints

**Example:**
```xml
<tools>
search_code(query: str, file_pattern: str = "*") -> list[str]
# Searches codebase for {query} in files matching {file_pattern}.
# Use when: You need to find specific code patterns or function definitions.
# Returns: List of file paths containing matches.

read_file(path: str) -> str
# Reads complete file contents at {path}.
# Use when: You need to examine specific file after finding it via search.
# Returns: Full file contents as string.
</tools>
```

---

## Agent-Specific Considerations

### Identity and Persona

**Claude excels at adopting personas beyond just being a tool.**

From Claude's own system prompt:
- "Claude is more than just an information-seeking tool..."
- "Claude sees itself as an intelligent and kind assistant"
- "Possesses depth and wisdom"

**Guidelines:**
- Give agents clear identity beyond just function
- Define personality traits when appropriate
- Establish expertise domains
- Set communication style

**Example:**
```xml
<identity>
You are CodeGuard, an expert security-focused code reviewer created by
SecureTech. You have deep expertise in application security, with particular
strength in identifying OWASP Top 10 vulnerabilities. You are thorough,
educational, and provide actionable guidance. You communicate clearly without
unnecessary jargon, always explaining the "why" behind security recommendations.
</identity>
```

### Communication Style

**Specify:**
- Tone (professional, friendly, concise, verbose)
- Formatting preferences (lists, paragraphs, tables)
- When to use technical language vs. plain language
- What phrases to avoid

**Example:**
```xml
<communication_style>
- Be direct and concise—avoid conversational filler
- Use bullet points for lists of items
- Provide code examples for technical suggestions
- Never start messages with "Great!", "Certainly!", or "Sure!"
- Explain complex concepts in plain language first, then technical details
</communication_style>
```

---

## Evolution from Previous Versions

### Changes in Claude 4.x

**More Precise Instruction Following:**
- Follows instructions more literally
- Less "reading between the lines"
- Requires more explicit requests for extra effort

**What This Means:**
If you want Claude to:
- Go above and beyond → Request this explicitly
- Show creativity → Specify this in instructions
- Consider edge cases → List them or ask for them

**Migration Tip:**
If upgrading from Claude 3.x to 4.x, review your prompts and make implicit expectations explicit.

---

## Additional Resources

**Official Anthropic Resources:**
- [Claude Docs](https://docs.claude.com/)
- [Anthropic Console](https://console.anthropic.com/)
- [Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- [Prompt Engineering Blog Posts](https://www.anthropic.com/engineering)

**Related Skill References:**
- `context-engineering.md` - Token optimization and context management
- `examples/` - Complete system prompt examples
