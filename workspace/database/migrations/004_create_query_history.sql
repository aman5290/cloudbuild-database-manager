-- ===========================================================
-- Project : CloudBuild Database Manager
--
-- Version : 5.8.0
--
-- File    : 004_create_query_history.sql
--
-- Purpose
-- -------
-- Store SQL queries executed by application users.
--
-- Author
-- ------
-- Aman
-- ===========================================================

-- -----------------------------------------------------------
-- Create Query History Table
-- -----------------------------------------------------------

CREATE TABLE IF NOT EXISTS portal.query_history (

    history_id BIGSERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    query_text TEXT NOT NULL,

    execution_time_ms NUMERIC(10,2),

    rows_returned INTEGER,

    executed_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_query_history_user
        FOREIGN KEY (user_id)
        REFERENCES portal.app_users(user_id)

);
