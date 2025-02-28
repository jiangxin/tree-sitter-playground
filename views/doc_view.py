from PySide6.QtWidgets import QTextEdit


class DocView(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(True)
        self.setLineWrapMode(QTextEdit.NoWrap)

    def setHtml(self, html):
        # 保存当前光标位置
        self._cursor_position = self.textCursor().position()

        # 设置 HTML
        super().setHtml(html)

        # 恢复光标位置
        cursor = self.textCursor()
        # 确保位置不超过文本长度
        position = min(self._cursor_position, len(self.toPlainText()))
        cursor.setPosition(position)
        self.setTextCursor(cursor)
