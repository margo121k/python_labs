from pathlib import Path
import json
import csv

from src.lab04.io_txt_csv import ensure_parent_dir, read_text, write_csv

def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV.
    Поддерживает список словарей [{...}, {...}], заполняет отсутствующие поля пустыми строками.
    Кодировка UTF-8. Порядок колонок — как в первом объекте.
    """
    json_file = Path(json_path)
    csv_file = Path(csv_path)
    if json_file.suffix.lower() != ".json":
        raise ValueError(f"Неверный формат входного файла: ожидается .json")
    if csv_file.suffix.lower() != ".csv":
        raise ValueError(f"Неверный формат выходного файла: ожидается .csv")
    if not json_file.exists():
        raise FileNotFoundError("Файл не найден")

     # читаем файл функцией из ЛР4
    text = read_text(json_path)

    if text.strip() == "":
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    # превращаем текст в python-объект (список словарей)
    data = json.loads(text)
    
    if not isinstance(data, list) or not all(isinstance(value, dict) for value in data):
        raise ValueError("Ожидается список словарей")
    if not data:
        raise ValueError("Пустой JSON-файл")
    
    header = list(data[0].keys())
    if len(header) == 0:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    # превращаем каждый словарь в строку-список значений
    rows = []
    for item in data:
        row = []
        for column in header:
            row.append(item.get(column, ""))  # нет ключа -> пустая строка
        rows.append(row)

    # записываем функцией из ЛР4
    write_csv(rows, csv_path, header=tuple(header))


def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV в JSON (список словарей).
    Заголовок обязателен, значения сохраняются как строки.
    """
    csv_file = Path(csv_path)
    json_file = Path(json_path)
    ensure_parent_dir(json_file)
    if json_file.suffix.lower() != ".json":
        raise ValueError(f"Неверный формат выходного файла: ожидается .json")
    if csv_file.suffix.lower() != ".csv":
        raise ValueError(f"Неверный формат входного файла: ожидается .csv")
    if not csv_file.exists():
        raise FileNotFoundError("Файл не найден")
    with csv_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV не содержит заголовок")
        data = [row for row in reader]
    if not data:
        raise ValueError("Пустой CSV")
        
    with json_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# json_to_csv("data/samples/people.json", "data/out/people.csv")
# csv_to_json("data/samples/people.csv", "data/out/people.json")

# csv_to_json("data/samples/cities.csv", "data/out/cities.json")

# # ValueError - пустой json файл
# json_to_csv("data/samples/empty.json", "data/out/empty.csv")

# # ValueError - неподдерживаемая структура
# json_to_csv("data/samples/broken.json", "data/out/broken.csv")
