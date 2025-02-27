from PySide6.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal
from .doc_view import DocView


class MainWindow(QMainWindow):
    # 定义信号
    open_file_event = Signal()
    language_changed_event = Signal(str)
    text_changed_event = Signal(str)
    doc_edit_cursor_event = Signal()

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
        open_action.triggered.connect(self.open_file_event.emit)
        file_menu.addAction(open_action)

        # Language 菜单
        language_menu = menubar.addMenu("&Language")
        self.language_menu_title = language_menu.menuAction()
        for language in self.supported_languages:
            action = QAction(language, self, checkable=True)
            action.triggered.connect(
                lambda checked, lang=language: self.language_changed_event.emit(lang)
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

        self.doc_edit = DocView()
        self.ast_edit = QTextEdit()

        layout.addWidget(self.doc_edit)
        layout.addWidget(self.ast_edit)

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
