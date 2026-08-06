from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Response,
    session
)



from src.database.db import (
    execute_select_query,
    save_query_history,
    get_query_history,
)



from src.utils.auth import (
    login_required,
)




workspace_bp = Blueprint(
    "workspace",
    __name__,
)



# ============================================================
# SQL Workspace
# ============================================================

@workspace_bp.route(
    "/sql-workspace",
    methods=["GET", "POST"]
)
@login_required
def sql_workspace():
    """
    ============================================================
    Purpose
    ------------------------------------------------------------
    Display the SQL Workspace and execute user-provided SQL
    queries.

    Current Features
    ------------------------------------------------------------
    ✓ Execute SELECT queries
    ✓ Display execution statistics
    ✓ Display query results
    ✓ Automatically save Query History
    ✓ Load queries from Saved Queries

    Future Scope
    ------------------------------------------------------------
    - Flash messages
    - Export results
    - Syntax highlighting
    - Auto complete
    ============================================================
    """

    # ------------------------------------------------------------
    # Ensure the user is authenticated.
    # ------------------------------------------------------------

    #if "user_id" not in session:
    #    return redirect(url_for("auth.login"))

    # ------------------------------------------------------------
    # Load a query from the session.
    #
    # This is used when the user clicks "Run" from the
    # Saved Queries page.
    #
    # session.pop() removes the value after it is read so that
    # refreshing the page does not reload the same query.
    # ------------------------------------------------------------

    query = session.pop(
        "loaded_query",
        ""
    )

    # ------------------------------------------------------------
    # Default page values.
    # ------------------------------------------------------------

    result = None

    error = None

    # ------------------------------------------------------------
    # Execute the submitted SQL query.
    # ------------------------------------------------------------

    if request.method == "POST":

        # --------------------------------------------------------
        # Read the SQL query entered by the user.
        # --------------------------------------------------------

        query = request.form.get(
            "query",
            ""
        ).strip()

        # --------------------------------------------------------
        # Validate that a query has been entered.
        # --------------------------------------------------------

        if not query:

            error = "Please enter a SQL query."

        else:

            try:

                # ------------------------------------------------
                # Execute the SQL query.
                # ------------------------------------------------

                result = execute_select_query(query)

                if result is None:

                    flash(

                        "Unable to execute query.",

                        "danger",

                    )

                    return redirect(

                        url_for("workspace.sql_workspace")

                    )

                if "error" in result:

                    flash(

                        result["error"],

                        "danger",

                    )

                    return redirect(

                        url_for("workspace.sql_workspace")

                    )

                # ------------------------------------------------
                # Automatically save successful queries to
                # Query History.
                # ------------------------------------------------

                save_query_history(

                    user_id=session["user_id"],

                    query_text=query,

                    rows_returned=result["row_count"],

                    execution_time_ms=result["execution_time_ms"]

                )

            except Exception as error_exception:

                # --------------------------------------------
                # Display the database error.
                # --------------------------------------------

                flash(
                    str(error_exception),
                    "error",
                )

                error = str(error_exception)

    # ------------------------------------------------------------
    # Render the SQL Workspace.
    # ------------------------------------------------------------

    return render_template(

        "sql-workspace.html",

        query=query,

        result=result,

        error=error,

        recent_queries=get_query_history(
            session["user_id"]
        )[:10],

    )






@workspace_bp.route(
    "/export/csv",
    methods=["POST"],
)
@login_required
def export_csv():

    query = request.form.get("query")

    result = execute_select_query(query)

    if "error" in result:

        flash(result["error"], "danger")

        return redirect(
            url_for("workspace.sql_workspace")
        )

    import csv
    import io

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(result["columns"])

    writer.writerows(result["rows"])

    output.seek(0)

    return Response(

        output.getvalue(),

        mimetype="text/csv",

        headers={

            "Content-Disposition":
                "attachment; filename=query_results.csv"

        }

    )
