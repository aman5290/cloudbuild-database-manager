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

from pathlib import Path

from flask import Flask, render_template, request

from database.db import (
    get_actor_by_id,
    get_all_actors
)

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

    actors = get_all_actors()

    return render_template(
        "actor-list.html",
        actors=actors
    )


# -----------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)