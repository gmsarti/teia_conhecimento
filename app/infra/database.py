import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

env = os.environ.get("ENVIRONMENT", "development")  # Get the environment
load_dotenv(f".env.{env}")


def query(qry: str):
    # Database connection details
    db_host = os.environ.get("POSTGRES_HOST")
    db_port = os.environ.get("POSTGRES_PORT")
    db_name = os.environ.get("POSTGRES_DB")
    db_user = os.environ.get("POSTGRES_USER")
    db_password = os.environ.get("POSTGRES_PASSWORD")

    # database_url = "postgresql+psycopg2://your_username:your_password@localhost:5432/your_database_name"
    database_url = (
        # "postgresql+psycopg2://postgres:local_password@localhost:5432/postgres"
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    engine = create_engine(database_url)

    with engine.connect() as connection:
        try:
            exec = connection.execute(text(qry))
        except Exception as e:
            print(e)
        result = exec.fetchall()
        print(result)
        return result
