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
from src.routes.workspace import workspace_bp
from src.routes.history import history_bp
from src.routes.saved_queries import saved_queries_bp


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
    
    app.register_blueprint(workspace_bp)
    
    app.register_blueprint(history_bp)
    
    app.register_blueprint(saved_queries_bp)
