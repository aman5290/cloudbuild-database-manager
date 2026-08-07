"""
============================================================
CloudBuild Database Manager
============================================================

File
----
explorer_db.py

Purpose
-------
Database Explorer database operations.

Responsibilities
----------------
1. Retrieve database tables.
2. Retrieve table data.
3. Retrieve table metadata.
4. Retrieve table columns.

============================================================
"""

# ============================================================
# Imports
# ============================================================

from psycopg import sql

from .connection import get_connection


# ============================================================
# Database Explorer Functions
# ============================================================

def get_database_tables():
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve all user tables from the PostgreSQL database.

    Returns
    ---------------------------------------------------------
    list
        A list containing table names.

    Notes
    ---------------------------------------------------------
    Only tables from the 'public' schema are returned.

    Future Scope
    ---------------------------------------------------------
    - Support multiple schemas
    - Filter system tables
    - Include row counts
    =========================================================
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
            )

            rows = cur.fetchall()

    tables = [

        row[0]

        for row in rows

    ]

    return tables
    
    
    
    
    
    
def get_database_objects():
    """
    Retrieve database objects grouped by type.
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT

                    table_name,

                    table_type

                FROM information_schema.tables

                WHERE table_schema='public'

                ORDER BY table_name;
                """
            )

            tables = []
            views = []

            for name, table_type in cur.fetchall():

                if table_type == "BASE TABLE":

                    tables.append(name)

                elif table_type == "VIEW":

                    views.append(name)

            cur.execute(
                """
                SELECT

                    sequence_name

                FROM information_schema.sequences

                WHERE sequence_schema='public'

                ORDER BY sequence_name;
                """
            )

            sequences = [

                row[0]

                for row in cur.fetchall()

            ]

            cur.execute(
                """
                SELECT

                    routine_name

                FROM information_schema.routines

                WHERE specific_schema='public'

                ORDER BY routine_name;
                """
            )

            functions = [

                row[0]

                for row in cur.fetchall()

            ]

            return {

                "tables": tables,

                "views": views,

                "sequences": sequences,

                "functions": functions

            }
            







def get_database_summary():
    """
    Return object counts for the explorer dashboard.
    """

    objects = get_database_objects()

    return {
        "tables": len(objects["tables"]),
        "views": len(objects["views"]),
        "functions": len(objects["functions"]),
        "sequences": len(objects["sequences"]),
    }     




     
     
     
            


# ============================================================
# Retrieve Table Data
# ============================================================

def get_table_data(
    table_name,
    limit=100,
):
    """
    Retrieve data from any PostgreSQL table.
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            query = sql.SQL(
                """
                SELECT *
                FROM {}
                LIMIT %s;
                """
            ).format(
                sql.Identifier(table_name)
            )

            cur.execute(
                query,
                (limit,),
            )

            columns = [

                column.name

                for column in cur.description

            ]

            rows = cur.fetchall()

            return columns, rows



# ============================================================
# Retrieve Table Information
# ============================================================

def get_table_information(table_name):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve metadata for a PostgreSQL table.

    Returns
    ---------------------------------------------------------
    Dictionary containing:

    - Row count
    - Column count
    - Primary key

    Future Scope
    ---------------------------------------------------------
    - Indexes
    - Foreign Keys
    - Table Size
    =========================================================
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            # -------------------------------------------------
            # Total Rows
            # -------------------------------------------------

            query = sql.SQL(
                """
                SELECT COUNT(*)
                FROM {};
                """
            ).format(
                sql.Identifier(table_name)
            )

            cur.execute(query)

            row_count = cur.fetchone()[0]

            # -------------------------------------------------
            # Total Columns
            # -------------------------------------------------

            cur.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_schema='public'
                AND table_name=%s;
                """,
                (table_name,),
            )

            column_count = cur.fetchone()[0]

            # -------------------------------------------------
            # Primary Key
            # -------------------------------------------------

            cur.execute(
                """
                SELECT
                    kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type='PRIMARY KEY'
                  AND tc.table_name=%s
                  AND tc.table_schema='public';
                """,
                (table_name,),
            )

            result = cur.fetchone()

            primary_key = (

                result[0]

                if result

                else "N/A"

            )

            return {

                "row_count": row_count,

                "column_count": column_count,

                "primary_key": primary_key,

            }


# ============================================================
# Retrieve Table Columns
# ============================================================

