from PySide6.QtWidgets import QTextEdit


class AstView(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setFontFamily("Courier New")  # 设置等宽字体
        self.setLineWrapMode(QTextEdit.NoWrap)
        # 启用自动填充背景
        self.setAutoFillBackground(True)
