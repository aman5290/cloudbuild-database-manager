"""
============================================================
CloudBuild Database Manager
============================================================

Database Routes

Purpose
-------
Database Explorer and Generic Table Viewer.

============================================================
"""

from flask import (
    Blueprint,
    render_template,
    request,
)

from src.database.db import (
    get_database_tables,
    get_table_data,
    get_table_information,
    get_table_columns,
)

from src.utils.auth import (
    login_required,
)

from src.utils.search import (
    filter_items,
)

# ============================================================
# Blueprint
# ============================================================

database_bp = Blueprint(
    "database",
    __name__,
)

# -----------------------------------------------------------
# Database Explorer
# -----------------------------------------------------------
@database_bp.route("/database-explorer")
@login_required
def database_explorer():
    """
    Display Database Explorer.
    """

    search = request.args.get(
        "search",
        ""
    ).strip()

    tables = get_database_tables()

    tables = filter_items(
        tables,
        search,
    )

    return render_template(
        "database-explorer.html",
        tables=tables,
        search=search,
        search_title="Search Tables",
        search_placeholder="Search table name...",
    )


# -----------------------------------------------------------
# Generic Table Viewer
# -----------------------------------------------------------
@database_bp.route("/table/<table_name>")
@login_required
def table_view(table_name):
    """
    Display any PostgreSQL table.
    """

    try:

        columns, rows = get_table_data(
            table_name
        )

        column_info = get_table_columns(
            table_name
        )

        table_info = get_table_information(
            table_name
        )

    except Exception as error:

        return (
            f"Unable to display table.<br><br>"
            f"Error : {error}",
            500,
        )

    return render_template(
        "table-view.html",
        table_name=table_name,
        table_info=table_info,
        column_info=column_info,
        columns=columns,
        rows=rows,
    )
