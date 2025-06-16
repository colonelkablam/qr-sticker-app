from pathlib import Path
from urllib.parse import urlparse, parse_qs
import re

def extract_slug(url: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # Try to get deviceId from query
    slug = query.get("deviceId", [None])[0]

    # If no deviceId, fallback to last path component
    if not slug:
        path = parsed.path.rstrip("/")
        slug = path.split("/")[-1] if path else None

    # Final fallback
    slug = slug or "qr-sticker"

    # Clean up filename: only allow a-z, 0-9, dashes, underscores
    slug = re.sub(r"[^a-zA-Z0-9_-]", "", slug)

    return slug or "qr-sticker"


def get_default_save_dir() -> Path:
    home = Path.home()

    # Try Downloads first
    downloads = home / "Downloads"
    if downloads.exists():
        return downloads

    # Fallback to Desktop
    desktop = home / "Desktop"
    if desktop.exists():
        return desktop

    # Final fallback
    return Path.cwd()



