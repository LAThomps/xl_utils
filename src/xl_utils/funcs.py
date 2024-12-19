"""
Helper functions for working with excel files in python
"""
import openpyxl
import pandas as pd
from .utils import in_range

ALPHA_RANGE = range(65, 91)
XL_COLS = [
    chr(i) for i in ALPHA_RANGE
] + [
    chr(i) + chr(j) for i in ALPHA_RANGE for j in ALPHA_RANGE
]


def write_df_to_sheet(
    df: pd.DataFrame,
    sheet_object: openpyxl.worksheet.worksheet.Worksheet,
    start_row: int,
    start_col: int | str
) -> None:
    """
    Utility function to write pandas DataFrame to openpyxl sheet object.
    **row/columns are 1 indexed to match Excel**

    Parameters
    ----------
    df : pd.Dataframe
        What you're writing.
    sheet_object : openpyxl.worksheet.worksheet.Worksheet
        Sheet obj you're writing to.
    start_row : int
        Row to start writing the df's values as read on excel sheet.
    start_col : int | str
        Column to start writing df's values. Will take *1-indexed* integer
        or excel-column string type e.g. 'A' or 'AF'.  The maximum range
        is 'ZZ' which equates to column 702. 
    """
    # error check row input
    assert isinstance(start_row, int), "start_row must be an integer"
    assert start_row > 0, "start_row must be valid excel row value"

    # check and convert integer column inputs if applicable
    if isinstance(start_col, int):
        if in_range(start_col - 1, XL_COLS):
            start_col = XL_COLS[start_col - 1]
        else:
            print(f"start_col out of range, must be in [A, ZZ] range")
            return

    # check range
    if start_col not in set(XL_COLS):
        print(f"start_col: {start_col} not available, must be in [A, ZZ] range")
        return

    # get indexes to help with writing
    start_col_idx = XL_COLS.index(start_col)
    end_col_idx = start_col_idx + df.shape[1] - 1

    # end points
    end_col = XL_COLS[end_col_idx]
    end_row = start_row + df.shape[0] - 1

    # do the writing
    for i, row in enumerate(range(start_row, end_row + 1)):
        for j, col in enumerate(range(start_col_idx, end_col_idx + 1)):
            sheed_object[f"{XL_COLS[col]}{row}"].value = df.iloc[i, j]

    return

def auto_cols(file_path: str, auto_filter: bool = True) -> None:
    """
    Autofit and autofilter all used columns of an excel sheet.

    Parameters
    ----------
    file_path : str
        Path to excel file.
    auto_filter : bool, optional
        Whether or not you want put filters on the columns, by default True
    """
    book = openpyxl.load_workbook(file_path)
    for sheet in book.worksheets:
        curr_sheet = book[sheet.title]
        if auto_filter:
            curr_sheet.auto_filter.ref = curr_sheet.dimensions
        for col in curr_sheet.columns:
            widest = max(len(str(cell.value)) for cell in col)
            curr_sheet.column_dimensions[col[0].column_letter].width = (
                widest + 2 if not auto_filter else widest + 7
            )
    book.save(file_path)
    del book
    return

