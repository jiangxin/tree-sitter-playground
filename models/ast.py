from tree_sitter import Language, Parser, Tree
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

        def traverse(node, parent=None):
            start_point = node.start_point
            end_point = node.end_point
            node_type = node.type
            node_name = node.text.decode("utf8", errors="replace") if node.text else ""
            lines.append(
                f"Type: {node_type}, Name: {node_name}, "
                f"Start Line: {start_point[0] + 1}, Start Column: {start_point[1]}, "
                f"End Line: {end_point[0] + 1}, End Column: {end_point[1]}"
            )
            for child in node.children:
                traverse(child, node)

        traverse(self.tree.root_node)
        return "\n".join(lines)
