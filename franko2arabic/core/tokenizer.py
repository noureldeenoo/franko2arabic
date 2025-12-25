from __future__ import annotations
import re
from typing import List
from .config import TransliterationConfig

class Tokenizer:
    """
    Splits into tokens: words, numbers, whitespace, punctuation.
    Keeping separators lets us preserve formatting.
    """
    def __init__(self, config: TransliterationConfig):
        self.config = config
        # word (letters/numbers/' ) | whitespace | punctuation/other
        self._pattern = re.compile(r"[a-z0-9']+|\s+|.", re.IGNORECASE)

    def tokenize(self, text: str) -> List[str]:
        return self._pattern.findall(text)
