from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


# ==========================================
# 1. STATE
# ==========================================

class ApprovalState(TypedDict):
    request: str
    amount: float
    approved: bool
    result: str


# ==========================================
# 2. ANALYZE
# ==========================================

def analyze_node(state: ApprovalState):
    print("\n[ANALYZE]")
    print("Solicitação:", state["request"])
    print("Valor:", state["amount"])

    return {}


# ==========================================
# 3. APPROVAL NODE
# ==========================================

def approval_node(state: ApprovalState):
    print("\n[APPROVAL NODE]")

    approval = interrupt(
        {
            "message": "Aprovação necessária",
            "request": state["request"],
            "amount": state["amount"],
        }
    )

    print("Resposta recebida após retomada:", approval)

    return {
        "approved": bool(approval)
    }


# ==========================================
# 4. ROUTING
# ==========================================

def route_after_approval(state: ApprovalState):
    if state["approved"]:
        return "execute"

    return "reject"


# ==========================================
# 5. EXECUTE
# ==========================================

def execute_node(state: ApprovalState):
    print("\n[EXECUTE]")

    result = (
        f"Solicitação aprovada e executada. "
        f"Valor: R$ {state['amount']:.2f}"
    )

    print(result)

    return {
        "result": result
    }


# ==========================================
# 6. REJECT
# ==========================================

def reject_node(state: ApprovalState):
    print("\n[REJECT]")

    result = "Solicitação rejeitada."

    print(result)

    return {
        "result": result
    }


# ==========================================
# 7. CHECKPOINTER
# ==========================================

checkpointer = InMemorySaver()


# ==========================================
# 8. GRAPH
# ==========================================

graph = StateGraph(ApprovalState)

graph.add_node(
    "analyze",
    analyze_node
)

graph.add_node(
    "approval",
    approval_node
)

graph.add_node(
    "execute",
    execute_node
)

graph.add_node(
    "reject",
    reject_node
)

graph.add_edge(
    START,
    "analyze"
)

graph.add_edge(
    "analyze",
    "approval"
)

graph.add_conditional_edges(
    "approval",
    route_after_approval,
    {
        "execute": "execute",
        "reject": "reject",
    },
)

graph.add_edge(
    "execute",
    END
)

graph.add_edge(
    "reject",
    END
)

app = graph.compile(
    checkpointer=checkpointer
)


# ==========================================
# 9. THREAD CONFIG
# ==========================================

config = {
    "configurable": {
        "thread_id": "approval-001"
    }
}


# ==========================================
# 10. PRIMEIRA EXECUÇÃO
# ==========================================

print("\n============================")
print("PRIMEIRA EXECUÇÃO")
print("============================")

result_1 = app.invoke(
    {
        "request": "Compra de equipamento",
        "amount": 15000.0,
        "approved": False,
        "result": "",
    },
    config=config,
)

print("\nResultado após interrupção:")
print(result_1)


# ==========================================
# 11. RESPOSTA HUMANA
# ==========================================

decision = input(
    "\nAprovar solicitação? (s/n): "
).strip().lower()

approved = decision == "s"


# ==========================================
# 12. RETOMADA
# ==========================================

print("\n============================")
print("RETOMANDO EXECUÇÃO")
print("============================")

result_2 = app.invoke(
    Command(
        resume=approved
    ),
    config=config,
)

print("\n=== RESULTADO FINAL ===")
print(result_2)