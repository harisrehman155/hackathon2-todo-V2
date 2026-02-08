# Google Gemini Prompt Engineering Best Practices

Official best practices for prompt design with Google Gemini models.

**Sources:**
- [Gemini API Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Vertex AI Prompt Design Strategies](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies)
- [Google Prompting Essentials](https://grow.google/prompting-essentials/)
- [Gemini for Google Workspace Prompting Guide 101](https://services.google.com/fh/files/misc/gemini-for-google-workspace-prompting-guide-101.pdf)

---

## Core Principles for Gemini 3 Models

### 1. Be Precise and Direct

**Principle:**
Gemini 3 models are designed for advanced reasoning and instruction following, and respond best to prompts that are **direct, well-structured, and clearly define the task and constraints**.

**Guidelines:**
- State your goal **clearly and concisely**
- Avoid **unnecessary or overly persuasive language**
- Be **direct** rather than verbose
- Focus on **what** you want, not how to convince the model

**Example:**
```
❌ Overly Persuasive:
"Please, if you could be so kind, I would really appreciate it if you might
consider helping me to possibly review this code and maybe provide some
feedback if you think it's appropriate..."

✅ Direct:
"Review this code for bugs, security issues, and performance problems. Provide
specific fixes for each issue found."
```

### 2. Use Consistent Structure

**Principle:**
Use **clear delimiters** like XML-style tags or Markdown headings to organize information.

**Supported Structures:**
- Markdown headings (##, ###)
- XML-style tags (`<tag>content</tag>`)
- Numbered lists
- Bullet points
- Code blocks with language specification

**Example:**
```markdown
## Task
Review the code below for issues.

## Code
```python
[code here]
```

## Focus Areas
- Security vulnerabilities
- Performance bottlenecks
- Code style

## Output Format
Provide findings as numbered list with severity ratings.
```

### 3. Define Parameters

**Principle:**
**Explicitly explain any ambiguous terms** to ensure the model understands your intent.

**Guidelines:**
- Define domain-specific terminology
- Clarify subjective terms
- Specify measurement criteria
- Explain context-specific meanings

**Example:**
```
❌ Ambiguous:
"Review code quality."

✅ Parameters Defined:
"Review code quality using these criteria:
- Readability: Clear variable names, appropriate comments, logical structure
- Maintainability: DRY principle, modular design, low coupling
- Performance: O(n) complexity or better, efficient data structures
- Security: Input validation, no hardcoded secrets, SQL injection prevention"
```

### 4. Control Output Verbosity

**Principle:**
Gemini 3 **provides direct answers by default** unless you request more detail.

**Guidelines:**
- Default: Concise, direct responses
- For more detail: Explicitly request it
- Specify desired length or depth

**Example:**
```
For brief answer:
"List the security vulnerabilities in this code."

For detailed answer:
"Analyze this code for security vulnerabilities. For each vulnerability:
1. Explain what it is and why it's dangerous
2. Show the vulnerable code snippet
3. Provide a corrected version
4. Suggest testing methods to verify the fix"
```

---

## Four Key Elements of Effective Prompts

From Google Workspace Prompting Guide 101:

### 1. Persona

**Definition:**
Who should the model act as?

**Examples:**
- "You are an expert security auditor..."
- "Act as a senior Python developer..."
- "You are a technical documentation specialist..."

**Guidelines:**
- Specify expertise level
- Define domain knowledge
- Set perspective

### 2. Task

**Definition:**
What should the model do?

**Guidelines:**
- Use clear action verbs
- Be specific about the objective
- Define scope boundaries

**Examples:**
- "Review this code for security vulnerabilities"
- "Generate unit tests for the following functions"
- "Refactor this code to improve performance"

### 3. Context

**Definition:**
What background information is needed?

**Examples:**
- Project requirements
- Constraints and limitations
- Target audience
- Technical environment
- Business goals

**Pattern:**
```
Context: This code is part of a payment processing system that handles
sensitive financial data. It must comply with PCI DSS standards and process
transactions within 200ms.

Task: Review for security and performance issues.
```

### 4. Format

**Definition:**
How should the output be structured?

**Examples:**
- Bulleted list
- Numbered steps
- Table format
- JSON structure
- Markdown with headings

**Pattern:**
```
Format your response as:
## Summary
[Brief overview]

## Issues Found
| Severity | Type | Location | Description |
|----------|------|----------|-------------|
| ... | ... | ... | ... |

## Recommendations
1. [Priority recommendation]
2. [Secondary recommendation]
```

---

## Prompt Structure Template

### Basic Template

```markdown
## Persona
You are [role/expertise].

## Task
[Clear, specific objective]

## Context
- [Background info 1]
- [Background info 2]
- [Constraints]

## Format
[Output structure specification]
```

### Advanced Template for Agents

```markdown
## Agent Identity
You are [name], [description of role and expertise].

## Core Functionality
Your primary functions:
1. [Function 1]
2. [Function 2]
3. [Function 3]

## Operational Context
- Purpose: [Why this agent exists]
- Environment: [Technical context]
- Constraints: [Limitations and boundaries]

## Workflow
When given [input type]:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Decision Logic
- If [condition A]: [action A]
- If [condition B]: [action B]
- Otherwise: [default action]

## Output Requirements
Provide responses in this format:
[Detailed format specification]

## Quality Standards
Your outputs must:
- [Standard 1]
- [Standard 2]
- [Standard 3]
```

---

## Best Practices Summary

### ✅ Do This

**Be Direct:**
```
"Analyze this code for security vulnerabilities."
```

**Use Structure:**
```markdown
## Task
Review code

## Focus
- Security
- Performance

## Output
Numbered list with severity ratings
```

**Define Terms:**
```
"High severity: Issues that could lead to data breaches or system compromise
Medium severity: Issues that could cause errors or degraded performance
Low severity: Code quality issues that don't affect functionality"
```

**Specify Format:**
```
"Return results as JSON with this structure: {...}"
```

### ❌ Avoid This

**Overly Persuasive Language:**
```
"I would really appreciate if you could please kindly help me..."
```

**Vague Instructions:**
```
"Look at this code."
```

**Undefined Terms:**
```
"Find important issues."
(What makes an issue "important"?)
```

**Unspecified Output:**
```
"Tell me what you find."
```

---

## Gemini-Specific Features

### Multimodal Capabilities

**Gemini can process:**
- Text
- Images
- Audio (Gemini 1.5+)
- Video (Gemini 1.5+)

**For Code Analysis:**
```
Analyze this architecture diagram [image] and the corresponding code:
[code]

Identify any discrepancies between the design and implementation.
```

### Long Context Windows

**Gemini 1.5 Pro:**
- Up to 2 million token context window
- Can process entire codebases
- Enables comprehensive analysis

**Best Practice:**
Even with large context, apply context engineering principles:
- Don't waste tokens on redundant information
- Structure information hierarchically
- Use progressive disclosure

### Structured Output

**Gemini supports:**
- JSON output with schema specification
- Consistent formatting
- Controlled generation

**Example:**
```
Return analysis in this JSON schema:
{
  "summary": string,
  "issues": [
    {
      "severity": "low" | "medium" | "high",
      "category": string,
      "description": string,
      "suggestion": string
    }
  ],
  "metrics": {
    "total_issues": number,
    "critical_count": number
  }
}
```

---

## Prompt Design Strategies

### Strategy 1: Zero-Shot Prompting

**When to Use:**
Simple, straightforward tasks

**Pattern:**
```
Task: [Clear instruction]
Input: [Data]
Output: [Expected format]
```

**Example:**
```
Task: Extract all function names from this code.
Input:
```python
[code]
```
Output: JSON array of function names
```

### Strategy 2: Few-Shot Prompting

**When to Use:**
- Complex patterns
- Specific formatting
- Domain-specific tasks

**Pattern:**
```
Task: [Instruction]

Example 1:
Input: [input_1]
Output: [output_1]

Example 2:
Input: [input_2]
Output: [output_2]

Now apply to:
Input: [actual_input]
```

### Strategy 3: Chain-of-Thought

**When to Use:**
- Complex reasoning
- Multi-step analysis
- Decision-making tasks

**Pattern:**
```
Task: [Complex task]
Approach: Think step-by-step:
1. First consider [aspect 1]
2. Then analyze [aspect 2]
3. Finally conclude [aspect 3]
```

**Example:**
```
Analyze this code for security issues. Think step-by-step:
1. Identify all input points
2. Check if inputs are validated
3. Trace data flow through the system
4. Identify potential injection points
5. Assess impact of each vulnerability
```

### Strategy 4: Retrieval-Augmented Generation (RAG)

**When to Use:**
- Large knowledge bases
- Dynamic information
- Context exceeds window

**Pattern:**
```
Available information: [Retrieved context]
Task: Answer using only the provided information.
Question: [Question]
```

---

## Error Handling and Edge Cases

### Specify Fallback Behavior

**Pattern:**
```
Instructions:
- [Normal case handling]
- If input is invalid: [error handling]
- If information is insufficient: [fallback behavior]
- If uncertain: [what to do]
```

**Example:**
```
If code cannot be analyzed due to syntax errors:
1. Report the syntax errors found
2. Analyze only the syntactically correct portions
3. Note which sections were skipped and why
```

### Handle Ambiguity

**Pattern:**
```
If [ambiguous situation]:
- Option 1: [interpretation 1] → [action 1]
- Option 2: [interpretation 2] → [action 2]
- If unclear which: [clarification behavior]
```

---

## Token Optimization

### Concise Instructions

**Before (32 tokens):**
```
I would like you to please review this code carefully and thoroughly, making
sure to identify any and all potential security vulnerabilities that might exist.
```

**After (11 tokens):**
```
Identify all security vulnerabilities in this code.
```

### Use Headers for Structure

**Before (Wall of text):**
```
You are a code reviewer. Your task is to find bugs. You should look for security
issues, performance problems, and style violations. Output should be a list...
[continues without structure]
```

**After (Structured):**
```markdown
## Role
Code reviewer

## Task
Find bugs: security, performance, style

## Output
Numbered list with severity ratings
```

### Reference Instead of Repeat

**Pattern:**
```
## Security Checklist
1. Input validation
2. SQL injection prevention
3. XSS prevention
[... more items ...]

## Task
Review code using Security Checklist above.
```

---

## Testing and Iteration

### Create Test Cases

**Pattern:**
```
Test Case 1:
Input: [code with SQL injection]
Expected: Should identify SQL injection vulnerability

Test Case 2:
Input: [code with XSS]
Expected: Should identify XSS vulnerability
```

### Measure Quality

**Metrics:**
- Accuracy: Correct identification of issues
- Completeness: No missed issues
- Precision: No false positives
- Consistency: Same input → same output

### Iterate Based on Results

**Process:**
1. Test with representative cases
2. Identify failure modes
3. Refine prompt to address failures
4. Re-test and measure improvement
5. Document what worked

---

## Common Patterns for Agents

### Analysis Agent

```markdown
## Persona
Expert analyzer specializing in [domain]

## Task
Analyze [input type] for [aspects]

## Workflow
1. Parse input
2. Apply [criteria]
3. Generate findings

## Output Format
{structured format}
```

### Generation Agent

```markdown
## Persona
Expert [creator type]

## Task
Generate [output type] based on [requirements]

## Requirements
- [Requirement 1]
- [Requirement 2]

## Output Format
{specification}
```

### Transformation Agent

```markdown
## Persona
Expert at transforming [input] to [output]

## Task
Convert [input type] to [output type]

## Constraints
- Preserve [what to preserve]
- Optimize for [optimization goal]

## Output Format
{specification}
```

---

## Additional Resources

**Official Google Resources:**
- [Gemini API Documentation](https://ai.google.dev/gemini-api)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai)
- [Google AI Studio](https://aistudio.google.com/)
- [Prompting Essentials Course](https://grow.google/prompting-essentials/)

**Related Skill References:**
- `context-engineering.md` - Token optimization
- `examples/` - Complete prompt templates
