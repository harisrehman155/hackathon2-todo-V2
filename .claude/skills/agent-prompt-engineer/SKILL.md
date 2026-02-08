---
name: agent-prompt-engineer
description: |
  Expert system for building and analyzing system prompts for AI agents using official best practices from Anthropic, OpenAI, and Google. This skill should be used when users want to create new system prompts for custom AI agents, improve existing agent prompts, apply context engineering techniques, or optimize agent performance across any LLM platform (Claude, GPT, Gemini, or platform-agnostic). Includes embedded domain expertise on prompt engineering patterns, context optimization strategies, and platform-specific features.
---

# Agent Prompt Engineer

Expert system for creating and optimizing system prompts for AI agents using official best practices from Anthropic, OpenAI, and Google.

## What This Skill Does

- **Builds** new system prompts for AI agents from requirements
- **Analyzes** existing system prompts and suggests improvements
- **Applies** context engineering techniques to optimize token efficiency
- **Adapts** prompts to specific LLM platforms (Claude, GPT, Gemini) or creates platform-agnostic prompts
- **Validates** prompts against official best practices

## What This Skill Does NOT Do

- Deploy or test agents in production environments
- Train or fine-tune models
- Handle agent infrastructure (APIs, hosting, monitoring)
- Create conversational prompts for end-users (focuses on system prompts for agents)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Requirements** | Agent purpose, capabilities, constraints, target platform |
| **Existing Prompts** | Current system prompt (if analyzing/improving) |
| **Codebase** | Agent architecture, tool definitions, workflows |
| **Skill References** | Best practices from `references/` (Anthropic, OpenAI, Google patterns) |
| **User Guidelines** | Specific standards, tone preferences, domain requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Core Workflow

### For Building New Prompts

```
Gather Requirements → Select Platform → Choose Agent Pattern → Apply Best Practices → Optimize Context → Validate → Deliver
```

**Step 1: Gather Requirements**

Ask the user (if not already provided):

| Question | Why |
|----------|-----|
| What does the agent do? | Defines core purpose and capabilities |
| What platform/LLM? | Determines platform-specific features to use |
| What tools does it use? | Informs tool guidance section |
| What constraints? | Security, tone, boundaries, limitations |
| What output format? | Structured responses, markdown, JSON, etc. |

**Step 2: Select Platform Strategy**

| Platform | Apply Features From |
|----------|-------------------|
| **Claude** | `references/anthropic-best-practices.md` - XML tags, thinking, tool patterns |
| **OpenAI GPT** | `references/openai-best-practices.md` - Instruction-following, role patterns |
| **Google Gemini** | `references/google-best-practices.md` - Direct prompts, structured output |
| **Platform-agnostic** | Universal principles from all three sources |

**Step 3: Choose Agent Pattern**

Common agent types (see `references/examples/` for full templates):

| Agent Type | Pattern | Key Sections |
|------------|---------|--------------|
| **Chatbot** | Conversational assistant | Identity, persona, communication style, boundaries |
| **Code Assistant** | Development helper | Language expertise, code standards, tool use, error handling |
| **Analyzer** | Data/content examiner | Scope, criteria, output format, validation |
| **Automation** | Task executor | Workflow steps, error handling, progress tracking |
| **Research** | Information gatherer | Search strategy, source evaluation, synthesis |

**Step 4: Apply Best Practices**

Use principles from `references/` (see Platform-Specific Guidance below).

**Step 5: Optimize Context**

Apply context engineering from `references/context-engineering.md`:

- **High-Signal Minimalism**: Use smallest set of high-signal tokens
- **Just-In-Time Context**: Load information dynamically vs upfront
- **Progressive Disclosure**: Tier information (always-loaded, conditional, on-demand)
- **Tool Optimization**: Self-contained, unambiguous tool descriptions

**Step 6: Validate**

Check against quality criteria:
- [ ] Clear, explicit instructions
- [ ] Context and reasoning provided
- [ ] Specific success criteria defined
- [ ] Platform-appropriate features used
- [ ] Token-efficient structure
- [ ] Security considerations addressed

**Step 7: Deliver**

Provide:
- Complete system prompt
- Explanation of design decisions
- Token count estimate
- Suggestions for iteration

### For Analyzing Existing Prompts

