from src.students.db.connection import connection


def _add_extensions():
    connection.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')


def _create_enums():
    """Creates the enums required by the rest of the DB."""

    connection.execute("""
        CREATE TYPE subject as ENUM('physics', 'chemistry', 'maths', 'english')
    """)

    connection.execute("""
        CREATE TYPE exam_type as ENUM('theory', 'practical')
    """)


def _create_table():
    connection.execute("""
create table if not exists student_marks
(
    id           int primary key generated always as identity,
    student_id   uuid      not null,
    subject      subject   not null,
    exam_type exam_type not null,
    marks        integer   not null,
    constraint marks_in_range
        check (marks BETWEEN 0 AND 100),
    unique (student_id, subject, exam_type)
)
    """)


def setup_db():
    """
    Gets the DB ready for use:
    - Sets up the enums
    - Sets up the tables
    """

    _add_extensions()
    _create_enums()  # Choosing an enum here since a FK table will be overkill for this demo.
    _create_table()
    connection.commit()
    register_enums()
