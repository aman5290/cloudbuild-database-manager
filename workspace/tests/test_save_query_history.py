"""
============================================================
Backend Test

Purpose
-------
Verify query history insertion.
============================================================
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from database.db import save_query_history


def main():

    save_query_history(

        user_id=1,

        query_text="SELECT * FROM actor LIMIT 5",

        rows_returned=5,

        execution_time_ms=4.25

    )

    print()

    print("Query history inserted successfully.")


if __name__ == "__main__":
    main()
