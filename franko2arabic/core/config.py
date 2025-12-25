from dataclasses import dataclass

@dataclass(frozen=True)
class TransliterationConfig:
    use_word_overrides: bool = True
    preserve_punctuation: bool = True
    preserve_numbers: bool = True
    lowercase_input: bool = True

    compress_repeated_letters: bool = True
    max_repeat: int = 2

    # NEW:
    keep_english_words: bool = True
    english_keep_words: tuple[str, ...] = (
        "voltage", "cell", "cells", "sensor", "connected", "menu", "context",
        "bq", "esp", "i2c", "testing", "balancing", "csv"
    )
