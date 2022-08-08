# Solutions for the end of discussion questions - Dataweave / Mohan GS

Requirements:

- Python 3.x
- Docker

## Setup
- If you wish to use virtualenv:
```shell
cd <to_here>
python3 -m venv .venv  # set up the virtual environment
```

## Number sorting

Given an iterable of numbers, sort them by comparing the sub number between any given two decimal places.
e.g. If the number is `12345`, and the decimal places are `[2, 3]`, the sub-number will be `34`.

So<br>
`[1190, 1111, 1110, 2450, 1450, 1350, 1200, 1220, 1300, 2950]`<br>
with sorting for 10th and 100th digits<br>
will be sorted as<br>
`[1111, 1110, 1190, 1200, 1220, 1300, 1350, 2450, 1450, 2950]`

```shell
# This is already done,, but in case of issues.
chmod +x sort.py

# ---
./sort.py --help
./sort.py 1111 1110 1190 1200 1220 1300 1350 2450 1450 2950 -s 3 -e 2
# Note the start and end digits count from `1`, but in the code, they count from `0` (since we do 10 ** exponent).
```
