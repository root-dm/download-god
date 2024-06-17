from pathlib import Path
import sys

ASSETS_PATH = Path(__file__).parent.parent / "assets/frame0"

def relative_to_assets(path: str) -> Path:
    base_path = getattr(sys, '_MEIPASS', Path(__file__).parent.parent)
    if (path == 'logo.ico'):
        return Path(base_path) / 'assets' / path
    else:
        return Path(base_path) / 'assets' / 'frame0' / path

def update_progress_bar(progress, canvas, is_verification=False):
    """Update the progress bar."""
    if is_verification:
        canvas.coords("progress_fg", 519.0, 342.0, 519.0 + 298.0 * progress, 355.0)
    else:
        canvas.coords("progress_fg", 519.0, 342.0, 519.0 + 298.0 * progress, 355.0)
