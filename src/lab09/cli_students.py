import argparse
import sys

from src.lab08.models import make_student, format_student
from src.lab09.group import ensure_storage, add_student, list_students, find_students, remove_student, update_student

DEFAULT_DB = "data/lab09/students.csv"


def fail(message):
    """Печатает ошибку в stderr и завершает программу с кодом 1."""
    print(f"Ошибка: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    # общий параметр --db для всех подкоманд
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", default=DEFAULT_DB, help=f"путь к CSV-хранилищу (по умолчанию {DEFAULT_DB})")

    parser = argparse.ArgumentParser(description="CLI для хранилища студентов (CSV)")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("add", parents=[common], help="Добавить студента")
    p.add_argument("--fio", required=True)
    p.add_argument("--birthdate", required=True, help="YYYY-MM-DD")
    p.add_argument("--group", required=True)
    p.add_argument("--gpa", type=float, required=True, help="от 0 до 5")

    p = sub.add_parser("list", parents=[common], help="Вывести всех студентов")
    p.add_argument("--sort", choices=["fio", "gpa"], help="сортировка")

    p = sub.add_parser("find", parents=[common], help="Поиск по подстроке в ФИО")
    p.add_argument("--q", required=True, help="подстрока (без учёта регистра)")

    p = sub.add_parser("remove", parents=[common], help="Удалить студента по ФИО")
    p.add_argument("--fio", required=True)

    p = sub.add_parser("update", parents=[common], help="Обновить поля студента")
    p.add_argument("--fio", required=True)
    p.add_argument("--gpa", type=float)
    p.add_argument("--group")
    p.add_argument("--birthdate")

    args = parser.parse_args()
    if args.cmd is None:
        parser.error("нужно указать подкоманду: add, list, find, remove или update")

    try:
        ensure_storage(args.db)

        if args.cmd == "add":
            student = make_student(args.fio, args.birthdate, args.group, args.gpa)
            add_student(args.db, student)
            print(f"Добавлен: {format_student(student)}")

        elif args.cmd == "list":
            students = list_students(args.db, args.sort)
            if not students:
                print("Студентов нет")
            for s in students:
                print(format_student(s))

        elif args.cmd == "find":
            students = find_students(args.db, args.q)
            if not students:
                print("Ничего не найдено")
            for s in students:
                print(format_student(s))

        elif args.cmd == "remove":
            print(f"Удалено записей: {remove_student(args.db, args.fio)}")

        elif args.cmd == "update":
            fields = {}
            if args.gpa is not None:
                fields["gpa"] = args.gpa
            if args.group is not None:
                fields["group"] = args.group
            if args.birthdate is not None:
                fields["birthdate"] = args.birthdate
            if not fields:
                parser.error("укажите хотя бы одно поле для обновления: --gpa, --group или --birthdate")
            if update_student(args.db, args.fio, **fields):
                print(f"Обновлено: {args.fio}")
            else:
                fail(f"студент не найден: {args.fio}")

    except KeyError as e:
        fail(e.args[0])
    except (ValueError, FileNotFoundError) as e:
        fail(e)


if __name__ == "__main__":
    main()