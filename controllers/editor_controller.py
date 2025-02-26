from PySide6.QtWidgets import QFileDialog
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

from models.document import Document
from views.editor_view import EditorView


class EditorController:
    def __init__(self, view: EditorView):
        self.view = view
        self.document = Document()

        # 连接信号
        self.view.open_file_triggered.connect(self.open_file)
        self.view.language_changed.connect(self.set_language)
        self.view.text_changed.connect(self.on_text_changed)
        self.view.cursor_position_changed.connect(self.print_cursor_position)

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )

        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.document.content = file.read()
                self.document.file_path = file_path

            self.view.cursor_position_changed.disconnect()
            self.document.set_language_from_extension()
            self.view.set_plain_text(self.document.content)
            self.set_language(self.document.language)
            self.view.cursor_position_changed.connect(self.print_cursor_position)

    def set_language(self, language):
        self.document.language = language
        self.view.update_language_menu(language)
        self.highlight_code()

    def highlight_code(self):
        if not self.document.language:
            return

        try:
            self.view.text_changed.disconnect()
            lexer = get_lexer_by_name(self.document.language, stripall=True)
            formatter = HtmlFormatter(
                style=get_style_by_name("colorful"),
                full=True,
                noclasses=True,
                linenos=False,
            )
            highlighted_code = highlight(self.document.content, lexer, formatter)
            self.view.set_editor_content(highlighted_code)
            self.view.text_changed.connect(self.on_text_changed)
        except Exception as e:
            print(f"Error highlighting code: {e}")
            self.view.set_plain_text(self.document.content)

    def on_text_changed(self, text):
        self.document.content = text
        self.highlight_code()

    def print_cursor_position(self):
        cursor = self.view.left_edit.textCursor()
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
