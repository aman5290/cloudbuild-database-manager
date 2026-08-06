from flask import (
    Blueprint,
    render_template,
    request,
    session,
)

from src.database.db import (
    get_query_history,
)

from src.utils.auth import (
    login_required,
)

from src.utils.search import (
    filter_items,
)

history_bp = Blueprint(
    "history",
    __name__,
)


# ============================================================
# Query History
# ============================================================

@history_bp.route("/query-history")
@login_required
def query_history():

    search = request.args.get(
        "search",
        ""
    ).strip()

    history = get_query_history(
        session["user_id"]
    )

    history = filter_items(

        history,

        search,

        key=lambda row: row[1]

    )

    return render_template(

        "query-history.html",

        history=history,

        search=search,

        search_title="Search Query History",

        search_placeholder="Search SQL query..."

    )
