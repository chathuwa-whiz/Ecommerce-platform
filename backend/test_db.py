# test_db.py
import psycopg2
from decouple import config

try:
    conn = psycopg2.connect(
        host=config('DATABASE_HOST'),
        database=config('DATABASE_NAME'),
        user=config('DATABASE_USER'),
        password=config('DATABASE_PASSWORD')
    )
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print(f"Database connection failed: {e}")