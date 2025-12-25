"""
Core package for Franko → Arabic transliteration.

This package contains:
- Configuration
- Normalization
- Tokenization
- Mapping engine
- Rule engine
- Main transliterator
"""

from .config import TransliterationConfig
from .types import MappingPack, TransliterationResult
from .transliterator import FrankoToArabicTransliterator

__all__ = [
    "TransliterationConfig",
    "MappingPack",
    "TransliterationResult",
    "FrankoToArabicTransliterator",
]
