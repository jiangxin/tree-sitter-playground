#!/usr/bin/env python3

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from controllers.main_controller import MainController
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # macOS specific settings
    if sys.platform == "darwin":
        app.setAttribute(Qt.AA_DontShowIconsInMenus)

    window = MainWindow()

    # In PySide6 (Qt), if EditorController(window) is not assigned, this object will be
    # immediately destroyed by Python's garbage collector because no references hold it.
    # Assign to _ to avoid both object collection and linter warnings.
    _ = MainController(window)

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
