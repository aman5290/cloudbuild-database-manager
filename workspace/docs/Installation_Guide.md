# Installation Guide

---

# Project

CloudBuild Database Manager

---

# Purpose

This guide explains how to install and configure the CloudBuild Database Manager project from scratch.

This guide reflects the project through **Version 6 Sprint 6.1.3**.

---

# System Requirements

Recommended Operating System

- Windows 10 / Windows 11

The application can also be adapted for Linux or macOS with minor command changes.

---

# Software Requirements

Install the following software before beginning.

## Python

Version

```
Python 3.13 or later
```

Verify

```
python --version
```

---

## PostgreSQL

Recommended Version

```
PostgreSQL 17
```

Verify

```
SELECT version();
```

---

## pgAdmin

Install the latest version of pgAdmin.

Purpose

- Database management
- Running migrations
- Query execution
- Database inspection

---

## Git

Verify

```
git --version
```

---

## Visual Studio Code

Recommended Extensions

- Python
- Jinja
- SQLTools
- GitLens
- PostgreSQL

---

# Clone the Repository

Example

```
git clone <repository-url>

cd pagila-project
```

---

# Project Structure

```
pagila-project/

³
ÃÄÄ database/
ÃÄÄ docs/
ÃÄÄ scripts/
ÃÄÄ tools/
ÃÄÄ versions/
ÀÄÄ workspace/
```

---

# Create Virtual Environment

Move to

```
workspace/
```

Create

```
python -m venv venv
```

Activate

Windows

```
venv\Scripts\activate
```

Verify

```
python --version
```

---

# Install Dependencies

Install

```
pip install -r requirements.txt
```

Verify

```
pip list
```

---

# Configure Environment Variables

Create

```
workspace/.env
```

Example

```
DB_HOST=localhost

DB_PORT=5432

DB_NAME=pagila

DB_USER=postgres

DB_PASSWORD=your_password

SECRET_KEY=replace_with_secure_random_value
```

Update the values according to your local PostgreSQL installation.

---

# PostgreSQL Setup

Create or restore the Pagila database.

Verify

```
SELECT current_database();
```

Expected

```
pagila
```

---

# Create Application Schema

Run migration

```
001_create_portal_schema.sql
```

Verify

```
portal
```

exists.

---

# Create Application Tables

Execute the migration files in order.

```
001_create_portal_schema.sql

002_create_app_users.sql

003_seed_admin_user.sql

004_create_query_history.sql
```

Do not skip migration numbers.

---

# Verify Migrations

Run

```sql
SELECT table_schema,
       table_name
FROM information_schema.tables
WHERE table_schema='portal';
```

Expected

```
portal.app_users

portal.query_history
```

---

# Default Login

The default administrator account is created by:

```
003_seed_admin_user.sql
```

Update the username and password if your project uses different credentials.

> **Security Note:** Do not commit real usernames, passwords, password hashes, or secrets to Git. If you want to document example credentials, use placeholders (for example, `admin` / `ChangeMe123!`) or refer readers to the seed migration instead.

---

# Start the Application

Activate the virtual environment.

```
venv\Scripts\activate
```

Start Flask

```
python src/app.py
```

Open

```
http://127.0.0.1:5000
```

---

# Run Backend Tests

Examples

```
python -m tests.test_password

python -m tests.test_database_explorer

python -m tests.test_table_data

python -m tests.test_execute_select

python -m tests.test_save_query_history

python -m tests.test_get_query_history
```

Each test should complete successfully.

---

# Verify Application Features

Login



Dashboard



Database Explorer



Generic Table Viewer



SQL Workspace



Query History

All features should operate without errors.

---

# Git Workflow

Check status

```
git status
```

Commit changes

```
git add .

git commit -m "Meaningful commit message"
```

View history

```
git log --oneline
```

---

# Common Problems

## Virtual Environment Not Activated

Symptoms

```
ModuleNotFoundError
```

Solution

```
venv\Scripts\activate
```

---

## Missing Python Package

Install dependencies again.

```
pip install -r requirements.txt
```

---

## PostgreSQL Connection Failed

Check

- PostgreSQL service
- Host
- Port
- Username
- Password

Verify the values in

```
workspace/.env
```

---

## Relation Does Not Exist

Example

```
relation "portal.query_history" does not exist
```

Cause

Migration not executed.

Solution

Execute the required migration in pgAdmin.

---

## Login Fails

Verify

- app_users table exists
- Seed migration executed
- Password hash matches the expected value

---

# Folder Purpose

| Folder | Purpose |
|----------|---------|
| database | Database resources |
| docs | Project documentation |
| workspace/src | Application source code |
| workspace/templates | HTML templates |
| workspace/static | CSS and static files |
| workspace/tests | Backend tests |
| workspace/screenshots | Project screenshots |
| versions | Version snapshots |

---

# Updating the Project

Pull the latest changes

```
git pull
```

Install any new dependencies

```
pip install -r requirements.txt
```

Apply any new database migrations in sequence before starting the application.

---

# Verification Checklist

- Python installed
- PostgreSQL installed
- pgAdmin installed
- Virtual environment created
- Dependencies installed
- Environment variables configured
- Pagila database available
- All migrations executed
- Flask application starts
- Login works
- Database Explorer works
- SQL Workspace works
- Query History works

---

# Summary

Following this guide should result in a fully functioning CloudBuild Database Manager development environment.

If issues occur, first verify:

- Virtual environment
- Environment variables
- PostgreSQL connection
- Migration status

Most setup problems originate from one of these four areas.
