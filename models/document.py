import os
from dataclasses import dataclass
from typing import Optional

from .lang_map import get_language


@dataclass
class Document:
    content: str = ""
    language: Optional[str] = None
    file_path: Optional[str] = None

    def set_language_from_extension(self):
        if not self.file_path:
            return
        self.language = get_language(self.file_path)
        if not self.language:
            raise Exception(
                "unknown language for file: '{}'".format(
                    os.path.basename(self.file_path)
                )
            )
