/*
=============================================================

Project : Pagila PostgreSQL Web Portal

Version : 4.0.0

File    : 002_create_app_users.sql

Author  : Aman

Purpose
-------
Create application users table.

=============================================================
*/

CREATE TABLE IF NOT EXISTS portal.app_users
(
    user_id SERIAL PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(255),

    role VARCHAR(20) NOT NULL DEFAULT 'ADMIN',

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    last_login TIMESTAMP
);
