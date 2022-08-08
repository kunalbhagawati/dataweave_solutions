import functools
import logging
from functools import cmp_to_key
from typing import Iterable, List

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")


def to_discrete_values(fn):
    """Converts the return value of fn to -1, 0, or 1."""

    @functools.wraps(fn)
    def inner(*args, **kwargs):
        val = fn(*args, **kwargs)
        if val < 0:
            return -1
        elif val == 0:
            return 0
        else:
            return 1

    return inner


@to_discrete_values
def place_value_comparator(num1: int, num2: int, start_place_value_exp: int, end_place_value_exp: int) -> int:
    """
    Compares num1 with num2 by comparing them from their start place values to end place values.
    :param start_place_value_exp: Power of 10 i.e. digit place where to start comparing. STARTS AT 0!
    :param end_place_value_exp: Power of 10 i.e. digit place where to end comparing. STARTS AT 0!
    :return: 1 if num1 > num2, 0 if num1 == num2, -1 if num1 < num2

    >>> place_value_comparator(2, 1, start_place_value_exp=1, end_place_value_exp=0)
    1

    >>> place_value_comparator(22, 13, start_place_value_exp=0, end_place_value_exp=0)
    -1

    >>> place_value_comparator(1221, 2112, start_place_value_exp=2, end_place_value_exp=1)
    1

    >>> place_value_comparator(1201, 2222, start_place_value_exp=2, end_place_value_exp=1)
    -1

    >>> place_value_comparator(1221, 2222, start_place_value_exp=2, end_place_value_exp=1)
    0

    >>> place_value_comparator(20, 10, start_place_value_exp=3, end_place_value_exp=3)
    0
    """
    # Invariants.
    # Ideally we would want to do this in compilation if the language supports refinement types.
    assert start_place_value_exp >= 0
    assert end_place_value_exp >= 0
    assert start_place_value_exp >= end_place_value_exp
    # ---

    logging.debug(f"Comparing | num1: {num1}  num2: {num2}")
    current_place_value = start_place_value_exp

    def _compare(exp):
        divisor = 10 ** exp
        num1_cmpr_digit = num1 // divisor % 10
        num2_cmpr_digit = num2 // divisor % 10
        logging.info(
            f"\tDiff | divisor: {divisor}  num1_cmpr_digit: {num1_cmpr_digit}  num2_cmpr_digit: {num2_cmpr_digit}")
        return num1_cmpr_digit - num2_cmpr_digit

    while current_place_value >= end_place_value_exp:
        if (res := _compare(current_place_value)) != 0:
            return res
        current_place_value -= 1

    return 0  # All iterations equal


def sort(numbers: Iterable[int], start_place_value_exp: int, end_place_value_exp: int) -> List[int]:
    """
    Given an iterable of numbers, sort using the place value comparator.
    If the comparator does not apply to any number, leaves it as it is.
    :param start_place_value_exp: Power of 10 i.e. digit place where to start comparing. STARTS AT 0!
    :param end_place_value_exp: Power of 10 i.e. digit place where to end comparing. STARTS AT 0!

    >>> sort([1, 2, 3], start_place_value_exp=1, end_place_value_exp=0)
    [1, 2, 3]

    >>> sort([1190, 1111, 1110, 2450, 1450, 1350, 1200, 1220, 1300, 2950], start_place_value_exp=2, end_place_value_exp=1)
    [1111, 1110, 1190, 1200, 1220, 1300, 1350, 2450, 1450, 2950]
    """

    partial = functools.partial(place_value_comparator,
                                start_place_value_exp=start_place_value_exp,
                                end_place_value_exp=end_place_value_exp)

    return sorted(numbers, key=cmp_to_key(partial))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    logger.setLevel(logging.INFO)
