import psycopg
from config import DB_CONFIG


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    return psycopg.connect(**DB_CONFIG)