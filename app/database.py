"""
Database module - simple SQLite storage for meeting history.
No ORM, just plain sqlite3 to keep things easy to read.
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "data/meetings.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            transcript TEXT,
            summary TEXT,
            decisions TEXT,
            action_items TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_meeting(filename, transcript, summary, decisions, action_items) -> int:
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO meetings (filename, transcript, summary, decisions, action_items, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            transcript,
            summary,
            json.dumps(decisions),
            json.dumps(action_items),
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    meeting_id = cursor.lastrowid
    conn.close()
    return meeting_id


def get_all_meetings():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, filename, summary, created_at FROM meetings ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_meeting(meeting_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM meetings WHERE id = ?", (meeting_id,)
    ).fetchone()
    conn.close()

    if row is None:
        return {"error": "Meeting not found"}

    meeting = dict(row)
    meeting["decisions"] = json.loads(meeting["decisions"])
    meeting["action_items"] = json.loads(meeting["action_items"])
    return meeting
