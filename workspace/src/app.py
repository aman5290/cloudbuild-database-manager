"""
=============================================================
Project : CloudBuild Database Manager
Version : 6.6.0-alpha1

File    : app.py

Author  : Aman

Purpose
-------
Application entry point.

Responsibilities
----------------
1. Create Flask application
2. Configure application
3. Register Blueprints
4. Configure sessions
5. Provide global template variables

Last Updated
------------
04-Aug-2026
=============================================================
"""

# ============================================================
# Standard Library Imports
# ============================================================


from datetime import (
    datetime,
    timedelta,
    timezone
)

from pathlib import Path

# ============================================================
# Third-Party Imports
# ============================================================

from flask import (
    Flask,
    redirect,
    url_for
)



# ============================================================
# Project Imports
# ============================================================

from src.constants import (
    APP_NAME,
    APP_VERSION,
    SESSION_TIMEOUT_MINUTES,
)


from src.routes import register_blueprints





# ============================================================
# Application Configuration
# ============================================================

# -----------------------------------------------------------
# Calculate workspace root directory
# -----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent




# -----------------------------------------------------------
# Create Flask application
# -----------------------------------------------------------
app = Flask(
    __name__,
    template_folder=BASE_DIR / "templates",
    static_folder=BASE_DIR / "static"
)




# -----------------------------------------------------------
# Register Application Blueprints
# -----------------------------------------------------------

register_blueprints(app)




# ============================================================
# Global Template Variables
# ============================================================

@app.context_processor
def inject_app_info():

    return {

        "app_name": APP_NAME,

        "app_version": APP_VERSION,

        "session_timeout_minutes": int(
            SESSION_TIMEOUT.total_seconds() / 60
        ),

    }



# -----------------------------------------------------------
# Flask Secret Key
# -----------------------------------------------------------
#
# Read the secret key from the environment.
# This keeps sensitive information outside
# the application source code.
#
from src.config import FLASK_SECRET_KEY

app.secret_key = FLASK_SECRET_KEY


# -----------------------------------------------------------
# Session Configuration
# -----------------------------------------------------------
#
# Automatically log out users after 5 minutes
# of inactivity.
#
SESSION_TIMEOUT = timedelta(

    minutes=SESSION_TIMEOUT_MINUTES

)


# ============================================================
# Public Routes
# ============================================================

# -----------------------------------------------------------
# Home Page
# -----------------------------------------------------------
@app.route("/")
def home():
    """
    Redirect users to the login page.
    """

    return redirect(
        url_for("auth.login")
    )







    






# -----------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
