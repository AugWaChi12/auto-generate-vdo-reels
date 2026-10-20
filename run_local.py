import sys
from pathlib import Path

# Fix Windows console UTF-8 emoji encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.pipeline import run_pipeline

if __name__ == "__main__":
    tool_arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(tool_arg)

