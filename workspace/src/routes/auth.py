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

# ============================================================
# Imports
# ============================================================

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

from src.database.auth_db import (
    get_user_by_username,
)

from src.utils.auth import (
    verify_password,
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
    methods=["GET", "POST"],
)
def login():
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Display the Login page and authenticate users.

    URL
    ---------------------------------------------------------
    /login

    HTTP Methods
    ---------------------------------------------------------
    GET
        Display Login page.

    POST
        Authenticate the user.

    =========================================================
    """

    # -------------------------------------------------------
    # Display Login Page
    # -------------------------------------------------------

    if request.method == "GET":

        return render_template(

            "login.html",

            message=request.args.get("message"),

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

    user = get_user_by_username(

        username

    )

    # -------------------------------------------------------
    # User not found.
    # -------------------------------------------------------

    if user is None:

        return render_template(

            "login.html",

            error="Invalid username or password.",

        )

    # -------------------------------------------------------
    # Verify password.
    # -------------------------------------------------------

    stored_hash = user[2]

    if not verify_password(

        password,

        stored_hash,

    ):

        return render_template(

            "login.html",

            error="Invalid username or password.",

        )

    # -------------------------------------------------------
    # Create authenticated session.
    # -------------------------------------------------------

    session.clear()

    session.permanent = True

    session["user_id"] = user[0]

    session["username"] = user[1]

    session["last_activity"] = datetime.now(

        timezone.utc

    ).isoformat()

    # -------------------------------------------------------
    # Success message.
    # -------------------------------------------------------

    flash(

        "Login successful.",

        "success",

    )

    # -------------------------------------------------------
    # Redirect to Dashboard.
    # -------------------------------------------------------

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
    =========================================================
    Purpose
    ---------------------------------------------------------
    End the current authenticated session.
    =========================================================
    """

    session.clear()

    flash(

        "You have been logged out.",

        "info",

    )

    return redirect(

        url_for("auth.login")

    )
