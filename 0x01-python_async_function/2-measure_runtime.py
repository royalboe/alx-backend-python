#!/usr/bin/env python3
""" an asynchronous coroutine  """
import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    measures the total execution time

    Argument:
    n: integer
    max_delay: integer
    """
    first = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    finish = time.perf_counter()
    total_time = finish - first
    return total_time / n
