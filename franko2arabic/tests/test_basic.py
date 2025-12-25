import json
from pathlib import Path

import pytest

from franko2arabic.core import (
    FrankoToArabicTransliterator,
    TransliterationConfig,
    MappingPack,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_mapping() -> MappingPack:
    data = json.loads((DATA_DIR / "base_mapping.json").read_text(encoding="utf-8"))
    return MappingPack(multi=data["multi"], single=data["single"])


def load_words() -> dict:
    return json.loads((DATA_DIR / "egyptian_words.json").read_text(encoding="utf-8"))


def load_phrases() -> dict:
    return json.loads((DATA_DIR / "phrases_eg.json").read_text(encoding="utf-8"))


@pytest.fixture
def tr():
    mapping = load_mapping()
    words = load_words()
    phrases = load_phrases()

    cfg = TransliterationConfig(
        use_word_overrides=True,
        preserve_punctuation=True,
        preserve_numbers=True,
        lowercase_input=True,

        keep_english_words=True,
        # technical words that are NOT in dictionaries can remain English
        english_keep_words=("overleaf", "teams", "latex", "resumeitemliststart", "resumeitemlistend"),
    )

    return FrankoToArabicTransliterator(
        mapping=mapping,
        config=cfg,
        word_overrides=words,
        phrase_overrides=phrases,
    )


def test_phrase_el7amdullelah(tr):
    res = tr.transliterate("El7amdullelah enta 3amel eh?")
    assert res.output_text == "الحمدلله إنت عامل إيه?"


def test_phrase_yalla_bena(tr):
    res = tr.transliterate("Yalla bena")
    assert res.output_text == "يلا بينا"


def test_phrase_3ashan_afham(tr):
    res = tr.transliterate("3ashan afham asdak bas")
    assert res.output_text == "علشان أفهم قصدك بس"


def test_phrase_asdak_awl_cell(tr):
    res = tr.transliterate("asdak 3ala awl cell khales?")
    assert res.output_text == "قصدك على أول خلية خالص?"


def test_phrase_need_voltage(tr):
    res = tr.transliterate("u need to know each cell voltage")
    assert res.output_text == "لازم تعرف فولت كل خلية"


def test_word_level_fallback(tr):
    # Not a full phrase in phrases_eg; should still translate via egyptian_words
    res = tr.transliterate("enta 3amel eh?")
    assert "إنت" in res.output_text
    assert "عامل" in res.output_text


def test_english_preserved_if_not_in_dict(tr):
    # not in egyptian_words and not in phrases_eg -> stays English
    res = tr.transliterate("Has context menu")
    assert res.output_text in ("has context menu", "Has context menu")


def test_punctuation_preserved(tr):
    res = tr.transliterate("ana eh?!")
    assert res.output_text.endswith("?!")