```
Read Prompt → Identify Platform → Evaluate Against Best Practices → Context Analysis → Generate Recommendations → Deliver Report
```

**Step 1: Read Prompt**

Extract current system prompt from conversation or files.

**Step 2: Identify Platform**

Detect platform from:
- Explicit mentions (Claude, GPT, Gemini)
- Platform-specific features (XML tags → Claude, role patterns → OpenAI)
- User context

**Step 3: Evaluate Against Best Practices**

Score prompt against criteria from `references/`:

| Dimension | Evaluate |
|-----------|----------|
| **Clarity** | Clear, explicit, unambiguous instructions? |
| **Context** | Provides reasoning and motivation? |
| **Specificity** | Explicit success criteria and constraints? |
| **Structure** | Well-organized sections with delimiters? |
| **Platform Fit** | Uses platform-specific features appropriately? |
| **Token Efficiency** | Concise without sacrificing clarity? |
| **Security** | Addresses input validation, boundaries, safety? |

**Step 4: Context Analysis**

Identify context engineering issues:
- Upfront loading vs just-in-time retrieval
- Token waste (redundancy, unnecessary examples)
- Missing progressive disclosure opportunities
- Bloated tool descriptions

**Step 5: Generate Recommendations**

Provide:
- Specific improvements with before/after examples
- Priority ranking (high/medium/low impact)
- Context optimization opportunities
- Platform-specific enhancements

**Step 6: Deliver Report**

Format:
```markdown
## Analysis Summary
- Current state assessment
- Key strengths
- Critical issues

## Recommendations
### High Priority
1. [Issue] → [Solution] (Impact: [reason])

### Medium Priority
...

### Low Priority
...

## Optimized Prompt
[Improved version with changes highlighted]

## Estimated Impact
- Token savings: X%
- Expected performance improvement: [qualitative]
```

---

## Platform-Specific Guidance

### Claude (Anthropic)

**Key Features** (from `references/anthropic-best-practices.md`):

