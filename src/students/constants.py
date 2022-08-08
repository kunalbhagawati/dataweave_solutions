"""
Runtime constant types.
"""
import enum


class Subject(str, enum.Enum):
    physics = 'physics'
    chemistry = 'chemistry'
    maths = 'maths'
    english = 'english'


class ExamType(str, enum.Enum):
    theory = 'theory'
    practical = 'practical'
