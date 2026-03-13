from __future__ import annotations

import math
import re
from collections import Counter
from typing import List, Dict

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

print("\n========================================")
print("🎯 Starting Retrieval Subtest (PURE)")
print("========================================\n")

# --------------------------------------------------
# 1) Tiny corpus + tokenizer + TF vectors
# --------------------------------------------------
docs: List[str] = [
    "LangChain provides composable building blocks.",
    "FAISS enables efficient vector similarity search.",
    "Retrievers turn your vector store into a search interface.",
]

print("📚 Documents in Corpus:")
for i, d in enumerate(docs):
    print(f"{i+1}. {d}")
print()

def tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z0-9]+", text.lower()) if t]

def tf_vector(text: str) -> Counter:
    return Counter(tokenize(text))

def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    common = set(a.keys()) & set(b.keys())
    num = sum(a[t] * b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return num / (norm_a * norm_b)

# Precompute vectors
vecs = [tf_vector(d) for d in docs]

print("🧮 TF Vectors:")
for i, v in enumerate(vecs):
    print(f"Doc {i+1} vector:", dict(v))
print()

# --------------------------------------------------
# 2) Simple retriever (top-k by cosine)
# --------------------------------------------------
def retrieve(query: str, k: int = 2) -> List[str]:
    print("🔍 Query:", query)
    qv = tf_vector(query)
    print("Query Vector:", dict(qv))
    print()

    scored = []
    for i, dv in enumerate(vecs):
        score = cosine(qv, dv)
        print(f"Cosine similarity with Doc {i+1}: {score:.4f}")
        scored.append((score, i))

    scored.sort(reverse=True)
    print()

    top_docs = [docs[i] for _, i in scored[:k]]
    print(f"📌 Top {k} Retrieved Docs:")
    for d in top_docs:
        print(">>>", d)
    print()

    return top_docs

query = "How do I search my text efficiently?"
retrieved = retrieve(query, k=2)

# --------------------------------------------------
# 3) Chain: Prompt -> Fake LLM -> String
# --------------------------------------------------
print("🧠 Running Summarization Chain...\n")

summarize_prompt = PromptTemplate(
    template=(
        "You are a helpful assistant. Summarize the key points from the docs for the question.\n"
        "Question: {question}\n\nDocs:\n{docs}\n\nReturn a one-sentence answer."
    ),
    input_variables=["question", "docs"],
)

responses = iter([
    "Use a simple retriever to compare query and documents (e.g., cosine) and return the closest texts.",
])

fake_llm = RunnableLambda(lambda _input: next(responses))
chain = summarize_prompt | fake_llm | StrOutputParser()

joined = "\n---\n".join(retrieved)
answer = chain.invoke({"question": query, "docs": joined})

print("📝 Final Answer:")
print(">>>", answer)
print()

print("✅ Retrieval subtest (PURE) completed successfully!\n")
