"""
=============================================================
Project : Pagila PostgreSQL Web Portal

Version : 3.0.0

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

from datetime import datetime, timedelta, timezone

from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from src.database.db import (
    get_actor_by_id,
    get_all_actors,
    get_user_by_username,
    get_database_tables,
    get_table_data,
    get_table_information,
    get_table_columns,
    execute_select_query,
    save_query_history
)

from src.utils.password import verify_password


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
SESSION_TIMEOUT = timedelta(minutes=5)


# -----------------------------------------------------------
# Home Page
# -----------------------------------------------------------
@app.route("/")
def home():
    """
    Display application home page.
    """
    return render_template("home.html")


# -----------------------------------------------------------
# Search One Actor
# -----------------------------------------------------------
@app.route("/actor")
def actor_search():
    """
    Search actor using Actor ID.
    """

    actor_id = request.args.get("actor_id", type=int)

    if actor_id is None:
        return "Actor ID is required.", 400

    actor = get_actor_by_id(actor_id)

    return render_template(
        "actor.html",
        actor=actor
    )


# -----------------------------------------------------------
# View All Actors
# -----------------------------------------------------------
@app.route("/actors")
def actor_list():
    """
    Display all actors.
    """

    columns, rows = get_all_actors()

    return render_template(
        "actor-list.html",
        columns=columns,
        rows=rows
    )



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

    # Store authenticated user information.
    # Never store passwords or password hashes.
    session["user_id"] = user[0]
    session["username"] = user[1]
    session["full_name"] = user[3]
    session["role"] = user[4]
    # Store the login time in UTC.
    session["last_activity"] = datetime.now(timezone.utc).isoformat()

    # Redirect user to Dashboard.
    return redirect(url_for("dashboard"))



# -----------------------------------------------------------
# Dashboard
# -----------------------------------------------------------
@app.route("/dashboard")
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
    if "user_id" not in session:
        return redirect(url_for("login"))

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
    return redirect(
        url_for(
            "login",
            message="You have been logged out successfully."
        )
    )



# -----------------------------------------------------------
# Database Explorer
# -----------------------------------------------------------
@app.route("/database-explorer")
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
    if "user_id" not in session:
        return redirect(url_for("login"))

    tables = get_database_tables()

    return render_template(
        "database-explorer.html",
        tables=tables
    )




# -----------------------------------------------------------
# Generic Table Viewer
# -----------------------------------------------------------
@app.route("/table/<table_name>")
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
    if "user_id" not in session:
        return redirect(url_for("login"))

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
    



# -----------------------------------------------------------
# SQL Workspace
# -----------------------------------------------------------
@app.route(
    "/sql-workspace",
    methods=["GET", "POST"]
)
def sql_workspace():
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Display and execute SQL queries.

    Version 5
    ---------------------------------------------------------
    Only SELECT statements are permitted.
    =========================================================
    """

    # -------------------------------------------------------
    # Ensure user is authenticated.
    # -------------------------------------------------------

    if "user_id" not in session:
        return redirect(url_for("login"))

    # -------------------------------------------------------
    # Default values.
    # -------------------------------------------------------

    query = ""

    result = None

    error = None

    # -------------------------------------------------------
    # Execute query.
    # -------------------------------------------------------

    if request.method == "POST":

        query = request.form.get(
            "query",
            ""
        )

        try:

            result = execute_select_query(query)
            
            # -------------------------------------------------------
            # Save successful query to history.
            # -------------------------------------------------------

            save_query_history(

            user_id=session["user_id"],

            query_text=query,

            rows_returned=result["row_count"],

            execution_time_ms=result["execution_time_ms"]

            )

        except Exception as ex:

            error = str(ex)

    return render_template(

        "sql-workspace.html",

        query=query,

        result=result,

        error=error

    )
    
    
        


# -----------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    
    

