import nbformat
from nbconvert import HTMLExporter

print("Running subtest_nbconvert.py...")

# Create a simple notebook
nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_markdown_cell("# Hello"),
    nbformat.v4.new_code_cell("print('Export test')"),
]

# Use the 'basic' template (safe but minimal)
exporter = HTMLExporter(template_name='basic')
html, _ = exporter.from_notebook_node(nb)

filename = "nbconvert_test.html"
with open(filename, "w", encoding="utf-8") as f:
    f.write(html)

#Instead of checking for <html>, check for known content
assert "Export test" in html or "Hello" in html

print(f"nbconvert test passed. Exported to {filename}")
print(f"Snippet of output:\n{html[:100].strip()}")
