from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


# ==========================================
# 1. STATE
# ==========================================

class AgentState(TypedDict):
    question: str
    category: str
    answer: str


# ==========================================
# 2. PROCESS NODE
# ==========================================

def process_node(state: AgentState):

    print("\n[PROCESS]")
    print("State recebido:")
    print(state)

    question = state["question"].lower()

    if "nota fiscal" in question:
        category = "finance"

        answer = (
            "A pergunta foi classificada "
            "como Finance."
        )

    elif "senha" in question or "acesso" in question:
        category = "it"

        answer = (
            "A pergunta foi classificada "
            "como IT."
        )

    elif "categoria" in question:

        if state["category"]:
            category = state["category"]

            answer = (
                f"A categoria anterior era "
                f"{state['category']}."
            )

        else:
            category = ""

            answer = (
                "Não tenho informação sobre "
                "a categoria anterior."
            )

    else:
        category = state["category"]
        answer = "Pergunta processada."

    return {
        "category": category,
        "answer": answer,
    }


# ==========================================
# 3. CHECKPOINTER
# ==========================================

checkpointer = InMemorySaver()


# ==========================================
# 4. GRAPH
# ==========================================

graph = StateGraph(AgentState)

graph.add_node(
    "process",
    process_node
)

graph.add_edge(
    START,
    "process"
)

graph.add_edge(
    "process",
    END
)

app = graph.compile(
    checkpointer=checkpointer
)


# ==========================================
# 5. THREADS
# ==========================================

config_finance = {
    "configurable": {
        "thread_id": "conversation-finance"
    }
}

config_it = {
    "configurable": {
        "thread_id": "conversation-it"
    }
}


# ==========================================
# 6. PRIMEIRA MENSAGEM — FINANCE
# ==========================================

print("\n============================")
print("THREAD FINANCE — TURNO 1")
print("============================")

result_finance_1 = app.invoke(
    {
        "question": "Minha nota fiscal foi paga?",
        "category": "",
        "answer": "",
    },
    config=config_finance,
)

print("\nResultado:")
print(result_finance_1)


# ==========================================
# 7. PRIMEIRA MENSAGEM — IT
# ==========================================

print("\n============================")
print("THREAD IT — TURNO 1")
print("============================")

result_it_1 = app.invoke(
    {
        "question": "Esqueci minha senha.",
        "category": "",
        "answer": "",
    },
    config=config_it,
)

print("\nResultado:")
print(result_it_1)


# ==========================================
# 8. SEGUNDO TURNO — FINANCE
# ==========================================

print("\n============================")
print("THREAD FINANCE — TURNO 2")
print("============================")

result_finance_2 = app.invoke(
    {
        "question": "E qual era a categoria?"
    },
    config=config_finance,
)

print("\nResultado:")
print(result_finance_2)


# ==========================================
# 9. SEGUNDO TURNO — IT
# ==========================================

print("\n============================")
print("THREAD IT — TURNO 2")
print("============================")

result_it_2 = app.invoke(
    {
        "question": "E qual era a categoria?"
    },
    config=config_it,
)

print("\nResultado:")
print(result_it_2)]