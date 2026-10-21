from src.lib.text import normalize, tokenize, count_freq, top_n
from src.lab04.io_txt_csv import read_text, write_csv

def main():
    try:
        raw_text = read_text("data/lab04/input.txt", encoding="utf-8")
    except FileNotFoundError:
        print("Ошибка: файл не найден")
        return

    tokens = tokenize(normalize(raw_text))
    freq = count_freq(tokens)
    total_words = len(tokens)
    unique_words = len(freq)

    all_rows = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    top5 = top_n(freq, n=5)

    write_csv(all_rows, "data/lab04/report.csv", header=("word", "count"))

    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5:")
    for word, count in top5:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()