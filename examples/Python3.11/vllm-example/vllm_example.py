import wrapt
import subprocess
import os
import sys

# CPU-friendly env vars
os.environ['VLLM_USE_CUSTOM_OPS'] = '0'
os.environ['VLLM_CPU_KVCACHE_SPACE'] = '8'
os.environ['VLLM_WORKER_MULTIPROC_METHOD'] = 'spawn'
os.environ['OMP_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'
os.environ['OPENBLAS_NUM_THREADS'] = '4'
os.environ['VLLM_TARGET_DEVICE'] = 'cpu'

from vllm import LLM


def main():
    print("=== 1. Model Initialization Test ===")
    print("[INFO] Environment variables set:")
    print(f"  VLLM_USE_CUSTOM_OPS: {os.environ.get('VLLM_USE_CUSTOM_OPS')}")
    print(f"  VLLM_CPU_KVCACHE_SPACE: {os.environ.get('VLLM_CPU_KVCACHE_SPACE')} GiB")
    print(f"  VLLM_WORKER_MULTIPROC_METHOD: {os.environ.get('VLLM_WORKER_MULTIPROC_METHOD')}")
    print(f"  OMP_NUM_THREADS: {os.environ.get('OMP_NUM_THREADS')}")

    llm = None
    try:
        llm = LLM(
            model="ibm-granite/granite-3.1-2b-instruct",
            max_model_len=2048,          # matches batch tokens
            max_num_batched_tokens=2048, # must be >= max_model_len
            enforce_eager=True,
            dtype="float32",
            tensor_parallel_size=1,
            trust_remote_code=False,
            max_num_seqs=1,
        )
        print("[INFO] Model loaded successfully.")
    except Exception as e:
        print("[ERROR] Model loading failed:", e)
        import traceback; traceback.print_exc()
        sys.exit(1)

    try:
        # --- 2. Check Model Config / Supported Tasks ---
        print("\n=== 2. Check Model Config / Supported Tasks ===")
        try:
            config = llm.llm_engine.model_config
            print("Served model name:", getattr(config, "model", "(unknown)"))
            print("Max sequence length:", getattr(config, "max_model_len", "(unknown)"))
            print("Supported tasks:", getattr(config, "supported_tasks", "Not available"))
        except Exception as e:
            print("[ERROR] Could not access model config:", e)

        # --- 3. Wrap .generate() Without Calling It ---
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

        # --- 4. List Tokenizer Info ---
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

        # --- 5. Check Engine Type / Device / Mode ---
        print("\n=== 5. Check Engine Type / Device / Mode ===")
        try:
            eng = llm.llm_engine
            print("llm_engine type:", type(eng).__name__)

            # CHANGED: robust device config access (newer vLLM exposes via vllm_config)
            vcfg = getattr(eng, "vllm_config", None)
            if vcfg is not None and hasattr(vcfg, "device_config"):
                dcfg = vcfg.device_config
                # Try common attributes
                device_type = getattr(dcfg, "device_type", None) or getattr(dcfg, "device", None)
                print("Device config:", dcfg)
                if device_type:
                    print("Device type:", device_type)
            else:
                # Fallback (older or differing builds) – this may not exist
                dcfg = getattr(eng, "device_config", None)
                if dcfg is not None:
                    print("Device config (legacy):", dcfg)
                else:
                    print("Device config: (not exposed by this vLLM build)")
        except Exception as e:
            print("[ERROR] Could not access engine/device info:", e)

        # --- 6. Fail Gracefully on Bad Model Name ---
        print("\n=== 6. Fail Gracefully on Bad Model Name ===")
        print("\nNOTE: INTENTIONAL FAILING OF TEST")
        try:
            _ = LLM(model="nonexistent/model-id")
        except Exception as e:
            print("[ERROR] Model loading failed as expected:", e)

        # --- 7. Run `vllm --help` Command ---
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

    finally:
        # CHANGED: ensure engine shuts down cleanly; avoids “EngineCore_DP0 died” at exit
        try:
            if llm is not None and hasattr(llm, "llm_engine") and llm.llm_engine is not None:
                llm.llm_engine.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()   # Required on spawn mode with Python 3.12+
    main()