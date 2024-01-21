import pandas as pd
from imblearn.under_sampling import NearMiss
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_transformer, make_column_selector


from utils.load_data import get_data_from_db


def get_weather_incident_data():
    query = "select * from filtered_weather_with_count_incidents"
    data = get_data_from_db(query=query)
    return data


def split_data(data, stratification_column):
    variable_columns = [col for col in data.columns if col != stratification_column]
    variables, stratified = data[variable_columns], data[stratification_column]
    return variables, stratified


def get_column_transformers(ordinal_columns, one_hot_columns):
    transformations = make_column_transformer(
        (OneHotEncoder(), one_hot_columns),
        (OrdinalEncoder(), ordinal_columns),
        ("passthrough", make_column_selector(dtype_include="number")),
    )

    return transformations


def inverse_transform_columns_to_df(transformers, x_resampled, variables_columns):

    count_oh_categories = transformers.named_transformers_['onehotencoder'].categories_[0].shape[0]

    weather_main = transformers.named_transformers_['onehotencoder'].inverse_transform(
        x_resampled[:, 0:count_oh_categories])

    dt_iso = (
        transformers
        .named_transformers_['ordinalencoder']
        .inverse_transform(
            x_resampled[:, count_oh_categories]
            .reshape(-1, 1)
        )
    )

    df = pd.DataFrame(x_resampled[:, count_oh_categories + 1:])
    df.columns = [col for col in variables_columns if col not in ['dt_iso', 'weather_main']]
    df["dt_iso"] = pd.Series(dt_iso.reshape(dt_iso.shape[0], ))
    df["weather_main"] = pd.Series(weather_main.reshape(dt_iso.shape[0], ))

    return df


def undersample_weather_data(under_sampler):

    data = get_weather_incident_data()
    variables, has_incident = split_data(data, stratification_column="has_incident")
    transformers = get_column_transformers(ordinal_columns=["dt_iso"], one_hot_columns=["weather_main"])
    variables_transformed = transformers.fit_transform(variables)
    variables_resampled, _ = under_sampler.fit_resample(variables_transformed, has_incident)
    dataframe = inverse_transform_columns_to_df(transformers, variables_resampled, variables.columns)
    return dataframe


if __name__ == '__main__':
    under_sampler = NearMiss(sampling_strategy=0.1, version=1)
    data = undersample_weather_data(under_sampler)
    print(data.columns)