#!/usr/bin/env python3
"""  a coroutine called async_comprehension that takes no arguments. """
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """ coroutine will loop 10 times, each time asynchronously wait 1 second,
    then yield a random number between 0 and 10
    """
    return([i async for i in async_generator()])
