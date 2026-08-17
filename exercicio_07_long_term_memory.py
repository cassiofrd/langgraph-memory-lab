from dataclasses import dataclass

from langchain.messages import HumanMessage, AIMessage

from langgraph.graph import (
    StateGraph,
    MessagesState,
    START,
    END,
)

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.runtime import Runtime


# ==========================================
# 1. CONTEXT
# ==========================================

@dataclass
class Context:
    user_id: str


# ==========================================
# 2. NODE
# ==========================================

def conversation_node(
    state: MessagesState,
    runtime: Runtime[Context],
):

    print("\n[CONVERSATION NODE]")

    user_id = runtime.context.user_id

    namespace = (
        user_id,
        "profile",
    )

    last_message = state["messages"][-1]

    text = last_message.content.lower()


    # ======================================
    # SALVAR LONG-TERM MEMORY
    # ======================================

    if "meu nome é" in text:

        name = (
            last_message.content
            .lower()
            .split("meu nome é", 1)[1]
            .strip()
            .replace(".", "")
            .title()
        )

        runtime.store.put(
            namespace,
            "name",
            {
                "name": name
            }
        )

        response = (
            f"Prazer, {name}. "
            "Vou lembrar dessa informação."
        )


    # ======================================
    # RECUPERAR LONG-TERM MEMORY
    # ======================================

    elif "qual é meu nome" in text:

        memories = runtime.store.search(
            namespace
        )

        if memories:

            name = memories[-1].value["name"]

            response = (
                f"Seu nome é {name}."
            )

        else:

            response = (
                "Não tenho seu nome salvo."
            )


    else:

        response = "Entendi."


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
# 4. LONG-TERM STORE
# ==========================================

store = InMemoryStore()


# ==========================================
# 5. GRAPH
# ==========================================

graph = StateGraph(
    MessagesState,
    context_schema=Context,
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
    checkpointer=checkpointer,
    store=store,
)


# ==========================================
# 6. THREAD 1
# ==========================================

config_thread_1 = {
    "configurable": {
        "thread_id": "conversation-001"
    }
}


print("\n============================")
print("THREAD 1")
print("============================")

result_1 = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="Meu nome é Cassio."
            )
        ]
    },
    config=config_thread_1,
    context=Context(
        user_id="user-123"
    ),
)

print(
    "\nResposta:",
    result_1["messages"][-1].content,
)


# ==========================================
# 7. THREAD 2
# ==========================================

config_thread_2 = {
    "configurable": {
        "thread_id": "conversation-002"
    }
}


print("\n============================")
print("THREAD 2")
print("============================")

result_2 = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="Qual é meu nome?"
            )
        ]
    },
    config=config_thread_2,
    context=Context(
        user_id="user-123"
    ),
)

print(
    "\nResposta:",
    result_2["messages"][-1].content,
)