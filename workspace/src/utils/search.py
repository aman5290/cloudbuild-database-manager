"""
============================================================
CloudBuild Database Manager
============================================================

Search Utilities

Purpose
-------
Reusable helper functions for filtering collections.

Current Features
----------------
✓ Case-insensitive text search
✓ Supports strings
✓ Supports tuples using a key function

Future Scope
------------
- Multiple search fields
- Wildcards
- Regex
- Database-backed search
- Object attribute search

============================================================
"""


# ============================================================
# Filter Items
# ============================================================

def filter_items(
    items,
    search_text,
    key=None,
):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Filter a collection using a case-insensitive search.

    Parameters
    ---------------------------------------------------------
    items
        Iterable containing strings, tuples or objects.

    search_text
        Text entered by the user.

    key
        Optional function used to extract the searchable
        value from each item.

    Returns
    ---------------------------------------------------------
    list
        Filtered collection.
    =========================================================
    """

    # --------------------------------------------------------
    # Empty search returns all items.
    # --------------------------------------------------------

    if not search_text:

        return list(items)

    # --------------------------------------------------------
    # Normalize search text.
    # --------------------------------------------------------

    search_text = search_text.strip().lower()

    # --------------------------------------------------------
    # Store matching items.
    # --------------------------------------------------------

    filtered_items = []

    # --------------------------------------------------------
    # Search each item.
    # --------------------------------------------------------

    for item in items:

        # ----------------------------------------------------
        # Determine searchable value.
        # ----------------------------------------------------

        value = key(item) if key else item

        # ----------------------------------------------------
        # Perform case-insensitive search.
        # ----------------------------------------------------

        if search_text in str(value).lower():

            filtered_items.append(item)

    # --------------------------------------------------------
    # Return matching items.
    # --------------------------------------------------------

    return filtered_items