1. **Clear, Explicit Instructions**
   - Claude 4.x responds well to direct instructions
   - State what you want explicitly (don't assume inference)
   - Request "above and beyond" behavior explicitly if desired

2. **Provide Context and Motivation**
   - Explain WHY something is important
   - Helps Claude understand underlying goals

3. **XML Tags for Structure**
   - Use tags like `<instructions>`, `<examples>`, `<constraints>`
   - Claude can parse and use XML structure effectively

4. **Thinking Capabilities**
   - Enable `<thinking>` for complex reasoning tasks
   - Useful for reflection after tool use
   - Guide initial or interleaved thinking

5. **Careful Example Selection**
   - Claude 4.x pays close attention to details in examples
   - Ensure examples align with desired behaviors
   - Minimize undesired patterns

**Template Structure:**
```xml
<identity>
[Who the agent is, created by, capabilities]
</identity>

<instructions>
[Clear, explicit operational instructions]
</instructions>

<context>
[Why this matters, goals, motivation]
</context>

<tools>
[Self-contained tool descriptions with clear use cases]
</tools>

<constraints>
[Boundaries, limitations, security considerations]
</constraints>

<output_format>
[Expected response structure]
</output_format>
```

### OpenAI (GPT-4.1+)

**Key Features** (from `references/openai-best-practices.md`):

1. **Outstanding Instruction-Following**
   - GPT-4.1+ excels at following complex instructions
   - Leverage precise, detailed specifications

2. **Role-Based Patterns**
   - Define clear role and responsibilities
   - Use "You are..." pattern for identity

3. **Explicit Workflow Guidance**
   - Break down complex tasks into numbered steps
   - Provide decision trees for conditional logic

4. **Clear Output Specifications**
   - Specify exact format requirements
   - Use examples for structured outputs

**Template Structure:**
```markdown
# Identity and Role
You are [description]. Your purpose is [goal].

# Capabilities
- [Capability 1]
- [Capability 2]

# Instructions
[Numbered workflow steps]

# Guidelines
- [Guideline 1]
- [Guideline 2]

# Output Format
[Specification with examples]

# Constraints
[Boundaries and limitations]
```

### Google Gemini

**Key Features** (from `references/google-best-practices.md`):

1. **Direct and Precise**
   - Be direct, avoid unnecessary or persuasive language
   - State goals clearly and concisely

2. **Consistent Structure**
   - Use clear delimiters (Markdown headings, XML tags)
   - Maintain consistent formatting

3. **Define Parameters**
   - Explicitly explain ambiguous terms
   - Provide clear definitions

4. **Control Verbosity**
   - Gemini 3 provides direct answers by default
   - Request more detail explicitly if needed

**Template Structure:**
```markdown
## Agent Purpose
[Concise description]

## Core Functionality
[Direct, specific capabilities]

## Workflow
[Step-by-step process]

## Output Requirements
[Explicit format specification]

## Constraints
[Clear boundaries]
```

### Platform-Agnostic

**Universal Best Practices** (work across all platforms):

1. **Be Clear and Explicit**
   - State requirements directly
   - Avoid ambiguity
   - Use simple language

2. **Provide Context and Reasoning**
   - Explain why things matter
   - Give background information

3. **Use Specificity**
   - Define success criteria
   - Set explicit constraints
   - Specify output formats

4. **Structure Information**
   - Use headings and sections
   - Group related information
   - Maintain logical flow

5. **Include Examples**
   - Show desired patterns
   - Demonstrate edge cases
   - Align with goals

6. **Context Engineering**
   - Minimize token usage while maximizing signal
   - Use just-in-time information retrieval
   - Implement progressive disclosure

---

## Context Engineering Techniques

Apply these techniques from `references/context-engineering.md`:

### 1. High-Signal Minimalism

**Principle:** "Smallest possible set of high-signal tokens that maximize likelihood of desired outcome."

**Apply:**
- Remove redundant instructions
- Consolidate similar guidelines
- Use concise language without sacrificing clarity
- Challenge every sentence: "Does this justify its token cost?"

**Example:**
```
❌ Before (78 tokens):
"When you are responding to user queries, it is very important that you
always make sure to provide clear, comprehensive, and well-structured
answers that fully address their questions. You should take care to be
thorough and complete in your responses."

✅ After (23 tokens):
"Provide clear, comprehensive answers that fully address user questions."
```

### 2. Just-In-Time Context Retrieval

**Principle:** Load information dynamically vs upfront.

**Apply:**
- Define tools for dynamic information retrieval
- Use lightweight references (file paths, IDs) instead of full content
- Load details only when needed for specific tasks

**Example:**
```
❌ Upfront Loading:
<documentation>
[Paste entire 50-page API documentation]
</documentation>

✅ Just-In-Time:
<tools>
- fetch_docs(topic): Retrieve relevant documentation for {topic}
- search_examples(query): Find code examples matching {query}
</tools>

Instructions: Use fetch_docs() to retrieve information as needed.
```

### 3. Progressive Disclosure

**Principle:** Tier information by usage frequency.

**Tiers:**
1. **Always-loaded** (~100 tokens): Core identity, critical instructions
2. **Conditional** (~500 tokens): Loaded for specific task types
3. **On-demand** (unlimited): Retrieved via tools when needed

**Apply:**
- Tier 1: Essential identity and purpose
- Tier 2: Detailed workflows (in main prompt or loaded conditionally)
- Tier 3: Examples, edge cases, detailed docs (via tools)

### 4. Tool Optimization

**Principle:** Self-contained, unambiguous tool descriptions.

**Apply:**
- Each tool has clear, single purpose
- No overlapping functionality
- Descriptive parameter names
- Concise descriptions (avoid bloat)

**Example:**
```
❌ Bloated:
search_database(query: str, options: dict)
# Search the database with various options including filters, sorting,
# pagination, field selection, aggregation, joins, and more. Options
# can include: filter (dict), sort (list), limit (int), offset (int),
# fields (list), aggregate (dict), join (list)...
[continues for 200 tokens]

✅ Optimized:
search_database(query: str, limit: int = 10)
# Search database for {query}. Returns top {limit} results.
```

### 5. Long-Horizon Strategies

For extended tasks that approach context limits:

**Compaction:**
- Summarize conversation when approaching limits
- Preserve architectural decisions and critical details
- Discard redundant outputs

**Structured Note-Taking:**
- Maintain external memory files (NOTES.md, TODO.md)
- Persist knowledge across context resets

**Sub-Agent Architecture:**
- Delegate focused tasks to specialized agents
- Return condensed summaries (1,000-2,000 tokens)
- Keep main agent context clean

---

## Quality Checklist

Before finalizing any system prompt, verify:

### Content Quality
- [ ] Clear, explicit instructions (no ambiguity)
- [ ] Context and reasoning provided (explains why)
- [ ] Specific success criteria defined
- [ ] Careful example selection (aligned with goals)
- [ ] Security considerations addressed

### Structure Quality
- [ ] Well-organized sections with clear delimiters
- [ ] Logical information flow
- [ ] Consistent formatting
- [ ] Platform-appropriate structure used

### Context Engineering
- [ ] High-signal minimalism applied (no unnecessary tokens)
- [ ] Just-in-time retrieval opportunities identified
- [ ] Progressive disclosure implemented
- [ ] Tool descriptions optimized

### Platform Fit
- [ ] Platform-specific features used appropriately
- [ ] Follows platform best practices
- [ ] Leverages platform strengths

### Validation
- [ ] Token count estimated and justified
- [ ] Examples tested (if included)
- [ ] Edge cases considered
- [ ] Iteration path identified

---

## Common Patterns and Anti-Patterns

### ✅ Do This

**Clear Identity:**
```
You are an expert code reviewer created by [Company]. You analyze code for
bugs, security issues, and performance problems.
```

**Explicit Instructions:**
```
When reviewing code:
1. Read the entire file first
2. Check for security vulnerabilities (SQL injection, XSS, etc.)
3. Identify performance bottlenecks
4. Suggest specific improvements with examples
```

**Context and Reasoning:**
```
Provide context in your reviews because developers need to understand WHY
a change is necessary, not just WHAT to change. This helps them learn and
avoid similar issues in the future.
```

**Platform-Specific Features (Claude):**
```xml
<thinking>
Before providing feedback, analyze:
- Code architecture and design patterns
- Security implications
- Performance characteristics
</thinking>
```

### ❌ Avoid This

**Vague Identity:**
```
You are helpful and friendly.
```

**Ambiguous Instructions:**
```
Review the code and provide feedback.
```

**No Context:**
```
Be thorough.
```

**Platform Mismatches:**
```
# Using OpenAI role pattern with Claude, missing XML structure
# Using Claude's <thinking> tags with GPT models that don't support them
```

**Token Waste:**
```
When you're reviewing code, it's really important that you take your time
and carefully consider every aspect of the code quality, including but not
limited to readability, maintainability, performance, security, scalability,
and documentation, and make sure you provide comprehensive feedback...
[continues unnecessarily]
```

---

## Examples and Templates

See `references/examples/` for complete templates:

- `chatbot-assistant.md` - Conversational AI agent
- `code-assistant.md` - Development helper
- `data-analyzer.md` - Analysis and insights
- `task-automation.md` - Workflow executor
- `research-agent.md` - Information gatherer

Each example includes:
- Requirements that drove the design
- Full system prompt
- Platform-specific variations (Claude/GPT/Gemini)
- Design decisions explained
- Token count analysis

---

## Iteration and Improvement

System prompts should evolve based on observed behavior:

**Iteration Process:**
1. **Deploy and Observe** - Use prompt in real scenarios
2. **Identify Failure Modes** - Where does agent struggle?
3. **Root Cause Analysis** - Why did it fail?
4. **Targeted Improvements** - Add specific instructions for failure cases
5. **Re-validate** - Test improvements

**Start Minimal:**
- Begin with simplest prompt that captures core requirements
- Add complexity only when failures justify it
- "Do the simplest thing that works"

**Track Changes:**
- Document what changed and why
- Measure impact (qualitative or quantitative)
- Version prompts for rollback capability

---

## Reference Materials

| File | Content |
|------|---------|
| `references/anthropic-best-practices.md` | Official Anthropic/Claude prompt engineering guidelines |
| `references/openai-best-practices.md` | Official OpenAI/GPT prompt engineering guidelines |
| `references/google-best-practices.md` | Official Google/Gemini prompt design strategies |
| `references/context-engineering.md` | Context engineering principles and techniques |
| `references/examples/` | Complete system prompt templates for common agent types |

Load these references as needed for detailed guidance.
