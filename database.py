"""
database.py
-----------
This file has ONE job: open a connection to your PostgreSQL database
and give it to whichever API route asks for it.
"""

import os                                   # built-in module to read environment variables
import psycopg2                             # library that lets Python talk to PostgreSQL
from psycopg2.extras import RealDictCursor  # makes query results come back as dict, e.g. {"cust_id": 1, "name": "Ravi"} instead of a plain tuple (1, "Ravi")
from dotenv import load_dotenv              # OPTIONAL: reads variables from a .env file into the environment

load_dotenv()   # OPTIONAL: only needed if you keep DB credentials in a ".env" file (recommended, keeps passwords out of code)

# Read DB credentials from environment variables.
# The second value in os.getenv(...) is a fallback/default, used only if .env is missing.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "your_database_name")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db():
    """
    This is a "dependency" function.
    FastAPI will call this automatically for every request that needs the database
    (you'll see `db: connection = Depends(get_db)` in the router files).

    - It opens a new connection
    - Hands it to the route (using `yield`)
    - Closes it automatically once the route finishes (even if an error happens)

    NOTE: opening a fresh connection per request is the SIMPLE/beginner way.
    Later, for a bigger project, you would replace this with a "connection pool"
    (e.g. psycopg2.pool) to reuse connections instead of opening a new one every time.
    That part is NOT required for a small learning project.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )
    try:
        yield conn
    finally:
        conn.close()
