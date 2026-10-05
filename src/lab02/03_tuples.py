def format_record(rec: tuple[str, str, float]) -> str:
    """
    Форматирует кортеж с данными студента в строку.
    
    :rec: Кортеж вида (fio, group, gpa)
    :raise TypeError: Если типы элементов кортежа не соответствуют (str, str, float/int).
    :raise ValueError: Если ФИО или группа пустые после очистки, или GPA вне диапазона [0.0, 5.0].
    :return: Сформированная строка по шаблону.
    """
    if not isinstance(rec, tuple) or len(rec) != 3:
        raise TypeError("Запись должна быть кортежем из 3 элементов")
    fio, group, gpa = rec
    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError('ФИО и группа должны быть строками')
    if not isinstance(gpa, (int, float)):
        raise TypeError("GPA должен быть числом")

    fio = fio.split() 
    fio_clean = " ".join(fio)
    if fio_clean == "":
        raise ValueError("ФИО не может быть пустой строкой")
    if group == "":
        raise ValueError("Группа не может быть пустой строкой")
    if not (0.0 <= gpa <= 5.0):
        raise ValueError("GPA должен быть в диапазоне от 0.0 до 5.0")
    
    fio1 = fio[0][0].upper() + fio[0][1:] + " "
    for i in range(len(fio)):
        if i!=0:
            fio1 += fio[i][0].upper() + '.'
    return f"{fio1}, гр. {group.strip()}, GPA {gpa:.2f}"

print(format_record(("Иванов Андрей Иванович", "BIVT-25", 4.6)))
print(format_record(("Петров Евгений", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))
try:
    print(format_record(("  ", 'IKBO-12', 4)))
except ValueError as e:
    print(f'ValueError: {e}')
try:
    print(format_record(("Иванов Иван Иванович", 6, 2.99)))
except TypeError as e:
    print(f'TypeError: {e}')
try:
    print(format_record(("Иванов Иван Иванович", 'BIVT-25', -2)))
except ValueError as e:
    print(f'ValueError: {e}')