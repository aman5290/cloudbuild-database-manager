"""
============================================================
CloudBuild Database Manager
============================================================

Sorting Utilities

Purpose
-------
Reusable helper functions for sorting collections.

============================================================
"""


# ============================================================
# Sort Items
# ============================================================

def sort_items(
    items,
    key=None,
    descending=False,
):
    """
    Sort a collection.

    Parameters
    ----------
    items
        Collection to sort.

    key
        Optional function used for sorting.

    descending
        Sort descending when True.

    Returns
    -------
    list
    """

    return sorted(

        items,

        key=key,

        reverse=descending

    )
