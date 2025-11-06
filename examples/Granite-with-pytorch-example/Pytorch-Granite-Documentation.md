# Granite 3.x and 4.0 Compatibility Validation with Python, PyTorch, and vLLM on PowerVM (CPU-only)

This document validates the compatibility of Granite 4.0 and Granite 3.2.2b with the Python ecosystem and PyTorch on PowerVM (CPU-only). It also details vLLM integration support for both Granite 3 and Granite 4 on PowerVM (CPU-only).

## Table of Contents

- [Introduction](#introduction)
- [Python Environment Setup for PyTorch](#python-environment-setup-for-pytorch)
- [Granite 4 with PyTorch](#granite-4-with-pytorch)
- [Granite 3.2.2b with PyTorch](#granite-322b-with-pytorch)
- [vLLM Docker Image Compatibility with Granite 3 & 4](#vllm-docker-image-compatibility-with-granite-3--4)
- [Integrated the vLLM Docker API into a Python Script](#integrated-the-vllm-docker-api-into-a-python-script)
- [Limitation and Challenges](#limitation-and-challenges)
- [Conclusion](#conclusion)

## Introduction
This document presents a comprehensive validation of the compatibility between Granite 4.0 and Granite 3.2.2b with the Python ecosystem and PyTorch, specifically on PowerVM environments configured for CPU-only execution. In addition to compatibility validation, this document also outlines support for vLLM (Very Large Language Model) integration with both Granite 3 and Granite 4.

## Python Environment Setup for PyTorch
To prepare the system for running Granite 4.0 and Granite 3.2.2b:

```
yum install -y gcc gcc-c++ make
yum install python3.12 python3.12-devel python3.12-pip
yum install libgfortran

mkdir granite-poc
cd granite-poc

python -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/libprotobuf/lib64:./venv/lib64/python3.12/site-packages/openblas/lib:$LD_LIBRARY_PATH
```

## Granite 4 with PyTorch
Code:
```
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
inputs = tokenizer("Explain IBM Granite 4.0 in simple terms", return_tensors="pt").to(model.device) 
outputs = model.generate(**inputs, max_length=100) 
print(tokenizer.decode(outputs[0], skip_special_tokens=True)) 
```

Output:
```
IBM Granite 4.0 is a large language model developed by IBM. It's like a very smart computer program that can understand and generate human language. It's trained on a vast amount of data, allowing it to learn and understand various topics, patterns, and structures in language.

Imagine it as a well-read, knowledgeable friend who can engage in conversations, answer questions, and even help with tasks related to language, such as writing,
```

## Granite 3.2.2b with PyTorch
Code:
```
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
#quantization_config = BitsAndBytesConfig(load_in_4bit=True)
llm= "ibm-granite/granite-3.2-2b-instruct"
tokenizer = AutoTokenizer.from_pretrained(llm) 
model = AutoModelForCausalLM.from_pretrained( 
    llm, 
    device_map="auto", 
    dtype=torch.bfloat16, 
 #   quantization_config=quantization_config
) 
inputs = tokenizer("Explain IBM Granite 3.0 in simple terms", return_tensors="pt").to(model.device) 
outputs = model.generate(**inputs, max_length=100) 
print(tokenizer.decode(outputs[0], skip_special_tokens=True)) 
```

Output:
```
IBM Granite series, specifically Granite 3.0, are advanced AI models developed by IBM. These models excel in understanding natural language and handling complex tasks like translation, summarization, and question-answering. With Granite 3.0, IBM aims to provide highly accurate, reliable, and safe AI solutions, making it easier for businesses to integrate AI into their operations.
```

## vLLM Docker Image Compatibility with Granite 3 & 4
Run the Docker Container
```
docker run -d   --name vllm-ppc64le-container   -p 8000:8000   icr.io/ppc64le-oss/vllm-ppc64le:0.10.1.dev852.gee01645db.d20250827   --max-model-len 37440   --max-num-batched-tokens 37440
```
<br/>


**1. Granite 3 supported on Power VM via Docker image icr.io/ppc64le-oss/vllm-ppc64le:0.10.1.dev852.gee01645db.d20250827**
Granite 3 is supported on Power VM using the Docker image icr.io/ppc64le-oss/vllm-ppc64le:0.10.1.dev852.gee01645db.d20250827, while Granite 4 is not supported with the same image.

To download and serve a Granite 3 model, execute the following command inside the running container.
The example below uses the ibm-granite/granite-3.3-8b-instruct model:
```
python3 -m vllm.entrypoints.openai.api_server --model ibm-granite/granite-3.3-8b-instruct --max-model-len 13107   --max-num-batched-tokens 131072
```

- ibm-granite/granite-vision-3.3-2b
Execute:
```
curl -X POST http://localhost:8000/v1/chat/completions   -H "Content-Type: application/json"   -d '{
        "model": "ibm-granite/granite-3.3-8b-instruct",
        "messages": [
          {"role": "user", "content": "How are you today?"}
        ]
      }'

```
Output:
```
{"id":"chatcmpl-8876bd9b74fc442088c98c20ff514045","object":"chat.completion","created":1760424863,"model":"ibm-granite/granite-3.3-8b-instruct","choices":[{"index":0,"message":{"role":"assistant","content":"I'm an artificial intelligence and don't have feelings, but I'm here and ready to assist you. How can I help you today?","refusal":null,"annotations":null,"audio":null,"function_call":null,"tool_calls":[],"reasoning_content":null},"logprobs":null,"finish_reason":"stop","stop_reason":null,"token_ids":null}],"service_tier":null,"system_fingerprint":null,"usage":{"prompt_tokens":64,"total_tokens":96,"completion_tokens":32,"prompt_tokens_details":null},"prompt_logprobs":null,"prompt_token_ids":null,"kv_transfer_params":null}
```

- ibm-granite/granite-vision-3.3-2b
Execute:
```
curl -X POST http://localhost:8000/v1curl -X POST http://localhost:8000/v1/chat/completions   -H "Content-Type: application/json"   -d '{
        "model": "ibm-granite/granite-vision-3.3-2b",
        "messages": [
          {"role": "user", "content": "How are you today?"}
        ]
      }'
```

Output:
```
{"id":"chatcmpl-f30b2aaf0a30404b9b806deaf88ac1ef","object":"chat.completion","created":1760423098,"model":"ibm-granite/granite-vision-3.3-2b","choices":[{"index":0,"message":{"role":"assistant","content":"I'm an artificial intelligence and don't have feelings, but I'm here and ready to assist you. How can I help you today?","refusal":null,"annotations":null,"audio":null,"function_call":null,"tool_calls":[],"reasoning_content":null},"logprobs":null,"finish_reason":"stop","stop_reason":null,"token_ids":null}],"service_tier":null,"system_fingerprint":null,"usage":{"prompt_tokens":53,"total_tokens":85,"completion_tokens":32,"prompt_tokens_details":null},"prompt_logprobs":null,"prompt_token_ids":null,"kv_transfer_params":null}
```
<br/>

**2. Granite 4 is not supported on Power VM via Docker image icr.io/ppc64le-oss/vllm-ppc64le:0.10.1.dev852.gee01645db.d20250827**
Granite 4 models are currently incompatible with this setup. Any attempt to run them results in the following error:
```
ValueError: CPU backend only supports V1, which leads to a RuntimeError: Engine process failed to start.
```

## Integrated the vLLM Docker API into a Python Script
Set up the Docker container specifically for Granite 3 by running the following command:
```
docker run -d   --name vllm-ppc64le-container   -p 8000:8000   icr.io/ppc64le-oss/vllm-ppc64le:0.10.1.dev852.gee01645db.d20250827   --model ibm-granite/granite-3.3-8b-instruct --max-model-len 13107   --max-num-batched-tokens 131072
```

Python Code:
```
import requests
import json

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}
payload = {
    "model": "ibm-granite/granite-3.3-8b-instruct",
    "messages": [
        {"role": "user", "content": "How are you today?"}
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print("Status code:", response.status_code)
print("Response text:", response.text)
```

Output:
```
Status code: 200
Response text: {"id":"chatcmpl-9c757313e20546979af361a71356f196","object":"chat.completion","created":1760449631,"model":"ibm-granite/granite-3.3-8b-instruct","choices":[{"index":0,"message":{"role":"assistant","content":"I'm an artificial intelligence and don't have feelings, but I'm here and ready to assist you. How can I help you today?","refusal":null,"annotations":null,"audio":null,"function_call":null,"tool_calls":[],"reasoning_content":null},"logprobs":null,"finish_reason":"stop","stop_reason":null,"token_ids":null}],"service_tier":null,"system_fingerprint":null,"usage":{"prompt_tokens":64,"total_tokens":96,"completion_tokens":32,"prompt_tokens_details":null},"prompt_logprobs":null,"prompt_token_ids":null,"kv_transfer_params":null}

```

## Limitation and Challenges
CUDA (Compute Unified Device Architecture) is a technology by NVIDIA that allows software developers to use NVIDIA GPUs (graphics processing units). To verify whether PowerVM supports CUDA, run commands such as nvcc --version and nvidia-smi. If these commands return no output or indicate that CUDA is not installed, it confirms the absence of CUDA support on the system.

- Model Quantization Implementation in PyTorch
```
quantization_config = BitsAndBytesConfig(load_in_4bit=True)
```

This configuration helps system to load a smaller, lighter version of the model so it uses less memory and runs faster by storing its numbers in 4 bits instead of the usual 16 or 32 bits. This significantly reduces GPU memory usage. When quantization_config is enabled, the dtype parameter is either ignored or only partially applied. If quantization_config is removed, the model respects the specified dtype and loads accordingly.

The PowerVM environment allotted for evaluation does not support BitsAndBytes, as BitsAndBytes operates in CPU-only mode without CUDA capabilities. When dtype=torch.bfloat16 is specified, the CPU attempts to use the bfloat16 data type. However, if bfloat16 is not supported, PyTorch may silently fall back to float32 without raising any error.

## Conclusion
This validation confirms that both Granite 3.2.2b and Granite 4.0 are compatible with the Python and PyTorch ecosystem on PowerVM (CPU-only) environments. While Granite 3 runs successfully in both the PyTorch Python environment and the vLLM Docker setup, Granite 4.0 is only supported in the PyTorch Python environment and is currently incompatible with the vLLM Docker image provided for PowerVM.