def get_table_columns(table_name):
    """
    =========================================================
    Purpose
    ---------------------------------------------------------
    Retrieve metadata for all columns in a PostgreSQL table.

    Returns
    ---------------------------------------------------------
    list[dict]

    Future Scope
    ---------------------------------------------------------
    - Character length
    - Default value
    - Identity columns
    =========================================================
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                ORDER BY ordinal_position;
                """,
                (table_name,),
            )

            return [

                {

                    "column_name": row[0],

                    "data_type": row[1],

                    "nullable": row[2],

                }

                for row in cur.fetchall()

            ]



# ============================================================
# Table Statistics
# ============================================================

def get_table_statistics():
    """
    Return estimated row count for every user table.
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT

                    relname,

                    n_live_tup

                FROM pg_stat_user_tables

                ORDER BY relname;
                """
            )

            return {

                row[0]: row[1]

                for row in cur.fetchall()

            }






def get_object_details(object_type, object_name):

    if object_type == "table":
        return get_table_details(object_name)

    if object_type == "view":
        return get_view_details(object_name)

    if object_type == "function":
        return get_function_details(object_name)

    if object_type == "sequence":
        return get_sequence_details(object_name)

    return {}







def get_table_details(table_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            schemaname,
            relname,
            n_live_tup
        FROM pg_stat_user_tables
        WHERE relname=%s
    """, (table_name,))

    table = cur.fetchone()

    if table is None:

        cur.close()
        conn.close()

        return {}

    cur.execute("""
        SELECT

            column_name,

            data_type,

            is_nullable

        FROM information_schema.columns

        WHERE table_name=%s

        ORDER BY ordinal_position
    """, (table_name,))

    columns = cur.fetchall()

    cur.close()
    conn.close()

    return {

        "schema": table[0],

        "table": table[1],

        "rows": table[2],

        "columns": [

            {
                "name": c[0],
                "type": c[1],
                "nullable": c[2]
            }

            for c in columns

        ]

    }
    
    
    
    



def get_table_ddl(table_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            column_name,

            data_type,

            character_maximum_length,

            is_nullable,

            column_default

        FROM information_schema.columns

        WHERE table_name=%s

        ORDER BY ordinal_position

    """,(table_name,))

    columns = cur.fetchall()

    ddl = f"CREATE TABLE {table_name} (\n"

    lines = []

    for column in columns:

        name = column[0]
        datatype = column[1]
        length = column[2]
        nullable = column[3]
        default = column[4]

        datatype_sql = datatype

        if length:

            datatype_sql += f"({length})"

        line = f"    {name} {datatype_sql}"

        if nullable == "NO":

            line += " NOT NULL"

        if default:

            line += f" DEFAULT {default}"

        lines.append(line)

    ddl += ",\n".join(lines)

    ddl += "\n);"

    cur.close()
    conn.close()

    return ddl
    
    
    
    
    
    
def get_object_ddl(object_type, object_name):

    if object_type == "table":

        return get_table_ddl(object_name)

    return "-- DDL not available."
    
    
    
    
    
    



def get_relationships(table_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

    WITH RECURSIVE tables AS (

        SELECT c.oid, c.relname

        FROM pg_class c

        WHERE c.relname=%s

        UNION

        SELECT child.oid,
               child.relname

        FROM pg_inherits i

        JOIN pg_class child
             ON child.oid=i.inhrelid

        JOIN tables t
             ON t.oid=i.inhparent

    )

    SELECT DISTINCT

        a.attname,

        ref.relname,

        af.attname

    FROM tables t

    JOIN pg_constraint con

        ON con.conrelid=t.oid

    JOIN pg_class ref

        ON ref.oid=con.confrelid

    JOIN unnest(con.conkey,con.confkey)

         WITH ORDINALITY cols(local_col,foreign_col,ord)

         ON TRUE

    JOIN pg_attribute a

        ON a.attrelid=t.oid
       AND a.attnum=cols.local_col

    JOIN pg_attribute af

        ON af.attrelid=ref.oid
       AND af.attnum=cols.foreign_col

    WHERE con.contype='f'

    ORDER BY 1;

    """,(table_name,))

    rows=cur.fetchall()

    cur.close()
    conn.close()

    return [

        {

            "column":r[0],

            "table":r[1],

            "foreign_column":r[2]

        }

        for r in rows

    ]
