"""
============================================================
CloudBuild Database Manager
============================================================

Dashboard Routes

Purpose
-------
Contains dashboard-related routes.

============================================================
"""

from flask import (
    Blueprint,
    render_template,
)

from src.utils.auth import login_required


# ============================================================
# Blueprint
# ============================================================

dashboard_bp = Blueprint(

    "dashboard",

    __name__,

)


# ============================================================
# Dashboard
# ============================================================

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Display the application dashboard.
    """

    return render_template(

        "dashboard.html"

    )
