"""
cli.py

This module contains the main logic for initializing and running the program.
The module may include functions for handling user input, setting up configurations,
starting services, or executing tasks required by the program.

Usage:
    python -m src.cli.cli <command>
"""

from datetime import datetime
from loguru import logger
import pandas as pd
import click
import humanize
from src.main import data_processor
from src.app.utils.rich_utils import print_dataframe, console
from src.app.config import settings


if settings.debug:
    console.log("Debug mode is ON")
else:
    console.log("Debug mode is OFF")


@click.command()
@click.argument("filepath")
def main(filepath: str) -> None:
    """
    This function is the entry point for the CLI command that processes the given CSV file.

    It performs the following tasks:
    1. Logs the start time of the process.
    2. Reads the CSV file from the specified filepath.
    3. Processes the data using the `data_processor` function.
    4. Prints the processed DataFrame.
    5. Logs the finish time along with the time taken to complete the task.

    Args:
        filepath (str): The path to the CSV file that needs to be processed.

    Returns:
        None
    """
    logger.info("-----------------------------------")
    time_s0 = datetime.now()
    logger.info("** Started at: " + time_s0.strftime("%Y-%m-%d %H:%M:%S"))

    df = pd.read_csv(filepath)
    df = data_processor(df)
    print_dataframe(df)

    time_sn = datetime.now()
    logger.info(
        "** Finished at: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        + f" ({humanize.naturaldelta(time_sn - time_s0)})"
    )
    logger.info("-----------------------------------")


if __name__ == "__main__":
    main()
