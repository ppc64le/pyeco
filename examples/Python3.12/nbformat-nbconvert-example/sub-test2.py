import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

print("Running subtest_ipykernel.py...")

# Create a notebook with actual computation
nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_code_cell("a = 10\nb = 5\na * b"),
    nbformat.v4.new_code_cell("print(f'Result: {a * b}')")
]

ep = ExecutePreprocessor(timeout=30, kernel_name="python3")

# Execute
try:
    ep.preprocess(nb, {})
    print("ipykernel test passed. Notebook executed successfully.")
    
    # Print outputs
    for i, cell in enumerate(nb.cells):
        if "outputs" in cell:
            for output in cell.outputs:
                if hasattr(output, 'text'):
                    print(f"Cell {i} output: {output.text.strip()}")
except Exception as e:
    print("ipykernel test failed:", e)
    raise
