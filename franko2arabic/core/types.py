from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True)
class MappingPack:
    multi: Dict[str, str]   # longest-first matching (e.g., "sh", "7'")
    single: Dict[str, str]  # single character mapping

@dataclass(frozen=True)
class TransliterationResult:
    input_text: str
    output_text: str
    tokens: List[str]
    notes: List[str]
