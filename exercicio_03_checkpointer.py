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
            "A pergunta sobre nota fiscal foi "
            "classificada como Finance."
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
# 5. THREAD CONFIG
# ==========================================

config = {
    "configurable": {
        "thread_id": "conversation-1"
    }
}


# ==========================================
# 6. PRIMEIRA EXECUÇÃO
# ==========================================

print("\n============================")
print("PRIMEIRA EXECUÇÃO")
print("============================")

result_1 = app.invoke(
    {
        "question": "Minha nota fiscal foi paga?",
        "category": "",
        "answer": "",
    },
    config=config,
)

print("\nResultado 1:")
print(result_1)


# ==========================================
# 7. SEGUNDA EXECUÇÃO
# ==========================================

print("\n============================")
print("SEGUNDA EXECUÇÃO")
print("============================")

result_2 = app.invoke(
    {
        "question": "E qual era a categoria dela?"
    },
    config=config,
)

print("\nResultado 2:")
print(result_2)