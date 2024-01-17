from typing import Literal
from pathlib import Path
from os.path import exists

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
import lightgbm as lgb
import joblib

from utils.trees import TreesData, TreeColumnsEnglish


class GeometryToLatLonTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer used to split geometry column into latitude and longitude columns inline.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy['latitude'] = X_copy[TreeColumnsEnglish.geometry].apply(lambda point: point.y)
        X_copy['longitude'] = X_copy[TreeColumnsEnglish.geometry].apply(lambda point: point.x)
        return X_copy[['latitude', 'longitude']]


class DataSplit:
    """
    Utility class used to convenience.
    """

    def __init__(self, x, y):
        self.predictors = x
        self.outcome = y


class Data:
    """
    Utility class used to convenience.
    """

    def __init__(self, x_train, x_test, y_train, y_test):
        self.TRAINING = DataSplit(x_train, y_train)
        self.TESTING = DataSplit(x_test, y_test)


def get_training_test_split(predictors, target, random_state):
    x_train, x_test, y_train, y_test = train_test_split(
        predictors,
        target,
        test_size=0.2,
        random_state=random_state,
    )

    return Data(x_train, x_test, y_train, y_test)


def get_predictor_columns():
    return [
        TreeColumnsEnglish.tree_type,
        TreeColumnsEnglish.tree_height,
        TreeColumnsEnglish.species_name_short,
        TreeColumnsEnglish.species_name_top,
        TreeColumnsEnglish.trunk_diameter_class,
        TreeColumnsEnglish.geometry
    ]


def get_predictors(dataframe):
    predictor_cols = get_predictor_columns()
    return dataframe[predictor_cols]


def get_outcome(dataframe):
    outcome_col = TreeColumnsEnglish.tree_age
    return dataframe[outcome_col]


def get_pipeline():
    ordinal_columns = [
        TreeColumnsEnglish.tree_height,
        TreeColumnsEnglish.tree_type,
        TreeColumnsEnglish.species_name_short,
        TreeColumnsEnglish.species_name_top,
        TreeColumnsEnglish.trunk_diameter_class
    ]

    geometry_columns = [
        TreeColumnsEnglish.geometry
    ]

    columns_transforms = make_column_transformer(
        (OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), ordinal_columns),
        (GeometryToLatLonTransformer(), geometry_columns),
        remainder='drop'
    )
    model = lgb.LGBMRegressor()
    return Pipeline(
        [
            ("column_transformation", columns_transforms),
            ("model", model),
        ]
    )


def get_tuning_params():
    return {
        "model__max_depth": [20, 50, 100, 200],
        "model__num_leaves": [20, 40, 100, 120],
        "model__learning_rate": [0.01, 0.05, 0.1, 0.2, 0.3],
        "model__n_estimators": [100, 500, 700, 1000],
        "model__colsample_bytree": [0.3, 0.5, 0.7, 1]
    }


def get_best_estimator(model, tuning_parameters, data):
    grid_search = RandomizedSearchCV(
        model,
        tuning_parameters,
        cv=5,
        scoring=["neg_mean_squared_error", "neg_mean_absolute_error"],
        refit="neg_mean_absolute_error",
        n_jobs=5
    )
    grid_search.fit(data.TRAINING.predictors, data.TRAINING.outcome)
    return grid_search.best_estimator_


def get_predictions_mae(model, data, mode: Literal["train", "test"]):

    if mode == "train":
        train_predictions = model.predict(data.TRAINING.predictors)
        mae_error = mean_absolute_error(data.TRAINING.outcome, train_predictions)
    else:
        train_predictions = model.predict(data.TESTING.predictors)
        mae_error = mean_absolute_error(data.TESTING.outcome, train_predictions)

    return mae_error


def persist_model(model, path: str):
    joblib.dump(model, path)


def generate_predictions(data):
    missing_year_trees = data[data[TreeColumnsEnglish.plant_year] <= 1800].copy()

    if not missing_year_trees.empty:
        model_file = Path(__file__).resolve().parents[1] / "predictive_models/tree_age_model.joblib"
        assert exists(model_file)
        age_model = joblib.load(str(model_file))
        correct_year_trees = data[data[TreeColumnsEnglish.plant_year] > 1800].copy()
        preds = missing_year_trees[get_predictor_columns()]
        test_predictions = age_model.predict(preds)
        missing_year_trees[TreeColumnsEnglish.tree_age] = test_predictions.round(0)
        missing_year_trees[TreeColumnsEnglish.predicted_age] = True
        data = pd.concat([correct_year_trees, missing_year_trees])

    return data


if __name__ == '__main__':

    models_dir = Path(__file__).resolve().parents[1] / "predictive_models"
    assert exists(models_dir)

    trees = TreesData().clean_data().dataframe
    valid_year_trees = trees[trees[TreeColumnsEnglish.plant_year] >= 1800].copy()
    predictors = get_predictors(valid_year_trees)
    outcome = get_outcome(valid_year_trees)
    data = get_training_test_split(predictors, outcome, 123)
    model_pipeline = get_pipeline()
    tuning_params = get_tuning_params()
    best_estimator = get_best_estimator(model_pipeline, tuning_params, data)
    print(get_predictions_mae(best_estimator, data, "train"))
    print(get_predictions_mae(best_estimator, data, "test"))
    persist_model(best_estimator, str(models_dir / "tree_age_model.joblib"))
