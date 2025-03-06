import re

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from PySide6.QtCore import QObject, Qt, QTimer
from PySide6.QtGui import QPalette, QTextCursor
from PySide6.QtWidgets import QFileDialog, QMessageBox

from models.ast import AST  # 添加导入语句
from models.document import Document
from views.main_window import MainWindow

DEFAULT_LANGUAGE = "python"
ast_pattern = re.compile(
    r"^(?P<indent>\s*)(?P<anonymous>\[anonymous\] )?((?P<name>.+): )?(?P<type>.+) (?P<range>\[[0-9]+, [0-9]+\] - \[[0-9]+, [0-9]+\])(?P<suffix>.*)$"
)


class MainController(QObject):
    def __init__(self, window: MainWindow):
        super().__init__()
        self.window = window
        self.document = Document()
        self.ast = AST()

        # 创建定时器用于防抖
        self._timer = QTimer(self)
        # 设置为单次触发
        self._timer.setSingleShot(True)
        self._timer.setInterval(500)
        self._timer.timeout.connect(self.emit_text_changed)

        # 连接信号
        self.window.open_file_event.connect(self.open_file)
        self.window.language_changed_event.connect(self.set_language)
        self.window.text_changed_event.connect(self.on_text_changed)
        self.window.doc_edit_cursor_event.connect(self.highlight_ast_region)
        self.window.ast_edit_cursor_event.connect(self.on_ast_edit_cursor_changed)
        self.window.doc_edit.textChanged.connect(self.handle_text_changed)
        self.window.text_changed_with_delay.connect(
            lambda text: self.window.text_changed_event.emit(text)
        )
        self.window.doc_edit.cursorPositionChanged.connect(
            self.window.doc_edit_cursor_event.emit
        )
        self.window.ast_edit.cursorPositionChanged.connect(
            self.window.ast_edit_cursor_event.emit
        )
        self.window.font_size_changed_event.connect(self.update_font_size)
        self.window.theme_changed_event.connect(self.handle_theme_changed)

        # 重置 Language 菜单
        self.window.language_changed_event.emit(DEFAULT_LANGUAGE)

        # 初始化主题
        self.handle_theme_changed(self.window.isDarkMode())

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )
        if not file_path:
            return
        self.document.file_path = file_path
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.document.content = file.read()
        except Exception as e:
            QMessageBox.critical(self.window, "ERROR", f"Fail to open file: {e}")
            return
        try:
            self.window.doc_edit.blockSignals(True)
            self.document.set_language_from_extension()
            self.window.doc_edit.setPlainText(self.document.content)
            self.window.doc_edit.blockSignals(False)
            self.set_language(self.document.language)
            self.ast_edit_load(self.document.language, self.document.content)
        except Exception as e:
            QMessageBox.critical(self.window, "ERROR", f"Error highlighting code: {e}")

    def set_language(self, language):
        self.document.language = language
        self.window.update_language_menu(language)
        self.highlight_code()
        self.ast_edit_load(self.document.language, self.document.content)

    def highlight_code(self):
        if not self.document.language:
            return

        try:
            self.window.doc_edit.blockSignals(True)
            language = self.document.language
            if language == "c_sharp":
                language = "csharp"
            lexer = get_lexer_by_name(language, stripall=True)
            palette = self.window.doc_edit.palette()
            # 获取系统背景色
            bg_color = palette.color(QPalette.Base).name()
            # 获取系统文本色
            text_color = palette.color(QPalette.Text).name()

            # 创建自定义样式
            style = {
                "bgcolor": bg_color,
                "color": text_color,
            }
            formatter = HtmlFormatter(
                style="default",
                full=True,
                noclasses=True,
                linenos=False,
                nobackground=True,
                style_defs=style,
            )
            highlighted_code = highlight(self.document.content, lexer, formatter)
            self.window.doc_edit.setHtml(highlighted_code)
        finally:
            self.window.doc_edit.blockSignals(False)

    def on_text_changed(self, text):
        self.document.content = text
        self.highlight_code()
        self.ast_edit_load(self.document.language, self.document.content)

    def ast_edit_load(self, language, content):
        if not content:
            self.window.ast_edit.clear()
            return
        try:
            self.ast.load(language, content)
        except Exception as e:
            QMessageBox.critical(self.window, "ERROR", f"Error loading AST: {e}")
            return

        ast_text = self.ast.get_plain_text()

        # 将普通文本转换为HTML格式
        html_lines = []
        for line in ast_text.split("\n"):
            match = ast_pattern.match(line)
            if not match:
                html_lines = f"<div style='normal'>{line}</div>"
                continue
            anonymous = match.group("anonymous")
            indent = match.group("indent")
            name = match.group("name")
            type = match.group("type")
            range = match.group("range")
            suffix = match.group("suffix")
            style = "anonymous" if anonymous else "normal"
            html_line = "".join(
                [
                    f"<div style='{style}'>",
                    f"<span style='indent'>{indent}</span>" if indent else "",
                    f"<span style='name'>{name}</span>: " if name else "",
                    f"<span style='type'>{type}</span>",
                    " ",
                    f"<span style='range'>{range}</span>",
                    suffix,
                    "</div>",
                ]
            )
            html_lines.append(html_line)

        html_head = """
        <html>
        <head>
            <style>
                /* 基础样式 */
                body {
                    font-family: Arial, sans-serif;
                }
                
                /* div 样式 */
                div {
                    line-height: 1.5;
                }

                /* 普通节点样式 */
                div[style='normal'] {
                    display: block;
                }

                /* 匿名节点样式 */
                div[style='anonymous'] {
                    display: block;
                    font-style: italic;
                    opacity: 0.6;
                }

                /* 匿名节点中的类型字段样式 */
                div[style='anonymous'] span[style='type'] {
                    color: #808080;
                }

                /* 缩进空格样式 */
                span[style='indent'] {
                    font-family: 'Courier New', monospace;
                    white-space: pre;
                    display: inline-block;
                }
                
                /* 名称字段样式 */
                span[style='name'] {
                    color: #569cd6;
                    font-weight: bold;
                }
                
                /* 范围字段样式 */
                span[style='range'] {
                    color: #808080;
                }
            </style>
        </head>
        <body>
        """
        html_tail = """
        </body>
        </html>
        """
        html_body = "\n".join(html_lines)
        html_content = f"{html_head}{html_body}{html_tail}"

        self.window.ast_edit.blockSignals(True)
        self.window.ast_edit.setHtml(html_content)
        self.window.ast_edit.blockSignals(False)

    def highlight_ast_region(self):
        self.window.ast_edit.blockSignals(True)
        cursor = self.window.doc_edit.textCursor()
        if cursor.hasSelection():
            cursor.setPosition(cursor.selectionEnd())
            line_number = cursor.blockNumber()
            column_number = cursor.columnNumber()
        else:
            line_number = cursor.blockNumber()
            column_number = cursor.columnNumber()
        match_index = self.ast.get_match_ast_line(line_number, column_number)

        # 新增代码：在 ast_edit 中选中对应的行
        if match_index is not None:
            ast_edit = self.window.ast_edit
            ast_edit_lines = ast_edit.toPlainText().split("\n")
            if 0 <= match_index < len(ast_edit_lines):
                ast_edit_cursor = ast_edit.textCursor()
                ast_edit_cursor.movePosition(QTextCursor.Start)
                for _ in range(match_index):
                    ast_edit_cursor.movePosition(QTextCursor.NextBlock)
                ast_edit_cursor.movePosition(QTextCursor.StartOfLine)
                ast_edit_cursor.movePosition(
                    QTextCursor.EndOfLine, QTextCursor.KeepAnchor
                )
                ast_edit.setTextCursor(ast_edit_cursor)
                ast_edit.ensureCursorVisible()
        self.window.ast_edit.blockSignals(False)

    def update_font_size(self, size):
        self.window.set_font_size(size)

    def on_ast_edit_cursor_changed(self):
        cursor = self.window.ast_edit.textCursor()
        line_number = cursor.blockNumber()
        start_line, start_column, end_line, end_column = self.ast.get_code_range(
            line_number
        )
        if start_line < 0:
            return

        self.window.doc_edit.blockSignals(True)
        doc_edit = self.window.doc_edit
        doc_edit_cursor = doc_edit.textCursor()

        # 获取文本块并转换为 bytes 以计算正确的长度
        block = doc_edit.document().findBlockByLineNumber(start_line)
        block_bytes = bytes(block.text(), "utf-8", errors="replace")
        start_position = block.position() + len(
            block_bytes[:start_column].decode("utf-8", errors="replace")
        )

        # 修改: 从 end_line 获取文本块以计算 end_position
        end_block = doc_edit.document().findBlockByLineNumber(end_line)
        end_block_bytes = bytes(end_block.text(), "utf-8", errors="replace")
        end_position = end_block.position() + len(
            end_block_bytes[:end_column].decode("utf-8", errors="replace")
        )

        doc_edit_cursor.setPosition(start_position)
        doc_edit_cursor.setPosition(end_position, QTextCursor.KeepAnchor)
        doc_edit.setTextCursor(doc_edit_cursor)
        doc_edit.ensureCursorVisible()
        self.window.doc_edit.blockSignals(False)

    def handle_text_changed(self):
        # 重置定时器
        self._timer.stop()
        self._timer.start()

    def emit_text_changed(self):
        # 发送带延迟的文本变化信号
        self.window.text_changed_with_delay.emit(self.window.doc_edit.toPlainText())

    def handle_theme_changed(self, is_dark_mode):
        # 获取应用程序实例的调色板
        palette = self.window.doc_edit.palette()
        # 根据主题设置颜色
        if is_dark_mode:
            # 深色模式
            palette.setColor(QPalette.Base, Qt.black)  # 背景色
            palette.setColor(QPalette.Text, Qt.white)  # 文本色
        else:
            # 浅色模式
            palette.setColor(QPalette.Base, Qt.white)  # 背景色
            palette.setColor(QPalette.Text, Qt.black)  # 文本色

        self.window.doc_edit.setPalette(palette)
        self.window.ast_edit.setPalette(palette)
