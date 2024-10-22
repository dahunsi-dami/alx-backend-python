#!/usr/bin/env python3
"""Type annotated function safely_get_value."""

from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')


# The types of the elements of the input are not known
def safely_get_value(dct: Mapping, key: Any, default: Union[T, None] = None) -> Union[Any, T]:
    """
    Returns value associated w/ key in the dictionary-
    -or the default if the key doesn't exist.
    """
    if key in dct:
        return dct[key]
    else:
        return default
