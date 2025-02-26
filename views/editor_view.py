from PySide6.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal


class EditorView(QMainWindow):
    # 定义信号
    open_file_triggered = Signal()
    language_changed = Signal(str)
    text_changed = Signal(str)
    cursor_position_changed = Signal()

    def __init__(self):
        super().__init__()
        self.supported_languages = ["c/c++", "python", "java"]
        self.selected_language_action = None
        self.language_menu_title = None

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Tree-sitter Playground")
        self.resize(800, 600)

        self.create_menus()
        self.create_editors()

    def create_menus(self):
        menubar = self.menuBar()

        # File 菜单
        file_menu = menubar.addMenu("&File")
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_triggered.emit)
        file_menu.addAction(open_action)

        # Language 菜单
        language_menu = menubar.addMenu("&Language")
        self.language_menu_title = language_menu.menuAction()
        for language in self.supported_languages:
            action = QAction(language, self, checkable=True)
            action.triggered.connect(
                lambda checked, lang=language: self.language_changed.emit(lang)
            )
            language_menu.addAction(action)

        # View 和 Help 菜单
        menubar.addMenu("&View")
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(QAction("&About", self))

    def create_editors(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        self.left_edit = QTextEdit()
        self.right_edit = QTextEdit()

        self.left_edit.setAcceptRichText(True)
        self.left_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.left_edit.textChanged.connect(
            lambda: self.text_changed.emit(self.left_edit.toPlainText())
        )
        self.left_edit.cursorPositionChanged.connect(self.cursor_position_changed.emit)

        layout.addWidget(self.left_edit)
        layout.addWidget(self.right_edit)

    def update_language_menu(self, language):
        if self.selected_language_action:
            self.selected_language_action.setChecked(False)

        for action in self.menuBar().actions():
            if action.text().startswith("&Language"):
                for sub_action in action.menu().actions():
                    if sub_action.text() == language:
                        sub_action.setChecked(True)
                        self.selected_language_action = sub_action
                        break

        self.language_menu_title.setText(f"&Language: {language}")

    def set_editor_content(self, html_content):
        self.left_edit.setHtml(html_content)

    def set_plain_text(self, text):
        self.left_edit.setPlainText(text)
