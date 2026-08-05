"""
=============================================================
Project : Pagila PostgreSQL Web Portal

Version : 6.1.3

File    : app.py

Author  : Aman

Purpose
-------
Main Flask application.

Responsibilities
----------------
1. Start Flask
2. Render HTML pages
3. Handle HTTP requests
4. Call database functions

Last Updated
------------
04-Aug-2026
=============================================================
"""

# ============================================================
# Standard Library Imports
# ============================================================

from datetime import datetime, timedelta, timezone

from pathlib import Path

# ============================================================
# Third-Party Imports
# ============================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)


from src.constants import (
    APP_NAME,
    APP_VERSION,
    SESSION_TIMEOUT_MINUTES,
)


# ============================================================
# Project Imports
# ============================================================

from src.database.db import (
#    get_actor_by_id,
#    get_all_actors,
    get_user_by_username,
    get_database_tables,
    get_table_data,
    get_table_information,
    get_table_columns,
    execute_select_query,
    save_query_history,
    get_query_history,
    save_query,
    get_saved_queries,
    get_saved_query_by_id,
    update_saved_query,
    delete_saved_query
)

from src.utils.auth import login_required

from src.utils.password import verify_password


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
        url_for("login")
    )


# -----------------------------------------------------------
# Search One Actor
# -----------------------------------------------------------
#@app.route("/actor")
#def actor_search():
#    """
#    Search actor using Actor ID.
#    """

#    actor_id = request.args.get("actor_id", type=int)

#    if actor_id is None:
#        return "Actor ID is required.", 400

#    actor = get_actor_by_id(actor_id)

#    return render_template(
#        "actor.html",
#        actor=actor
#    )


# -----------------------------------------------------------
# View All Actors
# -----------------------------------------------------------
#@app.route("/actors")
#def actor_list():
#    """
#    Display all actors.
#    """

#    columns, rows = get_all_actors()

#    return render_template(
#        "actor-list.html",
#        columns=columns,
#        rows=rows
#    )



# ============================================================
# Authentication Routes
# ============================================================

# -----------------------------------------------------------
# Login Page
# -----------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Purpose
    -------
    Display the login page and authenticate users.

    URL
    ---
    /login

    HTTP Methods
    ------------
    GET
        Display login form.

    POST
        Validate username and password.

    Future Scope
    ------------
    - Flask Session
    - Remember Me
    - MFA
    """

    # -----------------------------------------------------------
    # Display Login Page
    # -----------------------------------------------------------
    #
    # If this is a GET request, simply display
    # the login page.
    #
    if request.method == "GET":

        # Read any message passed through the URL.
        message = request.args.get("message")

        return render_template(
            "login.html",
            message=message
        )

    # -----------------------------------------------------------
    # Process Login Request (POST)
    # -----------------------------------------------------------
    #
    # If execution reaches here, the request
    # method is POST and we must authenticate
    # the user.
    #

    # Read values entered by the user.
    username = request.form.get("username")
    password = request.form.get("password")

    # Retrieve the user from PostgreSQL.
    user = get_user_by_username(username)

    # User does not exist.
    if user is None:
        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    # Password stored in database.
    stored_hash = user[2]

    # Verify bcrypt password.
    if not verify_password(password, stored_hash):
        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    # -----------------------------------------------------------
    # Login Successful
    # -----------------------------------------------------------
    #
    # Create a new authenticated session.
    #
    # Only store the minimum information required by the
    # application. Never store passwords or password hashes
    # inside the session.
    # -----------------------------------------------------------

    # Clear any previous session data.
    session.clear()

    # Mark this as a permanent session.
    session.permanent = True

    # -----------------------------------------------------------
    # Store authenticated user information.
    #
    # get_user_by_username() returns a tuple:
    #
    # user[0] -> user_id
    # user[1] -> username
    # user[2] -> password_hash
    # -----------------------------------------------------------

    session["user_id"] = user[0]

    session["username"] = user[1]

    # -----------------------------------------------------------
    # Store the login timestamp.
    #
    # This will later be used for session timeout handling
    # and activity tracking.
    # -----------------------------------------------------------

    session["last_activity"] = datetime.now(
        timezone.utc
    ).isoformat()

    # -----------------------------------------------------------
    # Display success message.
    # -----------------------------------------------------------

    flash(

        "Login successful.",

        "success",

    )

    # -----------------------------------------------------------
    # Redirect the user to the Dashboard.
    # -----------------------------------------------------------

    return redirect(

        url_for("dashboard")

    )


# ============================================================
# Dashboard
# ============================================================

# -----------------------------------------------------------
# Dashboard
# -----------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Display the Dashboard.

    Access
    ---------------------------------------------------------
    Authenticated users only.

    Future Scope
    ---------------------------------------------------------
    - Database statistics
    - Recent activity
    - Quick navigation
    =========================================================
    """

    # Check whether the user is logged in.
    #if "user_id" not in session:
    #    return redirect(url_for("login"))
    
    
    return render_template(
        "dashboard.html"
    )


    # Retrieve the last recorded activity time.
    last_activity = datetime.fromisoformat(
        session["last_activity"]
    )

    # Calculate inactivity duration.
    if datetime.now(timezone.utc) - last_activity > SESSION_TIMEOUT:

        # Session has expired.
        session.clear()

        return redirect(url_for("login"))

    # Update the user's last activity time in UTC.
    session["last_activity"] = datetime.now(timezone.utc).isoformat()
    

    return render_template(
        "dashboard.html",
        full_name=session["full_name"]
    )


