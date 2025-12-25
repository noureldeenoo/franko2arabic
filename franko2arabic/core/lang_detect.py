from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Set


_EN_WORD_RE = re.compile(r"^[a-z]+$", re.IGNORECASE)  # only letters


@dataclass(frozen=True)
class EnglishDetectionConfig:
    # If True: keep English words as-is
    keep_english_words: bool = True

    # Words you always keep (useful for technical terms)
    english_keep_words: Set[str] | None = None

    # If a token contains any of these, it's definitely Arabizi and should be transliterated
    arabizi_markers: str = "23456789'"  # includes numbers + apostrophe


class EnglishWordDetector:
    """
    Heuristic detector:
    - If token contains Arabizi markers (digits, apostrophe) -> NOT English.
    - If token is letters-only AND looks like a typical English word -> English.
    """

    def __init__(self, cfg: EnglishDetectionConfig):
        self.cfg = cfg
        self.keep = {w.lower() for w in (cfg.english_keep_words or set())}

    def is_english_word(self, token: str) -> bool:
        t = token.strip().lower()
        if not t:
            return False

        if any(ch in t for ch in self.cfg.arabizi_markers):
            return False

        if t in self.keep:
            return True

        # Must be letters only
        if not _EN_WORD_RE.match(t):
            return False

        # Optional extra heuristic: very short tokens are ambiguous ("el", "ya", "ok")
        # We'll treat them as NOT English (so overrides can handle them).
        if len(t) <= 2:
            return False

        return True
