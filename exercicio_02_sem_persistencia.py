from typing import TypedDict

from langgraph.graph import StateGraph, START, END


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
        "answer": answer
    }


# ==========================================
# 3. GRAPH
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

app = graph.compile()


# ==========================================
# 4. PRIMEIRA EXECUÇÃO
# ==========================================

print("\n============================")
print("PRIMEIRA EXECUÇÃO")
print("============================")

result_1 = app.invoke({
    "question": "Minha nota fiscal foi paga?",
    "category": "",
    "answer": ""
})

print("\nResultado 1:")
print(result_1)


# ==========================================
# 5. SEGUNDA EXECUÇÃO
# ==========================================

print("\n============================")
print("SEGUNDA EXECUÇÃO")
print("============================")

result_2 = app.invoke({
    "question": "E qual era a categoria dela?",
    "category": "",
    "answer": ""
})

print("\nResultado 2:")
print(result_2)