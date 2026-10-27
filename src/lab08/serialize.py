import json
from pathlib import Path

from src.lab08.models import *


def students_to_json(students, path):
    """Сохраняет список записей в JSON (массив объектов)."""
    data = [student_to_dict(s) for s in students]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def students_from_json(path):
    """Читает JSON-массив и возвращает список валидных записей.

    Политика: skip - битые записи пропускаются, в конце печатается,
    сколько пропущено и почему.
    """
    if not Path(path).is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("ожидается JSON-массив записей")

    students = []
    errors = []
    for number, item in enumerate(data, start=1):
        try:
            students.append(student_from_dict(item))
        except ValueError as e:
            errors.append(f"запись #{number}: {e}")

    if errors:
        print(f"Пропущено записей: {len(errors)}")
        for message in errors:
            print(f"  - {message}")
    return students


def main():
    # корректные записи туда-обратно
    students = students_from_json("data/lab08/students_input.json")
    for s in students:
        print(format_student(s))
    students_to_json(students, "data/lab08/students_output.json")
    print("Записано:", len(students), "записей в students_output.json")


    # файл с битыми записями
    good = students_from_json("data/lab08/students_bad.json")
    print("Прочитано валидных:", len(good))


if __name__ == "__main__":
    main()
