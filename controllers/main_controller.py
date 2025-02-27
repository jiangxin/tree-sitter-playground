from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)
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
        self.window.ast_edit_cursor_event.connect(self.on_ast_edit_cursor_changed)
        self.window.doc_edit.textChanged.connect(
            lambda: self.window.text_changed_event.emit(
                self.window.doc_edit.toPlainText()
            )
        )
        self.window.doc_edit.cursorPositionChanged.connect(
            self.window.doc_edit_cursor_event.emit
        )
        self.window.ast_edit.cursorPositionChanged.connect(
            self.window.ast_edit_cursor_event.emit
        )
        self.window.font_size_changed_event.connect(self.update_font_size)

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )
        if not file_path:
            return
        self.document.file_path = file_path
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.document.content = file.read()
        except Exception as e:
            QMessageBox.critical(self.window, "ERROR", f"Fail to open file: {e}")
            return
        try:
            self.window.doc_edit.blockSignals(True)
            self.document.set_language_from_extension()
            self.window.doc_edit.setPlainText(self.document.content)
            self.window.doc_edit.blockSignals(False)
            self.set_language(self.document.language)
            self.ast_edit_load(self.document.language, self.document.content)
        except Exception as e:
            QMessageBox.critical(self.window, "ERROR", f"Error highlighting code: {e}")

    def set_language(self, language):
        self.document.language = language
        self.window.update_language_menu(language)
        self.highlight_code()
        self.ast_edit_load(self.document.language, self.document.content)

    def highlight_code(self):
        if not self.document.language:
            return

        try:
            self.window.doc_edit.blockSignals(True)
            language = self.document.language
            if language == "c_sharp":
                language = "csharp"
            lexer = get_lexer_by_name(language, stripall=True)
            formatter = HtmlFormatter(
                style=get_style_by_name("colorful"),
                full=True,
                noclasses=True,
                linenos=False,
            )
            highlighted_code = highlight(self.document.content, lexer, formatter)
            self.window.doc_edit.setHtml(highlighted_code)
        finally:
            self.window.doc_edit.blockSignals(False)

    def on_text_changed(self, text):
        self.document.content = text
        self.highlight_code()
        self.ast_edit_load(self.document.language, self.document.content)

    def ast_edit_load(self, language, content):
        self.ast.load(language, content)
        ast_text = self.ast.get_plain_text()
        self.window.ast_edit.blockSignals(True)
        self.window.ast_edit.setPlainText(ast_text)
        self.window.ast_edit.blockSignals(False)

    def highlight_ast_region(self):
        self.window.ast_edit.blockSignals(True)
        cursor = self.window.doc_edit.textCursor()
        if cursor.hasSelection():
            cursor.setPosition(cursor.selectionEnd())
            line_number = cursor.blockNumber()
            column_number = cursor.columnNumber()
        else:
            line_number = cursor.blockNumber()
            column_number = cursor.columnNumber()
        match_index = self.ast.get_match_ast_line(line_number, column_number)

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
        self.window.ast_edit.blockSignals(False)

    def update_font_size(self, size):
        self.window.set_font_size(size)

    def on_ast_edit_cursor_changed(self):
        cursor = self.window.ast_edit.textCursor()
        line_number = cursor.blockNumber()
        start_line, start_column, end_line, end_column = self.ast.get_code_range(
            line_number
        )
        if start_line < 0:
            return

        self.window.doc_edit.blockSignals(True)
        doc_edit = self.window.doc_edit
        doc_edit_cursor = doc_edit.textCursor()

        # 获取文本块并转换为 bytes 以计算正确的长度
        block = doc_edit.document().findBlockByLineNumber(start_line)
        block_bytes = bytes(block.text(), "utf-8", errors="replace")
        start_position = block.position() + len(
            block_bytes[:start_column].decode("utf-8", errors="replace")
        )

        # 修改: 从 end_line 获取文本块以计算 end_position
        end_block = doc_edit.document().findBlockByLineNumber(end_line)
        end_block_bytes = bytes(end_block.text(), "utf-8", errors="replace")
        end_position = end_block.position() + len(
            end_block_bytes[:end_column].decode("utf-8", errors="replace")
        )

        doc_edit_cursor.setPosition(start_position)
        doc_edit_cursor.setPosition(end_position, QTextCursor.KeepAnchor)
        doc_edit.setTextCursor(doc_edit_cursor)
        doc_edit.ensureCursorVisible()
        self.window.doc_edit.blockSignals(False)
