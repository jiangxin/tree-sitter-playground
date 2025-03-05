import os
from dataclasses import dataclass
from typing import Optional

from .lang_map import lang_map


@dataclass
class Document:
    content: str = ""
    language: Optional[str] = None
    file_path: Optional[str] = None

    def set_language_from_extension(self):
        if not self.file_path:
            return
        _, ext = os.path.splitext(self.file_path)
        if ext not in lang_map:
            raise Exception(f"unknown file extension: {ext}")
        self.language = lang_map.get(ext)
