import nbformat as nbf

print("Running subtest_nbformat.py...")

# Create notebook
nb = nbf.v4.new_notebook()
nb.cells = [
    nbf.v4.new_markdown_cell("## Test Notebook"),
    nbf.v4.new_code_cell("x = 2\ny = 3\nx + y"),
]

# Save it
filename = "nbformat_test.ipynb"
with open(filename, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

# Reload and inspect
with open(filename, "r", encoding="utf-8") as f:
    loaded = nbf.read(f, as_version=4)

assert len(loaded.cells) == 2
print(f"nbformat test passed. Created notebook with {len(loaded.cells)} cells.")
print(f"Saved as: {filename}")
