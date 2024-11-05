#!/usr/bin/env python3
"""Function named task_wait_random."""

import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Create an asyncio.Task for wait_random and-
    -return task that wraps the wait_random coroutine.
    """
    return asyncio.create_task(wait_random(max_delay))