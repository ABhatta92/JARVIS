from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
WORKSPACE = PROJECT_ROOT / "workspace"

READ_ALLOWED = [PROJECT_ROOT]
WRITE_ALLOWED = [WORKSPACE]
