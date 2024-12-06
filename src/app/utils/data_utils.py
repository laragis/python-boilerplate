"""
data_utils.py

This module provides utility functions to handle common data processing tasks,
such as data cleaning, transformation, and validation.
"""

import pandas as pd


def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the input DataFrame by performing the following operations:
    1. Removes rows with NaN values.
    2. Normalizes column names by stripping whitespace and converting to lowercase.

    Args:
        dataframe (pd.DataFrame): The input DataFrame to be cleaned.

    Returns:
        pd.DataFrame: A cleaned DataFrame with NaN rows removed and normalized column names.
    """
    cleaned_df = dataframe.dropna()
    cleaned_df.columns = cleaned_df.columns.str.strip().str.lower()
    return cleaned_df


def aggregate_data(dataframe: pd.DataFrame, group_by_col: str, agg_col: str) -> pd.DataFrame:
    """
    Aggregates data in the DataFrame by grouping based on a specified column
    and calculating the sum of another specified column.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing the data.
        group_by_col (str): The name of the column to group by.
        agg_col (str): The name of the column to aggregate by summing its values.

    Raises:
        ValueError: If either `group_by_col` or `agg_col` is not present in the DataFrame.

    Returns:
        pd.DataFrame: A new DataFrame with grouped data and the aggregated sum.
    """
    if group_by_col not in dataframe.columns or agg_col not in dataframe.columns:
        raise ValueError("Columns not found in the dataframe")
    return dataframe.groupby(group_by_col)[agg_col].sum().reset_index()
