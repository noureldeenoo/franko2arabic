from __future__ import annotations
import json
from pathlib import Path

from franko2arabic import FrankoToArabicTransliterator, TransliterationConfig, MappingPack

DATA_DIR = Path(__file__).resolve().parent / "data"

def load_mapping() -> MappingPack:
    data = json.loads((DATA_DIR / "base_mapping.json").read_text(encoding="utf-8"))
    return MappingPack(multi=data["multi"], single=data["single"])

def load_overrides() -> dict:
    path = DATA_DIR / "egyptian_words.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    mapping = load_mapping()
    overrides = load_overrides()
    cfg = TransliterationConfig()

    tr = FrankoToArabicTransliterator(mapping=mapping, config=cfg, word_overrides=overrides)

    print("Type Franko text (Ctrl+C to exit):")
    while True:
        s = input("> ")
        res = tr.transliterate(s)
        print(res.output_text)

if __name__ == "__main__":
    main()
