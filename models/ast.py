import importlib
from typing import List, Optional

from tree_sitter import Language, Parser, Tree


class AST:
    def __init__(self):
        self.content: Optional[bytes] = None
        self.language: Optional[Language] = None
        self.parser: Optional[Parser] = Parser()
        self.tree: Optional[Tree] = None
        self.line_range = {}  # Add line_range field

    def get_language(self, language_name: str) -> Optional[Language]:
        if language_name == "c_sharp":
            language_name = "csharp"
        for module_name in [
            "tree_sitter_language_pack",
            "tree_sitter_languages",
            f"tree_sitter_{language_name}",
        ]:
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue
            if not module:
                continue
            if hasattr(module, "get_language"):
                return module.get_language(language_name)
            elif hasattr(module, "language"):
                language = module.language()
                if isinstance(language, Language):
                    return language
                else:
                    return Language(language)
            return None

    def load(self, language_name: str, content):
        self.content = (
            content.encode("utf8", errors="replace")
            if isinstance(content, str)
            else content
        )
        self.language = self.get_language(language_name)
        if not self.language:
            raise Exception(
                f"cannot find tree-sitter driver for language '{language_name}'"
            )
        self.parser = Parser()
        # For backward compatibility, use deprecated "set_language" for old version of tree-sitter
        if hasattr(self.parser, "set_language"):
            self.parser.set_language(self.language)
        else:
            # New version of tree-sitter use language attribute.
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
        self.line_range = {}  # 初始化 line_range 字典

        while stack:
            node, depth, index = stack.pop()
            start_point = node.start_point
            end_point = node.end_point
            node_type = node.type
            field_name = (
                node.parent.field_name_for_child(index) if node.parent else None
            )

            # 存储 start_point 和 end_point 到 line_range
            line_number = len(lines)
            self.line_range[line_number] = [
                start_point[0],
                start_point[1],
                end_point[0],
                end_point[1],
            ]

            lines.append(
                "{}{}{}{} [{}, {}] - [{}, {}]".format(
                    "  " * depth,
                    f"{field_name}: " if field_name else "",
                    "" if node.is_named else "[anonymous] ",
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

    def get_match_ast_line(self, line: int, column: int) -> Optional[int]:
        """Find the closest line_range index for the given line and column."""
        min_row_distance = -1
        min_col_distance = -1
        closest_index = None

        for index, (
            start_line,
            start_col,
            end_line,
            end_col,
        ) in self.line_range.items():
            if line < start_line or line > end_line:
                continue
            if line == start_line and column < start_col:
                continue
            if line == end_line and column > end_col:
                continue

            row_distance = abs(end_line - start_line)
            if min_row_distance < 0 or row_distance < min_row_distance:
                min_row_distance = row_distance
                closest_index = index
                continue
            elif row_distance > min_row_distance:
                continue

            col_distance = abs(end_col - start_col)
            if min_col_distance < 0 or col_distance < min_col_distance:
                min_col_distance = col_distance
                closest_index = index
                continue
            elif col_distance > min_col_distance:
                continue

        return closest_index

    def get_code_range(self, line_number: int) -> List[int]:
        """Return the start and end line and column numbers for the given line number."""
        return self.line_range.get(line_number, [-1, -1, -1, -1])
