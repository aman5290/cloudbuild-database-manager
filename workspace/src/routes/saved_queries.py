"""
============================================================
CloudBuild Database Manager
============================================================

File
----
saved_queries.py

Purpose
-------
Manage all Saved Query operations.

Responsibilities
----------------
1. Display Saved Queries
2. Create a Saved Query
3. Edit a Saved Query
4. Delete a Saved Query
5. Run a Saved Query

============================================================
"""

# ============================================================
# Flask Imports
# ============================================================

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# ============================================================
# Project Imports
# ============================================================

from src.database.db import (
    save_query,
    get_saved_queries,
    get_saved_query_by_id,
    update_saved_query,
    delete_saved_query,
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

saved_queries_bp = Blueprint(

    "saved_queries",

    __name__,

)

# ============================================================
# Saved Queries
# ============================================================

@saved_queries_bp.route("/saved-queries")
@login_required
def saved_queries():
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Display all saved SQL queries for the current user.

    Responsibilities
    ---------------------------------------------------------
    1. Read saved queries from PostgreSQL.
    2. Filter queries using the search text.
    3. Display matching saved queries.

    Future Scope
    ---------------------------------------------------------
    - Pagination
    - Sort by name
    - Sort by last updated
    - Search by SQL text
    =========================================================
    """

    # -------------------------------------------------------
    # Read search text from the URL.
    # -------------------------------------------------------

    search = request.args.get(
        "search",
        ""
    ).strip()

    # -------------------------------------------------------
    # Retrieve saved queries.
    # -------------------------------------------------------

    queries = get_saved_queries(
        session["user_id"]
    )

    # -------------------------------------------------------
    # Filter by query name.
    # -------------------------------------------------------

    queries = filter_items(

        queries,

        search,

        key=lambda query: query[1]

    )

    # -------------------------------------------------------
    # Render page.
    # -------------------------------------------------------

    return render_template(

        "saved-queries.html",

        queries=queries,

        search=search,

        search_title="Search Saved Queries",

        search_placeholder="Search query name..."

    )


# ============================================================
# New Saved Query
# ============================================================

@saved_queries_bp.route(
    "/saved-query/new",
    methods=["POST"],
)
@login_required
def new_saved_query():

    save_query(

        session["user_id"],

        request.form["query_name"],

        request.form["query_text"],

    )

    flash(

        "Query saved successfully.",

        "success",

    )

    return redirect(

        url_for("saved_queries.saved_queries")

    )


# ============================================================
# Delete Saved Query
# ============================================================

@saved_queries_bp.route(
    "/saved-query/delete/<int:saved_query_id>",
    methods=["POST"],
)
@login_required
def remove_saved_query(saved_query_id):

    delete_saved_query(

        saved_query_id,

        session["user_id"],

    )

    flash(

        "Saved query deleted successfully.",

        "success",

    )

    return redirect(

        url_for("saved_queries.saved_queries")

    )


# ============================================================
# Run Saved Query
# ============================================================

@saved_queries_bp.route(
    "/saved-query/run/<int:saved_query_id>"
)
@login_required
def run_saved_query(saved_query_id):

    query = get_saved_query_by_id(

        saved_query_id,

        session["user_id"],

    )

    if query is None:

        flash(

            "Saved query not found.",

            "error",

        )

        return redirect(

            url_for("saved_queries.saved_queries")

        )

    session["loaded_query"] = query[2]

    return redirect(

        url_for("workspace.sql_workspace")

    )


# ============================================================
# Edit Saved Query
# ============================================================

@saved_queries_bp.route(
    "/saved-query/edit/<int:saved_query_id>",
    methods=["GET", "POST"],
)
@login_required
def edit_saved_query(saved_query_id):

    if request.method == "POST":

        update_saved_query(

            saved_query_id,

            session["user_id"],

            request.form["query_name"],

            request.form["query_text"],

        )

        flash(

            "Saved query updated successfully.",

            "success",

        )

        return redirect(

            url_for("saved_queries.saved_queries")

        )

    query = get_saved_query_by_id(

        saved_query_id,

        session["user_id"],

    )

    return render_template(

        "saved-query-form.html",

        query=query,

    )
