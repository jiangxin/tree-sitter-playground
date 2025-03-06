import pytest

from models.document import Document
from models.lang_map import lang_map


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
    assert "unknown file extension" in str(exc_info.value)


def test_supported_languages():
    # Verify that all mapped languages are unique
    languages = set(lang_map.values())
    assert len(languages) > 0

    # Test some common extensions
    assert lang_map["py"] == "python"
    assert lang_map["js"] == "javascript"
    assert lang_map["cpp"] == "cpp"
