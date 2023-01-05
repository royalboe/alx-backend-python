#!/usr/bin/env python3
""" Function that returns a sublist of a given range from a tuple """
from typing import List, Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    Function that returns a sublist of a given range

    Arguments:
    lst: tuple
    factor: integer
    """

    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
