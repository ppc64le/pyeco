from __future__ import annotations

import json
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

print("\n=======================================")
print("🚀 Starting Tools/Agent Subtest (PURE)")
print("=======================================\n")

# --------------------------------------------------
# 1) Define simple tools
# --------------------------------------------------
@tool
def add(x: int, y: int) -> int:
    """Add two integers and return the sum."""
    result = x + y
    print(f"🛠 Executing Tool: add({x}, {y}) = {result}")
    return result

@tool
def weather(city: str) -> str:
    """Return a stubbed weather string for a city (no network)."""
    result = f"Weather in {city}: sunny, 28C"
    print(f"🛠 Executing Tool: weather({city}) -> {result}")
    return result

# --------------------------------------------------
# 2) Prompt for ReAct-like behavior
# --------------------------------------------------
template = (
    "You are a helpful assistant with tools: add, weather.\n"
    "When the user asks a calculative question, call add. For weather, call weather.\n"
    "User: {input}"
)

prompt = PromptTemplate(template=template, input_variables=["input"])
parser = StrOutputParser()

# Deterministic fake LLM (plan then final)
responses = iter([
    'TOOL: add({"x": 6, "y": 7})',
    'The sum is 13.',
])

llm = RunnableLambda(lambda _in: next(responses))

# --------------------------------------------------
# 3) Tiny controller to parse the plan and execute tools
# --------------------------------------------------
def run_with_tools(user_input: str) -> str:
    print("👤 User Input:", user_input)
    print()

    formatted_prompt = prompt.format(input=user_input)
    print("📜 Prompt Sent to LLM:")
    print(formatted_prompt)
    print()

    plan = parser.invoke(llm.invoke(formatted_prompt))
    print("🤖 LLM Plan:")
    print(">>>", plan)
    print()

    if plan.startswith("TOOL:") and "add" in plan:
        args_str = plan.split("add(", 1)[1].rsplit(")", 1)[0].strip()
        print("🔎 Extracted Arguments String:", args_str)

        if args_str.startswith("{"):
            args = json.loads(args_str)
        else:
            args = json.loads("{" + args_str + "}")

        print("📦 Parsed Arguments:", args)
        print()

        tool_result = add.invoke(args)
        print("📤 Tool Result:", tool_result)
        print()

        final_prompt = f"Tool result: {tool_result}. Provide the final answer succinctly."
        print("📜 Final Prompt Sent to LLM:")
        print(final_prompt)
        print()

        final = parser.invoke(llm.invoke(final_prompt))
        print("🤖 Final LLM Response:")
        print(">>>", final)
        print()

        return final

    return plan

# --------------------------------------------------
# Run Test
# --------------------------------------------------
output = run_with_tools("What is 6 + 7?")
print("✅ Final Output Returned to User:", output)
print()

assert "13" in output

print("🎉 Tools/Agent subtest (PURE) completed successfully!\n")
