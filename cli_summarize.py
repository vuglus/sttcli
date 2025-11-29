import sys
import os
import yaml
import datetime
from instruction.choose import choose_instruction
from files.tmp import save_local  
from files.context import load_context_for, draw_context
from models import get_model

def main():
    input_path, instruction, output_file = parse_args(sys.argv)

    base, ext = os.path.splitext(input_path)
    # Загружаем конфиг
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    ModelClass = get_model(config['model_name'])
    if not ModelClass:
        print(f"❌ No model for: {config['model_name']}")
        return
    summarizer = ModelClass(config)

    # Выбираем инструкцию
    if len(sys.argv) >= 3:
        instruction = sys.argv[2]
    else:
        instruction = choose_instruction(config)

    # Получаем контекст
    context = load_context_for(input_path)

    # Отображаем контекст
    if context != "":
        draw_context(context)

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

    print(f"→ Генерирую саммари с инструкцией '{instruction}'...")
    summary = summarizer.summarize(text_with_meta, instruction_type = instruction, context = context)

    if output_file == "": 
        output_file = base + f".{instruction}.md" 

    # Сохраняем результат
    save_local(output_file, summary)

if __name__ == "__main__":
    main()

def parse_args(argv):
    """
    Разбирает аргументы командной строки и возвращает:
    - input_path: путь к входному файлу
    - instruction: тип инструкции (или None)
    - output_file: путь к файлу вывода (или None)
    """
    if len(argv) < 2:
        print("Использование: python summarize_file.py <файл> [инструкция] [--output файл]")
        sys.exit(1)

    input_path = argv[1]
    instruction = None
    output_file = None

    args = argv[2:]

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--output":
            if i + 1 < len(args):
                output_file = args[i + 1]
                i += 2
                continue
            else:
                print("❌ Ошибка: после --output должен быть указан файл")
                sys.exit(1)

        # Если это не флаг, и инструкция ещё не выбрана
        if instruction is None and not arg.startswith("--"):
            instruction = arg

        i += 1

    if not os.path.exists(input_path):
        print(f"Файл не найден: {input_path}")
        sys.exit(1)

    return input_path, instruction, output_file    