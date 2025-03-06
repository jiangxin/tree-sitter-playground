from models.ast import AST


class MockNode:
    def __init__(self, type, start_point, end_point, children=None, is_named=True):
        self.type = type
        self.start_point = start_point
        self.end_point = end_point
        self.children = children or []
        self.is_named = is_named
        self.parent = None
        for child in self.children:
            child.parent = self

    def field_name_for_child(self, index):
        return None


class MockTree:
    def __init__(self, root_node):
        self.root_node = root_node


def test_ast_initialization():
    ast = AST()
    assert ast.content is None
    assert ast.language is None
    assert ast.parser is not None
    assert ast.tree is None
    assert ast.line_range == {}


def test_get_plain_text():
    ast = AST()
    # Create a mock tree structure
    root = MockNode(
        "module",
        (0, 0),
        (2, 0),
        [
            MockNode(
                "function",
                (0, 0),
                (1, 10),
                [
                    MockNode("identifier", (0, 4), (0, 7)),
                    MockNode("parameters", (0, 7), (0, 9), [], False),
                ],
            ),
            MockNode("variable", (1, 0), (1, 5)),
        ],
    )
    ast.tree = MockTree(root)

    text = ast.get_plain_text()
    lines = text.split("\n")

    assert len(lines) == 5
    assert "module" in lines[0]
    assert "function" in lines[1]
    assert "variable" in lines[4]


def test_get_match_ast_line():
    ast = AST()
    ast.line_range = {
        100: [12, 0, 28, 21],  # Function
        101: [12, 0, 12, 3],  # def
        102: [12, 4, 12, 8],  # name
        105: [13, 4, 28, 21],  # body
        106: [13, 4, 13, 32],  # expression
        108: [15, 4, 15, 29],  # comment
        120: [28, 4, 28, 21],  # return statement
        121: [28, 4, 28, 10],  # return
    }

    # Test exact match
    assert ast.get_match_ast_line(12, 0) == 101
    assert ast.get_match_ast_line(12, 3) == 101
    assert ast.get_match_ast_line(12, 5) == 102
    assert ast.get_match_ast_line(12, 7) == 102
    assert ast.get_match_ast_line(12, 404) == 100
    assert ast.get_match_ast_line(28, 7) == 121

    # Test no match
    assert ast.get_match_ast_line(300, 0) is None


def test_get_code_range():
    ast = AST()
    ast.line_range = {
        100: [12, 0, 28, 21],  # Function
        101: [12, 0, 12, 3],  # def
        102: [12, 4, 12, 8],  # name
        105: [13, 4, 28, 21],  # body
        106: [13, 4, 13, 32],  # expression
        108: [15, 4, 15, 29],  # comment
        120: [28, 4, 28, 21],  # return statement
        121: [28, 4, 28, 10],  # return
    }

    # Test existing line
    assert ast.get_code_range(100) == [12, 0, 28, 21]
    assert ast.get_code_range(101) == [12, 0, 12, 3]
    assert ast.get_code_range(102) == [12, 4, 12, 8]
    assert ast.get_code_range(105) == [13, 4, 28, 21]

    # Test non-existing line
    assert ast.get_code_range(999) == [-1, -1, -1, -1]
