#!/usr/bin/env python3
"""Async routine named wait_n."""

import asyncio
from random import uniform
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list:
    """
    Spawn wait_random n times w/ specced max_delay-
    -and return list of all delays in asc order.
    """
    delays = []

    tasks = [wait_random(max_delay) for _ in range(n)]

    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)

    return delays
