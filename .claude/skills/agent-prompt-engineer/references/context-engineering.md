# Context Engineering for AI Agents

Strategies for curating and maintaining optimal token sets during LLM inference.

**Source:**
- [Effective Context Engineering for AI Agents - Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

---

## What is Context Engineering?

**Definition:**
Context engineering refers to "strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."

**Evolution:**
- **Prompt Engineering** (2020-2023): Focus on finding right words/phrases in prompts
- **Context Engineering** (2024+): Focus on managing ALL information available to model

**Key Shift:**
Building with language models is becoming less about finding the right words and phrases for your prompts, and more about answering the broader question: **"What configuration of context is most likely to generate our model's desired behavior?"**

---

## Why Context Engineering Matters

### 1. Finite Attention Budget

**Problem:**
Language models have limited capacity to process context effectively.

**Research Finding:**
"Needle-in-a-haystack" benchmarking reveals that **model accuracy decreases as context window size grows**—a phenomenon called **context rot**.

**Implication:**
- More context ≠ better performance
- Quality over quantity
- Strategic information placement matters

### 2. Architectural Constraints

**Transformer Limitation:**
Transformer-based LLMs must compute **n² pairwise relationships** between tokens.

**Trade-off:**
Creates tension between:
- **Context size**: How much information is available
- **Attention focus**: How effectively the model processes it

**Additional Factor:**
Models trained primarily on shorter sequences show **reduced precision for long-range reasoning**.

---

## Core Principle: High-Signal Minimalism

**Principle:**
Find "the **smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome**."

**Context is a Public Good:**
- Every token in context competes for model's attention
- Wasted tokens reduce effectiveness for all information
- Optimization benefits entire system

**Good Context Engineering:**
Maximizing signal-to-noise ratio within your attention budget.

**Analogy:**
Like packing for a trip with weight limit—bring only essentials, maximize utility per item.

---

## Key Strategies

### 1. System Prompt Design

**Goal:**
Achieve the "right altitude"—balance between specificity and flexibility.

**Right Altitude Defined:**
- **Specific enough** to guide behavior effectively
- **Flexible enough** to avoid brittle, hardcoded logic

**Structure:**
Organize into distinct sections:

```markdown
## Background
[High-level context about the agent's purpose]

## Instructions
[Core operational guidelines]

## Tool Guidance
[When and how to use each tool]

## Output Specifications
[Expected response format and structure]
```

**Language:**
- Use clear, direct language
- Employ XML tagging or Markdown headers for clarity
- Minimize information while ensuring adequate guidance

**Anti-Pattern:**
```
❌ Too Specific (Brittle):
"If user says 'hello', respond 'Hello! How can I help you today?'
If user says 'hi', respond 'Hi there! What can I do for you?'
If user says 'hey', respond 'Hey! What's up?'"
[... 100 more exact patterns ...]

✅ Right Altitude:
"Greet users warmly and ask how you can help. Match their tone and formality level."
```

### 2. Tool Optimization

**Self-Contained Tools:**
Each tool should be independently understandable without cross-referencing.

**Unambiguous Purpose:**
Clear, single responsibility per tool.

**Avoid Bloat:**
- No overlapping functionality
- Concise descriptions (avoid 500-word tool docs)
- Descriptive parameter names

**Example:**
```
❌ Bloated:
search_database(query, options)
# Complex tool with 20 optional parameters, overlapping with other tools,
# 500-word documentation explaining every edge case...

✅ Optimized:
search_code(query: str) -> list[str]
# Searches codebase for {query}. Returns file paths with matches.

read_file(path: str) -> str
# Reads complete file at {path}. Returns contents.
```

**Tool Set Design:**
- Maintain clarity about which tool addresses specific situations
- Avoid redundant tools that do similar things
- Design parameters to play to model strengths

### 3. Few-Shot Prompting

**Quality Over Quantity:**
Include **diverse, canonical examples** rather than exhaustive edge cases.

**Purpose:**
Examples serve as visual demonstrations for desired behavior.

**Guidelines:**
- 2-4 examples typically sufficient
- Show variety of scenarios
- Demonstrate format and style
- Align with goals

**Anti-Pattern:**
```
❌ Too Many Examples:
[Includes 50 examples covering every possible variation]
[Consumes 5,000 tokens]

✅ Strategic Examples:
[3 diverse examples showing: simple case, complex case, edge case]
[Consumes 500 tokens]
```

### 4. Just-In-Time Context Retrieval ⭐

**Principle:**
Rather than pre-loading all data, agents maintain **lightweight references** (file paths, queries, links) and retrieve information dynamically at runtime using tools.

**Benefits:**
- Mirrors human cognition and external indexing systems
- Enables progressive disclosure through exploration
- Reduces token overhead
- Scales to large knowledge bases

**Pattern:**
```
❌ Upfront Loading:
System Prompt: Here's our entire 50-page documentation: [paste all docs]

✅ Just-In-Time:
System Prompt: You have access to documentation via search_docs(query) tool.
Runtime: Agent calls search_docs("authentication") when needed.
```

**Hybrid Strategy:**
Claude Code combines:
- **Upfront**: CLAUDE.md file (project context)
- **Dynamic**: glob/grep tools (specific files on-demand)
- **Balance**: Speed vs. exploration flexibility

**Implementation:**
```markdown
## Available Resources

### Documentation
Use `fetch_docs(topic)` to retrieve relevant documentation as needed.

### Code Examples
Use `search_examples(query)` to find code samples when implementing.

### Best Practices
Use `get_guidelines(category)` to access standards and patterns.

## Workflow
1. Gather requirements
2. **Retrieve relevant documentation** using tools
3. Implement solution
4. **Fetch examples** for reference
5. Validate against **retrieved guidelines**
```

### 5. Progressive Disclosure

**Principle:**
Tier information by usage frequency and load accordingly.

**Three Tiers:**

| Tier | Size | When Loaded | Content |
|------|------|-------------|---------|
| **Tier 1** | ~100 tokens | Always | Core identity, critical instructions |
| **Tier 2** | ~500 tokens | Conditional | Detailed workflows, loaded for specific tasks |
| **Tier 3** | Unlimited | On-demand | Examples, edge cases, detailed docs (via tools) |

**Example:**

**Tier 1 (Always):**
```markdown
You are CodeReview, an expert code reviewer. You identify bugs, security issues,
and performance problems. You provide specific, actionable feedback.
```

**Tier 2 (Loaded for code review tasks):**
```markdown
## Code Review Workflow
1. Read entire file for context
2. Check security (OWASP Top 10)
3. Identify performance bottlenecks
4. Review style and maintainability
5. Provide specific suggestions with examples
```

**Tier 3 (On-demand via tools):**
```markdown
Agent calls: get_security_checklist() when reviewing security
Agent calls: get_performance_patterns() when optimizing
Agent calls: search_examples("async patterns") when needed
```

---

## Long-Horizon Task Solutions

For extended tasks that approach context limits:

### 1. Compaction

**Strategy:**
Summarize conversation contents when approaching context limits.

**What to Preserve:**
- Architectural decisions
- Critical details
- Key conclusions

**What to Discard:**
- Redundant outputs
- Intermediate reasoning (if conclusion captured)
- Verbose explanations (if action taken)

**Example:**
```
Original (1,000 tokens):
User: Can you analyze this code?
Agent: I'll analyze the code. Let me read it first...
[Long analysis process]
Agent: I found 5 issues: [detailed descriptions]
[Back and forth discussion]
User: Fix issue #1
Agent: I'll fix issue #1. First, let me...
[Detailed fix process]

Compacted (200 tokens):
Analyzed code, found 5 issues (security: 2, performance: 2, style: 1).
Fixed issue #1 by [specific change]. Remaining issues: [list].
```

### 2. Structured Note-Taking

**Strategy:**
Agents maintain **external memory files** for persistent knowledge across context resets.

**Common Patterns:**
- `NOTES.md`: Key decisions and learnings
- `TODO.md`: Outstanding tasks
- `DECISIONS.md`: Architectural choices
- `CONTEXT.md`: Project-specific information

**Example:**
```markdown
# PROJECT_NOTES.md

## Architecture Decisions
- Using PostgreSQL for data persistence (decided 2024-01-15)
- REST API following OpenAPI 3.0 spec
- JWT for authentication

## Known Issues
1. Rate limiting not yet implemented
2. Email service needs error handling

## Next Steps
- [ ] Implement rate limiting
- [ ] Add email retry logic
- [ ] Write integration tests
```

**Benefits:**
- Survives context resets
- Shareable across sessions
- Version controlled with code

**Real-World Example:**
Claude playing Pokémon demonstrated this effectively—maintaining game state, strategies, and learnings in external files.

### 3. Sub-Agent Architectures

**Strategy:**
Delegate focused tasks to specialized agents with clean context windows.

**Pattern:**
```
Main Agent (Coordinator)
├─> Sub-Agent 1: Security Analysis (clean context)
│   Returns: Security report (1,500 tokens)
├─> Sub-Agent 2: Performance Analysis (clean context)
│   Returns: Performance report (1,200 tokens)
└─> Sub-Agent 3: Code Generation (clean context)
    Returns: Generated code (2,000 tokens)
```

**Benefits:**
- Each sub-agent starts with clean, focused context
- No context pollution from unrelated tasks
- Parallelizable execution
- Condensed summaries returned (1,000-2,000 tokens)

**Main Agent Receives:**
Short summaries instead of full conversation history.

**Example:**
```markdown
Main Agent Context:
- Task: Implement authentication system
- Delegated security review to Security-Agent
- Security-Agent returned: "Found 3 vulnerabilities: [list]. Recommendations: [list]."
- Now implementing fixes based on recommendations

vs. Including full security agent conversation (10,000 tokens)
```

---

## Practical Guidance

### Start Minimal, Iterate

**Process:**
1. **Start** with minimal prompts using best available model
2. **Observe** where agent fails
3. **Add** instructions based on identified failure modes
4. **Test** improvements
5. **Repeat**

**Principle:**
"Do the simplest thing that works."

**Anti-Pattern:**
```
❌ Over-Engineering Upfront:
[Create 10-page system prompt covering every possible scenario]
[Agent is brittle, slow, and still fails in unexpected ways]

✅ Iterative Approach:
[Start with 1-paragraph prompt]
[Agent fails at X]
[Add specific instruction for X]
[Agent works better]
[Repeat as needed]
```

### As Models Improve

**Trend:**
As model capabilities improve, agents can operate with progressively **less human curation**.

**Implication:**
- Don't over-specify with advanced models
- Let model intelligence handle ambiguity
- Focus on high-level goals rather than detailed steps

**Example with Claude 4.x:**
```
❌ Over-Specified:
"First, read the file. Then, parse line 1. Then check if line 1 contains...
Then, if it does, extract... Then, store in a variable... Then..."

✅ High-Level:
"Extract all function definitions from this file and return their signatures."
```

---

## Token Budget Examples

### Example 1: Code Review Agent

**Without Context Engineering (5,000 tokens):**
```
System Prompt: 2,000 tokens
- Verbose instructions
- 20 examples
- Complete documentation inlined
- All security rules listed
- All style guidelines listed

Tool Definitions: 3,000 tokens
- 15 tools with overlapping functionality
- Verbose descriptions
- Every parameter explained in detail
```

**With Context Engineering (1,200 tokens):**
```
System Prompt: 500 tokens
- Clear, concise instructions
- 3 strategic examples
- References to retrievable docs
- Key security principles only
- Core style rules only

Tool Definitions: 700 tokens
- 6 focused tools, no overlap
- Concise descriptions
- Self-explanatory parameters

Just-in-Time Resources:
- fetch_security_checklist() when needed
- get_style_guide() when needed
- search_examples() for patterns
```

**Result:**
- 76% token reduction
- Same or better functionality
- Faster processing
- More attention per token

### Example 2: Research Agent

**Without Context Engineering:**
```
Upfront Load: Entire knowledge base (50,000 tokens)
Result: Context rot, poor attention, slow
```

**With Context Engineering:**
```
Tier 1 (100 tokens):
"You are a research agent. Use search_knowledge(query) to find information."

Tier 3 (On-demand):
Agent calls search_knowledge("quantum computing") → returns 1,000 tokens
Agent uses specific information
Agent calls search_knowledge("entanglement") → returns 800 tokens

Total at any time: ~2,000 tokens (vs. 50,000)
```

---

## Common Patterns and Anti-Patterns

### ✅ Do This

**Minimal Core Prompt:**
```
You are [identity]. Your purpose is [goal].

Key capabilities: [list]
Critical constraints: [list]

Use tools to retrieve additional information as needed.
```

**Just-In-Time Retrieval:**
```
Available tools:
- search_docs(query): Retrieve relevant documentation
- get_examples(topic): Fetch code examples
- fetch_guidelines(category): Load specific standards
```

**Structured Note-Taking:**
```
Instructions: Maintain NOTES.md with key decisions and learnings.
Update after significant discoveries or decisions.
```

**Sub-Agent Delegation:**
```
For complex analysis:
1. Delegate to specialized sub-agent
2. Receive summary report
3. Integrate findings
```

### ❌ Avoid This

**Everything Upfront:**
```
System Prompt:
[Paste entire 50-page documentation]
[Include all 100 examples]
[List all possible scenarios]
[10,000+ tokens]
```

**Bloated Tools:**
```
super_tool(query, options, config, settings, preferences, ...)
# One tool trying to do everything
# 50 parameters
# 2,000 token description
```

**No Progressive Disclosure:**
```
[Load all information always, regardless of task]
[No tiering of importance]
[No dynamic retrieval]
```

**Context Pollution:**
```
[Include full conversation history in every sub-agent]
[Carry over irrelevant information across tasks]
[No summarization or compaction]
```

---

## Measuring Context Engineering Quality

### Metrics

**Token Efficiency:**
- Information per token ratio
- Redundancy percentage
- Unused context percentage

**Performance:**
- Task success rate
- Response accuracy
- Consistency across runs

**Attention Quality:**
- Relevant information recall
- Distractor resistance
- Long-range reasoning accuracy

### Optimization Checklist

Before deploying:
- [ ] System prompt is minimal and focused
- [ ] Tools are self-contained and unambiguous
- [ ] Examples are strategic, not exhaustive
- [ ] Just-in-time retrieval implemented for large resources
- [ ] Progressive disclosure tiers defined
- [ ] Long-horizon strategies in place (if applicable)
- [ ] Token budget justified and measured

---

## Case Study: Claude Code

**Challenge:**
Help users with software engineering tasks across diverse codebases.

**Context Engineering Approach:**

1. **Minimal Core System Prompt**
   - Essential identity and capabilities
   - High-level behavioral guidelines
   - ~1,000 tokens

2. **CLAUDE.md (Tier 1)**
   - Project-specific context
   - User-provided guidelines
   - Loaded upfront but typically <2,000 tokens

3. **Just-In-Time File Access (Tier 3)**
   - glob tool: Find files by pattern
   - grep tool: Search for specific content
   - read tool: Load specific files when needed

4. **Sub-Agents**
   - Explore agent: Codebase navigation
   - Plan agent: Implementation planning
   - Each gets clean context
   - Returns condensed results

5. **Structured Memory**
   - Todo lists for task tracking
   - Notes for key decisions
   - Persistent across context resets

**Result:**
- Handles codebases of any size
- Maintains context efficiency
- Scales to complex tasks
- Users feel understood without overwhelming the model

---

## Summary

**Key Takeaways:**

1. **Context is Limited**: Treat it as precious resource
2. **Quality Over Quantity**: High-signal minimalism wins
3. **Just-In-Time**: Retrieve information dynamically
4. **Progressive Disclosure**: Tier by importance
5. **Long-Horizon Tools**: Compaction, notes, sub-agents
6. **Start Simple**: Iterate based on failures

**The Fundamental Question:**
"What configuration of context is most likely to generate our model's desired behavior?"

Answer this through strategic curation, dynamic retrieval, and continuous optimization.

---

## Additional Resources

**Related References:**
- `anthropic-best-practices.md` - Claude-specific prompt patterns
- `openai-best-practices.md` - GPT-specific patterns
- `google-best-practices.md` - Gemini-specific patterns
- `examples/` - See context engineering in practice

**Further Reading:**
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering)
- Needle-in-a-haystack benchmarking research
- Transformer architecture papers
