# sub-test3.py
from typing import Generator
from tree_sitter import Language, Parser, Tree, Node
import tree_sitter_python
import textwrap

def traverse_tree(tree: Tree) -> Generator[Node, None, None]:
    cursor = tree.walk()
    visited_children = False
    while True:
        if not visited_children:
            yield cursor.node
            if not cursor.goto_first_child():
                visited_children = True
        elif cursor.goto_next_sibling():
            visited_children = False
        elif not cursor.goto_parent():
            break

def node_text(node: Node, src: bytes) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8")

def main():
    print("=== sub-test3: imports + class + method ===\n")

    code = b"""
import os
from pathlib import Path

class Greeter:
    def greet(self):
        return "hello"
"""
    print("Source:")
    print(textwrap.indent(code.decode("utf-8").rstrip("\n"), "  "))
    print()

    parser = Parser()
    parser.language = Language(tree_sitter_python.language())
    tree = parser.parse(code)
    root = tree.root_node

    node_types = [node.type for node in traverse_tree(tree)]
    print("Node types (preorder):")
    print(" ", node_types)
    print()

    # Collect imports, class name, methods
    imports = set()
    class_name = None
    methods = []

    for n in traverse_tree(tree):
        if n.type == "import_statement":
            for c in n.children:
                if c.type == "dotted_name":
                    imports.add(node_text(c, code))
        elif n.type == "import_from_statement":
            for c in n.children:
                if c.type == "dotted_name":
                    imports.add(node_text(c, code))
        elif n.type == "class_definition":
            name_node = n.child_by_field_name("name")
            if name_node:
                class_name = node_text(name_node, code)
            body = n.child_by_field_name("body")
            if body:
                for ch in body.children:
                    if ch.type == "function_definition":
                        mn = ch.child_by_field_name("name")
                        if mn:
                            methods.append(node_text(mn, code))

    # Expectations (silent assertions)
    assert "import_statement" in node_types
    assert "class_definition" in node_types
    assert "function_definition" in node_types
    assert "string" in node_types
    assert "os" in imports
    assert any("pathlib" in m for m in imports)
    assert class_name == "Greeter"
    assert "greet" in methods

    # Printed test results (no pass/fail wording)
    print("Test results:")
    print("  imports:", sorted(imports))
    print("  class name:", class_name)
    print("  methods:", methods)
    print("  import_statement present:", "import_statement" in node_types)
    print("  import_from_statement present:", "import_from_statement" in node_types)
    print("  class_definition present:", "class_definition" in node_types)
    print("  function_definition present:", "function_definition" in node_types)
    print("  string literal present:", "string" in node_types)


if __name__ == "__main__":
    main()
