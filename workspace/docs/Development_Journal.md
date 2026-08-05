# Development Journal

---

# Project

CloudBuild Database Manager

---

# Purpose

This journal records the chronological development of the project.

Each version documents:

- Features implemented
- Architecture changes
- Database changes
- Major decisions
- Testing
- Lessons learned

---

# Version 1

## Theme

REST API Foundation

---

## Objective

Build a simple REST API using Flask connected to the PostgreSQL Pagila database.

---

## Features

- Flask application created
- PostgreSQL connection established
- REST API endpoint created
- Actor information returned in JSON format

---

## Database

Used existing Pagila tables.

No application tables created.

---

## Learning

- Flask basics
- PostgreSQL connection
- JSON responses
- REST API concepts

---

# Version 2

## Theme

Actor Search Web Application

---

## Objective

Convert the REST API into a browser-based application.

---

## Features

- Home page
- Actor search
- Actor details page
- HTML templates
- CSS styling
- Form handling

---

## Database

No schema changes.

---

## Learning

- Jinja2 templates
- HTML forms
- Flask routing
- User input validation

---

# Version 3

## Theme

Authentication Preparation

---

## Objective

Prepare the application for secure user authentication.

---

## Features

- Project restructuring
- Authentication planning
- Password hashing research
- Session management planning

---

## Database

No schema changes.

---

## Learning

- Authentication design
- Password security
- Flask sessions

---

# Version 4

## Theme

Portal Foundation

---

## Objective

Transform the project into a database management portal.

---

## Features

### Authentication

- Login page
- Logout
- Session management
- Protected routes

### Dashboard

- Secure dashboard
- Navigation
- Portal layout

### Database

Created application schema.

```
portal
```

Created application table.

```
app_users
```

Created administrator account.

---

## Migrations

001_create_portal_schema.sql

002_create_app_users.sql

003_seed_admin_user.sql

---

## Learning

- Password hashing
- Database migrations
- Authentication
- Session security

---

# Version 5

## Theme

Database Manager

---

## Objective

Build generic database exploration tools.

---

## Features

### Database Explorer

- List database tables
- Generic table viewer
- Table summary

### Metadata

- Column information
- Primary key information
- Row counts

### SQL Workspace

- Execute SQL
- Read-only validation
- Error handling

### Query Statistics

Display

- Execution time
- Rows returned
- Columns returned

---

## Database

No new application tables.

---

## Major Design Decision

Database functions should be generic rather than table-specific.

---

## Learning

- Generic SQL
- Metadata queries
- Database abstraction
- Software architecture

---

# Version 6

## Theme

Application-Owned Data

---

## Objective

Begin storing application-specific information inside PostgreSQL.

---

## Sprint 6.1.1

### Feature

Query History Backend

### Database

Migration

```
004_create_query_history.sql
```

Table

```
portal.query_history
```

Implemented

```
save_query_history()
```

Backend test completed.

---

## Sprint 6.1.2

### Feature

Automatic Query History

Implemented

- SQL execution integration
- Automatic history recording

Only successful queries are stored.

---

## Sprint 6.1.3

### Feature

Query History Page

Implemented

```
get_query_history()
```

Added

```
/query-history
```

Created

```
query-history.html
```

Dashboard navigation updated.

Backend testing completed.

Browser testing completed.

---

## Database

Current Application Tables

```
portal.app_users

portal.query_history
```

---

## Learning

- Database design
- Foreign keys
- Application-owned data
- SQL logging
- Backend architecture

---

# Git Workflow

The project follows incremental development.

Each sprint includes

- Database
- Backend
- Testing
- Flask
- UI
- Documentation
- Git commit

---

# Coding Standards

Current standards

- Generic database functions
- Well-documented code
- Consistent comments
- Incremental commits
- Versioned migrations

---

# Challenges Encountered

## Import Issues

Resolved by organizing project imports consistently.

---

## Session Management

Implemented protected routes and login validation.

---

## SQL Validation

Restricted SQL Workspace to SELECT statements.

---

## Timezone Handling

Resolved naive vs aware datetime issues.

---

## Migration Execution

Established the rule that migrations must be:

1. Written
2. Executed
3. Verified
4. Used by the application

before backend development continues.

---

# Lessons Learned

Throughout development the following principles became increasingly important.

- Build generic solutions.
- Test backend before UI.
- Keep migrations versioned.
- Separate application data from sample data.
- Commit after every completed sprint.
- Document architectural decisions.

---

# Current Status

Current Version

```
Version 6 Sprint 6.1.3
```

Completed Modules

- Authentication
- Dashboard
- Database Explorer
- Generic Table Viewer
- SQL Workspace
- Query Statistics
- Query History

Application Status

Stable

Development Continues.

---

# Next Planned Work

Version 6

- Saved Queries
- Pagination
- Search
- Export

Version 7

- CRUD
- Audit Log
- User Management

Version 8

- AWS Deployment
- Monitoring
- Security

---

# Journal Maintenance

After every completed sprint, update this document with:

- Version
- Sprint
- Features
- Database changes
- Lessons learned
- Architectural decisions

This journal should remain a chronological history of the project throughout its lifetime.
