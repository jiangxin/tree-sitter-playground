from dataclasses import dataclass
from typing import Optional


@dataclass
class Document:
    content: str = ""
    language: Optional[str] = None
    file_path: Optional[str] = None

    def set_language_from_extension(self):
        if not self.file_path:
            return

        import os

        _, ext = os.path.splitext(self.file_path)

        extension_map = {
            ".py": "python",
            ".c": "cpp",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".java": "java",
        }

        self.language = extension_map.get(ext, "unknown")
