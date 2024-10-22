#!/usr/bin/env python3
"""Type-annotated function sum_mixed_list."""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Returns the sum of a list of ints and floats as a float."""
    return sum(mxd_lst)
