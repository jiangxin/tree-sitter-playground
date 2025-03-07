from PySide6.QtCore import QEvent, Signal
from PySide6.QtGui import QAction, QActionGroup, QFont, QPalette
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QSplitter, QWidget

from models.lang_map import lang_map

from .ast_view import AstView
from .doc_view import DocView


class MainWindow(QMainWindow):
    open_file_event: Signal = Signal()
    language_changed_event: Signal = Signal(str)
    text_changed_event: Signal = Signal(str)
    text_changed_with_delay = Signal(str)
    doc_edit_cursor_event: Signal = Signal()
    ast_edit_cursor_event: Signal = Signal()
    font_size_changed_event: Signal = Signal(int)
    theme_changed_event: Signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.supported_languages = sorted(set(lang_map.values()))
        self.selected_language_action = None
        self.language_menu_title = None
        self.font_size = 18

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Tree-sitter Playground")
        self.resize(800, 600)

        self.create_menus()
        self.create_editors()
        self.set_font_size(self.font_size)

    def create_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_event.emit)
        file_menu.addAction(open_action)

        # Language menu
        language_menu = menubar.addMenu("&Language")
        self.language_menu_title = language_menu.menuAction()
        for language in self.supported_languages:
            action = QAction(language, self)
            action.setCheckable(True)
            action.triggered.connect(
                (lambda lang: lambda checked: self.language_changed_event.emit(lang))(
                    language
                )
            )
            language_menu.addAction(action)

        # Size menu
        size_menu = menubar.addMenu("&Size")
        size_group = QActionGroup(self, exclusive=True)
        for size in range(10, 39, 2):  # 从 10 到 38，步长为 2
            action = QAction(str(size), self)
            action.setCheckable(True)
            action.triggered.connect(
                (lambda s: lambda checked: self.font_size_changed_event.emit(s))(size)
            )
            size_group.addAction(action)
            size_menu.addAction(action)
            if size == self.font_size:
                action.setChecked(True)
        # size_group.triggered.connect(lambda action: self.font_size_changed_event.emit(int(action.text())))

        # View and Help menus
        menubar.addMenu("&View")
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(QAction("&About", self))

    def set_font_size(self, size):
        self.font_size = size
        font = QFont()
        font.setPointSize(size)
        self.doc_edit.setFont(font)
        self.ast_edit.setFont(font)

    def create_editors(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter()

        self.doc_edit = DocView()
        self.ast_edit = AstView()

        splitter.addWidget(self.doc_edit)
        splitter.addWidget(self.ast_edit)

        splitter.setSizes([self.width() // 2, self.width() // 2])

        splitter.setStyleSheet(
            """
            QSplitter::handle {
                background-color: #ccc;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #999;
            }
        """
        )

        layout.addWidget(splitter)

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

    def changeEvent(self, event):
        if event.type() == QEvent.PaletteChange:
            is_dark_mode = self.isDarkMode()
            self.theme_changed_event.emit(is_dark_mode)
        super().changeEvent(event)

    def isDarkMode(self):
        app_palette = self.style().standardPalette()
        text_color = app_palette.color(QPalette.WindowText)
        return text_color.lightness() > 128
