# packages: nbformat, nbconvert, ipykernel, jupyter-core, matplotlib, numpy
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import numpy as np
import os

# Build a notebook in memory
nb = nbf.v4.new_notebook()
nb.cells = [
    nbf.v4.new_markdown_cell("# Auto Notebook\nThis was generated and executed programmatically."),
    nbf.v4.new_code_cell(
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "x = np.linspace(0, 6.28, 300)\n"
        "y = np.sin(x)\n"
        "plt.plot(x, y)\n"
        "plt.title('Sine')\n"
        "plt.savefig('nb_plot.png', dpi=120)\n"
        "print('sum(y)=', y.sum())"
    )
]

# Execute with ipykernel
ep = ExecutePreprocessor(timeout=120, kernel_name="python3")
ep.preprocess(nb, {})

# Save .ipynb
with open("auto_notebook.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

# Export to HTML 
exporter = HTMLExporter(template_name='basic')
(body, resources) = exporter.from_notebook_node(nb)
with open("auto_notebook.html", "w", encoding="utf-8") as f:
    f.write(body)

print("Saved -> auto_notebook.ipynb, auto_notebook.html, nb_plot.png")
