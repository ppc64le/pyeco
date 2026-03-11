import json
from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

try:
    from langchain_community.llms import FakeListLLM
except Exception:
    raise SystemExit(
        "langchain-community not installed. Install with: pip install langchain-community"
    )

print("\n==============================")
print("🚀 Starting LangChain Demo")
print("==============================\n")

# --------------------------------------------------
# 1) Prompt + Fake LLM
# --------------------------------------------------
print("STEP 1: Prompt + Fake LLM")
print("--------------------------")

prompt = PromptTemplate(
    template=(
        "You are a helpful assistant. Summarize the following text in one sentence.\n\n"
        "Text: {text}"
    ),
    input_variables=["text"],
)

llm = FakeListLLM(responses=[
    "This is a concise summary.",
])

chain = prompt | llm | StrOutputParser()

input_text = "LangChain helps you build LLM apps by composing components."
print("Input Text:", input_text)

out = chain.invoke({"text": input_text})

print("Generated Summary:")
print(">>>", out)
print()

# --------------------------------------------------
# 2) Structured parsing example
# --------------------------------------------------
print("STEP 2: Structured JSON Output")
print("-------------------------------")

llm_structured = FakeListLLM(responses=[
    '{"title": "LangChain", "bullets": ["chains", "prompts", "tools"]}'
])

json_prompt = PromptTemplate(
    template=(
        "Return a compact JSON object with keys 'title' and 'bullets' about: {topic}.\n"
        "No extra text."
    ),
    input_variables=["topic"],
)

def parse_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "raw": text}

structured_chain = json_prompt | llm_structured | parse_json

result = structured_chain.invoke({"topic": "LangChain"})

print("Raw Parsed Dictionary:")
print(result)

print("Title:", result.get("title"))
print("Bullets:", result.get("bullets"))
print()

# --------------------------------------------------
# 3) Runnable composition
# --------------------------------------------------
print("STEP 3: Sentiment Classification")
print("---------------------------------")

classify_prompt = PromptTemplate(
    template=(
        "Classify the sentiment (positive/neutral/negative).\n"
        "Text: {text}\n"
        "Answer with a single word."
    ),
    input_variables=["text"],
)

llm_classify = FakeListLLM(responses=["positive"])

classify_chain = {
    "text": RunnablePassthrough(),
} | classify_prompt | llm_classify | StrOutputParser()

sentence = "I love how composable this library feels!"
print("Input Sentence:", sentence)

sentiment = classify_chain.invoke(sentence)

print("Predicted Sentiment:")
print(">>>", sentiment)
print()

print("✅ All steps executed successfully!\n")
