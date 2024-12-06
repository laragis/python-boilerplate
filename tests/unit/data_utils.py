"""
data_utils.py

Test module for the data utilities functions.

This module contains unit tests for the functions defined in the data_utils.py
module. It validates the correctness and robustness of the utility functions
related to data processing, transformation, and manipulation. The tests check
for correct handling of various data types, edge cases, and expected errors.

Usage:
    pytest tests/unit/data_utils.py
"""

import pytest
import pandas as pd
from src.app.utils.data_utils import clean_data, aggregate_data


# Sample input data for testing
@pytest.fixture
def sample_data() -> pd.DataFrame:
    """
    Provides a sample DataFrame to be used in tests.

    Returns:
        pd.DataFrame: A sample DataFrame with 'Category' and 'Value' columns.
    """
    return pd.DataFrame({"Category": ["A", "B", "A", "B", "A"], "Value": [10, 20, 30, 40, 50]})


# Test for clean_data function
def test_clean_data() -> None:
    """
    Tests the `clean_data` function to ensure it removes rows with NaN values
    and normalizes column names.

    The test checks that the row with NaN value is removed and the column names
    are normalized (stripped of whitespace and converted to lowercase).

    Asserts:
        - The NaN value row should be removed.
        - The column names should be normalized to ['category', 'value'].

    Returns:
        None
    """
    sample_data().loc[2, "Value"] = None
    cleaned_df = clean_data(sample_data)

    # Ensure that the NaN row is removed
    expected_cleaned_data = pd.DataFrame(
        {"category": ["A", "B", "B", "A"], "value": [10, 20, 40, 50]}
    )
    pd.testing.assert_frame_equal(cleaned_df, expected_cleaned_data)


# Test for aggregate_data function
def test_aggregate_data() -> None:
    """
    Tests the `aggregate_data` function to ensure it correctly aggregates data
    by summing values based on the specified group.

    The test checks if the aggregation produces the correct sum for each category.

    Asserts:
        - The aggregated DataFrame should contain correct sums for each category.

    Returns:
        None
    """
    cleaned_df = clean_data(sample_data)
    aggregated_df = aggregate_data(cleaned_df, "category", "value")

    # Check if the aggregation is correct
    expected_aggregated_data = pd.DataFrame({"category": ["A", "B"], "value": [90, 60]})
    pd.testing.assert_frame_equal(aggregated_df, expected_aggregated_data)


# Test for empty DataFrame input to clean_data
def test_empty_dataframe_clean_data() -> None:
    """
    Tests the `clean_data` function with an empty DataFrame to ensure it handles
    empty input correctly.

    The test checks that an empty DataFrame remains empty after cleaning.

    Asserts:
        - The result should be an empty DataFrame with the same columns.

    Returns:
        None
    """
    empty_df = pd.DataFrame(columns=["Category", "Value"])
    cleaned_df = clean_data(empty_df)
    pd.testing.assert_frame_equal(cleaned_df, empty_df)


# Test for empty DataFrame input to aggregate_data
def test_empty_dataframe_aggregate_data() -> None:
    """
    Tests the `aggregate_data` function with an empty DataFrame to ensure it handles
    empty input correctly.

    The test checks that an empty DataFrame passed to `aggregate_data` results
    in an empty DataFrame with the expected columns.

    Asserts:
        - The result should be an empty DataFrame with the correct column names.

    Returns:
        None
    """
    empty_df = pd.DataFrame(columns=["category", "value"])
    aggregated_df = aggregate_data(empty_df, "category", "value")
    pd.testing.assert_frame_equal(aggregated_df, pd.DataFrame(columns=["category", "value"]))
