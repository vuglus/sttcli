import sys
import os
import yaml
import datetime
from yandex_summarize import summarize  # импорт твоей функции summarize

def main():
    if len(sys.argv) < 2:
        print("Использование: python summarize_file.py <имя_файла>")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Файл не найден: {input_path}")
        sys.exit(1)

    # Загружаем конфиг
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Получаем метаданные файла
    file_name = os.path.basename(input_path)
    created_ts = os.path.getctime(input_path)
    created_date = datetime.datetime.fromtimestamp(created_ts).strftime("%Y-%m-%d %H:%M:%S")

    # Читаем исходный текст
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Добавляем имя и дату создания файла в начало текста
    meta_info = f"Файл: {file_name}\nДата создания: {created_date}\n\n"
    text_with_meta = meta_info + text

    print("→ Генерирую саммари...")
    summary = summarize(config, text_with_meta)

    # Генерируем имя выходного файла
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_summary.txt"

    # Сохраняем результат
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✅ Саммари сохранено в {output_path}")

if __name__ == "__main__":
    main()
