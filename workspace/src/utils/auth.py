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

Future Scope
------------
- Role based access control (RBAC)
- Permission decorators
- Admin only routes
- Audit logging

============================================================
"""

from functools import wraps

from flask import (

    flash,

    redirect,

    session,

    url_for,

)


# ============================================================
# Login Required Decorator
# ============================================================

def login_required(view):
    """
    Ensure that the current user is authenticated.

    If the session does not contain a logged-in user,
    redirect the user to the Login page.

    Parameters
    ----------
    view : function
        Flask view function.

    Returns
    -------
    function
        Wrapped Flask view.
    """

    @wraps(view)
    def wrapper(*args, **kwargs):

        # ----------------------------------------------------
        # Verify that the user is logged in.
        # ----------------------------------------------------

        if "user_id" not in session:

            flash(

                "Please log in to continue.",

                "error"

            )

            return redirect(

                url_for("login")

            )

        return view(*args, **kwargs)

    return wrapper
