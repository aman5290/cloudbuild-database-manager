from pathlib import Path

from flask import Flask, render_template, request

from database.db import get_actor_by_id

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=BASE_DIR / "templates",
    static_folder=BASE_DIR / "static"
)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/actor")
def actor_search():

    actor_id = request.args.get("actor_id", type=int)

    if actor_id is None:
        return "Actor ID is required", 400

    actor = get_actor_by_id(actor_id)

    return render_template(
        "actor.html",
        actor=actor
    )


if __name__ == "__main__":
    app.run(debug=True)