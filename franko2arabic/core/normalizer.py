from __future__ import annotations
import re
from .config import TransliterationConfig

class TextNormalizer:
    """
    Normalizes Franko input to make matching more consistent.
    """
    _smart_quotes = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
    }

    def __init__(self, config: TransliterationConfig):
        self.config = config

    def normalize(self, text: str) -> str:
        t = text

        # unify quotes
        for k, v in self._smart_quotes.items():
            t = t.replace(k, v)

        if self.config.lowercase_input:
            t = t.lower()

        # optional: compress repeats (e.g., "cooool" -> "coool" -> "cool" depending settings)
        if self.config.compress_repeated_letters:
            t = self._compress_repeats(t, self.config.max_repeat)

        return t

    @staticmethod
    def _compress_repeats(text: str, max_repeat: int) -> str:
        # Keep at most max_repeat of a repeated character (letters only)
        def repl(m: re.Match) -> str:
            ch = m.group(1)
            return ch * max_repeat
        return re.sub(r"([a-z])\1{" + str(max_repeat) + r",}", repl, text)
