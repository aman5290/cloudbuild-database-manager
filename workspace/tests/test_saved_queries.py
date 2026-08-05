from src.database.db import (
    save_query,
    get_saved_queries,
    get_saved_query_by_id,
    update_saved_query,
    delete_saved_query,
)

USER_ID = 1


def main():

    print("Creating...")

    save_query(
        USER_ID,
        "Test Query",
        "SELECT * FROM actor LIMIT 5;"
    )

    queries = get_saved_queries(USER_ID)

    print(queries)

    saved_query_id = queries[0][0]

    query = get_saved_query_by_id(
        saved_query_id,
        USER_ID,
    )

    print(query)

    update_saved_query(
        saved_query_id,
        USER_ID,
        "Updated Query",
        "SELECT * FROM film LIMIT 3;"
    )

    delete_saved_query(
        saved_query_id,
        USER_ID,
    )

    print("Backend Test Passed")


if __name__ == "__main__":
    main()
