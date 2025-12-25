# Franko2Arabic 🇪🇬➡️AR

**Franko2Arabic** is a modular Python library for translating **Franco / Franko / Arabizi** text  
(Arabic written using Latin letters and numbers like `3`, `7`, `2`) into **proper Arabic script**.

The project is built for **real-world chat data** (WhatsApp, Teams, Messenger, etc.) and supports:
- Egyptian Arabic 🇪🇬
- Mixed Arabic + English sentences
- Phrase-level translation
- Word-level overrides
- Smart English detection

---

## ✨ Features

- 🔤 **Franco / Arabizi → Arabic**
- 🧠 **Phrase-based translation** (highest priority)
- 📚 **Extensible dictionaries**
- 🇬🇧 **Smart English handling**
  - English words are kept unless explicitly defined
- ⚙️ **Clean OOP & modular design**
- 🧪 **Tested with pytest**
- 🚀 Ready for CLI, API, or ML extensions

---

## 📂 Project Structure

```
franko2arabic/
│
├─ franko2arabic/
│  ├─ __init__.py
│  ├─ core/
│  │  ├─ transliterator.py
│  │  ├─ phrases.py
│  │  ├─ lang_detect.py
│  │  ├─ mapper.py
│  │  ├─ normalizer.py
│  │  ├─ tokenizer.py
│  │  ├─ rules.py
│  │  └─ config.py
│  │
│  └─ data/
│     ├─ base_mapping.json
│     ├─ egyptian_words.json
│     └─ phrases_eg.json
│
├─ tests/
│  └─ test_basic.py
│
├─ example_use.py
├─ pyproject.toml
└─ README.md
```

---

## 🧠 Translation Priority

1. Phrase overrides (`phrases_eg.json`)
2. Word overrides (`egyptian_words.json`)
3. Keep English words (if not in dictionaries)
4. Character-level transliteration (fallback)

---

## 🚀 Basic Usage

```python
print(translator.transliterate("el7amdullelah enta 3amel eh").output_text)
```

Output:
```
الحمدلله إنت عامل إيه
```

---

## 🧪 Run Tests

```bash
python -m pytest -v
```

---

## 🛠️ Adding Translations

Add words in `egyptian_words.json`  
Add phrases in `phrases_eg.json`

---

## 📜 License

MIT License
