#!/usr/bin/env python3
"""Async routine named measure_time."""

import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measure execution time for wait_n and-
    -return average time per call.
    """
    start_time = time.perf_counter()

    asyncio.run(wait_n(n, max_delay))

    end_time = time.perf_counter()
    total_time = end_time - start_time

    return total_time / n
