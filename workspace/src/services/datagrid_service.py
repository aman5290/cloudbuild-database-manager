"""
============================================================
CloudBuild Database Manager
============================================================

Data Grid Service

Purpose
-------
Provides reusable search, sorting and pagination.

============================================================
"""

from src.utils.search import filter_items
from src.utils.sorting import sort_items
from src.utils.pagination import paginate_items


# ============================================================
# Build Data Grid
# ============================================================

def build_datagrid(

    items,

    search="",

    key=None,

    descending=False,

    page=1,

    page_size=20,

):
    """
    Build a reusable data grid.
    """

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    filtered_items = filter_items(

        items,

        search,

        key=key,

    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    sorted_items = sort_items(

        filtered_items,

        key=key,

        descending=descending,

    )

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    return paginate_items(

        sorted_items,

        page,

        page_size,

    )
