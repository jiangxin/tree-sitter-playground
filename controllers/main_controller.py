from PySide6.QtWidgets import QFileDialog
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

from models.document import Document
from views.main_window import MainWindow


class MainController:
    def __init__(self, window: MainWindow):
        self.window = window
        self.document = Document()

        # 连接信号
        self.window.open_file_event.connect(self.open_file)
        self.window.language_changed_event.connect(self.set_language)
        self.window.text_changed_event.connect(self.on_text_changed)
        self.window.doc_edit_cursor_event.connect(self.print_cursor_position)
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
            self.window.doc_edit_cursor_event.connect(self.print_cursor_position)

    def set_language(self, language):
        self.document.language = language
        self.window.update_language_menu(language)
        self.highlight_code()

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

    def print_cursor_position(self):
        cursor = self.window.doc_edit.textCursor()
        if cursor.hasSelection():
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            cursor.setPosition(start)
            start_line = cursor.blockNumber() + 1
            start_column = cursor.columnNumber()
            cursor.setPosition(end)
            end_line = cursor.blockNumber() + 1
            end_column = cursor.columnNumber()
            print(
                f"Selected text from line {start_line}, column {start_column} "
                f"to line {end_line}, column {end_column}"
            )
        else:
            line_number = cursor.blockNumber() + 1
            print(f"Cursor is on line: {line_number}")
