"""
============================================================
CloudBuild Database Manager
============================================================

Route Registration

Purpose
-------
Registers all application blueprints.

============================================================
"""

# ============================================================
# Import Blueprints
# ============================================================

from src.routes.auth import auth_bp
from src.routes.dashboard import dashboard_bp
from src.routes.database import database_bp


# ============================================================
# Register Blueprints
# ============================================================

def register_blueprints(app):
    """
    Register all application blueprints.
    """

    app.register_blueprint(auth_bp)

    app.register_blueprint(dashboard_bp)
    
    app.register_blueprint(database_bp)
