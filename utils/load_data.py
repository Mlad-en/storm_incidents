from django.db import transaction


def load_data_into_db(data, validation_model, django_model, logger):
    with transaction.atomic():
        for record in data.to_dict("records"):
            item = validation_model(**record)
            django_model.objects.create(**item.model_dump())
            logger.info("Record loaded successfully.")
