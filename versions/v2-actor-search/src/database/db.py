import psycopg
from config import DB_CONFIG


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def get_actor_by_id(actor_id):

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

            return cur.fetchone()