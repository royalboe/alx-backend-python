#!/usr/bin/env python3
"""
    type-annotated function make_multiplier that takes a float multiplier
    as argument and returns a function that multiplies a float by multiplier
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    takes a float multiplier as argument
    and returns a function that multiplies a float by multiplier

    Argument:
    multiplier: float

    """
    def multiply(n: float) -> float:
        """ function that multiplies a float by multiplier.

        Argument:
        n: float
        """
        return n * multiplier

    return multiply
