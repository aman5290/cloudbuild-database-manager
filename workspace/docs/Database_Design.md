# Database Design

---

# Project

CloudBuild Database Manager

---

# Purpose

This document describes the database architecture used by the CloudBuild Database Manager application.

It explains:

- Database organization
- Schemas
- Tables
- Relationships
- Naming conventions
- Migration strategy
- Future database design

This document reflects the database design through **Version 6 Sprint 6.1.3**.

---

# Database Overview

The application uses PostgreSQL and is logically divided into two areas.

```
PostgreSQL

³
ÃÄÄ Pagila Sample Database Objects
³
ÀÄÄ Application Schema
        ³
        ÀÄÄ portal
```

The Pagila database provides sample business data for learning and SQL practice.

The **portal** schema contains all application-specific objects created for CloudBuild Database Manager.

---

# Schema Design

## public Schema

Purpose

- Pagila sample database
- Business entities
- Read-only exploration

Examples

- actor
- film
- customer
- rental
- payment

---

## portal Schema

Purpose

Store application-owned data.

Examples

- Authentication
- Query History
- Saved Queries (Future)
- User Preferences (Future)

---

# Current Tables

## portal.app_users

Purpose

Store application login credentials.

Current Columns

| Column | Data Type | Description |
|---------|-----------|-------------|
| user_id | INTEGER | Primary Key |
| username | VARCHAR | Login name |
| password_hash | TEXT | Hashed password |
| full_name | VARCHAR | User display name |
| created_at | TIMESTAMPTZ | Record creation timestamp |

> **Note:** Update this table if your implementation contains additional or differently named columns.

Primary Key

```
user_id
```

---

## portal.query_history

Purpose

Store successful SQL queries executed by authenticated users.

Current Columns

| Column | Data Type | Description |
|---------|-----------|-------------|
| history_id | BIGSERIAL | Primary Key |
| user_id | INTEGER | User executing the query |
| query_text | TEXT | Executed SQL statement |
| rows_returned | INTEGER | Number of rows returned |
| execution_time_ms | NUMERIC(10,2) | Query execution time |
| executed_at | TIMESTAMPTZ | Execution timestamp |

Primary Key

```
history_id
```

Foreign Key

```
user_id



portal.app_users.user_id
```

---

# Database Relationships

```
portal.app_users

user_id
    ³
    ³
    ÃÄÄÄÄÄÄÄÄÄÄÄÄÄÄ¿
    ³              ³
                  

query_history   (future tables)
```

Relationship

One User



Many Query History Records

---

# Naming Conventions

## Schemas

Use lowercase.

Example

```
portal
```

---

## Tables

Use lowercase with underscores.

Example

```
query_history

saved_queries
```

---

## Columns

Use lowercase with underscores.

Example

```
execution_time_ms

rows_returned

created_at
```

---

## Primary Keys

Use

```
table_name_id
```

Examples

```
user_id

history_id

saved_query_id
```

---

## Foreign Keys

Reference the primary key of the parent table.

Example

```
query_history.user_id



app_users.user_id
```

---

# Data Types

Preferred data types used in this project.

| Purpose | Data Type |
|----------|-----------|
| Identifier | BIGSERIAL / INTEGER |
| Name | VARCHAR |
| Description | TEXT |
| SQL Query | TEXT |
| Count | INTEGER |
| Time | TIMESTAMPTZ |
| Duration | NUMERIC(10,2) |

---

# Migration Strategy

All database changes are managed through SQL migration files.

Location

```
workspace/database/migrations/
```

Current Migrations

| Version | File | Status |
|----------|------|:------:|
| 001 | create_portal_schema | ? |
| 002 | create_app_users | ? |
| 003 | seed_admin_user | ? |
| 004 | create_query_history | ? |

Each migration has a single responsibility.

Applied migrations should not be modified after execution.

Future schema changes should always be implemented using new migration files.

---

# Current Database Flow

```
Browser



Flask



Database Layer



PostgreSQL



portal Schema



Application Data
```

---

# Security Considerations

Current implementation

- Password hashes stored instead of plain-text passwords.
- Application data separated from sample data.
- Session-based authentication.
- Read-only SQL execution.
- Query history linked to authenticated users.

Future improvements

- Role-based permissions.
- Row-level security.
- Query ownership validation.
- Audit logging.
- Encryption for sensitive application data.

---

# Index Strategy

Current

Primary key indexes are created automatically.

Future

Additional indexes may be added for:

```
query_history.user_id

query_history.executed_at

saved_queries.user_id
```

These will improve performance for user-specific searches and sorting.

---

# Future Tables

The following tables are planned.

| Table | Purpose |
|---------|---------|
| saved_queries | Save reusable SQL statements |
| user_preferences | Store user settings |
| audit_log | Record important application events |
| application_settings | Global application configuration |

These tables are not yet implemented.

---

# Design Principles

The database follows these principles.

## Separation of Data

Application data is stored separately from the Pagila sample data.

---

## Normalization

Avoid duplicate information.

Store relationships using foreign keys.

---

## Scalability

Design tables so they can grow without major redesign.

---

## Readability

Use clear, descriptive names for:

- Tables
- Columns
- Constraints

---

## Incremental Evolution

The schema evolves through versioned migration files.

No manual production schema changes.

---

# Version History

| Version | Database Changes |
|----------|------------------|
| V4 | Created portal schema and app_users |
| V5 | No application schema changes |
| V6 | Added query_history |

---

# Summary

The database design of CloudBuild Database Manager separates application-owned data from the Pagila sample database.

This approach provides:

- Better organization
- Cleaner ownership
- Easier maintenance
- Safer experimentation
- A structure similar to production PostgreSQL applications

The schema will continue to evolve through controlled migrations as new features are introduced.
