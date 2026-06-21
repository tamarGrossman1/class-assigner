"""טעינת הגדרות מקובץ .env בלבד (API key, שם אפליקציה).

טוען את משתני הסביבה מקובץ \u200E.env שבשורש הפרויקט וחושף אותם לשאר המערכת.
מפתח ה-API הוא אופציונלי: אם אין מפתח, המערכת עדיין תרוץ — ניתוח הטקסט של
Claude פשוט ידולג (ראי ההערה ב-\u200E.env).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# שורש הפרויקט = שתי רמות מעל הקובץ הזה (backend/config.py -> backend -> root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# טעינת \u200E.env מהשורש (override=False כדי לכבד משתני סביבה אמיתיים אם קיימים)
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _get_bool(name: str, default: bool = False) -> bool:
    """קריאת ערך בוליאני מהסביבה (true/1/yes => True)."""
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    """קריאת ערך מספרי מהסביבה עם ברירת מחדל בטוחה."""
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


# --- הגדרות ---

# מפתח ה-API של Anthropic — אופציונלי. None אם לא הוגדר/ריק.
ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY") or None

# מודל Claude לשימוש (לניתוח טקסט בלבד)
CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-opus-4-8")

APP_NAME: str = os.getenv("APP_NAME", "Class Assignment System")
DEBUG: bool = _get_bool("DEBUG", False)
OUTPUT_DIR: Path = (PROJECT_ROOT / os.getenv("OUTPUT_DIR", "./output")).resolve()
MAX_RETRIES: int = _get_int("MAX_RETRIES", 3)


def has_api_key() -> bool:
    """האם הוגדר מפתח API תקין (לא ריק)."""
    return bool(ANTHROPIC_API_KEY)
