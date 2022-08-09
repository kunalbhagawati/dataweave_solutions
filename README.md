# Solutions for the end of discussion questions - Dataweave / Mohan GS

Requirements:

- Python 3.9+
- Docker

## Setup
- If you wish to use virtualenv:
```shell
cd <to_here>
python3 -m venv .venv  # set up the virtual environment

chmod +x scripts/* # [Optional] In case of issues. Give execute permission to scripts.
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
# ---
scripts/sort --help
scripts/sort 1111 1110 1190 1200 1220 1300 1350 2450 1450 2950 -s 3 -e 2
# Note the start and end digits count from `1`, but in the code, they count from `0` (since we do 10 ** exponent).
```

# Student marks
Given a number of students and their marks, get the top 3 students ordered by their total marks (1st Level).<br>
In case of collisions, order by theory first (2nd Level).<br>
In case of further collisions, sort alphabetically (3rd Level).

```shell
# Run docker-compose to spin up the DB container and volume
docker-compose up -d

# Setup the DB with the tables.
scripts/db setup

# [Optional] Seed the DB
scripts/db seed

# Run the script
scripts/marks-analysis # Add -n optionally to specify number of students.

# To reset the data and the containers
docker-compose down -v
```

### Attempting to solve this using SQL:
Could only solve the first level of sorting. Efforts underway to solve the 2nd and 3rd level.

```postgresql
select r, student_id, total_marks
from (select dense_rank() over (order by sum(marks) desc) as r, student_id, sum(marks) as total_marks
      from student_marks
      group by student_id) sq
where sq.r <= 3;
```
