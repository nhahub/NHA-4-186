import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent

subprocess.run([
    sys.executable,
    "-m",
    "streamlit",
    "run",
    str(project_root / "app" / "home.py")
])