import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from controllers.main_controller import MainController
from views.main_window import MainWindow


@pytest.fixture(scope="session")
def app():
    """Create a QApplication instance once per test session."""
    if not QApplication.instance():
        app = QApplication([])
        yield app
        app.quit()
    else:
        yield QApplication.instance()


@pytest.fixture
def main_window(app):
    window = MainWindow()
    yield window
    window.close()


@pytest.fixture
def controller(main_window):
    controller = MainController(main_window)
    yield controller
    # 清理闪烁定时器
    if controller._blink_timer.isActive():
        controller._blink_timer.stop()
    if controller._timer.isActive():
        controller._timer.stop()


def test_initialization(controller):
    assert controller.document is not None
    assert controller.ast is not None
    assert controller._timer is not None
    assert controller._blink_timer is not None


def test_blink_animation(controller):
    # Test blink animation setup
    controller._start_blink_animation(controller.window.doc_edit)
    assert controller._blinking_editor is not None
    assert controller._blink_count == 0

    # Test first blink (highlight)
    controller._blink_selection()
    assert controller._blink_count == 1

    # Test second blink (normal)
    controller._blink_selection()
    assert controller._blink_count == 2

    # Test animation end
    controller._blink_count = 4
    controller._blink_selection()
    assert controller._blinking_editor is None


def test_theme_handling(controller):
    # Test light mode
    controller.handle_theme_changed(False)
    palette = controller.window.doc_edit.palette()
    assert palette.color(QPalette.ColorRole.Base) == QColor(Qt.white)
    assert palette.color(QPalette.ColorRole.Text) == QColor(Qt.black)

    # Test dark mode
    controller.handle_theme_changed(True)
    palette = controller.window.doc_edit.palette()
    assert palette.color(QPalette.ColorRole.Base) == QColor(Qt.black)
    assert palette.color(QPalette.ColorRole.Text) == QColor(Qt.white)
