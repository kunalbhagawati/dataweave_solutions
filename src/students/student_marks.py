import functools
from dataclasses import dataclass
from typing import Iterable, Any, Sequence, List
from uuid import UUID

from psycopg.rows import RowMaker

from src.students.constants import Subject, ExamType
from src.students.db.connection import connection


@dataclass
class _Row:
    id: int
    student_id: UUID
    subject: Subject
    exam_type: ExamType
    marks: int


@dataclass
class StudentMarks:
    student_id: UUID
    total: int
    total_theory: int
    total_practical: int


def _row_factory(_) -> RowMaker[_Row]:
    def make_row(values: Sequence[Any]) -> _Row:
        return _Row(
            id=values[0],
            student_id=values[1],
            subject=Subject(values[2]),
            exam_type=ExamType(values[3]),
            marks=values[4]
        )

    return make_row


def get_rows() -> Iterable[_Row]:
    with connection.cursor(row_factory=_row_factory) as c:
        c.execute("""SELECT id, student_id, subject, exam_type, marks FROM student_marks""")
        return c.fetchall()


def group_student_marks(rows: Iterable[_Row]) -> dict:
    student_details = {}
    for r in rows:
        if r.student_id not in student_details:
            student_details[r.student_id] = {'total': 0, ExamType.theory: 0, ExamType.practical: 0}
        student_details[r.student_id]['total'] += r.marks
        student_details[r.student_id][r.exam_type] += r.marks
    return student_details


def _get_sorted_student_marks(student_marks: Iterable[StudentMarks]) -> List[StudentMarks]:
    # TODO Move this to the dataclass internal comparison functions
    def comparator(a: StudentMarks, b: StudentMarks):
        """
        Reverse compares the 2 values:
          If a < b returns 1
          If a > b return -1
          Else return 0
        This is the opposite of a conventional ascending sorting behaviour,
        and it makes the sorting itself act in a reversed way.

        This is because:
        - we want a custom sorting function. This is NOT meant to be used in a generic manner.
        - we want the 3rd level sorting (if it reaches there) to be alphabetical.
        """
        # Compare using total
        if a.total != b.total:
            return -1 if a.total > b.total else 1

        # Compare using the theory marks
        if a.total_theory != b.total_theory:
            return -1 if a.total_theory > b.total_theory else 1

        if a.student_id > b.student_id:
            return 1
        elif a.student_id == b.student_id:
            return 0
        else:
            return -1

    # NOTE This is a very custom sorting, with a very custom comparator.
    #  Reverse sorting this will break final alphabetically ascending sort order.
    return sorted(student_marks, key=functools.cmp_to_key(comparator))


def get_top_n_highest_scorers(n=3):
    """
    Find the highest scorers in the DB as a sum of total marks.
    """

    grouped = group_student_marks(get_rows())
    return _get_sorted_student_marks(
        [StudentMarks(student_id=student_id,
                      total=marks_breakup['total'],
                      total_theory=marks_breakup[ExamType.theory],
                      total_practical=marks_breakup[ExamType.practical])
         for student_id, marks_breakup in grouped.items()]
    )[:n]
