#!/usr/bin/env python3
""" an asynchronous coroutine  """
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    an asynchronous coroutine

    Argument:
    max_delay: integer
    """
    i = random.uniform(0, max_delay)
    await asyncio.sleep(i)
    return(i)
