# main_example.py
from typing import Generator
from tree_sitter import Language, Parser, Tree, Node
import tree_sitter_python
import textwrap

PY_LANGUAGE = Language(tree_sitter_python.language())

parser = Parser()
parser.language = PY_LANGUAGE

tree = parser.parse(b"a = 1")


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
    print("=== main_example: simple assignment ===\n")

    code = "a = 1"
    print("Source:")
    print(textwrap.indent(code, "  "))
    print()

    node_types = [node.type for node in traverse_tree(tree)]
    print("Node types (preorder):")
    print(" ", node_types)
    print()

    # Expectations (silent if correct)
    expected = [
        "module",
        "expression_statement",
        "assignment",
        "identifier",
        "=",
        "integer",
    ]
    assert node_types == expected

    # Printed test results (no pass/fail wording)
    print("Test results:")
    print("  Expected node order matched:", node_types == expected)


if __name__ == "__main__":
    main()