# -----------------------------------------------------------
# Logout
# -----------------------------------------------------------
@app.route("/logout")
def logout():
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    End the current user session.

    URL
    ---------------------------------------------------------
    /logout

    Access
    ---------------------------------------------------------
    Logged-in users.

    Future Scope
    ---------------------------------------------------------
    - Audit logout time
    - Record logout IP
    =========================================================
    """
    
    # Remove all session data.
    session.clear()
    
    # Redirect user to the Login page with
    # a confirmation message.
    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(
        url_for("login")
    )



# ============================================================
# Database Explorer
# ============================================================

# -----------------------------------------------------------
# Database Explorer
# -----------------------------------------------------------
@app.route("/database-explorer")
@login_required
def database_explorer():
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Display all database tables.

    Responsibilities
    ---------------------------------------------------------
    1. Read table names from PostgreSQL.
    2. Display them in the browser.

    Future Scope
    ---------------------------------------------------------
    - Display table icons
    - Display row counts
    - Search tables
    =========================================================
    """

    # Ensure the user is authenticated.
    #if "user_id" not in session:
    #    return redirect(url_for("login"))

    tables = get_database_tables()

    return render_template(
        "database-explorer.html",
        tables=tables
    )




# -----------------------------------------------------------
# Generic Table Viewer
# -----------------------------------------------------------
@app.route("/table/<table_name>")
@login_required
def table_view(table_name):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Display any PostgreSQL table.

    URL
    ---------------------------------------------------------
    /table/<table_name>

    Responsibilities
    ---------------------------------------------------------
    1. Validate user session.
    2. Read table data.
    3. Render generic HTML table.

    Future Scope
    ---------------------------------------------------------
    - Pagination
    - Search
    - Sorting
    - Export
    =========================================================
    """

    # -------------------------------------------------------
    # Ensure the user is authenticated.
    # -------------------------------------------------------
    #if "user_id" not in session:
    #    return redirect(url_for("login"))

    try:

        columns, rows = get_table_data(table_name)
        
        # -------------------------------------------------------
        # Retrieve column metadata.
        # -------------------------------------------------------

        column_info = get_table_columns(table_name)
        
        # -------------------------------------------------------
        # Retrieve metadata for the selected table.
        # -------------------------------------------------------
        table_info = get_table_information(table_name)

    except Exception as error:

        return (
            f"Unable to display table.<br><br>"
            f"Error : {error}",
            500
        )

    return render_template(
        "table-view.html",
        table_name=table_name,
        table_info=table_info,
        column_info=column_info,
        columns=columns,
        rows=rows
    )
    



# ============================================================
# SQL Workspace
# ============================================================

@app.route(
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
    #    return redirect(url_for("login"))

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

        error=error

    )


    
    
# -----------------------------------------------------------
# Query History
# -----------------------------------------------------------
@app.route("/query-history")
@login_required
def query_history():

    #if "user_id" not in session:
    #    return redirect(url_for("login"))

    history = get_query_history(session["user_id"])

    return render_template(

        "query-history.html",

        history=history

    )




# ============================================================
# Saved Queries
# ============================================================

@app.route("/saved-queries")
@login_required
def saved_queries():

    flash(
        "Query saved successfully.",
        "success",
    )

    #if "user_id" not in session:
    #    return redirect(url_for("saved_queries"))

    queries = get_saved_queries(
        session["user_id"]
    )

    return render_template(
        "saved-queries.html",
        queries=queries,
    )
    
    


# ============================================================
# New Saved Query
# ============================================================


@app.route(
    "/saved-query/new",
    methods=["POST"],
)
@login_required
def new_saved_query():

    #if "user_id" not in session:
    #    return redirect(url_for("login"))

    save_query(
        session["user_id"],
        request.form["query_name"],
        request.form["query_text"],
    )

    return redirect(
        url_for("saved_queries")
    )


# ============================================================
# Delete Saved Query
# ============================================================


@app.route(
    "/saved-query/delete/<int:saved_query_id>",
    methods=["POST"],
)
@login_required
def remove_saved_query(
    saved_query_id,
):
    
    flash(
    "Saved query deleted successfully.",
        "success",
    )
    
    #if "user_id" not in session:
    #    return redirect(url_for("remove_saved_query"))

    delete_saved_query(
        saved_query_id,
        session["user_id"],
    )

    return redirect(
        url_for("saved_queries")
    )



# ============================================================
# Run Saved Query
# ============================================================

@app.route(
    "/saved-query/run/<int:saved_query_id>"
)
@login_required
def run_saved_query(saved_query_id):

    #if "user_id" not in session:
    #    return redirect(url_for("login"))

    query = get_saved_query_by_id(
        saved_query_id,
        session["user_id"],
    )

    if query is None:
        return redirect(url_for("saved_queries"))

    session["loaded_query"] = query[2]

    return redirect(url_for("sql_workspace"))



# ============================================================
# Edit Saved Query
# ============================================================
       
@app.route(
    "/saved-query/edit/<int:saved_query_id>",
    methods=["GET", "POST"],
)
@login_required
def edit_saved_query(saved_query_id):

    #if "user_id" not in session:
    #    return redirect(url_for("login"))

    if request.method == "POST":

        update_saved_query(
            saved_query_id,
            session["user_id"],
            request.form["query_name"],
            request.form["query_text"],
        )

        return redirect(url_for("saved_queries"))

    query = get_saved_query_by_id(
        saved_query_id,
        session["user_id"],
    )

    return render_template(
        "saved-query-form.html",
        query=query,
    )
        
                    


# -----------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
