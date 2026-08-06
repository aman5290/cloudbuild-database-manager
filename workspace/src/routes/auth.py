"""
============================================================
CloudBuild Database Manager
============================================================

Authentication Routes

Purpose
-------
Contains login and logout routes.

============================================================
"""

from datetime import (
    datetime,
    timezone,
)

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from src.database.db import (
    get_user_by_username,
)

from src.utils.auth import (
    verify_password,
)


from src.services.auth_service import (
    authenticate_user,
    create_user_session,
)


# ============================================================
# Blueprint
# ============================================================

auth_bp = Blueprint(

    "auth",

    __name__,

)


# ============================================================
# Login
# ============================================================

@auth_bp.route(

    "/login",

    methods=["GET", "POST"]

)
def login():
    """
    Display the Login page and authenticate users.
    """

    # -------------------------------------------------------
    # Display Login Page
    # -------------------------------------------------------

    if request.method == "GET":

        return render_template(

            "login.html",

            message=request.args.get("message")

        )

    # -------------------------------------------------------
    # Read user credentials.
    # -------------------------------------------------------

    username = request.form.get(

        "username"

    )

    password = request.form.get(

        "password"

    )

    # -------------------------------------------------------
    # Retrieve user.
    # -------------------------------------------------------

    success, user, error = authenticate_user(

        username,

        password,

    )

    if not success:

        return render_template(

            "login.html",

            error=error,

        )

    create_user_session(

        session,

    user,

    )

    flash(

        "Login successful.",

        "success",

    )

    return redirect(

        url_for("dashboard.dashboard")

    )


# ============================================================
# Logout
# ============================================================

@auth_bp.route(

    "/logout"

)
def logout():
    """
    End the current user session.
    """

    session.clear()

    flash(

        "You have been logged out.",

        "info",

    )

    return redirect(

        url_for("auth.login")

    )
