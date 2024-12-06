"""
main.py

This module serves as the main entry point for the application.
Handles the core logic and execution flow of the application.

Usage:
    python -m src.main
"""

import pandas as pd
from src.app.utils.data_utils import clean_data, aggregate_data


def data_processor(df: pd.DataFrame) -> pd.DataFrame:
    """
    A data processing pipeline that combines multiple steps:
    1. Converts input data into a DataFrame.
    2. Cleans the DataFrame by removing NaN rows and normalizing column names.
    3. Aggregates the data by summing values grouped by the "category" column.

    Args:
        df (pd.DataFrame): The input data in DataFrame format to be processed.

    Returns:
        pd.DataFrame: A processed DataFrame with aggregated results.
    """
    cleaned_df = clean_data(df)
    aggregated_df = aggregate_data(cleaned_df, "category", "value")
    return aggregated_df
