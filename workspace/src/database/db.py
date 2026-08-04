"""
=============================================================
Project : Pagila PostgreSQL Web Portal

Version : 3.0.0

File    : db.py

Author  : Aman

Purpose
-------
Contains all PostgreSQL database operations.

Responsibilities
----------------
1. Create database connection
2. Retrieve one actor
3. Retrieve all actors

Last Updated
------------
04-Aug-2026
=============================================================
"""

import psycopg

from config import DB_CONFIG


def get_connection():
    """
    Create and return a PostgreSQL connection.
    """

    return psycopg.connect(**DB_CONFIG)


def get_actor_by_id(actor_id):
    """
    Retrieve one actor using Actor ID.
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    actor_id,
                    first_name,
                    last_name
                FROM actor
                WHERE actor_id = %s;
            """, (actor_id,))

            return cur.fetchone()


def get_all_actors():
    """
    Retrieve all actors along with column names.

    Returns
    -------
    tuple
        (
            columns,
            rows
        )
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    actor_id,
                    first_name,
                    last_name
                FROM actor
                ORDER BY actor_id;
            """)

            # Fetch all rows
            rows = cur.fetchall()

            # Read column names returned by PostgreSQL
            columns = [column.name for column in cur.description]

            return columns, rows
            



# -----------------------------------------------------------
# Get Application User
# -----------------------------------------------------------
def get_user_by_username(username):
    """
    Retrieve an application user using the username.

    Purpose
    -------
    Used during the login process to verify whether
    the supplied username exists.

    Parameters
    ----------
    username : str
        Username entered on the login page.

    Returns
    -------
    tuple | None
        User record if found, otherwise None.

    Future Scope
    ------------
    - Password hashing (bcrypt)
    - Account lock
    - Failed login counter
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    user_id,
                    username,
                    password_hash,
                    full_name,
                    role,
                    is_active
                FROM portal.app_users
                WHERE username = %s;
            """, (username,))

            return cur.fetchone()