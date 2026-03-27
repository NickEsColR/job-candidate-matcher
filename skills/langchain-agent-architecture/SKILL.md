---
name: langchain-agent-architecture
description: >
  LangChain architecture decision guide for choosing workflows, a single agent, or multi-agent systems.
  Trigger: When deciding how to structure an AI system in LangChain.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Context7ResolveLibraryId, Context7QueryDocs
---

## When to Use

- Deciding whether a problem is a workflow, a single agent, or a multi-agent system
- Refactoring an overengineered AI system back to the simplest architecture that works
- Planning LangChain solutions where latency, cost, context size, or error tolerance matter
- Choosing between deterministic control flow and autonomous decision-making

## Critical Patterns

### Pattern 1: Start with workflows

- If you can write the steps in advance, it is a workflow.
- Use workflows for stable, repeatable processes that are easy to test and debug.
- Workflows can still include routing, parallel fan-out/fan-in, evaluator loops, and orchestrator-worker patterns when the control flow is predetermined.

### Pattern 2: Tools are capabilities, not agents

- A tool is something the system can do; an agent is the decision maker.
- Ten APIs behind one model is still a single agent, not multi-agent.
- Add tools before adding another decision maker.

### Pattern 3: Use one agent when the path is dynamic

- Choose a single agent when the next step depends on what the system discovers at runtime.
- Single agents work best when tasks are tightly coupled, global context matters, and the tool set is manageable.
- Rule of thumb: keep one agent under about 10-20 tools; beyond that, tool selection and context quality tend to degrade.

### Pattern 4: Escalate to multi-agent only for real constraints

- Use multi-agent systems when you need true parallelism, separate contexts, external agent interoperability, or hard security/data boundaries.
- Split agents when one context cannot hold the required tools and instructions without hurting quality.
- Do not split just because it sounds sophisticated.

### Pattern 5: Keep multi-agent systems orchestrated

- Prefer one orchestrator plus explicit handoffs.
- Avoid free-form peer-to-peer chatter between agents.
- Share artifacts through clear contracts, not hidden conversational state.

### Decision table

| If this is true | Use this | Why |
|---|---|---|
| You can define the full step sequence up front | Workflow | Predictable, cheap, testable |
| The path depends on discoveries made at runtime, but one context can manage it | Single agent | Autonomy without coordination overhead |
| Tasks are independent, tool sets diverge, or boundaries must stay separate | Multi-agent | Parallelism, modularity, separation |

## Code Examples

### Example 1: Workflow

```python
# Fixed control flow: classify -> route -> draft -> validate
def handle_ticket(ticket):
    category = classify(ticket)
    team = route(category)
    draft = draft_response(ticket, team)
    return validate(draft)
```

### Example 2: Single agent with tools

```python
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-5.4-mini",
    tools=[search, retrieve, validate],
    system_prompt="Use tools to solve the task step by step."
)
```

### Example 3: Multi-agent with an orchestrator

```python
# Orchestrator delegates research to one agent and writing to another.
research_agent = create_agent(...)
writing_agent = create_agent(...)
orchestrator = create_agent(...)
```

## Commands

```bash
uv add langchain langgraph
```

## Resources

- **Related skill**: See [langchain-agents](../langchain-agents/SKILL.md) for implementation patterns after the architecture choice is made.
