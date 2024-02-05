from undersampling import undersample_daily_weather_data, undersample_grid_data, DatabaseTables, FetchDBData

import pandas as pd

from imblearn.under_sampling import NearMiss

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

import lightgbm as lgb

import numpy as np

import joblib


from pathlib import Path
from os import path


def undersample_daily_weather():
    under_sampler = NearMiss(version=3, sampling_strategy=0.3)
    weather_data, has_incident = undersample_daily_weather_data(
        under_sampler, DatabaseTables.daily_weather_with_incidents
    )
    weather_data.loc[:, "has_incident"] = has_incident

    return weather_data


def undersample_grid():
    under_sampler = NearMiss(version=3, sampling_strategy=1)
    grid_data, has_incident = undersample_grid_data(under_sampler)
    grid_data.loc[:, "has_incident"] = has_incident

    return grid_data


def combine_all_data(weather_incidents, grid_incidents):
    incidents_grid_date = FetchDBData(DatabaseTables.count_tree_incidents_per_grid_date).get_database_data()
    weather_incidents["dt_iso"] = weather_incidents["dt_iso"].astype(str).str.split(' ').apply(lambda x: x[0])
    incidents_grid_date["date"] = incidents_grid_date["date"].astype(str)
    weather_data_incidents = (
        weather_incidents
        .query("`has_incident` == 1")
        .merge(incidents_grid_date, left_on="dt_iso", right_on="date")
    )

    weather_grid_has_incident = (
        weather_data_incidents
        .drop(["count_incidents_y", "count_incidents_x", "max_incident_priority", "has_incident"], axis=1)
        .merge(grid_incidents, on="grid_id")
    )

    weather_grid_no_incident = (
        grid_incidents
        .query("`has_incident` == 0")
        .merge(weather_data_incidents, how="cross")
        .drop(
            ["count_incidents_y", "count_incidents_x", "max_incident_priority", "has_incident_y", "grid_id_y"],
            axis=1
        )
        .rename(columns={"grid_id_x": "grid_id", "has_incident_x": "has_incident"})
    )

    weather_data_no_incidents = (
        weather_incidents
        .query("`has_incident` == 0")
        .merge(incidents_grid_date, left_on="dt_iso",right_on="date")
    )

    weather_grid_weather_no_incidents = (
        grid_incidents
        .query("`has_incident` == 0")
        .merge(weather_data_incidents,how="cross")
        .drop(
            ["count_incidents_y", "count_incidents_x", "max_incident_priority", "has_incident_y", "grid_id_y"],
            axis=1
        )
        .rename(columns={"grid_id_x": "grid_id", "has_incident_x": "has_incident"})
    )

    weather_grid_weather_no_incidents = weather_grid_weather_no_incidents[weather_grid_has_incident.columns]

    weather_grid_no_incident = weather_grid_no_incident[weather_grid_has_incident.columns]

    combined_data = pd.concat([
        weather_grid_has_incident,
        weather_grid_weather_no_incidents,
        weather_grid_no_incident])

    combined_data = combined_data.drop(["hour", "date", "total_incident_duration"], axis=1)

    combined_data = combined_data.drop(["grid_id", "weather_main", "dt_iso"], axis=1)

    return combined_data


def get_train_test_split(combined_data):
    exclude_cols = [
        "dt_iso",
        "grid_id",
    ]

    target_col = 'has_incident'

    predictor_cols = [col for col in combined_data.columns if col not in [target_col]]
    one_hot_cols = ["weather_main"]
    numeric_cols = [col for col in predictor_cols if col not in exclude_cols + one_hot_cols]

    X = combined_data[predictor_cols]
    y = combined_data[target_col]

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    return x_train, x_test, y_train, y_test


def train_model(x_train, y_train, decision_boundary):

    boundary = 0.04

    params = {
        'boosting_type': 'gbdt',
        'reg_alpha': 1,
        'reg_lambda': 5,
        'num_leaves': 90,
        'num_boost_round': 1_000,
        'scale_pos_weight': 20_000,
        'metric': 'binary_error',
        'verbose': 0
    }

    def lgb_f1_score(y_hat, data):
        y_true = data.get_label()
        y_hat = np.where(y_hat < boundary, 0, 1)
        return 'f1', f1_score(y_true, y_hat), True

    model = lgb.train(params, lgb.Dataset(decision_boundary, label=y_train), feval=lgb_f1_score)

    return model


def get_metrics(model, x_test, y_test, boundary):
    y_pred = model.predict(x_test, num_iteration=model.best_iteration)
    data = pd.DataFrame(
        {
            "actual": y_test.reset_index().drop("index", axis=1)["has_incident"],
            "predicted": np.where(y_pred < boundary, 0, 1),
        },
    )

    print(pd.crosstab(data.actual, data.predicted))

    f1 = f1_score(y_test, np.where(y_pred < boundary, 0, 1))
    recall = recall_score(y_test, np.where(y_pred < boundary, 0, 1))
    precision = precision_score(y_test, np.where(y_pred < boundary, 0, 1))
    accuracy = accuracy_score(y_test, np.where(y_pred < boundary, 0, 1))
    print(f"=" * 100)
    print(f"Accuracy in testing: {accuracy}")
    print(f"F1 Score in testing: {f1}")
    print(f"Recall Score in testing: {recall}")
    print(f"Precision in testing: {precision}")
    print(f"=" * 100)

    return f1, recall, precision, accuracy


if __name__ == '__main__':

    save_path = Path(__file__).resolve().parents[1] / "files"
    assert path.exists(save_path)

    weather_data = undersample_daily_weather()
    grid_data = undersample_grid()
    x_train, x_test, y_train, y_test = get_train_test_split(combine_all_data(weather_data, grid_data))
    model = train_model(x_train, y_train, decision_boundary=0.04)
    f1, recall, precision, accuracy = get_metrics(model, x_test, y_test, boundary=0.04)

    joblib.dump(model, f"lightgbm_model_{f1:.2f}.joblib")