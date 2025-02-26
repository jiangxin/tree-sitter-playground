import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget, QHBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("PySide 编辑器")

        # 创建菜单栏
        self.create_menus()

        # 创建左右两个编辑框
        self.create_editors()

        # 设置窗口大小
        self.resize(800, 600)

    def create_menus(self):
        # 获取菜单栏
        menubar = self.menuBar()

        # File 菜单
        file_menu = menubar.addMenu("&File")
        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)

        # Languages 菜单
        languages_menu = menubar.addMenu("&Languages")
        python_action = QAction("Python", self)
        languages_menu.addAction(python_action)

        # View 菜单
        menubar.addMenu("&View")

        # Help 菜单
        help_menu = menubar.addMenu("&Help")
        about_action = QAction("&About", self)
        help_menu.addAction(about_action)

    def create_editors(self):
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建水平布局
        layout = QHBoxLayout(central_widget)

        # 创建左右编辑框
        self.left_edit = QTextEdit()
        self.right_edit = QTextEdit()

        # 添加到布局
        layout.addWidget(self.left_edit)
        layout.addWidget(self.right_edit)


def main():
    app = QApplication(sys.argv)

    # macOS 特定设置
    if sys.platform == "darwin":
        app.setAttribute(Qt.AA_DontShowIconsInMenus)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
