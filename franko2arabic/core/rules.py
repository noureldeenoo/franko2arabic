from __future__ import annotations
from typing import Dict, List, Tuple
import re

class RuleEngine:
    """
    Post-processing rules to improve output (dialect-specific, spelling fixes).
    Keep these rules small and data-driven over time.
    """
    def __init__(self, word_overrides: Dict[str, str] | None = None):
        self.word_overrides = word_overrides or {}

        # Example regex-based post rules
        self._regex_rules: List[Tuple[re.Pattern, str]] = [
            # Common: "ال " spacing normalization might be handled later
            (re.compile(r"\s+"), " "),  # compress whitespace
        ]

    def apply_word_override(self, token: str) -> str | None:
        # token should already be normalized (lowercase etc.)
        return self.word_overrides.get(token)

    def postprocess_text(self, text: str) -> str:
        t = text
        for pat, repl in self._regex_rules:
            t = pat.sub(repl, t)
        return t.strip()
