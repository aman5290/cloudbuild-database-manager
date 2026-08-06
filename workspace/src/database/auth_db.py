"""
============================================================
CloudBuild Database Manager
============================================================

File
----
auth_db.py

Purpose
-------
Contains all database operations related to application
authentication.

Responsibilities
----------------
1. Retrieve user information.
2. Validate login credentials.

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
# Authentication Functions
# ============================================================

def get_user_by_username(username):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve an application user using the username.

    Used during login to verify whether the supplied
    username exists.

    Parameters
    ---------------------------------------------------------
    username : str
        Username entered by the user.

    Returns
    ---------------------------------------------------------
    tuple | None
        User record if found, otherwise None.

    Future Scope
    ---------------------------------------------------------
    - Account lockout
    - Failed login counter
    - MFA
    =========================================================
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    user_id,
                    username,
                    password_hash,
                    full_name,
                    role,
                    is_active
                FROM portal.app_users
                WHERE username = %s;
                """,
                (username,),
            )

            return cur.fetchone()
