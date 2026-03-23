# sub-test1.py
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


def main():
    print("=== sub-test1: assignment + binary expression ===\n")

    code = b"""
x = 1
x = x + 2
"""
    print("Source:")
    print(textwrap.indent(code.decode("utf-8").rstrip("\n"), "  "))
    print()

    parser = Parser()
    parser.language = Language(tree_sitter_python.language())
    tree = parser.parse(code)

    node_types = [node.type for node in traverse_tree(tree)]
    print("Node types (preorder):")
    print(" ", node_types)
    print()

    # Checks (silent errors if violated)
    assert "assignment" in node_types
    assert node_types.count("assignment") == 2
    assert "binary_operator" in node_types

    # Printed test results (no pass/fail wording)
    print("Test results:")
    print("  assignment present:", "assignment" in node_types)
    print("  assignment count:", node_types.count("assignment"))
    print("  binary_operator present:", "binary_operator" in node_types)


if __name__ == "__main__":
    main()
