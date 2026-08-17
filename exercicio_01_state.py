from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ==========================================
# 1. STATE
# ==========================================

class AgentState(TypedDict):
    question: str
    category: str
    processed: bool
    answer: str


# ==========================================
# 2. RECEIVE
# ==========================================

def receive_node(state: AgentState):

    print("\n[RECEIVE]")
    print("State recebido:")
    print(state)

    return {
        "category": "finance"
    }


# ==========================================
# 3. PROCESS
# ==========================================

def process_node(state: AgentState):

    print("\n[PROCESS]")
    print("State recebido:")
    print(state)

    answer = (
        f"Pergunta processada na categoria "
        f"{state['category']}."
    )

    return {
        "processed": True,
        "answer": answer
    }


# ==========================================
# 4. FINALIZE
# ==========================================

def finalize_node(state: AgentState):

    print("\n[FINALIZE]")
    print("State recebido:")
    print(state)

    return {}


# ==========================================
# 5. GRAPH
# ==========================================

graph = StateGraph(AgentState)

graph.add_node(
    "receive",
    receive_node
)

graph.add_node(
    "process",
    process_node
)

graph.add_node(
    "finalize",
    finalize_node
)

graph.add_edge(
    START,
    "receive"
)

graph.add_edge(
    "receive",
    "process"
)

graph.add_edge(
    "process",
    "finalize"
)

graph.add_edge(
    "finalize",
    END
)

app = graph.compile()


# ==========================================
# 6. INITIAL STATE
# ==========================================

initial_state = {
    "question": "Minha nota fiscal foi paga?",
    "category": "",
    "processed": False,
    "answer": ""
}


# ==========================================
# 7. EXECUTION
# ==========================================

result = app.invoke(initial_state)


print("\n=== RESULTADO FINAL ===")
print(result)