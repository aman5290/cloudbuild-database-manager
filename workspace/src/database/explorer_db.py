"""
============================================================
CloudBuild Database Manager
============================================================

File
----
explorer_db.py

Purpose
-------
Database Explorer database operations.

Responsibilities
----------------
1. Retrieve database tables.
2. Retrieve table data.
3. Retrieve table metadata.
4. Retrieve table columns.

============================================================
"""

# ============================================================
# Imports
# ============================================================

from psycopg import sql

from .connection import get_connection


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

            cur.execute(
                """
                SELECT
                    table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
            )

            rows = cur.fetchall()

    tables = [

        row[0]

        for row in rows

    ]

    return tables


# ============================================================
# Retrieve Table Data
# ============================================================

def get_table_data(
    table_name,
    limit=100,
):
    """
    Retrieve data from any PostgreSQL table.
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            query = sql.SQL(
                """
                SELECT *
                FROM {}
                LIMIT %s;
                """
            ).format(
                sql.Identifier(table_name)
            )

            cur.execute(
                query,
                (limit,),
            )

            columns = [

                column.name

                for column in cur.description

            ]

            rows = cur.fetchall()

            return columns, rows



# ============================================================
# Retrieve Table Information
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

            # -------------------------------------------------
            # Total Rows
            # -------------------------------------------------

            query = sql.SQL(
                """
                SELECT COUNT(*)
                FROM {};
                """
            ).format(
                sql.Identifier(table_name)
            )

            cur.execute(query)

            row_count = cur.fetchone()[0]

            # -------------------------------------------------
            # Total Columns
            # -------------------------------------------------

            cur.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_schema='public'
                AND table_name=%s;
                """,
                (table_name,),
            )

            column_count = cur.fetchone()[0]

            # -------------------------------------------------
            # Primary Key
            # -------------------------------------------------

            cur.execute(
                """
                SELECT
                    kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type='PRIMARY KEY'
                  AND tc.table_name=%s
                  AND tc.table_schema='public';
                """,
                (table_name,),
            )

            result = cur.fetchone()

            primary_key = (

                result[0]

                if result

                else "N/A"

            )

            return {

                "row_count": row_count,

                "column_count": column_count,

                "primary_key": primary_key,

            }


# ============================================================
# Retrieve Table Columns
# ============================================================

def get_table_columns(table_name):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve metadata for all columns in a PostgreSQL table.

    Returns
    ---------------------------------------------------------
    list[dict]

    Future Scope
    ---------------------------------------------------------
    - Character length
    - Default value
    - Identity columns
    =========================================================
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                ORDER BY ordinal_position;
                """,
                (table_name,),
            )

            return [

                {

                    "column_name": row[0],

                    "data_type": row[1],

                    "nullable": row[2],

                }

                for row in cur.fetchall()

            ]
