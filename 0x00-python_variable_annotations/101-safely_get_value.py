#!/usr/bin/env python3
""" Function that returns an item of an input with duck-typed annotations """
from typing import Mapping, Any, Union, TypeVar


X = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[X, None]) -> Union[Any, X]:
    """
    Function that returns a value for a given key from a dictionary

    Arguments:
    dct: dictionary
    key: given key in dictionary
    default: default return value
    """
    if key in dct:
        return dct[key]
    else:
        return default
