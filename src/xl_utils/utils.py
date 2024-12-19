"""
Helper functions
"""
from typing import Iterable

def in_range(
        index: int,
        list_: Iterable
    ) -> bool:
    """
    Checking if index passed is in range of iterable object.

    Parameters
    ----------
    index : int
        Index value to check.
    list_ : Iterable
        Says list but will work with any iterable object.

    Returns
    -------
    bool
        T/F on if that index is within the range of the iterable object.s
    """
    assert isinstance(index, int), "index must be an integer"
    if (index >= 0) and (index < len(list_)):
        return True
    else:
        return False