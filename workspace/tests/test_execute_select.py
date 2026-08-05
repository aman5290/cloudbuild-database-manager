from src.database.db import execute_select_query

result = execute_select_query("""

SELECT *
FROM actor
LIMIT 5;

""")

print()

print("Columns")

print("-" * 50)

for column in result["columns"]:

    print(column)

print()

print("Rows")

print("-" * 50)

for row in result["rows"]:

    print(row)
