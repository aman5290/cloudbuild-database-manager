"""
============================================================
CloudBuild Database Manager
============================================================

File
----
workspace_db.py

Purpose
-------
Contains all SQL Workspace database operations.

Responsibilities
----------------
1. Execute read-only SQL queries.

Author
------
Aman

============================================================
"""

# ============================================================
# Imports
# ============================================================

import time

from .connection import get_connection


# ============================================================
# Execute SELECT Query
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
    dict

        {
            columns,
            rows,
            row_count,
            column_count,
            execution_time_ms
        }

    Security
    ---------------------------------------------------------
    Only SELECT statements are permitted.

    =========================================================
    """

    # -------------------------------------------------------
    # Remove whitespace and trailing semicolon.
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
            # Start timer.
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
            # Stop timer.
            # ---------------------------------------------------

            end_time = time.perf_counter()

            execution_time_ms = (

                end_time - start_time

            ) * 1000

            return {

                "columns": columns,

                "rows": rows,

                "row_count": len(rows),

                "column_count": len(columns),

                "execution_time_ms": round(

                    execution_time_ms,

                    2,

                ),

            }
