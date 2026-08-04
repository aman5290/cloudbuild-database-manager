"""
=============================================================
Project : CloudBuild Database Manager

Version : 5.0.0

File    : test_database_explorer.py

Author  : Aman

Purpose
-------
Test database metadata functions.

Last Updated
------------
05-Aug-2026
=============================================================
"""

from src.database.db import get_database_tables

tables = get_database_tables()

print()

print("Tables Found")

print("-" * 40)

for table in tables:

    print(table[0])

print()

print(f"Total Tables : {len(tables)}")
