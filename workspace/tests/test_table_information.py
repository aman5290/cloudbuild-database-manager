from src.database.db import get_table_information

info = get_table_information("actor")

print()

print("Table Information")

print("-" * 40)

for key, value in info.items():
    print(f"{key:15}: {value}")
