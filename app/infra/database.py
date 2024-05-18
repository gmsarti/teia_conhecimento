from sqlalchemy import create_engine, text


def query(qry: str):
    # Database connection details
    # database_url = "postgresql+psycopg2://your_username:your_password@localhost:5432/your_database_name"
    database_url = (
        "postgresql+psycopg2://postgres:local_password@localhost:5432/postgres"
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
