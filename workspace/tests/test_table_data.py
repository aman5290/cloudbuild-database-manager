from src.database.db import get_table_data

columns, rows = get_table_data("actor", 5)

print("\nColumns")
print("-" * 40)

for column in columns:
    print(column)

print("\nRows")
print("-" * 40)

for row in rows:
    print(row)
