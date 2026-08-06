"""
============================================================
CloudBuild Database Manager
============================================================

Connection Functions

Purpose
-------
Create PostgreSQL database connections.

============================================================
"""

import psycopg

from src.config import DB_CONFIG


# ============================================================
# Get Database Connection
# ============================================================

def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    return psycopg.connect(
        **DB_CONFIG
    )
