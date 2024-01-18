import psycopg2
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
                        psycopg2.errors.InFailedSqlTransaction
                ) as e:
                    print(e)
                    connection.rollback()
        cursor.close()


if __name__ == '__main__':
    load_scripts_into_database()