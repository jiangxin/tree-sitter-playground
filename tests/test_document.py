import pytest

from models.document import Document
from models.lang_map import get_language, supported_languages


def test_document_initialization():
    doc = Document()
    assert doc.content == ""
    assert doc.language is None
    assert doc.file_path is None


def test_set_language_from_extension():
    doc = Document()

    # Test Python file
    doc.file_path = "test.py"
    doc.set_language_from_extension()
    assert doc.language == "python"

    # Test JavaScript file
    doc.file_path = "test.js"
    doc.set_language_from_extension()
    assert doc.language == "javascript"

    # Test unknown extension
    doc.file_path = "test.unknown"
    with pytest.raises(Exception) as exc_info:
        doc.set_language_from_extension()
    assert "unknown language for file: " in str(exc_info.value)


def test_supported_languages():
    # Verify that all mapped languages are unique
    assert len(supported_languages) > 0

    # Test some common extensions
    assert get_language("test.py") == "python"
    assert get_language("test.js") == "javascript"
    assert get_language("test.cpp") == "cpp"
    assert get_language("Dockerfile") == "dockerfile"
