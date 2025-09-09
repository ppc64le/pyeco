import wrapt
import subprocess
from vllm import LLM

print("=== 1. Model Initialization Test ===")
try:
    llm = LLM(model="ibm-granite/granite-3.1-2b-instruct",
              max_model_len = 4096)
    print("[INFO] Model loaded successfully.")
except Exception as e:
    print("[ERROR] Model loading failed:", e)

print("\n=== 2. Check Model Config / Supported Tasks ===")
try:
    config = llm.llm_engine.model_config
    print("Served model name:", config.model)
    print("Max sequence length:", config.max_model_len)  
    print("Supported tasks:", getattr(config, 'supported_tasks', 'Not available')) 
except Exception as e:
    print("[ERROR] Could not access model config:", e)


print("\n=== 3. Wrap .generate() Without Calling It ===")
@wrapt.decorator
def log_generate_call(wrapped, instance, args, kwargs):
    print(f"[WRAP] Would run: {wrapped.__name__} (generation skipped)")
    return None

try:
    llm.generate = log_generate_call(llm.generate)
    print("[INFO] generate() method wrapped with no execution.")
except Exception as e:
    print("[ERROR] Failed to wrap generate():", e)

print("\n=== 4. List Tokenizer Info ===")
try:
    tokenizer = llm.llm_engine.tokenizer
    print("Tokenizer class:", tokenizer.__class__.__name__)
    if hasattr(tokenizer, "tokenizer") and hasattr(tokenizer.tokenizer, "vocab_size"):
        print("Vocab size:", tokenizer.tokenizer.vocab_size)
    else:
        print("Vocab size: (not accessible)")
except Exception as e:
    print("[ERROR] Could not access tokenizer info:", e)

print("\n=== 5. Check Engine Type / Device / Mode ===")
try:
    print("llm_engine type:", type(llm.llm_engine).__name__)
    print("Device config:", llm.llm_engine.device_config)
except Exception as e:
    print("[ERROR] Could not access engine/device info:", e)

print("\n=== 6. Fail Gracefully on Bad Model Name ===")
print("\nNOTE: INTENTIONAL FAILING OF TEST")
try:
    bad_llm = LLM(model="nonexistent/model-id")
except Exception as e:
    print("[ERROR] Model loading failed as expected:", e)

print("\n=== 7. Run `vllm --help` Command ===")
try:
    result = subprocess.run(["vllm", "--help"], capture_output=True, text=True, check=True)
    print(result.stdout)
except FileNotFoundError:
    print("[ERROR] `vllm` CLI tool not found. Make sure it is installed and in your PATH.")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] `vllm --help` failed with exit code {e.returncode}")
    print(e.output)

print("\n=== Script Complete ===")
