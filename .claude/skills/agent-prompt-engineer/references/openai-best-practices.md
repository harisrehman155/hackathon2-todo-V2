# OpenAI GPT Prompt Engineering Best Practices

Official best practices for prompt engineering with OpenAI GPT models (GPT-4.1+, GPT-5.x series).

**Sources:**
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Best Practices for Prompt Engineering with OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
- [GPT-4.1 Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)
- [OpenAI Cookbook](https://cookbook.openai.com/)

---

## Core Principles

### 1. Write Clear Instructions

**Principle:**
GPT models cannot read your mind. If outputs are too long, ask for brief replies. If outputs are too simple, ask for expert-level writing. If you dislike the format, demonstrate the format you'd like to see.

**Tactics:**

**Include Details in Your Query**
- Be specific about what you want
- Provide context and constraints
- Specify desired length, style, or format

**Example:**
```
❌ Generic:
"Write a function to calculate primes."

✅ Specific:
"Write a Python function that efficiently calculates all prime numbers up to
n using the Sieve of Eratosthenes algorithm. Include docstring with complexity
analysis and type hints."
```

**Ask the Model to Adopt a Persona**
- Define role and expertise level
- Set communication style
- Establish perspective

**Example:**
```
You are an expert Python developer with 10 years of experience in backend
systems. You write clean, maintainable code following PEP 8 guidelines.
```

**Use Delimiters to Clearly Indicate Distinct Parts**
- Triple quotes: """
- XML tags: `<tag>content</tag>`
- Section headers: ### Section
- Markdown formatting

**Specify Steps Required to Complete a Task**
- Break complex tasks into numbered steps
- Provide decision trees for conditional logic
- Make workflow explicit

**Example:**
```
To review code:
1. Read the entire file to understand context
2. Check for security vulnerabilities (SQL injection, XSS, CSRF)
3. Identify performance bottlenecks
4. Review code style and readability
5. Suggest specific improvements with examples
```

**Provide Examples**
- Show desired input-output pairs
- Demonstrate format and style
- Illustrate edge case handling

**Specify Desired Output Length**
- Character, word, sentence, or paragraph count
- "Brief", "detailed", "comprehensive"
- Explicit length constraints

### 2. Provide Reference Text

**Principle:**
GPT models can confidently invent fake answers, especially when asked about esoteric topics, citations, or URLs. Providing reference text helps models answer with fewer fabrications.

**Tactics:**

**Instruct the Model to Answer Using Reference Text**
```
Use the following documentation to answer questions. If the answer cannot be
found in the documentation, say "I don't have enough information to answer."

<documentation>
{reference_text}
</documentation>
```

**Instruct the Model to Answer with Citations**
```
Answer the question using the provided documentation. Cite your sources using
[1], [2], etc., and include a references section at the end.
```

**For Agents:**
Use **retrieval tools** instead of embedding large reference texts:
- Define search/fetch tools
- Enable just-in-time retrieval
- Maintain lightweight references

### 3. Split Complex Tasks into Simpler Subtasks

**Principle:**
Complex tasks have higher error rates than simpler tasks. Complex tasks can often be re-defined as workflows of simpler tasks.

**Tactics:**

**Use Intent Classification**
- Identify task type first
- Route to appropriate workflow
- Apply specialized handling

**Example:**
```
Step 1: Classify user intent
- Code review → Use code_review_workflow
- Bug fix → Use debug_workflow
- Feature request → Use feature_workflow

Step 2: Execute appropriate workflow
```

**Summarize Long Documents Piecewise**
- Process in chunks
- Accumulate summaries
- Construct final summary from chunks

**Dialogue Applications: Summarize or Filter Previous Dialogue**
- Don't include entire conversation history
- Summarize older context
- Keep recent exchanges verbatim

### 4. Give the Model Time to "Think"

**Principle:**
Models make more reasoning errors when trying to answer immediately, rather than taking time to work out an answer. Asking for a chain of reasoning before an answer can help the model reason its way to correct answers more reliably.

**Tactics:**

**Instruct the Model to Work Out Its Own Solution**
```
Before providing feedback on the student's solution:
1. Work out your own solution to the problem
2. Compare your solution to the student's solution
3. Evaluate if the student's solution is correct

Only then provide feedback.
```

**Use Inner Monologue or Sequence of Queries**
- Hide reasoning from user
- Show only final output
- Process in multiple steps

**Ask if Model Missed Anything**
```
After your initial analysis, review it and ask yourself: "Did I miss anything?
Are there any other issues I should consider?" Then provide a complete response.
```

### 5. Use External Tools

**Principle:**
Compensate for model weaknesses by feeding it outputs from other tools.

**Tactics:**

**Embeddings-Based Search**
- Implement RAG (Retrieval-Augmented Generation)
- Search knowledge bases
- Retrieve relevant context

**Code Execution**
- Run code to get accurate results
- Perform calculations
- Process data

**Function Calling**
- Access external APIs
- Retrieve real-time data
- Execute actions

### 6. Test Changes Systematically

**Principle:**
Improving performance is easier if you can measure it. Systematically test modifications to see if they improve results.

**Tactics:**

**Evaluate Model Outputs with Reference to Gold-Standard Answers**
- Create test cases
- Define expected outputs
- Measure accuracy/quality

**Iterative Improvement:**
1. Establish baseline performance
2. Make one change at a time
3. Measure impact
4. Keep improvements, discard regressions

---

## GPT-4.1+ Specific Features

### Outstanding Instruction-Following

**Capability:**
GPT-4.1 and later models have outstanding instruction-following performance.

**How to Leverage:**
- Provide precise, detailed specifications
- Use complex multi-step instructions
- Rely on exact adherence to guidelines

**Example:**
```
Generate a REST API design following these exact requirements:
1. Use OpenAPI 3.0 specification format
2. Include authentication using Bearer tokens
3. Implement pagination with limit/offset parameters (max 100 items)
4. Return errors in RFC 7807 Problem Details format
5. Use kebab-case for endpoint paths
6. Include example responses for each endpoint
```

### Structured Outputs

**Feature:**
GPT-4.1+ can produce highly structured outputs reliably.

**How to Use:**
- Specify exact JSON schema
- Define required fields and types
- Provide format examples

**Example:**
```
Return your analysis in this exact JSON format:
{
  "severity": "low" | "medium" | "high" | "critical",
  "issues": [
    {
      "type": string,
      "location": string,
      "description": string,
      "suggestion": string,
      "code_example": string
    }
  ],
  "summary": string
}
```

---

## Prompt Structure Patterns

### System Message Pattern

**Structure:**
```
System Message: [Set role, capabilities, and behavior]
User Message: [Provide task and context]
```

**System Message Components:**
1. **Identity and Role**
   ```
   You are {name/role}. You {capabilities}.
   ```

2. **Expertise and Knowledge**
   ```
   You have expertise in {domains}. You are familiar with {technologies/concepts}.
   ```

3. **Communication Style**
   ```
   You communicate {style}. You {formatting preferences}.
   ```

4. **Operational Guidelines**
   ```
   When {condition}, you {action}.
   You always {required_behavior}.
   You never {prohibited_behavior}.
   ```

5. **Output Format**
   ```
   You respond using {format}. Your outputs include {components}.
   ```

### Complete Template

```markdown
# Identity and Role
You are {name}, {description}. Your purpose is {goal}.

# Capabilities
- {Capability 1}
- {Capability 2}
- {Capability 3}

# Expertise
You have expert knowledge in:
- {Domain 1}
- {Domain 2}
You are familiar with {technologies, frameworks, standards}.

# Workflow
When given a task:
1. {Step 1}
2. {Step 2}
3. {Step 3}

# Guidelines
## Required Behaviors
- {Behavior 1}
- {Behavior 2}

## Prohibited Behaviors
- Never {prohibited 1}
- Never {prohibited 2}

# Output Format
Provide responses in this format:
{format specification with example}

# Tools and Resources
Available tools:
- {tool_name}: {description and when to use}
- {tool_name}: {description and when to use}
```

---

## Best Practices for Agents

### Define Clear Workflows

**Pattern:**
```
Your workflow for {task_type}:
1. {Step 1 with specific action}
2. {Step 2 with specific action}
3. If {condition}:
   a. {Action A}
   b. {Action B}
4. {Step 4 with specific action}
5. Validate {what to validate}
```

### Handle Edge Cases Explicitly

**Pattern:**
```
Special cases:
- If {edge_case_1}: {specific_handling}
- If {edge_case_2}: {specific_handling}
- If uncertain: {fallback_behavior}
```

### Error Handling

**Pattern:**
```
Error handling:
- If {error_condition_1}: {recovery_action}
- If operation fails: {fallback_behavior}
- Always: {safety_behavior}
```

### Progress Tracking

**Pattern:**
```
For multi-step tasks:
1. Announce what you're about to do
2. Execute the step
3. Report outcome
4. Proceed to next step
```

---

## Common Patterns and Anti-Patterns

### ✅ Do This

**Clear Role Definition:**
```
You are an expert code reviewer specializing in Python. You have 10 years of
experience with Django, Flask, and FastAPI frameworks. You focus on security,
performance, and maintainability.
```

**Explicit Workflows:**
```
Code review process:
1. Read entire file for context
2. Identify security vulnerabilities (check OWASP Top 10)
3. Spot performance bottlenecks
4. Review code organization and style
5. Provide specific suggestions with code examples
```

**Structured Output Specifications:**
```
Format each finding as:
## Issue: {brief_title}
**Severity:** {Low|Medium|High|Critical}
**Location:** {file:line}
**Description:** {what's wrong}
**Impact:** {why it matters}
**Suggestion:** {how to fix}
**Example:**
```{language}
{code_example}
```
```

### ❌ Avoid This

**Vague Role:**
```
You are a helpful assistant.
```

**Implicit Workflow:**
```
Review the code and provide feedback.
```

**Unspecified Output:**
```
Tell me what you find.
```

**Overly Long Instructions:**
```
[500+ word paragraph without structure or delimiters]
```

---

## Function Calling Best Practices

### Tool Definition Quality

**Good Tool Definitions:**
```json
{
  "name": "search_code",
  "description": "Search codebase for specific patterns, functions, or classes. Returns file paths containing matches.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query (supports regex)"
      },
      "file_pattern": {
        "type": "string",
        "description": "File glob pattern (e.g., '*.py', 'src/**/*.js')",
        "default": "*"
      }
    },
    "required": ["query"]
  }
}
```

**Key Elements:**
- Clear, concise name
- Description includes purpose AND return value
- Well-documented parameters
- Sensible defaults where appropriate

### Tool Usage Guidance

**In System Prompt:**
```
Tool usage guidelines:
- Use search_code() to find relevant files before reading
- Use read_file() only after identifying specific files
- Always validate tool outputs before using them
- If a tool fails, try alternative approaches
```

---

## Token Optimization

### Minimize Redundancy

**Before:**
```
When you review code, make sure you check for security issues. Security is
important because vulnerabilities can be exploited. You should look for common
security problems like SQL injection, XSS, and CSRF. These are serious security
issues that need to be addressed.
```

**After:**
```
Check for security vulnerabilities: SQL injection, XSS, CSRF.
```

### Use Abbreviations for Repeated Concepts

**Pattern:**
Define abbreviations once, use throughout:
```
This agent analyzes code for:
- Security vulnerabilities (VULN)
- Performance issues (PERF)
- Code quality problems (QUAL)

Workflow:
1. Scan for VULN
2. Check PERF
3. Assess QUAL
```

### Reference Instead of Repeat

**Instead of:**
Repeating the same information multiple times

**Do:**
```
Output format: See FORMAT_SPEC section below.

[... other content ...]

## FORMAT_SPEC
{detailed format specification}
```

---

## Evaluation and Iteration

### Testing Prompts

**Create Test Suite:**
```python
test_cases = [
    {
        "input": "...",
        "expected_output": "...",
        "criteria": "Should identify SQL injection vulnerability"
    },
    # More cases
]
```

**Measure Performance:**
- Accuracy: Does it produce correct results?
- Consistency: Same input → same output?
- Completeness: Addresses all requirements?
- Efficiency: Minimal token usage?

### Iterative Improvement

**Process:**
1. Start with minimal prompt
2. Identify failure modes through testing
3. Add specific instructions for failures
4. Re-test and measure improvement
5. Repeat

**Document Changes:**
```
Version 1.0: Initial prompt
Version 1.1: Added explicit security check list (improved VULN detection by 30%)
Version 1.2: Restructured workflow steps (reduced missed issues by 15%)
```

---

## Model Selection Guidance

| Model | Best For | Prompt Considerations |
|-------|----------|----------------------|
| **GPT-4.1** | Complex reasoning, instruction-following | Can handle detailed, multi-step instructions |
| **GPT-4o** | Balanced performance, general purpose | Standard best practices apply |
| **GPT-3.5 Turbo** | Simple tasks, speed, cost efficiency | Keep instructions simpler, more explicit |

---

## Additional Resources

**Official OpenAI Resources:**
- [Platform Documentation](https://platform.openai.com/docs)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [API Reference](https://platform.openai.com/docs/api-reference)
- [Help Center](https://help.openai.com/)

**Related Skill References:**
- `context-engineering.md` - Token optimization strategies
- `examples/` - Complete system prompt templates
