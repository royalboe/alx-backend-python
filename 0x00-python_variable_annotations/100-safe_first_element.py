#!/usr/bin/env python3
""" Function that returns an item of an input with duck-typed annotations """
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Function that returns a the first element of an iterable argument

    Argument:
    lst: iterable argument with unknown elements
    """
    if lst:
        return lst[0]
    else:
        return None
