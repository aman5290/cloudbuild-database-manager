# CloudBuild Database Manager

> A production-inspired PostgreSQL Database Management application built with Python, Flask, and PostgreSQL.

---

# Project Overview

CloudBuild Database Manager is a learning-focused, production-inspired web application developed to strengthen backend development, PostgreSQL database management, software architecture, and AWS deployment skills.

Unlike a simple CRUD application, this project focuses on building reusable backend components, generic database utilities, secure authentication, SQL execution, and database exploration features while following professional software engineering practices.

The application uses the PostgreSQL Pagila sample database for exploration while maintaining its own application schema (`portal`) for authentication and application-specific data.

---

# Current Version

**Version:** 6.1.3

Status:

- Stable
- Development Continues

---

# Technologies Used

## Backend

- Python 3
- Flask
- psycopg (PostgreSQL Driver)

## Database

- PostgreSQL
- Pagila Sample Database

## Frontend

- HTML5
- CSS3
- Jinja2 Templates

## Development Tools

- pgAdmin
- Git
- GitHub
- Visual Studio Code

---

# Features Implemented

## Authentication

- User Login
- Password Hash Verification
- Session Management
- Protected Routes
- Logout

---

## Dashboard

- Secure Landing Page
- Navigation Menu
- Portal Home

---

## Database Explorer

- List Database Tables
- Generic Table Viewer
- Table Summary
- Column Metadata

---

## SQL Workspace

- Execute SQL Queries
- Read-Only (SELECT Only)
- SQL Validation
- Error Handling
- Query Execution Statistics

---

## Query History

- Save Successful Queries
- View Previous Queries
- User-specific Query History

---

# Project Structure

```text
pagila-project/

³
ÃÄÄ database/
³
ÃÄÄ docs/
³
ÃÄÄ scripts/
³
ÃÄÄ tools/
³
ÃÄÄ versions/
³
ÀÄÄ workspace/
    ³
    ÃÄÄ database/
    ³   ÀÄÄ migrations/
    ³
    ÃÄÄ src/
    ³
    ÃÄÄ static/
    ³
    ÃÄÄ templates/
    ³
    ÃÄÄ tests/
    ³
    ÃÄÄ screenshots/
    ³
    ÃÄÄ requirements.txt
    ³
    ÀÄÄ .env
```

---

# Database Architecture

Application Schema

```
portal
```

Application Tables

```
app_users
query_history
```

Sample Database

```
Pagila
```

Application tables are intentionally separated from the Pagila sample database to simulate a production environment.

---

# Application Flow

```
Browser



Flask



Application Routes



Database Layer



PostgreSQL
```

---

# Implemented Modules

| Module | Status |
|---------|:------:|
| Authentication | ? |
| Dashboard | ? |
| Database Explorer | ? |
| Generic Table Viewer | ? |
| SQL Workspace | ? |
| Query Statistics | ? |
| Query History | ? |

---

# Screenshots

The following screenshots are planned for documentation.

- Login Page
- Dashboard
- Database Explorer
- Generic Table Viewer
- SQL Workspace
- Query History

---

# Installation

Refer to:

```
docs/Installation_Guide.md
```

for complete installation instructions.

---

# Running the Application

Activate the virtual environment.

```
venv\Scripts\activate
```

Start Flask.

```
python src/app.py
```

Open the browser.

```
http://127.0.0.1:5000
```

---

# Testing

Backend tests are located in:

```
workspace/tests/
```

Example:

```
python -m tests.test_password

python -m tests.test_database_explorer

python -m tests.test_table_data

python -m tests.test_execute_select

python -m tests.test_save_query_history

python -m tests.test_get_query_history
```

---

# Git Versioning

The project follows incremental versioning.

Example:

```
V4 Portal Foundation



V5 Database Manager



V6 Query History
```

Each completed sprint is committed independently.

---

# Development Principles

The project follows these principles.

- Generic Database Functions
- Separation of Concerns
- Incremental Development
- Test Before Integration
- Reusable Components
- Migration-Based Database Changes
- Clear Documentation

---

# Roadmap

## Version 6

- Saved Queries
- Pagination
- Search
- Export CSV

## Version 7

- CRUD Operations
- Audit Logs
- User Management

## Version 8

- AWS Deployment
- Amazon RDS
- IAM
- CloudWatch
- Secrets Manager
- CloudFront

---

# Learning Objectives

This project is designed to provide practical experience with:

- Python
- Flask
- PostgreSQL
- SQL
- Database Design
- Git
- Software Architecture
- AWS Deployment

---

# Author

Aman

---

# License

This project is intended for educational and portfolio purposes.

