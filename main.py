import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from views.editor_view import EditorView
from controllers.editor_controller import EditorController


def main():
    app = QApplication(sys.argv)

    # macOS 特定设置
    if sys.platform == "darwin":
        app.setAttribute(Qt.AA_DontShowIconsInMenus)

    view = EditorView()
    _ = EditorController(view)
    view.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
