"""
main.py

Test module for the main.py functionality.

This module contains unit tests for the functions and features implemented in
the main.py module. The tests ensure that the core functionality of the
application works as expected. It includes tests for edge cases, valid inputs,
and error handling.

Usage:
    pytest tests/integration/main.py
"""

import pytest
import pandas as pd
from src.main import data_processor
from src.app.utils.data_utils import clean_data, aggregate_data


# Sample input data for testing
@pytest.fixture
def sample_data() -> pd.DataFrame:
    """
    Provides a sample DataFrame to be used in tests.

    Returns:
        pd.DataFrame: A sample DataFrame with 'category' and 'value' columns.
    """
    return pd.DataFrame({"category": ["A", "B", "A", "B", "A"], "value": [10, 20, 30, 40, 50]})


# Test for the data_processor function
def test_data_processor() -> None:
    """
    Tests the `data_processor` function to ensure it produces the correct result.

    The test checks that the `data_processor` function correctly cleans and aggregates the
    input data. The result of `data_processor` should match the expected output from
    applying the `clean_data` and `aggregate_data` functions.

    Asserts:
        - The output of `data_processor` should match the expected aggregated DataFrame.

    Returns:
        None
    """
    cleaned_df = clean_data(sample_data)
    aggregated_df = aggregate_data(cleaned_df, "category", "value")
    pd.testing.assert_frame_equal(data_processor(sample_data), aggregated_df)


# Test for empty DataFrame input
def test_empty_dataframe() -> None:
    """
    Tests the `data_processor` function with an empty DataFrame to ensure it handles it correctly.

    The test checks that when an empty DataFrame is passed to `data_processor`, it should
    return an empty DataFrame with the same columns ('category', 'value').

    Asserts:
        - The result should be an empty DataFrame with the correct column names.

    Returns:
        None
    """
    empty_df = pd.DataFrame(columns=["category", "value"])
    result_df = data_processor(empty_df)
    pd.testing.assert_frame_equal(result_df, pd.DataFrame(columns=["category", "value"]))
