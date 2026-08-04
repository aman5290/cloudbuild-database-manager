"""
=============================================================
Project : Pagila PostgreSQL Web Portal

Version : 4.0.0

File    : password.py

Author  : Aman

Purpose
-------
Provides helper functions for password hashing
and password verification using bcrypt.

Responsibilities
----------------
1. Generate bcrypt password hashes.
2. Verify user passwords.
3. Keep authentication logic separate
   from application routes.

Future Scope
------------
- Password strength validation
- Password expiry
- Password history
- Password reset tokens

Last Updated
------------
04-Aug-2026
=============================================================
"""

import bcrypt


# -----------------------------------------------------------
# Generate Password Hash
# -----------------------------------------------------------
def hash_password(password):
    """
    Generate a bcrypt hash for a plain-text password.

    Parameters
    ----------
    password : str
        Plain-text password entered by the user.

    Returns
    -------
    str
        Secure bcrypt hash.
    """

    # Convert string to bytes
    password_bytes = password.encode("utf-8")

    # Generate salt automatically
    salt = bcrypt.gensalt()

    # Create bcrypt hash
    hashed_password = bcrypt.hashpw(
        password_bytes,
        salt
    )

    # Convert bytes back to string
    return hashed_password.decode("utf-8")


# -----------------------------------------------------------
# Verify Password
# -----------------------------------------------------------
def verify_password(password, stored_hash):
    """
    Compare a plain-text password with
    a stored bcrypt hash.

    Parameters
    ----------
    password : str
        Password entered during login.

    stored_hash : str
        Password hash stored in PostgreSQL.

    Returns
    -------
    bool
        True if password matches.
        False otherwise.
    """

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_hash.encode("utf-8")
    )
