"""
=============================================================
Project : Pagila PostgreSQL Web Portal

Version : 6.1.3

File    : config.py

Author  : Aman

Purpose
-------
Load application configuration from the .env file.

Responsibilities
----------------
1. Load database configuration
2. Load application configuration
3. Keep sensitive information outside source code

Last Updated
------------
04-Aug-2026
=============================================================
"""

# ============================================================
# Standard Library Imports
# ============================================================

import os

# ============================================================
# Third-Party Imports
# ============================================================

from dotenv import load_dotenv

# -----------------------------------------------------------
# Load environment variables from .env
# -----------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------
# PostgreSQL Database Configuration
# -----------------------------------------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}


# -----------------------------------------------------------
# Flask Secret Key
# -----------------------------------------------------------
#
# Used by Flask to securely sign user sessions.
# Never hardcode this value in production.
#
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")