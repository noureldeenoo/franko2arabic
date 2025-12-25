import json
from pathlib import Path

from franko2arabic.core import (
    FrankoToArabicTransliterator,
    TransliterationConfig,
    MappingPack,
)

# -------------------------------------------------
# Load data files
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "franko2arabic" / "data"

# Load base mapping
mapping_data = json.loads(
    (DATA_DIR / "base_mapping.json").read_text(encoding="utf-8")
)
mapping = MappingPack(
    multi=mapping_data["multi"],
    single=mapping_data["single"],
)

# Load word overrides (Egyptian dictionary)
word_overrides = json.loads(
    (DATA_DIR / "egyptian_words.json").read_text(encoding="utf-8")
)

# Load phrase overrides
phrase_overrides = json.loads(
    (DATA_DIR / "phrases_eg.json").read_text(encoding="utf-8")
)

# -------------------------------------------------
# Config
# -------------------------------------------------
config = TransliterationConfig(
    use_word_overrides=True,
    keep_english_words=True,
)

# -------------------------------------------------
# Create transliterator
# -------------------------------------------------
translator = FrankoToArabicTransliterator(
    mapping=mapping,
    config=config,
    word_overrides=word_overrides,
    phrase_overrides=phrase_overrides,
)

# -------------------------------------------------
# Examples
# -------------------------------------------------
examples = [
    "Ok shokran ",
    "3la 2nhy link , CFR follow up?",
    "hwa bda2?"
]

for text in examples:
    result = translator.transliterate(text)
    print("INPUT :", text)
    print("OUTPUT:", result.output_text)
    print("-" * 40)
