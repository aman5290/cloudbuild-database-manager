"""
============================================================
CloudBuild Database Manager
============================================================

Pagination Utilities

============================================================
"""


# ============================================================
# Paginate Items
# ============================================================

def paginate_items(

    items,

    page,

    page_size,

):
    """
    Paginate a collection.
    """

    total_items = len(items)

    start = (page - 1) * page_size

    end = start + page_size

    page_items = items[start:end]

    return {

        "items": page_items,

        "total_items": total_items,

        "page": page,

        "page_size": page_size,

        "total_pages":

            (

                total_items + page_size - 1

            )

            // page_size

    }
