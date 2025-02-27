from tree_sitter import (
    Language,
    Parser,
    Tree,
)
import tree_sitter_language_pack
from typing import Optional, List


class AST:
    def __init__(self):
        self.content: Optional[bytes] = None
        self.language: Optional[Language] = None
        self.parser: Optional[Parser] = Parser()
        self.tree: Optional[Tree] = None

    def load(self, language_name: str, content):
        self.content = (
            content.encode("utf8", errors="replace")
            if isinstance(content, str)
            else content
        )
        if language_name == "c_sharp":
            language_name = "csharp"
        self.language = tree_sitter_language_pack.get_language(language_name)
        self.parser = Parser()
        self.parser.language = self.language
        data = (
            content.encode("utf8", errors="replace")
            if isinstance(content, str)
            else content
        )
        self.tree = self.parser.parse(data)

    def get_plain_text(self) -> str:
        if not self.tree:
            return ""

        lines: List[str] = []
        stack = [(self.tree.root_node, 0, 0)]  # (node, depth, id)

        while stack:
            node, depth, index = stack.pop()
            start_point = node.start_point
            end_point = node.end_point
            node_type = node.type
            field_name = (
                node.parent.field_name_for_child(index) if node.parent else None
            )

            lines.append(
                "{}{}{}{} [{}, {}] - [{}, {}]".format(
                    "  " * depth,
                    f"{field_name}: " if field_name else "",
                    "" if node.is_named else ". ",
                    node_type,
                    start_point[0] + 1,
                    start_point[1],
                    end_point[0] + 1,
                    end_point[1],
                )
            )

            # Add children to the stack with incremented depth and original index
            for id, child in enumerate(reversed(node.children)):
                original_id = len(node.children) - 1 - id
                stack.append((child, depth + 1, original_id))

        return "\n".join(lines)
