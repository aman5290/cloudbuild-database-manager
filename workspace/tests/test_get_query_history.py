"""
============================================================
Backend Test

Purpose
-------
Verify retrieval of query history.
============================================================
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from database.db import get_query_history


def main():

    history = get_query_history(1)

    print()

    print("Query History")

    print("-" * 60)

    for row in history:

        print(row)


if __name__ == "__main__":
    main()
