import sqlite3
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "processed_messages.db"


def init_db() -> None:
    """Create the database and required tables."""
    DATA_DIR.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_messages (
                message_id TEXT PRIMARY KEY,
                processed_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def is_message_processed(message_id: str) -> bool:
    """Check whether a message has already been processed."""
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT 1
            FROM processed_messages
            WHERE message_id = ?
            """,
            (message_id,),
        ).fetchone()

    return row is not None


def mark_message_processed(message_id: str) -> None:
    """Mark a message as successfully processed."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO processed_messages
            (message_id, processed_at)
            VALUES (?, ?)
            """,
            (message_id, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()