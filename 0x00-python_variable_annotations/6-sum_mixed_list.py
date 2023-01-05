#!/usr/bin/env python3
"""
    type-annotated function sum_mixed_list which takes a list
    mxd_lst of integers and floats and returns their sum as a float.
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    takes a list mxd_lst of integers and floats
    and returns their sum as a float.

    Arguments:
    mxd_lst: list of floats and/or integers

    """
    return float(sum(mxd_lst))
