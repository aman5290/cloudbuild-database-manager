"""
=============================================================
Project : Pagila PostgreSQL Web Portal

Version : 6.1.3

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

import time

import psycopg
from psycopg import sql


from src.config import DB_CONFIG

# ============================================================
# Connection Functions
# ============================================================

def get_connection():
    """
    Create and return a PostgreSQL connection.
    """

    return psycopg.connect(**DB_CONFIG)

# ============================================================
# Authentication Functions
# ============================================================

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

# ============================================================
# Legacy Actor Functions
# ============================================================

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

# ============================================================
# Database Explorer Functions
# ============================================================

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

# ============================================================
# Metadata Functions
# ============================================================

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
                        





# -----------------------------------------------------------
# Retrieve Table Columns
# -----------------------------------------------------------

def get_table_columns(table_name):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve metadata for all columns in a PostgreSQL table.

    Parameters
    ---------------------------------------------------------
    table_name : str

    Returns
    ---------------------------------------------------------
    list[dict]

    Example
    ---------------------------------------------------------
    [
        {
            "column_name": "actor_id",
            "data_type": "integer",
            "nullable": "NO"
        }
    ]

    Future Scope
    ---------------------------------------------------------
    - Character length
    - Default value
    - Identity columns
    =========================================================
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))

            return [
                {
                    "column_name": row[0],
                    "data_type": row[1],
                    "nullable": row[2]
                }
                for row in cur.fetchall()
            ]
            




# -----------------------------------------------------------
# Execute SELECT Query
# -----------------------------------------------------------

# ============================================================
# SQL Workspace Functions
# ============================================================

def execute_select_query(query):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Execute a read-only SQL query.

    Parameters
    ---------------------------------------------------------
    query : str

    Returns
    ---------------------------------------------------------
    Dictionary containing:
        - columns
        - rows
        - row_count
        - column_count
        - execution_time_ms

    Security
    ---------------------------------------------------------
    Only SELECT statements are permitted.

    Future Scope
    ---------------------------------------------------------
    - Query History
    - Pagination
    - Export CSV
    =========================================================
    """

    # -------------------------------------------------------
    # Remove unnecessary whitespace.
    # -------------------------------------------------------
    query = query.strip().rstrip(";")

    # -------------------------------------------------------
    # Validate query.
    # -------------------------------------------------------
    if not query.lower().startswith("select"):

        raise ValueError(
            "Only SELECT statements are allowed."
        )

    with get_connection() as conn:

        with conn.cursor() as cur:

            # ---------------------------------------------------
            # Start execution timer.
            # ---------------------------------------------------
            start_time = time.perf_counter()

            # ---------------------------------------------------
            # Execute query.
            # ---------------------------------------------------
            cur.execute(query)

            # ---------------------------------------------------
            # Retrieve column names.
            # ---------------------------------------------------
            columns = [
                column.name
                for column in cur.description
            ]

            # ---------------------------------------------------
            # Retrieve all rows.
            # ---------------------------------------------------
            rows = cur.fetchall()

            # ---------------------------------------------------
            # Stop execution timer.
            # ---------------------------------------------------
            end_time = time.perf_counter()

            # ---------------------------------------------------
            # Calculate execution time.
            # ---------------------------------------------------
            execution_time_ms = (
                end_time - start_time
            ) * 1000

            # ---------------------------------------------------
            # Return query results.
            # ---------------------------------------------------
            return {

                "columns": columns,

                "rows": rows,

                "row_count": len(rows),

                "column_count": len(columns),

                "execution_time_ms": round(
                    execution_time_ms,
                    2
                )

            }
            
            
            


# ============================================================
# Query History Functions
# ============================================================

# -----------------------------------------------------------
# Save Query History
# -----------------------------------------------------------

# ============================================================
# Query History Functions
# ============================================================

def save_query_history(
    user_id,
    query_text,
    rows_returned,
    execution_time_ms
):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Save a successfully executed SQL query.

    Parameters
    ---------------------------------------------------------
    user_id : int

    query_text : str

    rows_returned : int

    execution_time_ms : float

    Returns
    ---------------------------------------------------------
    None

    Future Scope
    ---------------------------------------------------------
    - Save failed queries
    - Database name
    - Client IP
    =========================================================
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
                    execution_time_ms
                )
            )

        conn.commit()





# ============================================================
# Get Query History
# ============================================================

def get_query_history(user_id):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve SQL query history for a user.

    Parameters
    ---------------------------------------------------------
    user_id : int

    Returns
    ---------------------------------------------------------
    list

    Future Scope
    ---------------------------------------------------------
    - Pagination
    - Search
    - Filter by date
    =========================================================
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
                (user_id,)
            )

            return cur.fetchall()




# ============================================================
# Save Query
# ============================================================

def save_query(
    user_id: int,
    query_name: str,
    query_text: str
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
                ORDER BY query_name;
                """,
                (user_id,),
            )

            return cur.fetchall()




# ============================================================
# Get Saved Query By ID
# ============================================================

def get_saved_query_by_id(
    saved_query_id: int,
    user_id: int
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




                