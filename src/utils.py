import glob
import os
from datetime import datetime, timedelta
from typing import Tuple


def gerar_datas() -> Tuple:
    """
    Generate dates related to the current period and return them as a tuple.

    Returns:
        Tuple: A tuple containing two dates formatted as "DD/MM/YYYY".
    """

    # Get the current date
    current_date = datetime.now()
    one_year_ago = current_date - timedelta(days=365)
    two_years_ago = current_date - timedelta(days=730)

    # Format the dates in the desired format (DD/MM/YYYY)
    current_date_formatted = current_date.strftime("%d/%m/%Y")
    one_year_ago_formatted = one_year_ago.strftime("%d/%m/%Y")
    two_years_ago_formatted = two_years_ago.strftime("%d/%m/%Y")

    # Return the tuple in the desired format
    return ((current_date_formatted, one_year_ago_formatted),
            (one_year_ago_formatted, two_years_ago_formatted))


def get_files() -> Tuple:
    """
    Get the two most recent files with the .xlsx extension in the
    current directory.

    Returns:
        Tuple: A tuple containing the paths of the two most recent files.
    """

    extension = "*.xlsx"

    # Use the provided directory or get the current directory
    directory = os.getcwd()

    # Combine the directory with the desired extension
    file_pattern = os.path.join(directory, extension)

    # List all files with the .xlsx extension in the directory
    xlsx_files = glob.glob(file_pattern)

    # Sort the files by creation date
    xlsx_files.sort(key=os.path.getctime, reverse=True)

    # Get the two most recent files
    recent_files = xlsx_files[:2]

    return tuple(recent_files)
