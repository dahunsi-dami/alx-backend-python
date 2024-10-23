#!/usr/bin/env python3
"""Type annotated zoom_array function."""

from typing import Tuple, List, TypeVar

T = TypeVar('T')


def zoom_array(lst: Tuple[T, ...], factor: int = 2) -> List[T]:
    """Zooms in on element of input list by a given factor."""
    zoomed_in: List[T] = [
        item for item in lst
        for _ in range(factor)
    ]
    return zoomed_in


array: Tuple[int, ...] = (12, 72, 91)

zoom_2x: List[int] = zoom_array(array)

zoom_3x: List[int] = zoom_array(array, 3)
