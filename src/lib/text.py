import re

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    """Привести текст к нормальной форме.

    Шаги нормализации:
      1. Регистр: ``casefold()``.
      2. Если ``yo2e=True`` — заменить ``ё``/``Ё`` на ``е``/``Е``.
      3. Заменить управляющие символы ``\\t``, ``\\r``, ``\\n`` на пробелы.
      4. «Схлопнуть» подряд идущие пробелы в один и обрезать края.
    """

    new_text = text
    # 1. Регистр
    if casefold:
        new_text = new_text.casefold()
    else: 
        new_text = new_text.lower()
    # 2. ё -> е
    if yo2e:
        new_text = new_text.replace('ё', 'е').replace('Ё', 'Е')
    # 3. Управляющие символы -> пробел
    for x in ("\t", "\r", "\n"):
        text = text.replace(x, " ")
    # 4. Схлопываем пробелы
    new_text = ' '.join(new_text.split())
    return new_text


def tokenize(text: str) -> list[str]:
    """Разбить текст на слова.

    Слово — это шаблон ``\\w+(?:-\\w+)*``: буквы/цифры/подчёркивание,
    при этом внутри слова допускается дефис. Всё остальное (пробелы,
    знаки препинания, эмодзи, длинное тире ``—``) — разделители.
    Числа считаются словами.
    """

    return [match.group() for match in re.finditer(r"\w+(?:-\w+)*", text)]



def count_freq(tokens: list[str]) -> dict[str, int]:
    """Подсчитать сколько раз каждое слово встречается в списке токенов.
    Возвращает словарь вида {слово: количество}.
    """
    freq = {}
    for token in tokens:
        # get(token, 0) возвращает текущий счётчик или 0 для нового слова.
        freq[token] = freq.get(token, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Вернуть N самых частых слов.

    Пары ``(слово, частота)`` сортируются по ключу ``(-частота, слово)``:
    сначала по убыванию частоты, а при равенстве частот — по алфавиту.
    """

    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]