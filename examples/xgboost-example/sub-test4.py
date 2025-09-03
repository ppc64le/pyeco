from roman import fromRoman
from sphinx.application import Sphinx
import os
import shutil

print("✅ Sub-test 4: Roman numerals + Sphinx")

# Roman numeral conversion
values = [10, 20, 30]
roman_values = [fromRoman("X")+fromRoman("V") for v in values]
print("Roman values:", roman_values)

# Minimal Sphinx project
docs_dir = "sphinx_sub_test_docs"
os.makedirs(docs_dir, exist_ok=True)
with open(os.path.join(docs_dir, "conf.py"), "w") as f:
    f.write("project='SubTestProject'\nmaster_doc='index'\n")
with open(os.path.join(docs_dir, "index.rst"), "w") as f:
    f.write("SubTestProject\n===============\nDocumentation for sub-test\n")
out_dir = os.path.join(docs_dir, "_build")
doctree_dir = os.path.join(docs_dir, "_doctrees")
app = Sphinx(docs_dir, docs_dir, out_dir, doctree_dir, buildername="html")
app.build()
print("Sphinx HTML build successful ->", out_dir)

shutil.rmtree(docs_dir)

