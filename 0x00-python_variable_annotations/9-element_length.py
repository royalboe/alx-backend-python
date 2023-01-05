#!/usr/bin/env python3
""" Function that returns a list of tuples with duck-typed annotations """
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Function that returns a list of tuples generated from an iterable argument

    Argument:
    lst: iterable argument
    """
    return [(i, len(i)) for i in lst]
