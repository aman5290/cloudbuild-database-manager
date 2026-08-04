"""
=============================================================
Project : Pagila PostgreSQL Web Portal

Version : 3.0.0

File    : db.py

Author  : Aman

Purpose
-------
Contains all PostgreSQL database operations.

Responsibilities
----------------
1. Create database connection
2. Retrieve one actor
3. Retrieve all actors

Last Updated
------------
04-Aug-2026
=============================================================
"""

import psycopg

from config import DB_CONFIG


def get_connection():
    """
    Create and return a PostgreSQL connection.
    """

    return psycopg.connect(**DB_CONFIG)


def get_actor_by_id(actor_id):
    """
    Retrieve one actor using Actor ID.
    """

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


def get_all_actors():
    """
    Retrieve all actors ordered by Actor ID.
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    actor_id,
                    first_name,
                    last_name
                FROM actor
                ORDER BY actor_id;
            """)

            actors = cur.fetchall()

            print("=" * 50)
            print("DEBUG")
            print("=" * 50)
            print("Rows:", len(actors))

            if actors:
                print("First row:", actors[0])

            return actors