import warnings
from enum import Enum, auto

import numpy as np
import pandas as pd
from imblearn.under_sampling import NearMiss, RandomUnderSampler, TomekLinks
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_transformer, make_column_selector, ColumnTransformer

from utils.load_data import get_data_from_db


class DatabaseTables(Enum):
    filtered_weather_with_count_incidents = auto()
    grid_environment_with_incidents = auto()
    count_tree_incidents_per_grid_date = auto()
    daily_weather_with_incidents = auto()


class FetchDBData:

    def __init__(self, data_base_table: DatabaseTables):
        self.data_base_table = data_base_table

    def get_query(self):
        if self.data_base_table == DatabaseTables.filtered_weather_with_count_incidents:
            return "select * from filtered_weather_with_count_incidents"

        if self.data_base_table == DatabaseTables.grid_environment_with_incidents:
            return "select * from grid_environment_with_incidents"

        if self.data_base_table == DatabaseTables.count_tree_incidents_per_grid_date:
            return "select * from count_tree_incidents_per_grid_date"

        if self.data_base_table == DatabaseTables.daily_weather_with_incidents:
            return "select * from daily_weather_with_incidents"

        raise NotImplementedError()

    def get_database_data(self) -> pd.DataFrame:

        warnings.simplefilter(action='ignore', category=UserWarning)

        query = self.get_query()
        data = get_data_from_db(query=query)
        return data


def split_data(data: pd.DataFrame, stratification_column: str) -> tuple[pd.DataFrame, pd.Series]:
    variable_columns = [col for col in data.columns if col != stratification_column]
    variables, stratified = data[variable_columns], data[stratification_column]
    return variables, stratified


def get_column_transformers(ordinal_columns, one_hot_columns) -> ColumnTransformer:
    transformations = make_column_transformer(
        (OneHotEncoder(), one_hot_columns),
        (OrdinalEncoder(), ordinal_columns),
        ("passthrough", make_column_selector(dtype_include="number")),
    )

    return transformations


def get_one_hot_columns(transformers, x_resampled) -> tuple[np.ndarray | None, int]:
    try:
        count_oh_categories = transformers.named_transformers_['onehotencoder'].categories_[0].shape[0]
        one_hot_cols = (
            transformers
            .named_transformers_['onehotencoder']
            .inverse_transform(x_resampled[:, 0:count_oh_categories])
        )

    except AttributeError as e:
        count_oh_categories = 0
        one_hot_cols = None

    return one_hot_cols, count_oh_categories


def get_ordinal_columns(transformers, x_resampled, index) -> np.ndarray:
    ordinal_columns = (
        transformers
        .named_transformers_['ordinalencoder']
        .inverse_transform(
            x_resampled[:, index]
            .reshape(-1, 1)
        )
    )
    return ordinal_columns


def inverse_transform_columns_to_df(
        transformers: ColumnTransformer,
        x_resampled: np.ndarray,
        variables_columns: list[str],
        ordinal_column_name: str,
        one_hot_column_name: str
) -> pd.DataFrame:

    one_hot_cols, index = get_one_hot_columns(transformers, x_resampled)
    ordinal_columns = get_ordinal_columns(transformers, x_resampled, index)

    df = pd.DataFrame(x_resampled[:, index + 1:])
    df.columns = [col for col in variables_columns if col not in [ordinal_column_name, one_hot_column_name]]
    df[ordinal_column_name] = pd.Series(ordinal_columns.reshape(ordinal_columns.shape[0], ))

    if one_hot_cols is not None:
        df[one_hot_column_name] = pd.Series(one_hot_cols.reshape(one_hot_cols.shape[0], ))

    return df


def undersample_weather_data(under_sampler: NearMiss | RandomUnderSampler | TomekLinks) -> pd.DataFrame:

    data = FetchDBData(DatabaseTables.filtered_weather_with_count_incidents).get_database_data()
    variables, has_incident = split_data(data, stratification_column="has_incident")
    transformers = get_column_transformers(ordinal_columns=["dt_iso"], one_hot_columns=["weather_main"])
    variables_transformed = transformers.fit_transform(variables)
    variables_resampled, strat = under_sampler.fit_resample(variables_transformed, has_incident)
    print("Ratio of Hourly Weather:")
    print(strat.value_counts())
    dataframe = inverse_transform_columns_to_df(
        transformers,
        variables_resampled,
        variables.columns,
        "dt_iso",
        "weather_main"
    )
    return dataframe


def undersample_grid_data(under_sampler: NearMiss | RandomUnderSampler | TomekLinks):
    data = FetchDBData(DatabaseTables.grid_environment_with_incidents).get_database_data()
    variables, has_incident = split_data(data, stratification_column="has_incident")
    transformers = get_column_transformers(ordinal_columns=["grid_id"], one_hot_columns=[])
    variables_transformed = transformers.fit_transform(variables)
    variables_resampled, strat = under_sampler.fit_resample(variables_transformed, has_incident)
    print("Ratio of Grids:")
    print(strat.value_counts())
    df = inverse_transform_columns_to_df(
        transformers,
        variables_resampled,
        variables.columns,
        "grid_id",
        ""
    )
    return df, strat


def undersample_daily_weather_data(under_sampler: NearMiss | RandomUnderSampler | TomekLinks):
    data = FetchDBData(DatabaseTables.daily_weather_with_incidents).get_database_data()
    variables, has_incident = split_data(data, stratification_column="has_incident")
    transformers = get_column_transformers(ordinal_columns=["dt_iso"], one_hot_columns=["weather_main"])
    variables_transformed = transformers.fit_transform(variables)
    variables_resampled, strat = under_sampler.fit_resample(variables_transformed, has_incident)
    print("Ratio of Daily Weather:")
    print(strat.value_counts())
    dataframe = inverse_transform_columns_to_df(
        transformers,
        variables_resampled,
        variables.columns,
        "dt_iso",
        "weather_main"
    )
    return dataframe
