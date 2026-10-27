from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def _check_text(value, name):
    """fio и group: строка, после strip() не пустая. Возвращает очищенную строку."""
    if not isinstance(value, str):
        raise ValueError(f"поле {name}: ожидается строка")
    value = value.strip()
    if value == "":
        raise ValueError(f"поле {name}: строка не должна быть пустой")
    return value


def _check_birthdate(value):
    """birthdate: строка YYYY-MM-DD, существующая дата, не в будущем."""
    if not isinstance(value, str):
        raise ValueError("поле birthdate: ожидается строка формата YYYY-MM-DD")
    try:
        d = date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"поле birthdate: '{value}' не является датой формата YYYY-MM-DD")
    if d > date.today():
        raise ValueError(f"поле birthdate: дата '{value}' в будущем")
    return value


def _check_gpa(value):
    """gpa: int или float, 0 <= gpa <= 5. Возвращает float."""
    if not isinstance(value, (int, float)):
        raise ValueError("поле gpa: ожидается число (int или float)")
    if not (0 <= value <= 5):
        raise ValueError(f"поле gpa: значение {value} вне диапазона 0..5")
    return float(value)


def make_student(fio, birthdate, group, gpa):
    """Собирает запись студента, проверяя каждое поле.

    make_student("Иванов Иван Иванович", "2007-05-14", "БИВТ-26-6-1", 4.3)
    """
    return {
        "fio": _check_text(fio, "fio"),
        "birthdate": _check_birthdate(birthdate),
        "group": _check_text(group, "group"),
        "gpa": _check_gpa(gpa),
    }


def validate_student(rec):
    """Проверяет готовую запись: набор ключей и значения. При ошибке - ValueError."""
    if not isinstance(rec, dict):
        raise ValueError("запись должна быть словарём")
    if set(rec) != set(STUDENT_FIELDS):
        missing = set(STUDENT_FIELDS) - set(rec)
        extra = set(rec) - set(STUDENT_FIELDS)
        raise ValueError(f"неверный набор ключей: нет {sorted(missing)}, лишние {sorted(extra)}")
    _check_text(rec["fio"], "fio")
    _check_birthdate(rec["birthdate"])
    _check_text(rec["group"], "group")
    _check_gpa(rec["gpa"])


def student_age(rec, today=None):
    """Полных лет на дату (по умолчанию сегодня)."""
    b = date.fromisoformat(rec["birthdate"])
    today = today or date.today()
    age = today.year - b.year
    if (today.month, today.day) < (b.month, b.day):  # день рождения ещё не был
        age -= 1
    return age


def _years_word(n):
    """Правильная форма слова: 1 год, 2 года, 5 лет."""
    if 11 <= n % 100 <= 14:
        return "лет"
    if n % 10 == 1:
        return "год"
    if 2 <= n % 10 <= 4:
        return "года"
    return "лет"


def format_student(rec):
    """Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30"""
    parts = rec["fio"].split()
    initials = "".join(p[0].upper() + "." for p in parts[1:3])
    name = parts[0] + (" " + initials if initials else "")
    age = student_age(rec)
    return f"{name} ({rec['group']}), {age} {_years_word(age)}, GPA {rec['gpa']:.2f}"


def student_to_dict(rec):
    """Копия записи (не тот же самый словарь) для сериализации."""
    validate_student(rec)
    return {key: rec[key] for key in STUDENT_FIELDS}


def student_from_dict(d):
    """Десериализация: берёт ровно нужные ключи, gpa приводит к float, валидирует."""
    if not isinstance(d, dict):
        raise ValueError("запись должна быть объектом (словарём)")
    for key in STUDENT_FIELDS:
        if key not in d:
            raise ValueError(f"нет поля {key}")
    return make_student(d["fio"], d["birthdate"], d["group"], d["gpa"])


def main():
    s = make_student("Сидоров Пётр Олегович", "2007-09-20", "БИВТ-26-6-1", 4)
    print("Создан студент:", s)

    # 1. форматирование
    print("Форматирование:", format_student(s))

    # 2. возраст до и после дня рождения
    print(student_age(s, date(2026, 9, 19)), student_age(s, date(2026, 9, 20)))

    # 3. неверная дата и gpa = 7
    for args in (("Иванов Иван Иванович", "2003-02-30", "БИВТ-26-6-1", 4.0),
                 ("Иванов Иван Иванович", "2007-05-14", "БИВТ-26-6-1", 7)):
        try:
            make_student(*args)
        except ValueError as e:
            print("ValueError:", e)

if __name__ == "__main__":
    main()