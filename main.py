import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QMenu, QVBoxLayout, QWidget, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("PySide 编辑器")

        # 创建菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")
        edit_menu = menubar.addMenu("编辑")
        help_menu = menubar.addMenu("帮助")

        # 创建左右两个编辑框
        left_edit = QTextEdit()
        right_edit = QTextEdit()

        # 创建水平布局并添加编辑框
        layout = QHBoxLayout()
        layout.addWidget(left_edit)
        layout.addWidget(right_edit)

        # 创建主窗口的中心部件并设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())