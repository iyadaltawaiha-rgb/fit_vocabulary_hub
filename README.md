# FIT Vocabulary Hub (Streamlit)

A modular Streamlit app for managing and learning bilingual vocabulary per course.

## Features
- Student mode: Flashcards, Quiz, Word list with search
- Admin mode: Manage courses and vocabulary
- Bulk import vocabulary from Excel

## Project structure
```
fit_vocabulary_hub/
  run_app.py
  requirements.txt
  README.md
  vocab_hub/
    app.py
    config.py
    utils.py
    state.py
    db/
      connection.py
      courses_repo.py
      vocab_repo.py
    services/
      seed.py
      quiz.py
      importer.py
    ui/
      sidebar.py
      student.py
      admin.py
```

## Run in development
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run vocab_hub/app.py
```

## Excel import format
Sheet name: `vocabulary`  
Required columns:
- course_name
- term_en
- definition_en
- definition_ar

Optional:
- term_ar
- example_en
- difficulty (1-3)
- category

## Build a Windows .exe (PyInstaller)

> Streamlit is web-based; the .exe will **start a local Streamlit server**.
> The user will access it via their browser.

1) Install build tools:
```bash
pip install pyinstaller
pip install -r requirements.txt
```

2) Build:
```bash
pyinstaller --noconfirm --onefile --name "FIT-Vocab-Hub" ^
  --add-data "vocab_hub;vocab_hub" ^
  run_app.py
```

3) Run:
- The exe will be in `dist\FIT-Vocab-Hub.exe`.

### Notes
- The SQLite database will be created automatically in:
  `C:\Users\<You>\.fit_vocab_hub\vocab.db`
- To override admin password:
  ```bash
  set FIT_VOCAB_ADMIN_PASSWORD=YourStrongPassword
  ```

## Troubleshooting
- If `--add-data` path separator fails on your OS:
  - Windows uses `;`
  - macOS/Linux uses `:`
