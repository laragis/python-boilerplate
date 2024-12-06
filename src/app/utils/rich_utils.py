"""
rich_utils.py

This module provides utility functions to leverage the Rich library for creating visually appealing
and enhanced console outputs.
"""

import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()


def print_dataframe(df: pd.DataFrame) -> None:
    """
    Prints a pandas DataFrame as a rich-styled table.

    Args:
        df: The pandas DataFrame to print.

    Returns:
        None
    """
    table = Table(show_header=True, header_style="bold magenta")

    for column in df.columns:
        table.add_column(column, justify="center")

    for _, row in df.iterrows():
        table.add_row(*[str(value) for value in row])

    console.print(table)
