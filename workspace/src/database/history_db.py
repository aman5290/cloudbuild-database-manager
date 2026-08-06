"""
============================================================
CloudBuild Database Manager
============================================================

File
----
history_db.py

Purpose
-------
Contains all Query History database operations.

Responsibilities
----------------
1. Save executed queries.
2. Retrieve query history.

Author
------
Aman

============================================================
"""

# ============================================================
# Imports
# ============================================================

from .connection import get_connection



# ============================================================
# Save Query History
# ============================================================

def save_query_history(
    user_id,
    query_text,
    rows_returned,
    execution_time_ms,
):
    """
    Save a successfully executed SQL query.
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO portal.query_history
                (
                    user_id,
                    query_text,
                    rows_returned,
                    execution_time_ms
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                );
                """,
                (
                    user_id,
                    query_text,
                    rows_returned,
                    execution_time_ms,
                ),
            )

        conn.commit()


# ============================================================
# Get Query History
# ============================================================

def get_query_history(user_id):
    """
    Retrieve SQL query history for a user.
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT

                    history_id,

                    query_text,

                    rows_returned,

                    execution_time_ms,

                    executed_at

                FROM portal.query_history

                WHERE user_id = %s

                ORDER BY executed_at DESC;
                """,
                (
                    user_id,
                ),
            )

            return cur.fetchall()
