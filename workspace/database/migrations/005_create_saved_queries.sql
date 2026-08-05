/*
============================================================
Project : CloudBuild Database Manager
============================================================

Version      : 6.3.1
Migration    : 005

File
----

005_create_saved_queries.sql

Purpose
-------

Create the portal.saved_queries table.

Responsibilities
----------------

1. Store reusable SQL queries.
2. Associate queries with application users.
3. Maintain creation and update timestamps.

Author
------

Aman

Last Updated
------------

05-Aug-2026
============================================================
*/

CREATE TABLE IF NOT EXISTS portal.saved_queries
(
    saved_query_id BIGSERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    query_name VARCHAR(100) NOT NULL,

    query_text TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_saved_queries_user
        FOREIGN KEY (user_id)
        REFERENCES portal.app_users(user_id)
        ON DELETE CASCADE
);
