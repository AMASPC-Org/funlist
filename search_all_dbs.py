import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INSTANCE_CONNECTION_NAME = "ama-ecosystem-prod:us-west1:ama-central-db-prod"
DB_USER = "postgres"
DB_PASS = "Marsha2025"
TARGET_EMAIL = "ryan@amaspc.com"

connector = Connector()

def get_db_conn(db_name):
    return connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=db_name,
        ip_type=IPTypes.PUBLIC
    )

def main():
    try:
        # First get list of all databases
        temp_pool = sqlalchemy.create_engine("postgresql+pg8000://", creator=lambda: get_db_conn("postgres"))
        with temp_pool.connect() as conn:
            dbs = conn.execute(sqlalchemy.text("SELECT datname FROM pg_database WHERE datistemplate = false")).fetchall()
            db_names = [r[0] for r in dbs]
        
        logger.info(f"Found databases: {db_names}")
        
        results = []
        for db_name in db_names:
            try:
                pool = sqlalchemy.create_engine("postgresql+pg8000://", creator=lambda db=db_name: get_db_conn(db))
                with pool.connect() as conn:
                    # Check if users table exists
                    table_exists = conn.execute(sqlalchemy.text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")).scalar()
                    if table_exists:
                        user = conn.execute(sqlalchemy.text("SELECT id, email, role_id, is_active FROM users WHERE email = :email"), {"email": TARGET_EMAIL}).fetchone()
                        if user:
                            results.append(f"DB: {db_name} | User: {user}")
                        else:
                            results.append(f"DB: {db_name} | User Not Found")
                    else:
                        results.append(f"DB: {db_name} | No users table")
            except Exception as e:
                results.append(f"DB: {db_name} | Error: {str(e)}")

        logger.info("\n".join(results))
        with open("db_search_results.txt", "w") as f:
            f.write("\n".join(results))

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
