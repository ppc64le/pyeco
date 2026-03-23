# sub-test2.py
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
    print("=== sub-test2: function definition ===\n")

    code = b"""
def add(a, b):
    return a + b
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

    # Extract function name, params, body
    func_node = None
    for n in traverse_tree(tree):
        if n.type == "function_definition":
            func_node = n
            break

    assert func_node is not None

    name_node = func_node.child_by_field_name("name")
    params_node = func_node.child_by_field_name("parameters")
    body_node = func_node.child_by_field_name("body")

    # Presence checks (silent if violated)
    assert name_node is not None
    assert params_node is not None
    assert body_node is not None

    # Inside body: return statement with binary op
    return_stmt = None
    if body_node:
        for ch in body_node.children:
            if ch.type == "return_statement":
                return_stmt = ch
                break

    assert return_stmt is not None
    assert "binary_operator" in [c.type for c in return_stmt.children] or "binary_operator" in node_types

    # Printed test results (no pass/fail wording)
    print("Test results:")
    print("  function_definition present:", func_node is not None)
    print("  function name:", node_text(name_node, code) if name_node else None)
    print("  parameters text:", node_text(params_node, code) if params_node else None)
    print("  return_statement present:", return_stmt is not None)
    print("  binary_operator present:", "binary_operator" in node_types)


if __name__ == "__main__":
    main()
