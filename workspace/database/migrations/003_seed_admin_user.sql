/*
=============================================================

Project : Pagila PostgreSQL Web Portal

Version : 4.0.0

File    : 003_seed_admin_user.sql

Author  : Aman

Purpose
-------
Insert the first application administrator.

NOTE
----
Temporary plain-text password for development.
Will be replaced with bcrypt hashing before production.

=============================================================
*/

INSERT INTO portal.app_users
(
    username,
    password_hash,
    full_name,
    email
)
VALUES
(
    'aman',
    'Admin123!',
    'Aman',
    'aman@example.com'
);
