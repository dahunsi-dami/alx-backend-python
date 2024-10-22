#!/usr/bin/env python3
"""Type annotated function safe_first_element."""

from typing import Sequence, Any, Union


# The types of the elements of the input are not known
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Returns 1st element of sequence (if the sequence exists) or-
    -returns None.
    """
    if lst:
        return lst[0]
    else:
        return None
