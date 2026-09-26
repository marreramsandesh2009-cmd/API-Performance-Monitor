import sqlite3

DATABASE = "monitor.db"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS api_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            response_size INTEGER,
            error TEXT,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def save_result(result):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO api_results
        (url, status, status_code, response_time, response_size, error)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            result["url"],
            result["status"],
            result["status_code"],
            result["response_time"],
            result["response_size"],
            result["error"]
        )
    )

    connection.commit()
    connection.close()

def get_results():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM api_results
        ORDER BY id DESC
        LIMIT 100
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]