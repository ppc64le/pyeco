import wrapt
import subprocess
import os
import sys

# Set critical environment variables before importing vllm
os.environ['VLLM_USE_CUSTOM_OPS'] = '0'
os.environ['VLLM_CPU_KVCACHE_SPACE'] = '8'  # Increase from default 4 GiB to 8 GiB
os.environ['VLLM_WORKER_MULTIPROC_METHOD'] = 'spawn'  # Use spawn instead of fork
os.environ['OMP_NUM_THREADS'] = '4'  # Limit OpenMP threads to avoid oversubscription
os.environ['MKL_NUM_THREADS'] = '4'  # Limit MKL threads
os.environ['OPENBLAS_NUM_THREADS'] = '4'  # Limit OpenBLAS threads

from vllm import LLM

print("=== 1. Model Initialization Test ===")
print("[INFO] Environment variables set:")
print(f"  VLLM_USE_CUSTOM_OPS: {os.environ.get('VLLM_USE_CUSTOM_OPS')}")
print(f"  VLLM_CPU_KVCACHE_SPACE: {os.environ.get('VLLM_CPU_KVCACHE_SPACE')} GiB")
print(f"  VLLM_WORKER_MULTIPROC_METHOD: {os.environ.get('VLLM_WORKER_MULTIPROC_METHOD')}")
print(f"  OMP_NUM_THREADS: {os.environ.get('OMP_NUM_THREADS')}")

try:
    # Initialize with CPU-specific settings
    llm = LLM(
        model="ibm-granite/granite-3.1-2b-instruct",
        max_model_len=4096,
        enforce_eager=True,  # Disable CUDA graphs (CPU doesn't support them)
        dtype="float32",  # Use float32 for CPU (more stable than bfloat16)
        tensor_parallel_size=1,  # Single process for CPU
        gpu_memory_utilization=0.0,  # Not using GPU
        trust_remote_code=False,
        max_num_seqs=1,  # Reduce concurrent sequences for CPU
        max_num_batched_tokens=2048,  # Reduce batch size for CPU
    )
    print("[INFO] Model loaded successfully.")
except Exception as e:
    print("[ERROR] Model loading failed:", e)
    import traceback
    traceback.print_exc()
    sys.exit(1)

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
