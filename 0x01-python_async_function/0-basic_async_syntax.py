#!/usr/bin/env python3
"""Asynchronous routine named wait_random."""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Waits for random delay btw 0 & max_delay seconds-
    -and returns float (actual delay time waited).
    """
    delay = random.uniform(0,  max_delay)
    await asyncio.sleep(delay)
    return delay
