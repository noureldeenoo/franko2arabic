from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class PhraseMatch:
    start: int
    end: int
    replacement: str


class PhraseMatcher:
    """
    Greedy longest-first phrase matcher over word tokens.
    """
    def __init__(self, phrases: Dict[str, str]):
        self.phrases = {k.strip().lower(): v for k, v in (phrases or {}).items()}
        self._sorted = sorted(self.phrases.items(), key=lambda kv: len(kv[0].split()), reverse=True)

    def match(self, words: List[str]) -> List[PhraseMatch]:
        out: List[PhraseMatch] = []
        i = 0
        while i < len(words):
            matched = False
            for phrase, repl in self._sorted:
                parts = phrase.split()
                n = len(parts)
                if i + n <= len(words) and words[i:i+n] == parts:
                    out.append(PhraseMatch(i, i+n, repl))
                    i += n
                    matched = True
                    break
            if not matched:
                i += 1
        return out
