---
name: langchain-agents
description: >
  LangChain v1 patterns for creating AI agents with create_agent, tools, prompts, and structured output.
  Trigger: When building AI agents with LangChain.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Context7ResolveLibraryId, Context7QueryDocs
---

## When to Use

- Building new AI agents with LangChain v1+
- Migrating from `create_react_agent` to `create_agent`
- Wiring tools directly into an agent
- Choosing between string model IDs, `init_chat_model()`, and provider-specific clients
- Configuring system prompts and structured output

## Critical Patterns

### Pattern 1: Use `create_agent`

- Prefer `create_agent` for all new agent work.
- Treat `create_react_agent` as legacy.

### Pattern 2: Pass tools directly

- Supply tools as a plain list.
- Do not wrap them in `ToolNode`.
- Keep tool definitions small and explicit.

### Pattern 3: Choose model configuration intentionally

- Use a string for the common case.
- Use `init_chat_model()` when you need runtime controls like temperature or timeout.
- Use `ChatOpenAI` when you need provider-specific parameters.

### Pattern 4: Use `system_prompt` for instructions

- Use a string for the common case.
- Use `SystemMessage` only when you need advanced provider features such as prompt caching.
- Do not use the old `prompt` parameter.

### Pattern 5: Use `response_format` for structured output

- Pass a Pydantic model directly for the common case.
- Use `ToolStrategy(Schema)` when tool-calling behavior is required.
- Use `ProviderStrategy(Schema)` when the provider supports native structured output.
- Read the validated object from `result["structured_response"]`.

### Pattern 6: Langchain libraries

- Always prefer langchain features inside langchain module over langchain-community.
- Use langchain-community only when no other option for the use case is available.
- langchain-x are integrations to specific techs and providers, only use when the additional features over the main langchain library are required.

## Code Examples

### Example 1: Simple agent with a tool

```python
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"


agent = create_agent(
    model="gpt-4.1-mini",
    tools=[search],
    system_prompt="You are a helpful assistant."
)
```

### Example 2: Agent with a custom model

```python
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

model = init_chat_model(
    model="gpt-4.1",
    temperature=0.1,
    max_tokens=1000
)

agent = create_agent(
    model=model,
    tools=[],
    system_prompt="You are a helpful assistant."
)
```

### Example 3: Agent with structured output

```python
from langchain.agents import create_agent
from pydantic import BaseModel

class ContactInfo(BaseModel):
    name: str
    email: str

agent = create_agent(
    model="gpt-4.1-mini",
    tools=[],
    response_format=ContactInfo,
    system_prompt="Extract contact information."
)

result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
result["structured_response"]  # ContactInfo instance
```

## Commands

```bash
uv add langchain
```

## Resources

- **Skills**: See [langchain-tests](../langchain-tests/SKILL.md) for testing agents and tools.
