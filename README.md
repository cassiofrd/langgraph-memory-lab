# LangGraph Memory Lab

Hands-on lab exploring state, persistence, short-term and long-term memory, and context management with LangGraph.

## About

This repository contains a sequence of small Python exercises created to study how state and memory work in LangGraph.

The examples are intentionally simple and focus on one concept at a time. The goal is not to build a production-ready agent, but to understand state, checkpoints, threads, interruptions, memory, and context before combining them in more complex agent architectures.

## Exercises

| # | Exercise | Main concept |
|---|---|---|
| 01 | `exercicio_01_state.py` | State updates across nodes |
| 02 | `exercicio_02_sem_persistencia.py` | Executions without persistence |
| 03 | `exercicio_03_checkpointer.py` | State persistence with a checkpointer |
| 04 | `exercicio_04_multiplas_threads.py` | Independent state across multiple threads |
| 05 | `exercicio_05_interrupt_resume.py` | Interrupt and resume / human-in-the-loop |
| 06 | `exercicio_06_short_term_memory.py` | Short-term conversational memory |
| 07 | `exercicio_07_long_term_memory.py` | Long-term memory across threads |
| 08 | `exercicio_08_context_management.py` | Selecting memory to use as context |

## Learning path

```text
State
  ↓
No persistence
  ↓
Checkpointer
  ↓
Multiple threads
  ↓
Interrupt / Resume
  ↓
Short-term memory
  ↓
Long-term memory
  ↓
Context management
```

### 01 — State

Introduces a typed LangGraph state and shows how nodes receive the current state and return partial updates that are incorporated into it.

### 02 — Without persistence

Runs the graph twice without a checkpointer to demonstrate that a new invocation does not automatically retain the state produced by the previous invocation.

### 03 — Checkpointer

Adds `InMemorySaver` and a `thread_id`, allowing LangGraph to recover state from an earlier invocation of the same thread.

### 04 — Multiple threads

Uses different `thread_id` values to demonstrate that separate conversations can use the same graph while maintaining independent state.

### 05 — Interrupt and resume

Uses `interrupt()` and `Command(resume=...)` to pause a workflow for human approval and later resume the same execution.

It also highlights an important design consideration: code before an interrupt may execute again when the node resumes, so side effects should be designed carefully.

### 06 — Short-term memory

Uses `MessagesState` and a checkpointer to maintain conversational history inside a thread across multiple turns.

### 07 — Long-term memory

Introduces `InMemoryStore` and a user-scoped namespace to store information that can be retrieved from a different conversation thread.

```text
Checkpointer + thread_id
        ↓
Short-term memory

Store + user namespace
        ↓
Long-term memory
```

### 08 — Context management

Demonstrates that the complete conversation state does not necessarily need to be used as model context.

The example preserves the complete message history while selecting only the most recent messages as context.

```text
Complete State
     ↓
Context selection
     ↓
Relevant context
     ↓
LLM
```

## Key concepts

### State vs. persistence

`State` represents the current data of a workflow. Persistence is the mechanism that allows that state to survive across graph invocations.

### Checkpointer vs. Store

A checkpointer persists state associated with a thread.

A Store can persist information outside a single thread, enabling long-term memory across conversations when appropriate.

### Memory vs. context

Memory represents information available to the application.

Context represents the subset of that information selected for a particular operation or model call.

```text
Available information
        ↓
Context engineering
        ↓
Information actually provided to the model
```

## Requirements

- Python 3.10+
- LangGraph
- LangChain

Install the dependencies:

```bash
pip install langgraph langchain
```

## Running the exercises

Clone the repository and run any exercise directly:

```bash
python exercicio_01_state.py
```

Then continue sequentially through the exercises.

No OpenAI API key is required for these examples because they focus on LangGraph state and memory concepts and use deterministic Python logic rather than LLM calls.

## Notes

The examples use in-memory implementations such as `InMemorySaver` and `InMemoryStore` for learning purposes. Their data is not intended to provide durable production persistence.

Production systems should also consider durable storage, identity and access boundaries, retention policies, security, observability, and failure recovery.

## Next steps

The next study block builds on these concepts with **context engineering**, including:

- static vs. dynamic context;
- different context for different nodes;
- relevant history selection;
- RAG context;
- long-term memory retrieval;
- tool context;
- token-based trimming;
- summarization;
- specialized context for supervisors and specialist agents.

## Purpose

This repository is part of a hands-on study series focused on understanding the architectural building blocks of AI agents with LangGraph through small, isolated, and progressively more complex examples.
