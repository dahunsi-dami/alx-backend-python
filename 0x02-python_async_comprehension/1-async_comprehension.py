#!/usr/bin/env python3
"""Coroutine called async_comprehension."""

from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Collects 10 random numbers from async_generator-
    -w/ a async comprehension.
    """
    return [i async for i in async_generator()]
