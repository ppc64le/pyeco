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

test_cases = [
    "Classify the sentiment of this sentence: 'I absolutely love this phone!' Answer with Positive, Neutral, or Negative.",
    "Extract the person's name and location from this sentence: 'Alice went to New York to attend a tech conference.' Return as JSON.",
]

# Run each test case
for i, prompt in enumerate(test_cases, 1):
    print(f"\n Task {i}: {prompt}")
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_length=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Output:\n{response}")