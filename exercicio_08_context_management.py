from langchain.messages import HumanMessage, AIMessage

from langgraph.graph import (
    StateGraph,
    MessagesState,
    START,
    END,
)

from langgraph.checkpoint.memory import InMemorySaver


# ==========================================
# 1. CONTEXT SIZE
# ==========================================

MAX_CONTEXT_MESSAGES = 4


# ==========================================
# 2. NODE
# ==========================================

def conversation_node(state: MessagesState):

    print("\n================================")
    print("[CONVERSATION NODE]")
    print("================================")

    all_messages = state["messages"]

    print(
        "\nTotal de mensagens no STATE:",
        len(all_messages),
    )

    print("\n--- STATE COMPLETO ---")

    for message in all_messages:

        print(
            f"{message.type}: "
            f"{message.content}"
        )


    # ======================================
    # SELEÇÃO DO CONTEXTO
    # ======================================

    context_messages = all_messages[
        -MAX_CONTEXT_MESSAGES:
    ]


    print("\n--- CONTEXTO SELECIONADO ---")

    for message in context_messages:

        print(
            f"{message.type}: "
            f"{message.content}"
        )


    # Neste exercício apenas simulamos
    # a geração da resposta.

    response = (
        f"Recebi sua mensagem. "
        f"O State possui "
        f"{len(all_messages)} mensagens, "
        f"mas eu usaria apenas "
        f"{len(context_messages)} como contexto."
    )


    return {
        "messages": [
            AIMessage(
                content=response
            )
        ]
    }


# ==========================================
# 3. CHECKPOINTER
# ==========================================

checkpointer = InMemorySaver()


# ==========================================
# 4. GRAPH
# ==========================================

graph = StateGraph(
    MessagesState
)

graph.add_node(
    "conversation",
    conversation_node,
)

graph.add_edge(
    START,
    "conversation",
)

graph.add_edge(
    "conversation",
    END,
)

app = graph.compile(
    checkpointer=checkpointer
)


# ==========================================
# 5. THREAD
# ==========================================

config = {
    "configurable": {
        "thread_id": "context-demo"
    }
}


# ==========================================
# 6. MULTIPLE TURNS
# ==========================================

questions = [
    "Meu nome é Cassio.",
    "Estou estudando LangGraph.",
    "Hoje estou estudando memória.",
    "Também quero estudar contexto.",
    "Qual foi o último assunto que mencionei?",
]


for i, question in enumerate(
    questions,
    start=1,
):

    print("\n\n")
    print("============================")
    print(f"TURNO {i}")
    print("============================")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content=question
                )
            ]
        },
        config=config,
    )

    print(
        "\nResposta:",
        result["messages"][-1].content,
    )