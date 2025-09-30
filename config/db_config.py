import os

from dotenv import load_dotenv

# Load .env from project root
load_dotenv()

def get_connection():
    import mysql.connector
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        auth_plugin=os.getenv("DB_AUTH_PLUGIN") or "mysql_native_password"
    )
