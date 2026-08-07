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
    jsonify,
)

from src.database.db import (
    get_database_objects,
    get_table_statistics,
    get_table_data,
    get_table_information,
    get_table_columns,
    get_database_summary,
)

from src.utils.auth import (
    login_required,
)

from src.utils.search import (
    filter_items,
)



from src.database.database_explorer_db import (
    get_object_details,
    get_object_ddl,
    get_relationships,
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

    
    
    database_objects = get_database_objects()

    database_summary = get_database_summary()

    table_statistics = get_table_statistics()

    database_objects["tables"] = filter_items(
        database_objects["tables"],
        search,
    )

    database_objects["views"] = filter_items(
        database_objects["views"],
        search,
    )

    database_objects["functions"] = filter_items(
        database_objects["functions"],
        search,
    )

    database_objects["sequences"] = filter_items(
        database_objects["sequences"],
        search,
    )



    return render_template(
        "database-explorer.html",
        database_objects=database_objects,
        database_summary=database_summary,
        table_statistics=table_statistics,
        search=search,
        search_title="Search Database Objects",
        search_placeholder="Search database objects..."
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




# -----------------------------------------------------------
# Load Metadata (AJAX)
# -----------------------------------------------------------

@database_bp.route("/object-details", methods=["GET"])
@login_required
def object_details():

    object_type = request.args.get("type")
    object_name = request.args.get("name")

    data = get_object_details(
        object_type,
        object_name
    )

    return jsonify(data)






@database_bp.route("/object-ddl")
@login_required
def object_ddl():

    object_type = request.args.get("type")
    object_name = request.args.get("name")

    ddl = get_object_ddl(
        object_type,
        object_name
    )

    return jsonify({

        "ddl": ddl

    })






@database_bp.route("/object-relationships")
@login_required
def object_relationships():

    table = request.args.get("name")

    return jsonify(

        get_relationships(table)

    )
