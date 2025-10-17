import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
#quantization_config = BitsAndBytesConfig(load_in_4bit=True)
llm= "ibm-granite/granite-4.0-micro"
tokenizer = AutoTokenizer.from_pretrained(llm) 
model = AutoModelForCausalLM.from_pretrained( 
    llm, 
    device_map="auto", 
    dtype=torch.bfloat16, 
 #   quantization_config=quantization_config
) 
print(f"\nLLM USED: {llm}\n")
inputs = tokenizer("Explain IBM Granite 4.0 in simple terms", return_tensors="pt").to(model.device) 
outputs = model.generate(**inputs, max_length=100) 
print(tokenizer.decode(outputs[0], skip_special_tokens=True)) 