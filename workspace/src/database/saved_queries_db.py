"""
============================================================
CloudBuild Database Manager
============================================================

File
----
saved_queries_db.py

Purpose
-------
Contains all Saved Query database operations.

Responsibilities
----------------
1. Save a query
2. Retrieve saved queries
3. Retrieve one saved query
4. Update a saved query
5. Delete a saved query

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
# Save Query
# ============================================================

def save_query(
    user_id: int,
    query_name: str,
    query_text: str,
) -> None:
    """
    Save a reusable SQL query.
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO portal.saved_queries
                (
                    user_id,
                    query_name,
                    query_text
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                );
                """,
                (
                    user_id,
                    query_name,
                    query_text,
                ),
            )

        conn.commit()


# ============================================================
# Get Saved Queries
# ============================================================

def get_saved_queries(user_id: int):

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    saved_query_id,
                    query_name,
                    query_text,
                    created_at,
                    updated_at
                FROM portal.saved_queries
                WHERE user_id = %s
                ORDER BY updated_at DESC;
                """,
                (
                    user_id,
                ),
            )

            return cur.fetchall()


# ============================================================
# Get Saved Query By ID
# ============================================================

def get_saved_query_by_id(
    saved_query_id: int,
    user_id: int,
):

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    saved_query_id,
                    query_name,
                    query_text
                FROM portal.saved_queries
                WHERE
                    saved_query_id = %s
                AND
                    user_id = %s;
                """,
                (
                    saved_query_id,
                    user_id,
                ),
            )

            return cur.fetchone()


# ============================================================
# Update Saved Query
# ============================================================

def update_saved_query(
    saved_query_id: int,
    user_id: int,
    query_name: str,
    query_text: str,
):

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                UPDATE portal.saved_queries
                SET
                    query_name = %s,
                    query_text = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE
                    saved_query_id = %s
                AND
                    user_id = %s;
                """,
                (
                    query_name,
                    query_text,
                    saved_query_id,
                    user_id,
                ),
            )

        conn.commit()


# ============================================================
# Delete Saved Query
# ============================================================

def delete_saved_query(
    saved_query_id: int,
    user_id: int,
):

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                DELETE FROM portal.saved_queries
                WHERE
                    saved_query_id = %s
                AND
                    user_id = %s;
                """,
                (
                    saved_query_id,
                    user_id,
                ),
            )

        conn.commit()
