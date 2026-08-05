# Architecture

---

# Project

CloudBuild Database Manager

---

# Purpose

This document describes the overall software architecture of the CloudBuild Database Manager application.

It explains:

- System architecture
- Folder structure
- Request flow
- Authentication flow
- SQL execution flow
- Query history flow
- Design principles

This document reflects the application architecture through **Version 6 Sprint 6.1.3**.

---

# High-Level Architecture

```
                 Browser
                     ³
                     ³ HTTP Request
                     
                Flask Application
                     ³
                     
               Application Routes
                     ³
                     
             Database Access Layer
                     ³
                     
              PostgreSQL Database
```

---

# Technology Stack

```
Frontend

HTML
CSS
Jinja2



Backend

Python
Flask



Database Layer

psycopg



Database

PostgreSQL
```

---

# Folder Architecture

```
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
    ³
    ÃÄÄ src/
    ³
    ÃÄÄ static/
    ³
    ÃÄÄ templates/
    ³
    ÃÄÄ tests/
    ³
    ÀÄÄ screenshots/
```

---

# Source Code Structure

```
src/

³
ÃÄÄ app.py

ÃÄÄ config.py

ÃÄÄ constants.py

ÃÄÄ database/
³      db.py

ÀÄÄ utils/
       password.py
```

---

# Application Layers

The application follows a layered architecture.

```
Presentation Layer



Business Logic Layer



Database Layer



PostgreSQL
```

---

# Layer Responsibilities

## Presentation Layer

Responsible for:

- HTML Templates
- Forms
- User Interaction
- Navigation

Files

```
templates/
static/
```

---

## Business Logic Layer

Responsible for:

- Flask Routes
- Request Processing
- Session Validation
- Data Preparation

File

```
src/app.py
```

---

## Database Layer

Responsible for:

- Database Connections
- SQL Execution
- Authentication
- Metadata Retrieval
- Query History

File

```
src/database/db.py
```

---

# Request Flow

```
Browser



HTTP Request



Flask Route



Database Function



PostgreSQL



Database Result



Jinja Template



Browser
```

---

# Authentication Flow

```
Login Form



Username

Password



Password Verification



Session Creation



Dashboard



Protected Pages
```

---

# Database Explorer Flow

```
Dashboard



Database Explorer



List Tables



Select Table



Retrieve Metadata



Retrieve Rows



Render Table
```

---

# SQL Workspace Flow

```
User SQL



Validation



SELECT Only



Execute Query



Retrieve Results



Execution Statistics



Display Results
```

---

# Query History Flow

```
Successful SQL Execution



Save Query



portal.query_history



Retrieve User History



Display History
```

---

# Database Architecture

Two logical areas exist inside PostgreSQL.

## Sample Database

Pagila

Purpose

Learning SQL

Database exploration

Sample business data

---

## Application Schema

```
portal
```

Purpose

Application-specific data

Current Tables

```
app_users

query_history
```

---

# Security Principles

The application currently implements:

- Session-based Authentication
- Password Hash Verification
- Protected Routes
- Read-only SQL Execution
- User-specific Query History

Only SELECT statements are allowed through the SQL Workspace.

---

# Development Workflow

Every feature follows the same lifecycle.

```
Design



Migration



Database Function



Backend Test



Flask Integration



Browser Test



Git Commit



Documentation Update
```

---

# Design Principles

The project follows these principles.

## Separation of Concerns

Routes do not execute SQL directly.

Database operations remain inside the database layer.

---

## Generic Functions

Functions are designed to be reusable.

Example

```
get_table_data()

execute_select_query()
```

---

## Incremental Development

Each sprint produces a working application.

Small commits.

Small changes.

Continuous testing.

---

## Documentation First

Every completed feature is documented.

Architecture

Database

Journal

Release Notes

Feature Log

---

# Current Modules

| Module | Status |
|---------|:------:|
| Authentication | ? |
| Dashboard | ? |
| Database Explorer | ? |
| Generic Table Viewer | ? |
| SQL Workspace | ? |
| Query History | ? |

---

# Planned Architecture

Future versions will introduce:

```
Saved Queries



Pagination



Search



Export



CRUD



Audit Log



AWS Deployment
```

---

# AWS Target Architecture

Planned deployment architecture.

```
Browser



CloudFront



Application Load Balancer



EC2



Gunicorn



Flask



Amazon RDS PostgreSQL



CloudWatch
```

Additional AWS services planned.

- IAM
- Secrets Manager
- Route 53
- ACM
- S3
- Systems Manager

---

# Summary

CloudBuild Database Manager is designed as a production-inspired learning project.

Rather than focusing on CRUD alone, the project emphasizes:

- Software Architecture
- PostgreSQL
- Backend Development
- Secure Authentication
- Database Design
- Testing
- Documentation
- AWS Readiness

The architecture intentionally evolves incrementally so that each version remains stable while introducing new concepts.
