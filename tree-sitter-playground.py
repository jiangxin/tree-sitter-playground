#!/usr/bin/env python3

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from controllers.main_controller import MainController
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # macOS 特定设置
    if sys.platform == "darwin":
        app.setAttribute(Qt.AA_DontShowIconsInMenus)

    window = MainWindow()

    # 在 PySide6 (Qt) 中，如果 EditorController(window) 不赋值，这个对象会立即被
    # Python 的垃圾回收器销毁，因为没有任何引用持有它。
    # 可以直接赋值给 _，既能避免对象回收，又能避免 linter 警告。
    _ = MainController(window)

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
