from __future__ import annotations

from typing import Dict, List, Optional

from .config import TransliterationConfig
from .normalizer import TextNormalizer
from .tokenizer import Tokenizer
from .types import MappingPack, TransliterationResult
from .mapper import GreedyMapper
from .rules import RuleEngine
from .phrases import PhraseMatcher
from .lang_detect import EnglishWordDetector, EnglishDetectionConfig


class FrankoToArabicTransliterator:
    """
    High-level orchestrator:
    normalize -> tokenize -> phrase overrides -> word overrides -> keep english -> greedy map -> postprocess
    """

    def __init__(
        self,
        mapping: MappingPack,
        config: TransliterationConfig | None = None,
        word_overrides: dict | None = None,
        phrase_overrides: dict | None = None,
    ):
        self.config = config or TransliterationConfig()
        self.normalizer = TextNormalizer(self.config)
        self.tokenizer = Tokenizer(self.config)
        self.mapper = GreedyMapper(mapping)

        # store overrides normalized
        self.word_overrides = {k.lower(): v for k, v in (word_overrides or {}).items()}
        self.phrase_overrides = {k.lower(): v for k, v in (phrase_overrides or {}).items()}

        self.rules = RuleEngine(word_overrides=self.word_overrides)

        self.phrase_matcher = PhraseMatcher(self.phrase_overrides)

        self.english_detector = EnglishWordDetector(
            EnglishDetectionConfig(
                keep_english_words=self.config.keep_english_words,
                english_keep_words=set(self.config.english_keep_words),
            )
        )

    def transliterate(self, text: str) -> TransliterationResult:
        notes: List[str] = []

        normalized = self.normalizer.normalize(text)
        tokens = self.tokenizer.tokenize(normalized)

        # Identify word-like tokens positions for phrase matching
        # (Tokenzier returns words/spaces/punct, so "wordish" tokens are [a-z0-9']+)
        word_positions: List[int] = []
        word_tokens: List[str] = []
        for idx, tok in enumerate(tokens):
            if tok and (tok[0].isalnum() or tok[0] == "'") and all(ch.isalnum() or ch == "'" for ch in tok):
                if not tok.isdigit():
                    word_positions.append(idx)
                    word_tokens.append(tok.lower())

        # Phrase matches on word_tokens
        phrase_matches = self.phrase_matcher.match(word_tokens)
        # Map start index -> (end index, replacement)
        phrase_map = {m.start: (m.end, m.replacement) for m in phrase_matches}

        out_tokens: List[str] = []

        i = 0          # index over tokens
        w_i = 0        # index over word_tokens
        while i < len(tokens):
            tok = tokens[i]

            # whitespace
            if tok.isspace():
                out_tokens.append(tok)
                i += 1
                continue

            # punctuation / symbols
            if len(tok) == 1 and not tok.isalnum() and tok not in ("'",):
                out_tokens.append(tok if self.config.preserve_punctuation else "")
                i += 1
                continue

            # numeric token
            if tok.isdigit():
                out_tokens.append(tok if self.config.preserve_numbers else "")
                i += 1
                continue

            # wordish?
            is_wordish = tok and (tok[0].isalnum() or tok[0] == "'") and all(ch.isalnum() or ch == "'" for ch in tok)

            if is_wordish and not tok.isdigit():
                key = tok.lower()

                # 1) Phrase overrides (highest priority)
                # If current token is a word token position and phrase starts here
                if w_i < len(word_positions) and word_positions[w_i] == i and w_i in phrase_map:
                    end_w, repl = phrase_map[w_i]
                    out_tokens.append(repl)

                    # skip tokens covered by the phrase
                    last_token_pos = word_positions[end_w - 1]
                    i = last_token_pos + 1
                    w_i = end_w
                    continue

                # 2) Word overrides (translate even if English)
                if self.config.use_word_overrides:
                    ov = self.word_overrides.get(key)
                    if ov is not None:
                        out_tokens.append(ov)
                        i += 1
                        w_i += 1
                        continue

                # 3) Keep English words as-is (only if not in overrides/phrases)
                if self.config.keep_english_words and self.english_detector.is_english_word(tok):
                    out_tokens.append(tok)
                    i += 1
                    w_i += 1
                    continue

                # 4) Transliterate with mapping
                mapped, mapper_notes = self.mapper.map_token(key)
                notes.extend(mapper_notes)
                out_tokens.append(mapped)
                i += 1
                w_i += 1
                continue

            # fallback (rare)
            out_tokens.append(tok)
            i += 1

        output = "".join(out_tokens)
        output = self.rules.postprocess_text(output)

        return TransliterationResult(
            input_text=text,
            output_text=output,
            tokens=tokens,
            notes=notes,
        )
