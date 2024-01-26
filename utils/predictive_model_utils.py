import joblib
from django.db.models import Q


def get_model_choices(predictive_models):
    choices = [
        (
            f'{model.name},v.{model.version}',
            f'{model.name},v.{model.version}'
        )
        for model in predictive_models
    ]

    return choices


def load_model(data, predictive_models):
    model_name, version = data['model'].split(",v.")
    filtered_models = predictive_models.filter(Q(name=model_name) | Q(version=version)).first()
    predictive_model = joblib.load(filtered_models.file.path)
    model_type = filtered_models.model_type

    return predictive_model, model_type
