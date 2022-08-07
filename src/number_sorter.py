import functools
from functools import cmp_to_key
from typing import Iterable

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")


def place_value_comparator(num1: int, num2: int, start_place_value_exp: int = 0, end_place_value_exp: int = 0) -> int:
    """
    Compares num1 with num2 by comparing them from their start place values to end place values.
    :param start_place_value_exp: Power of 10 i.e. digit place where to start comparing.
    :param end_place_value_exp: Power of 10 i.e. digit place where to end comparing.
    :return: negative number if num1 < num2, 0 if num1 == num2, positive number if num1 > num2
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
            logging.info(f"\tres: {res}")
            return res
        current_place_value -= 1

    return 0  # All iterations equal


def main(iter: Iterable[int]):
    """
    Given an iterable of numbers, sort using the place value comparator.
    If the comparator does not apply to any number, leaves it as it is.
    """

    partial = functools.partial(place_value_comparator, start_place_value_exp=2, end_place_value_exp=1)

    return sorted(iter, key=cmp_to_key(partial))


if __name__ == '__main__':
    iter = [1190, 1111, 1110, 2450, 1450, 1350, 1200, 1220, 1300, 2950]
    iter_sorted = main(iter)
    print(iter_sorted)
