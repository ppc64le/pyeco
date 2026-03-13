from __future__ import annotations

from typing import Dict

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableLambda

print("\n==============================================")
print("🗂️ Starting Conversational Memory Subtest")
print("==============================================\n")

# Prompt with history placeholder
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

print("✅ Chat prompt with memory placeholder created.\n")

# Deterministic fake LLM
responses = iter([
    "Noted: your favorite editor is VS Code.",
    "Your favorite editor is VS Code.",
])

llm = RunnableLambda(lambda _in: next(responses))

chain = chat_prompt | llm | StrOutputParser()

# Attach memory store
store: Dict[str, InMemoryChatMessageHistory] = {}

def get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        print(f"🆕 Creating new session history for: {session_id}")
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "test-session"}}

print("🔐 Using session_id: test-session\n")

# --------------------------------------------------
# Turn 1
# --------------------------------------------------
print("🔹 TURN 1")
user_input1 = "Remember: my favorite editor is VS Code."
print("👤 User:", user_input1)

out1 = chain_with_history.invoke({"input": user_input1}, config=config)

print("🤖 Assistant:", out1)
print()

# --------------------------------------------------
# Turn 2
# --------------------------------------------------
print("🔹 TURN 2")
user_input2 = "What is my favorite editor?"
print("👤 User:", user_input2)

out2 = chain_with_history.invoke({"input": user_input2}, config=config)

print("🤖 Assistant:", out2)
print()

# --------------------------------------------------
# Inspect Stored Memory
# --------------------------------------------------
print("📚 Inspecting Stored Conversation History...\n")

hist = get_history("test-session").messages

for i, msg in enumerate(hist, 1):
    print(f"{i}. {msg.type.upper()}: {msg.content}")

print(f"\n📊 Total Messages in History: {len(hist)}")
print()

assert len(hist) >= 4  # 2 human + 2 ai expected

print("🎉 Conversational memory subtest (PURE) completed successfully!\n")
