from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-small"  # You can also try flan-t5-base or flan-t5-large

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

prompts = [
    "What is first letter of Alphabet?",
    "What is AI?", 
    "Write a poem for sun"
]

for prompt in prompts:
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=20)
    print(f"Prompt: {prompt}")
    print("Output:", tokenizer.decode(outputs[0], skip_special_tokens=True))
    print("-" * 30)
