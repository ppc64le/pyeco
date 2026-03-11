import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


llm= "ibm-granite/granite-3.2-2b-instruct"
tokenizer = AutoTokenizer.from_pretrained(llm) 
model = AutoModelForCausalLM.from_pretrained( 
    llm, 
    device_map="auto", 
    dtype=torch.bfloat16, 
) 
print(f"\nLLM USED: {llm}\n")

print("\n Example1:\n")
inputs = tokenizer("Explain IBM Granite 3.0 in simple terms", return_tensors="pt").to(model.device) 
outputs = model.generate(**inputs, max_length=100) 
print(tokenizer.decode(outputs[0], skip_special_tokens=True)) 

print("\n Example2: \n")
inputs = tokenizer("Write a python script to return sum of two variables", return_tensors="pt").to(model.device) 
outputs = model.generate(**inputs, max_length=100) 
print(tokenizer.decode(outputs[0], skip_special_tokens=True)) 