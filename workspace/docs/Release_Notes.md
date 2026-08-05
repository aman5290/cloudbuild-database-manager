# Release Notes

---

# Version 6 Sprint 6.1.3

Release Date

(To be updated)

---

## New Features

### Query History

Added automatic recording of successful SQL queries.

Implemented:

- save_query_history()
- get_query_history()
- Query History page
- Dashboard navigation

---

## Database

Added

portal.query_history

Migration

004_create_query_history.sql

---

## Improvements

- User-specific query history
- Query ordering
- Automatic timestamps

---

## Testing

Completed

- Backend Tests
- Browser Tests
- Database Verification

---

## Known Limitations

- Failed queries are not stored.
- Query history cannot yet be deleted.
- No pagination.
- No search.

---

# Previous Releases

## Version 5

Database Manager

- SQL Workspace
- Database Explorer
- Metadata
- Execution Statistics

---

## Version 4

Portal Foundation

- Login
- Dashboard
- Authentication

---

## Version 2

Actor Search

---

## Version 1

REST API
