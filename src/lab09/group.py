import csv
from pathlib import Path

from src.lab08.models import STUDENT_FIELDS, student_from_dict, student_to_dict, validate_student

HEADER = STUDENT_FIELDS


def ensure_storage(path):
    """Создаёт каталоги и файл с одной строкой-заголовком, если файла ещё нет"""
    path = Path(path)
    if not path.exists():
        save_students(path, [])


def _gpa_to_float(value):
    """Из CSV gpa приходит строкой - приводим к float в одном месте"""
    if value is None or value.strip() == "":
        raise ValueError("поле gpa: пустое значение")
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"поле gpa: '{value}' не является числом")


def load_students(path):
    """Читает все записи из CSV. Каждая строка проходит через student_from_dict."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")

    students = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("в CSV нет строки-заголовка")
        if set(reader.fieldnames) != set(HEADER):
            raise ValueError(
                f"неверный заголовок CSV: {reader.fieldnames}, ожидается {list(HEADER)}"
            )
        for number, row in enumerate(reader, start=2):  # строка 1 - заголовок
            if None in row:
                raise ValueError(f"строка {number}: лишние колонки")
            try:
                row["gpa"] = _gpa_to_float(row["gpa"])
                students.append(student_from_dict(row))
            except ValueError as e:
                raise ValueError(f"строка {number}: {e}")
    return students


def save_students(path, students):
    """Перезаписывает файл целиком."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(students)


def add_student(path, student):
    """Валидирует запись и дописывает её в конец."""
    validate_student(student)
    students = load_students(path)
    students.append(student_to_dict(student))
    save_students(path, students)


def list_students(path, sort_by=None):
    """Все студенты; sort_by: None, "fio" или "gpa" (по возрастанию)."""
    students = load_students(path)
    if sort_by is None:
        return students
    if sort_by not in ("fio", "gpa"):
        raise ValueError(f"неизвестное поле сортировки: {sort_by}")
    return sorted(students, key=lambda s: s[sort_by])


def find_students(path, substr):
    """Записи, у которых substr входит в ФИО (без учёта регистра)."""
    students = load_students(path)
    needle = substr.casefold()
    return [s for s in students if needle in s["fio"].casefold()]


def remove_student(path, fio):
    """Удаляет все записи с таким ФИО, возвращает их количество."""
    students = load_students(path)
    kept = [s for s in students if s["fio"] != fio]
    removed = len(students) - len(kept)
    if removed > 0:
        save_students(path, kept)
    return removed


def update_student(path, fio, **fields):
    """Обновляет поля первой записи с таким ФИО. True, если запись найдена."""
    for key in fields:
        if key not in HEADER:
            raise KeyError(f"неизвестное поле: {key}")
    students = load_students(path)
    for i in range(len(students)):
        if students[i]["fio"] == fio:
            new_rec = dict(students[i])
            new_rec.update(fields)
            students[i] = student_from_dict(new_rec)  # проверка результата
            save_students(path, students)
            return True
    return False