from src.database.db import get_table_columns

columns = get_table_columns("actor")

print("\nColumn Metadata")
print("-" * 60)

for column in columns:
    print(
        f"{column['column_name']:15}"
        f"{column['data_type']:25}"
        f"{column['nullable']}"
    )
