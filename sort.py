#! /usr/bin/env python
from typing import List

import typer

from src.number_sorter import sort


def main(numbers: List[int],
         start_place_value_exp: int = typer.Option(..., "--start-digit", "-s"),
         end_place_value_exp: int = typer.Option(..., "--end-digit", "-e")):
    res = sort(numbers, start_place_value_exp - 1, end_place_value_exp - 1)
    print("---------------------")
    print(f"Sorted List: {res}")


if __name__ == '__main__':
    typer.run(main)
