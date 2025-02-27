from PySide6.QtWidgets import QTextEdit


class DocView(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
