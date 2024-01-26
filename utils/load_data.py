import psycopg2
from pandas.io import sql as sql_io
import pandas as pd
from django.db import transaction
import os
from pathlib import Path
from dotenv import load_dotenv


def load_data_into_db(data, validation_model, django_model, logger):
    with transaction.atomic():
        for record in data.to_dict("records"):
            item = validation_model(**record)
            django_model.objects.create(**item.model_dump())
            logger.info("Record loaded successfully.")


def get_connection():
    load_dotenv()
    connection = psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST_NAME"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )

    return connection


def get_script_files():
    project_root = Path(__file__).resolve().parent.parent
    scripts_dir = project_root / "scripts"
    assert os.path.exists(scripts_dir)
    scripts = [scripts_dir/script for script in os.listdir(scripts_dir) if script.endswith(".sql")]
    scripts.sort()
    return scripts


def load_scripts_into_database():
    with get_connection() as connection:
        cursor = connection.cursor()
        for script in get_script_files():
            print(f"loading script: {script}")
            with open(script, "r") as src:
                try:
                    cursor.execute(src.read())
                    connection.commit()
                except (
                        psycopg2.errors.DuplicateTable,
                        psycopg2.errors.UniqueViolation,
                        psycopg2.errors.InFailedSqlTransaction,
                        psycopg2.errors.UndefinedTable,
                        psycopg2.errors.NotSupportedError
                ) as e:
                    print(e)
                    print(script)
                    connection.rollback()
        cursor.close()


def get_data_from_db(query):
    connection = get_connection()
    return sql_io.read_sql_query(query, con=connection)


if __name__ == '__main__':
    load_scripts_into_database()
