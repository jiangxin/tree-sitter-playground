from PySide6.QtWidgets import QTextEdit


class AstView(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(True)
        self.setFontFamily("Courier New")  # Set monospace font
        self.setLineWrapMode(QTextEdit.NoWrap)
        # Enable auto background fill
        self.setAutoFillBackground(True)
