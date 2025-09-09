from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "ibm-granite/granite-3.1-2b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

prompts = [
    "What is first letter of Alphabet?",
    "What is AI?", 
    "Write a poem for sun"
]

for prompt in prompts:
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=50)
    print(f"Prompt: {prompt}")
    print("Output:", tokenizer.decode(outputs[0], skip_special_tokens=True))
    print("-" * 30)
