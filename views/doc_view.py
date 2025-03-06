from PySide6.QtWidgets import QTextEdit


class DocView(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        # 启用自动填充背景
        self.setAutoFillBackground(True)

    def setHtml(self, html):
        # Save current cursor position
        self._cursor_position = self.textCursor().position()

        # Set HTML
        super().setHtml(html)

        # Restore cursor position
        cursor = self.textCursor()
        # Ensure position doesn't exceed text length
        position = min(self._cursor_position, len(self.toPlainText()))
        cursor.setPosition(position)
        self.setTextCursor(cursor)
