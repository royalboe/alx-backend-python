#!/usr/bin/env python3
"""  coroutine that will execute async_comprehension four times """
import asyncio
import time
from typing import Generator
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ coroutine that will execute async_comprehension
    four times in parallel using asyncio.gather
    """
    start = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for i in range(4)))
    return(time.perf_counter() - start)
