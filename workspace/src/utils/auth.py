"""
============================================================
CloudBuild Database Manager
============================================================

Authentication Utilities

Purpose
-------
Reusable authentication helpers and decorators.

Current Features
----------------
✓ Login required decorator
✓ Password hashing
✓ Password verification

Future Scope
------------
- Role based access control (RBAC)
- Permission decorators
- Admin only routes
- Audit logging

============================================================
"""

from functools import wraps

import bcrypt

from flask import (
    flash,
    redirect,
    session,
    url_for,
)


# ============================================================
# Hash Password
# ============================================================

def hash_password(password):
    """
    Generate a bcrypt hash for a password.
    """

    return bcrypt.hashpw(

        password.encode("utf-8"),

        bcrypt.gensalt()

    ).decode("utf-8")


# ============================================================
# Verify Password
# ============================================================

def verify_password(
    password,
    password_hash,
):
    """
    Verify a password against a bcrypt hash.
    """

    return bcrypt.checkpw(

        password.encode("utf-8"),

        password_hash.encode("utf-8")

    )


# ============================================================
# Login Required Decorator
# ============================================================

def login_required(view):
    """
    Ensure that the current user is authenticated.
    """

    @wraps(view)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash(

                "Please log in to continue.",

                "error",

            )

            return redirect(

                url_for("login")

            )

        return view(*args, **kwargs)

    return wrapper
