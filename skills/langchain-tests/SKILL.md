---
name: langchain-test-agent
description: >
  Testing patterns for LangChain v1 agents and tools with pytest and LangSmith.
  Trigger: When writing tests for LangChain agents, tools, or structured output.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Context7ResolveLibraryId, Context7QueryDocs
---

## When to Use

- Testing tool logic, validation, and error handling
- Testing agent behavior that depends on LLM decisions
- Testing structured output, RAG quality, prompt quality, latency, token usage, or other execution metrics
- Verifying guardrails and other model-driven behavior

## Critical Patterns

| Scenario | Use | Why |
|----------|-----|-----|
| Tool logic / validation / errors | Pytest | Deterministic and fast |
| External I/O around a tool | Pytest + mocks | Avoid network and LLM cost |
| Tool selection / multi-step traces | LangSmith | The model decides the path |
| Structured output / RAG / prompt quality | LangSmith | Needs model-level evaluation |
| Latency / tokens / cost | LangSmith traces + experiment metrics | Execution metrics live in tracing |

### Pattern 1: Test tools directly

- Call the tool's `.invoke()` method or the underlying function.
- Assert success, validation errors, and mocked dependencies.
- Do not wrap deterministic logic in agent tests.

### Pattern 2: Use LangSmith only when model behavior matters

- Mark the test with `@pytest.mark.langsmith`.
- Log inputs and outputs for traceability.
- Assert tool choice, trace shape, or other LLM-driven behavior.

### Pattern 3: Validate structured output at the agent boundary

- Use `response_format` on `create_agent`.
- Assert `result["structured_response"]`.
- Keep the schema test separate only if the schema has its own logic.

### Pattern 4: Keep tests focused and isolated

- One behavior per test.
- Prefer fixtures for agent setup.
- Mock slow or external dependencies.

### Pattern 5: Separate RAG evaluation from execution monitoring

- RAG evaluation focuses on retrieval quality and generation grounded in context.
- Latency and token monitoring come from traced executions and experiment metrics.
- Do not use a retrieval-quality evaluator to measure performance, and do not use performance metrics to judge factual grounding.

**Why this separation matters:**

- **RAG evaluation** detects bad retrieval or hallucinations even when the model sounds fluent.
- **Execution metrics** reveal bottlenecks and token spikes that hurt cost and responsiveness.

## Code Examples

### Example 1: Tool unit test

```python
from langchain_core.tools import tool
import pytest


@tool
def calculate_score(score: int) -> str:
    """Return PASS or FAIL based on score."""
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100")
    return "PASS" if score >= 60 else "FAIL"


def test_calculate_score_pass():
    assert calculate_score.invoke({"score": 85}) == "PASS"


def test_calculate_score_invalid():
    with pytest.raises(ValueError, match="0 and 100"):
        calculate_score.invoke({"score": 150})
```

### Example 2: Agent test with LangSmith and structured output

```python
import pytest
from langchain.agents import create_agent
from langsmith import testing as t
from pydantic import BaseModel


class ContactInfo(BaseModel):
    name: str
    email: str


@pytest.mark.langsmith
def test_agent_structured_output():
    query = "Extract: John Doe, john@example.com"
    t.log_inputs({"query": query})

    agent = create_agent(
        model="gpt-4.1-mini",
        tools=[],
        response_format=ContactInfo,
        system_prompt="Extract contact info."
    )

    result = agent.invoke({"messages": [{"role": "user", "content": query}]})

    t.log_outputs({"structured_response": result["structured_response"]})

    assert result["structured_response"].name == "John Doe"
    assert result["structured_response"].email == "john@example.com"
```

### Example 3: RAG evaluation with an LLM-as-a-judge

```python
from typing_extensions import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langsmith import evaluate


class FaithfulnessGrade(TypedDict):
    explanation: Annotated[str, ..., "Explain the score"]
    faithful: Annotated[bool, ..., "The answer is supported by the context"]


judge_llm = ChatOpenAI(model="gpt-4.1", temperature=0).with_structured_output(
    FaithfulnessGrade,
    method="json_schema",
    strict=True,
)


def faithfulness_evaluator(inputs: dict, outputs: dict) -> bool:
    prompt = f"Context: {inputs['context']}\nAnswer: {outputs['answer']}"
    grade = judge_llm.invoke(
        [
            {"role": "system", "content": "Evaluate whether the answer is grounded only in the context."},
            {"role": "user", "content": prompt},
        ]
    )
    return grade["faithful"]


evaluate(
    rag_chain,
    data="rag-dataset-name",
    evaluators=[faithfulness_evaluator],
)
```

### Example 4: Latency and token monitoring from experiment metrics

```python
from langsmith import Client


client = Client()

experiment = client.evaluate(
    rag_chain,
    data="rag-dataset-name",
    evaluators=[faithfulness_evaluator],
    experiment_prefix="rag-fidelity",
)

print(f"Latency p50: {experiment.latency_p50}")
print(f"Total tokens: {experiment.total_tokens}")
print(f"Prompt tokens: {experiment.prompt_tokens}")
print(f"Completion tokens: {experiment.completion_tokens}")
```

## Commands

```bash
uv add pytest pytest-mock langsmith
pytest tests/tools/ -v
LANGSMITH_API_KEY=your_key pytest tests/agents/ -v
```

## Resources

- **Skills**: See [langchain-agents](../langchain-agents/SKILL.md) for agent creation patterns.
- **Skills**: See [pytest](../pytest/SKILL.md) for pytest fixtures, async tests, and mocks.
