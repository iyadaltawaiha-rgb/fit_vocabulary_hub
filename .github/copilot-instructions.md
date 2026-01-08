# FIT Vocabulary Hub — AI assistant guide

This repository is a small Streamlit application with a local SQLite store. The goal of these instructions is to help AI coding agents be immediately productive by describing architecture, workflows, conventions, and important files.

- **Big picture:** The app is a single-process Streamlit app for bilingual (English/Arabic) vocabulary learning. Entry points:
  - Development: run `streamlit run streamlit_app.py` (recommended launcher). Primary logic in `vocab_hub/app.py`.
- **Packaged exe: `run_app.py` is a PyInstaller-friendly entry-point that programmatically invokes Streamlit (only when frozen as exe). For normal runs (e.g., Streamlit Cloud), it executes the app directly to avoid runtime conflicts.**

- **Major components & boundaries:**
  - `vocab_hub/app.py` — orchestrates startup: session state, DB init, demo seeding, and UI mode routing (`Student` vs `Admin`).
  - `streamlit_app.py` — recommended top-level launcher for hosting (Streamlit Cloud). Use this file as the app entrypoint to avoid import/path issues when Streamlit executes scripts from a temp directory.
  - `vocab_hub/ui/` — UI renderers split by responsibility: `sidebar.py`, `student.py`, `admin.py`.
  - `vocab_hub/state.py` — centralized session-state keys and initial/default values. Use these keys when reading/writing `st.session_state`.
  - `vocab_hub/db/` — persistence layer using SQLite. `connection.py` creates a new connection per call; repos (`courses_repo.py`, `vocab_repo.py`) encapsulate SQL.
  - `vocab_hub/services/` — business logic helpers: `seed.py` (demo data), `importer.py` (Pandas-based Excel import), `quiz.py` (quiz logic).

- **Data flow & important details:**
  - DB path: determined by `vocab_hub/config.get_db_path()` and stored under the user home dir (`~/.fit_vocabulary_hub/vocab.db`).
  - `get_connection()` opens a connection per call and enables foreign keys; code assumes lightweight, short-lived connections.
  - The app supports bilingual vocabulary; quiz tests Arabic terms against English definitions.
  - Import expects a sheet named `vocabulary` with required columns: `course_name`, `term_en`, `definition_en`, `definition_ar`. Optional: `term_ar`, `example_en`, `difficulty` (1-3), `category` (see `services/importer.py`).

- **Project-specific conventions & patterns:**
  - Session state keys are centralized in `vocab_hub/state.py` (use constants like `ADMIN_KEY`, `COURSE_KEY`). Do not invent ad-hoc keys.
  - DB repo functions return raw `sqlite3.Row` objects or primitives; follow existing patterns (no ORM).
  - Validation is performed in repo/service layers (e.g., `_normalize_difficulty`, required field checks). Mirror this style when adding features.
  - Demo data is seeded automatically if the database is empty (see `services/seed.py`).

- **Dev/run workflows (practical commands):**
  - Local dev (venv + streamlit):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    streamlit run streamlit_app.py  # recommended launcher
    # Alternative: streamlit run vocab_hub/app.py
    ```
  - Run via PyInstaller (Windows packaging) — `run_app.py` is used by the built exe; see README for `pyinstaller --add-data` details.
  - Default admin password is 'admin123' (override with `FIT_VOCAB_ADMIN_PASSWORD` env var before launch).

- **What to look for when editing code:**
  - Always respect `st.session_state` initialization in `init_state()` — new keys should be added there.
  - Database schema changes require updating `vocab_hub/db/connection.py` and handling migrations manually (no migration framework present).
  - When modifying queries, preserve `row_factory = sqlite3.Row` usage in `get_connection()` so callers can access columns by name.

- **Common tasks examples:**
  - Add a new student-level view: create a renderer in `vocab_hub/ui/`, import it in `app.py`, and map a new mode via `render_sidebar()`.
  - Add a DB field: add column SQL in `connection.init_db()` and update repo read/write functions in `vocab_hub/db/`.

- **Dependencies & integration points:**
  - `streamlit` (UI runtime), `pandas` (Excel import), and `openpyxl` (Excel reading). See `requirements.txt`.
  - SQLite file at `get_db_path()`; packaged apps rely on `get_app_dir()` creating a user-writable folder.

- **Notes for automated changes by AI:**
  - Avoid changing `st.session_state` keys without updating `init_state()`.
  - Keep SQL logic inside `vocab_hub/db/*` and use `get_connection()` for consistent PRAGMA settings.
  - Prefer adding a top-level launcher (`streamlit_app.py`) for hosted deployments (Streamlit Cloud) instead of adding `sys.path` hacks inside package modules. If a `sys.path` fallback exists, remove it after confirming the launcher works.
