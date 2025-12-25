from __future__ import annotations
from typing import Dict, List, Tuple
from .types import MappingPack

class GreedyMapper:
    """
    Greedy longest-match mapper for a single token.
    Example: "sh" should match before "s" + "h".
    """
    def __init__(self, mapping: MappingPack):
        self.mapping = mapping
        # Pre-sort multi keys by length descending for greedy matching
        self._multi_keys = sorted(mapping.multi.keys(), key=len, reverse=True)

    def map_token(self, token: str) -> Tuple[str, List[str]]:
        out = []
        notes: List[str] = []

        i = 0
        while i < len(token):
            matched = False

            # try multi
            for k in self._multi_keys:
                if token.startswith(k, i):
                    out.append(self.mapping.multi[k])
                    i += len(k)
                    matched = True
                    break

            if matched:
                continue

            ch = token[i]

            # single map
            if ch in self.mapping.single:
                out.append(self.mapping.single[ch])
            else:
                # unknown char: keep as-is (or you can replace with "؟" or "")
                out.append(ch)
                notes.append(f"Unmapped char kept: {ch!r}")

            i += 1

        return "".join(out), notes
