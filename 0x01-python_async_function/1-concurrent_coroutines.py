#!/usr/bin/env python3
""" an asynchronous coroutine  """
import asyncio
import random
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    an asynchronous coroutine

    Argument:
    n: integer
    max_delay: integer
    """
    x = [asyncio.create_task(wait_random(max_delay)) for i in range(n)]
    finish = [await task for task in asyncio.as_completed(x)]
    return finish
