from flask import Flask, jsonify

from database.db import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to the Pagila PostgreSQL Web Portal!"


@app.route("/actor/<int:actor_id>")
def get_actor(actor_id):

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT
                        actor_id,
                        first_name,
                        last_name
                    FROM actor
                    WHERE actor_id = %s;
                """, (actor_id,))

                actor = cur.fetchone()

                if actor is None:
                    return jsonify({"message": "Actor not found"}), 404

                return jsonify({
                    "actor_id": actor[0],
                    "first_name": actor[1],
                    "last_name": actor[2]
                })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)