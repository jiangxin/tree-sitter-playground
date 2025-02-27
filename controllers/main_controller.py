from PySide6.QtWidgets import QFileDialog
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from PySide6.QtGui import QTextCursor

from models.ast import AST  # 添加导入语句
from models.document import Document
from views.main_window import MainWindow


class MainController:
    def __init__(self, window: MainWindow):
        self.window = window
        self.document = Document()
        self.ast = AST()  # 初始化 AST 对象

        # 连接信号
        self.window.open_file_event.connect(self.open_file)
        self.window.language_changed_event.connect(self.set_language)
        self.window.text_changed_event.connect(self.on_text_changed)
        self.window.doc_edit_cursor_event.connect(self.highlight_ast_region)
        self.window.doc_edit.textChanged.connect(
            lambda: self.window.text_changed_event.emit(
                self.window.doc_edit.toPlainText()
            )
        )
        self.window.doc_edit.cursorPositionChanged.connect(
            self.window.doc_edit_cursor_event.emit
        )

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )

        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.document.content = file.read()
                self.document.file_path = file_path

            self.window.doc_edit_cursor_event.disconnect()
            self.document.set_language_from_extension()
            self.window.doc_edit.setPlainText(self.document.content)
            self.set_language(self.document.language)
            self.window.doc_edit_cursor_event.connect(self.highlight_ast_region)

    def set_language(self, language):
        self.document.language = language
        self.window.update_language_menu(language)
        self.highlight_code()
        self.ast_edit_load(self.document.language, self.document.content)

    def highlight_code(self):
        if not self.document.language:
            return

        try:
            self.window.text_changed_event.disconnect()
            lexer = get_lexer_by_name(self.document.language, stripall=True)
            formatter = HtmlFormatter(
                style=get_style_by_name("colorful"),
                full=True,
                noclasses=True,
                linenos=False,
            )
            highlighted_code = highlight(self.document.content, lexer, formatter)
            self.window.doc_edit.setHtml(highlighted_code)
            self.window.text_changed_event.connect(self.on_text_changed)
        except Exception as e:
            print(f"Error highlighting code: {e}")
            self.window.doc_edit.setPlainText(self.document.content)

    def on_text_changed(self, text):
        self.document.content = text
        self.highlight_code()

        # 新增代码：解析 AST 并显示在 ast_edit 中
        self.ast.load(self.document.language, text)
        ast_text = self.ast.get_plain_text()
        self.window.ast_edit.setPlainText(ast_text)

    def highlight_ast_region(self):
        cursor = self.window.doc_edit.textCursor()
        if cursor.hasSelection():
            end = cursor.selectionEnd()
            cursor.setPosition(end)
            line_number = cursor.blockNumber()
            column_number = cursor.columnNumber()
        else:
            line_number = cursor.blockNumber()
            column_number = cursor.columnNumber()
        match_index = self.ast.get_match_ast_line(line_number, column_number)
        print(
            f"Code line: {line_number}, column: {column_number}, Matched AST index: {match_index}"
        )

        # 新增代码：在 ast_edit 中选中对应的行
        if match_index is not None:
            ast_edit = self.window.ast_edit
            ast_edit_lines = ast_edit.toPlainText().split("\n")
            if 0 <= match_index < len(ast_edit_lines):
                ast_edit_cursor = ast_edit.textCursor()
                ast_edit_cursor.movePosition(QTextCursor.Start)
                for _ in range(match_index):
                    ast_edit_cursor.movePosition(QTextCursor.NextBlock)
                ast_edit_cursor.movePosition(QTextCursor.StartOfLine)
                ast_edit_cursor.movePosition(
                    QTextCursor.EndOfLine, QTextCursor.KeepAnchor
                )
                ast_edit.setTextCursor(ast_edit_cursor)
                ast_edit.ensureCursorVisible()
