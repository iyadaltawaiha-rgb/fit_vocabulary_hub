from __future__ import annotations

import os
import sys
from pathlib import Path

from streamlit.web import cli as stcli

def main() -> int:
    """
    Entry-point script suitable for PyInstaller.
    It launches the Streamlit app programmatically.
    """
    base_dir = Path(__file__).parent
    app_path = base_dir / "vocab_hub" / "app.py"

    # You can tweak server options here
    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]
    return stcli.main()

if __name__ == "__main__":
    raise SystemExit(main())
