import csv
from pathlib import Path
from typing import Iterable, Sequence

def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Прочитать файл целиком как одну строку.

    Кодировка по умолчанию — UTF-8. Если файл в другой кодировке
    (например, Windows-1251), передайте её явно::

        read_text("data/input.txt", encoding="cp1251")

    Исключения FileNotFoundError и UnicodeDecodeError не подавляются
    Файл читается целиком. Для очень больших файлов
    в реальных проектах стоит читать построчно.
    """
    p = Path(path)
    return p.read_text(encoding=encoding)

def write_csv(rows: Iterable[Sequence], path: str | Path, header: tuple[str, ...] | None = None) -> None:
    """Записать строки в CSV (разделитель ','). Перезаписывает файл.

    Если передан header — он записывается первой строкой.
    Все строки должны иметь одинаковую длину, иначе ValueError.
    """
    rows = list(rows)

    # Проверка одинаковой длины всех строк (включая header, если он задан)
    lengths = {len(r) for r in rows}
    if header is not None:
        lengths.add(len(header))
    if len(lengths) > 1:
        raise ValueError("Все строки должны иметь одинаковую длину")

    ensure_parent_dir(path)
    p = Path(path)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header is not None:
            w.writerow(header)
        for r in rows:
            w.writerow(r)

