#!/usr/bin/env python3
"""Type annotated function element_length."""

from typing import List, Iterable, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns list of tuples where each tuple-
    -contains an element & its length.
    """
    return [(i, len(i)) for i in lst]
