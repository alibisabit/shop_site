from collections.abc import Callable
from functools import reduce
from typing import TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def compose(*functions: Callable) -> Callable:
    """Объединяет функции: результат правой передаётся в левую."""
    if not functions:
        return lambda value: value

    return reduce(
        lambda combined, function: lambda value: combined(function(value)),
        functions,
    )


def pipe(value, *functions):
    """Последовательно передаёт значение через функции слева направо."""
    return reduce(
        lambda result, function: function(result),
        functions,
        value,
    )
