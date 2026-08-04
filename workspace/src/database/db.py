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
from psycopg import sql


from src.config import DB_CONFIG


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
            




# -----------------------------------------------------------
# Retrieve Database Tables
# -----------------------------------------------------------
def get_database_tables():
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve all user tables from the PostgreSQL database.

    Returns
    ---------------------------------------------------------
    list
        A list containing table names.

    Notes
    ---------------------------------------------------------
    Only tables from the 'public' schema are returned.

    Future Scope
    ---------------------------------------------------------
    - Support multiple schemas
    - Filter system tables
    - Include row counts
    =========================================================
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)

            return cur.fetchall()




# -----------------------------------------------------------
# Retrieve Table Data
# -----------------------------------------------------------
def get_table_data(table_name, limit=100):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve data from any PostgreSQL table.

    Parameters
    ---------------------------------------------------------
    table_name : str
        Name of the table.

    limit : int
        Maximum number of rows.

    Returns
    ---------------------------------------------------------
    tuple
        (columns, rows)

    =========================================================
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Build a safe SQL statement.
            query = sql.SQL("""
                SELECT *
                FROM {}
                LIMIT %s;
            """).format(
                sql.Identifier(table_name)
            )

            cur.execute(query, (limit,))

            columns = [
                column.name
                for column in cur.description
            ]

            rows = cur.fetchall()

            return columns, rows




# -----------------------------------------------------------
# Retrieve Table Information
# -----------------------------------------------------------
def get_table_information(table_name):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve metadata for a PostgreSQL table.

    Returns
    ---------------------------------------------------------
    Dictionary containing:

    - Row count
    - Column count
    - Primary key

    Future Scope
    ---------------------------------------------------------
    - Indexes
    - Foreign Keys
    - Table Size
    =========================================================
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            # ---------------------------------------------
            # Total Rows
            # ---------------------------------------------
            query = sql.SQL("""
                SELECT COUNT(*)
                FROM {};
            """).format(
                sql.Identifier(table_name)
            )

            cur.execute(query)

            row_count = cur.fetchone()[0]

            # ---------------------------------------------
            # Total Columns
            # ---------------------------------------------
            cur.execute("""
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_schema='public'
                AND table_name=%s;
            """, (table_name,))

            column_count = cur.fetchone()[0]

            # ---------------------------------------------
            # Primary Key
            # ---------------------------------------------
            cur.execute("""
                SELECT
                    kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type='PRIMARY KEY'
                  AND tc.table_name=%s
                  AND tc.table_schema='public';
            """, (table_name,))

            result = cur.fetchone()

            primary_key = result[0] if result else "N/A"

            return {
                "row_count": row_count,
                "column_count": column_count,
                "primary_key": primary_key
            }
                        