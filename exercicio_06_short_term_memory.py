from langchain.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import InMemorySaver


# ==========================================
# 1. NODE
# ==========================================

def conversation_node(state: MessagesState):

    print("\n[CONVERSATION NODE]")

    print("Histórico recebido:")

    for message in state["messages"]:
        print(
            f"- {message.type}: "
            f"{message.content}"
        )

    last_message = state["messages"][-1]
    user_text = last_message.content.lower()

    # Lógica simples e determinística
    if "meu nome é" in user_text:

        name = (
            last_message.content
            .lower()
            .split("meu nome é", 1)[1]
            .strip()
            .replace(".", "")
            .title()
        )

        response = (
            f"Prazer, {name}. "
            "Vou considerar seu nome nesta conversa."
        )

    elif "qual é meu nome" in user_text:

        name = None

        for message in state["messages"]:

            if (
                isinstance(message, HumanMessage)
                and "meu nome é" in message.content.lower()
            ):

                name = (
                    message.content
                    .lower()
                    .split("meu nome é", 1)[1]
                    .strip()
                    .replace(".", "")
                    .title()
                )

        if name:
            response = (
                f"Seu nome é {name}."
            )

        else:
            response = (
                "Você ainda não informou "
                "seu nome nesta conversa."
            )

    else:
        response = (
            "Entendi sua mensagem."
        )

    return {
        "messages": [
            AIMessage(
                content=response
            )
        ]
    }


# ==========================================
# 2. CHECKPOINTER
# ==========================================

checkpointer = InMemorySaver()


# ==========================================
# 3. GRAPH
# ==========================================

graph = StateGraph(MessagesState)

graph.add_node(
    "conversation",
    conversation_node
)

graph.add_edge(
    START,
    "conversation"
)

graph.add_edge(
    "conversation",
    END
)

app = graph.compile(
    checkpointer=checkpointer
)


# ==========================================
# 4. THREAD
# ==========================================

config = {
    "configurable": {
        "thread_id": "conversation-001"
    }
}


# ==========================================
# 5. PRIMEIRO TURNO
# ==========================================

print("\n============================")
print("TURNO 1")
print("============================")

result_1 = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="Meu nome é Cassio."
            )
        ]
    },
    config=config,
)

print("\nResposta:")
print(
    result_1["messages"][-1].content
)


# ==========================================
# 6. SEGUNDO TURNO
# ==========================================

print("\n============================")
print("TURNO 2")
print("============================")

result_2 = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="Qual é meu nome?"
            )
        ]
    },
    config=config,
)

print("\nResposta:")
print(
    result_2["messages"][-1].content
)